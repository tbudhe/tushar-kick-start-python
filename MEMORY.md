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

Tushar has completed Day 0 through Day 19 of the curriculum — Phase 1 complete (capstone Day 17), now in the Phase 1→2 bridge doing eval engineering on Project 2 (running roughly 2x the original day-per-topic pace; treat "18-week" boundaries as loose from here and track by topic completion instead):

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

**Active open items:**
- **Floor-plan category finding:** "What is a floor plan view?" refuses under category="floors" — verify chunk category in ingest.py, fix tag or eval (Day 20).
- **evals.py green run** after the 3-tuple refactor — syntax-checked but not yet executed.
- **RAGAS metrics to add:** answer_relevancy, context_precision; also model cost decision and proper ragas upgrade to drop the vertexai import stub.
- **git push** of Day 19 commit (20f9005) — commit made in sandbox, push needs Tushar's credentials.

**Resolved since last update:**
- **Project 1 VERIFIED AND SHIPPED** — streaming CLI chatbot in chatbots/revit-chatbot/ (memory, streaming, TTFT). The long-standing "content outpacing builds" risk is closed: 2 of 4 portfolio projects shipped.
- Refusal-exclusion in RAGAS evals (Day 18 exercise, done correctly: skip refusals, refusal_rate separate metric, all-refusals guard).
- Double-retrieval bug in ragas_evals.py (Day 19 refactor).

**Recall/articulation quality:** Markedly improved since Day 7. Tushar is now producing full, precise restated sentences unprompted (e.g., Day 16 Q2 self-corrected "prompts drive it" → "prompt size drives it" in the same pass). The "precision gap" pattern flagged below is closing — keep watching, don't assume fully resolved yet.

**Next content block:** Day 20 — close the floor-plan category finding + green evals.py run, add answer_relevancy + context_precision, then start Phase 2 (streaming + async Claude API patterns). The build-vs-content gap is closed; the current mode (build → eval surfaces a finding → fix → learn) is working well and should continue.

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
- **Analogy anchors that work:** Kafka pipelines, SQL queries (ORDER BY / WHERE), distributed systems, cache-aside pattern (Redis vs database), Express middleware vs HTTP request body, TCP sliding window for chunk overlap, PostGIS for embeddings, event loop with dynamic dispatch (agent tool loop), Redux store (LangGraph state, not yet covered). Walmart fraud detection system is the strongest recurring anchor.
- **ChromaDB threshold principle (repeatedly reinforced):** The vector database always returns n results — it does not filter by relevance. Threshold filtering is the application's responsibility, not the database's. This concept is now solid across Days 5–7; treat as internalized rather than needing repeated correction.
- **Metadata filtering mechanics:** The `where` filter runs before vector search — documents that fail the filter are excluded entirely and never reach similarity ranking. Closest allowed result is always returned regardless of actual relevance.
- **Pacing vs. building gap:** Tushar is consuming topics faster than he is building portfolio artifacts (16 content days vs. zero verified projects). This is the top coaching risk going into Phase 2 — prioritize build sessions over new content until Project 1 is confirmed.

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