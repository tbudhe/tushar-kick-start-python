# day59_retry.py - Day 59 producer: send one call_api and time it
import time

from celery_lab.day59_tasks import call_api

start = time.time()
result = call_api.delay(7)               # send to Redis, returns at once
print(f"sent task id: {result.id}")

value = result.get(timeout=60)           # wait here until the worker finishes
elapsed = time.time() - start
print(f"result: {value}  (took {elapsed:.1f}s)")