# celery_demo.py - the PRODUCER: asks for the work, never does it
import time

from tasks import ingest_task

result = ingest_task.delay()           # drop ticket on queue (/0) -> returns instantly
print(f"task_id: {result.id}")

start = time.time()
while not result.ready():              # ready() = SUCCESS or FAILURE yet?
    print(f"{time.time() - start:5.1f}s  {result.state}")   # read status screen (/1)
    time.sleep(1)

print(f"{time.time() - start:5.1f}s  {result.state}")
print(f"result: {result.get()}")       # the dict run_ingest() returned