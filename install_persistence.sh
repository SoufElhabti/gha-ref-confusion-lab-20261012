#!/usr/bin/env bash
set -euo pipefail

sudo install -d -m 0755 /opt/controlled
sudo install -m 0755 controlled_capture.py /opt/controlled/capture.py
sudo install -m 0755 controlled_git_wrapper.sh /usr/local/bin/git

echo "Installed the controlled Git wrapper; the administrator cleanup hook should remove it."
