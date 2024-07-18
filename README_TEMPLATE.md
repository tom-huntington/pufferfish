# <p align="center">🐡 Pufferfish 🐡</p>

Pufferfish is an alternative syntax for [Jello](https://github.com/codereport/jello)
/ 🪼 [Jellyfish](https://github.com/codereport/jellyfish) 🪼

Jello/Jellyfish is based on the idea that we an build up arbitrary functions by composing builtins (i.e. `sort`, `head`) with two variadic functions (higher order).
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

### `F₁` and `F₂`

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
| (2, 2) |  ε | `fn = ε(f,g) = x,y -> g(f(x,y), y)` |
| (1, 2, 1) |  D₂ | `fn d₂(f,g,h) = x,y -> f(g(x),h(y))` |
| (2, 1) |  B₁ |`fn b₁(f,g) = x,y -> g(f(x,y))` |
| (1, 2, 2) |  Φ.₂ | `fn Φ.₂(f,g,h) = x,y -> g(f(x),h(x,y))` |
| (1, 2) |  Δ |  `fn Δ(f,g) = x,y -> f(g(x),y)` |
| (1, 1) |  B.₃ | `fn (f,g) = x,y -> g(f(x))` |



### Other higher order functions
Jelly also has explicit higher order functions. Pufferfish requires you to specify the arity of the result by whether you use braces `{}` or parenthese `()` at the call size i.e. `hof_name(func1 func2)` for a monadic result.

# Examples