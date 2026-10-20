#!/usr/bin/env python3
"""Prepare isolated agent tasks or check outcomes from outside their workspace."""

import argparse
import importlib.util
from pathlib import Path
import shutil
import sqlite3
import subprocess
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
CASES = {"local-refactor", "behavior-change", "migration", "architecture"}


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def prepare(case, workspace):
    if workspace.exists():
        raise ValueError("destination must not exist")
    workspace.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(ROOT / "evals/fixtures" / case, workspace)
    installed = workspace / ".agents/skills/project-workflow"
    installed.mkdir(parents=True)
    for name in ("SKILL.md", "LICENSE", "references", "templates", "scripts"):
        source = ROOT / name
        if source.is_dir():
            shutil.copytree(source, installed / name, ignore=shutil.ignore_patterns("__pycache__"))
        else:
            shutil.copy(source, installed / name)
    (workspace / "AGENTS.md").write_text(
        "# Fixture project\n\nWorkflow skill: `.agents/skills/project-workflow/SKILL.md`\n\n"
        "Use this workflow for the requested task. Keep changes inside this workspace.\n"
        "Use Python's standard library. Existing checks: "
        "`python3 -m unittest discover -v`.\n"
        "Do not edit the installed skill. No network or publication is needed.\n"
    )
    (workspace / ".gitignore").write_text("__pycache__/\n*.py[cod]\n")
    for args in (
        ["git", "init", "-q"],
        ["git", "add", "."],
        ["git", "-c", "user.name=Workflow Evaluation",
         "-c", "user.email=evaluation@example.invalid", "commit", "-qm", "Fixture baseline"],
    ):
        subprocess.run(args, cwd=workspace, check=True)
    print(f"Prepared {case}: {workspace}")


def tests_for(case, workspace):
    class Outcome(unittest.TestCase):
        def test_workflow_state(self):
            script = workspace / ".agents/skills/project-workflow/scripts/validate-workflow.py"
            result = subprocess.run(
                [sys.executable, str(script), "project", str(workspace)],
                capture_output=True, text=True,
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            records = list((workspace / "docs/changes").rglob("*.md"))
            if case == "local-refactor":
                self.assertEqual(records, [])
                self.assertFalse((workspace / "docs").exists())
            else:
                self.assertEqual(len(records), 1)
                body = records[0].read_text()
                self.assertIn("status: completed", body)
                if case == "architecture":
                    self.assertIn("intent: planning", body)
                    self.assertIn("stage: design", body)
                    self.assertNotEqual(records[0].parent.name, "archive")
                else:
                    self.assertIn("intent: delivery", body)
                    self.assertIn("grade: " + ("L" if case == "migration" else "M"), body)
                    self.assertEqual(records[0].parent.name, "archive")

        def test_installed_skill_unchanged(self):
            result = subprocess.run(
                ["git", "diff", "--exit-code", "HEAD", "--", ".agents", "AGENTS.md"],
                cwd=workspace, capture_output=True, text=True,
            )
            self.assertEqual(result.returncode, 0, result.stdout)

    if case == "local-refactor":
        def behavior(self):
            module = load(workspace / "labels.py", "candidate_labels")
            for values in ([], [" A ", "", "  ", "B", " A "], [" Ä ", "\tİ\n", "É"]):
                self.assertEqual(module.labels(values),
                                 [v.strip().lower() for v in values if v.strip().lower()])
            class Counted(str):
                calls = 0
                def strip(self, *args):
                    type(self).calls += 1
                    return super().strip(*args)
            values = [Counted(" A "), Counted(""), Counted("B")]
            self.assertEqual(module.labels(values), ["a", "b"])
            self.assertEqual(Counted.calls, len(values))
        Outcome.test_behavior = behavior
    elif case == "behavior-change":
        def behavior(self):
            module = load(workspace / "tasks.py", "candidate_tasks")
            rows = [
                {"id": 9, "completed": True}, {"id": 5, "completed": False},
                {"id": 3}, {"id": 8, "completed": 1}, {"id": 6, "completed": "true"},
                {"id": 2, "completed": None},
            ]
            before = [dict(row) for row in rows]
            actual = module.visible_tasks(rows)
            self.assertEqual([row["id"] for row in actual], [5, 3, 8, 6, 2])
            self.assertEqual(rows, before)
            actual[0]["id"] = -1
            self.assertEqual(rows, before)
            self.assertEqual(module.visible_tasks([]), [])
        def retained_spec(self):
            body = (workspace / "docs/behavior.md").read_text()
            self.assertIn("## REQ-2: Preserve input", body)
            self.assertIn("Rendering must preserve input order and must not mutate input objects.", body)
            self.assertNotIn("## REQ-3", body)
            self.assertNotIn("The default list includes every task.", body)
            self.assertFalse(any("delete" in name.lower() for name in
                                 vars(load(workspace / "tasks.py", "candidate_tasks"))))
        Outcome.test_behavior = behavior
        Outcome.test_retained_spec_and_scope = retained_spec
    elif case == "migration":
        def database():
            con = sqlite3.connect(":memory:")
            load(workspace / "schema.py", "candidate_schema").create_schema(con)
            con.executemany("INSERT INTO items VALUES (?, ?)", [(2, "two"), (7, "seven")])
            con.commit()
            return con
        def snapshot(con):
            return (
                con.execute("PRAGMA user_version").fetchone(),
                con.execute("PRAGMA table_info(items)").fetchall(),
                con.execute("SELECT * FROM items ORDER BY id").fetchall(),
                con.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name").fetchall(),
            )
        def migration(self):
            module = load(workspace / "migration.py", "candidate_migration")
            con = database()
            self.addCleanup(con.close)
            before = snapshot(con)
            module.migrate(con)
            self.assertEqual(con.execute("PRAGMA user_version").fetchone()[0], 2)
            self.assertEqual(con.execute("SELECT id,name,status FROM items ORDER BY id").fetchall(),
                             [(2, "two", "pending"), (7, "seven", "pending")])
            after = snapshot(con)
            module.migrate(con)
            self.assertEqual(snapshot(con), after)
            with self.assertRaises(sqlite3.IntegrityError):
                con.execute("UPDATE items SET status='invalid' WHERE id=2")
            con.rollback()
            with self.assertRaises(sqlite3.IntegrityError):
                con.execute("UPDATE items SET status=NULL WHERE id=2")
            con.rollback()
            module.rollback(con)
            self.assertEqual(snapshot(con), before)
        def invalid_data(self):
            module = load(workspace / "migration.py", "candidate_migration")
            for value in (None, "", "   "):
                with self.subTest(value=value):
                    con = database()
                    self.addCleanup(con.close)
                    con.execute("INSERT INTO items VALUES (10, ?)", (value,))
                    con.commit()
                    before = snapshot(con)
                    with self.assertRaises(Exception):
                        module.migrate(con)
                    self.assertEqual(snapshot(con), before)
        def refused_rollback(self):
            module = load(workspace / "migration.py", "candidate_migration")
            con = database()
            self.addCleanup(con.close)
            module.migrate(con)
            con.execute("UPDATE items SET status='done' WHERE id=2")
            con.commit()
            before = snapshot(con)
            with self.assertRaises(Exception):
                module.rollback(con)
            self.assertEqual(snapshot(con), before)
        def unsupported_version(self):
            module = load(workspace / "migration.py", "candidate_migration")
            con = database()
            self.addCleanup(con.close)
            con.execute("PRAGMA user_version=9")
            con.commit()
            before = snapshot(con)
            with self.assertRaises(Exception):
                module.migrate(con)
            self.assertEqual(snapshot(con), before)
        def commit_failure(self):
            module = load(workspace / "migration.py", "candidate_migration")
            con = database()
            self.addCleanup(con.close)
            before = snapshot(con)
            denied = []
            def authorize(action, arg1, arg2, db, trigger):
                commit = action == sqlite3.SQLITE_TRANSACTION and arg1 == "COMMIT"
                release = action == sqlite3.SQLITE_SAVEPOINT and arg1 == "RELEASE"
                if (commit or release) and not denied:
                    denied.append(True)
                    return sqlite3.SQLITE_DENY
                return sqlite3.SQLITE_OK
            con.set_authorizer(authorize)
            with self.assertRaises(Exception):
                module.migrate(con)
            con.set_authorizer(lambda *args: sqlite3.SQLITE_OK)
            self.assertTrue(denied, "migration must expose a transactional commit boundary")
            self.assertEqual(snapshot(con), before)
        Outcome.test_migration_idempotency_and_recovery = migration
        Outcome.test_invalid_data_atomicity = invalid_data
        Outcome.test_refuse_lossy_rollback = refused_rollback
        Outcome.test_unsupported_version = unsupported_version
        Outcome.test_commit_failure_atomicity = commit_failure
    elif case == "architecture":
        def planning_only(self):
            self.assertEqual((workspace / "context.md").read_bytes(),
                             (ROOT / "evals/fixtures/architecture/context.md").read_bytes())
            for path in workspace.rglob("*"):
                relative = path.relative_to(workspace)
                if any(part in {".git", ".agents", "__pycache__"} for part in relative.parts):
                    continue
                if path.is_file():
                    self.assertIn(path.suffix, {".md", ""}, f"unexpected implementation: {relative}")
        Outcome.test_planning_only = planning_only
    return unittest.defaultTestLoader.loadTestsFromTestCase(Outcome)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("prepare", "check"))
    parser.add_argument("case", choices=sorted(CASES))
    parser.add_argument("workspace", type=Path)
    args = parser.parse_args()
    workspace = args.workspace.resolve()
    if workspace == ROOT or ROOT in workspace.parents:
        parser.error("evaluation workspaces must be outside the skill checkout")
    if args.action == "prepare":
        prepare(args.case, workspace)
        return 0
    if not workspace.is_dir():
        parser.error("workspace does not exist")
    result = unittest.TextTestRunner(verbosity=2).run(tests_for(args.case, workspace))
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(main())
