# Changelog

## 0.2.0 (2026-09-01)

Pin the tested default to Harnessie 1.2.0 and expose its v1 evidence-bundle adoption contract through `evidence-bundle` and `evidence-root` inputs. Raw criteria and `criteria: auto` remain backward compatible; an explicit criteria path plus a bundle is rejected as ambiguous. Bundle mode skips PR.diff staging so the action cannot invalidate the bundle's exact dirty-state claim, and recorded bundle commands remain evidence rather than executable input. Action values now cross into Bash through environment variables, shortcut model configuration is serialized without shell interpolation, verifier prose is confined to the report artifact as documented, and third-party actions are pinned to immutable commits. CI constructs exact-revision, content-addressed bundles outside the workspace and proves valid, failed-check, and stale-preflight paths. The action preserves its public outputs and fail-closed verdict contract (VERIFIED / FAILED / CANNOT_VERIFY; 0/1/2).

## 0.1.3 (2026-08-20)

Pin the tested default to Harnessie 1.1.0. The `harnessie verify` CLI contract is unchanged between 1.0.0 and 1.1.0, so the action's public inputs, outputs, and fail-closed verdict contract (VERIFIED / FAILED / CANNOT_VERIFY; 0/1/2) are preserved. Harnessie 1.1.0 was installed from the live PyPI index before this pin advanced; this repository's fixture matrix remains the release gate.

## 0.1.2 (2026-08-19)

Pin the tested default to Harnessie 1.0.0. The `harnessie verify` CLI contract is unchanged between 0.8.0 and 1.0.0, so the action's public inputs, outputs, and fail-closed verdict contract (VERIFIED / FAILED / CANNOT_VERIFY; 0/1/2) are preserved. Verified against a fresh-venv PyPI 1.0.0 install with the fixture mock provider mapping a failing check to exit 1.

## 0.1.1 (2026-08-04)

Pin the tested default to Harnessie 0.8.0 while preserving the action's public inputs, outputs, and fail-closed verdict contract. Extract the `pull_request_target` refusal into one runtime script shared by the action and CI, replacing a conditional CI job that could never run under the workflow's configured events. The offline matrix now executes both the unsafe-trigger refusal and safe-trigger admission alongside the FAILED and CANNOT_VERIFY mappings.

## 0.1.0 (2026-07-10)

Initial release, adopted via harnessie decisions/AIDR-0007 (four-provider position sweep, human-arbitrated). Composite action wrapping harnessie verify 0.7.1: claim-by-claim PR verification with a fail-closed exit contract (0 verified / 1 failed / 2 cannot-verify, cannot-verify failing by default). PR-body-verbatim auto criteria with provenance stamp and no extraction intelligence. PR diff staging for change-surface claims. pull_request_target refused at runtime. Sandbox inherited from the harness (bubblewrap/firejail/docker, fail-closed). Structured claim table to the job summary; model prose confined to the report artifact. Offline CI matrix proving the exit-code mapping with a mock provider.
