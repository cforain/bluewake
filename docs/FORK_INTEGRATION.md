# Source-fork integration

BlueWake integrates GPL-covered source changes from
[elliotttate/Wind-Waker-Recomp](https://github.com/elliotttate/Wind-Waker-Recomp), whose source is
public as checked on October 1, 2026. The imported commits retain elliotttate's authorship. BlueWake's
release restrictions, game-module privacy rules, PadMint workflow, bundle identifier and saves remain
the project's own.

## Shared runtime and iOS

The integration imports the main branch's feature commits through `887c26dfddba`:

- Renderer interpolation, matching of scenery and particles, steady 60/120 Hz presentation,
  batching, staging-buffer uploads and overload pacing.
- Optional jump, sprint, shorter fades, acceleration while a scene is fully black, and quick doors.
- Desktop mouse camera and direct right-stick camera, with aiming, zoom and collision checks.
- Fifteen Better Wind Waker settings selected inside newly translated modules, plus widescreen 16:10.
- Guest-alias synchronization/cache, actor-search budget optimization, a larger REL scratch window,
  and contextual frame-dip logging.

BlueWake adds touch Jump/Run buttons using its existing layout editor, forwards iOS keyboard jump
events, preserves the existing Smooth Motion preference and ProMotion choice, and leaves the new
gameplay options off until enabled. The iOS camera retains its original behavior by default.
The alias-cache epoch is atomic across the game and graphics threads. Existing dependency checkouts
fetch the parent without recursively fetching a new submodule from its old remote, then synchronize
the translator's remote before updating it.

RecompCore is pinned at `68929476fcc6be8539007583aa62a89c08fa63d0` and DolRecomp at
`b8b534591cba8ca7cd43943a655ee6e2591cf5de`. These are the fork's changes over BlueWake's previous
`2d60636` and `5c91d6e`. Base translation must still satisfy the existing composite digest.
New Better Wind Waker options and 16:10 require rebuilding the personal module. App-only validation
does not establish that module generation, training and gameplay with every option have passed.

## Checks performed here

- iOS app-only build and native Apple Silicon Mac host build pass.
- All 21 registered BlueWake host tests pass, including a new fast-transition test covering black
  menus, fade ordering, return to rendering, timeout, and disabled settings.
- Actor-search equivalence also passes with undefined-behavior sanitization.
- The composite generator's 18 synthetic fixtures pass. The separate CPU ABI script needs the
  absent `generated/full/composite-lib` developer fixture; it was not counted as a pass.
- Repository audit and public-assets check on the app-only IPA pass. This does not authorize a release.

The broader CTest discovery includes donor tests that were not built and placeholder tests named
`*_NOT_BUILT`; those were reported as not run, separate from the 21 passing BlueWake tests.
Imported Mac performance figures in the status ledger are the author's measurements, not new iPad
or iPhone performance evidence. Full device movement/door acceptance and thermal comparisons remain.

## Desktop work

The native Mac host now contains the fork's desktop controls and options menu. The fork's public
Mac packaging scripts bundle translated game code; that packaging model is not imported.
Windows has a separate source branch, `windows-release`, with additional code-generation changes
and experimental 60 Hz simulation. Windows integration and validation are tracked separately; neither
its ready-made releases nor their game modules are inputs to this work. Parallels remains off at the
user's request. Cross-compilation can check Windows source without claiming Direct3D/gameplay proof.

## Contribution path

The source integration gives elliotttate credit through Git authorship and the project notices.
Future changes can be contributed as ordinary pull requests against BlueWake. A source import does
not grant repository write access or imply the author has agreed to maintain BlueWake.
