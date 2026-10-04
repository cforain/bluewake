# BlueWake goal loop

## Current loop: Mac and iPad stability, October 4, 2026

Make BlueWake steadier on Mac and iPad and keep the docs true, without growing the project. Windows
belongs to Elliott (his hardware); a native Linux port is not planned (players can try Proton, README FAQ).

### Limits

- Use one Apple Silicon Mac: the Mac app and the iOS Simulator. No physical iPad in this loop; anything
  that needs one is labeled `needs-device` and left for a device session.
- No new platforms or features. Fix what players report, in small changes. Anything risky is off by default.
- One concern per pull request, following [AGENTS.md](../AGENTS.md).

### Steps

| Step | Done when |
| --- | --- |
| 0. Docs | README, AGENTS.md, this file, [migration status](MIGRATION_STATUS.md), the build guides and the Windows pages agree with `main`. |
| 1. Triage | Every open issue has a platform label and one status: `needs-info`, `needs-windows`, `needs-device` or `confirmed`. Duplicates point to one issue. Nothing is closed without the reporter, except clear duplicates. |
| 2. Reproduce and fix on the Mac | With a Mac build from current `main`, each Mac-reproducible report (music in the intro and scripted scenes, the slow bird and Aryll scenes, dungeon maps, the pirate flag, the Forsaken Fortress soft lock, Smooth Motion at 120 Hz, HD texture shading) is fixed with before and after evidence, explained, or labeled. |
| 3. iPad in the Simulator | The iPad app builds and runs in the Simulator with no regressions in menus, touch controls or saves. |
| 4. Release candidate | A Mac/iPad app-only release (no game code) and its PadMint recipe are built from `main` and pass the release check. Chris decides whether to publish. |

### Each iteration

1. Pick the highest step that isn't done and name what will close it.
2. Reproduce before changing anything. A fix needs the same scene before and after, with the same settings.
3. Make the smallest change that addresses the cause, then run the host tests and the affected scene.
4. Update the issue in Chris's voice and the [migration status](MIGRATION_STATUS.md) when something changes.

Stop when every item is fixed, explained, or labeled as needing hardware.

Earlier loops, including the October 3 stability and migration loops, are in
[the archive](archive/GOAL_LOOP_HISTORY.md).
