#ifndef HW04_PARSER_H
#define HW04_PARSER_H

#include <utility>
#include "lexer.h"

class Parser {
public:
    Parser(std::vector<Lexeme_info *>& lexemes_list) : _lexemes_list(lexemes_list) {};
    bool parse();

private:
    bool parseRelation();
    bool parseDisjunction();
    bool parseConjunction();
    bool parseTerminal();
    bool parseLexeme(lexeme cur_lexeme);

    int _cur_pos = 0;
    std::vector<Lexeme_info *>& _lexemes_list;
};

#endif //HW04_PARSER_H
