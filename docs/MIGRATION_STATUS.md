# Wind Waker Recomp is moving to BlueWake

Updated October 3, 2026 (evening).

Elliott Tate's [Wind-Waker-Recomp](https://github.com/elliotttate/Wind-Waker-Recomp) and BlueWake are
combining into one project. BlueWake is where development continues. This page tracks what is done
and what is still open. The [migration log](WIND_WAKER_RECOMP_MIGRATION.md) records each step and
what was changed on Wind-Waker-Recomp.

New bug reports, feature requests and pull requests should go to
[BlueWake](https://github.com/chrissotraidis/bluewake/issues).

## Done

- Elliott's Windows port, rendering, camera, controls, settings, save state and performance
  work through his v0.4.0 release, and his later Windows branch, is merged into BlueWake `main` ([#37](https://github.com/chrissotraidis/bluewake/pull/37),
  [#38](https://github.com/chrissotraidis/bluewake/pull/38)). His commits keep his authorship, and
  jointly adapted changes credit him as co-author.
- The shared runtime lives in [chrissotraidis/RecompCore](https://github.com/chrissotraidis/RecompCore),
  branch `bluewake-next`. BlueWake's dependency lock selects the exact commit.
- On an Apple Silicon Mac, a complete build from a player's own disc works through PadMint and the
  BlueWake builder: translation, local training, compilation and packaging. The result was played
  with an actual game save followed by a separate reload.
- On a physical iPad, an in-place update kept existing saves and settings, and an actual game save
  reloaded correctly.
- On Windows, the app builds and passes its automated tests in GitHub Actions.
- Original 30 FPS game logic stays the default. Smooth Motion and experimental 60 FPS logic are off
  unless a player turns them on.

## Open

| Item | Owner | Status |
| --- | --- | --- |
| Windows build and gameplay on real hardware | Elliott | Not started. Building and playing from your own disc on Windows has not been tested yet. [Checklist](WINDOWS_ACCEPTANCE.md). |
| Elliott's work after v0.4.0 | BlueWake | Merged in [#40](https://github.com/chrissotraidis/bluewake/pull/40) and [#43](https://github.com/chrissotraidis/bluewake/pull/43): the save-state crash fix, steadier Smooth Motion pacing, shaders compiled on several threads and before play, the ubershader (Windows), lighter graphics work, Smooth Motion for cloth and colours, the wider speed training and the faster tiered build. Still to wire in: his second set of nine native functions, which BlueWake routes through its opt-in native options. |
| Random slowdowns | BlueWake | Logs now name the cause of each slow second and show when Smooth Motion is paused. On the iPad, single hitches no longer turn Smooth Motion off (before: off 35 of 40 seconds in the test). Next: measure the reported scenes. [Stability plan](status/STABILITY_PLAN_2026-10-03.md). |
| Elliott's recent uncommitted fixes | Elliott | To arrive as BlueWake pull requests. |
| Move open issues | Chris and Elliott | 27 open issues in Wind-Waker-Recomp (October 3) are to be recreated here with links back; the [migration log](WIND_WAKER_RECOMP_MIGRATION.md) describes how. GitHub cannot transfer issues between repositories owned by different accounts. The [stability plan](status/STABILITY_PLAN_2026-10-03.md) sorts them by whether they affect BlueWake. |
| Move open pull requests | Elliott and authors | Wind-Waker-Recomp [#17](https://github.com/elliotttate/Wind-Waker-Recomp/pull/17) (center window on startup), [#15](https://github.com/elliotttate/Wind-Waker-Recomp/pull/15) (FPS overlay position) and [#13](https://github.com/elliotttate/Wind-Waker-Recomp/pull/13) (Android port) are to be reopened against BlueWake, keeping their authors. The Android port is new platform work, reviewed separately. |
| Fresh build of current `main` | BlueWake | The iPad check used the current app with a game module built from an earlier revision. A completely fresh build from current `main` is next. |
| Longer gameplay session | BlueWake | About 30 minutes of real play with a controller and audio on Mac and iPad, to catch problems short checks miss. |
| Matched performance comparison | BlueWake and Elliott | Compare BlueWake with Wind-Waker-Recomp in the same scenes, settings and hardware. |
| Pictobox freeze | BlueWake | [#13](https://github.com/chrissotraidis/bluewake/issues/13). A fix passes on Mac. Windows confirmation is part of the checklist above. |
| Point Wind-Waker-Recomp to BlueWake | Chris and Elliott | Done October 3: its README, issue form and description point here. Archiving the fork waits until issues are moved, Windows is checked and both agree. |

Linux, other game regions and an Android port are later work. They are not part of this move.

## Releases

Public app releases are paused until the maintainer's release audit is clear. Build BlueWake yourself
from your own disc. Builds that contain game code are personal and must never be uploaded or shared;
only source and app-only packages without game code may be published.

## How to help

- Windows testers with a Direct3D 12 GPU: follow the [Windows checklist](WINDOWS_ACCEPTANCE.md) and
  report results in a BlueWake issue.
- Report bugs with your platform, the BlueWake commit you built and steps to reproduce.
- Attach your session log (iPhone/iPad: Help & Feedback › Share Session Log; Windows:
  `%APPDATA%\BlueWake\logs`). `python3 scripts/triage_session_log.py LOG` summarizes one.
- Keep game files, saves and personal builds out of issues and pull requests.

Detailed evidence: [reconciliation ledger](status/FORK_RECONCILIATION_2026-10-02.md).
