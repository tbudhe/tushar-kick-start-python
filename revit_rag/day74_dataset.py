"""Day 74 step 2 - upload the golden questions to LangSmith (run once)."""
from dotenv import load_dotenv
from langsmith import Client

load_dotenv()          # loads LANGSMITH_API_KEY from .env into os.environ
ls = Client()          # Client reads LANGSMITH_API_KEY by itself

DATASET = "revit-rag-golden"
QUESTIONS = [          # same 5 questions as day62_judge.py
    "How do I create a wall in Revit?",
    "How do I add a door to a wall?",
    "How do I place a window?",
    "What is a floor plan view?",
    "How do I export a model to DWG?",
]

if ls.has_dataset(dataset_name=DATASET):
    print(f"dataset '{DATASET}' already exists - skipping")
else:
    ls.create_dataset(DATASET, description="Revit how-to questions for RAG faithfulness evals")
    ls.create_examples(
        dataset_name=DATASET,
        examples=[{"inputs": {"question": q}} for q in QUESTIONS],
    )
    print(f"created '{DATASET}' with {len(QUESTIONS)} examples")