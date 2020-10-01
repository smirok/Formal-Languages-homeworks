cmake_minimum_required(VERSION 3.16.3)
project(parser)

set(CMAKE_CXX_STANDARD 17)

include_directories(include)

add_executable(parser main.cpp
        src/lexer.cpp include/lexer.h
        src/parser.cpp include/parser.h
        src/reader.cpp include/reader.h)
