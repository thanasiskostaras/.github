#!/usr/bin/env bash
# setup-pr-labels.sh — create/refresh the PR-label taxonomy the pr-label.yml workflow applies.
# Idempotent: creates a label, or updates its color/description if it already exists.
#
#   ./setup-pr-labels.sh <owner/repo>            # e.g. ./setup-pr-labels.sh thanasiskostaras/dotfiles
#
# Families: Type (maintenance — enhancement/bug/documentation already ship as GitHub defaults),
# Size (size/XS…XL), Area (ci/frontend/backend/infra), Priority (priority:critical…low).
set -euo pipefail
REPO="${1:?usage: setup-pr-labels.sh <owner/repo>}"

ensure() {  # name color description
  gh label create "$1" --repo "$REPO" --color "$2" --description "$3" 2>/dev/null \
    || gh label edit "$1" --repo "$REPO" --color "$2" --description "$3" >/dev/null
  echo "  ✓ $1"
}

echo "PR-label taxonomy → $REPO"
# Type (only the one GitHub defaults don't cover)
ensure "maintenance"      "ededed" "refactor / chore / build / ci / perf / test / style"
# Size (gradient light→heavy)
ensure "size/XS"          "c2e0c6" "<10 lines changed"
ensure "size/S"           "7fd38a" "10–49 lines changed"
ensure "size/M"           "fbca04" "50–199 lines changed"
ensure "size/L"           "d93f0b" "200–499 lines changed"
ensure "size/XL"          "b60205" "500+ lines changed"
# Area
ensure "ci"               "1d76db" "CI / GitHub Actions changes"
ensure "frontend"         "5319e7" "Frontend / UI changes"
ensure "backend"          "0e8a16" "Backend / API / library changes"
ensure "infra"            "006b75" "Infrastructure / IaC / launchd changes"
# Priority (mirrors the All Work board Priority field)
ensure "priority:critical" "b60205" "Inherited from a linked issue: Critical"
ensure "priority:high"     "d93f0b" "Inherited from a linked issue: High"
ensure "priority:medium"   "fbca04" "Inherited from a linked issue: Medium"
ensure "priority:low"      "0075ca" "Inherited from a linked issue: Low"
echo "Done."
