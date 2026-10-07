// SPDX-License-Identifier: GPL-3.0-or-later
#pragma once
// Player 1 for a connected controller while no controller is player 1 (#61).
//
// BlueWake reads player 1 only, and Aurora reads a port from SDL's player
// slot. SDL gives a controller a slot when it detects it, and only if it
// recognizes it then. One it recognizes later, through gamecontrollerdb.txt
// (loaded once SDL is already running), is opened but never placed, so it did
// nothing; so did a sole controller left in slot 2 after the first one was
// unplugged. Call this whenever a controller is added, removed or remapped:
// with player 1 free, the first connected controller takes it.
//
// The choice is not saved. PADSetPortForIndex would save it, and a saved port
// then keeps every other controller off player 1 until that one returns.
#include <stdbool.h>
#include <stdio.h>
#include <dolphin/pad.h>
#include <SDL3/SDL_gamepad.h>

static inline bool bw_claim_player_one(void) {
    if (PADGetIndexForPort(0) >= 0)
        return false;
    const u32 count = PADCount();
    for (u32 i = 0; i < count; i++) {
        SDL_Gamepad* pad = PADGetSDLGamepadForIndex(i);
        if (pad == NULL)
            continue;
        const int previous = SDL_GetGamepadPlayerIndex(pad);
        if (!SDL_SetGamepadPlayerIndex(pad, 0))
            continue;
        const char* name = SDL_GetGamepadName(pad);
        if (previous < 0)
            fprintf(stderr, "[pad] '%s' is player 1 (it had no player slot)\n", name ? name : "controller");
        else
            fprintf(stderr, "[pad] '%s' is player 1 (it was player %d)\n", name ? name : "controller",
                    previous + 1);
        return true;
    }
    return false;
}
