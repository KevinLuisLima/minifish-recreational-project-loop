#=============================================================
# File: build_system/CMakeLists.txt
# Description: CMake configuration file for building the core C game logic.
# Purpose: Compiles chess_engine/chess.c into a reusable static library (libchesscore).
#=============================================================

cmake_minimum_required(VERSION 3.10)
project(ChessCoreEngine LANGUAGES C)

# The project is restricted to plain C (no C++ sources are compiled here).
set(CMAKE_C_STANDARD 99)
set(CMAKE_C_STANDARD_REQUIRED ON)
set(CMAKE_C_EXTENSIONS OFF)

# Default build type when none is given on the command line.
if(NOT CMAKE_BUILD_TYPE)
    set(CMAKE_BUILD_TYPE Debug CACHE STRING "Build type" FORCE)
endif()

# Source files of the core logic (plain C only).
set(SOURCE_FILES
    ${CMAKE_CURRENT_SOURCE_DIR}/../chess_engine/chess.c
)

# Static library encapsulating all C game rules.
add_library(chesscore STATIC ${SOURCE_FILES})

# Public headers live in chess_engine/ (api_c_layer.h).
target_include_directories(chesscore PUBLIC
    ${CMAKE_CURRENT_SOURCE_DIR}/../chess_engine
)

target_compile_options(chesscore PRIVATE
    $<$<C_COMPILER_ID:GNU,Clang>:-Wall -Wextra>
)
