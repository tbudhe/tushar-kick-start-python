# day56_send.py - Day 56: send 2 LLM tasks + 2 embed tasks, see who ran each
from celery_lab.day56_queues import fake_llm, fake_embed

handles = [
    fake_llm.delay(0),      # task_routes -> "llm" queue
    fake_llm.delay(1),
    fake_embed.delay(0),    # task_routes -> "ingest" queue
    fake_embed.delay(1),
]

for h in handles:
    try:
        print(h.get())    # each task returns "<name> <n> -> ran on <worker>"
    except Exception as error:
        print(f"error: {error!r}")