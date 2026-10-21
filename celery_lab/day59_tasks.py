# day59_tasks.py - Day 59: retry with backoff on a fake 429
from celery import Celery

app = Celery(
    "day59_tasks",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/1",
)
app.conf.worker_pool = "threads"
app.conf.worker_concurrency = 4


class RateLimited(Exception):          # stands in for HTTP 429 Too Many Requests
    pass


def fake_api(attempt):
    if attempt < 3:                    # first 3 calls get throttled
        raise RateLimited("429 Too Many Requests")
    return "200 OK"


@app.task(bind=True, autoretry_for=(RateLimited,), retry_backoff=True, max_retries=5)
def call_api_auto(self, n):
    attempt = self.request.retries
    print(f"[worker] call_api_auto {n} attempt {attempt}")
    status = fake_api(attempt)         # raises RateLimited -> Celery retries for us
    print(f"[worker] call_api_auto {n} -> {status}")
    return f"ok {n} after {attempt} retries"

@app.task(rate_limit="1/s")            # THIS worker starts at most 1 call_llm per second
def call_llm(n):
    print(f"[worker] call_llm {n} started")   # worker log timestamp shows the spacing
    return n