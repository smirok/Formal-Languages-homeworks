#include <iostream>
#include "parser.h"

bool Parser::parseRelation() {
    if (parseLexeme(lexeme::Identifier)) {
        if (parseLexeme(lexeme::Dot))
            return true;

        if (parseLexeme(lexeme::Corkscrew) &&
            parseDisjunction() && parseLexeme(lexeme::Dot))
            return true;
    }

    return false;
}

bool Parser::parseDisjunction() {
    if (!parseConjunction())
        return false;

    if (parseLexeme(lexeme::Semicolon))
        return parseDisjunction();

    return true;
}

bool Parser::parseConjunction() {
    if (!parseTerminal())
        return false;

    if (parseLexeme(lexeme::Comma))
        return parseConjunction();

    return true;
}

bool Parser::parseTerminal() {
    if (parseLexeme(lexeme::Identifier))
        return true;

    if (parseLexeme(lexeme::OpenBracket) && parseDisjunction() && parseLexeme(lexeme::CloseBracket))
        return true;

    return false;
}

bool Parser::parseLexeme(lexeme cur_lexeme) {
    if (_cur_pos == _lexemes_list.size() || _lexemes_list[_cur_pos]->_lexeme != cur_lexeme)
        return false;

    _cur_pos++;
    return true;
}

bool Parser::parse() {
    while (_cur_pos != _lexemes_list.size()) {
        if (!parseRelation()) {
            if (_cur_pos == _lexemes_list.size()) {
                std::cout << "Syntax error: EOF" << "\n";
            } else {
                std::cout << "Syntax error: line " << _lexemes_list[_cur_pos]->_line << ", col: "
                          << _lexemes_list[_cur_pos]->_col << "\n";
            }
            return false;
        }
    }
    return true;
}