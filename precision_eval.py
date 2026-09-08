"""Day 40 — retrieval precision harness. No LLM in the loop."""
from retriever import client

v2 = client.get_or_create_collection(name="revit_docs_v2")

data = v2.get(include=["documents"])
print(f"=== {len(data['ids'])} chunks in revit_docs_v2 ===")
for id_, doc in sorted(zip(data["ids"], data["documents"])):
    snippet = doc.replace("\n", " ")[:70]
    print(f"  {id_:22} {len(doc):5} chars  \"{snippet}\"")

# Expected = the chunk(s) that ANSWER the question, not the ones ABOUT the topic.
# Test applied per chunk: if a reader got ONLY this chunk, could they do the thing?
# [] means: nothing in this corpus should answer it.
CASES = [
    {"q": "How do I create a wall in Revit?", "expected": ["walls_overview_0", "about_walls_1"]},
    {"q": "How do I add a door to a wall?",   "expected": ["place_a_door_0", "place_a_door_2"]},
    {"q": "How do I place a window?",         "expected": ["place_a_window_0", "place_a_window_1"]},
    {"q": "What is a floor plan view?",       "expected": ["about_plan_views_0"]},
    {"q": "How do I export a model to DWG?",  "expected": []},
]

DEPTH = 10  # look far past production's N_RESULTS=2 — we want the rank, not the hit

print(f"\n=== RETRIEVAL PRECISION — revit_docs_v2, depth {DEPTH} ===")
print(f"{'question':38} {'expected chunk':22} {'rank':>4}  dist")
for case in CASES:
    res = v2.query(query_texts=[case["q"]], n_results=DEPTH,
                   include=["distances"])
    ids, dists = res["ids"][0], res["distances"][0]

    if not case["expected"]:
        print(f"{case['q']:38} {'<none expected>':22} {'-':>4}  {dists[0]:.3f}")
        continue

    # best rank among the acceptable chunks; None if none of them made depth
    hits = [(ids.index(e) + 1, dists[ids.index(e)])
            for e in case["expected"] if e in ids]
    if hits:
        rank, dist = min(hits)
        print(f"{case['q']:38} {ids[rank-1]:22} {rank:>4}  {dist:.3f}")
    else:
        print(f"{case['q']:38} {case['expected'][0]:22} {'MISS':>4}  -")


# Aggregates. Only questions WITH an expected chunk count here — the DWG case
# is a coverage test, scored separately below.
answerable = [c for c in CASES if c["expected"]]
ranks = []
for case in answerable:
    res = v2.query(query_texts=[case["q"]], n_results=DEPTH, include=[])
    ids = res["ids"][0]
    found = [ids.index(e) + 1 for e in case["expected"] if e in ids]
    ranks.append(min(found) if found else None)

hit_at = lambda k: sum(1 for r in ranks if r and r <= k) / len(ranks)
mrr = sum(1 / r for r in ranks if r) / len(ranks)

print(f"\nhit@2  (what production sees at N_RESULTS=2): "
      f"{sum(1 for r in ranks if r and r <= 2)}/{len(ranks)} = {hit_at(2):.3f}")
print(f"hit@{DEPTH} (what the store can even reach):     "
      f"{sum(1 for r in ranks if r and r <= DEPTH)}/{len(ranks)} = {hit_at(DEPTH):.3f}")
print(f"MRR:                                         {mrr:.3f}")


print("\n=== hit@k SWEEP — where does widening the window actually pay? ===")
for k in range(1, DEPTH + 1):
    n = sum(1 for r in ranks if r and r <= k)
    print(f"  k={k:2}  {n}/{len(ranks)} = {n/len(ranks):.3f}  {'#' * n}")