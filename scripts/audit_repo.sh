#!/usr/bin/env bash
# BlueWake repository safety audit (P0)
set -euo pipefail

fail=0
tracked=$(git ls-files)

echo "=== BlueWake repository audit ==="

for pattern in "*.iso" "*.gcm" "*.rvz" "*.nfs" "*.wbfs" "*.wia" "*.ciso" "*.gcz" "*.dol" "*.rel"; do
  matches=$(echo "$tracked" | grep -i "$pattern" || true)
  if [ -n "$matches" ]; then echo "FAIL: tracked file matching $pattern: $matches"; fail=1; fi
done

for dir in "ref/" "local-research/" "generated/" "build"; do
  matches=$(echo "$tracked" | grep "^${dir}" || true)
  if [ -n "$matches" ]; then echo "FAIL: tracked files under ${dir}: $matches"; fail=1; fi
done

for pattern in "*.sav" "*.gci" "*.p12" "*.mobileprovision" "*.provisionprofile" "dolphin_*.bin"; do
  matches=$(echo "$tracked" | grep -i "$pattern" || true)
  if [ -n "$matches" ]; then echo "FAIL: tracked sensitive file matching $pattern: $matches"; fail=1; fi
done

if [ ! -f config/dependencies.lock.json ]; then
  echo "FAIL: config/dependencies.lock.json missing"; fail=1
elif ! python3 -c "import json; json.load(open('config/dependencies.lock.json'))" 2>/dev/null; then
  echo "FAIL: config/dependencies.lock.json is not valid JSON"; fail=1
else
  echo "OK: dependency lock is valid JSON"
fi

for f in docs/status/CURRENT.md docs/status/GATES.md docs/status/BLOCKERS.md docs/status/DECISIONS.md docs/status/COMPATIBILITY.md docs/status/PERFORMANCE.md docs/status/RELEASE.md tests/coverage/catalog.json; do
  if [ ! -f "$f" ]; then echo "FAIL: required ledger $f missing"; fail=1; fi
done

if [ "$fail" -eq 0 ]; then echo "AUDIT PASS"; else echo "AUDIT FAIL"; exit 1; fi
