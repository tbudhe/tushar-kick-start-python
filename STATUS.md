STATUS.md — Tushar's AI Learning (SINGLE SOURCE OF TRUTH)

Last Updated: 2026-08-21

RULE FOR CLAUDE: "CURRENT STATUS" here overrides ALL other documents. If any doc conflicts, this file wins.

PROTOCOLS (condensed — full history in LEARNING_NOTES.md)
- DOC (2026-08-10): one session = one day number, sequential. Session end: update LEARNING_NOTES.md (one Day block, MAX 5 POINTS — Tushar's rule 2026-08-21), STATUS.md, MEMORY.md, then commit.
- QUIZ (revised 2026-08-21 — Tushar's correction): MAX 5 QUESTIONS PER DAY-TOPIC (not per session). Default: 2–3 on the last day + 1 cold rotation pick (Days 0–current, prioritise weak spots); follow-up nudges count toward that topic's 5. Log the rotation pick. Answers in SENTENCES first; a run or code block is evidence, not an answer.
- COACHING (2026-08-18, verified working): before EVERY exercise — (1) GOAL first: show the exact final printout; (2) numbered step list; (3) ONE step at a time, confirm before the next. If Tushar says "I didn't understand the question": don't repeat it — rebuild with one sentence of concrete context, then a simpler version.
- REVISION WEEK (2026-08-17): when Phase 2 completes, one full week of Phase 1+2 revision before Phase 3. No new content; weak-spots list is the syllabus.

MILESTONES (recalibrate at each phase end)
Sep 2026: Phase 2 complete (tool use, LangChain/LlamaIndex, Project 2 hardened) → REVISION WEEK → Nov 2026: Phase 3 complete (LangGraph, agents, MCP, LangSmith) → Dec 2026: Projects 3+4 shipped → Feb 2027: job search opens → Jul 2027: Walmart Staff/Principal AI Engineer.

CURRENT STATUS
Day: 31 COMPLETE | Week: 6 — Phase 2 | Next session = Day 32 (decide at start: LangChain cont. — bind tools to a model, what replaces `while stop_reason == "tool_use"` — or Project 2 hardening)
Goal: Staff SWE → AI Backend Engineer (Autodesk) → Staff/Principal AI Engineer, Walmart, July 2027
Just completed: Day 31 (2026-08-21) — LangChain intro. `@tool` collapses all FOUR Day 30 registries (schema, function, dispatch, validator) into one decorator generated from the function signature — one source of truth, so the wrong-validator bug is structurally impossible. Exercise `exercises/day31_langchain_tool.py` COMPLETED AND VERIFIED: printed the generated registries, re-ran the Day 30 chain via `.invoke()` (YUNextGenAI→YNXT→42.0), and fired the free validator ("company_name Field required" — specific, actionable, AND correct this time). Direction-inversion weak spot fired LIVE in a tool description and was caught and fixed. Deliberately short session (low energy) — one concept, one exercise, clean stop.
Exercise status: COMPLETED AND VERIFIED — all three goal sections matched. Code + full notes in LEARNING_NOTES.md Day 31.
Quiz results (Day 30 topic + cold Day 28): Day 30 Q1 error-text lesson LANDED after 3 nudges. Q2 four registries: 3 of 4 named (missed the function itself); "why does the model only need TOOLS" missed — re-ask cold. Day 28 give_up() WHY PASSED cleanly — CLOSED.
Project 1: SHIPPED. Project 2: RAGAS triad + typed RagResponse done; remaining: real Autodesk chunks, model cost decision, ragas upgrade, one paid ragas_evals.py run.
Currently strong on: give_up() mechanism (exact sentence, unprompted); predicted @tool's internals from hand-built experience; fixed the inverted description once pointed at it.

WEAK SPOTS (revisit)
1. SENTENCES vs CODE — recurred 08-21 (registries answered in code; Step-5 prediction skipped). Demand the sentence first, patiently.
2. FOUR REGISTRIES — still shaky: names 3 of 4, forgets the function itself; and "model only sees TOOLS because it only WRITES a JSON request, never runs code" — re-ask cold.
3. Sentinel mechanics (Day 27): no raise → except never runs → is_error stays False — re-ask due.
4. Sibling-tools failure mode (Day 27): try around the loop kills innocent siblings' tool_results — re-ask due.
5. Day 20 first print — count-print missed 3×. Drill as one breath: "layer = filter, print = count." Re-ask ~08-24.
6. DIRECTION INVERSIONS — fired live 08-21 in a @tool description ("Look up the ticker symbol to get prices"). Rule: say the arrow out loud, THEN write the description. Stays open.
CLOSED 2026-08-21: give_up()-tools-disabled WHY (Day 28) — passed with the exact mechanism sentence.

CARRIED FORWARD
(1) Phase 1 recap out loud (owed since 08-08; folds into REVISION WEEK). (2) tool_loop.py line-22 description inversion. (3) Trim-experiment + prefill re-attach re-test.

NEXT SESSION (Day 32) — QUIZ PLAN (max 5 per topic)
Day 31 topic: Q1. Why can't the Day 30 wrong-validator bug happen with @tool? (one-source-of-truth sentence). Q2. When a model "calls a tool," what does it actually produce, and why is TOOLS the only registry it needs?
Cold pick: Q3 (Day 27). Sentinel mechanics — why does a sentinel string keep is_error False? (sibling-tools queues behind it.)

ONE-SENTENCE SUMMARY (say out loud)
"@tool replaced my four hand-wired registries — schema, function, dispatch, validator — by generating all of them from the one function signature, so the wrong-validator bug can't happen because there are no separate copies left to disagree."

ACTIVE MENTAL MODELS (top of mind — full running list archived in LEARNING_NOTES.md)
- @tool = @RestController: four registries generated from one signature; nothing removed, everything automated — validation still runs, you just don't write it
- The model never runs code — it WRITES a JSON tool_use request; TOOLS is the menu of requests it may write; function/dispatch/validator are server-side
- One source of truth cannot drift — copies drift; Day 30's bug was two hand-maintained copies of one contract
- Docstring/description = model-facing prompt engineering; say the arrow out loud ("X in, Y out") BEFORE writing it
- .invoke() takes a dict because that's the shape model tool_use arguments arrive in
- Dependency chain = B's argument IS A's output; N links need MAX_ITERATIONS ≥ N+1
- A wrong validator's error steers the model wrong — the model OBEYS error text; actionable+specific+WRONG is worse than vague
- A model retrying the same call means its tool_result was an error — retries are a diagnostic signal
- give_up() = forced landing: no tools param → tool_use structurally impossible → end_turn text is the only exit
- Pydantic errors name the CONTRACT; TypeErrors name Python internals — specificity is the tell (400 vs 500)
- A hardcoded literal beside a lookup dict is an allowlist bug — data must be the authority
- A run is evidence, not an explanation — the check question wants a sentence
- Refusal debugging: layer = filter, print = COUNT

PROGRESS LOG (most recent first — headline only)
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
