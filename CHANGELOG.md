# Changelog

## 0.1.0 (2026-07-10)

Initial release, adopted via harnessie decisions/AIDR-0007 (four-provider position sweep, human-arbitrated). Composite action wrapping harnessie verify 0.7.1: claim-by-claim PR verification with a fail-closed exit contract (0 verified / 1 failed / 2 cannot-verify, cannot-verify failing by default). PR-body-verbatim auto criteria with provenance stamp and no extraction intelligence. PR diff staging for change-surface claims. pull_request_target refused at runtime. Sandbox inherited from the harness (bubblewrap/firejail/docker, fail-closed). Structured claim table to the job summary; model prose confined to the report artifact. Offline CI matrix proving the exit-code mapping with a mock provider.
