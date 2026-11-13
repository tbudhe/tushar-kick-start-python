# NUMPY_STATUS.md — NumPy daily drills (SINGLE SOURCE OF TRUTH for NumPy)

Last Updated: 2026-11-13 (Drill 1 done)
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
Next drill: **Drill 2 — axis** (mean per column vs mean per row)

## LADDER
| # | Topic | Status |
|---|---|---|
| 1 | np.array, .shape, arr * 2, arr[0], arr[1, 2] | DONE 2026-11-13 |
| 2 | axis: .mean(axis=0) vs .mean(axis=1) | next |
| 3 | broadcasting (array + row, array * column) | |
| 4 | boolean masks (arr[arr > 3]) | |
| 5 | dot product + cosine similarity | |
| 6 | argsort -> top-k indices | |
| 7 | softmax | |
| 8 | normalize (L2 / min-max) | |
| 9+ | mixed interview problems (timed) | |

## DRILL LOG (max 3 lines each)
### Drill 1 — 2026-11-13 — arrays and shape
- `arr = np.array(data)` — must ASSIGN it; `np.array(data)` alone builds it and throws it away (like `.map()` without assigning in JS).
- `arr.shape` = (rows, columns); a plain Python list has no `.shape`.
- `arr * 2` = math on every element, no loop. `arr[1, 2]` = row 1, col 2 (JS: `data[1][2]`).

## KEY RULES TO REMEMBER
- Always `import numpy as np`.
- First move on any NumPy interview problem: check `.shape`.
- `axis` = the direction that gets COLLAPSED (axis=0 squashes rows -> one value per column).
