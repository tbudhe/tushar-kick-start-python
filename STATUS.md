STATUS.md — Tushar's AI Learning (SINGLE SOURCE OF TRUTH)

Last Updated: 2026-08-10

RULE FOR CLAUDE: This file's "CURRENT STATUS" section overrides ALL other documents in this project. If any other doc conflicts, this file wins.

CURRENT STATUS
Day: 25 IN PROGRESS (quiz done 2026-08-10) | Week: 5 — Phase 2
Goal: Staff SWE → AI Backend Engineer (Autodesk) → Staff/Principal AI Engineer, Walmart, July 2027
Just completed: Day 24 (finished 2026-08-07) — structured outputs + Pydantic deep dive. (1) Cleanup: stale lines 27–28 in structured_output.py deleted by Tushar, clean run verified (file tail = re-attach prefix → validate → print). (2) Field constraints: Field(ge=0.0, le=1.0), min_length — value rules on top of type rules; planted bad input confidence=1.7 → ValidationError naming field/rule/value (less_than_equal). Learned: expected traceback = passing test. (3) Caught him re-running the happy path and calling it a "pass" for the missing-field case — corrected: to test absence, feed absence. He then predicted required-field failure correctly AND ran it (error type=missing). (4) Optional fields: Optional[str] = None — Optional alone still requires the key; the = None default is what permits absence. Design rule: required-by-default, optional only for legitimate absence. (5) Nested models: Source inside RevitAnswer, one validate call recurses the tree, error paths like sources.1.score — noted this shape IS Project 2's answer+chunks. (6) Quiz say-backs: Q3 trim-experiment finally closed (print showed first role = assistant + call succeeded → role-check is hygiene). Q4 stop_reason closed on attempt 6 — accepted the final sentence but see weak spots: re-quiz cold.
Project 1 status: SHIPPED; multi_turn_chat.py (Day 23, trim fix)
Project 2 status: RAGAS triad complete + sabotage-tested. Remaining: real Autodesk doc chunks, model cost decision, ragas upgrade to remove vertexai stub, AND (new) wire typed Pydantic response into eval pipeline (Day 25 warm-up).
Currently strong on: running experiments on demand with printed evidence (planted bad inputs twice, read error output correctly), predicted required-field failure before running, constraint mechanics
Weak spots from quiz (revisit): (1) Optional[str] vs = None split — FAILED twice on 2026-08-10, never produced clean two-part sentence ("Optional allows null value; = None allows absent key") — re-quiz COLD next session. (2) stop_reason "why at the end": CLOSED 2026-08-10 on second attempt (landed "reason doesn't exist mid-stream"), but first framed it as "reason of failure" — watch: end_turn is the happy case, it's the stream's status code. (3) SSE event roles: CLOSED 2026-08-10 — full lifecycle recited in order after 3 skips. (4) Trim experiment finding + prefill re-attach: not re-tested 2026-08-10 — carry. (5) Tendency to test the happy path and declare victory — watch for this in exercises. (6) Nested error paths: framed sources.1.score as "line of code" — corrected to data-tree path (JSON path, not stack trace).
EXERCISE DONE (verified 2026-08-07 with pasted output): nested_practice.py — valid JSON parsed; bad JSON failed at sources.1.score (zero-based index confirmed). structured_output.py restored to minimal known-good (schema/prompt agree, parse lines live, dead experiments deleted); clean run pasted, caveat=None default observed live. NOTE the recurring pattern caught 3x this session: dead/commented code left in file after fixes — watch in future exercises.
CARRIED FORWARD (was due Saturday 2026-08-08 — UNVERIFIED as of 2026-08-10, now overdue): (1) evals.py TEST_CASES still has France in position 4 — run debug_floor.py to confirm ⚠️ follows France mid-list, restore order, run evals.py for 5/5 (retriever n_results now 2, audit prints top-2). (2) Phase 1 recap — explain embeddings → RAG → prompting → evals out loud, plain English.
Next up: Day 25 — (warm-up) wire typed RevitAnswer (with nested Source list) into Project 2's eval pipeline; then tool use / function calling in production (builds on Day 12's tool_use_id: model requests, your code executes).
RECALL QUESTIONS FOR TOMORROW (answer before the session)
1. Optional[str] vs = None — what does EACH part permit? (Two-part sentence, no hints — failed twice 2026-08-10.)
2. What did the printed evidence show in the trim experiment — the finding, not the lesson?
3. Prefill gotcha: what must you do to the response before parsing, and why?
ONE-SENTENCE SUMMARY (say out loud)
"My schema is the API contract for the model's output — constraints catch bad values, Optional declares legitimate absence, and nesting validates the whole tree in one call at the boundary."
KEY MENTAL MODELS (carry into every session)
Schema = API contract for model output — constraints (value rules) + Optional (legitimate absence) + nesting (whole tree, one call)
Optional allows null; only = None default allows ABSENCE — both parts, or the key is still required
Required-by-default (NOT NULL) — optional fields just move the failure downstream to whoever reads None
Expected traceback = passing test — ask "did I expect this?" before "what broke?"
To test absence, feed absence — a happy-path run proves nothing about the missing-field case
Nested validation errors give the full path (sources.1.score) — RAG responses are trees, not flat dicts
When a fix replaces a line, delete the old line in the same edit — last write silently wins
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
stop_reason arrives in message_delta at the END — the reason doesn't exist until the model stops (HTTP trailer); sent to YOUR code so it can decide retry/warn/continue
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
Day 25 (quiz): SSE roles CLOSED, stop_reason closed ("stop creates the reason"); Optional/= None split failed twice → top weak spot; docs synced; Saturday carry-forward still unverified
Day 24 (complete): Pydantic deep dive — Field constraints (planted 1.7 → less_than_equal), Optional + = None (absence vs null), nested models (sources.1.score paths); stale-line cleanup done; "test absence by feeding absence" lesson; stop_reason say-back closed attempt 6 (re-quiz cold)
Day 24 (partial): Structured outputs + Pydantic — untrusted-input boundary validation, both ValidationError modes hit live, prefill fix; trim experiment FALSIFIED the 400 claim with printed evidence; live amnesia demo
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
