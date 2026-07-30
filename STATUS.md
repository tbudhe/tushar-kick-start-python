STATUS.md — Tushar's AI Learning (SINGLE SOURCE OF TRUTH)

Last Updated: 2026-07-30

RULE FOR CLAUDE: This file's "CURRENT STATUS" section overrides ALL other documents in this project. If any other doc conflicts, this file wins.

CURRENT STATUS
Day: 20 | Week: 4
Goal: Staff SWE → AI Backend Engineer (Autodesk) → Staff/Principal AI Engineer, Walmart, July 2027
Just completed: Day 20 — resolved the floor-plan finding via three-layer debugging: hypothesis 1 (miscategorized chunk) falsified in ingest.py (doc5 correctly tagged "floors"); hypothesis 2 (threshold refusal) falsified via debug_floor.py (distance 1.12 < 1.2, gate passed); real cause = layer 3, the LLM's refusal prompt working correctly — context was about creating floor ELEMENTS, question was about floor plan VIEWS. Coverage gap, not bug. Fixed with data: added doc6 (floor plan view, category "floors"), re-ingested (count 6), doc6 now retrieves at 0.76. evals.py 5/5 green (regression check after corpus change).
Project 1 status: SHIPPED — streaming CLI chatbot in chatbots/revit-chatbot/
Project 2 status: floor-plan finding CLOSED (doc6 added, evals green). Remaining: add answer_relevancy + context_precision RAGAS metrics, real Autodesk doc chunks, model cost decision, proper ragas upgrade to remove vertexai stub.
Currently strong on: three-layer refusal debugging (filter → threshold → LLM), evidence-over-hypothesis (print the number), knowledge gap → data fix not code fix
Weak spots from quiz (revisit): needed two re-teaches on WHY the judge grades returned chunks instead of re-retrieving (audit log vs replay) — landed eventually ("second retrieval is a guess about the past, not a record") but fragile, re-quiz it; initially crossed wires between the Q2 filter chain and Q3 tuple unpacking
Exercise owed (do tomorrow morning as warm-up, 15–20 min): extend debug_floor.py to loop over ALL 5 eval questions, print each question's top-3 (id, distance), and flag any question whose best distance is > 1.0 as a "coverage risk" — this builds the habit of auditing retrieval quality before blaming the LLM
Next up: Day 21 — review the exercise output, then add answer_relevancy + context_precision to ragas_evals.py; after that start Phase 2 (streaming + async Claude API patterns)
RECALL QUESTIONS FOR TOMORROW (answer before the session)
1. Name the three layers a RAG refusal can come from, in the order you check them.
2. Doc5 passed the filter AND the threshold — so why did Claude still refuse? Why was that refusal correct?
3. (Repeat — fragile) Why must the RAGAS judge grade against the chunks the pipeline returned instead of calling retrieve() again?
ONE-SENTENCE SUMMARY (say out loud)
"A refusal can fire at the filter, the threshold, or the LLM — I debug the layers in order with printed evidence, and when the LLM refuses correctly, the fix is data, not code."
KEY MENTAL MODELS (carry into every session)
Refusals have three layers: empty filter → distance gate → LLM refusal prompt; check in order, with evidence
A correct refusal that surprises you = coverage gap; fix is data (add docs), not code
Falsify hypotheses with printed numbers — two hypotheses died on Day 20 before the truth surfaced
Corpus changes need regression evals, same as code changes
One pipeline, many importers: prod, deterministic evals, RAGAS all import rag_service — a copied pipeline drifts and evals score a ghost
Judge must grade against the chunks the answer was actually built from — audit log, not replay; a second retrieve() is a guess about the past
Python tuple unpacking is strict: change a return arity → update every caller (unlike JS destructuring)
Eval files are dev tools that test production code — they never ship, but they must import what ships
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
