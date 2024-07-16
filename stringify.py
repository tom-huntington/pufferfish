from dataclasses import dataclass, field

from lark import Transformer
from core import InteriorWrapper, LeafWrapper, puffer_eval
import parse_pythonic_syntax
from numpy.typing import NDArray
import numpy as np
from more_itertools import interleave_longest, windowed
from itertools import repeat, accumulate
from operator import add
import lark_parser
import jello
from jelly.utils import attrdict
import jelly
import tokens

def stringify_2d_unicode(result : NDArray):
    return '\n'.join(''.join(row) for row in result)

def print2d_unicode(result : NDArray):
    print(stringify_2d_unicode(result))

def draw(node : InteriorWrapper | LeafWrapper) -> NDArray:
    match node:
        case LeafWrapper(link, token):
            return np.array(list(token)).reshape(1,-1)
        case InteriorWrapper():
            children = [draw(child) for child in node.children]
            max_height = max(child.shape[0] for child in children)

            def padbottom(child):
                d1, d0 = child.shape
                padding_bottom = np.array([[(' ' if i != d0//2 else '│') for i in range(d0)] for _ in range(max_height - d1)])
                padding_bottom2 = padding_bottom.reshape(-1, d0)
                result = np.concatenate([child, padding_bottom2], axis=-2)
                # print2d_unicode(result)
                return result
            
            padded = [padbottom(c) for c in children]

            seperator = np.array([' '] * max_height).reshape(-1, 1)

            # interleaved = [e for c in padded for e in (c, seperator)][:-1]
            interleaved = list(interleave_longest(padded, repeat(seperator, len(padded) -1 )))
            body = np.concatenate(interleaved, axis=-1)
            acc_width = list(accumulate((c.shape[1] for c in children), lambda a, x: a+x+1, initial=0))
            middles = list(map(add, acc_width, (c.shape[1]//2 for c in children)))
            # print("middles", middles)
            

            def footer(middles, width):
                middle = width//2
                for i in range(width):
                    if i in middles:
                        if i == middles[0]: yield "╰"
                        elif i == middles[-1]: yield "╯"
                        elif i == middle: yield "┼"
                        else: yield '┴'
                        
                    elif i < middles[0] or middles[-1] < i: yield " "
                    else: yield "─" if i != middle else '┬'
        
            width = body.shape[1]
            foot = np.array([*footer(middles, width)]).reshape(1,-1)
            middle_range = range(width//2, width//2 + len(node.token()))

            foot2 = np.array([(' ' if i not in middle_range else node.token()[middle_range.index(i)]) for i in range(width)]).reshape(1,-1)
            result = np.concatenate((body, foot, foot2), axis=0)
            # print2d_unicode(result)
            return result

# root = parse("{add1 pair | add1 }")
# draw(root)  

def stringify_tree(root):
    return stringify_2d_unicode(draw(root))



class NodeTransformer(Transformer):
    def builtin(self, tokens):
        token, = tokens
        s = token.value
        if link := jelly.interpreter.atoms.get(jello.to_jelly(s), None):
            pass
        else:
            link = create_constant(None, s)
        return LeafWrapper(link, s)

    def monad(self, children):
        return InteriorWrapper(attrdict(arity=1), None, children)
        return apply_combinator([c for c in children if c is not None], 1)

    def dyad(self, children):
        return InteriorWrapper(attrdict(arity=2), None, children)
        return apply_combinator([c for c in children if c is not None], 2)
    
    def dyad_end(self, children):
        return InteriorWrapper(attrdict(arity=2), None, children)
        return apply_combinator([c for c in children if c is not None], 2)
    
    def monad_end(self, children):
        return InteriorWrapper(attrdict(arity=1), None, children)
        return apply_combinator([c for c in children if c is not None], 1)
    
    def hof(self, children):
        quick_name, *hof_arguments = children
        q = jelly.interpreter.quicks.get(tokens.quick.get(quick_name, None), None)
        # assert q.condition(hof_arguments)
        link, = q.quicklink(hof_arguments, [], None)
        return InteriorWrapper(link, None, [LeafWrapper(attrdict(arity=1), children[0].value), *children[1:]])
        quick_name, *hof_arguments = children
        q = jelly.interpreter.quicks.get(tokens.quick.get(quick_name, None), None)
        assert q.condition(hof_arguments)
        link, = q.quicklink(hof_arguments, [], None)
        return link
    
    def dot(self, children):
        return None
        # return attrdict(arity = None, call = None)

if __name__ == "__main__":
    # b, default_args = parse_pythonic_syntax.parse(a)
    # print(stringify_tree(b))
    # c = puffer_eval(b, {}, default_args)
    # print(c)jjkkkk

    ast = lark_parser.puffer_parse("\ key len . \ idx_max at_idx . sum")    
    print(ast)
    b = NodeTransformer().transform(ast)
    print(stringify_tree(b))
