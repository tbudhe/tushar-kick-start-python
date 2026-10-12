from celery_lab.day53_tasks import fake_llm_task
import time

start = time.time()
handles = []
for n in range(4):
    handles.append(fake_llm_task.delay(n))
print(f"sent 4 tasks at {time.time() - start:.1f}s")       # how long did SENDING take?

results = []
for h in handles:
    results.append(h.get())
    print(f"  got {results[-1]} at {time.time() - start:.1f}s")   # when did EACH result arrive?

print(f"results: {results}")
print(f"elapsed: {time.time() - start:.1f}s")