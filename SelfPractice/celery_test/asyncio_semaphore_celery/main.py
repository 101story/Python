import itertools
import asyncio
from termcolor import colored
from celery import Celery
from celery_test.asyncio_semaphore_celery.async_tasks import celeryconfig


def log(ms, color='white'): return print(colored(ms, color))


celery = Celery('tasks')
celery.config_from_object(celeryconfig)


def print_worker_inspect(name, color):
    i = celery.control.inspect()

    # Show the items that have an ETA or are scheduled for later processing
    log(f'{name} schedueled: {i.scheduled()}', color)

    # Show tasks that are currently active.
    log(f'{name} active: {i.active()}', color)

    # Show tasks that have been claimed by workers
    log(f'{name} reserved: {i.reserved()}', color)


async def worker(name, task='xsum', data=[], timeout: int = 10, color='yello'):
    log(f'---- start {name}: {task} ---- ', color)
    try:
        print_worker_inspect(name, color)
        result = celery.send_task(
            f'async_tasks.{task}', args=(data), time_limit=timeout)

        log(f'{name} {task} run: {data} = {result}', color)

        # while result.state == 'PENDING':
        #     await asyncio.sleep(1)

        # result = result.get()

        log(f'{name} {task} result: {result}', color)
        print_worker_inspect(name, color)

        return result
    except Exception as e:
        log(f'{name} {task} error: {e}', color)
    finally:
        log(f'---- end {name}: {task} ---- ', color)


async def start_tasks(name, sema, color, timeout, *args):
    try:
        async with sema:
            log(f'{name}: entering sema', color)
            workers_tasks = []
            workers_tasks.append(worker(
                name, task='xmin', data=args, color=color, timeout=timeout))
            workers_tasks.append(worker(
                name, task='xmax', data=args, color=color, timeout=timeout))
            workers_tasks.append(worker(
                name, task='xsum', data=args, color=color, timeout=timeout))
            group_result = await asyncio.gather(*workers_tasks, return_exceptions=True)
            # await worker(name, task='xsum', data=args, color=color, timeout=timeout)
            # await asyncio.gather(worker(name, task='xsum', data=args, color=color, timeout=timeout))
            log(f'{name} finished total{group_result}', color)

        print_worker_inspect(name, color)
    except Exception as e:
        log(f'{name} error: {e}', color)
    finally:
        log(f'---- end {name} ---- ', color)



async def main():
    log("----------- START --------------")
    colors = 'green blue magenta cyan white'.split()
    colors_seq = itertools.cycle(colors)
    sema = asyncio.Semaphore(2)
    timeout = 30
    calculate_data = [(1, 2), (3, 4, 5), (6, 7, 8, 9), (10, 11, 12, 13, 14)]

    for i, (color, data) in enumerate(zip(colors_seq, calculate_data)):
        try:
            # asyncio.create_task(
            #     worker(f'WORKER {i:02d}', task='xsum', data=list(data), color=color, timeout=timeout)
            # )
            # await asyncio.gather(worker(f'WORKER {i:02d}', task='xsum', data=list(data), color=color, timeout=timeout))
            await asyncio.create_task(start_tasks(
                f'WORKER {i:02d}', sema, color, timeout, list(data))
            )
            # await asyncio.gather(start_tasks(
            #     f'WORKER {i:02d}', sema, color, timeout, list(data))
            # )
        except asyncio.TimeoutError:
            pass
        finally:
            log("----------- END --------------")


if __name__ == '__main__':
    asyncio.run(main())


# $ python -m celery_test.asyncio_semaphore_celery.main