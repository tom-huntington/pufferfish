import jello
import jelly
from jello import utils
from jelly.interpreter import *

def parse_code_(code):
    lines = regex_flink.findall(code)
    links = [[] for line in lines]
    for index, line in enumerate(lines):
        chains = links[index]
        flat_map = lambda f, xs: [y for ys in xs for y in f(ys)]
        words = flat_map(lambda s: s[1:] if s[0] == "Θ" else [s], regex_chain.findall(line))
        for word in words:
            chain = []
            arity, start, is_forward = chain_separators.get(word[:1], default_chain_separation)
            for token in regex_token.findall(start + word):
                if token in atoms:
                    chain.append(atoms[token])
                elif token in quicks:
                    popped = []
                    while not quicks[token].condition(popped) and (chain or chains):
                        popped.insert(0, chain.pop() if chain else chains.pop())
                    chain += quicks[token].quicklink(popped, links, index)
                elif token in hypers:
                    x = chain.pop() if chain else chains.pop()
                    chain.append(hypers[token](x, links))
                else:
                    chain.append(create_literal(regex_liter.sub(parse_literal, token)))
            chains.append(create_chain(chain, arity, is_forward))
    return links


def jelly_eval(code, arguments):
    return variadic_chain(parse_code_(code)[-1] if code else "", arguments)

expr = 'add1 pair pair'
a = utils.remove_all(utils.split_keep_multiple_delimiters(expr, r" \(\)"), ["", " "])
res = jelly_eval(jello.convert(a), [1,10])
print(res)
