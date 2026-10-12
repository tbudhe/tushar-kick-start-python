import os, time
from concurrent.futures import ProcessPoolExecutor

def fake_embedding_math(n):
    print(f"task {n}: pid={os.getpid()}")
    total = 0
    for i in range(80_000_000):
        total += i
    return total

if __name__ == "__main__":
    start = time.time()
    for n in range(4):
        fake_embedding_math(n)
    print(f"solo:      {time.time() - start:.1f}s")

    start = time.time()
    with ProcessPoolExecutor(max_workers=4) as pool:
        list(pool.map(fake_embedding_math, range(4)))
    print(f"processes: {time.time() - start:.1f}s")
