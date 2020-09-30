#include "lexer.h"

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

bool Lexer::lex(std::string file) try {
    _reader = Reader(std::move(file));
    _current_lexeme = lexeme::Nothing;
    _lexemes_list.clear();
    std::string cur_identifier;

    while (true) {
        char sym = _reader.readChar();

        switch (_current_lexeme) {
            case Corkscrew: {
                lexCorkscrew(sym);
                break;
            }
            case Identifier: {
                lexIdentifier(cur_identifier, sym);
            }
            case Nothing: {
                lexNothing(cur_identifier, sym);
                break;
            }
        }

        if (sym == '\0') {
            return true;
        }
    }
} catch (...) {
    return false;
}

std::vector<Lexeme_info *> &Lexer::getLexemesList() {
    return _lexemes_list;
}

void Lexer::lexCharKeywords(char sym) {
    switch (sym) {
        case '(':
            _lexemes_list.push_back(
                    new Lexeme_info(lexeme::OpenBracket, _reader.getLine(), _reader.getColumn())
            );
            break;
        case ')':
            _lexemes_list.push_back(
                    new Lexeme_info(lexeme::CloseBracket, _reader.getLine(), _reader.getColumn())
            );
            break;
        case ',':
            _lexemes_list.push_back(
                    new Lexeme_info(lexeme::Comma, _reader.getLine(), _reader.getColumn())
            );
            break;
        case ';':
            _lexemes_list.push_back(
                    new Lexeme_info(lexeme::Semicolon, _reader.getLine(), _reader.getColumn())
            );
            break;
        case '.':
            _lexemes_list.push_back(
                    new Lexeme_info(lexeme::Dot, _reader.getLine(), _reader.getColumn())
            );
            break;
        case ' ':
            break;
        case '\n':
            break;
        case '\0': {
            if (_current_lexeme == lexeme::Corkscrew)
                throw std::exception();
            break;
        }
        default:
            throw std::exception();
    }
}

void Lexer::lexCorkscrew(char sym) {
    if (sym == '-') {
        _current_lexeme = lexeme::Nothing;
        _lexemes_list.push_back(
                new Lexeme_info(lexeme::Corkscrew, _reader.getLine(), _reader.getColumn() - 1)
        );
    } else {
        throw std::exception();
    }
}

void Lexer::lexNothing(std::string &cur_identifier, char sym) {
    if (sym == ':') {
        _current_lexeme = lexeme::Corkscrew;
    } else if (valid_identify(sym, _current_lexeme)) {
        cur_identifier += sym;
        _current_lexeme = lexeme::Identifier;
    } else
        lexCharKeywords(sym);
}

void Lexer::lexIdentifier(std::string &cur_identifier, char sym) {
    if (valid_identify(sym, _current_lexeme)) {
        cur_identifier += sym;
        _current_lexeme = lexeme::Identifier;
    } else {
        _lexemes_list.push_back(
                new Identifier_info(cur_identifier, lexeme::Identifier,
                                    _reader.getLine(), _reader.getColumn() - cur_identifier.size())
        );
        _current_lexeme = Nothing;
        cur_identifier.clear();
    }
}

bool valid_identify(char sym, lexeme cur_lexeme) {
    if (cur_lexeme == lexeme::Identifier) {
        return sym == '_' || (sym >= '0' && sym <= '9') || (sym >= 'a' && sym <= 'z') || (sym >= 'A' && sym <= 'Z');
    } else {
        return sym == '_' || (sym >= 'a' && sym <= 'z') || (sym >= 'A' && sym <= 'Z');
    }
}