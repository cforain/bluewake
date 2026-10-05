# Open issues and reports, October 5, 2026

Every open GitHub issue on October 5, 2026, plus problems players reported in the BlueWake Discord on
October 4 and 5. Discord reports are recorded here to be fixed in the next version; they don't get replies
or their own issues. This is a snapshot: [GOAL_LOOP.md](../GOAL_LOOP.md) has the work and its progress.

Every Windows player is still on Wind Waker Recomp 0.4.0, so a Windows report doesn't show whether
`main` has the problem. Logs attached to issues were read with `scripts/triage_session_log.py` and by hand.

## What the October 5 loop found

| Report | Result |
| --- | --- |
| #58 Exact sound crash | Already fixed in `main`; recovery message made plain in [#111](https://github.com/chrissotraidis/bluewake/pull/111). Moved to "fixed in `main`" above. |
| Camera inverting by itself | Two causes. In 0.4.0, the camera switched between the fast stick camera and the game's own camera (swimming, the boat, targeting), which turns the other way; #44 in `main` fixes that. On the Mac, the right stick's invert setting didn't reach the game's own camera; fixed in [#112](https://github.com/chrissotraidis/bluewake/pull/112). Better Wind Waker's "Invert camera left and right" now says what it affects ([#114](https://github.com/chrissotraidis/bluewake/pull/114)). |
| Controls settings reverting | `main` stopped launch overrides from overwriting saved Windows settings on October 1 and 2 (`8b4611d`, `e3536b1`), after 0.4.0. A crash recovery also resets settings (with a backup), and now says so. |
| Mouse and keyboard rebinding | Done on Mac and Windows ([#113](https://github.com/chrissotraidis/bluewake/pull/113)). Checked on the Mac: right-click set to B logged B; A moved to L logged A on L and nothing on J. |
| Quit from the menu, Brisk Sail and Unrestricted boat | Windows has "Quit the game"; both menus explain the two options ([#114](https://github.com/chrissotraidis/bluewake/pull/114)). |
| #74 dungeon map, sea charts | On the Mac, the Forsaken Fortress minimap, the sea chart and its Charts screen draw correctly (community saves from cbartondock/Windwaker, on scratch cards). No save inside a dungeon was at hand, so the large dungeon map is still unchecked; Chris was asked for one, and WINDOWS_TASKS.md says what to capture. |
| #65, #97 cutscene sound | On the Mac, the opening cutscene logs `cues=4 sounds=4 missing=0 silent=0.4s` with default settings, mouse camera off, Better Wind Waker on and 16:9 (no HD pack installed to try). None of them drops its sound on the Mac, so the cause is on Windows or in a later scene (the bird dropping Tetra); a Windows `[demo] end` line decides it. |
| Forsaken Fortress map and compass | No BlueWake patch touches dungeon items (only Tingle Chest markers and the new-game sea chart reveal), and the Mac shows the fortress minimap on the first visit with no patch involved. Most likely the original game; left as is. |
| #77 and Discord: `BlueWake.exe` does nothing on older CPUs | A message box now names the AVX2 requirement instead of a silent exit ([#117](https://github.com/chrissotraidis/bluewake/pull/117)); checked by compiling for Windows on the Mac, still to run under Intel SDE on Windows (task 2). |
| #61 8BitDo GameCube mod kit | Its Switch mode works with A and B swapped (Swap A and B is in `main`). Its generic mode needs an SDL mapping: BlueWake now loads `gamecontrollerdb.txt` from the folder with the saves ([#116](https://github.com/chrissotraidis/bluewake/pull/116)); the reporter was told how to try it with the next Windows build. |

## Fixed in `main`, waiting for a Windows build

These close once a Windows build from `main` is out and the reporter confirms.

| Issue | What | Note |
| --- | --- | --- |
| #13 | Pictobox photo freezes the picture | Fixed on the Mac. |
| #55 | Switch Pro controller A and B reversed | Swap A and B, Swap X and Y. |
| #64 | Portable mode | `portable.txt` beside `BlueWake.exe` (#103). |
| #66 | Controller remapping | 0.4.0 has none, which is why Danither3al can't find it. |
| #71 | Jump and sprint always on | Off by default in `main`. |
| #73 | Camera turns the other way in water | #44. DonatelloEsq also sees it after talking to someone (#65). |
| #79 | 120 Hz Smooth Motion keeps switching | The log shows the game at 13.7 to 25.9 game frames a second on an Intel Arc handheld, so Smooth Motion stepped down as designed. The reporter says newer builds don't do it. |
| #58 | "Exact" sound crashes, then every launch crashes | The crash (a call to address 0) was fixed on October 1 (`ef29510`, RecompCore patch 0114), after the 0.4.0 download. A crash before the game runs is now also recovered on the next launch, with a plain message (#111). |

## Bugs

| Report | Where | What we know | Loop step |
| --- | --- | --- | --- |
| #65, #97, Discord (Xand3r, Dale, shargul, Aleximo, GinOkami428): music, Link's voice and effects missing in cutscenes; the intro story silent; Tower of the Gods rises silently | Windows 0.4.0 | The intro has sound for some players and not others. DonatelloEsq got the bird dropping Tetra back by turning off the HD texture pack, the Better Wind Waker options and mouse camera; Xand3r says 4:3 helps. On the Mac the opening cutscene logs `cues=4 sounds=4 missing=0`. | 8 |
| #74, Discord (Xand3r, Chris): dungeon map shows the room icons but not the floor drawing | Windows 0.3.0 and 0.4.0 | Seen in Forbidden Woods and Dragon Roost Cavern on every floor. Not yet tried on the Mac. | 7 |
| Discord (Dale): every sea chart shows the same island, changing as the story goes on | Windows | Dale had "Reveal the full sea chart" off, as far as he knows. | 7 |
| Discord (Xand3r, ∀˥∩⅁I˥∀Ɔ), #65: camera left and right inverts by itself; Controls settings revert | Windows 0.4.0 | 0.4.0 has two left-and-right invert settings, one under Controls and Better Wind Waker's under Mods, and they interact (`bluewake_game_options_invert_camera_x`). | 4 |
| Discord (shargul): Forsaken Fortress map and compass in the inventory from the start | Windows | Possibly a Better Wind Waker option. | 9 |
| #77, Discord (Rai): `BlueWake.exe` does nothing | Windows | DheikoGW's CPU has no AVX2; a clear message is Windows task 2. ImNotRyan01 hasn't said which CPU. | WINDOWS_TASKS |
| #76: soft lock in the Forsaken Fortress after a Moblin falls | Windows | Needs a Windows check; may be the original game. | WINDOWS_TASKS |
| #80: HD pack shading and orange hair on an AMD GPU | Windows | Asked whether the PNG pack does it too. | needs info |
| #61: 8BitDo GameCube mod kit controller not seen | Windows | Needs a Windows check. | WINDOWS_TASKS |
| #69: pirate ship flag has no texture | Windows 0.3.0 | Asked for a check on 0.4.0. | needs info |

## Slow scenes

Not in this loop. Recorded so the evidence isn't lost.

| Report | What we know |
| --- | --- |
| #86 (i7-6950X, RTX 3080), #59, #72 | #86's log: the game's GX thread is 92 to 95% busy and the game runs at 85% speed at sea; the GPU waits about 1 ms. The limit is on the CPU side of the renderer. #59 and #72 were asked to retest on 0.4.0. |
| Discord (Greatwhitedragon, Pharoah): 30 FPS on Steam Deck, 20 under Proton on a faster PC | Pharoah got steady speed by turning on the Steam Deck's CPU boost. Same CPU-side limit as #86. |

## Requests

| Request | Who | Loop step |
| --- | --- | --- |
| Bind the right mouse button (for example to B), attack with a click instead of K, change keyboard keys | Discord (ᏦOI TAIYO, umut) | 5 |
| Quit from the menu or with a controller | Discord (sliv) | 6 (the Mac menu has "Quit the game"; Windows doesn't) |
| Explain Brisk Sail and Unrestricted Boat | Discord (kaiiboraka) | 6 |
| Button remapping on Windows | Discord (Neo Drayk), #66 | Waiting for Windows |
| Ultrawide | #70, Discord (Nael) | Later |
| Hotkey to switch the Wind Waker HD and GameCube renderers | #108 | Later; the screenshot is from a newer Wind Waker Recomp build |
| Wind Waker HD effects and HD textures in the download | Discord (Aleximo, Pharoah, yunghiphopmaster) | Not in a BlueWake release yet |
| Rumble on by default | Discord (∀˥∩⅁I˥∀Ɔ) | Question |

## Not planned or waiting on others

| Issue | State |
| --- | --- |
| #56 Linux | jkoehler11's port is PR #107. |
| #75 Android | LiquidAzir's port is PR #93. |
| #60 European disc, #57 Wii U interface, #62 Switch, #48 Intel Mac | Not planned now. |
| #104 PadMint feedback | Open thread for players. |
