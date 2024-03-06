'''
queue
[10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
producer add more data
workers consume data
'''

import asyncio
from random import uniform, randrange
from termcolor import colored
from typing import List

queue: List[int] = []


def log(ms, color='black'): return print(colored(ms, color))


async def producer(async_event: asyncio.Event, num, name='producer', color='red'):
    delay = uniform(0.1, 1.6)

    for _ in range(num):
        log(f'---- start {name} ---- ', color)
        await asyncio.sleep(delay)
        async_event.clear()

        # append new data
        queue[:0] = [randrange(1, 100) for _ in range(10)]
        await asyncio.sleep(delay * 3)
        log(f'{name}: queue updated {queue}', color)

        async_event.set()
        await asyncio.sleep(delay * 3)
        log(f'---- end {name} ---- ', color)


async def worker(async_event: asyncio.Event, sema: asyncio.Semaphore, name='worker', timeout: int = 10, color='yello'):
    delay = uniform(0.5, 1.6)
    data: List[int] = []

    log(f'---- start {name} ---- ', color)
    try:
        async with asyncio.timeout(timeout) as cm:
            while True:
                log(f'{name}: waiting', color)
                await async_event.wait()

                async with sema:
                    log(f'{name}: entering sema', color)
                    if not queue:
                        log(f'{name}: queue is empty', color)
                        continue
                    for _ in range(3):
                        await asyncio.sleep(delay)
                    log(f'{name}: starting work', color)
                    r = queue.pop()
                    data.append(r)
                    log(f'{name}: finished {r}', color)
                    await asyncio.sleep(delay)
    except asyncio.TimeoutError:
        pass
    finally:
        log(f'{name}: finished total{data}', color)
        log(f'---- end {name} ---- ', color)


async def main():
    log("---------- START ----------")
    colors = 'green blue magenta cyan white'.split()
    producer_running_time = 2
    # asyncio.Semaphore is to limit the number of tasks that can access a resource or pool of resources concurrently
    sema = asyncio.Semaphore(3)
    timeout = 30

    # asyncio.Event is to notify multiple asyncio tasks that some event has happened
    async_event = asyncio.Event()

    # create_task is preferred over ensure_future
    producer_task = asyncio.create_task(
        producer(async_event, producer_running_time))
    workers_task = [asyncio.create_task(
        worker(async_event, sema,
               name=f'WORKER {i+1:02d}', color=colors[i], timeout=timeout)
    ) for i in range(len(colors))]

    # wait is for aws iterable concurrently and block until the condition specified by return_when.
    await asyncio.wait(workers_task)
    try:
        # Wait_for is for the aw awaitable to complete with a timeout.
        await asyncio.wait_for(producer_task, 1)
    except asyncio.TimeoutError:
        pass
    finally:
        log("---------- END ----------")

'''
worker 5
timeout 30s
total_work 10*2 = 20
semaphore 3
'''

if __name__ == '__main__':
    asyncio.run(main())
