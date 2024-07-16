from lark import Lark, Transformer, Tree, Token
from lark.indenter import Indenter
from core import *
import run_lark
import tokens
import argparse
import stringify as puffer_stringify
import jello

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
        return apply_combinator([c for c in children if c is not None], 1)

    def dyad(self, children):
        return apply_combinator([c for c in children if c is not None], 2)
    
    def dyad_end(self, children):
        return apply_combinator([c for c in children if c is not None], 2)
    
    def monad_end(self, children):
        return apply_combinator([c for c in children if c is not None], 1)
    
    def hof(self, children):
        quick_name, *hof_arguments = children
        q = jelly.interpreter.quicks.get(tokens.quick.get(quick_name, None), None)
        assert q.condition(hof_arguments)
        link, = q.quicklink(hof_arguments, [], None)
        return link
    
    def dot(self, children):
        return None
        # return attrdict(arity = None, call = None)

parser = Lark(run_lark.grammar, debug=False)

sample_string = """\
\ i scan pair .
"""

def puffer_parse(code):
    for t in parser.lex(code):
        print((t.line, t.column), repr(t))

    print("code\n", code)
    syntax_tree = parser.parse(code)
    print(syntax_tree.data, "\n----")
    print(syntax_tree.pretty())
    return syntax_tree

def make_link(ast):
    puffer_stringify.stringify_tree()

    t = LinkTransformer()
    link = t.transform(ast)
    return link


def evaluate_code(code, args):
    code = code.lstrip()
    if code[0] == '@':
        default_args, code = code.split('\n', 1)
        default_args = [eval(arg) for arg in default_args.split(' ')[1:]]
    
    ast = puffer_parse(code)
    link = make_link(ast)

    match link.arity:
        case 1:
            arg, = args or default_args
            return monadic_link(link, arg)
        case 2:
            assert len(args) == 2
            return dyadic_link(link, args)

def main():
    parser = argparse.ArgumentParser(description='Pufferfish interpreter')

    parser.add_argument('-c', '--code', type=str, help='Code')
    parser.add_argument('-f', '--file', type=str, help='Code file path')
    parser.add_argument('-a', '--args', nargs='+')
    args = parser.parse_args()
    print(args.args)
    if args.file and not args.code:
        with open(args.file) as f:
            code = f.read()
    
    if not (args.code or args.file):
        print("No code provided")
        exit(1)

    print(evaluate_code(args.code or code, [eval(arg) for arg in args.args]))
    


if __name__ == '__main__':
    main()
