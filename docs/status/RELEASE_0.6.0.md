# BlueWake 0.6.0 release record

The working record for 0.6.0. The steps are in [GOAL_LOOP.md](../GOAL_LOOP.md). Fill in each check with the device,
the commit and what was seen. A row stays "not yet" until someone runs it.

## Candidate

| | |
| --- | --- |
| Version | 0.6.0, build 5 (`version.json`) |
| Candidate commit | `2c8a659416233864ab9d7a069e759bf5af558e2b` (merge of #170) |
| RecompCore | `35e037f285ded1b766b7110783b47c976fe2ed10` (patches 0157 to 0159) |
| DolRecomp | `b8b534591cba8ca7cd43943a655ee6e2591cf5de` |
| Previous release | 0.5.0, `0d1f821`, October 5 |

## Release notes (draft, for the release page)

Fixes and changes since 0.5.0:

- Dungeon maps show their grid and rooms again (#74).
- The history intro after the title screen has its music on Mac, iPhone and iPad (#97). Windows: see below.
- Controllers that were detected but did nothing now play as player 1, including ones recognized through
  `gamecontrollerdb.txt` and a second controller left over after the first is unplugged (#61).
- Conducting with the Wind Waker on a controller is no longer mirrored (#156).
- The left stick has no big dead zone or sudden jump anymore, and reaches full speed near the end of its travel (#138).
- New option under Controls: invert the left stick's up and down while aiming in first person or with an item (#154).
- Touch controls are released when Apple's menus open (iPhone and iPad).
- Quitting is cleaner on every platform (a fix from the Linux port).
- Building from source works with Visual Studio 2022 again (#153).
- The session log names the controller mapping in use, to help with controller reports.

Windows: the intro-music fix is [on / off, after step 4]. To try it when it's off, start BlueWake from PowerShell with
`$env:BLUEWAKE_DEFER_DVD_COMPLETION="1"`.

## Checks

| Check | Platform and device | Commit | Result |
| --- | --- | --- | --- |
| App-only IPA, PadMint audit, release check | Mac (M3 Max) | `2c8a659` | Pass: `BlueWake-v0.6.0-ios-unsigned.ipa` reports 0.6.0 build 5 and has no Frameworks folder (no game module); PadMint 0.4.10 `audit` and `check_public_assets.sh` pass (0 address-named functions). The source zip (960 files) and the recipe (unchanged since 0.5.0, `check-manifest` ok) pass too. |
| Full PadMint build from an owned disc | Mac (M3 Max), PadMint 0.4.10 (`v0.4.10`), scratch `PADMINT_HOME` | `2c8a659` | Pass: `padmint make bluewake ios --ref main` with the new app-only IPA, fresh clone at the candidate, RecompCore `35e037f`. About 2 hours with 16 jobs (training about 26 minutes, compile about 72). The personal IPA reports 0.6.0 build 5 and holds the iOS module; it stays private. |
| Intro after title music, captured audio | Mac (M3 Max), headless, builder-configured host | `c82f375` (the candidate differs only in docs and `version.json`) | Pass: the default is on; `1tale.afc` plays through 3600; last 10 s 639,010 nonzero samples. A Windfall save loads (play scene at 609). All 72 host tests pass. |
| Intro after title music, with the PadMint-built module | iOS Simulator (iPad Pro 12.9), container backed up first | `2c8a659` | Pass: log shows `deferred completion=on (default)`; `1tale.afc` starts at 1953; last 10 s of a 59.8 s capture have 639,118 nonzero samples. The card and settings were unchanged afterwards. |
| Load a save, dungeon map, quit | iOS Simulator or a device | | not yet: covered on the Mac host above; the Windows rows below repeat it |
| Windows build from the candidate | Chris's PC | | not yet: steps in [WINDOWS_BUILD_0.6.0.md](WINDOWS_BUILD_0.6.0.md) |
| Intro with the variable on, then off | Windows | | not yet |
| Dungeon map with a copied save | Windows | | not yet |
| Quit from the menu | Windows | | not yet |
| Controller rows (player 1, baton, left stick, aim option) | Windows, if a controller is at hand | | not yet |
| Windows intro default decided | | | not yet |
| Release check on all five assets | Mac | | not yet |
