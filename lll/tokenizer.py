from collections import namedtuple
from re import compile, sub

Token = namedtuple("Token", ("type", "string", "len"))

class Tokenizer:
    REGEXES = [
        ("SPACE",   compile(r'\s+|;.*')),
        ("LPAREN",  compile(r'\(')),
        ("RPAREN",  compile(r'\)')),
        ("FLOAT",   compile(r'[+\-]?[0-9]+\.[0-9]+')),
        ("INT",     compile(r'[+\-]?[0-9]+')),
        ("IDENT",   compile(r'[A-Za-z0-9~!@$%^&*\-_=+|<>?]+')),
        ("STRING",  compile(r'"(\\"|[^"])*"'))
    ]

    ESCAPE_SEQUENCES = (
        (r'\n', '\n'),
        (r'\t', '\t'),
        (r'\\', '\\'),
        (r'\"', '"')
    )

    def __init__(self, code):
        self.code = code

    def tokenize(self):
        tokens = []
        while self.code:
            token = self.next_token()
            self.code = self.code[token.len:]
            if token.type != "SPACE":
                tokens.append(token)
        tokens.append(Token("EOF", None, 0))
        return tokens

    def next_token(self):
        for type, regex in self.REGEXES:
            match = regex.match(self.code)
            if match:
                string = match.group(0)
                strlen = len(string)
                if type == "STRING":
                    string = self.tokenize_string(string)
                return Token(type, string, strlen)
        raise TokenizeError("Don't know the token: %s" % repr(self.code))

    def tokenize_string(self, string):
        string = string[1:-1]
        for sequence, replacement in self.ESCAPE_SEQUENCES:
            string = string.replace(sequence, replacement)
        return string

class TokenizeError(RuntimeError):
    pass
