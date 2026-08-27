STATUS.md — Tushar's AI Learning (SINGLE SOURCE OF TRUTH)

Last Updated: 2026-08-27

RULE FOR CLAUDE: "CURRENT STATUS" here overrides ALL other documents. If any doc conflicts, this file wins.

PROTOCOLS (condensed — full history in LEARNING_NOTES.md)
- DOC (2026-08-10): one session = one day number, sequential. Session end: update LEARNING_NOTES.md (one Day block, MAX 5 POINTS — Tushar's rule 2026-08-21), STATUS.md, MEMORY.md, then commit.
- QUIZ (revised 2026-08-21 — Tushar's correction): MAX 5 QUESTIONS PER DAY-TOPIC (not per session). Default: 2–3 on the last day + 1 cold rotation pick (Days 0–current, prioritise weak spots); follow-up nudges count toward that topic's 5. Log the rotation pick. Answers in SENTENCES first; a run or code block is evidence, not an answer.
- COACHING (2026-08-18, verified working): before EVERY exercise — (1) GOAL first: show the exact final printout; (2) numbered step list; (3) ONE step at a time, confirm before the next. If Tushar says "I didn't understand the question": don't repeat it — rebuild with one sentence of concrete context, then a simpler version.
- DEBUG PROTOCOL (2026-08-26): when a result doesn't change after an edit, READ THE FILE ON DISK before theorising. When behavior and docs disagree, read the installed library source in .venv. Probe config with BEHAVIOR, never formatting. GENERALISED 2026-08-27: a good instrument has exactly ONE explanation for its failure.
- MORALE (2026-08-24): he undercounts his own wins. Open sessions by naming one concrete previous win before the quiz; when discouragement surfaces, answer with same-session evidence, not reassurance. (Steady 08-25 → 08-27, no dip.)
- EXERCISE OWNERSHIP (2026-08-24): Tushar writes the exercise code himself — outside AI agents don't. (Honored 08-25, 08-26, 08-27 — he built A/B/C of Day 35 unaided and ahead of the step gate.)
- REVISION WEEK (2026-08-17): when Phase 2 completes, one full week of Phase 1+2 revision before Phase 3. No new content; weak-spots list is the syllabus.
- ENV NOTE (2026-08-27): the .venv python symlink does not resolve from Claude's mounted shell — Claude cannot run his code. Claude reads source in .venv and reasons; Tushar runs everything.

MILESTONES (recalibrate at each phase end)
Sep 2026: Phase 2 complete (tool use, LangChain/LlamaIndex, Project 2 hardened) → REVISION WEEK → Nov 2026: Phase 3 complete (LangGraph, agents, MCP, LangSmith) → Dec 2026: Projects 3+4 shipped → Feb 2027: job search opens → Jul 2027: Walmart Staff/Principal AI Engineer.

CURRENT STATUS
Day: 35 IN PROGRESS — Parts A/B/C done and verified, Part D (Step 5) pending | Week: 7 — Phase 2 | Next session = FINISH Day 35 Part D first (15 min), then Day 36 (decide at start: streaming on create_agent, or Project 2 hardening)
Goal: Staff SWE → AI Backend Engineer (Autodesk) → Staff/Principal AI Engineer, Walmart, July 2027
Topic in flight: Day 35 (2026-08-27) — checkpointer + thread_id, the framework's session store. Day 34 proved memory is something he passes in; `checkpointer=InMemorySaver()` moves it into a store and `thread_id` becomes the key. THE AGENT DID NOT BECOME STATEFUL — a store remembers, and he now sends a session ID instead of a transcript. Spring mapping he accepted: agent = stateless @RestController (unchanged), checkpointer = Spring Session + Redis, thread_id = JSESSIONID, graph loads before / appends after. `thread_id → checkpointer lookup key`, consumed by the graph BEFORE the model call — the model never sees it. Collision on one thread_id = shared mutable list = real cross-tenant leak plus a race (his own answer, unprompted). InMemorySaver is debug-only per its own docstring — a dict in one process.
Exercise status: `exercises/day35_react_agent.py` — A (no checkpointer → amnesia), B (checkpointer + thread_id → remembered from ONE message), C (different thread_id → amnesia, key isolates) ALL WORKING. Part D not written: `agent.get_state(cfg).values["messages"]` → count per thread + check whether ANY stored message is a SystemMessage (predict before running; expected False).
THE DAY'S UNPLANNED FIND: his own output reproduced Day 34's proof-marker lesson WITH A CONTROL GROUP — `[YNXT-BOT]` present on A, B-turn-2 and C (no tool loop concluded), dropped on B-turn-1 (concluded a tool loop). One run of this file would have settled the entire Day 34 dispute. Second find: B turn 2 answered "YNXT" without calling get_ticker — session state is a latency/cost argument, not only a UX one.
Quiz results (Day 34 topic + cold): 4/4. Q1 system-prompt location PASSED (2 nudges; first said it DOES appear in result["messages"], then recovered with his own better framing: "it stopped being conversation data and became request-building configuration"). Q2 stateless B/C contrast PASSED clean, first try. Q3 proof markers PASSED (1 nudge) landing on the general rule about single-explanation instruments. Q4 direction-inversion drill PASSED COLD, no nudge — read the SIGNATURE over the description's word order.
Project 1: SHIPPED. Project 2: RAGAS triad + typed RagResponse done; remaining: real Autodesk chunks, model cost decision, ragas upgrade, one paid ragas_evals.py run.
Currently strong on: cold recall of the previous day's weak spot; reading a signature/source instead of guessing; self-correcting an inverted arrow after ONE nudge; adding design-review depth to quiz answers unprompted (the cross-tenant leak answer).

WEAK SPOTS (revisit)
1. DIRECTION INVERSIONS / SLOT SWAPS — DOWNGRADED 2026-08-27 from PRIORITY to WATCH. Passed the cold drill clean (get_ticker_symbol arrow, resisting the "ticker symbol for a company name" word-order bait) but inverted thread_id in the check question and needed one nudge. ONE MORE CLEAN COLD PASS CLOSES IT. Drill: say the arrow out loud BEFORE describing; trust the signature over the prose.
2. SENTENCES vs CODE — good three sessions running. Keep light pressure, don't grind.
CLOSED 2026-08-26: MENU-vs-TRIPS (open since Day 32).

CARRIED FORWARD
(1) Phase 1 recap out loud (owed since 08-08; folds into REVISION WEEK). (2) tool_loop.py line-22 description inversion — FILE NOT FOUND in repo on 08-27; either locate it or drop this item. (3) Trim-experiment + prefill re-attach re-test. (4) SYSTEM_PROMPT still carries the `[YNXT-BOT]` probe line in BOTH day34 and day35 files — but do NOT delete it from day35 until the control-group table is captured; it is now evidence. Clean day34, keep day35's until Part D is done.

NEXT SESSION (Day 35 finish → Day 36) — QUIZ PLAN (max 5 per topic)
Day 35 topic: Q1. `thread_id` — say the ARROW first, then who consumes it and at what moment relative to the model call. Q2. The agent has a checkpointer now. Is it stateful? One sentence, and say what actually changed. Q3. Why is InMemorySaver debug-only — answer in Walmart-deployment terms, not library terms.
Cold picks: Q4 (weak spot 1, one clean pass from CLOSED) — any tool docstring in the repo, arrow before description. Q5 (if time, Day 27) — an orphaned tool_use with no tool_result: what does the API do, and why is is_error data rather than a crash?
Morale opener: he built Parts A, B and C of Day 35 unaided, ahead of the step gate, and they ran correctly the first time — including the isolation test that most people don't think to write.

ONE-SENTENCE SUMMARY (say out loud)
"The checkpointer didn't make the agent stateful — it gave the memory a home outside the agent, so I send a thread_id key instead of the whole transcript, exactly like a session cookie instead of resending my history."

ACTIVE MENTAL MODELS (top of mind — full running list archived in LEARNING_NOTES.md)
- checkpointer = Spring Session + Redis; thread_id = JSESSIONID; the agent is still the stateless @RestController
- thread_id → checkpointer lookup key, consumed by the graph BEFORE the model call — the model never sees the key
- Two users on one thread_id = one shared mutable list = cross-tenant leak + a race, not a UX quirk
- Session state can skip a tool call entirely — memory is a latency and cost argument
- A good instrument has exactly ONE explanation for its failure — that's why French beat [YNXT-BOT]
- Config is re-applied every call; state is accumulated — system_prompt is config, messages are state
- system_prompt = Day 32's messages[0] relocated to config time; factory.py prepends it every call and it never lands in result["messages"]
- The agent is stateless between invokes — memory is something I pass in, not something it has
- Stateless = horizontally scalable; checkpointer= is the session-store decision made explicit
- The library is in my .venv — when docs and behavior disagree, read the source; it outranks both hypotheses
- When the output doesn't move, verify the code that ran is the code on disk
- No tools bound → tool_use structurally impossible → text is the only exit: give_up()'s honest landing and an unguarded model's hallucination are the same mechanic
- create_agent = Spring Boot for the loop: raw servlets → @RestController was Day 31's @tool; the hand loop → agent.invoke() is Day 33
- ReAct = reason→act→observe→repeat; Reason is the model's turn (including asking for a tool), Act is MY code running it and appending the result
- The debugging dividend: "agent hung" = iteration budget exhausted (Day 28); "API rejected" = orphaned tool_use missing its tool_result (Day 27)
- create_agent binds internally — raw model in; the tools you pass separately are what actually dispatch
- result["messages"] = the grown transcript, returned: Human → AI(tool_calls) → Tool → AI(tool_calls) → Tool → AI(text, end_turn)
- Python dict[key] THROWS on miss (KeyError); .get() is Java's null-returning map.get()
- Python takes the LAST assignment silently — duplicated definitions shadow, where Java's compiler would refuse
- bind_tools = printing the menu (config-time); rounds = trips to the kitchen (runtime, N links → N+1 invokes) — MENU SIZE NEVER ENTERS THE MATH
- Binding is static, dispatch is dynamic — the input to the lookup doesn't exist before execution (his sentence, Day 33)
- Transcript order: AIMessage BEFORE its ToolMessages; every tool_use needs its tool_result or the API rejects the turn
- try around the whole dispatch loop kills innocent siblings
- A run is evidence, not an explanation — the check question wants a sentence

PROGRESS LOG (most recent first — headline only)
Day 35 (IN PROGRESS): checkpointer + thread_id — memory gets a home outside the agent; A/B/C prove amnesia, recall-from-one-message and thread isolation; his output accidentally reproduced Day 34's proof-marker finding with a control group; quiz 4/4, direction-inversion downgraded to watch; Part D pending
Day 34: system prompt moves to config, state stays mine — stateless agent proven by the B/C contrast; false "framework broken" verdict overturned by reading factory.py in .venv; proof markers must be behavioral; quiz 4/4, menu-vs-trips CLOSED
Day 33: create_agent takes the loop — ReAct named, deprecation churn handled live, transcript proved the framework runs my Day 32 rounds; Yieldnext dict bug caught by tracing; quiz 3/4, TWO weak spots closed (give_up, sibling-tools)
Day 32: bind_tools kills the plumbing, the loop survives — round-traced chain via response.tool_calls; agent-broken code diagnosed live (no return, no loop, no append); menu-vs-trips resolved; quiz 4/4, THREE weak spots closed
Day 31: LangChain intro — @tool collapsed the four registries into one decorator; chain re-ran via .invoke(); free validator fired correctly; direction inversion caught live; give_up() WHY closed; new rules: 5 Qs per day-topic, 5-point day blocks
Day 30: Multi-step planning FINISHED — chain ran (YNXT→42.0→"$42.00"); INPUT_MODELS fourth registry closed the landmine; wrong-validator error steered the model wrong; self-found AAPL allowlist bug
Day 29: Multi-step planning STARTED — chain concept, world-knowledge bypass, two directions = two tools, three registrations; coaching rule created
Day 28: Max-iteration guards — for range(MAX_ITERATIONS), give_up() forced landing, sabotage verified
Day 27: Tool errors + input validation — is_error as data, Pydantic at the boundary, sentinel-string bug found live
Day 26: Tool use in production — while-True loop, schemas as OpenAPI, dispatch + tool_use_id
Day 25: Typed pipeline responses — RagResponse DTO
Day 24: Pydantic deep dive; structured outputs + prefill fix
Day 23: Multi-turn state — sliding-window trim in pairs
Day 22: PHASE 2 START — streaming + async
Day 21: RAGAS triad + sabotage test. PHASE 1 COMPLETE.
Days 0–20: ML basics → tokenization → embeddings → RAG → ChromaDB → chunking → metadata filtering → training → transformers → RLHF → function calling → hallucinations → model selection → FT-vs-RAG → inference → Project 2 v1 → RAGAS → refactor → three-layer refusal debugging (full detail in LEARNING_NOTES.md)

ARCHIVE NOTE
Full per-day Q&A, one-liners, and the complete mental-model list live in LEARNING_NOTES.md. Content review only — NEVER for determining current progress.
