# BlueWake Autonomous Goal-Based Implementation Loop

## Current operating loop — stability and slowdowns, October 3, 2026

Make BlueWake hold full speed and stay stable in the places players report, and make every
slowdown explain itself in the session log. The [stability plan](status/STABILITY_PLAN_2026-10-03.md)
owns the evidence, the report table and the import list. Migration acceptance (below) continues in
parallel; its remaining gate is Elliott's Windows testing.

### Starting point

- BlueWake `main` holds Elliott's work through his v0.4.0 release. His later `windows-release`
  work (`9921398`..`13355b8`, runtime patches 0121-0129 and builder changes) is not
  imported. Track any newer donor commits separately; do not chase a moving head.
- Player logs show two causes of "random slowdowns": the GX worker saturating in heavy scenes
  (Forsaken Fortress exterior: game at 67-89% speed, worker at least 85% busy, GPU idle), and
  Smooth Motion dropping its in-between frames on single hitches and holding them off for up to
  120 s. Shader compilation adds separate hitches.
- `scripts/triage_session_log.py` summarizes any session log: crashes, dips by cause and place,
  Smooth Motion drops, hitches.

### Critical path and exit evidence

| Priority / work package | Next action and completion evidence |
| --- | --- |
| 1. Logging that isolates slowdowns | Merged (#39, #41; runtime `886e138`): causes in `[fps-dip]` including `smooth-motion-paused` (60 shown, 30 moving), `[smooth-motion]`, `[device]`, `[perf-summary]`, `[gx-slow-sum]`, `[rel-vcall]`; menu/background time left out. Remaining: a real heavy scene (step 2), a live shader-compile stall (Windows), and the on-screen counter, which still shows 60 while Smooth Motion is paused (iOS label and Aurora overlay). |
| 2. Baseline measurements | Mac and iPad, original 30 Hz and Smooth Motion 60, fixed routes or states: Outset, opening bird, Aryll's abduction, Forsaken Fortress exterior, open sea. Done when each scene has game speed, dips by cause, frame-time tails and audio recorded with exact app/module identities. |
| 3. Import Elliott's post-0.4.0 batch | Merged: detector (#40), runtime 0143-0150 and app/builder commits (#43), Windows optimization defaults matching his builds (#45). Remaining: his second set of nine natives and `lean_memory.py`, which need adapting to BlueWake's opt-in native handshakes; Metal timing of the device lock and live D3D12 checks come from Elliott's Windows run. |
| 4. Reported bugs | Reproduce before changing: scripted/intro music (#1, #12), camera flip in water (#24), dungeon map (#25), flag texture (#20), Moblin soft lock (#27). Each closes only with a before/after reproduction on the affected platform. |
| 5. Windows confirmation | Extend Elliott's [checklist](WINDOWS_ACCEPTANCE.md) with the imported batch and the slow scenes; his results close the Windows rows. |

### Iteration contract

1. Read live status, the stability plan and this table. Pick the highest-priority item whose
   prerequisites are available; name the observation that closes it.
2. Measure or reproduce first. A slowdown claim needs the scene, settings and the log's cause; a fix
   claim needs the same scene before and after with matched settings on the same device.
3. Make the smallest change that addresses the established cause. Keep imports one concern per PR
   with original authorship or co-author credit. Never enable experiments by default.
4. Run the relevant regressions, captures and the affected scenes. Preserve failed evidence and
   original player data; use copied saves.
5. Record identities, results and limits in the stability plan; push validated source to `main`
   or `bluewake-next`; update [migration status](MIGRATION_STATUS.md) when a public row changes.

After three materially identical failures, change the experiment. Unavailable hardware (native
Windows, physical controllers) is a dependency to record, not a pass. Releases follow
[AGENTS.md](../AGENTS.md); personal builds and game data stay private.

## Migration acceptance loop — October 3, 2026 (continuing; Windows gate with Elliott)

Make BlueWake the maintained home for the approved consolidation with Elliott.
The [reconciliation ledger](status/FORK_RECONCILIATION_2026-10-02.md) owns the
feature inventory, platform matrix and evidence. Source consolidation is merged
into `main` at `e73a218`, with Windows local training follow-up #38 merged
at `597feef`; runtime is merged into `bluewake-next` at `c74d1034`.
New development can proceed entirely in BlueWake. Finish the
player paths and gameplay qualification before recommending cutover. Historical
v56/v55/Route B campaigns below do not control this goal.

### Preserve the completed work

- Merged cumulative [PR #37](https://github.com/chrissotraidis/bluewake/pull/37)
  contains the integration ancestry, including 26 Elliott-authored commits and
  13 Elliott co-author trailers in BlueWake. Runtime adaptations carry their own
  attribution. Continue from `main`; do not create another import stack.
- Current maintained runtime is `0568fedd`; its product code matches
  `2218107d` (the follow-up only fixes a Windows test output path). Translator
  stays `b8b5345`. Windows host linking, all 58 source regressions and 24 Windows builder
  contract/cache checks pass at #38 head `6b64f45`. A full Windows owned-disc
  build and native gameplay remain unverified.
- The frozen clean Mac player build is BlueWake `3392854` / runtime `18ba3b64`.
  Its owned-disc translation, local training, O2 compilation, signed relocatable
  package, bounded restart/resume, game save/separate reload, settings, states,
  local upgrade and bounded progression remain accepted within their scope.
- The personal Pictobox candidate overlays host `9706637` / runtime `2218107d`
  on that module. Regular/Deluxe photos, repeat/cancel, actual card saves,
  separate album reload and legacy-state capture pass on Mac. Queued camera
  pitch and water/wall collision also pass. This overlay is not a new clean build.

Do not rerun these accepted checks without a relevant source change, failure or
identified coverage gap. Documentation-only changes do not invalidate binaries.

### Critical path and exit evidence

| Priority / work package | Next action and completion evidence | Current dependency |
| --- | --- | --- |
| 1. Source consolidation and candidate identity | Source landing is complete: BlueWake #37 and runtime #1–#4 are merged with exact tree equality to the tested commits. At the October 2 audit the live donor heads added documentation only; the later Windows work (`9921398`..`13355b8`) is tracked in the stability loop above. New changes start from BlueWake `main` / runtime `bluewake-next`; qualify the final package identity separately. | Closed for the recorded donor source; no hardware prerequisite for collaboration. |
| 2. Complete the player build paths | The retained `3392854` PadMint assembly/provenance and interrupted-build reuse now pass. Qualify the maintained candidate's reproducible app/update path and determine whether changed module inputs require a rebuild. The current `27c02a1` / `0568fedd` app-only shell already builds and passes ZIP/provenance/content checks. Signing, physical iPad run/save/reload and in-place data-preserving upgrade now pass for that compatibility candidate; finish sustained and matched performance qualification. Do not count the older workspace as a clean build of the newer candidate. | The build completed with all 662 retained objects and four profiles byte-identical. A separate current-shell/retained-module compatibility candidate passes package checks and bounded physical iPad acceptance. All ten original critical save/settings files remain byte-identical after testing. |
| 3. Finish local Mac gameplay coverage | Use isolated copied saves and the existing identified app for the remaining option/climbing checks. Establish the relevant gameplay action before an off/on comparison. Complete real mouse/controller input, audible intro/scripted music, and a representative 30-minute gameplay route with actual progression, settings, save/reload and scene transitions. | Small functional checks can proceed. Real controller/audio acceptance needs the relevant input/output observation. Sustained performance needs an uncontended host. |
| 4. Native Windows player acceptance | On confirmed x64 hardware, build the owned-disc O2 module and run native Direct3D. Cover disc import/recovery, fullscreen/restart, settings, controls/haptics, saves/states/upgrade, Pictobox, startup and scripted-music reports. Record app/module/source identities and distinguish reproduction from a claimed fix. | Chris has no native Windows PC. A concrete testing handoff is prepared for Elliott; execution and results remain pending. CI is green but cannot close these checks. Do not restart the suspended ARM64 VM as a substitute. |
| 5. Performance and migration decision | Use matched original-30-Hz configurations and scenes, compare correctness plus frame-time tails/stalls, and complete sustained play on each claimed target. Review the single platform matrix, tested instructions, issue dispositions and proposed donor notice against those results. | Quiet hardware and completed player candidates required. Historical 22.8% Outset gain is bounded, not final performance parity. No redirect, donor closure or public release. |

Select the highest-priority **available** missing result. Unavailable hardware
or storage is a dependency, not a reason to repeat completed tests or add
optimization families. Do not fetch new donor features into this fixed campaign
unless they address an established migration blocker; track later changes apart.

### Iteration contract

1. Read live repository status and the ledger's current summary. Name one
   missing acceptance result and the observation that would close it.
2. Check prerequisites before launching. For gameplay, first prove the action
   occurs (for example, an actual dialogue for instant text). A clean exit,
   enabled-option log, idle screenshots or a compiled fixture does not suffice.
3. Run the smallest discriminating check. If automation misses the action,
   record a setup failure and correct the route before spending on an A/B pair.
   After three materially identical failures, change the experiment. Do not
   extend small input probes indefinitely while a larger gate is actionable.
4. Change source only for an established defect. Run relevant regressions and
   affected gameplay checks; preserve failed evidence and original player data.
5. Record exact identities, result, limits and the next gate. Checkpoint validated
   source-only progress from `main` and update the private continuation. Summarize
   closed gates and external dependencies rather than counting probes or PRs.

The October 3 Windfall instant-text setup did not open dialogue. A corrected
fresh-intro state now supplies a discriminating check: at the same retrace, Off
reveals Aryll's sentence gradually while On shows it complete immediately.
`instant-text-dialogue-pair-y5_5t7i3` passes with both copied cards/settings and
the source state unchanged. Keep this bounded first-dialogue result; do not
repeat the earlier Windfall or item-menu setups. Other options remain open.

The retained PadMint build completed successfully; session31108 is terminal.
Do not restart it. Verification and current-shell update receipts are under
`build/reconciliation/padmint-resume-zy6khxs9` and
`build/reconciliation/current-ios-personal-update`. Preserve the frozen build
and all original packages. Chris authorized the attached physical M2 iPad; its
Documents and Library were backed up before installing in place. Windows VM
remains suspended; native Windows acceptance needs an external tester. A quiet
performance window and physical controller coverage are still required.

The current iOS compatibility candidate is signed, installed and passes bounded
physical iPad acceptance (`ipad-acceptance-eycd2x1l`): normal launch, actual game
save on an isolated copied card, separate-process reload with rendered gameplay,
and unchanged original saves/settings. The normal app was relaunched for Chris.
His brief touch/audio feedback was “its fine”; sustained play, full scripted-music
and matched performance coverage remain open. Mac climbing now passes the neutral-stick
hanging check as well: stamina drains at 40% of the climbing rate, then exhaustion
releases Link. The current app's native-window capture also shows the partly
depleted green stamina wheel beside him. Normal ground refill is also observed
on the return route. Preserve these results; recovery/regrab after exhaustion
and physical controls remain separate checks.

### Retained state and completion boundary

Primary checkout: `main`; nested runtime:
`codex/bluewake-pe-token`. The `bluewake-cpu-contract` worktree stays clean at
`3392854`, runtime `18ba3b64`, for exact PadMint resume. Keep the other evidence
worktrees, failed baseline, personal modules, profiles, captures, saves and
signing material. Do not clean up unique artifacts to make a build fit.

The goal remains incomplete until required parity, player-build and gameplay
checks have current evidence. Original 30 Hz simulation, Smooth Motion Off and
experimental 60 Hz Off remain defaults; preserve explicit preferences.
Public releases additionally require the private Clear audit and artifact gate.
Publishing personal builds or donor redirects/closures is outside this goal.

---

**Historical — v56, 2026-09-23. The iPadOS loop.** The user redirected the project:
make the game actually work on iPadOS, tested in the iOS simulators one at a
time, with no hardware iPad yet. Route A is hosted on iPadOS by `apple/ios` and
already reaches controllable Outset gameplay in the simulator; the loop now
works down what stops a person from playing on an iPad. The operating document
is [GOAL_PROMPT_V56_2026-09-23.md](archive/GOAL_PROMPT_V56_2026-09-23.md) and the
decision record is
[status/IPADOS_REORIENTATION_2026-09-23.md](status/IPADOS_REORIENTATION_2026-09-23.md).
The v55 Route B campaign below continues as a background track.

**Superseded by v56 — v50, 2026-09-21. Finish the project.** The product half of macOS is
met: the signed app boots the retail disc through the original flow into
controllable Outset gameplay with real keys, real video, real audio, the game's
own save and a normal stop, and Route A is the shipping route. What is left is
everything after "it runs": authentic play-scene speed (the only large item),
the renderer's cost and its p99 tail, graphics correctness, physical
controller, the compatibility campaign from new game to ending, a composite
that regenerates from the tree, and then iPhone and iPad. The full operating
document is [GOAL_PROMPT_V50_2026-09-21.md](archive/GOAL_PROMPT_V50_2026-09-21.md),
and its first act is to resolve the two different instruction counts the ledger
carries for the same play window before any further performance work is
planned.

**September 9 stopping point (historical):** TWW 0267–0268 repaired null heap
exchange and native DVD/audio command handoff. The private original
scheduler/Painter experiment ran 600 frame cycles with original audio startup and
reached the opening request; transition/profile and archive handoff were left
unfinished, and its deliberate end fence was not boot success. See the
[session handoff](archive/status/SESSION_HANDOFF_2026-09-09.md) for that evidence.

**Original cold-start integration / TWW 0265–0266:** a strict headless
experiment now completes original `mDoGph_Create` and the complete LOGO profile's
Create method, drains its queued DVD preloads, and exits zero. Full resource
ownership replaces the path-rejecting diagnostic loader. Native JKR heap context
is now per-thread, and host OS registries survive game-global destruction; both
bugs have failing-before/passing-after regressions. All 24 regression runs pass,
including the existing world replay and unchanged paced cursor PCM fingerprint.
Source replay and private-data audits pass. Earlier failed-link claims of “no
duplicate definitions” were premature: executable closure exposed conflicting
diagnostic owners, removed from this experiment. Normal LOGO drawing/deletion,
archive handoff, opening transition and METER admission remain next; audio startup,
reset recovery and legacy MAT2/BLS formats are not qualified here. Solid-heap
individual-free/size warnings remain recorded. No product gate advances; full PRD
goal active. Recovery: `local-research/checkpoints/reorientation-20260909-logo-cold-start/`.
See [world integration evidence](status/ROUTE_B_WORLD_INTEGRATION_2026-09-09.md).

**Governing requirements:** [PRD.md](archive/PRD.md)

**Purpose:** operating procedure for a long-running implementation agent

**Prepared:** 2026-08-21

**Terminal condition:** every PRD definition-of-done item passes with current
evidence

Earlier loops, now superseded, are in [the archive](archive/GOAL_LOOP_HISTORY.md).
