from lark import Lark, logger
from lark.indenter import Indenter
import tokens

hofs = ' | '.join(f'"{k}"' for k in tokens.quick.keys())
monads = ' | '.join(f'"{a}"' for a in [*tokens.dyadic.keys(), *tokens.monadic.keys()])

grammar=f"""
?start: func_end | "\\\\" monad_end | "|" dyad_end
monad_end: func -> monad
dyad_end: func -> dyad
monad: monad3? func? (func_end | func) | monad "." func? (func_end | func)
monad3: (monad "." | monad3 | func) func (func_end | func) -> monad
dyad: dyad3? func? (func_end | func) | dyad "." func? (func_end | func)
dyad3: (dyad ":" | dyad3 | func) func (func_end | func) -> dyad
?func_end: "\\\\" monad | "|" dyad 
?func: "(" monad | monad_end ")" | "{{" dyad | dyad_end"}}" | builtin | hof | literal
!hof: HOFS func
HOFS: {hofs}
builtin: BUILTIN_DYAD | BUILTIN_MONAD
BUILTIN_DYAD: {' | '.join(f'"{a}"' for a in tokens.dyadic.keys())}
BUILTIN_MONAD: {' | '.join(f'"{a}"' for a in tokens.monadic.keys())}
dot: "."

number: SIGNED_NUMBER
literal: number
%import common.SIGNED_NUMBER

%import common.CNAME -> NAME
%import common.WS_INLINE
%import common.NEWLINE
%ignore WS_INLINE
%ignore NEWLINE
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
\ pair 1
"""
# sample_string="\ scan pair"
# logger.setLevel(logging.DEBUG)
if __name__ == "__main__":
    print(sample_string)
    parser = Lark(grammar, debug=False)
    for i, t in enumerate(parser.lex(sample_string)):
        print((t.line, t.column), repr(t))
    parse_tree = parser.parse(sample_string)
    print(parse_tree)
    print(parse_tree.pretty())

