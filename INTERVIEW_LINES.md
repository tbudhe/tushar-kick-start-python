# INTERVIEW_LINES.md — say these OUT LOUD

Rules: answer FIRST in one sentence, then one detail from MY project, then stop.
Every line here comes from something I built or measured (Day N = where in LEARNING_NOTES.md).
Updated at the end of every session. Next session opens with ONE line said cold.

---

## 0. Intro + stories (from STATUS.md interview kit)

**90-sec intro:** "I'm Tushar. I've spent 16 years building production systems end to end. Right now I'm an AI engineer at Autodesk building MSSP, a copilot agent that works directly in Contentful so marketers can set up A/B tests and launch campaigns without waiting on engineering. My background is systems at scale: at Walmart I scaled Scan & Go to 300,000 requests a minute, at Fidelity I built on the DX Exchange crypto platform, and at EY I built global SSO for 300,000+ users. On the side I've built a RAG service over Revit docs with its own retrieval evals, and a LangGraph agent with tools, persistent memory and async ingestion on Celery. What I keep learning is that the model is the easy part — the hard part is the platform around it: serving, throughput, cost, evals and reliability."

**Walmart p99 story:** "Checkout p99 was 5 seconds at peak. Prometheus traced it to the payment path. I reused the payment contract per checkout session instead of creating one each time, resized an under-sized connection pool, and moved non-critical work off the sync path onto a stream. p99 went from 5s to 2.97s at 300K requests a minute, blue/green, zero downtime. LLM serving is the same problem: p99, throughput, cost per request."

**Regression found by my own eval (Day 62):** "After a repo reorganisation, my eval script was the first thing to fail — a stale import meant the API itself was broken. That's why I treat the eval suite as a smoke test on every change."

---

## 1. LLM fundamentals (Days 0–16, 43)

- **Training vs inference:** "Training changes the weights — predict, measure loss, nudge weights with gradient descent. Everything I build with RAG and prompting is inference; it never touches the weights."
- **Overfitting:** "The model memorised the examples instead of the pattern; a held-out test split gives the honest score."
- **How an LLM generates:** "It tokenises the text, uses self-attention to relate every token to every other, and predicts the next token one at a time."
- **Pretraining / SFT / RLHF:** "Pretraining learns language from next-token prediction at scale; SFT teaches instruction-following from curated examples; RLHF shapes behaviour toward what humans prefer."
- **Why LLMs hallucinate:** "Softmax always picks some next token — there's no 'I don't know' option — so without the facts it produces a confident, plausible wrong answer."
- **Prefill vs decode:** "Prefill reads the whole prompt in parallel and sets time-to-first-token; decode generates one token at a time and sets streaming speed."
- **Model choice:** "It's a spec-sheet decision — context window, cost, latency, quality on my task — not 'biggest model wins'."
- **Fine-tune vs RAG vs prompt:** "One question: did it not know, or did it know and misbehave? Knowledge gap → RAG. Behaviour gap → prompting first, fine-tuning only if prompting maxes out."

## 2. RAG (Days 2–7, 17–21, 38–42)

- **RAG in one breath:** "Chunk and embed the docs, embed the question, fetch the nearest chunks, and have the LLM answer only from those."
- **Why chunk:** "One vector is one meaning — embed 40 pages as one and every question scores weakly. Overlap keeps a sentence cut at a boundary whole in at least one chunk."
- **Threshold:** "Vector DBs return the closest, not the relevant. I calibrated: relevant distances 0.18–0.75, junk 1.69+, so I set 1.2 — the threshold is an experiment's output, not a guess."
- **Metadata filter:** "It's a SQL WHERE that runs before the vector search, so you get a small honest result set instead of padded neighbours."
- **Refusal debugging:** "A refusal can come from three layers — filter, threshold, or the LLM's refusal prompt. I check them in order with evidence."
- **Ranking vs retrieval (Day 39–40):** "Vector search ranks aboutness, not answerhood. My eval showed hit@10 = 1.0 but hit@2 = 0.75 — the right chunk was always there, ranked too low. That's a reranking problem, not a data problem."
- **Frameworks (Day 38):** "LlamaIndex gave me my own pipeline with its defaults — same chunks, same ranking. It buys less code, not better retrieval, and constants don't port: it reports exp(-distance), so my 1.2 became 0.301."
- **Deploy (Day 41):** "The vector DB is derived data — rebuild it from the tracked corpus in the build step. And blue/green only works if someone flips the pointer: production served the toy corpus for two sessions."
- **Health check (Day 42):** "My /health reports identity, not liveness — collection name, count, embedder, threshold — read from the same handle the request path uses."

## 3. Structured output + API contracts (Days 22–25)

- **Model output is untrusted input:** "I validate it at the boundary with a Pydantic schema and fail loud there, not silently downstream."
- **Typed response:** "Every branch of my pipeline returns one RagResponse; refusal is a declared field, `refused`, never a magic string clients have to match."
- **Statelessness:** "The Claude API is stateless — conversation memory is the messages list I own and re-send, trimmed with a sliding window."
- **Streaming:** "It's SSE — text arrives in content_block_delta events and stop_reason is the stream's status code."

## 4. Tool use + agents (Days 26–37, 46–52)

- **What an agent is:** "A tool loop plus a budget: the model requests a tool, my code runs it and returns the result, until it answers in text — capped with a max-iteration guard and a forced final answer."
- **Model never executes:** "The model only writes a structured request; my code runs the function."
- **Tool errors:** "A failed tool returns a tool_result with is_error true, so the model can recover — never let the exception escape the loop."
- **Tool descriptions:** "The description is prompt engineering — the model routes on it."
- **Latency:** "Async overlaps waiting, but a chain of dependent tool calls stays serial — the only latency lever is fewer rounds."
- **Grounding leak (Day 50):** "When I wrapped my RAG as an agent tool, the inner pipeline said 'I don't know' and the outer agent answered from training data anyway. Wrapping a grounded pipeline in an agent drops the guarantee unless the agent is forced to answer only from the tool."
- **Memory:** "A checkpointer is a session store for the graph — thread_id is the cookie. LangGraph loads history before the run and saves after. With SqliteSaver it survives a process restart; memory is input to the LLM, not a cached answer."
- **LangGraph vs hand loop:** "ToolNode and tools_condition are my hand-written while loop, prebuilt. I wrote it by hand first so I know what the framework does."

## 5. Celery + Redis (Days 53–61)

- **Why Celery:** "The caller gets a task_id instantly; the slow job runs in a worker, so it survives API restarts, doesn't steal request capacity, and scales on its own."
- **Pool choice:** "I measured it: threads took IO-bound work from 8s to 2s and did nothing for CPU work; processes took CPU work from 6.3s to 1.9s. LLM-calling workers get threads, CPU-heavy ingestion gets prefork."
- **Queues:** "LLM calls and ingestion go on separate queues, each with the right pool, so a 1,000-document ingest can't starve user-facing LLM calls."
- **Chord:** "Ingest fans out as a chord — chunks embed in parallel and the callback flips the collection pointer only when every chunk succeeded."
- **acks_late:** "Ingest tasks ack after they finish, so an OOM-kill doesn't drop work — the message is redelivered. That's at-least-once, so the tasks are idempotent."
- **PENDING:** "PENDING means Celery found no record of that id — not 'queued'. A real status API keeps its own status row."
- **visibility_timeout:** "It must be longer than the slowest task, or Redis assumes the worker died and hands the task to a second worker — a duplicate."
- **Retries on 429:** "Exponential backoff with jitter, so 500 throttled workers don't retry in lockstep — and rate_limit so the 429 doesn't happen in the first place."
- **Redis durability:** "Redis as a broker isn't durable by default — I'd turn on AOF and set maxmemory-policy noeviction. If loss is unacceptable, like payments, RabbitMQ or SQS."
- **Rate limit across servers:** "INCR a per-user-per-minute key with a 60s expiry and check the returned value; over the limit returns 429. A sliding window uses a sorted set to avoid the boundary burst."

## 6. Evals + observability (Days 18–21, 40, 62)

- **Two layers:** "Retrieval I test deterministically with a golden set and hit@k / MRR — no LLM, free in CI. Generation I test with an LLM-as-judge for faithfulness."
- **LLM-as-judge:** "A narrow binary rubric — is every claim supported by the retrieved chunks — and I spot-check the judge against my own labels first, because an unvalidated judge is just a second unverified model."
- **Faithfulness ≠ truth:** "Faithfulness measures grounding in the retrieved context, not truth. Refusals score 0 on it, so I exclude them and track refusal_rate separately."
- **The RAGAS triad:** "Context precision grades retrieval, faithfulness grades grounding, answer relevancy grades direction."
- **The label set IS the test (Day 40):** "My first golden set labelled by topic and scored 100% on a known bug. Label the chunk that ANSWERS, not the one ABOUT the topic."
- **Grade the real evidence (Day 19):** "The judge grades the chunks the pipeline actually returned — re-retrieving in the eval is a guess about the past."
- **Offline + online:** "Offline, I run the golden set plus judges on every prompt or model change, as a regression gate. Online, I trace production with LangSmith and sample real traffic into the dataset, so the eval set grows from real failures."
- **Test the tester (Day 63):** "Before trusting my judge, I fed it my real chunks with a fabricated answer — it said NO. Faithfulness came out 4/4 on answered questions, refusals tracked separately at 1/5."

## 7. Guardrails (Days 63–64)

- **Prompt injection:** "Instructions and data reach the LLM as one token stream, so text in the data can act as an instruction — it's SQL injection with no parameterized query."
- **Indirect injection:** "In RAG the dangerous one is indirect: a poisoned document gets ingested and retrieval hands it to the model — stored XSS for LLMs. Retrieved chunks are untrusted input."
- **Injection defense (Day 63):** "Tags and scanning lower the odds; limiting what the model can do limits the damage. I planted an injection in my Revit RAG — Opus and Haiku both ignored it 0 for 3 even untagged — but I don't count model training as my defense. My RAG has no tools, so the worst case is a wrong answer; in my agent, write tools need human approval."

## 8. Multi-agent — coming Day 65
## 9. MCP — coming Day 66
