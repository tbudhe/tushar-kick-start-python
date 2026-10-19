# day57_chord.py - Day 57: group + callback (chord = Promise.all(...).then(summarize), on the WORKER)
import time

from celery import chord

from celery_lab.day53_tasks import fake_llm_task, summarize_task

start = time.time()
header = [fake_llm_task.s(n) for n in range(4)]   # the 4 parallel calls (same as Day 55's group)
result = chord(header)(summarize_task.s())        # attach the callback AND send; returns the CALLBACK's handle
print(f"sent chord at {time.time() - start:.1f}s")

summary = result                      # waits for summarize_task, not for the 4 tasks
print(f"summary: {summary}")
print(f"elapsed: {time.time() - start:.1f}s")