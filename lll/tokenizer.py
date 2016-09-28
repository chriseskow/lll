from collections import namedtuple
from re import compile, sub

Token = namedtuple('Token', ('type', 'value'))

class Tokenizer:
    REGEXES = [
        ('SPACE',   compile(r'\s+|;.*')),
        ('LPAREN',  compile(r'\(')),
        ('RPAREN',  compile(r'\)')),
        ('FLOAT',   compile(r'[+\-]?[0-9]+\.[0-9]+')),
        ('INT',     compile(r'[+\-]?[0-9]+')),
        ('IDENT',   compile(r'[A-Za-z0-9~!@$%^&*\-_=+|<>?]+')),
        ('STRING',  compile(r'"(\\"|[^"])*"'))
    ]

    ESCAPE_SEQUENCES = (
        (r'\n', '\n'),
        (r'\t', '\t'),
        (r'\\', '\\'),
        (r'\"', '"')
    )

    def __init__(self, code):
        self.code = code

    def next(self):
        while self.code:
            for type, regex in self.REGEXES:
                match = regex.match(self.code)
                if match:
                    string = match.group(0)
                    value = self.eval(type, string)
                    token = Token(type, value)
                    self.code = self.code[len(string):]
                    break
            if not token:
                raise TokenizeError("Don't know the token: %s" % repr(self.code))
            if token.type != 'SPACE':
                return token
        return None

    def eval(self, type, string):
        if type == 'STRING':
            string = string[1:-1] # Remove quotes
            for sequence, replacement in self.ESCAPE_SEQUENCES:
                string = string.replace(sequence, replacement)
            return string
        elif type == 'INT':
            return int(string)
        elif type == 'FLOAT':
            return float(string)
        else:
            return string

class TokenizeError(RuntimeError):
    pass
