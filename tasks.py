# tasks.py - Celery app + the ingest task
import time

from celery import Celery

from ingest_corpus import run_ingest

app = Celery(
    "tasks",
    broker="redis://localhost:6379/0",    # the queue (kitchen rail)
    backend="redis://localhost:6379/1",   # the status screen (results)
)
app.conf.task_track_started = True        # report STARTED, not just PENDING -> SUCCESS


@app.task
def ingest_task():
    print("[worker] ingest started")
    time.sleep(5)                         # demo only: so you can SEE "STARTED"
    return run_ingest()                   # {"files": 7, "chunks": 18} -> stored in Redis