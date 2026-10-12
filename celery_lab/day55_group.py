# day55_group.py - Day 55: collect 4 results with ONE wait (group = Promise.all)
import time

from celery import group

from celery_lab.day53_tasks import fake_llm_task

start = time.time()
job = group(fake_llm_task.s(n) for n in range(4))   # 4 packed calls, not sent yet
result = job.apply_async()                           # send all 4 at once
print(f"sent group at {time.time() - start:.1f}s")

results = result.get()                               # ONE wait for all 4
print(f"results: {results}")
print(f"elapsed: {time.time() - start:.1f}s")