#include "parser.h"

regexp_type Regexp::getType() const {
    return _type;
}

bool isEq(Regexp *fst, Regexp *snd) {
    if (fst->getType() != snd->getType()) {
        return false;
    } else {
        if (fst->getType() == regexp_type::rEmpty || fst->getType() == regexp_type::rEpsilon)
            return true;
        if (fst->getType() == regexp_type::rChar) {
            auto fst_char = dynamic_cast<Char *>(fst);
            auto snd_char = dynamic_cast<Char *>(snd);
            return fst_char->_symbol == snd_char->_symbol;
        }
        if (fst->getType() == regexp_type::rSequence) {
            auto fst_seq = dynamic_cast<Sequence *>(fst);
            auto snd_seq = dynamic_cast<Sequence *>(snd);
            return isEq(fst_seq->_p, snd_seq->_p) && isEq(fst_seq->_q, snd_seq->_q);
        }
        if (fst->getType() == regexp_type::rAlternative) {
            auto fst_alt = dynamic_cast<Alternative *>(fst);
            auto snd_alt = dynamic_cast<Alternative *>(snd);
            return isEq(fst_alt->_p, snd_alt->_p) && isEq(fst_alt->_q, snd_alt->_q);
        }
        if (fst->getType() == regexp_type::rStar) {
            auto fst_star = dynamic_cast<Star *>(fst);
            auto snd_star = dynamic_cast<Star *>(snd);
            return isEq(fst_star->_p, snd_star->_p);
        }
        return false;
    }
}

bool nullable(Regexp *regexp) {
    if (regexp->getType() == regexp_type::rEmpty)
        return false;
    if (regexp->getType() == regexp_type::rEpsilon)
        return true;
    if (regexp->getType() == regexp_type::rChar)
        return false;
    if (regexp->getType() == regexp_type::rAlternative) {
        auto alt = dynamic_cast<Alternative *>(regexp);
        return nullable(alt->_q) || nullable(alt->_p);
    }
    if (regexp->getType() == regexp_type::rSequence) {
        auto seq = dynamic_cast<Sequence *>(regexp);
        return nullable(seq->_p) && nullable(seq->_q);
    }
    if (regexp->getType() == regexp_type::rStar) {
        return true;
    }
    return false;
}

Regexp *make_alternative(Regexp *p, Regexp *q) {
    if (p->getType() == regexp_type::rEmpty)
        return q;
    if (q->getType() == regexp_type::rEmpty)
        return p;
    if (p->getType() == regexp_type::rEpsilon) {
        if (nullable(q))
            return q;
        else
            return new Alternative(p, q);
    }
    if (q->getType() == regexp_type::rEpsilon) {
        if (nullable(p))
            return p;
        else
            return new Alternative(q, p);
    }
    if (isEq(p, q))
        return p;
    return new Alternative(p, q);
}

Regexp *make_sequence(Regexp *p, Regexp *q) {
    if (p->getType() == regexp_type::rEmpty)
        return p;
    if (q->getType() == regexp_type::rEmpty)
        return q;
    if (p->getType() == regexp_type::rEpsilon)
        return q;
    if (q->getType() == regexp_type::rEpsilon)
        return p;
    return new Sequence(p, q);
}

Regexp *make_star(Regexp *p) {
    if (p->getType() == regexp_type::rEmpty)
        return new Epsilon();
    if (p->getType() == regexp_type::rEpsilon)
        return p;
    if (p->getType() == regexp_type::rStar)
        return p;
    return new Star(p);
}

Regexp *derivative(char symbol, Regexp *regexp) {
    if (regexp->getType() == regexp_type::rEmpty)
        return new Empty();
    if (regexp->getType() == regexp_type::rEpsilon)
        return new Empty();
    if (regexp->getType() == regexp_type::rChar) {
        auto ch = dynamic_cast<Char *>(regexp);
        if (symbol == ch->_symbol)
            return new Epsilon();
        else
            return new Empty();
    }
    if (regexp->getType() == regexp_type::rSequence) {
        auto seq = dynamic_cast<Sequence *>(regexp);
        if (nullable(seq->_p))
            return make_alternative(make_sequence(derivative(symbol, seq->_p), seq->_q), derivative(symbol, seq->_q));
        else
            return make_sequence(derivative(symbol, seq->_p), seq->_q);
    }
    if (regexp->getType() == regexp_type::rAlternative) {
        auto alt = dynamic_cast<Alternative *>(regexp);
        return make_alternative(derivative(symbol, alt->_p), derivative(symbol, alt->_q));
    }
    if (regexp->getType() == regexp_type::rStar) {
        auto seq = dynamic_cast<Star *>(regexp);
        return make_sequence(derivative(symbol, seq->_p), make_star(seq->_p));
    }
    return new Empty();
}

bool match(Regexp *regexp, const std::string &needle) {
    for (int i = 0; i < needle.size(); ++i) {
        regexp = derivative(needle[i], regexp);
    }
    return nullable(regexp);
}
