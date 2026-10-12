# AI/ML Learning Lab

Hands-on curriculum for building LLM applications (tokenization, embeddings, RAG, prompting, agents, async workers) with the Claude API and a running Autodesk Revit example.

## Structure

| Folder | What's in it |
| --- | --- |
| [revit_rag/](revit_rag/) | **Project 2:** RAG API over Revit help docs (FastAPI + ChromaDB). `app`, `rag_service`, `retriever`, `ingest_corpus`, `corpus/` |
| [revit_rag/evaluation/](revit_rag/evaluation/) | Deterministic evals, retrieval-precision harness, RAGAS evals, corpus audit |
| [chatbots/](chatbots/) | **Project 1:** streaming multi-turn chatbot, tool use, chain-of-thought; stocks agent loop |
| [agents/](agents/) | Day 31–52: LangChain tools, ReAct, streaming/async agents, LlamaIndex, LangGraph graphs, memory, persistence |
| [celery_lab/](celery_lab/) | Day 53–55: Celery background ingest, pool choice (threads vs processes), `group` |
| [foundations/](foundations/) | ML basics, tokenization, embeddings, vector DB, RAG basics, metadata filtering, prompting, notebooks |
| [system_design/](system_design/) | System-design practice code (consistent hashing) |
| [practice/](practice/) | NumPy/Pandas tutorials, data analysis, LeetCode practice |
| [scratch/](scratch/) | Experiments not tied to the curriculum |

Learning log: `STATUS.md` (current position), `LEARNING_NOTES.md` (per-day notes).

## Setup

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env    # fill in CLAUDE_API_KEY
```

## Running code — always from the repo root

Use `python -m folder.file` (no `.py`). Running from the root lets every folder import `revit_rag` — like running `node` from the project root so `node_modules` resolves.

```bash
python -m revit_rag.ingest_corpus              # build the vector DB from corpus/
uvicorn revit_rag.app:app --reload             # serve the RAG API (try revit_rag/api.http)
python -m revit_rag.evaluation.precision_eval  # retrieval precision, $0
python -m agents.day50_rag_tool                # agent that uses the RAG as a tool

celery -A celery_lab.day53_tasks worker --loglevel=info   # terminal 1 (needs Redis)
python -m celery_lab.day55_group                          # terminal 2
```

Chroma DB folders (`revit_db_07_25/`, `metadata_filter/`, ...) and `memory.db` are generated output and gitignored.
