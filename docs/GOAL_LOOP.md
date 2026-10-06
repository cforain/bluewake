# BlueWake goal loop

Latest checkpoint: [October 6 targeted follow-up](status/TARGETED_PASS_2026-10-06.md).
The [earlier handoff](status/HANDOFF_2026-10-06.md) retains the preceding investigation evidence.

Updated October 6, 2026. Work from [TECH_DEBT.md](TECH_DEBT.md), the maintained queue of all known
reports and technical debt. The earlier loop is preserved in [history](archive/GOAL_LOOP_HISTORY.md).

## Current checkpoint

Chris resumed with a targeted pass. The latest private host is installed on the iPad with
17 save/configuration files verified unchanged; gameplay checks await an unlocked device.
Linux shutdown evidence was reviewed and a log-summary repair prepared in PR #148.
No scheduled monitoring is active. Resume from the targeted follow-up rather than repeating
completed comparisons or assuming the installation proves gameplay.

## Objective

Diagnose and fix the most disruptive rendering, cutscene-audio, input and performance problems after
0.5.0, while keeping Mac, Windows and Apple mobile code in step. Evaluate Linux for official support
from contributor evidence and the existing PR. Publication is a separate decision for Chris.

## Each iteration

1. Read AGENTS.md, check working changes, current main, open PRs and new issue responses. Avoid duplicate
   work and preserve player data. Update the queue when evidence changes, not merely its date.
2. Pick the highest-priority actionable item. Write a hypothesis, competing explanation and one check that
   distinguishes them. For regressions, identify the actual old/new build and relevant source/runtime delta.
3. Inspect existing logs/source first. Reproduce on a scratch save with matched scene/settings. Spend roughly
   30 minutes on a diagnostic question; extend only if new evidence makes the next step specific. Never loop
   on the same unchanged result, run hours of soak testing or broaden a passing test without a reason.
4. Make the smallest verified fix or diagnostic improvement. One concern per PR. Runtime work uses RecompCore
   bluewake-next and the pin/patch workflow. Shared host changes reach Windows; settings belong in both menus.
   Gameplay/timing/rendering behavior stays off by default until tested on the affected platform.
5. Run relevant tests, repository/attribution checks and Windows CI before merging. Report actual device,
   source revision, settings and limits. Compilation is not gameplay and logging is not an audible/visual test.
6. Update TECH_DEBT.md and any detailed evidence record in the same PR, and WINDOWS_TASKS.md when a Windows
   hardware check is pending. Distinguish diagnosed, fixed in source, shipped and reporter-confirmed.
7. Continue to the next actionable item. If hardware or reporter evidence is missing, record the precise
   handoff and continue independent work. End a bounded pass with changes, evidence and remaining gates.

## Initial order and acceptance

| Work | First discriminating check | Done for this pass when |
| --- | --- | --- |
| Flickering #136 | Actual 0.4.0 to 0.5.0 render delta; original textures at 30 vs 60/120 | Cause isolated and tested, or narrowed suspects with a precise capture/hardware request and diagnostic path |
| Audio #97/#65 | Trace why 1tale.afc returns from playing to idle after two retraces | Specific stop/read/decoder cause or a bounded diagnostic that exposes the missing link; no cue-count-only acceptance |
| Performance #137/#59/#86 | Matching Outset profile with warm caches; compare optimization sets | Measured bottleneck and validated bounded improvement, or exact next probe and hardware handoff |
| Controls/Pictobox #138/#13 | Stick curve through both clamps; two photos and gamepad save selection | Separate minimal fixes with meaningful controller/render acceptance, or reproducible explanation |
| HD shading / flag #80/#69 | Matched on/off frames and draw context | Cause isolated or location-specific evidence that distinguishes replacement/sampler/palette/draw issues |
| Dungeon map #74 | Windows check of merged #134 | Hardware result recorded; release delivery remains separate |
| Linux #107 | Full session log, current-main parity, CI, shutdown backtrace | Clear merge/support gates communicated; reviewed evidence recorded without premature support claims |

GitHub: the Linux follow-up is authorized. Other replies must be useful, evidence-backed and consistent
with Chris's current communication instructions; never close without reporter confirmation or a clear
duplicate/off-topic reason. Discord remains draft-only. Optional promotional footage needs permission to
reuse, carries no private paths/notifications, and is not a prerequisite for a technical merge.

This is an execution loop, not a scheduled background monitor. Refresh documentation on each substantive
work pass. Do not create recurring notifications unless Chris asks.
