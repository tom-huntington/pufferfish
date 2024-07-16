from lark import Lark, logger
from lark.indenter import Indenter
import tokens

hofs = ' | '.join(f'"{k}"' for k in tokens.quick.keys())
atoms = ' | '.join(f'"{a}"' for a in [*tokens.dyadic.keys(), *tokens.monadic.keys()])

grammar=f"""
start: "\\\\" monad | "|" dyad
monad: (monad | func) func (func_end | func)
dyad: (dyad | func) func (func_end | func)
?func_end: "\\\\" monad | "|" dyad
?func: "(" monad ")" | "{{" dyad "}}" | builtin | dot | hof
!hof: HOFS func
HOFS: {hofs}
builtin: BUILTIN
BUILTIN: {atoms}
dot: "."

%import common.CNAME -> NAME
%import common.WS_INLINE
%import common.NEWLINE
%ignore WS_INLINE
%ignore NEWLINE
"""
print(grammar)

sample_string ="""\
\ scan pair ..
"""
# sample_string="\ scan pair"
# logger.setLevel(logging.DEBUG)
if __name__ == "__main__":
    print(sample_string)
    parser = Lark(grammar)
    for i, t in enumerate(parser.lex(sample_string)):
        print((t.line, t.column), repr(t))
    parse_tree = parser.parse(sample_string)
    print(parse_tree)
    print(parse_tree.pretty())

