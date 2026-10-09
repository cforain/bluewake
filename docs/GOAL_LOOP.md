# BlueWake goal loop: 0.6.1 and the speed measurement

Updated October 9, 2026. The 0.6.0 loop is finished and kept in
[archive/GOAL_LOOP_2026-10-08.md](archive/GOAL_LOOP_2026-10-08.md). What to work on after this is in
[PRIORITIES.md](PRIORITIES.md); the speed plan is [PERFORMANCE.md](PERFORMANCE.md).

## Goal

One build day (planned for October 10, when Chris has the compute) makes two things from **one commit of `main`**:

1. **0.6.1**, a small release of what's in `main` since 0.6.0. These are fixes only; nothing changes gameplay or
   timing. It ships as usual: the ready-made Windows build, the iPhone and iPad app without game code, the source
   and the PadMint recipe.
2. **A `--lean-blocks` build of the same commit**, not released. It is measured against the 0.6.1 build to see
   whether Elliott's lean block copies close the 30% speed gap ([PERFORMANCE.md](PERFORMANCE.md), phase 4).

## What 0.6.1 contains

| Change | Issue | Ships to | Checked so far | Still to check |
| --- | --- | --- | --- | --- |
| Controllers plugged in at launch get the smooth stick and play as player 1 (pdale-boop, #195) | #138, #155 | Windows, Mac, Linux | pdale-boop on Windows with two controllers; a test in CI | Mac with a controller at launch |
| Portable mode keeps controller remaps, keyboard bindings and `imgui.ini` in the `user` folder (#184) | #64 | Windows | CI | A Windows PC ([WINDOWS_TASKS.md](WINDOWS_TASKS.md)) |
| The window opens in place: centred, then where you left it (saulob, #197; RecompCore patch 0161) | #89 | Windows | CI, once merged | A Windows PC |
| Linux builds from source (jkoehler11, #107) | #56 | Linux | Two laptops and a Steam Deck | A package audit before any Linux download |

Not in 0.6.1: `--lean-blocks` on by default (it needs the measurement and Chris's decision), the Smooth Motion
pacing and renderer-fallback fixes (PERFORMANCE.md phase 2, not written yet), Android (#93).

## Steps

| # | Step | Who | Done when |
| --- | --- | --- | --- |
| 1 | **Freeze.** Merge #196 (`--lean-blocks`) and #197 (fast-forward RecompCore `bluewake-next` to #19's commit first). Set `version.json` to 0.6.1 build 6, fill in [RELEASE_0.6.1.md](status/RELEASE_0.6.1.md) and record the commit. | Codex | CI green; the commit written in the record |
| 2 | **Windows 0.6.1.** `python scripts\windows\build.py DISC` from the commit, as for 0.6.0. Check the three Windows rows in WINDOWS_TASKS.md: a controller connected at launch, portable remaps, the window in place. Keep a copy of the build folder for step 3. | Chris's PC or a contributor | Build made, rows checked |
| 3 | **The speed build.** Same commit, same machine: `build.py DISC --lean-blocks --out build\windows-lean`. It reuses the translation; only preparation, training and the compile repeat. | Same machine | Build made |
| 4 | **Measure.** From save states made once from your own card (PERFORMANCE.md, "How to test"): Outset, the bird scene and Tower room 0, headless and rendered, unpaced, both builds. Then play the lean build for 30 minutes: Outset, a cutscene with music, Dragon Roost Cavern, sailing, a fight. | Chris, or pdale-boop / jkoehler11, who offered | A row in PERFORMANCE.md's "Results" |
| 5 | **Apple.** `scripts/builder/build.sh --app-only --ipa BlueWake-v0.6.1-ios-unsigned.ipa`, PadMint's `audit` and `scripts/release/check_public_assets.sh`. No game build is needed for this. | Codex, on the Mac | Every check passes |
| 6 | **Package and publish.** The Windows zip into a **draft** release, the release check on every asset, `SHA256SUMS`, the notes. Chris publishes. | Codex prepares; Chris publishes | Release live; each issue above told |
| 7 | **Decide on lean blocks.** If step 4 shows Outset at least 10% faster and the play went cleanly, Chris decides the acceptance standard ([PERFORMANCE.md](PERFORMANCE.md#decisions)) and whether `--lean-blocks` becomes the default for 0.7.0. | Chris, with Elliott | Recorded in PERFORMANCE.md |

## Rules for each turn

1. Read [AGENTS.md](../AGENTS.md), check `main`, open pull requests and new issue replies before acting.
2. Never move a result from one build to another. The 0.6.1 build and the lean build come from the same commit,
   and each result names its build.
3. Builds, game modules, discs, cards, save states and logs stay private. Only the release assets are uploaded.
4. A second `build.py` run into the same folder can fail at `native-game-math` (pdale-boop, #59; a fix is
   offered). Until it's merged, use a fresh `--out` folder for each build.
