# <p align="center">🐡 Pufferfish 🐡</p>

Pufferfish is an alternative syntax for [Jello](https://github.com/codereport/jello)
/ 🪼 [Jellyfish](https://github.com/codereport/jellyfish) 🪼

Jello/Jellyfish is based on the idea that we an build up arbitrary functions by composing builtins (i.e. `sort`, `head`) with two variadic functions.
```c++
is_unary_invocable auto F₁(is_invocable auto ...fns)
is_binary_invocable auto F₂(is_invocable auto ...fns)
```
For example, consider the following [leetcode](https://leetcode.com/contest/biweekly-contest-122/problems/divide-an-array-into-subarrays-with-minimum-cost-i/) solution:
```
F₁(F₁(F₁(F₁(tail sort) take 2) pair head) F₁(flat sum))
```

We can make calls to `F₁` and `F₂` implicit by using parentheses `()` and curly braces `{}` to disambiguate whether we are calling `F₁` or `F₂` respectively

```
((((tail sort) take 2) pair head) (flat sum))
```
Closing parentheses, `)` and `}`, at the end of the scope are unnecessary to disambiguate the syntax.
We can replace the corresponding opening parenthesis with `\` and `|` respectively and omit the closing parenthesis.

```
\ (((tail sort) take 2) pair head) \ flat sum
```

Opening parentheses, `(` and `{`, at the start of the scope are again unnecessary to disambiguate the syntax.
We can replace the corresponding closing parenthesis with `.` and `:` respectively and omit the opening parenthesis.

```
\ tail sort . take 2 . pair head . \ flat sum
```

In fact our `F₁` and `F₂` only take at most three arguments. Only when we all applying `F₁` and `F₂` to less than three arguments is it necessary to make `.` and `:` explicit.
We can omit `.` and `:` when we have exactly three arguments:
```
\ tail sort . take 2 pair head \ flat sum
```

To help you read the code, pufferfish will print the combinator tree:
```
tail sort take 2 pair head flat sum
  ╰─┬──╯    │  │   │    │    ╰─┬─╯
    B       │  │   │    │      B
    ╰───┬───┴──╯   │    │      │
       Φₖ          │    │      │
        ╰────┬─────┴────╯      │
             Φ                 │
             ╰───┬─────────────╯
                 B
```

## Definition of `F₁` and `F₂`

`F₁` and `F₂` are solely determined by the arity of their arguments.
They can be described by the following tables for `F₁` and `F₂` respectively.

| Arities | Combinator | Definition |
| --- | --- | --- |
| (1, 2, 1) |  Φ  | `fn Φ(f,g,h) = x -> g(f(x),h(x))` |
| (1, 2) |  Σ  |  `fn Σ(f,g) = x -> g(x,f(x))` |
| (1, 1) |  B  |`fn b(f,g) = x -> g(f(x))` |
| (2, 1) |  S  | `fn s(f,g) = x -> f(g(x),x)` |
| (2,) |  W  | `fn w(f) = x -> f(x,x)` |


| Arities | Combinator | Definition |
| --- | --- | -- |
| (2, 2, 2)  |  Φ₁ | `fn Φ₁(f,g,h) = x,y -> g(f(x,y),h(x,y))` |
| (2, 2) |  ε | `fn ε(f,g) = x,y -> g(f(x,y), y)` |
| (1, 2, 1) |  D₂ | `fn d₂(f,g,h) = x,y -> f(g(x),h(y))` |
| (2, 1) |  B₁ |`fn b₁(f,g) = x,y -> g(f(x,y))` |
| (1, 2, 2) |  Φ.₂ | `fn Φ.₂(f,g,h) = x,y -> g(f(x),h(x,y))` |
| (1, 2) |  Δ |  `fn Δ(f,g) = x,y -> f(g(x),y)` |
| (1, 1) |  B.₃ | `fn (f,g) = x,y -> g(f(x))` |



### Other higher order functions
Jelly also has explicit higher order functions. Pufferfish requires you to specify the arity of the result by whether you use braces `{}` or parenthese `()` at the call site i.e. `hof_name(func1 func2)` for a monadic result.

# Examples
The solutions are [@codereport](https://github.com/codereport)'s https://github.com/codereport/jello/blob/main/challenges.md.
| Problem | Solution |
|---------|----------|
| [3005. Count Elements With Maximum Frequency](https://leetcode.com/contest/weekly-contest-380/problems/count-elements-with-maximum-frequency/) | `\ key{len} . \ idx_max at_idx . sum` |
| [3010. Divide an Array Into Subarrays With Minimum Cost I](https://leetcode.com/contest/biweekly-contest-122/problems/divide-an-array-into-subarrays-with-minimum-cost-i/) | `\ tail sort . take 2 pair head \ flat sum` |
| [3028. Ant on the Boundary](https://leetcode.com/contest/weekly-contest-383/problems/ant-on-the-boundary/) | `\ sums = 0 sum` |
| [3038. Maximum Number of Operations With the Same Score I](https://leetcode.com/contest/biweekly-contest-124/problems/maximum-number-of-operations-with-the-same-score-i/) | `\ len idiv 2 c{take} chunk_fold(+ 2) \ = head . sum` |
| [PWC 250 - Task 1: Smallest Index](https://theweeklychallenge.org/blog/perl-weekly-challenge-250/) | `\ len iota0 . mod 10 = . \| keep head` |
| [1365. How Many Numbers Are Smaller Than the Current Number](https://leetcode.com/problems/how-many-numbers-are-smaller-than-the-current-number/description/) | `\ w(outer{<}) each(sum)` |
| [1295. Find Numbers with Even Number of Digits](https://leetcode.com/problems/find-numbers-with-even-number-of-digits/) | `\ i_to_d \ len_each \ odd? \ not sum` |
| [2859. Sum of Values at Indices With K Set Bits](https://leetcode.com/problems/sum-of-values-at-indices-with-k-set-bits/description/) | `\| (len iota0 . bits) = r * l sum` |
