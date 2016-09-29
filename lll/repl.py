from traceback import print_exc
import readline
from lll.tokenizer import Source
from lll.parser import IncompleteParseError
from lll.interpreter import Env
from lll.builtins import builtin_repr

if 'libedit' in readline.__doc__:
    readline.parse_and_bind("bind -e")
    readline.parse_and_bind("bind '\t' rl_complete")
else:
    readline.parse_and_bind("tab: complete")

class REPL:
    INPUT_PROMPT = '> '
    CONT_PROMPT = '- '
    OUTPUT_PROMPT = '= '

    def __init__(self, interpreter):
        self.interpreter = interpreter
        self.env = None
        readline.set_completer(self.complete)

    def run(self):
        source = Source('<repl>', '')
        self.env = Env(source)

        input = ''
        while True:
            try:
                try:
                    prompt = self.CONT_PROMPT if input else self.INPUT_PROMPT
                    input += raw_input(prompt) + '\n'
                except (EOFError, KeyboardInterrupt):
                    print('')
                    return
                try:
                    self.env.source.code = input
                    value = self.interpreter.execute(self.env)
                except IncompleteParseError as e:
                    continue
                if value is not None:
                    print(self.OUTPUT_PROMPT + builtin_repr(value))
            except:
                print_exc()
            input = ''

    def complete(self, text, state):
        symbols = sorted(self.env.all().keys())
        matches = [sym + ' ' for sym in symbols if sym.startswith(text)] + [None]
        return matches[state]
