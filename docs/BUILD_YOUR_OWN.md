# Build your own BlueWake

BlueWake is distributed as source. You build it on your Mac from your own copy of *The Wind Waker*, and the
result is an app for your own iPhone or iPad. The game's code is translated from your disc during the
build, so **the app you build is yours alone: never share or upload it.**

## What you need

- A Mac with Apple silicon that runs the current Xcode, and at least 12 GB of free disk space
  for the baseline build; allow at least 25 GB when trying local optimization training
- Xcode from the App Store. Open it once, and under **Settings › Components** install the iOS platform.
- [Homebrew](https://brew.sh), then in Terminal:
  ```sh
  brew install cmake ninja
  ```
- Your disc image of *The Legend of Zelda: The Wind Waker*, GameCube USA (`GZLE01`, revision 0), as an
  `.iso`. The build checks it and refuses other versions.
- An iPhone or iPad with an A13 chip or newer, on iOS/iPadOS 17 or later

## 1. Build the baseline or trained candidate

```sh
git clone https://github.com/chrissotraidis/bluewake.git
cd bluewake
scripts/builder/build.sh "/path/to/The Legend Of Zelda The Wind Waker.iso" --source-only
```

`--source-only` checks your tools and disc and generates the base source. It stops before mods,
training, compilation and packaging; it produces no app. If it passes, the **baseline** build is:

```sh
scripts/builder/build.sh "/path/to/The Legend Of Zelda The Wind Waker.iso" --ipa build/BlueWake.ipa
```

The baseline measured about 27.5 FPS at the tested Outset scene on an iPad Pro M2. It does not
include locally trained game counters. For that candidate, use the separate training command below.

The baseline build measured 83 minutes on an M3 Max. Local optimization training adds another build
and a training run; its complete time and performance are still being verified. Smaller Macs take
longer, and the Mac stays busy. Rerunning the same command reuses compatible compiled objects and
completed matching profiles. Interrupted training playback starts again from an isolated card; it does
not resume mid-sequence. Keep the same output directory and build options to reuse completed work.

Generated game code and build outputs stay in `build/`; downloaded runtime and translator sources
live in `ref/`. Nothing is uploaded.
Keep the IPA there or anywhere else that is not synced: iCloud Drive (including a synced Desktop or
Documents folder), Dropbox and similar would upload it.

## Experimental local optimization

The developer build reaches about 30 FPS in the measured iPad scenes; the baseline player build
measured about 27.5 FPS. To help validate a locally generated replacement for the private game
optimization profile, use:

```sh
scripts/builder/build.sh "/path/to/disc.iso" --train-pgo \
    --out build/device-trained --ipa build/BlueWake-trained.ipa
```

This builds an instrumented Mac version, runs a training sequence from your disc, records execution
counts, then uses them to compile the device version. You do not need to play through it manually or
supply a save. The HLE playback portion took
18 minutes 24 seconds on the development M3 Max, in addition to the separate training compile and
final iOS compile; this is not a complete-build time estimate. The terminal reports the stage and elapsed time; logs are under `build/device-trained/logs` and
`build/device-trained/pgo-local/logs`. No full-speed result is promised yet: completing training is
not the same as passing hardware performance tests.

Training starts with a new private card by default; that is the route validated so far. You can add
`--training-save "/path/to/GZLE01.card"`
to train with a copy of your own BlueWake memory card; your original is not modified. This requires
a BlueWake `.card` container, not a Dolphin `.gci` or `.raw` file directly. Use quoted absolute paths.
The optional saved-card route has not been validated in this pass. Generated profiles and training saves remain private under the build directory. Matching completed profiles
are reused on later runs; changes to inputs invalidate them.

## 2. Install

The IPA is unsigned; it needs signing before installation. Common signing tools are listed below;
BlueWake-specific end-to-end installation has not been verified with every tool.

| Tool | Notes |
| --- | --- |
| [Sideloadly](https://sideloadly.io/) | Mac app: connect the device, drag the IPA in, sign in with your Apple ID |
| [AltStore](https://altstore.io/) | AltServer on the Mac installs AltStore on the device; add the IPA from AltStore's **My Apps** |
| [SideStore](https://sidestore.io/) | Like AltStore, but refreshes on the device without the Mac |
| Xcode | Sign and install from the Builder directly: `--identity`, `--profile` and `--install` ([DEVICE_BUILD.md](status/DEVICE_BUILD.md)) |

With a free Apple ID, apps expire after seven days; refresh them with the same tool (your saves stay).
The device needs **Developer Mode** on (Settings › Privacy & Security), and the first launch may ask you to
trust your Apple ID under Settings › General › VPN & Device Management.

## 3. Copy the disc to the device

The app reads the game's graphics, sound and world data from your disc. Copy the same `.iso` to the
device: in Finder, select the device, open **Files** and drag it onto **BlueWake**, or save it in
local **On My iPad** or **On My iPhone** storage in Files. Open BlueWake and pick it; the app checks
it and prepares the game. Keep the imported disc on the device: the game reads it while you play.
**⋯ › Game Data & Saves › Remove Disc Image…** removes the imported disc and extracted game files,
keeps your saves and settings, and requires importing the disc again before playing.

## Updating

```sh
git pull
scripts/builder/build.sh "/path/to/disc.iso" --ipa build/BlueWake.ipa
```

Compatible completed work is reused. Sign with the same Apple ID/team and app identifier, then install
the new IPA **over** the existing app. If your installer requires removing BlueWake, stop and resolve
the signing mismatch first. Never delete BlueWake to update it: deleting it deletes its saves.
Back up first with **⋯ › Game Data & Saves › Back Up Saves…**.

If you used local training, rerun your original command with `--train-pgo` and
the same `--out` directory (and `--training-save`, if selected). Omitting those
options builds the baseline version instead of updating the trained version.

## Bringing your Dolphin saves

Export the save from Dolphin (**Tools › Memory Card Manager**, or the `.gci` file in its GC folder), copy
it to the device, then open **⋯ › Game Data & Saves › Import Dolphin Save…**. Choose the quest log and the
BlueWake slot for it; your current saves are backed up first. USA saves only.

## Mods

The build includes the Widescreen and Better Wind Waker code mods (`--no-mods` leaves them out). Better
Wind Waker also needs a patched disc, which the build writes to `build/device/mods/betterww.iso`: copy it
to the device and use **⋯ › Mods › Install Better Wind Waker…**. See [MODS.md](MODS.md).
With a custom `--out`, the patched disc is in that directory's `mods/betterww.iso`.

## If something fails

Each step writes a log under `build/device/logs`, and the error names it. Rerunning the same command
reuses compatible completed work. For help, ask on [Discord](https://discord.gg/xwHfUD2bxW) or
[open an issue](https://github.com/chrissotraidis/bluewake/issues), with the failing stage and relevant error excerpt.
Review logs for personal paths, signing details and device identifiers before posting. Never attach the IPA, disc, patched disc, game files, saves,
optimization profiles or signing/provisioning files, and do not upload the whole build directory.
