import asyncio


def fetch(url):
    """Make the request and get the results"""
    pass


def worker(name, queue, results):
    """A function to take unmake requests from a queue and perform the work then add resutls to the resutls list"""
    pass


def distribute_work(url, requests, concurrency, results):
    """Divide up the work int obatches and collect the final results"""
    pass


def assault(url, requests, concurrency):
    """Entrypoint to make requests"""
    pass
