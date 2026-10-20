# day58_acks.py - Day 58: send ONE slow task, survive a worker kill
import time

from celery_lab.day58_tasks import slow_task

start = time.time()
result = slow_task.delay(7)           # A: send it to the queue (same call you used on Day 53)
print(f"sent task id: {result.id}")       # compare this id with the worker log after the restart

answer = result.get(timeout=120)    # B: block until the result lands in Redis
print(f"result: {answer}")
print(f"elapsed: {time.time() - start:.1f}s")