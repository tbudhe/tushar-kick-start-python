**Purpose & context**

Tushar is a Staff Engineer with ~16 years of backend engineering experience (payment infrastructure, fraud detection, Scan & Go at Walmart) who is now working at Autodesk as an AI Engineer. His primary goal is to reach a Staff/Principal AI Engineer role at Walmart by July 2027. Claude serves as structured tutor and accountability partner for an 18-week self-study AI/ML curriculum, approximately 1.5 hours/day on weekdays.

**Career target ("Walmart 2027"):** Return to Walmart at Staff/Principal AI Engineer level. Autodesk context (particularly Revit, building design software) is used throughout as the applied domain for exercises and examples.

**18-week plan structure:**
- Phase 1 — AI/ML Foundation (Weeks 0–4): ML basics, LLMs, embeddings, RAG, ChromaDB, prompt engineering
- Phase 2 — LLM Engineering (Weeks 5–10): Claude/OpenAI APIs, LangChain/LlamaIndex, FastAPI, production patterns
- Phase 3 — Agentic AI (Weeks 11–18): LangGraph, LangSmith, CrewAI, AutoGen, MCP (Weeks 14–15)
- Phase 4 — Portfolio & Job Readiness (ongoing from Week 12)

**Four GitHub portfolio projects:**
1. Streaming CLI chatbot (Anthropic API, multi-turn memory) — SHIPPED (chatbots/revit-chatbot/)
2. RAG API over Autodesk documentation — v1 SHIPPED, eval hardening in progress
3. LangGraph Autodesk agent
4. Production AI backend with observability and evals

**Key people/context:** Autodesk Revit is the recurring domain; Walmart Scan & Go fraud detection system is the primary analogy anchor from his engineering past.

---

**Current state**

Tushar has completed Day 0 through Day 26 of the curriculum — Phase 1 FULLY COMPLETE; Phase 2 in progress since Day 22 (running roughly 2x the original day-per-topic pace; treat "18-week" boundaries as loose and track by topic completion instead):

- Day 0: ML basics (supervised/unsupervised, neural net forward pass)
- Day 1: Tokenization, embeddings, self-attention (Q/K/V), next-token prediction
- Day 2: Embeddings & cosine similarity
- Day 3: RAG pipeline end-to-end
- Day 4: Prompt engineering (system vs. user prompt, few-shot)
- Day 5: ChromaDB (persistence, distance vs. similarity)
- Day 6: Chunking & overlap
- Day 7: Metadata filtering (`where` clause, pre-filter before vector search)
- Day 8: Loss, gradient descent, overfitting (Week 0 gap session — closed)
- Day 9: Weight/bias, underdetermined systems
- Day 10: Transformers (multi-head attention, layer stacking, positional encoding)
- Day 11: Pretraining → SFT → RLHF pipeline
- Day 12: Chain-of-thought & function calling (tool_use_id mechanics)
- Day 13: Hallucinations (softmax-always-answers, RAG grounding vs. refusal prompting)
- Day 14: Model comparison (Fable 5 / Opus 4.8 / Sonnet 5 / Sonnet 4.6 / Haiku 4.5 spec sheet)
- Day 15: Fine-tuning vs. RAG vs. prompting (knowledge gap vs. behavior gap test)
- Day 16: Inference in production (prefill vs. decode, TTFT vs. tokens/sec, why output costs ~5x input)
- Day 17: Phase 1 capstone + Project 2 v1 SHIPPED — RAG API (FastAPI + ChromaDB + Claude), deterministic evals 5/5
- Day 18: RAGAS faithfulness evals wired into Project 2 (judge=Claude via LangchainLLMWrapper); found refusal-scoring distortion (correct "I don't know" scores 0.0)
- Day 19: Double-retrieval refactor — answer_question returns (answer, sources, chunks), all 3 callers updated; category-filtered eval surfaced a likely miscategorized floor-plan chunk
- Day 20: Floor-plan finding closed via three-layer refusal debugging (filter → threshold → LLM); two hypotheses falsified with printed evidence; correct LLM refusal exposed a coverage gap — fixed with data (doc6), not code; evals 5/5
- Day 21: Retrieval audit loop in debug_floor.py (top-k distances + coverage-risk flag); RAGAS triad completed (answer_relevancy + context_precision, with embeddings model and reference ground truths); sabotage test proved refusal_rate catches what judge metrics miss (broke retrieval → judge metrics stayed perfect, refusal_rate 0.5); layer-2 refusal proven with distances 1.636/1.653 > 1.2
- Day 22: PHASE 2 START — streaming (SSE event lifecycle, stop_reason in message_delta) + async (asyncio.gather = Promise.all); sync/async client-mixing bug caught live; display-vs-API truncation settled with printed evidence (async_batch_questions.py)
- Day 23: Multi-turn state + system prompts — messages list = conversation store (stateless API), sliding-window trim in pairs; odd/even trim bug found + fixed in multi_turn_chat.py; the "400 at turn 11" claim later FALSIFIED by experiment (API accepts assistant-first; role-check downgraded to hygiene)
- Day 25: Typed pipeline responses — answer_question returns one RagResponse (answer + nested list[Source] with id/text/distance + category) instead of a 3-tuple; both branches return the same contract; all 3 callers (app.py, evals.py, ragas_evals.py) read fields by name. Exercise proved the payoff: adding a field broke zero callers, where Day 19's tuple change broke all three. Also closed both overdue weekend items — debug_floor.py audit loop restored, retrieval verified healthy, Day 21 indentation bug confirmed gone
- Day 24: Structured outputs + Pydantic — boundary validation (model_validate_json), prefill "{" + re-attach gotcha, Field constraints (planted 1.7 → less_than_equal), Optional vs = None (null vs absence), nested models with tree error paths (sources.1.score); exercises: structured_output.py, nested_practice.py
- Day 26: Tool use / function calling in production — while-True loop until stop_reason != "tool_use", tool schemas as OpenAPI specs (description = prompt engineering), dispatch dict + tool_use_id correlation, tool results as role="user", RAG=push vs tools=pull, agents = loop + catalog; exercise tool_loop.py (chatbots/stocks_chatbot/) VERIFIED with printed output (tool_use → tool_use → end_turn, sequential dependency chain); Day-25 review fixes verified (evals 5/5, debug_floor healthy); COLD quiz Optional/= None PASSED after two prior failures
- Day 27: Tool errors + input validation in the loop — a tool that RAISES and a tool called with BAD ARGUMENTS both end as a tool_result with is_error: True (a FIELD, not an exception; identical shape to a success). try wraps the SINGLE call not the loop; except ValidationError before except Exception; the error string is prompt engineering and never a raw traceback (internals = untrusted OUTPUT); block.input is a request body validated with Pydantic at the boundary. The protocol rule anchoring all of it: every tool_use block must be answered, so there is no "skip it" branch. HEADLINE FINDING — the sentinel-string bug caught live and A/B'd: NAMES.get(ticker, "unknown ticker") cannot fail, so failures shipped with is_error=False and the model guessed tickers across 3+ paid iterations; switching to raise + an actionable message ("known: ['AAPL','MSFT']") produced ONE call and a clean end_turn. Day 25's own rule violated three weeks after writing it down. Also flagged: the unbounded while True over a paid API is a production incident (Day 28 hook)

**Active open items:**
- **Phase 1 recap owed:** explain embeddings → RAG → prompting → evals out loud, plain English (overdue since the weekend of 2026-08-08 — 6 days as of Day 27, and it is the direct intervention for the recall problem below).
- **Project 2 v2 remaining:** real Autodesk doc chunks, model cost decision (opus → sonnet/haiku), ragas upgrade to drop the vertexai stub, wire typed RevitAnswer into the eval pipeline (Day 25 warm-up).
- **tool_loop.py final-answer check:** the Google run printed the final assistant text; the AAPL run still never did. Confirm 189.50 appears in the FINAL text, not just in a tool_result.
- **tool_loop.py line 22:** get_company_name's description is STILL inverted (says it returns a ticker; it takes a ticker and returns a name). Fifth direction inversion.
- **Day 27 sabotage step not done:** force block.input = {"ticker": ["AAPL"]} to prove the ValidationError branch fires instead of a TypeError crash. The exception path is verified; the validation path is not.
- **tool_loop.py StockPriceInput:** one Pydantic model validating input for BOTH tools. Works only because both take `ticker` — needs per-tool models keyed by block.name before a tool takes different arguments.
- **Revision protocol (agreed 2026-08-10):** every quiz = 3 questions on the last day + 1 COLD question from a random earlier day (rotate Days 0–26, prioritise weak-spots). Retention is the identified risk, not pace. Log the rotation pick in the day's notes. Picks so far: Day 24 (2026-08-11, PASSED), Day 20 (2026-08-14, FAILED — named RAGAS metrics instead of the three refusal mechanisms; re-ask ~2026-08-21). Optional/= None needs one more cold check ~2026-08-18.
- **Weak spot — ADJACENT VOCABULARY (new, Day 27):** every wrong quiz answer used real terms from the correct neighbourhood (TOOL_FUNCTIONS for "why a loop", stop_reason for "how does a result go back", RAGAS metrics for "what causes a refusal"). Drill before answering: name the MOMENT IN TIME the question is about.
- **Weak spot — direction inversions:** five occurrences now (name vs ticker, in vs out, push vs pull, line 22 twice). Rule: say the signature or flow out loud, then transcribe.
- **Pattern to coach against:** recall lags application badly. He rebuilds concepts correctly at the keyboard and debugs with real rigour, but cannot retrieve them cold. Quizzes are the weak surface, not the exercises.
- **Milestones (set 2026-08-10):** Sep 2026 Phase 2 done; Nov 2026 Phase 3 done; Dec 2026 projects 3+4 shipped; Feb 2027 job search opens; Jul 2027 Walmart target with ~5 months buffer. Tushar asked "am I behind?" — he is not: Phase 1 took 21 sessions against 25 budgeted, and 2 of 4 projects are shipped. Reassure with numbers when this recurs, and redirect the worry to retention and consistency.
- **Doc protocol (agreed 2026-08-10):** ONE SESSION = ONE DAY NUMBER, sequential. Never reopen a day as partial/complete/check-in — that is what made Days 24–25 feel stalled (7 headings for 2 "days"). LEARNING_NOTES headings are `## Day N — Topic Name`, no dates or qualifiers. Update all three docs + commit at the end of every session.
- **git push** of Days 22–25 work — commits made locally (through 2ff02c4), Tushar pushes; the sandbox has no GitHub credentials.

**Resolved since last update:**
- **structured_output.py lines 33–34 deleted (2026-08-14):** the commented-out no_topics experiment is gone. Carried item closed.
- **Day 25 review fixes VERIFIED (2026-08-11):** evals.py 5/5 (refused=True, sources=[] on France), debug_floor.py healthy (real queries rank #1 under 0.7, France 1.896/1.973 drop + coverage flag). evals.py TEST_CASES order item closed with it.
- **Floor-plan category finding** (Day 20): not a bug — correct LLM refusal revealing a coverage gap; doc6 added, evals 5/5 green.
- **RAGAS triad complete** (Day 21): answer_relevancy + context_precision wired and sabotage-tested; judge non-determinism observed (relevancy 0.75–0.92 same code) — read as trends, never absolutes.
- **evals.py green run** after the 3-tuple refactor (Day 20).
- **Project 1 VERIFIED AND SHIPPED** — streaming CLI chatbot in chatbots/revit-chatbot/ (memory, streaming, TTFT). The long-standing "content outpacing builds" risk is closed: 2 of 4 portfolio projects shipped.
- Refusal-exclusion in RAGAS evals (Day 18 exercise, done correctly: skip refusals, refusal_rate separate metric, all-refusals guard).
- Double-retrieval bug in ragas_evals.py (Day 19 refactor).

**Recall/articulation quality:** Markedly improved since Day 7. Tushar is now producing full, precise restated sentences unprompted (e.g., Day 16 Q2 self-corrected "prompts drive it" → "prompt size drives it" in the same pass). The "precision gap" pattern flagged below is closing — keep watching, don't assume fully resolved yet.

**Next content block:** Day 27 — quiz on Day 26 + cold pick, then multi-tool + error handling in the tool loop: tool_result with is_error when a tool raises, letting the model recover, validating tool input (schema is a request, not a guarantee). Bridges toward Phase 3 agents. The current mode (build → eval surfaces a finding → fix → learn) is working well and should continue.

---

**On the horizon**

- **Immediate next step:** GPU fundamentals micro-topic (inference at scale, VRAM, batching, cost) — now well-motivated by Day 16 and a natural bridge before Phase 2. Also relevant: Autodesk-specific GPU contention between Fusion rendering and AI inference workloads.
- **Weeks 5–6 (Phase 2 start):** Claude/OpenAI API engineering; Anthropic Academy "Building with the Claude API" applicable here.
- **Weeks 9–10:** FastAPI and production patterns — secondary GPU fundamentals touchpoint.
- **Weeks 11+:** Anthropic Academy "Intro to MCP + Agent Skills" applicable.
- **Post-plan exploration:** Hybrid Ollama architecture — Tushar's own idea: local Ollama model for cheap/fast tasks (routing, classification, summarization) + Claude/OpenAI API for complex reasoning. Deferred deliberately to keep current plan clean. GPU/VRAM relevance resurfaces here.
- **Anthropic Academy:** Claude 101 (recommended immediately, ~1 hour), Building with the Claude API (Weeks 5–6), Intro to MCP (Week 11+).

---

**Key learnings & principles**

- **Tushar self-reports forgetting easily** — this is why the quiz-first protocol exists and why one-day-at-a-time pacing is enforced. Compressing the plan increases forgetting.
- **Precision gap pattern:** Tushar's conceptual instincts are generally correct, but verbal articulation was historically imprecise — directionally right but losing the specific outcome or mechanism. Improving markedly as of Day 16 (self-corrections happening unprompted); Claude should keep pushing for full clean sentences but can ease off the correction frequency if the trend holds.
- **Skipping articulation sentences:** Historically, Tushar had a recurring pattern of skipping restatement exercises after corrections. Not observed recently (Day 7 Q3 was completed cleanly) — Claude should still hold the boundary if the pattern recurs.
- **Current error pattern — Python indentation/block scope (Day 21, 3 incidents in one session):** dedented blocks running once on leaked loop variables (output looked right by accident), for...else trap, per-chunk vs per-question placement. Watch every new block's level; anchor = "indentation is how many times this line runs; you are the closing brace."
- **Evidence-over-guess is landing:** Day 20 falsified two hypotheses; Day 21 Tushar guessed layer 3 for the sabotage refusal and the printed distance (1.636 > 1.2) proved layer 2. Keep demanding printed numbers before verdicts.
- **Analogy anchors that work:** Kafka pipelines, SQL queries (ORDER BY / WHERE), distributed systems, cache-aside pattern (Redis vs database), Express middleware vs HTTP request body, TCP sliding window for chunk overlap, PostGIS for embeddings, event loop with dynamic dispatch (agent tool loop), Redux store (LangGraph state, not yet covered). Walmart fraud detection system is the strongest recurring anchor.
- **ChromaDB threshold principle (repeatedly reinforced):** The vector database always returns n results — it does not filter by relevance. Threshold filtering is the application's responsibility, not the database's. This concept is now solid across Days 5–7; treat as internalized rather than needing repeated correction.
- **Metadata filtering mechanics:** The `where` filter runs before vector search — documents that fail the filter are excluded entirely and never reach similarity ranking. Closest allowed result is always returned regardless of actual relevance.
- **Pacing vs. building gap:** CLOSED — Projects 1 and 2 both shipped; every Phase 2 day since has ended with working committed code.
- **Happy-path-as-proof pattern (Day 24):** offered a topics-present run as evidence for the topics-absent case — rule: to test absence, feed absence. Watch in every exercise.
- **Dead-code residue pattern (Day 24, caught 3x; NOT observed Day 25):** stale/commented lines left in file after fixes — rule: when a fix replaces a line, delete the old line in the same edit. Broken as of Day 25; keep watching.
- **Verification-of-own-work gap (Day 25, 3 incidents):** declared P1 fixed while the file still read category=None; predicted "all tests pass" for a refactor that would have crashed; offered a green evals.py as proof for a debug_floor.py question. His evidence habit is strong when DEBUGGING and switches off when CONFIRMING his own fixes. Coaching line that landed: "verify your fixes with the same skepticism you apply to your bugs."
- **Pushback is developing (Day 25):** Tushar challenged a claim about which file/lines were being referenced and was right to check. Encourage this — it is the same evidence-over-assertion habit, now applied to the teacher.
- **Overwhelm signal (Day 25):** when several findings stack up he says "I am not getting what you are trying to say — go step by step." Response that worked: Where you are / Goal right now / ONE action / explicitly parked items. Park secondary findings out loud rather than dropping them silently.

---

**Approach & patterns**

- **Session protocol (strict, no exceptions):** Quiz on prior day's material → verify any open items → advance to new content. New teaching is withheld until quiz criteria are met.
- **Teaching sequence:** Plain-English explanation with backend/infrastructure analogy → hands-on coding exercise → closing recall questions for next session cold open.
- **Analogy-first for abstractions:** Every abstract ML concept is grounded in Tushar's backend experience before code is shown.
- **Accountability on open items:** Claude tracks deliverables explicitly across sessions (Project 1, ChromaDB hygiene) and does not let them drop.
- **Note format preference:** Plain text shown directly in chat — one-sentence day summary followed by numbered Q&A pairs with Tushar's own answers.
- **Plan discipline:** Tushar prefers keeping the current 18-week plan clean rather than adding scope mid-execution (demonstrated when deferring Ollama and GPU topics).

---

**Tools & resources**

- **Libraries/tools in use:** `tiktoken`, `sentence-transformers` (`all-MiniLM-L6-v2`), ChromaDB (persistent, `./revit_db`), Anthropic Python SDK, `python-dotenv`
- **Repo structure:** `week-0/`, `week-1/`, `week-2/day-7/metadata_filter.py`, `project-1/`
- **Environment:** `.env` file with `ANTHROPIC_API_KEY`
- **Planned tools (later phases):** LangChain (`RecursiveCharacterTextSplitter` already referenced), LlamaIndex, FastAPI, LangGraph, LangSmith, CrewAI, AutoGen, MCP, Ollama (post-plan)
- **Reference resources:** Anthropic Academy (Claude 101 recommended now); 3Blue1Brown neural network video and StatQuest used in early sessions
---

**Session addendum — 2026-08-17 (Day 28)**

- Day 28: Max-iteration guards — agent = tool loop + budget + catalog + goal. agent_loop.py created (run_agent), sabotage-verified both ways: MAX_ITERATIONS=1 forced give_up()'s forced landing (final call with tools disabled → useful text with $189.50); restored to 10 → clean normal exit. Both tools ran in ONE iteration (independent args → parallel calls, Day 26 rule observed live). Ceiling = backstop, error-message quality = fix.
- PLAN CHANGE: after Phase 2 completes, ONE FULL WEEK of Phase 1+2 revision before Phase 3 (Tushar's request, targets the recall gap). Milestones updated in STATUS.md.
- Quiz: Day 20 re-ask — three refusal layers PASSED in order (big improvement from the 08-14 cold fail); first-print (raw query COUNT) still missed. Day 27 Q3 sentinel mechanics FAILED (can fix, can't explain); Q2 sibling-tools not retrieved.
- New pattern named: answers check questions with pasted RUNS instead of SENTENCES (3x this session). A run is evidence, not an explanation.
- Open: Day 27 ValidationError sabotage = Day 29 take-home; line-22 description inversion now in BOTH tool_loop.py and agent_loop.py; per-tool Pydantic models; Optional/= None cold check due 2026-08-18 (Day 29's cold pick). CLOSED: AAPL final text contains 189.50.
- Next: Day 29 — multi-step planning (dependency chains the agent discovers itself, how it decides it's done); last bridge before LangChain/LangGraph.

**Session addendum — 2026-08-18 (Day 29)**

- Day 29: Multi-step planning / dependency chains — STARTED, NOT COMPLETED (session ended early on frustration; Day 30 = "(cont.)"). Core lesson landed: a dependency chain exists only when the model cannot produce tool B's argument without tool A's output; world knowledge is a bypass (model filled AAPL from pretraining, so both calls batched in one turn); chain of N tools = N sequential iterations. Direction lesson: get_company_name (ticker→name) cannot serve name→ticker — two directions, two tools.
- Day 27 ValidationError sabotage take-home: VERIFIED AND CLOSED (forced list-for-string → ValidationError branch, field-level message, loop survived). Pydantic-vs-TypeError tell = specificity (schema/field names vs Python internals).
- Quiz: Q4 cold Optional/= None PASSED clean — weak spot CLOSED (third attempt, first unassisted). Q1 sentinel-spiral PARTIAL, Q2 parallel-calls PARTIAL (code half only), Q3 why-give_up-disables-tools FAILED — re-ask ~2026-08-21 with sentinel mechanics, sibling-tools, Day 20 first-print.
- Exercise incomplete: get_ticker_symbol never registered (data added to wrong dict; no function/TOOLS/dispatch entries) — "a tool needs THREE registrations" lesson. Model guessed the fictional company as a ticker, Day 27 error message handled it gracefully. Day 30 finishes the chain exercise; the shared-StockPriceInput landmine (carried item 4) is left in deliberately and will fire on iteration 0.
- File findings: agent_loop.py line-22 inversion FIXED (verified); tool_loop.py still owed. Self-added get_company_minimum_stock_price is broken 3 ways (str>int compare → TypeError; returns name not price; description promises absent param) — agreed action: DELETE it.
- **NEW COACHING RULE (2026-08-18):** state the exercise GOAL first (what the final printout looks like), then a NUMBERED step list, ONE step at a time with confirmation between steps. The destination-in-prose style caused the frustration that ended the session. Also: sentences-vs-runs recurred twice — keep demanding the sentence before accepting the run.

**Session addendum — 2026-08-20 (Day 30)**

- Day 30: Multi-step planning FINISHED — the chain RAN, goal printout matched exactly (iteration 0 get_ticker_symbol→YNXT, iteration 1 get_stock_price→42.0, iteration 2 "$42.00"); MAX_ITERATIONS ≥ N+1 verified live. Landmine fired as planted: one shared StockPriceInput rejected the lookup tool's valid input; fixed with INPUT_MODELS per-tool validator dispatch (the FOURTH registry, keyed by block.name — carried item since Day 27 CLOSED). Key lesson: the wrong validator's well-formed error message steered the model into calling the wrong tool — error text is prompt engineering even when the error is your bug. Bonus self-found bug: hardcoded AAPL allowlist in get_stock_price replaced with PRICES membership check + known-tickers error. get_company_minimum_stock_price deleted (all 3 registrations).
- NEW RULE (Tushar's request): quiz capped at MAX 5 questions/session (2 last-day + 1 cold + ≤2 follow-ups). STATUS.md shortened same day; full mental-model list archived into LEARNING_NOTES.md.
- Quiz: Q1 chain-vs-parallel PASSED; Q2 three-registrations FAILED (re-ask cold); Q3 Pydantic-vs-TypeError PARTIAL; cold Day 20 count-print missed a THIRD time ("layer = filter, print = count").
- Open: give_up-WHY, sentinel mechanics, sibling-tools re-asks all DUE next session; tool_loop.py line-22; Phase 1 out-loud recap; trim/prefill re-test.
- Next: Day 31 — LangChain intro (map hand-built loop onto framework abstractions) or Project 2 hardening; decide at session start.

**Session addendum — 2026-08-21 (Day 31)**

- Day 31: LangChain intro — `@tool` collapses all FOUR hand-built registries (TOOLS schema, function, TOOL_FUNCTIONS dispatch, INPUT_MODELS validator) into one decorator generated from the function signature; one source of truth means the Day 30 wrong-validator bug is structurally impossible. Spring analogy anchored it: hand-built loop = raw servlets, @tool = @RestController — nothing removed, everything automated (validation still runs, never written). Exercise `exercises/day31_langchain_tool.py` COMPLETED AND VERIFIED (goal-first format, no API call): printed generated registries, re-ran the Day 30 chain via `.invoke()` (YUNextGenAI→YNXT→42.0), fired the free validator on bad input — "company_name Field required", correct this time because the validator is generated from the tool's own signature.
- Direction-inversion weak spot fired LIVE: wrote get_stock_price description as "Look up the ticker symbol to get prices" (both tools opened with identical words); caught via the printed catalog and fixed. Rule reinforced: say the arrow out loud BEFORE writing the description.
- NEW RULES (Tushar): quiz cap = MAX 5 QUESTIONS PER DAY-TOPIC (not per session); LEARNING_NOTES.md day blocks = MAX 5 POINTS each.
- Quiz: Day 30 error-text-is-prompt-engineering LANDED after 3 nudges; four-registries still shaky (3 of 4, missed the function itself; "model only sees TOOLS because it only WRITES a JSON request" missed — both re-ask cold). Day 28 give_up()-WHY PASSED cleanly — CLOSED. Sentences-vs-code recurred (Step-5 prediction skipped).
- Session deliberately short (low-energy day): one concept + exercise, clean stop. Model for future heavy days.
- Next: Day 32 — LangChain cont. (bind tools to a model; what replaces `while stop_reason == "tool_use"`) or Project 2 hardening; decide at session start.

**Session addendum — 2026-08-24 (Day 32)**

- Day 32: LangChain cont. — `.bind_tools()` staples the TOOLS menu onto the model (config-time) and parses replies into `response.tool_calls`; `tool.invoke(tc)` fires validator+function+dispatch in one call and returns a ToolMessage with the id pre-threaded. THE LOOP SURVIVES: "loop again or done" (`if not response.tool_calls:`) is runtime orchestration and still hand-written — agent frameworks take it later. Exercise `exercises/day32_bind_tools.py` COMPLETED AND VERIFIED: round trace get_ticker→YNXT, get_price→42.0, empty tool_calls → "$42.00".
- AGENT-BROKEN CODE INCIDENT: Tushar had an outside AI agent modify the exercise mid-session; it deleted `return response`, the `for range(MAX_ITERATIONS)` wrapper, and `messages.append(response)`. Turned into a guided three-bug hunt he substantially solved (found the missing return himself; articulated that only the MODEL, on the NEXT invoke, can request the second tool). Pedagogically excellent — but watch for outside-agent use on exercises; the deal is he writes, agents don't.
- Menu-vs-trips confusion resolved: he conflated bind_tools tool COUNT with MAX_ITERATIONS. Anchor that landed: menu size (config) vs trips to the kitchen (runtime, sized by the question's dependency chain, N links → MAX_ITERATIONS ≥ N+1). Verify once cold.
- Quiz 4/4 — THREE weak spots CLOSED: four-registries + model-only-sees-TOOLS (clean, unprompted); Day 27 sentinel mechanics (cold, exact mechanism); Day 20 count drill (with the why, after 3 prior misses). NEW OPEN: fallthrough guard vs give_up() — bare `return response` after the guard exhausts hands back an AIMessage still full of tool_calls; give_up() re-calls with no tools → honest end_turn text. He answered half, in code — re-ask cold. Sentences-vs-code recurred twice.
- MORALE: ended the session saying "I am not able to grasp much / why can't I learn quickly." Countered with same-session evidence (4/4, three closures, self-diagnosed broken code). Pattern to watch: he undercounts his own wins — open future sessions by naming a concrete previous win before the quiz.
- Next: Day 33 — LangChain cont. (what finally replaces the hand loop: agent abstractions) or Project 2 hardening; decide at session start.

**Session addendum — 2026-08-25 (Day 33)**

- Day 33: Agent abstractions — `create_agent` (né `create_react_agent`; deprecation to the langchain.agents import fired live mid-exercise) is the Day 32 loop shipped as a library function. ReAct = Reason+Act (not React JS — he asked, good question). Raw model in, no bind_tools, no loop in the file; `agent.invoke()` runs the rounds and `result["messages"]` is the proof transcript. Exercise `exercises/day33_react_agent.py` COMPLETED AND VERIFIED (6-line transcript matched GOAL).
- Bug caught by TRACING before running: dict key "YUNextGenAI" vs question "Yieldnext"; his first fix attempt was `TICKERS[x] or None` — Java habit; landed that Python `dict[key]` throws KeyError before `or` evaluates, `.get()` is the null-returning form.
- Quiz 3/4: Q1 config-vs-runtime PASSED (1 nudge; excellent closing sentence: "binding is static, dispatch is dynamic — the lookup input doesn't exist before execution"). Q3 fallthrough-vs-give_up PASSED clean in SENTENCES — weak spot CLOSED. Q4 sibling-tools PASSED cold, both halves — weak spot CLOSED (open since Day 27). Q2 menu-vs-trips NOT clean (said 1 round, missed the N+1 final trip, then drifted to range() mechanics); topic cap hit, answer given — STAYS OPEN, re-ask cold next session.
- Session tone: steady; no morale dip this time. Morale opener (named the Day 32 self-found `return` win) used per protocol.
- Next: Day 34 — agent abstractions cont. (system prompt / state / streaming on create_agent) or Project 2 hardening; decide at session start.

**Session addendum — 2026-08-26 (Day 34)**

- Day 34: create_agent cont. — `system_prompt=` is KEYWORD-ONLY and is Day 32's `messages[0]` moved to config time (factory.py:1417 prepends the SystemMessage on every model call; it never appears in `result["messages"]`). State did NOT move: the agent is stateless between invokes. Exercise `exercises/day34_react_agent.py` COMPLETED AND VERIFIED — same agent object, part B (one message in) had amnesia, part C (`result["messages"] + follow_up`) answered correctly. His sentence: "conversation memory isn't something it has, it's something I pass in on every call."
- THE DAY'S REAL FIND (a coaching miss worth reusing): the proof marker I chose — "always begin your reply with [YNXT-BOT]" — was silently deprioritized by the model on the turn concluding a tool loop, producing a false "framework is broken" verdict that survived three tests. A BEHAVIORAL marker ("always reply in French") proved delivery instantly. Rule: probe config with behavior the model cannot half-comply with. I told him plainly the flawed instrument was mine, not his code.
- DEBUG SEQUENCE HE NOW OWNS: layer split (raw-model probe vs agent) → shrink to minimal failing case → read the installed library source in `.venv`. The source settled a dispute both our hypotheses got wrong. Separate habit installed: when a result does not move after an edit, verify the file on disk is the code that ran (his French edit lived only in chat for one round; I caught it by reading the file).
- Self-found bug: duplicated `model`/`agent` definitions in one file (Python takes the last assignment silently; Java's compiler would refuse). Second self-catch in two days — the tracing habit from Day 33 is holding.
- Quiz 4/4. Q4 menu-vs-trips PASSED COLD with the dependency-chain sentence — WEAK SPOT CLOSED (open since Day 32). Direction inversion fired twice: ReAct's Act half ("request a tool" = still the model) and the step-5 fill-in-the-blank slots swapped — stays the top open weak spot, drill it cold next session.
- Next: Day 35 — `checkpointer` + `thread_id` (framework session store, the Redis analogy writes itself) or streaming on create_agent, or Project 2 hardening; decide at session start.

**Session addendum — 2026-08-27 (Day 35, IN PROGRESS)**

- Day 35: `checkpointer` + `thread_id` — the framework's session store. `create_agent(..., checkpointer=InMemorySaver())` plus `config={"configurable": {"thread_id": ...}}`. The agent did NOT become stateful: a store remembers and he passes a KEY instead of a TRANSCRIPT. Spring mapping he accepted immediately: agent = stateless @RestController (unchanged), checkpointer = Spring Session + Redis, thread_id = JSESSIONID, graph loads before the run and appends after. `InMemorySaver` is debug-only per its own docstring — a dict in one process.
- Exercise `exercises/day35_react_agent.py`: Parts A (no checkpointer → amnesia), B (checkpointer + thread_id → recalled from ONE message), C (different thread_id → amnesia, key isolates) WRITTEN UNAIDED, ahead of the step gate, correct first run. Part D pending: `agent.get_state(cfg).values["messages"]` counts per thread + check for any stored SystemMessage (expected False — verifies Day 34's Q1 against the store rather than a printed transcript).
- UNPLANNED WIN: his own output reproduced Day 34's proof-marker finding WITH A CONTROL GROUP — `[YNXT-BOT]` present on every turn that did not conclude a tool loop (A, B-turn-2, C), dropped on the one that did (B-turn-1). One run of this file would have settled the entire Day 34 dispute. Second observation: B turn 2 answered "YNXT" without calling get_ticker — stored state skipped a tool call, i.e. memory is a latency/cost argument too.
- Quiz 4/4 (Day 34 topic + cold). Q1 system-prompt location (2 nudges; first said it DOES appear in result["messages"], then produced a better framing than the notes had: "it stopped being conversation data and became request-building configuration"). Q2 stateless B/C clean first try. Q3 proof markers (1 nudge) → generalised rule: A GOOD INSTRUMENT HAS EXACTLY ONE EXPLANATION FOR ITS FAILURE. Q4 direction-inversion drill PASSED COLD, no nudge, resisting the description's word-order bait by reading the signature.
- WEAK SPOT 1 (direction inversion) DOWNGRADED PRIORITY → WATCH: clean cold pass, but he inverted `thread_id` in the check question ("passed to the model") and needed one nudge. One more clean cold pass closes it. Answer depth notable: the thread_id-collision answer was a full cross-tenant-leak + race analysis, unprompted.
- ENV: the repo `.venv` python symlink does not resolve from Claude's mounted shell — Claude cannot execute his code. Reads `.venv` source, Tushar runs everything.
- Next: finish Day 35 Part D (~15 min), then Day 36 — streaming on create_agent or Project 2 hardening; decide at session start.

**Session addendum — 2026-08-31 (Day 36)**

- Day 36: streaming on `create_agent`. `.stream()` is request-time, `create_agent()` is build-time — he first wrote `create_agent(...).stream()` chained, corrected via the Day 34 config-vs-state distinction. Three modes measured in one file: `updates` (5 yields, node-keyed delta), `values` (6 yields, whole growing list, no node key), `messages` ((token, metadata) tuple, sub-message). Ship verdict: `stream_mode=["updates","messages"]`; `values` is a debugger.
- Exercise `exercises/day36_streaming_agent.py` COMPLETE — Parts A, B, C all green.
- Quiz 3/3 (the new 3-question cap, honored). Q1 thread_id four-blank frame — all four correct, no nudge. Q2 shared thread_id in prod — answered "cross-user data leakage in both directions", the leak framing unprompted. Q3 cold Day 27 orphaned tool_use — he did not just answer, he RAN A FOUR-CASE CONTROL SET including the inverted error (tool_result with a bogus id → "unexpected tool_use_id"). CARRIED-FORWARD ITEM 5 CLOSED (that question was previously answered by Claude, not him).
- FRICTION THIS SESSION, CLAUDE'S FAULT, TWICE: (a) traced the example with `get_ticker` returning a price, contradicting his own Day 30 two-tool chain — he caught it and said he was confused; redrawn with his real chain fixed it. (b) Handed him a code FRAGMENT referencing `msg`/`node` when his file had `m`/`label` — he pushed back ("I don't see msg... be specific and correct") and was right. RULE: when he is mid-exercise, paste COMPLETE blocks with every variable's origin named, never fragments.
- `getattr` vs `.get()` swap: he wrote `getattr(TICKERS, "tool_calls", None)` on a dict. Attribute access vs key access. Failure mode named as the teaching point — both tools returned None for every input with NO exception (Day 30's silent-wrong-beats-KeyError, live). Later he used `getattr(msg, "tool_calls", None)` correctly — both cases now sit in one file.
- Next: Day 37 — async agent (`ainvoke`/`astream`, concurrent tools, where async does NOT help). Short day, Node.js background carries it. Optional 60-second opener: the deferred `input_json_delta` check from Day 36 Part C.
