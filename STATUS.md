STATUS.md — Tushar's AI Learning (SINGLE SOURCE OF TRUTH)

Last Updated: 2026-08-03

RULE FOR CLAUDE: This file's "CURRENT STATUS" section overrides ALL other documents in this project. If any other doc conflicts, this file wins.

CURRENT STATUS
Day: 22 | Week: 5 — PHASE 2 STARTED
Goal: Staff SWE → AI Backend Engineer (Autodesk) → Staff/Principal AI Engineer, Walmart, July 2027
Just completed: Day 22 (full, exercise included) — streaming + async Claude API. (1) Streaming = SSE/chunked transfer: .stream() context manager, text_stream generator, flush=True; raw event sequence message_start → content_block_start → content_block_delta (text) → content_block_stop → message_delta (stop_reason, output tokens) → message_stop. stop_reason = stream's HTTP status code ("end_turn" vs "max_tokens" truncation). (2) Async: AsyncAnthropic + asyncio.gather = Promise.all (concurrent, ordered, fail-fast); asyncio.run(main()) starts the loop (Node's is always running); * spreads the iterable. Ran 3 Revit questions concurrently in chatbots/revit-chatbot/async_batch_questions.py. (3) Bug hit live: swapped in AsyncAnthropic but kept sync def/with — async client needs async def + async with + async for; client class must match function style. (4) Exercise DONE with evidence: ask() returns tuple[str, str] (text, stop_reason), caller unpacks (a, stop_reason) — arity rule applied unprompted. At max_tokens=1000 all three questions returned end_turn with len 1975/1005/1141 — the "..." was the [:60] print slice (display truncation), not API truncation. Assumed max_tokens was the cause; printed evidence proved otherwise.
Project 1 status: SHIPPED — streaming CLI chatbot in chatbots/revit-chatbot/; async_batch_questions.py added (Day 22)
Project 2 status: RAGAS triad complete + sabotage-tested. Remaining: real Autodesk doc chunks, model cost decision, proper ragas upgrade to remove vertexai stub.
Currently strong on: gather/Promise.all mapping, dotenv env handling (added on his own), tuple-arity discipline, evidence-over-guess (applied twice in one day)
Weak spots from quiz (revisit): Q1 metric-triad needed a retry — named concepts instead of the objects compared (answer vs chunks / answer vs question / chunks vs reference); Q3 evidence precision — said "1.6 and 1.5", actual 1.636/1.653; re-quiz exact-evidence recall. Sync/async client mixing (caught live Day 22).
CARRIED FORWARD (do Saturday 2026-08-08): (1) evals.py TEST_CASES still has France in position 4 — run debug_floor.py to confirm ⚠️ follows France mid-list, restore order, run evals.py for 5/5 (retriever n_results now 2, audit prints top-2). (2) Phase 1 recap — explain embeddings → RAG → prompting → evals out loud, plain English.
Next up: Day 23 — multi-turn conversation state + system prompts via the API (messages list = the conversation store; ties to Project 1 upgrade), then structured outputs/Pydantic later in the week.
RECALL QUESTIONS FOR TOMORROW (answer before the session)
1. Sync client uses def/with/for — what three keywords change with AsyncAnthropic, and what must you call once at the entry point?
2. stop_reason "end_turn" vs "max_tokens" — what does each mean, and what evidence proved your "..." was display truncation, not API truncation?
3. In the SSE event sequence, which event type carries the text, and which carries stop_reason?
ONE-SENTENCE SUMMARY (say out loud)
"Streaming is SSE — text arrives as typed events with stop_reason as the stream's status code; async is Promise.all as asyncio.gather, and the client class must match the function style."
KEY MENTAL MODELS (carry into every session)
Streaming = SSE/chunked transfer; text_stream = filtered consumer, raw events = the full topic
stop_reason = HTTP status code of the stream — never render it, never ignore it
asyncio.gather = Promise.all; asyncio.run starts the loop yourself (Node's always runs)
Client class must match function style: Async client → async def/async with/async for
Display truncation vs API truncation — printed evidence (stop_reason, len) decides, not rendered output
Prefill = parallel, sets TTFT; decode = sequential, sets streaming speed
Metric triad = pipeline stages: context_precision→retrieval, faithfulness→grounding, answer_relevancy→direction
Refused questions never reach the judge — refusal_rate and n catch what quality metrics miss
Coverage-risk flag means "can't ground this" — human interprets: domain question = gap, off-topic = working as designed
Judge metrics are non-deterministic — trends and comparisons, never single absolutes
Reference = expected value of a unit test; judge can't grade chunk relevance without an answer key
collection.query = local vector DB (free); the LLM call is the guarded one
Retriever = bouncer (per-chunk threshold), service = manager (empty → refuse)
Python indentation = "how many times does this line run"; you are the closing brace
KeyError points at the crash line, but the bug lives where the dict was built
Refusals have three layers: empty filter → distance gate → LLM refusal prompt; check in order, with evidence
A correct refusal that surprises you = coverage gap; fix is data, not code
Falsify hypotheses with printed numbers — layer-3 guess died on a 1.636
Corpus changes need regression evals, same as code changes
One pipeline, many importers: prod, deterministic evals, RAGAS all import rag_service
Python tuple unpacking is strict: change a return arity → update every caller
Faithfulness = grounding, not truth; correct refusals score 0 — exclude them; refusal_rate is its own metric
Deterministic evals = unit tests (every change, free); RAGAS = load tests (costs money)
Thresholds are outputs of calibration experiments, not guesses
DBs return "closest," not "relevant" — thresholds are application code's job
Knowledge gap → RAG; behavior gap → prompting first, fine-tuning last
site-packages-only traceback = dependency conflict, not your code; venv = node_modules
PROGRESS LOG (most recent first — headline only)
Day 22: PHASE 2 START — streaming (SSE events, stop_reason) + async (gather = Promise.all); sync/async client-mixing bug caught live; stop_reason evidence proved display truncation, not API truncation
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
