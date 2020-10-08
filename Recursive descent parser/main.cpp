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
    std::cout << "Lex results:\n";
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

int main(int argc, char* argv[]) {
    std::string file = read_file(argv[1]);
    Lexer lexer;
    if (!lexer.lex(file)) {
        std::cout << "Lexing error\n";
        return 0;
    }
    auto &x = lexer.getLexemesList();

    printLexResult(x);
    
    std::cout << "Parse result:\n";	
    Parser parser(x);
    if (parser.parse())
        std::cout << "OK";
    return 0;
}
