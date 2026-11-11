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
