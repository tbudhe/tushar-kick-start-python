# Graph Patterns Plan

Started: 2026-10-26 · Pace: 1 pattern/session, review after #4 and #8 → ~10 sessions, target ~Nov 13

## The 3 questions (ask before every graph problem)
1. What is a **node**?
2. What is an **edge**?
3. What is the **ask**? reach · shortest · order · groups · cheapest → this picks the pattern

## Patterns

| # | Pattern | Signal in the question | Anchor problem | Status |
|---|---|---|---|---|
| 1 | DFS/BFS traversal | count regions / can I reach | LC 200 Number of Islands | ✅ 2026-10-26 |
| 2 | Multi-source BFS | everything spreads at once | LC 994 Rotting Oranges | ✅ 2026-10-26 |
| 3 | BFS shortest path (unweighted) | minimum steps | LC 127 Word Ladder | ✅ 2026-10-27 |
| 4 | Topological sort | order / prereqs possible? | LC 207 / 210 Course Schedule | ⏭ next |
| — | Review 1–4 | mixed, timed | | |
| 5 | Union-Find | connected? / groups merge | LC 684 Redundant Connection | |
| 6 | Bipartite / 2-coloring | split into two teams | LC 785 Is Graph Bipartite | |
| 7 | Dijkstra | cheapest path, weights ≥ 0 | LC 743 Network Delay Time | |
| 8 | Bellman-Ford / bounded BFS | cheapest with ≤ K stops | LC 787 Cheapest Flights | |
| — | Review 5–8 | mixed, timed | | |

## Directed or undirected?
If A connects to B, does B automatically connect to A? Yes → undirected (add both edges). No → directed.
Directed clues: prerequisite, depends on, from u to v, one-way, follows, `[u, v, w]`.

## BFS checklist (run before every BFS)
1. Queue seeded with start node
2. `visited` seeded with start node
3. `popleft()`, not `pop()`
4. Mark visited when you ENQUEUE, not when you pop
5. Return on reaching target + fallback return AFTER the loop

## Python ↔ JS cheat sheet
| Python | JS |
|---|---|
| `deque([(0, 0)])` (takes a collection) | `[[0, 0]]` |
| `q.append((r, c))` (takes ONE item) | `q.push([r, c])` |
| `q.popleft()` / `q.pop()` | `q.shift()` / `q.pop()` |
| `s.add(x)`, `x in s` | `s.add(x)`, `s.has(x)` |
| `defaultdict(list)` | `Map` + `if (!m.has(k)) m.set(k, [])` |
| `w[:i] + "*" + w[i+1:]` | `w.slice(0, i) + "*" + w.slice(i + 1)` |
| `[[0] * C for _ in range(R)]` (never `[[0]*C]*R`) | `Array.from({length: R}, () => Array(C).fill(0))` |

## Session format (mentor + interviewer)
Goal output first → node/edge/ask out loud → I write the code → interviewer review → complexity in R/C terms.

## Log

### 2026-10-26 — Pattern 1: Number of Islands (DFS)
- Node = land cell, edge = shared side (4 dirs), ask = count connected components
- Wrote own test cases before coding (incl. all-water → 0) and asked the mutate-vs-visited question up front
- Correct on first paste; fixes: `if not grid: return 0`, unused `import copy` → use `deepcopy`, hint `list[list[str]]`
- Marking `'2'` (not `'0'`) keeps the grid restorable — say it in the interview
- Time O(R·C) (each cell touched ≤ 5×), space O(R·C) recursion stack; Python recursion limit ~1000 → mention BFS + deque

### 2026-10-26 — Pattern 2: Rotting Oranges (multi-source BFS)
- First submission was agent-written; own version had the right structure (seed all rotten, `fresh` counter, -1 check, empty-grid guard)
- Bug: `queue.pop()` = stack → rot jumps 2 steps/minute → grid1 gave 3 not 4. Fix: `popleft()`
- `for _ in range(len(queue))` = snapshot of this minute's batch ("rope in the bank line")
- `while queue and fresh > 0` avoids the extra empty minute
- Real gap found: Python fluency, not graph logic

### 2026-10-27 — Python warm-up + Pattern 3: Word Ladder (BFS shortest path)
- Warm-up A–F done by hand; key trap: `deque((1,0))` → 2 items, `append([(0,0)])` → unpack error
- Node = word, edge = differ by one letter (undirected), ask = BFS level when `endWord` first reached
- Bugs fixed: `defaultdict(str)`→`list`, slice `[:i+1]`→`[i+1:]`, `append((a, b))`, added `visited`, `return 0` dedented out of loop, start count at 1 (words, not steps)
- Design lesson: sorted-adjacent comparison misses edges (`hot`/`lot`) → compare all pairs, O(N²·L)
- Why BFS = shortest: FIFO explores by distance, so first hit is shortest (only with equal edge weights). Follow-up: pattern map `h*t → [hit, hot]` for O(N·L²)
