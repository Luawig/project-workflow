#!/usr/bin/env bash
# Validate project-workflow routing and completed-change closeout.
# Run from the project root:
#   path/to/scripts/validate-project.sh
#   path/to/scripts/validate-project.sh /path/to/project
set -euo pipefail

PROJECT_ROOT=${1:-.}
if [[ ! -d "$PROJECT_ROOT" ]]; then
  echo "error: project root does not exist: $PROJECT_ROOT" >&2
  exit 1
fi

PROJECT_ROOT=$(CDPATH= cd -- "$PROJECT_ROOT" && pwd)
cd "$PROJECT_ROOT"

failures=0
warnings=0

fail() {
  echo "FAIL: $1"
  failures=$((failures + 1))
}

warn() {
  echo "WARN: $1"
  warnings=$((warnings + 1))
}

ok() {
  echo "OK: $1"
}

is_project_workflow() {
  local file=$1
  [[ -f "$file" ]] && grep -E -q '^name:[[:space:]]*project-workflow[[:space:]]*$' "$file"
}

SKILL_FILE=""

if [[ -f AGENTS.md ]]; then
  while IFS= read -r candidate; do
    candidate=${candidate#\`}
    candidate=${candidate%\`}
    if [[ "$candidate" != *SKILL.md ]]; then
      continue
    fi
    expanded=$candidate
    if [[ "$expanded" == ~* ]]; then
      expanded="${expanded/#\~/$HOME}"
    fi
    if is_project_workflow "$expanded"; then
      SKILL_FILE=$candidate
      break
    fi
  done < <(grep -oE '`[^`]+`' AGENTS.md || true)
fi

if [[ -z "$SKILL_FILE" ]]; then
  for candidate in \
    .cursor/skills/project-workflow/SKILL.md \
    .agents/skills/project-workflow/SKILL.md \
    skills/project-workflow/SKILL.md
  do
    if is_project_workflow "$candidate"; then
      SKILL_FILE=$candidate
      break
    fi
  done
fi

if [[ -z "$SKILL_FILE" ]]; then
  fail "project-workflow SKILL.md not found; AGENTS.md must point to the installed copy"
else
  ok "project-workflow at $SKILL_FILE"
fi

if [[ -f AGENTS.md ]]; then
  if grep -q "project-workflow" AGENTS.md; then
    ok "AGENTS.md references project-workflow"
  else
    fail "AGENTS.md exists but does not mention project-workflow"
  fi
else
  fail "AGENTS.md missing"
fi

if [[ -d docs ]]; then
  if [[ ! -f docs/README.md ]]; then
    warn "docs/ exists but docs/README.md is missing"
  fi
  if [[ -d docs/product && ! -f docs/product/scope.md ]]; then
    warn "docs/product/ exists but docs/product/scope.md is missing"
  fi
fi

has_open_checkbox() {
  grep -E -q "^[[:space:]]*-[[:space:]]*\[[[:space:]]\]" "$1"
}

has_checked_checkbox() {
  grep -E -q "^[[:space:]]*-[[:space:]]*\[[xX]\]" "$1"
}

flag_completed_tasks() {
  local tasks=$1
  local label=$2
  if [[ ! -f "$tasks" ]]; then
    return
  fi
  if has_checked_checkbox "$tasks" && ! has_open_checkbox "$tasks"; then
    fail "completed tasks left active: $label"
  fi
}

if [[ -d openspec/changes ]]; then
  shopt -s nullglob
  for change_dir in openspec/changes/*/; do
    base=$(basename "$change_dir")
    if [[ "$base" == "archive" ]]; then
      continue
    fi
    flag_completed_tasks "${change_dir}tasks.md" "$change_dir"
  done
  shopt -u nullglob
fi

if [[ -d docs/changes ]]; then
  shopt -s nullglob
  for record in docs/changes/*.md; do
    flag_completed_tasks "$record" "$record"
  done
  shopt -u nullglob
fi

echo
echo "failures=$failures warnings=$warnings"
if [[ "$failures" -gt 0 ]]; then
  exit 1
fi
