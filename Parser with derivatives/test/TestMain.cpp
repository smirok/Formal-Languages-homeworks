#define DOCTEST_CONFIG_IMPLEMENT_WITH_MAIN

#include "doctest.h"
#include "parser.h"

TEST_SUITE ("Char") {
    TEST_CASE ("Char") {
        Regexp *r = new Char('a');
        std::string s = "a";
                CHECK_EQ(match(r, s), true);
    }

    TEST_CASE ("Char") {
        Regexp *r = new Char('a');
        std::string s = "b";
                CHECK_EQ(match(r, s), false);
    }

    TEST_CASE ("Char") {
        Regexp *r = new Char('a');
        std::string s = "aa";
                CHECK_EQ(match(r, s), false);
    }

    TEST_CASE ("Char") {
        Regexp *r = new Char('a');
        std::string s;
                CHECK_EQ(match(r, s), false);
    }
}

TEST_SUITE ("Epsilon") {
    TEST_CASE ("Epsilon") {
        Regexp *r = new Epsilon();
        std::string s = "ab";
                CHECK_EQ(match(r, s), false);
    }

    TEST_CASE ("Epsilon") {
        Regexp *r = new Epsilon();
        std::string s;
                CHECK_EQ(match(r, s), true);
    }
}

TEST_SUITE ("Empty") {
    TEST_CASE ("Empty") {
        Regexp *r = new Empty();
        std::string s;
                CHECK_EQ(match(r, s), false);
    }

    TEST_CASE ("Empty") {
        Regexp *r = new Empty();
        std::string s = "NOT EMPTY :)";
                CHECK_EQ(match(r, s), false);
    }
}

TEST_SUITE ("Alternative") {
    TEST_CASE ("Alternative") {
        Regexp *r = new Alternative(new Char('a'), new Char('b'));
        std::string s = "a";
                CHECK_EQ(match(r, s), true);
    }

    TEST_CASE ("Alternative") {
        Regexp *r = new Alternative(new Char('a'), new Char('b'));
        std::string s = "b";
                CHECK_EQ(match(r, s), true);
    }

    TEST_CASE ("Alternative") {
        Regexp *r = new Alternative(new Char('a'), new Char('b'));
        std::string s = "ab";
                CHECK_EQ(match(r, s), false);
    }

    TEST_CASE ("Alternative") {
        Regexp *r = new Alternative(new Char('a'), new Char('b'));
        std::string s = "c";
                CHECK_EQ(match(r, s), false);
    }
}

TEST_SUITE ("Sequence") {
    TEST_CASE ("Sequence") {
        Regexp *r = new Sequence(new Char('a'), new Char('b'));
        std::string s = "ab";
                CHECK_EQ(match(r, s), true);
    }

    TEST_CASE ("Sequence") {
        Regexp *r = new Sequence(new Char('c'), new Sequence(new Char('a'), new Char('b')));
        std::string s = "cab";
                CHECK_EQ(match(r, s), true);
    }

    TEST_CASE ("Sequence") {
        Regexp *r = new Sequence(new Char('a'), new Char('b'));
        std::string s = "a";
                CHECK_EQ(match(r, s), false);
    }

    TEST_CASE ("Sequence") {
        Regexp *r = new Sequence(new Char('a'), new Char('b'));
        std::string s = "abb";
                CHECK_EQ(match(r, s), false);
    }
}

TEST_SUITE ("Star") {
    TEST_CASE ("Star") {
        Regexp *r = new Star(new Char('a'));
        std::string s = "a";
                CHECK_EQ(match(r, s), true);
    }

    TEST_CASE ("Star") {
        Regexp *r = new Star(new Char('a'));
        std::string s = "aaaa";
                CHECK_EQ(match(r, s), true);
    }

    TEST_CASE ("Star") {
        Regexp *r = new Star(new Char('a'));
        std::string s = "aaaab";
                CHECK_EQ(match(r, s), false);
    }
}

TEST_SUITE ("Combinations") {
    TEST_CASE ("Comb#1") {
        Regexp *r = new Sequence(new Star(new Char('a')), new Char('a'));
        std::string s = "aa";
        match(r, s);
                CHECK_EQ(match(r, s), true);
    }

    TEST_CASE ("Comb#1") {
        Regexp *r = new Sequence(new Star(new Char('a')), new Char('a'));
        std::string s;
                CHECK_EQ(match(r, s), false);
    }

    TEST_CASE ("Comb#1") {
        Regexp *r = new Sequence(new Star(new Char('a')), new Char('a'));
        std::string s = "b";
                CHECK_EQ(match(r, s), false);
    }

    TEST_CASE ("Comb#1") {
        Regexp *r = new Sequence(new Star(new Char('a')), new Char('a'));
        std::string s = "aaaab";
                CHECK_EQ(match(r, s), false);
    }

    TEST_CASE ("Comb#2") {
        Regexp *a = new Alternative(new Char('b'), new Char('c'));
        Regexp *r = new Sequence(new Char('a'), new Sequence(a, new Char('d')));
        std::string s = "abd";
                CHECK_EQ(match(r, s), true);
    }

    TEST_CASE ("Comb#2") {
        Regexp *a = new Alternative(new Char('b'), new Char('c'));
        Regexp *r = new Sequence(new Char('a'), new Sequence(a, new Char('d')));
        std::string s = "acd";
                CHECK_EQ(match(r, s), true);
    }

    TEST_CASE ("Comb#2") {
        Regexp *a = new Alternative(new Char('b'), new Char('c'));
        Regexp *r = new Sequence(new Char('a'), new Sequence(a, new Char('d')));
        std::string s = "abcd";
                CHECK_EQ(match(r, s), false);
    }

    TEST_CASE ("Comb#3") {
        Regexp *r = new Alternative(new Char('a'), new Char('a'));
        std::string s = "a";
                CHECK_EQ(match(r, s), true);
    }

    TEST_CASE ("Comb#3") {
        Regexp *r = new Alternative(new Char('a'), new Char('a'));
        std::string s = "aaa";
                CHECK_EQ(match(r, s), false);
    }
}