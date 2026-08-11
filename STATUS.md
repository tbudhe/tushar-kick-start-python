STATUS.md — Tushar's AI Learning (SINGLE SOURCE OF TRUTH)

Last Updated: 2026-08-11

RULE FOR CLAUDE: This file's "CURRENT STATUS" section overrides ALL other documents in this project. If any other doc conflicts, this file wins.

DOC PROTOCOL (agreed 2026-08-10): ONE SESSION = ONE DAY NUMBER, sequential, no exceptions. Never reopen a day as "partial", "complete" or "check-in" — if a topic spans two sessions, the second session gets the next number and the heading says "(cont.)". LEARNING_NOTES.md headings are always `## Day N — Topic Name` (no dates, no qualifiers). At the end of EVERY session, update all three: LEARNING_NOTES.md (one new Day block), STATUS.md (this file), MEMORY.md (curriculum line + open items), then commit.

REVISION PROTOCOL (agreed 2026-08-10): every session's quiz is 3 questions on the LAST day PLUS 1 cold question drawn from a RANDOM earlier day (rotate through Days 0–25; prioritise anything on the weak-spots line). Log the rotation pick in the day's notes. Rotation picks so far: Day 24 (2026-08-11, passed).

MILESTONES (set 2026-08-10, 11 months to target — recalibrate at each phase end)
Sep 2026: Phase 2 complete — tool use/function calling, LangChain or LlamaIndex, Project 2 hardened (real Autodesk chunks, model cost decision, ragas upgrade)
Nov 2026: Phase 3 complete — LangGraph, agent loops, memory, multi-agent, MCP, LangSmith, guardrails
Dec 2026: Projects 3 and 4 shipped — portfolio complete (4/4)
Feb 2027: job search opens — resume refresh, AI system design interview prep
Jul 2027: Walmart Staff/Principal AI Engineer target — ~5 months of buffer

CURRENT STATUS
Day: 26 COMPLETE | Week: 5 — Phase 2 | Next session = Day 27
Goal: Staff SWE → AI Backend Engineer (Autodesk) → Staff/Principal AI Engineer, Walmart, July 2027
Just completed: Day 26 (2026-08-11) — tool use / function calling in production. Three concepts: (1) the loop — `while True` calling the API until stop_reason != "tool_use"; can't be a single if because round-trip count is unknown; stop_reason steers control flow. (2) Tool schemas — OpenAPI-spec analogy; description field is prompt engineering not docs; input_schema = JSON Schema (Pydantic's rules, opposite direction: schema = what I accept, Pydantic = validate what the model sends); schema is a request not a guarantee — tools still validate. (3) tool_use content blocks — id/name/input(dict), dispatch via TOOL_FUNCTIONS[name] (event loop + dynamic dispatch made literal), tool_result echoes tool_use_id (correlation ID / Kafka reply-key), results return as role="user". Big picture landed after "what are we trying to do": RAG = push (my code drives fetching), tool use = pull (model drives); agents = this loop + tool catalog. Clarified stop_reason is NOT streaming-only (Day 22 only taught WHERE it arrives when streaming).
Day 26 warm-up VERIFIED with pasted output: evals.py 5/5 (refused=True sources=[] on France row), debug_floor.py healthy (all real queries rank #1 under 0.7, France 1.896/1.973 drop + coverage flag). All Day-25 review fixes confirmed landed.
Quiz results (Day 25 material + cold): Q2 position-vs-name — correct after tightening (had the what, not the mechanism). Q3 Source.text — 80%, didn't name ragas_evals.py as the consumer. Q1 branch-contract failure mode — needed full reframe + 10-line demo; closed on "crash in the caller, only when the rarer branch fires; bug location ≠ crash location". Q4 (COLD, Day 24, failed twice before): Optional[str] vs = None — PASSED, correct Joi analogy. One more cold re-check ~2026-08-18 to confirm.
Project 1 status: SHIPPED; multi_turn_chat.py (Day 23, trim fix)
Project 2 status: RAGAS triad complete + sabotage-tested; typed RagResponse end-to-end, review fixes verified 2026-08-11. Remaining: real Autodesk doc chunks, model cost decision, ragas upgrade to remove vertexai stub, run ragas_evals.py once against typed pipeline (costs money — not yet re-run).
Currently strong on: reading printed evidence before verdicts, questioning teacher claims (challenged stop_reason-as-streaming), Day 12 tool_use_id recall word-perfect
Weak spots from quiz (revisit): (1) Optional vs = None — passed 2026-08-11 after two failures; ONE more cold check ~2026-08-18. (2) Trim-experiment finding + prefill re-attach — still not re-tested, carry. (3) Failure-mode reasoning (what breaks if the contract is violated) — describes contracts well but had to be walked to the crash-here-bug-there consequence; probe "what breaks and where" in future quizzes. (4) Schema/description direction — wrote inverted descriptions twice (name vs ticker, in vs out); rule: say the signature out loud, then transcribe.
EXERCISE DONE (verified 2026-08-11 with pasted output): tool_loop.py (chatbots/stocks_chatbot/) ran the full loop — stop_reason sequence tool_use → tool_use → end_turn, sequential tool calls (get_company_name then get_stock_price, dependency chain), dispatch dict + tool_result round trip working. Debugging detour: fixed scripted-future bug (response.content inside the call creating response), wrong-loop bug (REPL where the tool loop belonged), inverted get_company_name. Learned VS Code debugpy setup (integratedTerminal for input(), cwd for load_dotenv, breakpoints on messages.append to watch the transcript grow).
CARRIED FORWARD: (1) Phase 1 recap — explain embeddings → RAG → prompting → evals out loud, plain English (owed since weekend of 2026-08-08). (2) structured_output.py lines 33–34 commented-out no_topics experiment — delete. (3) Confirm tool_loop.py's final answer text actually contained 189.50 (round trip end-to-end) — not yet pasted.
Next up: Day 27 — quiz on Day 26 + cold pick, then multi-tool + error handling in the loop: what to send back when a tool RAISES (tool_result with is_error), letting the model recover, and validating tool input (schema is a request, not a guarantee). Bridges toward Phase 3 agents.
RECALL QUESTIONS FOR TOMORROW (answer before the session)
1. Why is the tool loop `while True` instead of a fixed two calls?
2. Tool results go back with which role, and why does that fit "messages list = conversation store you own"?
3. RAG vs tool use — who decides what data gets fetched, in each?
ONE-SENTENCE SUMMARY (say out loud)
"Tool use is a loop I own: I declare tools like an OpenAPI spec, the model stops with stop_reason='tool_use' when it needs one, my code dispatches by name, returns results by correlation ID, and we go around until it answers."
KEY MENTAL MODELS (carry into every session)
Tool loop = while stop_reason == "tool_use" — round-trip count unknown in advance; stop_reason steers control flow, not just logs
Tool schema = OpenAPI spec for internal functions; description field is prompt engineering — vague or inverted description = wrong/skipped calls
input_schema and Pydantic are the same JSON Schema idea in opposite directions: schema = what I accept, Pydantic = validate what the model sent
Schema is a request, not a guarantee — tool functions validate their input; model output = untrusted input even mid-tool-call
tool_use_id = correlation ID (Kafka reply-key) — one turn can request multiple tools; the ID pairs each result to its call
Dispatch dict TOOL_FUNCTIONS[block.name] = event loop with dynamic dispatch, made literal
Tool results return as role="user" — the conversation store you own carries the round trip; the transcript is GROWN by the loop, never hand-written
Dependency chain between tools = sequential turns; independent needs = parallel calls in one turn
RAG = push (my code decides context up front); tool use = pull (model decides mid-conversation); agents = the tool loop + a bigger catalog
Say the function signature out loud, then transcribe to schema — the schema should never contain a word the signature doesn't
Pipeline returns a DTO, not a tuple — callers read names, new fields break nobody (tuple arity breaks everyone)
A function's return type is a promise made by EVERY branch — and the violation crashes in the CALLER, only when the rarer branch fires (bug location ≠ crash location)
Same type is not the same contract — branches must populate the same FIELDS too, or the object lies about itself
Sentinel strings across module boundaries are silent-failure bugs — producer declares state in a field; consumers never parse prose
An assertion that breaks loudly when the contract changes is a gift; one that silently tolerates it is the bug that reaches production
Verify your own fixes with the skepticism you apply to your bugs — grep the file, don't trust the memory of editing it
Design the response object against every consumer, not the loudest one (RAGAS needs chunk text)
Identical output after a refactor proves nothing; callers running without TypeError proves it
Schema = API contract for model output — constraints + Optional (legitimate absence) + nesting (whole tree, one call)
Optional allows null; only = None default allows ABSENCE — both parts, or the key is still required
Required-by-default (NOT NULL) — optional fields just move the failure downstream
Expected traceback = passing test — ask "did I expect this?" before "what broke?"
To test absence, feed absence — a happy-path run proves nothing about the missing-field case
Nested validation errors give the full path (sources.1.score) — RAG responses are trees
When a fix replaces a line, delete the old line in the same edit — last write silently wins
Model output = untrusted input; validate at the boundary — Pydantic model_validate_json fails loud
Prompt instructions are requests, not guarantees — prefill "{" forces mid-JSON continuation; re-attach before parsing
Schema enforcement lives in YOUR code at runtime — the API returns text, nothing more
Messages list = conversation store you own; API = stateless REST (JWT, not server session)
System prompt = request header, not body — re-sent every call, never in messages
Long conversations = cache with no eviction; sliding window trims in pairs, must start with user role
Odd-length list + even slice = wrong role — re-check structural invariants AFTER slicing (current API accepts assistant-first; role-check is hygiene)
Falsify hypotheses with printed numbers — INCLUDING the teacher's
Trimming bug = amnesia, not garbage-in
Send-trim caps API cost; store-trim caps RAM — know which one you fixed
stop_reason arrives in message_delta at the END when streaming; on every response otherwise — new value "tool_use" = control-flow signal
Streaming = SSE/chunked transfer; text_stream = filtered consumer, raw events = the full topic
stop_reason = HTTP status code of the stream — never render it, never ignore it
asyncio.gather = Promise.all; asyncio.run starts the loop yourself
Client class must match function style: Async client → async def/async with/async for
Display truncation vs API truncation — printed evidence decides
Prefill = parallel, sets TTFT; decode = sequential, sets streaming speed
Metric triad = pipeline stages: context_precision→retrieval, faithfulness→grounding, answer_relevancy→direction
Refused questions never reach the judge — refusal_rate and n catch what quality metrics miss
Coverage-risk flag means "can't ground this" — human interprets
Judge metrics are non-deterministic — trends and comparisons, never single absolutes
Reference = expected value of a unit test
collection.query = local vector DB (free); the LLM call is the guarded one
Retriever = bouncer (per-chunk threshold), service = manager (empty → refuse)
Python indentation = "how many times does this line run"
KeyError points at the crash line, but the bug lives where the dict was built
Refusals have three layers: empty filter → distance gate → LLM refusal prompt; check in order, with evidence
A correct refusal that surprises you = coverage gap; fix is data, not code
Corpus changes need regression evals, same as code changes
One pipeline, many importers: prod, deterministic evals, RAGAS all import rag_service
Python tuple unpacking is strict: change a return arity → update every caller
Faithfulness = grounding, not truth; correct refusals score 0 — exclude them
Deterministic evals = unit tests (free, every change); RAGAS = load tests (costs money)
Thresholds are outputs of calibration experiments, not guesses
DBs return "closest," not "relevant" — thresholds are application code's job
Knowledge gap → RAG; behavior gap → prompting first, fine-tuning last
site-packages-only traceback = dependency conflict, not your code; venv = node_modules
PROGRESS LOG (most recent first — headline only)
Day 26: Tool use in production — the while-True loop (stop_reason="tool_use" as control flow), tool schemas as OpenAPI specs (description = prompt engineering), dispatch dict + tool_use_id correlation, RAG=push vs tools=pull, agents = loop + catalog; tool_loop.py VERIFIED (tool_use → tool_use → end_turn, sequential dependency chain); warm-up verified Day-25 fixes (evals 5/5, debug_floor healthy); COLD Q Optional/= None PASSED after two failures
Day 25: Typed pipeline responses — answer_question returns RagResponse (nested list[Source]) not a 3-tuple, both branches same contract, 3 callers updated to read by name; Source.text miss caught by checking the third caller; debug_floor.py audit restored + retrieval verified healthy; quiz: SSE roles + stop_reason CLOSED, Optional/= None failed twice
Day 24 (complete): Pydantic deep dive — Field constraints, Optional + = None, nested models; "test absence by feeding absence"; stop_reason say-back closed attempt 6
Day 24 (partial): Structured outputs + Pydantic — boundary validation, both ValidationError modes live, prefill fix; trim experiment FALSIFIED the 400 claim
Day 23: Multi-turn state + system prompts — messages list = conversation store, sliding-window trim in pairs; latent odd/even trim bug found + fixed
Day 22: PHASE 2 START — streaming (SSE, stop_reason) + async (gather = Promise.all); sync/async client-mixing bug caught live
Day 21: Retrieval audit loop + RAGAS triad + sabotage test. PHASE 1 COMPLETE.
Day 20: Floor-plan finding closed — three-layer refusal debugging, doc6 added, evals 5/5
Day 19: Double-retrieval refactor — (answer, sources, chunks), 3 callers
Day 18: RAGAS faithfulness on Project 2 — judge LLM, refusal distortion found
Day 17: Phase 1 capstone + Project 2 v1 shipped — RAG API end-to-end, evals 5/5
Day 16: Inference in production — prefill/decode, TTFT
Day 15: Fine-tuning vs RAG vs prompting — knowledge gap vs behavior gap
Day 14: Model comparison — spec-sheet selection
Day 13: Hallucinations — softmax has no "I don't know"
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
