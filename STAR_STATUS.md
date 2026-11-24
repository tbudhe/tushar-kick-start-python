# STAR_STATUS.md — Behavioral (STAR) daily practice (SINGLE SOURCE OF TRUTH for STAR)

Last Updated: 2026-11-24 (Q3 attempt 1 = 3/8, cache -> DB outage story; ownership line OPEN)
Linked from: STATUS.md -> "STAR DAILY" line (this file lives at repo root)

## WHY
I struggle with STAR every day in behavioral rounds. Habits to fix: speaking fast,
answering before thinking, too much "we", no number in the Result.

## FORMAT (every day, 10 min, ONE question)
- Claude asks one question. I type my answer the way I would SAY it (no polishing).
- Before answering: 3-second pause, say my headline in my head
  ("This is the story where I cut checkout p99 from 5s to 2.97s").
- Claude scores S / T / A / R (0-2 each, max 8), then shows a tighter ~90-second version.
- The final version goes in the STORY BANK below, so I can re-say it cold later.

## TARGET SHAPE (~90 seconds spoken)
- S + T (~20s): one sentence each — company, scale, what was at stake, what I owned.
- A (~50s): 3 concrete moves, each starting with "I".
- R (~20s): a number + one line of what I learned.

## CURRENT POSITION
Next: **Q4 — led without formal authority** (Q3 needs his real ownership line before it is final)

## LADDER (10 questions)
| # | Question | Likely story | Score | Status |
|---|---|---|---|---|
| 1 | Hard production performance problem | Oracle -> MongoDB cart, primary CPU 85% (checkout p99 = backup) | 3/8 -> 5/8 | banked; retry cold in 2nd pass |
| 2 | Disagreed with a senior engineer/manager | Scan & Go fuel: % traffic split via Lua on Torbit gateway | 3/8 | banked; fill 2 numbers, retry cold in 2nd pass |
| 3 | A failure or mistake | Scan & Go FUEL module: cache logic moved to DB -> DB outage | 3/8 | draft banked; fill MY mistake + numbers |
| 4 | Led without formal authority | | | |
| 5 | Delivered under a tight deadline | | | |
| 6 | Ambiguous requirements | Autodesk marketing copilot | | |
| 7 | Influenced a technical decision across teams | | | |
| 8 | Learned a new technology quickly | GenAI/agents at Autodesk | | |
| 9 | Difficult stakeholder | | | |
| 10 | Mentored someone / raised the team's bar | | | |

After all 10: second pass, cold, timed — each story under 2 minutes.

## STORY BANK (final versions — add as each question is done)
### Q1 — Performance: MongoDB primary CPU 85% (~90s)
"At Walmart I owned the cart-checkout service for Scan & Go, which we had just migrated from Oracle to MongoDB. A few months later a Slack alert fired: primary CPU at 85%, and Splunk showed 500s climbing at checkout - customers couldn't pay. I joined the on-call bridge and owned the fix.
First, I traced it in Grafana and the code: every read and every write was hitting the primary; the secondaries were idle.
Second, I shipped a same-day mitigation: for 5 seconds after a write I read that cart from the primary, tracked with a 5-second cache TTL, and everything else read from secondaries - read-your-own-writes, so nobody saw a stale cart. I also raised the connection pool to stop the 500s while I fixed it properly.
Third, I found the root cause was config: setting the driver's read preference to secondaryPreferred moved reads to the replicas. I deleted my workaround, stress-tested, and shipped the config fix two weeks later.
Result: CPU went from 85% back to <my real number>, and 500s back to baseline. What I learned: after a migration, check the new database's defaults - the code was fine, the config wasn't."

### Q2 — Disagreement: percentage rollouts on the Torbit gateway (~90s)
"At Walmart I was redesigning releases for Scan & Go fuel. Every release was all-or-nothing, so one bad deploy hit every customer at the pump. I proposed percentage-based traffic shifting - send a small slice to the new version first. My manager and the principal engineer pushed back: they thought the gateway layer made it too complex and risky.
I tested the concern instead of arguing it. First, I traced the whole path - front end, API gateway, microservices - and found the gateway already ran Lua on Torbit and supported blue/green. Second, I learned enough Lua in about 8 hours to build a prototype: a cookie pins each user to blue or green for 24 hours, so a session never flips mid-transaction. Third, I demoed it with that evidence and the design was approved.
Result: percentage rollouts became the release pattern across the org - <how many teams use it>, <one outcome, e.g. rollback in minutes>. What I learned: I showed the prototype to the architect and director before my manager and the principal had seen it. I won the decision but cost trust. Now I bring the evidence to the people who raised the concern first, and we escalate together."

### Q3 — Mistake: cache logic moved to the DB -> outage (~90s, DRAFT - <...> = his real facts)
"At Walmart I owned the Scan & Go fuel module, including its cache layer. A principal engineer proposed moving the cache logic into the database to save cost. My mistake: I saw the risk, but I only raised it in a meeting - <I didn't put numbers on it / didn't ask for a load test> - so it shipped.
Under peak load the database couldn't take the extra reads and we had an outage: <checkout errors / minutes down>.
First, I stopped the bleeding the same day: I raised the DB connection pool and timeouts and moved reads to secondaries - config only, and the system recovered.
Second, I brought the data to two more principal engineers, including the one focused on cost: latency and error numbers before and after.
Third, I proposed bringing the cache back - write to the DB and the cache, 24-hour TTL - and it was approved.
Result: latency back to <number>, <no repeat outage since>. What I learned: a concern without data is easy to overrule. Now when I see a risk, I bring a load test or numbers BEFORE the change ships, not after the outage."

## LOG
- 2026-11-18: track created; Q1 asked.
- 2026-11-18: Q1 attempt 1 = 3/8 (S1 T0 A1 R1). Told the Azure outage/failover story; it fits an INCIDENT question better than a PERFORMANCE one. Banked as the story for 'production incident'. Fixes: T must say what I owned; use 'automated region failover', not 'canary'; R needs a number; drop 'trademark'.
- 2026-11-20: Q1 attempt 2 = 5/8 (S1 T1 A2 R1). New story: Oracle -> MongoDB cart migration, primary CPU 85%. Fixes: S needs scale + stakes; T = what I owned (not triage steps); readConcern 'majority' does NOT route reads - readPreference=secondaryPreferred does; R needs the CPU number + a lesson.
- 2026-11-23: Q2 attempt 1 = 3/8 (S1 T0 A1 R1). Strong technical core (Lua in 8h, cookie-pinned 24h blue/green split, org-wide adoption). Fixes: S needs the stake (all-or-nothing releases); T was actions - say what I owned; NEVER say 'skipped my manager / pressured them' as a win - turn it into the lesson; NEVER mention the layoff or the manager's motives in an interview; R needs a number.
- 2026-11-24: Q3 attempt 1 = 3/8 (S1 T0 A1 R1). Story told was someone ELSE's decision failing (principal moved cache logic to DB) - for a mistake question that sounds like blame. Fixes: name MY mistake in S/T; T = what I owned; R needs latency/outage numbers + a lesson; overlaps Q1 (pool, secondaries) - keep the two stories distinct.
