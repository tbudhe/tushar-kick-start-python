"""Day 39 step 2 — compare retrieval over the real corpus vs the toy corpus.

Reads THRESHOLD from retriever.py so the audit mirrors production instead of
retyping the constant (same rule debug_floor.py follows).
"""
import statistics

from retriever import client, THRESHOLD

QUESTIONS = [
    "How do I create a wall in Revit?",
    "How do I add a door to a wall?",
    "How do I place a window?",
    "What is a floor plan view?",
    "How do I export a model to DWG?",     # nothing in the corpus answers this
]

v2 = client.get_or_create_collection(name="revit_docs_v2")
toy = client.get_or_create_collection(name="revit_docs_project_2")

# --- chunk size: the number that explains everything below -----------------
sizes = [len(d) for d in v2.get(include=["documents"])["documents"]]
print("=== CHUNK SIZE (revit_docs_v2) ===")
print(f"count {len(sizes)} | min {min(sizes)} | "
      f"median {int(statistics.median(sizes))} | max {max(sizes)} chars"
      f"   <- MAX_CHARS was 600\n")

# --- same question, both collections, distances side by side ---------------
print("=== RETRIEVAL: v2 (real docs) vs project_2 (toy) ===")
for question in QUESTIONS:
    print(f"\nQ: {question}")
    for label, coll, k in (("v2 ", v2, 2), ("toy", toy, 1)):
        res = coll.query(query_texts=[question], n_results=k,
                         include=["documents", "distances"])
        for id_, doc, dist in zip(res["ids"][0], res["documents"][0],
                                  res["distances"][0]):
            verdict = "PASS  " if dist < THRESHOLD else "REJECT"
            snippet = doc.replace("\n", " ")[:58]
            print(f"  {label}  {id_:20} {dist:.3f}  {verdict}  \"{snippet}\"")

            # --- does rank track chunk LENGTH? ----------------------------------------
print("\n=== RANK vs CHUNK LENGTH — 'How do I create a wall in Revit?' ===")
res = v2.query(query_texts=["How do I create a wall in Revit?"], n_results=8,
               include=["documents", "distances"])
for rank, (id_, doc, dist) in enumerate(
        zip(res["ids"][0], res["documents"][0], res["distances"][0]), start=1):
    print(f"  {rank}. {id_:20} {dist:.3f}  {len(doc):5} chars")
