"""
第18章: 并发编程
=============================

Python并发编程核心知识.
- threading多线程
- multiprocessing多进程
- concurrent.futures
- 线程同步
"""

import threading
import multiprocessing
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed
import time
import queue
import itertools
from typing import List, Callable, Any


# ============== 基础线程 ==============

def worker(name: str, duration: int):
    """工作线程"""
    print(f"[{name}] 开始")
    time.sleep(duration)
    print(f"[{name}] 完成")
    return f"{name} done"


def basic_threading():
    """基础线程演示"""
    threads = []
    
    for name, duration in [("A", 0.5), ("B", 0.3), ("C", 0.7)]:
        t = threading.Thread(target=worker, args=(name, duration))
        threads.append(t)
        t.start()
    
    for t in threads:
        t.join()
    
    print("所有线程完成")


# ============== 线程池 ==============

def thread_pool_demo():
    """线程池演示"""
    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = [
            executor.submit(worker, f"Task-{i}", 0.3)
            for i in range(5)
        ]
        
        for future in as_completed(futures):
            print(f"结果: {future.result()}")


# ============== 进程池 ==============

def process_worker(n: int) -> int:
    """进程工作函数"""
    time.sleep(0.5)
    return n * 2


def process_pool_demo():
    """进程池演示"""
    with ProcessPoolExecutor(max_workers=3) as executor:
        results = list(executor.map(process_worker, range(5)))
        print(f"结果: {results}")


# ============== 线程同步 ==============

class Counter:
    """线程计数器"""
    
    def __init__(self):
        self.count = 0
        self.lock = threading.Lock()
    
    def increment(self):
        with self.lock:
            self.count += 1
            return self.count


def sync_demo():
    """线程同步演示"""
    counter = Counter()
    
    def inc():
        for _ in range(1000):
            counter.increment()
    
    threads = [threading.Thread(target=inc) for _ in range(10)]
    
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    
    print(f"最终计数: {counter.count}")


# ============== 信号量 ==============

class Pool:
    """连接池"""
    
    def __init__(self, size: int):
        self.size = size
        self.semaphore = threading.Semaphore(size)
        self.connections = queue.Queue(size)
        
        for i in range(size):
            self.connections.put(f"conn-{i}")
    
    def acquire(self):
        self.semaphore.acquire()
        conn = self.connections.get()
        return conn
    
    def release(self, conn):
        self.connections.put(conn)
        self.semaphore.release()


def semaphore_demo():
    """信号量演示"""
    pool = Pool(2)
    
    def use_connection(name):
        conn = pool.acquire()
        print(f"[{name}] 使用 {conn}")
        time.sleep(0.3)
        pool.release(conn)
        print(f"[{name}] 释放 {conn}")
    
    threads = [threading.Thread(target=use_connection, args=(i,)) for i in range(5)]
    
    for t in threads:
        t.start()
    for t in threads:
        t.join()


# ============== 条件变量 ==============

class ProducerConsumer:
    """生产者消费者"""
    
    def __init__(self, capacity: int = 2):
        self.queue = queue.Queue(capacity)
        self.lock = threading.Lock()
        self.not_full = threading.Condition(self.lock)
        self.not_empty = threading.Condition(self.lock)
    
    def produce(self, item):
        with self.not_full:
            while self.queue.full():
                self.not_full.wait()
            
            self.queue.put(item)
            print(f"生产: {item}")
            self.not_empty.notify()
    
    def consume(self):
        with self.not_empty:
            while self.queue.empty():
                self.not_empty.wait()
            
            item = self.queue.get()
            print(f"消费: {item}")
            self.not_full.notify()
            return item


def producer_consumer_demo():
    """生产者消费者演示"""
    pc = ProducerConsumer(2)
    
    def producer():
        for i in range(5):
            pc.produce(i)
            time.sleep(0.2)
    
    def consumer():
        for _ in range(5):
            pc.consume()
            time.sleep(0.3)
    
    threading.Thread(target=producer).start()
    threading.Thread(target=consumer).start()
    time.sleep(2)


# ============== 屏障 ==============

class BarrierDemo:
    """屏障演示"""
    
    def __init__(self, count: int):
        self.barrier = threading.Barrier(count)
    
    def worker(self, name):
        print(f"[{name}] 等待中...")
        self.barrier.wait()
        print(f"[{name}] 开始工作")


def barrier_demo():
    """屏障演示"""
    demo = BarrierDemo(3)
    
    threads = [threading.Thread(target=demo.worker, args=(i,)) for i in range(3)]
    
    for t in threads:
        t.start()
    for t in threads:
        t.join()


# ============== 线程局部变量 ==============

thread_local = threading.local()


def thread_local_worker(name):
    """线程局部变量"""
    thread_local.value = name
    
    def get_value():
        return thread_local.value
    
    time.sleep(0.1)
    print(f"[{name}] 值: {get_value()}")


def thread_local_demo():
    """线程局部变量演示"""
    threads = [threading.Thread(target=thread_local_worker, args=(i,)) for i in range(3)]
    
    for t in threads:
        t.start()
    for t in threads:
        t.join()


# ============== 定时器 ==============

def timer_demo():
    """定时器演示"""
    def callback():
        print("定时任务执行!")
    
    timer = threading.Timer(0.5, callback)
    timer.start()
    print("定时器已启动")
    timer.join()


# ============== 队列 ==============

def queue_demo():
    """队列演示"""
    q = queue.Queue()
    
    def put():
        for i in range(5):
            q.put(i)
            time.sleep(0.1)
    
    def get():
        items = []
        while True:
            try:
                item = q.get(timeout=0.5)
                items.append(item)
                q.task_done()
            except queue.Empty:
                break
        print(f"获取: {items}")
    
    threading.Thread(target=put).start()
    threading.Thread(target=get).start()
    time.sleep(1)


# ============== GIL说明 ==============

def gil_demo():
    """GIL演示 - IO密集型 vs CPU密集型"""
    
    def io_bound(n):
        time.sleep(0.1)
        return n
    
    def cpu_bound(n):
        total = 0
        for i in range(n * 100000):
            total += i
        return total
    
    start = time.perf_counter()
    with ThreadPoolExecutor(max_workers=4) as executor:
        list(executor.map(io_bound, range(10)))
    print(f"IO密集型: {time.perf_counter() - start:.3f}s")
    
    start = time.perf_counter()
    with ProcessPoolExecutor(max_workers=4) as executor:
        list(executor.map(cpu_bound, range(10)))
    print(f"CPU密集型: {time.perf_counter() - start:.3f}s")


# ============== 测试运行 ==============

if __name__ == "__main__":
    print("=" * 50)
    print("18. 并发编程")
    print("=" * 50)
    
    # 测试1: 基础线程
    print("\n--- 1. 基础线程 ---")
    basic_threading()
    
    # 测试2: 线程池
    print("\n--- 2. 线程池 ---")
    thread_pool_demo()
    
    # 测试3: 进程池
    print("\n--- 3. 进程池 ---")
    process_pool_demo()
    
    # 测试4: 同步
    print("\n--- 4. 线程同步 ---")
    sync_demo()
    
    # 测试5: 信号量
    print("\n--- 5. 信号量 ---")
    semaphore_demo()
    
    # 测试6: 生产者消费者
    print("\n--- 6. 生产者消费者 ---")
    producer_consumer_demo()
    
    # 测试7: 屏障
    print("\n--- 7. 屏障 ---")
    barrier_demo()
    
    # 测试8: 定时器
    print("\n--- 8. 定时器 ---")
    timer_demo()
    time.sleep(1)
    
    # 测试9: 队列
    print("\n--- 9. 队列 ---")
    queue_demo()
    
    # 测试10: GIL
    print("\n--- 10. GIL ---")
    gil_demo()
    
    print("\n" + "=" * 50)
    print("并发编程学习完成!")
    print("=" * 50)