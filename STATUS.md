STATUS.md — Tushar's AI Learning (SINGLE SOURCE OF TRUTH)

Last Updated: 2026-09-24 (Day 48 - PHASE 3: Claude inside the loop. A tool-calling agent built by hand in `exercises/day48_agent_loop.py`)

RULE FOR CLAUDE: "CURRENT STATUS" here overrides ALL other documents. If any doc conflicts, this file wins.

PROTOCOLS (condensed — full history in LEARNING_NOTES.md)
- DOC (2026-08-10): one session = one day number, sequential. Session end: update LEARNING_NOTES.md (one Day block, MAX 5 POINTS), STATUS.md, MEMORY.md, then commit.
- QUIZ (2026-08-28, HONORED 08-31 → 09-04): **MAX 3 QUESTIONS PER SESSION, ONE PART EACH.** A question with sub-parts counts as that many questions — don't write them. If an answer is incomplete, Claude COMPLETES IT in one line and moves on; a gap never becomes a follow-up question. Nudges count.
- COACHING (2026-08-18, verified working): before EVERY exercise — (1) GOAL first: show the exact final printout; (2) numbered step list; (3) ONE step at a time, confirm before the next. SHAPE BEFORE STEPS (2026-09-24): after 6/6 steps matched he said \"I didn't understand today's logic\" - compliance is not comprehension. For any new framework construct, show the PLAIN-CODE equivalent (<=12 lines, no framework) plus a one-line real-world analogy BEFORE the goal printout. Day 48's fix that landed: the Slack coworker who can't touch the DB + a 10-line `while True` loop mapped row-by-row to the nodes.
- WHY BEFORE INSTRUMENT (2026-09-01, HONORED 09-02 and 09-04): every non-obvious line of scaffolding gets ONE sentence of purpose BEFORE the code — what claim it tests, and what the two possible outcomes look like.
- CONTENT DENSITY (2026-09-02, **HONORED 09-04 — it worked**): at most **ONE library-internals dive per session**, and 09-04 used ZERO. Teach the framework's SHAPE before its footnotes. Day 38b opened with the five-stage pipeline on one screen and he immediately reasoned forward from it unprompted. Keep this cap.
- ANALOGY DOMAIN (2026-09-02, his explicit correction): **anchor analogies in Node.js/TypeScript or C#, NOT Java/Spring** — "I am not from Java." EF Core vs raw ADO.NET landed instantly on 09-04.
- SHOW HIS OWN CODE (2026-09-02, HONORED 09-04): when referencing his files, PASTE THE CODE inline with exact file:line — he cannot browse installed packages.
- CODE DELIVERY (2026-08-31, EXTENDED 09-04): paste COMPLETE blocks, name the file AND the exact position in it. 09-04 FAILURE: "add it after ask_llamaindex(), before if __name__" was not precise enough — line numbers had drifted, the block landed INSIDE the __main__ block, and it silently swallowed the whole COMPARISON tail into the function body. FIX: when giving an insertion point, read the file on disk FIRST and quote the two real anchor lines it goes between. 09-23 FAILURE: "change line 15 to `if True:`" was misapplied TWICE (edited line 16 -> `return True` -> KeyError: True; then `if state["attempts"] is True:` -> stopped after 1). FIX: for any edit inside a function, give the WHOLE FUNCTION as a replacement block, never a one-line "change line N".
- EXAMPLE FIDELITY (2026-08-31): examples must use HIS tools with HIS semantics. His Anthropic key env var is `CLAUDE_API_KEY`, not `ANTHROPIC_API_KEY`; his QA model is `claude-opus-4-8`; his RAG entry point is `rag_service.answer_question()`. VERSION FIDELITY (2026-09-23): predict from HIS INSTALLED version, not memory - langgraph is 1.2.9 and its DEFAULT_RECURSION_LIMIT is 10007 (`langgraph/_internal/_config.py:32`, env `LANGGRAPH_DEFAULT_RECURSION_LIMIT`), not 25. Claude predicted 25 and was wrong; check `.venv/.../*.dist-info` before any library-behaviour prediction.
- DEBUG PROTOCOL (2026-08-26/27, EXTENDED 08-31, APPLIED 09-01 → 09-04): when a result doesn't change after an edit, READ THE FILE ON DISK. When behavior and docs disagree, read the installed library source in .venv (subject to the CONTENT DENSITY cap). Probe config with BEHAVIOR, never formatting. A good instrument has exactly ONE explanation for its failure. An instrument that FILTERS its input reports the filter. DOC-EDIT NOTE (2026-09-04, Claude's near-miss): when patching this file by string index, anchor on a UNIQUE marker — "CURRENT STATUS" also appears inside the RULE FOR CLAUDE line, and slicing on the first match silently deleted the whole PROTOCOLS block. Restored with `git show HEAD:STATUS.md > STATUS.md` (plain `git checkout --` fails in the mounted shell: cannot unlink).
- MORALE (2026-08-24, EXTENDED 08-28): he undercounts his wins — open with one concrete previous win before the quiz. When frustration surfaces, FIRST check whether Claude caused it. A process complaint gets a protocol fix, not encouragement.
- EXERCISE OWNERSHIP (2026-08-24): Tushar writes the exercise code himself. (Honored 08-25 → 09-04.)
- REVISION WEEK (2026-08-17): when Phase 2 completes, one full week of Phase 1+2 revision before Phase 3. Weak-spots list is the syllabus.
- ENV NOTE (2026-08-27): the .venv python symlink does not resolve from Claude's mounted shell — Claude cannot run his code. Claude reads source and reasons; Tushar runs everything.
- EDITOR NOTE (2026-09-02): VS Code "organize imports" HOISTS every import above a `sys.path.insert(...)` bootstrap and breaks repo-root imports from `exercises/`. Fix applied: `# isort: skip_file`. Permanent fix still unconfirmed: `.vscode/launch.json` with `"env": {"PYTHONPATH": "${workspaceFolder}"}`.

MCP TIMING DECISION (2026-08-28, Tushar's call): KEEP THE SEQUENCE. MCP stays in Phase 3 (~Nov 2026); no spike day, no reorder. Reassess only at Phase 2 close.

MILESTONES (recalibrate at each phase end)
Sep 2026: Phase 2 complete (tool use, LangChain/LlamaIndex, Project 2 hardened) → REVISION WEEK → Nov 2026: Phase 3 complete (LangGraph, agents, MCP, LangSmith) (incl. 2-session CELERY BUILD in week 2) → late Nov 2026: GUARDRAILS MODULE (added 2026-09-17, 4 sessions) → Dec 2026: Projects 3+4 shipped → Feb 2027: job search opens → Jul 2027: Walmart Staff/Principal AI Engineer.

CURRENT STATUS
Day: 48 COMPLETE (2026-09-24) | Week: PHASE 3, week 1 | Next session = Day 49.
Goal: Staff SWE -> AI Backend Engineer (Autodesk) -> Staff/Principal AI Engineer, Walmart, July 2027
Topic: Day 48 - CLAUDE INSIDE THE LOOP. Hand-built tool-calling agent in `exercises/day48_agent_loop.py` (his code, 6/6 steps, goal printout matched line for line): State{messages: list} -> `agent` (model.bind_tools([get_price]), claude-opus-4-8) -> `should_continue` ("tools" if last.tool_calls else END) -> `tools` (TOOLS[name].invoke(args) -> ToolMessage with the same toolu_ id) -> plain edge `tools -> agent` (the backward edge) -> invoke with recursion_limit=10 -> 4 messages.
FINDINGS THIS SESSION: (1) CLAUDE NEVER RUNS THE TOOL - step 1 printed `[{'name': 'get_price', 'args': {'ticker': 'YNXT'}, 'id': 'toolu_...'}]` and no price; the `tools` node is the executor. (2) NO REDUCER = OVERWRITE: nodes return `state["messages"] + [response]`; he dropped the brackets -> `TypeError: can only concatenate list (not "AIMessage") to list`. (3) `return` INDENTED INSIDE `for` in his `tools` node - invisible with 1 tool call, would drop the 2nd ToolMessage and the API would reject the next call. Fixed; homework tests it. (4) ROUTER vs LOOP: router = switch (choose once, never return); agent = router + a PLAIN edge back to Claude = while. (5) WHY LANGGRAPH (his question "just for routing?"): for this example a `while` loop is enough; LangGraph earns its place with checkpointing/resume, human-in-the-loop pause, per-node streaming. C# anchor: async method vs Azure Durable Functions.
Quiz results: 3/3, clean (Q3 in his words: "a backstop, not a budget").
PREDICTION RECORD: 6 stated by Claude, 6 MATCH (tool_calls list; 2 messages -> AIMessage; 3 -> ToolMessage; tools/__end__; node list; full goal printout).
COACHING NOTE: every step matched and he still said "I didn't understand today's logic" - Claude had given steps without the SHAPE. The plain while-loop + Slack-coworker version landed; he followed with a sharp design question (why LangGraph at all). Protocol added: SHAPE BEFORE STEPS. Also: he twice deleted the wrong `__main__` lines (kept old, removed new) -> for __main__ changes say "delete everything from `if __name__` to end of file, then paste".
Exercise: `exercises/day48_agent_loop.py` - DONE. HOMEWORK (not yet run): change the question to "Compare the prices of YNXT and AAPL." Predict: parallel tool calls -> [tools] twice, 4 messages; or sequential -> 6 messages.
OPEN: (a) paid ragas run - still needs yes/no + dollar cap (will not ask again); (b) Render service not created (BACKLOG LANE item 1); (c) `dgx_sim.py`, `image_split.py` committed in a240b8e as "need review after phase 3" - not curriculum; (d) NVIDIA 90-sec intro NOT done on Day 48 (he stopped after the core) - moves to Day 49 tail.
Project 1: SHIPPED. Project 2: pushed; remaining: Render service, remote eval run, model cost decision, ragas upgrade, paid ragas run, grow CASES. Project 3 (LangGraph Autodesk agent): router graph (day46_graph.py) + hand-built agent loop (day48) - next: put `rag_service.answer_question` in as a tool.
Currently strong on: predicting before running; asking "why do we need the framework at all?" - a staff-level question.
WEAK SPOTS (revisit)
1. MENU-vs-TRIPS — **CLOSED 2026-09-04.** Answered cold and correctly for the second session running (Q3, refine at top_k=10, with the async caveat attached unprompted). Do not re-drill.
2. SENTENCES vs CODE — good eight sessions running. Keep light pressure, don't grind.
3. `getattr` vs `.get()` — 2026-08-31. Still not retested. Watch once more, don't drill.
4. LLAMAINDEX SHAPE (opened 2026-09-02) — **CLOSED 2026-09-04.** He can now state what the framework IS in one sentence ("it replaced my glue code, not my retrieval") and reasoned forward from the shape unprompted.
5. LABEL SETS / ANSWERHOOD (opened 2026-09-08) — labelled a precision test by SOURCE DOCUMENT, twice, including the known false-positive chunk. The rule to re-test: "if a reader got ONLY this chunk, could they do the thing?" Retest by asking him to label 3 new questions cold at the start of REVISION WEEK.
6. PHASE 1 MODEL LAYER (opened 2026-09-17) - training vs inference collapsed into RAG vocabulary. Re-test the five sentences across REVISION WEEK, max 3 per session: Day 44 = tokens, attention, generation.
7. IO-BOUND vs CPU-BOUND IN PYTHON (opened 2026-09-17, from a REAL AI-engineer interview): asked about Celery (said "I don't know", no bridge) and IO operations (answered spawn/exec/fork child processes - that is the CPU-bound answer). Fix: IO-bound -> asyncio or threads (GIL released while waiting); CPU-bound -> processes. Celery pools: prefork for CPU, gevent/threads for IO (LLM calls are IO). Fold into Day 44 agents block (Day 37 async). Also practise the BRIDGE answer for unknown tools.
CLOSED 2026-08-28: DIRECTION INVERSIONS / SLOT SWAPS (open since Day 26).

CARRIED FORWARD
(0) **Day 39's biggest item — RETRIEVAL PRECISION EVAL — BUILT 2026-09-08** (`precision_eval.py`, $0 per run, no LLM). What it opened in turn: (a) GROW CASES to 15-20 questions — at n=4 each question is 25 points; (b) DECIDE `N_RESULTS`: 2 -> 6 makes hit@2 -> 1.000 on this corpus but triples context per request, and the sweep shows k=3,4,5 buy nothing — decide it as a cost/precision trade, measured; (c) RERANKING is the real fix and stays in Phase 3, now with his own hit@k cliff as the argument for it; (d) still open from Day 39: hard-bound the chunker (split inside an oversized paragraph), the title-prepend experiment in `ingest_corpus.py`, `category` metadata written but unused by the audit.
(1) Phase 1 recap out loud (owed since 08-08; folds into REVISION WEEK). (2) Trim-experiment + prefill re-attach re-test. (3) DONE 2026-09-17: `time.sleep(2)` deleted from `get_price` in day36. (4) Optional 2-minute Day 37 extension: add a batch `get_prices(tickers: list[str])` tool and show the 10-company question collapsing from 10 rounds to 1. (5) **THE QUIET TWIN — named 09-04, NOT tested:** two embedding models with the SAME width (384) but different vector spaces (MiniLM vs `bge-small-en-v1.5`) produce NO error and silently wrong neighbours. Part B proved only the loud failure. Costs a ~130MB model download; worth 10 minutes inside REVISION WEEK. (6) `.vscode/launch.json` CONFIRMED CREATED 2026-09-09 (appeared untracked in git status; committed in 35f29df). (7) Optional 5-minute parity close: add `SimilarityPostprocessor(similarity_cutoff=0.301)` to the query engine and show the refusal case coming back.

INTERVIEW DETOUR (declared 2026-09-08 — PAUSED 2026-09-17 by Tushar in favour of REVISION WEEK; kept for reference, re-slot only if he names a date)
TRIGGER: Tushar has a real interview (not a recruiter screen) WITHIN 2 WEEKS, for a CONTRACT AI ENGINEER role. Loop format: EXPERIENCE DEEP-DIVE + AI/ML SYSTEM DESIGN. **No live-coding screen** — so the Python-under-time-pressure risk is NOT in play for this loop and must not be prepped for.
DECISION: compress by REORDERING, not by adding sessions. Cadence stays ~4/week — Day 38 proved that pushing volume costs more than it buys. Phase 4 (portfolio/deploy/story) is pulled FORWARD; Phase 2 close, REVISION WEEK and Phase 3 all slide right ~2 weeks. Phase 3's CrewAI/AutoGen/multi-agent depth is NOT interview-load-bearing for this role — cut it to LangGraph + agent loop + evals, which he already has from Days 31-37.
- Day 41 (Wed Sep 9) - DEPLOY config: DONE, pushed (35f29df).
- Day 42 (Thu Sep 10) - DEPLOY HARDENING: DONE in code (69fe01d, unpushed). **STILL OPEN: create the Render web service** - Build `pip install -r requirements-serve.txt && python ingest_corpus.py`, Start `uvicorn app:app --host 0.0.0.0 --port $PORT` (that command runs ON RENDER, not in his shell), env `CLAUDE_API_KEY` + `REVIT_COLLECTION=revit_docs_v2`, Free tier (512MB - watch for OOM against chromadb+onnx).
- Day 43 (Fri Sep 11) - FINISH THE DEPLOY FIRST (push, Render service, `precision_eval.py` against the deployed URL - it must reproduce 0.750/1.000), then STORY PACKAGING: the 4-minute Project 2 narrative and a 90-second Autodesk-current-work narrative. The paid ragas run rides along only if budgeted.
- Day 44 (Mon Sep 15) — SYSTEM DESIGN drill 1: "design RAG over a 2M-document corpus." Out loud, graded hard.
- Day 45 (Tue Sep 16) — SYSTEM DESIGN drill 2: agent/tool-use design + cost, latency, guardrails, evals in CI.
- Day 46 (Wed Sep 17) — ADVERSARIAL MOCK DEEP-DIVE: Claude interrogates the Project 2 story as a skeptical staff engineer.
Then: Phase 2 close -> REVISION WEEK -> Phase 3 (~early October).

STORY GUARDRAILS (do not let him overstate these in prep or in the loop)
- The corpus is 7 Autodesk help pages / 18 chunks; evals are n=4. Frame as "TOY CORPUS, REAL INSTRUMENT" — the finding is about METHOD, not scale. Inflating it and being caught discounts everything else he says.
- Two corpus pages (`about_doors.md`, `about_levels.md`) came back partly paraphrased by the fetch — fine as data, NOT quotable as Autodesk documentation.
- The headline story, and it is a genuinely senior one: "my RAG was answering from the wrong chunk with every guard green — threshold passing, refused=False, faithfulness high. I built a precision harness with labelled expected chunk IDs, found hit@10 = 1.000 vs hit@2 = 0.750, and proved the answering chunk sat UNDER my threshold at 1.082 — N_RESULTS was the gate, not THRESHOLD. The hit@k sweep was flat k=2..5 and jumped at k=6, so widening retrieval is a cliff, not a dial. That is an argument for reranking, measured rather than read."

PHASE 2 CLOSE PLAN (deferred by the INTERVIEW DETOUR above — resume after Day 46)
- Day 41 — Project 2 hardening II (deferred from Day 40): model cost decision (haiku vs sonnet, measured not guessed), ragas upgrade, ONE paid ragas_evals.py run with the numbers recorded. EXTERNAL DEPENDENCY: the paid run must be budgeted BEFORE the session — it was unmet on Day 40 and cost the day's original plan.
- Day 42 — PHASE 2 CLOSE: no new content. Capstone review of Days 22-41, weak-spots list becomes the REVISION WEEK syllabus, Phase 1 recap out loud (owed since 08-08).
Then: REVISION WEEK (Phase 1+2, no new content) -> Phase 3 opens ~late September.

REVISION WEEK PLAN (declared 2026-09-17; OPTION A chosen same day - CONCEPTS ONLY, 3 sessions, must finish THIS WEEK. Weekday slot only Fri left; weekend mornings belong to system design + YUNextGenAI, so Sat 6:00-7:30 is the one borrowed slot)
- Day 43 (Thu 9/17) - Phase 1 Weeks 0-1: training, overfitting, tokens, attention, generation. DONE.
- Day 44 (Fri 9/18) - [+ weak spot 7: IO vs CPU in Python, 10 min, inside the agents block] TWO concept blocks, out loud, no experiments: Phase 1 Weeks 2-4 (embeddings, prompting, RAG vs fine-tune vs prompt) + Phase 2 agents (tool use, LangGraph loop, checkpointers, Days 31-37). Keep the one-dive cap at ZERO - two blocks is already the density ceiling.
- Day 45 (Sat 9/19, 6:00-7:30) - Phase 2 RAG + evals (Days 38-42) + LABEL 3 NEW QUESTIONS COLD (weak spot 5, concept-level, ~10 min).
Then: PHASE 3 OPENS Mon 9/21 as Day 46. Nov milestone holds; guardrails module still follows Phase 3.

BACKLOG LANE (moved out of revision by Option A) - one item as a ~30-min tail on Phase 3 sessions, in this order:
1. Deploy block (~1 h, Phase 3 week 1): Render service; `precision_eval.py` against the deployed URL (must reproduce 0.750/1.000); haiku vs sonnet cost measured.
2. THE QUIET TWIN - same-width different embedder (MiniLM vs bge-small-en-v1.5), ~130MB download.
3. Trim-experiment + prefill re-attach re-test.
4. Batch `get_prices(tickers)` - 10 rounds collapse to 1.
5. Grow CASES to 15 + measured `N_RESULTS` decision.
6. `SimilarityPostprocessor(similarity_cutoff=0.301)` parity close.
7. Paid ragas run - ONLY after his yes/no + dollar cap.
PARKED FURTHER (reranking-adjacent, belongs with Phase 3 reranking): chunker hard bound, title-prepend, `category` metadata.

CELERY BUILD (added 2026-09-17 at Tushar's go - driven by a REAL AI-engineer interview gap; 2 sessions in PHASE 3 WEEK 2, before multi-agent)
Why: AI-engineer JDs cluster on LangGraph + multi-agent + Celery/async Python; he answered "I don't know" on Celery. Build it on HIS pipeline so the next answer is a project, not theory.
EXTERNAL DEPENDENCY: Redis running locally on his Mac (`brew install redis` or Docker) BEFORE session C1.
- C1 SHAPE + FIRST TASK: producer / broker / worker / result backend on one screen; FastAPI `POST /ingest` returns a `task_id` at once; `ingest_corpus.py` becomes a Celery task; `GET /ingest/{task_id}` reads state. Predict-then-run: state goes PENDING -> STARTED -> SUCCESS.
- C2 PRODUCTION BEHAVIOUR: `chord` = group(embed batches) -> callback flips the collection pointer (Day 41 blue/green, now async); `acks_late=True` + idempotent upsert, proved by killing a worker mid-task; `worker_prefetch_multiplier=1`; `rate_limit` + `retry_backoff` on 429; separate `ingest` queue; prefork vs gevent pool tied to weak spot 7 (IO vs CPU).
Interview line it must produce: "I moved my RAG ingestion onto Celery - here is why acks_late and prefetch=1, and why the pool is gevent for LLM calls."
Content-density rule applies: Celery internals at most one dive per session.

GUARDRAILS MODULE (added 2026-09-17 at Tushar's request - runs AFTER Phase 3, before Projects 3+4; ~4 sessions, one week)
Why after Phase 3: guardrails are only testable once there is an agent with tools to misuse. Already built in Project 2 (name these on day 1): distance-threshold refusal, `refused` as a declared field, 422 input validation.
- G1 INPUT: prompt injection (incl. injected text inside RETRIEVED chunks), PII redaction before the LLM call (Presidio), topic/scope filter. Exercise: plant an injection in a corpus chunk and prove Project 2 obeys it, then block it.
- G2 OUTPUT: structured output + Pydantic validation with retry, grounding/citation check (every claim maps to a source chunk), moderation classifier (Llama Guard class). Exercise: reject an answer that cites a chunk it was not given.
- G3 AGENT/TOOLS: tool allowlists, argument validation, max-steps and token/dollar budgets per run, human-in-the-loop approval via LangGraph interrupt for write actions. Exercise: agent tries a destructive tool call and pauses for approval.
- G4 OPERATE + COMPARE: guardrail hit-rates as metrics (LangSmith), red-team eval set in CI that fails the build, cost/latency added per guard. Framework survey in ONE session, not three: Guardrails AI vs NeMo Guardrails vs hand-rolled - decide which layer each belongs in.
Content-density rule applies: one framework's internals at most per session.

NVIDIA PREP LANE (declared 2026-09-23): an NVIDIA RECRUITER REACHED OUT - no date yet, role/JD not yet shared. UPDATE same day: CALL SCHEDULED MON 2026-09-28 (assumed recruiter screen - confirm). Plan: Thu 9/24 Day 48 + tail = 90-sec 'tell me about yourself'; Fri 9/25 Day 49 + tail = 60-sec Project 2 story + 'why NVIDIA'; weekend = one-page call cheat sheet (role/team/loop-format questions, availability, comp: ask their range first); Mon 9/28 = call, NO new content that day. After the call: dated detour for the technical loop. DECISION: Phase 3 keeps going (hand-built agent loop is interview-load-bearing); the ~30-min session TAIL switches from BACKLOG LANE to interview prep until a date exists. Order: (1) reply to recruiter + get JD; (2) 4-min Project 2 story + 90-sec Autodesk-current-work story, out loud; (3) system design drill "RAG over 2M documents"; (4) Walmart-scale story tied to AI serving (throughput, latency, cost); (5) JD-specific block once the JD is in (e.g. GPU inference serving if the role asks for it - do not guess before the JD). When a DATE lands: switch to a dated day-by-day detour like 09-08's. Backlog lane resumes after.

NEXT SESSION (Day 49 - SAME LOOP, THREE WAYS: while loop -> his graph -> prebuilt ToolNode) - file `exercises/day49_three_ways.py`
Why: Day 48 ran clean but "I didn't understand today's logic". Consolidate before adding anything new.
Shape FIRST (before goal): the Slack coworker + the 10-line `while True` loop from Day 48's close, on one screen.
Steps: (1) homework review - YNXT vs AAPL message count; (2) HE writes the plain `while` loop himself in `day49_three_ways.py` (same tool, same question) and gets the same 4 messages; (3) replace his `tools` + `should_continue` with `ToolNode([get_price])` + `tools_condition` from langgraph.prebuilt - same printout; say it: "the prebuilt pieces ARE my Day 48 pieces". CHECK `langgraph_prebuilt-1.1.0` source for tools_condition's return values BEFORE predicting (VERSION FIDELITY) - that is the session's one dive.
Coaching: shape -> GOAL printout + file -> numbered steps, ONE at a time, whole-function blocks; for __main__ edits say "delete from `if __name__` to end of file, then paste".
QUIZ PLAN (MAX 3, ONE PART EACH)
Q1. Fill the blank: "Claude never runs `get_price`. It only ______." (writes a tool_call request - name + args + id)
Q2. Fill the blank: "A router is a switch; an agent loop is a while because of the edge ______." (tools -> agent, back to Claude)
Q3. Fill the blank: "A `return` indented inside a `for` loop ______." (exits on the first item - later tool calls never run)
Morale opener: 6/6 predictions matched, and he asked the staff-level question "why do we need LangGraph at all?" - answered with checkpointing / human pause / streaming.
TAIL (~30 min, NVIDIA lane, call is Mon 9/28): 90-sec "tell me about yourself" out loud (carried from Day 48), then 60-sec Project 2 story if energy remains. Weekend: one-page call cheat sheet.
