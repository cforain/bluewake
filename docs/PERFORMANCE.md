# Making BlueWake faster

The plan for frame rate and slowdowns: what players hit, what is ruled out, the levers in order of payoff for
effort, and the fast way to test them. [PRIORITIES.md](PRIORITIES.md) places this work among everything else.
Owner: Chris. Written October 8, 2026; add every result below as it comes in.

## What players hit

Seventeen session logs attached to issues (#137, #159, #155, #61, #97, #65, #80, #107) and the Steam Deck reports,
read on October 8:

| Machine | Where | Game speed when slow | What limits it |
| --- | --- | --- | --- |
| Ryzen 7 2700, 8 cores (#137), Smooth Motion 120 | Outset | 21 to 22 game frames a second | Game thread (27 s), Smooth Motion stepping down (21 s), late frames (14 s), graphics thread (8 s) |
| i7-6500U, 2 cores (#159) | Outset, title | 38 to 65% | Game thread, every slow second |
| i7-4790K, 4 cores (#97) | Title | 79 to 85% | Game thread; the graphics thread 70 to 77% busy |
| Ryzen 7 7840HS, Linux, Vulkan | Outset, bird scene | median 91%, lowest 74% | Game thread |
| Steam Deck (Linux) | Outset | about 22 FPS | Game thread, about 30% short |
| i9-9900K, Ryzen 5800X, Radeon 860M laptop | Title, Outset | 90% and up | Little |
| Mac M4 | Everywhere | 98 to 100% | Nothing |

Almost every slow second is the **game thread**: the translated game code plus the runtime around it. It is too
much work for one core of an older or mobile x86 CPU, and just enough for an Apple M4. Resolution and GPU settings
don't change it. The slow places are Outset and the title flyover, which every player sees first.

## Ruled out or small

- **Denormal floats:** the game sets non-IEEE mode at boot, so flush-to-zero is on all session (jkoehler11, #59).
- **The native entries** (#179): measured on October 2 at about 1% of the game thread together
  ([NATIVE_ENTRIES_2026-10-02.md](status/NATIVE_ENTRIES_2026-10-02.md)). Worth having, not a fix.
- **GPU and resolution:** the logs show the GPU waiting, not working.
- **`-O3` and `-mcpu`:** neutral on the Mac (September).
- **The DSP:** already high-level on every platform.
- **The Linux bird scene at 4%:** an OpenGL ES fallback; with Vulkan its lowest is 74%.

## The levers, in order

### 1. The instruction gap: lean block copies (biggest)

*Evidence:* on the same Galaxy Z Fold 7, LiquidAzir measured BlueWake's game thread at about 158 M instructions
per retrace on Outset, against 110 M for his port built from Wind Waker Recomp's translation (#93). That is 30%,
about what the Steam Deck is short. The most likely difference between the two is the prepaid block copies:
Elliott's builder makes lean copies of almost every block (443,166) and drops the bookkeeping stores of plain loads
and stores, while BlueWake's makes conservative copies that skip nearly every block touching memory. Elliott
measured his set at 26.3 to 23.6 ms of game thread a frame on four cores, and it is in Wind Waker Recomp's
Windows builds.

*Why it isn't on:* on October 2 Elliott's version passed 30,000 function comparisons but differed in BlueWake's
strict boot-route comparison, which demands the exact same guest state at the same cycle: the final PC and 22 of
600 samples differed. Dropping the bookkeeping stores moves when interrupts land by a few cycles, so this is
expected. It is not, on its own, evidence of a gameplay bug.

*The decision this needs (Chris, with Elliott):* for performance changes, accept "plays the same" instead of
"cycle-exact". That means the same milestones on the boot and Outset routes within a few frames, saves that load
and play, cutscene audio, and long sessions without a crash or a soft lock, as Elliott's builds were judged. Keep
the strict comparison for correctness fixes.

*Then:* bring Elliott's block preparation in behind a builder flag (`--lean-blocks`), and run one build each on
Linux and Windows. Measure with the benchmark below, play the routes, and make it the default if both hold.
*Expected:* 10 to 30% less game-thread work. *Effort:* a few days and two builds.

### 2. Code the training skipped is compiled for size (cheapest test)

*Evidence:* the Windows and Linux builders train on the opening and a tour of warps, then compile code the training
never ran as cold: optimized for size, and at `-O1` with tiering. The tour has no cutscenes, combat or bosses, so
that code is the slow kind on x86. The Mac and iPhone build compiles everything at `-O2` and only uses the profile
for the hottest chunks. When the Apple build tried `-O1` everywhere, the iPad dropped from 30 to 26 FPS
([BUILDER.md](BUILDER.md)).

*Test:* build once with `--no-cold` (added October 8: every chunk at `-O2`, profile-guided size optimization
off) and compare the bird scene, a dungeon and Outset with the default build. *Expected:* nothing at Outset, which
is trained; up to about 15% in scenes the training skips. *Effort:* one longer build.

*If it helps:* make it the default, or train on a longer tour that plays cutscenes and fights, or ship a profile
trained by maintainers over a long playthrough. The last also lets players skip the 30-minute training run, which
first-launch builds need anyway ([DIRECTION.md](DIRECTION.md#1-no-game-code-in-any-release)).

### 3. Smooth Motion steps down and stays down (how it feels)

*Evidence:* on #137's eight-core Ryzen at 120 FPS, the game ran at 21 to 22 game frames a second on Outset.
Smooth Motion went from 3 in-between frames to 1, then 0, waiting 3, then 6, then 12 seconds before coming back.
Half of that log's slow seconds kept full game speed: they were the pacing, not the game. The rule was tuned on
four efficiency cores, where in-between frames compete with the game thread. On eight cores they don't. *Change:*
keep in-between frames when the CPU has cores to spare, and come back about a second after a hitch, as Wind
Waker HD Recomp's v0.2.7 does. Runtime only, no game module rebuild. *Expected:* fewer visible drops, not a faster
game.

### 4. Say when the renderer falls back

A missing Vulkan loader on Linux silently meant OpenGL ES at a fraction of the speed. One line on screen and in
the log. Runtime only.

### 5. The graphics thread on four-core CPUs

*Evidence:* the i7-4790K's graphics thread is 70 to 77% busy when the game is slow, and #86's is 92 to 98%; it
competes for the same few cores. *First step:* profile it at the benchmark spot.

### 6. Smooth Motion on two-core CPUs

#159's two cores run the game at 38 to 65% even with Smooth Motion off, so this alone won't fix them. Start it
off on CPUs with four threads or fewer, so it never makes things worse.

The long-term lever is native rendering, replacing the CPU-side conversion of drawing commands, as Wind Waker HD
Recomp does for the Wii U's graphics library. It comes after 1, 2 and 5.

## How to test without the long loop

The slow part is compiling the game module (17 to 45 minutes on a desktop, longer on a laptop). Everything else is
minutes.

- **Measure with a script, not by playing.** \`scripts/bench_tour.py\` (to write) uses pieces the builders already
  have. It copies the tester's own memory card and places a save on Outset (\`scripts/card_set_restart.py\`), then
  continues it with the pad script the save acceptance uses, which reaches control in about 833 retraces. Then it
  warps through Windfall, Dragon Roost Cavern, the sea and back (\`BLUEWAKE_TEST_WARP\`, the training tour's stops)
  with \`BLUEWAKE_WALL_PACE=0\`, so the game runs as fast as the machine allows. It prints game frames a second at
  each stop, headless and rendered, plus \`BLUEWAKE_GUEST_CHECKPOINT_INTERVAL\` hashes that show two builds behave
  the same (jkoehler11's check on #178). One unattended run takes a few minutes, needs nothing private shared,
  and gives the same numbers on any machine.
- **Save states** (\`BLUEWAKE_LOAD_STATE\`) cover a scene the tour can't reach, like the bird scene. They're made
  from a maintainer's own card and never committed or attached.
- **Runtime and host changes** (items 3, 4 and 6) rebuild the app without recompiling the game module.
- **Build-flag changes** (items 1 and 2) are one unattended build each, on the fastest machine available: pdale-boop's
  i5-12600KF builds in about 17 minutes, jkoehler11's Ryzen 9 5900X on Linux.
- **One change per build,** and its result written below.

## Plan

| Order | Step | Who | Done when |
| --- | --- | --- | --- |
| 1 | `scripts/bench_state.py` and the three save states | Codex; Chris makes the states | One command prints speed and checkpoints for two builds |
| 2 | LiquidAzir's two Android builds, same spot: game frames a second and their build options | LiquidAzir (asked on #93) | The 30% instruction gap has a frame-rate number |
| 3 | `--no-cold` against the default, same machine | jkoehler11 on Linux or pdale-boop on Windows | Bird scene, dungeon and Outset numbers |
| 4 | Smooth Motion pacing (3), fallback message (4), two-core default (6) | Codex, in the shared runtime | Checked on Chris's Ryzen 7 5700U; in the next build |
| 5 | The acceptance standard for performance changes (1) | Chris, with Elliott | Written in this file |
| 6 | Elliott's lean block copies behind `--lean-blocks`, A/B, routes played | Codex, a Linux and a Windows tester | Default on, or the reason it isn't |
| 7 | Graphics thread profile on a four-core CPU (5) | A tester with one, or the i7-4790K's owner | The hot paths named |
| 8 | A maintainer-trained profile shipped with the builder | Codex | Players skip training; cutscenes trained |

Targets, measured with the benchmark: Outset at 30 game frames a second on a Ryzen 7 2700 (21 to 22 today), and a
Steam Deck holding 30 (about 22 today). No promise of a date: these need levers 1 and 2 together.

## Results

| Date | Change | Machine | State | Before | After | Same behavior? |
| --- | --- | --- | --- | --- | --- | --- |
