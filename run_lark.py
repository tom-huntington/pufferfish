from lark import Lark, logger
from lark.indenter import Indenter
import logging

grammar="""\
start: block_monad | block_dyad | inl_monad _NL* | inl_dyad _NL*
?func: monad0 | dyad0
?func_d: builtin _DNL | monad_d | dyad_d
builtin: NAME

block_monad: "." _NL monad_d? func+
block_dyad: ":" _NL dyad_d? func+
?monad0: _INDENT block_monad _DEDENT | inl_monad _NL | builtin _NL
?dyad0: _INDENT block_dyad _DEDENT | inl_dyad _NL | builtin _NL
inl_monad: "(" m? inl_func+ ")"
inl_dyad: "{" d? inl_func+ "}"
monad_d: monad_d? func* func_d
dyad_d: dyad_d? func* func_d
d: d? inl_func+ ":"
m: m? inl_func+ "."

?inl_func: builtin | inl_monad | inl_dyad

_NL: /\\n */
_DNL: /\\n\\n */

%declare _INDENT _DEDENT
%import common.CNAME -> NAME
%import common.WS_INLINE
%ignore WS_INLINE
"""
sample_string ="""\
.
c
    .
    a
    b
f
"""


class TreeIndenter(Indenter):
    NL_type = 'NL'
    OPEN_PAREN_types = []
    CLOSE_PAREN_types = []
    INDENT_type = '_INDENT'
    DEDENT_type = '_DEDENT'
    tab_len = 4

# logger.setLevel(logging.DEBUG)
print(sample_string)
parser = Lark(grammar, postlex=TreeIndenter())
# parser = Lark(grammar, postlex=TreeIndenter(), debug=True)
for i, t in enumerate(parser.lex(sample_string)):
    print((t.line, t.column), repr(t))
parse_tree = parser.parse(sample_string)
print(parse_tree)
print(parse_tree.pretty())

