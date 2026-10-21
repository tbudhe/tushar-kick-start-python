# day59_auto.py - Day 59 producer for the autoretry version
import time

from celery_lab.day59_tasks import call_api_auto

start = time.time()
result = call_api_auto.delay(8)
print(f"sent task id: {result.id}")

value = result.get(timeout=60)
elapsed = time.time() - start
print(f"result: {value}  (took {elapsed:.1f}s)")