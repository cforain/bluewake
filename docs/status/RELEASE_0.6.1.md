# BlueWake 0.6.1 release record

The working record for 0.6.1. The steps are in [GOAL_LOOP.md](../GOAL_LOOP.md). Fill in each check with the device,
the commit and what was seen. A row stays "not yet" until someone runs it.

## Candidate

| | |
| --- | --- |
| Version | 0.6.1, build 6 (`version.json`, set at the freeze) |
| Candidate commit | not yet |
| RecompCore | `de9d15d2a5104b891236b6c85533197d3d431588` (patches 0160 and 0161), once #197 merges |
| Previous release | 0.6.0, October 8 |

## Release notes (draft, for the release page)

BlueWake 0.6.1 is a small update with fixes for controllers and Windows, and a native Linux build you can make
from source. Every version needs your own USA (GZLE01) disc image. Nothing from the game is included.

- A controller that's already plugged in when BlueWake starts now gets the smooth stick and plays as player 1.
  Before, the 0.6.0 stick fix only reached controllers connected after launch (#138). Thanks to pdale-boop.
- Windows: the window opens where you left it, or centred the first time, instead of appearing and then jumping.
  Thanks to saulob (#89).
- Windows portable mode keeps controller remaps, keyboard bindings and window layout in the `user` folder, so
  nothing is written to `%APPDATA%\BlueWake` anymore (#64).
- Linux: BlueWake builds and runs natively from your own disc, with saves, controllers, settings and HD packs
  (#107). Thanks to jkoehler11 (KongMing), and to fehnomenal and the Steam Deck testers. The steps are in
  `docs/LINUX.md`. Make sure Vulkan is installed: without it, BlueWake falls back to a much slower renderer.

Speed is the next big focus. The plan, and how it's being measured, is in `docs/PERFORMANCE.md`.

## Checks

| Check | Platform and device | Commit | Result |
| --- | --- | --- | --- |
| Windows build from the commit | | | not yet |
| A controller connected at launch: smooth stick, player 1, the `[pad]` lines in the log | | | not yet |
| Portable mode: remaps kept in `user`, nothing new in `%APPDATA%\BlueWake` | | | not yet |
| The window opens in place; a removed monitor gives a centred window | | | not yet |
| App-only IPA, PadMint audit, release check | | | not yet |
| Source zip and recipe | | | not yet |
| `check_public_assets.sh` on every asset | | | not yet |

## The lean-blocks measurement (not released)

| State | Mode | 0.6.1 build | `--lean-blocks` build | Change |
| --- | --- | --- | --- | --- |
| Outset | headless | | | |
| Outset | rendered | | | |
| Bird scene | headless | | | |
| Tower room 0 | headless | | | |

30-minute play on the lean build: not yet.
