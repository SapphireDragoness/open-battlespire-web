cmake_minimum_required(VERSION 3.25)

project(OpenBattlespireWeb
    DESCRIPTION "OpenBattlespire in the browser"
    LANGUAGES C)

if(NOT EMSCRIPTEN)
    message(FATAL_ERROR "Build this with Emscripten: cmake --preset web-debug (see README.md)")
endif()

# The engine, as it is upstream: only the libraries and the game, no tests or tools, drawing with
# OpenGL ES 3.0 (WebGL 2).
set(BS_BUILD_TESTS OFF CACHE BOOL "" FORCE)
set(BS_BUILD_TOOLS OFF CACHE BOOL "" FORCE)
set(BS_GLES ON CACHE BOOL "" FORCE)
set(SDL3_DIR "${CMAKE_CURRENT_SOURCE_DIR}/cmake/sdl3-port" CACHE PATH "" FORCE)
add_subdirectory(engine EXCLUDE_FROM_ALL)

# The engine's game, built as the page: build/<preset>/site/index.html, .js and .wasm.
set(SHELL_FILE "${CMAKE_CURRENT_SOURCE_DIR}/web/shell.html")
target_sources(openbattlespire PRIVATE src/sdl_stubs.c)
set_target_properties(openbattlespire PROPERTIES
    OUTPUT_NAME "index"
    SUFFIX ".html"
    RUNTIME_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/site"
    LINK_DEPENDS "${SHELL_FILE}")
target_link_options(openbattlespire PRIVATE
    "--shell-file=${SHELL_FILE}"
    -sMIN_WEBGL_VERSION=2
    -sMAX_WEBGL_VERSION=2
    -sALLOW_MEMORY_GROWTH=1
    -sSTACK_SIZE=4MB              # native stacks are megabytes; Emscripten's default is 64 KB
    -sINVOKE_RUN=0                # the page starts the game once the files are in
    -sEXPORTED_RUNTIME_METHODS=callMain,FS
    -sFORCE_FILESYSTEM=1)

add_custom_target(site ALL DEPENDS openbattlespire)
