#!/usr/bin/env bash
# Package a BlueWake Linux app folder as an AppImage with zsync delta updates.
#
#   scripts/linux/make_appimage.sh APP_DIR OUT.AppImage [--zsync] [--no-update]
#
# APP_DIR is the builder's OUT/BlueWake folder (a personal build: it holds the
# translated module and the disc, never share it). The AppImage embeds the app
# unchanged, so it needs no appimagetool at runtime and self-updates by zsync
# against a GitHub release asset of the same name (AppImageUpdate-compatible).
#
# A published release's AppImage (game code included, made from the owner's
# disc on a personal machine and attached by hand) must pass
# scripts/release/check_public_assets.sh first.
set -euo pipefail
app_dir=${1:?usage: make_appimage.sh APP_DIR OUT.AppImage [--zsync]}
out=${2:?usage: make_appimage.sh APP_DIR OUT.AppImage [--zsync]}
zsync=0
for a in "${@:3}"; do
  case "$a" in
    --zsync) zsync=1 ;;
    *) echo "unknown option $a" >&2; exit 2 ;;
  esac
done
app_dir=$(cd "$app_dir" && pwd)
root=$(cd "$(dirname "$0")/../.." && pwd)

command -v appimagetool >/dev/null || {
  echo "appimagetool is required: https://github.com/AppImage/appimagetool/releases" >&2
  echo "download the AppImage, chmod +x, and put it on your PATH" >&2
  exit 1
}

stage=$(mktemp -d "$root/build/appimage-stage.XXXXXX")
trap 'rm -rf "$stage"' EXIT
mkdir -p "$stage/BlueWake.AppDir"

# The app, unchanged: the entry shim resolves paths beside the executable and
# the disc stays in game/. Nothing is unpacked at runtime.
cp -a "$app_dir/." "$stage/BlueWake.AppDir/"

# AppRun: just run the bundled bluewake, from the AppDir (not CWD) so the
# executable-relative defaults point inside the mounted image.
cat > "$stage/BlueWake.AppDir/AppRun" <<'APPRUN'
#!/bin/sh
HERE=$(dirname "$(readlink -f "$0")")
exec "$HERE/bluewake" "$@"
APPRUN
chmod +x "$stage/BlueWake.AppDir/AppRun"

cat > "$stage/BlueWake.AppDir/bluewake.desktop" <<DESKTOP
[Desktop Entry]
Type=Application
Name=BlueWake
Comment=The Legend of Zelda: The Wind Waker, statically recompiled
Exec=AppRun
Icon=bluewake
Terminal=false
Categories=Game;
DESKTOP

# An icon is optional for a personal AppImage; use the repo's app icon if present.
if [ -f "$root/apple/ios/resources/BlueWave.png" ]; then
  cp "$root/apple/ios/resources/BlueWave.png" "$stage/BlueWake.AppDir/bluewake.png"
fi

# The app's .so module must stay inside the AppDir; the release gate forbids
# shipping disc images, extracted files, saves or keys, so a public build
# attaches the game-code AppImage by hand and re-runs the gate on it.
appimagetool_args=("$stage/BlueWake.AppDir" "$out")
[ "$zsync" -eq 1 ] && appimagetool_args+=(--updateinformation "zsync|${out}.zsync")
appimagetool "${appimagetool_args[@]}"

echo "AppImage: $out"
if [ "$zsync" -eq 1 ]; then
  echo "zsync delta: ${out}.zsync"
  echo "publish both under the same URL for AppImageUpdate."
fi
