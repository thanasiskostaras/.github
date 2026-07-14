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
  `uses: …/<name>.yml@<release-sha> # v1.0.0` — pin to a release SHA, not `@main`
  (supply-chain hardening, dotfiles#72; Dependabot bumps it). E.g. a standard
  lint/test workflow, a labeler, stale-issue sweeps, auto-assign).
- **Profile README** — [`profile/README.md`](profile/README.md) renders the landing page on my GitHub profile.
- Other defaults: `FUNDING.yml`, `SECURITY.md`, `SUPPORT.md`, `CODE_OF_CONDUCT.md`.

## Claude PR review (`claude-review.yml`)
[`.github/workflows/claude-review.yml`](.github/workflows/claude-review.yml) is a reusable
senior-review workflow: every PR gets an automated Claude review that leads with a verdict +
risk summary, then severity-ordered findings citing `file:line`. It runs on my **Max
subscription** via an OAuth token, so it costs **$0 in API spend**.

**Adopt it in a repo** — drop this ~10-line caller at `.github/workflows/review.yml`:

```yaml
name: Review
on:
  pull_request:
    types: [opened]
jobs:
  review:
    uses: thanasiskostaras/.github/.github/workflows/claude-review.yml@b180f60d535694c745481799f0eea6e9aed7c11e # v1.0.0
    permissions:
      contents: read
      pull-requests: write
      issues: write
    secrets: inherit   # passes CLAUDE_CODE_OAUTH_TOKEN through to the reusable workflow
```

Override the default model (`claude-sonnet-5`) with `with: { model: claude-opus-4-8 }` if needed.

**One manual step** — add the repo (or org) secret `CLAUDE_CODE_OAUTH_TOKEN`. Generate the
token once with:

```bash
claude setup-token
```

then paste it under **Settings → Secrets and variables → Actions → New repository secret**.
`secrets: inherit` in the caller forwards it into the reusable workflow.

## On-demand Claude (`claude-mention.yml`)
The reviewer above runs **automatically on every PR**. GitHub does **not** let you
request a bot from the native *Reviewers* panel, so to *summon* Claude yourself, comment
**`@claude review this`** (or any `@claude …` question) on a PR — [`claude-mention.yml`](.github/workflows/claude-mention.yml)
picks it up and responds in-thread, on the same **Max subscription** ($0 API).

Add this caller at `.github/workflows/mention.yml`:

```yaml
name: Claude on-demand
on:
  issue_comment:
    types: [created]
jobs:
  mention:
    uses: thanasiskostaras/.github/.github/workflows/claude-mention.yml@<release-sha> # vX.Y.Z
    permissions:
      contents: read
      pull-requests: write
      issues: write
    secrets:
      CLAUDE_CODE_OAUTH_TOKEN: ${{ secrets.CLAUDE_CODE_OAUTH_TOKEN }}
```

It only fires on **PR** comments that mention `@claude` **and** come from the repo owner —
random visitors can't spend the subscription quota. Note: `issue_comment` workflows always
run from the **default branch**, so `@claude` works once `mention.yml` is merged (it can't be
tested from a PR branch).
