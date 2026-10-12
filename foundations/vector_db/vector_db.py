import chromadb

client = chromadb.PersistentClient("./revit_db")

collection = client.get_or_create_collection(name="revit_docs")

collection.add(
    documents=[
        "In Revit, You can create curve wall using the Arc Wall tool.",
        "To add the Window in Revit, use the window tool on existing wall",
         "To add a door in Revit, use the Door tool on an existing wall.",
        "To create a wall in Revit, use the Wall tool in the Architecture tab.",
        "To create a floor in Revit, use the Floor tool and sketch the boundary.",
    ],
    ids = ["doc1","doc2","doc3", "doc4", "doc5"]
)

# result = collection.query(query_texts="How do I add windows in Revit?",n_results=1)
results = collection.query(
    query_texts=["How do I add a door in Revit?"],
    n_results=3,
    include=["documents", "distances"]  # ask for the scores
)

# print(results["documents"])
# print(results["distances"])
print("Count: " , collection.count())
print(collection.peek())   # shows first few docs + metadata