cmake_minimum_required(VERSION 3.16.3)
project(HW04)

set(CMAKE_CXX_STANDARD 17)

include_directories(include)

add_executable(HW04 main.cpp src/lexer.cpp include/lexer.h)
