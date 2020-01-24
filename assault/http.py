import asyncio
import os
import time
import requests


def fetch(url):
    """Make the request and get the results"""
    started_at = time.monotonic()
    response = requests.get(url)
    request_time = time.monotonic() - started_at
    return {"status_code": response.status_code, "request_time": request_time}


async def worker(name, queue, results):
    """A function to take unmake requests from a queue and perform the work then add results to the resutls list"""
    loop = asyncio.get_event_loop()
    while True:
        url = await queue.get()
        if os.getenv("DEBUG"):
            print(f"{name} - Fetching {url}")
        future_result = loop.run_in_executor(None, fetch, url)
        result = await future_result
        results.append(result)
        queue.task_done()


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

