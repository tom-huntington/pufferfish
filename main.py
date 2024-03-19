import jello
import jelly
from jello import utils
from jelly.interpreter import *
import itertools
from typing import Callable, Any
from dataclasses import dataclass

@dataclass
class InteriorWrapper:
    link : Callable
    is_left_child : bool
    children : list

    def __repr__(self):
        assert type(self.children) == list
        assert len(self.children) > 0
        inner = " ".join(str(c) for c in self.children)

        match self.link.arity:
            case 1:
                return f"({inner})" if not self.is_left_child else f"{inner} |"
            case 2:
                return f"{{{inner}}}" if not self.is_left_child else f"{inner} |"
        
        raise Exception("not reached")

@dataclass
class LeafWrapper:
    link : Callable
    token : str

    def __repr__(self):
        return self.token


@dataclass(frozen=True)
class FunctionTokens:
    arity : int
    data : list | str

    # def __repr__(self):
    #     #return f"{[self.arity, *self.data]}"
    #     assert type(self.data) == list
    #     assert len(self.data) > 0
    #     inner = str(self.data)[1:-1]
    #     match self.arity:
    #         case 1:
    #             return f"({inner})"
    #         case 2:
    #             return f"{{{inner}}}"
    #         case -1:
    #             return f"[{inner}]"
        
    #     return f"{[self.arity, *self.data]}"



def parse_parentheses(expression):
    result = FunctionTokens(-1, [])
    stack = []
    current = ""
    state = None

    for char in expression:
        if char in ("(", "{"):
            if current:
                result.data.append(FunctionTokens(None, current))
            current = ""
            stack.append(result)
            result = FunctionTokens({'(':1,'{':2}[char], [])
        elif char in (")", "}"):
            
            if char != {1:')',2:'}'}[result.arity]:
                raise Exception("Parentheses dont match")
                
            if current:
                result.data.append(FunctionTokens(None, current))
            current = ""
            if stack:
                last_result = stack.pop()
                last_result.data.append(result)
                result = last_result
        elif char.isspace():
            if current:
                result.data.append(FunctionTokens(None, current))
            current = ""
        else:
            current += char

    if current:
        result.data.append(FunctionTokens(-1, current))

    assert len(result.data) == 1, "Must specify arity"
    return result.data[0]



combinators = {
    'phi1': lambda f, g, h: attrdict(
        arity = 2,
        call = lambda x, y: dyadic_link(g, (dyadic_link(f, (x,y)), dyadic_link(h, (x, y))))
    ),
    'phi.2': lambda f, g, h: attrdict(
        arity = 2,
        call = lambda x, y: dyadic_link(g, (monadic_link(f, x), dyadic_link(h, (x, y))))
    ),
    # 'psi': lambda f, g: attrdict(
    #     arity = 2,
    #     call = lambda x, y: dyadic_link(g, (monadic_link(f, x), monadic_link(f, y)))
    # ),
    'delta': lambda f, g: attrdict(
        arity = 2,
        call = lambda x, y: dyadic_link(g, (monadic_link(f, x), y))
    ),
    'B1': lambda f, g: attrdict(
        arity = 2,
        call = lambda x, y: monadic_link(g, dyadic_link(f, (x, y)))
    ),
    'B.3': lambda f, g: attrdict(
        arity = 2,
        call = lambda x, _: monadic_link(g, monadic_link(f, x))
    ),
    'eps': lambda f, g: attrdict(
        arity = 2,
        call = lambda x, y: dyadic_link(g, (dyadic_link(f, (x, y)), y)) 
    ),
    'phi': lambda f, g, h: attrdict(
        arity = 1,
        call = lambda x: dyadic_link(g, (monadic_link(f, x), monadic_link(h, x)))
    ),
    'sig': lambda f, g: attrdict(
        arity = 1,
        call = lambda x: dyadic_link(g, (monadic_link(f, x), x))
    ),
    'B': lambda f, g: attrdict(
        arity = 1,
        call = lambda x: monadic_link(g, monadic_link(f, x))
    ),
    'S': lambda f, g: attrdict(
        arity = 1,
        call = lambda x: dyadic_link(g, (x, monadic_link(f, x)))
    ),
    'W': lambda f: attrdict(
        arity = 1,
        call = lambda x: dyadic_link(f, (x, x))
    ),
}

jelly_dyadic_rules = {
    (2, 2, 2) : "phi1",
    (2, 2): "eps",
    (2, 1): "B1",
    (1, 2, 2): "phi.2",
    (1, 2): "delta",
    (1, 1): "B.3",
}

jelly_monadic_rules = {
    (1, 2, 1) : "phi",
    (1, 2): "sig",
    (1, 1): "B",
    (2, 1): "S",
    (2): "W",
}

def get_arity(o):
    match o:
        case str(): return 1
        case FunctionTokens(arity): return arity


def apply_combinator(funcs, arity):
    rules = {1: jelly_monadic_rules, 2: jelly_dyadic_rules}[arity]
    arities = tuple(f.arity for f in funcs)
    rule = rules[arities]
    return combinators[rule](*funcs)


def nest_left_branches(l):
    match l.data:
        case FunctionTokens(): return l
        case list():
            def map_reduce(iterator, f0, f):
                head, *tail = iterator
                result = functools.reduce(f, tail, f0(head))
                return result
            
            ret = map_reduce(
                    (list(v) for k, v in itertools.groupby(l.data, lambda x: x.data != '|') if k),
                    lambda x: FunctionTokens(l.arity, x),
                    lambda head, tail: FunctionTokens(l.arity, [head, *tail]), 
                    )
            return ret


def FoldCombinatorTree(l, index):
    assert type(l) == FunctionTokens
    match l.data:
        case list(children):
            children = [FoldCombinatorTree(c, i) for i, c in enumerate(children)]
            link = apply_combinator([c.link for c in children], l.arity)
            return InteriorWrapper(link, index==0, children)
             
        case str(s):
            link = jelly.interpreter.atoms.get(jello.to_jelly(s), None) or jelly.interpreter.create_literal(regex_liter.sub(parse_literal, s))
            ret = LeafWrapper(link, s)
            return ret


b = parse_parentheses("{add1 pair | add1 }")
b = nest_left_branches(b)
b = FoldCombinatorTree(b, 1)
print(b)
print(dyadic_link(b.link, (1, 10)))
