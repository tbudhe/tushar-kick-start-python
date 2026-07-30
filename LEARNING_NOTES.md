# Tushar's AI / GenAI / Agentic AI Learning Notes
# (ARCHIVE — for content review only. Current progress lives in STATUS.md.)

Staff Software Engineer → AI Backend Engineer (Autodesk) → target: Staff/Principal AI Engineer, Walmart, July 2027.

---

## Day 0 — ML Basics
**One-liner:** ML learns from data; supervised needs human labels, unsupervised finds patterns; a neural network transforms input through layers to make a prediction.

1. Rule-based vs. ML? Rule-based = hardcoded logic in code. ML = predictions based on patterns learned from data.
2. Supervised vs. unsupervised? Supervised = humans label the data, model learns to match labels. Unsupervised = no labels, model finds structure on its own.
3. How does a neural network work? Input × weight → sum → + bias → activation function → output.

## Day 1 — Tokenization, Embeddings, Attention
**One-liner:** An LLM breaks text into tokens, uses self-attention to relate tokens to each other, then predicts the next token one at a time.

1. Tokenization: text → token IDs → decoded back to sub-words.
2. Embedding: each token ID becomes a list of numbers capturing meaning — "King" and "Queen" land close together, "King" and "Pizza" don't.
3. Self-attention: Query = what am I looking for, Key = what do I contain, Value = what do I actually pass forward. Attention computes a weighted relevance score between every token's Query and every other token's Key, then uses those weights to blend Values — that's what "relates tokens to each other" means mechanically.
4. Prediction: next-token prediction, one token at a time, each new token conditioned on everything before it.

## Day 2 — Embeddings & Cosine Similarity
**One-liner:** Embeddings turn meaning into numbers; cosine similarity measures how close two meanings are — that's how RAG finds the right document before calling the LLM.

1. Embedding: a list of numbers representing the meaning of a word or sentence.
2. Cosine similarity = 0.07: essentially unrelated — near-zero overlap in meaning space.
3. Connection to RAG (backend analogy): RAG is cache-aside — check the vector store for similar content before calling the LLM, just like checking Redis before hitting the DB.

## Day 3 — RAG Pipeline
**One-liner:** RAG embeds your docs, embeds the question, finds the closest chunks by cosine similarity, and passes only those chunks to the LLM so it answers from your data, not guesswork.

1. Why chunk before embedding? Smaller pieces keep cosine similarity meaningful — one embedding per big document dilutes the meaning (connects forward to Day 6).
2. Retrieval threshold: a cutoff score (0.75 used) below which a result is considered irrelevant and dropped.
3. What goes to the LLM? Both — the original question and the retrieved chunks.
   Flow: docs → chunk → embed (build the index) / question → embed → cosine similarity against the index → top chunks + question → LLM.
   Reminder: cosine similarity — higher = better (keep ≥0.75). ChromaDB distance — lower = better (keep ≤~1.5). Inverted scales measuring the same thing.

## Day 4 — Prompt Engineering
**One-liner:** A system prompt sets the role; few-shot examples set the output format — together they give the LLM rules and a pattern to follow.

1. System prompt vs. user prompt: System prompt = the rules of the game, set once, invisible to the user (like Express middleware). User prompt = the actual question, changes every turn (like the HTTP request body).
2. Fixing verbose answers: few-shot examples — show the model the exact format/length wanted instead of describing it.
3. role: user / role: assistant: user = the question being asked; assistant = the model's response, shown in few-shot examples to demonstrate the desired format.

## Day 5 — ChromaDB
**One-liner:** ChromaDB persists embeddings to disk and indexes them for fast search; it returns distances (lower = better), but the threshold decision is yours, not the database's.

1. Two problems solved vs. Day 3's in-memory approach: persistence (survives restarts) and indexed search (fast at scale, no full re-scan).
2. Distance vs. similarity: Chroma gives distance, not similarity — the read flips. Lower distance = better match (<0.5 cutoff used), instead of higher = better.
3. Pizza query returned distances >2.0 — why, and whose job is filtering? ChromaDB always returns the N nearest documents in the collection, no matter how far away they actually are — it has no concept of "good enough," only "closest available." Filtering by a distance threshold is application code's job, not the database's.


## Day 6 — Chunking
**One-liner:** Chunking splits documents into small pieces so each embedding stays sharp; overlap ensures a sentence cut at a boundary still appears whole in at least one chunk.

1. Why not embed a 40-page doc as one vector? One vector = one meaning. Averaging 40 pages into one embedding dilutes it — even a relevant question scores weakly. Small, focused chunks keep the meaning sharp and produce strong matches.
2. Why overlap exists: like a book — the last sentence of page 1 carries into page 2, so page 2 alone still has enough context to make sense. Overlap prevents a sentence split across a chunk boundary from becoming two meaningless halves.
3. 0.73 distance on an irrelevant chunk — what does that teach you? Never trust top-N results blindly; the database returns "closest," not "relevant." Fix = enforce your distance/similarity threshold in application code (same principle as Day 5 Q3).

## Day 7 — Metadata Filtering
**One-liner:** Metadata filtering narrows the search to an exact subset — like a SQL WHERE clause — before vector search finds the closest meaning within it.

1. Before or after similarity search? Before. ChromaDB narrows the candidate pool to only documents matching `where` first, then runs nearest-neighbor search inside that smaller pool.
2. "Waterproof doors" query, only 2 door-category docs in 500: With the filter, you get at most those 2 (or fewer) — a small, honest result set. Without a filter, you'd always get N results padded with whatever's next-closest, even if it's a bad match.
3. What gap does metadata filtering close that pure semantic similarity can't? Semantic similarity only measures "how close is the meaning" — it can't enforce hard facts like category, version, or region. Metadata filtering adds exact yes/no constraints on top of that, like a SQL WHERE clause before the ranking happens.
4. A document is highly relevant, but its metadata doesn't match your `where` filter — what happens to it? It's excluded entirely before similarity search ever runs. Relevance doesn't matter — the filter is exact-match, not fuzzy, so a non-matching document never enters the candidate pool, no matter how good its embedding match would have been.

## Day 8 — Loss, Gradient Descent, Overfitting
**One-liner:** Training is a loop of predict → measure → adjust guided by loss; train/test split checks whether the model learned the pattern or just memorized the training data.

1. What does loss measure? How wrong the prediction is. Lower = better.
2. Gradient descent — nudges weights in what direction, based on what? Direction is based on the gradient — the slope of the loss function with respect to each weight, at the current weight values. Gradient descent nudges every weight opposite the gradient (the gradient itself points toward steepest increase), i.e. in the direction that decreases loss fastest.
3. High train score, low test score? Overfitting — the model memorized training data (including its noise) instead of the general pattern, so it fails on unseen data.

## Day 9 — Weight, Bias, and Underdetermined Systems
**One-liner:** Weight scales the input and bias shifts the output regardless of input; you need more data points than parameters to pin down one correct answer instead of many that fit equally well.

1. Weight vs. bias: Weight multiplies the input — controls the slope/steepness of the relationship between input and output. Bias is added afterward regardless of input value — controls the offset, shifting the whole output up or down (like a line's y-intercept).
2. Why couldn't gradient descent find a unique answer with one data point? One point is consistent with infinitely many lines (infinite weight/bias combinations pass through it) — the system is underdetermined. Need at least as many data points as free parameters to constrain a single, unique solution.
3. Four Week 0 concepts in order: loss → gradient descent → weight/bias updates → train/test split (checking for overfitting).

## Day 10 — Transformers
**One-liner:** A transformer adds positional encoding so order isn't lost, runs multiple attention heads in parallel to catch different relationships, and stacks many blocks so each layer refines what the last one built.

1. Why multi-head attention? A single attention pass can only learn one kind of relationship at a time. Multiple heads run in parallel on the same input, each specializing (grammar, topic, long-range reference, etc.), then combine — like running several independent analyses instead of one generalist pass.
2. Why stack layers instead of one big layer? Each layer refines the already-refined output of the previous layer, like pipeline stages building on prior work rather than starting from scratch. Depth (many simple layers) captures more complex patterns than one giant layer trying to do it all at once.
3. Remove positional encoding entirely? The model loses all sense of word order — "dog bites man" and "man bites dog" would look identical, since attention alone has no notion of sequence, only relationships.

## Day 11 — Pretraining, SFT, RLHF
**One-liner:** Pretraining learns language from self-generated next-token pairs at massive scale; SFT (Supervised Fine-Tuning) teaches instruction-following from curated human examples; RLHF (Reinforcement Learning from Human Feedback) shapes behavior toward what humans actually prefer.

1. Why is pretraining "self-supervised" rather than manually supervised? The label is just the next word in the existing text — no human annotates anything. Every sentence on the internet supplies its own labels for free (predict token n+1 from tokens 1..n), which is why it scales to trillions of tokens.
2. SFT vs. RLHF — what does each teach? SFT teaches the model what a good response looks like — format, instruction-following — from a curated set of human-written example Q&A pairs. RLHF teaches the model which of several responses humans prefer — tone, helpfulness, safety — by training on human rankings/feedback rather than fixed examples.
3. Three pipeline stages, in order: Pretraining → SFT → RLHF.

## Day 12 — Chain-of-Thought & Function Calling
**One-liner:** Chain-of-thought gives the model more reasoning tokens to work through a problem before committing to an answer; function calling lets the model request that your code run a real function, then feeds the result back so the answer is grounded in fact, not a guess.

1. Why does "think step by step" improve accuracy, mechanically? Each token is conditioned on everything before it, so reasoning tokens let the model solve a hard problem as a chain of small, easy steps instead of jumping straight to the answer.
2. In function calling, what does the model actually execute? Just the request — it outputs a structured "call this function with these arguments" message. Your code is what actually runs the function; the model never executes anything itself.
3. What two pieces does your code send back, and why does `tool_use_id` matter? The function's real result (as a `tool_result` message) plus the matching `tool_use_id`. The ID matters because a single turn can request multiple tool calls at once — the ID is how the model matches each result back to the specific call that produced it.

## Day 13 — Hallucinations
**One-liner:** An LLM doesn't know when it doesn't know — it always predicts the next most likely token, so when it lacks the real answer it confidently generates a plausible-sounding wrong one instead of saying "I don't know."

1. Why does an LLM always produce an answer, even when it doesn't actually know one? Softmax distributes 100% probability across the entire vocabulary — there's no "I don't know" bubble in that distribution. The model always outputs whatever has the highest probability, like a multiple-choice question with no fill-in-the-blank option.
2. RAG grounding and refusal prompting both fight hallucination — what gap does each one close? RAG grounding closes the knowledge gap: it gives the model real facts to condition on, so it doesn't need to guess. Refusal prompting closes the behavior gap: even with good context, the model needs explicit permission in the system prompt to say "I don't know" instead of defaulting to a confident guess.
3. What does the "switch statement with no default case" analogy illustrate? The LLM's flaw: every input falls into some branch, so it always returns something, even if wrong (no-default = the hallucination problem). Adding `default: throw NotFoundException` is the fix — that's what refusal prompting does (default-that-throws = the fix).

## Day 14 — Model Comparison
**One-liner:** Model selection is a spec-sheet decision — context window, cost, latency, and benchmarks — not just picking the biggest model available.

```
ChromaDB ──chunks──►  ┌─────────┐
User question ──────► │   LLM   │ ──► answer
System prompt ──────► └─────────┘
        (all INPUT)              (OUTPUT)
```

| Model | API Model ID | Context | Max Output | Price In ($/1M) | Price Out ($/1M) | Latency Profile | Key Benchmarks | Best For |
|---|---|---|---|---|---|---|---|---|
| Fable 5 | claude-fable-5 | 1M | 128K | $10.00 | $50.00 | Slow to first token; long-horizon async work; always-on adaptive thinking | SWE-bench Verified 95%; SWE-bench Pro 80.3% | Hardest multi-file refactors, long autonomous agent runs, frontier coding |
| Opus 4.8 | claude-opus-4-8 | 1M | 128K | $5.00 | $25.00 | Moderate; Fast mode available at premium pricing | SWE-bench Verified 88.6%; SWE-bench Pro 69.2% | Opus-tier reasoning at half Fable's per-token price |
| Sonnet 5 | claude-sonnet-5 | 1M | 64K | $2.00 | $10.00 | Mid-tier; best for interactive/real-time; thinking can be disabled | SWE-bench Verified 85.2%; SWE-bench Pro 63.2%; HLE w/ tools 57.4% | Default for coding agents, chat, knowledge work; interactive UX |
| Sonnet 4.6 | claude-sonnet-4-6 | 1M | 64K | $3.00 | $15.00 | Mid-tier | Prior-gen Sonnet; solid coding/agent baseline | Ecosystem continuity for existing Sonnet 4.x workloads |
| Haiku 4.5 | claude-haiku-4-5 | 200K | 64K | $1.00 | $5.00 | Fastest tier; lowest time-to-first-token | Strong on simple/high-volume tasks (not frontier benchmarks) | Real-time support bots, classification, extraction, bulk summarization (+ Batch API 50% off) |

Pricing is API list price per 1M tokens (USD), as of July 2026. Sonnet 5: $2/$10 introductory through Aug 31, 2026, then $3/$15 standard. Benchmarks are Anthropic vendor-reported; scores vary by scaffolding.

1. Real-time support chatbot at Autodesk — high volume, simple queries, latency matters. Which model, and which two spec-sheet numbers drove it? **Haiku 4.5** — lowest time-to-first-token and lowest $/1M price (both in and out).
2. Input vs. output pricing, and why it matters for RAG: **Output is more expensive** (~5x). RAG makes calls bigger because it stuffs chunks into the prompt — but that inflation lands on the cheaper counter (input), not the expensive one (output).
3. Sonnet 5 (85.2%) vs Fable 5 (95%) on SWE-bench Verified — why pick Sonnet 5 for production anyway, beyond cost? (a) Latency — Sonnet 5 is mid-tier/interactive, Fable 5 is slow-to-first-token and built for long-horizon async work, which is wrong UX for an interactive coding agent. (b) Fable 5's "always-on adaptive thinking cannot be disabled," which adds overhead/unpredictability for high-volume production traffic where Sonnet 5 lets you disable thinking when not needed.

## Day 15 — Fine-Tuning vs RAG vs Prompting
**One-liner:** Prompting changes what I tell the model, RAG changes what data it sees, fine-tuning changes the model itself — knowledge gaps get RAG, behavior gaps get prompting first.

Lacked it → knowledge gap → RAG. Had it, delivered wrongly → behavior gap → prompting first (few-shot examples), fine-tuning only if prompting maxes out.

1. Knowledge gap vs. behavior gap — the one-question test, and which tool fixes each? Ask: did it not know, or did it know but misbehave? Didn't know → feed it data (RAG). Knew but delivered it wrong → coach the delivery (prompting first; fine-tuning only if prompting caps out).
2. Why is fine-tuning the wrong tool for injecting facts like release notes? Three reasons:
   - **Lossy** — weights half-remember details, not exact. Like a blurry photo of a document: you see the shape, can't read every word.
   - **Stale** — weights freeze facts at training time. Like bread left out for a week.
   - **No receipts** — weights can't cite a source; RAG can point to the exact chunk. "Receipts" = evidence of where an answer came from.
3. Retrieved chunks in a RAG call — which token counter do they hit, and from whose perspective is input/output defined? From the LLM/model call's perspective: retrieved chunks are **input tokens** (prompt), the model's response is the **output token**.

## Day 16 — Inference in Production
**One-liner:** Prefill reads the whole prompt at once (parallel) and sets time-to-first-token; decode generates one token at a time (sequential) and sets streaming speed.

```
[Enter pressed]────silent pause────[first word appears]────words stream────[done]
                    ↑ PREFILL                                ↑ DECODE
```
RAG inputs (chunks, question, system prompt) are processed by prefill. Output generation (the answer) is decode.

TTFT (time-to-first-token) is the UX metric; tokens-per-second is the throughput metric — and prompt size drives TTFT. Fewer chunks → smaller prompt → less prefill work → shorter silent pause → feels snappier. Shorter answers → less decode → total time and token bill both drop (output is the 5x-cost side) — real benefits, but the user was never staring at silence during that part.

1. Prefill vs. decode — what does each do, and which is parallel vs. sequential? Prefill reads the entire prompt in one parallel pass (processes input, system prompt, and RAG chunks all at once). Decode generates output one token at a time, each new token conditioned on everything generated so far — which is why it can't be parallelized.
2. Which metric is the UX metric for a streaming chatbot, and what drives it? TTFT. Driven by prompt size: more chunks, longer system prompt, bigger context = more prefill work = longer pause before the first word appears.
3. Mechanically, why do output tokens cost ~5x input tokens? Prefill processes input tokens in a single parallel GPU pass — cheap per token. Decode can't do that; it runs sequentially, running the entire model per output token, because each token depends on the one before it.

## 🚢 Project 1 — Streaming CLI Chatbot (SHIPPED — built across Days 4–16)
**What it is:** Multi-turn Revit CLI chatbot in `chatbots/revit-chatbot/` — chatbot.py (memory + streaming + TTFT measurement), tool_use.py (function calling), chain_of_thought.py.

1. Multi-turn memory: the `conversation` list — append user message, call Claude with FULL history, append assistant reply. The API is stateless; memory is my job (like session state in a stateless REST service).
2. Streaming: `client.messages.stream(...)` + `stream.text_stream`, print chunks with `flush=True` — decode tokens shown as they arrive instead of waiting for the full response.
3. System prompt: sets role + behavior rules once, outside the message history (middleware, not request body).
4. TTFT instrumentation: timestamp before the stream, log elapsed time at first chunk — measured prefill cost directly, and saw a fat system prompt raise TTFT (Day 16 lesson in code).
5. Roadmap check: Project 1 of 4 done. Next: Project 2 (RAG API), then LangGraph agent, then production AI backend.

## Day 17 — Phase 1 Capstone + Project 2 v1 (RAG API shipped)
**One-liner:** Wired FastAPI + ChromaDB + Claude into a working /ask endpoint with calibrated threshold, empty-context short-circuit, refusal system prompt, and evals that test the production code path.

1. How do you pick a distance threshold? Calibrate, don't guess — run known-relevant and known-irrelevant queries, look at the distance gap (relevant: 0.18–0.75, junk: 1.69+), pick a value inside the gap (chose 1.2).
2. Where does the threshold live and why? Application code (retriever.py) — vector DBs return "closest," not "relevant."
3. Write path vs. read path rule? ingest.py writes (upsert, idempotent, run manually), retriever.py reads (per-request, threshold applied); neither imports the other.
4. What happens when retrieval returns zero chunks? Short-circuit — return "I don't know" WITHOUT calling Claude: no hallucination, no cost, faster response.
5. What makes a system prompt hallucination-resistant? Answer ONLY from provided context; reply exactly "I don't know" if context lacks the answer; keep answers short. Rules go in system (middleware policy), context + question go in the user message (request payload).
6. Why did "Revite" (typo) still retrieve door docs? Embeddings are semantic, not lexical — cosine/L2 distance tolerates typos that string matching would not.
7. Why must evals import the same function the API uses? Duplicated pipeline logic means evals test a copy — they can pass while production code is broken. Extracted rag_service.answer_question() so evals exercise the real path.
8. Why anchor the ChromaDB path with Path(__file__).parent? A relative path resolves against the process's cwd — launching uvicorn from another directory silently creates a fresh empty DB and every answer becomes "I don't know" with no error.
9. What's the general principle about thresholds? Thresholds are outputs of a calibration experiment, not guesses.

## Day 18 — RAGAS faithfulness on Project 2 (judge LLM, grounding vs. truth, refusal distortion)
**One-liner:** RAGAS faithfulness uses a judge LLM to check that every claim in the answer is contained in the retrieved context — it measures grounding, not truth, and refusals must be scored separately.

1. What is faithfulness? Supported claims ÷ total claims — judge LLM decomposes the answer into atomic claims and checks each against the retrieved contexts. Domain-blind containment check (answer ⊆ contexts), NOT a truth check.
2. Why did "I don't know" score 0.0? A correct refusal has no supporting context, so the judge marks it unsupported. Exclude refusals from faithfulness; track refusal_rate as its own metric.
3. HF Dataset vs. ChromaDB? Dataset = ephemeral fixtures array (eval input packaging, rebuilt every run); ChromaDB = persistent production data. Only eval SCORES over time are worth persisting.
4. Why separate ragas_evals.py from evals.py? Deterministic checks are fast/free/run-every-change (unit tests); LLM-judged evals are slow/costly/run-on-prompt-threshold-chunk-changes (load tests). Both import rag_service — the prod path.
5. Judge LLM vs. pipeline LLM? Pipeline LLM writes the answer under domain policy (system prompt); judge LLM grades evidence-match with no domain knowledge at all.
6. Debugging lesson: a traceback whose paths are all in site-packages = dependency version conflict, not your code. venv = node_modules for Python; never pip install without (.venv) in the prompt.
7. Open refactor: ragas_evals.py retrieves twice (inside answer_question + directly for contexts) — correctness risk if calls diverge. Fix: answer_question returns (answer, sources, chunks). Exercise for Day 19.

## Day 19 — Double-retrieval refactor: pipeline returns its own evidence
**One-liner:** answer_question now returns (answer, sources, chunks) so evals grade against the real context — re-retrieving in the eval risks scoring against evidence the answer never saw.The judge must grade against the evidence the pipeline returned, because a second retrieval is a guess about the past, not a record of it.

1. Why is calling retrieve() a second time inside the eval a bug? The judge may grade against different chunks than the answer was built from (filters, re-ingest, non-determinism) — the eval lies silently. Also double ChromaDB cost.
2. What breaks when you add a third return value in Python? Every caller unpacking 2 values crashes with ValueError (strict unpacking). Unlike JS destructuring, Python won't silently drop extras. Fix: answer, sources, _ = ...
3. refusal_rate jumped to 0.5 after adding category filters — bug or finding? Finding. WHERE filter runs before vector search; a miscategorized chunk gets filtered out → empty retrieval → short-circuit refusal. The eval surfaced a real data problem.
4. Do eval files ship to production? No — they're dev/CI tools. But they must IMPORT production code (rag_service), never copy it, so they always test the real code path. One pipeline, many importers; a copied pipeline drifts and evals score a ghost.
5. Pipeline behavior vs. eval behavior are different layers: the distance threshold explains why a refusal HAPPENED; "no supported claims" explains why the judge SCORES it 0.
6. Open finding: floor-plan chunk likely tagged with a category other than "floors" — verify in ingest.py and fix tag or eval (Day 20).
7. Why must the RAGAS judge score against the chunks returned by answer_question instead of calling retrieve() again? A: The judge grades a past event — "was this answer supported by what the LLM actually saw?" The returned chunks are the audit log (proof); a second retrieve() is a replay (guess) that can differ due to re-ingest, different params, or code drift. Grade the evidence, never re-fetch it.
8. Walk through the chain that refused "floor plan view" with category="floors" — before the LLM was called. A: (1) category becomes a ChromaDB WHERE filter, (2) filter runs BEFORE vector search, (3) miscategorized chunk excluded → empty retrieval, (4) short-circuit returns refusal without calling the LLM. The refusal was application code, not the model — like a Redis cache miss with no DB fallback.
9. What happens when a 2-var caller unpacks a 3-value return? A: Python: ValueError: too many values to unpack — strict arity, fails loud. Node: [a, b] = threeThings() silently drops the third — fails quiet. Python's crash is a feature: it forces you to update every caller.
10. My own words (say this out loud): "The judge must grade against the evidence the pipeline returned, because a second retrieval is a guess about the past, not a real record of the transaction."

## Day 20 — Three-layer refusal debugging: filter → threshold → LLM
**One-liner:** A RAG refusal can fire at three layers — metadata filter (empty retrieval), distance threshold (gate in application code), or the LLM's refusal prompt — debug them in order with evidence, never guesses; ours was layer 3: a correct refusal exposing a coverage gap, fixed with data (new doc), not code.

1.  What are the three layers where a RAG refusal can originate? A: (1) WHERE filter excludes everything → empty retrieval → short-circuit; (2) chunks return but all distances fail the threshold gate in retrieve(); (3) chunks pass into the prompt but the LLM's refusal system prompt says the context doesn't answer the question. Check them in order.
2. How did we falsify the "miscategorized chunk" hypothesis? A: Opened ingest.py — doc5 was correctly tagged "floors". Evidence killed hypothesis #1.
3. How did we falsify the "threshold refusal" hypothesis? A: debug_floor.py printed distance 1.12 < 1.2 threshold — doc5 passed the gate, so the short-circuit never fired. Hypothesis #2 dead. One printed number beats any amount of reasoning.
4. So why did Claude say "I don't know"? A: The retrieved chunk was about *creating a floor element*; the question was about *floor plan views*. Context genuinely didn't answer the question — the refusal system prompt worked exactly as designed. Not a bug: a correct refusal revealing a coverage gap.
5. Knowledge gap fix — code or data? A: Data. Added doc6 (floor plan view doc, category "floors") to ingest.py. Day 15's rule applied: knowledge gap → RAG/data, behavior gap → prompting. After re-ingest: doc6 distance 0.76 (vs doc5's 1.12) — relevant doc now ranks first.
6. Why re-run evals.py after only changing data? A: Corpus changes can break existing behavior — regression check. 5/5 still green, including the off-topic "I don't know" case.
7. Chroma lists (documents/ids/metadatas) must stay the same length — same strict-arity spirit as Python tuple unpacking.
8. Debug scripts (debug_floor.py) = one-off curl against your own API: import the SAME collection object production uses, probe below the abstraction, delete or keep after.

## 🚢 Project 2 — RAG API over Revit Docs (SHIPPED v1 — Day 17)
**What it is:** FastAPI RAG service — `POST /ask` answers Revit questions grounded in ChromaDB docs with sources. Files: ingest.py, retriever.py, rag_service.py, app.py, prompting/revit_context_qa.py, evals.py.

1. Architecture: write path (ingest.py, idempotent upsert) vs. read path (retriever.py, per-request) — neither imports the other; app.py and evals.py share rag_service.answer_question() so evals test the production pipeline.
2. Calibrated threshold: measured distances (relevant 0.18–0.75, junk 1.69+) → chose 1.2. Threshold is an output of an experiment, not a guess.
3. Hallucination control: refusal system prompt (context-only, exact "I don't know", short answers) + empty-retrieval short-circuit that skips Claude entirely.
4. Evals: 5/5 — four grounded questions checked against expected source ids, one off-topic question required to return exactly "I don't know".
5. Remaining for v2: ~~refusal-exclusion in RAGAS evals + double-retrieval refactor~~ (done Days 18–19), floor-plan category finding, more RAGAS metrics (answer_relevancy, context_precision), real Autodesk doc chunks, model cost decision (opus → sonnet/haiku), proper ragas upgrade to drop the vertexai stub.

## 📊 Portfolio scoreboard (2 of 4 shipped)
- ✅ Project 1: Streaming CLI chatbot (memory, streaming, TTFT)
- ✅ Project 2: RAG API v1 (FastAPI + ChromaDB + evals)
- ⬜ Project 3: LangGraph Autodesk agent
- ⬜ Project 4: Production AI backend (FastAPI + RAG + LangGraph + LangSmith)

---

## Recurring analogies (anchor list)
- LLM token prediction = Kafka consumer predicting next message type from stream history
- Embeddings = PostGIS index where proximity means semantic similarity, not distance
- RAG pipeline = cache-aside pattern (check vector store before hitting LLM, like Redis before DB)
- Agent tool loop = event loop with dynamic dispatch (LLM decides which function to call)
- Context window = max request body size limit
- LLM evals = integration tests for AI behavior (fuzzy, not exact match)
- Async LLM calls = Promise.all / asyncio.gather
- FastAPI = Express.js with different syntax
- System prompt vs. user prompt = Express middleware vs. HTTP request body
