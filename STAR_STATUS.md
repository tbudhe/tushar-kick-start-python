# STAR_STATUS.md — Behavioral (STAR) daily practice (SINGLE SOURCE OF TRUTH for STAR)

Last Updated: 2026-11-20 (Q1 attempt 2 = 5/8, MongoDB story banked)
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
Next: **Q2 — disagreed with a senior engineer/manager**

## LADDER (10 questions)
| # | Question | Likely story | Score | Status |
|---|---|---|---|---|
| 1 | Hard production performance problem | Oracle -> MongoDB cart, primary CPU 85% (checkout p99 = backup) | 3/8 -> 5/8 | banked; retry cold in 2nd pass |
| 2 | Disagreed with a senior engineer/manager | | | |
| 3 | A failure or mistake | | | |
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


## LOG
- 2026-11-18: track created; Q1 asked.
- 2026-11-18: Q1 attempt 1 = 3/8 (S1 T0 A1 R1). Told the Azure outage/failover story; it fits an INCIDENT question better than a PERFORMANCE one. Banked as the story for 'production incident'. Fixes: T must say what I owned; use 'automated region failover', not 'canary'; R needs a number; drop 'trademark'.
- 2026-11-20: Q1 attempt 2 = 5/8 (S1 T1 A2 R1). New story: Oracle -> MongoDB cart migration, primary CPU 85%. Fixes: S needs scale + stakes; T = what I owned (not triage steps); readConcern 'majority' does NOT route reads - readPreference=secondaryPreferred does; R needs the CPU number + a lesson.
