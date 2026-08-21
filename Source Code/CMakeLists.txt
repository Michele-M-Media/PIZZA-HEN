cmake_minimum_required (VERSION 3.20)

project("PIZZA_HEN")

# PIZZA HEN FIX13: SDK-release-neutral build layer.
# The build launcher sets PIZZA_HEN_SDK_ROOT, PS5_PAYLOAD_SDK and PS5SDK.
# Keep source subprojects independent from one specific SDK directory name.
if(NOT DEFINED PS5_PAYLOAD_SDK OR "${PS5_PAYLOAD_SDK}" STREQUAL "")
    if(DEFINED PIZZA_HEN_SDK_ROOT AND NOT "${PIZZA_HEN_SDK_ROOT}" STREQUAL "")
        set(PS5_PAYLOAD_SDK "${PIZZA_HEN_SDK_ROOT}")
    elseif(DEFINED ENV{PS5_PAYLOAD_SDK} AND NOT "$ENV{PS5_PAYLOAD_SDK}" STREQUAL "")
        set(PS5_PAYLOAD_SDK "$ENV{PS5_PAYLOAD_SDK}")
    elseif(DEFINED ENV{PS5SDK} AND NOT "$ENV{PS5SDK}" STREQUAL "")
        set(PS5_PAYLOAD_SDK "$ENV{PS5SDK}")
    endif()
endif()
if(NOT DEFINED PS5_PAYLOAD_SDK OR "${PS5_PAYLOAD_SDK}" STREQUAL "")
    message(FATAL_ERROR "PIZZA HEN: PS5 payload SDK root was not provided by the multi-SDK launcher")
endif()
set(PIZZA_HEN_SDK_ROOT "${PS5_PAYLOAD_SDK}" CACHE PATH "Selected PS5 SDK root" FORCE)
set(PS5SDK "${PS5_PAYLOAD_SDK}" CACHE PATH "Compatibility SDK alias" FORCE)

find_package(Python3 COMPONENTS Interpreter REQUIRED)
if(NOT DEFINED PIZZA_HEN_OBJCOPY OR "${PIZZA_HEN_OBJCOPY}" STREQUAL "")
    find_program(PIZZA_HEN_OBJCOPY
        NAMES llvm-objcopy llvm-objcopy-22 llvm-objcopy-21 llvm-objcopy-20 llvm-objcopy-19 llvm-objcopy-18 objcopy
        HINTS "${PS5_PAYLOAD_SDK}/bin")
endif()
if(NOT PIZZA_HEN_OBJCOPY)
    message(FATAL_ERROR "PIZZA HEN: llvm-objcopy/objcopy not found")
endif()
message(STATUS "PIZZA HEN SDK root: ${PS5_PAYLOAD_SDK}")
message(STATUS "PIZZA HEN objcopy: ${PIZZA_HEN_OBJCOPY}")


set(PROJECT_ROOT "${CMAKE_CURRENT_SOURCE_DIR}")
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${PROJECT_ROOT}/bin)
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${PROJECT_ROOT}/lib)
set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${PROJECT_ROOT}/lib)	# static libs are archive

include_directories	(SYSTEM "${PROJECT_ROOT}/include")
include_directories(SYSTEM "${PS5_PAYLOAD_SDK}")
include_directories(SYSTEM "${PS5_PAYLOAD_SDK}/include")

add_subdirectory(libhijacker)
add_subdirectory(libNidResolver)
# add_subdirectory(libRPI)
add_subdirectory(libSelfDecryptor)
add_subdirectory(libNineS)
add_subdirectory(libelfldr)
add_subdirectory(shellui)
add_subdirectory(fps_elf)

# PIZZA HEN v1.0: CheatRunner v0.17 is the sole active cheat backend.
# Build the vendored upstream source as its own ELF; daemon embeds/deploys it on demand.
add_subdirectory(third_party/CheatRunner-0.17)
set_target_properties(CheatRunner PROPERTIES RUNTIME_OUTPUT_DIRECTORY "${PROJECT_ROOT}/bin")

add_subdirectory(daemon)
add_subdirectory(util)
add_subdirectory(selector_action)
add_subdirectory(toolbox_action)
add_subdirectory(toolbox_api)
add_subdirectory(bootstrapper)
add_subdirectory(unpacker)