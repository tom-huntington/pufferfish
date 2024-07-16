from lark import Lark, Transformer, Tree, Token
from lark.indenter import Indenter
from core import *
import run_lark
import tokens


def func(arity, children):
    link = apply_combinator([c.link for c in children], arity)
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

class LinkTransformer(Transformer):
    def builtin(self, tokens):
        token, = tokens
        s = token.value
        if link := jelly.interpreter.atoms.get(jello.to_jelly(s), None):
            pass
        elif jelly_token := jello_tokens.quick.get(s, None):
            raise "not implemented"
            return hof_token(s, jelly_token, hof_arity[s])
        else: link = create_constant(None, s)
        return link

    def monad(self, children):
        return apply_combinator(children, 1)

    def dyad(self, children):
        return apply_combinator(children, 2)
    
    def hof(self, children):
        quick_name, *hof_arguments = children
        q = jelly.interpreter.quicks.get(tokens.quick.get(quick_name, None), None)
        assert q.condition(hof_arguments)
        link, = q.quicklink(hof_arguments, [], None)
        return link

parser = Lark(run_lark.grammar)

sample_string = """\
\ i scan pair .
"""

def test():
    print(sample_string)
    syntax_tree, = parser.parse(sample_string).children
    print(syntax_tree.data, "\n----")
    print(syntax_tree.pretty())
    t = LinkTransformer()
    link = t.transform(syntax_tree)
    # call_link = monadic_link if link.data == "monad" else dyadic_link
    print(monadic_link(link, [1, 2, 3]))

if __name__ == '__main__':
    test()
