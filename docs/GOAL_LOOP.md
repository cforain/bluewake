# BlueWake goal loop

## Current loop: cutscene audio, PadMint and fixes Windows can pick up, October 4, 2026

Find out why cutscenes lose their music and sound effects without needing play sessions to do it,
confirm that the PadMint path players are told to use works, and land small fixes that Elliott's Windows
build gets just by building from `main`.

### Limits

- One Apple Silicon Mac. No Windows PC and no physical iPad in this loop. Anything that needs one goes
  into [WINDOWS_TASKS.md](WINDOWS_TASKS.md) or is labeled `needs-device`.
- No long play sessions. Short automated runs are fine to confirm that new log lines appear.
- Follow [Keep Windows in step](../AGENTS.md#keep-windows-in-step): shared code first, both desktop menus,
  Windows CI green, and the Windows check listed.
- No new platforms or features beyond what players asked for. Anything risky is off by default.

### Steps

| Step | Done when |
| --- | --- |
| 1. Audio logging | Every build (Mac, iPad, Windows) writes `[audio]` lines when something changes: whether a cutscene or event is running, the state and volume of the background music and the streamed track, how loud the output is, and samples the host dropped. An `[audio-lost]` line marks music or all sound going quiet while the game runs, with the scene and the game's speed. `scripts/triage_session_log.py` summarizes them. A short automated Mac run shows the lines and the Windows CI passes. |
| 2. Audio code review | Each difference between Wind Waker Recomp 0.4.0 and `main` that can affect sound timing has been checked in the code: Smooth Motion's in-between frames, the experimental 60 Hz gameplay (in 0.4.0 only), the native function replacements, DSP and streamed-music handling, and slow frames. Any that can drop cutscene audio is fixed in shared code or turned off by default, or written up in WINDOWS_TASKS.md with the log lines that would confirm it. |
| 3. PadMint confirmation | The player path, `padmint make bluewake ios` from the published release and a disc, runs on this Mac to a finished IPA that passes PadMint's audit. The time and result are in [PADMINT_HANDOFF.md](PADMINT_HANDOFF.md), and the README asks players to say whether it worked. Installing on an iPad waits for the iPad. |
| 4. Small fixes | Each fix is in shared code or both menus, passes the Windows CI, is listed under "In `main`, waiting for a Windows build", and its issue is answered. First: portable mode for Windows (#64). |
| 5. Linux | With Chris's go-ahead, the author of the native Linux port (Wind-Waker-Recomp PR #33) is invited to open it on BlueWake, and its release workflow follows the Linux rules in AGENTS.md (no disc in CI). |
| 6. Issues and docs | Every pass: new issues and comments answered in Chris's voice and labeled, nothing closed without the reporter, and README, MIGRATION_STATUS.md and WINDOWS_TASKS.md match `main`. |

### Each iteration

1. Pick the first step that isn't done and name what will close it.
2. Prefer reading the code and adding logging over playing the game.
3. Make the smallest change, run the host tests, and let the Windows CI build it.
4. Update the issue, WINDOWS_TASKS.md and the progress below.

Stop when steps 1 to 4 are done or blocked on hardware, and say which. Don't repeat runs that can't tell
causes apart.

### Progress

- October 4: loop written. Done before it: controller button remapping on Mac and Windows (#66), Jump
  and Sprint off by default everywhere (#71), #67 closed after the reporter confirmed 0.4.0 fixed it.
- **1. Audio logging:** done. `runtime/host/src/audio_watch.c` writes `[demo]`, `[demo-sound]` and
  `[audio-lost]` in every build; the triage script reports them. On the Mac, a new game to control logs
  the opening cutscene as `cues=4 sounds=4 missing=0 silent=0.4s of 104.7s`. A test feeds it a
  fake cutscene with a missing sound and silence.
- **2. Audio code review:** done. The audio pacing settings are the same on every platform; only the
  Windows 0.4.0 download has native math on, Smooth Motion on by default and the 60 Hz option. How to
  read the new lines and where each points is in [WINDOWS_TASKS.md](WINDOWS_TASKS.md#reading-the-cutscene-sound-lines-65-97).
  Confirming the cause needs a log from a Windows build of `main`.
- **5. Linux:** the port's author was invited to open it on BlueWake without the disc in CI
  ([comment](https://github.com/elliotttate/Wind-Waker-Recomp/pull/33#issuecomment-5979167274)).
- **3. PadMint confirmation:** done on this Mac. `padmint make bluewake ios` from the 0.2.0 release
  finished with a personal IPA in 2 h 37 min on a busy machine ([PADMINT_HANDOFF.md](PADMINT_HANDOFF.md)).
  [#104](https://github.com/chrissotraidis/bluewake/issues/104) asks players how it went. Installing it
  waits for the iPad.
- **4. Small fixes:** Windows portable mode (#64) merged in
  [#103](https://github.com/chrissotraidis/bluewake/pull/103) and listed for a Windows check.
- **6. Issues:** #64 answered; #65 and #97 asked to retest 0.4.0 with Smooth Motion and 60 Hz gameplay
  off, which separates the remaining causes without a new build.

Earlier loops are in [the archive](archive/GOAL_LOOP_HISTORY.md).
