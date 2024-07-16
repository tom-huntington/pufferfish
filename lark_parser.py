from lark import Lark, Transformer, Tree, Token
from lark.indenter import Indenter
from core import *
import run_lark
import tokens
import argparse


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
    
    def hof(self, children):
        quick_name, *hof_arguments = children
        q = jelly.interpreter.quicks.get(tokens.quick.get(quick_name, None), None)
        assert q.condition(hof_arguments)
        link, = q.quicklink(hof_arguments, [], None)
        return link
    
    def dot(self, children):
        return None
        # return attrdict(arity = None, call = None)

parser = Lark(run_lark.grammar)

sample_string = """\
\ i scan pair .
"""

def evaluate_code(code, args):
    code = code.lstrip()
    if code[0] == '@':
        default_args, code = code.split('\n', 1)
        default_args = default_args.split(' ')[1:]
        
    print("code\n", code)
    syntax_tree, = parser.parse(code).children
    print(syntax_tree.data, "\n----")
    print(syntax_tree.pretty())
    t = LinkTransformer()
    link = t.transform(syntax_tree)
    match link.arity:
        case 1:
            arg, = args
            print(monadic_link(link, eval(arg)))
        case 2:
            assert len(args) == 2
            print(dyadic_link(link, [eval(a) for a in args]))

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

    evaluate_code(args.code or code, args.args)
    


if __name__ == '__main__':
    main()
