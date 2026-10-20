"""Repair Strata's owner-private runtime and adopt this project's saved profile.

Uses the installed, pinned Strata implementation; never bypasses its ACL checks.
Does not download weights, rewrite model choices or remove runtime records.
"""
import json
import os
import stat
import sys
from datetime import datetime, timezone
from pathlib import Path


def main():
    if os.name != "nt":
        raise RuntimeError("This repair command is for Windows only.")
    repo = Path(__file__).resolve().parent.parent
    data = repo / "var"
    terminal = data / "strata-terminal"
    sys.path.insert(0, str(terminal))
    from strata_control import private_files, profiles, runtime

    runtime_path = data / "strata-runtime"
    # Never apply permissions to a junction or to a path outside this project.
    if runtime_path.resolve() != data.resolve() / "strata-runtime":
        raise RuntimeError("Unexpected runtime directory; refusing permission changes.")
    if runtime_path.exists():
        attrs = getattr(runtime_path.lstat(), "st_file_attributes", 0)
        if runtime_path.is_symlink() or attrs & stat.FILE_ATTRIBUTE_REPARSE_POINT:
            raise RuntimeError("Linked runtime directories are not repaired automatically.")
    else:
        runtime_path.mkdir(parents=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    backups = data / "verification"
    backups.mkdir(parents=True, exist_ok=True)

    if not private_files.is_unshared(runtime_path):
        before = private_files.dacl_sddl(runtime_path)
        backup = backups / f"strata-runtime-acl-{stamp}.json"
        with backup.open("x", encoding="utf-8") as stream:
            json.dump({"path": str(runtime_path), "sddl": before}, stream, indent=2)
        private_files.restrict_to_current_user(runtime_path, directory=True)
    os.environ["STRATA_RUNTIME_DIR"] = str(runtime_path)
    if runtime.runtime_dir() != runtime_path or not private_files.is_unshared(runtime_path):
        raise RuntimeError("Strata's owner-private runtime validation did not pass.")
    print("Strata runtime: owner-private access verified.")

    os.environ["STRATA_PROFILE_DIR"] = str(data / "strata-profiles")
    profile_path = data / "strata-profiles" / "launch-elec5620-ba.json"
    if not profile_path.exists():
        return
    profile, _ = profiles.load("launch-elec5620-ba")
    source = Path(profile["source_config"]).resolve()
    try:
        source.relative_to(data.resolve())
        return  # Existing project-local configuration stays byte-for-byte unchanged.
    except ValueError:
        pass
    if runtime.status("launch-elec5620-ba").get("state") != "stopped":
        print("Active model profile preserved; its launch file can be adopted after StopModel.")
        return
    # A failed `launch` may already have created a profile but no launch preset.
    # Its generated config lives in LOCALAPPDATA even with STRATA_INSTALL_DIR set.
    if source.name != "elec5620-ba.json" or not source.is_file():
        raise RuntimeError("Saved profile source is unexpected/missing; inspect it manually.")
    config = json.loads(source.read_text(encoding="utf-8-sig"))
    args = config.get("args", [])
    if config.get("host", "127.0.0.1") != "127.0.0.1" or "--native" not in args:
        raise RuntimeError("Only this project's loopback model profile can be adopted.")
    native = Path(args[args.index("--native") + 1]).resolve()
    native.relative_to((data / "models").resolve())
    folder = data / "strata-launch"
    folder.mkdir(parents=True, exist_ok=True)
    private_files.restrict_to_current_user(folder, directory=True)
    local_source = folder / "elec5620-ba.json"
    if local_source.exists():
        raise RuntimeError("Project-local launch config already exists; it was preserved for manual reconciliation.")
    # Preserve the old config/profile, including all user choices, before relocating.
    for name, payload in ((f"strata-profile-before-{stamp}.json", profile_path.read_bytes()),
                          (f"strata-launch-before-{stamp}.json", source.read_bytes())):
        path = backups / name
        with path.open("xb") as stream:
            stream.write(payload)
        private_files.restrict_to_current_user(path, directory=False)
    config["log"] = str(folder / "elec5620-ba.engine.log")
    with local_source.open("x", encoding="utf-8") as stream:
        json.dump(config, stream, ensure_ascii=False, indent=2)
        stream.write("\n")
    private_files.restrict_to_current_user(local_source, directory=False)
    proposed, revision = profiles.propose_source("launch-elec5620-ba", str(local_source))
    profiles.save("launch-elec5620-ba", proposed, expected_revision=revision)
    print("Saved model profile adopted under var/strata-launch; original settings backed up.")


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print(f"Strata runtime preparation failed ({type(error).__name__}): {error}", file=sys.stderr)
        raise SystemExit(1)
