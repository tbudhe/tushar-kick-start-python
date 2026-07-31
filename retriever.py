from pathlib import Path

import chromadb

# Anchor the DB path to THIS file's directory, not the process's cwd —
# otherwise launching uvicorn from elsewhere silently creates an empty DB.
DB_PATH = str(Path(__file__).parent / "revit_db_07_25")

client = chromadb.PersistentClient(DB_PATH)

collection = client.get_or_create_collection(name="revit_docs_project_2")


def retrieve(question, category=None, threshold=1.2):
    results = collection.query(
        query_texts=[question],
        where={"category": category} if category else None,
        n_results=2,
        include=["documents", "distances"]
    )

    chunks = []
    for text, id_, distance in zip(
        results["documents"][0], results["ids"][0], results["distances"][0]
    ):
        if distance < threshold:
            chunks.append({"text": text, "id": id_, "distance": distance})

    return chunks
