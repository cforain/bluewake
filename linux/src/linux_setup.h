#ifndef BLUEWAKE_LINUX_SETUP_H
#define BLUEWAKE_LINUX_SETUP_H

#ifdef __cplusplus
extern "C" {
#endif

// Show the opt-in Linux setup window. Returns 1 to continue into the game,
// 0 when the player closes or cancels it, and -1 after reporting an error.
// The selected disc is returned in `disc`; preferences are written to the
// normal XDG settings file.
int bw_linux_setup(const char* data_dir, char* disc, unsigned long disc_size);

#ifdef __cplusplus
}
#endif

#endif
