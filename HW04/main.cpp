#include "lexer.h"

#include <iostream>
#include <fstream>
#include <iterator>
//using namespace std;



std::string read_file(const std::string &file_name) {
    std::ifstream in = std::ifstream(file_name);
    return std::string((std::istreambuf_iterator<char>(in)),
                       std::istreambuf_iterator<char>());
}

void printLexResult(std::vector<Lexeme_info *> &list) {
    int i = 0;
    for (auto info : list) {
        switch (info->_lexeme) {
            case Corkscrew:
                std::cout << ++i << ") " << "Corkscrew" << " " << info->_line << " " << info->_col << "\n";
                break;
            case Dot:
                std::cout << ++i << ") " << "Dot" << " " << info->_line << " " << info->_col << "\n";
                break;
            case Identifier: {
                auto *iden_info = dynamic_cast<Identifier_info *>(info);
                std::cout << ++i << ") " << "Identifier" << " " << iden_info->_identifier << " "
                          << info->_line << " " << info->_col << "\n";
                break;
            }
            case Comma:
                std::cout << ++i << ") " << "Comma" << " " << info->_line << " " << info->_col << "\n";
                break;
            case Semicolon:
                std::cout << ++i << ") " << "Semicolon" << " " << info->_line << " " << info->_col << "\n";
                break;
            case OpenBracket:
                std::cout << ++i << ") " << "OpenBracket" << " " << info->_line << " " << info->_col << "\n";
                break;
            case CloseBracket:
                std::cout << ++i << ") " << "CloseBracket" << " " << info->_line << " " << info->_col << "\n";
                break;
            case Nothing:
                break;
        }
    }
}

int main() {
    std::string file_name;
    std::cin >> file_name;

    std::string file = read_file(file_name);
    for (auto x : file) {
        if (x == '\n')
            std::cout << "*";
        else
            std::cout << x;
    }
    Lexer lexer = Lexer(file);
    lexer.lex();
    auto x = lexer.getLexemesList();

    printLexResult(x);
    return 0;
}
