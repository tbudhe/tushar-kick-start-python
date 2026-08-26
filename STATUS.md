STATUS.md — Tushar's AI Learning (SINGLE SOURCE OF TRUTH)

Last Updated: 2026-08-26

RULE FOR CLAUDE: "CURRENT STATUS" here overrides ALL other documents. If any doc conflicts, this file wins.

PROTOCOLS (condensed — full history in LEARNING_NOTES.md)
- DOC (2026-08-10): one session = one day number, sequential. Session end: update LEARNING_NOTES.md (one Day block, MAX 5 POINTS — Tushar's rule 2026-08-21), STATUS.md, MEMORY.md, then commit.
- QUIZ (revised 2026-08-21 — Tushar's correction): MAX 5 QUESTIONS PER DAY-TOPIC (not per session). Default: 2–3 on the last day + 1 cold rotation pick (Days 0–current, prioritise weak spots); follow-up nudges count toward that topic's 5. Log the rotation pick. Answers in SENTENCES first; a run or code block is evidence, not an answer.
- COACHING (2026-08-18, verified working): before EVERY exercise — (1) GOAL first: show the exact final printout; (2) numbered step list; (3) ONE step at a time, confirm before the next. If Tushar says "I didn't understand the question": don't repeat it — rebuild with one sentence of concrete context, then a simpler version.
- DEBUG PROTOCOL (NEW 2026-08-26): when a result doesn't change after an edit, READ THE FILE ON DISK before theorising — the edit may have lived only in chat. When behavior and docs disagree, read the installed library source in .venv. Probe config with BEHAVIOR, never formatting.
- MORALE (2026-08-24): he undercounts his own wins. Open sessions by naming one concrete previous win before the quiz; when discouragement surfaces, answer with same-session evidence, not reassurance. (Worked 08-25 and 08-26: steady, no dip.)
- EXERCISE OWNERSHIP (2026-08-24): Tushar writes the exercise code himself — outside AI agents don't. (Honored 08-25, 08-26.)
- REVISION WEEK (2026-08-17): when Phase 2 completes, one full week of Phase 1+2 revision before Phase 3. No new content; weak-spots list is the syllabus.

MILESTONES (recalibrate at each phase end)
Sep 2026: Phase 2 complete (tool use, LangChain/LlamaIndex, Project 2 hardened) → REVISION WEEK → Nov 2026: Phase 3 complete (LangGraph, agents, MCP, LangSmith) → Dec 2026: Projects 3+4 shipped → Feb 2027: job search opens → Jul 2027: Walmart Staff/Principal AI Engineer.

CURRENT STATUS
Day: 34 COMPLETE | Week: 7 — Phase 2 | Next session = Day 35 (decide at start: checkpointer + thread_id — the framework's session store — or streaming on create_agent, or Project 2 hardening)
Goal: Staff SWE → AI Backend Engineer (Autodesk) → Staff/Principal AI Engineer, Walmart, July 2027
Just completed: Day 34 (2026-08-26) — create_agent cont.: system prompt moves to config, state stays mine. `system_prompt=` is KEYWORD-ONLY (positional args stop at model, tools) and is Day 32's `messages[0]` relocated to config time — factory.py:1417 does `messages = [request.system_message, *messages]` on EVERY model call, and it never lands in `result["messages"]` (injected at call time, not stored in state). State did NOT move: the agent is stateless between invokes — same object, part B (one message in) had amnesia, part C (`result["messages"] + follow_up`) answered correctly. THE DAY'S REAL FIND: a formatting proof marker ("begin with [YNXT-BOT]") was silently dropped by the model on the turn concluding a tool loop and produced a false "framework is broken" verdict that survived three tests; a behavioral marker ("reply in French") proved delivery on the first run. The dispute was settled by reading the installed library source in .venv.
Exercise status: `exercises/day34_react_agent.py` COMPLETED AND VERIFIED — B/C contrast matched GOAL. Code + full notes in LEARNING_NOTES.md Day 34.
Quiz results (Day 33 topic + cold): 4/4. Q1 ReAct halves PASSED (2 nudges; inverted Act at first). Q2 raw-vs-bound model PASSED clean and unprompted, with a drift point he added himself (advertised menu vs dispatch registry can disagree). Q3 tool_calls-still-present PASSED clean (iteration budget exhausted). Q4 menu-vs-trips PASSED COLD with the dependency-chain sentence — CLOSED.
Project 1: SHIPPED. Project 2: RAGAS triad + typed RagResponse done; remaining: real Autodesk chunks, model cost decision, ragas upgrade, one paid ragas_evals.py run.
Currently strong on: cold recall of concepts he missed the day before (Q4); reading a signature/source instead of guessing at an API; self-finding his own bugs two sessions running.

WEAK SPOTS (revisit)
1. DIRECTION INVERSIONS / SLOT SWAPS — PRIORITY, fired TWICE on 08-26: ReAct's Act half ("request a tool" is still the model talking; Act is MY code running the function) and the step-5 fill-in-the-blank slots swapped (put "stateless" in the wrong hole). Drill: say the arrow out loud BEFORE writing the description.
2. SENTENCES vs CODE — good on 08-26 (Q2, Q3, Q4 all clean sentences). Keep light pressure, don't grind.
CLOSED 2026-08-26: MENU-vs-TRIPS (was weak spot 3, open since Day 32) — answered cold: "rounds come from the question's dependency chain (N links → N+1 model invokes), never the menu size."

CARRIED FORWARD
(1) Phase 1 recap out loud (owed since 08-08; folds into REVISION WEEK). (2) tool_loop.py line-22 description inversion. (3) Trim-experiment + prefill re-attach re-test. (4) Clean the day34 file: probe lines are commented out, system_prompt is still the French test string — restore SYSTEM_PROMPT before committing it as reference.

NEXT SESSION (Day 35) — QUIZ PLAN (max 5 per topic)
Day 34 topic: Q1. Where did the system prompt live in your Day 32 hand loop, where does it live now, and why does it never show up in `result["messages"]`? Q2. Same agent object, two invokes seconds apart — B forgot, C remembered. One sentence: why? Q3. Why was "[YNXT-BOT]" a bad proof marker and "reply in French" a good one?
Cold picks: Q4 (weak spot 1, PRIORITY) — pick any tool docstring in the repo and say the ARROW out loud before reading the description; then state which side is input and which is output. Q5 (if time, Day 28) — a final AIMessage still holding tool_calls: what happened, and what would give_up() have done instead?
Morale opener: name a concrete Day 34 win before the quiz — he found the duplicated model/agent definitions himself, and the library source (not either of our hypotheses) settled the system_prompt dispute because he went and printed the signature.

ONE-SENTENCE SUMMARY (say out loud)
"The system prompt moved to config time — the framework prepends it on every model call — but state didn't move: the agent is stateless between invokes, so conversation memory isn't something it has, it's something I pass in on every call."

ACTIVE MENTAL MODELS (top of mind — full running list archived in LEARNING_NOTES.md)
- system_prompt = Day 32's messages[0], relocated to config time; factory.py prepends it every call and it never lands in result["messages"]
- The agent is stateless between invokes — a reusable @RestController bean; memory is something I pass in, not something it has
- Stateless = horizontally scalable; checkpointer= is the session-store decision made explicit
- Probe config with BEHAVIOR, not formatting — a model concluding a tool loop drops "start with [TAG]" but not "reply in French"
- The library is in my .venv — when docs and behavior disagree, read the source; it outranks both hypotheses
- When the output doesn't move, verify the code that ran is the code on disk
- No tools bound → tool_use structurally impossible → text is the only exit: give_up()'s honest landing and an unguarded model's hallucination are the same mechanic
- create_agent = Spring Boot for the loop: raw servlets → @RestController was Day 31's @tool; the hand loop → agent.invoke() is Day 33
- ReAct = reason→act→observe→repeat; Reason is the model's turn (including asking for a tool), Act is MY code running it and appending the result
- Names churn, the loop doesn't: create_react_agent → create_agent mid-exercise
- The debugging dividend: "agent hung" = iteration budget exhausted (Day 28); "API rejected" = orphaned tool_use missing its tool_result (Day 27)
- create_agent binds internally — raw model in; a bind_tools'd model would print the menu twice, and the tools you pass separately are what actually dispatch
- result["messages"] = the grown transcript, returned: Human → AI(tool_calls) → Tool → AI(tool_calls) → Tool → AI(text, end_turn)
- Python dict[key] THROWS on miss (KeyError); .get() is Java's null-returning map.get()
- Python takes the LAST assignment silently — duplicated definitions shadow, where Java's compiler would refuse
- bind_tools = printing the menu (config-time); rounds = trips to the kitchen (runtime, N links → N+1 invokes) — MENU SIZE NEVER ENTERS THE MATH
- Binding is static, dispatch is dynamic — the input to the lookup doesn't exist before execution (his sentence, Day 33)
- Transcript order: AIMessage BEFORE its ToolMessages; every tool_use needs its tool_result or the API rejects the turn
- try around the whole dispatch loop kills innocent siblings
- A run is evidence, not an explanation — the check question wants a sentence

PROGRESS LOG (most recent first — headline only)
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
