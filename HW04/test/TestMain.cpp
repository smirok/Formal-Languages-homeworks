#define DOCTEST_CONFIG_IMPLEMENT_WITH_MAIN

#include "doctest.h"
#include "parser.h"

TEST_SUITE ("Lexer") {
    TEST_CASE ("EasyTrue") {
        Lexer lexer;
                CHECK_EQ(lexer.lex("f."), true);
                CHECK_EQ(lexer.lex("f :- g."), true);
                CHECK_EQ(lexer.lex("f :- g, h; t."), true);
                CHECK_EQ(lexer.lex("f :- g, (h; t)."), true);
    }

    TEST_CASE ("EasyFalse") {
        Lexer lexer;
                CHECK_EQ(lexer.lex(": -"), false);
                CHECK_EQ(lexer.lex("#"), false);
                CHECK_EQ(lexer.lex("f:"), false);
                CHECK_EQ(lexer.lex("trololo123 .;;-"), false);
    }

    TEST_CASE ("HardTrue") {
        Lexer lexer;
                CHECK_EQ(lexer.lex("f. \n f.\n:-:-:-"), true);
                CHECK_EQ(lexer.lex("f :- g. \n ;;;;......()"), true);
                CHECK_EQ(lexer.lex("f :- g, h; t. \n )))))) ..;;,,,"), true);
                CHECK_EQ(lexer.lex("f :- g, (h; t). \n\n\n\n           )"), true);
    }

    TEST_CASE ("HardFalse") {
        Lexer lexer;
                CHECK_EQ(lexer.lex(":-:-:-asdasdas123\n{"), false);
                CHECK_EQ(lexer.lex("......,,,,,,      1     \n  "), false);
                CHECK_EQ(lexer.lex("asd :- ..:-;;2"), false);
    }
}

TEST_SUITE ("Parser") {
    TEST_CASE ("EasyTrue") {
        Lexer lexer;
        {
            lexer.lex("f.");

            Parser parser(lexer.getLexemesList());
                    CHECK_EQ(parser.parse(), true);
        }
        {
            lexer.lex("f :- g.");
            Parser parser(lexer.getLexemesList());
                    CHECK_EQ(parser.parse(), true);
        }
        {
            lexer.lex("f :- g, h; t.");
            Parser parser(lexer.getLexemesList());
                    CHECK_EQ(parser.parse(), true);
        }
        {
            lexer.lex("f :- g, (h; t).");

            Parser parser(lexer.getLexemesList());
                    CHECK_EQ(parser.parse(), true);
        }
    }

    TEST_CASE ("EasyFalse") {
        Lexer lexer;
        {
            lexer.lex("f");

            Parser parser(lexer.getLexemesList());
                    CHECK_EQ(parser.parse(), false);
        }
        {
            lexer.lex(":- g.");
            Parser parser(lexer.getLexemesList());
                    CHECK_EQ(parser.parse(), false);
        }
        {
            lexer.lex("f :- .");
            Parser parser(lexer.getLexemesList());
                    CHECK_EQ(parser.parse(), false);
        }
        {
            lexer.lex("f :- g; h, .");

            Parser parser(lexer.getLexemesList());
                    CHECK_EQ(parser.parse(), false);
        }
        {
            lexer.lex("f :- (g; (h).");
            Parser parser(lexer.getLexemesList());
                    CHECK_EQ(parser.parse(), false);

        }
    }

    TEST_CASE ("HardTrue") {
        Lexer lexer;
        {
            lexer.lex("f\n.");

            Parser parser(lexer.getLexemesList());
                    CHECK_EQ(parser.parse(), true);
        }
        {
            lexer.lex("f\n :- g.\n");
            Parser parser(lexer.getLexemesList());
                    CHECK_EQ(parser.parse(), true);
        }
        {
            lexer.lex("f\n :- ((((g, (h; t)))))\n.");
            Parser parser(lexer.getLexemesList());
                    CHECK_EQ(parser.parse(), true);
        }
        {
            lexer.lex("f\n :-\n g\n, \n(\nh\n;\n t\n)\n.");

            Parser parser(lexer.getLexemesList());
                    CHECK_EQ(parser.parse(), true);
        }
    }

    TEST_CASE ("HardFalse") {
        Lexer lexer;
        {
            lexer.lex("f.\n f.\n g :- f. \n g");

            Parser parser(lexer.getLexemesList());
                    CHECK_EQ(parser.parse(), false);
        }
        {
            lexer.lex("g :- (g :- f.).");
            Parser parser(lexer.getLexemesList());
                    CHECK_EQ(parser.parse(), false);
        }
        {
            lexer.lex("f :- (((a,b),c),d),e)");
            Parser parser(lexer.getLexemesList());
                    CHECK_EQ(parser.parse(), false);
        }
        {
            lexer.lex("f :- g;\n h,t;\n .");

            Parser parser(lexer.getLexemesList());
                    CHECK_EQ(parser.parse(), false);
        }
        {
            lexer.lex("f :- (g; (h).");
            Parser parser(lexer.getLexemesList());
                    CHECK_EQ(parser.parse(), false);

        }
    }
}