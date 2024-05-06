import re
import collections

Token = collections.namedtuple('Token', ['type', 'value', 'line', 'column'])

token_specification = [
    ('NUMBER',      r'\d+(\.\d*)?'),         # Integer or decimal number
    ('STRING',      r'"[^"]*"'),             # String literals
    ('COMMENT',     r'//[^\n]*'),            # Single-line comments
    ('PRINT',       r'\bprint\b'),           # print keyword
    ('IF',          r'\bif\b'),              # if keyword
    ('ELSE',        r'\belse\b'),            # else keyword
    ('ASSIGN',      r'='),                   # Assignment operator
    ('END',         r';'),                   # Statement terminator
    ('ID',          r'[A-Za-z_][A-Za-z0-9_]*'),  # Identifiers
    ('OP',          r'[+\-*/]'),             # Arithmetic operators
    ('COMPARE',     r'==|!=|<=|>=|>|<'),     # Comparison operators
    ('LPAREN',      r'\('),                  # Left Parenthesis
    ('RPAREN',      r'\)'),                  # Right Parenthesis
    ('LBRACE',      r'\{'),                  # Left Curly Brace
    ('RBRACE',      r'\}'),                  # Right Curly Brace
    ('NEWLINE',     r'\n'),                  # Line endings
    ('SKIP',        r'[ \t]+'),              # Skip over spaces and tabs
    ('MISMATCH',    r'.'),                   # Any other character
]



def tokenize(code):
    linestart = 0
    line = 1
    token_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)
    for mo in re.finditer(token_regex, code):
        kind = mo.lastgroup
        value = mo.group()
        column = mo.start() - linestart
        if kind == 'NEWLINE':
            linestart = mo.end()
            line += 1
        elif kind in ['SKIP', 'COMMENT']:
            continue  # Skip whitespace and comments
        elif kind == 'MISMATCH':
            raise RuntimeError(f'{line}:{column}: Illegal character {value!r}')
        else:
            if kind == 'NUMBER':
                value = float(value) if '.' in value else int(value)
            yield Token(kind, value, line, column)

