# OpenBattlespire Web

[OpenBattlespire](https://github.com/SapphireDragoness/open-battlespire) in the browser: the same engine,
compiled to WebAssembly with Emscripten, drawing with WebGL 2.

**No game data is included.** Players choose the folder of their own Battlespire install (GOG or Steam)
and the page reads it in the browser tab; nothing is uploaded. The files it needs are kept in the
browser's IndexedDB, so later visits offer Play without choosing the folder again, and so are the saved
games and settings.

## Storage

All in the site's IndexedDB, all in `web/shell.html`:

- `openbattlespire-install`: the install's files as the page copied them (`files`: Blobs keyed by path;
  `meta`: their list, written last so a copy cut short is never offered). "Forget these files" clears it.
- `/saves` and `/libsdl`: Emscripten IDBFS mounts with `autoPersist`, read in before the game starts.
  `/saves` is `--saves` (our save slots and the CharacterMaker's classes); `/libsdl` holds SDL's pref
  path, where `settings.ini` goes. Each file the engine writes is copied to IndexedDB when it closes it.

Not affiliated with or endorsed by Bethesda. The Elder Scrolls and Battlespire are trademarks of their
owners.

## Layout

- `engine/`: the engine, as a git submodule. Fixes to the game go there (upstream), not here.
- `web/shell.html`: the page: the folder picker, loading the files, starting the game.
- `src/`: C that only the browser build needs.
- `cmake/sdl3-port/`: lets the engine's `find_package(SDL3)` use Emscripten's SDL3 port.
- `tools/serve.py`: a development server (localhost only).

## Building

Needs CMake ≥ 3.25, Ninja and the [Emscripten SDK](https://emscripten.org/docs/getting_started/downloads.html):

```sh
git clone --recursive <this repo>    # or: git submodule update --init
source ~/emsdk/emsdk_env.sh
cmake --preset web-debug             # or web-release
cmake --build build/debug
```

The site is `build/debug/site/`: `index.html`, `index.js` and `index.wasm`, to serve as static files.

## Running it locally

```sh
tools/serve.py --data ~/Games/Battlespire
```

Then open <http://localhost:8000/> and choose the folder, or skip the picker on reloads with
<http://localhost:8000/?dev>, which loads the install `--data` names. `?dev&cd` also loads the CD image
(intro video, voices), and `?dev&args=--level,l1.bs6,--mute` passes options to the game as on the
command line.

## Status

The title screen, menus and levels run, from GAME.EXE, GAMEDATA and MUSIC (about 230 MB, held in memory);
the CD image is optional. The files, the saved games and the settings are kept between visits. Not done
yet: browser key conflicts (Ctrl+W, Esc, F12), exporting and importing saves.
