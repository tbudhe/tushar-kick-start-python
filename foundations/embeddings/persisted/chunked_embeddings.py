import chromadb

client = chromadb.PersistentClient("./revit_db_2")

collection = client.get_or_create_collection(name="revit_docs_2")


def chunk_text(text, chunk_size=200, overlap=50):
    # chunk_size and overlap are in characters (real systems use tokens)
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start = end - overlap   # step back by 'overlap' so chunks share text
    return chunks


doc = ("In Revit, walls are created using the Wall tool in the Architecture tab. "
       "You can choose between basic walls and curtain walls. "
       "Curtain walls are made of panels and mullions. "
       "To edit a wall profile, select the wall and click Edit Profile.")
documents = []
ids = []
for i, chunk in enumerate(chunk_text(doc, chunk_size=150, overlap=40)):
    print(f"Chunk {i}: {chunk!r}\n")
    documents.append(chunk)
    ids.append(str(i))


collection.add(documents=documents, ids=ids)

# result = collection.query(query_texts="How do I add windows in Revit?",n_results=1)
results = collection.query(
    query_texts=["How do I make a curved wall in Revit?"],
    n_results=3,
    include=["documents", "distances"]  # ask for the scores
)

print(results["documents"])
print(results["distances"])
print(collection.count())
