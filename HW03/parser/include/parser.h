#ifndef PARSERCPP_PARSER_H
#define PARSERCPP_PARSER_H

#include <string>

enum regexp_type {
    rEmpty,
    rEpsilon,
    rChar,
    rSequence,
    rAlternative,
    rStar
};

class Regexp {
public:
    explicit Regexp(regexp_type type) : _type(type) {};

    virtual ~Regexp() = default;

    regexp_type getType() const;

private:
    regexp_type _type;
};

bool isEq(const Regexp* fst, const Regexp* snd);

class Empty : public Regexp {
public:
    Empty() : Regexp(regexp_type::rEmpty) {}
};

class Epsilon : public Regexp {
public:
    Epsilon() : Regexp(regexp_type::rEpsilon) {}
};

class Char : public Regexp {
public:
    Char(char symbol) : Regexp(regexp_type::rChar), _symbol(symbol) {}

    char _symbol;
};

class Sequence : public Regexp {
public:
    Sequence(Regexp *p, Regexp *q) : Regexp(regexp_type::rSequence), _p(p), _q(q) {}

    Regexp *_p;
    Regexp *_q;
};

class Alternative : public Regexp {
public:
    Alternative(Regexp *p, Regexp *q) : Regexp(regexp_type::rAlternative), _p(p), _q(q) {}

    Regexp *_p;
    Regexp *_q;
};

class Star : public Regexp {
public:
    Star(Regexp *p) : Regexp(regexp_type::rStar), _p(p) {}

    Regexp *_p;
};

bool nullable(Regexp *regexp);

Regexp *make_alternative(Regexp *p, Regexp *q);

Regexp *make_sequence(Regexp *p, Regexp *q);

Regexp *make_star(Regexp *p);

Regexp *derivative(char symbol, Regexp *regexp);

bool match(Regexp *regexp, const std::string &needle);

#endif //PARSERCPP_PARSER_H
