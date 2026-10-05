# Open issues and reports, October 5, 2026

Every open GitHub issue on October 5, 2026, plus problems players reported in the BlueWake Discord on
October 4 and 5. Discord reports are recorded here to be fixed in the next version; they don't get replies
or their own issues. This is a snapshot: [GOAL_LOOP.md](../GOAL_LOOP.md) has the work and its progress.

Every Windows player is still on Wind Waker Recomp 0.4.0, so a Windows report doesn't show whether
`main` has the problem. Logs attached to issues were read with `scripts/triage_session_log.py` and by hand.

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

## Bugs

| Report | Where | What we know | Loop step |
| --- | --- | --- | --- |
| #58, Discord (StarXfusion, Xand3r, Dale): the Exact sound setting crashes, and the game then crashes on every launch | Windows | #58's log ends with `[dsp-lle] authentic DSPCore shadow route enabled` and a null read (`0xC0000005` at address 0) within a second. Players recover by deleting the `.ini` in `%APPDATA%\BlueWake` or setting its `lle_audio` line to 0. | 3 |
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
