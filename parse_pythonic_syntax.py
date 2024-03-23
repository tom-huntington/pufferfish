from main import FunctionTokens, FoldCombinatorTree, dyadic_link
import itertools
import functools
import re
a1 = """\
. a b
  c : e f
      g
    h
  i
j k
l
"""
a = """\
: add1 : add1
      pair
    add1
  pair
pair pair
add1
"""

a = a[:-1] if a[-1] == '\n' else a
# a = a[2:]
lines = a.split('\n')

def split_on_predicate(lst, predicate):
    result = []
    current_group = []

    for item in lst:
        if predicate(item):
            result.append(current_group)
            current_group = []
        current_group.append(item)

    if current_group:
        result.append(current_group)

    return result[1:]

def parse_right_branch(lines : list[str]) -> FunctionTokens:
    spec, sp, *lines[0] = lines[0]
    assert sp == ' ', "Expected space"
    assert not lines[0][0].isspace(), "Expected only one space"

    match spec:
            case '.': arity = 1
            case ':': arity = 2
            case _: raise Exception(f"Parsing error. Need to start with monadic or dyadic specifier. Got {spec}")

def parse_combinator(lines: list[str], arity):
    def split_first(l):
        match = re.search(r'[:.]', l)
        if match:
            s = match.start()
            return [l[:s], '  ' + l[s:]]
        return [l]
    flat_map = lambda f, xs: [y for ys in xs for y in f(ys)]
    a = list(flat_map(split_first, lines))
    grou = list([k, list(v)] for k,v in itertools.groupby(a, key=lambda x: x[0] == ' '))
    z = 0
    linegroups = list(itertools.chain.from_iterable(([parse_indented_subtree(list(v))] if k == True else parse_leaves(list(v))) for k, v in grou))
    return FunctionTokens(arity, linegroups)
    
def parse_leaves(l : list[str]):
    return [FunctionTokens(None, s)
                for st in l
                for s in st.split(' ') if s != '']
    # return list(map(lambda s: FunctionTokens(None, s), string.split(' ')))

def deindent(line):
        assert line[0] == ' ' and line[1] == ' '
        return line[2:]

def parse_indented_subtree(lines):
    temp = list(map(deindent, lines))
    ret = parse_function(temp)
    return ret


def parse_function(lines):
    separator = lines[0][0]
    assert lines[0][1] == ' '
    lines[0] = lines[0][2:]
    match separator:
         case '.': arity = 1
         case ':': arity = 2
         case _: raise ValueError("expected : or .")
    r = parse_left_branches(lines, arity)
    return r

def parse_left_branches(lines : list[str], arity : int) -> FunctionTokens:
    index = 0 
    # index = lines.find(lambda x: not x.isspace())
    assert len(lines) > 0
    if len(lines) == 1:
         return parse_leaves(lines[0])
    
    b = split_on_predicate(lines, lambda l: l[0] != ' ')
    
    e2 = [f"{h=}, {t=}" for h, *t in b]
    left_branches = [[h, *map(deindent, t)] for h, *t in b]


    z = 0
    
    c = [parse_combinator(l, arity) for l in left_branches]
    d = functools.reduce(lambda head, tail: FunctionTokens(arity, [head, *tail.data]), c)
    print(d)
    return d


out = parse_function(lines)
b  = FoldCombinatorTree(out, 1)
print(dyadic_link(b.link, (1, 10)))
z = 0
