import asyncio
import time


def fetch(url):
    """Make the request and get the results"""
    pass


async def worker(name, queue, results):
    """A function to take unmake requests from a queue and perform the work then add resutls to the resutls list"""
    while True:
        item = await queue.get()
        print(f"{name} read {item}")


async def distribute_work(url, requests, concurrency, results):
    """Divide up the work int obatches and collect the final results"""
    queue = asyncio.Queue()

    for _ in range(requests):
        queue.put_nowait(url)

    tasks = []
    for i in range(concurrency):
        task = asyncio.create_task(worker(f"worker-{i+1}", queue, results))
        tasks.append(task)

    started_at = time.monotonic()
    await queue.join()  # triggers work to be done
    total_time = time.monotonic() - started_at

    for task in tasks:
        task.cancel()  # stops the workers, as work has finished

    print("---")
    print(
        f"{concurrency} workers took {total_time:.2f} seconds to complete {len(results)} requests"
    )


def assault(url, requests, concurrency):
    """Entrypoint to make requests"""
    results = []
    asyncio.run(distribute_work(url, requests, concurrency, results))
    print(results)

