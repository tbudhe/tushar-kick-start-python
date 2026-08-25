STATUS.md — Tushar's AI Learning (SINGLE SOURCE OF TRUTH)

Last Updated: 2026-08-25

RULE FOR CLAUDE: "CURRENT STATUS" here overrides ALL other documents. If any doc conflicts, this file wins.

PROTOCOLS (condensed — full history in LEARNING_NOTES.md)
- DOC (2026-08-10): one session = one day number, sequential. Session end: update LEARNING_NOTES.md (one Day block, MAX 5 POINTS — Tushar's rule 2026-08-21), STATUS.md, MEMORY.md, then commit.
- QUIZ (revised 2026-08-21 — Tushar's correction): MAX 5 QUESTIONS PER DAY-TOPIC (not per session). Default: 2–3 on the last day + 1 cold rotation pick (Days 0–current, prioritise weak spots); follow-up nudges count toward that topic's 5. Log the rotation pick. Answers in SENTENCES first; a run or code block is evidence, not an answer.
- COACHING (2026-08-18, verified working): before EVERY exercise — (1) GOAL first: show the exact final printout; (2) numbered step list; (3) ONE step at a time, confirm before the next. If Tushar says "I didn't understand the question": don't repeat it — rebuild with one sentence of concrete context, then a simpler version.
- MORALE (2026-08-24): he undercounts his own wins. Open sessions by naming one concrete previous win before the quiz; when discouragement surfaces, answer with same-session evidence, not reassurance. (Worked 08-25: steady session, no dip.)
- EXERCISE OWNERSHIP (2026-08-24): Tushar writes the exercise code himself — outside AI agents don't. (Honored 08-25.)
- REVISION WEEK (2026-08-17): when Phase 2 completes, one full week of Phase 1+2 revision before Phase 3. No new content; weak-spots list is the syllabus.

MILESTONES (recalibrate at each phase end)
Sep 2026: Phase 2 complete (tool use, LangChain/LlamaIndex, Project 2 hardened) → REVISION WEEK → Nov 2026: Phase 3 complete (LangGraph, agents, MCP, LangSmith) → Dec 2026: Projects 3+4 shipped → Feb 2027: job search opens → Jul 2027: Walmart Staff/Principal AI Engineer.

CURRENT STATUS
Day: 33 COMPLETE | Week: 7 — Phase 2 | Next session = Day 34 (decide at start: agent abstractions cont. — system prompt / state / streaming on create_agent — or Project 2 hardening)
Goal: Staff SWE → AI Backend Engineer (Autodesk) → Staff/Principal AI Engineer, Walmart, July 2027
Just completed: Day 33 (2026-08-25) — create_agent: the framework takes the loop. ReAct = Reason+Act (the academic name for the Day 26–32 loop; nothing to do with React JS). `create_agent(model, tools)` takes the RAW model (binds internally — no bind_tools) and runs the whole invoke→run-tools→append→invoke loop inside `agent.invoke()`; `result["messages"]` is the proof transcript. Deprecation churn handled live (create_react_agent → langchain.agents.create_agent): names churn, the loop doesn't — and seven days of hand-writing it is what makes the black box debuggable. Exercise `exercises/day33_react_agent.py` COMPLETED AND VERIFIED (6-line transcript matched GOAL). Bug caught by tracing BEFORE running: dict key mismatch ("YUNextGenAI" vs "Yieldnext"); learned Python `dict[key]` throws KeyError before `or None` can run — `.get()` is Java's null-returning `map.get()`.
Exercise status: COMPLETED AND VERIFIED — GOAL transcript matched. Code + full notes in LEARNING_NOTES.md Day 33.
Quiz results (Day 32 topic + colds): 3/4. Q1 config-vs-runtime PASSED (1 nudge; his sentence: "binding is static, dispatch is dynamic — the lookup input doesn't exist before execution"). Q2 menu-vs-trips NOT CLEAN — stays open. Q3 fallthrough-vs-give_up PASSED clean in sentences — CLOSED. Q4 sibling-tools PASSED cold — CLOSED (open since Day 27).
Project 1: SHIPPED. Project 2: RAGAS triad + typed RagResponse done; remaining: real Autodesk chunks, model cost decision, ragas upgrade, one paid ragas_evals.py run.
Currently strong on: config-time vs runtime distinction (his best sentence of the session); answering "why" questions in sentences (Q3, Q4 both clean); tracing code before running it.

WEAK SPOTS (revisit)
1. SENTENCES vs CODE — mostly good 08-25 (Q3/Q4 clean sentences) but Q2 drifted to range() mechanics instead of the concept. Keep enforcing, patiently.
2. DIRECTION INVERSIONS — say the arrow out loud, THEN write the description. Not tested 08-25; stays open.
3. MENU-vs-TRIPS (Day 32) — MISSED 08-25: said "1 round" (forgot the N+1 final trip where the model sees the result and answers), then hit the topic cap. The sentence he owes: "rounds come from the question's dependency chain (N links → N+1 invokes), never the menu size." Re-ask cold — priority pick.
CLOSED 2026-08-25: fallthrough guard vs give_up() (was weak spot 4); sibling-tools try/except (was weak spot 2, open since Day 27).

CARRIED FORWARD
(1) Phase 1 recap out loud (owed since 08-08; folds into REVISION WEEK). (2) tool_loop.py line-22 description inversion. (3) Trim-experiment + prefill re-attach re-test.

NEXT SESSION (Day 34) — QUIZ PLAN (max 5 per topic)
Day 33 topic: Q1. ReAct — what do the two words stand for, and where in your day32 code did each half live? Q2. Why does create_agent take the RAW model instead of a bind_tools'd one — and who staples the menu now? Q3. A teammate's create_agent app returns an AIMessage still full of tool_calls — from your Day 28 knowledge, what happened inside the black box?
Cold picks: Q4 (weak spot 3, PRIORITY). 10 bound tools, "price of AAPL", ticker given — how many invoke() calls total, and why does 10 appear nowhere? SENTENCE about dependency chains required. Q5 (weak spot 2, if time): pick a tool docstring and say the arrow out loud before reading it.
Morale opener: name a concrete Day 33 win before the quiz (e.g. "you caught the Yieldnext dict mismatch by tracing, before the code ever ran").

ONE-SENTENCE SUMMARY (say out loud)
"create_agent is my Day 32 loop shipped as a library function — ReAct means reason→act→observe→repeat, the framework runs it inside agent.invoke(), and the messages transcript it returns proves the same rounds still happen."

ACTIVE MENTAL MODELS (top of mind — full running list archived in LEARNING_NOTES.md)
- create_agent = Spring Boot for the loop: raw servlets → @RestController was Day 31's @tool; the hand loop → agent.invoke() is Day 33. Nothing removed, everything relocated.
- ReAct = reason→act→observe→repeat — the paper's name for the loop I hand-wrote for seven days
- Names churn, the loop doesn't: create_react_agent → create_agent mid-exercise; concepts have the longer half-life
- The debugging dividend: "agent hung" = iteration budget exhausted (Day 28); "API rejected" = orphaned tool_use missing its tool_result (Day 27) — I can see inside the black box because I built one
- create_agent binds internally — raw model in; bind_tools'd model in would print the menu twice
- result["messages"] = the grown transcript, returned: Human → AI(tool_calls) → Tool → AI(tool_calls) → Tool → AI(text, end_turn)
- Python dict[key] THROWS on miss (KeyError) — `x[k] or None` can't rescue what already raised; .get() is Java's null-returning map.get()
- getattr(m, "tool_calls", None) = null-safe field check on a mixed list of message DTOs
- bind_tools = printing the menu (config-time); rounds = trips to the kitchen (runtime, N links → N+1 invokes) — MENU SIZE NEVER ENTERS THE MATH
- Binding is static, dispatch is dynamic — the input to the lookup doesn't exist before execution (his sentence, Day 33)
- give_up() = forced landing: no tools bound → tool_use structurally impossible → honest end_turn text is the only exit
- Transcript order: AIMessage BEFORE its ToolMessages; every tool_use needs its tool_result or the API rejects the turn
- try around the whole dispatch loop kills innocent siblings — exception on tool #2 skips #3 and all appends
- A run is evidence, not an explanation — the check question wants a sentence

PROGRESS LOG (most recent first — headline only)
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
