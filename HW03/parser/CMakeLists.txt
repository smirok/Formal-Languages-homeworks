cmake_minimum_required(VERSION 3.16)
project(parser)

set(CMAKE_CXX_STANDARD 17)

include_directories(include)

add_executable(parser main.cpp src/parser.cpp include/parser.h)
