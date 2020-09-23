import ply.lex as lex
import sys

reserved = {
    'module': 'MODULE',
    'sig': 'SIG',
    'type': 'TYPE'
}

operators = {
    '->': 'ARGUMENTS_CONVEYOR',
    ':-': 'DEFINITION_OP'
}

delimeters = {
    ',': 'COMMA',
    '.': 'DOT',
    '[': 'OPEN_LIST_BRACKET',
    ']': 'CLOSE_LIST_BRACKET',
    '|': 'PIPE'
}

tokens = [
             'NUM',
             'ID',
             'STRING_LITERAL'
         ] + list(reserved.values()) + list(operators.values()) + list(delimeters.values())

t_STRING_LITERAL = r'"[^"]*"'


def t_delimeters(t):
    r'[\.\,\[\]\|]'
    t.type = delimeters.get(t.value)
    return t


def t_operators(t):
    r'->|:-'
    t.type = operators.get(t.value)
    return t


def t_ID(t):
    r'[A-Za-z_][A-Za-z_0-9]*'
    t.type = reserved.get(t.value, 'ID')
    return t


def t_NUM(t):
    r'[0-9]+'
    t.value = int(t.value)
    return t


t_ignore = ' \t'


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def t_error(t):
    print(f'Illegal character {t.value[0]}')
    t.lexer.skip(1)


def token_column(string: str, token) -> int:
    line_start = string.rfind('\n', 0, token.lexpos) + 1
    return token.lexpos - line_start


lexer = lex.lex()

input_file = open(sys.argv[1], 'r')
text = input_file.read()

lexer.input(text)

output_file = open(f'{input_file.name}.out', 'w')

while True:
    tok = lexer.token()
    if not tok:
        break
    output_file.write(
        f'LexToken : (TOKEN:{tok.type}),({tok.value}),(line:{tok.lineno}),(col:{token_column(string=text, token=tok)})\n')

output_file.close()
