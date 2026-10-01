# Focused stability loop, October 1, 2026

This is work on the next BlueWake version, not a release or whole-game acceptance.
Personal discs, translated modules, memory cards, states and audio remain in ignored local storage.
Parallels is not used; local builds are limited to two jobs.

## Profiling isolation guard repaired

The one-game guard's previous Mac pattern ended at the executable name, so it did not match
`BlueWake.app/Contents/MacOS/BlueWake MODULE.dylib`. The guard now accepts either the end of the
command or whitespace after that executable, without matching `BlueWakeHelper` or unrelated apps.
Seven synthetic process-list fixtures cover native arguments, spaces in paths, raw host/Dolphin,
simulator opt-out and unrelated/empty process lists; they pass and run in repository CI.
A live check during a timed Mac run also correctly refuses another game launch.

One new instruction-count pair overlapped for approximately six seconds before this was caught,
as confirmed by the private log creation/completion times. Both runs are excluded from performance
comparisons. The replacement sequence waits for each child to exit and uses the repaired guard.
Earlier serial cache A/B/B/A runs were individually completed before the next began; their existing
no-FPS-gain conclusion is unchanged. The guard checks already-running processes, not an atomic
cross-agent launch lock; do not dispatch concurrent game launches.

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
silence in these particular guest-PCM captures. Subsequent stream tracing and direct disc-track
comparison identify the expected music in the captures (below), but do **not** prove speaker output
or reproduce the report on Windows/iOS or a newly rebuilt Better Wind Waker module.
No speculative DSP change has been made. The next audio gate is a rendered/output-device
reproduction with the reporter's platform, build and settings.

Initial Dolphin captures are not accepted as a narrated-intro reference: their replay has not been
shown to reach the same scene, and late-window RMS correlation is low (0.42-0.45). A fixed-timing
button movie did not include name-entry Start; replaying the recorded BlueWake pad trace also did
not yield a verified scene match. Capture processes were stopped after their bounded runs; the
files are retained privately, not treated as proof of an audio mismatch or fix. Use scene-confirmed
reference playback before interpreting the comparison.

The game's source prepares `JA_STRM_DEMO_01_01` at opening timer 40 only when the overlap is no
longer peeking, then calls stream play at state 2. That is a diagnostic lead, not an established
BlueWake bug. Sources: [opening state machine](https://github.com/zeldaret/tww/blob/main/src/d/d_s_open_sub.cpp),
[stream prepare/play](https://github.com/zeldaret/tww/blob/main/src/JAZelAudio/JAIZelBasic.cpp).

### Expected intro music is present in the tested Mac PCM

A developer-only, read-only probe (`BLUEWAKE_ENABLE_DEVELOPER_TRACING=ON` and
`BLUEWAKE_TRACE_BGM_STREAM=1`) observes the GZLE01 stream calls and changes in the sound state.
With fast defaults it records prepare for `0xC0000024` at retrace 896, a valid stream handle at
897, `Audiores/Stream/1tale.afc` loaded/ready at 899, play at 1000, and sound state 4 (playing) at
1001. The audio-disabled flag stays clear. The probe's capture remains byte-identical to the
untraced baseline: 1,918,984 stereo frames, hash `81DF89AD`.

The requested AFC was extracted privately from the same personal disc and decoded locally with
FFmpeg. Comparing the captured 30-32 second window against that track gives sample-level
correlations of 0.999999 (HLE fast), 0.984158 (LLE fast), and 0.999998 (HLE original transitions).
The 30-59 second RMS envelopes correlate at 0.987479, 0.945278 and 0.971072 respectively.
This is specific music evidence, not just a nonzero-samples test. It does not establish playback
through speakers or rule out a platform/settings-specific report. The stream probe compiles out
of ordinary builds; the final native Mac build has tracing OFF. No track, capture, disc or state
is committed or uploaded.

A subsequent rendered native Metal/HLE run with a fresh card/SRAM, no stored settings and wall
pacing reaches the same narrated-intro milestone at retrace 806 and exits normally at 2,400
retraces. Its guest PCM also matches the expected track at 0.999999 sample correlation in the
30-32 second window. SDL reports successful playback start at its 40 ms prebuffer and remains
playing with nonzero buffers during the intro, without output-open/start/queue errors in the log.
There are 498 low-queue pushes out of 159,873, so this is not a clean audio-stutter acceptance run;
other project simulators remain active. Successful queueing/resume still does not prove audible
speaker output, the affected reporter's build, Windows or physical-device playback.

## Windows cache race fixed

The Windows per-call-site environment cache formerly read and published a `volatile` pointer.
Concurrent first readers could race and publish different string allocations. `volatile` is not
synchronization. It now uses an acquire load and compare/exchange publication, frees losing copies,
and retries after allocation failure rather than permanently recording a present variable as unset.
Its steady-state path remains one cached atomic read, not a CRT environment scan/lock.

The synthetic regression forces 16 readers to allocate before any publishes, then checks identical
returned pointers and contents, cached absence, independent call sites, copied-value lifetime after
an environment change, and allocation-failure retry. Optimized and ThreadSanitizer runs pass on
macOS. All 24 registered BlueWake host CTests pass, including this test and the FPS classifier. The Windows source-only
workflow also compiles/runs the same test with native clang/MSVC; its result is recorded separately
after CI completes. No Windows gameplay claim follows from this test.
The first native CI attempt linked the app but rejected the new standalone test under `-Werror`
because its CRT deprecation policy did not match the runtime's. The harness now uses the same
`_CRT_SECURE_NO_WARNINGS` policy and a length-bounded memcpy; native CI is rerun rather than counting
that attempt as a pass.

The native source-only workflow subsequently **passes at `60be199`**, including the full app link
and 16-reader cache regression:
[CI run 36805880425](https://github.com/chrissotraidis/bluewake/actions/runs/36805880425).
The expanded opt-in CMake/CTest configuration also **passes at `830bf7d`**, including native app
linking and both the cache and shared FPS classifier/worker-counter tests under the Windows
compatibility layer: [CI run 36808815002](https://github.com/chrissotraidis/bluewake/actions/runs/36808815002).
These remain source-only checks, not Direct3D gameplay or output-device audio acceptance.

## Interpolation and graphics regression coverage

The pinned runtime includes a standalone matching/blending/pacing regression suite that its CMake
did not register. BlueWake now builds and runs that existing suite against the linked runtime on
Mac and in the opt-in Windows regression configuration. It covers camera-cut rejection, frame
matching, blended transforms, pacing/drop recovery and mode changes, including 120-to-60 recovery.
The suite passes locally, bringing the registered BlueWake host checks to **25 passing CTests**.
The new Windows target also **passes natively at `ec6e797`**, along with the full app link and the
other two tests: [CI run 36810248709](https://github.com/chrissotraidis/bluewake/actions/runs/36810248709).

Five existing graphics/frontend/trace tests and five render-worker ordering, backpressure, sync,
shutdown and frame-slot tests also pass. They need no personal game input or GPU. They are useful
regression coverage, not proof of correct whole-game pictures or hardware performance.

A bounded native Metal run restores the same Outset room-44 state, uses 960x720, 1x scale, Smooth
Motion and no live input, and verifies cached derived pipeline state by re-deriving it on each hit
(`DOL_GXCORE_DERIVED_VERIFY=1`). At normal exit after 1,400 retraces, it reports **2,781,228 verified
comparisons and zero mismatches**. All 2,869,165 submitted draws are planned with zero rejected or
failed draws, vertex-decode failures, missing projections, payload overruns or unresolved arrays.
The state restore also reports 150 fields and no missing fields/mismatches. This checks cache
equivalence in one live scene, not pixel equivalence, all shader features or a speed improvement;
verification itself adds work. Personal inputs and captures stay local.

An eight-frame raw GX capture did **not** pass the existing `--against-stats` replay comparison:
seven compared frames differed, with a first-frame draw count of 6,842 replay versus 2,699 recorded.
Restored-state CP/register initialization and legacy-versus-current renderer statistics are leads,
not established causes. The capture is not accepted as a faithful optimization baseline, and the
comparison was not relaxed. A seeded/from-boot capture and a current-renderer-equivalent comparison
are needed before drawing performance conclusions from replay. Live cache verification above is
independent of this failed capture.

## Windows monotonic-clock initialization

The Windows timing shim also had unsynchronized first-read access to its static performance-counter
frequency. It now caches the scalar with relaxed atomic loads/stores; concurrent first callers may
query the same boot-fixed frequency, but the steady-state path remains one atomic load with no
mutex or repeated frequency query. This relies on the documented
[Windows QPF contract](https://learn.microsoft.com/en-us/windows/win32/api/profileapi/nf-profileapi-queryperformancefrequency).
It rejects failed counter reads and unsupported clock IDs rather than dividing by zero or silently
returning wall-clock time for an unknown ID.

A new native Windows regression releases 16 readers together, checks 160,000 monotonic reads,
nanosecond normalization and bounds against direct QPC samples, and checks realtime/CPU clocks,
null output and unsupported-ID errors. The source and test cross-compile/link with LLVM-MinGW on
Mac. Native clang/MSVC CI also **passes at `74da8ee`**, with the full app link and all four
regressions: [CI run 36810799124](https://github.com/chrissotraidis/bluewake/actions/runs/36810799124).
This test is not a Windows
ThreadSanitizer run or a measured FPS improvement.

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
- With the FIFO worker on and Smooth Motion off, the same scene runs near 60 retraces / 30 game
  presents per second after startup. This isolates interpolation/extra presentation as a lead, not
  a proven root cause: foreground/occlusion and repeat-order effects still need controlled A/B.

## FPS diagnostic corrected

The Smooth Motion-off run was reporting healthy 29-31 FPS at full simulation speed as
`reason=presents late`: the old logger unconditionally expected 60 shown FPS. It now reads the live
interpolation setting and uses 95% of the selected 30/60/120 mode as its presentation threshold.
The target is included in each dip line. Nine synthetic cases cover normal output, real slow game
speed, rejected interpolation, late presents and out-of-range step clamping.

A rebuilt native Metal repeat with Smooth Motion off completes normally. Healthy 30 FPS/full-speed
periods no longer log `presents late`; actual sub-95% dips still log `target=30` and slow-game reasons.
The native Mac host and iOS/tvOS app targets compile/link after this shared change; all 24 registered
BlueWake CTests pass. Physical device installation, Windows gameplay and 120 Hz display acceptance
are not implied. Neither the selected mode nor any player's stored settings was changed.

Slowdown logs now include CPU utilization for the FIFO, interpolation-helper and render workers,
using their existing cumulative counters. Four additional synthetic cases guard normal utilization,
idle counters, worker replacement/reset and a zero-length interval. The counter subtraction is
guarded against unsigned underflow when a worker exits. These are diagnostic improvements, not a
claimed speedup.

Two longer visible/foreground-observed repeats have post-startup one-second VI-rate medians of
58.7 and 59.7, compared with 44.75 in an earlier isolated repeat. They still have substantial dips;
one includes a brief minimize/restore check. Other project simulators/background processes were
active, and the earlier slow runs also logged gained focus without subsequent focus loss. Therefore
focus alone is **not** an established cause and these are not controlled before/after benchmarks.
No worker-priority, App Nap, global interpolation or quality change has been made.

A subsequent four-run cache-disabled/enabled/enabled/disabled comparison uses the same restored
scene, window/scale/interpolation, copied card, no live input, 2,800-retrace stop and ten-second
sample procedure. All four exit normally at 1,366,321 guest blocks, PC `0x802d837c`, with exactly
13,019,891 planned draws and no rejected/failed draws. Both cache-enabled runs log 12,607,611 hits
and 412,280 misses (96.83% hits). The sample tool's **top-of-stack** table records 895/891 samples
in `build_draw_plan_into` with caching off versus 682/707 with it on; these are sampled instruction
locations, not instructions retired or an inclusive-parent subtraction.

Post-startup VI-rate medians are 59.9/59.75/58.9/59.9, with 7/10/9/10 one-second samples below 57.
Pacing caps both configurations and background load remains uncontrolled. This supports the
existing cache's intended cost reduction in this scene, but **not** a reliable FPS win, a newly
implemented optimization, whole-game equivalence or a reason to change player defaults. The next
discriminator is per-retrace CPU/instruction cost across the remaining graphics translation and
guest dispatch, using normal-stop/work-count guards and a reproducible workload.

The sample parser now accepts both macOS main-thread labels (`com.apple.main-thread` and
`: Main Thread`) without counting worker stacks as game-thread work. Three synthetic fixtures
guard both labels and refusal to guess an unidentified thread; they also run in repository CI.

## Measured dispatch optimization

The fixed-address mouse, climb, quick-door and draw-tag hooks now share one unsigned range check
before their individual dispatch checks. Calls outside the fixed GZLE01 hook interval skip those
checks and armed-flag reads. Hook order is unchanged. Jump stays outside this filter because it
can observe a dynamic player-procedure call; interrupts, exceptions, aliases and actor search are
also unchanged. This is a small host change, not a generator or simulation-rate change.

The source-only regression compares the original dispatch sequence with the filtered sequence at
every aligned MEM1 address for all eight combinations of the three armed/enable flags, plus range
edges and unrelated/mirrored addresses. Hook counts and order agree. All **26 Mac host CTests pass**;
the final shared source also compiles/links in the native iOS and tvOS app targets. The new fifth
Windows regression is included in source-only CI; native validation is pending for this change.

Retired-instruction comparisons use the same Outset room-44 state, 960x720, 1x scale, FIFO worker
enabled, no live input and isolated copied card/SRAM. Smooth Motion and audio stretching are off
only for these timing runs, not in player settings. Each pair subtracts a 1,800-retrace run from
a 2,800-retrace run to exclude fixed startup work. Every lower/upper run stops normally at the
same respective guest blocks/PC and draw totals (5,754,709 / 13,019,891), with no rejected/failed draws.
Runs are serial and unsampled; `/usr/bin/time -l` supplies retired instructions.

| Fixed workload, instructions per additional retrace | Control | Candidate | Reduction |
| --- | ---: | ---: | ---: |
| Existing donor-derived pipeline cache, off then on | 331,385,424 | 327,224,983 | 1.26% |
| New dispatch filter, control then candidate, cache on | 327,224,983 | 324,077,636 | 0.96% |
| Dispatch repeat, candidate then control, cache on | 326,725,860 | 324,093,609 | 0.81% |

The first row measures already-integrated contributor work, not a new cache implementation. The
two dispatch comparisons support a modest CPU-work reduction in this scene. Background work and
presentation pacing remain uncontrolled; none establishes an FPS gain, Windows/iPad performance
or whole-game acceptance. These percentages are not added together as a general speed claim.

With Smooth Motion enabled again, control and candidate save the same restored workload at
retrace 1,501 and stop normally at 1,600, with 454,689 guest blocks and 4,310,921 planned draws.
All nine guest/host payload chunks are byte-identical. The raw GX chunks differ at 63 bytes in
21 resolved host-pointer fields: eight texture ranges, twelve TMEM-TLUT ranges and the copy range.
Offsets are attributed using `offsetof` against the actual runtime headers; every pointer has the
same relocation delta and **all other GX bytes agree**, including the entire sink payload. Raw
snapshots are retained unchanged. This is state/register/work-count evidence, not pixel equivalence.

A fresh final-candidate HLE intro run reaches the narrated scene and stops normally at 3,600
retraces. Its 1,918,984 stereo PCM frames remain byte-identical to the earlier HLE baseline
(hash `81DF89AD`). The dispatch change therefore does not alter this tested intro's generated
audio; speaker audibility and the reporter's affected build remain separate unresolved gates.

These runs reveal a repeatability/scheduling or graphics-translation problem worth investigating.
Do not subtract inclusive sampled owner shares to infer self time. Next: repeat the worker A/B with
controlled foreground/occlusion, collect FIFO-worker and draw-plan costs, confirm the Smooth Motion A/B,
and validate the chosen change against scene pictures, audio and saved-state equivalence. Native
Windows Direct3D play and longer physical-device/thermal runs remain unverified.
