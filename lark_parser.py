from lark import Lark, Transformer, Tree, Token
from lark.indenter import Indenter

tree_grammar = r"""
    ?start: (mm | dd)
    ?child: line | tree

    ?tree: _INDENT (mm | dd) _DEDENT
    mm: "." _NL child+
    dd: ":" _NL child+
    arity: ":" | "."
    ?line: func _NL

    ?func: monad | dyad | NAME
    dyad: "{" d? func+ "}"
    d: d? func+ ":"
    monad: "(" m? func+ ")"
    m: m? func+ "."

    %import common.CNAME -> NAME
    %import common.WS_INLINE
    %declare _INDENT _DEDENT
    %ignore WS_INLINE

    _NL: /(\r?\n[\t ]*)+/
"""

class TreeIndenter(Indenter):
    NL_type = '_NL'
    OPEN_PAREN_types = []
    CLOSE_PAREN_types = []
    INDENT_type = '_INDENT'
    DEDENT_type = '_DEDENT'
    tab_len = 8

class MyTransformer(Transformer):
    def d(self, items):
        return Tree(Token('RULE', 'dyad'), items)
    def m(self, items):
        return Tree(Token('RULE', 'monad'), items)
    def mm(self, items):
        return Tree(Token('RULE', 'monad'), items)
    def dd(self, items):
        return Tree(Token('RULE', 'dyad'), items)

parser = Lark(tree_grammar, parser='lalr', postlex=TreeIndenter())

test_tree = """\
.
a
    .
    (b b)
    c
        :
        d
        e
    f
        .
        g
"""

def test():
    print(test_tree)
    syntax_tree = parser.parse(test_tree)
    t = MyTransformer()
    syntax_tree = t.transform(syntax_tree)
    print(syntax_tree.pretty())

if __name__ == '__main__':
    test()
