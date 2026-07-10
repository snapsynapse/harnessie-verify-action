# harnessie-verify-action

Claim-by-claim verification of pull requests, as a merge gate. The PR body is treated as claims to test, never as evidence: your deterministic checks run first (sandboxed, exit codes only), then a fresh-context verifier model that never sees the author's narrative tests each claim against the actual artifacts. Fail-closed: 0 verified, 1 failed, 2 cannot-verify, and cannot-verify fails the job by default because unverified is not passed.

Reviewers opine. This adjudicates.

Powered by [`harnessie verify`](https://harnessie.com/) (Apache-2.0). The action is a thin composite wrapper pinning a tested harnessie version; the verifier model is yours, any OpenAI-compatible endpoint, including one on your own infrastructure, so untrusted diffs never have to leave machines you control.

## Quickstart (the safe pattern)

```yaml
name: verify-pr-claims
on:
  pull_request:        # NEVER pull_request_target; see Security
jobs:
  verify:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0            # enables change-surface claims via PR.diff
      - uses: snapsynapse/harnessie-verify-action@v0
        with:
          criteria: auto            # claims = the PR body, verbatim
          checks: |
            python3 -m pytest tests/ -q
          models-endpoint: ${{ vars.VERIFIER_ENDPOINT }}
          models-model: ${{ vars.VERIFIER_MODEL }}
        env:
          HARNESSIE_MODEL_API_KEY: ${{ secrets.VERIFIER_API_KEY }}
```

That is the whole install. The job summary gets a claim-by-claim table; the full report and proof artifacts upload as a workflow artifact; the exit code gates the merge.

## Inputs

| Input | Default | What it does |
|---|---|---|
| `criteria` | `auto` | Path to a claims file, or `auto` to use the PR body verbatim (HTML comments stripped, provenance-stamped). Auto applies no extraction intelligence, deliberately: an action that authors the claims it grades is self-dealing. |
| `checks` | none | Deterministic check commands, one per line, run sandboxed in the workspace. |
| `models` | none | Path to a Harnessie `models.yaml` in your repo (full control: tiers, fallbacks, local endpoints). |
| `models-endpoint` / `models-model` | none | Shortcut for a single OpenAI-compatible endpoint when you have no models.yaml. Key arrives via the `HARNESSIE_MODEL_API_KEY` env var, never as an input. |
| `allow-network` | `false` | Let check commands use the network. The verifier agent stays network-denied regardless. |
| `stage-diff` | `true` | Write the PR diff to `PR.diff` in the workspace so claims like "docs-only" and "additive" are checkable. Needs `fetch-depth: 0`. |
| `fail-on-cannot-verify` | `true` | Exit 2 fails the job. Set `false` for advisory mode; the job passes with a warning stating that nothing was verified. |
| `report-artifact` | `true` | Upload report.md plus proof files as a workflow artifact. |
| `harnessie-version` | pinned | The harnessie release this action version is tested against. Override at your own risk. |
| `max-steps` | `20` | Verifier agent step ceiling. |

Outputs: `verdict` (VERIFIED / FAILED / CANNOT_VERIFY), `exit-code`, `report-path`.

## Security

- Use `on: pull_request`. Never `pull_request_target` with a checkout of the PR head: that pattern hands the PR author your secrets. The action detects `pull_request_target` and refuses to run.
- Deterministic checks execute the PR's code, exactly like your normal CI running PR tests, with the same GitHub protections (fork PRs get no secrets). Checks additionally run inside an OS sandbox under harness control (bubblewrap, firejail, or docker on Linux runners) and are network-denied unless you opt in. No sandbox backend means checks are blocked and the run reports cannot-verify; nothing ever runs unsandboxed.
- The verifier model reads workspace artifacts as data. Model-generated prose goes to the report artifact; what returns to the PR page is the structured claim table.
- Sending diff content to a model is an egress decision. For repositories where that matters, point `models-endpoint` at infrastructure you control.

## What the exit codes mean

- `0` VERIFIED: every check passed and every claim was reproduced against the artifacts.
- `1` FAILED: a check failed or the verifier refuted a claim. The report names which and why.
- `2` CANNOT_VERIFY: the infrastructure could not earn a verdict (no sandbox backend, provider error, missing config). Neither pass nor fail was earned, and by default that blocks the merge, because a gate that converts "could not check" into confidence is lying.

## Provenance

The tool's first real run refuted a claim in its own author's PR; the description was corrected and only then did it verify. The decision record behind the standalone verify surface, and behind this action, are public AIDRs in the harnessie repo: [AIDR-0006](https://github.com/snapsynapse/harnessie/blob/main/decisions/AIDR-0006-standalone-verifier-surface-for-agent-produced-prs.md), [AIDR-0007](https://github.com/snapsynapse/harnessie/blob/main/decisions/AIDR-0007-ship-harnessie-verify-as-a-github-action.md).

## Limits, honestly

- CI here proves the wiring and the fail-closed mapping offline (mock provider). A VERIFIED run requires your live verifier endpoint.
- Claims needing an environment the runner does not have (another OS, live credentials, a device) are reported as not verifiable, never silently passed.
- This is not a review bot. It posts no opinions, no suggestions, no comments. It answers one question: is the PR's own story true?

Apache-2.0.
