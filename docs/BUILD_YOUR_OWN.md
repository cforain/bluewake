# Build your own BlueWake

BlueWake is not downloadable. You build it on your Mac from your own copy of *The Wind Waker*, and the
result is an app for your own iPhone or iPad. The game's code is translated from your disc during the
build, so **the app you build is yours alone: never share or upload it.**

## What you need

- A Mac with Apple silicon that runs the current Xcode, and about 12 GB of free disk space
- Xcode from the App Store. Open it once, and under **Settings › Components** install the iOS platform.
- [Homebrew](https://brew.sh), then in Terminal:
  ```sh
  brew install cmake ninja
  ```
- Your disc image of *The Legend of Zelda: The Wind Waker*, GameCube USA (`GZLE01`, revision 0), as an
  `.iso`. The build checks it and refuses other versions.
- An iPhone or iPad with an A13 chip or newer, on iOS/iPadOS 17 or later

## 1. Build

```sh
git clone https://github.com/chrissotraidis/bluewake.git
cd bluewake
scripts/builder/build.sh "/path/to/The Legend Of Zelda The Wind Waker.iso" --source-only
```

`--source-only` checks your tools and disc and translates the game in a few minutes. If it passes, build
the app and an IPA:

```sh
scripts/builder/build.sh "/path/to/The Legend Of Zelda The Wind Waker.iso" --ipa build/BlueWake.ipa
```

The first build compiles the whole game for iOS: it takes about 1.5 hours on an M3 Max (longer on
smaller Macs), and the Mac stays busy. It resumes where it stopped if interrupted, and later builds only redo what
changed.

Everything the build makes stays in `build/` inside the checkout. Nothing is uploaded.
Keep the IPA there or anywhere else that is not synced: iCloud Drive (including a synced Desktop or
Documents folder), Dropbox and similar would upload it.

## 2. Install

The IPA is unsigned; your sideloading tool signs it with your Apple ID. Any of these works:

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
device: in Finder, select the device, open **Files** and drag it onto **BlueWake**, or save it anywhere in
the Files app. Open BlueWake and pick it; the app checks it and prepares the game. After that you can
remove the `.iso` with **⋯ › Game Data & Saves › Remove Disc Image…** if you need the space.

## Updating

```sh
git pull
scripts/builder/build.sh "/path/to/disc.iso" --ipa build/BlueWake.ipa
```

Only what changed is rebuilt. Install the new IPA **over** the existing app with the same tool you used
before; your saves and settings stay. Never delete BlueWake to update it: deleting it deletes its saves.
Back up first with **⋯ › Game Data & Saves › Back Up Saves…**.

## Bringing your Dolphin saves

Export the save from Dolphin (**Tools › Memory Card Manager**, or the `.gci` file in its GC folder), copy
it to the device, then open **⋯ › Game Data & Saves › Import Dolphin Save…**. Choose the quest log and the
BlueWake slot for it; your current saves are backed up first. USA saves only.

## Mods

The build includes the Widescreen and Better Wind Waker code mods (`--no-mods` leaves them out). Better
Wind Waker also needs a patched disc, which the build writes to `build/device/mods/betterww.iso`: copy it
to the device and use **⋯ › Mods › Install Better Wind Waker…**. See [MODS.md](MODS.md).

## If something fails

Each step writes a log under `build/device/logs`, and the error names it. Rerunning the same command
resumes where it stopped. For help, ask on [Discord](https://discord.gg/xwHfUD2bxW) or
[open an issue](https://github.com/chrissotraidis/bluewake/issues), with the failing log, but never
attach the IPA, the disc or game files.
