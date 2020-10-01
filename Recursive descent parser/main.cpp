#include "lexer.h"
#include "parser.h"

#include <iostream>
#include <fstream>

std::string read_file(const std::string &file_name) {
    std::ifstream in = std::ifstream(file_name);
    return std::string((std::istreambuf_iterator<char>(in)),
                       std::istreambuf_iterator<char>());
}

void printLexResult(std::vector<Lexeme_info *> &list) {
    int i = 0;
    for (auto &info : list) {
        std::cout << ++i << ") ";
        switch (info->_lexeme) {
            case Corkscrew:
                std::cout << "Corkscrew";
                break;
            case Dot:
                std::cout << "Dot";
                break;
            case Identifier: {
                auto *iden_info = dynamic_cast<Identifier_info *>(info);
                std::cout << "Identifier" << " " << iden_info->_identifier;
                break;
            }
            case Comma:
                std::cout << "Comma";
                break;
            case Semicolon:
                std::cout << "Semicolon";
                break;
            case OpenBracket:
                std::cout << "OpenBracket";
                break;
            case CloseBracket:
                std::cout << "CloseBracket";
                break;
            case Nothing:
                break;
        }
        std::cout << " " << info->_line << " " << info->_col << "\n";
    }
}

int main() {
    std::string file_name;
    std::cin >> file_name;

    std::string file = read_file(file_name);
    Lexer lexer;
    lexer.lex(file);
    auto &x = lexer.getLexemesList();

    printLexResult(x);

    Parser parser(x);
    if (parser.parse())
        std::cout << "OK";
    return 0;
}
