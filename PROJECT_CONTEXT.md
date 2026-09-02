# Project Context

## What this is

`harnessie-verify-action` is a GitHub Action (Marketplace listing) that acts
as a merge gate: it verifies a pull request's claims (from its PR body, or a
supplied claims file) claim-by-claim, using deterministic sandboxed checks
plus an independent, fresh-context verifier model, rather than relying on
reviewer opinion or the author's own narrative. It is a thin composite
wrapper around the `harnessie verify` CLI from https://harnessie.com/
(Apache-2.0), pinning a tested harnessie version per release.

## Ecosystem relationship

This repository owns the GitHub Action adapter, its security boundary, tested Harnessie pin, Marketplace release, and stable-major tag. The federated Harnessie authority map and release train live in [Harnessie ECOSYSTEM.md](https://github.com/snapsynapse/harnessie/blob/main/ECOSYSTEM.md). Core releases propagate here only after the released Harnessie version passes this repository's tests; this repository does not own Harnessie product strategy or engine-wrapper claims.

Positioning line from the README: "Reviewers opine. This adjudicates."

## Audience

- Engineering teams and maintainers who want an automated, fail-closed
  merge gate for PRs — especially teams merging AI/agent-authored PRs where
  the PR description can't be trusted as evidence.
- GitHub Marketplace browsers evaluating the action for adoption (README is
  written for that audience: quickstart-first, inputs table, security
  section up front).
- Security-conscious users who care about the `pull_request_target` /
  secret-exfiltration failure mode and about keeping model egress under
  their own control (self-hosted OpenAI-compatible endpoints supported).

## Style / tone

Terse, technical, security-literate. Short declarative sentences, no
marketing fluff. Willing to state limits plainly (see README's "Limits,
honestly" section) rather than oversell. Uses precise exit-code / verdict
vocabulary consistently (VERIFIED / FAILED / CANNOT_VERIFY; 0/1/2) across
`README.md`, `action.yml`, and `CHANGELOG.md` — preserve this vocabulary
exactly in any new content.

## Key URLs

- Harnessie tool: https://harnessie.com/
- Provenance / decision records (in the sibling `harnessie` repo):
  - AIDR-0006: https://github.com/snapsynapse/harnessie/blob/main/decisions/AIDR-0006-standalone-verifier-surface-for-agent-produced-prs.md
  - AIDR-0007: https://github.com/snapsynapse/harnessie/blob/main/decisions/AIDR-0007-ship-harnessie-verify-as-a-github-action.md
- Repo remote: https://github.com/snapsynapse/harnessie-verify-action

## Current status

Release `0.2.0` pins Harnessie 1.2.0 and exposes its evidence-bundle intake
through backward-compatible action inputs while preserving the public outputs
and fail-closed verdict contract. The unsafe-trigger guard is shared by runtime and CI so the
`pull_request_target` refusal is executed rather than represented by a
permanently skipped job. Exact-version and stable-major tags promote only
after the release commit passes CI.
