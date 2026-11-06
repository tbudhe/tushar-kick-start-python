import os
from pypdf import PdfReader
import numpy as np
from sentence_transformers import SentenceTransformer
import anthropic
from dotenv import load_dotenv

PDF_DIR = "revit_rag/pdfs"
CHUNK_WORDS = 120     # words per chunk
OVERLAP_WORDS = 20    # words shared between neighbouring chunks
TOP_K = 3
THRESHOLD = 0.3     # measured: real questions ~0.5, off-topic < 0.2

def load_pages(path):
    reader = PdfReader(path)
    pages = []
    for page_number, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""
        text = " ".join(text.split())          # collapse whitespace and newlines
        if text:
            pages.append((page_number, text))
        else:
            print(f"  WARNING: {path} page {page_number} has no text - scanned? needs OCR")
    print(f"loaded {os.path.basename(path)}: {len(reader.pages)} pages")
    return pages


def chunk(text):
    words = text.split()                      # a list of whole words
    chunks = []
    start = 0
    while start < len(words):
        piece = words[start:start + CHUNK_WORDS]
        chunks.append(" ".join(piece))        # glue them back into a string
        start += CHUNK_WORDS - OVERLAP_WORDS
    return chunks


CHUNKS = []
for filename in sorted(os.listdir(PDF_DIR)):
    if filename.endswith(".pdf"):
        for page_number, text in load_pages(os.path.join(PDF_DIR, filename)):
            for piece in chunk(text):
                CHUNKS.append({"text": piece, "source": filename, "page": page_number})

print(len(CHUNKS), "chunks")
print(CHUNKS[0])


model = SentenceTransformer("all-MiniLM-L6-v2")
texts = [c["text"] for c in CHUNKS]           # embed the text, keep metadata alongside
vectors = model.encode(texts, normalize_embeddings=True)
print(vectors.shape)
print(np.linalg.norm(vectors[0]))

def retrieve(question):
    q = model.encode(question, normalize_embeddings=True)
    scores = vectors @ q                          # similarity to all 107 chunks at once
    best = np.argsort(scores)[::-1][:TOP_K]       # indexes of the highest scores
    return [(int(i), round(float(scores[i]), 2)) for i in best if scores[i] > THRESHOLD]


for question in ["What is the difference between RAG-Sequence and RAG-Token?",
                 "What is the capital of France?"]:
    hits = retrieve(question)
    print(question)
    print("  hits (chunk, score):", hits)
    for i, score in hits:
        print(f"    page {CHUNKS[i]['page']}: {CHUNKS[i]['text'][:80]}")


load_dotenv()
client = anthropic.Anthropic(api_key=os.getenv("CLAUDE_API_KEY"))

SYSTEM = ("Answer ONLY from the sources in the user's message, in 2-3 sentences. "
          "Cite pages like [page 3]. If the sources don't contain the answer, reply exactly: I don't know.")


def answer(question):
    hits = retrieve(question)
    if not hits:
        return "I don't know. (no chunk passed the threshold - LLM not called)"
    context = "\n\n".join(f"[page {CHUNKS[i]['page']}] {CHUNKS[i]['text']}" for i, _ in hits)
    response = client.messages.create(
        model="claude-opus-4-8",
        max_tokens=300,
        system=SYSTEM,
        messages=[{"role": "user", "content": f"Sources:\n{context}\n\nQuestion: {question}"}],
    )
    return response.content[0].text


for question in ["What is the difference between RAG-Sequence and RAG-Token?",
                 "What is the capital of France?"]:
    print("\nQ:", question)
    print("A:", answer(question))