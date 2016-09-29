from traceback import print_exc
import readline
from lll.parser import IncompleteParseError

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
        self.env = self.interpreter.make_global_env()

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
                    value = self.interpreter.execute_string(input, self.env)
                except IncompleteParseError as e:
                    continue
                if value:
                    print(self.OUTPUT_PROMPT + self.interpreter.builtin_repr(value))
            except:
                print_exc()
            input = ''

    def complete(self, text, state):
        symbols = sorted(self.env.all().keys())
        matches = [sym + ' ' for sym in symbols if sym.startswith(text)] + [None]
        return matches[state]
