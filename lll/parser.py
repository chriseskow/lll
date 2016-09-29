from collections import namedtuple

Program = namedtuple('Program', ('expressions'))
List = namedtuple('List', ('items'))
Identifier = namedtuple('Identifier', ('name'))
String = namedtuple('String', ('value'))
Integer = namedtuple('Integer', ('value'))
Float = namedtuple('Float', ('value'))

class Parser:
    def __init__(self, tokenizer):
        self.tokenizer = tokenizer

    def parse(self):
        self.curr_token = None
        self.next_token = None
        self.consume()
        return self.parse_program()

    # program = expression*
    def parse_program(self):
        expressions = []
        while self.next_token:
            expressions.append(self.parse_expression())
        return Program(expressions)

    # expression = IDENT | STRING | INT | FLOAT | list
    def parse_expression(self):
        if self.accept('IDENT'):
            return Identifier(self.curr_token.value)
        elif self.accept('STRING'):
            return String(self.curr_token.value)
        elif self.accept('INT'):
            return Integer(self.curr_token.value)
        elif self.accept('FLOAT'):
            return Float(self.curr_token.value)
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
        return List(expressions)

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
