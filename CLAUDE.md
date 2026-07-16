# CLAUDE.md

Agent guidance for working in this repo.

## Purpose

`harnessie-verify-action` is a GitHub composite Action that gates PR merges on
claim-by-claim verification instead of reviewer opinion. The PR body (or a
supplied claims file) is treated as claims to test, never as evidence:
deterministic sandboxed checks run first, then a fresh-context verifier model
(any OpenAI-compatible endpoint, no baked-in provider) checks each claim
against the actual workspace artifacts, never seeing the author's narrative.
Fail-closed exit contract: `0` VERIFIED, `1` FAILED, `2` CANNOT_VERIFY
(cannot-verify fails the job by default).

It is a thin wrapper pinning a tested version of the `harnessie verify` CLI
(https://harnessie.com/, Apache-2.0, PyPI package `harnessie`).

## Tech stack

- GitHub composite Action (`action.yml`), no build step — steps are inline
  `shell: bash` + Python one-liners.
- Runtime dependency: `harnessie` Python package, installed via `pip` at
  action-run time, version pinned by the `harnessie-version` input (default
  `0.7.1` as of this writing — check `action.yml` for current pin).
- Sandbox backends on Linux runners: bubblewrap, firejail, or docker (fail
  closed to CANNOT_VERIFY if none is admitted).
- CI: GitHub Actions (`.github/workflows/ci.yml`), fully offline via a mock
  model provider (`fixture/models-mock.yaml`) — no live model calls in CI.

## Directory layout

- `action.yml` — the composite action definition: inputs, outputs, and all
  run steps (refuse `pull_request_target`, install harnessie, probe sandbox
  backend, stage PR diff, resolve criteria/models, run `harnessie verify`,
  upload report artifact).
- `README.md` — user-facing docs: quickstart, inputs table, security model,
  exit code meanings, provenance, honest limits section.
- `CHANGELOG.md` — release notes, one entry per version.
- `fixture/` — offline CI fixtures: `claims.md` (sample claims),
  `models-mock.yaml` (mock provider config, produces no verdict by design),
  `workspace/out.txt` (sample artifact the fixture claims reference).
- `.github/workflows/ci.yml` — offline test matrix proving the exit-code
  mapping (failing check → FAILED, no sandbox/mock provider → CANNOT_VERIFY
  fail-closed and advisory-mode variants, `pull_request_target` refusal).
- `.github/FUNDING.yml` — Snap Synapse repo convention.
- `LICENSE` — Apache-2.0.

## Conventions

- Never run on `pull_request_target` with a PR-head checkout — the action
  actively refuses this trigger at runtime (secret-exfiltration pattern).
- `criteria: auto` deliberately applies zero extraction intelligence to the
  PR body (HTML comments stripped, provenance-stamped) — an action that
  authors the claims it grades is self-dealing. Don't "improve" this by
  adding model-based claim extraction.
- Model API keys arrive only via the `HARNESSIE_MODEL_API_KEY` env var, never
  as an action input — preserve this when touching `models-endpoint`.
- Deterministic checks run sandboxed and network-denied by default; the
  verifier model stays network-denied regardless of `allow-network`.
- CANNOT_VERIFY (exit 2) fails the job by default (`fail-on-cannot-verify:
  true`) — the README is explicit that converting "could not check" into a
  pass would be dishonest. Don't change this default casually.
- Decisions of consequence are recorded as AIDRs in the sibling `harnessie`
  repo (see README Provenance section: AIDR-0006, AIDR-0007), not as ad hoc
  comments here.

## Build / test (from docs — not executed by this assessment)

There is no build step. Per `README.md` and `.github/workflows/ci.yml`:

- CI (`ci.yml`) runs on push to `main` and on PRs, exercising the action
  against itself (`uses: ./`) with `fixture/models-mock.yaml` (mock
  provider, zero network calls) to prove the exit-code → job-outcome mapping:
  failing check → FAILED/exit 1; no verdict from the mock provider →
  CANNOT_VERIFY/exit 2, fail-closed by default and advisory when
  `fail-on-cannot-verify: false`; `pull_request_target` trigger → refused.
- A real VERIFIED (exit 0) run requires a live verifier endpoint
  (`models-endpoint` / `models-model` + `HARNESSIE_MODEL_API_KEY`, or a
  `models.yaml`) — this is documented as a manual dogfood step, not part of
  CI.
- To manually validate a change, follow the Quickstart in `README.md` in a
  real workflow, or run the fixture scenarios from `ci.yml` locally with
  `act` or by pushing to a branch/PR.

## Current state

- Version: `0.1.0` (per `CHANGELOG.md`), tags `v0` and `v0.1.0` on `main`.
- `main` is clean and up to date with `origin/main` as of the last check
  from this assessment; most recent commits (2026-07-09/10) were the initial
  release, a sandbox/AppArmor fix for Ubuntu 24.04 runners, Marketplace
  description trims, and a `FUNDING.yml` addition.
- No open TODOs/FIXMEs found in the tracked files. The README's own "Limits,
  honestly" section is the closest thing to a known-gaps list: CI proves
  wiring offline only; a live verifier endpoint is required for an actual
  VERIFIED run; environment-dependent claims report cannot-verify rather
  than silently passing.
