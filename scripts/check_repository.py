"""Check provenance, case tracking and obvious accidental local-data inclusion."""
import ast
import csv
import hashlib
import json
import re
import subprocess
from pathlib import Path

if __package__:
    from .start_work import validate_handoff
else:
    from start_work import validate_handoff

ROOT = Path(__file__).resolve().parent.parent


def source_files():
    if (ROOT / ".git").is_dir():
        result = subprocess.run(["git", "ls-files", "--cached", "--others", "--exclude-standard", "-z"],
                                cwd=ROOT, check=True, capture_output=True)
        return sorted({ROOT / p.decode() for p in result.stdout.split(b"\0") if p})
    ignored = {".git", ".venv", "__pycache__", "var", "output", "node_modules"}
    return sorted(p for p in ROOT.rglob("*") if p.is_file() and not any(x in ignored for x in p.relative_to(ROOT).parts))


def check():
    failures = []
    manifest = json.loads((ROOT / "docs/source-manifest.json").read_text(encoding="utf-8"))
    for source in manifest["sources"]:
        path = ROOT / source["excerpt_file"]
        if hashlib.sha256(path.read_bytes()).hexdigest() != source["excerpt_sha256"]:
            failures.append("Reference excerpt changed without updated provenance: " + source["excerpt_file"])
        if source.get("reference_pdf"):
            pdf = ROOT / source["reference_pdf"]
            if not pdf.is_file() or hashlib.sha256(pdf.read_bytes()).hexdigest() != source["reference_pdf_sha256"]:
                failures.append("Reference PDF differs from its declared reference hash: " + source["reference_pdf"])
    failures.extend(validate_handoff(ROOT))
    expected = {f"{prefix}-T-{number:02d}" for prefix, count in [("BA", 7), ("CS", 7), ("MC", 7), ("AP", 8), ("CO", 8), ("GR", 4)] for number in range(1, count + 1)}
    with (ROOT / "docs/traceability.csv").open(newline="") as stream:
        rows = list(csv.DictReader(stream))
    if len(rows) != 41 or {row["case_id"] for row in rows} != expected:
        failures.append("Traceability must retain exactly the 41 original case IDs.")
    tests = "\n".join(p.read_text(encoding="utf-8") for p in (ROOT / "tests").glob("test_*.py"))
    for row in rows:
        for prefix in row["automated_test_prefixes"].split(";"):
            if prefix and prefix not in tests:
                failures.append("Unverified test mapping: " + prefix)
        if row["implementation_status"] not in {"NOT_STARTED", "PARTIAL", "PASSED", "FAILED"}:
            failures.append("Unknown traceability status: " + row["case_id"])
        if row["implementation_status"] == "PARTIAL" and not row["remaining_scope"]:
            failures.append("Partial case needs a stated remaining scope: " + row["case_id"])
    files = source_files()
    for path in files:
        if not path.exists():
            continue
        relative = path.relative_to(ROOT)
        if relative.as_posix() == "docs/reference/stage1-final-report.pdf":
            failures.append("Unredacted private report must not enter public source.")
        if path.suffix.lower() in {".pem", ".p12", ".key", ".db", ".sqlite", ".sqlite3", ".log"} or path.name == ".env":
            failures.append("Runtime/credential file would enter source: " + str(relative))
        if path.suffix == ".py":
            ast.parse(path.read_text(encoding="utf-8"), filename=str(relative))
        if path.suffix in {".py", ".js", ".md", ".txt", ".json", ".yml"}:
            content = path.read_text(encoding="utf-8")
            if re.search(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----", content):
                failures.append("Private key material found: " + str(relative))
    if failures:
        raise SystemExit("Repository checks failed:\n" + "\n".join(failures))
    print(f"Repository checks passed: {len(files)} source files, 41 tracked cases, source hashes and five-member handoff verified.")
    print("This is a bounded local check, not a comprehensive secret or security audit.")


if __name__ == "__main__":
    check()
