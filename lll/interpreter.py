from collections import namedtuple
from lll.parser import *

Lambda = namedtuple("Lambda", ("params", "body"))

class Interpreter:
    BUILTINS = {
        "def": "builtin_def",
        "lambda": "builtin_lambda",
        "if": "builtin_if",
        "print": "builtin_print",
        "=": "builtin_eq",
        "<": "builtin_lt",
        ">": "builtin_gt",
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

    def builtin_if(self, args):
        if len(args) != 3:
            raise RuntimeError("if requires 3 arguments")
        cond = self.eval_expression(args[0])
        if (cond):
            return self.eval_expression(args[1])
        else:
            return self.eval_expression(args[2])

    def builtin_print(self, args):
        args = self.eval_args(args)
        for arg in args:
            if isinstance(arg, (int, long, float)):
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
