# day53_tasks.py - Celery app + ingest_task (Day 53) + fake_llm_task (Day 54)
import time

from celery import Celery

from ingest_corpus import run_ingest

app = Celery(
    "day53_tasks_1",
    broker="redis://localhost:6379/0",    # the queue (kitchen rail)
    backend="redis://localhost:6379/1",   # the status screen (results)
)
app.conf.task_track_started = True        # report STARTED, not just PENDING -> SUCCESS
app.conf.worker_pool = "threads"          # Day 54: same as --pool=threads (IO-bound tasks)
app.conf.worker_concurrency = 4           # Day 54: same as --concurrency=4 (CLI flags override these)

@app.task
def ingest_task():
    print("[worker] ingest started")
    time.sleep(5)                         # demo only: so you can SEE "STARTED"
    return run_ingest()                   # {"files": 7, "chunks": 18} -> stored in Redis


@app.task
def fake_llm_task(n):
    print(f"[worker] fake_llm {n} started")
    time.sleep(2)                         # stands in for waiting on an LLM API (IO-bound)
    return n                              # stored in Redis /1, read back by .get()

