# <p align="center">🐡 Pufferfish 🐡</p>

An alternative syntax for [Jello](https://github.com/codereport/jello)
/ 🪼 [Jellyfish](https://github.com/codereport/jellyfish) 🪼

We can build functions by specifying trees where the leaf nodes are literals, and interior nodes are combinators.

Which combinator an interior node has is determined by both it's arity and the arities of it's children i.e. by our choice of a function `F`
```
F : (arity : Int) -> List Int -> Combinator arity
```

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




<style>

td:nth-child(2) {
    text-overflow: ellipsis;
    max-width: 200px;
    white-space: nowrap;
    overflow: hidden;
    /*word-wrap: ellipsis;*/
    /*overflow: hidden;*/
    /*white-space: nowrap;*/
    /*hyphens: auto;*/
}
</style>

| Column 1 | Column 2 | Column 3 |
|----------|----------|----------|
| Lorem ipsum dolor sit amet, consectetur adipiscing elit. Mauris eget eros vitae sem tristique convallis. | Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo. | Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum. |
