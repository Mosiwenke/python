"""
第14章: 协程与asyncio异步编程
================================

Python异步编程核心知识.
- 协程基础
- asyncio事件循环
- async/await语法
- 异步迭代器与生成器
"""

import asyncio
import sys
import time
from typing import Coroutine, AsyncIterator


# ============== 协程基础 ==============

async def simple_coroutine():
    """最简单的协程"""
    await asyncio.sleep(0.1)
    return "完成"


def run_coroutine():
    """运行协程"""
    result = asyncio.run(simple_coroutine())
    print(f"协程结果: {result}")


# ============== async/await ==============

async def fetch_data():
    """模拟获取数据"""
    print("开始获取数据...")
    await asyncio.sleep(1)
    print("数据获取完成")
    return {"data": [1, 2, 3]}


async def process_data():
    """处理数据"""
    print("开始处理...")
    data = await fetch_data()
    await asyncio.sleep(0.5)
    print(f"处理完成: {data}")
    return data


# ============== 并发执行 ==============

async def task_a():
    """任务A"""
    await asyncio.sleep(0.5)
    return "A完成"


async def task_b():
    """任务B"""
    await asyncio.sleep(0.3)
    return "B完成"


async def task_c():
    """任务C"""
    await asyncio.sleep(0.7)
    return "C完成"


async def concurrent_tasks():
    """并发执行多个任务"""
    start = time.perf_counter()
    
    results = await asyncio.gather(task_a(), task_b(), task_c())
    
    elapsed = time.perf_counter() - start
    print(f"并发执行: {results}, 耗时: {elapsed:.2f}秒")


async def concurrent_with_exceptions():
    """捕获异常"""
    async def risky_task():
        await asyncio.sleep(0.1)
        raise ValueError("出错了!")
    
    async def safe_task():
        await asyncio.sleep(0.2)
        return "安全"
    
    try:
        await asyncio.gather(safe_task(), risky_task(), return_exceptions=True)
    except ValueError as e:
        print(f"捕获异常: {e}")


# ============== 异步生成器 ==============

async def async_range(start: int, stop: int):
    """异步生成器"""
    for i in range(start, stop):
        await asyncio.sleep(0.1)
        yield i


async def async_generator_demo():
    """异步生成器演示"""
    async for value in async_range(3, 7):
        print(f"值: {value}")


# ============== 异步迭代器 ==============

class AsyncCounter:
    """异步迭代器"""
    
    def __init__(self, max_count: int):
        self.max_count = max_count
        self.current = 0
    
    def __aiter__(self):
        return self
    
    async def __anext__(self):
        if self.current >= self.max_count:
            raise StopAsyncIteration
        await asyncio.sleep(0.1)
        self.current += 1
        return self.current


async def async_iterator_demo():
    """异步迭代器演示"""
    async for count in AsyncCounter(5):
        print(f"计数: {count}")


# ============== 异步上下文管理器 ==============

class AsyncTimer:
    """异步上下文管理器"""
    
    def __init__(self, name: str):
        self.name = name
    
    async def __aenter__(self):
        self.start = time.perf_counter()
        print(f"[{self.name}] 开始")
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        elapsed = time.perf_counter() - self.start
        print(f"[{self.name}] 结束, 耗时: {elapsed:.2f}秒")


async def async_context_manager_demo():
    """异步上下文管理器演示"""
    async with AsyncTimer("任务"):
        await asyncio.sleep(0.3)


# ============== 异步信号量 ==============

async def limited_task(task_id: int, semaphore: asyncio.Semaphore):
    """限制并发数的任务"""
    async with semaphore:
        print(f"任务 {task_id} 开始")
        await asyncio.sleep(0.5)
        print(f"任务 {task_id} 结束")
        return task_id


async def semaphore_demo():
    """信号量演示"""
    semaphore = asyncio.Semaphore(2)
    
    tasks = [limited_task(i, semaphore) for i in range(5)]
    results = await asyncio.gather(*tasks)
    print(f"结果: {results}")


# ============== 异步锁 ==============

class AsyncCounterWithLock:
    """线程安全的异步计数器"""
    
    def __init__(self):
        self.count = 0
        self.lock = asyncio.Lock()
    
    async def increment(self):
        async with self.lock:
            self.count += 1
            return self.count


async def lock_demo():
    """异步锁演示"""
    counter = AsyncCounterWithLock()
    
    async def inc():
        for _ in range(10):
            await counter.increment()
    
    await asyncio.gather(inc(), inc())
    print(f"最终计数: {counter.count}")


# ============== 异步队列 ==============

async def producer(queue: asyncio.Queue):
    """生产者"""
    for i in range(5):
        await asyncio.sleep(0.1)
        await queue.put(i)
        print(f"生产: {i}")
    await queue.put(None)


async def consumer(queue: asyncio.Queue):
    """消费者"""
    while True:
        item = await queue.get()
        if item is None:
            break
        print(f"消费: {item}")
        await asyncio.sleep(0.2)


async def queue_demo():
    """异步队列演示"""
    queue = asyncio.Queue()
    await asyncio.gather(producer(queue), consumer(queue))


# ============== Task管理 ==============

async def task_demo():
    """Task管理演示"""
    task = asyncio.create_task(task_a())
    
    task_b_result = await task_b()
    print(f"task_b: {task_b_result}")
    
    task_result = await task
    print(f"task_a: {task_result}")
    
    print("主任务完成")


# ============== 取消任务 ==============

async def cancellable_task():
    """可取消的任务"""
    try:
        for i in range(10):
            print(f"计数: {i}")
            await asyncio.sleep(0.2)
    except asyncio.CancelledError:
        print("任务被取消")
        raise


async def cancel_demo():
    """取消演示"""
    task = asyncio.create_task(cancellable_task())
    
    await asyncio.sleep(0.5)
    task.cancel()
    
    try:
        await task
    except asyncio.CancelledError:
        print("已取消")


# ============== 事件循环 ==============

def custom_event_loop():
    """自定义事件循环"""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    try:
        result = loop.run_until_complete(task_a())
        print(f"结果: {result}")
    finally:
        loop.close()


# ============== 测试运行 ==============

if __name__ == "__main__":
    print("=" * 50)
    print("14. 协程与asyncio异步编程")
    print("=" * 50)
    
    # 测试1: 基础协程
    print("\n--- 1. 基础协程 ---")
    run_coroutine()
    
    # 测试2: async/await
    print("\n--- 2. async/await ---")
    asyncio.run(process_data())
    
    # 测试3: 并发执行
    print("\n--- 3. 并发执行 ---")
    asyncio.run(concurrent_tasks())
    
    # 测试4: 异步生成器
    print("\n--- 4. 异步生成器 ---")
    asyncio.run(async_generator_demo())
    
    # 测试5: 异步迭代器
    print("\n--- 5. 异步迭代器 ---")
    asyncio.run(async_iterator_demo())
    
    # 测试6: 异步上下文管理器
    print("\n--- 6. 异步上下文管理器 ---")
    asyncio.run(async_context_manager_demo())
    
    # 测试7: 信号量
    print("\n--- 7. 异步信号量 ---")
    asyncio.run(semaphore_demo())
    
    # 测试8: 异步锁
    print("\n--- 8. 异步锁 ---")
    asyncio.run(lock_demo())
    
    # 测试9: 队列
    print("\n--- 9. 异步队列 ---")
    asyncio.run(queue_demo())
    
    # 测试10: Task
    print("\n--- 10. Task管理 ---")
    asyncio.run(task_demo())
    
    # 测试11: 取消
    print("\n--- 11. 取消任务 ---")
    asyncio.run(cancel_demo())
    
    print("\n" + "=" * 50)
    print("异步编程学习完成!")
    print("=" * 50)