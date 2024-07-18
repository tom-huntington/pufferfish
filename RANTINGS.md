# Notes
The syntax is either explicit (`.` and `:`) or regular.
You do *not* need to know the arities to determine the combinator groupings.
(although you do need to know arities to determine which combinator results from a group)


We can build functions by specifying trees where the leaf nodes are literals, and interior nodes are combinators.

Which combinator an interior node has is determined by both it's arity and the arities of it's children i.e. by our choice of a function `F`


We can then fold any such tree down into single function. Composition is all you need.


Since our trees are left leaning we will optimize our syntax for this and introduce `|` as a `cons` operator
```
[[[a b] c d] e] == [a b | c d | e]
```

We will also specify the arity, using parentheses `()` for trees that fold to monadic (unary) functions, and `{}` parentheses for trees that fold to dyadic (binary) functions. Again we will make an optimization for left leaning trees: combinators on the left branch will inherit their arity form their parent.

TODO:
- [ ] Python syntax using indenting and line breaks to replace Lisp style nested parentheses
- [ ] Read Buffer Evaluate Loop
- [ ] Plot the combinator trees in terminal



# Notes

To read code, there programmer must parse the operator precedence, associativity and arity.
These operator languages can be different levels in the chompsky hierachy.

Take for example a language where all operators are binary and have the same level of precedence and are all left associative.

To parse the operator all is necessary is to determine whether an identifier is even or odd.
```
a   b c  d f  g h
0   1 2  3 4  5 6
((a b c) d f) g h
```
Odd identifiers are the operators, even identifiers are the operands.
The left operand is whatever the expression of everything on the left evaluates to.

This is a regular grammar.

However, in languages with ambivalence the operator grammar becomes context sentitive.
The arity of an identifier changes depending on the previous context.

Jelly removes ambivalence but the pattern matching rules once again mean the what combinator the identifier is a operand of (and what position it is in) changes depending on the previous context.

The operator grammar being context sentitive makes array language very hard to read.

Pufferfish solves this by the Lisp way by explicitly specifying the parentheses.


