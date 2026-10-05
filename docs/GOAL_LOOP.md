# BlueWake goal loop

## Current loop: Mac fixes for the next Windows build and Mac release, October 5, 2026

Fix the reported problems that can be fixed or reproduced on a Mac, so the next Windows build and the next
Mac release get them. A separate agent is building and checking Windows 0.5.0 on Chris's Windows PC at the
same time: it owns the Windows build, packaging and the release draft. This loop doesn't wait for it and
doesn't repeat its work.

The reports this loop works from are catalogued in
[OPEN_ISSUES_2026-10-05.md](status/OPEN_ISSUES_2026-10-05.md).

### How to work

- Targeted, not exhaustive. Each step has a time limit; when it runs out, write down what was found, mark
  the step "not finished" and move on.
- Read code and logs before running the game. Short automated runs only, one run per question. No long
  play sessions, no performance work, no repeated runs that can't tell causes apart.
- Fixes go in shared code (`runtime/host/src`, or RecompCore `bluewake-next` with the pin and patch
  export). A desktop setting goes in both menus, `runtime/host/src/settings_menu.cpp` and
  `windows/src/win_settings.cpp`, sharing a header where possible as `button_remap.h` does. Host tests
  pass and the Windows CI is green before merging, and the change gets a row under "In `main`, waiting
  for a Windows build" in [WINDOWS_TASKS.md](WINDOWS_TASKS.md) in the same pull request.
- Anything that changes gameplay, timing or rendering is off by default.
- One concern per pull request, on a `codex/<topic>` branch from `origin/main`. Never push to `main`.
- The Windows agent's files are left alone: `codex/win-*` branches, `scripts/windows/package_release.py`
  and `docs/status/WINDOWS_BUILD_*.md`.

### Every pass

1. `git fetch` and `gh pr list`. If the Windows report (`docs/status/WINDOWS_BUILD_2026-10-05.md`) has
   appeared, add its findings to the catalog; anything it shows broken in shared code moves to the front.
2. Take the first step that isn't done, make the smallest change that finishes it, and update the progress
   below.

### Steps

| Step | Limit | Done when |
| --- | --- | --- |
| 1. Catalog and loop | 30 min | The catalog lists every open issue and the Discord reports; this loop replaces the last one, which is archived. |
| 2. Replies on GitHub | 45 min | #58, #66, #64, #65, #108, #70, #75, #60, #61 and #57 are answered in Chris's voice and labeled. Nothing is closed. Discord reports get no replies. |
| 3. Exact sound crash (#58) | 1 h | Exact works, or a crash with it on can't trap the player: the next launch uses Fast and says so. |
| 4. Camera invert and settings that revert | 45 min | Each camera control does one clear thing and Controls settings survive a restart on the Mac, or the cause is written up. |
| 5. Mouse buttons and keyboard rebinding | 2 h | In both menus, the right, middle and side mouse buttons can press any GameCube button (or nothing) and the keyboard keys can be changed; on the Mac, right-click set to B presses B and survives a restart. |
| 6. Small menu fixes | 45 min | Windows has the Mac's "Quit the game" button; Brisk Sail and Unrestricted Boat have plain descriptions in both menus. |
| 7. Dungeon map and sea charts (#74) | 1.5 h | Reproduced on the Mac and fixed or explained, or shown not to happen on the Mac and written up for Windows. Without a save that reaches a dungeon after 20 minutes, ask Chris and move on. |
| 8. Cutscene sound (#65, #97) | 1 h | One opening-cutscene run per option (Better Wind Waker, mouse camera, 16:9 vs 4:3, HD textures if installed), each `[demo] end` line recorded, and either the cause fixed or the result written down. |
| 9. Forsaken Fortress map and compass | 30 min | Code reading shows whether a BlueWake patch hands them out; fixed if so, written up if not. |
| 10. Hand-off for the second Windows run | 15 min | When steps 3 to 6 are merged, WINDOWS_TASKS.md lists exactly the new rows the Windows PC should check. |

Not in this loop: performance (#86, Steam Deck), ultrawide (#70), the graphics hotkey (#108), Android, the
European disc, the Wii U interface, reviewing PRs #106 and #107, and releases (only Chris publishes).

Stop when steps 1 to 10 are done or blocked, and say which. A step that needs Windows hardware is done once
it is written up in WINDOWS_TASKS.md; finishing doesn't depend on the Windows PC.

### Progress

- October 5: loop written; catalog added (step 1).

Earlier loops are in [the archive](archive/GOAL_LOOP_HISTORY.md).
