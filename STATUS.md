STATUS.md — Tushar's AI Learning (SINGLE SOURCE OF TRUTH)

Last Updated: 2026-07-31

RULE FOR CLAUDE: This file's "CURRENT STATUS" section overrides ALL other documents in this project. If any other doc conflicts, this file wins.

CURRENT STATUS
Day: 21 | Week: 4 — PHASE 1 COMPLETE
Goal: Staff SWE → AI Backend Engineer (Autodesk) → Staff/Principal AI Engineer, Walmart, July 2027
Just completed: Day 21 (full) — (1) retrieval audit loop in debug_floor.py: all eval questions, top-k (id, distance) via zip, coverage-risk flag at best distance > 1.0; France flags at 1.896 = correct behavior. Three indentation bugs debugged the hard way (dedented block ran once on leaked loop variables and looked right by accident because France was last; for...else trap; per-chunk vs per-question flag placement). (2) RAGAS triad completed in ragas_evals.py: answer_relevancy (needs embeddings model — LangchainEmbeddingsWrapper + all-MiniLM-L6-v2) and context_precision (needs reference ground-truth per question). Results: faithfulness 1.0, relevancy 0.75–0.98 across runs (judge non-determinism observed 3×), precision 1.0. (3) Sabotage test DONE: floor question forced to category "walls" → all judge metrics stayed perfect but refusal_rate jumped to 0.5 and n dropped to 1 — retrieval failure surfaced as refusal, invisible to quality metrics. Layer identified with evidence: wall-chunk distances 1.636/1.653 > 1.2 threshold = layer 2, LLM never called (guessed layer 3 first; printed number flipped it). Traced short-circuit through code: retrieve() filters per-chunk, answer_question() returns "I don't know" on empty chunks before ask_revit_question — the only real LLM call (collection.query = local ChromaDB, free). Reverted; final run n=2, refusal_rate 0.0.
Naming (committed Day 21, commit 2decd7a): judge → judge_llm, questions → EVAL_QUESTIONS in ragas_evals.py; SYSTEM_PROMPT constant in prompting/revit_context_qa.py; retriever.py n_results 3 → 2.
Project 1 status: SHIPPED — streaming CLI chatbot in chatbots/revit-chatbot/
Project 2 status: RAGAS triad complete + sabotage-tested. Remaining: real Autodesk doc chunks, model cost decision, proper ragas upgrade to remove vertexai stub.
Currently strong on: metric triad mapping (precision→retrieval, faithfulness→grounding, relevancy→direction), refusal_rate as the metric that catches what judge metrics miss, evidence-over-guess (predicted layer 3, number proved layer 2)
Weak spots from quiz (revisit): Day 20 Q2 took three attempts — kept reaching for falsified "wrong category chunk" instead of "context didn't answer the question, refusal prevented hallucination"; re-quiz correct-refusal reasoning. Indentation discipline — two dedent/indent bugs in one session. Briefly confused collection.query with an LLM call — re-check "which call is which" awareness.
Exercise owed (Saturday, 5 min): evals.py TEST_CASES is still committed with France in position 4 — run debug_floor.py to confirm the ⚠️ follows France mid-list, then restore original order and run evals.py for 5/5. Note: retriever n_results is now 2, so audit prints top-2.
WEEKEND PLAN
Saturday: light — owed item above + say the 3 recall questions out loud. Nothing new.
Sunday: weekly quiz = PHASE 1 RECAP — explain Phase 1 back in plain English (embeddings → RAG → prompting → evals). Phase boundary consolidation.
Next up: Day 22 (Monday) — START PHASE 2: streaming + async Claude API patterns (streaming tokens = chunked transfer encoding / SSE; async batch = Promise.all → asyncio.gather). Builds toward Project 1 upgrades and Project 4.
RECALL QUESTIONS FOR TOMORROW (answer before the session)
1. Faithfulness checks the answer against ___; answer_relevancy against ___; context_precision checks the ___ against the ___.
2. You broke retrieval and all three judge metrics stayed perfect — what caught the failure, and why didn't the judge see it?
3. Which layer refused the sabotaged floor question, and what evidence proved it (numbers)?
ONE-SENTENCE SUMMARY (say out loud)
"Context_precision grades retrieval, faithfulness grades grounding, answer_relevancy grades direction — but a refused question reaches none of them, so refusal_rate and n are the metrics that catch what the judges can't see."
KEY MENTAL MODELS (carry into every session)
Metric triad = pipeline stages: context_precision→retrieval, faithfulness→grounding, answer_relevancy→direction
Refused questions never reach the judge — refusal_rate and n catch what quality metrics miss (error rate vs latency dashboard)
Faithful but irrelevant = retrieval problem (answer came entirely from chunks)
Coverage-risk flag means "can't ground this" — human interprets: domain question = gap, off-topic = working as designed
Judge metrics are non-deterministic (0.75–0.92 same code) — trends and comparisons, never single absolutes
Reference = expected value of a unit test; judge can't grade chunk relevance without an answer key
collection.query = local vector DB (free); ask_revit_question = the only LLM call (guarded by the short-circuit)
Retriever = bouncer (per-chunk threshold), service = manager (empty → refuse); repo returns empty, service decides 404
Python indentation = "how many times does this line run"; you are the closing brace; leaked loop variables make wrong code look right
KeyError points at the crash line, but the bug lives where the dict was built
Refusals have three layers: empty filter → distance gate → LLM refusal prompt; check in order, with evidence
A correct refusal that surprises you = coverage gap; fix is data, not code
Falsify hypotheses with printed numbers — layer-3 guess died on a 1.636
Corpus changes need regression evals, same as code changes
One pipeline, many importers: prod, deterministic evals, RAGAS all import rag_service
Judge must grade against the chunks the answer was actually built from — audit log, not replay
Python tuple unpacking is strict: change a return arity → update every caller
Faithfulness = grounding, not truth; correct refusals score 0 — exclude them; refusal_rate is its own metric
Deterministic evals = unit tests (every change, free); RAGAS = load tests (costs money)
Thresholds are outputs of calibration experiments, not guesses
ingest = write path; retriever = read path; neither imports the other
Empty retrieval → short-circuit before the LLM: no context, no call, no hallucination, no cost
Refusal rules in system prompt; context + question in user message
DBs return "closest," not "relevant" — thresholds are application code's job
Knowledge gap → RAG; behavior gap → prompting first, fine-tuning last
Prefill = parallel, sets TTFT; decode = sequential, sets streaming speed
site-packages-only traceback = dependency conflict, not your code; venv = node_modules
PROGRESS LOG (most recent first — headline only)
Day 21: Retrieval audit loop + RAGAS triad + sabotage test — refusal_rate caught what judge metrics missed; layer-2 refusal proven with 1.636 > 1.2; judge non-determinism observed. PHASE 1 COMPLETE.
Day 20: Floor-plan finding closed — three-layer refusal debugging, two hypotheses falsified, correct LLM refusal exposed coverage gap, doc6 added, evals 5/5
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
