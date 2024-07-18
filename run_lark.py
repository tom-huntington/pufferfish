from lark import Lark, logger
from lark.indenter import Indenter
import tokens
import logging

dyadic_quicks = ('chunk_fold', 'slide_fold')
hofs1 = ' | '.join(f'"{k}"' for k in tokens.quick.keys() if k not in dyadic_quicks)
hofs2 = ' | '.join(f'"{k}"' for k in dyadic_quicks)
# monads = ' | '.join(f'"{a} "' for a in [*tokens.dyadic.keys(), *tokens.monadic.keys()])


grammar=f"""
?start: func_end 
monad: (monad3 _ws)? (func _ws)? (func_end | func) | monad "." (func _ws)? (func_end | func)
monad3: (monad _ws "." | monad3 | func) _ws func _ws (func_end | func) -> monad
dyad: (dyad3 _ws)? (func _ws)? (func_end | func) | dyad "." (func _ws)? (func_end | func)
dyad3: (dyad _ws ":" | dyad3 | func) _ws func _ws (func_end | func) -> dyad
?func_end: "\\\\" _ws monad | "|" _ws dyad
?func: "(" monad ")" | "{{" dyad "}}" | hof | builtin | literal
!hof: (HOFS1 _ws func) | (HOFS2 _ws func _ws func)
HOFS1: {hofs1}
HOFS2 . 1: {hofs2}
builtin: BUILTIN_DYAD | BUILTIN_MONAD
BUILTIN_DYAD: {' | '.join(f'"{a}"' for a in tokens.dyadic.keys())}
BUILTIN_MONAD: {' | '.join(f'"{a}"' for a in tokens.monadic.keys() if a != "part")}

number: SIGNED_NUMBER
literal: number
%import common.SIGNED_NUMBER
%import common.WS
%ignore WS

_ws: (" " | "\\n" | "\\t")+
"""

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
| chunk_fold + 2"""
# sample_string="\ scan pair"
# logger.setLevel(logging.DEBUG)
if __name__ == "__main__":
    logger.setLevel(logging.DEBUG)
    print(sample_string)
    parser = Lark(grammar, debug=False, strict=True)
    for i, t in enumerate(parser.lex(sample_string)):
        print((t.line, t.column), repr(t))
    parse_tree = parser.parse(sample_string)
    print(parse_tree.pretty())
    print(parse_tree)

