from collections import namedtuple

class Symbol(str):
    def __repr__(self):
        return 'Symbol(%s)' % self

class Parser:
    def __init__(self, tokenizer):
        self.tokenizer = tokenizer

    def parse(self):
        self.curr_token = None
        self.next_token = None
        self.consume()
        return self.parse_sequence()

    # sequence = expression*
    def parse_sequence(self):
        expressions = []
        while self.next_token:
            expressions.append(self.parse_expression())
        return expressions

    # expression = IDENT | STRING | INT | FLOAT | list
    def parse_expression(self):
        if self.accept('IDENT'):
            return Symbol(self.curr_token.value)
        elif self.accept('STRING'):
            return self.curr_token.value
        elif self.accept('INT'):
            return self.curr_token.value
        elif self.accept('FLOAT'):
            return self.curr_token.value
        else:
            return self.parse_list()

    # list = LPAREN expression* RPAREN
    def parse_list(self):
        self.expect('LPAREN')
        expressions = []
        while True:
            try:
                expressions.append(self.parse_expression())
            except ParseError:
                break
        self.expect('RPAREN')
        return expressions

    def accept(self, type):
        if self.next_token and self.next_token.type == type:
            self.consume()
            return True
        else:
            return False

    def expect(self, type):
        if not self.accept(type):
            if self.next_token:
                actual_type = self.next_token.type
                raise UnexpectedTokenError("Expected token %s (got %s)" % (type, actual_type))
            else:
                raise IncompleteParseError("Unexpected end-of-input")

    def consume(self):
        (self.curr_token, self.next_token) = (self.next_token, self.tokenizer.next())

class ParseError(RuntimeError):
    pass

class UnexpectedTokenError(ParseError):
    pass

class IncompleteParseError(ParseError):
    pass
