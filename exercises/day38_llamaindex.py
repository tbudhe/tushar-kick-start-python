"""Day 38 — LlamaIndex vs the hand-rolled pipeline, over identical chunks."""
import math
import os
import sys
from pathlib import Path

# exercises/ is one level below the repo root — make retriever.py importable.
# This MUST run before the repo-root imports below, not after them.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from dotenv import load_dotenv
from llama_index.core import Document, Settings, StorageContext, VectorStoreIndex
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.anthropic import Anthropic
from llama_index.vector_stores.chroma import ChromaVectorStore

from rag_service import answer_question  # noqa: E402
from retriever import client, collection, THRESHOLD, N_RESULTS  # noqa: E402


load_dotenv()

QUESTION = "How do I create a wall in Revit?"

# Pinned deliberately: this is the SAME model Chroma used by default when
# ingest.py wrote revit_docs_project_2. Unpinned, LlamaIndex reaches for OpenAI.
EMBED_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
LI_COLLECTION = "revit_docs_llamaindex"


def load_same_chunks():
    """Pull the EXACT rows the hand-rolled pipeline searches, so both
    frameworks are provably eating the same input."""
    raw = collection.get(include=["documents", "metadatas"])
    rows = list(zip(raw["ids"], raw["documents"], raw["metadatas"]))
    rows.sort(key=lambda r: r[0])
    return rows


def build_llamaindex(rows):
    Settings.embed_model = HuggingFaceEmbedding(model_name=EMBED_MODEL_NAME)
    Settings.llm = Anthropic(
        model="claude-opus-4-8",                     # default is claude-2.1
        api_key=os.getenv("CLAUDE_API_KEY"),         # not ANTHROPIC_API_KEY
        max_tokens=1024,
    )

    # from_documents ADDS — reset so re-runs stay at 6 nodes, not 12, 18, 24
    try:
        client.delete_collection(LI_COLLECTION)
    except Exception:
        pass
    li_collection = client.get_or_create_collection(name=LI_COLLECTION)

    vector_store = ChromaVectorStore(chroma_collection=li_collection)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    documents = [
        Document(
            text=text,
            metadata={"chroma_id": id_, "category": meta.get("category")},
            # Bookkeeping only — keep it OUT of the vector, so both pipelines
            # embed the identical bare sentence.
            excluded_embed_metadata_keys=["chroma_id", "category"],
        )
        for id_, text, meta in rows
    ]
    index = VectorStoreIndex.from_documents(documents,
                                            storage_context=storage_context)
    return index, li_collection


def dim_of(coll):
    """Vector width of a collection — the number Part B is about."""
    embs = coll.get(include=["embeddings"])["embeddings"]
    return len(embs[0]) if len(embs) else None


def ask_llamaindex(index, question):
    """The whole hand-rolled pipeline — retrieve, stuff context, call the
    model, return answer + sources — as one object."""
    engine = index.as_query_engine(similarity_top_k=N_RESULTS)
    response = engine.query(question)
    sources = [
        (n.node.metadata.get("chroma_id"), n.score, n.node.text)
        for n in response.source_nodes
    ]
    return str(response), sources


if __name__ == "__main__":
    rows = load_same_chunks()
    print("=== SAME CHUNKS (pulled from the existing collection) ===")
    for id_, text, meta in rows:
        print(f"{id_}  [{meta.get('category')}]  {text}")
    print(f"\n{len(rows)} chunks | THRESHOLD={THRESHOLD} N_RESULTS={N_RESULTS}\n")

    index, li_collection = build_llamaindex(rows)
    print("=== PART A setup ===")
    print(f"llamaindex collection: {LI_COLLECTION:22} "
          f"nodes: {li_collection.count()}  dim: {dim_of(li_collection)}")
    print(f"existing   collection: {'revit_docs_project_2':22} "
          f"rows : {collection.count()}  dim: {dim_of(collection)}")
    print("\n=== PART A — llamaindex ===")
    print(f"Q: {QUESTION}\n")
    li_answer, li_sources = ask_llamaindex(index, QUESTION)
    print(f"[llamaindex ]  answer : {li_answer}")
    for cid, score, text in li_sources:
        print(f"source : {cid} (score {score:.3f})  {text[:60]}")

    print("\n=== PART A — hand-rolled ===")
    hr = answer_question(QUESTION)
    print(f"[hand-rolled]  answer : {hr.answer}")
    for s in hr.sources:
        print(f"source : {s.id} (dist {s.distance:.3f})  {s.text[:60]}")

    print("\n=== COMPARISON ===")
    li_top = li_sources[0][0] if li_sources else None
    hr_top = hr.sources[0].id if hr.sources else None
    print(
        f"top chunk   llamaindex={li_top}   hand-rolled={hr_top}   MATCH: {li_top == hr_top}")
    print("\nscore vs distance — same number, two costumes:")
    for (cid, score, _), s in zip(li_sources, hr.sources):
        # -ln(0) is undefined — a zero/negative score has no distance twin
        dist = f"{-math.log(score):.3f}" if score and score > 0 else "n/a"
        print(f"  {cid}: li score {score:.3f}  ->  -ln(score) = {dist}"
              f"   |   chroma dist = {s.distance:.3f}")
    print(f"\nyour THRESHOLD {THRESHOLD} translates to a llamaindex "
          f"score cutoff of {math.exp(-THRESHOLD):.3f}")
    print("\n=== what the framework swapped out ===")
    for name, tmpl in index.as_query_engine().get_prompts().items():
        print(f"  {name}:\n{tmpl.get_template()[:220]}\n")