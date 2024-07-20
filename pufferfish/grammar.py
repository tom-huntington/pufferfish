from lark import Lark, logger
from lark.indenter import Indenter
from jello.tokens import quick, dyadic, monadic
import logging

dyadic_quicks = ('chunk_fold', 'slide_fold')
hofs1 = ' | '.join(f'"{k}"' for k in quick.keys() if k not in dyadic_quicks)
hofs2 = ' | '.join(f'"{k}"' for k in dyadic_quicks)
# monads = ' | '.join(f'"{a} "' for a in [*tokens.dyadic.keys(), *tokens.monadic.keys()])


grammar=f"""
?start: func_end 
monad: (monad3)? (func)? (func_end | func) | monad "." (func)? (func_end | func) | monad3
monad3: (monad "." | monad3 | func) func (func_end | func) -> monad
dyad: (dyad3)? (func)? (func_end | func) | dyad "." (func)? (func_end | func) | dyad3
dyad3: (dyad ":" | dyad3 | func) func (func_end | func) -> dyad
?func_end: "\\\\" monad | "|" dyad
?func: "(" monad ")" | "{{" dyad "}}" | _hof | builtin | literal
hofm: HOF1 "(" func ")" | HOF2 "(" func~2 ")"
hofd: HOF1 "{{" func  "}}" | HOF2 "{{" func~2 "}}"
_hof: hofm | hofd
HOF1: {hofs1}
HOF2 . 1: {hofs2}
builtin: BUILTIN_DYAD | BUILTIN_MONAD | BUILTIN_MONAD_L
BUILTIN_DYAD: {' | '.join(f'"{a}"' for a in dyadic.keys())}
BUILTIN_MONAD: {' | '.join(f'"{a}"' for a in monadic.keys() if a not in ["i"])}
BUILTIN_MONAD_L . -1: "i"

number: SIGNED_NUMBER
literal: number
%import common.SIGNED_NUMBER
%import common.WS
%ignore WS

"""

# _ws: (" " | "\\n" | "\\t")+
# literal: string
#         | number
#         | "True"     -> true
#         | "False"    -> false
#         | "None"     -> null
#         | list
#         | dict

# string  : ESCAPED_STRING
# list    : "[" [literal ("," literal)*] "]"
# dict    : "{" [pair ("," pair)*] "}"
# pair    : string ":" literal

# %import common.ESCAPED_STRING


print(grammar)

sample_string ="""\
| idiv"""
# sample_string="\ scan pair"
# logger.setLevel(logging.DEBUG)
if __name__ == "__main__":
    logger.setLevel(logging.DEBUG)
    print(sample_string)
    parser = Lark(grammar, debug=False, strict=False, lexer="basic")
    for i, t in enumerate(parser.lex(sample_string)):
        print((t.line, t.column), repr(t))
    parse_tree = parser.parse(sample_string)
    print(parse_tree.pretty())
    print(parse_tree)

