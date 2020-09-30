#include <iostream>
#include "parser.h"

bool Parser::parseRelation() {
    int snapshot_pos = _cur_pos;
    if (parseLexeme(lexeme::Identifier) && parseLexeme(lexeme::Dot))
        return true;

    _cur_pos = snapshot_pos;
    if (parseLexeme(lexeme::Identifier) && parseLexeme(lexeme::Corkscrew) &&
        parseDisjunction() && parseLexeme(lexeme::Dot))
        return true;

    _cur_pos = snapshot_pos;
    return false;
}

bool Parser::parseDisjunction() {
    int snapshot_pos = _cur_pos;
    if (!parseConjunction()) {
        _cur_pos = snapshot_pos;
        return false;
    }

    while (parseLexeme(lexeme::Semicolon)) {
        if (!parseConjunction()) {
            _cur_pos = snapshot_pos;
            return false;
        }
    }
    return true;
}

bool Parser::parseConjunction() {
    int snapshot_pos = _cur_pos;
    if (!parseTerminal()) {
        _cur_pos = snapshot_pos;
        return false;
    }

    while (parseLexeme(lexeme::Comma)) {
        if (!parseTerminal()) {
            _cur_pos = snapshot_pos;
            return false;
        }
    }

    return true;
}

bool Parser::parseTerminal() {
    int snapshot_pos = _cur_pos;
    if (parseLexeme(lexeme::Identifier))
        return true;

    _cur_pos = snapshot_pos;
    if (parseLexeme(lexeme::OpenBracket) && parseDisjunction() && parseLexeme(lexeme::CloseBracket))
        return true;

    _cur_pos = snapshot_pos;
    return false;
}

bool Parser::parseLexeme(lexeme lexema) {
    if (_cur_pos == _lexemes_list.size() || _lexemes_list[_cur_pos]->_lexeme != lexema) {
        _error_pos = _cur_pos;
        return false;
    }
    _cur_pos++;
    return true;
}

void Parser::parse() {
    while (_cur_pos != _lexemes_list.size()) {
        if (!parseRelation()) {
            std::cerr << "Syntax error: line " << _lexemes_list[_error_pos]->_line << ", col: "
                      << _lexemes_list[_error_pos]->_col << "\n";
            throw std::exception();
        }
    }
}