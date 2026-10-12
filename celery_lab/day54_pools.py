import time
from concurrent.futures import ThreadPoolExecutor

import os, threading

def fake_llm_call(n):
    time.sleep(2)
    return n

start = time.time()
for n in range(4):             # like --pool=solo: one task at a time
    fake_llm_call(n)
print(f"solo:    {time.time() - start:.1f}s")

start = time.time()
with ThreadPoolExecutor(max_workers=4) as pool:   # like --pool=threads
    list(pool.map(fake_llm_call, range(4)))
print(f"threads: {time.time() - start:.1f}s")