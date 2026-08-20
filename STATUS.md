STATUS.md — Tushar's AI Learning (SINGLE SOURCE OF TRUTH)

Last Updated: 2026-08-20

RULE FOR CLAUDE: "CURRENT STATUS" here overrides ALL other documents. If any doc conflicts, this file wins.

PROTOCOLS (condensed — full history in LEARNING_NOTES.md)
- DOC (2026-08-10): one session = one day number, sequential. Session end: update LEARNING_NOTES.md (one Day block), STATUS.md, MEMORY.md, then commit.
- QUIZ (revised 2026-08-20 — Tushar's request): MAX 5 QUESTIONS PER SESSION, TOTAL. Default shape: 2 on the last day + 1 cold rotation pick (Days 0–current, prioritise weak spots) + up to 2 follow-ups. Log the rotation pick. Answers in SENTENCES first; a run or code block is evidence, not an answer.
- COACHING (2026-08-18, verified working 2026-08-20): before EVERY exercise — (1) GOAL first: show the exact final printout; (2) numbered step list; (3) ONE step at a time, confirm before the next.
- REVISION WEEK (2026-08-17): when Phase 2 completes, one full week of Phase 1+2 revision before Phase 3. No new content; weak-spots list is the syllabus.

MILESTONES (recalibrate at each phase end)
Sep 2026: Phase 2 complete (tool use, LangChain/LlamaIndex, Project 2 hardened) → REVISION WEEK → Nov 2026: Phase 3 complete (LangGraph, agents, MCP, LangSmith) → Dec 2026: Projects 3+4 shipped → Feb 2027: job search opens → Jul 2027: Walmart Staff/Principal AI Engineer.

CURRENT STATUS
Day: 30 COMPLETE | Week: 6 — Phase 2 | Next session = Day 31 (decide at start: LangChain intro — map the hand-built loop onto framework abstractions — or Project 2 hardening)
Goal: Staff SWE → AI Backend Engineer (Autodesk) → Staff/Principal AI Engineer, Walmart, July 2027
Just completed: Day 30 (2026-08-20) — Multi-Step Planning (cont.). THE CHAIN RAN — goal printout matched exactly: iteration 0 get_ticker_symbol("YUNextGenAI")→YNXT; iteration 1 get_stock_price("YNXT")→42.0; iteration 2 "$42.00". MAX_ITERATIONS ≥ N+1 verified live (2 links + landing = 3). The planted landmine fired (StockPriceInput validating every tool rejected the lookup tool's valid input) and was fixed with INPUT_MODELS — per-tool Pydantic models keyed by block.name, the FOURTH registry. Key new lesson: the WRONG validator's error message actively steered the model wrong (after "ticker Field required" ×2 it stuffed the company name into get_stock_price) — error text is prompt engineering even when the error is your bug. Bonus self-found bug: hardcoded `if ticker != "AAPL"` allowlist in get_stock_price → replaced with PRICES membership check + known-tickers error message.
Exercise status: COMPLETED AND VERIFIED — printout matched line for line. Full code samples in LEARNING_NOTES.md Day 30.
Quiz results (Day 29 + cold Day 20): Q1 chain-vs-parallel PASSED (after one push). Q2 three-registrations FAILED cold, relearned by hands; end-of-day re-ask still swapped function for validator — re-ask cold. Q3 Pydantic-vs-TypeError tell PARTIAL (code instead of the "specificity" sentence). Q4 COLD Day 20 PARTIAL — layer right again, count-print missed a THIRD time.
Project 1: SHIPPED. Project 2: RAGAS triad + typed RagResponse done; remaining: real Autodesk chunks, model cost decision, ragas upgrade, one paid ragas_evals.py run.
Currently strong on: ran the full diagnosis loop solo (retry→print→read→fix boundary); found the allowlist bug unprompted; direction arrows said right all day (real progress on inversions).

WEAK SPOTS (revisit)
1. SENTENCES vs CODE — worst day yet (≥4 code-instead-of-sentence answers 08-20). Demand the sentence first, patiently; code is not an answer to "why".
2. give_up()-tools-disabled WHY (Day 28) — re-ask DUE next session.
3. Sentinel mechanics (Day 27): no raise → except never runs → is_error stays False — re-ask due.
4. Sibling-tools failure mode (Day 27): try around the loop kills innocent siblings' tool_results — re-ask due.
5. Day 20 first print — THIRD miss on count-print (layer solid). Drill as one breath: "layer = filter, print = count." Re-ask ~08-24.
6. THREE REGISTRATIONS — schema (TOOLS), function, dispatch (TOOL_FUNCTIONS); + fourth registry INPUT_MODELS. Re-ask cold.
7. DIRECTION INVERSIONS — progress 08-20; one more clean session then consider closed.
CLOSED 2026-08-20: Day 29 exercise; per-tool Pydantic models (since Day 27); delete get_company_minimum_stock_price; hardcoded AAPL allowlist.

CARRIED FORWARD
(1) Phase 1 recap out loud (owed since 08-08; folds into REVISION WEEK). (2) tool_loop.py line-22 description inversion. (3) Trim-experiment + prefill re-attach re-test.

NEXT SESSION (Day 31) — QUIZ PLAN (max 5)
Q1. The wrong validator produced a well-formed, actionable error — and made things WORSE. What did the model do with "ticker Field required", and what does that teach about error text?
Q2. Name the three registrations AND the fourth registry; which does the model see vs the loop use?
Q3 (cold re-ask). Why does give_up() disable tools — the WHY, not the where?
(+ up to 2 follow-ups; sentinel mechanics and sibling-tools queue behind these.)

ONE-SENTENCE SUMMARY (say out loud)
"The chain ran because the catalog described both directions and each tool had its own contract — two links cost two iterations plus a landing, and every error message in the loop is prompt engineering, even the ones produced by my own bugs."

ACTIVE MENTAL MODELS (top of mind — full running list archived in LEARNING_NOTES.md)
- Dependency chain = B's argument IS A's output; all arguments in a turn are written BEFORE any tool runs → each link costs one iteration; N links need MAX_ITERATIONS ≥ N+1
- World knowledge is a chain bypass — models guess internal IDs they think they know
- A tool needs THREE registrations (TOOLS schema, function, dispatch) + a fourth in a hardened loop (INPUT_MODELS validator) — all keyed by the same name; data alone is invisible to the model
- Two lookup directions = two tools; say the arrow out loud: "X in, Y out"; one dict, one contract
- Per-tool validators dispatch like functions — one shared model is only legal when contracts truly match
- A wrong validator's error steers the model wrong — the model OBEYS error text; actionable+specific+WRONG is worse than vague
- A model retrying the same call means its tool_result was an error — retries are a diagnostic signal
- A hardcoded literal beside a lookup dict is an allowlist bug — data must be the authority
- Pydantic errors name the CONTRACT (schema/field/type tag); TypeErrors name Python internals — specificity is the tell (400 vs 500)
- give_up() = forced landing: tools disabled → only end_turn remains; ceiling = backstop, error quality = fix
- Every tool_use block must be answered; is_error is a FIELD; try wraps the SINGLE call, not the loop
- A run is evidence, not an explanation — the check question wants a sentence
- Refusal debugging: layer = filter, print = COUNT (raw collection.query count before any distances)

PROGRESS LOG (most recent first — headline only)
Day 30: Multi-step planning FINISHED — chain ran (YNXT→42.0→"$42.00"); INPUT_MODELS fourth registry closed the landmine; wrong-validator error steered the model wrong; self-found AAPL allowlist bug; quiz cap set at 5/day
Day 29: Multi-step planning STARTED — chain concept, world-knowledge bypass, two directions = two tools, three registrations; coaching rule created
Day 28: Max-iteration guards — for range(MAX_ITERATIONS), give_up() forced landing, sabotage verified
Day 27: Tool errors + input validation — is_error as data, Pydantic at the boundary, sentinel-string bug found live
Day 26: Tool use in production — while-True loop, schemas as OpenAPI, dispatch + tool_use_id
Day 25: Typed pipeline responses — RagResponse DTO
Day 24: Pydantic deep dive; structured outputs + prefill fix
Day 23: Multi-turn state — sliding-window trim in pairs
Day 22: PHASE 2 START — streaming + async
Day 21: RAGAS triad + sabotage test. PHASE 1 COMPLETE.
Days 0–20: ML basics → tokenization → embeddings → RAG → ChromaDB → chunking → metadata filtering → training → transformers → RLHF → function calling → hallucinations → model selection → FT-vs-RAG → inference → Project 2 v1 → RAGAS → refactor → three-layer refusal debugging (full detail in LEARNING_NOTES.md)

ARCHIVE NOTE
Full per-day Q&A, one-liners, and the complete mental-model list live in LEARNING_NOTES.md. Content review only — NEVER for determining current progress.
