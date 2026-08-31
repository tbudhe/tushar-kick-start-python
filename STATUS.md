STATUS.md — Tushar's AI Learning (SINGLE SOURCE OF TRUTH)

Last Updated: 2026-08-31

RULE FOR CLAUDE: "CURRENT STATUS" here overrides ALL other documents. If any doc conflicts, this file wins.

PROTOCOLS (condensed — full history in LEARNING_NOTES.md)
- DOC (2026-08-10): one session = one day number, sequential. Session end: update LEARNING_NOTES.md (one Day block, MAX 5 POINTS), STATUS.md, MEMORY.md, then commit.
- QUIZ (2026-08-28, HONORED 08-31): **MAX 3 QUESTIONS PER SESSION, ONE PART EACH.** A question with sub-parts counts as that many questions — don't write them. If an answer is incomplete, Claude COMPLETES IT in one line and moves on; a gap never becomes a follow-up question. Nudges count.
- COACHING (2026-08-18, verified working): before EVERY exercise — (1) GOAL first: show the exact final printout; (2) numbered step list; (3) ONE step at a time, confirm before the next. Fill-in-the-blank frames outperform open questions (verified again 08-31: the four-blank thread_id frame got all four slots clean, no nudge).
- **CODE DELIVERY (NEW 2026-08-31, Tushar's explicit pushback):** when he is mid-exercise, paste **COMPLETE blocks** with every variable's origin named — never fragments. On 08-31 a snippet referencing `msg`/`node` when his file had `m`/`label` cost two round-trips; he said "I don't see msg... be specific and correct" and was right. A fragment assumes a file state Claude cannot see.
- **EXAMPLE FIDELITY (NEW 2026-08-31):** examples must use HIS tools with HIS semantics. Claude traced `get_ticker` returning a price, contradicting his own Day 30 two-tool chain, and he reported confusion. Check the repo's actual signatures before inventing a trace.
- DEBUG PROTOCOL (2026-08-26/27, EXTENDED 08-31): when a result doesn't change after an edit, READ THE FILE ON DISK before theorising. When behavior and docs disagree, read the installed library source in .venv. Probe config with BEHAVIOR, never formatting. A good instrument has exactly ONE explanation for its failure. NEW: an instrument that FILTERS its input reports the filter as much as the signal.
- MORALE (2026-08-24, EXTENDED 08-28): he undercounts his wins — open with one concrete previous win before the quiz, answer discouragement with same-session evidence. When frustration surfaces, FIRST check whether Claude caused it. A process complaint gets a protocol fix, not encouragement.
- EXERCISE OWNERSHIP (2026-08-24): Tushar writes the exercise code himself — outside AI agents don't. (Honored 08-25 → 08-31.)
- REVISION WEEK (2026-08-17): when Phase 2 completes, one full week of Phase 1+2 revision before Phase 3. Weak-spots list is the syllabus.
- ENV NOTE (2026-08-27): the .venv python symlink does not resolve from Claude's mounted shell — Claude cannot run his code. Claude reads source in .venv and reasons; Tushar runs everything.

MCP TIMING DECISION (2026-08-28, Tushar's call): KEEP THE SEQUENCE. MCP stays in Phase 3 (~Nov 2026); no spike day, no reorder. Reassess only at Phase 2 close.

MILESTONES (recalibrate at each phase end)
Sep 2026: Phase 2 complete (tool use, LangChain/LlamaIndex, Project 2 hardened) → REVISION WEEK → Nov 2026: Phase 3 complete (LangGraph, agents, MCP, LangSmith) → Dec 2026: Projects 3+4 shipped → Feb 2027: job search opens → Jul 2027: Walmart Staff/Principal AI Engineer.

CURRENT STATUS
Day: 36 COMPLETE (2026-08-31) | Week: 7 — Phase 2 | Next session = Day 37 (async agent).
Goal: Staff SWE → AI Backend Engineer (Autodesk) → Staff/Principal AI Engineer, Walmart, July 2027
Topic completed: Day 36 — streaming on `create_agent`. `.invoke()` and `.stream()` run the SAME graph; streaming changes WHEN you look, not what happens. Three modes measured side by side in one file: `updates` (node-keyed delta, N yields, flat size), `values` (whole growing list, N+1 yields, no node key), `messages` (`(token, metadata)` TUPLE, sub-message granularity). Ship verdict: `stream_mode=["updates","messages"]` together — tokens drive the typewriter, updates give the node boundary and the "calling get_price…" badge; `values` is a state inspector, not a transport.
Exercise: `exercises/day36_streaming_agent.py` COMPLETE — A (updates, 5 yields, ReAct loop visible: model→tools→model→tools→model), B (values, 6 yields, 1→6 messages, NO SystemMessage anywhere), C (messages, token-by-token with timed silent gaps).
NEW FINDINGS THIS SESSION: (1) **5 vs 6** — `values` emits the initial state before any node runs; `updates` never does. N+1 snapshots vs N events. (2) His own numbers: `input_tokens 755→858→950` and `stop_reason tool_use→tool_use→end_turn` — the transcript is re-sent in full every round and the loop's exit condition is visible in the stream. (3) **Claude's prediction failed, the data won**: the 0.6s gaps were time-to-first-token before model bursts, NOT tool execution — his dict-lookup tools are instant. Adding `time.sleep(2)` to `get_price` put a 2.0s gap exactly before `42.0|`, isolating the tool gap deliberately. (4) `stream_mode="messages"` carries TOOL output interleaved with model prose, indistinguishable without `metadata["langgraph_node"]`.
Quiz results: 3 asked, 3 passed. Q1 `thread_id` four-blank frame — all four slots correct, NO nudge. Q2 shared thread_id in production — answered with the leak framing unprompted ("cross-user data leakage in both directions"). Q3 cold Day 27 orphaned `tool_use` — he didn't just answer, he RAN A FOUR-CASE CONTROL SET including the inverted error (`tool_result` with a bogus id → "unexpected tool_use_id"). CARRIED-FORWARD ITEM 5 CLOSED.
Project 1: SHIPPED. Project 2: RAGAS triad + typed RagResponse done; remaining: real Autodesk chunks, model cost decision, ragas upgrade, one paid ragas_evals.py run.
Currently strong on: turning a quiz question into a run experiment with a control group; reading cost and control-flow signals out of raw stream metadata; pushing back when Claude's example or snippet is wrong — twice this session, correct both times.

WEAK SPOTS (revisit)
1. SENTENCES vs CODE — good five sessions running. Keep light pressure, don't grind.
2. `getattr` vs `.get()` — NEW 2026-08-31. Wrote `getattr(TICKERS, "tool_calls", None)` on a dict: attribute access where key access was needed, returning None for EVERY input with no exception. Later used `getattr(msg, "tool_calls", None)` correctly on a message object — both cases now live in day36 file. Watch once more, don't drill.
3. Tendency to answer only the first part of a multi-part prompt — NO LONGER TESTED FOR (multi-part prompts banned by the quiz rule). Watch only.
CLOSED 2026-08-28: DIRECTION INVERSIONS / SLOT SWAPS (open since Day 26).
CLOSED 2026-08-26: MENU-vs-TRIPS (open since Day 32).

CARRIED FORWARD
(1) Phase 1 recap out loud (owed since 08-08; folds into REVISION WEEK). (2) Trim-experiment + prefill re-attach re-test. (3) **NEW — Day 36 deferred check (~60 seconds):** in day36 Part C, add `print(metadata.get("langgraph_node"), repr(token.content))` inside the loop to settle whether the 3–10s silent gaps in run 2 were API latency or dropped `input_json_delta` chunks (streamed tool ARGUMENTS carry `partial_json`, not `text`, so the isinstance filter discards them while they still reset the timer). Good Day 37 opener. (4) Delete `time.sleep(2)` from `get_price` before reusing day36 as a reference.
DROPPED 2026-08-31: `[YNXT-BOT]` probe removal (done), Day 27 orphaned-tool_use re-ask (closed, answered by him with a control set), tool_loop.py line-22 item (file not found, never resurfaced).

PHASE 2 CLOSE PLAN (5 sessions to the end of Phase 2, then REVISION WEEK)
- Day 37 — Async agent. `ainvoke`/`astream`, concurrent tool execution, and where async does NOT help. Artifact: day37_async_agent.py timing two tools serial vs concurrent. (Short day — his Node.js background carries it. Day 36's `time.sleep(2)` tool is already a ready-made slow tool to parallelize.)
- Day 38 — LlamaIndex vs LangChain. Only untouched Phase 2 item. Rebuild EXISTING retrieval in LlamaIndex over the same chunks; write the 5-line "when I'd pick which" verdict. Artifact: llamaindex/ + verdict in notes.
- Day 39 — Project 2 hardening I: real Autodesk chunks through ingest.py; re-run retrieval audit; note what broke vs the toy corpus. (Also: `PRICES[ticker]` KeyError vs `.get()` → None is a hardening pattern to carry over.)
- Day 40 — Project 2 hardening II: model cost decision (haiku vs sonnet, measured not guessed), ragas upgrade, ONE paid ragas_evals.py run with the numbers recorded.
- Day 41 — PHASE 2 CLOSE: no new content. Capstone review of Days 22-40, weak-spots list becomes the REVISION WEEK syllabus, Phase 1 recap out loud (owed since 08-08).
Then: REVISION WEEK (Phase 1+2, no new content) → Phase 3 opens ~late September.

NEXT SESSION (Day 37) — QUIZ PLAN (MAX 3, ONE PART EACH)
Q1. `updates` vs `values` — which one yields more, and why the extra one? One line.
Q2. You're building a chat UI on this agent. Which stream_mode(s) do you ship, and what does each one drive?
Q3. Cold pick, Day 32: menu size vs number of rounds — what determines how many trips the model makes?
Morale opener: on Q3 he didn't answer the question, he ran a four-case control set and surfaced the inverted `tool_result` error nobody predicts — and he caught two of Claude's own mistakes mid-session and was right both times.

ONE-SENTENCE SUMMARY (say out loud)
"Streaming didn't change what the agent does — it changed when I'm allowed to look; `updates` tells me what changed, `values` tells me what is, and `messages` tells me what's being typed right now, and a real UI needs the first and the last."

ACTIVE MENTAL MODELS (top of mind — full running list archived in LEARNING_NOTES.md)
- updates = what changed / values = what is / messages = what's being typed right now
- `values` yields N+1 (it includes the initial state), `updates` yields N — and `values` re-sends the whole list every time
- `stream_mode="messages"` carries TOOL output too, interleaved and indistinguishable — split on `metadata["langgraph_node"]`
- A timer measures gaps between chunks you chose to PRINT, not gaps in the stream — a filtered instrument reports the filter
- `create_agent()` is build-time, `.stream()`/`.invoke()` is request-time — never chain them
- `getattr(obj,"x")` asks for an ATTRIBUTE; `dict.get("x")` asks for a KEY — the swap fails silently, None for every input
- checkpointer = Spring Session + Redis; thread_id = JSESSIONID; the agent is still the stateless @RestController
- thread_id → lookup key into the saver's store; the GRAPH loads before the model call and appends after — the model never sees the key
- result["messages"] is the WHOLE thread, never the delta
- InMemorySaver in 12 pods = 12 disconnected dicts; amnesia is a CORRECTNESS failure, not a latency one
- A tool's model obeys the DESCRIPTION while the function obeys the SIGNATURE — the silent-wrong-answer case is worse than the KeyError
- is_error is data, not a crash — the model must SEE the failure to recover from it
- Config is re-applied every call; state is accumulated — system_prompt is config, messages are state
- A good instrument has exactly ONE explanation for its failure
- The library is in my .venv — when docs and behavior disagree, read the source
- create_agent = Spring Boot for the loop; ReAct = reason→act→observe→repeat
- bind_tools = printing the menu (config-time); rounds = trips to the kitchen (runtime) — MENU SIZE NEVER ENTERS THE MATH
- Transcript order: AIMessage BEFORE its ToolMessages; every tool_use needs its tool_result or the API rejects the turn
- A run is evidence, not an explanation — the check question wants a sentence

PROGRESS LOG (most recent first — headline only)
Day 36: streaming on the agent — updates/values/messages measured side by side, 5-vs-6 yields explained, ship verdict is both modes at once; token growth 755→858→950 read out of his own metadata; Claude's tool-gap prediction falsified by his timer, then the gap manufactured on purpose with sleep(2); 3/3 quiz with a four-case control set on the cold question, carried-forward item 5 CLOSED
Day 35: checkpointer + thread_id — memory gets a home outside the agent; A/B/C/D all green with Part D predicted 4/4 before running; the [YNXT-BOT] control group closed Day 34's open question; 3/3 + clean cold pass, DIRECTION INVERSIONS CLOSED; quiz volume broke him mid-session → quiz rule rewritten to 3 single-part questions
Day 34: system prompt moves to config, state stays mine — stateless agent proven by the B/C contrast; false "framework broken" verdict overturned by reading factory.py in .venv; proof markers must be behavioral; quiz 4/4, menu-vs-trips CLOSED
Day 33: create_agent takes the loop — ReAct named, deprecation churn handled live, transcript proved the framework runs my Day 32 rounds; quiz 3/4, TWO weak spots closed
Day 32: bind_tools kills the plumbing, the loop survives — round-traced chain via response.tool_calls; menu-vs-trips resolved; quiz 4/4, THREE weak spots closed
Day 31: LangChain intro — @tool collapsed the four registries into one decorator; direction inversion caught live; give_up() WHY closed
Day 30: Multi-step planning FINISHED — chain ran (YNXT→42.0→"$42.00"); INPUT_MODELS fourth registry closed the landmine; self-found AAPL allowlist bug
Day 29: Multi-step planning STARTED — chain concept, world-knowledge bypass, two directions = two tools, three registrations
Day 28: Max-iteration guards — for range(MAX_ITERATIONS), give_up() forced landing, sabotage verified
