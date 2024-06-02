from lark import Lark, Transformer, Tree, Token
from lark.indenter import Indenter
from core import *
# import jello
# import jelly
# import tokens as jello_tokens
# from jelly.interpreter import *

tree_grammar = r"""
    ?start: (mm | dd)
    ?child: line | tree

    ?tree: _INDENT (mm | dd) _DEDENT
    mm: "." _NL child+
    dd: ":" _NL child+
    arity: ":" | "."
    ?line: func _NL

    builtin: NAME
    ?func: monad | dyad | builtin
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

def func(arity, children):
    link = apply_combinator([c.link for c in children], 1)
    return InteriorWrapper(link, None, children)

class JelloTransformer(Transformer):
    def builtin(self, tokens):
        token, = tokens
        s = token.value
        if link := jelly.interpreter.atoms.get(jello.to_jelly(s), None):
            pass
        elif jelly_token := jello_tokens.quick.get(s, None):
            return hof_token(s, jelly_token, hof_arity[s])
        else: link = create_constant(None, s)
        ret = LeafWrapper(link, s)
        return ret

    def monad(self, children):
        return func(1, children)
    def dyad(self, children):
        return func(2, children)

parser = Lark(tree_grammar, parser='lalr', postlex=TreeIndenter())

test_tree = """\
.
pair
    .
    (add1 add1)
    pair
        :
        add1
        pair
    add1
        .
        pair
        add1
"""

def test():
    print(test_tree)
    syntax_tree = parser.parse(test_tree)
    t = MyTransformer()
    syntax_tree = t.transform(syntax_tree)
    print(syntax_tree.pretty())
    syntax_tree = JelloTransformer().transform(syntax_tree)

if __name__ == '__main__':
    test()
