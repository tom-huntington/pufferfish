import itertools
from prompt_toolkit import PromptSession
from pufferfish import main as main_module
from typing import Callable
from prompt_toolkit.styles import Style
from prompt_toolkit.lexers import Lexer
from prompt_toolkit.document import Document
from prompt_toolkit.formatted_text import StyleAndTextTuples
import jello.tokens
from ast import literal_eval

class KeywordLexer(Lexer):
    def __init__(self, red_words, blue_words, green_words):
        self.red_words = set(red_words)
        self.blue_words = set(blue_words)
        self.green_words = set(green_words)

    def lex_document(self, document: Document) -> Callable[[int], StyleAndTextTuples]:
        def get_line(lineno: int) -> StyleAndTextTuples:
            line = document.lines[lineno]
            words = line.split()  # Simple split on whitespace
            result = []
            
            for word in words:
                if word in self.red_words:
                    result.append(('class:red', word + ' '))
                elif word in self.blue_words:
                    result.append(('class:blue', word + ' '))
                elif word in self.green_words:
                    result.append(('class:green', word + ' '))
                else:
                    result.append(('', word + ' '))

            return result

        return get_line


# Define styles for the keywords
style = Style.from_dict({
    'red': 'ansired',
    'blue': 'ansiblue',
    'green': 'ansigreen',
})

# Define the keywords
red_words = ["fold"]
blue_words = ["add1"]
green_words = ["pair"]

# Create the custom lexer
lexer = KeywordLexer(jello.tokens.quick.keys(), jello.tokens.monadic.keys(), jello.tokens.dyadic.keys())

def eval_args(string_args):
    string_args_split = string_args.split(' ')
    assert len(string_args_split) in (1,2)
    return [literal_eval(arg) for arg in string_args_split]

def main():
    session = PromptSession(lexer=lexer, style=style)

    string_args = session.prompt('Provide argumemnts: ').strip()
    args = eval_args(string_args)

    for i in itertools.count(0):
        input = session.prompt(f'{string_args} >> ')
        match input:
            case _ if input.startswith('!set'):
                string_args = input.removeprefix('!set').strip()
                args = eval_args(string_args)
            case _:
                try:
                    print('\n', main_module.evaluate_code(input, args), '\n')
                except Exception as e:
                    print(f"error: {e}\n")
            
            

if __name__ == "__main__":
    main()