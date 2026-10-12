from sentence_transformers import SentenceTransformer, util
model = SentenceTransformer('all-MiniLM-L6-V2')
sentences = [
    "Autodesk Revit is used for building design",
    "Architects use Revit for structural modeling",
    "I enjoy eating pasta for dinner"
]

embeddings = model.encode(sentences)
print(f"S1 vs S2: {util.cos_sim(embeddings[0], embeddings[1]).item():.2f}")
print(f"S1 vs S3: {util.cos_sim(embeddings[0], embeddings[2]).item():.2f}")
print(f"S2 vs S3: {util.cos_sim(embeddings[1], embeddings[2]).item():.2f}")