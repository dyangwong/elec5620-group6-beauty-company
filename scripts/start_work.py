"""Resolve an explicitly declared contributor and prepare a local task packet."""
import argparse
import csv
import hashlib
import json
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


class HandoffError(ValueError):
    pass


def load_data(root):
    root = Path(root)
    return (
        json.loads((root / "docs/team.json").read_text(encoding="utf-8")),
        json.loads((root / "docs/tasks.json").read_text(encoding="utf-8")),
        json.loads((root / "docs/source-manifest.json").read_text(encoding="utf-8")),
    )


def normalise(value):
    return " ".join(str(value).split()).casefold()


def validate_handoff(root):
    """Validate evidence links and cross-member boundaries; do not infer actual claims."""
    root = Path(root)
    team, registry, manifest = load_data(root)
    failures = []
    source = next(item for item in manifest["sources"] if item["id"] == "stage1")
    for filename, data in [("team.json", team), ("tasks.json", registry)]:
        if data.get("source_id") != "stage1" or data.get("source_sha256") != source["original_sha256"]:
            failures.append(filename + " does not match the declared final Stage 1 source.")
    reference = root / source.get("reference_pdf", "missing-reference.pdf")
    if not reference.is_file() or hashlib.sha256(reference.read_bytes()).hexdigest() != source["reference_pdf_sha256"]:
        failures.append("Portable report reference is missing or differs from its declared derivative hash.")
    kind = source.get("reference_kind", "byte_identical")
    if kind == "privacy_redacted":
        if source.get("derived_from_sha256") != source["original_sha256"] or "student_ids" not in source.get("redacted_fields", []):
            failures.append("Public report derivative is not bound to the original source/redaction scope.")
    elif kind != "byte_identical" or source["reference_pdf_sha256"] != source["original_sha256"]:
        failures.append("Unrecognised or mismatched report-reference provenance.")
    baseline = (root / source["excerpt_file"]).read_text(encoding="utf-8")
    # Extract the actual report roster, rather than validating against a second invented roster.
    roster = {
        "M" + match.group(1): (normalise(match.group(2)), match.group(3))
        for match in re.finditer(r"(?m)^([1-5])[ \t]+([A-Za-z]+(?:[ \t]+[A-Za-z]+)+)[ \t]+(?:[0-9]{9}|\[STUDENT_ID_REDACTED\])[ \t]+(BA|CS|MC|AP|CO)\b", baseline)
    }
    if len(roster) != 5:
        failures.append("Could not ground all five member chains in the retained Stage 1 roster.")
    members = team["members"]
    tasks = registry["tasks"]
    if len(members) != 5 or len({m["member_id"] for m in members}) != 5 or {m["module"] for m in members} != {"BA", "CS", "MC", "AP", "CO"}:
        failures.append("Exactly five unique Stage 1 member chains are required.")
    if len(tasks) != 5 or len({t["id"] for t in tasks}) != 5:
        failures.append("Prepare exactly one unique initial task per member.")
    by_id = {m["member_id"]: m for m in members}
    task_ids = {t["id"] for t in tasks}
    with (root / "docs/traceability.csv").open(newline="") as stream:
        case_ids = {r["case_id"] for r in csv.DictReader(stream)}
    for member in members:
        code = member["module"]
        if roster.get(member["member_id"]) != (normalise(member["name"]), code):
            failures.append("Member/name/module differs from the report: " + member["member_id"])
        if member["requirement"] != code + "-M-01" or member["use_case"] != code + "-UC-01":
            failures.append("Requirement/use-case chain mismatch: " + code)
        if set(member["features"]) != {f"{code}-F-{n:02d}" for n in (1, 2, 3)}:
            failures.append("Missing core/optional feature IDs: " + code)
        if set(member["acceptance_cases"]) != {c for c in case_ids if c.startswith(code + "-")}:
            failures.append("Member acceptance list differs from traceability: " + code)
        if member["starter_task"] not in task_ids or not (root / member["module_guide"]).is_file():
            failures.append("Missing member task or module guide: " + code)
        if any(type(page) is not int or not 1 <= page <= source["original_page_count"] for page in member["reading_pdf_pages"]):
            failures.append("Invalid original PDF page locator: " + code)
    primary_owners = {}
    jira_keys = set()
    for task in tasks:
        owner = by_id.get(task["owner_member_id"])
        if not owner or owner["module"] != task["module"] or owner["starter_task"] != task["id"]:
            failures.append("Task is assigned across member chains: " + task["id"])
            continue
        if not set(task["features"]).issubset(owner["features"]) or not set(task["acceptance_cases"]).issubset(owner["acceptance_cases"]):
            failures.append("Task feature/case scope crosses its member chain: " + task["id"])
        jira_key = task.get("jira_key")
        if jira_key:
            project_key = registry.get("jira_project_key", "")
            if not project_key or not re.fullmatch(re.escape(project_key) + r"-\d+", jira_key):
                failures.append("Jira key does not match the declared project: " + task["id"])
            if jira_key in jira_keys:
                failures.append("A Jira task key is reused across member chains: " + jira_key)
            jira_keys.add(jira_key)
            expected_url = registry.get("jira_project_url", "").split("/jira/", 1)[0] + "/browse/" + jira_key
            if task.get("jira_url") != expected_url or not expected_url.startswith("https://"):
                failures.append("Jira task URL differs from its declared key/site: " + task["id"])
        if not (root / task["brief"]).is_file():
            failures.append("Missing task brief: " + task["id"])
        if not set(task["depends_on"]).issubset(task_ids):
            failures.append("Unknown task dependency: " + task["id"])
        for path in task["primary_files"]:
            if path in primary_owners and primary_owners[path] != task["id"]:
                failures.append("Initial tasks collide on a primary file: " + path)
            primary_owners[path] = task["id"]
        for path in task["primary_files"] + [item["path"] for item in task["shared_change_scope"]]:
            relative = Path(path)
            if relative.is_absolute() or ".." in relative.parts:
                failures.append("Task scope escapes the repository: " + path)
        if task["claim_state"] == "UNCLAIMED" and task["claimed_by"] is not None:
            failures.append("Unclaimed task has a claimed member: " + task["id"])
    return failures


def prepare_session(root, identity, task_id=None):
    root = Path(root)
    team, registry, manifest = load_data(root)
    if not isinstance(identity, str) or not identity.strip():
        raise HandoffError("Explicitly provide your full report name, member ID or module code; identity is never guessed.")
    key = normalise(identity)
    matches = [m for m in team["members"] if key in {normalise(m["name"]), normalise(m["member_id"]), normalise(m["module"])}]
    if len(matches) != 1:
        raise HandoffError("Identity is unknown or ambiguous. Use the exact full name, M1–M5 or BA/CS/MC/AP/CO from START_HERE.md.")
    member = matches[0]
    selected = task_id or member["starter_task"]
    task = next((t for t in registry["tasks"] if t["id"] == selected), None)
    if not task or task["owner_member_id"] != member["member_id"]:
        raise HandoffError("That task is not assigned to the declared Stage 1 member. No other chain was selected.")
    if task["readiness"] != "READY":
        raise HandoffError("The task is not currently marked READY; inspect its recorded dependency or blocker.")
    if task["claim_state"] != "UNCLAIMED" and task["claimed_by"] != member["member_id"]:
        raise HandoffError("A different/shared claim is recorded. Reconcile it before doing duplicate work.")
    source = next(s for s in manifest["sources"] if s["id"] == "stage1")
    if team["source_sha256"] != source["original_sha256"] or registry["source_sha256"] != source["original_sha256"]:
        raise HandoffError("Handoff metadata and the report baseline differ; resolve the source revision first.")
    return {
        "session_state": "PREPARED_LOCALLY",
        "member": member,
        "task": task,
        "reading_order": ["AGENTS.md", "START_HERE.md", "docs/STATUS.md", "docs/REQUIREMENTS.md",
                          "docs/CONTRACTS.md", "docs/COLLABORATION.md", "docs/JIRA.md", "docs/SHARED_FILES.md",
                          member["module_guide"], task["brief"], "docs/reference/acceptance-cases.txt"],
        "report": {"path": source["reference_pdf"], "sha256": source["original_sha256"], "reference_sha256": source["reference_pdf_sha256"], "reference_kind": source.get("reference_kind", "byte_identical"), "pdf_pages": member["reading_pdf_pages"]},
        "shared_claim_verified": False,
        "local_profile": "var/work-session.json",
        "notes": [
            "Identity comes from explicit contributor input, not a verified GitHub/product login.",
            "This helper reads local files only; check actual shared claims before parallel work.",
            "READY means the task brief is prepared, not that implementation has started or passed.",
            "Use the published common baseline and task branch; do not make independent root commits.",
            "Live/local model installation and external writes are outside these starter tasks.",
        ],
    }


def save_session(root, packet):
    path = Path(root) / "var/work-session.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({**packet, "prepared_at": datetime.now(timezone.utc).isoformat()}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return path


def branch_note(root):
    if not (Path(root) / ".git").exists():
        return "No Git checkout detected. Use the common repository baseline before branch-based collaboration."
    result = subprocess.run(["git", "rev-parse", "--verify", "HEAD"], cwd=root, capture_output=True)
    if result.returncode:
        return "The local repository has no initial commit yet. The maintainer must publish one common baseline before teammates clone and branch."
    return "Read the current branch/dirty state and shared claim, then use the task branch. This helper does not switch branches."


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--member", help="Exact Stage 1 full name, member ID or module code")
    group.add_argument("--list", action="store_true", help="List the five prepared entry tasks")
    parser.add_argument("--task", help="Explicit task ID; must belong to the declared member")
    parser.add_argument("--json", action="store_true", help="Print a machine-readable packet")
    parser.add_argument("--save", action="store_true", help="Save only an ignored local work session")
    args = parser.parse_args()
    try:
        failures = validate_handoff(ROOT)
        if failures:
            raise HandoffError("Invalid handoff metadata:\n" + "\n".join(failures))
        if args.list:
            if args.task or args.save:
                parser.error("--task/--save requires --member.")
            team, registry, _ = load_data(ROOT)
            if args.json:
                print(json.dumps({"members": team["members"], "tasks": registry["tasks"]}, ensure_ascii=False, indent=2))
            else:
                for member in team["members"]:
                    print(f"{member['member_id']} | {member['name']} | {member['module']} | {member['starter_task']}")
                print("Prepared task briefs only; no shared claim or external write performed.")
            return
        packet = prepare_session(ROOT, args.member, args.task)
        packet["branch_note"] = branch_note(ROOT)
        if args.save:
            save_session(ROOT, packet)
        if args.json:
            print(json.dumps(packet, ensure_ascii=False, indent=2))
        else:
            member, task = packet["member"], packet["task"]
            print(f"{member['name']} ({member['member_id']}) → {member['module']} / {task['id']}\n{task['title']}\n")
            if task.get("jira_key"):
                print("Jira task: " + task["jira_key"] + " / " + task["jira_url"])
                print("Planned assignee: " + (task.get("jira_assignee_display_name") or "Unassigned; account not verified."))
                print("Assignment is not a personal claim; check Jira for current state.\n")
            print("Read in order:\n" + "\n".join("  " + path for path in packet["reading_order"]))
            print("\nOriginal PDF pages: " + ", ".join(map(str, packet["report"]["pdf_pages"])))
            print("Primary files:\n" + "\n".join("  " + path for path in task["primary_files"]))
            print("Shared exceptions:\n" + ("\n".join("  " + item["path"] + ": " + item["limit"] for item in task["shared_change_scope"]) or "  None in this starter task."))
            print("\nSuggested branch: " + task["suggested_branch"])
            print("Completion boundary: " + task["completion_boundary"])
            print("\n" + packet["branch_note"])
            print("No network access, shared claim, Jira update, branch switch or code implementation performed.")
            if args.save:
                print("Saved ignored local session: var/work-session.json (not a shared task claim).")
    except (HandoffError, OSError, KeyError, ValueError) as error:
        parser.exit(2, str(error) + "\n")


if __name__ == "__main__":
    main()
