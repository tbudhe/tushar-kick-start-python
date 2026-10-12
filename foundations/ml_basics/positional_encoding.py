tokens = ["dog", "bites", "man"]
embeddings = [[0.2, 0.8], [0.5, 0.5], [0.9, 0.1]]  # pretend embeddings

def add_position(embedding, position):
    return [v + position * 0.01 for v in embedding]  # simplified position signal

positioned = [add_position(emb, i) for i, emb in enumerate(embeddings)]
print(positioned)