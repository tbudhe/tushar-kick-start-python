STATUS.md — Tushar's AI Learning (SINGLE SOURCE OF TRUTH)

Last Updated: 2026-09-02

RULE FOR CLAUDE: "CURRENT STATUS" here overrides ALL other documents. If any doc conflicts, this file wins.

PROTOCOLS (condensed — full history in LEARNING_NOTES.md)
- DOC (2026-08-10): one session = one day number, sequential. Session end: update LEARNING_NOTES.md (one Day block, MAX 5 POINTS), STATUS.md, MEMORY.md, then commit.
- QUIZ (2026-08-28, HONORED 08-31 → 09-02): **MAX 3 QUESTIONS PER SESSION, ONE PART EACH.** A question with sub-parts counts as that many questions — don't write them. If an answer is incomplete, Claude COMPLETES IT in one line and moves on; a gap never becomes a follow-up question. Nudges count.
- COACHING (2026-08-18, verified working): before EVERY exercise — (1) GOAL first: show the exact final printout; (2) numbered step list; (3) ONE step at a time, confirm before the next.
- WHY BEFORE INSTRUMENT (2026-09-01, HONORED 09-02): every non-obvious line of scaffolding gets ONE sentence of purpose BEFORE the code — what claim it tests, and what the two possible outcomes look like. Worked all session on 09-02.
- **CONTENT DENSITY (NEW 2026-09-02 — THE FAILURE OF THIS SESSION):** quiz volume was fine (3 questions, no complaint); he burned out on CONTENT volume instead. Day 38 spent ~an hour inside library internals — `math.exp(-distance)`, `MetadataMode.EMBED`, four prompt templates — chasing a discrepancy Claude's own example created. He ended with "I am burning out, can't understand this LlamaIndex, I think I am lost." CAP: **at most ONE library-internals dive per session.** When a second one appears, name it, write it in the notes, and move on — do not open `.venv` twice in one day. Teach the framework's SHAPE before its footnotes.
- ANALOGY DOMAIN (NEW 2026-09-02, his explicit correction): **anchor analogies in Node.js/TypeScript or C#, NOT Java/Spring** — "I am not from Java." Spring Boot/Spring Data comparisons were rejected mid-session; Express+`pg` vs Prisma, and ADO.NET vs Entity Framework, landed immediately.
- SHOW HIS OWN CODE (NEW 2026-09-02): when referencing his files, PASTE THE CODE inline. "That's your ingest.py + retriever.py" is not enough — he can't easily read source inside installed libraries either, so quote the exact file:line and the lines themselves.
- CODE DELIVERY (2026-08-31): when he is mid-exercise, paste **COMPLETE blocks** with every variable's origin named — never fragments. Also state WHICH FILE the block goes in and WHERE in it (he asked twice on 09-02).
- EXAMPLE FIDELITY (2026-08-31): examples must use HIS tools with HIS semantics. Check the repo's actual signatures before inventing a trace. His Anthropic key env var is `CLAUDE_API_KEY`, not `ANTHROPIC_API_KEY`; his QA model is `claude-opus-4-8`.
- DEBUG PROTOCOL (2026-08-26/27, EXTENDED 08-31, APPLIED 09-01 and 09-02): when a result doesn't change after an edit, READ THE FILE ON DISK. When behavior and docs disagree, read the installed library source in .venv. Probe config with BEHAVIOR, never formatting. A good instrument has exactly ONE explanation for its failure. An instrument that FILTERS its input reports the filter.
- MORALE (2026-08-24, EXTENDED 08-28): he undercounts his wins — open with one concrete previous win before the quiz. When frustration surfaces, FIRST check whether Claude caused it. A process complaint gets a protocol fix, not encouragement. (09-02: Claude caused it — see CONTENT DENSITY.)
- EXERCISE OWNERSHIP (2026-08-24): Tushar writes the exercise code himself — outside AI agents don't. (Honored 08-25 → 09-02.)
- REVISION WEEK (2026-08-17): when Phase 2 completes, one full week of Phase 1+2 revision before Phase 3. Weak-spots list is the syllabus.
- ENV NOTE (2026-08-27): the .venv python symlink does not resolve from Claude's mounted shell — Claude cannot run his code. Claude reads source in .venv and reasons; Tushar runs everything.
- EDITOR NOTE (NEW 2026-09-02): VS Code "organize imports" HOISTS every import above a `sys.path.insert(...)` bootstrap and breaks repo-root imports from `exercises/`. Fix applied: `# isort: skip_file` at the top of the file. Permanent fix offered (not yet confirmed created): `.vscode/launch.json` with `"env": {"PYTHONPATH": "${workspaceFolder}"}`.

MCP TIMING DECISION (2026-08-28, Tushar's call): KEEP THE SEQUENCE. MCP stays in Phase 3 (~Nov 2026); no spike day, no reorder. Reassess only at Phase 2 close.

MILESTONES (recalibrate at each phase end)
Sep 2026: Phase 2 complete (tool use, LangChain/LlamaIndex, Project 2 hardened) → REVISION WEEK → Nov 2026: Phase 3 complete (LangGraph, agents, MCP, LangSmith) → Dec 2026: Projects 3+4 shipped → Feb 2027: job search opens → Jul 2027: Walmart Staff/Principal AI Engineer.

CURRENT STATUS
Day: 38 PART A COMPLETE (2026-09-02) | Week: 7 — Phase 2 | Next session = Day 38b (finish Part B + verdict, SHORT session).
Goal: Staff SWE → AI Backend Engineer (Autodesk) → Staff/Principal AI Engineer, Walmart, July 2027
Topic: Day 38 — LlamaIndex vs the hand-rolled pipeline. Same 6 chunks, same MiniLM embedder, two frameworks → **identical top chunk and identical ordering (`MATCH: True`)**. Verdict so far: the framework buys CODE, not better retrieval — and every default it substitutes replaces a decision he made on purpose.
Exercise: `exercises/day38_llamaindex.py` — Parts A + 5b green. Part B (dimension probe) written but NOT RUN. Verdict block not yet written.
FINDINGS THIS SESSION: (1) LlamaIndex returns `score = math.exp(-distance)` (`vector_stores/chroma/base.py:472`), not Chroma's distance — his `THRESHOLD=1.2` becomes `score > 0.301`; constants don't port across frameworks. (2) LlamaIndex embeds METADATA with the text by default (`indices/utils.py:192` → `MetadataMode.EMBED`); two bookkeeping fields inflated doc4's distance 0.128 → 0.365 (~185%) and NOT by a constant. `excluded_embed_metadata_keys` fixed it and `-ln(score)` then matched `chroma dist` to 3 decimals — diagnosis confirmed by prediction, not argument. (3) `chat_content_qa_template` silently replaced his `SYSTEM_PROMPT`, including the `refused=True` refusal contract; LlamaIndex also ships NO similarity threshold. (4) `refine_template` = one LLM call PER chunk, sequential — `top_k=10` is 10 serial round trips; Day 37's "width is free, depth costs" showing up inside someone else's framework.
SESSION ENDED EARLY: he stopped at Part B with "I am burning out. Can't understand this LlamaIndex. I think I am lost." Cause diagnosed as Claude's: two consecutive library-internals dives, both chasing a discrepancy Claude's own example (`chroma_id` in metadata) introduced. The framework's SHAPE never got taught — only its footnotes. See CONTENT DENSITY protocol. Next session opens by re-teaching the shape in one screen, then finishing Part B.
Quiz results: **3/3 CLEAN, best start yet.** Q1 async C-vs-B — correct, and he named the mechanism ("in flight at the same time"). Q2 10-company latency — BETTER than the expected answer: batch the tool AND collapse the chain, "width is already free; only depth costs latency." Q3 cold Day 35 `InMemorySaver` × 12 pods — "Correctness: thread state is per-pod, so history vanishes." Instant, correct.
UNPROMPTED WINS: he added a `-ln(0)` guard to Claude's comparison code before it could raise; he challenged the delete-and-rebuild step and independently proposed versioned collections (= blue/green indexing); he asked "why do we need LlamaIndex if Chroma already has an index?" — the single best question of the day, and the one Claude should have opened with.
Project 1: SHIPPED. Project 2: RAGAS triad + typed RagResponse done; remaining: real Autodesk chunks, model cost decision, ragas upgrade, one paid ragas_evals.py run.
Currently strong on: converting an explanation into a controlled experiment (four sessions running); reading a claim's confirmation out of numbers rather than prose; stopping the session to ask "why are we doing this?" — it improved the teaching three times on 09-02.

WEAK SPOTS (revisit)
1. MENU-vs-TRIPS — REOPENED 2026-09-01, **effectively re-closed 2026-09-02** by Q2 ("width is already free; only depth costs latency"). Re-ask COLD once more in 2-3 sessions with a 3-tool / 2-dependent-step case before closing formally.
2. SENTENCES vs CODE — good seven sessions running. Keep light pressure, don't grind.
3. `getattr` vs `.get()` — 2026-08-31. Still not retested. Watch once more, don't drill.
4. **LLAMAINDEX SHAPE (NEW 2026-09-02)** — he can prove things about LlamaIndex's internals but cannot yet say in one sentence what the framework IS. Teach Document → Node → Index → Retriever → QueryEngine as one picture, in one screen, before touching any more internals.
CLOSED 2026-08-28: DIRECTION INVERSIONS / SLOT SWAPS (open since Day 26).

CARRIED FORWARD
(1) Phase 1 recap out loud (owed since 08-08; folds into REVISION WEEK). (2) Trim-experiment + prefill re-attach re-test. (3) Delete `time.sleep(2)` from `get_price` in **day36** before reusing that file as a reference (day37 uses `await asyncio.sleep(2)` deliberately — leave it). (4) Optional 2-minute Day 37 extension: add a batch `get_prices(tickers: list[str])` tool and show the 10-company question collapsing from 10 rounds to 1 — "fewer rounds" is still asserted, not measured. (5) **NEW — the scary twin of Part B:** two embedding models with the SAME width (384) but different vector spaces (MiniLM vs `bge-small-en-v1.5`) produce NO error and silently wrong neighbours. Part B only proves the loud failure; this is the quiet one. (6) **NEW —** confirm `.vscode/launch.json` with `PYTHONPATH` was created.

PHASE 2 CLOSE PLAN (updated 2026-09-02 — Day 38 split in two)
- Day 38b — SHORT session. Re-teach the LlamaIndex shape in one screen (Document → Node → Index → Retriever → QueryEngine), run Part B, write the 5-line "when I'd pick which" verdict into the file. Nothing else. No .venv.
- Day 39 — Project 2 hardening I: real Autodesk chunks through ingest.py; re-run retrieval audit; note what broke vs the toy corpus. EXTERNAL DEPENDENCY: needs a real Autodesk corpus staged before the session starts.
- Day 40 — Project 2 hardening II: model cost decision (haiku vs sonnet, measured not guessed), ragas upgrade, ONE paid ragas_evals.py run with the numbers recorded. EXTERNAL DEPENDENCY: needs the paid run budgeted.
- Day 41 — PHASE 2 CLOSE: no new content. Capstone review of Days 22-40, weak-spots list becomes the REVISION WEEK syllabus, Phase 1 recap out loud (owed since 08-08).
Then: REVISION WEEK (Phase 1+2, no new content) → Phase 3 opens ~late September.

NEXT SESSION (Day 38b) — QUIZ PLAN (MAX 3, ONE PART EACH)
Q1. LlamaIndex found the same top chunk as your own code. So what did the framework actually change? (one sentence)
Q2. You add `source_file` and `page_number` to every chunk's metadata for citations. What happens to your retrieval, and why?
Q3. Cold, Day 37: your agent answers a 10-company question and you set `similarity_top_k=10` with refine mode. What just happened to your latency?
Morale opener: 3/3 cold quiz — his best start — and his Q2 answer beat the model answer. Plus three unprompted wins in one session: the `-ln(0)` guard, proposing blue/green indexing before being taught it, and asking "why do we need LlamaIndex at all?"

ONE-SENTENCE SUMMARY (say out loud)
"LlamaIndex didn't give me anything new — it gave me my own pipeline with ITS defaults instead of mine, and every default it swapped in (my threshold, my system prompt, my embedded text) was one I had chosen on purpose."

ACTIVE MENTAL MODELS (top of mind — full running list archived in LEARNING_NOTES.md)
- Chroma is Postgres+pgvector (the HNSW index); LlamaIndex is Prisma (the pipeline around it) — never NEEDED, reached for when boilerplate outgrows the query
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
- The library is in my .venv — when docs and behavior disagree, read the source
- bind_tools = printing the menu (config-time); rounds = trips to the kitchen (runtime) — MENU SIZE NEVER ENTERS THE MATH
- Transcript order: AIMessage BEFORE its ToolMessages; every tool_use needs its tool_result
- A run is evidence, not an explanation — the check question wants a sentence

PROGRESS LOG (most recent first — headline only)
Day 38 (Part A): LlamaIndex vs hand-rolled over identical chunks — same top chunk, same order (`MATCH: True`); `score = exp(-distance)` read out of the library; metadata-in-the-embedding found, predicted, fixed, and confirmed to 3 decimals; his system prompt and threshold both silently replaced by framework defaults; 3/3 cold quiz, best start yet; session ended early on burnout caused by two back-to-back .venv dives — CONTENT DENSITY protocol added
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
