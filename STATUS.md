STATUS.md — Tushar's AI Learning (SINGLE SOURCE OF TRUTH)

Last Updated: 2026-08-24

RULE FOR CLAUDE: "CURRENT STATUS" here overrides ALL other documents. If any doc conflicts, this file wins.

PROTOCOLS (condensed — full history in LEARNING_NOTES.md)
- DOC (2026-08-10): one session = one day number, sequential. Session end: update LEARNING_NOTES.md (one Day block, MAX 5 POINTS — Tushar's rule 2026-08-21), STATUS.md, MEMORY.md, then commit.
- QUIZ (revised 2026-08-21 — Tushar's correction): MAX 5 QUESTIONS PER DAY-TOPIC (not per session). Default: 2–3 on the last day + 1 cold rotation pick (Days 0–current, prioritise weak spots); follow-up nudges count toward that topic's 5. Log the rotation pick. Answers in SENTENCES first; a run or code block is evidence, not an answer.
- COACHING (2026-08-18, verified working): before EVERY exercise — (1) GOAL first: show the exact final printout; (2) numbered step list; (3) ONE step at a time, confirm before the next. If Tushar says "I didn't understand the question": don't repeat it — rebuild with one sentence of concrete context, then a simpler version.
- MORALE (new 2026-08-24): he undercounts his own wins ("why can't I learn quickly" after a 4/4 session that closed three weak spots). Open sessions by naming one concrete previous win before the quiz; when discouragement surfaces, answer with same-session evidence, not reassurance.
- EXERCISE OWNERSHIP (new 2026-08-24): Tushar writes the exercise code himself — outside AI agents don't. (An agent rewrote day32 mid-session and deleted the loop, the return, and the append; the rescue was great teaching, but the rule stands.)
- REVISION WEEK (2026-08-17): when Phase 2 completes, one full week of Phase 1+2 revision before Phase 3. No new content; weak-spots list is the syllabus.

MILESTONES (recalibrate at each phase end)
Sep 2026: Phase 2 complete (tool use, LangChain/LlamaIndex, Project 2 hardened) → REVISION WEEK → Nov 2026: Phase 3 complete (LangGraph, agents, MCP, LangSmith) → Dec 2026: Projects 3+4 shipped → Feb 2027: job search opens → Jul 2027: Walmart Staff/Principal AI Engineer.

CURRENT STATUS
Day: 32 COMPLETE | Week: 7 — Phase 2 | Next session = Day 33 (decide at start: LangChain cont. — what finally replaces the hand-written loop (agent abstractions) — or Project 2 hardening)
Goal: Staff SWE → AI Backend Engineer (Autodesk) → Staff/Principal AI Engineer, Walmart, July 2027
Just completed: Day 32 (2026-08-24) — bind_tools kills the plumbing, the loop survives. `.bind_tools()` staples the TOOLS menu on at config time; `response.tool_calls` arrives pre-parsed; `tool.invoke(tc)` fires validator+function+dispatch in one call. The orchestration decision — loop again or done (`if not response.tool_calls:`) — is runtime and still hand-written. Exercise `exercises/day32_bind_tools.py` COMPLETED AND VERIFIED (round trace → "$42.00"). Bonus: an outside agent rewrote the file and broke it three ways (no return, no loop, no append); Tushar diagnosed it live — proof the loop is orchestration and it's his. Menu-vs-trips confusion (bind_tools count vs MAX_ITERATIONS) resolved with the restaurant analogy.
Exercise status: COMPLETED AND VERIFIED — GOAL trace matched. Code + full notes in LEARNING_NOTES.md Day 32.
Quiz results (Day 31 topic + colds): 4/4. Q1 one-source-of-truth PASSED (1 nudge). Q2 model-writes-JSON/TOOLS-is-the-menu PASSED clean unprompted — CLOSED. Day 27 sentinel mechanics PASSED cold — CLOSED. Day 20 count drill PASSED with the why after 3 prior misses — CLOSED.
Project 1: SHIPPED. Project 2: RAGAS triad + typed RagResponse done; remaining: real Autodesk chunks, model cost decision, ragas upgrade, one paid ragas_evals.py run.
Currently strong on: three long-standing weak spots closed in one session; found the agent-deleted `return` himself; articulated the round-2 mechanism (only the MODEL, on the NEXT invoke, can request the second tool).

WEAK SPOTS (revisit)
1. SENTENCES vs CODE — recurred 08-24 twice (guard question answered in pseudocode; bug-2 mechanism needed a fill-in-the-blank). Demand the sentence first, patiently.
2. Sibling-tools failure mode (Day 27): try around the loop kills innocent siblings' tool_results — re-ask OVERDUE (not asked 08-24).
3. DIRECTION INVERSIONS — say the arrow out loud, THEN write the description. Not tested 08-24; stays open.
4. NEW (08-24): fallthrough guard vs give_up() — bare `return response` after MAX_ITERATIONS exhausts hands back an AIMessage still FULL of tool_calls (a request for more work dressed as an answer); give_up() re-calls with NO tools bound so honest end_turn text is the only exit. Answered half, in code — re-ask cold.
5. Menu-vs-trips (08-24, resolved same-session): bind_tools size ≠ MAX_ITERATIONS; rounds come from the question's dependency chain. Verify once cold, then close.
CLOSED 2026-08-24: four-registries + model-only-sees-TOOLS (Day 30/31); sentinel mechanics (Day 27); Day 20 count-print drill (after 3 misses).

CARRIED FORWARD
(1) Phase 1 recap out loud (owed since 08-08; folds into REVISION WEEK). (2) tool_loop.py line-22 description inversion. (3) Trim-experiment + prefill re-attach re-test.

NEXT SESSION (Day 33) — QUIZ PLAN (max 5 per topic)
Day 32 topic: Q1. bind_tools kills which job and which job survives — and why can't config-time decide a runtime question? Q2. Menu vs trips: 10 bound tools, ticker already given — how many rounds, and why doesn't 10 appear? (closes weak spot 5 if clean).
Cold picks: Q3 (weak spot 4). What does a bare `return response` after the guard exhausts hand back, and what did give_up() do instead? — SENTENCE required. Q4 (weak spot 2, overdue). Day 27 sibling-tools: why does try around the whole loop kill innocent siblings' tool_results?
Morale opener: name one concrete win from Day 32 before the quiz (e.g. "you found the deleted return yourself").

ONE-SENTENCE SUMMARY (say out loud)
"bind_tools staples the tool menu onto the model and hands me pre-parsed tool_calls, but the loop — invoke, run tools, append, invoke again until tool_calls is empty — is still my orchestration, and MAX_ITERATIONS is sized by the question's dependency chain, not the menu."

ACTIVE MENTAL MODELS (top of mind — full running list archived in LEARNING_NOTES.md)
- bind_tools = printing the menu (config-time); the loop = trips to the kitchen (runtime, sized by the question's chain: N links → MAX_ITERATIONS ≥ N+1)
- Plumbing vs orchestration: parsing/id-matching/tool_result-building is gone; "loop again or done" is yours until an agent framework takes it
- `if not response.tool_calls:` is the new `stop_reason == "tool_use"` — a runtime check on each fresh reply
- tool.invoke(tc) = validator + function + dispatch in one call; ToolMessage arrives with the id pre-threaded
- Transcript order: AIMessage BEFORE its ToolMessages — the request must precede its results or the API rejects the turn
- The model is the only planner and invoke() is its only pair of eyes — a ToolMessage nobody sends back is a round 2 that never happens
- NETWORK BOUNDARY (Tushar's own question, 08-24): invoke() is an HTTP round trip — the model runs in Anthropic's data center, the tools run in YOUR process/pod; the ONLY channel is text over the wire (JSON tool request out, tool result back), so execution over there is physically impossible and each chain link costs one round trip
- @tool = @RestController: four registries generated from one signature; one source of truth cannot drift
- The model never runs code — it WRITES a JSON tool_use request; TOOLS is the menu of requests it may write
- give_up() = forced landing: no tools param → tool_use structurally impossible → end_turn text is the only exit; a fallthrough `return response` is an unfinished flight handed to the caller
- Docstring/description = model-facing prompt engineering; say the arrow out loud BEFORE writing it
- A run is evidence, not an explanation — the check question wants a sentence
- Refusal debugging: layer = filter, print = COUNT

PROGRESS LOG (most recent first — headline only)
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
