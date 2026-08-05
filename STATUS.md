STATUS.md — Tushar's AI Learning (SINGLE SOURCE OF TRUTH)

Last Updated: 2026-08-05

RULE FOR CLAUDE: This file's "CURRENT STATUS" section overrides ALL other documents in this project. If any other doc conflicts, this file wins.

CURRENT STATUS
Day: 24 | Week: 5 — Phase 2
Goal: Staff SWE → AI Backend Engineer (Autodesk) → Staff/Principal AI Engineer, Walmart, July 2027
Just completed: Day 24 (2026-08-05, PARTIAL — resume here) — structured outputs + Pydantic, plus the trim experiment. (1) TRIM EXPERIMENT (see weak-spots item 3): Claude's 400-at-turn-11 claim FALSIFIED with printed evidence — current API accepts assistant-first; role-check downgraded to hygiene. Live amnesia demo observed (window=4 → model lost early turns, drifted off-domain). (2) STRUCTURED OUTPUTS: model output = untrusted input; define schema as Pydantic BaseModel, validate at the boundary with model_validate_json — fails loud at the edge (controller, not DAO). API does NOT enforce schema; your code does, at runtime, per call. (3) Hit failure mode #1 live: model wrapped JSON in markdown fences despite instructions → ValidationError line 1 col 1. Fix = assistant PREFILL: end messages list with {"role":"assistant","content":"{"} — model continues mid-JSON, can't emit preamble; response EXCLUDES prefill so re-attach "{" before parsing. (4) Prefill worked (typed object printed, confidence=1.0 as float) but stale un-prefixed parse line at line 28 caused a second ValidationError ("trailing characters") — diagnosed, fix = delete stale line. (5) NOT yet done: cleanup of structured_output.py, deeper Pydantic (validators, optional fields, nested models), wiring typed output into multi_turn_chat / Project 2. Resume Day 24 here tomorrow — it is NOT complete.
Day 23 recap (previous): multi-turn conversation state + system prompts. (1) API is stateless: messages list = conversation store the client owns (JWT vs server session); full history re-sent every call. (2) Two appends per turn: user msg before call, assistant reply after — missing the second breaks referents ("give me an example of one"). (3) System prompt = separate top-level param (header, not body); re-sent every call, never in messages. Counted 3-message list correctly but initially counted system as #4 — corrected. (4) Growth problem: pay input tokens for full history every call; context window = max request body. Fix = sliding-window trim in PAIRS (list must start with user role). Trimming bug = amnesia (evicted facts), not garbage-in. (5) Exercise DONE: multi_turn_chat.py works multi-turn ("OneExample" referent resolved); latent trim bug found in review — list at send time is odd-length (always ends with user), so even slice [-20:] starts with assistant at turn 11 → API 400; fix applied = role re-check after slice. Noted send-trim vs store-trim: request cost capped, but global list still grows in RAM (eviction problem moved, not solved).
Project 1 status: SHIPPED; multi_turn_chat.py added (Day 23) with trim fix
Project 2 status: RAGAS triad complete + sabotage-tested. Remaining: real Autodesk doc chunks, model cost decision, proper ragas upgrade to remove vertexai stub.
Currently strong on: message-list mechanics (traced 3-message loop correctly with role order), stateless-API ↔ JWT/REST mapping, applied trim fix on his own after review
Weak spots from quiz (revisit): (1) Day 24 morning quiz (2026-08-05): Q1 half credit — knew memory lives in messages list but couldn't name the two appends ("append user BEFORE the call, append assistant AFTER"); corrected, re-quiz tomorrow. Q2 initially gave the fix without the cause; corrected to "input tokens for entire history every call, grows linearly until context window." Q3 corrected to full mechanism (odd-length list + even slice → starts with assistant → 400). (2) SSE event roles re-quiz SKIPPED twice (Day 22 weak spot still open) — text in content_block_delta, stop_reason in message_delta at the end; MUST re-quiz next session. (3) Trim repro RUN 2026-08-05 with instrumentation (printed len + first role) — RESULT: Claude's 400 claim FALSIFIED. Current API accepted first role = assistant, no error. Role-check fix downgraded from crash-prevention to defensive hygiene (keeps trimmed history starting on user turn). Tushar also falsified his own "always user first" hypothesis with the same print. Bonus live amnesia demo: window=4, "show me all messages" → model listed only last window, drifted off-domain (warehouse mgmt ≠ Revit) because grounding turns were evicted.
CARRIED FORWARD (do Saturday 2026-08-08): (1) evals.py TEST_CASES still has France in position 4 — run debug_floor.py to confirm ⚠️ follows France mid-list, restore order, run evals.py for 5/5 (retriever n_results now 2, audit prints top-2). (2) Phase 1 recap — explain embeddings → RAG → prompting → evals out loud, plain English.
Next up: Day 24 continued — (a) verify stale line 28 deleted from structured_output.py and clean run pasted; (b) Pydantic deeper: Field constraints/validators, Optional fields, nested models; (c) wire a typed response into Project 2's eval pipeline. THEN Day 25: tool use / function calling in production (builds on Day 12's tool_use_id).
STILL OWED (say-back, dodged 4x): "stop_reason arrives in message_delta at the END because the model only knows why it stopped once it stops" — make him say it in his own words before any new material.
RECALL QUESTIONS FOR TOMORROW (answer before the session)
1. In structured outputs, what enforces the schema — the API or your code — and what does that mean about when it can fail?
2. How does assistant prefill prevent markdown-fenced JSON, and what must you do to the response text before parsing?
3. What did the trim experiment prove, and what printed evidence proved it?
4. (say-back, owed 4x) Why does stop_reason arrive in message_delta at the END of the stream?
ONE-SENTENCE SUMMARY (say out loud)
"The model's output is untrusted input — validate it at the boundary with a Pydantic schema, and prefill '{' so it starts inside the JSON with no room for preamble."
KEY MENTAL MODELS (carry into every session)
Model output = untrusted input; validate at the boundary (controller, not DAO) — Pydantic model_validate_json fails loud with field-level errors
Prompt instructions are requests, not guarantees — prefill "{" as last assistant message forces mid-JSON continuation; re-attach prefill before parsing
Schema enforcement lives in YOUR code at runtime, per call — the API returns text, nothing more
Messages list = conversation store you own; API = stateless REST (JWT, not server session)
System prompt = request header, not body — re-sent every call, never in messages
Long conversations = cache with no eviction; sliding window trims in pairs, must start with user role
Odd-length list + even slice = starts on the wrong role — re-check structural invariants AFTER slicing (NOTE 2026-08-05: current API accepts assistant-first — no 400; role-check is hygiene, not crash-prevention)
Falsify hypotheses with printed numbers — INCLUDING the teacher's (400-at-turn-11 claim died on a printed "first role = assistant" + successful call)
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
Day 24 (partial): Structured outputs + Pydantic — untrusted-input boundary validation, both ValidationError modes hit live, prefill fix; trim experiment FALSIFIED the 400 claim with printed evidence; live amnesia demo; resume Day 24 tomorrow
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
