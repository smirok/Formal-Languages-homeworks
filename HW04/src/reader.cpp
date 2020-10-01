#include "reader.h"

char Reader::readChar() {
    char cur_char = _file[_pos++];
    if (cur_char == '\n') {
        _line++;
        prev_column = _column;
        _column = -1;
        _is_newline = true;
    } else {
        _column++;
        _is_newline = false;
    }
    return cur_char;
}

int Reader::getLine() const {
    return _line - (_is_newline ? 1 : 0);
}

int Reader::getColumn() const {
    return _is_newline ? prev_column + 1 : _column;
}