import sys
import ply.yacc as yacc

from abstractSyntaxTree import *
from lexer import *

root = None


def p_definition(p):
    """definition : atom CORKSCREW disjunction DOT
                  | atom DOT"""
    if len(p) == 3:
        p[0] = Node('DEFINITION', [p[1], Node('.')])
    else:
        p[0] = Node('DEFINITION', [p[1], Node(':-'), p[3], Node('.')])
    global root
    root = p[0]


def p_disjunction(p):
    """disjunction : conjunction
                   | conjunction SEMICOLON disjunction"""
    if len(p) == 2:
        p[0] = Node('DISJ', [p[1]])
    else:
        p[0] = Node('DISJ', [p[1], p[3]])


def p_conjunction(p):
    """conjunction : expression
                   | expression COMMA conjunction"""
    if len(p) == 2:
        p[0] = Node('CONJ', [p[1]])
    else:
        p[0] = Node('CONJ', [p[1], p[3]])


def p_expression(p):
    """expression : atom
                  | OPEN_BRACKET disjunction CLOSE_BRACKET"""
    if len(p) == 2:
        p[0] = Node('EXPRESSION', [p[1]])
    else:
        p[0] = Node('EXPRESSION', [Node('OBR'),
                                   p[2],
                                   Node('CBR')])


def p_atom(p):
    """atom : ID
            | ID atom
            | ID OPEN_BRACKET inneratom CLOSE_BRACKET inneratom
            | ID OPEN_BRACKET inneratom CLOSE_BRACKET"""
    if len(p) == 2:
        p[0] = Node('ATOM', [Node(f'ID {p[1]}')])
    if len(p) == 3:
        p[0] = Node('ATOM', [Node(f'ID {p[1]}'), p[2]])
    if len(p) == 5:
        p[0] = Node('ATOM', [Node(f'ID {p[1]}'),
                             Node('OBR'),
                             p[3], Node('CBR')])
    if len(p) == 6:
        p[0] = Node('ATOM', [Node(f'ID {p[1]}'),
                             Node('OBR'),
                             p[3], Node('CBR'), p[5]])


def p_inneratom(p):
    """inneratom : ID
                 | ID inneratom
                 | OPEN_BRACKET inneratom CLOSE_BRACKET
                 | OPEN_BRACKET inneratom CLOSE_BRACKET inneratom"""
    if len(p) == 2:
        p[0] = Node('ATOM', [Node(f'ID {p[1]}')])
    if len(p) == 3:
        p[0] = Node('ATOM', [Node(f'ID {p[1]}'), p[2]])
    if len(p) == 4:
        p[0] = Node('ATOM', [Node('OBR'),
                             p[2],
                             Node('CBR')])
    if len(p) == 5:
        p[0] = Node('ATOM', [Node('OBR'),
                             p[2],
                             Node('CBR'), p[4]])


def p_error(p):
    raise SyntaxError(p)


def step(input_file):
    text = open(input_file, 'r').read()
    definition_list = text.split('.')
    output_file = open(f'{input_file}.out', 'w')
    for i in range(len(definition_list) - 1):
        definition_list[i] = definition_list[i] + '.'
    if definition_list[-1].count('\n') + definition_list[-1].count(' ') == len(definition_list[-1]):
        definition_list.pop()

    for definition in definition_list:
        try:
            parser.parse(definition)
        except SyntaxError as e:
            output_file.close()
            output_file = open(f'{input_file}.out', 'w')
            p = e.args[0]
            if p:
                output_file.write(f'Syntax error at {p.value} by type {p.type}\n'
                                  f'Parser position : line:{p.lineno}, col:{token_column(string=definition, token=p)}')
            else:
                output_file.write("Syntax error at EOF")
            return
        traverse(output_file, root, '')


parser = yacc.yacc(start="definition")

if __name__ == '__main__':
    try:
        step(f'{sys.argv[1]}')
    except Exception as e:
        print(e.args[0])
