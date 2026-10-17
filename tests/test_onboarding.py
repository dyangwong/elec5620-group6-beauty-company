"""Protect member identity, source grounding and local-versus-shared claim boundaries."""
import json
import shutil
import tempfile
import unittest
from pathlib import Path

from scripts.start_work import HandoffError, load_data, prepare_session, save_session, validate_handoff

ROOT = Path(__file__).resolve().parent.parent


class OnboardingTests(unittest.TestCase):
    def metadata_copy(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        root = Path(temp.name)
        (root / "docs").mkdir()
        for filename in ("team.json", "tasks.json", "source-manifest.json"):
            shutil.copyfile(ROOT / "docs" / filename, root / "docs" / filename)
        return root

    def test_all_five_declared_members_get_only_their_own_starter(self):
        team, _, manifest = load_data(ROOT)
        source = next(s for s in manifest["sources"] if s["id"] == "stage1")
        for member in team["members"]:
            for declaration in (member["name"], member["member_id"], member["module"].lower()):
                packet = prepare_session(ROOT, declaration)
                self.assertEqual(packet["task"]["owner_member_id"], member["member_id"])
                self.assertEqual(packet["task"]["module"], member["module"])
                self.assertEqual(packet["report"]["sha256"], source["original_sha256"])
                self.assertFalse(packet["shared_claim_verified"])

    def test_missing_and_partial_identity_is_not_guessed(self):
        for declaration in (None, "", "Lei", "Siyuan", "founder", "administrator"):
            with self.assertRaises(HandoffError):
                prepare_session(ROOT, declaration)

    def test_member_cannot_silently_select_someone_elses_task(self):
        with self.assertRaises(HandoffError):
            prepare_session(ROOT, "Siyuan Lei", "AP-START-01")

    def test_preparation_and_local_save_do_not_claim_shared_tasks(self):
        root = self.metadata_copy()
        registry = root / "docs/tasks.json"
        before = registry.read_bytes()
        packet = prepare_session(root, "CS")
        self.assertFalse((root / "var/work-session.json").exists())
        saved = save_session(root, packet)
        self.assertEqual(json.loads(saved.read_text(encoding="utf-8"))["session_state"], "PREPARED_LOCALLY")
        self.assertEqual(registry.read_bytes(), before)
        self.assertTrue(all(t["claim_state"] == "UNCLAIMED" for t in json.loads(before)["tasks"]))
        # A saved profile must never become implicit identity on a later task.
        with self.assertRaises(HandoffError):
            prepare_session(root, None)

    def test_blocked_task_or_different_claim_prevents_default_start(self):
        root = self.metadata_copy()
        path = root / "docs/tasks.json"
        registry = json.loads(path.read_text(encoding="utf-8"))
        task = next(t for t in registry["tasks"] if t["module"] == "CS")
        task["readiness"] = "BLOCKED"
        path.write_text(json.dumps(registry), encoding="utf-8")
        with self.assertRaises(HandoffError):
            prepare_session(root, "CS")
        task["readiness"] = "READY"
        task["claim_state"] = "CLAIMED"
        task["claimed_by"] = "M4"
        path.write_text(json.dumps(registry), encoding="utf-8")
        with self.assertRaises(HandoffError):
            prepare_session(root, "CS")

    def test_changed_report_fingerprint_stops_old_handoff(self):
        root = self.metadata_copy()
        path = root / "docs/source-manifest.json"
        manifest = json.loads(path.read_text(encoding="utf-8"))
        next(s for s in manifest["sources"] if s["id"] == "stage1")["original_sha256"] = "0" * 64
        path.write_text(json.dumps(manifest), encoding="utf-8")
        with self.assertRaises(HandoffError):
            prepare_session(root, "CS")

    def test_jira_mapping_rejects_reused_keys_and_mismatched_links(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        root = Path(temp.name)
        shutil.copytree(ROOT / "docs", root / "docs")
        path = root / "docs/tasks.json"
        registry = json.loads(path.read_text(encoding="utf-8"))
        first, second = registry["tasks"][:2]
        second["jira_key"] = first["jira_key"]
        second["jira_url"] = first["jira_url"]
        path.write_text(json.dumps(registry), encoding="utf-8")
        self.assertTrue(any("reused across member chains" in e for e in validate_handoff(root)))
        shutil.copyfile(ROOT / "docs/tasks.json", path)
        registry = json.loads(path.read_text(encoding="utf-8"))
        registry["tasks"][0]["jira_url"] = "https://example.invalid/browse/WRONG-1"
        path.write_text(json.dumps(registry), encoding="utf-8")
        self.assertTrue(any("differs from its declared key/site" in e for e in validate_handoff(root)))

    def test_public_reference_cannot_be_tampered_or_rebound(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        root = Path(temp.name)
        shutil.copytree(ROOT / "docs", root / "docs")
        manifest_path = root / "docs/source-manifest.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        source = next(item for item in manifest["sources"] if item["id"] == "stage1")
        source["derived_from_sha256"] = "0" * 64
        manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
        self.assertTrue(any("not bound" in error for error in validate_handoff(root)))
        shutil.copyfile(ROOT / "docs/source-manifest.json", manifest_path)
        reference = root / source["reference_pdf"]
        reference.write_bytes(reference.read_bytes() + b"tampered")
        self.assertTrue(any("derivative hash" in error for error in validate_handoff(root)))

    def test_report_mapping_and_noncolliding_task_scopes_are_grounded(self):
        self.assertEqual(validate_handoff(ROOT), [])
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        root = Path(temp.name)
        shutil.copytree(ROOT / "docs", root / "docs")
        path = root / "docs/team.json"
        team = json.loads(path.read_text(encoding="utf-8"))
        team["members"][0]["name"], team["members"][1]["name"] = team["members"][1]["name"], team["members"][0]["name"]
        path.write_text(json.dumps(team), encoding="utf-8")
        self.assertTrue(any("differs from the report" in error for error in validate_handoff(root)))
        shutil.copyfile(ROOT / "docs/team.json", path)
        path = root / "docs/tasks.json"
        registry = json.loads(path.read_text(encoding="utf-8"))
        registry["tasks"][1]["primary_files"].append(registry["tasks"][0]["primary_files"][0])
        path.write_text(json.dumps(registry), encoding="utf-8")
        self.assertTrue(any("collide" in error for error in validate_handoff(root)))


if __name__ == "__main__":
    unittest.main()
