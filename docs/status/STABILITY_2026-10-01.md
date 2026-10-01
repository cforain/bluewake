# Focused stability loop, October 1, 2026

This is work on the next BlueWake version, not a release or whole-game acceptance.
Personal discs, translated modules, memory cards, states and audio remain in ignored local storage.
Parallels is not used; local builds are limited to two jobs.

## Intro audio report

[The fork's issue #1](https://github.com/elliotttate/Wind-Waker-Recomp/issues/1) reports missing
music during the narrated new-game intro. Its body does not specify platform, build or settings;
no comments supplied those details at this check. BlueWake has no open issues at this check.

Using the existing personal GZLE01 module, fresh isolated card/SRAM files and no saved settings,
three native Mac headless runs completed normally at 3,600 retraces:

| DSP / transitions | Narrated-intro resource requested | Captured PCM |
| --- | --- | --- |
| HLE / fast defaults | Retrace 806 | 59.97 seconds, 32 kHz stereo, peak 21,631 |
| LLE / fast defaults | Retrace 803 | 59.97 seconds, 32 kHz stereo, peak 22,646 |
| HLE / original fades, no fast-forward | Retrace 916 | 59.97 seconds, 32 kHz stereo, peak 21,733 |

Both DSP modes have similar five-second RMS envelopes and nonzero samples throughout the later
intro window. Disabling transition acceleration also produces nonzero audio. This rules out total
silence in these particular guest-PCM captures. It does **not** identify the expected music, prove
speaker output, or reproduce the report on Windows/iOS or a newly rebuilt Better Wind Waker module.
No speculative DSP change has been made. The next gate is comparison against an isolated Dolphin
reference and a rendered/output-device reproduction with the reporter's settings.

The game's source prepares `JA_STRM_DEMO_01_01` at opening timer 40 only when the overlap is no
longer peeking, then calls stream play at state 2. That is a diagnostic lead, not an established
BlueWake bug. Sources: [opening state machine](https://github.com/zeldaret/tww/blob/main/src/d/d_s_open_sub.cpp),
[stream prepare/play](https://github.com/zeldaret/tww/blob/main/src/JAZelAudio/JAIZelBasic.cpp).

## Windows cache race fixed

The Windows per-call-site environment cache formerly read and published a `volatile` pointer.
Concurrent first readers could race and publish different string allocations. `volatile` is not
synchronization. It now uses an acquire load and compare/exchange publication, frees losing copies,
and retries after allocation failure rather than permanently recording a present variable as unset.
Its steady-state path remains one cached atomic read, not a CRT environment scan/lock.

The synthetic regression forces 16 readers to allocate before any publishes, then checks identical
returned pointers and contents, cached absence, independent call sites, copied-value lifetime after
an environment change, and allocation-failure retry. Optimized and ThreadSanitizer runs pass on
macOS. All 23 registered BlueWake host CTests pass, including this test. The Windows source-only
workflow also compiles/runs the same test with native clang/MSVC; its result is recorded separately
after CI completes. No Windows gameplay claim follows from this test.

## Gameplay profiling, not an FPS claim

Native Metal, Outset room 44, 960x720 window, 1x internal scale, Smooth Motion enabled, same restored
personal state and no live input:

- An initial capture reached approximately 60 retraces/second. Its early timing is contaminated by
  overlap with a headless diagnostic run and is not a valid comparative benchmark.
- An isolated worker-enabled repeat started near full speed, then fell to roughly 21-42 retraces
  per second with graphics-drain waits. During its ten-second sample, the main thread spent 47.6%
  waiting in `shadow_frontend_flush`; the FIFO worker was actively parsing/building draw plans.
- An isolated FIFO-worker-disabled run sustained roughly 45-47 retraces/second near its end, with
  no graphics-drain wait but 100% game-thread busy time. That moves graphics work onto the guest
  thread; it is not a demonstrated general optimization and is not made the default.

These runs reveal a repeatability/scheduling or graphics-translation problem worth investigating.
Do not subtract inclusive sampled owner shares to infer self time. Next: repeat the worker A/B with
controlled foreground/occlusion, collect FIFO-worker and draw-plan costs, compare Smooth Motion off,
and validate the chosen change against scene pictures, audio and saved-state equivalence. Native
Windows Direct3D play and longer physical-device/thermal runs remain unverified.
