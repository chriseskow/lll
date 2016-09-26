#!/usr/bin/env python

from sys import argv
from lll.tokenizer import Tokenizer
from lll.parser import Parser
from lll.interpreter import Interpreter

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
