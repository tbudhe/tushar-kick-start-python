STATUS.md — Tushar's AI Learning (SINGLE SOURCE OF TRUTH)

Last Updated: 2026-07-25

RULE FOR CLAUDE: This file's "CURRENT STATUS" section overrides ALL other documents in this project. If any other doc conflicts, this file wins.

CURRENT STATUS
Day: 17 | Week: 4
Goal: Staff SWE → AI Backend Engineer (Autodesk) → Staff/Principal AI Engineer, Walmart, July 2027
Just completed: Day 17 — Phase 1 capstone review + Project 2 v1 SHIPPED (RAG API: FastAPI /ask + ChromaDB retriever with calibrated threshold 1.2 + Claude refusal prompt + sources + evals 5/5 on production code path)
Project 1 status: SHIPPED (built Days 4–16) — streaming CLI chatbot in chatbots/revit-chatbot/: multi-turn memory, streaming, system prompt, TTFT instrumentation, tool-use + CoT variants
Project 2 status: v1 complete (ingest.py, retriever.py, rag_service.py, app.py, prompting/revit_context_qa.py, evals.py). Refactored: shared rag_service so evals test prod path; DB path anchored to file dir. Remaining: RAGAS evals, more/real Autodesk doc chunks, model cost decision (currently opus — consider sonnet/haiku).
Currently strong on: full RAG pipeline in real code, threshold calibration methodology, write-path/read-path separation, refusal prompting, empty-context short-circuit
Weak spots from capstone quiz (revisit): stating full query-time steps unprompted; hallucination-control = instructions in system prompt, not just prompt assembly
Next up: Day 18 — RAGAS evals on Project 2, then start Phase 2 (streaming + async Claude API patterns)
KEY MENTAL MODELS (carry into every session)
Thresholds are outputs of calibration experiments, not guesses (gap between 0.75 and 1.69 → chose 1.2)
ingest = write path (seed job); retriever = read path (DAO); neither imports the other
Empty retrieval → short-circuit before the LLM: no context, no call, no hallucination, no cost
Refusal rules live in system prompt (middleware policy); context + question in user message (request payload)
Evals must import the same function production runs — never a copy of the pipeline
DBs return "closest," not "relevant" — thresholds are application code's job
Knowledge gap → RAG; behavior gap → prompting first, fine-tuning last
Prefill = parallel, sets TTFT; decode = sequential, sets streaming speed
PROGRESS LOG (most recent first — headline only)
Day 17: Phase 1 capstone + Project 2 v1 shipped — RAG API end-to-end, evals 5/5
Day 16: Inference in production — prefill/decode, TTFT
Day 15: Fine-tuning vs RAG vs prompting — knowledge gap vs behavior gap
Day 14: Model comparison — spec-sheet selection (context, cost, latency, benchmarks)
Day 13: Hallucinations — softmax has no "I don't know"; RAG closes knowledge gap, refusal prompting closes behavior gap
Day 12: Chain-of-thought + function calling (model requests, your code executes; tool_use_id)
Day 11: Pretraining → SFT → RLHF
Day 10: Transformers — positional encoding, multi-head attention, stacked layers
Day 9: Weight vs. bias; underdetermined systems
Day 8: Loss, gradient descent, overfitting, train/test split
Day 7: Metadata filtering (WHERE clause before vector search)
Day 6: Chunking + overlap
Day 5: ChromaDB — persistence, distance vs. similarity
Day 4: Prompt engineering — system prompt, few-shot
Day 3: RAG pipeline
Day 2: Embeddings + cosine similarity
Day 1: Tokenization, embeddings, attention
Day 0: ML basics
ARCHIVE NOTE

Full per-day Q&A and one-liners live in the "Learning Notes" doc. Use it for content review only — NEVER for determining current progress.
