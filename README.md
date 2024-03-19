# <p align="center">🐡 Pufferfish 🐡</p>

An alternative syntax for [Jello](https://github.com/codereport/jello)
/[Jellyfish](https://github.com/codereport/jellyfish)

We build functions by specifying trees where the leaf nodes are literals, and interior nodes are combinators.

Combinators are determined by our choice of a function `F`
```
F ∘ (map arity) :: List<Callable> -> Combinator
```

We can then fold any such tree down into single function. Composition is all you need.


Since our trees are left leaning we will optimize our syntax for this and introduce `|` as a `cons` operator
```
[[[a b] c d] e] == [a b | c d | e]
```

We will also specify the arity, using parentheses `()` for trees that fold to monadic (unary) functions, and `{}` parentheses for trees that fold to dyadic (binary) functions.