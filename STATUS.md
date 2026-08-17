STATUS.md — Tushar's AI Learning (SINGLE SOURCE OF TRUTH)

Last Updated: 2026-08-17

RULE FOR CLAUDE: This file's "CURRENT STATUS" section overrides ALL other documents in this project. If any other doc conflicts, this file wins.

DOC PROTOCOL (agreed 2026-08-10): ONE SESSION = ONE DAY NUMBER, sequential, no exceptions. Never reopen a day as "partial", "complete" or "check-in" — if a topic spans two sessions, the second session gets the next number and the heading says "(cont.)". LEARNING_NOTES.md headings are always `## Day N — Topic Name` (no dates, no qualifiers). At the end of EVERY session, update all three: LEARNING_NOTES.md (one new Day block), STATUS.md (this file), MEMORY.md (curriculum line + open items), then commit.

REVISION PROTOCOL (agreed 2026-08-10): every session's quiz is 3 questions on the LAST day PLUS 1 cold question drawn from a RANDOM earlier day (rotate through Days 0–27; prioritise anything on the weak-spots line). Log the rotation pick in the day's notes. Rotation picks so far: Day 24 (2026-08-11, PASSED), Day 20 (2026-08-14, FAILED), Day 20 RE-ASK (2026-08-17, layers PASSED / first-print still missed — re-ask first-print ~2026-08-20).

REVISION WEEK (agreed 2026-08-17): when Phase 2 completes, insert ONE FULL WEEK of Phase 1 + Phase 2 revision BEFORE Phase 3 starts. No new content that week — cold recall drills across Days 0–end-of-Phase-2, weak-spots list as the syllabus, out-loud plain-English recaps as the primary exercise. This directly targets the recall-lags-application gap.

MILESTONES (set 2026-08-10, revised 2026-08-17 — recalibrate at each phase end)
Sep 2026: Phase 2 complete — tool use/function calling, LangChain or LlamaIndex, Project 2 hardened (real Autodesk chunks, model cost decision, ragas upgrade)
Sep/Oct 2026: REVISION WEEK — full Phase 1 + 2 revision (new, agreed 2026-08-17)
Nov 2026: Phase 3 complete — LangGraph, agent loops, memory, multi-agent, MCP, LangSmith, guardrails
Dec 2026: Projects 3 and 4 shipped — portfolio complete (4/4)
Feb 2027: job search opens — resume refresh, AI system design interview prep
Jul 2027: Walmart Staff/Principal AI Engineer target — ~5 months of buffer

CURRENT STATUS
Day: 28 COMPLETE | Week: 6 — Phase 2 | Next session = Day 29
Goal: Staff SWE → AI Backend Engineer (Autodesk) → Staff/Principal AI Engineer, Walmart, July 2027
Just completed: Day 28 (2026-08-17) — max-iteration guards: what turns a tool loop into an agent. An agent = tool loop + iteration ceiling + bigger catalog + multi-step goal. `for iteration in range(MAX_ITERATIONS)` replaces `while True`; the MODEL still decides when it's done (stop_reason != "tool_use"), but I decide the most it can spend deciding. When the budget dies, give_up() makes a FORCED LANDING — one final call with tools disabled so the model must answer in text from what it already collected — instead of a crash. Node anchor: while True over a paid API = a consumer with no max.poll limit and no circuit breaker. Key nuance: the ceiling is a BACKSTOP, not a fix — with the Day 27 sentinel bug it still burns 10 paid calls; error-message quality is the fix; they are layers (circuit breaker + error contract).
Exercise VERIFIED (pasted output, both paths): agent_loop.py created (tool_loop.py preserved as reference), loop renamed run_agent. Sabotage run: MAX_ITERATIONS=1 + two-tool question → BOTH tools ran in ONE iteration (independent args → parallel calls in one turn, Day 26 rule seen live), guard fired, give_up() landed with useful text including $189.50 and an honest "ran out of tool-call attempts". Restored MAX_ITERATIONS=10 and re-ran: normal exit, clean end_turn, price in final text. Lesson re-learned live: his first run only proved the Day 27 error-message fix — the guard never executed; to test the ceiling, HIT the ceiling.
Quiz results (Day 27 + cold Day 20 re-ask): Q1 protocol rule PASS. Q2 try placement PARTIAL — location right, sibling-tools failure mode not retrieved even on retry. Q3 sentinel mechanics FAILED — pasted the correct fix but could not say WHY is_error never fired (no raise → except never runs → field stays False). Q4 Day 20 RE-ASK: three layers PASSED in order (empty WHERE filter → distance gate → LLM refusal) — real progress on a cold fail — but the first print (raw collection.query COUNT) missed again. Also: dodged the in-session check question three times, answering with runs instead of sentences.
Project 1 status: SHIPPED; multi_turn_chat.py (Day 23, trim fix)
Project 2 status: RAGAS triad complete + sabotage-tested; typed RagResponse end-to-end. Remaining: real Autodesk doc chunks, model cost decision, ragas upgrade to remove vertexai stub, run ragas_evals.py once against typed pipeline (costs money — not yet re-run).
Currently strong on: testing the failure path once told which path to test — designed and ran the MAX_ITERATIONS=1 sabotage correctly first try, and read the parallel-tool-call behavior out of the output himself.
Weak spots from quiz (revisit):
 (1) SENTENCES vs RUNS — NEW. Answered the check question three times with pasted terminal output instead of the one-sentence answer. A run is evidence, not an explanation. The out-loud recap and the revision week are the interventions.
 (2) Sentinel mechanics (Day 27 Q3) — can fix it, cannot explain it: no raise → except never runs → is_error stays False. Re-ask ~2026-08-20.
 (3) Sibling-tools failure mode (Day 27 Q2) — try around the loop kills innocent siblings' tool_results → unanswered tool_use_id → request rejected. Re-ask ~2026-08-20.
 (4) Day 20 first print — raw collection.query COUNT before any distances (layers now PASS; only this fragment owed). Re-ask ~2026-08-20.
 (5) ADJACENT VOCABULARY (from Day 27) — improved this session (Q4 layers were the right mechanisms, not RAGAS metrics) but keep the drill: name the MOMENT IN TIME the question is about.
 (6) DIRECTION INVERSIONS — agent_loop.py likely inherited tool_loop.py's inverted line-22 description via the copy; fix owed.
 (7) Optional vs = None — one more cold check owed ~2026-08-18 (due now — use as Day 29's cold pick alongside nothing else).
 (8) Trim-experiment finding + prefill re-attach — still not re-tested, carry.
CARRIED FORWARD: (1) Phase 1 recap out loud (owed since 2026-08-08 — will fold into REVISION WEEK if still open, but attempt sooner). (2) get_company_name description inversion — now in BOTH tool_loop.py and agent_loop.py; fix in both. (3) Day 27 ValidationError sabotage = Day 29 take-home: force block.input = {"ticker": ["AAPL"]} in agent_loop.py, prove the ValidationError branch fires (is_error + validation message, not TypeError crash). (4) Per-tool Pydantic models keyed by block.name — StockPriceInput still validates BOTH tools. CLOSED this session: AAPL final text confirmed containing 189.50 (twice — forced landing and normal exit).
Next up: Day 29 — quiz on Day 28 + cold pick (Optional vs = None, due 2026-08-18), verify the ValidationError take-home, then multi-step planning: giving the agent a goal that REQUIRES sequencing tools across turns (dependency chains it must discover itself) and how it decides it is done — the last conceptual bridge before LangChain/LangGraph territory.
RECALL QUESTIONS FOR TOMORROW (answer in SENTENCES, not runs)
1. Day 27 spiral, sentinel bug still in place, MAX_ITERATIONS = 10: what happens, what does the user see, and what did it cost?
2. In the sabotage test, why did BOTH tools run in a single iteration?
3. Why does give_up() make its final call with tools disabled?
ONE-SENTENCE SUMMARY (say out loud)
"An agent is a tool loop with a budget: the model decides when it's done, I decide the most it can spend deciding, and when the budget runs out it makes a forced landing in text instead of crashing."
KEY MENTAL MODELS (carry into every session)
The ceiling is a backstop, not a fix — the guard caps the damage of a bad error message; error quality is the fix; they are layers (circuit breaker + error contract)
for iteration in range(MAX_ITERATIONS) replaces while True — same loop, with a budget; two exits, two deciders (model: stop_reason; me: range exhausted)
give_up() = forced landing — final call with tools DISABLED so the model must answer in text from what it already has; crash and silent partial transcript are the alternatives you reject
To test the ceiling, hit the ceiling — a happy-path run proves the OLD fix, not the new guard
A run is evidence, not an explanation — the check question wants a sentence
Agent = tool loop + iteration budget + bigger catalog + multi-step goal — no magic
Every tool_use block MUST be answered — an unanswered correlation ID is a rejected request, not a silent no-op; this is WHY errors are data
is_error is a FIELD, not an exception — the error result has the identical shape to a success
try wraps the SINGLE tool call, not the loop — one failure must not take down sibling tools in the same turn
except ValidationError BEFORE except Exception — the subclass gets swallowed otherwise
The error message is prompt engineering — actionable text ends the conversation cleanly; every model guess is a paid API call
A function that CANNOT fail (.get with a default) cannot report failure — no raise → except never runs → is_error stays False
Model output = untrusted input; YOUR internals = untrusted output — no raw tracebacks into the context window
block.input is a request body — validate with Pydantic at the boundary; `**` splat of a dict you didn't build TypeErrors before the function body runs
When you see `**x`, say "x must be a dict" — a dotted expression naming one field is a value, not a mapping
An unbounded while True over a paid API is a production incident — iteration ceilings are not optional
Answer the MOMENT IN TIME the question asks about — adjacent vocabulary from the right neighbourhood is still a wrong answer
Tool loop = while stop_reason == "tool_use" — stop_reason steers control flow, not just logs
Tool schema = OpenAPI spec for internal functions; description field is prompt engineering — vague or inverted description = wrong/skipped calls
input_schema and Pydantic are the same JSON Schema idea in opposite directions: schema = what I accept, Pydantic = validate what the model sent
Schema is a request, not a guarantee — tool functions still validate their input
tool_use_id = correlation ID (Kafka reply-key) — one turn can request multiple tools; the ID pairs each result to its call
Dispatch dict TOOL_FUNCTIONS[block.name] = event loop with dynamic dispatch, made literal
Tool results return as role="user" — the transcript is GROWN by the loop, never hand-written
Dependency chain between tools = sequential turns; independent needs = parallel calls in one turn (seen live on Day 28)
RAG = PUSH (my code decides context up front); tool use = PULL (model decides mid-conversation); agents = the tool loop + a bigger catalog
Say the function signature out loud, then transcribe to schema — the schema should never contain a word the signature doesn't
Pipeline returns a DTO, not a tuple — callers read names, new fields break nobody (tuple arity breaks everyone)
A function's return type is a promise made by EVERY branch — the violation crashes in the CALLER, only when the rarer branch fires
Same type is not the same contract — branches must populate the same FIELDS too
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
Prompt instructions are requests, not guarantees — prefill "{" forces mid-JSON continuation; re-attach before parsing
Schema enforcement lives in YOUR code at runtime — the API returns text, nothing more
Messages list = conversation store you own; API = stateless REST (JWT, not server session)
System prompt = request header, not body — re-sent every call, never in messages
Long conversations = cache with no eviction; sliding window trims in pairs, must start with user role
Odd-length list + even slice = wrong role — re-check structural invariants AFTER slicing
Falsify hypotheses with printed numbers — INCLUDING the teacher's
Trimming bug = amnesia, not garbage-in
Send-trim caps API cost; store-trim caps RAM — know which one you fixed
stop_reason arrives in message_delta at the END when streaming; on every response otherwise — value "tool_use" = control-flow signal
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
Refusals have three layers: empty filter → distance gate → LLM refusal prompt; check IN ORDER, cheapest first — the raw query COUNT before any distance
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
Day 28: Max-iteration guards — agent = tool loop + budget; for range(MAX_ITERATIONS) replaces while True, give_up() = forced landing with tools disabled; sabotage run VERIFIED (MAX_ITERATIONS=1 → both tools in ONE iteration via parallel calls, guard fired, landing landed with $189.50); "ceiling = backstop, error quality = fix"; Day 20 re-ask layers PASSED (first-print still owed); new pattern named: answers with runs instead of sentences; REVISION WEEK after Phase 2 agreed
Day 27: Tool errors + input validation — errors as DATA (is_error field), try around the single call, except ordering, error string as prompt engineering, Pydantic on block.input; SENTINEL-STRING bug found live and A/B'd; unbounded while True flagged
Day 26: Tool use in production — the while-True loop, tool schemas as OpenAPI specs, dispatch dict + tool_use_id correlation, RAG=push vs tools=pull
Day 25: Typed pipeline responses — RagResponse DTO, both branches same contract, 3 callers read by name
Day 24 (complete): Pydantic deep dive — Field constraints, Optional + = None, nested models
Day 24 (partial): Structured outputs + Pydantic — boundary validation, prefill fix
Day 23: Multi-turn state + system prompts — sliding-window trim in pairs; odd/even trim bug fixed
Day 22: PHASE 2 START — streaming (SSE, stop_reason) + async (gather = Promise.all)
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
