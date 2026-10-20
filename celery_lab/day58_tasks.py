# day58_tasks.py - Day 58: acks_late + kill a worker mid-task
import time

from celery import Celery

app = Celery(
    "day58_tasks",
    broker="redis://localhost:6379/0",    # same Redis queue as Day 53
    backend="redis://localhost:6379/1",   # same results db
)
app.conf.worker_pool = "threads"          # one process -> kill -9 takes the whole worker down
app.conf.worker_concurrency = 4
app.conf.broker_transport_options = {"visibility_timeout": 20}   # parked msg returns after 20s (default 1h)


@app.task(acks_late=False)                 # ack AFTER the task finishes, not on receive
def slow_task(n):
    print(f"[worker] slow_task {n} started")
    time.sleep(10)                        # 10s window to kill the worker mid-task
    return f"done {n}"