STATUS.md — Tushar's AI Learning (SINGLE SOURCE OF TRUTH)

Last Updated: 2026-09-08 (Day 40)

RULE FOR CLAUDE: "CURRENT STATUS" here overrides ALL other documents. If any doc conflicts, this file wins.

PROTOCOLS (condensed — full history in LEARNING_NOTES.md)
- DOC (2026-08-10): one session = one day number, sequential. Session end: update LEARNING_NOTES.md (one Day block, MAX 5 POINTS), STATUS.md, MEMORY.md, then commit.
- QUIZ (2026-08-28, HONORED 08-31 → 09-04): **MAX 3 QUESTIONS PER SESSION, ONE PART EACH.** A question with sub-parts counts as that many questions — don't write them. If an answer is incomplete, Claude COMPLETES IT in one line and moves on; a gap never becomes a follow-up question. Nudges count.
- COACHING (2026-08-18, verified working): before EVERY exercise — (1) GOAL first: show the exact final printout; (2) numbered step list; (3) ONE step at a time, confirm before the next.
- WHY BEFORE INSTRUMENT (2026-09-01, HONORED 09-02 and 09-04): every non-obvious line of scaffolding gets ONE sentence of purpose BEFORE the code — what claim it tests, and what the two possible outcomes look like.
- CONTENT DENSITY (2026-09-02, **HONORED 09-04 — it worked**): at most **ONE library-internals dive per session**, and 09-04 used ZERO. Teach the framework's SHAPE before its footnotes. Day 38b opened with the five-stage pipeline on one screen and he immediately reasoned forward from it unprompted. Keep this cap.
- ANALOGY DOMAIN (2026-09-02, his explicit correction): **anchor analogies in Node.js/TypeScript or C#, NOT Java/Spring** — "I am not from Java." EF Core vs raw ADO.NET landed instantly on 09-04.
- SHOW HIS OWN CODE (2026-09-02, HONORED 09-04): when referencing his files, PASTE THE CODE inline with exact file:line — he cannot browse installed packages.
- CODE DELIVERY (2026-08-31, EXTENDED 09-04): paste COMPLETE blocks, name the file AND the exact position in it. 09-04 FAILURE: "add it after ask_llamaindex(), before if __name__" was not precise enough — line numbers had drifted, the block landed INSIDE the __main__ block, and it silently swallowed the whole COMPARISON tail into the function body. FIX: when giving an insertion point, read the file on disk FIRST and quote the two real anchor lines it goes between.
- EXAMPLE FIDELITY (2026-08-31): examples must use HIS tools with HIS semantics. His Anthropic key env var is `CLAUDE_API_KEY`, not `ANTHROPIC_API_KEY`; his QA model is `claude-opus-4-8`; his RAG entry point is `rag_service.answer_question()`.
- DEBUG PROTOCOL (2026-08-26/27, EXTENDED 08-31, APPLIED 09-01 → 09-04): when a result doesn't change after an edit, READ THE FILE ON DISK. When behavior and docs disagree, read the installed library source in .venv (subject to the CONTENT DENSITY cap). Probe config with BEHAVIOR, never formatting. A good instrument has exactly ONE explanation for its failure. An instrument that FILTERS its input reports the filter. DOC-EDIT NOTE (2026-09-04, Claude's near-miss): when patching this file by string index, anchor on a UNIQUE marker — "CURRENT STATUS" also appears inside the RULE FOR CLAUDE line, and slicing on the first match silently deleted the whole PROTOCOLS block. Restored with `git show HEAD:STATUS.md > STATUS.md` (plain `git checkout --` fails in the mounted shell: cannot unlink).
- MORALE (2026-08-24, EXTENDED 08-28): he undercounts his wins — open with one concrete previous win before the quiz. When frustration surfaces, FIRST check whether Claude caused it. A process complaint gets a protocol fix, not encouragement.
- EXERCISE OWNERSHIP (2026-08-24): Tushar writes the exercise code himself. (Honored 08-25 → 09-04.)
- REVISION WEEK (2026-08-17): when Phase 2 completes, one full week of Phase 1+2 revision before Phase 3. Weak-spots list is the syllabus.
- ENV NOTE (2026-08-27): the .venv python symlink does not resolve from Claude's mounted shell — Claude cannot run his code. Claude reads source and reasons; Tushar runs everything.
- EDITOR NOTE (2026-09-02): VS Code "organize imports" HOISTS every import above a `sys.path.insert(...)` bootstrap and breaks repo-root imports from `exercises/`. Fix applied: `# isort: skip_file`. Permanent fix still unconfirmed: `.vscode/launch.json` with `"env": {"PYTHONPATH": "${workspaceFolder}"}`.

MCP TIMING DECISION (2026-08-28, Tushar's call): KEEP THE SEQUENCE. MCP stays in Phase 3 (~Nov 2026); no spike day, no reorder. Reassess only at Phase 2 close.

MILESTONES (recalibrate at each phase end)
Sep 2026: Phase 2 complete (tool use, LangChain/LlamaIndex, Project 2 hardened) → REVISION WEEK → Nov 2026: Phase 3 complete (LangGraph, agents, MCP, LangSmith) → Dec 2026: Projects 3+4 shipped → Feb 2027: job search opens → Jul 2027: Walmart Staff/Principal AI Engineer.

CURRENT STATUS
Day: 40 COMPLETE (2026-09-08) | Week: 7 — Phase 2 | Next session = Day 41.
Goal: Staff SWE -> AI Backend Engineer (Autodesk) -> Staff/Principal AI Engineer, Walmart, July 2027
Topic: Day 40 — THE RETRIEVAL PRECISION HARNESS. `precision_eval.py` at repo root: labelled expected chunk IDs per question, queried at DEPTH=10, RANK recorded. No LLM, no API key, $0 per run.
PLAN CHANGE (Claude's recommendation, Tushar's go): this replaced the planned model-cost decision + paid ragas run, whose budget dependency was still unmet. That work moves to Day 41; PHASE 2 CLOSE moves to Day 42. Still inside September; revision week still opens late Sept.
Exercise: `precision_eval.py` — (1) chunk inventory, (2) CASES: question -> expected chunk ids, `[]` = nothing should answer it, (3) rank loop at depth 10, (4) hit@2 / hit@10 / MRR, (5) hit@k sweep.
FINDINGS THIS SESSION: (1) **THE HEADLINE — a precision test labelled by SOURCE DOCUMENT scores the Day 39 bug as a PASS.** The first label set listed every chunk from each file, including `about_walls_2` (the auditing footnote that ranked 1st on Day 39) and excluding `walls_overview_0` (the closest thing to a real answer). The label set IS the test: label by topic and the instrument agrees with whatever the retriever already does. (2) **hit@10 = 1.000, hit@2 = 0.750.** Retrieval is not broken — RANKING is. The answering chunk is in the store for every question; production's window never reaches it. (3) **THE THRESHOLD WAS NEVER THE CONSTRAINT.** `walls_overview_0` sits at 1.082, comfortably under `THRESHOLD = 1.2`. `N_RESULTS = 2` is what excludes it. Two sessions spent tuning the gate while the bug lived in the window. (4) **WIDENING IS A CLIFF, NOT A DIAL** — hit@k measured flat at 0.750 for k=2,3,4,5 and 1.000 at k=6. 3x the context tokens for zero gain until one specific k. That is the measured case for RERANKING (Phase 3), not for raising N_RESULTS. (5) HONEST CAVEAT, n=4: each question is worth 25 points. This is a smoke test, not a metric — do not read a hit@2 delta as progress until CASES is 15-20 questions.
MEASURED TABLE (depth 10, revit_docs_v2): wall -> `walls_overview_0` rank 6, 1.082 | door -> `place_a_door_0` rank 2, 0.756 | window -> `place_a_window_0` rank 1, 0.654 | plan view -> `about_plan_views_0` rank 1, 0.573 | DWG (none expected) top hit 1.537, correctly rejected.
Quiz results: **3/3 CLEAN — FIFTH CONSECUTIVE SESSION, nothing needing completion.** Q1 named precision, said none of his guards catch it, and cited `context_precision` at ragas_evals.py:21 as the only candidate — correctly noting it has never been pointed at `revit_docs_v2`. Q2 specified the ENTIRE day's exercise before it was taught: labelled expected chunk IDs, depth past `N_RESULTS`, record the RANK, `retrieve()` called directly with no Claude in the loop. Q3 cold Day 33/34 answered with his own B-vs-C experiment cited as the proof.
UNPROMPTED WINS: Q2 was the exercise spec, written cold.
COACHING NOTE (Claude's own miss): the re-label loop was asked twice and failed twice — the second paste was unchanged plus a copy slip (walls chunks in the door row). The correct move was to hand over the finished CASES block after ONE worked example, not to ask a third time. Labelling judgment gets taught once with a worked table, then delivered.
Project 1: SHIPPED. Project 2: RAGAS triad + typed RagResponse + REAL CORPUS + PRECISION HARNESS done; remaining: model cost decision, ragas upgrade, one paid ragas_evals.py run, grow CASES.
Currently strong on: converting an explanation into a controlled experiment (seven sessions running); specifying a test before being taught it.

WEAK SPOTS (revisit)
1. MENU-vs-TRIPS — **CLOSED 2026-09-04.** Answered cold and correctly for the second session running (Q3, refine at top_k=10, with the async caveat attached unprompted). Do not re-drill.
2. SENTENCES vs CODE — good eight sessions running. Keep light pressure, don't grind.
3. `getattr` vs `.get()` — 2026-08-31. Still not retested. Watch once more, don't drill.
4. LLAMAINDEX SHAPE (opened 2026-09-02) — **CLOSED 2026-09-04.** He can now state what the framework IS in one sentence ("it replaced my glue code, not my retrieval") and reasoned forward from the shape unprompted.
5. LABEL SETS / ANSWERHOOD (opened 2026-09-08) — labelled a precision test by SOURCE DOCUMENT, twice, including the known false-positive chunk. The rule to re-test: "if a reader got ONLY this chunk, could they do the thing?" Retest by asking him to label 3 new questions cold at the start of REVISION WEEK.
CLOSED 2026-08-28: DIRECTION INVERSIONS / SLOT SWAPS (open since Day 26).

CARRIED FORWARD
(0) **Day 39's biggest item — RETRIEVAL PRECISION EVAL — BUILT 2026-09-08** (`precision_eval.py`, $0 per run, no LLM). What it opened in turn: (a) GROW CASES to 15-20 questions — at n=4 each question is 25 points; (b) DECIDE `N_RESULTS`: 2 -> 6 makes hit@2 -> 1.000 on this corpus but triples context per request, and the sweep shows k=3,4,5 buy nothing — decide it as a cost/precision trade, measured; (c) RERANKING is the real fix and stays in Phase 3, now with his own hit@k cliff as the argument for it; (d) still open from Day 39: hard-bound the chunker (split inside an oversized paragraph), the title-prepend experiment in `ingest_corpus.py`, `category` metadata written but unused by the audit.
(1) Phase 1 recap out loud (owed since 08-08; folds into REVISION WEEK). (2) Trim-experiment + prefill re-attach re-test. (3) Delete `time.sleep(2)` from `get_price` in **day36** before reusing that file as a reference (day37 uses `await asyncio.sleep(2)` deliberately — leave it). (4) Optional 2-minute Day 37 extension: add a batch `get_prices(tickers: list[str])` tool and show the 10-company question collapsing from 10 rounds to 1. (5) **THE QUIET TWIN — named 09-04, NOT tested:** two embedding models with the SAME width (384) but different vector spaces (MiniLM vs `bge-small-en-v1.5`) produce NO error and silently wrong neighbours. Part B proved only the loud failure. Costs a ~130MB model download; worth 10 minutes inside REVISION WEEK. (6) Confirm `.vscode/launch.json` with `PYTHONPATH` was created. (7) Optional 5-minute parity close: add `SimilarityPostprocessor(similarity_cutoff=0.301)` to the query engine and show the refusal case coming back.

PHASE 2 CLOSE PLAN (updated 2026-09-08 — Day 40 closed, plan shifted one day)
- Day 41 — Project 2 hardening II (deferred from Day 40): model cost decision (haiku vs sonnet, measured not guessed), ragas upgrade, ONE paid ragas_evals.py run with the numbers recorded. EXTERNAL DEPENDENCY: the paid run must be budgeted BEFORE the session — it was unmet on Day 40 and cost the day's original plan.
- Day 42 — PHASE 2 CLOSE: no new content. Capstone review of Days 22-41, weak-spots list becomes the REVISION WEEK syllabus, Phase 1 recap out loud (owed since 08-08).
Then: REVISION WEEK (Phase 1+2, no new content) -> Phase 3 opens ~late September.

NEXT SESSION (Day 41) — QUIZ PLAN (MAX 3, ONE PART EACH)
Q1. Your hit@k sweep was flat from k=2 to k=5 and jumped at k=6. Why does that argue for reranking rather than for raising `N_RESULTS`?
Q2. Your first label set would have scored Day 39's broken retrieval as a pass. In one sentence, what makes a label set honest?
Q3. Cold, Day 30ish: deterministic evals are free and RAGAS costs money. Name one thing only the paid one can tell you.
Morale opener: FIVE consecutive 3/3 quizzes — and on Day 40 his Q2 answer WAS the exercise spec, written before it was taught: expected chunk IDs, depth past N_RESULTS, record the rank, no LLM in the loop.

ONE-SENTENCE SUMMARY (say out loud)
"My threshold guards whether the answer is good enough; `N_RESULTS` decides whether the answer is even in the room — and only one of them was ever measured."

ACTIVE MENTAL MODELS (top of mind — full running list archived in LEARNING_NOTES.md)
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

PROGRESS LOG (most recent first — headline only)
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
