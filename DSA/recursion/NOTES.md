# Recursion Notes

## Subsets II (LC 90), 2026-11-03
- File: DSA/recursion/subset.ii.py
- Signal: input may contain duplicates + output must be unique + order inside a result doesn't matter
- Template: loop + start, one recursive call dfs(i + 1, path), record path[:] at the top
- Key lines: nums.sort() before dfs; skip when i > start and nums[i] == nums[i-1]
- Why i > start: duplicates are siblings in the recursion tree (same loop/slot). i == start is the first candidate for a slot, so always allowed; i > start with the same value as the one before is a repeat for the same slot, so skip it
- No used[] needed: that's for Permutations (loop from 0)
- Complexity: Time O(n * 2^n) (2^n subsets x n copy cost, plus n log n sort). Space O(n) auxiliary (call stack + path), output O(n * 2^n)
