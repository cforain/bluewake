# Windows build for BlueWake 0.6.0

Steps 3 to 5 of the [0.6.0 loop](../GOAL_LOOP.md), on Chris's Windows PC. Follow them in order and fill in the
results table at the end. The 0.5.0 run is the model: [Windows build for 0.5.0](WINDOWS_BUILD_0.5.0.md).

## What to build

| | |
| --- | --- |
| Commit | `2c8a659416233864ab9d7a069e759bf5af558e2b` (version 0.6.0, build 5) |
| RecompCore | `35e037f285ded1b766b7110783b47c976fe2ed10` (the builder fetches it) |
| DolRecomp | `b8b534591cba8ca7cd43943a655ee6e2591cf5de` |
| Generated source | digest `54f54434…`, the verified tree (unchanged since 0.5.0) |

## 1. Build

In PowerShell, in the BlueWake checkout:

```
git fetch
git checkout 2c8a659416233864ab9d7a069e759bf5af558e2b
git rev-parse HEAD
python scripts\windows\build.py C:\BlueWake-private\GZLE01.iso
```

Visual Studio 2026 18.10 or newer uses the app's optimization profile. With an older one the builder prints
`note: building the app without its optimization profile` and carries on (#153), which is fine for testing but
not for the release. The first build took 129 minutes for 0.5.0. Write down the build time and the clang version
the builder prints.

## 2. Checks

Use portable mode so nothing touches the real saves: put an empty `portable.txt` beside `BlueWake.exe` in the build
folder (`build\windows\BlueWake`). Saves, settings and logs then go to `user\` beside it. Logs are in `user\logs`.
Summarize each with `python scripts\triage_session_log.py LOG`. Keep the logs private.

| # | Check | How | Passes when |
| --- | --- | --- | --- |
| a | Intro music, fix on | In PowerShell: `$env:BLUEWAKE_DEFER_DVD_COMPLETION="1"`, then `.\BlueWake.exe` from that window. Wait at the title until its music plays (about 15 seconds), start a new file, enter a name, and listen through the history intro without skipping (about four minutes). | Music to the end of the intro. The log says `[dvd] deferred completion=on (BLUEWAKE_DEFER_DVD_COMPLETION)`; `1tale.afc` reaches state 4 and the triage summary says `streamed playback ended within 60 retraces: 0`. |
| b | Intro music, fix off | Close the game, `Remove-Item Env:BLUEWAKE_DEFER_DVD_COMPLETION`, run the same steps. | Recorded either way (silence is the known bug). The log says `off (default)`. |
| c | Loading with the fix on | With the variable set again: from check a, play to control on Outset, go through one door, save in the game (Start, Save), quit, start again and load that file. | The room loads, the save loads, nothing stalls. |
| d | Dungeon map | Copy the prepared test card (on Chris's Mac: `build/release-0.6.0/windows-test/GZLE01.card`, a Windfall save moved into Dragon Roost Cavern) to `user\GZLE01.card`. Load slot 1 and open the map. | The grid and the visited room are drawn, not only the door markers. The log's `[gx-core] shutdown` line has `unsupported_texgen=0` and `tev_stages_over=0`. |
| e | Quit | F1 › Quit the game. Start again. | No recovery message on the next launch; the log ends without a crash or `double free`. |
| f | Controller, if one is at hand | The controller rows in [WINDOWS_TASKS.md](../WINDOWS_TASKS.md#in-main-waiting-for-a-windows-build): player 1, the baton, the left stick, the aim option. | Each row as written there. |

Then delete the test card and `portable.txt` from the build folder before packaging. The packager only takes files on its
allowlist, but don't rely on that.

## 3. Package

```
python scripts\windows\package_release.py 0.6.0
```

This writes `build\windows\release\BlueWake-v0.6.0-windows-x64.zip` and a source zip of the same commit. Note the zip's
SHA-256 (`Get-FileHash`) and copy the zip to the Mac's `build/release-0.6.0/`. The Mac runs the release check on it.

## 4. If check a passes

Turning the intro fix on for Windows is a one-line change in `runtime/host/src/main.c`, done as its own pull request.
After it merges, check out the new commit, run `python scripts\windows\build.py` again (the game module and its
training are reused; only the app is rebuilt), repeat check a without the variable, and package again.

## Results

| Item | Result |
| --- | --- |
| Commit built | |
| Build time, clang version | |
| Module SHA-256 | |
| a. Intro, fix on | |
| b. Intro, fix off | |
| c. Loading with the fix on | |
| d. Dungeon map | |
| e. Quit | |
| f. Controller | |
| Zip SHA-256 | |
