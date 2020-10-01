#ifndef HW04_LEXER_H
#define HW04_LEXER_H

#include "reader.h"

#include <utility>
#include <vector>

enum lexeme {
    Corkscrew,
    Dot,
    Identifier,
    Comma,
    Semicolon,
    OpenBracket,
    CloseBracket,
    Nothing
};

struct Lexeme_info {
    Lexeme_info(lexeme lexeme, int line, int col) : _lexeme(lexeme), _line(line), _col(col) {};

    virtual ~Lexeme_info() = default;

    lexeme _lexeme;
    int _line;
    int _col;
};

struct Identifier_info : public Lexeme_info {
    Identifier_info(std::string identifier, lexeme lexeme, int line, int col) :
            Lexeme_info(lexeme, line, col), _identifier(std::move(identifier)) {};

    std::string _identifier;
};

class Lexer {
public:
    explicit Lexer() = default;

    bool lex(std::string file);

    std::vector<Lexeme_info *> &getLexemesList();

private:
    void lexCharKeywords(char sym);
    void lexCorkscrew(char sym);
    void lexNothing(std::string &cur_identifier, char sym);
    void lexIdentifier(std::string &cur_identifier, char sym);

    Reader _reader;
    lexeme _current_lexeme = Nothing;
    std::vector<Lexeme_info *> _lexemes_list;
};

bool valid_identify(char sym, lexeme cur_lexeme);

#endif //HW04_LEXER_H
