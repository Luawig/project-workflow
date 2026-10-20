"""Exercise observable CLI behavior and state/evidence invariants."""

import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/validate-workflow.py"
spec = importlib.util.spec_from_file_location("validator", SCRIPT)
validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)


class ValidatorTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.skill = self.root / ".agents/skills/project-workflow"
        self.skill.mkdir(parents=True)
        shutil.copy(ROOT / "SKILL.md", self.skill / "SKILL.md")
        self.agents = self.root / "AGENTS.md"
        self.agents.write_text("Workflow skill: `.agents/skills/project-workflow/SKILL.md`\n")
        self.record = self.root / "docs/changes/example.md"
        self.record.parent.mkdir(parents=True)
        self.record.write_text((ROOT / "templates/change-record.md").read_text())
        (self.root / "app.py").write_text("def answer():\n    return 42\n")
        (self.root / "spec.md").write_text("R1: answer is 42\nR2: retain this requirement\n")

    def run_cli(self, *args, code=0):
        result = subprocess.run(
            [sys.executable, str(SCRIPT), *map(str, args)], capture_output=True, text=True
        )
        self.assertEqual(result.returncode, code, result.stdout + result.stderr)
        return result.stdout + result.stderr

    def check(self, code=0, *args):
        return self.run_cli("project", self.root, *args, code=code)

    def replace(self, old, new):
        body = self.record.read_text()
        self.assertIn(old, body)
        self.record.write_text(body.replace(old, new))

    def pass_evidence(self, ident="EV-1", inputs=("app.py", "spec.md")):
        fingerprint = self.run_cli("fingerprint", self.root,
                                   self.record.relative_to(self.root), *inputs)
        body = (
            f"### {ident}\nacceptance: AC-1\nresult: pass\n"
            "method: isolated acceptance check\nenvironment: local fixture\n"
            "baseline: fixture working tree\n" + fingerprint
        )
        text = self.record.read_text()
        if "## Evidence\nnone" in text:
            text = text.replace("## Evidence\nnone", "## Evidence\n" + body)
        else:
            text = text.replace("## Closeout", body + "\n## Closeout")
        self.record.write_text(text)

    def finish(self):
        self.replace("stage: triage", "stage: closeout")
        self.replace("status: active", "status: completed")
        self.replace("next_action: Inspect relevant implementation and acceptance sources.",
                     "next_action: none")
        self.replace("verification: pending", "verification: passed")
        self.replace("knowledge_sync: pending", "knowledge_sync: complete")

    def archive(self, name="2026-01-02-example.md"):
        destination = self.record.parent / "archive" / name
        destination.parent.mkdir(exist_ok=True)
        self.record.rename(destination)
        self.record = destination

    def test_valid_active_installation(self):
        self.check()

    def test_missing_route_does_not_use_installed_fallback(self):
        self.agents.unlink()
        self.assertIn("explicit Workflow skill", self.check(1))

    def test_mention_is_not_route(self):
        self.agents.write_text("Use project-workflow for everything.\n")
        self.check(1)

    def test_broken_route_does_not_use_installed_fallback(self):
        self.agents.write_text("Workflow skill: `missing/SKILL.md`\n")
        self.assertIn("no fallback", self.check(1))

    def test_standalone_does_not_require_route(self):
        self.agents.unlink()
        self.check(0, "--standalone")

    def test_standalone_still_checks_declared_route(self):
        self.agents.write_text("Workflow skill: `missing/SKILL.md`\n")
        self.check(1, "--standalone")

    def test_absolute_route_with_spaces(self):
        target = self.root / "installed skill/SKILL.md"
        target.parent.mkdir()
        shutil.copy(ROOT / "SKILL.md", target)
        self.agents.write_text(f"Workflow skill: `{target}`\n")
        self.check()

    def test_fenced_route_not_installed(self):
        self.agents.write_text("```md\n" + self.agents.read_text() + "```\n")
        self.check(1)

    def test_duplicate_route_rejected(self):
        self.agents.write_text(self.agents.read_text() * 2)
        self.check(1)

    def test_wrong_skill_name_rejected(self):
        target = self.skill / "SKILL.md"
        target.write_text(target.read_text().replace("name: project-workflow", "name: other"))
        self.check(1)

    def test_empty_and_non_string_descriptions_rejected(self):
        target = self.skill / "SKILL.md"
        for value in ('""', "''", "null", "true", "[some, text]", "{}", "# comment",
                      "42", "0x10", ".nan", ".inf", "1_000", "2026-10-20"):
            with self.subTest(value=value):
                target.write_text(f"---\nname: project-workflow\ndescription: {value}\n---\n")
                self.check(1)

    def test_quoted_descriptions_are_parsed(self):
        target = self.skill / "SKILL.md"
        for value in ('"Guide authorized changes."', "'Guide authorized changes.'"):
            target.write_text(f"---\nname: project-workflow\ndescription: {value}\n---\n")
            self.check()

    def test_checked_tasks_do_not_complete_blocked_work(self):
        self.replace("- [ ]", "- [x]")
        self.replace("status: active", "status: blocked")
        self.replace("blocked_reason: none", "blocked_reason: Required environment unavailable.")
        self.check()

    def test_fenced_examples_do_not_change_state(self):
        self.replace("## Tasks\n", "## Tasks\n~~~md\n## Metadata\nstatus: completed\n"
                     "- [x] finished example\n~~~\n")
        self.check()

    def test_both_fence_styles_and_longer_fences(self):
        text = "````md\n```\n## Metadata\nstatus: completed\n````\nvisible"
        self.assertEqual(validator.visible(text).strip(), "visible")
        self.assertEqual(validator.visible("   ~~~md\nhidden\n   ~~~\nshown").strip(), "shown")

    def test_missing_field_rejected(self):
        self.replace("grade: M\n", "")
        self.assertIn("missing field grade", self.check(1))

    def test_duplicate_field_rejected(self):
        self.replace("status: active", "status: active\nstatus: completed")
        self.assertIn("duplicate field status", self.check(1))

    def test_duplicate_section_rejected(self):
        self.record.write_text(self.record.read_text() + "\n## Goal\nAnother goal\n")
        self.check(1)

    def test_invalid_status_rejected(self):
        self.replace("status: active", "status: green")
        self.check(1)

    def test_blocked_requires_reason_and_next_action(self):
        self.replace("status: active", "status: blocked")
        self.check(1)
        self.replace("blocked_reason: none", "blocked_reason: Awaiting environment.")
        self.replace("next_action: Inspect relevant implementation and acceptance sources.",
                     "next_action: none")
        self.check(1)

    def test_completed_delivery_left_active(self):
        self.pass_evidence()
        self.finish()
        self.assertIn("left active", self.check(1))

    def test_unfinished_record_in_archive(self):
        self.archive()
        self.assertIn("unfinished record in archive", self.check(1))

    def test_complete_archive_and_historical_evidence(self):
        self.pass_evidence()
        self.finish()
        self.archive()
        self.check()
        (self.root / "app.py").unlink()
        (self.root / "spec.md").write_text("Later authorized version\n")
        self.check()  # Archived observations are not today's claims.
        with tempfile.TemporaryDirectory() as external:
            outside = Path(external) / "app.py"
            outside.write_text("unrelated later code\n")
            (self.root / "app.py").symlink_to(outside)
            self.check()  # A later symlink must not change historical evidence.

    def test_archive_date_validated(self):
        self.pass_evidence()
        self.finish()
        self.archive("2026-02-30-example.md")
        self.assertIn("valid YYYY-MM-DD", self.check(1))

    def test_completed_without_evidence_rejected(self):
        self.finish()
        self.archive()
        self.assertIn("lacks latest passing evidence", self.check(1))

    def test_completed_without_sync_rejected(self):
        self.pass_evidence()
        self.finish()
        self.replace("knowledge_sync: complete", "knowledge_sync: pending")
        self.archive()
        self.check(1)

    def test_planning_checkpoint_not_delivery(self):
        self.replace("intent: delivery", "intent: planning")
        self.replace("verification: pending", "verification: not-applicable")
        self.replace("stage: triage", "stage: design")
        self.replace("status: active", "status: completed")
        self.replace("next_action: Inspect relevant implementation and acceptance sources.",
                     "next_action: none")
        self.check()
        self.archive()
        self.assertIn("planning stays outside", self.check(1))

    def test_planning_cannot_enter_implementation(self):
        self.replace("intent: delivery", "intent: planning")
        self.replace("verification: pending", "verification: not-applicable")
        self.replace("stage: triage", "stage: implement")
        self.check(1)

    def test_planning_cannot_claim_delivery_verification(self):
        self.replace("intent: delivery", "intent: planning")
        self.assertIn("no delivery claim", self.check(1))

    def test_delivery_cannot_skip_verification_as_not_applicable(self):
        self.replace("verification: pending", "verification: not-applicable")
        self.check(1)

    def test_cancelled_needs_disposition(self):
        self.replace("status: active", "status: cancelled")
        self.replace("next_action: Inspect relevant implementation and acceptance sources.",
                     "next_action: none")
        self.replace("Record affected owners, remaining issues and terminal disposition here.", "")
        self.replace("For planning, set verification to not-applicable and describe document review.", "")
        self.archive()
        self.assertIn("cancellation needs a disposition", self.check(1))
        self.record.write_text(self.record.read_text() + "User cancelled; changes retained for review.\n")
        self.check()

    def test_source_change_invalidates_passing_evidence(self):
        self.pass_evidence()
        self.check()
        (self.root / "app.py").write_text("def answer():\n    return 0\n")
        self.assertIn("stale evidence input app.py", self.check(1))
        self.replace("result: pass", "result: invalidated")
        self.check()

    def test_acceptance_and_decision_changes_invalidate_evidence(self):
        for section in ("Acceptance", "Decisions", "Constraints"):
            with self.subTest(section=section):
                original = self.record.read_text()
                self.pass_evidence()
                self.replace(f"## {section}\n", f"## {section}\nChanged condition.\n")
                self.assertIn("contract digest", self.check(1))
                self.record.write_text(original)

    def test_spec_edit_preserves_unaffected_requirement_and_rechecks(self):
        self.pass_evidence()
        owner = self.root / "spec.md"
        owner.write_text("R1: answer is configurable\nR2: retain this requirement\n")
        self.check(1)
        self.assertIn("R2: retain this requirement", owner.read_text())
        self.replace("result: pass", "result: invalidated")
        self.pass_evidence("EV-2")
        self.check()
        owner.write_text("R2: retain this requirement\n")
        self.check(1)

    def test_superseded_pass_does_not_force_historical_inputs_to_stay_current(self):
        self.pass_evidence()
        (self.root / "app.py").write_text("def answer():\n    return 43\n")
        self.pass_evidence("EV-2")
        self.check()

    def test_independent_acceptance_can_reaffirm_without_claiming_a_new_test(self):
        self.replace("## Decisions", "- AC-2: Independent documentation check.\n\n## Decisions")
        self.pass_evidence(inputs=("app.py",))
        self.replace("Independent documentation check.", "Independent revised documentation check.")
        self.assertIn("stale", self.check(1))
        self.pass_evidence("EV-2", inputs=("spec.md",))
        text = self.record.read_text()
        first, second = text.split("### EV-2")
        second = second.replace("acceptance: AC-1", "acceptance: AC-2")
        self.record.write_text(first + "### EV-2" + second)
        self.check(1)  # AC-1 still needs an applicability review.
        self.pass_evidence("EV-3", inputs=("app.py",))
        first, third = self.record.read_text().split("### EV-3")
        third = third.replace(
            "method: isolated acceptance check",
            "method: Applicability review of EV-1; only AC-2 changed; "
            "AC-1 and app.py are identical. Original test not rerun.",
        )
        self.record.write_text(first + "### EV-3" + third)
        self.check()

    def test_later_failure_cannot_hide_behind_old_pass(self):
        self.pass_evidence()
        self.replace("## Closeout", "### EV-2\nacceptance: AC-1\nresult: fail\n"
                     "method: negative test\nenvironment: local\nbaseline: fixture\n\n## Closeout")
        self.finish()
        self.archive()
        self.assertIn("lacks latest passing evidence", self.check(1))

    def test_unknown_acceptance_rejected(self):
        self.pass_evidence()
        self.replace("acceptance: AC-1", "acceptance: AC-2")
        self.check(1)

    def test_evidence_paths_cannot_escape(self):
        self.pass_evidence()
        self.replace('"app.py":', '"../app.py":')
        self.check(1)

    def test_active_evidence_symlink_cannot_escape(self):
        self.pass_evidence()
        with tempfile.TemporaryDirectory() as external:
            outside = Path(external) / "app.py"
            outside.write_bytes((self.root / "app.py").read_bytes())
            (self.root / "app.py").unlink()
            (self.root / "app.py").symlink_to(outside)
            self.assertIn("escapes project root", self.check(1))

    def test_fingerprint_read_only_and_exact_byte_hash(self):
        before = self.record.read_bytes()
        output = self.run_cli("fingerprint", self.root, "docs/changes/example.md", "app.py")
        data = json.loads(output.split("files: ", 1)[1])
        self.assertEqual(data["app.py"], hashlib.sha256((self.root / "app.py").read_bytes()).hexdigest())
        self.assertEqual(before, self.record.read_bytes())

    def test_fingerprint_rejects_record_self_reference_and_missing_input(self):
        self.run_cli("fingerprint", self.root, "docs/changes/example.md",
                     "docs/changes/example.md", code=2)
        self.run_cli("fingerprint", self.root, "docs/changes/example.md",
                     "missing.py", code=2)

    def test_invalid_root_is_input_error(self):
        self.run_cli("project", self.root / "absent", code=2)

    def test_unreadable_encoding_is_input_error(self):
        self.record.write_bytes(b"\xff")
        self.check(2)

    def test_nested_record_is_not_silently_ignored(self):
        target = self.record.parent / "nested/record.md"
        target.parent.mkdir()
        self.record.rename(target)
        self.check(1)

    def test_symlink_archive_cannot_hide_unfinished_records(self):
        storage = self.root / "elsewhere"
        storage.mkdir()
        self.record.rename(storage / "2026-01-02-example.md")
        (self.root / "docs/changes/archive").symlink_to(storage, target_is_directory=True)
        self.assertIn("symlink storage", self.check(1))

    def test_dangling_record_storage_is_not_absent(self):
        self.record.unlink()
        self.record.parent.rmdir()
        self.record.parent.symlink_to(self.root / "missing", target_is_directory=True)
        self.assertIn("must not be symlinked", self.check(1))


class PackageTests(unittest.TestCase):
    def test_package_and_template_links(self):
        report = validator.Report()
        validator.skill(ROOT, report)
        self.assertEqual(report.errors, [])

    def test_broken_local_link_and_fragment_are_detected(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            for name in validator.RESOURCES:
                target = root / name
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy(ROOT / name, target)
            (root / "README.md").write_text("[bad](missing.md)\n[bad](SKILL.md#missing-heading)\n")
            report = validator.Report()
            validator.skill(root, report)
            self.assertTrue(any("missing link" in error for error in report.errors))
            self.assertTrue(any("missing heading" in error for error in report.errors))


if __name__ == "__main__":
    unittest.main()
