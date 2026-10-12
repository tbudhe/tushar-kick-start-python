from sentence_transformers import SentenceTransformer, util
# Our fake "Autodesk documentation" — 5 chunks
docs = [
    "In Revit, you can create a curved wall using the Arc Wall tool under the Architecture tab.",
    "Fusion 360 supports parametric modeling for mechanical parts and assemblies.",
    "AutoCAD allows you to draw 2D floor plans with precision using coordinate input.",
    "To add a door in Revit, select the Door tool and click on any existing wall.",
    "Revit families are reusable components like windows, doors, and furniture.",
]

# Step 1 — embed all doc chunks once and store them
model = SentenceTransformer("all-MiniLM-L6-v2")
doc_embeddings = model.encode(docs)

# Step 2 — embed the user's question
question = "How do I create a curved wall in Revit?"
question_embedding = model.encode(question)

# Step 3 — cosine similarity: question vs every chunk
scores = util.cos_sim(question_embedding, doc_embeddings)[0]

# Step 4 — find the top 2 most relevant chunks
top_2 = scores.topk(2)
print("Top matching chunks:\n")
for score, idx in zip(top_2.values, top_2.indices):
    print(f"Score: {score:.2f} → {docs[idx]}\n")


documentTwo = [
    "In Revit, you can create a curved wall using the Arc Wall tool under the Architecture tab.",
    "Fusion 360 supports parametric modeling for mechanical parts and assemblies.",
    "AutoCAD allows you to draw 2D floor plans with precision using coordinate input.",
    "To add a door in Revit, select the Door tool and click on any existing wall.",
    "Revit families are reusable components like windows, doors, and furniture.",
    "To add a window in Revit, use the Window tool and place it on an existing wall."]
doc_embeddings_two = model.encode(documentTwo)

question_two = "How do I add a window in Revit?"
question_embedding_two = model.encode(question_two)

scores_two = util.cos_sim(question_embedding_two, doc_embeddings_two)[0]

top_2_2 = scores_two.topk(2)
print("Top matching chunks 2:\n")
for score, idx in zip(top_2_2.values, top_2_2.indices):
    print(f"Score: {score:.2f} → {documentTwo[idx]}\n")
