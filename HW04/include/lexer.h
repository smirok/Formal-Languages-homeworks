#ifndef HW04_LEXER_H
#define HW04_LEXER_H

#include <string>

enum lexeme {
    Corkscrew,
    Dot,
    Identifier,
    Comma,
    Semicolon,
    OpenBracket,
    CloseBracket,
    Bad
};

class Reader {
public:
    Reader(std::string file) : _file(file) {};
    void readChar();
    int getLine() const;
    int getColumn() const;
private:
    std::string _file;
    int current_line = 0;
    int current_column = 0;
};

class Lexer {
public:
    Lexer(std::string file) : _reader(Reader(file)) {};
    void lex();
private:
    Reader _reader;
    lexeme current_lexeme;
};

#endif //HW04_LEXER_H
