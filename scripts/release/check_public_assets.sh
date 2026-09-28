#!/usr/bin/env bash
# Check files before they are made public (release assets, source archives).
#
#   scripts/release/check_public_assets.sh FILE...
#
# Fails closed. A file fails if:
#   - it is, or contains, the translated game module (gGZLE01_recomp.dylib), a
#     disc image, main.dol, a REL, or a memory card / save file;
#   - the maintainer's release gate (~/.codex/release-gate/release_gate.py, or
#     BLUEWAKE_RELEASE_GATE) reports it; or the gate is missing or cannot run.
# Exit 0 only when every file passes.
set -uo pipefail

gate=${BLUEWAKE_RELEASE_GATE:-$HOME/.codex/release-gate/release_gate.py}
[ $# -gt 0 ] || { echo "usage: $0 FILE..." >&2; exit 2; }
if [ ! -f "$gate" ]; then
    echo "check_public_assets: release gate not found at $gate; nothing may be published" >&2
    exit 1
fi

forbidden='(^|/)(gGZLE01_recomp\.dylib|main\.dol|[^/]*\.(iso|gcm|rvz|wbfs|ciso|gcz|rel|card|gci|sav|raw))$'
status=0
for f in "$@"; do
    if [ ! -f "$f" ]; then
        echo "FAIL $f: not a file"; status=1; continue
    fi
    bad=""
    if printf '%s\n' "$f" | grep -Eiq "$forbidden"; then
        bad=$(basename "$f")
    else
        case "$f" in
            *.ipa|*.zip) bad=$(unzip -Z1 "$f" 2>/dev/null | grep -Ei "$forbidden" | head -3 | tr '\n' ' ') ;;
            *.tar|*.tar.gz|*.tgz) bad=$(tar tf "$f" 2>/dev/null | grep -Ei "$forbidden" | head -3 | tr '\n' ' ') ;;
        esac
    fi
    if [ -n "$bad" ]; then
        echo "FAIL $f: contains game module, disc or save files: $bad"; status=1; continue
    fi
    if ! python3 "$gate" "$f"; then
        status=1
    fi
done
[ $status -eq 0 ] && echo "check_public_assets: all $# file(s) passed" || echo "check_public_assets: FAILED; do not publish" >&2
exit $status
