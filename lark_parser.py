from lark import Lark, Transformer, Tree, Token
from lark.indenter import Indenter
from core import *
import run_lark
import tokens
import argparse
import stringify as puffer_stringify
import jello
from ast import literal_eval

def func(arity, children):
    link = apply_combinator([c.link for c in children], arity)
    return InteriorWrapper(link, None, children)

def make_link_for_quick_hyper(key, hof_arguments):

    jello_name = jello.to_jelly(key)
    if q := jelly.interpreter.quicks.get(jello_name, None):
        assert q.condition(hof_arguments)
        link, = q.quicklink(hof_arguments, [], None)
        return link
    else:
        link, = hof_arguments
        return jelly.interpreter.hypers[jello_name](link)

class LinkTransformer(Transformer):
    def builtin(self, tokens):
        token, = tokens
        s = token.value
        link = jelly.interpreter.atoms.get(jello.to_jelly(s))
        return link


    def monad(self, children):
        return apply_combinator(children, 1)

    def dyad(self, children):
        return apply_combinator(children, 2)

    def literal(self, children):
        child, = children
        literal_as_str, = child.children
        value = literal_eval(literal_as_str)
        return attrdict(call=(lambda: value), arity=0)
    
    def hof(self, children):
        name, *hof_arguments = children
        link = make_link_for_quick_hyper(name, hof_arguments)
        return link
    
parser = Lark(run_lark.grammar, debug=False, lexer="auto")

sample_string = """\
\ i scan pair .
"""

def puffer_parse(code):
    print("code\n", code)
    for t in parser.lex(code):
        print((t.line, t.column), repr(t))

    syntax_tree = parser.parse(code)
    print(syntax_tree.data, "\n----")
    print(syntax_tree.pretty())
    return syntax_tree

def make_link(ast):
    print(puffer_stringify.stringify_tree(ast))

    t = LinkTransformer()
    link = t.transform(ast)
    return link

def evaluate_code_ignoring_default_args(code, args):
    code = code.lstrip()
    if code[0] == '@':
        _, code = code.split('\n', 1)
    
    return evaluate_code(code, args)
    
        

def evaluate_maybe_string_args(code, maybe_args):
    code = code.lstrip()
    if maybe_args:
        args = [literal_eval(arg) for arg in maybe_args]
    else:
        assert code[0] == '@'
        default_args, code = code.split('\n', 1)
        args = [literal_eval(arg) for arg in default_args.split(' ')[1:]]
    
    return evaluate_code(code, args)


def evaluate_code(code, args):
    ast = puffer_parse(code)
    link = make_link(ast)

    match link.arity:
        case 1:
            arg, = args
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

    print(evaluate_maybe_string_args(args.code or code, args.args))
    


if __name__ == '__main__':
    main()
