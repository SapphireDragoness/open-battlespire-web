/* What Emscripten's SDL3 port leaves out but the engine links against. None of it is reached in the
 * browser: the page picks the Battlespire folder and starts the game with -d, so the startup screen
 * (and its Browse button) never shows. */
#include <SDL3/SDL.h>

void SDL_ShowOpenFolderDialog(SDL_DialogFileCallback callback, void *userdata, SDL_Window *window,
                              const char *default_location, bool allow_many)
{
    (void)window;
    (void)default_location;
    (void)allow_many;
    SDL_SetError("no folder dialog in the browser");
    callback(userdata, NULL, -1);
}
