from lark import Lark, logger
from lark.indenter import Indenter
import tokens

hofs = ' | '.join(f'"{k}"' for k in tokens.quick.keys())
monads = ' | '.join(f'"{a}"' for a in [*tokens.dyadic.keys(), *tokens.monadic.keys()])

grammar=f"""
?start: func_end | "\\\\" monad_end | "|" dyad_end
monad_end: func
dyad_end: func
monad: (monad "." | monad func | func ~ 0..2 ) (func_end | func)
dyad: (dyad ":" | dyad func | func ~ 0..2) (func_end | func)
?func_end: "\\\\" monad | "|" dyad 
?func: "(" monad | monad_end ")" | "{{" dyad | dyad_end"}}" | builtin | dot | hof
!hof: HOFS func
HOFS: {hofs}
builtin: BUILTIN_DYAD | BUILTIN_MONAD
BUILTIN_DYAD: {' | '.join(f'"{a}"' for a in tokens.dyadic.keys())}
BUILTIN_MONAD: {' | '.join(f'"{a}"' for a in tokens.monadic.keys())}
dot: "."

%import common.CNAME -> NAME
%import common.WS_INLINE
%import common.NEWLINE
%ignore WS_INLINE
%ignore NEWLINE
"""
print(grammar)

sample_string ="""\
\ add1 . pair i
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

