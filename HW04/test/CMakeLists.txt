cmake_minimum_required(VERSION 3.16)
project(parserTest)

set(CMAKE_CXX_STANDARD 17)

include_directories(../include)

add_executable(parserTest ../src/parser.cpp ../include/parser.h ../src/lexer.cpp ../include/lexer.h TestMain.cpp)