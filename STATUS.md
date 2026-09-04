STATUS.md — Tushar's AI Learning (SINGLE SOURCE OF TRUTH)

Last Updated: 2026-09-04 (Day 39)

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
Day: 39 COMPLETE (2026-09-04) | Week: 7 — Phase 2 | Next session = Day 40.
Goal: Staff SWE → AI Backend Engineer (Autodesk) → Staff/Principal AI Engineer, Walmart, July 2027
Topic: Day 39 — Project 2 hardening I. The 6 toy one-liners replaced with 7 REAL Autodesk Revit help pages (1,734 words -> 18 chunks) in a new collection `revit_docs_v2`; `revit_docs_project_2` left untouched so every comparison is data, not memory.
Exercise: `ingest_corpus.py` and `audit_corpus.py`, both at REPO ROOT (so `from retriever import client` works with no `sys.path` bootstrap — the structural fix for Day 38's VS Code import breakage). Corpus in `corpus/revit_help/` + `manifest.json`.
FINDINGS THIS SESSION: (1) **THE HEADLINE — a PRECISION failure with every guard silent.** "How do I create a wall in Revit?" ranked a footnote about AUDITING PROJECT FILES first (0.619) and a DOORS chunk second (0.827); the chunk that answers the question ranked 7th (1.106). Distance gate PASSES, `refused=True` never fires, RAGAS faithfulness would score HIGH — the answer is faithfully grounded in the WRONG chunk. (2) CLAUDE'S HYPOTHESIS FALSIFIED #1: `THRESHOLD = 1.2` SURVIVED the corpus swap — real hits 0.573-0.838, out-of-corpus miss 1.485-1.623. Constant left alone, on the numbers. (3) CLAUDE'S HYPOTHESIS FALSIFIED #2: length dilution is NOT the cause of the bad ranking — rank vs chars was 233, 358, 560, 567, **2623**, 446, 533, 524. What separates rank 1 from rank 7 is vocabulary ("creating walls" vs "walls are instances of predefined system family types"). (4) A chunker that respects paragraph boundaries has NO upper bound: `MAX_CHARS = 600` produced a 2,623-char chunk. (5) `count() == total_chunks` proved the `f"{stem}_{i}"` ID scheme makes the ingest idempotent.
Quiz results: **3/3 CLEAN — FOURTH CONSECUTIVE SESSION, nothing needing completion.** Q1 named Chroma as the component that raised the error AND drew the conclusion (orchestration glue, not the owner of the contract). Q2 was the QUIET failure case answered cold before it had ever been taught: "the store accepts every write, and retrieval silently rots — still computed, still ranked, no longer meaning anything." Q3 cold Day 35 added the sticky-sessions caveat unprompted.
UNPROMPTED WINS: the sticky-sessions caveat on Q3; and reading the "516 words -> 2 chunks" line as wrong before being told.
DEPENDENCY NOTE: Day 39's external dependency was UNMET at session start — no real corpus existed. Claude fetched one (7 pages) rather than swapping the day. Two pages (`about_doors.md`, `about_levels.md`) came back partly paraphrased by the fetch: fine as corpus, NOT citable.
Project 1: SHIPPED. Project 2: RAGAS triad + typed RagResponse + REAL CORPUS done; remaining: precision eval, model cost decision, ragas upgrade, one paid ragas_evals.py run.
Currently strong on: converting an explanation into a controlled experiment (six sessions running); reading a printed table and spotting the row that contradicts the story.

WEAK SPOTS (revisit)
1. MENU-vs-TRIPS — **CLOSED 2026-09-04.** Answered cold and correctly for the second session running (Q3, refine at top_k=10, with the async caveat attached unprompted). Do not re-drill.
2. SENTENCES vs CODE — good eight sessions running. Keep light pressure, don't grind.
3. `getattr` vs `.get()` — 2026-08-31. Still not retested. Watch once more, don't drill.
4. LLAMAINDEX SHAPE (opened 2026-09-02) — **CLOSED 2026-09-04.** He can now state what the framework IS in one sentence ("it replaced my glue code, not my retrieval") and reasoned forward from the shape unprompted.
CLOSED 2026-08-28: DIRECTION INVERSIONS / SLOT SWAPS (open since Day 26).

CARRIED FORWARD
(0) **NEW, Day 39, the biggest one — RETRIEVAL PRECISION EVAL:** a test with EXPECTED CHUNK IDS per question. He has a coverage instrument (Day 20 threshold + refusal) and has NEVER had a precision one. Related: hard-bound the chunker (split inside an oversized paragraph); the title-prepend experiment left as his call in `ingest_corpus.py`; `category` metadata is written but unused by the audit; reranking is the real precision fix (Phase 3).
(1) Phase 1 recap out loud (owed since 08-08; folds into REVISION WEEK). (2) Trim-experiment + prefill re-attach re-test. (3) Delete `time.sleep(2)` from `get_price` in **day36** before reusing that file as a reference (day37 uses `await asyncio.sleep(2)` deliberately — leave it). (4) Optional 2-minute Day 37 extension: add a batch `get_prices(tickers: list[str])` tool and show the 10-company question collapsing from 10 rounds to 1. (5) **THE QUIET TWIN — named 09-04, NOT tested:** two embedding models with the SAME width (384) but different vector spaces (MiniLM vs `bge-small-en-v1.5`) produce NO error and silently wrong neighbours. Part B proved only the loud failure. Costs a ~130MB model download; worth 10 minutes inside REVISION WEEK. (6) Confirm `.vscode/launch.json` with `PYTHONPATH` was created. (7) Optional 5-minute parity close: add `SimilarityPostprocessor(similarity_cutoff=0.301)` to the query engine and show the refusal case coming back.

PHASE 2 CLOSE PLAN (updated 2026-09-04 — Day 39 closed)
- Day 40 — Project 2 hardening II: model cost decision (haiku vs sonnet, measured not guessed), ragas upgrade, ONE paid ragas_evals.py run with the numbers recorded. EXTERNAL DEPENDENCY: needs the paid run budgeted.
- Day 41 — PHASE 2 CLOSE: no new content. Capstone review of Days 22-40, weak-spots list becomes the REVISION WEEK syllabus, Phase 1 recap out loud (owed since 08-08).
Then: REVISION WEEK (Phase 1+2, no new content) → Phase 3 opens ~late September.

NEXT SESSION (Day 40) — QUIZ PLAN (MAX 3, ONE PART EACH)
Q1. Your threshold passed a chunk that didn't answer the question. Which failure is that — coverage or precision — and which of your guards would have caught it?
Q2. What would a retrieval precision test need that your current evals don't have?
Q3. Cold, Day 33/34: `create_agent()` is build-time and `.stream()` is request-time. Name one thing that belongs in each.
Morale opener: FOUR consecutive 3/3 quizzes with nothing to complete, and on Day 39 he falsified two of Claude's hypotheses in one session with instruments he ran himself.

ONE-SENTENCE SUMMARY (say out loud)
"My retrieval ranks what a chunk is ABOUT, not whether it ANSWERS the question — and a distance threshold can never tell the difference."

ACTIVE MENTAL MODELS (top of mind — full running list archived in LEARNING_NOTES.md)
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
