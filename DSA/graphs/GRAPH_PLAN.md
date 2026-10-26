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
| 2 | Multi-source BFS | everything spreads at once | LC 994 Rotting Oranges | ⏭ next |
| 3 | BFS shortest path (unweighted) | minimum steps | LC 127 Word Ladder | |
| 4 | Topological sort | order / prereqs possible? | LC 207 / 210 Course Schedule | |
| — | Review 1–4 | mixed, timed | | |
| 5 | Union-Find | connected? / groups merge | LC 684 Redundant Connection | |
| 6 | Bipartite / 2-coloring | split into two teams | LC 785 Is Graph Bipartite | |
| 7 | Dijkstra | cheapest path, weights ≥ 0 | LC 743 Network Delay Time | |
| 8 | Bellman-Ford / bounded BFS | cheapest with ≤ K stops | LC 787 Cheapest Flights | |
| — | Review 5–8 | mixed, timed | | |

## Session format (mentor + interviewer)
Goal output first → node/edge/ask out loud → I write the code → interviewer review → complexity in R/C terms.

## Log

### 2026-10-26 — Pattern 1: Number of Islands (DFS)
- Node = land cell, edge = shared side (4 dirs), ask = count connected components
- Wrote own test cases before coding (incl. all-water → 0) and asked the mutate-vs-visited question up front
- Correct on first paste; fixes: `if not grid: return 0`, unused `import copy` → use `deepcopy`, hint `list[list[str]]`
- Marking `'2'` (not `'0'`) keeps the grid restorable — say it in the interview
- Time O(R·C) (each cell touched ≤ 5×), space O(R·C) recursion stack; Python recursion limit ~1000 → mention BFS + deque
