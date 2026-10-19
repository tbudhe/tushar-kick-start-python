# day57_flip.py - Day 57 exercise: async blue/green flip (chord -> flip only after ALL ingests finish)
import time

from celery import chord

from celery_lab.day53_tasks import fake_llm_task, flip_task          # blank 1: the callback you just wrote

start = time.time()
header = [fake_llm_task.s(n) for n in [5, 6, 7]]                    # 3 "files": 5, 6 and 7 chunks                 # blank 2: the 3 chunk counts
result = chord(header)(flip_task.s())                               # blank 3: same as blank 1
print(f"sent flip chord at {time.time() - start:.1f}s")

flip = result.get()                                                 # wait for the flip callback
print(flip)
print(f"elapsed: {time.time() - start:.1f}s")