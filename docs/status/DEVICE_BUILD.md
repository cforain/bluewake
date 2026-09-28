# Building BlueWake for an iPad or iPhone

This builds the signed BlueWake app for a physical device from a fresh checkout and your own disc
image of The Legend of Zelda: The Wind Waker (GZLE01, USA, revision 0). One script does it all:

```bash
scripts/ios/build_device.sh "/path/to/The Legend Of Zelda The Wind Waker.iso"
```

It is the Builder (`scripts/builder/build.sh`, [BUILDER.md](../BUILDER.md)) with the BlueWake profile,
and takes the same options; `--ipa FILE` also writes an unsigned IPA for sideloading
([BUILD_YOUR_OWN.md](../BUILD_YOUR_OWN.md)). The mods are built in (`--no-mods` skips them). It needs no
`build/`, `generated/` or `ref/` directory beforehand and no files from any other machine. Everything it makes stays under `build/device` (git ignores it), and nothing is uploaded.

## What you need

- A Mac with Apple silicon and Xcode (verified with Xcode 26.6, iOS SDK 26.5, macOS 26.6). Run
  `xcode-select -s /Applications/Xcode.app` once if the command-line tools point elsewhere.
- CMake 3.25 or newer and Ninja: `brew install cmake ninja` (verified with CMake 3.27.1, Ninja
  1.13.2). Python 3, git and curl come with macOS and Xcode; the mods' Python packages
  (PyYAML, Pillow) are installed into `build/python` when missing.
- Network access to GitHub on the first run, and about 5 GB of free disk space (the build takes about 3.6 GB).
- The disc image, GZLE01 USA revision 0. Other revisions and regions are refused.
- To install: an Apple ID in Xcode, the iPad or iPhone (A13 or newer, iOS/iPadOS 17 or newer)
  with Developer Mode on, and a USB cable or the same network.

## What the script does

| Step | What happens | Time (M2 MacBook Air) |
| --- | --- | --- |
| 1 dependencies | Fetches the pinned RecompCore fork (GXRuntime, the vendored Aurora renderer, the Dolphin DSP sources) into `ref/recompcore`, its DolRecomp submodule (the translator), and the pinned Dawn iOS package (checksum checked) into `build/deps` | under a minute |
| 2 extract | Builds the app's own disc importer (`apple/ios/src/disc_import.c`) for the Mac and extracts `main.dol` and the 415 RELs | seconds |
| 3 translate | Builds DolRecomp and translates the DOL and all 415 RELs to C | under a minute |
| 4 composite | `scripts/generate_composite.py` merges them into one tree (748 chunks, 415 REL modules) and the script checks its digest against the verified tree | under a minute |
| 5 compile | Compiles that tree for arm64 iOS (`-mcpu=apple-a13`, iOS 17.0) into `gGZLE01_recomp.dylib` | about 4 hours on an idle Air (11.4 hours on 2026-09-25 with other apps loading it); far less on an M3 Max |
| 6 app | Builds BlueWake.app (SDL is downloaded by CMake), embeds the composite in `Frameworks`, signs it | 6 minutes |

`--source-only` stops after step 4, so you can check the tools, the dependencies and your disc in a
couple of minutes before the long compile. The compile resumes where it stopped if interrupted: rerun
the same command. The log of every step is in `build/device/logs`.

The result is `build/device/app/BlueWake.app`. Without signing options it is signed ad hoc, which
proves the build but will not install on a device.

## Signing and installing on the iPad

1. **A signing certificate.** In Xcode, Settings > Accounts, add your Apple ID. Select the team and
   click Manage Certificates > + > Apple Development. Check it:
   ```bash
   security find-identity -v -p codesigning
   # 1) 0123ABCD... "Apple Development: Your Name (TEAMID1234)"
   ```
   A free Personal Team works; its apps expire after seven days (rerun step 5 below to reinstall).
2. **Developer Mode.** Connect the iPad to the Mac, unlock it and trust the computer. Open Xcode's
   Window > Devices and Simulators once so the iPad is prepared. On the iPad, Settings > Privacy &
   Security > Developer Mode, turn it on and restart.
3. **A provisioning profile for `dev.bluewake.BlueWake`.** The simplest way: in Xcode, File > New >
   Project > iOS App, set the Bundle Identifier to `dev.bluewake.BlueWake` and your Team, choose the
   connected iPad as the run destination and press Run once. Xcode registers the iPad and makes
   the profile ("iOS Team Provisioning Profile: dev.bluewake.BlueWake"). Find its file:
   ```bash
   for f in ~/Library/Developer/Xcode/UserData/Provisioning\ Profiles/*.mobileprovision \
            ~/Library/MobileDevice/Provisioning\ Profiles/*.mobileprovision; do
     [ -f "$f" ] && security cms -D -i "$f" 2>/dev/null | grep -q 'dev.bluewake.BlueWake' && echo "$f"
   done
   ```
   With a paid account you can instead register the App ID and the iPad in the developer portal
   and download an iOS App Development profile. Delete the placeholder app from the iPad afterwards.
4. **The device id.**
   ```bash
   xcrun devicectl list devices      # the Identifier column, or the device name
   ```
5. **Build, sign and install** (after a first full build, only the signing and install run again;
   steps 1-4 take a minute and the compile is reused):
   ```bash
   scripts/ios/build_device.sh "/path/to/The Legend Of Zelda The Wind Waker.iso" \
       --identity "Apple Development: Your Name (TEAMID1234)" \
       --profile "/path/to/profile.mobileprovision" \
       --install <device identifier>
   ```
   The script embeds the profile, signs the composite and the app with the profile's
   entitlements, verifies the signature and installs with `xcrun devicectl`. It refuses a profile
   made for another bundle id. With a free team, the first launch may say "Untrusted Developer":
   Settings > General > VPN & Device Management, trust your Apple ID, then launch again.
6. **The disc on the iPad.** The app contains no game data. Copy the same disc image to the iPad:
   in Finder, select the iPad, open the Files tab and drag the ISO onto BlueWake (or put it in
   iCloud Drive or On My iPad with the Files app). On first launch BlueWake shows what is missing,
   imports the disc through the document picker (a file named `GZLE01.iso` in BlueWake's folder is
   picked up too), checks that it is GZLE01 USA revision 0 and prepares `main.dol` and `rels/` on the
   device. Saves stay in the app's container.

What to check on the iPad is listed in [IPAD_STATE_2026-09-24.md](IPAD_STATE_2026-09-24.md).

## Optional profile-guided builds (faster)

The build tested in the iPad simulator on 2026-09-24 used three LLVM profiles recorded from
training runs of the game on the macOS host. They are optional: the script builds without them,
and nothing in the repository refers to them. They are not committed because they are recorded
from running the game (function names and counts of the translated code). Measured on the macOS
host, the composite profiles cut game-thread cycles by about 20 percent and the host profile by
6.5 percent ([CURRENT.md](CURRENT.md), 2026-09-23); on the iPad simulator the build without them took about 20 percent longer per retrace in the heaviest view (see Verified). The speeds in [IPAD_STATE_2026-09-24.md](IPAD_STATE_2026-09-24.md) were measured with all three.

| Profile | Path on the development Mac | Size | Covers |
| --- | --- | --- | --- |
| Hot chunks | `build/composite-pgo/prof/merged.profdata` | 22.6 MB | the 100 DOL chunks carrying 95 percent of translated-code time |
| Composite runtime | `build/composite-pgo-rt/prof/merged.profdata` | 26 KB | `cpu.c`, `dispatch_loop.c` and the other runtime files |
| Host | `build/host-pgo-gen/prof/merged.profdata` | 689 KB | the app's host code (device services, renderer glue, DSP) |

They still match this build: the 206 DOL chunks, the composite metadata and the runtime files are
byte-identical to the tree they were trained on (only REL chunks differ, and REL code is about 4
percent of the time). To use them, copy the three files to the other Mac (any path without spaces)
and pass them; repeated `--composite-pgo` files are merged:

```bash
scripts/ios/build_device.sh "/path/to/disc.iso" \
    --composite-pgo /path/to/composite-hot.profdata \
    --composite-pgo /path/to/composite-rt.profdata \
    --host-pgo /path/to/host.profdata \
    --out build/device-pgo            # a separate directory: the flags change every object
```

Recording new profiles is a macOS research workflow (`scripts/pgo_composite_hot.py`,
`scripts/pgo_host_train.sh`); it needs a macOS composite build and a training run of the game.

## Where the sources come from

| Component | Source | Pinned |
| --- | --- | --- |
| RecompCore (GXRuntime, Aurora, DSP) | https://github.com/chrissotraidis/RecompCore, branch `bluewake` | `2d6063614a9bc899f6b4d11c7e7b3cd66e4d96f3` |
| DolRecomp (translator) | https://github.com/chrissotraidis/DolRecomp, branch `bluewake` (RecompCore's `DolRecomp` submodule) | `5c91d6ed1ac7ac2f1aa6535b893eabb70f0f0d8f` |
| Aurora | vendored in RecompCore at `GXRuntime/graphics/aurora` (plain files) | with RecompCore |
| Dawn (WebGPU) for iOS | https://github.com/encounter/dawn/releases v20260618.032059, `dawn-ios-arm64.tar.gz` | sha256 `ada0bafc...a7ae2` |
| SDL 3.4.10, fmt, xxhash and the rest | fetched by Aurora's CMake at configure time | Aurora's pins |

The RecompCore fork is the upstream base `5c3611e` (ExpansionPak/RecompCore) plus the 76 BlueWake
commits that were only on the development Mac, including the former local head `3476998`, plus the
files that were never committed there (`GXRuntime/include/core/cpu.h`, `GXRuntime/src/core/cpu.c`,
`Source/Core/Core/DSP/Interpreter/DSPIntTables.cpp` and `.h`). The DolRecomp fork is the translator
exactly as it produced the shipped composite; a fresh build of it is byte-identical to the one used.

`patches/recompcore` and `patches/dolrecomp` are history. The RecompCore series starts at 0008
(0001-0007 were never exported), so it cannot apply to the base; the fork commit replaces it.

## How the composite is generated

These are the commands the script runs (step 3 and 4), recovered on 2026-09-25:

```bash
dolrecomp --gamecube --backend c --cpu gekko --partition-instructions 4096 main.dol OUT_DOL -j8
dolrecomp --gamecube --backend c --cpu gekko --rel-base 0xC0400000 rels/ OUT_RELS -j8
python3 scripts/generate_composite.py --dol-dir OUT_DOL/generated \
    --rels-dir OUT_RELS/generated/rels --rels-bin-dir rels/ --main-dol main.dol --output-dir COMPOSITE
```

The REL namespace failure recorded earlier came from a stale REL translation made with the old
low aperture (0x80400000); the RELs must be translated with `--rel-base 0xC0400000`, and
`--rels-dir` must name `generated/rels` (naming `generated` finds no RELs). The result passes the
generator's checks (748 chunks, 415 REL modules, 417 code ranges). Its five metadata files and all
206 DOL chunks are identical to the composite shipped to the simulator. The 542 REL chunk files
differ from that tree, which had been assembled by hand from two translator versions (its DOL chunks
regenerated after DolRecomp patch 0018, its REL chunks still from before it); the fresh tree has
every file from the same translator. The runtime checks below were run on the fresh tree.

The script pins the digest of the generated tree
(`python3 scripts/ios/composite_manifest.py DIR`, 753 files,
`9e4a847d50eddfec953e91272234e4af767d158fb1f55347487cf1a46509df7c`) and stops if a disc or
translator produces anything else; `--accept-new-composite` overrides that for development.

## Verified

On 2026-09-25, on an M2 MacBook Air (Xcode 26.6, CMake 3.27.1), from fresh clones of this
repository with no `ref/`, `build/` or `generated/`:

- **Sources.** Steps 1-4 fetched RecompCore 086f282 and DolRecomp 5c91d6e from GitHub and Dawn from
  its release (checksum matched), and the source check passed in 1 minute 40 seconds: 206 DOL
  chunks, 415 RELs, generator PASS (748 chunks, 415 REL modules, 417 code ranges), composite digest
  `9e4a847d...` equal to the pinned one. It was reproduced in a second fresh clone.
- **Extraction and translation.** The extractor's `main.dol` and 415 RELs are byte-identical to the
  files the development Mac used; the DolRecomp built from the fork is byte-identical to the one
  that made the shipped composite.
- **The app's host code** builds with the StaticRecomp ABI header from RecompCore (no ModernGekko):
  the macOS host and its 218 tests pass (218/218) and the simulator app builds.
- **The optional profiles** apply to the fresh tree: the composite runtime files compile for iOS
  against the merged composite profile with no out-of-date or unprofiled-function warnings.
- **Device code on the Mac.** The composite is plain C linked only against libSystem, so the device
  dylib retagged to macOS (`scripts/ios/retag_macho_platform.py`) runs in the macOS host. The device
  composite of 2026-09-24 retagged this way reproduces the certified route digest `83d2590d...` over
  1,050 records. The same check is used on the clean build below.

**The complete clean build.** One run of `scripts/ios/build_device.sh DISC.iso --jobs 7` in a fresh
clone of commit c9f064b (the build inputs of e68f3c9 and later are the same; only documentation
changed) finished with exit status 0: steps 1-4 in under a minute, the composite compile in 684
minutes (this Air shared its cores with other applications all day; the 2026-09-24 device composite
took about 4 hours on the idle machine), the app in 6 minutes. `codesign -v --strict --deep` passes;
the app and the composite are platform IOS, minos 17.0; the app is 426 MB; the build directory took
3.4 GB. The composite's sha256 was `5bcfffee...74e1` (not pinned: it depends on the Xcode version).
Nothing in it refers to local paths (the only `/Users/` strings are Dawn's CI source paths).

**The clean composite at run time,** with the device code itself (no profiles):

- `scripts/verify_abi_coverage.py` on it retagged to macOS: PASS (417 code ranges, 748 chunks,
  415 REL modules, 8,079 REL sections).
- The certified headless route on the macOS host: digest `83d2590d...` over 1,050 records, the
  same as the tested build, stopping at the same blocks and pcs (10,557,120 at 0x80307ef4 and
  11,174,010 at 0x8027fa30). 232.7 M instructions a retrace against 218.4 M for the profiled
  2026-09-24 device composite.
- `scripts/ios/sim_save_acceptance.sh` on the iPad simulator with this composite (retagged for the
  simulator, code byte-identical): PASS. Opening complete at retrace 13,861 and play at 13,921
  (certified 13,850 and 13,910), pause-menu save written, the guest's own reset, stereo audio
  captured, reload into control at retrace 831.
- Speed without the profiles, the simulator's heavy Outset view back to back: median retrace time
  55.7 ms against 45.6 ms for the profiled 2026-09-24 device composite, about 20 percent slower. The
  absolute rates that afternoon (12-14 retraces a second for both, and 13.3 for the macOS composite
  that measured 51-54 on the idle Mac) were set by the load on the Mac, not by the build.

**Not verified here:** installing and running on a physical iPad (this Mac has no signing identity)
and the `--identity`, `--profile` and `--install` path, which only runs with them.

