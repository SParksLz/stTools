cmake_minimum_required(VERSION 3.1)
project(renderOverrideTestB)

set(CMAKE_MODULE_PATH ${CMAKE_CURRENT_SOURCE_DIR}/modules)

set(SOURCE_FILES "pluginMain.cpp"
                 "sampleCmd.cpp"
                 "sampleCmd.h")

find_package(Maya REQUIRED)

add_library(renderOverrideTestB SHARED ${SOURCE_FILES})
target_link_libraries(renderOverrideTestB PRIVATE Maya::Maya)
target_include_directories(renderOverrideTestB PRIVATE Maya::Maya)
MAYA_PLUGIN(renderOverrideTestB)