from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import anthropic
import os
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("CLAUDE_API_KEY"))

# 1. Tiny in-memory "knowledge base" — same idea as your Day 3 docs list
docs = [
    "The Eiffel Tower is located in Paris, France.",
    "Python was created by Guido van Rossum in 1991.",
    "ChromaDB is a vector database used for storing embeddings.",
]

# 2. Same embedding model you used on Day 2/3
model = SentenceTransformer("all-MiniLM-L6-v2")
doc_embeddings = model.encode(docs)


def retrieve(question, threshold=0.5):
    """Return the best-matching doc, or None if nothing clears the threshold."""
    q_embedding = model.encode([question])
    scores = cosine_similarity(q_embedding, doc_embeddings)[0]
    best_idx = scores.argmax()
    if scores[best_idx] < threshold:
        return None  # application-level filtering, same principle as Day 5/6
    return docs[best_idx]


# 3. Today's new piece: a system prompt that gives the model permission to refuse
SYSTEM_PROMPT = (
    "Answer ONLY using the provided context. "
    "If the context does not contain the answer, say "
    "'I don't have enough information to answer that.' "
    "Do not guess."
)

# client = anthropic.Anthropic()  # reads ANTHROPIC_API_KEY from your environment


def ask(question):
    context = retrieve(question)
    context_text = context if context else "No relevant context found."
    response = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=200,
        system=SYSTEM_PROMPT,
        messages=[{
            "role": "user",
            "content": f"Context: {context_text}\n\nQuestion: {question}"
        }]
    )
    return response.content[0].text


# 4. Test both cases
print("Grounded question (answer IS in docs):")
print(ask("Where is the Eiffel Tower?"))

print("\nUngrounded question (answer is NOT in docs):")
print(ask("What is the capital of Australia?"))