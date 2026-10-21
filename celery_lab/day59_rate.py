# day59_rate.py - Day 59: send 5 call_llm at once, time how long they take
import time

from celery_lab.day59_tasks import call_llm

start = time.time()
results = []
for n in range(5):
    results.append(call_llm.delay(n))     # all 5 land in Redis at the same moment

for result in results:
    result.get(timeout=60)                # wait for every one
print(f"5 tasks done in {time.time() - start:.1f}s")