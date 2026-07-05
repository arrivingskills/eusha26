import asyncio
import math
import os
import time
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor


# -----------------------------
# Workloads
# -----------------------------
def io_bound_task(duration_s: float) -> float:
    """Simulated I/O: blocks the current thread (e.g., file/network wait)."""
    time.sleep(duration_s)
    return duration_s


async def io_bound_task_async(duration_s: float) -> float:
    """Simulated I/O: non-blocking wait that cooperates with the event loop."""
    await asyncio.sleep(duration_s)
    return duration_s


def cpu_bound_task(n: int) -> int:
    """
    CPU-heavy work: count primes up to n (pure Python loops -> GIL matters for threads).
    Adjust n to make this slower/faster on your machine.
    """
    count = 0
    for x in range(2, n + 1):
        is_prime = True
        r = int(math.isqrt(x))
        for d in range(2, r + 1):
            if x % d == 0:
                is_prime = False
                break
        if is_prime:
            count += 1
    return count


# -----------------------------
# Timing helpers
# -----------------------------
def timed(label: str, fn):
    start = time.perf_counter()
    result = fn()
    elapsed = time.perf_counter() - start
    print(f"{label:<28} {elapsed:8.3f}s")
    return result, elapsed


# -----------------------------
# Benchmarks
# -----------------------------
def benchmark_io(num_tasks: int = 50, sleep_s: float = 0.05, max_workers: int = 20):
    print("\n=== I/O-bound benchmark (simulated with sleep) ===")
    durations = [sleep_s] * num_tasks

    def run_sequential():
        return [io_bound_task(d) for d in durations]

    def run_threads():
        with ThreadPoolExecutor(max_workers=max_workers) as ex:
            return list(ex.map(io_bound_task, durations))

    async def run_async():
        tasks = [io_bound_task_async(d) for d in durations]
        return await asyncio.gather(*tasks)

    timed("I/O sequential", run_sequential)
    timed(f"I/O threads ({max_workers} workers)", run_threads)
    _, async_time = timed("I/O asyncio", lambda: asyncio.run(run_async()))

    print("Note: threads + asyncio both help for I/O; asyncio does it with one thread.\n")
    return async_time


def benchmark_cpu(num_tasks: int = 8, n: int = 60_000, max_workers: int | None = None):
    print("\n=== CPU-bound benchmark (count primes) ===")
    work = [n] * num_tasks
    if max_workers is None:
        max_workers = os.cpu_count() or 2

    def run_sequential():
        return [cpu_bound_task(x) for x in work]

    def run_threads():
        with ThreadPoolExecutor(max_workers=max_workers) as ex:
            return list(ex.map(cpu_bound_task, work))

    def run_processes():
        with ProcessPoolExecutor(max_workers=max_workers) as ex:
            return list(ex.map(cpu_bound_task, work))

    timed("CPU sequential", run_sequential)
    timed(f"CPU threads ({max_workers} workers)", run_threads)
    timed(f"CPU processes ({max_workers} workers)", run_processes)

    print(
        "Note: threads usually DON'T speed up pure-Python CPU work due to the GIL; "
        "processes often do (at the cost of overhead).\n"
    )


def main():
    print("Python concurrency demo: threads vs processes vs asyncio")
    print(f"Python PID={os.getpid()}, CPU cores={os.cpu_count()}")

    # I/O: keep tasks small & many to see concurrency benefits clearly.
    benchmark_io(num_tasks=80, sleep_s=0.05, max_workers=20)

    # CPU: make this heavier if results look too similar on your machine.
    benchmark_cpu(num_tasks=8, n=120_000, max_workers=os.cpu_count() or 2)


if __name__ == "__main__":
    main()