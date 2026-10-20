#!/usr/bin/env python3
"""Read-only structural checks for project-workflow (Python 3.8+)."""

import argparse
import datetime
import hashlib
import json
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit


SECTIONS = (
    "Metadata", "Goal", "Non-goals", "Constraints", "Acceptance", "Decisions",
    "Tasks", "Recovery", "Evidence", "Closeout",
)
CONTRACT = ("Goal", "Non-goals", "Constraints", "Acceptance", "Decisions")
ENUMS = {
    "intent": {"planning", "delivery"},
    "grade": {"S", "M", "L"},
    "stage": {"triage", "clarify", "design", "spec", "implement", "verify", "closeout"},
    "status": {"active", "blocked", "completed", "cancelled"},
}
SLUG = r"[a-z0-9]+(?:-[a-z0-9]+)*"
SHA = re.compile(r"[0-9a-f]{64}")
RESOURCES = (
    "SKILL.md", "LICENSE",
    *(f"references/{name}.md" for name in (
        "lifecycle", "authority", "planning", "clarify", "design", "spec",
        "implement", "verify", "closeout", "record-format",
    )),
    *(f"templates/{name}.md" for name in (
        "change-record", "agents-block", "design-artifacts", "spec-artifacts",
    )),
    "scripts/validate-workflow.py",
)


class InputError(Exception):
    """Input cannot be inspected reliably."""


class Report:
    def __init__(self):
        self.errors = []

    def fail(self, message):
        self.errors.append(message)

    def require(self, condition, message):
        if not condition:
            self.fail(message)


def read(path):
    return path.read_text(encoding="utf-8")


def visible(text):
    """Preserve line positions while hiding CommonMark backtick/tilde fences."""
    output = []
    fence = None
    for line in text.splitlines():
        if fence:
            if re.fullmatch(r" {0,3}" + re.escape(fence[0]) + r"{"
                            + str(fence[1]) + r",}\s*", line):
                fence = None
            output.append("")
        else:
            match = re.match(r" {0,3}(`{3,}|~{3,})(.*)$", line)
            if match and not (match[1][0] == "`" and "`" in match[2]):
                fence = (match[1][0], len(match[1]))
                output.append("")
            else:
                output.append(line)
    return "\n".join(output)


def sections(text, level, report, label):
    """Headings in fences are ignored; bodies retain original fenced content."""
    raw = text.splitlines()
    marks = []
    for index, line in enumerate(visible(text).splitlines()):
        match = re.fullmatch("#" * level + r" +(.+?)\s*", line)
        if match:
            marks.append((index, match[1]))
    result = {}
    for index, (start, name) in enumerate(marks):
        end = marks[index + 1][0] if index + 1 < len(marks) else len(raw)
        if name in result:
            report.fail(f"{label}: duplicate heading {name}")
        result[name] = "\n".join(raw[start + 1:end]).strip()
    return result


def fields(text, report, label):
    result = {}
    for key, value in re.findall(r"^([a-z_][a-z0-9_]*):[ \t]*(.*)$", visible(text), re.M):
        if key in result:
            report.fail(f"{label}: duplicate field {key}")
        result[key] = value.strip()
    return result


def required_fields(values, names, report, label):
    for name in names:
        report.require(bool(values.get(name)), f"{label}: missing field {name}")


def contract_digest(parts):
    normalized = "\n\n".join(
        f"## {name}\n" + "\n".join(
            line.rstrip() for line in parts.get(name, "").splitlines()
        ).strip()
        for name in CONTRACT
    )
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()


def file_digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def inside(path, root):
    try:
        path.relative_to(root)
        return True
    except ValueError:
        return False


def relative_file(root, value):
    """Reject absolute, escaping and symlink-escaping evidence paths."""
    path = Path(value)
    if path.is_absolute() or ".." in path.parts or not value:
        raise ValueError("must be a project-relative path without '..'")
    resolved = (root / path).resolve()
    if not inside(resolved, root.resolve()):
        raise ValueError("path escapes project root")
    return resolved


def parse_record(text, report, label):
    parts = sections(text, 2, report, label)
    for name in SECTIONS:
        report.require(bool(parts.get(name)), f"{label}: missing/empty section {name}")
    meta = fields(parts.get("Metadata", ""), report, label)
    required_fields(meta, ENUMS, report, label)
    for key, choices in ENUMS.items():
        if key in meta:
            report.require(meta[key] in choices, f"{label}: invalid {key}: {meta[key]}")
    acceptance = {}
    for ident, description in re.findall(
        r"^- (AC-[1-9][0-9]*):[ \t]*(.*)$", visible(parts.get("Acceptance", "")), re.M
    ):
        report.require(ident not in acceptance, f"{label}: duplicate acceptance {ident}")
        report.require(bool(description.strip()), f"{label}: empty acceptance {ident}")
        acceptance[ident] = description
    report.require(bool(acceptance), f"{label}: no AC-* acceptance entries")
    return parts, meta, acceptance


def evidence(parts, acceptance, root, record, archived, report, label):
    body = parts.get("Evidence", "")
    entries = sections(body, 3, report, label + " evidence")
    report.require(bool(entries) or visible(body).strip() == "none",
                   f"{label}: Evidence must contain EV-* entries or none")
    latest = {}
    parsed = {
        ident: fields(entry, report, f"{label} {ident}") for ident, entry in entries.items()
    }
    latest_entry = {}
    for ident, data in parsed.items():
        for ac in data.get("acceptance", "").split(","):
            latest_entry[ac.strip()] = ident
    required = ("acceptance", "result", "method", "environment", "baseline")
    for ident, data in parsed.items():
        prefix = f"{label} {ident}"
        report.require(bool(re.fullmatch(r"EV-[1-9][0-9]*", ident)),
                       f"{prefix}: invalid evidence ID")
        required_fields(data, required, report, prefix)
        ids = [item.strip() for item in data.get("acceptance", "").split(",")]
        for ac in ids:
            report.require(ac in acceptance, f"{prefix}: unknown acceptance {ac}")
            latest[ac] = data.get("result")
        result = data.get("result")
        report.require(result in {"pass", "fail", "pending", "invalidated"},
                       f"{prefix}: invalid evidence result")
        if result != "pass":
            continue
        current = any(latest_entry.get(ac) == ident for ac in ids)
        report.require(bool(SHA.fullmatch(data.get("contract_sha256", ""))),
                       f"{prefix}: missing/invalid contract digest")
        if current:
            report.require(data.get("contract_sha256") == contract_digest(parts),
                           f"{prefix}: stale or missing contract digest")
        try:
            mapping = json.loads(data.get("files", ""))
        except (ValueError, TypeError):
            report.fail(f"{prefix}: files must be a JSON object")
            continue
        if not isinstance(mapping, dict) or not mapping:
            report.fail(f"{prefix}: passing evidence needs a nonempty files object")
            continue
        for name, digest in mapping.items():
            if not isinstance(digest, str) or not SHA.fullmatch(digest):
                report.fail(f"{prefix}: invalid SHA-256 for {name}")
                continue
            try:
                # Archived paths are historical names, not today's symlink targets.
                if archived or not current:
                    raw_path = Path(name)
                    if raw_path.is_absolute() or ".." in raw_path.parts or not name:
                        raise ValueError("must be a project-relative path without '..'")
                    path = root / raw_path
                else:
                    path = relative_file(root, name)
            except ValueError as exc:
                report.fail(f"{prefix}: {name}: {exc}")
                continue
            if path == record.resolve():
                report.fail(f"{prefix}: do not hash the record itself")
            elif not archived and current:
                if not path.is_file():
                    report.fail(f"{prefix}: missing evidence input {name}")
                elif file_digest(path) != digest:
                    report.fail(f"{prefix}: stale evidence input {name}")
    return latest


def validate_record(path, root, archived, report):
    label = str(path.relative_to(root))
    parts, meta, acceptance = parse_record(read(path), report, label)
    status, stage, intent = (meta.get(key) for key in ("status", "stage", "intent"))
    recovery = fields(parts.get("Recovery", ""), report, label)
    required_fields(recovery, ("next_action", "blocked_reason"), report, label)
    if status in {"active", "blocked"}:
        report.require(recovery.get("next_action", "none") != "none",
                       f"{label}: unfinished work needs next_action")
    elif status in {"completed", "cancelled"}:
        report.require(recovery.get("next_action") == "none",
                       f"{label}: terminal next_action must be none")
    if status == "blocked":
        report.require(recovery.get("blocked_reason", "none") != "none",
                       f"{label}: blocked work needs blocked_reason")
    else:
        report.require(recovery.get("blocked_reason") == "none",
                       f"{label}: blocked_reason must be none unless blocked")
    close = fields(parts.get("Closeout", ""), report, label)
    required_fields(close, ("verification", "knowledge_sync"), report, label)
    report.require(close.get("verification") in {"pending", "passed", "not-applicable"},
                   f"{label}: invalid verification disposition")
    report.require(close.get("knowledge_sync") in {"pending", "complete", "not-applicable"},
                   f"{label}: invalid knowledge_sync disposition")
    latest = evidence(parts, acceptance, root, path, archived, report, label)
    if intent == "planning":
        report.require(stage in {"triage", "clarify", "design", "spec"},
                       f"{label}: planning cannot enter delivery stages")
        report.require(close.get("verification") == "not-applicable",
                       f"{label}: planning uses verification: not-applicable (no delivery claim)")
    elif intent == "delivery":
        report.require(close.get("verification") != "not-applicable",
                       f"{label}: delivery verification cannot be not-applicable")
    if status == "completed":
        if intent == "delivery":
            report.require(stage == "closeout", f"{label}: delivery completes at closeout")
            report.require(close.get("verification") == "passed",
                           f"{label}: completed delivery needs passed verification")
            report.require(close.get("knowledge_sync") in {"complete", "not-applicable"},
                           f"{label}: completed delivery needs knowledge sync")
        elif intent == "planning":
            report.require(stage in {"clarify", "design", "spec"},
                           f"{label}: planning completes at a requested checkpoint")
    if close.get("verification") == "passed":
        for ac in acceptance:
            report.require(latest.get(ac) == "pass",
                           f"{label}: {ac} lacks latest passing evidence")
    if status == "cancelled":
        prose = re.sub(r"^[a-z_][a-z0-9_]*:.*$", "", visible(parts.get("Closeout", "")), flags=re.M)
        report.require(bool(prose.strip()) and prose.strip() != "none",
                       f"{label}: cancellation needs a disposition")
    if archived:
        report.require(status in {"completed", "cancelled"},
                       f"{label}: unfinished record in archive")
        report.require(not (intent == "planning" and status == "completed"),
                       f"{label}: completed planning stays outside delivery archive")
        match = re.fullmatch(r"(\d{4}-\d{2}-\d{2})-(" + SLUG + r")\.md", path.name)
        valid_date = False
        if match:
            try:
                datetime.date.fromisoformat(match[1])
                valid_date = True
            except ValueError:
                pass
        report.require(valid_date, f"{label}: expected valid YYYY-MM-DD-<slug>.md")
    else:
        report.require(bool(re.fullmatch(SLUG + r"\.md", path.name)),
                       f"{label}: expected kebab-case record filename")
        report.require(not (status == "completed" and intent == "delivery")
                       and status != "cancelled",
                       f"{label}: terminal delivery/cancellation left active; finish archive")


def frontmatter(path, report):
    text = read(path)
    match = re.match(r"\A---\r?\n(.*?)\r?\n---(?:\r?\n|$)", text, re.S)
    if not match:
        report.fail(f"{path.name}: missing frontmatter")
        return
    data = match[1]
    report.require(len(re.findall(r"^name:", data, re.M)) == 1,
                   f"{path.name}: name must appear once")
    report.require(bool(re.search(r"^name:\s*project-workflow\s*$", data, re.M)),
                   f"{path.name}: name must be project-workflow")
    matches = list(re.finditer(r"^description:[ \t]*(.*)(?:\n((?:[ \t]+.*\n?)*))?", data, re.M))
    report.require(len(matches) == 1, f"{path.name}: description must appear once")
    if len(matches) == 1:
        value = matches[0][1]
        if value in {">", ">-", "|", "|-"}:
            value = " ".join((matches[0][2] or "").split())
        elif value.startswith('"'):
            try:
                value = json.loads(value)
            except ValueError:
                value = None
        elif value.startswith("'"):
            value = value[1:-1].replace("''", "'") if value.endswith("'") else None
        else:
            value = re.split(r"\s+#", value, maxsplit=1)[0].strip()
            if (not value or not value[0].isalpha()
                    or value.lower() in {"null", "true", "false", "yes", "no", "on", "off"}):
                value = None
        report.require(isinstance(value, str) and 0 < len(value.strip()) <= 1024,
                       f"{path.name}: description must contain 1-1024 characters")


def validate_route(root, standalone, report):
    agents = root / "AGENTS.md"
    text = visible(read(agents)) if agents.is_file() else ""
    declarations = re.findall(r"^Workflow skill:.*$", text, re.M)
    if not declarations and standalone:
        print("INFO: standalone record validation; no installation route declared")
        return
    report.require(len(declarations) == 1, "AGENTS.md: expected one explicit Workflow skill route")
    if len(declarations) != 1:
        return
    match = re.fullmatch(r"Workflow skill: `([^`]+)`\s*", declarations[0])
    if not match:
        report.fail("AGENTS.md: route must be Workflow skill: `<path>/SKILL.md`")
        return
    target = Path(match[1]).expanduser()
    if not target.is_absolute():
        target = root / target
    if target.name != "SKILL.md" or not target.is_file():
        report.fail("AGENTS.md: declared SKILL.md does not exist; no fallback used")
        return
    frontmatter(target, report)


def project(root, standalone, report):
    validate_route(root, standalone, report)
    changes = root / "docs" / "changes"
    if changes.is_symlink() or not inside(changes.resolve(), root):
        report.fail("docs/changes: record storage must not be symlinked or escape the project")
        return
    if not changes.exists():
        return
    if not changes.is_dir():
        raise InputError("docs/changes is not a directory")
    for path in changes.rglob("*"):
        if path.is_symlink() and (path.is_dir() or not path.exists()):
            report.fail(f"{path.relative_to(root)}: symlink storage is not traversed")
    for path in sorted(changes.rglob("*.md")):
        if path.is_symlink() or not inside(path.resolve(), root):
            report.fail(f"{path.name}: change records must remain inside the project")
            continue
        parent = path.parent
        if parent not in {changes, changes / "archive"}:
            report.fail(f"{path.name}: records must be directly in changes/ or changes/archive/")
            continue
        validate_record(path, root, parent.name == "archive", report)


def heading_ids(text):
    result = set()
    counts = {}
    for title in re.findall(r"^#{1,6} +(.+?)\s*#*\s*$", visible(text), re.M):
        base = re.sub(r"[^\w -]", "", title.lower()).replace(" ", "-")
        count = counts.get(base, 0)
        counts[base] = count + 1
        result.add(base if count == 0 else f"{base}-{count}")
    return result


def skill(root, report):
    for name in RESOURCES:
        report.require((root / name).is_file(), f"missing resource {name}")
    if (root / "SKILL.md").is_file():
        frontmatter(root / "SKILL.md", report)
    paths = [root / "SKILL.md", root / "README.md"]
    for directory in ("references", "templates"):
        paths.extend(sorted((root / directory).glob("*.md")))
    for path in paths:
        if not path.is_file():
            continue
        for target in re.findall(r"\[[^\]]*\]\(([^)]+)\)", visible(read(path))):
            url = urlsplit(target.strip("<>"))
            if url.scheme or url.netloc:
                continue
            resolved = (path.parent / unquote(url.path)).resolve() if url.path else path
            report.require(inside(resolved, root), f"{path.name}: link escapes package")
            if not resolved.exists():
                report.fail(f"{path.name}: missing link {target}")
            elif url.fragment and resolved.suffix == ".md":
                report.require(unquote(url.fragment) in heading_ids(read(resolved)),
                               f"{path.name}: missing heading {target}")
    template = root / "templates/change-record.md"
    if template.is_file():
        parse_record(read(template), report, "change record template")
    routing = root / "templates/agents-block.md"
    if routing.is_file():
        report.require("Workflow skill: `<skill-path>`" in read(routing),
                       "routing template: missing explicit route")


def fingerprint(root, record_name, names):
    try:
        record = relative_file(root, record_name)
        if not record.is_file():
            raise InputError("record does not exist")
        report = Report()
        parts, _, _ = parse_record(read(record), report, record_name)
        if report.errors:
            raise InputError("; ".join(report.errors))
        mapping = {}
        for name in names:
            path = relative_file(root, name)
            if path == record or not path.is_file():
                raise InputError(f"{name}: must be an existing file other than the record")
            mapping[name] = file_digest(path)
        print("contract_sha256: " + contract_digest(parts))
        print("files: " + json.dumps(mapping, ensure_ascii=False, sort_keys=True))
    except ValueError as exc:
        raise InputError(str(exc)) from exc


def main(argv=None):
    if sys.version_info < (3, 8):
        print("ERROR: Python 3.8 or newer is required; use documented manual checks.",
              file=sys.stderr)
        return 2
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    for name in ("skill", "project", "fingerprint"):
        child = sub.add_parser(name)
        child.add_argument("root", type=Path)
        if name == "project":
            child.add_argument("--standalone", action="store_true")
        if name == "fingerprint":
            child.add_argument("record")
            child.add_argument("files", nargs="+")
    args = parser.parse_args(argv)
    try:
        root = args.root.resolve()
        if not root.is_dir():
            raise InputError("root must be an existing directory")
        if args.command == "fingerprint":
            fingerprint(root, args.record, args.files)
            return 0
        report = Report()
        if args.command == "skill":
            skill(root, report)
        else:
            project(root, args.standalone, report)
        for message in report.errors:
            print("FAIL: " + message)
        print(f"Structural check: {len(report.errors)} violation(s). "
              "Behavior, authorization and evidence coverage require review.")
        return 1 if report.errors else 0
    except (OSError, UnicodeError, InputError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
