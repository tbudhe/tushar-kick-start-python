from pathlib import Path

import chromadb

import os
# Anchor the DB path to THIS file's directory, not the process's cwd —
# otherwise launching uvicorn from elsewhere silently creates an empty DB.
DB_PATH = str(Path(__file__).parent / "revit_db_07_25")

client = chromadb.PersistentClient(DB_PATH)

# Pointer, not a constant. Blue/green: ingest into a new collection name,
# then flip this env var — no code change, no redeploy of logic.
COLLECTION_NAME = os.environ.get("REVIT_COLLECTION", "revit_docs_v2")

collection = client.get_or_create_collection(name=COLLECTION_NAME)

# Single source of truth for retrieval params — debug_floor.py imports these
# instead of retyping them, so the audit always mirrors production.
THRESHOLD = 1.2
N_RESULTS = 2


def retrieve(question, category=None, threshold=THRESHOLD):
    results = collection.query(
        query_texts=[question],
        where={"category": category} if category else None,
        n_results=N_RESULTS,
        include=["documents", "distances"]
    )

    chunks = []
    for text, id_, distance in zip(
        results["documents"][0], results["ids"][0], results["distances"][0]
    ):
        if distance < threshold:
            chunks.append({"text": text, "id": id_, "distance": distance})

    return chunks
