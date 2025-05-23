import asyncio

async def task_with_timeout(task_id: int, timeout: float):
    """
    Launches a task with a timeout and handles cancellations gracefully.
    """
    try:
        print(f"Task {task_id} started.")
        result = await asyncio.wait_for(simulated_task(task_id), timeout)
        print(f"Task {task_id} completed with result: {result}")
        return result
    except asyncio.TimeoutError:
        print(f"Task {task_id} timed out.")
        return None

async def simulated_task(task_id: int):
    """
    Simulates a task with a random delay.
    """
    delay = task_id * 0.5  
    await asyncio.sleep(delay)
    return f"Result from task {task_id}"

class RateLimiter:
    """
    A rate limiter to control the number of tasks executed per second.
    """
    def __init__(self, rate: int):
        self.semaphore = asyncio.Semaphore(rate)
        self.rate = rate

    async def __aenter__(self):
        await self.semaphore.acquire()
        await asyncio.sleep(1 / self.rate)

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        self.semaphore.release()

async def limited_task(task_id: int, rate_limiter: RateLimiter, timeout: float):
    async with rate_limiter:
        return await task_with_timeout(task_id, timeout)

async def launch_tasks_with_timeout():
    """
    Launches multiple tasks with timeouts and handles their results.
    """
    rate_limiter = RateLimiter(rate=2)  
    tasks = [
        limited_task(task_id=i, rate_limiter=rate_limiter, timeout=2.0)
        for i in range(1, 6)
    ]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    print("All tasks completed.")
    return results

if __name__ == "__main__":
    asyncio.run(launch_tasks_with_timeout())
