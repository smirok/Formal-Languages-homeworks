#include <iostream>
#include "parser.h"

int main() {
    Regexp *r = new Sequence(new Star(new Char('a')), new Char('a'));
    std::cout << "Enter string to match with (a*)a\n";

    std::string s;
    std::cin >> s;

    if (match(r,s))
        std::cout << "True\n";
    else
        std::cout << "False\n";
    return 0;
}
