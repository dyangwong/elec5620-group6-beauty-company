"""Make a local source archive without .git, runtime state or credentials."""
import argparse
import zipfile
from pathlib import Path

from check_repository import ROOT, check, source_files


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", default=str(ROOT / "output/prototype-source.zip"))
    args = parser.parse_args()
    check()
    output = Path(args.output).resolve()
    if output.exists():
        parser.error("Output already exists; choose a new path to preserve the previous archive.")
    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, "w", zipfile.ZIP_DEFLATED) as archive:
        for path in source_files():
            if path.is_file() and path.resolve() != output:
                archive.write(path, path.relative_to(ROOT))
    print(f"Local source archive created: {output}")
    print("This does not upload to Canvas or establish that final acceptance has passed.")


if __name__ == "__main__":
    main()
