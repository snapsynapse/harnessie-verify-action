#!/usr/bin/env bash
set -euo pipefail

# pull_request_target with a PR-head checkout hands the PR author repository
# privileges. This action refuses to be part of that pattern. The optional
# positional event name is a narrow test seam; runtime uses GITHUB_EVENT_NAME.
event_name="${1:-${GITHUB_EVENT_NAME:-}}"

if [ "$event_name" = "pull_request_target" ]; then
  echo "::error::harnessie-verify-action must run on pull_request, never pull_request_target. See README: safe trigger pattern."
  exit 1
fi
