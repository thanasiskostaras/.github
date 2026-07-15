#!/usr/bin/env python3
"""labels.py — sync the canonical labels.yml taxonomy into a repo.

    python3 scripts/labels.py <owner/repo> [path/to/labels.yml]

Idempotent and additive: creates each label, or updates its colour/description if it
already exists. It never deletes labels, so GitHub defaults and Dependabot's labels are
left alone. Drives the `gh` CLI, so it works anywhere gh is authenticated — locally, or
in CI with GH_TOKEN set. Stdlib-only on purpose (no PyYAML/yq): the mini and the GitHub
runners both have python3, nothing else guaranteed. It therefore parses only the small,
flat YAML subset labels.yml is written in — see that file's header.
"""
from __future__ import annotations

import os
import subprocess
import sys


def _unquote(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
        return value[1:-1]
    return value


def parse_labels(text: str) -> list[dict[str, str]]:
    """Parse the `labels:` list from our controlled YAML subset.

    Recognises a top-level `labels:` key followed by list items of the form
        - name: <str>
          color: <hex>
          description: <str>
    Blank lines and `#` comments are ignored. Values after the first `: ` are taken
    verbatim (then unquoted), so colons/slashes inside a description are fine.
    """
    labels: list[dict[str, str]] = []
    current: dict[str, str] | None = None
    in_list = False

    for raw in text.splitlines():
        line = raw.split("#", 1)[0].rstrip() if not raw.lstrip().startswith("#") else ""
        if not line.strip():
            continue

        if not in_list:
            if line.strip() == "labels:":
                in_list = True
            continue

        stripped = line.strip()
        if stripped.startswith("- "):
            # New list item — flush the previous one.
            if current is not None:
                labels.append(current)
            current = {}
            stripped = stripped[2:].strip()  # allow `- name: x` on one line

        if current is None:
            continue

        if ":" in stripped:
            key, _, val = stripped.partition(":")
            key = key.strip()
            if key in ("name", "color", "description"):
                current[key] = _unquote(val)

    if current is not None:
        labels.append(current)
    return [l for l in labels if l.get("name")]


def sync(repo: str, labels: list[dict[str, str]]) -> int:
    print(f"Label taxonomy → {repo}  ({len(labels)} labels)")
    failures = 0
    for label in labels:
        name = label["name"]
        color = label.get("color", "ededed")
        desc = label.get("description", "")
        create = ["gh", "label", "create", name, "--repo", repo,
                  "--color", color, "--description", desc]
        edit = ["gh", "label", "edit", name, "--repo", repo,
                "--color", color, "--description", desc]
        if subprocess.run(create, capture_output=True).returncode == 0:
            print(f"  + {name}")
            continue
        # Already exists (or a transient error) — reconcile colour/description.
        done = subprocess.run(edit, capture_output=True, text=True)
        if done.returncode == 0:
            print(f"  ✓ {name}")
        else:
            failures += 1
            print(f"  ✗ {name}: {done.stderr.strip()}", file=sys.stderr)
    if failures:
        print(f"{failures} label(s) failed.", file=sys.stderr)
        return 1
    print("Done.")
    return 0


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print("usage: labels.py <owner/repo> [labels.yml]", file=sys.stderr)
        return 2
    repo = argv[1]
    here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    path = argv[2] if len(argv) > 2 else os.path.join(here, "labels.yml")
    with open(path, encoding="utf-8") as fh:
        labels = parse_labels(fh.read())
    if not labels:
        print(f"no labels parsed from {path}", file=sys.stderr)
        return 1
    return sync(repo, labels)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
