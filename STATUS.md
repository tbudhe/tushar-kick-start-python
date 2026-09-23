STATUS.md — Tushar's AI Learning (SINGLE SOURCE OF TRUTH)

Last Updated: 2026-09-23 (Day 47 - PHASE 3: the backward edge. A LangGraph loop built by hand in `exercises/day47_loop.py`)

RULE FOR CLAUDE: "CURRENT STATUS" here overrides ALL other documents. If any doc conflicts, this file wins.

PROTOCOLS (condensed — full history in LEARNING_NOTES.md)
- DOC (2026-08-10): one session = one day number, sequential. Session end: update LEARNING_NOTES.md (one Day block, MAX 5 POINTS), STATUS.md, MEMORY.md, then commit.
- QUIZ (2026-08-28, HONORED 08-31 → 09-04): **MAX 3 QUESTIONS PER SESSION, ONE PART EACH.** A question with sub-parts counts as that many questions — don't write them. If an answer is incomplete, Claude COMPLETES IT in one line and moves on; a gap never becomes a follow-up question. Nudges count.
- COACHING (2026-08-18, verified working): before EVERY exercise — (1) GOAL first: show the exact final printout; (2) numbered step list; (3) ONE step at a time, confirm before the next.
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
Day: 47 COMPLETE (2026-09-23) | Week: PHASE 3, week 1 | Next session = Day 48.
Goal: Staff SWE -> AI Backend Engineer (Autodesk) -> Staff/Principal AI Engineer, Walmart, July 2027
Topic: Day 47 - THE BACKWARD EDGE. A loop in LangGraph is a conditional edge whose mapping points back at a node that already ran. Built `exercises/day47_loop.py` himself, goal-first, 6 steps: State{attempts} -> `work` node -> `should_continue` (the while-condition) -> `{"work": "work", END: END}` -> invoke -> break the stop condition.
BACKFILL (confirmed by Tushar 2026-09-23): Days 44-46 ran 9/18-9/22 in sessions NOT recorded in this file. Evidence on disk only: `exercises/day45_stategraph.py` (StateGraph, TypedDict state, keyword `classify` + `add_conditional_edges`, he added a `greet` node himself; committed a240b8e); `exercises/day46_llm_router.py` (Claude as classifier, max_tokens=5, `label if label in ROUTES else "docs"` safety net) and `exercises/day46_graph.py` (router wired into the graph, `docs` node calls `rag_service.answer_question`). Whether REVISION WEEK Days 44-45 (concept blocks, weak spots 5-7) actually ran is UNKNOWN - treat weak spots 5, 6, 7 as still open.
FINDINGS THIS SESSION: (1) THE BACKWARD EDGE IS THE WHOLE IDEA - router vs loop differ by one dict entry pointing back; the routing fn is the TS `while` condition. (2) KeyError: True - a routing function's return value is looked up as a KEY in the mapping dict; anything not a key crashes. Same failure his Day 46 `in ROUTES` safety net prevents. (3) RECURSION LIMIT IS 10,007 in his langgraph 1.2.9 - he ran the broken loop to ~10k attempts. Claude predicted 25 (old default) and was WRONG; his run caught it. (4) SET YOUR OWN BUDGET: `graph.invoke(..., config={"recursion_limit": 10})` -> exactly 10 attempts then GraphRecursionError, matched prediction. It is the framework version of his own Day 2x `for iteration in range(MAX_ITERATIONS)`. (5) HIS CATCH: noticed unprompted that `return END` is never reached under `if True:` - dead code.
Quiz results: 3/3 (Q1 self-corrected mid-answer "price" -> "docs"; Q2 mapping-dict lookup; Q3 keyword router picks docs for "hi, how much does Fusion cost?").
PREDICTION RECORD: 2 stated by Claude - recursion limit 25 (MISS, it is 10007), limit 10 -> 10 attempts + GraphRecursionError (MATCH).
COACHING NOTE: session opened with concept-before-goal; he pushed back ("Give me goal first approach with file names... I am new to AI"). Restarted goal-first and it ran clean. Goal-first is non-negotiable even for "just one concept" days.
Exercise: `exercises/day47_loop.py` - his code, 6/6 steps + homework DONE same day: `done: bool` added; `work` writes `done = new_count >= 3`; router reads only `state["done"]`. He first returned `{"done": True}` from the ROUTER idea (corrected: nodes return dicts, routers return strings), then set done=True on every pass -> 1 attempt, matching prediction (the "too early" bug). Framed as: stop at the RIGHT moment - too late = 10,007 paid passes, too early = unfinished job; only the node that saw Claude's response knows. Node analogy that landed: paginated fetch, `hasMore = page.has_more`. He asked "why do we need to stop retry?" - each pass is a STEP, not a retry.
OPEN: (a) paid ragas run - still needs yes/no + dollar cap (will not ask again); (b) Render service not created (BACKLOG LANE item 1); (c) `dgx_sim.py`, `image_split.py` committed in a240b8e as "need review after phase 3" - not curriculum.
Project 1: SHIPPED. Project 2: pushed; remaining: Render service, remote eval run, model cost decision, ragas upgrade, paid ragas run, grow CASES. Project 3 (LangGraph Autodesk agent): router graph exists (day46_graph.py) - Day 48's loop is its engine.
Currently strong on: predicting before running; catching dead code and test gaps unprompted.
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

NEXT SESSION (Day 48 - CLAUDE INSIDE THE LOOP: hand-built tool-calling agent in LangGraph) - file `exercises/day48_agent_loop.py`
Shape: State{messages} -> `agent` node calls Claude (`claude-opus-4-8`, `CLAUDE_API_KEY`) with one tool (`get_price` from day36) -> `should_continue` returns "tools" if the last response has a tool_use block, else END -> `tools` node runs the tool and appends the tool_result -> edge BACK to `agent`. recursion_limit set explicitly. This is what `create_agent` (Day 33) hid.
Coaching: GOAL printout first + file name, numbered steps, ONE at a time, whole-function replacement blocks only. Zero library dives planned.
QUIZ PLAN (MAX 3, ONE PART EACH)
Q1. Fill the blank: "A LangGraph graph loops instead of just branching when a conditional edge ______" (maps to a node that already ran - points back).
Q2. Fill the blank: "`KeyError: True` from a routing function means ______" (it returned a value that is not a key in the mapping dict).
Q3. Fill the blank: "In a loop that calls a paid API, I set `recursion_limit` myself because ______" (the default in 1.2.9 is 10,007 steps - thousands of paid calls before the framework stops it).
Morale opener: he predicted, ran, and caught Claude's wrong prediction (25 vs 10,007) with his own run - then spotted the dead `return END` unprompted.
BACKLOG LANE tail (only if energy remains, ~30 min): item 1, the Render service.

ONE-SENTENCE SUMMARY (say out loud)
"A LangGraph loop is just a conditional edge that points back - the routing function is my while-condition, and recursion_limit is my budget, not the framework's."

ACTIVE MENTAL MODELS (top of mind - full running list archived in LEARNING_NOTES.md)
- A loop is a conditional edge that points BACK - router and loop differ by one dict entry
- The routing function is the while-condition: nodes return dicts, routers return strings
- A router's return value is a dict KEY - anything else is KeyError (why `in ROUTES` exists)
- The framework's recursion limit (10,007 in langgraph 1.2.9) is a backstop, not a budget - set recursion_limit yourself
- Training changes the weights; inference freezes them - prompts, RAG and messages only change the input
- w is the model, loss is the report card - only w ships
- An accumulator's scope decides what it sums - declared outside the epoch loop, it sums history, not the current weight
- Batch GD updates once per pass, SGD once per example, LLMs per mini-batch - a mid-pass loss is a partial sum, not a measurement
- The minus sign is "downhill" - flip it and the same loop climbs without bound
- Tokens are billed by the LLM API, in and out - the vector DB is not where token cost lives
- Liveness is not identity - a health check that cannot name the data it serves certifies nothing
- A health check must read the SAME handle the request path uses, or it certifies a connection nobody serves from
- An in-process contract does not survive serialization for free - a flag must be in the response model
- Two error shapes mean two parsers - one envelope per failure class
- A wrapper class name is not a model identity - versions pin the vectors
- Refusal is a retrieval decision, made before any token is bought
- Blue/green is TWO steps: build the new collection AND flip the pointer — only the first one is in the ingest script
- A collection name is a pointer, not a constant — env var, so a corpus swap needs no code change
- The vector DB is derived data; the corpus is source — if the build step can't rebuild it from git, the deploy is a guess
- A test whose PASS state is indistinguishable from "the test never ran" is not an instrument — add a marker only a real run can produce
- Dev dependencies are not serving dependencies — ask `sys.modules` after a real request, not the requirements file
- Pin the embedder explicitly: an eval that cannot reproduce its own numbers is worthless
- The label set IS the test — label by SOURCE DOCUMENT and the eval agrees with whatever the retriever already does
- Answerhood test for a label: if a reader got ONLY this chunk, could they do the thing?
- hit@k measures what the STORE can reach; hit@N_RESULTS measures what PRODUCTION sees — the gap is the bug
- THRESHOLD is a quality gate, N_RESULTS is an admission gate — a chunk under threshold that never gets retrieved is invisible to both
- Widening retrieval is a cliff, not a dial — pay 3x context for nothing until one specific k, which is the argument for reranking
- A precision harness costs $0 and is deterministic; a judge metric costs money and is a trend — build the free one first
- n=4 means every question is worth 25 points — a smoke test, not a metric
- Vector search ranks ABOUTNESS, not ANSWERHOOD — cosine distance has no notion of "answers the question"
- A distance threshold measures COVERAGE; it cannot measure PRECISION — two failures, two instruments
- A grounded answer built from the WRONG chunk passes every guard I own: threshold PASS, refusal silent, faithfulness high
- A chunker that respects paragraph boundaries has no upper bound — max_chars is a preference, not a contract
- Toy corpora hide precision failures: one chunk per topic makes "closest" and "correct" the same row
- Real prose sits further away than a paraphrase of the question (0.57-0.84 vs 0.128) — normal, not broken
- LlamaIndex is a pipeline object, not a search engine — the search is still Chroma's
- Document → Node → Index → Retriever → QueryEngine; `from_documents` is the only stage I never wrote by hand
- LlamaIndex = EF Core / Prisma; Chroma = the database. The ORM never made the DB faster, it stopped me writing SqlCommand
- The vector STORE owns the embedding contract — a dimension mismatch is a schema violation, and the store is what raises it
- A collection is pinned to the width of its FIRST vector; changing embedder = rebuild, not config
- Width mismatch fails LOUDLY; same-width-different-model fails SILENTLY — only the second one reaches production
- Python has no hoisting: a top-level `def` closes the indented block above it and binds its name only when reached
- "Index" is overloaded: Chroma's index is a DATA STRUCTURE, LlamaIndex's VectorStoreIndex is an ORCHESTRATION OBJECT
- A framework's real cost is the defaults it substitutes for decisions I made on purpose
- Metadata added for bookkeeping silently becomes part of what I do semantic search over — `excluded_embed_metadata_keys` is the control
- Scores and distances are the same number in two costumes — a threshold constant does NOT port across frameworks
- `from_documents` = ingest job; `from_vector_store` = serving path — wiring the first into a request handler is running migrations on every request
- A build step writing to durable storage must be idempotent, or results depend on how many times I ran it
- delete-and-rebuild is fine with ONE reader and no uptime need; serving traffic means versioned collection + pointer flip (blue/green indexing)
- `refine` mode converts WIDTH into DEPTH — one LLM call per chunk, sequentially
- Width is already free; only depth costs latency (HIS sentence, 09-02)
- Async overlaps WAITING, never CAUSALITY — a dependent chain is serial in any runtime
- `gather` can only start calls that EXIST; the model can't emit an argument it hasn't been told
- Concurrency is a property of the REQUEST shape, not of my code
- The latency lever is FEWER ROUNDS (batch tools), not more async
- LangChain = model/tool layer; LangGraph = the runtime that owns the loop and the state
- Wall clock mixes model latency + tool time + network — stamp the thing you are actually measuring
- updates = what changed / values = what is / messages = what's being typed right now
- A filtered instrument reports the filter as much as the signal
- `create_agent()` is build-time, `.stream()`/`.invoke()` is request-time — never chain them
- `getattr(obj,"x")` asks for an ATTRIBUTE; `dict.get("x")` asks for a KEY — the swap fails silently
- checkpointer = session store + Redis; thread_id = the session cookie; the agent is still a stateless request handler
- InMemorySaver in 12 pods = 12 disconnected dicts; amnesia is a CORRECTNESS failure, not a latency one
- A tool's model obeys the DESCRIPTION while the function obeys the SIGNATURE
- `is_error` is data, not a crash — the model must SEE the failure to recover from it
- Config is re-applied every call; state is accumulated — system_prompt is config, messages are state
- A good instrument has exactly ONE explanation for its failure
- The library is in my .venv — when docs and behavior disagree, read the source (once per session, not twice)
- bind_tools = printing the menu (config-time); rounds = trips to the kitchen (runtime) — MENU SIZE NEVER ENTERS THE MATH
- Transcript order: AIMessage BEFORE its ToolMessages; every tool_use needs its tool_result
- A run is evidence, not an explanation — the check question wants a sentence

PROGRESS LOG (most recent first - headline only)
Day 43: REVISION WEEK OPENS (his call; interview detour paused). Phase 1 recap exposed decay - all five sentences came back as inference-time RAG answers; organizing sentence: training changes weights, inference only changes input. Wrote one-weight gradient descent himself before being asked: two SCOPE bugs (accumulators outside the epoch loop, update inside the point loop), math all right; half-fixed version still converged (SGD vs batch). 67.5 -> 0.0000, w 2.9991 exact; sign flip -> 59.9M. Quiz 2/3, streak ends at seven (miss: HTTP response model boundary). day36 sleep deleted
Day 42: DEPLOY HARDENING - `/heartbeat` had been certifying nothing; `/health` now reports serving IDENTITY (collection, 18 chunks, embedder, chromadb 1.5.9, threshold, n_results) off the same handle production queries. `refused` finally crosses the HTTP boundary, so clients branch on a flag instead of string-matching "I don't know". One `{code, message}` envelope for 422 BAD_REQUEST and 502 UPSTREAM_ERROR. The France question proved the cheapest response is the honest one - $0, Claude never called. 3/3 quiz, seventh running; 6 predictions, 5 matched, and the miss found the wrapper-alias embedder name. Committed 69fe01d, NOT pushed; Render service still not created
Day 41: DEPLOY, part 1 — production had been serving the 6-chunk TOY corpus the whole time; two sessions of corpus and precision work were never on the request path. Blue/green built the new collection and nobody flipped the pointer. Collection name is now an env var. Vector DB proven rebuildable from tracked source (build step = `ingest_corpus.py`), and the first "passing" rebuild was caught as a test that never ran. Serving deps measured by `sys.modules`, not guessed: 1.8GB dev venv, 7 packages actually imported. 3/3 quiz, sixth running; 4 predictions, 4 matches
Day 40: THE PRECISION HARNESS — `precision_eval.py`, labelled expected chunk IDs, depth 10, $0 per run. His own first label set (by source document) would have scored Day 39's bug as a PASS — the label set IS the test. hit@10 = 1.000 vs hit@2 = 0.750: retrieval isn't broken, ranking is. The answering chunk sits at 1.082, UNDER the 1.2 threshold — `N_RESULTS = 2` is what excludes it, not the gate. hit@k flat 0.750 through k=5, 1.000 at k=6: widening is a cliff, not a dial, and that is the measured case for reranking. 3/3 quiz, fifth running; Q2 was the exercise spec written cold
Day 39: real Autodesk corpus replaces the 6 toy one-liners (1,734 words -> 18 chunks, new collection, old one untouched); THRESHOLD=1.2 SURVIVED and length-dilution was falsified — but the wall question ranked an auditing footnote 1st and the answering chunk 7th, with every guard silent. Vector search ranks ABOUTNESS, not ANSWERHOOD; coverage and precision are different failures needing different instruments. 3/3 quiz, fourth running; two of Claude's hypotheses falsified in one session
Day 38b: LlamaIndex SHAPE taught in one screen and mapped onto his own file (EF Core anchor); Part B green — a 768-wide vector into a 384-wide collection raised `InvalidArgumentError` FROM CHROMA, proving the store owns the embedding contract; he traced it forward unprompted to `Settings.embed_model` defaulting to OpenAI at 1536, and named `SimilarityPostprocessor(similarity_cutoff=0.301)` as the parity fix; 3/3 cold quiz with nothing to complete, MENU-vs-TRIPS and LLAMAINDEX SHAPE both CLOSED; zero .venv dives — the CONTENT DENSITY cap worked
Day 38 (Part A): LlamaIndex vs hand-rolled over identical chunks — same top chunk, same order (`MATCH: True`); `score = exp(-distance)` read out of the library; metadata-in-the-embedding found, predicted, fixed, and confirmed to 3 decimals; his system prompt and threshold both silently replaced by framework defaults; 3/3 cold quiz; session ended early on burnout caused by two back-to-back .venv dives — CONTENT DENSITY protocol added
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
