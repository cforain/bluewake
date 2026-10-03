# Agent instructions

## Contributor attribution

Do not add AI tools or models as commit authors or co-authors, or add generated-by
attribution or AI session links to commit messages and pull requests. Preserve
human authorship and human co-author credits, including imported donor history.
The Attribution workflow enforces this with `scripts/check_attribution.py`.

## Releases

The maintainers decided on October 4, 2026 to make one exception: BlueWake publishes a ready-made Windows build that contains the translated game module, as Wind Waker Recomp did. Mac, iPhone and iPad stay on PadMint: their releases hold source and the app without game code. Do not publish any other build with game code.

Every release artifact must pass `scripts/release/check_public_assets.sh <artifact>...`, which runs `python3 ~/.codex/release-gate/release_gate.py` on the maintainer's machine. For the Windows build the only accepted finding is `containsTranslatedGameCode: true`. Any other failure is a stop, not a note: the Windows build must contain no disc data, game assets, saves, signing material or console keys (Elliott's `nodtool.exe` embeds Wii common keys, so it is left out).

## Personal builds stay personal

The game module (`gGZLE01_recomp.dylib`) is translated from the player's own disc. An IPA or app that contains it is a personal build: never upload, attach, commit or link it anywhere. The maintainers' Windows release build is the only exception. Public releases hold source plus the app without game code (`scripts/builder/build.sh --app-only --ipa BlueWake-vX.Y.Z-ios-unsigned.ipa`, checked with PadMint's `audit` before upload); players add their own module with PadMint (`padmint make bluewake ios`) or `scripts/builder/build.sh DISC.iso --ipa OUT.ipa`.
