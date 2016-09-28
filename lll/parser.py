from collections import namedtuple

Program = namedtuple("Program", ("expressions"))
List = namedtuple("List", ("items"))
Identifier = namedtuple("Identifier", ("name"))
String = namedtuple("String", ("value"))
Integer = namedtuple("Integer", ("value"))
Float = namedtuple("Float", ("value"))

class Parser:
    def __init__(self, tokenizer):
        self.tokenizer = tokenizer
        self.tokens = tokenizer.tokenize()

    def parse(self):
        return self.parse_program()

    # program = expression* EOF
    def parse_program(self):
        expressions = []
        while self.tokens:
            if self.accept("EOF"):
                break
            expressions.append(self.parse_expression())
        return Program(expressions)

    # expression = IDENT | STRING | INT | FLOAT | list
    def parse_expression(self):
        token = self.accept("IDENT")
        if token: return Identifier(token.string)

        token = self.accept("STRING")
        if token: return String(token.string)

        token = self.accept("INT")
        if token: return Integer(int(token.string))

        token = self.accept("FLOAT")
        if token: return Float(float(token.string))

        return self.parse_list()

    # list = LPAREN expression* RPAREN
    def parse_list(self):
        self.expect("LPAREN")
        expressions = []
        while True:
            try:
                expressions.append(self.parse_expression())
            except ParseError:
                break
        self.expect("RPAREN")
        return List(expressions)

    def accept(self, type):
        token = self.tokens[0]
        if token.type == type:
            self.tokens = self.tokens[1:]
            return token
        else:
            return None

    def expect(self, type):
        token = self.accept(type)
        if token:
            return token
        else:
            actual_type = self.tokens[0].type
            raise ParseError("Expected token %s (got %s)" % (type, actual_type))

class ParseError(RuntimeError):
    pass
