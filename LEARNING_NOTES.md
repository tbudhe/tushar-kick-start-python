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

## Day 24 — Structured Outputs & Pydantic
**One-liner:** Model output is untrusted input — define a Pydantic schema, validate at the boundary, prefill "{" to force mid-JSON, and use constraints, Optional and nesting to turn the schema into a real contract.

1. What enforces the schema — the API or your code? Your code, at runtime, after the response arrives. The API returns text; model_validate_json is the boundary. It can fail on ANY call — that's why the validation line exists.
2. What are the two ValidationError failure modes? (a) Malformed JSON — the model wrapped output in ```json fences despite instructions. (b) Schema violation — wrong type for a field, error names the exact field. Fail loud at the edge, not silently downstream (validate at the controller, not the DAO).
3. How does prefill fix the markdown-fence problem? End the messages list with {"role":"assistant","content":"{"} — the model CONTINUES from it, already mid-JSON, so it can't emit preamble or fences. Instructions are requests; prefill is enforcement.
4. What's the prefill parsing gotcha? The response EXCLUDES your prefill — re-attach the "{" before parsing, or you get "trailing characters at line 2" with input starting at "answer": and no opening brace.
5. Where is an assistant message legal as the LAST message? Prefill — the one place it's a feature. You're putting words in the model's mouth and it continues them.
6. confidence: float vs confidence: float = Field(ge=0.0, le=1.0)? Bare float catches type errors only (1.7 passes). Field adds value rules — planted 1.7 failed with less_than_equal naming field, rule and value. Joi.number() vs Joi.number().min(0).max(1).
7. Optional[str] without = None — can the key be missing? NO. Two separate permissions: Optional allows the VALUE to be null; = None allows the KEY to be absent. Optional alone still throws type=missing.
8. Design rule for optional fields? Required-by-default (NOT NULL). Optional only for legitimate absence — otherwise you move the failure downstream to whoever reads None.
9. How do you test the missing-field case? Feed absence. A happy-path run proves nothing (caught offering a topics-present run as proof for the topics-absent case).
10. How does nested validation report failures? Full path into the DATA tree, not a code line: sources.1.score = index 1 (zero-based) of the sources list, field score. One call recurses the whole tree — this shape IS Project 2's answer+chunks response.
11. What did the stale-line cleanup teach? When a fix replaces a line, delete the old line in the same edit — last write silently wins.
12. Day 23 correction carried in: the "400 at turn 11" trim claim was FALSIFIED by experiment — instrumentation printed "first role = assistant" and the call SUCCEEDED. The role-check is defensive hygiene, not crash prevention. Both hypotheses died on printed evidence, including the teacher's.
13. Exercises: structured_output.py (constraints, prefill, clean run with caveat=None observed live) and nested_practice.py (valid JSON parsed; planted bad JSON failed at sources.1.score).

## Day 25 — Typed Pipeline Responses & First Code Review
**One-liner:** answer_question returns one validated RagResponse (answer + nested list[Source]) instead of a 3-tuple — every branch returns the same contract, callers read fields by name, new fields cost nothing, and the review found the contract still leaking through a magic string.

1. What was wrong with returning (answer, sources, chunks)? Nothing describes or validates the shape — callers must know order and arity. Day 19 proved the cost: adding a third value broke all three callers. A tuple is res.send([a,b,c]); a Pydantic model is a DTO with a declared contract.
2. Why must BOTH return statements return the same type? The refusal branch and the happy branch are one promise. Return a DTO on one and a tuple on the other and resp.answer crashes only when a refusal happens — passes every test, breaks at 3am on the one off-topic question.
3. What proved the refactor took effect? evals.py RAN. Identical 5/5 output is weak evidence (it's also what you'd see if nothing changed), but any caller still unpacking three values would have died on TypeError before case 1.
4. Why did Source need a text field? ragas_evals.py grades faithfulness against chunk TEXT — the response object is the pipeline's audit log. The first schema had id + distance only, designed from two callers and never checked against the third. Design the DTO against every consumer, not the loudest one.
5. How did each caller change? app.py: resp.answer + [s.id for s in resp.sources]. evals.py: same, unpacking removed. ragas_evals.py: resp.answer + [s.text for s in resp.sources]. Each takes what it needs, by name.
6. What did adding category prove? Zero callers changed, suite stayed green. Adding a field to a DTO is backward-compatible; adding a slot to a tuple is a breaking change for everyone. Same change, opposite cost.
7. Same type is not the same contract — what was P1? The refusal branch hardcoded category=None while the happy path passed the real value, so a refused "floors" question reported no category. Branches must populate the same FIELDS, not just return the same type.
8. What is P2 actually about? Not the behavior — "no chunks → I don't know" is correct. It's that other modules DETECT the refusal by string-matching an English sentence. Checking a response body for the word "error" instead of reading the status code.
9. P2 proven live: the refusal message was reworded to "I don't know based on the available docs." and evals.py's == assertion went red immediately, while ragas_evals.py's substring match sailed through. Predicted an hour earlier, then triggered for real.
10. Why isn't "i don't know" in answer.lower() the fix? It survived the reword, which is what makes it dangerous — it tolerates the coupling silently. And it invents refusals: "I don't know the exact Revit version, but use the Door tool" is a real answer that would be counted as a refusal. == under-counts, in over-counts; both guess intent from prose.
11. Loud break vs silent tolerance? evals.py failed visibly — a gift. ragas_evals.py passed while staying wrong — the bug that reaches production. Prefer the assertion that breaks when the contract changes. Java anchor: catch (NotFoundException e) instead of e.getMessage().includes("not found").
12. Why did n_results=3 return only 2 rows? The WHERE filter runs BEFORE vector search — only 2 docs were tagged "floors", so only 2 candidates could be ranked. The query gives you what exists after filtering.
13. Why is expected_id in sources a weak assertion? Membership, not rank — it passes whether the right doc ranked 1st or 2nd. sources[0] == expected_id catches a rank regression the old suite slept through.
14. Why must the refusal case also assert sources == []? It pins WHICH layer refused. Layer 2 (threshold) returns no chunks and never calls Claude; layer 3 (LLM refusal) has chunks and costs an API call. Same answer text, completely different systems.
15. Why must debug_floor.py import N_RESULTS and THRESHOLD? Retyping them is how an audit starts lying — it was printing top-3 unfiltered while production took top-2 at 1.2. One pipeline, many importers (Day 19), applied to the debug tool.
16. Verification-of-own-work gap (3 incidents): declared P1 fixed while the file still read category=None; predicted "all tests pass" for a refactor that would have crashed; offered a green evals.py as proof for a debug_floor.py question. Evidence habit is strong when debugging, switches off when confirming his own fixes.

## Day 26 — Tool Use / Function Calling in Production
**One-liner:** The tool loop is `while stop_reason == "tool_use"` — declare tools like an OpenAPI spec, the model requests by name, my code dispatches and replies with tool_result + tool_use_id (correlation ID), results ride back as a user message, and we go around until end_turn; agents are this loop with a bigger catalog.

1. Why can't tool use be a single if-statement instead of a loop? The model may need tool B after seeing tool A's result — round-trip count is unknown in advance. Proven live: one question cost three API calls (tool_use → tool_use → end_turn), sequential because the second call depended on the first's result.
2. What does the tool schema's description field actually do? It's prompt engineering, not documentation — the model routes on those sentences to decide when to call the tool. Vague or inverted description = wrong tool picked or skipped, like bad swagger docs causing client misuse.
3. input_schema vs Pydantic — same JSON Schema idea, what's the difference? Direction. input_schema tells the model what MY tool accepts; Pydantic validates what the model sends ME. And the schema is a request, not a guarantee — tool functions still validate (model output = untrusted input, even mid-tool-call).
4. Is stop_reason a streaming feature? No — it's on every response. Streaming only changes WHERE it arrives (final message_delta, because the reason doesn't exist until the model stops). New value today: "tool_use" — a control-flow signal steering the loop, not a log line.
5. What's in response.content when stop_reason == "tool_use"? A list of tool_use blocks, each with id, name, and input (already a dict, not a JSON string). My job: dispatch TOOL_FUNCTIONS[block.name](**block.input), append tool_result blocks echoing tool_use_id, send them back as role="user", loop.
6. Why does tool_use_id exist? One turn can request multiple tools at once — the ID pairs each result to the call that produced it. Correlation ID, same as a Kafka reply carrying the request's key.
7. RAG vs tool use in one contrast? RAG = push — my code decides context up front and stuffs the prompt (cache-aside). Tool use = pull — the model decides mid-conversation what to fetch. Agents (Phase 3) = this loop + a bigger tool catalog.
8. Schema bugs made this session (2 inversions): get_stock_price declared length/width params (copied geometry example); get_company_name's description described the reverse lookup and its property was named for the OUTPUT. Prevention rule: say the signature out loud — "takes a ticker, returns a name" — then transcribe; the schema should never contain a word the signature doesn't.
9. Code bugs made this session: scripted the future (response.content typed inside the call that CREATES response — the transcript is grown by the loop, never hand-written); wrote the REPL loop where the tool loop belonged (API called once = the single if-statement we said it can't be); get_company_name took a name and returned {ticker: name} with ticker undefined.
10. Exercise verified with printed output: tool_loop.py — two canned-dict tools, dispatch dict, while-True loop; stop_reason sequence tool_use → tool_use → end_turn; model confirmed ticker via get_company_name before calling get_stock_price (dependency chain = sequential turns; independent needs = possible parallel calls in one turn, which is what tool_use_id is for).
11. Bonus: VS Code debugpy setup — launch.json with integratedTerminal (input() hangs in debug console) and cwd for load_dotenv; breakpoints on the messages.append lines to watch the transcript grow per iteration.

Quiz rotation pick: Day 24 cold — Optional[str] vs = None PASSED after two prior failures (value-may-be-null vs key-may-be-absent, Joi analogy correct).

## Day 27 — Tool Errors and Input Validation in the Loop
**One-liner:** A tool that RAISES and a tool called with BAD ARGUMENTS end the same way — a tool_result with is_error: True, written as a message for the model to read — because the protocol forbids leaving any tool_use unanswered.

1. Why not let a tool exception propagate out of the loop? The model is a caller sitting mid-conversation waiting on a response. Escaping with the exception kills the conversation and throws away a participant that could have recovered. Node anchor: unhandled promise rejection crashing the process vs. catching it and returning { ok: false, error } to a caller who can retry or degrade.
2. What is the shape of an error result? Identical to a success — same tool_result type, same tool_use_id, content as a string — plus is_error: True. is_error is a FIELD, not an exception. Producer declares state in a field; consumers never parse prose (Day 25, applied to the model as the consumer).
3. Where does the try/except go? Around the SINGLE tool call, not around the loop. Wrapping the loop means one failing tool takes down the sibling tools requested in the same turn.
4. Why is the error string prompt engineering? The model READS it and decides what to do next. "Tool failed: KeyError" is useless; "unknown ticker 'GOOGL' — known: ['AAPL','MSFT']" gets a clean stop or a corrected retry. Same instinct as the description field (Day 26).
5. Why never send a raw traceback? It leaks file paths, internal function names, sometimes connection strings into a context window that may be logged, cached, or shown to a user. Model output = untrusted input; MY internals = untrusted OUTPUT. The boundary cuts both ways.
6. Three tools requested and the second raises — how many tool_results? Three. One per tool_use_id, each with its own is_error. Partial failure is normal; the model handles it as long as every call gets an answer.
7. Why is block.input untrusted? input_schema is a request, not a guarantee. TOOL_FUNCTIONS[name](**block.input) splats a dict I did not build — an unexpected key is an instant TypeError before the function body runs. Pydantic at the boundary turns bad input into a conversation instead of a crash.
8. Which direction does each schema point? input_schema = what I accept, going OUT to the model. Pydantic model = validate what came back IN. Same JSON Schema idea, opposite arrows.
9. Why can't I just skip the tool_result for a failed call? PROTOCOL RULE — every tool_use block must be answered in the next message or the request is rejected. An unanswered correlation ID is a broken exchange, not a silent no-op. This is exactly WHY errors must be data: there is no "skip it" branch available.
10. Bug made live #1 — the `**` splat: wrote TOOL_FUNCTIONS[block.name](**args.ticker) and got "argument after ** must be a mapping, not str". After model_validate, args is an OBJECT; args.ticker reaches inside and pulls out the string. Fix: pass positionally, or **args.model_dump() to go back to a dict. Rule: when you see **x, say out loud "x must be a dict" — a dotted expression naming one field is a value, not a dict.
11. Bug made live #2 — the SENTINEL STRING, and the best finding of the session. get_company_name used NAMES.get(ticker, "unknown ticker"), which CANNOT fail, so failures shipped as 'content': 'unknown ticker', 'is_error': False. The model was told "success, and the answer is the phrase 'unknown ticker'" and started guessing: GOOGL → GOOG → still going when the crash stopped it. Day 25's own rule, violated three weeks after writing it down.
12. The A/B that proves point 4: same model, same question, one variable. With the sentinel string → 3+ iterations of ticker guessing. With raise + is_error: True + "known: ['AAPL','MSFT']" → ONE call, then a clean end_turn telling the user which companies are available and offering alternatives. Error message quality is a control on model behavior, measured in API calls.
13. except ordering matters: ValidationError BEFORE bare Exception. ValidationError is a subclass; a bare `except Exception` above it silently swallows the validation case and you lose the distinction between "bad arguments" and "tool blew up".
14. Free finding from the failed run: the loop has no ceiling. A model receiving unhelpful results keeps trying, and every iteration is a paid API call — an unbounded while True over a paid API is a production incident. Max-iteration guard = Day 28.
15. Exercise status: is_error: True verified in the transcript, exception path verified, final assistant text printed and graceful. NOT yet done — the sabotage step (force block.input = {"ticker": ["AAPL"]} to prove the ValidationError branch fires instead of a TypeError), and tool schema line 22 is STILL inverted (fifth direction inversion; the run passed only because the user prompt spelled out the tool order).

Quiz rotation pick: Day 20 COLD — FAILED. Named RAGAS metrics (refusal_rate, answer_relevancy, context_precision) instead of the three pipeline mechanisms. Metrics MEASURE quality; they do not CAUSE refusals. Correct: empty filter → distance gate → LLM refusal prompt, and the FIRST thing printed is the raw collection.query COUNT, because if it is zero there are no distances to look at. Re-ask ~2026-08-21.

Session pattern named (new weak spot): ADJACENT VOCABULARY. Every wrong answer used real terms from the correct neighbourhood — TOOL_FUNCTIONS for "why a loop", stop_reason for "how does a result go back", RAGAS metrics for "what causes a refusal". Drill: before answering, name the MOMENT IN TIME the question is about.

## Day 28 — Max-Iteration Guards: Tool Loop → Agent Skeleton
**One-liner:** An agent is the tool loop plus a budget — `for iteration in range(MAX_ITERATIONS)` replaces `while True`, the model still exits normally via stop_reason, and when the budget dies give_up() makes a forced landing (one final call with tools DISABLED) instead of a crash.

1. Why is an unbounded while True over a paid API a production incident? Every lap is a paid call, and a model receiving unhelpful results keeps trying — on Day 27 only a crash stopped the GOOGL→GOOG guessing spiral. Node anchor: a consumer with no max.poll limit and no circuit breaker — Walmart would never ship it.
2. What turns a tool loop into an agent? Three additions: an iteration ceiling (budget), a bigger tool catalog, and a goal it works toward across multiple steps. No magic — tool_loop.py was already 90% of an agent.
3. Two exits, two deciders: `stop_reason != "tool_use"` = the MODEL decides it is done (normal path, unchanged from Day 26); range exhausted = I decide it has spent enough. The model steers, I hold the budget.
4. give_up() design = forced landing: one final call with tools disabled, so the model MUST answer in text from whatever it already collected. Crash / partial transcript / forced landing were the options; forced landing is the production pattern.
5. The ceiling is a BACKSTOP, not a fix. With the sentinel bug still in place, MAX_ITERATIONS=10 stops the spiral after 10 PAID calls — error-message quality is the fix, the guard is the circuit breaker. They are layers, not alternatives.
6. Sabotage test verified with printed output: MAX_ITERATIONS=1 + a two-tool question → BOTH tools ran in ONE iteration (get_company_name and get_stock_price both take the same ticker — independent needs = parallel calls in one turn, Day 26 rule seen live), then the guard fired and give_up() produced a useful final text including $189.50 and an honest "ran out of tool-call attempts". Closes the carried item: AAPL's price finally appeared in FINAL assistant text.
7. Lesson re-learned live: the first agent_loop.py run proved the Day 27 error-message fix (one call, clean end_turn) — the new guard code never executed. Happy-path run ≠ guard verified. To test the ceiling, HIT the ceiling.

Quiz results (Day 27 + cold Day 20 RE-ASK): Q1 protocol rule PASS (every tool_use answered or request rejected, correlation ID). Q2 try placement PARTIAL — location right (single call), but the sibling-tools failure mode not retrieved even on retry. Q3 sentinel mechanics FAILED — could paste the correct fix but not articulate WHY is_error never fired (no raise → except never runs → field stays False; a function that cannot fail cannot report failure). Q4 Day 20 RE-ASK: the three layers PASSED in order (empty WHERE filter → distance gate → LLM refusal prompt) after a cold fail on 2026-08-14 — but the FIRST print (raw collection.query COUNT) was missed again. New pattern named: answered a check question with a RUN instead of a SENTENCE three times — the recall gap wearing a new coat.

Quiz rotation pick: Day 20 RE-ASK — layers PASSED, first-print still owed (~2026-08-20 with Q2/Q3 misses).

PLAN CHANGE (agreed 2026-08-17): after Phase 2 completes, ONE FULL WEEK of Phase 1 + Phase 2 revision before Phase 3 starts.

## Day 29 — Multi-Step Planning: Dependency Chains (cont. next session)
**One-liner:** A dependency chain only exists if the model CANNOT produce tool B's argument without tool A's output — world knowledge is a bypass (the model knows Apple→AAPL from pretraining, so no lookup tool gets called), and a chain of N dependent tools costs N sequential iterations because all arguments in one turn must be written before any tool runs.

1. ValidationError take-home VERIFIED: forced block.input = {"ticker": ["AAPL"]} → the ValidationError branch fired with "Invalid arguments: 1 validation error for StockPriceInput / ticker / Input should be a valid string [type=string_type, input_value=['AAPL'], input_type=list]". Loop continued — raising is not crashing; the boundary turns exceptions into error contracts.
2. How to tell Pydantic's branch from a TypeError: SPECIFICITY. Pydantic errors talk about the CONTRACT — schema name (StockPriceInput), field name (ticker), machine-readable type tag (string_type). A TypeError talks about Python INTERNALS ("'list' object has no attribute 'upper'") with no idea a ticker was involved. 400-with-field-message vs 500-with-stack-trace.
3. The sabotage payload {"ticker": ["AAPL"]} is NOT "passing an array instead of a map" — the outer dict is fine; the FIELD VALUE is a list where the schema promises str. "Body malformed" and "body fine, one field fails validation" are different conversations.
4. Why can't the model call get_ticker_symbol and get_stock_price in one turn when the user says "Apple"? Because all tool arguments in a single response are written BEFORE any tool executes — there is no "pipe A's output into B" within a turn. B's argument = A's output ⇒ sequential turns, one iteration per link. (Mental model 72, first half, now understood.)
5. Why did the live Apple run still batch both calls in one turn? The model filled ticker='AAPL' from PRETRAINING — world knowledge bypassed the dependency. Production warning: the model will "helpfully" guess internal IDs (Autodesk hub IDs) instead of calling the lookup tool, and sometimes guess wrong.
6. Kafka anchor: request chaining / orchestration — correlation-ID request-reply where B's request is built from A's response, so B must run after A completes. Sequential by construction.
7. Why get_ticker_symbol when get_company_name exists? DIRECTION. get_company_name is ticker→name; the user gave a name and get_stock_price needs a ticker: name→ticker, the opposite arrow. An index on ticker→name can't serve a name→ticker query — same data, wrong direction. (Direction-inversion weak spot, now appearing in system design, not just descriptions.)
8. A tool needs THREE registrations: the schema entry in TOOLS, the function, and the TOOL_FUNCTIONS dispatch entry. Exercise run failed because only the DATA was added (and into the wrong dict — name→ticker mapping stuffed into NAMES, which is ticker→name: two contracts in one map). Model had no lookup tool, guessed "YUNextGenAI" as a ticker, got the good Day 27 error message, bailed gracefully — accidentally proving error-message quality, not the chain.
9. Found in file: get_company_minimum_stock_price — self-added, broken 3 ways (description promises a price filter the schema doesn't take; returns a name, not a price; NAMES[ticker] > 150 compares str to int → TypeError → except Exception branch). Decision: DELETE all three registrations; design tools on paper first — a bad description misleads the model on EVERY call.
10. agent_loop.py line-22 description inversion: FIXED (verified by reading the file). tool_loop.py still owed.
11. EXERCISE NOT COMPLETED — session ended early. Day 30 finishes it: add get_ticker_symbol (3 registrations, param company_name NOT ticker), TICKERS dict for the new direction, print iteration numbers, ask "What's the current stock price of YUNextGenAI?" — expect iteration 0 = lookup, iteration 1 = price, iteration 2 = final text $42.00. Landmine left in deliberately: StockPriceInput validates ALL tools but requires ticker; the lookup tool sends company_name → per-tool Pydantic models (carried item 4) will fire on iteration 0.

Quiz results (Day 28 + cold Day 24): Q1 sentinel-spiral-with-guard PARTIAL (shape right, never walked the timeline: 10 paid calls, guard fires, give_up lands, user sees an okay answer and nobody notices the 10x cost). Q2 parallel-calls PARTIAL (gave the code half — handle_tools loops over blocks — missed the model half: independent args → model batches both in ONE response). Q3 why-tools-disabled FAILED (said where give_up lives, not why: tools attached ⇒ model can answer with another tool_use ⇒ either budget violated or unanswered tool_use_id ⇒ stripping tools forces end_turn). Re-ask ~2026-08-21.

Quiz rotation pick: Day 24 cold — Optional vs = None PASSED clean, unassisted, in a SENTENCE ("Optional allows the VALUE to be null; = None allows the KEY to be absent; Optional alone still throws type=missing"). Weak spot CLOSED after two prior failures. Notably: the one pure-sentence answer was the one PASS; the code-reaching answers were the misses.

Sentences-vs-runs pattern: recurred twice (pasted run when asked for the one-sentence proof; second attempt attributed Pydantic's own artifacts to the TypeError side). The evidence-vs-explanation drill continues.

COACHING RULE (agreed 2026-08-18, from end-of-session feedback): before EVERY exercise, state the GOAL first — what the final output/printout should look like — then give a NUMBERED step list, one step at a time, confirming each before the next. No destination-in-prose.

## Day 30 — Multi-Step Planning: The Chain Runs (cont.)
**One-liner:** The chain ran end-to-end once the catalog described both directions AND each tool had its own validation contract — two links cost two iterations plus a landing (MAX_ITERATIONS ≥ N+1 verified live), and the landmine proved that error text is prompt engineering even when the error is your own bug.

**The goal printout (achieved, verbatim):**
```
iteration: 0
tool call: get_ticker_symbol {'company_name': 'YUNextGenAI'}
tool result: YNXT
iteration: 1
tool call: get_stock_price {'ticker': 'YNXT'}
tool result: 42.0
iteration: 2
The current stock price of **YUNextGenAI** (ticker: **YNXT**) is **$42.00**.
```

1. THE LANDMINE FIRED as planted on Day 27: `StockPriceInput.model_validate(block.input)` ran for EVERY tool, so `get_ticker_symbol`'s perfectly valid `{'company_name': 'YUNextGenAI'}` was rejected — "ticker / Field required [type=missing]". One validator, two contracts.
2. THE SUBTLE HORROR: after receiving "ticker Field required" twice, the model OBEYED the error text — abandoned the lookup tool and called `get_stock_price(ticker='YUNextGenAI')`, stuffing a company name into a ticker field. A well-formed, actionable, WRONG error message steered the model into a wall for 3 paid calls. Error text is prompt engineering even when the error is your bug.
3. DIAGNOSIS CHAIN (run in order, cheapest evidence first): model RETRYING the same call ⇒ its tool_result was an error → add `print("tool result:", result)` → read the error's vocabulary (Pydantic contract words = boundary rejection, validation never reached the function) → fix the boundary.
4. THE FIX — per-tool validators, dispatched like functions (the FOURTH registry, same key as the other three):
```python
class TickerSymbolInput(BaseModel):
    company_name: str

INPUT_MODELS = {
    "get_stock_price": StockPriceInput,
    "get_company_name": StockPriceInput,   # legitimately shared — same contract (ticker in)
    "get_ticker_symbol": TickerSymbolInput,
}

# in handle_tools — dispatched, not hardcoded:
args = INPUT_MODELS[block.name].model_validate(block.input)
```
Sharing a model across tools is legal ONLY when the contracts truly match (Tushar spotted get_company_name qualifies); the crime is forcing one contract on a tool with a different one.
5. BONUS SELF-FOUND BUG: `get_stock_price` contained a hardcoded `if ticker != "AAPL":` — an allowlist masquerading as a lookup; the PRICES dict may as well not exist. Fix makes data the authority, and the error message teaches the model what IS valid:
```python
def get_stock_price(ticker):
    if ticker not in PRICES:
        raise ValueError(f"unknown ticker '{ticker}'. Known tickers: {list(PRICES)}")
    return PRICES[ticker]
```
Verdict on the YNXT failure: BOTH a code bug (hardcode) and a data gap (YNXT missing from PRICES).
6. Chain math verified live: 2 dependent links + 1 landing turn = 3 iterations; the model planned the chain UNPROMPTED once the catalog described both directions.
7. Registrations, final form: a tool needs THREE — schema (TOOLS, the only part the model sees), function, dispatch (TOOL_FUNCTIONS) — plus a FOURTH in a hardened loop: its validator (INPUT_MODELS). All keyed by the same name. (Failed cold at quiz, relearned by hands, end-of-day re-ask still swapped function for validator — re-ask cold next session.)

Quiz results (Day 29 + cold Day 20): Q1 chain-vs-parallel PASSED (after one push for the timing half). Q2 three-registrations FAILED. Q3 Pydantic-vs-TypeError PARTIAL (code instead of the "specificity" sentence). Q4 COLD Day 20 PARTIAL — layer right (WHERE filter), count-print missed a THIRD time (answered the inputs N_RESULTS/THRESHOLD, not the output COUNT). Drill: "layer = filter, print = count."

Sentences-vs-code pattern: worst day yet — ≥4 code-instead-of-sentence answers. Rule stands: a run/code block is evidence; a "why" question wants a sentence.

NEW RULE (Tushar's request, 2026-08-20): quiz capped at MAX 5 QUESTIONS PER SESSION, total — default 2 on the last day + 1 cold pick + up to 2 follow-ups.

CLOSED: Day 29 exercise; per-tool Pydantic models (carried since Day 27); get_company_minimum_stock_price deleted (all 3 registrations); AAPL allowlist bug.
CARRIED: Phase 1 out-loud recap; tool_loop.py line-22 description inversion; trim-experiment + prefill re-attach re-test.
Next: Day 31 — LangChain intro (map TOOLS/TOOL_FUNCTIONS/INPUT_MODELS/budget onto framework abstractions) or Project 2 hardening.

## Day 31 — LangChain Intro: @tool Collapses the Four Registries
**One-liner:** `@tool` generates all four registries — schema, function, dispatch, validator — from the one function signature, so the Day 30 wrong-validator bug is structurally impossible: no separate copies left to disagree.

**The goal printout (achieved — `exercises/day31_langchain_tool.py`, no API call, no cost):**
```
=== WHAT @tool GENERATED ===
TOOL: get_ticker_symbol
  description: Look up the ticker symbol for a company name.
  args schema: {'company_name': {'title': 'Company Name', 'type': 'string'}}
TOOL: get_stock_price
  description: Get the current stock price for a ticker symbol.
  args schema: {'ticker': {'title': 'Ticker', 'type': 'string'}}

=== THE DAY 30 CHAIN, VIA LANGCHAIN ===
step 1: YUNextGenAI -> YNXT
step 2: YNXT -> 42.0

=== THE FREE VALIDATOR ===
bad input rejected: 1 validation error ... company_name Field required
```

1. SPRING ANALOGY: the hand-built loop was raw servlets; `@tool` is `@RestController` — nothing was removed, it was automated. Validation still runs on every invoke; you just never write or import Pydantic (like `@Valid` vs hand-rolled request checks).
2. ONE SOURCE OF TRUTH: schema AND validator are both generated from the type hints; description comes from the docstring or `@tool(description=...)` (Javadoc vs `@Operation` — same output, prefer the one living with the code). Day 30's bug — two hand-maintained copies of "what does this tool accept" drifting apart — cannot happen when there are no copies.
3. DIRECTION INVERSION FIRED LIVE (weak spot #7 stays open): wrote `get_stock_price` description as "Look up the ticker symbol to get prices" — both tools then OPENED with the same words, exactly the ambiguous catalog that misleads a model. Fix: say the arrow out loud, then write it — "Get the current stock price for a ticker symbol."
4. `.invoke({"company_name": ...})` on the tool object = the dispatch dict absorbed; the input is a DICT because that is the same shape a model's `tool_use` arguments arrive in. The Day 30 chain re-ran by hand in 4 lines: B's argument IS A's output.
5. THE FREE VALIDATOR: feeding `{"wrong_field": ...}` produced "company_name Field required" — specific, actionable, AND correct, because the validator is generated from the tool's own signature and structurally cannot belong to a different tool. Contrast with Day 30, where the same-shaped error was wrong and steered the model into the ditch.

Quiz results (Day 30 topic + cold Day 28): Day 30 Q1 error-text-is-prompt-engineering LANDED after 3 nudges (initially described the bug cause, not the model's obedient behavior). Q2 four-registries: named 3 of 4 in code — missed the function itself; final check ("why does the model only need TOOLS?") missed — answer: the model never runs code, it only WRITES a JSON tool_use request, and TOOLS is the menu of requests it may write. Re-ask both cold. Day 28 cold give_up()-WHY: PASSED cleanly, exact mechanism sentence — weak spot CLOSED. Sentences-vs-code recurred (skipped the Step 5 prediction sentence).

NEW RULES (Tushar, 2026-08-21): quiz cap is 5 questions PER DAY-TOPIC (not per session); LEARNING_NOTES day blocks capped at 5 points.

Session note: deliberately short — low-energy day, stopped after one concept + exercise rather than pushing. An honest short day beats a blurry long one.

CLOSED: give_up()-tools-disabled WHY (Day 28).
CARRIED: Phase 1 out-loud recap; tool_loop.py line-22 description inversion; trim-experiment + prefill re-attach re-test.
Next: Day 32 — LangChain continued (bind tools to a model / the loop side: what replaces while stop_reason == "tool_use") or Project 2 hardening.

## Day 32 — LangChain cont.: bind_tools Kills the Plumbing, the Loop Survives
**One-liner:** `.bind_tools()` staples the TOOLS menu onto the model and parses replies into `response.tool_calls`, but the orchestration loop — invoke, run tools, append, invoke again until `tool_calls` is empty — is still yours to write.

**The goal printout (achieved — `exercises/day32_bind_tools.py`, ChatAnthropic + haiku):**
```
=== ROUND 0 === get_ticker{'company_name': 'YUNextGenAI'} -> YNXT
=== ROUND 1 === get_price{'ticker': 'YNXT'} -> 42.0
=== ROUND 2 === tool_calls=[] , stop_reason='end_turn' -> "$42.00"
```

1. PLUMBING vs ORCHESTRATION: the Day 26 loop had two jobs. `bind_tools` + `tool.invoke(tc)` kill job 1 — digging through content blocks, matching `tool_use_id`, hand-building `tool_result`. Job 2 — "loop again or done" — survives, because it's a RUNTIME decision per fresh reply while `bind_tools` runs once at CONFIG time. Agent frameworks take the loop later; today it's still yours.
2. `tool.invoke(tc)` = three registries in one call: validates args (the free validator), runs the function, returns a `ToolMessage` with the id pre-threaded. New stop check: `if not response.tool_calls:` replaces `stop_reason == "tool_use"`.
3. MENU vs TRIPS TO THE KITCHEN: bind_tools size has NOTHING to do with MAX_ITERATIONS. Rounds are driven by the question's dependency chain (N links → N tool rounds + 1 final ⇒ MAX_ITERATIONS ≥ N+1) and ended by the empty-`tool_calls` exit; the menu size never enters the loop. 10 bound tools + ticker-already-given = 2 rounds. (Confusion fired live; restaurant analogy landed.)
4. AGENT-BROKEN CODE RESCUE: an outside agent rewrote the exercise and deleted three things — `return response` (so `final` was `None`), the `for _ in range(MAX_ITERATIONS)` wrapper (so no round 2: only the MODEL, seeing `messages` on the NEXT invoke, can request `get_price`), and `messages.append(response)` (round 2 would send a tool_result answering a request not in the transcript). Diagnosed and rebuilt live — the best possible proof that the loop is orchestration and it's yours.
5. TRANSCRIPT ORDER RULE: the AIMessage goes into `messages` BEFORE its ToolMessages — the request must appear before its results or the API rejects the turn.

Quiz results (Day 31 + colds): Q1 one-source-of-truth PASSED after 1 nudge (exact sentence). Q2 model-writes-JSON / TOOLS-is-the-menu PASSED cleanly unprompted — weak spot CLOSED. Day 27 sentinel mechanics PASSED cold (no raise → except never runs → is_error stays False) — CLOSED. Day 20 count drill PASSED with the why, after 3 prior misses — CLOSED. 4/4.

NEW OPEN: fallthrough guard vs give_up() — the loop's bare `return response` after MAX_ITERATIONS exhausts hands back an AIMessage still FULL of tool_calls (a request for more work dressed as an answer); give_up() re-calls with NO tools bound → end_turn text is the only exit. Answered half, in code — re-ask cold.

Session note: end-of-session discouragement ("why can't I learn quickly") — countered with same-session evidence: 4/4 quiz, three long-standing weak spots closed. Spaced retrieval IS the method; slow-then-permanent.

## Archived Mental Models (moved from STATUS.md 2026-08-20 — STATUS.md now keeps only the active top-of-mind set)
- World knowledge is a bypass — models guess internal IDs they think they know
- A half-designed tool is not neutral — its description misleads the model on EVERY call
- Raising is not crashing — the boundary turns the raise into an error contract
- The ceiling is a backstop, not a fix — guard + error quality are layers (circuit breaker + error contract)
- for iteration in range(MAX_ITERATIONS) replaces while True — two exits, two deciders
- To test the ceiling, hit the ceiling — happy-path runs prove the OLD fix
- Agent = tool loop + iteration budget + bigger catalog + multi-step goal — no magic
- An unanswered tool_use_id is a rejected request, not a silent no-op — WHY errors are data
- except ValidationError BEFORE except Exception — the subclass gets swallowed otherwise
- A function that CANNOT fail (.get with default) cannot report failure — no raise → is_error stays False
- Model output = untrusted input; YOUR internals = untrusted output — no raw tracebacks into context
- block.input is a request body — `**` splat of a dict you didn't build TypeErrors before the body runs
- When you see `**x`, say "x must be a dict"
- An unbounded while True over a paid API is a production incident
- Answer the MOMENT IN TIME the question asks about — adjacent vocabulary is still wrong
- Tool loop = while stop_reason == "tool_use" — stop_reason steers control flow
- Tool schema = OpenAPI spec for internal functions; description field is prompt engineering
- input_schema and Pydantic = the same JSON Schema idea in opposite directions
- Schema is a request, not a guarantee — tool functions still validate
- tool_use_id = correlation ID (Kafka reply-key)
- Dispatch dict = event loop with dynamic dispatch, made literal
- Tool results return as role="user" — the transcript is GROWN by the loop
- Dependency chain = sequential turns; independent needs = parallel calls in one turn
- RAG = PUSH, tool use = PULL, agents = the tool loop + a bigger catalog
- Say the function signature out loud, then transcribe to schema
- Pipeline returns a DTO, not a tuple — callers read names
- A return type is a promise made by EVERY branch — violations crash in the CALLER
- Same type is not the same contract — branches must populate the same FIELDS
- Sentinel strings across module boundaries are silent-failure bugs
- A loud assertion is a gift; a silently tolerant one reaches production
- Verify your own fixes with the skepticism you apply to your bugs — grep, don't trust memory
- Design the response object against every consumer, not the loudest one
- Identical output after a refactor proves nothing; callers running without TypeError proves it
- Schema = API contract for model output — constraints + Optional + nesting
- Optional allows null; only = None allows ABSENCE — both parts or the key is required
- Required-by-default (NOT NULL) — optional fields move the failure downstream
- Expected traceback = passing test — "did I expect this?" before "what broke?"
- To test absence, feed absence
- Nested validation errors give the full path (sources.1.score)
- When a fix replaces a line, delete the old line in the same edit
- Prompt instructions are requests — prefill "{" forces mid-JSON continuation; re-attach before parsing
- Schema enforcement lives in YOUR code at runtime
- Messages list = conversation store you own; API = stateless REST (JWT, not session)
- System prompt = request header, re-sent every call, never in messages
- Sliding window trims in pairs, must start with user role; re-check invariants AFTER slicing
- Falsify hypotheses with printed numbers — INCLUDING the teacher's
- Trimming bug = amnesia, not garbage-in; send-trim caps API cost, store-trim caps RAM
- stop_reason arrives in message_delta at the END when streaming — control-flow signal, never render it
- Streaming = SSE; text_stream = filtered consumer, raw events = the full topic
- asyncio.gather = Promise.all; client class must match function style
- Display truncation vs API truncation — printed evidence decides
- Prefill = parallel (TTFT); decode = sequential (streaming speed)
- Metric triad: context_precision→retrieval, faithfulness→grounding, answer_relevancy→direction
- Refused questions never reach the judge — refusal_rate and n catch what quality metrics miss
- Judge metrics are non-deterministic — trends, never single absolutes; reference = expected value of a unit test
- collection.query = free local call; the LLM call is the guarded one
- Retriever = bouncer (per-chunk threshold), service = manager (empty → refuse)
- KeyError points at the crash line; the bug lives where the dict was built
- Refusals: empty filter → distance gate → LLM refusal; check in order, cheapest first — COUNT before distances
- A surprising correct refusal = coverage gap; fix is data, not code
- Corpus changes need regression evals, same as code changes
- One pipeline, many importers (prod, deterministic evals, RAGAS)
- Tuple unpacking is strict — change arity, update every caller
- Faithfulness = grounding, not truth; correct refusals score 0 — exclude them
- Deterministic evals = unit tests (free); RAGAS = load tests (costs money)
- Thresholds are outputs of calibration experiments; DBs return "closest", not "relevant"
- Knowledge gap → RAG; behavior gap → prompting first, fine-tuning last
- site-packages-only traceback = dependency conflict; venv = node_modules
- Python indentation = "how many times does this line run"
