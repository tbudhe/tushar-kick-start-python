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

1.  What are the three layers where a RAG refusal can originate? (1) WHERE filter excludes everything → empty retrieval → short-circuit; (2) chunks return but all distances fail the threshold gate in retrieve(); (3) chunks pass into the prompt but the LLM's refusal system prompt says the context doesn't answer the question. Check them in order.
2. How did we falsify the "miscategorized chunk" hypothesis? Opened ingest.py — doc5 was correctly tagged "floors". Evidence killed hypothesis #1.
3. How did we falsify the "threshold refusal" hypothesis? debug_floor.py printed distance 1.12 < 1.2 threshold — doc5 passed the gate, so the short-circuit never fired. Hypothesis #2 dead. One printed number beats any amount of reasoning.
4. So why did Claude say "I don't know"? The retrieved chunk was about *creating a floor element*; the question was about *floor plan views*. Context genuinely didn't answer the question — the refusal system prompt worked exactly as designed. Not a bug: a correct refusal revealing a coverage gap.
5. Knowledge gap fix — code or data? Data. Added doc6 (floor plan view doc, category "floors") to ingest.py. Day 15's rule applied: knowledge gap → RAG/data, behavior gap → prompting. After re-ingest: doc6 distance 0.76 (vs doc5's 1.12) — relevant doc now ranks first.
6. Why re-run evals.py after only changing data? Corpus changes can break existing behavior — regression check. 5/5 still green, including the off-topic "I don't know" case.
7. Chroma lists (documents/ids/metadatas) must stay the same length — same strict-arity spirit as Python tuple unpacking.
8. Debug scripts (debug_floor.py) = one-off curl against your own API: import the SAME collection object production uses, probe below the abstraction, delete or keep after.

## Day 21 — Retrieval audit loop + RAGAS triad (answer_relevancy, context_precision) + sabotage test
**One-liner:** Built a retrieval audit (top-k distances + coverage-risk flag per eval question), completed the RAGAS triad — precision grades retrieval, faithfulness grades grounding, relevancy grades direction — then broke retrieval on purpose and learned that refusal_rate catches what judge metrics can't see.

1. What does the coverage-risk flag (best distance > 1.0) actually mean? "Retrieval cannot ground this question" — the human interprets it: Revit question flagged = coverage gap (add docs); off-topic question flagged = system working (threshold will refuse). Same alert, two responses — like a p99 alert during a load test vs 2pm Tuesday.
2. Faithfulness vs answer_relevancy in one line each? Faithfulness = answer vs retrieved chunks only (grounding, not truth). Answer_relevancy = answer vs question (direction). A grounded answer to the wrong question scores 1.0 / low — the Day 20 floor-elements-vs-views bug as a metric.
3. How is answer_relevancy computed, and what does it need that faithfulness doesn't? Judge reverse-engineers questions from the answer, embeds them, cosine-compares to the real question — so it needs an embeddings model passed to evaluate() (LangchainEmbeddingsWrapper + all-MiniLM-L6-v2), not just the judge LLM.
4. Why does context_precision need a `reference` (ground-truth answer) per question? The judge can't grade a chunk as "relevant" without an answer key — like a unit test assertion needing an expected value. It scores whether useful chunks were retrieved AND ranked at the top (signal-to-noise of top-k).
5. Faithfulness 1.0 but relevancy 0.4 — where's the bug? Retrieval. Faithfulness 1.0 means the answer came entirely from the chunks, so off-topic answer = off-topic chunks. Confirm with the debug_floor audit.
6. Two Python indentation traps from today? (1) A block dedented one level too far runs once-after-the-loop on leaked loop variables — output can look right by accident (France was last). (2) for...else is legal Python that runs else once after the loop; an else aligned with for is almost always a misindented if/else. Habit: indentation = "how many times does this line run"; you are the closing brace.
7. Why did floor-plan relevancy read 0.788, 0.923, and 0.750 across three runs of the same code? Judge metrics are LLM calls — non-deterministic. Read trends and same-run comparisons, never single absolutes. Deterministic evals = exact unit tests; RAGAS = wobbly load tests.
8. You broke retrieval (floor question forced to category "walls") — which metric caught it? None of the judge metrics — the refused question never reached the judge (skipped row). refusal_rate went 0.0 → 0.5 while faithfulness/relevancy/precision stayed perfect and n silently dropped 2 → 1. Like error rate rising while the latency dashboard stays green — failed requests never reach the histogram. Watch refusal_rate and n, always.
9. Which layer refused the sabotaged floor question, and what proved it? Layer 2 (threshold gate). Evidence: wall-chunk distances 1.636 and 1.653, both > 1.2 — retrieve() returned [] and answer_question short-circuited before ask_revit_question. I guessed layer 3 first; the printed number flipped it. Bonus: fewer results than n_results — only 2 wall chunks exist; the query gives you what exists, not what you asked for.
10. Is collection.query() an LLM call? No — ChromaDB nearest-neighbor lookup with local embeddings (fast, free). The ONLY Claude call is ask_revit_question(); the empty-chunks short-circuit exists to guard that expensive line. Retriever = bouncer (per-chunk threshold), service = manager (empty → "I don't know" before the LLM). Redis-before-DB, in my own code.

## Day 22 — PHASE 2 START: Streaming + async Claude API
**One-liner:** Streaming is SSE — text arrives as typed events with stop_reason as the stream's status code; async is Promise.all as asyncio.gather, and the client class must match the function style.

1. What does .stream() return and how do you consume just text? A context manager (`with ... as stream`); `stream.text_stream` is a generator yielding text chunks; `flush=True` or streaming *looks* broken even when it works.
2. List the SSE event sequence for a simple response. A: message_start → content_block_start → content_block_delta (many — carries the text) → content_block_stop → message_delta (carries stop_reason + output tokens) → message_stop. text_stream is a filtered consumer on this topic; raw events are the full stream.
3. Why check stop_reason? "max_tokens" means truncated mid-answer — would tank relevancy scores with no visible error. "end_turn" = finished naturally. It's the HTTP status code of the stream: never render it, never ignore it.Text streams in content_block_delta; stop_reason arrives in message_delta at the end because the model only knows why it stopped once it stops.
4. asyncio.gather vs Promise.all — same and different? Same semantics (concurrent, ordered results, fail-fast). Different: Python spreads args with `*(...)`, and you start the event loop yourself with `asyncio.run(main())` — Node's loop is always running.
5. Bug I hit: AsyncAnthropic with sync `with` — why does it break? The async client returns awaitables/async context managers everywhere; needs `async def` + `async with` + `async for`. Mixing = treating a Promise like its value. Client class must match function style.
6. All my answers ended in "..." — API truncation? No — proved with evidence: ask() returned (text, stop_reason), all three questions showed end_turn with len 1975/1005/1141 at max_tokens=1000. The "..." was the [:60] print slice — display truncation, not API truncation. Assumed max_tokens first; printed numbers flipped it (again).
7. Prefill/decode connection to streaming? Prefill (parallel) sets TTFT — how fast the first chunk arrives; decode (sequential) sets streaming speed — how fast subsequent chunks arrive.
8. Where does this code live? chatbots/revit-chatbot/async_batch_questions.py — concurrent batch of 3 Revit questions with per-question stop_reason + length. First Phase 2 code.

## 🚢 Project 2 — RAG API over Revit Docs (SHIPPED v1 — Day 17)
**What it is:** FastAPI RAG service — `POST /ask` answers Revit questions grounded in ChromaDB docs with sources. Files: ingest.py, retriever.py, rag_service.py, app.py, prompting/revit_context_qa.py, evals.py.

1. Architecture: write path (ingest.py, idempotent upsert) vs. read path (retriever.py, per-request) — neither imports the other; app.py and evals.py share rag_service.answer_question() so evals test the production pipeline.
2. Calibrated threshold: measured distances (relevant 0.18–0.75, junk 1.69+) → chose 1.2. Threshold is an output of an experiment, not a guess.
3. Hallucination control: refusal system prompt (context-only, exact "I don't know", short answers) + empty-retrieval short-circuit that skips Claude entirely.
4. Evals: 5/5 — four grounded questions checked against expected source ids, one off-topic question required to return exactly "I don't know".
5. Remaining for v2: ~~refusal-exclusion in RAGAS evals + double-retrieval refactor~~ (done Days 18–19), ~~floor-plan category finding~~ (closed Day 20, doc6), ~~more RAGAS metrics (answer_relevancy, context_precision)~~ (done Day 21, sabotage-tested), real Autodesk doc chunks, model cost decision (opus → sonnet/haiku), proper ragas upgrade to drop the vertexai stub.

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
- faithfulness = answer vs chunks, relevancy = answer vs question
- Metric triad = pipeline stages: context_precision→retrieval(reference answer), faithfulness→grounding(retrieved chucks), answer_relevancy→direction(answer against the question)
- Refused questions never reach the judge — refusal_rate and n catch what quality metrics miss (error rate vs latency dashboard)
- Python indentation = "how many times does this line run"; you are the closing brace
## Day 23 — Multi-turn conversation state + system prompts
**One-liner:** API is stateless like REST — messages list = the conversation store you own (JWT, not server session); system prompt = header not body; growing list = cache with no eviction → sliding-window trim in pairs.

1. Where does conversation memory live in the Claude API? Nowhere on the server — the API is stateless. You re-send the full messages list every call. Memory = your list.
2. What two appends maintain the conversation? Append the user message before the call, append the assistant reply after. Forget the second and follow-ups like "give me an example of one" lose their referent.
3. Is the system prompt part of the messages list? No — separate top-level parameter, like a request header vs body. Re-sent every call but never counted in messages.
4. Why do long conversations get expensive? You pay input tokens for the ENTIRE history every call. Turn 50 re-sends 49 turns. List grows → cost grows → context window (max request body) eventually hit.
5. What's the sliding-window trim rule? Keep last N messages, trim in PAIRS — list must start with a user message and alternate roles or the API rejects it.
6. What bug does trimming cause? Amnesia, not garbage — model loses facts from evicted turns ("use the approach we agreed on" → "which approach?"). Cache eviction of a key you still needed.
7. Why did messages[-20:] break at turn 11 in multi_turn_chat.py? At send time the list always ends with user, so its length is odd (21 at turn 11). An even slice off an odd list starts with assistant → API 400. Fix: re-check the first role AFTER slicing and drop one if wrong. Re-check structural invariants after slicing, not before.
8. Send-trim vs store-trim? Trimming what you send caps API cost; the global list still grows in RAM. In a long-running service, trim (or persist) the store itself.

## Day 24 — Morning check-in (2026-08-05): Day 23 recall quiz
**One-liner:** memory = two appends (user BEFORE the call, assistant AFTER); cost grows linearly because full history = input tokens every call; even slice off odd list starts on assistant → 400.

1. Where does conversation memory live, and what maintains it? Client-side in the messages list — nowhere on the server. Maintained by two appends: append the user message BEFORE the API call, append the assistant reply AFTER. (Quiz: knew the container, missed naming the appends — re-quiz.)
2. Why does a long conversation get more expensive per call? Cause first: you pay input tokens for the ENTIRE history every call — cost grows linearly with turns until the context window. Cure second: sliding-window trim. (Quiz: gave the cure before the cause — corrected.)
3. Why must the first message be user role after trimming? List at send time always ends with user → odd length; an even slice like [-20:] drops a user turn and starts on assistant → API rejects with 400. Fix: re-check first role AFTER slicing. (Quiz: correct after correction.)
4. Still owed (evidence habit): SSE re-quiz (text = content_block_delta, stop_reason = message_delta, arrives last — dodged twice); trim-bug repro with MAX_MESSAGES=4 (shrink the load threshold to make a load-dependent bug reproducible in seconds — same trick as a 2-connection pool for pool exhaustion).
5. CORRECTION (2026-08-05, supersedes Day 23 Q7): The "400 at turn 11" claim was FALSIFIED by experiment. With the role-check disabled and MAX_MESSAGES=4, instrumentation printed "first role = assistant" and the API call SUCCEEDED — the current Messages API accepts a list starting with assistant (the old contract rejected it). The role-check fix is downgraded: defensive hygiene (start history on a user turn), not crash prevention. Both hypotheses died on printed evidence: Tushar's "always user first" AND Claude's "400 at turn 11."
6. Live amnesia demo (window=4): asked "show me all messages in order" at turn 5 — model listed only the last window and drifted off-domain (answered about warehouse management software, not Revit) because the grounding turns were evicted. Eviction of keys you still needed, observed first-hand.

## Day 24 (partial) — Structured outputs + Pydantic (2026-08-05)
**One-liner:** model output = untrusted input — define a Pydantic schema, validate at the boundary (model_validate_json), and prefill "{" so the model starts inside the JSON with no room for preamble; the API enforces nothing, your code does, at runtime.

1. What enforces the schema — the API or your code? Your code, at runtime, after the response arrives. The API returns text; Pydantic's model_validate_json is the boundary. It can fail on ANY call — that's why the validation line exists.
2. What are the two ValidationError failure modes (both hit live today)? (a) Malformed JSON — model wrapped output in ```json fences despite instructions → "expected value at line 1 column 1". (b) Schema violation — wrong type for a field → error names the exact field. Fail loud at the edge, not silently downstream (validate at controller, not DAO).
3. How does prefill fix the markdown-fence problem? End the messages list with {"role":"assistant","content":"{"} — the model CONTINUES from it, already mid-JSON, so it can't emit preamble or fences. Instructions are requests; prefill is enforcement.
4. What's the gotcha with prefill and parsing? The response EXCLUDES your prefill — re-attach the "{" before model_validate_json ("trailing characters at line 2" = you forgot; input starts at "answer": with no opening brace).
5. Where is prefill's assistant-last legal? Prefill is the one place an assistant message LAST is a feature — you're putting words in the model's mouth and it continues them.
6. What proof shows the value arrived typed? parsed.confidence == 1.0 as float (not "1.0" string) — printed from the validated object.
STILL OPEN for Day 24 continuation: delete stale un-prefixed parse line (line 28), clean run; Field constraints/validators, Optional, nested models; wire typed output into Project 2 evals.

## Day 24 (complete) — Pydantic deep dive: constraints, Optional, nested models (2026-08-07)
**One-liner:** schema = API contract for model output — Field constraints add value rules on top of type rules, Optional allows null but only = None allows absence, nested models validate the whole tree in one call with full error paths (sources.1.score).

1. confidence: float vs confidence: float = Field(ge=0.0, le=1.0)? Bare float catches type errors only (1.7 passes). Field adds value rules — planted 1.7 failed with less_than_equal naming field, rule, and value. Joi.number() vs Joi.number().min(0).max(1).
2. Optional[str] without = None — can the key be missing? NO. Two separate permissions: Optional allows the VALUE to be null; = None allows the KEY to be absent. Optional alone still throws type=missing on an absent key. Joi: .allow(null) vs .optional() with default.
3. Design rule for optional fields? Required-by-default (NOT NULL). Optional only for legitimate absence — otherwise you just move the failure downstream to whoever reads None.
4. How do you test the missing-field case? Feed absence — a happy-path run proves nothing. (Caught offering a topics-present run as proof for the topics-absent case; corrected, then predicted the required-field failure and ran it: error type=missing.)
5. How does nested validation report failures? Full path into the DATA tree, not a code line: sources.1.score = index 1 (zero-based) of the sources list, field score. One model_validate_json call recurses the whole tree. This shape IS Project 2's answer+chunks response.
6. What did the stale-line cleanup teach? When a fix replaces a line, delete the old line in the same edit — last write silently wins. (Dead/commented code left behind caught 3x this session.)
7. EXERCISE (verified with pasted output): nested_practice.py — valid JSON parsed; planted bad JSON failed at sources.1.score. structured_output.py restored to minimal known-good; caveat=None default observed live.

## Day 25 — Morning check-in (2026-08-10): Day 24 recall quiz + cold re-quizzes
**One-liner:** expected traceback = passing test; stop_reason doesn't exist until the model stops — the stop CREATES the reason (HTTP trailer, in message_delta).

1. Q1 constraints: PASS — type check vs value rules, Joi analogy held.
2. Q2 Optional/= None: FAILED twice, never produced the clean two-part sentence unprompted (said "optional means it can be missing" — backwards). STILL WEAK — re-quiz cold next session.
3. Q3 nested paths: half — knew sources.1.score, framed it as "line of code"; corrected to data-tree path (JSON path, not stack trace).
4. Cold A (stop_reason why): closed with cleanup — event right (message_delta), but called it "reason of failure" (end_turn is the happy case — it's the stream's status code, 200 is also a status) and first said "can't stop without knowing why" (backwards: the stop creates the reason). Second attempt landed: mid-stream the stop hasn't happened, so the reason doesn't exist yet.
5. Cold B (SSE event roles): PASS after 3 prior skips — full lifecycle recited in order; text = content_block_delta, stop_reason = message_delta. CLOSED.
6. Carried-forward (Saturday 2026-08-08) still unverified: evals.py France-position fix + Phase 1 recap out loud.

## Day 25 — Typed pipeline responses: tuple → Pydantic DTO across all callers (2026-08-10)
**One-liner:** answer_question now returns one validated RagResponse (answer + nested list[Source]) instead of a 3-tuple — every branch returns the same contract, callers read fields by name, and new fields cost nothing.

1. What was wrong with returning (answer, sources, chunks)? Nothing describes or validates the shape — callers must know order and arity. Day 19 proved the cost: adding a third value broke all three callers with ValueError. A tuple is res.send([a,b,c]); a Pydantic model is a DTO with a declared contract.
2. Why must BOTH return statements return the same type? The refusal branch and the happy branch are one promise. Return RagResponse on one and a tuple on the other and resp.answer crashes only when a refusal happens — passes every test, breaks at 3am on the one off-topic question. A function's return type is a promise made by every branch.
3. What proved the refactor actually took effect? evals.py RAN. Identical 5/5 output is weak evidence (it's also what you'd see if nothing changed), but any caller still unpacking three values would have died on TypeError: cannot unpack non-iterable RagResponse before case 1. Silent pass across three callers is the real signal.
4. Why did Source need a text field? ragas_evals.py grades faithfulness against chunk TEXT — the response object is the pipeline's audit log (Day 19). Claude's first schema had id + distance only, designed from two callers and never checked against the third; RAGAS would have had nothing to grade. Design the DTO against every consumer, not the loudest one.
5. How did each caller change? app.py: resp.answer + [s.id for s in resp.sources]. evals.py: same, unpacking removed. ragas_evals.py: resp.answer + [s.text for s in resp.sources]. Each takes only what it needs, by name, and none care that the others exist.
6. Carried-forward items CLOSED this session: debug_floor.py audit loop restored (sabotage query + live category filter deleted) — retrieval verified healthy, doc3/doc5/doc2/doc4 all rank #1, France correctly flagged ⚠️ mid-list, which also proved the Day 21 indentation bug is gone.
7. Why did n_results=3 return only 2 rows? The WHERE filter runs BEFORE vector search — only 2 docs were tagged "floors", so only 2 candidates could be ranked. The query gives you what exists after filtering, not what you asked for (Day 7 rule, Day 21 finding).
8. Dead-code residue: first session it did NOT appear — the unused sources = [c["id"] ...] line was deleted in the same edit as the fix. Pattern broken after 4 sessions.

## Day 25 (exercise + code review) — the DTO payoff, and where the contract still leaks (2026-08-10)
**One-liner:** Adding category to RagResponse broke zero callers (Day 19's equivalent broke all three) — but the review found the contract is only half-kept: both branches return the same type, not the same fields.

1. What did the exercise prove? Added category: str | None = None to RagResponse, set it in answer_question, ran all 3 callers untouched — 5/5 green. Adding a field to a DTO is backward-compatible; adding a slot to a tuple is a breaking change for every caller. Same change, opposite cost.
2. P1 bug found in review — what's wrong with the refusal branch? It returns RagResponse(answer="I don't know", sources=[]) and never sets category, while the happy path does. Ask with category="floors", get refused, and the response claims category=None — a lie. A contract is the shape AND the values; anything grouping by category under-counts exactly the rows you most want to see.
3. P2 tech debt — why is "I don't know" dangerous as a magic string? rag_service produces it, ragas_evals detects refusals by comparing against it. Reword it in one place and refusal_rate silently reports 0.0 forever — no error, just a dead metric. Fix: a refused: bool field set at the branch that knows. The producer declares refusal; consumers never parse prose to infer it.
4. P3 — why is expected_id in sources a weak assertion? Membership, not rank: it passes whether the right doc ranked 1st or 2nd. debug_floor.py shows every expected doc currently ranks #1, so sources[0] == expected_id would catch a rank regression this suite sleeps through. Widening an assertion from equals-first to contains keeps tests green while catching less.

## Day 25 (close) — P2 proven live: rewording the refusal string broke a consumer (2026-08-10)
**One-liner:** Changed the refusal message to "I don't know based on the available docs." and instantly broke evals.py's == assertion while ragas_evals.py's substring match sailed through — the exact coupling failure P2 predicted, demonstrated by accident within the hour.

1. What is P2 actually about? Not the behavior — "no chunks → I don't know" is correct. It's that OTHER code detects the refusal by string-matching an English sentence produced in a different module. Checking a response body for the word "error" instead of reading the HTTP status code.
2. What broke when the message was reworded? evals.py asserts answer.strip() == "I don't know" — the France case went red. Predicted an hour earlier, then triggered for real by a legitimate UX improvement.
3. Why is ragas_evals.py's "i don't know" in answer.lower() NOT the fix? It survived this reword, which is exactly what makes it dangerous — it tolerates the coupling silently. And it introduces the opposite failure: a real answer like "I don't know the exact Revit version, but use the Door tool" gets counted as a refusal. == misses refusals (silent under-count); in invents them (silent over-count). Both guess intent from prose.
4. Loud break vs silent tolerance? evals.py's == failed visibly — a gift. ragas_evals.py passed while staying wrong — the bug that reaches production. Prefer the assertion that breaks when the contract changes.
5. The fix? refused: bool on RagResponse, set True at the branch that decides; consumers read the flag. The producer declares the state; consumers never parse prose to infer it. Java anchor: catch (NotFoundException e) instead of e.getMessage().includes("not found").
6. Verification-of-own-work gap (3rd time today): declared P1 fixed while the file still read category=None; grep proved otherwise. Strong evidence habit when debugging, switches off when confirming his own fixes.
