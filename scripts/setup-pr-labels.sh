#!/usr/bin/env bash
# setup-pr-labels.sh — apply the canonical label taxonomy to a repo from your machine.
# Thin wrapper over labels.py; the taxonomy itself lives in ../labels.yml (single source
# of truth, also applied in CI by the label-sync.yml workflow). Idempotent & additive:
# creates a label, or updates its colour/description if it already exists — never deletes.
#
#   ./setup-pr-labels.sh <owner/repo>     # e.g. ./setup-pr-labels.sh thanasiskostaras/dotfiles
set -euo pipefail
REPO="${1:?usage: setup-pr-labels.sh <owner/repo>}"
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
exec python3 "$HERE/labels.py" "$REPO"
