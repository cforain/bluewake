# Windows tasks

Work that needs a Windows PC, in priority order. Elliott owns Windows; anyone with the hardware can help.
Read [AGENTS.md](../AGENTS.md) first. One pull request per task, results in the linked issue.

**You need:** Windows 10 or 11 (x64), a CPU with AVX2, a Direct3D 12 GPU, your own USA `GZLE01` revision 0
disc, and the build tools in [BlueWake on Windows](WINDOWS.md#what-you-need).

**Where things stand (October 5, 2026):** the published Windows download is still Elliott's Wind Waker
Recomp 0.4.0 build. The first Windows build from BlueWake `main` (`c56d6b6`) was built and checked on one PC
and is a draft release, `v0.5.0-windows`, waiting for Chris to run the release gate and publish it. Results:
[Windows build, October 5](status/WINDOWS_BUILD_2026-10-05.md).

## In `main`, waiting for a Windows build

Fixes and features already in `main` that the current Windows download doesn't have. Task 1 ships them;
check each one on a Windows PC and tell the linked issue. New entries are added by the pull request that
lands the change ([AGENTS.md](../AGENTS.md#keep-windows-in-step)).

| Change | Issue | What to check | 0.5.0 draft, October 5 |
| --- | --- | --- | --- |
| Pictobox photos no longer freeze the picture | #13 | Take a Pictobox photo; the game keeps drawing. | Not tested |
| Swap A and B, Swap X and Y | #55 | F1 › Controls; the swap takes effect at once. | Not tested |
| Camera no longer flips direction in water | #73 | Swim and turn the camera with the stick and the mouse. | Not tested |
| Controller button remapping | #66 | F1 › Controls › Controller buttons: change a button, confirm the game follows it, restart, confirm it was kept. | Not tested (no controller) |
| Portable mode: `portable.txt` beside `BlueWake.exe` keeps saves, settings and logs in a `user` folder beside it | #64 | With `portable.txt`, the log's `[windows] ... data=` line points to the `user` folder and saves land there; without it, `%APPDATA%\BlueWake` as before. | Partial: Aurora's caches and `imgui.ini` still go to `%APPDATA%\BlueWake` |
| Jump and Run off by default (0.4.0 has them always on) | #71 | A new install has no jump on Space or the left bumper; F1 › Mods › Jump and Run turns both on after a restart. | Default off; not pressed live |
| Smooth Motion off by default, and the "Smooth Motion paused" counter | #79 | A new install runs at 30 FPS; turning Smooth Motion on shows the counter when it pauses. | 30 FPS by default; counter not tested |
| `[music-stream]` log line | #65, #97 | A session log shows the line when the intro music starts. | Pass |
| Cutscene sound log: `[demo]`, `[demo-sound]`, `[audio-lost]` | #65, #97 | Play to the first cutscene; the log has a `[demo] end` line with `cues`, `sounds` and `missing`. | Pass: intro `cues=4 sounds=4 missing=0` |
| "Quit the game" in the settings menu; notes under Brisk Sail, Unrestricted boat and Invert camera left and right | Discord | F1: "Quit the game" next to Close ends BlueWake (and the next launch shows no recovery message); with a controller, the d-pad reaches it. F1 › Mods: the three options have a line saying what they do. | Not in 0.5.0 (merged after `c56d6b6`) |
| "Exact" sound no longer crashes at launch (fixed October 1, after 0.4.0) | #58 | F1 › Sound and files › Exact, restart: the game starts and plays sound. | Pass: started and ran with Exact on, no crash |
| A launch that crashes is recovered: the next launch starts with Fast sound and mods off, backs up `settings.ini` and says so in plain words | #58 | Turn on a mod, end `BlueWake.exe` in Task Manager within a few seconds of starting, start it again: the message shows, a `settings.ini.before-safe-mode-*` file is beside `settings.ini`, and the next normal launch has no message. | Not in 0.5.0 (merged after `c56d6b6`) |
| The camera-stick inversion now comes from a header shared with the Mac (no change intended on Windows) | #73 | F1 › Controls › "camera stick left and right inverted" on: the camera turns the same inverted way on land, swimming and on the boat. | Not in 0.5.0 (merged after `c56d6b6`) |
| Mouse buttons and keyboard keys can be changed | Discord | F1 › Controls › Mouse buttons: set the right button to B; click the game, right-click, and Link uses his sword. Keyboard keys for the GameCube buttons: give A another key; it works in game, J no longer does, and both survive a restart (`mouse_buttons=` and `key_map=` in `settings.ini`). | Not in 0.5.0 (merged after `c56d6b6`) |
| `gamecontrollerdb.txt` beside the saves adds controller mappings | #61 | Put the SDL_GameControllerDB file in `%APPDATA%\BlueWake`; the session log has `[pad] N controller mappings from ...` with N above 0, and a controller that worked before still works. | Not in 0.5.0 (merged after `c56d6b6`) |
| Older CPUs get a message instead of nothing | #77 | Task 2 below: `sde64 -nhm -- BlueWake.exe` shows "BlueWake can't run on this processor"; a normal launch is unchanged. | Not in 0.5.0 (merged after `c56d6b6`) |
| The first-launch disc prompt offers .rvz only when `nodtool.exe` is beside `BlueWake.exe` | #120 | From the release zip (no `nodtool.exe`), with no disc chosen yet: the message says .iso or .gcm and how to convert an .rvz in Dolphin, and the picker lists only *.iso and *.gcm. A self-built folder still offers .rvz. | Not in 0.5.0 (merged after `c56d6b6`) |
| Portable mode keeps Aurora's shader and pipeline caches in the `user` folder too | #64 | With `portable.txt` and no `%APPDATA%\BlueWake` folder before: after a run, `dawn_cache.db` and `pipeline_cache.db` are in `user`. `%APPDATA%\BlueWake` may still appear holding only `imgui.ini` (needs a RecompCore change). Without `portable.txt`, the caches stay in `%APPDATA%\BlueWake` as before. | Not in 0.5.0 (merged after `c56d6b6`) |


### The second Windows run (added October 5)

If the first BlueWake Windows build was made before these merged (from `c00397e` on, October 5),
rebuild from `main` and check only these rows of the table above, nothing else again (the 0.5.0 draft, built from `c56d6b6`, has none of them; Exact sound was already checked on it):

1. A launch that crashes is recovered, with the plain message (#58).
2. The camera-stick inversion from the shared header (#73).
3. Mouse buttons and keyboard keys can be changed.
4. "Quit the game" and the three option notes.
5. Older CPUs get a message instead of nothing (#77, task 2).
6. `gamecontrollerdb.txt` beside the saves adds controller mappings (#61).
7. The disc prompt offers .rvz only when `nodtool.exe` is there.
8. Portable mode keeps the shader caches in the `user` folder (#64).

## 1. A Windows build from BlueWake `main`

**Why:** ships everything in the list above to Windows players.

1. Build from a clean checkout of `main`: `python scripts/windows/build.py "D:\path\to\GZLE01.iso"`.
2. Run checks 1 to 4 of the [Windows checklist](WINDOWS_ACCEPTANCE.md), and the checks in the list above.
3. Package it like Wind Waker Recomp's releases (its `scripts/windows/package_release.py` is a starting
   point; bring it over as a pull request): `BlueWake-vX.Y.Z-windows-x64.zip` holding the build folder,
   licenses and a `BuilderProvenance.json`, **without `nodtool.exe`** (it embeds Wii keys), plus a source zip.
4. Attach both to a **draft** release on BlueWake. Chris runs the release check and publishes; nobody else
   publishes releases.

**Done when:** the draft has both zips and the checklist results are posted.

**Status (October 5, 2026):** built from `c56d6b6` and packaged with `scripts/windows/package_release.py`
(#119). The draft release `v0.5.0-windows` has both zips. The checks in the table above that need a save, a
controller or the settings menu by hand are still open.

## 2. A clear message on CPUs without AVX2 (#77)

**Why:** on an older CPU, such as an Intel Core i7 860, `BlueWake.exe` exits silently.

**In `main` (October 5):** `windows/src/win_entry.c` checks the CPU from the C runtime's initializer table
(`.CRT$XIU`, before the C++ static initializers and `main`), in functions compiled for plain x86-64, and shows a
message box instead of stopping silently. Only builds for x86-64-v3 include it. On the Mac, the same code
compiled for Windows showed the entry in `.CRT$XIU` and no AVX instructions in the check; it hasn't run on Windows.

**Done when:** under Intel SDE emulating an older CPU (`sde64 -nhm -- BlueWake.exe`), the message appears
instead of nothing, and a normal launch (and `sde64 -hsw -- BlueWake.exe`) is unchanged.

## 3. Opening the window in place (PR #89)

**Why:** the window appears and then jumps to its saved position. saulob's PR fixes that but needs
`window_pos_x` and `window_pos_y` in `AuroraBackendConfig` (RecompCore,
`GXRuntime/include/gxruntime/aurora_backend.h`), passed on to Aurora's `windowPosX` and `windowPosY`.

**Done when:** that runtime change is merged into RecompCore `bluewake-next`, pinned here, and #89 builds
and opens the window in place.

## 4. Elliott's native functions and lean memory

**Why:** `--native-entries` and `--lean-memory` are in BlueWake's Windows builder but change nothing yet.
The natives hook only where the translated code matches what Wind Waker Recomp's builder produces (0 of 15
match today), and lean memory needs the deadline test in Wind Waker Recomp's newer `fast_blocks.py`.

1. Bring Wind Waker Recomp's `fast_blocks.py` and its step order into `scripts/windows/build.py`.
2. Build with both options and check the `native-entries` log for how many certify.
3. Compare speed in the same scenes with and without them.

**Done when:** the natives certify, the speedup is measured, and the defaults are decided from the numbers.

## 5. Windows-only reports

Use `python3 scripts/triage_session_log.py session-*.log` on any attached log.

| Issue | What to do |
| --- | --- |
| #80 HD pack shading on AMD | Try the Hypatia DDS pack on Windows, with and without it; compare with the PNG pack. |
| #61 8BitDo GameCube controller | Check whether SDL sees it and what it maps to. |
| #76 Forsaken Fortress soft lock | Try to reproduce on the tower with the Moblins; it may be the original game's behaviour. |
| #74 dungeon map without its drawing | Not Windows-only: reproduced on the Mac on October 5 (see [OPEN_ISSUES_2026-10-05.md](status/OPEN_ISSUES_2026-10-05.md#what-the-october-5-loop-found)). The cause is RecompCore's shader limits, so the fix is a runtime change; nothing to capture on Windows until it lands. |
| #65, #97 missing music or sound in cutscenes | Play an affected scene (the intro after naming Link, the bird scenes) with task 1's build and read the `[demo] end` line for it (see below). The Mac plays them: the opening cutscene logs `cues=4 sounds=4 missing=0 silent=0.4s of 104.7s`. On the Mac (October 5), the opening cutscene also logs `cues=4 sounds=4 missing=0` with mouse camera off, with Better Wind Waker on and at 16:9, so if a scene is silent on Windows, the option-by-option comparison (HD textures, Better Wind Waker, mouse camera, 16:9 vs 4:3) belongs in that scene, on Windows. |
| #59, #72, #79, #86 slowdowns | Measure the scenes with the triage script. The #76 log already shows the Forsaken Fortress exterior limited by the GX worker (83 of 97 slow seconds). |

Close an issue only when the reporter confirms the fix, or with a clear explanation.

### Reading the cutscene sound lines (#65, #97)

Every build writes one `[demo] end` line per cutscene, and `[audio-lost]` when a cutscene, or the intro
story's streamed music, goes silent for 6 seconds.

| What the log shows | What it means | Where to look |
| --- | --- | --- |
| `cues=0` on a cutscene that should have sound | The cutscene never asked for its sounds: its sound track didn't run. | Settings that change game timing: the experimental 60 Hz gameplay and the native math in Wind Waker Recomp 0.4.0 (`BLUEWAKE_NATIVE_MATH=1`). Both are off in `main`. |
| `missing` above 0, with `[demo-sound] ... no sound` lines | The cutscene asked, but the game couldn't start the sound, usually because its sound data wasn't loaded in time. | Slow disc or ARAM reads; compare the slow seconds (`[fps-dip]`) around the cue. |
| `sounds` equal to `cues` but `[audio-lost]` or a long `silent=` | The sounds started but nothing reached the speakers. | The audio output: Smooth Motion (on by default in 0.4.0, off in `main`), and drops when the game falls behind real time. |
| No `[music-stream]` line with `state=4` during the intro | The streamed music never started playing. | Reading `Audiores/Stream/*.afc` from the disc image. |

On Mac, iPad and Windows `main`, the audio pacing settings are the same (`BLUEWAKE_WALL_PACE=1`,
`DOL_AUDIO_NO_THROTTLE=1`, `BLUEWAKE_CLOCK=now`), so they don't explain a Windows-only problem by
themselves. What differs on the 0.4.0 download is the native math, Smooth Motion's default and the
60 Hz option. A Windows build from `main` turns those off, so if the cutscenes have sound there, one
of them was the cause.
