STATUS.md — Tushar's AI Learning (SINGLE SOURCE OF TRUTH)

Last Updated: 2026-07-29

RULE FOR CLAUDE: This file's "CURRENT STATUS" section overrides ALL other documents in this project. If any other doc conflicts, this file wins.

CURRENT STATUS
Day: 19 | Week: 4
Goal: Staff SWE → AI Backend Engineer (Autodesk) → Staff/Principal AI Engineer, Walmart, July 2027
Just completed: Day 19 — double-retrieval refactor: answer_question now returns (answer, sources, chunks); all 3 callers updated (app.py, evals.py, ragas_evals.py); ragas_evals grades the judge against the pipeline's ACTUAL chunks, second retrieve() deleted. Eval with category filters surfaced a real finding: "floor plan view" refused under category="floors" (likely miscategorized chunk — WHERE filter ran before vector search, empty retrieval → short-circuit).
Project 1 status: SHIPPED — streaming CLI chatbot in chatbots/revit-chatbot/
Project 2 status: refusal-exclusion + (answer, sources, chunks) refactor DONE. Remaining: verify floor-plan chunk category in ingest (open finding), run evals.py to confirm green, add answer_relevancy + context_precision, real Autodesk doc chunks, model cost decision, proper ragas upgrade to remove vertexai stub (deprecation warnings now visible for ragas.metrics import and LangchainLLMWrapper).
Currently strong on: single-source-of-truth pipeline (import, never copy), refusal exclusion + refusal_rate as separate metric, why judge must score against the chunks the answer was built from
Weak spots from quiz (revisit): confused WHY the judge scores refusals 0 (no supported claims) with WHY the refusal happened (distance threshold) — pipeline behavior vs eval behavior are different layers; Python strict tuple unpacking (3-return crashes 2-var callers — Node array destructuring silently drops extras, Python doesn't)
Next up: Day 20 — resolve the floor-plan category finding (check ingest tags), run evals.py green, add answer_relevancy + context_precision, then start Phase 2 (streaming + async Claude API patterns)
KEY MENTAL MODELS (carry into every session)
One pipeline, many importers: prod, deterministic evals, RAGAS all import rag_service — a copied pipeline drifts and evals score a ghost
Judge must grade against the chunks the answer was actually built from — return them from the pipeline, never re-retrieve
Python tuple unpacking is strict: change a return arity → update every caller (unlike JS destructuring)
Eval files are dev tools that test production code — they never ship, but they must import what ships
A surprising refusal in evals is a finding, not a bug — trace it: filter → empty retrieval → short-circuit
Faithfulness = grounding, not truth: judge checks answer ⊆ contexts, domain-blind
Correct refusals score 0 on faithfulness — exclude them; refusal_rate is its own metric
Deterministic evals = unit tests (every change, free); RAGAS = load tests (on prompt/threshold/chunk changes, costs money)
Thresholds are outputs of calibration experiments, not guesses
ingest = write path; retriever = read path; neither imports the other
Empty retrieval → short-circuit before the LLM: no context, no call, no hallucination, no cost
Refusal rules in system prompt (middleware policy); context + question in user message (request payload)
DBs return "closest," not "relevant" — thresholds are application code's job
Knowledge gap → RAG; behavior gap → prompting first, fine-tuning last
Prefill = parallel, sets TTFT; decode = sequential, sets streaming speed
site-packages-only traceback = dependency conflict, not your code; venv = node_modules
PROGRESS LOG (most recent first — headline only)
Day 19: Double-retrieval refactor — (answer, sources, chunks), 3 callers, judge grades real chunks; category filter surfaced miscategorized-chunk finding
Day 18: RAGAS faithfulness on Project 2 — judge LLM, refusal distortion found, per-row analysis
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

Full per-day Q&A and one-liners live in LEARNING_NOTES.md. Use it for content review only — NEVER for determining current progress.
