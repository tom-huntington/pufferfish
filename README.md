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
| Problem | Solution |
|---------|----------|
| [3005. Count Elements With Maximum Frequency](https://leetcode.com/contest/weekly-contest-380/problems/count-elements-with-maximum-frequency/) | `\ key{len} . \ idx_max at_idx . sum` |
| [3010. Divide an Array Into Subarrays With Minimum Cost I](https://leetcode.com/contest/biweekly-contest-122/problems/divide-an-array-into-subarrays-with-minimum-cost-i/) | `\ tail sort . take 2 pair head \ flat sum` |
| [3028. Ant on the Boundary](https://leetcode.com/contest/weekly-contest-383/problems/ant-on-the-boundary/) | `\ sums = 0 sum` |
| [3038. Maximum Number of Operations With the Same Score I](https://leetcode.com/contest/biweekly-contest-124/problems/maximum-number-of-operations-with-the-same-score-i/) | `\ len idiv 2 c{take} chunk_fold(+ 2) \ = head . sum` |
