# The Builder

The Builder turns a player's own game disc into their own app, on their own Mac. Nothing it produces is
published: the game code is translated from the player's disc during the build and stays on their Mac
and device. This is how BlueWake is distributed. Players get the source and build their personal IPA
themselves (docs/BUILD_YOUR_OWN.md).

```sh
scripts/builder/build.sh "/path/to/The Legend Of Zelda The Wind Waker.iso" --ipa ~/BlueWake.ipa
```

`scripts/ios/build_device.sh` is the same command with the BlueWake profile preselected; it takes the same
options. `--help` lists them.

## Pipeline and profile

The Builder has two parts:

- **The pipeline**, `scripts/builder/build.sh`, is the same for every game. It parses options, checks the
  Mac's tools, runs the game's steps in order with a log per step, embeds the game module in the app,
  signs it (ad hoc, or with the player's identity and provisioning profile), writes the unsigned IPA,
  and installs with `devicectl` when asked. It refuses to write an IPA anywhere inside the repository
  that git could commit.
- **A profile**, `scripts/builder/profiles/NAME.sh`, holds everything specific to one game: which disc it
  accepts, the pinned translator and runtime, how the translated code is generated and checked, the mods,
  and the app target. `--game NAME` selects it; the default is `bluewake`.

The steps are:

| Step | Who | What |
| --- | --- | --- |
| 1 tools | pipeline + `profile_check_tools` | Xcode, iOS SDK, CMake 3.25+, Ninja, plus the game's extras |
| 2 dependencies | `profile_dependencies` | Fetch pinned sources (commit hashes, checksums) |
| 3 extract | `profile_extract` | Read the disc; refuse the wrong game or revision |
| 4 translate | `profile_translate` | Translate the game's code to C |
| 5 generate | `profile_generate` | Assemble the source to compile; compare it with the verified digest |
| 6 mods | `profile_mods` | Optional code mods (skipped with `--no-mods`) |
| 7 compile | `profile_compile` | Compile the game module (the long step); set `module` |
| 8 app | `profile_build_app`, then pipeline | Build the app, set `app`; the pipeline embeds and signs |
| 9 package | pipeline | `--ipa` and `--install` |

`--source-only` stops after step 5, so a player can check their disc and tools in minutes before the long
compile. Each step reuses finished work, so an interrupted build resumes.

## Writing a profile for another port

A profile is a shell file sourced by the pipeline. It sets:

| Variable | Example (BlueWake) |
| --- | --- |
| `PROFILE_NAME`, `PROFILE_TITLE` | `bluewake`, the game title and disc revision |
| `PROFILE_APP_NAME`, `PROFILE_BUNDLE_ID` | `BlueWake`, `dev.bluewake.BlueWake` |
| `PROFILE_MODULE` | `gGZLE01_recomp.dylib`: the file name the app loads from `Frameworks/` |
| `PROFILE_DEFAULT_OUT` | `build/device` (must be git-ignored) |
| `PROFILE_HAS_MODS` | `1` or `0` |

and defines the eight `profile_*` hooks in the table above. Hooks may use the pipeline's helpers
(`run LOGNAME cmd...`, `die`, `pgo_flags FILE`) and variables (`root`, `out`, `logs`, `jobs`, `iso`,
`opt_level`, `device_cpu`, `composite_pgo`, `host_pgo`, `accept_new`, `mods`). `profile_compile` must
set `module` and `profile_build_app` must set `app`.

A port's profile has to answer three questions, which are also its safety checks:

1. **Which disc?** Refuse anything but the exact game and revision the port was verified with (BlueWake
   checks the disc ID and the executable's hash).
2. **Which translator?** Pin every source by commit or checksum, so every player's build is the same.
3. **Is the result the verified one?** Compare the generated source with a recorded digest before
   compiling, so a wrong disc or translator fails in minutes instead of producing a broken app hours later.

A port whose app builds differently only changes its `profile_build_app`.

## Build time

A fresh-clone run on 2026-09-28 (M3 Max, 16 jobs, default settings with mods) took 83 minutes, 80 of them
compiling the game module at the default `-O2`; it needed about 10 GB in `build/` and wrote a 96 MB IPA.
Smaller Macs take longer.

A lighter `-O1` build was measured the same day as a faster option: it compiled in 47 minutes, but on an
iPad Pro (M2) at the Outset Island pier it averaged 26.1 FPS with the CPU at 99 percent (121 one-second
samples, none at 29 FPS or above), where the owner's build holds 30. It was dropped: it saves about half an
hour and loses the game's frame rate.

## Optimization profiles

The game module and the app are compiled with LLVM profile-guided optimization (PGO) when profiles are
available. The BlueWake profile bundles two in `scripts/builder/profiles/bluewake/`, both trained on the
macOS host: `composite-rt.profdata` (the runtime's dispatch, memory and CPU helpers) and `host.profdata` (the
app's host code: renderer glue, input, DSP). They name only BlueWake's own functions and contain counts,
no code; both pass `release_gate.py`. `--no-pgo` skips them.

A third profile, for the translated game code itself, is kept private: it names the game's functions by
address and fails the release gate. Measured on 2026-09-28 on an iPad Pro (M2) at the Outset pier, same
scripted route:

| Build | FPS | CPU |
| --- | --- | --- |
| No profiles | 26.0 | 99% |
| The two bundled profiles | 27.5 | 99% |
| All three (the developer's build) | 29.9 | 83% |

## What is public and what is not

The repository and its source archives contain no game code, disc data, keys or saves;
`scripts/release/check_public_assets.sh` checks every public asset and fails closed. The IPA the Builder
writes contains the player's translated game module (`gGZLE01_recomp.dylib`): it is a personal build
and is never uploaded, attached or shared (AGENTS.md).
