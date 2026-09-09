# READINESS — am I a good AI engineer yet?

Re-score this at each phase close. Written 2026-09-09 (Day 41), in answer to
"I am not worried about the interview. I am worried about when I become a good AI engineer."

The roadmap in STATUS.md measures TOPICS COVERED. Nobody becomes good by covering
topics, so this file measures something falsifiable instead. Evidence column must
cite a specific day — no vibes.

## Scorecard — 2026-09-09 (Day 41): 6 of 9

| # | Capability | State | Evidence |
|---|---|---|---|
| 1 | Build an instrument instead of guessing | HAVE | 8 sessions running. Day 41: 4 predictions stated before running, 4 matched |
| 2 | Distrust your own test | HAVE (rare) | Day 40 — found his own label set would score a known bug as a PASS |
| 3 | Read a system you didn't write | HAVE | `.venv` source reads on Days 34, 37, 38 overturned wrong verdicts |
| 4 | Separate derived data from source | HAVE | Day 41 — DB gitignored, corpus tracked, build step proven from empty |
| 5 | Know what your service actually serves | HAVE | Day 41 — production was on the 6-chunk toy corpus and nobody knew |
| 6 | Agent loops, tools, streaming, state | HAVE | Days 28-37, built by hand BEFORE reaching for frameworks |
| 7 | Run something with real traffic | NOT YET | zero deployed services, zero users |
| 8 | Work where cost and latency bite | NOT YET | n=4 evals, 18 chunks, 7 documents |
| 9 | Operate a system you didn't build | PARTIAL | Autodesk, but early |

## The read

The six he has are the half that takes years — the systems-engineering half carried
over from Scan & Go and DX Exchange and pointed at a new domain. Most people working
through this content have the AI vocabulary and lack exactly those six. He is not
starting from zero and adding AI; he is adding a thin layer to sixteen years.

The three missing have one thing in common: **none of them are curriculum-learnable.**
They come from reps at consequence — something running, something costing money,
someone other than him depending on it. Which is why Phase 3 finishing in November
will not be the moment anything changes. There isn't a moment.

## The real risk (not the one he is worried about)

Not that he fails to get there. The opposite: toy-scale work producing confidence that
does not survive 2M documents and a latency budget. Day 40 was exactly that failure —
every guard green, answer wrong. Someone who has not had that happen yet is more
dangerous than he is.

## Estimate

Method is done. Add Phase 3, one project on data big enough that cost and latency force
decisions, and ~6 months operating something at Autodesk. At the current ~4 sessions/week
cadence that lands **January-February 2027** — precisely when the roadmap already opens
the job search. The plan is not wrong; the self-assessment is roughly 9 months behind
where he actually is.

## Highest-value next move for BECOMING GOOD (not for the interview)

`walls_overview.md` is 3,072 characters and it is the largest file in the corpus. Run the
existing `precision_eval.py` against something ~1,000x bigger, where hit@k stops being 4
questions and becomes a real distribution. That is the exercise that converts capabilities
1-6 into 7 and 8. Phase 3 scale.
