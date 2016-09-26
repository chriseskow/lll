from collections import namedtuple
from re import compile

Token = namedtuple("Token", ("type", "string"))

class Tokenizer:
    REGEXES = [
        ("SPACE",   compile(r'\s+|#.*')),
        ("LPAREN",  compile(r'\(')),
        ("RPAREN",  compile(r'\)')),
        ("FLOAT",   compile(r'[+\-]?[0-9]+\.[0-9]+')),
        ("INT",     compile(r'[+\-]?[0-9]+')),
        ("IDENT",   compile(r'[A-Za-z0-9~!@$%^&*\-_=+|<>?]+'))
    ]

    def __init__(self, code):
        self.code = code

    def tokenize(self):
        tokens = []
        while self.code:
            token = self.next_token()
            self.code = self.code[len(token.string):]
            if token.type != "SPACE":
                tokens.append(token)
        tokens.append(Token("EOF", None))
        return tokens

    def next_token(self):
        for type, regex in self.REGEXES:
            match = regex.match(self.code)
            if match:
                return Token(type, match.group(0))
        raise TokenizeError("Don't know the token: %s" % repr(self.code))

class TokenizeError(RuntimeError):
    pass
