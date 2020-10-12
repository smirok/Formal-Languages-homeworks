import ply.lex as lex

tokens = [
    'ID',
    'DOT',
    'CLOSE_BRACKET',
    'OPEN_BRACKET',
    'COMMA',
    'SEMICOLON',
    'CORKSCREW'
]

t_ID = r'[A-Za-z_][A-Za-z_0-9]*'
t_DOT = r'\.'
t_CLOSE_BRACKET = r'\)'
t_OPEN_BRACKET = r'\('
t_COMMA = r','
t_SEMICOLON = r';'
t_CORKSCREW = r':-'

t_ignore = ' \t'


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def t_error(t):
    print(f'Illegal character {t.value[0]}')
    raise Exception("Lexing error")


def token_column(string: str, token) -> int:
    line_start = string.rfind('\n', 0, token.lexpos) + 1
    return token.lexpos - line_start


lexer = lex.lex()
