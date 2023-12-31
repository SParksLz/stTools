cmake_minimum_required( VERSION 3.6 )

project( hdk_sopNurbs )

# CMAKE_PREFIX_PATH must contain the path to the toolkit/cmake subdirectory of
# the Houdini installation. See the "Compiling with CMake" section of the HDK
# documentation for more details, which describes several options for
# specifying this path.
set(HFS "C:/Program\ Files/Side\ Effects\ Software/Houdini\ 18.5.351")
list( APPEND CMAKE_PREFIX_PATH "${HFS}/toolkit/cmake" )

# Locate Houdini's libraries and header files.
# Registers an imported library target named 'Houdini'.
find_package( Houdini REQUIRED )

set( library_name SOP_NURBS )

# Code generation for the embedded DS file in SOP_Star.C.
# houdini_generate_proto_headers( FILES SOP_NURBS.C )

# Add a library and its source files.
add_library( ${library_name} SHARED
    SOP_NURBS.C
    SOP_NURBS.h
)

# Link against the Houdini libraries, and add required include directories and
# compile definitions.
target_link_libraries( ${library_name} Houdini )

# Include ${CMAKE_CURRENT_BINARY_DIR} for the generated header.
target_include_directories( ${library_name} PRIVATE
    ${CMAKE_CURRENT_BINARY_DIR}
)

# Sets several common target properties, such as the library's output directory.
houdini_configure_target( ${library_name} )
