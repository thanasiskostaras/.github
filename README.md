# .github — account-wide defaults for @thanasiskostaras

This repo provides **default community health files** to every repository I own that
doesn't define its own. GitHub reads them automatically, so a fresh repo inherits sane
issue/PR structure with zero setup. A repo with its own `.github/ISSUE_TEMPLATE/` or
`CONTRIBUTING.md` overrides these (e.g. `corekit` ships its own).

> This repo is **public** because GitHub requires it — but the defaults apply to my
> **private** repos too. It contains only templates and conventions, no secrets.

## What's here
- `.github/ISSUE_TEMPLATE/` — **Task** and **Bug** issue forms + `config.yml`
- `.github/pull_request_template.md` — default PR template
- `CONTRIBUTING.md` — issue/PR conventions: small · concrete · test-verifiable · human-readable

The Task form is designed to double as a build spec: a well-formed issue flows straight
into the autonomous-run mini (`/mini run <issue#>` or Telegram `/run`), and PR comments
(`/mini fix …` / `/fix`) steer it.

## Also the home for account-wide automation
Natural place to grow shared GitHub automation without touching each repo:
- **Reusable workflows** — `.github/workflows/*.yml`, called from any repo via
  `uses: thanasiskostaras/.github/.github/workflows/<name>.yml@main` (e.g. a standard
  lint/test workflow, a labeler, stale-issue sweeps, auto-assign).
- **Profile README** — add `profile/README.md` to render a landing page on my GitHub profile.
- Other defaults: `FUNDING.yml`, `SECURITY.md`, `SUPPORT.md`, `CODE_OF_CONDUCT.md`.
