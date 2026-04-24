"""
第49章: asyncio异步编程进阶
=============================

asyncio进阶.
- 异步队列
- 异步锁
- asyncio.gather
- asyncio.create_task
"""

import asyncio


async def async_sleep():
    """异步睡眠"""
    await asyncio.sleep(0.1)
    return "done"


async def gather_demo():
    """gather"""
    results = await asyncio.gather(
        async_sleep(),
        async_sleep(),
        async_sleep()
    )
    print(f"gather: {results}")


async def create_task_demo():
    """create_task"""
    task = asyncio.create_task(async_sleep())
    result = await task
    print(f"task result: {result}")


async def async_queue():
    """异步队列"""
    q = asyncio.Queue()
    await q.put(1)
    await q.put(2)
    item = await q.get()
    print(f"queue get: {item}")


async def async_lock():
    """异步锁"""
    lock = asyncio.Lock()
    async with lock:
        print("acquired")
    print("released")


async def async_timeout():
    """超时"""
    try:
        await asyncio.wait_for(async_sleep(), timeout=0.01)
    except asyncio.TimeoutError:
        print("timeout")


async def async_comprehension():
    """异步推导"""
    async def gen():
        for i in range(3):
            yield i
    
    result = [x async for x in gen()]
    print(f"comprehension: {result}")


if __name__ == "__main__":
    print("=" * 50)
    print("49. asyncio进阶")
    print("=" * 50)
    asyncio.run(gather_demo())
    asyncio.run(create_task_demo())
    asyncio.run(async_queue())
    asyncio.run(async_lock())
    asyncio.run(async_timeout())
    asyncio.run(async_comprehension())
    print("=" * 50)