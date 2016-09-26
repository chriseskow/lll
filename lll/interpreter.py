from collections import namedtuple
from lll.parser import *

Builtin = namedtuple("Builtin", ("attr_name"))
Lambda = namedtuple("Lambda", ("params", "body"))

class Scope:
    def __init__(self, symbols={}, prev=None):
        self.symbols = symbols
        self.prev = prev

    def lookup(self, name):
        if name in self.symbols:
            return self.symbols[name]
        elif self.prev:
            return self.prev.lookup(name)
        else:
            raise RuntimeError("Undefined identifier: %s" % name)

    def define(self, name, value):
        self.symbols[name] = value

class Interpreter:
    BUILTINS = {
        "def": Builtin("builtin_def"),
        "lambda": Builtin("builtin_lambda"),
        "if": Builtin("builtin_if"),
        "print": Builtin("builtin_print"),
        "=": Builtin("builtin_eq"),
        "<": Builtin("builtin_lt"),
        ">": Builtin("builtin_gt"),
        "+": Builtin("builtin_add"),
        "-": Builtin("builtin_sub"),
        "*": Builtin("builtin_mul")
    }

    def __init__(self, program):
        self.program = program
        self.scope = Scope(self.BUILTINS)

    def execute(self):
        for expr in self.program.expressions:
            self.eval(expr)

    def eval(self, expr):
        if isinstance(expr, (String, Integer, Float)):
            return expr.value
        elif isinstance(expr, Identifier):
            return self.scope.lookup(expr.name)
        elif isinstance(expr, List):
            return self.call(expr.items)
        else:
            raise RuntimeError("[BUG] Invalid expression: %s" % repr(expr))

    def call(self, items):
        if not items:
            raise RuntimeError("Cannot call empty list")

        func = self.eval(items[0])
        raw_args = items[1:]

        if isinstance(func, Builtin):
            callable = getattr(self, func.attr_name)
            return callable(raw_args)
        elif isinstance(func, Lambda):
            args = self.eval_args(raw_args)
            if len(func.params) != len(args):
                raise RuntimeError("Wrong number of arguments (expected %d, got %d)" % (len(func.params), len(args)))
            locals = dict(zip(func.params, args))
            self.scope = Scope(locals, self.scope)
            retval = None
            for expr in func.body:
                retval = self.eval(expr)
            self.scope = self.scope.prev
            return retval
        else:
            raise RuntimeError("Cannot call non-function: %s" % repr(func))

    def eval_args(self, args):
        return [self.eval(arg) for arg in args]

    def builtin_def(self, args):
        if len(args) != 2:
            raise RuntimeError("def called with wrong number of arguments")
        if not isinstance(args[0], Identifier):
            raise RuntimeError("def called without an identifier as first argument")
        key = args[0].name
        value = self.eval(args[1])
        self.scope.define(key, value)
        return value

    def builtin_lambda(self, args):
        if len(args) < 2:
            raise RuntimeError("lambda called with wrong number of arguments")
        params = self.require_param_list(args[0])
        return Lambda(params, args[1:])

    def builtin_if(self, args):
        if len(args) != 3:
            raise RuntimeError("if requires 3 arguments")
        cond = self.eval(args[0])
        if (cond):
            return self.eval(args[1])
        else:
            return self.eval(args[2])

    def builtin_print(self, args):
        args = self.eval_args(args)
        for arg in args:
            if isinstance(arg, (str, int, long, float)):
                print(arg)
            elif isinstance(arg, Lambda):
                print("<lambda>")
            else:
                raise RuntimeError("[BUG] Don't know how to print: %s" % repr(arg))

    def builtin_eq(self, args):
        args = self.eval_args(args)
        self.require_nonempty_numeric_args(args)
        if len(args) == 1:
            raise RuntimeError("Need more than one argument")
        return int(args.count(args[0]) == len(args))

    def builtin_lt(self, args):
        if len(args) != 2:
            raise RuntimeError("Need two arguments")
        args = self.eval_args(args)
        self.require_nonempty_numeric_args(args)
        return int(args[0] < args[1])

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
