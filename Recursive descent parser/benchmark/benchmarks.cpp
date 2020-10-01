#include "benchmark/include/benchmark/benchmark.h"
#include "parser.h"

static void BM_SMALL_PROGRAM(benchmark::State &state) {
    Lexer lexer;
    std::string s = "f :- (g, h); t.\n";
    for (int i = 0; i < 10; ++i) {
        s += s;
    }

    lexer.lex(s);
    for (auto _ : state) {
        Parser parser(lexer.getLexemesList());
        parser.parse();
    }
}


static void BM_BIG_PROGRAM(benchmark::State &state) {
    Lexer lexer;
    std::string s = "f :- (g, h); t.\n";
    for (int i = 0; i < 20; ++i) {
        s += s;
    }

    lexer.lex(s);

    for (auto _ : state) {
        Parser parser(lexer.getLexemesList());
        parser.parse();
    }
}

BENCHMARK(BM_SMALL_PROGRAM)->Unit(benchmark::kMillisecond);
BENCHMARK(BM_BIG_PROGRAM)->Unit(benchmark::kMillisecond);

BENCHMARK_MAIN();