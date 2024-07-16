cmake_minimum_required(VERSION 3.20)
project(Ironwail)

# Options
option(DO_USERDIRS "Enable user directories" OFF)
option(USE_CODEC_WAVE "Enable Wave codec" ON)
option(USE_CODEC_FLAC "Enable FLAC codec" OFF)
option(USE_CODEC_MP3 "Enable MP3 codec" ON)
option(USE_CODEC_VORBIS "Enable Vorbis codec" ON)
option(USE_CODEC_OPUS "Enable Opus codec" OFF)
option(USE_CODEC_MIKMOD "Enable Mikmod codec" OFF)
option(USE_CODEC_XMP "Enable XMP codec" OFF)
option(USE_CODEC_MODPLUG "Enable Modplug codec" OFF)
option(USE_CODEC_UMX "Enable UMX codec" OFF)

set(MP3LIB "mad" CACHE STRING "Library to use for MP3 decoding (mad or mpg123)")
set(VORBISLIB "vorbis" CACHE STRING "Library to use for OGG decoding (vorbis or tremor)")

# C Standard
set_property(GLOBAL PROPERTY C_STANDARD 11)
set($ENV{LD_LIBRARY_PATH} ${CMAKE_SOURCE_DIR}/gl4es)
set($ENV{EMCC_DEBUG} 1)
set($ENV{EMCC_STRICT} 1)
set($ENV{DEBUG} 1)
include_directories(${CMAKE_SOURCE_DIR}/gl4es/include)

# Build configurations
set(CMAKE_C_FLAGS "-Wall -Wno-trigraphs -pthread -sPTHREAD_POOL_SIZE=8 --use-port=sdl2 -sFULL_ES2=1 -sMAX_WEBGL_VERSION=2 -Wl,--error-limit=0 -sSTACK_OVERFLOW_CHECK=2 -fsanitize=address -fsanitize=undefined -sINITIAL_MEMORY=1024MB -sSTACK_SIZE=512MB -sALLOW_MEMORY_GROWTH  --embed-file=../id1@/id1")

if(DEFINED ENV{DEBUG} AND "$ENV{DEBUG}" STREQUAL "1")
    set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -DDEBUG -g -gsource-map")
else()
    set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -DNDEBUG -O2")
endif()

if(DO_USERDIRS)
    set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -DDO_USERDIRS=1")
endif()

set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -DUSE_SDL2")

# Music Sources
set(MUSIC_SOURCES
    Quake/bgmusic.c
    Quake/snd_codec.c
    Quake/snd_flac.c
    Quake/snd_wave.c
    Quake/snd_vorbis.c
    Quake/snd_opus.c
    Quake/snd_mp3tag.c
    Quake/snd_mikmod.c
    Quake/snd_modplug.c
    Quake/snd_xmp.c
    Quake/snd_umx.c
)

# Sound Objects
set(COMOBJ_SND
    Quake/snd_dma.c
    Quake/snd_mix.c
    Quake/snd_mem.c
    ${MUSIC_SOURCES}
)

set(SYSOBJ_SND
    Quake/snd_sdl.c
)

set(SYSOBJ_CDA
    Quake/cd_sdl.c
)

set(SYSOBJ_INPUT
    Quake/in_sdl.c
)

set(SYSOBJ_GL_VID
    Quake/gl_vidsdl.c
)

set(SYSOBJ_NET
    Quake/net_bsd.c
    Quake/net_udp.c
)

set(SYSOBJ_SYS
    Quake/pl_linux.c
    Quake/sys_sdl_unix.c
)

set(SYSOBJ_MAIN
    Quake/main_sdl.c
)

set(GLOBJS
    Quake/gl_refrag.c
    Quake/gl_rlight.c
    Quake/gl_rmain.c
    Quake/gl_fog.c
    Quake/gl_rmisc.c
    Quake/r_part.c
    Quake/r_world.c
    Quake/gl_screen.c

    # Quake/gl_shaders.c
    Quake/gl_sky.c
    Quake/gl_warp.c
    ${SYSOBJ_GL_VID}
    Quake/gl_draw.c
    Quake/image.c
    Quake/gl_texmgr.c
    Quake/gl_mesh.c
    Quake/r_sprite.c
    Quake/r_alias.c
    Quake/r_brush.c
    Quake/gl_model.c
)

set(SOURCES
    Quake/strlcat.c
    Quake/strlcpy.c
    ${GLOBJS}
    ${SYSOBJ_INPUT}
    ${COMOBJ_SND}
    ${SYSOBJ_SND}
    ${SYSOBJ_CDA}
    ${SYSOBJ_NET}
    Quake/net_dgrm.c
    Quake/net_loop.c
    Quake/net_main.c
    Quake/chase.c
    Quake/cl_demo.c
    Quake/cl_input.c
    Quake/cl_main.c
    Quake/cl_parse.c
    Quake/cl_tent.c
    Quake/console.c
    Quake/keys.c
    Quake/menu.c
    Quake/sbar.c
    Quake/view.c
    Quake/wad.c
    Quake/cmd.c
    Quake/common.c

    # Quake/steam.c
    # Quake/json.c
    Quake/miniz.c
    Quake/crc.c
    Quake/cvar.c
    Quake/cfgfile.c
    Quake/host.c
    Quake/host_cmd.c
    Quake/mathlib.c
    Quake/pr_cmds.c
    Quake/pr_edict.c
    Quake/pr_exec.c
    Quake/sv_main.c
    Quake/sv_move.c
    Quake/sv_phys.c
    Quake/sv_user.c
    Quake/world.c
    Quake/zone.c
    ${SYSOBJ_SYS}
    ${SYSOBJ_MAIN}
)

# Add executable
add_executable(ironwail ${SOURCES})
set_target_properties(ironwail PROPERTIES OUTPUT_NAME "ironwail")
set_target_properties(ironwail PROPERTIES SUFFIX ".html")
add_definitions(-DWITHOUT_CURL -DDEBUG)

# Link Libraries
target_link_libraries(ironwail ${CMAKE_SOURCE_DIR}/gl4es/libGL.a)
target_link_options(ironwail PUBLIC "LINKER:-lGL")

if(USE_CODEC_FLAC)
    target_link_libraries(ironwail FLAC)
endif()

if(USE_CODEC_VORBIS)
    if(VORBISLIB STREQUAL "vorbis")
        add_definitions(-DUSE_VORBIS=1 -DUSE_OGG=1)

    # target_link_libraries(ironwail vorbisfile vorbis ogg)
    elseif(VORBISLIB STREQUAL "tremor")
        add_definitions(-DVORBIS_USE_TREMOR)
        target_link_libraries(ironwail vorbisidec ogg)
    endif()
endif()

if(USE_CODEC_MP3)
    if(MP3LIB STREQUAL "mad")
    # target_link_libraries(ironwail mad)
    elseif(MP3LIB STREQUAL "mpg123")
        target_link_libraries(ironwail mpg123)
    endif()
endif()

if(USE_CODEC_MIKMOD)
    target_link_libraries(ironwail mikmod)
endif()

if(USE_CODEC_XMP)
    target_link_libraries(ironwail xmp)
endif()

if(USE_CODEC_MODPLUG)
    target_link_libraries(ironwail modplug)
endif()

if(USE_CODEC_UMX)
    target_compile_definitions(ironwail PRIVATE USE_CODEC_UMX)
endif()

# Install rules
install(TARGETS ironwail DESTINATION /usr/local/games/quake)
