# BlueWake on Linux

Build The Legend of Zelda: The Wind Waker (GameCube USA, GZLE01 revision 0)
from your own disc and play it on Linux. This is the same game as the Windows
build: a native host, the translated game module, and the DSP, packaged as a
folder you run with `./bluewake`.

## What you need

- An x86-64 Linux PC.
- Your own GZLE01 revision 0 disc image, as an uncompressed `.iso` or `.gcm`.
  (A Dolphin-compressed image like `.rvz`/`.wia` is not converted here; convert
  it in Dolphin: right-click the game, Convert File, format ISO.)
- clang (with lld and llvm-profdata), CMake 3.25+, Ninja, Python 3.10+, git:
  `sudo apt install clang lld llvm cmake ninja-build git` (or your distro's
  equivalent). Vulkan drivers for your GPU. The host and the game module both
  build with clang, matching the Windows build's optimization pipeline.

## Build

    python scripts/linux/build.py path/to/GZLE01.iso --out build/linux

The first build clones the pinned RecompCore and DolRecomp sources into
`ref/recompcore`, translates your disc, and compiles the game module (the long
step). Rerun the same command to continue or reuse an existing build. Your
disc, the extracted files and the translated module stay in `build/linux`,
which git ignores.

Useful options:

    --source-only  stop after translating: checks tools, disc and translation
                   in minutes, before the long compile
    --no-mods      skip the widescreen and Better Wind Waker variants
    --opt-level 1  faster to compile, a little slower in game
    --jobs N       parallel compile jobs (default: all cores, limited by memory)

## Play

    build/linux/BlueWake/bluewake

Run the app with `--setup` to open **BlueWake Setup**. Choose the USA revision-0
disc image and, optionally, a Dolphin-format HD texture-pack folder, then press
**Start BlueWake**. Display, gameplay, controls and other preferences remain in
the shared F1/Esc settings menu used on every desktop platform. The setup file
and folder buttons use SDL's native dialog through an XDG
portal or Zenity. Dragging an ISO/GCM onto the setup window and entering paths
directly also work.

Without `--setup`, BlueWake keeps its ordinary launch behavior: it asks for a
missing disc with the native file picker and otherwise starts the game.

`--help` lists the options (widescreen, Smooth Motion, Better Wind Waker, fullscreen,
disc and module paths). Keyboard: arrows D-pad, J/K/U/I face buttons, W/A/S/D stick,
H/F/T/G C-stick, E/R L/R, Q Z, Return START; game controllers work. Mouse: click the
game and move to turn the camera, Esc releases it.

Your saves, settings and session logs live in `~/.local/share/BlueWake`, outside
the build, so rebuilding never touches them. The settings menu (Esc or F1) saves to
`~/.config/BlueWake/settings.ini`.

## The app folder

`build/linux/BlueWake/` is a personal build: `gGZLE01_recomp.so` is code
translated from your disc and `game/` holds your disc image. Never share or
upload it.

## The AppImage

`scripts/linux/make_appimage.sh` packages the built app folder as an AppImage
(the default `build/linux/BlueWake-x86_64.AppImage` plus its `.zsync` metadata
for delta-capable update tools). It bundles the host, the translated game
module, the DSP roms and every shared library the host links except the
glibc/libstdc++ baseline, so the image runs on any x86-64 desktop. The player's
disc is not bundled: on first run the launcher asks for it and prepares it into
the data dir (a disc and files extracted from it are never distributed).

### Build the AppImage

The build machine needs `appimagetool`, `desktop-file-validate` (usually from
`desktop-file-utils`) and `zsyncmake` (usually from `zsync` or `zsync-curl`) on
`PATH`. ImageMagick is optional and is used to convert the application icon.
After creating the Linux build from your disc as described above, run:

    scripts/linux/make_appimage.sh

The outputs are:

    build/linux/BlueWake-x86_64.AppImage
    build/linux/BlueWake-x86_64.AppImage.zsync

To use another build directory or output name:

    scripts/linux/make_appimage.sh BUILD_DIR OUT.AppImage

These are generated artifacts and are ignored by Git. Do not commit them. The
AppImage contains the translated game module, so only a maintainer may publish
it under the Linux release exception, after it passes the release asset check:

    scripts/release/check_public_assets.sh build/linux/BlueWake-x86_64.AppImage

### Run the downloaded AppImage

1. Make the download executable (you only need to do this once):

       chmod +x BlueWake-x86_64.AppImage

2. Open the graphical setup to choose your disc and optional texture pack:

       ./BlueWake-x86_64.AppImage --setup

   Leave **Add or update BlueWake in the application menu** enabled to install
   a launcher with a **Configure BlueWake** action. The launcher points to this
   AppImage, so keep it at the same path after setup.

3. On later launches, start BlueWake normally by double-clicking the AppImage
   or running:

       ./BlueWake-x86_64.AppImage

The setup window is opt-in: launching without `--setup` keeps BlueWake's normal
behavior. You can also skip setup and supply a disc directly:

    ./BlueWake-x86_64.AppImage --disc "/path/to/Wind Waker.iso"

If your system cannot mount AppImages with FUSE, extract and run it temporarily
instead:

    APPIMAGE_EXTRACT_AND_RUN=1 ./BlueWake-x86_64.AppImage --setup

The setup UI itself has no extra GUI dependency: SDL and Dear ImGui are bundled
in the AppImage. Its **Choose** buttons need one of these system file-dialog
providers:

- an XDG desktop portal plus a backend for your desktop (for example,
  `xdg-desktop-portal` and `xdg-desktop-portal-gtk`); or
- Zenity.

Most desktop Linux installations already provide an XDG portal. If the buttons
do not open, install the appropriate backend or type/drag the paths into the
setup window. FUSE is optional; use `APPIMAGE_EXTRACT_AND_RUN=1` as shown above
when it is unavailable.

## Releases

When a ready-made Linux build is published, it follows the same exception as
Windows: it is made on a maintainer's or contributor's personal machine from
their disc and attached to the release by hand. The disc, files extracted from
it, and console keys never enter GitHub or CI (a secret could not hold a 1.4 GB
disc, and must not). CI builds and tests everything that does not need the disc
(`.github/workflows/linux-host.yml`), and every published artifact passes
`scripts/release/check_public_assets.sh`. Only Chris publishes or changes a
release.

## Why clang

The host (Aurora, SDL3, the DSP) and the game module both build with clang, matching
the Windows build. Aurora uses C++20 designated-initializer field orders that gcc
rejects, so the host needs clang. The game module's translated chunks are each one
enormous generated function, and clang's optimizer is pathologically slow on them
(many minutes per chunk at `-O2`); the build defeats that with `-fno-slp-vectorize`
and `-mllvm -large-interval-freq-threshold=10` (the two superlinear passes), the same
flags the Windows builder uses, and then applies the certified native accelerators,
fixed CPU/RAM, direct calls, gather pipe and a locally trained PGO profile — the
pipeline that reaches 30 FPS (see docs/PERFORMANCE_OPTIMIZATIONS.md).
