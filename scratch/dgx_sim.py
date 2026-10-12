"""
dgx_sim.py — a discrete-event simulator for a cluster of NVIDIA DGX nodes.

Week 1 scope: gang scheduling of multi-GPU jobs onto 8-GPU nodes, three
scheduling policies, and the metrics that let you compare them.

Run it:      python3 dgx_sim.py
Stdlib only. No numpy, no pandas, no install.

The question this answers: on a fixed fleet of DGX nodes, how much does the
*scheduling policy* change queue wait and GPU utilisation, holding the
workload constant? Answer (spoiler): a lot, and the reason is fragmentation.
"""

from __future__ import annotations

import heapq
import random
import statistics
from collections import defaultdict
from dataclasses import dataclass, field

# --- Hardware model -------------------------------------------------------
# DGX H100: 8x H100 SXM, 80 GB HBM3 each, NVLink/NVSwitch inside the node.
# The NVLink domain is why a job wants all its GPUs on ONE node: crossing
# nodes drops you to InfiniBand and the collective gets much slower.
GPUS_PER_NODE = 8
HBM_GB_PER_GPU = 80


@dataclass(frozen=True)
class Job:
    jid: int
    arrival: float          # seconds
    gpus: int               # gang size — needs all of them, at once, same node
    duration: float         # seconds of runtime once it starts
    mem_gb: float           # HBM needed per GPU
    kind: str               # "inference" | "finetune" | "training"


@dataclass
class Node:
    node_id: int
    free: set[int] = field(default_factory=lambda: set(range(GPUS_PER_NODE)))

    @property
    def n_free(self) -> int:
        return len(self.free)


@dataclass
class Run:
    job: Job
    node_id: int
    gpus: tuple[int, ...]
    start: float
    end: float

    @property
    def wait(self) -> float:
        return self.start - self.job.arrival


# --- Placement ------------------------------------------------------------

def place(nodes: list[Node], job: Job, *, best_fit: bool) -> tuple[int, tuple[int, ...]] | None:
    """Find a node with room for the whole gang. None if nowhere fits.

    best_fit picks the *tightest* node that still fits, which leaves the
    roomy nodes intact for the 8-GPU jobs. first-fit just takes the first.
    """
    if job.gpus > GPUS_PER_NODE or job.mem_gb > HBM_GB_PER_GPU:
        raise ValueError(f"job {job.jid} can never be placed on this hardware")

    candidates = [n for n in nodes if n.n_free >= job.gpus]
    if not candidates:
        return None
    node = min(candidates, key=lambda n: n.n_free) if best_fit else candidates[0]
    gpus = tuple(sorted(node.free)[: job.gpus])
    return node.node_id, gpus


# --- Schedulers -----------------------------------------------------------
# Each returns the jobs to start RIGHT NOW, in order. The simulator does the
# bookkeeping; the policy only decides.

# A policy returns the jobs it started, each with the node and GPUs it took.
Started = list[tuple[Job, int, tuple[int, ...]]]


def fifo(queue: list[Job], nodes: list[Node], running: list[Run], now: float) -> Started:
    """Strict head-of-line. If the oldest job can't fit, nothing else runs.

    Fair, and terrible for utilisation: one queued 8-GPU job idles the whole
    fleet while 1-GPU jobs sit behind it. This is the baseline to beat.
    """
    started: Started = []
    while queue:
        spot = place(nodes, queue[0], best_fit=False)
        if spot is None:
            break
        job = queue.pop(0)
        _claim(nodes, spot)
        started.append((job, *spot))
    return started


def greedy(queue: list[Job], nodes: list[Node], running: list[Run], now: float) -> Started:
    """Run anything that fits, oldest first. Max utilisation, no fairness.

    Big gang jobs can starve indefinitely — watch the mean wait for
    'training' specifically, not the average across all jobs.
    """
    started: Started = []
    skipped: list[Job] = []
    for job in queue:
        spot = place(nodes, job, best_fit=True)
        if spot is None:
            skipped.append(job)
            continue
        _claim(nodes, spot)
        started.append((job, *spot))
    queue[:] = skipped
    return started


def easy_backfill(queue: list[Job], nodes: list[Node], running: list[Run], now: float) -> Started:
    """EASY backfill: the head job gets a reservation, others fill the gaps.

    This is what real HPC schedulers (Slurm, LSF) do. Compute when the head
    job *would* start — its 'shadow time' — then let any smaller job run now
    as long as it finishes before then. Nobody delays the head job, and the
    holes get filled. Best of both, and only ~20 lines.
    """
    started: Started = []
    while queue:
        spot = place(nodes, queue[0], best_fit=True)
        if spot is None:
            break
        job = queue.pop(0)
        _claim(nodes, spot)
        started.append((job, *spot))

    if not queue:
        return started

    head = queue[0]
    shadow = _shadow_time(head, nodes, running, now)

    survivors: list[Job] = []
    for job in queue:
        if job is head or now + job.duration > shadow:
            survivors.append(job)
            continue
        spot = place(nodes, job, best_fit=True)
        if spot is None:
            survivors.append(job)
            continue
        _claim(nodes, spot)
        started.append((job, *spot))
    queue[:] = survivors
    return started


def _shadow_time(head: Job, nodes: list[Node], running: list[Run], now: float) -> float:
    """Earliest time enough GPUs free up on ONE node for the head job."""
    per_node = defaultdict(list)
    for run in running:
        per_node[run.node_id].append(run)

    best = float("inf")
    for node in nodes:
        free = node.n_free
        if free >= head.gpus:
            return now
        for run in sorted(per_node[node.node_id], key=lambda r: r.end):
            free += len(run.gpus)
            if free >= head.gpus:
                best = min(best, run.end)
                break
    return best


def _claim(nodes: list[Node], spot: tuple[int, tuple[int, ...]]) -> None:
    node_id, gpus = spot
    nodes[node_id].free -= set(gpus)


# --- Simulator ------------------------------------------------------------

def simulate(jobs: list[Job], n_nodes: int, policy) -> dict:
    """Event-driven loop. Time only advances to the next arrival or finish —
    no fixed tick, so a 12-hour training run costs one event, not 43,200."""
    nodes = [Node(i) for i in range(n_nodes)]
    pending = sorted(jobs, key=lambda j: j.arrival)
    queue: list[Job] = []
    running: list[Run] = []
    finished: list[Run] = []
    finish_heap: list[tuple[float, int]] = []  # (end_time, jid)
    now = 0.0

    while pending or queue or running:
        # Advance to the next thing that can change the world.
        next_arrival = pending[0].arrival if pending else float("inf")
        next_finish = finish_heap[0][0] if finish_heap else float("inf")
        now = min(next_arrival, next_finish)
        if now == float("inf"):
            break

        while pending and pending[0].arrival <= now:
            queue.append(pending.pop(0))

        while finish_heap and finish_heap[0][0] <= now:
            _, jid = heapq.heappop(finish_heap)
            run = next(r for r in running if r.job.jid == jid)
            running.remove(run)
            finished.append(run)
            nodes[run.node_id].free |= set(run.gpus)

        for job, node_id, gpus in policy(queue, nodes, running, now):
            run = Run(job, node_id, gpus, now, now + job.duration)
            running.append(run)
            heapq.heappush(finish_heap, (run.end, job.jid))

    return _metrics(finished, n_nodes)


def _metrics(finished: list[Run], n_nodes: int) -> dict:
    waits = sorted(r.wait for r in finished)
    makespan = max(r.end for r in finished)
    gpu_seconds_used = sum(len(r.gpus) * r.job.duration for r in finished)
    gpu_seconds_available = n_nodes * GPUS_PER_NODE * makespan

    by_kind = defaultdict(list)
    for r in finished:
        by_kind[r.job.kind].append(r.wait)

    return {
        "jobs": len(finished),
        "makespan_h": makespan / 3600,
        "utilisation": gpu_seconds_used / gpu_seconds_available,
        "wait_mean_m": statistics.mean(waits) / 60,
        "wait_p99_m": waits[int(len(waits) * 0.99)] / 60,
        "wait_by_kind_m": {k: statistics.mean(v) / 60 for k, v in sorted(by_kind.items())},
    }


# --- Workload -------------------------------------------------------------

def workload(n: int = 400, seed: int = 7) -> list[Job]:
    """A realistic-ish enterprise mix: lots of small inference, a few whales.

    The shape matters more than the numbers. Change the ratios and watch
    which policy wins — that's the experiment.
    """
    rng = random.Random(seed)
    shapes = [
        # (kind,        weight, gpus,        duration_s,           mem_gb)
        ("inference",   0.70,   lambda: 1,   lambda: rng.expovariate(1 / 900),   40),
        ("finetune",    0.22,   lambda: rng.choice([2, 4]), lambda: rng.expovariate(1 / 7200), 70),
        ("training",    0.08,   lambda: 8,   lambda: rng.expovariate(1 / 28800), 78),
    ]
    kinds = [s[0] for s in shapes]
    weights = [s[1] for s in shapes]
    lookup = {s[0]: s for s in shapes}

    jobs, t = [], 0.0
    for jid in range(n):
        t += rng.expovariate(1 / 240)  # a job arrives every ~4 min on average
        kind = rng.choices(kinds, weights)[0]
        _, _, gpus_fn, dur_fn, mem = lookup[kind]
        jobs.append(Job(jid, t, gpus_fn(), max(60.0, dur_fn()), mem, kind))
    return jobs


# --- Report ---------------------------------------------------------------

def main() -> None:
    jobs = workload()
    n_nodes = 4
    fleet = n_nodes * GPUS_PER_NODE

    print(f"\n{len(jobs)} jobs onto {n_nodes} DGX nodes ({fleet} GPUs)\n")
    mix = defaultdict(int)
    for j in jobs:
        mix[j.kind] += 1
    print("  mix: " + ", ".join(f"{k} {v}" for k, v in sorted(mix.items())) + "\n")

    header = f"{'policy':<16}{'util':>8}{'wait avg':>11}{'wait p99':>11}{'makespan':>11}"
    print(header)
    print("-" * len(header))

    for name, policy in [("fifo", fifo), ("greedy", greedy), ("easy-backfill", easy_backfill)]:
        m = simulate(jobs, n_nodes, policy)
        print(
            f"{name:<16}{m['utilisation']:>7.1%}"
            f"{m['wait_mean_m']:>10.0f}m{m['wait_p99_m']:>10.0f}m{m['makespan_h']:>10.1f}h"
        )

    print("\nwait by job kind (minutes, mean):")
    for name, policy in [("fifo", fifo), ("greedy", greedy), ("easy-backfill", easy_backfill)]:
        m = simulate(jobs, n_nodes, policy)
        detail = "  ".join(f"{k}={v:.0f}" for k, v in m["wait_by_kind_m"].items())
        print(f"  {name:<16}{detail}")

    print(
        "\nRead the 'training' column. greedy wins on average wait and loses"
        "\nbadly on the 8-GPU jobs — that's starvation, and it's the whole"
        "\nargument for backfill over pure greedy packing.\n"
    )


if __name__ == "__main__":
    main()
