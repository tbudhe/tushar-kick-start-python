from pathlib import Path

import chromadb

# Same anchoring as retriever.py — both must point at the SAME directory.
DB_PATH = str(Path(__file__).parent / "revit_db_07_25")

client = chromadb.PersistentClient(DB_PATH)

collection = client.get_or_create_collection(name="revit_docs_project_2")


if __name__ == "__main__":
    collection.upsert(
        documents=[
            "In Revit, You can create curve wall using the Arc Wall tool.",
            "To add the Window in Revit, use the window tool on existing wall",
            "To add a door in Revit, use the Door tool on an existing wall.",
            "To create a wall in Revit, use the Wall tool in the Architecture tab.",
            "To create a floor in Revit, use the Floor tool and sketch the boundary.",
        ],
        ids=["doc1", "doc2", "doc3", "doc4", "doc5"],
        metadatas=[{"category": "walls"},  {"category": "windows"}, {
            "category": "doors"}, {"category": "walls"}, {"category": "floors"}]
    )

    print("Count: ", collection.count())
    print(collection.peek())   # shows first few docs + metadata
