#!/bin/bash
# Pre-commit key-leak scan: fails if any actual secret VALUE from either .env
# appears in staged content. Never prints the values themselves.
set -euo pipefail
REPO="$(cd "$(dirname "$0")/../.." && pwd)"
LEAK=0
for ENVFILE in "$REPO/.env" "$HOME/Desktop/Blueprint-GTM-Skills/.env"; do
  [ -f "$ENVFILE" ] || continue
  while IFS= read -r line; do
    case "$line" in
      \#*|"") continue ;;
    esac
    val="${line#*=}"
    val="${val%\"}"; val="${val#\"}"
    [ "${#val}" -lt 12 ] && continue
    if git -C "$REPO" diff --cached | grep -qF -- "$val"; then
      name="${line%%=*}"
      echo "LEAK DETECTED: value of $name appears in staged changes" >&2
      LEAK=1
    fi
  done < "$ENVFILE"
done
if [ "$LEAK" -eq 1 ]; then
  echo "COMMIT BLOCKED — remove the secret from staged files first." >&2
  exit 1
fi
echo "keyscan: clean"
