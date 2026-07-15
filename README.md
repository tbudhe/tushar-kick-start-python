# AI/ML Learning Lab

Personal, hands-on curriculum for learning the building blocks of LLM applications: tokenization, embeddings, retrieval-augmented generation (RAG), prompting, and vector databases — using the Claude API and a running Autodesk Revit example.

Organized by topic rather than by week, so related exercises stay together regardless of when they were written.

## Structure

| Folder | What's in it |
| --- | --- |
| [tokenization/](tokenization/) | How text becomes tokens (`tiktoken`) |
| [embeddings/similarity/](embeddings/similarity/) | Sentence embeddings + cosine similarity |
| [embeddings/persisted/](embeddings/persisted/) | Chunking text and persisting embeddings to Chroma |
| [rag/basics/](rag/basics/) | Minimal retrieval-augmented generation from scratch |
| [rag/metadata-filtering/](rag/metadata-filtering/) | Filtering Chroma retrieval results by metadata |
| [prompting/](prompting/) | Few-shot prompting with the Claude API |
| [vector-db/](vector-db/) | Basic Chroma persistent vector store usage |
| [ml-foundations/](ml-foundations/) | Train/test splits, overfitting demo, k-means, self-supervised training pairs, positional encoding |
| [chatbots/revit-chatbot/](chatbots/revit-chatbot/) | Multi-turn streaming chatbot, tool use, and chain-of-thought prompting with the Claude API |
| [deepfashion-multimodal-rag/](deepfashion-multimodal-rag/) | In-progress: DeepFashion dataset for a multimodal RAG project |
| [exercises/](exercises/) | NumPy/Pandas tutorials, data analysis practice, LeetCode-style practice |
| [notebooks/](notebooks/) | Jupyter notebooks (conceptual walkthroughs) |
| [scratch/](scratch/) | Empty/in-progress files not yet tied to a topic |

Chroma-backed scripts (`embeddings/persisted`, `rag/metadata-filtering`, `vector-db`) write their database files next to the script when run (e.g. `revit_db/`) — these are regenerated output and gitignored, not source.

## Setup

```bash
pip3 install -r requirements.txt

cp .env.example .env
# then fill in CLAUDE_API_KEY (and OPENAI_API_KEY if needed)
```

## Running an exercise

Each script assumes it's run from its own directory (relative paths for Chroma DBs and CSVs are relative to cwd):

```bash
cd prompting
python3 claude_prompting.py
```

## Requirements

- Python 3.13
- A `CLAUDE_API_KEY` (Anthropic) for anything under `prompting/` and `chatbots/`
