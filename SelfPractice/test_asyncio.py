import asyncio
import time


async def say(cnt, what):
    for i in range(cnt):
        print(what + ' ' + str(i))
        await asyncio.sleep(1)


async def main(name):
    task1 = asyncio.create_task(say(1, f'hello {name}'))
    task2 = asyncio.create_task(say(2, f'world {name}'))
    print(f"started at {time.strftime('%X')}")
    await task1
    await task2
    print(f"finished at {time.strftime('%X')}")


if __name__ == "__main__":
    semaphore = asyncio.Semaphore(2)
    print('------------------')
    asyncio.create_task(main('gom')).run(semaphore, *args)
    print('------------------')
    asyncio.create_task(main('kom')).run(semaphore, *args)
