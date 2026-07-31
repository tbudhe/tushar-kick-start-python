from retriever import collection
# from evals import TEST_CASES
# for case in TEST_CASES:
#     print(case["question"])
#     results = collection.query(
#         query_texts=[case["question"]],
#         n_results=3,
#         # where={"category": "floors"},
#         include=["distances"],
#     )
#     for doc_id, dist in zip(results["ids"][0], results["distances"][0]):
#         print(f"  {doc_id}  {dist:.3f}")
#     best = results["distances"][0][0]
#     if best > 1.0:
#         print("  ⚠️ COVERAGE RISK")

results = collection.query(
    query_texts=["What is a floor plan view?"],
    n_results=3,
    where={"category": "walls"},
    include=["distances"],
)
print(results["distances"][0])