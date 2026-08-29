# Contributing

How we write issues and PRs here. The aim: **small, concrete, human-readable, and
machine-actionable** — good enough for a person to grok at a glance *and* for automated
tooling to build from without guessing.

## Issues

Use the **Task** form for work and the **Bug** form for defects (New issue → pick a form).

A good task is:

- **One focused outcome** — roughly a day or less. If it needs "and" to describe, split it.
- **Test-verifiable** — every acceptance criterion is provable by a command or test, and the
  verify command is named. "Works well" is not a criterion; `pytest tests/test_x.py passes` is.
- **Scoped** — say what's in, what's out, which patterns to follow, and what *not* to touch.
- **Human-readable first** — write the goal in a sentence a teammate understands, then the
  machine-checkable detail. Not a wall of JSON; not a one-liner with no acceptance criteria.

Why this shape: a well-formed task **is** the spec. Work proceeds one acceptance criterion
at a time and is only done when the named verify commands pass — so vague issues produce
confident drift, and precise ones produce mergeable PRs.

## Pull requests

- **Small and reviewable** — one logical change. Split unrelated work.
- Fill the PR template: **what & why**, **changes**, **how verified** (name the commands you ran),
  and **link the issue** (`Closes #N`).
- Keep behaviour changes documented — update the README/docs in the same PR.

## Commit authorship

Commits and PRs are authored by the repo owner. **Do not add AI co-author trailers**
(`Co-Authored-By: Claude …`) or "Generated with Claude Code" footers — the tools assist,
but the work is mine, and listing an assistant as a collaborator is misleading. Automated
runs honour this too (`includeCoAuthoredBy: false`).

## Every repo has a README

A human landing on any repo should learn what it is, how to run it, and how to work on it
from the README. Create a starter if one is missing; "a current README exists" is a
done-criterion, not a nice-to-have.
