# Technical debt and known issues

Latest checkpoint: [October 6 targeted follow-up](status/TARGETED_PASS_2026-10-06.md):
latest private iPad host installed and player data verified; gameplay awaits device unlock.
The [earlier handoff](status/HANDOFF_2026-10-06.md) retains prior candidate evidence.

Updated October 6, 2026 (JST). Owner: Chris. This is the maintained work queue for
[the goal loop](GOAL_LOOP.md), covering reported bugs, unverified fixes and support debt.
The dated [October 5 catalog](status/OPEN_ISSUES_2026-10-05.md) is historical evidence.

Update this page after each meaningful investigation, new reporter result, fix or release.
Each update must retain the issue link, affected version/platform, evidence, next discriminating
check and remaining hardware/release gate. Put detailed findings in dated `docs/status/` records
and link them here. A hypothesis, passing CI and a reporter-confirmed fix are different states.
Do not count a request for logs as a completed investigation or repeatedly ask for evidence already supplied.

P1: rendering/audio/progression/performance problems or fixes awaiting delivery. P2: narrower defects,
verification and port readiness. P3: new features/platforms. Re-rank if evidence shows data loss,
crashes or progression blockers; these take precedence. All 30 currently open issues are assigned to Chris.

## Priority queue

| Priority | Issue | Classification | Evidence / current state | Next check or gate |
| --- | --- | --- | --- | --- |
| P1 | [#136 Clouds and waves flickering (v0.5.0)](https://github.com/chrissotraidis/bluewake/issues/136) | Rendering regression | Reported in 0.5.0 on NVIDIA at 60/120 FPS. Mac title-view base frames match with interpolation off/on; reporter's failure remains unreproduced. | Follow the [short Windows capture procedure](WINDOWS_TASKS.md#flickering-capture-136); distinguish intermediate-frame failure from a base-frame or cold-cache problem. |
| P1 | [#97 No sound during the game intro](https://github.com/chrissotraidis/bluewake/issues/97) | Audio / opt-in fix | Deferred DVD completion restores the title-to-intro track in matched Mac and physical M2 iPad runs; Mac save/load also checked. Default remains off. | Windows test with `BLUEWAKE_DEFER_DVD_COMPLETION=1`; later music transitions, normal loading and speaker listening remain gates. See the physical iPad evidence below. |
| P1 | [#65 Music Cues Missing in Scripted Scenes](https://github.com/chrissotraidis/bluewake/issues/65) | Audio | Scripted music/effects absent; changing three settings together once helped. No single cause established. | Track with #97, but compare history intro and bird scene separately; retain possible separate causes. |
| P1 | [#137 Game Frame Rate averaging low 20s](https://github.com/chrissotraidis/bluewake/issues/137) | Performance | Ryzen 2700/RTX 4070; 70/83 intervals miss the display target, but only 35 log slow game speed. No new pipelines; native accelerators active. | Same Outset camera at 30 vs 60/120; isolate interpolation workload before profiling the remaining game/GX bottleneck. Linux's optimization set already matches Windows. |
| P1 | [#138 Windows: left stick has a large dead zone, then jumps to ~20–30%](https://github.com/chrissotraidis/bluewake/issues/138) | Controls | Wired Xbox One; host cutoff and local GZLE01 guest clamp explain an axial jump to 16/72 (22%). No hardware fix tested. | Correct the combined input curve; test fine aiming, full travel, diagonals and drift on controller hardware. |
| P1 | [#13 pictobox freezes game picture but sound keeps running](https://github.com/chrissotraidis/bluewake/issues/13) | Rendering / controls | 0.5.0 freeze resolved for knapman. Stale second preview reproduced on Mac and repaired by opt-in forwarding of skipped cache-flush instructions. Gamepad save selection is separate. | Test `BLUEWAKE_CACHE_FLUSH_FALLBACK=1` on iPad/Windows; keep default off. Verify regular/Deluxe photos, save/reload and gamepad selection. [Evidence](status/PICTOBOX_CACHE_2026-10-06.md). |
| P1 | [#80 HD Texture packs seem to cause shadows issues and tone oddities](https://github.com/chrissotraidis/bluewake/issues/80) | HD textures | Both DDS and PNG affected on Radeon 860M. A matched local Mac PNG pair does not reproduce the reported shading; forced/normal shader final frames match. Local and reporter pack variants differ. | Match exact pack/save and isolate BetterWW, widescreen and interpolation; then compare D3D12 fallback mode after compilation. [Evidence and limits](status/TRIAGE_2026-10-06.md#hd-shading-comparison-80). |
| P1 | [#86 Constant FPS drops](https://github.com/chrissotraidis/bluewake/issues/86) | Performance | Existing recurring frame drops; waiting for current-version comparison. | Group evidence with #137/#59 without assuming identical cause. |
| P1 | [#59 Bird scene at the beginning of the game is still very slow](https://github.com/chrissotraidis/bluewake/issues/59) | Performance | Bird opening slows down; #72 is already a duplicate. | One matching scene profile with warmed caches and known settings. |
| P1 | [#74 Dungeon maps are not shown correctly](https://github.com/chrissotraidis/bluewake/issues/74) | Rendering / delivery | Fixed in main via #134; Mac visual checks and Windows CI passed. Not in 0.5.0. | Windows dungeon-map check and audited next release; reporter confirmation after delivery. |
| P2 | [#55 Switch pro controller A-B input switch](https://github.com/chrissotraidis/bluewake/issues/55) | Confirmation | nextux confirms swaps work; original migrated reporter was manassm. | Record participating tester confirmation; decide closure in a later support pass. |
| P2 | [#56 Linux Support](https://github.com/chrissotraidis/bluewake/issues/56) | Platform port | PR #107 reports 434 watched intervals with one below target; full log not attached. Approved CI now fails SDL XTEST configuration. | Contributor: add libxtst-dev, incorporate current main/shared queue test; full log, shutdown heap error and package audit still pending. |
| P2 | [#58 Game won't launch](https://github.com/chrissotraidis/bluewake/issues/58) | Launch / acceptance | Exact launch and crash recovery checked on Windows 0.5.0. | Await affected reporter confirmation; preserve issue until confirmed. |
| P2 | [#61 8BitDo GameCube Modkit Controller unsupported](https://github.com/chrissotraidis/bluewake/issues/61) | Controllers | Mappings load in 0.5.0; affected 8BitDo controller not tested. | Reporter test and controller identification; loading a mapping count is not input proof. |
| P2 | [#64 Portable Mode - Allow user to set files folder and stop copying original game data](https://github.com/chrissotraidis/bluewake/issues/64) | Portable mode | Caches stay portable; imgui.ini still uses APPDATA. | Route UI ini with portable data path; check normal mode unaffected. |
| P2 | [#66 Controller Remap](https://github.com/chrissotraidis/bluewake/issues/66) | Controls / compatibility | Remapping shipped; overnight Wine black-screen/Proton 30 FPS reports are separate. | Check remap persistence on hardware; interpret Linux compatibility report separately from native port. |
| P2 | [#69 No texture on pirate ship flag](https://github.com/chrissotraidis/bluewake/issues/69) | Missing textures | Pirate flag missing; no new overnight evidence. | Capture d_a_sail draw context; add location-specific diagnostics only if needed. |
| P2 | [#71 Add Option to Disable Sprint and manual Jump](https://github.com/chrissotraidis/bluewake/issues/71) | Options / acceptance | Jump and Run option is in 0.5.0, off by default. | Await reporter confirmation; default check does not prove live input behavior. |
| P2 | [#73 Camera X-axis (horizontal) sudden invertion](https://github.com/chrissotraidis/bluewake/issues/73) | Controls / verification | Camera-invert fix shipped; controller hardware check remains. | Land/swim/boat right-stick check with inversion both ways. |
| P2 | [#76 Forsekin Fortress Soft lock](https://github.com/chrissotraidis/bluewake/issues/76) | Progression | Forsaken Fortress soft lock report remains unverified. | Exact encounter and input sequence; distinguish original behavior from port failure. |
| P2 | [#77 BlueWake.exe does not run](https://github.com/chrissotraidis/bluewake/issues/77) | CPU compatibility | AVX2 requirement message verified with SDE emulation. | Await reporter; do not claim unsupported CPUs can play. |
| P2 | [#79 120hz frame interpolation broken in 0.40](https://github.com/chrissotraidis/bluewake/issues/79) | Confirmation | Original reporter rc2189 says interpolation appears fixed. | Ready for acknowledgment/closure consideration; separate new flicker #136. |
| P2 | [#104 Built BlueWake with PadMint? Tell me how it went](https://github.com/chrissotraidis/bluewake/issues/104) | Builder feedback | M4 Air user reports 3-hour build and installed/running IPA; version/device details ambiguous. | Record positive result; identify BlueWake/tool version and device if needed. HaloPad aside stays separate. |
| P3 | [#48 Intel Mac support?](https://github.com/chrissotraidis/bluewake/issues/48) | Platform request | Intel Mac support request, no overnight update. | Establish build/dependency feasibility before promising support. |
| P3 | [#57 Request: UI redone based on the Wii U HD port](https://github.com/chrissotraidis/bluewake/issues/57) | Interface request | Wii U-style UI request. | Keep outside stability work until scope and assets are defined. |
| P3 | [#60 Wind waker Europe support](https://github.com/chrissotraidis/bluewake/issues/60) | Disc region | European disc support request. | Separate translation/asset compatibility project; not a bugfix prerequisite. |
| P3 | [#62 Nintendo Switch Support?](https://github.com/chrissotraidis/bluewake/issues/62) | Platform request | Nintendo Switch support request. | Defer pending platform feasibility and scope decision. |
| P3 | [#70 Support for ultrawide](https://github.com/chrissotraidis/bluewake/issues/70) | Display request | Ultrawide support request. | Rendering correctness at existing ratios first. |
| P3 | [#75 Any plans for Android?](https://github.com/chrissotraidis/bluewake/issues/75) | Platform request | Android PR #93 open; no new overnight response. | Require current main, performance and touch/settings parity with KartPad-informed design. |
| P3 | [#108 Feature Request, Graphics Toggle through Hotkey](https://github.com/chrissotraidis/bluewake/issues/108) | Convenience request | Graphics hotkey request. | Clarify setting to toggle; defer behind rendering/input fixes. |

## Investigation notes: October 6

### Flickering: inspect the release delta first (#136)

0.5.0 includes donor rendering changes imported in #50: transform-state reuse (patch 0152),
water/indexed-mesh UV and HUD interpolation (0153), replacement-texture mip sampling (0154),
and restricting vertex blending to written meshes (0155). They are candidates, not diagnosed causes.
Start with the same sea/cloud view and no texture pack at original 30 FPS versus Smooth Motion 60/120.
If only intermediate frames fail, inspect matching and UV wrap/blend; if base frames fail too,
inspect transform reuse/depth and texture sampling. Only test HD mip behavior with replacements enabled.
The original 0.4.0 download came from Wind Waker Recomp; BlueWake's v0.2.0 is not a valid proxy baseline.
The dungeon-map patch 0157 landed after 0.5.0 and cannot have caused this reported regression.
The source comparison also includes pixel-colour interpolation, cloth blending and the D3D12-only
ubershader fallback; see [the October 6 investigation](status/TRIAGE_2026-10-06.md).
The follow-up Mac control used the regular host capture path with interpolation off: all 13 common
retrace captures are pixel-identical to the on run. Six sampled intermediate-frame pairs show motion
without obvious cloud disappearance. This is a limited Metal/title-view result, not a negative test
of the NVIDIA sea report or a historical 0.4.0 comparison. Existing bounded capture/trace facilities
are sufficient for the next probe; do not add continuous per-draw logging before locating a bad frame.

### Audio: separate file presence, stream lifetime and audible output (#65/#97)

The [Windows 0.5.0 log](https://github.com/chrissotraidis/bluewake/issues/97#issuecomment-5996307585)
shows `Audiores/Stream/1tale.afc` preparing and reaching state 4 at retrace 2081, then state 0 at
2083, roughly 25 ms of wall time later. This is stronger evidence than a missing-file guess.
The `cues=1 sounds=1` demo summary belongs to `sea_T`, before name input; it does not validate the
history intro. A mixed-output peak can also be ambience with missing music. Trace the stop/read/decoder
path and annotate short-lived playback; do not declare audio fixed from a state-4 sample or cue counts.
The Mac M4 attachment lacks the detailed diagnostics and exact source revision, so its report is
relevant but not a matched reproduction. Earlier option testing changed several variables at once.
Disc file presence alone does not establish successful reads, correct decoding or sustained playback.
The first diagnostics change extends stream-state lines with stop/play flags, decoded/playback sample
counts and DVD/buffer state, and teaches the triage script to flag observed short playback spans.
A bounded Mac run that skips title music reaches and retains playing state. The next pass reproduced
the failure by waiting at the title: the host completes the asynchronous read callback inline, before
the caller sets its pending flag. The flag remains set, blocking the next stream's initialization.
The opt-in deferred-completion candidate now keeps the intro playing on Mac and restores nonzero
captured audio. A bounded follow-up reaches the track's full decoded sample count and the next Outset
scene; later bird cues and a subsequent streamed track remain untested. It handles ordinary async
archive reads through the same queue and preserves accepted
work in save states. A physical M2 iPad matched pair now reproduces the silent intro with the flag
off and sustained intro output with it on (3600 retraces each). A later listening launch also logs full intro-track completion and the next sea event.
This checks captured output/stream state, not speaker quality or all later music. It remains off by default: Windows hardware, later transitions
and broader loading checks are unverified. Keep #65's other missing cues separate. [Reproduction and candidate limits](status/TRIAGE_2026-10-06.md#deferred-completion-candidate).

### Performance (#137/#59/#86)

The [new Outset log](https://github.com/chrissotraidis/bluewake/issues/137#issuecomment-6000997715)
has zero new pipelines but 70/83 watched intervals below the requested display target. Of those,
35 say `game below full speed`, 23 `frames not interpolated` and 12 `presents late`. The latter
35 retain 98–102% game speed: all 70 must not be described as game slowdowns. Cause classifications
are mixed: game thread 27, GX worker 8, Smooth Motion paused 21, unclear 14. The log confirms native
accelerators are on and used. First compare the same Outset camera with Smooth Motion off versus
60/120; retain settings and warmed caches. Do not prescribe lower resolution or copy the Linux
optimization set, which already matches Windows. Counters identify where to profile, not proof of
a shared root cause. [Breakdown and next probe](status/TRIAGE_2026-10-06.md#performance--linux).

### Controller dead zone (#138)

Source and local GZLE01 inspection confirm the default host cutoff stacks with the guest's own clamp.
The first positive axial value is 31 at the host and 16 after the guest subtracts 15, or 22% of its
maximum 72. This matches the reported jump. Axial saturation is around 68% of SDL range, not the
reporter's estimated 56%, because the guest subtracts the dead zone before limiting the value.
The host backend does not call Aurora's separate PADClamp implementation; do not change that unused
clamp expecting it to fix BlueWake. [Input-chain evidence](status/TRIAGE_2026-10-06.md#controller-dead-zone-138).
No input behavior changed in this pass; a candidate curve still needs controller testing.

### Linux support (#107/#56)

[Follow-up sent](https://github.com/chrissotraidis/bluewake/pull/107#issuecomment-6006055403): keep one PR,
attach the full log, CPU, commit and settings; diagnose shutdown `double free or corruption (!prev)`;
pass Linux and Windows checks; review main/pin/builder parity; check a packaged native build with a short
launch, save/reload, controller, settings, Outset/sailing, dungeon-map and clean-quit pass. Run the release
audit before distribution. A quoted performance summary is not a completed hardware gate.
The source-only CI runs for `9bec954` were reviewed and approved; audit and attribution passed.
Linux then failed before host compilation because SDL's XTEST dependency is absent. The
[specific follow-up](https://github.com/chrissotraidis/bluewake/pull/107#issuecomment-6007552494)
requests `libxtst-dev`, current-main integration and the shared DVD queue test in Linux CI.
Official support follows accepted implementation and hardware/package evidence, with Chris approving
publication. No date promised. Requested an optional gameplay clip and permission to reuse it publicly;
a promotional recording is not a merge gate. No Discord message was posted.

## Support and delivery debt

- #126: original reporter confirmed Molgera's floor and closed the issue; retain as a renderer regression check.
- #92: Spanish-text workaround confirmed; disc-size question remains informational, outside this bug loop.
- Discord-only mouse rebinding: implemented in both menus, checked on Mac; Windows physical mouse test remains.
- Tingle Tuner: unsupported and documented; implementing GBA communication is outside this stability loop.
- PRs #46/#100: Windows PadMint and iPhone-module builder paths remain parked, not superseded by a ready-made download.
- PRs #89/#106: window placement/FPS position depend on shared runtime review and remain separate concerns.
- Avoid stale `fixed-in-main` labels implying an unreleased fix when it shipped in 0.5.0; reconcile labels in a support pass.
- [Windows checklist](WINDOWS_TASKS.md) distinguishes shipped checks from changes after 0.5.0. A new release must
  include the source/runtime pin, package audit, hashes and accurate platform testing limits.
- Raw logs can contain personal paths. Keep them and all game inputs out of Git; commit only short relevant findings.

## Logging priorities

1. Make short-lived streamed playback visible, including track, start/end retrace, state and scene. Never label
   general sound activity as proof of audible music; distinguish an intentional skip from an unknown stop.
2. If rendering remains unreproduced, record bounded per-scene changes in dropped/unresolved draw counters.
   Avoid per-draw disk logging and record enough settings/build context to compare releases.
3. Reuse existing per-second performance and shutdown summaries; add a probe only for a specific unanswered
   question. Remove or gate expensive diagnostic traces. Missing diagnostics must be reported as unknown, not zero failures.
