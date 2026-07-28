STATUS.md — Tushar's AI Learning (SINGLE SOURCE OF TRUTH)

Last Updated: 2026-07-28

RULE FOR CLAUDE: This file's "CURRENT STATUS" section overrides ALL other documents in this project. If any other doc conflicts, this file wins.

CURRENT STATUS
Day: 18 | Week: 4
Goal: Staff SWE → AI Backend Engineer (Autodesk) → Staff/Principal AI Engineer, Walmart, July 2027
Just completed: Day 18 — RAGAS faithfulness evals wired into Project 2 (ragas_evals.py: judge=Claude via LangchainLLMWrapper, per-row scores via to_pandas; found refusal-scoring distortion — correct "I don't know" scored 0.0)
Project 1 status: SHIPPED — streaming CLI chatbot in chatbots/revit-chatbot/
Project 2 status: v1 + RAGAS faithfulness running on prod code path. Remaining: refusal-exclusion exercise (assigned), double-retrieval refactor — answer_question should return (answer, sources, chunks) (assigned, Day 19), more RAGAS metrics (answer_relevancy, context_precision), real Autodesk doc chunks, model cost decision, proper ragas upgrade to remove vertexai stub.
Currently strong on: faithfulness mechanics (claim decomposition, answer ⊆ contexts), judge-vs-pipeline LLM roles, deterministic vs LLM-judged eval separation, venv + dependency-conflict debugging
Weak spots from quiz (revisit): threshold formula recall (said 1.8; it's (0.75+1.69)/2 ≈ 1.2); state BOTH halves of prompt placement (system = policy AND user message = payload)
Next up: Day 19 — verify refusal-exclusion + (answer, sources, chunks) refactor across all 3 callers, add answer_relevancy + context_precision, then start Phase 2 (streaming + async Claude API patterns)
KEY MENTAL MODELS (carry into every session)
Faithfulness = grounding, not truth: judge checks answer ⊆ contexts, domain-blind
Correct refusals score 0 on faithfulness — exclude them; refusal_rate is its own metric
Deterministic evals = unit tests (every change, free); RAGAS = load tests (on prompt/threshold/chunk changes, costs money)
Both eval files import rag_service — never a copy of the pipeline
Thresholds are outputs of calibration experiments, not guesses
ingest = write path; retriever = read path; neither imports the other
Empty retrieval → short-circuit before the LLM: no context, no call, no hallucination, no cost
Refusal rules in system prompt (middleware policy); context + question in user message (request payload)
DBs return "closest," not "relevant" — thresholds are application code's job
Knowledge gap → RAG; behavior gap → prompting first, fine-tuning last
Prefill = parallel, sets TTFT; decode = sequential, sets streaming speed
site-packages-only traceback = dependency conflict, not your code; venv = node_modules
PROGRESS LOG (most recent first — headline only)
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
