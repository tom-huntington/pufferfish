# <p align="center">🐡 Pufferfish 🐡</p>

Pufferfish is an alternative syntax for [Jello](https://github.com/codereport/jello)
/ 🪼 [Jellyfish](https://github.com/codereport/jellyfish) 🪼

Jello/Jellyfish is based on the idea that we an build up arbitrary functions by composing builtins (i.e. `sort`, `head`) with just two variadic functions
```c++
is_unary_invocable auto F₁(is_invocable auto ...fns)
is_binary_invocable auto F₂(is_invocable auto ...fns)
```
For example:
```
F₁(F₁(F₁(F₁(tail sort) take 2) pair head) F₁(flat sum))
```

We can make calls to `F₁` and `F₂` implicit by using parentheses `()` and curly braces `{}` to disambiguate whether we are calling `F₁` or `F₂` respectively

```
((((tail sort) take 2) pair head) (flat sum))
```
Closing parentheses (`)` and `}`) at the end of the scope are unnecessary to disambiguate the syntax.
We can replace the corresponding opening parenthesis with `\` and `|` respectively and omit the closing parenthesis.

```
\ (((tail sort) take 2) pair head) \ flat sum
```

Opening parentheses (`(` and `{`) at the start of the scope are again unnecessary to disambiguate the syntax.
We can replace the corresponding closing parenthesis with `.` and `:` respectively and omit the opening parenthesis.

```
\ tail sort . take 2 . pair head . \ flat sum
```

In fact our `F₁` and `F₂` only take at most three arguments. Only when we all applying `F₁` and `F₂` to less than three arguments is it necessary to make `.` and `:` explicit.
We can omit `.` and `:` when we have exactly three arguments:
```
\ tail sort . take 2 pair head \ flat sum
```

## `F₁` and `F₂`

`F₁` and `F₂` are solely determined by the arity of their arguments.
They can be described by the following tables

| Arities | Combinator |
| --- | --- |
| (1, 2, 1) |  Φ  |
| (1, 2) |  Σ  |
| (1, 1) |  B  |
| (2, 1) |  S  |
| (2,) |  W  |


| Arities | Combinator |
| --- | --- |
| (2, 2, 2)  |  Φ₁ |
| (2, 2) |  ε |
| (1, 2, 1) |  D₂ |
| (2, 1) |  B₁ |
| (1, 2, 2) |  Φ.₂ |
| (1, 2) |  Δ |
| (1, 1) |  B.₃ |


| Name | Arites | Definition |
| --- | -------   | --- |
| W  |   2→1   |   `fn w(f) = x -> f(x,x)` |
| C  |   2→2   |   `fn c(f) = x,y -> f(y,x)` |
| B  |   11→1   |  `fn b(f,g) = x -> g(f(x))` |
| B₁  |  21→2   |  `fn b₁(f,g) = x,y -> g(f(x,y))` |
| Σ  |   12→1   |  `fn s(f,g) = x -> g(x,f(x))` |
| S  |   21→1   |  `fn Σ(f,g) = x -> f(g(x),x)` |
| D  |   21→2   |  `fn d(f,g) = x,y -> f(x,g(y))` |
| Δ  |   12→2   |  `fn Δ(f,g) = x,y -> f(g(x),y)` |
| Ψ  |   21→2   |  `fn Ψ(f,g) = x,y -> g(f(x),f(y))` |
| Φ  |   121→1   | `fn Φ(f,g,h) = x -> g(f(x),h(x))` |
| D₂  |  121→2   | `fn d₂(f,g,h) = x,y -> f(g(x),h(y))` |
| Φ.₂  | 122→2   | `fn Φ.₂(f,g,h) = x,y -> g(f(x),h(x,y))` |
| Φ₁  |  222→2   | `fn Φ₁(f,g,h) = x,y -> g(f(x,y),h(x,y))` |

# Examples
| Problem | Solution |
|---------|----------|
| [3005. Count Elements With Maximum Frequency](https://leetcode.com/contest/weekly-contest-380/problems/count-elements-with-maximum-frequency/) | `\ key{len} . \ idx_max at_idx . sum` |
| [3010. Divide an Array Into Subarrays With Minimum Cost I](https://leetcode.com/contest/biweekly-contest-122/problems/divide-an-array-into-subarrays-with-minimum-cost-i/) | `\ tail sort . take 2 pair head \ flat sum` |
| [3028. Ant on the Boundary](https://leetcode.com/contest/weekly-contest-383/problems/ant-on-the-boundary/) | `\ sums = 0 sum` |
| [3038. Maximum Number of Operations With the Same Score I](https://leetcode.com/contest/biweekly-contest-124/problems/maximum-number-of-operations-with-the-same-score-i/) | `\ len idiv 2 c{take} chunk_fold(+ 2) \ = head . sum` |
