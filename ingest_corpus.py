"""Ingest the real Autodesk Revit help corpus into a NEW collection.

Blue/green: revit_docs_project_2 (the 6 toy one-liners) is left untouched so
step 2 can compare the two side by side instead of relying on memory.
"""
import json
from pathlib import Path

# client comes from retriever.py — same PersistentClient, same DB_PATH.
# Importing it (instead of making a second one) is what guarantees both
# collections live in the same revit_db_07_25 directory.
from retriever import client

CORPUS_DIR = Path(__file__).parent / "corpus" / "revit_help"
MANIFEST = CORPUS_DIR / "manifest.json"
NEW_COLLECTION = "revit_docs_v2"
MAX_CHARS = 600


def chunk_paragraphs(text, max_chars=MAX_CHARS):
    """Split on blank lines, then merge consecutive paragraphs until adding
    the next one would cross max_chars. Keeps whole paragraphs intact —
    a numbered step never gets cut in half."""
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    chunks, current = [], ""
    for para in paragraphs:
        if current and len(current) + len(para) + 2 > max_chars:
            chunks.append(current)
            current = para
        else:
            current = f"{current}\n\n{para}" if current else para
    if current:
        chunks.append(current)
    return chunks


if __name__ == "__main__":
    manifest = json.loads(MANIFEST.read_text())
    collection = client.get_or_create_collection(name=NEW_COLLECTION)

    print(f"=== INGEST corpus/revit_help -> {NEW_COLLECTION} ===")
    total_chunks = 0

    for entry in manifest:
        path = CORPUS_DIR / entry["file"]
        text = path.read_text()
        chunks = chunk_paragraphs(text)

        ids, documents, metadatas = [], [], []
        for i, chunk in enumerate(chunks):
            # YOUR CALL: prepend the title so the chunk carries its own topic
            # into the VECTOR, e.g. f"{entry['title']}\n\n{chunk}".
            # Chunk 3 of place_a_door.md is a bare options table — it never
            # says the word "door". Prepending fixes that and costs you
            # 3 words of dilution on every chunk. Decide, don't default.
            documents.append(chunk)

            ids.append(f"{path.stem}_{i}")          # stable -> upsert, not duplicate
            metadatas.append({
                "source_file": entry["file"],
                "title": entry["title"],
                "category": entry["category"],
                "revit_version": entry["revit_version"],
                "source_url": entry["source_url"],
                "chunk_index": i,
            })

        collection.upsert(ids=ids, documents=documents, metadatas=metadatas)
        total_chunks += len(chunks)

        words = len(text.split())
        print(f"{entry['file']:24} {entry['category']:8} "
              f"v{entry['revit_version']}  {words:5} words -> {len(chunks):2} chunks")

    old = client.get_or_create_collection(name="revit_docs_project_2")
    print(f"\n{len(manifest)} files -> {total_chunks} chunks  |  "
          f"collection {NEW_COLLECTION} count: {collection.count()}")
    print(f"old collection revit_docs_project_2 count: {old.count()}   (untouched)")