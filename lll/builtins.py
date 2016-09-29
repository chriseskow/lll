from lll.parser import Symbol
from lll.interpreter import Operator, Builtin, Lambda

def builtin_list(*args):
    return list(args)

def builtin_to_string(value):
    if isinstance(value, (Symbol, str, int, long, float)):
        return str(value)
    elif isinstance(value, list):
        return '(' + ' '.join(builtin_to_string(item) for item in value) + ')'
    elif isinstance(value, Operator):
        return '<operator>'
    elif isinstance(value, Builtin):
        return '<builtin>'
    elif isinstance(value, Lambda):
        return '<lambda>'
    else:
        raise RuntimeError("[BUG] Don't know how to print: %s" % repr(value))

def builtin_repr(value):
    if isinstance(value, (Symbol, int, long, float)):
        return str(value)
    elif isinstance(value, str):
        return '"' + value + '"' # TODO: escape slashes
    elif isinstance(value, list):
        return '(' + ' '.join(builtin_repr(item) for item in value) + ')'
    elif isinstance(value, Operator):
        return '<operator>'
    elif isinstance(value, Builtin):
        return '<builtin>'
    elif isinstance(value, Lambda):
        return '<lambda>'
    else:
        raise RuntimeError("[BUG] Don't know how to print: %s" % repr(value))

def builtin_print(*args):
    print(''.join(builtin_to_string(arg) for arg in args))
    return None

def builtin_eq(*args):
    return int(args.count(args[0]) == len(args))

def builtin_lt(x, y):
    return int(x < y)

def builtin_gt(x, y):
    return int(x > y)

def builtin_add(*args):
    return sum(args)

def builtin_sub(*args):
    return reduce(lambda sum, n: sum - n, args[1:], args[0])

def builtin_mul(*args):
    return reduce(lambda product, n: product * n, args, 1)
