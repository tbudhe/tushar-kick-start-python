from retriever import collection

results = collection.query(
    query_texts=["floor plan view"],
    n_results=3,
    where={"category": "floors"},
    include=["documents", "distances"],
)
print(results["documents"])
print(results["distances"])
