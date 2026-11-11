# Recursion Notes

## Subsets II (LC 90), 2026-11-03
- File: DSA/recursion/subset.ii.py
- Signal: input may contain duplicates + output must be unique + order inside a result doesn't matter
- Template: loop + start, one recursive call dfs(i + 1, path), record path[:] at the top
- Key lines: nums.sort() before dfs; skip when i > start and nums[i] == nums[i-1]
- Why i > start: duplicates are siblings in the recursion tree (same loop/slot). i == start is the first candidate for a slot, so always allowed; i > start with the same value as the one before is a repeat for the same slot, so skip it
- No used[] needed: that's for Permutations (loop from 0)
- Complexity: Time O(n * 2^n) (2^n subsets x n copy cost, plus n log n sort). Space O(n) auxiliary (call stack + path), output O(n * 2^n)

## Letter Combinations of a Phone Number (LC 17) — 2026-11-11

**Signal:** each position in the input has its own set of choices (digit -> letters). One level per position.

**Knobs**
| Knob | Setting |
|---|---|
| Loop over | letters of PHONE[digits[index]] |
| Recurse with | index + 1 |
| Record when | index == len(digits) |
| Skip condition | none |

**My code**
```python
class Solution:
    def letterCombinations(self, digits: str) -> list[str]:
        n = len(digits)
        PHONE = {
            "2": "abc", "3": "def", "4": "ghi", "5": "jkl",
            "6": "mno", "7": "pqrs", "8": "tuv", "9": "wxyz",
        }
        result = []
        if n == 0:
            return result

        def dfs(st, path):
            if st >= n:
                result.append(path)
                return
            number = digits[st]
            keys = PHONE[number]
            for key in keys:
                dfs(st + 1, path + key)

        dfs(0, "")
        return result


solution = Solution()
print(solution.letterCombinations('23'))  # ['ad', 'ae', 'af', 'bd', 'be', 'bf', 'cd', 'ce', 'cf']
print(solution.letterCombinations('2'))   # ['a', 'b', 'c']
print(solution.letterCombinations(''))    # []
```

**Complexity**
- Time: O(n * 4^n) — 4 choices per level (digits 7 and 9), n levels, n work to build each string
- Auxiliary space: O(n) recursion depth
- Output space: O(n * 4^n)

**My mistakes**
- Skipped the "" example; it returned [''] instead of []
- Read [''] as [] — they are different (length 1 vs length 0)
- Reused 2^n from Subsets instead of deriving choices^levels
- Used default arguments on dfs; pass dfs(0, "") explicitly

**Interview lines**
- "This is a DFS where each level is one digit, and I branch over that digit's letters."
- "There's no start index and no skip condition, because each position draws from its own set of letters."
- "I record a result when the index reaches the length of the input."
- "Strings are immutable in Python, so I pass path + letter and don't need to pop or copy."
- "Empty input returns an empty list, so I guard for it before recursing."
- "Time is O(n * 4^n), auxiliary space is O(n) for the recursion depth."

**Re-solve dates:** 11/14, 11/18, 11/25

## Palindrome Partitioning (LC 131) — 2026-11-11

**Signal:** cut a string into pieces where every piece must pass a check. Partitioning means choosing where to cut. The letters never move, so this is NOT permutations.

**Picture:** a string of length n has n-1 gaps. Each gap is cut or not cut.
"aab" -> 2 gaps -> 4 ways: aab ✗ | a,ab ✗ | aa,b ✓ | a,a,b ✓

**Knobs**
| Knob | Setting |
|---|---|
| Loop over | i from start + 1 to len(s), inclusive |
| Piece | s[start:i] |
| Skip when | piece is not a palindrome (continue) |
| Recurse with | i (slice excludes i, so i is the first unused character) |
| Record when | start >= len(s) |

**My code**
```python
class Solution:
    def partition(self, s: str) -> list[list[str]]:
        n = len(s)
        result = []

        def dfs(start, path):
            if start>=n:
                result.append(path[:])
                return

            for i in range(start + 1, n + 1):
                piece = s[start:i]
                if piece != piece[::-1]:
                    continue
                path.append(piece)
                dfs(i,path)
                path.pop()

        dfs(0, [])
        return result

solution = Solution()
print(solution.partition("aab"))  # [['a', 'a', 'b'], ['aa', 'b']]
print(solution.partition("a"))    # [['a']]
print(solution.partition("aba"))  # [['a', 'b', 'a'], ['aba']]
```

**Python string notes**
- s[start:i] stops before index i (same as s.slice(start, i) in TypeScript)
- piece[::-1] reverses a string; piece == piece[::-1] is the palindrome check
- range(start + 1, n + 1): the + 1 is needed because range stops one short
- Strings are immutable: s[i] = "" raises TypeError. Never edit s, only path.

**Complexity**
- Time: O(n * 2^n) — n-1 gaps, each cut or not, n work per partition
- Auxiliary space: O(n) for recursion depth and path

**My mistakes**
- Thought it needed permutations (asked why "baa" was missing)
- Tried to edit the string instead of append/pop on path
- result.push(path) — push is JavaScript; Python is append, with path[:]
- Typo path.appened, and deleted return result — both caught only by running

**Interview lines**
- "Partitioning means choosing where to cut. The letters never move, so this is not permutations."
- "At each level I stand at start and try every possible end for the next piece."
- "I only recurse if the piece is a palindrome, so invalid branches are pruned early."
- "I record a copy of the path when start reaches the end of the string."
- "There are n minus 1 gaps, each cut or not, so time is O(n * 2^n) with O(n) auxiliary space."

## Backtracking skeleton (one template, five slots)

```python
def dfs(start, path):
    if DONE:
        result.append(path[:])
        return
    for i in range(...):
        if NOT_ALLOWED:
            continue
        path.append(CHOICE)
        dfs(NEXT, path)
        path.pop()
```

| Slot | Combination Sum II | Palindrome Partitioning |
|---|---|---|
| DONE | target == 0 | start >= n |
| Loop | range(start, n) | range(start + 1, n + 1) |
| NOT_ALLOWED | duplicate value | piece != piece[::-1] |
| CHOICE | candidates[i] | s[start:i] |
| NEXT | i + 1 | i |

**Re-solve dates:** 11/11 evening (blank file, 15 min), 11/14, 11/18, 11/25
