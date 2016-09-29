import os
from collections import namedtuple
from lll.tokenizer import Source, Tokenizer
from lll.parser import Parser, Symbol

Operator = namedtuple('Operator', ('attr_name'))
Builtin = namedtuple('Builtin', ('func', 'required_args', 'variable_args'))
Lambda = namedtuple('Lambda', ('params', 'body', 'env'))

# TODO: this needs to be below above classes due to circular dependency
import lll.builtins as builtins

class Env:
    PRIMITIVES = {
        'quote': Operator('op_quote'),
        'def': Operator('op_def'),
        'lambda': Operator('op_lambda'),
        'if': Operator('op_if'),
        'load': Operator('op_load'),
        'load-paths': ['.'],
        'type': Builtin(builtins.builtin_type, 1, False),
        'list': Builtin(builtins.builtin_list, 0, True),
        'to-string': Builtin(builtins.builtin_to_string, 1, False),
        'repr': Builtin(builtins.builtin_repr, 1, False),
        'print': Builtin(builtins.builtin_print, 0, True),
        '<=>': Builtin(builtins.builtin_compare, 2, False),
        '=': Builtin(builtins.builtin_eq, 2, True),
        '<': Builtin(builtins.builtin_lt, 2, False),
        '>': Builtin(builtins.builtin_gt, 2, False),
        '+': Builtin(builtins.builtin_add, 1, True),
        '-': Builtin(builtins.builtin_sub, 1, True),
        '*': Builtin(builtins.builtin_mul, 1, True)
    }

    def __init__(self, source, symbols=None, outer=None):
        self.source = source
        self.symbols = symbols if symbols else self.PRIMITIVES.copy()
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

    def all(self):
        symbols = {}
        if self.outer:
            symbols.update(self.outer.all())
        symbols.update(self.symbols)
        return symbols

class Interpreter:
    def execute(self, env):
        tokenizer = Tokenizer(env.source)
        parser = Parser(tokenizer)
        sequence = parser.parse()
        retval = None
        for expr in sequence:
            retval = self.eval(expr, env)
        return retval

    def eval(self, expr, env):
        if isinstance(expr, Symbol):
            return env.lookup(expr)
        elif isinstance(expr, (str, int, long, float)):
            return expr
        elif isinstance(expr, list):
            return self.eval_list(expr, env)
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
            return func.func(*args)
        elif isinstance(func, Lambda):
            self.check_args(args, len(func.params), False)
            symbols = dict(zip(func.params, args))
            env = Env(func.env.source, symbols, func.env)
            retval = None
            for expr in func.body:
                retval = self.eval(expr, env)
            return retval

    def check_args(self, args, num_required, has_variable):
        num_args = len(args)
        if num_args < num_required:
            raise RuntimeError(
                "Too few arguments (min %d, but got %d)" %
                (num_required, num_args))
        if num_args > num_required and not has_variable:
            raise RuntimeError(
                "Too many arguments (max %d, but got %d)" %
                (num_required, num_args))

    def op_quote(self, args, env):
        if len(args) != 1:
            raise RuntimeError("quote requires 1 argument")
        return args[0]

    def op_def(self, args, env):
        if len(args) == 2 and isinstance(args[0], Symbol):
            (name, expr) = args
            value = self.eval(expr, env)
        elif len(args) >= 2 and self.is_symbol_list(args[0]):
            (name, params) = (args[0][0], args[0][1:])
            body = args[1:]
            value = Lambda(params, body, env)
        else:
            raise RuntimeError("Invalid syntax for def")
        env.define(name, value)
        return value

    def op_lambda(self, args, env):
        if len(args) < 2 or not self.is_symbol_list(args[0]):
            raise RuntimeError("Invalid syntax for lambda")
        return Lambda(args[0], args[1:], env)

    def op_if(self, args, env):
        if len(args) != 3:
            raise RuntimeError("Invalid syntax for if")
        (cond, then_expr, else_expr) = args
        return self.eval(then_expr if self.eval(cond, env) else else_expr, env)

    def op_load(self, args, env):
        if len(args) != 1:
            raise RuntimeError("Invalid syntax for load")
        filename = self.eval(args[0], env)
        if not isinstance(filename, str):
            raise RuntimeError("Invalid syntax for load")
        resolved_filename = self.resolve_filename(filename, env)
        code = open(resolved_filename).read()
        old_source = env.source
        env.source = Source(filename, code)
        self.execute(env)
        env.source = old_source
        return None

    def resolve_filename(self, filename, env):
        load_paths = list(env.lookup('load-paths'))
        if '/' in filename:
            dir = os.path.dirname(env.source.filename)
            if dir:
                load_paths.insert(0, dir)
        for path in load_paths:
            full_path = os.path.join(path, filename)
            if os.path.isfile(full_path):
                return full_path
        raise RuntimeError("Cannot find file: %s in %s" % (filename, builtins.builtin_repr(load_paths)))

    def is_symbol_list(self, items):
        return isinstance(items, list) and all(isinstance(item, Symbol) for item in items)
