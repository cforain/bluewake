# Source release preparation

The release goal is a public BlueWake source repository and a reproducible,
interactive Mac builder that produces a personal IPA from the player's disc.
The optimized player build must pass the same device performance checks as the
developer build. A successful compile alone does not establish readiness.

## Goal loop

1. Preserve the private development repository and local data. Start the new
   repository from reviewed source with fresh history; retain the README,
   badges, community links, license and repository presentation.
2. Audit every tracked file and the public source archive. Keep disc contents,
   translated modules, saves, signing material and private training profiles
   out of Git. Review binary fixtures and patches manually as well as running
   the automated checks.
3. Make the builder generate its optimization profile on the player's Mac.
   Train using their disc, verify that training reached gameplay, then compile
   the optimized iOS module. Generate supported mod variants locally too.
4. Show stage, elapsed time, compiler progress and actionable failures. Cache
   only results whose input identities match. Preserve logs for diagnosis.
5. Build from a fresh source checkout without development-only dependencies.
   Validate the personal package and install in place after backing up saves.
6. Compare the player and developer builds on the same iPad, settings, scenes
   and thermal conditions. Check Outset and a second demanding area. Preserve
   save data and record actual gameplay evidence.
7. Transfer the proven stages and their progress/cache contract to PadForge;
   keep one shared builder with game-specific adapters.
8. Recheck the exact source archive and Git history, review player instructions,
   update the private audit record, then publish only cleared source/tooling.

After a failure, record the cause, make the smallest justified fix, and repeat
the affected check. Do not substitute an easier scene or a developer-only
profile for the player build. Do not call the release ready while a required
check remains unverified.

## Current status

- The private repository was renamed and its local checkout preserved.
- The new checkout began with the same source tree and one initial commit.
- A fresh-card Mac training run reached player control and produced valid game
  counters: 262 translated functions executed, including all 100 covered by
  the developer's retained profile. That first run used LLE audio. Validation
  with the shipping HLE backend and optimized device performance is in progress.
- Fresh extraction, translation and all mod variants reproduced the same
  805-file source digest as the training input. The iOS host app also compiled.
- Stage cancellation (including a TERM-resistant descendant), profile changes
  forcing recompilation, paths with spaces and mod-cache invalidation passed
  focused checks. The source archive passed the publication scan and manual
  metadata/patch review.
- GitHub Actions could not start because of an account billing/spending-limit
  error; its repository audit and dependency checks passed locally.
- Earlier matched Outset tests measured about 26 FPS without PGO, 27.5 FPS
  with runtime/host profiles, and 29.9 FPS with the developer's full profile.
  These measurements do not yet prove the new local-training path.
- Public distribution remains paused pending the checks above. Personal IPAs
  contain translated game code and remain on the builder's machine.
- The iPad is unavailable during this pass. All ongoing work is Mac-only;
  hardware acceptance is deferred until the owner makes it available.

See [PadForge handoff](PADFORGE_HANDOFF.md) for the shared-builder contract.
