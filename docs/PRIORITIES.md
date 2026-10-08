# BlueWake priorities

The ranked list of what to fix and build next. Read this first if you are picking up work in this
repository, then [AGENTS.md](../AGENTS.md) for the rules and [GOAL_LOOP.md](GOAL_LOOP.md) for the current work loop
(release 0.6.0).

Updated October 8, 2026 (JST) after the first pass over replies to 0.6.0 ([October 8 triage](status/TRIAGE_2026-10-08.md)).
Before that: the [October 7 fix pass](status/FIXES_2026-10-07.md) and a pass over GitHub and the Discord
conversations the same day. Owner: Chris.
Today's evidence is in [the October 7 triage record](status/TRIAGE_2026-10-07.md); older investigation
notes are in [TECH_DEBT.md](TECH_DEBT.md) and the dated files in [status/](status/).

## Right now

The short version, as shared with the community on October 7:

1. Done: 0.6.0 was published on October 8 with the fixes in the "Shipped in 0.6.0" table below. Each reporter has been asked to confirm.
2. Performance on everyday CPUs (Steam Deck, laptops, older desktops): measure, then cut the game thread's per-frame work (Tier 2, rank 1).
3. The remaining game-breaking bugs: missing sound in later cutscenes (#65), controllers with scrambled layouts (#61, #155), the cloud and wave flicker (#136).
4. The native Linux build into BlueWake (#107).
5. Community tools and test saves (the "Community ideas" table).

## What's next after 0.6.0

The plan as of October 7, 2026, agreed with Chris. Answer "what are we doing next for BlueWake?" from this section,
checked against current issues and pull requests.

**0.6.0 is out** (October 8, [release record](status/RELEASE_0.6.0.md)). Each fix's issue asks its reporter to confirm; close an issue only when they do. How well each fix was proven at release:

| Fix | Proven by | Still needs |
| --- | --- | --- |
| Dungeon maps (#74) | Reproduced and fixed on the Mac with a save in Dragon Roost; three other scenes unchanged | Windows (Direct3D 12): the 0.6.0 Windows run, check c |
| Intro music (#97) | Captured audio on the Mac, a physical iPad and the iPad simulator; two players' Windows logs show the same cause | Windows with the fix on: check a, which decides #172 |
| Controller as player 1 (#61) | A test with the real SDL and Aurora libraries reproduces the report and passes with the fix | A physical controller; the scrambled layout is a separate open problem |
| Baton (#156) | Cause in code; a live Mac trace of the conducting flag | Conducting with a physical controller |
| Left stick (#138) | A test reproduces the reporter's numbers and fails on the old code | A physical stick |
| Aim invert (#154) | New option; compiled and tested in CI | Trying it in game |
| VS2022 builder (#153) | The reporter's error reproduced with LLVM 18 and 20 | The reporter's rebuild |

**Then, in order:**

1. **A shared performance benchmark.** One save placed at the same spot on Outset with `scripts/card_set_restart.py`
   (sea, room 44), the same settings and warm caches, read from the session log's `[perf-summary]` and `[fps-dip]`
   lines. The Mac, a Windows laptop and the Steam Deck use the same test, so every performance change is measured,
   not guessed. KongMing's RecompCore work starts from it too.
2. **Smooth Motion's cost on small CPUs** (Tier 2, rank 3). Its helper thread used 62 to 70% of a core at the title.
   On 2-core laptops (#159) that competes with the game. Measure it with the benchmark, then decide whether it should
   start off, or switch off by itself, on CPUs with few cores. A cheap first win if the numbers support it.
3. **The game thread** (Tier 2, rank 1), the biggest lever. Find which of Elliott's lean memory block copies cause the
   boot-route difference, keep the safe ones, measure. Expect roughly 5 to 10%, not a doubling. KongMing's
   RecompCore pull requests (aiming at the about 30% the Steam Deck needs for 30 FPS) belong here, each with
   before and after numbers from the benchmark and identical game behavior.
4. **The graphics thread** (Tier 2, rank 2). Profile command conversion and vertex decoding at the benchmark spot.
5. **The remaining game-breaking bugs:** missing sound in later cutscenes (#65), scrambled controller layouts
   (#61's second half, #155), the cloud and wave flicker (#136).
6. **Linux release** (#107), once it is on current `main` and audited. Steam Deck speed is items 1 to 4, not a
   Linux gate.
7. **iPhone and iPad builds from Windows through PadMint** (#100, draft). It needs a full end-to-end run on a real
   PC and an install on a device before it ships. Mac apps can't be built on Windows.
8. **Long term: native rendering** (wowjinxy's idea), replacing the CPU-side drawing conversion piece by piece with
   the decompilation. The largest gain and the most work, after items 3 and 4.

No promise of 30 FPS on a Steam Deck yet: no single change gets there, so it takes several measured gains stacked
together.

## How this list is ordered

1. **Game-breaking bugs first:** a crash, a soft lock, a controller that can't play, missing sound or
   drawing that players need, or a regression in the current release.
2. **Performance next:** low or uneven frame rates are the most common complaint, on every platform.
3. **Everything else after:** narrower bugs, then requested features, then new platforms.

Within a tier, what affects the most players and has the clearest fix comes first. Re-rank as soon as
evidence changes: a new crash or data-loss report goes straight to the top.

Keep the states apart: *suspected* (a hypothesis), *cause found* (shown in code, logs or a reproduction),
*fixed in main* (merged), *shipped* (in a release) and *confirmed* (the reporter says it works). Only
close an issue when its reporter confirms, or it is a clear duplicate. When you change a row, update the
issue, this page and, for Windows checks, [WINDOWS_TASKS.md](WINDOWS_TASKS.md) in the same pull request.

## Shipped in 0.6.0

Published October 8, 2026 from `806d65c` (Windows zip built from `4eb41f0`, the same game and app code). What each
still needs is a confirmation, not a release:

| Shipped in 0.6.0 | Issue | Still to confirm |
| --- | --- | --- |
| Dungeon maps draw their grid and rooms (RecompCore patch 0157) | [#74](https://github.com/chrissotraidis/bluewake/issues/74) | Windows check from the [task list](WINDOWS_TASKS.md#in-main-waiting-for-a-windows-build) |
| A controller recognized late, or left as player 2, plays as player 1 (October 7) | [#61](https://github.com/chrissotraidis/bluewake/issues/61) | A physical controller that needs `gamecontrollerdb.txt` |
| The Wind Waker baton is no longer mirrored (October 7) | [#156](https://github.com/chrissotraidis/bluewake/issues/156) | Conducting with a controller |
| No big dead zone or jump on the left stick (RecompCore patch 0159, October 7) | [#138](https://github.com/chrissotraidis/bluewake/issues/138) | Slow aiming, diagonals and drift on a physical controller |
| Intro music after the title music: on by default everywhere ([#163](https://github.com/chrissotraidis/bluewake/pull/163), [#172](https://github.com/chrissotraidis/bluewake/pull/172)) | [#97](https://github.com/chrissotraidis/bluewake/issues/97) | Players on Windows waiting for the title music, then a new file |
| Windows builder: Visual Studio 2022 builds again (October 7) | [#153](https://github.com/chrissotraidis/bluewake/issues/153) | The reporter's Visual Studio 2022 build |
| Option: invert the left stick's up and down when aiming (October 7, [#166](https://github.com/chrissotraidis/bluewake/pull/166)) | [#154](https://github.com/chrissotraidis/bluewake/issues/154) | Menu check on Windows |
| Linux port's shutdown fix for every platform (RecompCore patch 0158, [#167](https://github.com/chrissotraidis/bluewake/pull/167)) | [#56](https://github.com/chrissotraidis/bluewake/issues/56) | Windows quit check |
| The session log names the controller mapping in use ([#165](https://github.com/chrissotraidis/bluewake/pull/165)) | [#61](https://github.com/chrissotraidis/bluewake/issues/61) | None (a log line) |
| Touch controls no longer stay held after Apple menus open | none (found in testing) | Physical iPhone/iPad touch check |
| Opt-in Pictobox fix, `BLUEWAKE_CACHE_FLUSH_FALLBACK=1` (still off by default) | [#13](https://github.com/chrissotraidis/bluewake/issues/13) | Windows and physical iPad check; then decide the default |

Only Chris publishes releases. Follow [RELEASE.md](status/RELEASE.md) and run the release audit.

## Tier 1: bugs that break the game

| Rank | Problem | Who it hits | What we know | Fix and next step |
| --- | --- | --- | --- | --- |
| 1 | **Intro and cutscene music missing** ([#97](https://github.com/chrissotraidis/bluewake/issues/97), [#65](https://github.com/chrissotraidis/bluewake/issues/65)) | All platforms. Seen on Windows, a Mac M4 and a physical iPad | *Shipped in 0.6.0 on every platform*: disc reads now complete after the game marks them pending, so the intro track plays after the title music ([cause](status/TRIAGE_2026-10-06.md#title-to-intro-reproduction-and-callback-ordering), [checks](status/FIXES_2026-10-07.md#intro-music-97)). Windows has it on by default too since #172; `BLUEWAKE_DEFER_DVD_COMPLETION=0` turns it off for a comparison. #65's bird scene may be a separate cause: DonatelloEsq got its sound back only after turning off the HD pack, Better Wind Waker and mouse camera together. | Reporter confirmation on Windows. October 8: two logs without the fix (Mac M4, Linux) show the bird scene (`sea` event 251) losing its music exactly as the intro did, so 0.6.0 may fix it too ([details](status/TRIAGE_2026-10-08.md#the-bird-scene-one-cutscene-two-problems-65-59)). Next: a 0.6.0 run from a new file to that scene (asked on #65). |
| 2 | **Some controllers don't work at all** ([#61](https://github.com/chrissotraidis/bluewake/issues/61) 8BitDo GameCube mod kit, [#155](https://github.com/chrissotraidis/bluewake/issues/155) GameCube controller on a Mayflash adapter) | Windows and Mac, any controller SDL doesn't know without `gamecontrollerdb.txt`, and anyone with several controllers | *Detection shipped in 0.6.0*: a connected controller takes player 1 whenever nobody has it ([details](status/FIXES_2026-10-07.md#controllers-and-player-1-61)); the reporter confirmed that connecting late gets it detected. *Layout suspected*: its buttons and sticks are scrambled with both his line and the stock file. SDL uses a mapping with a `crc:` field only on an exact CRC match, and the stock 8BitDo line puts the right stick on a2/a3 and L/R on a5/a4 where his tool found a3/a4 and b6/b7. The log now names the mapping in use (#165). #155 has no log yet. | #61: his one-line `gamecontrollerdb.txt` works with B and X swapped (October 7); asked him to fix those under Controller buttons on 0.6.0, then close. #155: the 0.5.0 log shows the adapter as four GameCube controllers, all removed 12 seconds in; asked for a 0.6.0 log with the controller in port 1 ([details](status/TRIAGE_2026-10-08.md#controllers-61-155)). |
| 3 | **Wind Waker baton left and right reversed** ([#156](https://github.com/chrissotraidis/bluewake/issues/156)) | Windows and Mac with the fast right-stick camera on (the default); new in 0.5.0 | *Shipped in 0.6.0* (fixed October 7): #44's C-stick flip for the game's own camera is skipped while the game's conducting flag is set, confirmed live on the Mac ([details](status/FIXES_2026-10-07.md#the-wind-waker-baton-156)). | Reporter confirmation; play each song with a controller. |
| 4 | **Clouds and distant waves flicker** ([#136](https://github.com/chrissotraidis/bluewake/issues/136)) | Windows on NVIDIA at 60 and 120 FPS; a regression from 0.4.0 | *Suspected*: 0.5.0 brought in water/HUD interpolation, transform reuse, texture mip and blending changes (RecompCore patches 0152 to 0155). Not reproduced on the Mac (Metal). | *Cause narrowed* (October 8): a second reporter (RTX 5070 Ti) shows it clean at 30 and flickering at 120, and the Outset forest's fog flickers too. Look at how the in-between frames carry moving-texture draws (patches 0152 to 0155). [Capture steps](WINDOWS_TASKS.md#flickering-capture-136). |
| 5 | **Left stick dead zone, then a jump to about 22%** ([#138](https://github.com/chrissotraidis/bluewake/issues/138)) | Every controller player; worst for fine aiming (Mirror Shield) | *Shipped in 0.6.0* (fixed October 7, RecompCore patch 0159): Aurora's cutoff is off for player 1's controller and the stick's full travel is scaled to a GameCube stick's, so the game's own clamp is the only dead zone ([details](status/FIXES_2026-10-07.md#the-left-stick-138)). | Reporter confirmation: slow aiming, diagonals, full travel and drift at rest on a physical controller. |
| 6 | **Soft lock in the Forsaken Fortress** ([#76](https://github.com/chrissotraidis/bluewake/issues/76)) | One Windows report | *Unverified*: a Moblin knocked off a ledge mid-capture. May be the original game. | Reproduce with a copied save placed in the fortress (`scripts/save_set_restart.py`); compare with Dolphin before changing anything. |
| 7 | **HD texture packs: dark shading and orange hair** ([#80](https://github.com/chrissotraidis/bluewake/issues/80)) | Windows, Radeon 860M, with any HD pack (PNG or DDS) | *Unreproduced* on the Mac with a PNG pack. The reporter's 0.5.0 log covers only 30 seconds at the title screen (three textures replaced), so it shows the setup but not the problem. | October 8: packs named (Hypatia 2.0 DDS-Full, Hypatia's PNG release), a longer log with no renderer errors, and Smooth Motion, resolution and filtering make no difference. Asked whether Dolphin shows the same; next, the PNG pack on the Mac in the same spot. |
| 8 | **Pictobox shows the previous photo** ([#13](https://github.com/chrissotraidis/bluewake/issues/13)) | All platforms | The 0.5.0 freeze is fixed. The stale second preview is repaired by the opt-in flag above in Mac and iPad simulator runs. | Physical iPad and Windows checks, then decide the default (see "Shipped in 0.6.0"). |
| 9 | **Pirate ship flag has no texture** ([#69](https://github.com/chrissotraidis/bluewake/issues/69)) | Windows 0.3.0 report | *Needs info*: not rechecked on 0.5.0. The sail module keeps its texture in its own data, like Molgera's floor (#126, fixed). | Load a save near the ship and check on the Mac; if it is blank, trace the sail's texture address as #126 was traced. |

## Tier 2: performance

Players on older or mid-range CPUs see 20 to 25 FPS on Outset and in heavy scenes, whatever their GPU.
This is the most visible problem after the bugs above, and it is on BlueWake's side.

| Rank | Bottleneck | Reports | What we know | Next step |
| --- | --- | --- | --- | --- |
| 1 | **Game thread (the translated game code)** | [#137](https://github.com/chrissotraidis/bluewake/issues/137) (Ryzen 7 2700), [#59](https://github.com/chrissotraidis/bluewake/issues/59) (bird scene), [#159](https://github.com/chrissotraidis/bluewake/issues/159) (i7-6500U laptop: 10 to 20 FPS where Dolphin gets 30 to 40), Steam Deck on the Linux port (22 FPS on average, CPU-bound, about 30% short of 30) | In #137's log, 35 of 83 seconds ran below full speed (lowest 65%); 27 name the game thread. On the Mac, the host's per-block bookkeeping costs about a sixth as much as the game code itself, so fewer block boundaries is the lever. The Windows release has BlueWake's conservative prepaid block copies, which skip nearly every block that touches memory: Elliott's `lean_memory.py` then changes 0 accesses and his native entries certify 0 of 15. His full transform failed BlueWake's strict boot-route comparison on October 2 ([findings](status/FIXES_2026-10-07.md#performance-findings)). | Find which block forms cause that divergence, chunk by chunk; copy the safe ones with lean accesses; measure on Windows in the same Outset spot. James Koehler-Killeen (KongMing) offered to measure on the Steam Deck first (`perf record`, `[fps-dip]` lines), then send small RecompCore PRs with before/after numbers ([plan](https://github.com/chrissotraidis/bluewake/pull/107)). October 8: the bird scene runs at 4 to 20% on a Linux x86 laptop and at 99% or more on a Mac M4; suspected denormal floats on x86 (FTZ/DAZ is on only when the game sets FPSCR NI); asked for a `perf record` there ([details](status/TRIAGE_2026-10-08.md#the-bird-scene-one-cutscene-two-problems-65-59)). #179's 0 of 15 native entries is the conservative copies, not drift; the comparison tests need a Linux loader to be rerun ([details](status/TRIAGE_2026-10-08.md#native-entries-certify-0-of-15-179)). |
| 2 | **Graphics thread (GX worker) converting the game's drawing to GPU work on the CPU** | [#86](https://github.com/chrissotraidis/bluewake/issues/86) (i7-6950X, RTX 3080), Steam Deck reports on Discord | In Outset the GX worker is 92 to 98% busy and the game drops to 55 to 90% speed; resolution barely matters. The title flyover is about 20,000 draws a frame. The app's own optimization profile cut the GX worker's time per frame from about 16.9 to 14 ms on an i9 (October 2), and older Visual Studio builds now skip that profile with a note (#153). | Profile the GX worker in the same Outset spot with warm caches; find the hot paths in command conversion and vertex decoding. |
| 3 | **Smooth Motion's own cost** | #137, [#79](https://github.com/chrissotraidis/bluewake/issues/79) | At 120 FPS the in-between frames cost CPU time and pause after every slowdown (six step-downs in #137's two minutes); its helper thread used 62 to 70% of a core at the title. | Compare the same spot at 30, 60 and 120 to measure the cost; make sure the pause is not triggered by the interpolation's own work. |
| 4 | **Build time** | [#104](https://github.com/chrissotraidis/bluewake/issues/104) (3 hours on an M4 MacBook Air), [#153](https://github.com/chrissotraidis/bluewake/issues/153) (45-minute compile on an i5-12600KF) | The Windows builder assumes 2.5 GB per compile job, but #153 measured about 0.3 GB per clang process with 19 GB free. Training takes about 30 minutes of the Windows build. | Recheck the memory-per-job estimate to allow more jobs; see whether a reviewed profile could let players skip training. |

Use matched comparisons: same scene, settings, warm caches and hardware, one change at a time. Do not
tell players to lower settings as the fix; the logs show the limit is CPU time per game frame.

## Tier 3: smaller bugs, easy wins and support

| Problem | Issue | Fix |
| --- | --- | --- |
| Windows build fails with Visual Studio's clang older than 22 (`app.profdata` format) | [#153](https://github.com/chrissotraidis/bluewake/issues/153) | *Shipped in 0.6.0* (fixed October 7): the builder tests the profile with the same toolchain's `llvm-profdata` and builds the app without it, with a note. Checked with LLVM 18, 20 and 22 against the real profile; waiting for the reporter's confirmation. |
| Portable mode still writes `imgui.ini` to `%APPDATA%` | [#64](https://github.com/chrissotraidis/bluewake/issues/64) | Fixed in [#184](https://github.com/chrissotraidis/bluewake/pull/184) (RecompCore patch 0160): `imgui.ini`, controller remaps and keyboard bindings follow the portable folder. Waiting for a Windows run. |
| CPUs without AVX2 can't run the Windows build | [#77](https://github.com/chrissotraidis/bluewake/issues/77) | 0.5.0 now says so instead of closing silently. No build for those CPUs is planned. |
| Waiting on the reporter to confirm a shipped fix | [#55](https://github.com/chrissotraidis/bluewake/issues/55), [#58](https://github.com/chrissotraidis/bluewake/issues/58), [#66](https://github.com/chrissotraidis/bluewake/issues/66), [#73](https://github.com/chrissotraidis/bluewake/issues/73) | Close each when its reporter confirms. |

## Enhancements

In order. None of these should displace a Tier 1 or Tier 2 item.

1. **Controller picker** for player 1 in both menus ([#155](https://github.com/chrissotraidis/bluewake/issues/155)), once its log shows whether the Mayflash adapter needs it.
2. **Stick dead zone setting** ([#138](https://github.com/chrissotraidis/bluewake/issues/138)), only if players with worn sticks still need one after the October 7 fix.
3. **Invert the left stick's up and down while aiming** ([#154](https://github.com/chrissotraidis/bluewake/issues/154)): an option in both menus, October 7 ([#166](https://github.com/chrissotraidis/bluewake/pull/166)).
4. **Ultrawide** ([#70](https://github.com/chrissotraidis/bluewake/issues/70)): needs the widescreen code's camera and HUD values extended past 16:9.
5. **Wind Waker HD-style options** ([#152](https://github.com/chrissotraidis/bluewake/issues/152)): Hero Mode, moving while aiming, the shorter Triforce quest. These would be built-in options like Better Wind Waker's.
6. **Graphics hotkey** ([#108](https://github.com/chrissotraidis/bluewake/issues/108)): waits for Wind Waker Recomp's HD renderer to be brought over.
7. **Mod folder for game files and models** ([#152](https://github.com/chrissotraidis/bluewake/issues/152)): BlueWake reads files from the disc image and has no file replacement path yet. Large.
8. **Wii U-style interface** ([#57](https://github.com/chrissotraidis/bluewake/issues/57)): not planned now.

Open contributor pull requests: FPS overlay position ([#106](https://github.com/chrissotraidis/bluewake/pull/106)) and centering
the window ([#89](https://github.com/chrissotraidis/bluewake/pull/89)) need review against current `main`.

## Community ideas (Discord, October 7)

| Idea | From | How it fits |
| --- | --- | --- |
| Rework parts of RecompCore for speed; about 30% is needed for 30 FPS on a Steam Deck | KongMing | Tier 2, rank 1. Measure first, then small pull requests to RecompCore `bluewake-next` with matched before/after numbers and identical game behavior (the boot-route comparison). |
| Replace the CPU-side GX conversion with native rendering bit by bit, using the decomp (about 70% done) | wowjinxy | Long-term. It extends what the certified native J3D, skinning and math replacements already do; each swap needs a comparison test. Tier 2 rank 1 (game thread) comes first. |
| A save editor | Dale | Welcome as a separate tool. It has to keep both copies of each quest log and their checksums right, as `scripts/save_set_restart.py` and the Dolphin importer do, and work on copies. |
| Test saves at key scenes: a card in Ganon's Castle with New Game+, and about 45 save states from Outset to Ganon | Discord testers | Reproduce scene bugs without playing there: #65's bird scene, #76's fortress, #69's ship, dungeon maps. Keep them private; never commit or attach them. |

## Platforms

| Platform | Where it stands | What it needs |
| --- | --- | --- |
| Linux ([#56](https://github.com/chrissotraidis/bluewake/issues/56), [PR #107](https://github.com/chrissotraidis/bluewake/pull/107)) | jkoehler11 (KongMing on Discord) checked saves, controllers, settings, HD packs and quitting on his desktop and a Steam Deck. His shutdown fix is in RecompCore and pinned in `main` (#167). His Ryzen 9 5900X holds 30; the Steam Deck averages 22, the same CPU limit Windows players hit (Tier 2). | Bring current `main` in and drop the PR's own pin, CI green, a package audit. Steam Deck speed is shared performance work, not a Linux-only gate. Chris approves a Linux release. |
| Android ([#75](https://github.com/chrissotraidis/bluewake/issues/75), [PR #93](https://github.com/chrissotraidis/bluewake/pull/93)) | LiquidAzir's port builds an APK from the player's disc. Quiet since October 5; on October 8 he was asked whether he's still on it, with an offer to carry it forward on a branch that keeps his commits. | The iPhone app's menu and touch layout, current `main`, and performance evidence, as asked on the PR. The Mac has the Android SDK and NDK; an Android device is needed to test. |
| Windows through PadMint ([PR #46](https://github.com/chrissotraidis/bluewake/pull/46), [PR #100](https://github.com/chrissotraidis/bluewake/pull/100)) | Parked. | A maintainer decision; see [PROPOSALS.md](PROPOSALS.md). |
| European disc ([#60](https://github.com/chrissotraidis/bluewake/issues/60)), Intel Mac ([#48](https://github.com/chrissotraidis/bluewake/issues/48)), Switch ([#62](https://github.com/chrissotraidis/bluewake/issues/62)) | Not planned now. | Revisit after Tier 1 and 2. |
