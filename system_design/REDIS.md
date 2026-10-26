# Redis — Concepts, Celery Internals & Interview Answers

> One-file reference. Built from Day 60 (2026-10-26).
> Interview habit: **first sentence answers the question → then why → then trade-off.**

---

## 1. What Redis is (one sentence)

**A single-threaded, in-memory data-structure server: every command is atomic, so I pick the data type for the job.**

- **In-memory** → microsecond reads/writes; RAM is the limit.
- **Single-threaded command execution** → like Node's event loop: one command at a time, never interleaved.
  - ✅ `INCR`, `LPUSH`, `SET NX` are atomic with **no locks**.
  - ❌ One slow command (`KEYS *`, a huge `LRANGE`) blocks **every** client — like a CPU loop blocking Node. Use `SCAN` instead of `KEYS`.
- **Shared by everyone** → like a JS `Map` living on its own server that all 50 app instances reach over the network.
- Default port **6379** ("MERZ" on a phone keypad). 16 logical databases: `/0` … `/15`.

---

## 2. Data types: pick one per job

| Type | Think of it as | Use it for | Key commands |
|---|---|---|---|
| **String** | a value / counter | cache entry, counter, lock | `GET` `SET` `INCR` `SET k v NX PX 30000` |
| **Hash** | a JS object | user profile, session | `HSET` `HGET` `HGETALL` |
| **List** | a queue | job queue (Celery, BullMQ) | `LPUSH` `RPOP` **`BRPOP`** |
| **Set** | unique bag | tags, "who's online" | `SADD` `SISMEMBER` |
| **Sorted set** | items ranked by a score | leaderboard, delayed jobs, sliding-window rate limit | `ZADD` `ZRANGEBYSCORE` `ZREMRANGEBYSCORE` |
| **Stream** | a mini Kafka topic | durable event log with consumer groups | `XADD` `XREADGROUP` `XACK` |
| **Pub/Sub** | an EventEmitter over the network | fire-and-forget notifications (no storage!) | `PUBLISH` `SUBSCRIBE` |

**Any key can carry a TTL:** `EXPIRE key 60`, or `SET key v EX 60`.

---

## 3. Classic patterns (interview favourites)

### Rate limiting: 100 requests / user / minute across 50 servers
**Answer first:** *"One Redis counter per user per minute, incremented with `INCR` — atomic because Redis is single-threaded — and I check the value `INCR` returns."*

```python
key = f"rate:{user_id}:{minute}"      # e.g. rate:user42:09:45
count = r.incr(key)                   # atomic: two servers get 100 and 101, never 99/99
if count == 1:
    r.expire(key, 60)                 # first hit starts the 60s window
if count > 100:
    return 429                        # 429 Too Many Requests (NOT 409 = Conflict)
```

- ❌ Wrong: `GET` → check → `SET`. Both servers read 99 and both get through (a race).
- Follow-up: **"100 requests at 09:45:59 + 100 at 09:46:00?"** → a fixed window allows 200 in 2 seconds. Fix: **sliding window** = sorted set of request timestamps per user (`ZADD` now, `ZREMRANGEBYSCORE` anything older than 60s, `ZCARD` to count).
- Detail: if the app crashes between `INCR` and `EXPIRE`, the key never expires. Wrap both in a `MULTI` pipeline or a Lua script.

### Cache-aside (like Redis-before-DB at Walmart)
1. Read: check Redis → hit? return. Miss → read DB → `SET key value EX ttl` → return.
2. Write: update DB → `DEL` the cache key.
- **Stampede** (a hot key expires, 1,000 requests hit the DB): add jitter to TTLs, or let one request rebuild while holding a lock.
- **Stale data:** the TTL is your upper bound on staleness. Choose it from the business flow (e.g. Walmart checkout: 1-hour TTL scoped to the shopping trip).

### Distributed lock
```
SET lock:order42 <my-uuid> NX PX 30000    # NX = only if not exists, PX = auto-expire 30s
```
- Release only if the value is still **your** uuid (a Lua compare-and-delete), or you might delete someone else's lock.
- The auto-expiry stops a crashed holder from locking forever.
- Caveat for interviews: it isn't bulletproof under failover (that's the Redlock debate). For money, pair it with an idempotency key in the DB.

---

## 4. How Celery uses Redis (the BullMQ mapping)

```
broker  = redis://localhost:6379/0   → the QUEUE   (messages waiting)
backend = redis://localhost:6379/1   → the RESULTS (task-meta keys)
```

| BullMQ (Node) | Celery (Python) | Redis feature underneath |
|---|---|---|
| `queue.add('job', data)` | `task.delay(x)` | **List** `celery` ← `LPUSH` |
| `new Worker('q', fn)` | `celery -A app worker` | **`BRPOP`** from the list |
| job "active" | task received, not acked yet | **Hash** `unacked` + **sorted set** `unacked_index` |
| `job.returnvalue` | `AsyncResult(id).get()` | **String** `celery-task-meta-<id>` with TTL (`result_expires`, default 1 day) |
| job finished event | `.get()` wakes instantly | **Pub/Sub** |
| job not found | `PENDING` | that key **doesn't exist** |

**Interview line:** *"Celery with a Redis broker is a Redis list: producers LPUSH, workers BRPOP, unacked messages are tracked in a hash so they can be redelivered, and results are TTL'd strings in the backend database."*

### Why `BRPOP`, not `RPOP` in a loop?
**Answer first:** *"BRPOP blocks inside Redis until a message arrives, so pickup is instant and idle costs nothing; polling is either late or floods Redis."*
- Node: `await redis.brpop('celery', 0)` vs `setInterval(() => redis.rpop('celery'), 100)`.
- Only that **one connection** waits. Nothing else is blocked, just like `await` doesn't block the event loop.

### Why a separate worker, not a thread inside the API?
**Answer first:** *"A thread inside the API dies with the API; a message in Redis survives."*
1. **Durability:** a deploy or crash kills in-flight threads, while a queued message is redelivered.
2. **Isolation:** a 2-minute PDF job steals CPU and memory from user requests.
3. **Independent scaling:** 3 API pods, 20 workers.
- The worker *does* use threads or processes internally (`worker_pool`, `worker_concurrency`).
- The worker's **main process consumes and supervises; child processes or threads execute** (= Node `cluster` primary / PM2). A crashing task kills only a child.

### Large payloads (the PDF case)
- **Never put the file in the message.** Stream the upload to blob storage (Node `req.pipe(...)`, or FastAPI's `UploadFile.file`), enqueue `{doc_id, blob_ref}`, return **`202 Accepted` + task_id**, and let the client poll status.
- No shared memory (it only works on one machine) and no protobuf (the message is tiny; JSON is fine).

```
Client --upload--> API --stream--> Blob storage
                    +--> enqueue {doc_id, blob_ref} --> Redis --> Worker --> status
                    +--> 202 + task_id      Client --poll--> PENDING / SUCCESS / FAILURE
```

---

## 5. Delivery guarantees (Day 61 preview: concept 3)

- **Default (`acks_late=False`):** ack on receive → a worker crash mid-task **loses** the task (at-most-once).
- **`acks_late=True`:** ack after the work → a crash means **redelivery** (at-least-once) → the task **must be idempotent** (Day 58: double charge reproduced, then fixed).
- **`visibility_timeout`** (Redis transport, default **1 hour**): an unacked message older than this is redelivered to another worker.
  - Rule: `visibility_timeout` > your longest task **and** > your longest retry countdown, or the task runs twice while still running.
- Retries (Day 59): the **same task id** is re-sent with `retries + 1`; `retry_backoff` uses `2 ** retries` as the **ceiling**, and jitter only makes the wait shorter.

## 6. Task states (concept 4)

`PENDING → (STARTED) → SUCCESS | FAILURE | RETRY`
- **PENDING = "no record for this id"**: never sent, typo'd id, expired result, or a lost write. Never trust it without a timeout.
- **STARTED** only appears if `task_track_started=True`.
- **SUCCESS** = the function returned, not that the business outcome was correct.

## 7. Redis under failure (concept 5)

| Topic | What to say |
|---|---|
| **Persistence** | **RDB** = periodic snapshots (fast restart, can lose minutes). **AOF** = append-only log of every write, `fsync` every second (loses ≤ 1s). Production often runs both. |
| **Eviction** | `maxmemory-policy`. For a **cache**: `allkeys-lru`. For a **broker**: **`noeviction`**, or Redis will silently delete queued tasks when memory fills. |
| **High availability** | Replication (primary → replicas). **Sentinel** = automatic failover. **Cluster** = sharding across 16,384 hash slots. |
| **Failover risk** | Replication is async, so a just-written message can be lost on failover. |
| **When NOT Redis as broker** | Need strong durability, complex routing, very long tasks, or huge scale → **RabbitMQ** (real acks and routing) or **SQS** (managed, no ops). Need replayable event history → **Kafka** or Redis Streams. |

---

## 8. Mock interview bank (answer-first)

1. **"Why is Redis fast?"** → *"It's in-memory and single-threaded, so no disk on the hot path and no locks or context switches."*
2. **"Rate limit across 50 servers?"** → `INCR` + `EXPIRE` per user per window, check the returned value, 429. Follow-up: sliding window with a sorted set.
3. **"Why BRPOP over polling?"** → blocking pop: instant pickup, zero idle cost.
4. **"Background thread vs Celery?"** → a thread dies with the API, steals request capacity, and can't scale separately; the queue survives restarts.
5. **"Worker crashed mid-task. What happens?"** → with `acks_late`, the message is redelivered after `visibility_timeout`, so the task must be idempotent.
6. **"Redis memory is full and you use it as a broker."** → it must be `noeviction`, otherwise tasks vanish; alert on memory and scale out.
7. **"Pub/Sub vs Streams vs List?"** → Pub/Sub stores nothing (offline subscribers miss messages); a list is a simple work queue; Streams are a durable log with consumer groups and acks, like a mini Kafka.
8. **"When would you replace Redis with RabbitMQ or SQS?"** → when durability, routing, or long-running tasks matter more than simplicity.

**Don't know an answer?** Reason out loud: *"I haven't used X directly, but based on Y I'd expect Z, because…"*

---

## 9. Ports to know

Redis **6379** · Postgres 5432 · MySQL 3306 · Kafka 9092 · RabbitMQ 5672 · MongoDB 27017
