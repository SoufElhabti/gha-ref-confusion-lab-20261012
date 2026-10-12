#!/usr/bin/env bash
set -euo pipefail

echo "controlled strong cleanup hook: removing root-owned persistence markers"
/usr/bin/sudo -n /usr/bin/rm -f /usr/local/bin/git
/usr/bin/sudo -n /usr/bin/rm -rf /opt/controlled
