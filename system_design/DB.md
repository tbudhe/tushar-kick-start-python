# Mock Interview: Scaling a Marketplace Orders Database (MongoDB)

System design practice covering **replication, read-your-own-writes, write concern, and sharding**, worked through as a mock interview.

---

## 📋 The Scenario

> An online marketplace. Buyers place orders, sellers fulfill them. The Orders DB is a single **MongoDB replica set** (1 primary + 2 secondaries). **All reads and writes go to the primary.**

| Metric | Today | Next year (3×) |
|---|---|---|
| Reads | 20,000/sec (~90% of load) | 60,000/sec |
| Writes | 2,000/sec | 6,000/sec |
| Primary CPU (peak) | 85% | — |

Last Black Friday the site slowed down badly. Leadership wants a plan.

---

## 🧭 Step 0: Classify the Problem Before Fixing It

Before proposing anything, ask: **is this a read, write, durability, or stale-read problem?**

| Problem | Tool |
|---|---|
| Too many **reads** | Replicas (`readPreference`), cache hot data |
| Too many **writes** for one primary | **Shard** (each shard has its own primary) |
| **Durability**: acked writes lost on failover | `w: "majority"` |
| **Stale reads** after a user's own write | Read-your-own-writes (RYOW) |
| Big table, slow scans, archiving | Partitioning (organizes one server, **adds no capacity**) |

For every decision, state three things: **WHAT** I'd do → **HOW** I'd build it → what it **COSTS**.

---

## Q1. What's the bottleneck, and how do you confirm it?

**Answer**
- 90% of load is reads, all hitting the primary. **Two secondaries are idle.** That's the main issue.
- Confirm by checking the slowest queries and index usage (Atlas Profiler / `explain()`), and the CPU breakdown of reads vs writes.
- Short-term firefighting (scale up, roll back a bad deploy) buys time but isn't the plan for 3× growth.

⚠️ Connection pool size, retries, and circuit breakers are **not** diagnosis. A larger pool under CPU saturation makes it worse.

---

## Q2. What's the simpler fix before sharding?

**WHAT:** Move reads to the secondaries.
**HOW:** `readPreference: "secondaryPreferred"`.
**COST:** Replicas lag, so reads can be stale (see Q3).

**Load math (today):**
- ~2% of reads stay on the primary (recent writers, see Q3) → **~400 reads/sec**
- ~98% go to secondaries → **~9,800 reads/sec each**
- Primary is left with writes plus a small slice of reads, so CPU drops sharply.

```python
from pymongo import MongoClient, ReadPreference

client = MongoClient("mongodb://host1,host2,host3/?replicaSet=rs0")
orders = client.shop.orders

# Bulk reads go to secondaries
orders_read = orders.with_options(read_preference=ReadPreference.SECONDARY_PREFERRED)
```

---

## Q3. A buyer places an order and doesn't see it in "My Orders". Why, and how do you fix it?

**Why:** Replication is **async**. The write landed on the primary, but the read hit a secondary that hadn't applied it yet. That's **replication lag**, a stale read.

**WHAT:** Route users who wrote in the last few seconds to the primary (RYOW).
**HOW:** On every write, set a short-lived Redis marker per user. TTL = measured p99 replication lag (e.g., 5s).
**COST:** One tiny Redis key per recent writer, plus one extra Redis call per read. About 1–2% of reads hit the primary.

```python
import redis
from pymongo import ReadPreference

r = redis.Redis()
RYOW_TTL_SECONDS = 5  # set from measured p99 replication lag

def place_order(user_id, order):
    orders.insert_one(order)
    r.set(f"lastwrite:{user_id}", 1, ex=RYOW_TTL_SECONDS)

def my_orders(user_id):
    recent_writer = r.exists(f"lastwrite:{user_id}")
    pref = ReadPreference.PRIMARY if recent_writer else ReadPreference.SECONDARY_PREFERRED
    return list(orders.with_options(read_preference=pref).find({"customerId": user_id}))
```

**Why Redis instead of app memory?** It works across all stateless app servers, and the TTL handles cleanup automatically.

**Alternative:** MongoDB causal-consistency sessions. The secondary waits until it has caught up to the user's write.

```python
with client.start_session(causal_consistency=True) as s:
    orders.insert_one(order, session=s)
    orders.with_options(read_preference=ReadPreference.SECONDARY).find_one(
        {"_id": order["_id"]}, session=s)   # waits for this write
```

⚠️ **Don't** "fix" stale reads by making replication synchronous. Sync replication guarantees the secondary has the write **in its log** (durability), not that it has **applied** it (freshness). It also slows every write for every user.

---

## Q4. The primary acknowledged an order, then crashed. After failover, the order is gone. Why?

**Why (with `w: 1`):**
1. The primary says "OK, saved" **before** any secondary has the write.
2. The primary crashes before shipping it.
3. A secondary is elected without the write. When the old primary rejoins, the write is **rolled back**.

That's a **lost acknowledged write**, which is a durability problem, not a stale read.

**WHAT:** Use `w: "majority"` for orders.
**HOW:** The client gets "OK" only after a majority (3 nodes → 2, 5 nodes → 3) has the write. Elections also require a majority, and **two majorities always overlap**, so the new primary must have every acknowledged write.
**COST:** Higher write latency → connections held longer → lower write throughput. No writes can be acknowledged if a majority is down.

```python
from pymongo import WriteConcern

orders_durable = orders.with_options(write_concern=WriteConcern(w="majority"))
orders_durable.insert_one(order)
```

### Write concern and RYOW are independent choices

| Data | Write concern | RYOW? |
|---|---|---|
| Orders, payments | `majority` | ✅ |
| Shipping address | `majority` | ✅ |
| Clicks, view counts | `w: 1` | ❌ |

> Write concern = *can I afford to lose it?* RYOW = *does the writer need to see it immediately?*

---

## Q5. Planning for 3× growth (60K reads/sec, 6K writes/sec)

### Reads
- Add more secondaries (each takes a share of 60K/sec).
- Optionally cache **hot** data (e.g., active order status) in Redis with a short TTL. Add it only if replicas aren't enough; it costs memory and invalidation complexity.
- Keep RYOW for recent writers.

⚠️ **Shards don't solve reads.** Replicas and caches do.

### Writes
- First check whether one primary can handle 6K/sec after indexing and scaling up.
- If not, **shard**. Each shard is its own replica set with its own primary, so writes split across N primaries.

### Choosing the shard key: follow the most common query

| Candidate | Result |
|---|---|
| `createdAt` (range) | ❌ **Hot shard.** Every new order has the newest timestamp, so all writes hit the last shard. |
| `orderId` (range) | ❌ Same problem if IDs increase (ObjectIds start with a timestamp). |
| `hash(orderId)` | Spreads writes ✅, but "My Orders" (by `customerId`) becomes **scatter-gather** across all shards ❌ |
| **`hash(customerId)`** | ✅ "My Orders" hits one shard, writes spread across millions of customers, not monotonic. |

```javascript
// mongosh
sh.shardCollection("shop.orders", { customerId: "hashed" })
```

### The seller side loses. Handle it with a second copy

```
orders_by_customer  (shard key: hash(customerId))  ← buyers read
        │ change stream / CDC
        ▼
      Kafka ──► consumer ──► orders_by_seller (shard key: hash(sellerId))  ← sellers read
```

- ✅ Both buyers and sellers get single-shard queries.
- ❌ Double storage. The seller view is **eventually consistent** (Kafka consumer lag).
- RYOW **doesn't** help here: the seller isn't the writer. Instead, set an SLO on consumer lag (e.g., p99 < 5s), alert on it, and push updates to the seller dashboard over WebSocket.
- Heavy seller analytics → a separate analytics store (Elasticsearch / warehouse).

### Edge case: whales
`hash(customerId)` balances customers, not one huge customer. For very large accounts, use a compound key such as `{ customerId: 1, orderId: "hashed" }` so their data can split across chunks, accepting multi-shard reads for those few accounts.

---

## ✅ Model Staff-Level Answer (3× growth)

> **Reads (60K/sec):** add secondaries and cache hot reads like order status in Redis with a short TTL. Keep RYOW for recent writers via a per-user Redis marker.
> **Writes (6K/sec):** first check whether one primary handles it after indexing and scaling up. If not, shard by `hash(customerId)`, since buyer reads dominate. That keeps "My Orders" on one shard and spreads writes. Sellers get a second copy keyed by `sellerId`, fed by change streams through Kafka, eventually consistent within a few seconds.
> **Durability:** `w: majority` for orders, because we can't lose them.

---

## 📚 Core Concepts Cheat Sheet

| Concept | One-liner |
|---|---|
| **Replica** | Full copy of the data on another server, kept in sync from the primary's log. Adds readers, never writers. **Not a backup**: bad deletes replicate too. |
| **Sync vs async replication** | Sync = no acked write lost, slower writes. Async = fast writes, lag, possible loss on failover. |
| **Replication lag** | Secondary hasn't applied the latest writes yet → stale reads. |
| **RYOW** | Recent writers read from the primary; everyone else reads replicas. |
| **`w: majority`** | Write survives failover because majorities overlap. Prevents lost writes, not stale reads. |
| **Partitioning** | Splits a table on **one** server. Pruning and archiving. Adds no CPU/RAM. |
| **Sharding** | Splits data across **many** servers, each with its own primary. Scales writes and storage. |
| **Vertical vs horizontal scaling** | Vertical = bigger box. Horizontal = more boxes (sharding, replicas). |
| **Scatter-gather** | Query without the shard key → router asks every shard and merges results. |
| **Hot shard** | Monotonic key (timestamps, increasing IDs) sends all new writes to one shard. |

> **Sharding decides *which server* holds the data. Replication decides *how many copies* exist. Partitioning organizes data *inside* one server.**

---

## ⚠️ Common Mistakes to Avoid

1. Proposing fixes (pool size, retries, sharding) before naming the bottleneck.
2. Adding shards to solve a **read** problem.
3. Expecting `w: majority` to reduce load or remove stale reads.
4. Partitioning on one server to fix CPU.
5. Picking a shard key before asking *"what's the most common query?"*
6. Stating the WHAT but not the HOW and COST out loud.
