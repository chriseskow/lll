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
    def __init__(self, source, symbols={}, outer=None):
        self.source = source
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

    def all(self):
        symbols = {}
        if self.outer:
            symbols.update(self.outer.all())
        symbols.update(self.symbols)
        return symbols

class Interpreter:
    PRIMITIVES = {
        'quote': Operator('op_quote'),
        'def': Operator('op_def'),
        'lambda': Operator('op_lambda'),
        'if': Operator('op_if'),
        'load': Operator('op_load'),
        'load-paths': ['.'],
        'to-string': Builtin(builtins.builtin_to_string, 1, False),
        'repr': Builtin(builtins.builtin_repr, 1, False),
        'print': Builtin(builtins.builtin_print, 0, True),
        '=': Builtin(builtins.builtin_eq, 2, True),
        '<': Builtin(builtins.builtin_lt, 2, False),
        '>': Builtin(builtins.builtin_gt, 2, False),
        '+': Builtin(builtins.builtin_add, 1, True),
        '-': Builtin(builtins.builtin_sub, 1, True),
        '*': Builtin(builtins.builtin_mul, 1, True)
    }

    def execute(self, source, env=None):
        tokenizer = Tokenizer(source)
        parser = Parser(tokenizer)
        sequence = parser.parse()
        if env is None:
            env = self.make_global_env(source)

        retval = None
        for expr in sequence:
            retval = self.eval(expr, env)
        return retval

    def make_global_env(self, source):
        return Env(source, self.PRIMITIVES.copy())

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
        if len(args) != 2:
            raise RuntimeError("def called with wrong number of arguments")
        (symbol, value_expr) = args
        if not isinstance(symbol, Symbol):
            raise RuntimeError("def called without an identifier as first argument")
        value = self.eval(value_expr, env)
        env.define(symbol, value)
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

    def op_load(self, args, env):
        if len(args) != 1:
            raise RuntimeError("load requires 1 argument")
        filename = self.eval(args[0], env)
        if not isinstance(filename, str):
            raise RuntimeError("load requires a string argument")
        resolved_filename = self.resolve_filename(filename, env)
        code = open(resolved_filename).read()
        old_source = env.source
        env.source = Source(filename, code)
        self.execute(env.source, env)
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

    def require_param_list(self, items):
        if not isinstance(items, list):
            raise RuntimeError("lambda called without argument list")
        params = []
        for item in items:
            if not isinstance(item, Symbol):
                raise RuntimeError("lambda called with non-identifier param")
            params.append(item)
        return params
