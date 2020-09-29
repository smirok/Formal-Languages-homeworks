#include <iostream>
#include <fstream>
#include <iterator>
//using namespace std;

std::string read_file(const std::string &file_name) {
    std::ifstream in = std::ifstream(file_name);
    return std::string((std::istreambuf_iterator<char>(in)),
                       std::istreambuf_iterator<char>());
}

int main() {
    std::string file_name;
    std::cin >> file_name;

    std::cout << read_file(file_name);
    return 0;
}
