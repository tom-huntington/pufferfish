import jello
import jelly
import tokens as jello_tokens
from jello import utils
from jelly.interpreter import *
import itertools
from typing import Callable, Any
from dataclasses import dataclass
import ast

@dataclass
class InteriorWrapper:
    link : Callable
    is_left_child : bool
    children : list

    # @property
    def token(self):
        rules = {1: jelly_monadic_rules, 2: jelly_dyadic_rules}[self.link.arity]
        arities = tuple(l.link.arity for l in self.children)
        ascii = rules[arities]
        return {
            'phi.2': 'Φ.₂',
            'phi1':'Φ₁',
            'D2':'D₂',
            'phi':'Φ',
            'psi':'Ψ',
            'delta':'Δ',
            'sig': 'Σ',
            'B1': 'B₁',

        }.get(ascii, ascii)

    # def __repr__(self):
    #     assert type(self.children) == list
    #     assert len(self.children) > 0
    #     inner = " ".join(str(c) for c in self.children)

    #     match self.link.arity:
    #         case 1:
    #             return f"({inner})" if not self.is_left_child else f"{inner} |"
    #         case 2:
    #             return f"{{{inner}}}" if not self.is_left_child else f"{inner} |"
        
    #     raise Exception("not reached")

@dataclass
class LeafWrapper:
    link : Callable
    token : str

    def __repr__(self):
        return self.token

@dataclass
class HofWrapper:
    link : Callable
    token_ : str
    children : list[LeafWrapper | InteriorWrapper]

    def token(self):
        return self.token_

    # def __repr__(self):
    #     return self.token

@dataclass(frozen=True)
class FunctionTokens:
    arity : int
    data : list | str

    # def __repr__(self):
    #     inner = str(self.data)[1:-1]
    #     match self.arity:
    #         case 1:
    #             return f"({inner})"
    #         case 2:
    #             return f"{{{inner}}}"
    #         case -1:
    #             return f"[{inner}]"
    #         case None:
    #             return str(self.data)
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
    'Φ₁': lambda f, g, h: attrdict(
        arity = 2,
        call = lambda x, y: dyadic_link(g, (dyadic_link(f, (x,y)), dyadic_link(h, (x, y))))
    ),
    'Φ.₂': lambda f, g, h: attrdict(
        arity = 2,
        call = lambda x, y: dyadic_link(g, (monadic_link(f, x), dyadic_link(h, (x, y))))
    ),
    'D₂': lambda f, g, h: attrdict(
        arity = 2,
        call = lambda x, y: dyadic_link(g, (monadic_link(f, x), monadic_link(h, x)))
    ),
    # 'Ψ': lambda f, g: attrdict(
    #     arity = 2,
    #     call = lambda x, y: dyadic_link(g, (monadic_link(f, x), monadic_link(f, y)))
    # ),
    'Δ': lambda f, g: attrdict(
        arity = 2,
        call = lambda x, y: dyadic_link(g, (monadic_link(f, x), y))
    ),
    'B₁': lambda f, g: attrdict(
        arity = 2,
        call = lambda x, y: monadic_link(g, dyadic_link(f, (x, y)))
    ),
    'B.3': lambda f, g: attrdict(
        arity = 2,
        call = lambda x, _: monadic_link(g, monadic_link(f, x))
    ),
    'ε': lambda f, g: attrdict(
        arity = 2,
        call = lambda x, y: dyadic_link(g, (dyadic_link(f, (x, y)), y)) 
    ),
    'Φ': lambda f, g, h: attrdict(
        arity = 1,
        call = lambda x: dyadic_link(g, (monadic_link(f, x), monadic_link(h, x)))
    ),
    #             1  2
    'Σ': lambda f, g: attrdict(
        arity = 1,
        call = lambda x: dyadic_link(g, (monadic_link(f, x), x))
    ),
    'B': lambda f, g: attrdict(
        arity = 1,
        call = lambda x: monadic_link(g, monadic_link(f, x))
    ),
    #           2  1
    'S': lambda f, g: attrdict(
        arity = 1,
        call = lambda x: dyadic_link(f, (x, monadic_link(g, x)))
    ),
    'W': lambda f: attrdict(
        arity = 1,
        call = lambda x: dyadic_link(f, (x, x))
    ),
    'I': lambda f: f,
    #           2  0 -> 1
    'bb': lambda f, g: attrdict(
        arity = 1,
        call = lambda x: dyadic_link(f, (x, niladic_link(g)))
    ),
    #            0  2 -> 1
    'bf': lambda f, g: attrdict(
        arity = 1,
        call = lambda x: dyadic_link(g, (niladic_link(f), x))
    ),
    #
    'Φₖ': lambda f, g, h: attrdict(
        arity = 1,
        call = lambda x: dyadic_link(g, (monadic_link(f, x), niladic_link(h))),
    )
}



jelly_dyadic_rules = {
    (2, 2, 2) : "Φ₁",
    (2, 2): "ε",
    (1, 2, 1): "D₂",
    (2, 1): "B₁",
    (1, 2, 2): "Φ.₂",
    (1, 2): "Δ",
    (1, 1): "B.₃",
    (2,): "I",
}

jelly_monadic_rules = {
    kkk,
    (1,): "I",
    (2, 0): "bb",
    (0, 2): "bf",
    (1, 2, 0): "Φₖ",
}

def get_arity(o):
    assert 0
    match o:
        case str(): return 1
        case FunctionTokens(arity): return arity


def apply_combinator(funcs, arity):
    rules = {1: jelly_monadic_rules, 2: jelly_dyadic_rules}[arity]
    arities = tuple(f.arity for f in funcs)
    rule = rules[arities]
    # index of function that shouldn't be constant: last argument or middle argument
    index = -1 if len(funcs) < 3 else 1
    if funcs[index].get("is_constant", False):
        raise Exception("Warning constant on non-leaf, you code doesn't make sense")
    return combinators[rule](*funcs)


def nest_left_branches(l):
    match l.data:
        case FunctionTokens(): return l
        case list():
            # TODO bind quicks here
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


def create_constant(arity, s):
    assert arity is not None
    # value = jelly.interpreter.create_literal(regex_liter.sub(parse_literal, s))
    value = ast.literal_eval(s)

    return attrdict(
        arity = arity,
        call = (lambda _, __: value) if arity == 2 else (lambda _: value),
        is_constant = True
    )

@dataclass
class hof_token:
    jello_token : str
    jelly_token : str
    arity : int
    
hof_arity = {
    "each":         1,
    "each_over":    1,
    "fold":         1,
    "chunk_fold":   2,
    "scan":         1,
    "slide_fold":   2,
    "prior":        1,
    "outer":        1,
    "w":            1,
    "c":            1,
    "filter":       1,
    "key":          1,
    "part":         1,
    "part_by":      1,
    "max_by":       1,

}

def FoldCombinatorTree(l, index, parent_arity = None):
    assert type(l) == FunctionTokens
    match l.data:
        case list(children):
            children = [FoldCombinatorTree(c, i, l.arity) for i, c in enumerate(children)]
            while (i := next((i for i, c in enumerate(children) if isinstance(c, hof_token)), None)) is not None:
                c : hof_token = children[i]
                hof_arguments = children[i+c.arity:i:-1] # should we have -1 or not ???
                children = children[:i+1] + children[i+1+c.arity:]
                
                if q := jelly.interpreter.quicks.get(c.jelly_token, None):
                    assert q.condition([a.link for a in hof_arguments])
                    link, = q.quicklink(hof_arguments, [], None) # return more than one links
                elif link := jelly.interpreter.hypers.get(c.jelly_token, None):
                    pass
                else: raise ValueError("hof not found")
                children[i] = HofWrapper(link, c.jelly_token, hof_arguments)
                if len(children) == 1: return children[0]
            
            link = apply_combinator([c.link for c in children], l.arity)
            return InteriorWrapper(link, index==0, children)
             
        case str(s):
            assert parent_arity is not None
            if link := jelly.interpreter.atoms.get(jello.to_jelly(s), None):
                pass
            elif jelly_token := jello_tokens.quick.get(s, None):
                return hof_token(s, jelly_token, hof_arity[s])
            else: link = create_constant(parent_arity, s)
            ret = LeafWrapper(link, s)
            return ret


if __name__ == "__main__":
    b = parse_parentheses("{add1 pair | add1 }")
    b = nest_left_branches(b)
    b = FoldCombinatorTree(b, 1, None)
    print(b)
    print(dyadic_link(b.link, (1, 10)))


def parse(code : str):
    return FoldCombinatorTree(nest_left_branches(parse_parentheses(code)), 1)

def puffer_eval(expr : InteriorWrapper, args, default_args):
    args_list = []
    for i in range(expr.link.arity):
        if i in args:
            args_list.append(args[i])
        elif i in default_args:
                args_list.append(default_args[i])
        else: raise ValueError(f"Neither an explicity or default argument in position {i} was provided")
    
    args_list = tuple(args_list)
    match expr.link.arity:
        case 1: return monadic_link(expr.link, args_list)
        case 2: return dyadic_link(expr.link, args_list)