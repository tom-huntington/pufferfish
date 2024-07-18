# <p align="center">🐡 Pufferfish 🐡</p>

Pufferfish is an alternative syntax for [Jello](https://github.com/codereport/jello)
/ 🪼 [Jellyfish](https://github.com/codereport/jellyfish) 🪼

Jello/Jellyfish is based on the idea that we an build up arbitrary functions by composing builtins (i.e. `sort`, `head`) with two variadic functions
```c++
std::is_unary_invocable auto F₁(std::is_invocable auto ...fns)
std::is_binary_invocable auto F₂(std::is_invocable auto ...fns)
```
For example:
```
F₁(F₁(F₁(F₁(tail sort) take 2) pair head) F₁(flat sum))
```

We can make calls to `F₁` and `F₂` implicit by using curly braces `{}` for `F₂` and parentheses `()` for `F₁`.

```
((((tail sort) take 2) pair head) (flat sum))
```
Closing parentheses `})` at the end of the scope are unnecessary to disambiguate the syntax.
We can replace the corresponding opening parenthesis/brace with `\`/`|` and omit the closing parenthesis/brace.

```
\ (((tail sort) take 2) pair head) \ flat sum
```

Opening parentheses `{(` at the start of the scope are again unnecessary to disambiguate the syntax.
We can replace the corresponding closing parenthesis/brace with `.`/`:` and omit the opening parenthesis/brace.

```
\ tail sort . take 2 . pair head . \ flat sum
```

It turns out that `F₁` and `F₂` only take at most 3 arguments.
We only need `.` and `:` to disambiguate the syntax when we are taking less than three arguments:
```
\ tail sort . take 2 pair head \ flat sum
```

# Examples