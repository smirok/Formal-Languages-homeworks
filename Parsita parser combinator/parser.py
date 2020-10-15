import sys

from parsita import *


class Parser(TextParsers, whitespace=r'[ \n\t]*'):
    keyword_module = lit('module ') > (lambda x: 'MODULE')
    keyword_type = lit('type ') > (lambda x: 'TYPE_DEF')

    var = reg(r'[A-Z][a-zA-Z0-9_]*') > (lambda x: f'(VAR {x})')

    out_ident = (lambda x: f'(ID {x})')
    ident = pred(reg(r'[a-z_][a-zA-Z0-9_]*'), lambda x: x != 'module' and x != 'type', 'kek') > out_ident

    DOT = lit('.') > (lambda x: '')
    LIST_DIVIDER = lit('|') > (lambda x: '')
    OBR = lit('(') > (lambda x: '(')
    CBR = lit(')') > (lambda x: ')')
    LIST_OBR = lit('[') > (lambda x: '')
    LIST_CBR = lit(']') > (lambda x: '')
    CORKSCREW = lit(':-') > (lambda x: '')
    SEMICOLON = lit(';') > (lambda x: '')
    COMMA = lit(',') > (lambda x: '')
    RIGHTARROW = lit('->') > (lambda x: '')

    subatom = (OBR & subatom & CBR > (lambda x: f'{x[1]}')) | atom
    out_atom = lambda x: f'(ATOM {x[0]} {" ".join(list(x[1]))})' if x[1] != [] else f'(ATOM {x[0]})'
    atom = ident & rep(subatom | ident | var | LIST) > out_atom

    out_expr = (lambda x: ''.join(x))
    expression = (OBR >> disjunction << CBR) | (atom > out_expr)

    out_conj = (lambda x: f'(CONJ {" ".join(x)})' if len(x) != 1 else f'{x[0]}')
    conjunction = (rep1sep(expression, COMMA) > out_conj)
    out_disj = (lambda x: f'(DISJ {" ".join(x)})' if len(x) != 1 else f'{x[0]}')
    disjunction = (rep1sep(conjunction, SEMICOLON) > out_disj)

    out_definition = (lambda x: f'(DEF {x[0][0]} {x[0][2]})' if len(x[0]) == 3 else f'(DEF {x[0]})')
    definition = ((atom & CORKSCREW & disjunction | atom) & DOT) > out_definition

    type_item = ((atom | var | ident) > (lambda x: f'{x}')) | (OBR >> type_item << CBR) | (
            (OBR >> local_t_sequence << CBR) > (lambda x: f'(TYPE {" ".join(x)})'))
    local_t_sequence = rep1sep(type_item, RIGHTARROW) > (lambda x: x)
    type_sequence = ((type_item & RIGHTARROW & type_sequence) > (lambda x: f'(TYPE {x[0]} {x[2]})')) | type_item
    type_def = (keyword_type & ident & type_sequence & DOT) > (lambda x: f'({x[0]} {x[1]} {" ".join(x[2:-1])})')

    module_output = (lambda x: f'({x[0]} {x[1]})')
    module = keyword_module & ident & DOT > module_output

    usual_list = (LIST_OBR & repsep(atom | var | LIST, COMMA) & LIST_CBR) > (
        lambda x: cons_fold(x[1][::-1]) if x[1] != [] else f'(nil)')
    haskell_list = (LIST_OBR & (atom | var | LIST) &
                    LIST_DIVIDER & (var | LIST) & LIST_CBR) > (lambda x: f'(cons {x[1]} {x[3]})')

    LIST = usual_list | haskell_list

    program = (module & rep(type_def) & rep(definition)) > (
        lambda x: x[0] + "!" + "!".join(x[1]) + "!" + "!".join(x[2]))


def cons_fold(list_):
    result = 'nil'
    for i in range(len(list_)):
        result = f'(cons {list_[i]} {result})'
    return result


def step(file_name: str, mode: str):
    input_file = open(file_name, 'r')
    text = input_file.read()
    output_file = open(file_name + '.out', 'w')
    if mode == '--atom':
        lines = str(Parser.atom.parse(text))[9:-2].split('!')
    elif mode == '--typeexpr':
        lines = str(Parser.type_sequence.parse(text))[9:-2].split('!')
    elif mode == '--type':
        lines = str(Parser.type_def.parse(text))[9:-2].split('!')
    elif mode == '--module':
        lines = str(Parser.module.parse(text))[9:-2].split('!')
    elif mode == '--relation':
        lines = str(Parser.definition.parse(text))[9:-2].split('!')
    elif mode == '--list':
        lines = str(Parser.LIST.parse(text))[9:-2].split('!')
    elif mode == '--disj':
        lines = str(Parser.disjunction.parse(text))[9:-2].split('!')
    else:
        lines = str(Parser.program.parse(text))[9:-2].split('!')

    for line in lines:
        output_file.write(line + '\n')


if __name__ == '__main__':
    step(sys.argv[1], sys.argv[2])
