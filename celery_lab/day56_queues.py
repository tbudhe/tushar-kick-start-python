# day56_queues.py - Day 56: two queues, two workers, each with the right pool
import time
import random
from celery import Celery

app = Celery(
    "day56_queues",
    broker="redis://localhost:6379/0",    # same kitchen rail as Day 53
    backend="redis://localhost:6379/1",   # same status screen
)

# the ROUTES dict: task name -> queue name (a Redis list with that name)
app.conf.task_routes = {
    "fake_llm":   {"queue": "llm"},
    "fake_embed": {"queue": "ingest"},
}


@app.task(bind=True, name="fake_llm")     # bind=True -> first arg 'self' = this task run
def fake_llm(self, n):
    time.sleep(2)                         # IO-bound: waiting on an LLM API
    return f"fake_llm   {n} -> ran on {self.request.hostname}"


@app.task(bind=True, name="fake_embed")
def fake_embed(self, n):
    total = 0
    for i in range(20_000_000):           # CPU-bound: stands in for embedding math
        total += i
    return f"fake_embed {n} -> ran on {self.request.hostname}"