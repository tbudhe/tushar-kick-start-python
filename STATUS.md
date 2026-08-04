STATUS.md — Tushar's AI Learning (SINGLE SOURCE OF TRUTH)

Last Updated: 2026-08-04

RULE FOR CLAUDE: This file's "CURRENT STATUS" section overrides ALL other documents in this project. If any other doc conflicts, this file wins.

CURRENT STATUS
Day: 23 | Week: 5 — Phase 2
Goal: Staff SWE → AI Backend Engineer (Autodesk) → Staff/Principal AI Engineer, Walmart, July 2027
Just completed: Day 23 (full, exercise DONE) — multi-turn conversation state + system prompts. (1) API is stateless: messages list = conversation store the client owns (JWT vs server session); full history re-sent every call. (2) Two appends per turn: user msg before call, assistant reply after — missing the second breaks referents ("give me an example of one"). (3) System prompt = separate top-level param (header, not body); re-sent every call, never in messages. Counted 3-message list correctly but initially counted system as #4 — corrected. (4) Growth problem: pay input tokens for full history every call; context window = max request body. Fix = sliding-window trim in PAIRS (list must start with user role). Trimming bug = amnesia (evicted facts), not garbage-in. (5) Exercise DONE: multi_turn_chat.py works multi-turn ("OneExample" referent resolved); latent trim bug found in review — list at send time is odd-length (always ends with user), so even slice [-20:] starts with assistant at turn 11 → API 400; fix applied = role re-check after slice. Noted send-trim vs store-trim: request cost capped, but global list still grows in RAM (eviction problem moved, not solved).
Project 1 status: SHIPPED; multi_turn_chat.py added (Day 23) with trim fix
Project 2 status: RAGAS triad complete + sabotage-tested. Remaining: real Autodesk doc chunks, model cost decision, proper ragas upgrade to remove vertexai stub.
Currently strong on: message-list mechanics (traced 3-message loop correctly with role order), stateless-API ↔ JWT/REST mapping, applied trim fix on his own after review
Weak spots from quiz (revisit): (1) Day 22 quiz — missed asyncio.run(main()) as entry point; evidence recall imprecise ([:60] is chars not words; didn't cite stop_reason+len as proof); said content_block_stop carries stop_reason — it's message_delta (retried, corrected). Re-quiz SSE event roles. (2) Trimming consequence — said "irrelevant data" instead of amnesia/lost referents. (3) Verify he actually ran the 11-turn test to see the 400 with old trim (evidence habit).
CARRIED FORWARD (do Saturday 2026-08-08): (1) evals.py TEST_CASES still has France in position 4 — run debug_floor.py to confirm ⚠️ follows France mid-list, restore order, run evals.py for 5/5 (retriever n_results now 2, audit prints top-2). (2) Phase 1 recap — explain embeddings → RAG → prompting → evals out loud, plain English.
Next up: Day 24 — verify 11-turn trim test evidence first, then structured outputs + Pydantic (typed API responses; ties to Project 2's eval pipeline).
RECALL QUESTIONS FOR TOMORROW (answer before the session)
1. The API is stateless — where does conversation memory actually live, and what two appends per turn maintain it?
2. Why does a long conversation get more expensive per call, and what's the simplest eviction strategy?
3. Why did the even slice [-20:] break at turn 11, and what does the fixed trim() check after slicing?
ONE-SENTENCE SUMMARY (say out loud)
"The API is stateless — the messages list is the conversation store I own, re-sent in full every call, so it needs an eviction policy like any cache."
KEY MENTAL MODELS (carry into every session)
Messages list = conversation store you own; API = stateless REST (JWT, not server session)
System prompt = request header, not body — re-sent every call, never in messages
Long conversations = cache with no eviction; sliding window trims in pairs, must start with user role
Odd-length list + even slice = starts on the wrong role — re-check structural invariants AFTER slicing
Trimming bug = amnesia (evicted keys you still needed), not garbage-in
Send-trim caps API cost; store-trim caps RAM — know which one you fixed
stop_reason arrives in message_delta at the END — model only knows why it stopped once it stops (HTTP trailer)
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
Day 23: Multi-turn state + system prompts — messages list = conversation store (stateless API/JWT), system = header not body, sliding-window trim in pairs; latent odd/even trim bug found + fixed in multi_turn_chat.py; amnesia-not-garbage trimming bug
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
