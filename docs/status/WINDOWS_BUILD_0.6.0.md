# Windows build for BlueWake 0.6.0

Steps 3 to 5 of the [0.6.0 loop](../GOAL_LOOP.md), written so Codex on Chris's Windows PC can run them on its own.
Chris only has to say:

> Pull the latest chrissotraidis/bluewake and follow docs/status/WINDOWS_BUILD_0.6.0.md as a goal loop until its
> hand-off is done.

When the hand-off is done, Codex on Chris's Mac checks the zip, finishes the release with all five files, and Chris
publishes it. Nothing is copied between the computers by hand: the zip travels as a file on a **draft** GitHub
release, and the results travel as a pull request.

## Rules for the Windows agent

- Read [AGENTS.md](../../AGENTS.md) first. Use the BlueWake checkout already on this PC, or clone
  `https://github.com/chrissotraidis/bluewake` if there is none.
- Do only what this file says: no refactors, no extra tests, no code edits. If a step fails, stop, show the error
  with your best read of the cause, and wait for Chris.
- Never touch the real saves in `%APPDATA%\BlueWake`: read them only, and test in portable mode. Logs, the game
  module, the disc and saves stay on this PC; quote summary lines from logs, never attach them.
- Ask Chris only for what needs a person: watching, listening, pressing buttons, or the disc path if you can't
  find it. One short instruction at a time, saying exactly what to look or listen for. Read the logs yourself.
- The release stays a draft. Don't publish it, don't comment on issues, don't push to `main`.

## What to build

| | |
| --- | --- |
| Branch | `codex/intro-music-default-windows` ([#172](https://github.com/chrissotraidis/bluewake/pull/172)): current `main` plus the intro-music fix on by default for Windows. Its game and app code is the 0.6.0 candidate `2c8a659` except that one line; the rest is docs and test scripts. |
| Fallback | `2c8a659416233864ab9d7a069e759bf5af558e2b`, the candidate with the fix off, used only if check a fails. It has an older copy of this file, so keep this one open. |
| RecompCore | `35e037f285ded1b766b7110783b47c976fe2ed10` (the builder fetches it) |
| Version | 0.6.0, build 5 |

## The loop

**1. Sync and build.** `git fetch origin`, `git checkout --detach origin/codex/intro-music-default-windows`, and note
`git rev-parse HEAD`. Then `git diff --stat 2c8a659 HEAD -- runtime windows apple config patches scripts/builder scripts/windows version.json`
must list only `runtime/host/src/main.c`; if it lists anything else, stop and tell Chris. Find the disc:
`C:\BlueWake-private\GZLE01.iso` or `%APPDATA%\BlueWake\GZLE01.iso`; otherwise ask Chris. Then:

```
python scripts\windows\build.py DISC
```

The first build takes about two hours. Start it and check on it now and then. Note the build time, the clang version
it prints, and the SHA-256 of `build\windows\BlueWake\gGZLE01_recomp.dll`. If it prints `building the app without its
optimization profile`, stop and tell Chris: the release needs Visual Studio 2026 18.10 or newer (#153).

**2. Prepare.** Put an empty `portable.txt` beside `build\windows\BlueWake\BlueWake.exe`: saves, settings and logs then
go to `build\windows\BlueWake\user\`, which starts with an empty card. Start every run from a PowerShell window in
that folder with `.\BlueWake.exe`. After each run, summarize the newest file in `user\logs` with
`python scripts\triage_session_log.py LOG` and judge it against the table.

Before check c, close the game and replace the portable card with a test save made from a copy of Chris's own card
(his card is only read):

```
python scripts\card_set_restart.py %APPDATA%\BlueWake\GZLE01.card build\windows\BlueWake\user\GZLE01.card M_NewD2 0 0
```

Quest log 1 then starts in Dragon Roost Cavern. If the card is missing or slot 1 is empty, ask Chris which slot holds
a save and pass it as the last argument; if he has none, skip check c and say so.

**3. Checks.**

| # | Check | Chris does | Passes when |
| --- | --- | --- | --- |
| a | Intro music, default (no variable set) | Waits at the title **until its music plays** (about 15 s), starts a new file, names Link, and listens through the history intro without skipping until the scrolls end. Then quits. | Chris hears music to the end. The log has `[dvd] deferred completion=on (default)`, and the triage says `streamed playback ended within 60 retraces: 0` with `1tale.afc` reaching state 4. |
| b | Intro, fix off | `$env:BLUEWAKE_DEFER_DVD_COMPLETION="0"`, the same route, stopping once the scrolls start. Then `Remove-Item Env:BLUEWAKE_DEFER_DVD_COMPLETION`. | Recorded either way. Expected: silence, `off (BLUEWAKE_DEFER_DVD_COMPLETION)`, `1tale.afc` stopping within 60 retraces. This shows the fix is what makes the difference. |
| c | Load, dungeon map, save, quit | Loads quest log 1 (Dragon Roost Cavern), opens the map with D-pad right (right arrow key), closes it, walks through one door, saves (Start, Save), quits with F1 › Quit the game, starts again and loads the same file. | The map shows its grid and rooms, not only the door marker. The room and the save load without a stall. No recovery message on the second launch. The first log's `[gx-core] shutdown` line has `unsupported_texgen=0` and `tev_stages_over=0`, and it ends without a crash or `double free`. |
| d | Controller, only if one is at hand | The rows in [WINDOWS_TASKS.md](../WINDOWS_TASKS.md#in-main-waiting-for-a-windows-build): player 1, the baton, the left stick, the aim option. | Each row as written there. |

**If a fails:** check out the fallback commit, run `build.py` again (the game module is reused; only the app is
rebuilt), repeat c's quit and relaunch once, and package that build. The release notes then say how to turn the fix on.

**4. Package.** Delete `user\GZLE01.card` and `portable.txt` from the build folder, then:

```
python scripts\windows\package_release.py 0.6.0
```

Note the SHA-256 of `build\windows\release\BlueWake-v0.6.0-windows-x64.zip` (`Get-FileHash`).

**5. Hand-off.**

1. Upload the Windows zip to the draft release, creating the draft if it doesn't exist yet:
   ```
   gh release view v0.6.0 || gh release create v0.6.0 --draft --title "BlueWake 0.6.0" --notes "Draft. The Windows build is from Chris's PC; the Mac finishes the release."
   gh release upload v0.6.0 build\windows\release\BlueWake-v0.6.0-windows-x64.zip --clobber
   ```
   Check with `gh release view v0.6.0` that it is still a draft. Upload only this zip.
2. On a branch `codex/windows-0.6.0-results` from `origin/main`, fill in the Results table below and open a pull
   request "Windows 0.6.0 build results" with no log files attached.
3. Tell Chris it's done, with the results table and the pull request link. Then stop.

## Results

| Item | Result |
| --- | --- |
| Commit built (and whether the fallback was used) | |
| Build time, clang version, optimization profile used | |
| Module SHA-256 | |
| a. Intro, default | |
| b. Intro, fix off | |
| c. Load, dungeon map, save, quit | |
| d. Controller | |
| Zip SHA-256, uploaded to the v0.6.0 draft | |

## After the hand-off (Codex on the Mac)

Download the zip from the draft and compare its SHA-256. Run `scripts/release/check_public_assets.sh` on it (the only
accepted finding is `containsTranslatedGameCode: true`). If check a passed, merge #172 and rebuild the source zip
and the iPhone/iPad IPA from that commit. Then upload all five assets with `SHA256SUMS` and the notes to the draft,
and Chris publishes.
