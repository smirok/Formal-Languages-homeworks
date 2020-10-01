#ifndef HW04_READER_H
#define HW04_READER_H

#include <string>

class Reader {
public:
    Reader() = default;
    explicit Reader(std::string file) : _file(std::move(file)) {};

    char readChar();
    int getLine() const;
    int getColumn() const;

private:
    std::string _file;
    bool _is_newline = false;
    int _line = 0;
    int _column = -1;
    int _pos = 0;
    int prev_column = -1;
};

#endif //HW04_READER_H
