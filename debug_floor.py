"""Retrieval audit — prints what production would actually retrieve.

Imports N_RESULTS and THRESHOLD from retriever so the audit can never
drift from the pipeline. Retyping them here is how an audit starts lying.
"""
from retriever import collection, N_RESULTS, THRESHOLD
from evals import TEST_CASES

print(f"audit params: n_results={N_RESULTS} threshold={THRESHOLD}\n")

for case in TEST_CASES:
    print(case["question"])
    results = collection.query(
        query_texts=[case["question"]],
        n_results=N_RESULTS,
        # where={"category": "floors"},   # toggle to reproduce a filtered query
        include=["distances"],
    )

    distances = results["distances"][0]
    if not distances:
        print("  (no results — filter excluded everything)")
        continue

    for doc_id, dist in zip(results["ids"][0], distances):
        kept = "keep" if dist < THRESHOLD else "drop"
        print(f"  {doc_id}  {dist:.3f}  {kept}")

    if distances[0] > THRESHOLD:
        print("  ⚠️ COVERAGE RISK")
