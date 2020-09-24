#include "benchmark/include/benchmark/benchmark.h"
#include "parser.h"

static void BM_BAD_REGEXP(benchmark::State &state) {
    Regexp *star_A = new Star(
            new Alternative(new Char('a'), new Alternative(new Char('a'), new Char('a')))
    );
    Regexp *b = new Char('b');
    Regexp *star_C = new Star(
            new Alternative(new Char('c'), new Alternative(new Char('c'), new Char('c')))
    );

    std::string s = "aaaaaaaaaaaaabcccccccccccccccccc";

    for (auto _ : state)
        match(new Sequence(star_A, new Sequence(b, star_C)), s);
}


static void BM_OPTIMAL_REGEXP(benchmark::State &state) {
    Regexp *star_A = new Star(new Char('a'));
    Regexp *b = new Char('b');
    Regexp *star_C = new Star(new Char('c'));

    std::string s = "aaaaaaaaaaaaabcccccccccccccccccc";
    for (auto _ : state) {
        match(new Sequence(star_A, new Sequence(b, star_C)), s);
    }
}

static void BM_OPTIMAL_REGEXP_LONG_TEXT(benchmark::State &state) {
    Regexp *star_A = new Star(new Char('a'));
    Regexp *b = new Char('b');
    Regexp *star_C = new Star(new Char('c'));

    std::string s;
    for (int i = 0; i < 5e6; ++i)
        s.push_back('a');
    s.push_back('b');
    for (int i = 0; i < 5e6; ++i)
        s.push_back('c');


    for (auto _ : state) {
        match(new Sequence(star_A, new Sequence(b, star_C)), s);
    }
}

static void BM_BAD_REGEXP_LONG_TEXT(benchmark::State &state) {
    Regexp *star_A = new Star(
            new Alternative(new Char('a'), new Alternative(new Char('a'), new Char('a')))
    );
    Regexp *b = new Char('b');
    Regexp *star_C = new Star(
            new Alternative(new Char('c'), new Alternative(new Char('c'), new Char('c')))
    );

    std::string s;
    for (int i = 0; i < 5e6; ++i)
        s.push_back('a');
    s.push_back('b');
    for (int i = 0; i < 5e6; ++i)
        s.push_back('c');

    for (auto _ : state) {
        match(new Sequence(star_A, new Sequence(b, star_C)), s);
    }
}

static void BM_SAMPLE_FROM_PRACTICE(benchmark::State &state) {
    Regexp *r = new Sequence(new Star(new Char('a')), new Char('a'));

    std::string s;
    for (int i = 0; i < 1e6; ++i)
        s.push_back('a');

    for (auto _ : state) {
        match(r, s);
    }
}

BENCHMARK(BM_OPTIMAL_REGEXP)->Unit(benchmark::kMillisecond);
BENCHMARK(BM_BAD_REGEXP)->Unit(benchmark::kMillisecond);
BENCHMARK(BM_OPTIMAL_REGEXP_LONG_TEXT)->Unit(benchmark::kMillisecond);
BENCHMARK(BM_BAD_REGEXP_LONG_TEXT)->Unit(benchmark::kMillisecond);
BENCHMARK(BM_SAMPLE_FROM_PRACTICE)->Unit(benchmark::kMillisecond);

BENCHMARK_MAIN();