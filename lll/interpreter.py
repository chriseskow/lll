from collections import namedtuple
from lll.parser import *

Operator = namedtuple("Operator", ("attr_name"))
Builtin = namedtuple("Builtin", ("attr_name", "required_args", "variable_args"))
Lambda = namedtuple("Lambda", ("params", "body", "env"))

class Env:
    def __init__(self, symbols={}, outer=None):
        self.symbols = symbols
        self.outer = outer

    def lookup(self, name):
        if name in self.symbols:
            return self.symbols[name]
        elif self.outer:
            return self.outer.lookup(name)
        else:
            raise RuntimeError("Undefined identifier: %s" % name)

    def define(self, name, value):
        self.symbols[name] = value

class Interpreter:
    GLOBAL_SYMBOLS = {
        "def": Operator("op_def"),
        "lambda": Operator("op_lambda"),
        "if": Operator("op_if"),
        "print": Builtin("builtin_print", 0, True),
        "=": Builtin("builtin_eq", 2, True),
        "<": Builtin("builtin_lt", 2, False),
        ">": Builtin("builtin_gt", 2, False),
        "+": Builtin("builtin_add", 1, True),
        "-": Builtin("builtin_sub", 1, True),
        "*": Builtin("builtin_mul", 1, True)
    }

    def __init__(self, program):
        self.program = program

    def execute(self):
        env = Env(self.GLOBAL_SYMBOLS)
        for expr in self.program.expressions:
            self.eval(expr, env)

    def eval(self, expr, env):
        if isinstance(expr, (String, Integer, Float)):
            return expr.value
        elif isinstance(expr, Identifier):
            return env.lookup(expr.name)
        elif isinstance(expr, List):
            return self.eval_list(expr.items, env)
        else:
            raise RuntimeError("[BUG] Invalid expression: %s" % repr(expr))

    def eval_list(self, items, env):
        if not items:
            raise RuntimeError("Cannot call empty list")

        func = self.eval(items[0], env)
        raw_args = items[1:]

        if isinstance(func, Operator):
            callable = getattr(self, func.attr_name)
            return callable(raw_args, env)
        elif isinstance(func, (Builtin, Lambda)):
            args = [self.eval(arg, env) for arg in raw_args]
            return self.apply(func, args)
        else:
            raise RuntimeError("Cannot call non-function: %s" % repr(func))

    def apply(self, func, args):
        if isinstance(func, Builtin):
            self.check_args(args, func.required_args, func.variable_args)
            callable = getattr(self, func.attr_name)
            return callable(*args)
        elif isinstance(func, Lambda):
            self.check_args(args, len(func.params), False)
            symbols = dict(zip(func.params, args))
            env = Env(symbols, func.env)
            retval = None
            for expr in func.body:
                retval = self.eval(expr, env)
            return retval

    def check_args(self, args, num_required, has_variable):
        num_args = len(args)
        if num_args < num_required:
            raise RuntimeError(
                "Too few arguments for builtin (min %d, but got %d)" %
                (num_required, num_args))
        if num_args > num_required and not has_variable:
            raise RuntimeError(
                "Too many arguments for builtin (max %d, but got %d)" %
                (num_required, num_args))

    def call(self, func, args):
        pass

    def op_def(self, args, env):
        if len(args) != 2:
            raise RuntimeError("def called with wrong number of arguments")
        (ident, value_expr) = args
        if not isinstance(ident, Identifier):
            raise RuntimeError("def called without an identifier as first argument")
        key = ident.name
        value = self.eval(value_expr, env)
        env.define(key, value)
        return value

    def op_lambda(self, args, env):
        if len(args) < 2:
            raise RuntimeError("lambda called with wrong number of arguments")
        params = self.require_param_list(args[0])
        return Lambda(params, args[1:], env)

    def op_if(self, args, env):
        if len(args) != 3:
            raise RuntimeError("if requires 3 arguments")
        (cond, then_expr, else_expr) = args
        return self.eval(then_expr if self.eval(cond, env) else else_expr, env)

    def builtin_print(self, *args):
        for arg in args:
            if isinstance(arg, (str, int, long, float)):
                print(arg)
            elif isinstance(arg, Lambda):
                print("<lambda>")
            else:
                raise RuntimeError("[BUG] Don't know how to print: %s" % repr(arg))

    def builtin_eq(self, *args):
        return int(args.count(args[0]) == len(args))

    def builtin_lt(self, x, y):
        return int(x < y)

    def builtin_add(self, *args):
        return sum(args)

    def builtin_sub(self, *args):
        return reduce(lambda sum, n: sum - n, args[1:], args[0])

    def builtin_mul(self, *args):
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
