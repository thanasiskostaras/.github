# .github — account-wide defaults for @thanasiskostaras

This repo provides **default community health files** to every repository I own that
doesn't define its own. GitHub reads them automatically, so a fresh repo inherits sane
issue and PR structure with zero setup. A repo with its own `.github/ISSUE_TEMPLATE/` or
`CONTRIBUTING.md` overrides these.

> This repo is **public** because GitHub requires it — default community health files and
> the profile README only work from a public `.github` repo. The defaults still apply to my
> **private** repos. Nothing operational lives here: no secrets, no workflows, no automation.

## What's here

- `.github/ISSUE_TEMPLATE/` — **Task** and **Bug** issue forms, plus `config.yml`
- `.github/pull_request_template.md` — default PR template
- `CONTRIBUTING.md` — issue and PR conventions: small · concrete · test-verifiable · human-readable
- `profile/README.md` — renders the landing page on my GitHub profile

## What's deliberately not here

Reusable workflows, the label taxonomy and their scripts live in a **private** repo. They
never needed to be public, and a public automation surface is free reconnaissance. Only the
files GitHub obliges to be public remain in this repo.
