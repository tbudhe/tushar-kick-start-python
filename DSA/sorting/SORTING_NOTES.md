# Sorting Notes

## 2026-10-31 — Basic O(n²) sorts (`basic_sorts.py`)

| Sort | One-line idea | Best | Worst | Space | Stable? |
|---|---|---|---|---|---|
| Selection | Find the min of the unsorted part, swap it to position `i` | O(n²) | O(n²) | O(1) | No |
| Bubble | Swap ADJACENT pairs; the biggest "bubbles" to the end each pass | O(n) with early exit | O(n²) | O(1) | Yes |
| Insertion | Take `nums[i]`, shift bigger items right, drop it in the gap | O(n) (already sorted) | O(n²) | O(1) | Yes |

### Say it out loud
- **Selection:** fewest swaps (n−1 max) — useful when writes are expensive.
- **Insertion:** best on nearly-sorted data; Python's built-in Timsort uses it for small runs.
- **Bubble:** mostly a teaching sort; its only edge is the early exit when a pass makes no swaps.

### ⚠️ Fix owed: my `bubble_sort` is really exchange sort
It compares `nums[i]` with every `nums[j]` — that's not bubble sort. An interviewer will catch it.
Real bubble sort compares neighbours `nums[j]` and `nums[j+1]`, and each pass shrinks the range by one:

```python
def bubble_sort(nums: list[int]) -> list[int]:
    n = len(nums)
    for i in range(n):
        swapped = False
        for j in range(n - 1 - i):          # last i items are already in place
            if nums[j] > nums[j + 1]:
                nums[j], nums[j + 1] = nums[j + 1], nums[j]
                swapped = True
        if not swapped:                     # no swaps = sorted -> O(n) best case
            break
    return nums
```

### Small Python habit
Type hint is `list[int]`, not `[int]` (`[int]` runs, but it's a list containing the type, not a type).

---

## 2026-10-31 — Merge sort (`merge_sort.py`) ✅ correct first try

**Idea:** split in half until size 1, then merge two sorted halves with two pointers.

| Best | Worst | Space | Stable? |
|---|---|---|---|
| O(n log n) | O(n log n) | O(n) extra | Yes |

### Say it out loud
- "log n levels of splitting, O(n) merge work per level → O(n log n), every case."
- "`<=` in the merge keeps it stable — on a tie, the LEFT item goes first."
- "The trade-off vs quicksort: guaranteed O(n log n) and stable, but needs O(n) extra memory."
- Where it shows up: sorting linked lists, external sort (data bigger than RAM — sort chunks, merge from disk), and Timsort's merge step.

### Code notes
- Base case `len(nums) <= 1` — stops the recursion; a 1-item list is already sorted.
- The 3 while loops: main merge, then drain whatever is left in `left`, then `right`. Only one of the two drain loops actually runs.
- `nums[:mid]` copies the list — that slicing is where the O(n) extra space comes from.
- `merge` writes back into `nums`, so the top-level call also sorts the caller's list in place.

---

## 2026-10-31 — Quick sort (`quick_sort.py`) — logic ✅, one fix owed

**Idea:** pick a pivot (last item), move everything `<= pivot` to its left, drop the pivot in its final spot, recurse on both sides.

| Best / Avg | Worst | Space | Stable? |
|---|---|---|---|
| O(n log n) | O(n²) | O(log n) stack | No |

### ⚠️ Fix owed: prints `None`
The sort itself is correct (it sorts the list in place), but `quick_sort()` has no `return`, and a Python function with no return gives back `None` — same as a JS function with no `return` gives `undefined`.
Fix: add `return nums` as the last line of `quick_sort`.
Prevent it: decide up front — "in-place, returns nothing" (like `list.sort()`) OR "returns the list" (like `sorted()`). Pick one and make the print match.

### Say it out loud
- "Partition puts the pivot in its final position — left side ≤ pivot, right side > pivot."
- "Worst case O(n²) happens when the pivot is always the min or max — e.g. already-sorted input with last-element pivot. Fix: random pivot or median-of-three."
- "Quick vs merge: quick sorts in place (O(log n) stack, no copies) and is usually faster in practice; merge is stable and guarantees O(n log n)."

### Code notes (Lomuto partition)
- `i` = last index of the "≤ pivot" zone. Starts at `low - 1` = zone is empty.
- Each `nums[j] <= pivot` → grow the zone (`i += 1`) and swap `nums[j]` into it.
- After the loop, `i + 1` is the first slot after the zone → swap the pivot there; that's its final spot.
- Recurse on `low..pi-1` and `pi+1..high` — the pivot itself is never touched again.

---

## 2026-10-31 — LeetCode set: sorting + heaps

Solved: 912, 1167, 252, 1213, 88, 703, 215, 937. Code saved in `DSA/leetcode/` for 252 and 215.

| LC | Problem | Pattern | Key line |
|---|---|---|---|
| 912 | Sort an Array | merge / quick sort | Must be O(n log n) — plain quicksort can hit O(n²) on sorted input; merge sort is safe |
| 1167 | Min Cost to Connect Sticks | min-heap, greedy | Always join the two smallest — pop 2, push their sum |
| 252 | Meeting Rooms | sort by start, check neighbours | Sort by start; conflict if `prev.end > curr.start` (equal = no conflict) |
| 1213 | Intersection of Three Sorted Arrays | three pointers | Move the pointer with the smallest value |
| 88 | Merge Sorted Array | two pointers from the END | Fill from the back so you never overwrite unread `nums1` values |
| 703 | Kth Largest in a Stream | min-heap of size k | Heap top = kth largest |
| 215 | Kth Largest in an Array | min-heap of size k | Push, pop when size > k → O(n log k), O(k) space |
| 937 | Reorder Log Files | custom sort key | Key returns a tuple: letter logs `(0, content, id)`, digit logs `(1,)` — stable sort keeps digit order |

### Say it out loud
- **252:** "Sort by start time; after sorting, only neighbours can overlap. O(n log n)."
- **215 / 703:** "Keep a min-heap of size k — the smallest of the top k sits on top, so `pq[0]` is the kth largest. O(n log k) beats sorting's O(n log n) when k is small."
- **Why a MIN-heap for the k LARGEST:** the heap is a bouncer — the weakest of the top k is at the door and gets kicked out first.

### Code notes
- 215 `findKthLargestOld` (sort) is O(n log n) and mutates the input — fine as the brute-force answer to say first.
- 252: `hasConflicts` as a `@staticmethod` is clean; `end > start` (not `>=`) is the right call — a meeting ending at 10 and one starting at 10 don't clash.
- Python heaps are MIN-heaps only. For a max-heap, push `-num`.

---

## 2026-11-02 — In-place partitioning with pointers (`two_pointer_partition.py`)

All three passed 500 random tests. One question to settle on segregate.

| Problem | Pattern | Time / Space | Key line |
|---|---|---|---|
| Segregate evens & odds | 2 pointers from both ends | O(n) / O(1) | Left skips what belongs left, right skips what belongs right, swap when both are stuck |
| Merge one sorted array into another | 3 pointers from the END | O(n) / O(1) | Fill from the back — the zeros are free space, so nothing unread gets overwritten (same as LC 88) |
| Dutch National Flag | 3 pointers: `ri`, `gi`, `bi` | O(n) / O(1), one pass | R → swap to front, both move; B → swap to back, ONLY `bi` moves; G → `gi` moves |

### ⚠️ Segregate: check which side the task wants
My code puts **odds first**: `[1, 2, 3, 4]` → `[1, 3, 2, 4]`. The usual version of this problem wants **evens first**.
For evens first, flip the two skip checks: skip `numbers[l] % 2 == 0` on the left and `numbers[r] % 2 != 0` on the right.
Also: the inner `else: l += 1` can never run — the two checks above it already guarantee left is even and right is odd. The swap needs no `if`.

### Say it out loud
- **Dutch flag:** "Three zones: everything before `ri` is red, between `ri` and `gi` is green, after `bi` is blue, and `gi..bi` is unknown. Each step shrinks the unknown zone by one."
- **Why `gi` does NOT move after a blue swap:** the ball swapped in from the back hasn't been looked at yet. After a red swap it HAS been seen (it came from the green zone), so `gi` moves.
- **Merge into another:** "Fill from the back so you never overwrite a number you still need."

### Code notes
- Merge: the last `while ni >= 0` loop never actually moves anything — those items are already in place. Harmless; mention it if asked.
- Dutch flag is quicksort's partition with 3 zones instead of 2 — it's the fix for quicksort on inputs with lots of duplicates.
