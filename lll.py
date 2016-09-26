#!/usr/bin/env python

from sys import argv
from collections import namedtuple
import re

###############################################################################

Token = namedtuple("Token", ("type", "string"))

class Tokenizer:
    REGEXES = [
        ("SPACE",   re.compile(r'\s+|#.*')),
        ("LPAREN",  re.compile(r'\(')),
        ("RPAREN",  re.compile(r'\)')),
        ("FLOAT",   re.compile(r'[+\-]?[0-9]+\.[0-9]+')),
        ("INT",     re.compile(r'[+\-]?[0-9]+')),
        ("IDENT",   re.compile(r'[A-Za-z0-9~!@$%^&*\-_=+|<>?]*'))
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

###############################################################################

Program = namedtuple("Program", ("expressions"))
List = namedtuple("List", ("items"))
Identifier = namedtuple("Identifier", ("name"))
Integer = namedtuple("Integer", ("value"))
Float = namedtuple("Float", ("value"))

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens

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

    # expression = IDENT | INT | FLOAT | list
    def parse_expression(self):
        token = self.accept("IDENT")
        if token: return Identifier(token.string)

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

###############################################################################

Lambda = namedtuple("Lambda", ("params", "body"))

class Interpreter:
    BUILTINS = {
        "def": "builtin_def",
        "lambda": "builtin_lambda",
        "print": "builtin_print",
        "+": "builtin_add",
        "-": "builtin_sub",
        "*": "builtin_mul"
    }

    def __init__(self, program):
        self.program = program
        self.symbol_table = {}

    def execute(self):
        for expression in self.program.expressions:
            self.eval_expression(expression)

    def eval_expression(self, expression):
        if isinstance(expression, Integer):
            return expression.value
        elif isinstance(expression, Float):
            return expression.value
        elif isinstance(expression, Identifier):
            if expression.name in self.symbol_table:
                return self.symbol_table[expression.name]
            else:
                raise RuntimeError("Undefined identifier: %s" % expression.name)
        elif isinstance(expression, List):
            return self.eval_list(expression.items)
        else:
            raise RuntimeError("[BUG] Don't know how to evaluate: %s" % repr(expression))

    def eval_list(self, items):
        if not items:
            raise RuntimeError("Tried to call an empty list")
        first = items[0]
        if not isinstance(first, Identifier):
            raise RuntimeError("Tried to call non-function")
        return self.call_func(first.name, items[1:])

    def call_func(self, name, args):
        if name in self.BUILTINS:
            func = getattr(self, self.BUILTINS[name])
            return func(args)
        elif name in self.symbol_table:
            func = self.symbol_table[name];
            if not isinstance(func, Lambda):
                raise RuntimeError("Trying to call non-function")
            args = self.eval_args(args)
            if len(func.params) != len(args):
                raise RuntimeError("Wrong number of arguments (expected %d, got %d)" % (len(func.params), len(args)))
            for i, param in enumerate(func.params):
                self.define_var(param, args[i])
            retval = None
            for expr in func.body:
                retval = self.eval_expression(expr)
            return retval
        else:
            raise RuntimeError("Calling undefined method: %s" % name)

    def eval_args(self, args):
        return [self.eval_expression(arg) for arg in args]

    def define_var(self, name, value):
        self.symbol_table[name] = value

    def builtin_def(self, args):
        if len(args) != 2:
            raise RuntimeError("def called with wrong number of arguments")
        if not isinstance(args[0], Identifier):
            raise RuntimeError("def called without an identifier as first argument")
        key = args[0].name
        value = self.eval_expression(args[1])
        self.define_var(key, value)
        return value

    def builtin_lambda(self, args):
        if len(args) < 2:
            raise RuntimeError("lambda called with wrong number of arguments")
        params = self.require_param_list(args[0])
        return Lambda(params, args[1:])

    def builtin_print(self, args):
        args = self.eval_args(args)
        for arg in args:
            if isinstance(arg, (int, long, float)):
                print(arg)
            elif isinstance(arg, Lambda):
                print("<lambda>")
            else:
                raise RuntimeError("[BUG] Don't know how to print: %s" % repr(arg))

    def builtin_add(self, args):
        args = self.eval_args(args)
        self.require_nonempty_numeric_args(args)
        return reduce(lambda sum, n: sum + n, args, 0)

    def builtin_sub(self, args):
        args = self.eval_args(args)
        self.require_nonempty_numeric_args(args)
        return reduce(lambda sum, n: sum - n, args[1:], args[0])

    def builtin_mul(self, args):
        args = self.eval_args(args)
        self.require_nonempty_numeric_args(args)
        return reduce(lambda product, n: product * n, args, 1)

    def require_param_list(self, list):
        if not isinstance(list, List):
            raise RuntimeError("lambda called without argument list")
        params = []
        for item in list.items:
            if not isinstance(item, Identifier):
                raise RuntimeError("lambda called with non-identifier param")
            params.append(item.name)
        return params

    def require_nonempty_numeric_args(self, args):
        if not args:
            raise RuntimeError("Argument list is empty")
        if any([type(arg) not in (int, long, float) for arg in args]):
            raise RuntimeError("Need numeric arguments")

###############################################################################

def main():
    if len(argv) != 2:
        raise RuntimeError("Usage: %s [filename]", argv[0])

    code = open(argv[1]).read()
    tokenizer = Tokenizer(code)
    tokens = tokenizer.tokenize()
    parser = Parser(tokens)
    program = parser.parse()
    interpreter = Interpreter(program)
    interpreter.execute()

if __name__ == "__main__":
    main()
