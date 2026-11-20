# NUMPY_STATUS.md — NumPy daily drills (SINGLE SOURCE OF TRUTH for NumPy)

Last Updated: 2026-11-20 (Drill 5 done - zeros/ones/eye/dtype + diag)
Linked from: STATUS.md -> "NUMPY DAILY" line (this file lives at repo root)

## WHY
Interview gap with evidence: ServiceNow DSA round (2026-11-05) gave a NumPy problem;
I switched to TypeScript because I wasn't comfortable. Goal: NumPy muscle memory for interviews.

## FORMAT (every day, 10 min)
- One drill = one file: `numpy_drills/drillNN.py`
- Goal printout shown FIRST, then I TYPE the code myself (no paste)
- Run: `python numpy_drills/drillNN.py`
- One new idea per drill. Started from zero on 2026-11-13.

## CURRENT POSITION
Next drill: **Drill 6 — concatenate (axis), stacking**

## LADDER (two goals: HackerRank NumPy track + AI-style NumPy)
| # | Topic | Status |
|---|---|---|
| 1 | np.array, .shape, arr * 2, arr[0], arr[1, 2] | DONE 2026-11-13 |
| 2 | axis: .mean(axis=0) vs .mean(axis=1) | DONE 2026-11-16 |
| 3 | HackerRank input: read stdin -> np.array (`input().split()`, `map(int, ...)`) | DONE 2026-11-17 |
| 4 | reshape, transpose, flatten | DONE 2026-11-18 |
| 5 | zeros / ones / eye / identity, dtype | DONE 2026-11-20 |
| 6 | concatenate (axis), stacking | next |
| 7 | element-wise math, floor / ceil / rint, sum / prod / min / max | |
| 8 | mean / var / std | |
| 9 | broadcasting (array + row, array * column) | |
| 10 | boolean masks (arr[arr > 3]) | |
| 11 | dot / cross / inner / outer | |
| 12 | dot product -> cosine similarity | |
| 13 | argsort -> top-k indices | |
| 14 | softmax, normalize (L2 / min-max) | |
| 15+ | timed mixed problems: HackerRank NumPy track, then AI-style problems | |

## DRILL LOG (max 3 lines each)
### Drill 1 — 2026-11-13 — arrays and shape
- `arr = np.array(data)` — must ASSIGN it; `np.array(data)` alone builds it and throws it away (like `.map()` without assigning in JS).
- `arr.shape` = (rows, columns); a plain Python list has no `.shape`.
- `arr * 2` = math on every element, no loop. `arr[1, 2]` = row 1, col 2 (JS: `data[1][2]`).

### Drill 2 — 2026-11-16 — axis
- `arr.mean(axis=0)` = one answer per COLUMN (the totals row at the bottom of a spreadsheet) -> [2. 3. 4. 5.].
- `arr.mean(axis=1)` = one answer per ROW (the totals column on the right) -> [2.5 3.5 4.5].
- axis = the direction that gets squashed. Both predictions matched on first run.

### Drill 4 — 2026-11-18 — reshape, transpose, flatten
- `arr.reshape(2, 3)` = same 6 numbers, new grid; rows x cols MUST equal size -> `reshape(4, 2)` on 6 items = ValueError.
- `reshape(-1, 2)` = "you work out the rows" -> (3, 2). `.T` swaps rows/cols (2,3)->(3,2), like Excel paste-transpose.
- `.flatten()` = back to 1-D. All printouts matched on first run.

### Drill 5 — 2026-11-20 — zeros, ones, eye, dtype, diag
- `np.zeros((2, 3))` = float (`0.`); `np.ones((2, 3), dtype=int)`; shape is ONE tuple - `np.zeros(2, 3)` = TypeError (2nd arg is dtype).
- `np.eye(3, k=1)` shifts the diagonal. `np.diag(a)` reads (2-D) / builds (1-D); anti-diagonal = `np.diag(np.fliplr(a))`; `np.trace(a)` = sum.
- My bug: `print(np.diag(ones), k=1)` - kwarg went to print. Put it before the inner `)`.

## KEY RULES TO REMEMBER
- Always `import numpy as np`.
- First move on any NumPy interview problem: check `.shape`.
- `axis` = the direction that gets COLLAPSED (axis=0 squashes rows -> one value per column).
