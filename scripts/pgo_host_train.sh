#!/usr/bin/env bash
# Train the host's profile for profile-guided builds (macOS host and the iOS app).
#
# usage: scripts/pgo_host_train.sh
# Builds the instrumented host (scripts/pgo_host.sh gen), runs four training
# routes one game at a time, and merges the profile into
# build/host-pgo-gen/prof/merged.profdata, the path build/ios-sim and
# scripts/pgo_host.sh use read. Then rebuild: scripts/pgo_host.sh use
# build/host-pgo-gen/prof/merged.profdata for the macOS host, and a clean
# rebuild of build/ios-sim for the app (ninja does not track the profile).
#
# The fourth route is rendered (Aurora, the GX worker and the frame path),
# which the headless routes never reach: adding it took the rendered save view
# from 459/460 to 432/433 M instructions per 100 retraces on the macOS host and
# the simulator's heavy view from 1,246/1,252 to 1,176/1,182 G instructions per
# run (docs/status/CURRENT.md, 2026-09-24). Retrain after changing hot host code:
# a changed function loses its profile.
set -euo pipefail
cd "$(dirname "$0")/.."
scripts/one_game_guard.sh
bash scripts/pgo_host.sh gen >/dev/null
P=$PWD/build/host-pgo-gen
mkdir -p "$P/prof"
old=$P/prof/previous-$(date +%Y%m%d-%H%M%S)
mkdir -p "$old"
for f in "$P"/prof/*.profraw "$P"/prof/merged.profdata; do
    [ -e "$f" ] && mv "$f" "$old"/
done
export BLUEWAKE_PLAY_HOST=$P/bluewake_host
card=local-research/ipad/acceptance-20260923-095148/save.card
script=$(python3 -c "print(','.join('%d:0x0100:2' % p for p in range(340, 1601, 60)))")
LLVM_PROFILE_FILE=$P/prof/a-%p.profraw scripts/play.sh --headless --route --retraces 14700 | grep -a stopped
LLVM_PROFILE_FILE=$P/prof/b-%p.profraw scripts/play.sh --headless --route-full --retraces 21500 | grep -a stopped
LLVM_PROFILE_FILE=$P/prof/c-%p.profraw BLUEWAKE_PAD_SCRIPT=$script BLUEWAKE_PAD_CONFIRM_EVENT=any \
    scripts/play.sh --headless --route --card "$card" --retraces 3000 | grep -a stopped
LLVM_PROFILE_FILE=$P/prof/d-%p.profraw BLUEWAKE_PAD_SCRIPT=$script BLUEWAKE_PAD_CONFIRM_EVENT=any \
    scripts/play.sh --route --card "$card" --retraces 3000 | grep -a stopped
xcrun llvm-profdata merge -o "$P/prof/merged.profdata" "$P"/prof/*.profraw
ls -la "$P/prof/merged.profdata"
