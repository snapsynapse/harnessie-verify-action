# Changelog

## 0.1.2 (2026-08-19)

Pin the tested default to Harnessie 1.0.0. The `harnessie verify` CLI contract is unchanged between 0.8.0 and 1.0.0, so the action's public inputs, outputs, and fail-closed verdict contract (VERIFIED / FAILED / CANNOT_VERIFY; 0/1/2) are preserved. Verified against a fresh-venv PyPI 1.0.0 install with the fixture mock provider mapping a failing check to exit 1.

## 0.1.1 (2026-08-04)

Pin the tested default to Harnessie 0.8.0 while preserving the action's public inputs, outputs, and fail-closed verdict contract. Extract the `pull_request_target` refusal into one runtime script shared by the action and CI, replacing a conditional CI job that could never run under the workflow's configured events. The offline matrix now executes both the unsafe-trigger refusal and safe-trigger admission alongside the FAILED and CANNOT_VERIFY mappings.

## 0.1.0 (2026-07-10)

Initial release, adopted via harnessie decisions/AIDR-0007 (four-provider position sweep, human-arbitrated). Composite action wrapping harnessie verify 0.7.1: claim-by-claim PR verification with a fail-closed exit contract (0 verified / 1 failed / 2 cannot-verify, cannot-verify failing by default). PR-body-verbatim auto criteria with provenance stamp and no extraction intelligence. PR diff staging for change-surface claims. pull_request_target refused at runtime. Sandbox inherited from the harness (bubblewrap/firejail/docker, fail-closed). Structured claim table to the job summary; model prose confined to the report artifact. Offline CI matrix proving the exit-code mapping with a mock provider.
