**Purpose & context**

Tushar is a Staff Engineer with ~16 years of backend engineering experience (payment infrastructure, fraud detection, Scan & Go at Walmart) who is now working at Autodesk as an AI Engineer. His primary goal is to reach a Staff/Principal AI Engineer role at Walmart by July 2027. Claude serves as structured tutor and accountability partner for an 18-week self-study AI/ML curriculum, approximately 1.5 hours/day on weekdays.

**Career target ("Walmart 2027"):** Return to Walmart at Staff/Principal AI Engineer level. Autodesk context (particularly Revit, building design software) is used throughout as the applied domain for exercises and examples.

**18-week plan structure:**
- Phase 1 — AI/ML Foundation (Weeks 0–4): ML basics, LLMs, embeddings, RAG, ChromaDB, prompt engineering
- Phase 2 — LLM Engineering (Weeks 5–10): Claude/OpenAI APIs, LangChain/LlamaIndex, FastAPI, production patterns
- Phase 3 — Agentic AI (Weeks 11–18): LangGraph, LangSmith, CrewAI, AutoGen, MCP (Weeks 14–15)
- Phase 4 — Portfolio & Job Readiness (ongoing from Week 12)

**Four GitHub portfolio projects:**
1. Streaming CLI chatbot (Anthropic API, multi-turn memory) — SHIPPED (chatbots/revit-chatbot/)
2. RAG API over Autodesk documentation — v1 SHIPPED, eval hardening in progress
3. LangGraph Autodesk agent
4. Production AI backend with observability and evals

**Key people/context:** Autodesk Revit is the recurring domain; Walmart Scan & Go fraud detection system is the primary analogy anchor from his engineering past.

---

**Current state**

Tushar has completed Day 0 through Day 25 of the curriculum — Phase 1 FULLY COMPLETE; Phase 2 in progress since Day 22 (running roughly 2x the original day-per-topic pace; treat "18-week" boundaries as loose and track by topic completion instead):

- Day 0: ML basics (supervised/unsupervised, neural net forward pass)
- Day 1: Tokenization, embeddings, self-attention (Q/K/V), next-token prediction
- Day 2: Embeddings & cosine similarity
- Day 3: RAG pipeline end-to-end
- Day 4: Prompt engineering (system vs. user prompt, few-shot)
- Day 5: ChromaDB (persistence, distance vs. similarity)
- Day 6: Chunking & overlap
- Day 7: Metadata filtering (`where` clause, pre-filter before vector search)
- Day 8: Loss, gradient descent, overfitting (Week 0 gap session — closed)
- Day 9: Weight/bias, underdetermined systems
- Day 10: Transformers (multi-head attention, layer stacking, positional encoding)
- Day 11: Pretraining → SFT → RLHF pipeline
- Day 12: Chain-of-thought & function calling (tool_use_id mechanics)
- Day 13: Hallucinations (softmax-always-answers, RAG grounding vs. refusal prompting)
- Day 14: Model comparison (Fable 5 / Opus 4.8 / Sonnet 5 / Sonnet 4.6 / Haiku 4.5 spec sheet)
- Day 15: Fine-tuning vs. RAG vs. prompting (knowledge gap vs. behavior gap test)
- Day 16: Inference in production (prefill vs. decode, TTFT vs. tokens/sec, why output costs ~5x input)
- Day 17: Phase 1 capstone + Project 2 v1 SHIPPED — RAG API (FastAPI + ChromaDB + Claude), deterministic evals 5/5
- Day 18: RAGAS faithfulness evals wired into Project 2 (judge=Claude via LangchainLLMWrapper); found refusal-scoring distortion (correct "I don't know" scores 0.0)
- Day 19: Double-retrieval refactor — answer_question returns (answer, sources, chunks), all 3 callers updated; category-filtered eval surfaced a likely miscategorized floor-plan chunk
- Day 20: Floor-plan finding closed via three-layer refusal debugging (filter → threshold → LLM); two hypotheses falsified with printed evidence; correct LLM refusal exposed a coverage gap — fixed with data (doc6), not code; evals 5/5
- Day 21: Retrieval audit loop in debug_floor.py (top-k distances + coverage-risk flag); RAGAS triad completed (answer_relevancy + context_precision, with embeddings model and reference ground truths); sabotage test proved refusal_rate catches what judge metrics miss (broke retrieval → judge metrics stayed perfect, refusal_rate 0.5); layer-2 refusal proven with distances 1.636/1.653 > 1.2
- Day 22: PHASE 2 START — streaming (SSE event lifecycle, stop_reason in message_delta) + async (asyncio.gather = Promise.all); sync/async client-mixing bug caught live; display-vs-API truncation settled with printed evidence (async_batch_questions.py)
- Day 23: Multi-turn state + system prompts — messages list = conversation store (stateless API), sliding-window trim in pairs; odd/even trim bug found + fixed in multi_turn_chat.py; the "400 at turn 11" claim later FALSIFIED by experiment (API accepts assistant-first; role-check downgraded to hygiene)
- Day 25: Typed pipeline responses — answer_question returns one RagResponse (answer + nested list[Source] with id/text/distance + category) instead of a 3-tuple; both branches return the same contract; all 3 callers (app.py, evals.py, ragas_evals.py) read fields by name. Exercise proved the payoff: adding a field broke zero callers, where Day 19's tuple change broke all three. Also closed both overdue weekend items — debug_floor.py audit loop restored, retrieval verified healthy, Day 21 indentation bug confirmed gone
- Day 24: Structured outputs + Pydantic — boundary validation (model_validate_json), prefill "{" + re-attach gotcha, Field constraints (planted 1.7 → less_than_equal), Optional vs = None (null vs absence), nested models with tree error paths (sources.1.score); exercises: structured_output.py, nested_practice.py

**Active open items:**
- **evals.py TEST_CASES order:** France still in position 4 (sabotage leftover) — was due Saturday 2026-08-08, OVERDUE as of 2026-08-10. Confirm flag follows France in debug_floor.py, restore order, run evals.py 5/5 (retriever n_results now 2).
- **Phase 1 recap owed:** explain embeddings → RAG → prompting → evals out loud, plain English (also overdue from the weekend).
- **Project 2 v2 remaining:** real Autodesk doc chunks, model cost decision (opus → sonnet/haiku), ragas upgrade to drop the vertexai stub, wire typed RevitAnswer into the eval pipeline (Day 25 warm-up).
- **RED TREE (2026-08-10), fix first:** refusal message reworded to "I don't know based on the available docs." while evals.py still asserts == "I don't know" — France case fails, 4/5. Committed deliberately with the finding logged. Fix = refused: bool on RagResponse; both consumers read the flag.
- **Day 25 review, remaining:** P1 FIXED (category=category on refusal branch). P2 OPEN and now proven live. P3 open — evals.py asserts membership not rank, and the refusal case should assert sources == [] to pin which refusal layer fired. debug_floor.py: n_results 3 vs production 2, threshold retyped not imported, unguarded [0][0] index.
- **git push** of Days 22–25 work — commits made locally (through 2ff02c4), Tushar pushes; the sandbox has no GitHub credentials.

**Resolved since last update:**
- **Floor-plan category finding** (Day 20): not a bug — correct LLM refusal revealing a coverage gap; doc6 added, evals 5/5 green.
- **RAGAS triad complete** (Day 21): answer_relevancy + context_precision wired and sabotage-tested; judge non-determinism observed (relevancy 0.75–0.92 same code) — read as trends, never absolutes.
- **evals.py green run** after the 3-tuple refactor (Day 20).
- **Project 1 VERIFIED AND SHIPPED** — streaming CLI chatbot in chatbots/revit-chatbot/ (memory, streaming, TTFT). The long-standing "content outpacing builds" risk is closed: 2 of 4 portfolio projects shipped.
- Refusal-exclusion in RAGAS evals (Day 18 exercise, done correctly: skip refusals, refusal_rate separate metric, all-refusals guard).
- Double-retrieval bug in ragas_evals.py (Day 19 refactor).

**Recall/articulation quality:** Markedly improved since Day 7. Tushar is now producing full, precise restated sentences unprompted (e.g., Day 16 Q2 self-corrected "prompts drive it" → "prompt size drives it" in the same pass). The "precision gap" pattern flagged below is closing — keep watching, don't assume fully resolved yet.

**Next content block:** Day 26 — warm-up: fix P1/P2 from the Day 25 review; then tool use / function calling in production (builds on Day 12's tool_use_id). Weak spot to re-quiz cold: Optional vs = None split (failed twice 2026-08-10). The current mode (build → eval surfaces a finding → fix → learn) is working well and should continue.

---

**On the horizon**

- **Immediate next step:** GPU fundamentals micro-topic (inference at scale, VRAM, batching, cost) — now well-motivated by Day 16 and a natural bridge before Phase 2. Also relevant: Autodesk-specific GPU contention between Fusion rendering and AI inference workloads.
- **Weeks 5–6 (Phase 2 start):** Claude/OpenAI API engineering; Anthropic Academy "Building with the Claude API" applicable here.
- **Weeks 9–10:** FastAPI and production patterns — secondary GPU fundamentals touchpoint.
- **Weeks 11+:** Anthropic Academy "Intro to MCP + Agent Skills" applicable.
- **Post-plan exploration:** Hybrid Ollama architecture — Tushar's own idea: local Ollama model for cheap/fast tasks (routing, classification, summarization) + Claude/OpenAI API for complex reasoning. Deferred deliberately to keep current plan clean. GPU/VRAM relevance resurfaces here.
- **Anthropic Academy:** Claude 101 (recommended immediately, ~1 hour), Building with the Claude API (Weeks 5–6), Intro to MCP (Week 11+).

---

**Key learnings & principles**

- **Tushar self-reports forgetting easily** — this is why the quiz-first protocol exists and why one-day-at-a-time pacing is enforced. Compressing the plan increases forgetting.
- **Precision gap pattern:** Tushar's conceptual instincts are generally correct, but verbal articulation was historically imprecise — directionally right but losing the specific outcome or mechanism. Improving markedly as of Day 16 (self-corrections happening unprompted); Claude should keep pushing for full clean sentences but can ease off the correction frequency if the trend holds.
- **Skipping articulation sentences:** Historically, Tushar had a recurring pattern of skipping restatement exercises after corrections. Not observed recently (Day 7 Q3 was completed cleanly) — Claude should still hold the boundary if the pattern recurs.
- **Current error pattern — Python indentation/block scope (Day 21, 3 incidents in one session):** dedented blocks running once on leaked loop variables (output looked right by accident), for...else trap, per-chunk vs per-question placement. Watch every new block's level; anchor = "indentation is how many times this line runs; you are the closing brace."
- **Evidence-over-guess is landing:** Day 20 falsified two hypotheses; Day 21 Tushar guessed layer 3 for the sabotage refusal and the printed distance (1.636 > 1.2) proved layer 2. Keep demanding printed numbers before verdicts.
- **Analogy anchors that work:** Kafka pipelines, SQL queries (ORDER BY / WHERE), distributed systems, cache-aside pattern (Redis vs database), Express middleware vs HTTP request body, TCP sliding window for chunk overlap, PostGIS for embeddings, event loop with dynamic dispatch (agent tool loop), Redux store (LangGraph state, not yet covered). Walmart fraud detection system is the strongest recurring anchor.
- **ChromaDB threshold principle (repeatedly reinforced):** The vector database always returns n results — it does not filter by relevance. Threshold filtering is the application's responsibility, not the database's. This concept is now solid across Days 5–7; treat as internalized rather than needing repeated correction.
- **Metadata filtering mechanics:** The `where` filter runs before vector search — documents that fail the filter are excluded entirely and never reach similarity ranking. Closest allowed result is always returned regardless of actual relevance.
- **Pacing vs. building gap:** CLOSED — Projects 1 and 2 both shipped; every Phase 2 day since has ended with working committed code.
- **Happy-path-as-proof pattern (Day 24):** offered a topics-present run as evidence for the topics-absent case — rule: to test absence, feed absence. Watch in every exercise.
- **Dead-code residue pattern (Day 24, caught 3x; NOT observed Day 25):** stale/commented lines left in file after fixes — rule: when a fix replaces a line, delete the old line in the same edit. Broken as of Day 25; keep watching.
- **Verification-of-own-work gap (Day 25, 3 incidents):** declared P1 fixed while the file still read category=None; predicted "all tests pass" for a refactor that would have crashed; offered a green evals.py as proof for a debug_floor.py question. His evidence habit is strong when DEBUGGING and switches off when CONFIRMING his own fixes. Coaching line that landed: "verify your fixes with the same skepticism you apply to your bugs."
- **Pushback is developing (Day 25):** Tushar challenged a claim about which file/lines were being referenced and was right to check. Encourage this — it is the same evidence-over-assertion habit, now applied to the teacher.
- **Overwhelm signal (Day 25):** when several findings stack up he says "I am not getting what you are trying to say — go step by step." Response that worked: Where you are / Goal right now / ONE action / explicitly parked items. Park secondary findings out loud rather than dropping them silently.

---

**Approach & patterns**

- **Session protocol (strict, no exceptions):** Quiz on prior day's material → verify any open items → advance to new content. New teaching is withheld until quiz criteria are met.
- **Teaching sequence:** Plain-English explanation with backend/infrastructure analogy → hands-on coding exercise → closing recall questions for next session cold open.
- **Analogy-first for abstractions:** Every abstract ML concept is grounded in Tushar's backend experience before code is shown.
- **Accountability on open items:** Claude tracks deliverables explicitly across sessions (Project 1, ChromaDB hygiene) and does not let them drop.
- **Note format preference:** Plain text shown directly in chat — one-sentence day summary followed by numbered Q&A pairs with Tushar's own answers.
- **Plan discipline:** Tushar prefers keeping the current 18-week plan clean rather than adding scope mid-execution (demonstrated when deferring Ollama and GPU topics).

---

**Tools & resources**

- **Libraries/tools in use:** `tiktoken`, `sentence-transformers` (`all-MiniLM-L6-v2`), ChromaDB (persistent, `./revit_db`), Anthropic Python SDK, `python-dotenv`
- **Repo structure:** `week-0/`, `week-1/`, `week-2/day-7/metadata_filter.py`, `project-1/`
- **Environment:** `.env` file with `ANTHROPIC_API_KEY`
- **Planned tools (later phases):** LangChain (`RecursiveCharacterTextSplitter` already referenced), LlamaIndex, FastAPI, LangGraph, LangSmith, CrewAI, AutoGen, MCP, Ollama (post-plan)
- **Reference resources:** Anthropic Academy (Claude 101 recommended now); 3Blue1Brown neural network video and StatQuest used in early sessions