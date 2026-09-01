STATUS.md — Tushar's AI Learning (SINGLE SOURCE OF TRUTH)

Last Updated: 2026-09-01

RULE FOR CLAUDE: "CURRENT STATUS" here overrides ALL other documents. If any doc conflicts, this file wins.

PROTOCOLS (condensed — full history in LEARNING_NOTES.md)
- DOC (2026-08-10): one session = one day number, sequential. Session end: update LEARNING_NOTES.md (one Day block, MAX 5 POINTS), STATUS.md, MEMORY.md, then commit.
- QUIZ (2026-08-28, HONORED 08-31 and 09-01): **MAX 3 QUESTIONS PER SESSION, ONE PART EACH.** A question with sub-parts counts as that many questions — don't write them. If an answer is incomplete, Claude COMPLETES IT in one line and moves on; a gap never becomes a follow-up question. Nudges count.
- COACHING (2026-08-18, verified working): before EVERY exercise — (1) GOAL first: show the exact final printout; (2) numbered step list; (3) ONE step at a time, confirm before the next.
- **WHY BEFORE INSTRUMENT (NEW 2026-09-01):** he stopped mid-exercise twice with "why are we doing this / what are we going to prove?" Both times Claude had handed him a mechanism before its purpose. Every non-obvious line of scaffolding (a stamp, a fake sleep, a control group) gets ONE sentence of purpose BEFORE the code — what claim it tests, and what the two possible outcomes look like.
- CODE DELIVERY (2026-08-31): when he is mid-exercise, paste **COMPLETE blocks** with every variable's origin named — never fragments. Honored 09-01, zero re-typing round trips all session.
- EXAMPLE FIDELITY (2026-08-31): examples must use HIS tools with HIS semantics. Check the repo's actual signatures before inventing a trace.
- DEBUG PROTOCOL (2026-08-26/27, EXTENDED 08-31, APPLIED 09-01): when a result doesn't change after an edit, READ THE FILE ON DISK. When behavior and docs disagree, read the installed library source in .venv (done again this session — `ToolNode._func` vs `_afunc`). Probe config with BEHAVIOR, never formatting. A good instrument has exactly ONE explanation for its failure. An instrument that FILTERS its input reports the filter.
- MORALE (2026-08-24, EXTENDED 08-28): he undercounts his wins — open with one concrete previous win before the quiz. When frustration surfaces, FIRST check whether Claude caused it. A process complaint gets a protocol fix, not encouragement.
- EXERCISE OWNERSHIP (2026-08-24): Tushar writes the exercise code himself — outside AI agents don't. (Honored 08-25 → 09-01.)
- REVISION WEEK (2026-08-17): when Phase 2 completes, one full week of Phase 1+2 revision before Phase 3. Weak-spots list is the syllabus.
- ENV NOTE (2026-08-27): the .venv python symlink does not resolve from Claude's mounted shell — Claude cannot run his code. Claude reads source in .venv and reasons; Tushar runs everything.

MCP TIMING DECISION (2026-08-28, Tushar's call): KEEP THE SEQUENCE. MCP stays in Phase 3 (~Nov 2026); no spike day, no reorder. Reassess only at Phase 2 close.

MILESTONES (recalibrate at each phase end)
Sep 2026: Phase 2 complete (tool use, LangChain/LlamaIndex, Project 2 hardened) → REVISION WEEK → Nov 2026: Phase 3 complete (LangGraph, agents, MCP, LangSmith) → Dec 2026: Projects 3+4 shipped → Feb 2027: job search opens → Jul 2027: Walmart Staff/Principal AI Engineer.

CURRENT STATUS
Day: 37 COMPLETE (2026-09-01) | Week: 7 — Phase 2 | Next session = Day 38 (LlamaIndex vs LangChain).
Goal: Staff SWE → AI Backend Engineer (Autodesk) → Staff/Principal AI Engineer, Walmart, July 2027
Topic completed: Day 37 — async agent. Three cases measured, not argued: (A) INDEPENDENT tool calls in one round → async helps (4s of sleep in 2.0s); (B) DEPENDENT chain across rounds → async does NOTHING (`gather` can only start calls that EXIST); (C) two SEPARATE agent runs → 13.8s serial vs 6.9s concurrent, exactly 2x. Ship verdict: async is not an agent-latency feature, it's a CONCURRENCY feature — `agent.ainvoke` under FastAPI parks N coroutines on one loop instead of N threads blocked on the Anthropic API. The only real latency lever is FEWER ROUNDS (batch tools), not more async.
Exercise: `exercises/day37_async_agent.py` COMPLETE — async tools (`await asyncio.sleep(2)`), a `stamp()` instrument, Parts A/B/C1/C2 all green, plus a written VERDICT block at the bottom of the file.
NEW FINDINGS THIS SESSION: (1) Read out of his own .venv: `ToolNode._func` (sync) uses `executor.map` — a THREADPOOL; `_afunc` (async) uses `await asyncio.gather` — one thread. Both parallelize tool calls; async's win is not burning an OS thread per blocking wait. (2) `langchain/tools/tool_node.py` is a 3-line re-export of `langgraph.prebuilt.tool_node` — LangChain is the model/tool layer, LangGraph is the runtime that owns the loop. (3) HIS OWN HYPOTHESIS, tested unprompted: `part_a` and `part_b` are byte-identical except one string, so pasting B's question into A must produce B's timing — he ran it and it did. Concurrency is a property of the REQUEST, not the code. (4) Part A's two STARTs were identical to the centisecond (one gather); Part C-2's were 0.22s apart (two independent runs, API skew). (5) Wall clock swung 4.4s → 8.6s on IDENTICAL runs while the tool interval stayed 2.00s every time — model latency is the noise.
CARRIED-FORWARD ITEM 3 CLOSED: Day 36's "silent gaps" were discarded `input_json_delta` chunks carrying `partial_json` (streamed tool ARGUMENTS). Unfiltered, everything collapsed to ~0.6s except two genuine ~5s API stalls. The filtered instrument was reporting the filter.
Quiz results: 3 asked. Q1 `updates` vs `values` — gave the definitions, not the count (completed by Claude: values N+1, updates N). Q2 ship decision — described all three modes, didn't pick (completed: `["updates","messages"]`). Q3 cold Day 32 menu-vs-trips — **REGRESSED**: transcript trace was correct but he attributed trips to the NUMBER OF TOOLS (2). Corrected in place: trips = dependency depth, menu size never enters the math. Day 37's Part B then put a stopwatch on that exact correction.
Project 1: SHIPPED. Project 2: RAGAS triad + typed RagResponse done; remaining: real Autodesk chunks, model cost decision, ragas upgrade, one paid ragas_evals.py run.
Currently strong on: converting an explanation into a controlled experiment without being asked (three sessions running); reading round boundaries and API skew straight out of timestamps; stopping the session to ask "why are we doing this?" instead of executing steps blindly — that question improved the teaching twice today.

WEAK SPOTS (revisit)
1. MENU-vs-TRIPS — **REOPENED 2026-09-01** (was closed 2026-08-26). Cold-asked what determines the number of trips, he answered "number of tools (2)". Trace shape was right, cause was wrong. Day 37 Part B is now the measured counterexample — re-ask COLD in 2-3 sessions, once, using a case with 3 tools and 2 dependent steps so tool-count and depth can't be confused.
2. SENTENCES vs CODE — good six sessions running. Keep light pressure, don't grind.
3. `getattr` vs `.get()` — 2026-08-31. Not retested. Watch once more, don't drill.
CLOSED 2026-08-28: DIRECTION INVERSIONS / SLOT SWAPS (open since Day 26).

CARRIED FORWARD
(1) Phase 1 recap out loud (owed since 08-08; folds into REVISION WEEK). (2) Trim-experiment + prefill re-attach re-test. (3) Delete `time.sleep(2)` from `get_price` in **day36** before reusing that file as a reference (day37 uses `await asyncio.sleep(2)` deliberately — leave it). (4) Optional 2-minute Day 37 extension whenever a slow day needs filler: add a batch `get_prices(tickers: list[str])` tool and show the 10-company question collapsing from 10 rounds to 1 — the "fewer rounds" claim is currently asserted, not measured.
CLOSED 2026-09-01: Day 36 `input_json_delta` deferred check (answered with data).

PHASE 2 CLOSE PLAN (4 sessions to the end of Phase 2, then REVISION WEEK)
- Day 38 — LlamaIndex vs LangChain. Only untouched Phase 2 item. Rebuild EXISTING retrieval in LlamaIndex over the same chunks; write the 5-line "when I'd pick which" verdict. Artifact: llamaindex/ + verdict in notes.
- Day 39 — Project 2 hardening I: real Autodesk chunks through ingest.py; re-run retrieval audit; note what broke vs the toy corpus. EXTERNAL DEPENDENCY: needs a real Autodesk corpus staged before the session starts.
- Day 40 — Project 2 hardening II: model cost decision (haiku vs sonnet, measured not guessed), ragas upgrade, ONE paid ragas_evals.py run with the numbers recorded. EXTERNAL DEPENDENCY: needs the paid run budgeted.
- Day 41 — PHASE 2 CLOSE: no new content. Capstone review of Days 22-40, weak-spots list becomes the REVISION WEEK syllabus, Phase 1 recap out loud (owed since 08-08).
Then: REVISION WEEK (Phase 1+2, no new content) → Phase 3 opens ~late September.

NEXT SESSION (Day 38) — QUIZ PLAN (MAX 3, ONE PART EACH)
Q1. Async gave you 2x on Part C but zero on Part B. One sentence: what is the difference between those two situations?
Q2. Your agent answers a question about 10 companies by name. Name the ONE change that cuts the latency most, and say why.
Q3. Cold pick, Day 35: `InMemorySaver` across 12 pods — what breaks, and is it a latency bug or a correctness bug?
Morale opener: he ran an unprompted hypothesis test — spotted that part_a and part_b differed by a single string, predicted the outcome of swapping it, and confirmed it with a run. Third session running where an explanation became an experiment.

ONE-SENTENCE SUMMARY (say out loud)
"Async doesn't make my agent faster — it makes my server hold more agents at the same time; the chain inside one request is serial no matter what, and the only way to shorten it is fewer round trips."

ACTIVE MENTAL MODELS (top of mind — full running list archived in LEARNING_NOTES.md)
- Async overlaps WAITING, never CAUSALITY — a dependent chain is serial in any runtime
- `gather` can only start calls that EXIST; the model can't emit an argument it hasn't been told
- Concurrency is a property of the REQUEST shape, not of my code
- The latency lever is FEWER ROUNDS (batch tools), not more async
- `ToolNode._func` = threadpool (sync), `_afunc` = `asyncio.gather` (async) — both parallelize; async just doesn't park an OS thread
- LangChain = model/tool layer; LangGraph = the runtime that owns the loop and the state
- Wall clock mixes model latency + tool time + network — stamp the thing you are actually measuring
- `await asyncio.sleep` releases the thread; `time.sleep` freezes it — the waiter walks away vs stands in the kitchen
- updates = what changed / values = what is / messages = what's being typed right now
- `values` yields N+1 (it includes the initial state), `updates` yields N
- `stream_mode="messages"` carries TOOL output too — split on `metadata["langgraph_node"]`
- A filtered instrument reports the filter as much as the signal
- `create_agent()` is build-time, `.stream()`/`.invoke()` is request-time — never chain them
- `getattr(obj,"x")` asks for an ATTRIBUTE; `dict.get("x")` asks for a KEY — the swap fails silently
- checkpointer = Spring Session + Redis; thread_id = JSESSIONID; the agent is still the stateless @RestController
- result["messages"] is the WHOLE thread, never the delta
- InMemorySaver in 12 pods = 12 disconnected dicts; amnesia is a CORRECTNESS failure, not a latency one
- A tool's model obeys the DESCRIPTION while the function obeys the SIGNATURE
- is_error is data, not a crash — the model must SEE the failure to recover from it
- Config is re-applied every call; state is accumulated — system_prompt is config, messages are state
- A good instrument has exactly ONE explanation for its failure
- The library is in my .venv — when docs and behavior disagree, read the source
- create_agent = Spring Boot for the loop; ReAct = reason→act→observe→repeat
- bind_tools = printing the menu (config-time); rounds = trips to the kitchen (runtime) — MENU SIZE NEVER ENTERS THE MATH
- Transcript order: AIMessage BEFORE its ToolMessages; every tool_use needs its tool_result
- A run is evidence, not an explanation — the check question wants a sentence

PROGRESS LOG (most recent first — headline only)
Day 37: async agent — three cases measured (independent calls 4s→2s, dependent chain zero benefit, two runs 13.8s→6.9s); `ToolNode._func` threadpool vs `_afunc` gather read from his own .venv; his unprompted hypothesis test proved concurrency is a property of the request, not the code; Day 36 `input_json_delta` question CLOSED with data; menu-vs-trips REOPENED on the cold question
Day 36: streaming on the agent — updates/values/messages measured side by side, 5-vs-6 yields explained, ship verdict is both modes at once; token growth 755→858→950 read out of his own metadata; Claude's tool-gap prediction falsified by his timer, then the gap manufactured on purpose with sleep(2); 3/3 quiz with a four-case control set on the cold question
Day 35: checkpointer + thread_id — memory gets a home outside the agent; A/B/C/D all green with Part D predicted 4/4 before running; the [YNXT-BOT] control group closed Day 34's open question; 3/3 + clean cold pass, DIRECTION INVERSIONS CLOSED; quiz volume broke him mid-session → quiz rule rewritten to 3 single-part questions
Day 34: system prompt moves to config, state stays mine — stateless agent proven by the B/C contrast; false "framework broken" verdict overturned by reading factory.py in .venv; proof markers must be behavioral; quiz 4/4, menu-vs-trips CLOSED
Day 33: create_agent takes the loop — ReAct named, deprecation churn handled live, transcript proved the framework runs my Day 32 rounds; quiz 3/4, TWO weak spots closed
Day 32: bind_tools kills the plumbing, the loop survives — round-traced chain via response.tool_calls; menu-vs-trips resolved; quiz 4/4, THREE weak spots closed
Day 31: LangChain intro — @tool collapsed the four registries into one decorator; direction inversion caught live; give_up() WHY closed
Day 30: Multi-step planning FINISHED — chain ran (YNXT→42.0→"$42.00"); INPUT_MODELS fourth registry closed the landmine; self-found AAPL allowlist bug
Day 29: Multi-step planning STARTED — chain concept, world-knowledge bypass, two directions = two tools, three registrations
Day 28: Max-iteration guards — for range(MAX_ITERATIONS), give_up() forced landing, sabotage verified
