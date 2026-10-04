# Windows tasks

Work that needs a Windows PC, in priority order. Elliott owns Windows; anyone with the hardware can help.
Read [AGENTS.md](../AGENTS.md) first. One pull request per task, results in the linked issue.

**You need:** Windows 10 or 11 (x64), a CPU with AVX2, a Direct3D 12 GPU, your own USA `GZLE01` revision 0
disc, and the build tools in [BlueWake on Windows](WINDOWS.md#what-you-need).

**Where things stand (October 4, 2026):** the Windows download on the
[Releases page](https://github.com/chrissotraidis/bluewake/releases/latest) is still Elliott's Wind Waker
Recomp 0.4.0 build. BlueWake `main` has fixes that build doesn't, and its Windows build from a disc has
not yet been run on real hardware.

## 1. A Windows build from BlueWake `main`

**Why:** ships fixes Windows players are waiting for: the Pictobox freeze (#13), Swap A and B (#55), the
camera turning the other way in water (#73), the "Smooth Motion paused" counter, Smooth Motion **off** by
default, and the `[music-stream]` log line (#65).

1. Build from a clean checkout of `main`: `python scripts/windows/build.py "D:\path\to\GZLE01.iso"`.
2. Run checks 1 to 4 of the [Windows checklist](WINDOWS_ACCEPTANCE.md), and confirm each fix above.
3. Package it like Wind Waker Recomp's releases (its `scripts/windows/package_release.py` is a starting
   point; bring it over as a pull request): `BlueWake-vX.Y.Z-windows-x64.zip` holding the build folder,
   licenses and a `BuilderProvenance.json`, **without `nodtool.exe`** (it embeds Wii keys), plus a source zip.
4. Attach both to a **draft** release on BlueWake. Chris runs the release check and publishes; nobody else
   publishes releases.

**Done when:** the draft has both zips and the checklist results are posted.

## 2. A clear message on CPUs without AVX2 (#77)

**Why:** on an older CPU, such as an Intel Core i7 860, `BlueWake.exe` exits silently.

The app itself is compiled with `-march=x86-64-v3`, so the check has to run before any AVX2 code: a small
function built for plain x86-64 (for example `__attribute__((target("arch=x86-64")))`) in an early C runtime
initializer, which checks CPUID and shows a message box naming the requirement, then exits.

**Done when:** under Intel SDE emulating an older CPU (`sde64 -nhm -- BlueWake.exe`), the message appears
instead of nothing, and normal launches are unchanged.

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
| #65 missing music in cutscenes | With task 1's build, check the `[music-stream]` lines in an affected scene. |
| #59, #72, #79, #86 slowdowns | Measure the scenes with the triage script. The #76 log already shows the Forsaken Fortress exterior limited by the GX worker (83 of 97 slow seconds). |

Close an issue only when the reporter confirms the fix, or with a clear explanation.
