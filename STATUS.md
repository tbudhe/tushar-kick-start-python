STATUS.md — Tushar's AI Learning (SINGLE SOURCE OF TRUTH)

Last Updated: 2026-08-14

RULE FOR CLAUDE: This file's "CURRENT STATUS" section overrides ALL other documents in this project. If any other doc conflicts, this file wins.

DOC PROTOCOL (agreed 2026-08-10): ONE SESSION = ONE DAY NUMBER, sequential, no exceptions. Never reopen a day as "partial", "complete" or "check-in" — if a topic spans two sessions, the second session gets the next number and the heading says "(cont.)". LEARNING_NOTES.md headings are always `## Day N — Topic Name` (no dates, no qualifiers). At the end of EVERY session, update all three: LEARNING_NOTES.md (one new Day block), STATUS.md (this file), MEMORY.md (curriculum line + open items), then commit.

REVISION PROTOCOL (agreed 2026-08-10): every session's quiz is 3 questions on the LAST day PLUS 1 cold question drawn from a RANDOM earlier day (rotate through Days 0–26; prioritise anything on the weak-spots line). Log the rotation pick in the day's notes. Rotation picks so far: Day 24 (2026-08-11, PASSED), Day 20 (2026-08-14, FAILED — re-ask ~2026-08-21).

MILESTONES (set 2026-08-10, 11 months to target — recalibrate at each phase end)
Sep 2026: Phase 2 complete — tool use/function calling, LangChain or LlamaIndex, Project 2 hardened (real Autodesk chunks, model cost decision, ragas upgrade)
Nov 2026: Phase 3 complete — LangGraph, agent loops, memory, multi-agent, MCP, LangSmith, guardrails
Dec 2026: Projects 3 and 4 shipped — portfolio complete (4/4)
Feb 2027: job search opens — resume refresh, AI system design interview prep
Jul 2027: Walmart Staff/Principal AI Engineer target — ~5 months of buffer

CURRENT STATUS
Day: 27 COMPLETE | Week: 5 — Phase 2 | Next session = Day 28
Goal: Staff SWE → AI Backend Engineer (Autodesk) → Staff/Principal AI Engineer, Walmart, July 2027
Just completed: Day 27 (2026-08-14) — tool errors + input validation in the loop. One idea, two faces: a tool that RAISES and a tool called with BAD ARGUMENTS both end as a tool_result with is_error: True. (1) Letting the exception escape kills the conversation — the model is a caller mid-turn who could have recovered (Node: unhandled rejection crashing the process vs. returning {ok:false} to a caller who can degrade). (2) The error result has the IDENTICAL shape to a success — same tool_use_id, is_error is a FIELD not an exception. (3) try wraps the SINGLE call, not the loop, or one failure takes down sibling tools in the same turn. (4) The error string is prompt engineering — actionable text changes what the model does next; NEVER a raw traceback (internals = untrusted OUTPUT, mirror of model output = untrusted input). (5) block.input is a request body — `**` splat of a dict I didn't build TypeErrors before the function body runs; Pydantic at the boundary turns bad input into a conversation. (6) THE PROTOCOL RULE — every tool_use block must be answered or the request is rejected, which is WHY errors must be data: there is no skip branch. (7) except ValidationError BEFORE except Exception, or the subclass gets swallowed.
Headline finding (his own, from printed evidence): the SENTINEL STRING bug, live. get_company_name used NAMES.get(ticker, "unknown ticker"), which cannot fail, so failures shipped as content='unknown ticker' with is_error=False — the model was told "success, the answer is the phrase 'unknown ticker'" and started guessing tickers (GOOGL → GOOG → still going when the crash stopped it). After switching to raise + is_error: True + "known: ['AAPL','MSFT']": ONE call, clean end_turn, model told the user which companies are available and offered alternatives. Same model, same question, one variable — error-message quality measured in API calls. This is Day 25's own rule ("producer declares state in a field; consumers never parse prose") violated three weeks after writing it down, then proven by A/B.
Quiz results (Day 26 material + cold Day 20): 1 partial, 3 WRONG on first pass — weakest quiz in several sessions. Q1 while True: partial, PASSED on retry ("runtime, dependency on previous results"). Q2 tool_result role + tool_use_id: FAILED — answered with stop_reason, i.e. the loop EXIT moment instead of the result-RETURN moment. Q3 RAG/tool-use push vs pull: FAILED, INVERTED. Q4 COLD Day 20 refusal layers: FAILED — named RAGAS metrics instead of pipeline mechanisms; the retry on "first thing you print" was also wrong order (jumped to distances instead of the raw collection.query count).
Project 1 status: SHIPPED; multi_turn_chat.py (Day 23, trim fix)
Project 2 status: RAGAS triad complete + sabotage-tested; typed RagResponse end-to-end, review fixes verified 2026-08-11. Remaining: real Autodesk doc chunks, model cost decision, ragas upgrade to remove vertexai stub, run ragas_evals.py once against typed pipeline (costs money — not yet re-run).
Currently strong on: debugging with printed evidence — read two runs side by side and extracted the causal variable unprompted; took a hard grading without deflating and landed both retries.
Weak spots from quiz (revisit):
 (1) ADJACENT VOCABULARY — NEW, and the headline issue. Every wrong answer used real terms from the correct neighbourhood (TOOL_FUNCTIONS, stop_reason, RAGAS metric names). Drill: before answering, name the MOMENT IN TIME the question is about.
 (2) DIRECTION INVERSIONS — fifth occurrence (name vs ticker, in vs out, push vs pull, and tool_loop.py line 22 still inverted at session end). Rule stands: say the signature or flow out loud, then transcribe.
 (3) Day 20 three-layer refusal debugging — FAILED COLD. Re-ask ~2026-08-21. Must say: empty filter → distance gate → LLM refusal prompt, and the FIRST print is the raw collection.query COUNT.
 (4) Optional vs = None — passed 2026-08-11 after two failures; one more cold check still owed ~2026-08-18.
 (5) Trim-experiment finding + prefill re-attach — still not re-tested, carry.
 (6) Recall lags application — he rebuilds concepts correctly at the keyboard but cannot retrieve them cold. The out-loud recap is the intervention.
EXERCISE (mostly verified 2026-08-14 with pasted output): tool_loop.py — added get_stock_price_strict raising ValueError, get_company_name switched from sentinel string to raise, second except Exception branch added. VERIFIED: is_error: True in the transcript with an actionable message, stop_reason tool_use → end_turn, final assistant text printed and graceful. NOT DONE: the sabotage step (force block.input = {"ticker": ["AAPL"]} to prove the ValidationError branch fires instead of a TypeError crash).
CARRIED FORWARD: (1) Phase 1 recap — explain embeddings → RAG → prompting → evals out loud, plain English (owed since weekend of 2026-08-08; now 6 days overdue and directly relevant to the recall problem). (2) tool_loop.py line 22 description still inverted — fix. (3) Sabotage/ValidationError step of the Day 27 exercise. (4) Confirm the AAPL run's FINAL assistant text contains 189.50 — the Google run printed final text, the Apple run never did. (5) StockPriceInput is validating input for BOTH tools; per-tool models keyed by block.name when a tool takes different arguments. CLOSED this session: structured_output.py lines 33–34 deleted.
Next up: Day 28 — quiz on Day 27 + cold pick (Day 20 RE-ASK), then the bridge into Phase 3: what turns a tool loop into an AGENT — max-iteration guards (the unbounded while True over a paid API is a production incident, seen live on Day 27), multi-step planning, and how an agent decides it is done.
RECALL QUESTIONS FOR TOMORROW (answer before the session)
1. Why can't you just skip sending a tool_result when a tool fails?
2. Where does the try go — around the loop or around the single tool call — and what breaks if you get it wrong?
3. input_schema vs the Pydantic model in your handler: which direction does each one point?
ONE-SENTENCE SUMMARY (say out loud)
"A failed tool is still a tool result — every tool_use_id must be answered, so errors go back as data with is_error: True, and the model gets to recover instead of my process crashing."
KEY MENTAL MODELS (carry into every session)
Every tool_use block MUST be answered — an unanswered correlation ID is a rejected request, not a silent no-op; this is WHY errors are data
is_error is a FIELD, not an exception — the error result has the identical shape to a success
try wraps the SINGLE tool call, not the loop — one failure must not take down sibling tools in the same turn
except ValidationError BEFORE except Exception — the subclass gets swallowed otherwise, and "bad arguments" and "tool blew up" stop being distinguishable
The error message is prompt engineering — actionable text ends the conversation cleanly; a vague one makes the model guess, and every guess is a paid API call
A function that CANNOT fail (.get with a default) cannot report failure — sentinel strings ship as is_error: False and the model treats them as answers
Model output = untrusted input; YOUR internals = untrusted output — the boundary cuts both ways, so no raw tracebacks into the context window
block.input is a request body — `**` splat of a dict you didn't build TypeErrors before the function body runs; validate with Pydantic at the boundary
When you see `**x`, say "x must be a dict" — a dotted expression naming one field is a value, not a mapping
An unbounded while True over a paid API is a production incident — iteration ceilings are not optional
Answer the MOMENT IN TIME the question asks about — adjacent vocabulary from the right neighbourhood is still a wrong answer
Tool loop = while stop_reason == "tool_use" — round-trip count unknown in advance; stop_reason steers control flow, not just logs
Tool schema = OpenAPI spec for internal functions; description field is prompt engineering — vague or inverted description = wrong/skipped calls
input_schema and Pydantic are the same JSON Schema idea in opposite directions: schema = what I accept, Pydantic = validate what the model sent
Schema is a request, not a guarantee — tool functions still validate their input
tool_use_id = correlation ID (Kafka reply-key) — one turn can request multiple tools; the ID pairs each result to its call
Dispatch dict TOOL_FUNCTIONS[block.name] = event loop with dynamic dispatch, made literal
Tool results return as role="user" — the conversation store you own carries the round trip; the transcript is GROWN by the loop, never hand-written
Dependency chain between tools = sequential turns; independent needs = parallel calls in one turn
RAG = PUSH (my code decides context up front, before the model sees the question); tool use = PULL (model decides mid-conversation); agents = the tool loop + a bigger catalog
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
Day 27: Tool errors + input validation — errors as DATA (is_error field, identical result shape), try around the single call not the loop, except ordering, error string as prompt engineering, no raw tracebacks, Pydantic on block.input, and the protocol rule that every tool_use must be answered (hence no skip branch); SENTINEL-STRING bug found live and A/B'd — sentinel → 3 iterations of model guessing, raise + is_error → 1 call and a clean end_turn; unbounded while True flagged as a production incident (Day 28 hook); quiz was the weakest in weeks (3 wrong incl. inverted push/pull and a failed cold Day 20)
Day 26: Tool use in production — the while-True loop (stop_reason="tool_use" as control flow), tool schemas as OpenAPI specs (description = prompt engineering), dispatch dict + tool_use_id correlation, RAG=push vs tools=pull, agents = loop + catalog; tool_loop.py VERIFIED; COLD Q Optional/= None PASSED after two failures
Day 25: Typed pipeline responses — answer_question returns RagResponse (nested list[Source]) not a 3-tuple, both branches same contract, 3 callers updated to read by name; debug_floor.py audit restored
Day 24 (complete): Pydantic deep dive — Field constraints, Optional + = None, nested models; "test absence by feeding absence"
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
