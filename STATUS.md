STATUS.md — Tushar's AI Learning (SINGLE SOURCE OF TRUTH)

Last Updated: 2026-08-10

RULE FOR CLAUDE: This file's "CURRENT STATUS" section overrides ALL other documents in this project. If any other doc conflicts, this file wins.

DOC PROTOCOL (agreed 2026-08-10): ONE SESSION = ONE DAY NUMBER, sequential, no exceptions. Never reopen a day as "partial", "complete" or "check-in" — if a topic spans two sessions, the second session gets the next number and the heading says "(cont.)". LEARNING_NOTES.md headings are always `## Day N — Topic Name` (no dates, no qualifiers). At the end of EVERY session, update all three: LEARNING_NOTES.md (one new Day block), STATUS.md (this file), MEMORY.md (curriculum line + open items), then commit.

REVISION PROTOCOL (agreed 2026-08-10): every session's quiz is 3 questions on the LAST day PLUS 1 cold question drawn from a RANDOM earlier day (rotate through Days 0–24; prioritise anything on the weak-spots line). Retention, not pace, is the risk — Optional/= None has failed twice and Day 22's SSE questions took three sessions to close. Log the rotation pick in the day's notes so the same days don't keep coming up.

MILESTONES (set 2026-08-10, 11 months to target — recalibrate at each phase end)
Sep 2026: Phase 2 complete — tool use/function calling, LangChain or LlamaIndex, Project 2 hardened (real Autodesk chunks, model cost decision, ragas upgrade)
Nov 2026: Phase 3 complete — LangGraph, agent loops, memory, multi-agent, MCP, LangSmith, guardrails
Dec 2026: Projects 3 and 4 shipped — portfolio complete (4/4)
Feb 2027: job search opens — resume refresh, AI system design interview prep
Jul 2027: Walmart Staff/Principal AI Engineer target — ~5 months of buffer

CURRENT STATUS
Day: 25 COMPLETE | Week: 5 — Phase 2 | Next session = Day 26
Goal: Staff SWE → AI Backend Engineer (Autodesk) → Staff/Principal AI Engineer, Walmart, July 2027
Just completed: Day 25 (finished 2026-08-10) — typed pipeline responses. answer_question returns one RagResponse (answer + nested list[Source] with id/text/distance) instead of a 3-tuple; both branches (refusal + happy path) return the same contract; all 3 callers updated to read fields by name (app.py ids, evals.py ids, ragas_evals.py text). Claude's first Source schema omitted text and would have broken RAGAS faithfulness — caught by checking the third caller; lesson: design the DTO against every consumer. Proof the refactor landed = evals.py RAN (any stale 3-value unpack would TypeError); 5/5 green. Dead-code residue did NOT recur — unused sources line deleted in the same edit. ALSO: both overdue Saturday items closed — debug_floor.py audit loop restored (sabotage query + live category filter removed), retrieval verified healthy (doc3/doc5/doc2/doc4 all rank #1, France flagged mid-list = Day 21 indentation bug gone).
Prior day: Day 24 (finished 2026-08-07) — structured outputs + Pydantic deep dive. (1) Cleanup: stale lines 27–28 in structured_output.py deleted by Tushar, clean run verified (file tail = re-attach prefix → validate → print). (2) Field constraints: Field(ge=0.0, le=1.0), min_length — value rules on top of type rules; planted bad input confidence=1.7 → ValidationError naming field/rule/value (less_than_equal). Learned: expected traceback = passing test. (3) Caught him re-running the happy path and calling it a "pass" for the missing-field case — corrected: to test absence, feed absence. He then predicted required-field failure correctly AND ran it (error type=missing). (4) Optional fields: Optional[str] = None — Optional alone still requires the key; the = None default is what permits absence. Design rule: required-by-default, optional only for legitimate absence. (5) Nested models: Source inside RevitAnswer, one validate call recurses the tree, error paths like sources.1.score — noted this shape IS Project 2's answer+chunks. (6) Quiz say-backs: Q3 trim-experiment finally closed (print showed first role = assistant + call succeeded → role-check is hygiene). Q4 stop_reason closed on attempt 6 — accepted the final sentence but see weak spots: re-quiz cold.
Project 1 status: SHIPPED; multi_turn_chat.py (Day 23, trim fix)
Project 2 status: RAGAS triad complete + sabotage-tested; pipeline now returns typed RagResponse end-to-end. Remaining: real Autodesk doc chunks, model cost decision, ragas upgrade to remove vertexai stub, run ragas_evals.py once against the typed pipeline (costs money — not yet re-run).
Currently strong on: reading printed evidence before verdicts, pushing back on claims and checking files, deleting dead code in the same edit as the fix
Weak spots from quiz (revisit): (1) Optional vs = None split — failed twice 2026-08-10, re-quiz COLD. (2) Trim-experiment finding + prefill re-attach — not re-tested, carry. (3) Happy-path-as-proof habit — improving; identical-output-proves-nothing point landed 2026-08-10. CLOSED 2026-08-10: stop_reason, SSE event roles.
EXERCISE DONE (verified 2026-08-10 with pasted output): added category: str | None = None to RagResponse, set it in answer_question, ran all 3 callers UNEDITED — 5/5 green. DTO payoff proven against Day 19, where the equivalent tuple change broke all three callers.
ALL DAY-25 REVIEW FINDINGS FIXED (2026-08-10, needs a verification run): refused: bool added to RagResponse and set at the refusal branch; evals.py and ragas_evals.py now read the flag instead of matching the string; evals.py asserts rank (sources[0] == expected_id) and asserts sources == [] on refusal to pin the layer; retriever.py exposes THRESHOLD/N_RESULTS and debug_floor.py imports them instead of retyping, with an empty-results guard. VERIFY: run python evals.py (expect 5/5) and python debug_floor.py before Day 26 teaching.
CARRIED FORWARD: (1) Phase 1 recap — explain embeddings → RAG → prompting → evals out loud, plain English (still owed from weekend of 2026-08-08). (2) structured_output.py lines 33–34 still hold a commented-out no_topics experiment — delete.
Next up: Day 26 — warm-up: verify the review fixes (python evals.py → 5/5, python debug_floor.py → keep/drop per row), then tool use / function calling in production (builds on Day 12's tool_use_id: model requests, your code executes).
RECALL QUESTIONS FOR TOMORROW (answer before the session)
1. Two return statements in one function — why must both return the same type, and what's the failure mode if they don't?
2. Adding a field to RagResponse breaks no callers, but adding a tuple slot broke all three. Why?
3. Why did Source need a text field when neither app.py nor evals.py uses it?
4. (COLD, failed twice) Optional[str] vs = None — what does each part permit?
ONE-SENTENCE SUMMARY (say out loud)
"My pipeline returns one validated object, not a tuple of loose values — every branch returns the same contract, and callers read fields by name so new fields cost nothing."
KEY MENTAL MODELS (carry into every session)
Pipeline returns a DTO, not a tuple — callers read names, new fields break nobody (tuple arity breaks everyone)
A function's return type is a promise made by EVERY branch — refusal path and happy path must return the same contract
Same type is not the same contract — branches must populate the same FIELDS too, or the object lies about itself
Sentinel strings across module boundaries are silent-failure bugs — the producer declares state in a field; consumers never parse prose to infer it
== misses refusals when wording changes; substring `in` invents refusals inside real answers — both guess intent from prose, one under-counts, one over-counts
An assertion that breaks loudly when the contract changes is a gift; one that silently tolerates the change is the bug that reaches production
Verify your own fixes with the skepticism you apply to your bugs — grep the file, don't trust the memory of editing it
Design the response object against every consumer, not the loudest one — a dropped field starves a downstream caller (RAGAS needs chunk text)
Identical output after a refactor proves nothing; what proves it is that the callers RAN without TypeError
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
Day 25: Typed pipeline responses — answer_question returns RagResponse (nested list[Source]) not a 3-tuple, both branches same contract, 3 callers updated to read by name; Source.text miss caught by checking the third caller; debug_floor.py audit restored + retrieval verified healthy (Day 21 indentation bug gone); quiz: SSE roles + stop_reason CLOSED, Optional/= None failed twice
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
