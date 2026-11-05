# Stands in for SDL3's CMake package: Emscripten builds SDL3 itself with --use-port=sdl3,
# so the engine's find_package(SDL3 CONFIG) finds this and links the port.
if(NOT TARGET SDL3::SDL3)
    add_library(SDL3::SDL3 INTERFACE IMPORTED)
    set_target_properties(SDL3::SDL3 PROPERTIES
        INTERFACE_COMPILE_OPTIONS "--use-port=sdl3"
        INTERFACE_LINK_OPTIONS "--use-port=sdl3")
endif()
set(SDL3_FOUND TRUE)
