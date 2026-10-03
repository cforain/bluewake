# Stability and slowdown plan — October 3, 2026

BlueWake now contains Elliott Tate's Wind-Waker-Recomp work through his v0.4.0 release, so reports
filed against his Windows builds (0.2.1 to 0.4.0) mostly describe BlueWake's code as well: the
runtime, renderer, audio and camera are shared, and Apple builds run the same runtime with Metal.
This plan sorts those reports, records what the attached session logs show about the "random FPS
slowdowns", and sets the order of work. The [goal loop](../GOAL_LOOP.md) runs it.

## What the logs show about slowdowns

Three logs are attached to Wind-Waker-Recomp issues (#5, #19, #27). The longest, 104 minutes on a
Ryzen 9 5900HX laptop with 0.4.0, summarized with `scripts/triage_session_log.py`:

- 97 seconds fell below the selected FPS. 91 of them were the game itself running below full speed
  (median 89%, lowest 67%). 89 of the 97 were at the Forsaken Fortress exterior (stage `MajyuE`).
- In 83 of the 91, the GX worker, the thread that converts the game's drawing commands for the GPU,
  was at least 85% busy (mostly above 92%) and the game waited on it roughly 400 ms of every second. The GPU waited about 1 ms.
  The slowdown is CPU work on that thread, not the graphics card, which matches the #6 comment
  ("GPU usage is extremely low, but the FPS counter says 60").
- Smooth Motion lowered its in-between frames 71 times. After a quick relapse it waits up to
  120 seconds of calm before coming back, so a short overload can look like "30 FPS for a while,
  then 60 again".
- 1,587 slow GX batches happened while pipelines compiled or textures loaded: compile and upload stutter, a
  second, separate cause.

Two mechanisms therefore need separate fixes: real overload of the GX worker in heavy scenes, and a
pacing rule that drops in-between frames for one hitch (an 8-frame average) and then holds them off.
The other logs show the Windows audio crash at address zero that BlueWake already fixed (#5) and a
short Pictobox session whose black screen left no error in the log (#19).

## Elliott's newer work, not yet in BlueWake

After v0.4.0, Wind-Waker-Recomp's `windows-release` gained about 20 commits (`9921398` to
`13355b8`, October 2) aimed at exactly these problems. His measurements, not yet repeated here:

| Change | His runtime patch | Result he reports |
| --- | --- | --- |
| Dawn device lock | 0121 | Crash after loading a save state: 3 in 24 runs to 0 in 80. He notes the Mac needs it too. |
| Slow-game detector: median of 60 frame gaps, ignores gaps of 150 ms+, two slow windows | 0122 | Single hitches no longer drop the in-between frames |
| Pipelines compiled on several threads, 513-pipeline seed, "compile shaders before playing" | 0123 | Seed compiles in about 1.1 s instead of 4 s |
| Ubershader for draws whose pipeline is still compiling (D3D12 only) | 0128-0129 | Skipped draws after warm-up cut by 80-96% |
| GX worker: attribute arrays found once, vertex constants reused | 0124, 0127 | GX worker CPU per frame down about 12% |
| Smooth Motion for cloth, sails, colours | 0125-0126 | Flags and sails blended (needs a rebuilt module) |
| Training tours ten places; app PGO and ThinLTO; tiered compile | builder | 425 instead of 288 functions trained; GX worker CPU 16.9 to 14 ms; build 39 to 15 minutes |
| Nine more certified native functions | builder | Outset on four E-cores 37.5 to 44.5 game FPS, with the above |

BlueWake's own runtime patches 0121-0139 use the same numbers for different changes (save safety,
the Pictobox fix, post-texture state), so imports are renumbered. BlueWake's card safety and Pictobox
patches are not in his branch; they must survive every import.

## The reports, applied to BlueWake

| Report | Applies to BlueWake | Status | Next step |
| --- | --- | --- | --- |
| Slow bird scene (#6), slow abduction (#23), Forsaken Fortress dips (#27 log) | Yes, shared runtime | Not measured on BlueWake in these scenes | Measure on Mac and iPad, then import the batch above |
| Missing music in intro and scripted scenes (#1, #12) | Likely, shared audio | Not reproduced | Reproduce on Mac with audio capture and the audio logs |
| Camera left/right flips in water (#24) | Likely, shared camera code | Suspect: the stick camera hands control back to the game's C-stick in some modes, which turns the other way | Mac stick test while swimming |
| Dungeon map drawn wrong (#25), pirate flag without texture (#20) | Likely, shared renderer | Not reproduced | Reproduce on Mac from saves; compare captures |
| Soft lock after a Moblin falls (#27) | Unknown | Log attached | Try to reproduce; may be the original game's behaviour |
| Pictobox black screen (#19, BlueWake #13) | Yes | Fixed in BlueWake, passes on Mac | Windows confirmation |
| Crash at launch with Exact audio (#5) | Was | Fixed in BlueWake | Windows confirmation |
| Freeze after disc import (#16), exe does not open (#28) | Possibly | Windows only, no BlueWake data | Elliott's Windows testing; ask reporters for session logs |
| Button layout and remapping (#2, #14), 8BitDo modkit (#8) | Partly | BlueWake has A/B and X/Y swaps; no full remap | Remapping as a feature |
| Disable sprint and jump (#22) | Answered | BlueWake's "Jump and Run" is off by default | Point the reporter to the setting |
| Linux, PAL, Switch, Android, Wii U UI, portable mode, ultrawide, language (#3, #18, #7, #9, #26, #4, #10, #11, #21, #29) | Feature requests | | Migrate as feature requests |

## Logging: what is there and what is missing

Already written by the shared host on every platform: a once-a-second `[perf]` and
`[fps]` line; `[fps-dip]` for each second below the selected FPS, with the reason, game
speed, waits, each worker's CPU and Link's stage, room and position; `[interp-pace]` when Smooth
Motion changes; `[render-slow]` and `[present-slow]`; crash reports. iOS shares the log from
Help & Feedback; Windows keeps the newest eight in `%APPDATA%\BlueWake\logs`.

Missing or misleading:

1. `[gx-slow]` fires for every batch over 20 ms: 33,712 lines in the 104-minute log, written from
   the overloaded thread itself. Aggregate it per second; print single batches only at 50 ms or when
   a pipeline or texture was made.
2. `[fps-dip]` says "game below full speed" without naming the saturated part. Add the
   classification the triage script makes: game thread, GX worker, GPU/presentation, or compiling.
3. Settings are not beside the dips. Log Smooth Motion steps, render scale, HD textures, mods, present
   mode and ubershader at start and on every change.
4. No end-of-session summary. Add one `[perf-summary]`: dips by cause and stage, Smooth Motion
   drops, worst frames, shader compiles.
5. iOS logs show "macOS" and an unknown CPU. Log the device model, OS and thermal state.
6. A capped module-call trace is labelled `[panic] vcall-after` in normal sessions. Rename it.

## Order of work

1. **Logging** (items above), checked with a scripted stall and a real heavy scene so each cause is
   named correctly, and the log stays small.
2. **Measure before changing**: fixed scenes on the Mac and iPad, original 30 Hz and Smooth Motion
   60: Outset, the opening bird, Aryll's abduction, the Forsaken Fortress exterior, open sea. Record
   game speed, dips by cause, frame-time tails and audio for each.
3. **Import Elliott's batch** as focused, credited runtime PRs on `bluewake-next`, in this order:
   device lock, slow-game detector, pipeline threads and seed, GX worker changes, Smooth Motion cloth
   and colours, wider training and tiered compile, natives, then the ubershader (D3D12 first; Metal
   only after its own captures). Each: regression tests, Mac capture comparison, Windows CI, a note
   on whether old modules still work, and the step-2 scenes again.
4. **Specific bugs** from the table, each reproduced before it is changed.
5. **Windows confirmation** through Elliott's [checklist](../WINDOWS_ACCEPTANCE.md), extended with the
   new batch and the slow scenes.

Defaults stay: original 30 Hz logic, Smooth Motion off, experimental 60 Hz off.

