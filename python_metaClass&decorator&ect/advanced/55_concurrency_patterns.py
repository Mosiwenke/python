"""
第55章: 并发模式与实践
=============================

并发模式与最佳实践.
- 生产者-消费者
- 读者-写者
- 主从模式
"""

import threading
import queue


def producer_consumer():
    """生产者-消费者"""
    q = queue.Queue()
    stop = threading.Event()
    
    def producer():
        for i in range(3):
            q.put(i)
        stop.set()
    
    def consumer():
        while not stop.is_set() or not q.empty():
            if not q.empty():
                item = q.get()
                print(f"consumed: {item}")
    
    t1 = threading.Thread(target=producer)
    t2 = threading.Thread(target=consumer)
    t1.start(); t2.start()
    t1.join(); t2.join()


def reader_writer():
    """读者-写者"""
    data = {"value": 0}
    lock = threading.Lock()
    readers = 0
    read_lock = threading.Lock()
    
    def reader():
        nonlocal readers
        with read_lock:
            readers += 1
            if readers == 1:
                lock.acquire()
        print(f"read: {data['value']}")
        with read_lock:
            readers -= 1
            if readers == 0:
                lock.release()
    
    def writer():
        with lock:
            data["value"] += 1
            print(f"wrote: {data['value']}")
    
    threads = [
        threading.Thread(target=reader),
        threading.Thread(target=writer),
        threading.Thread(target=reader)
    ]
    for t in threads: t.start()
    for t in threads: t.join()


def thread_pool_pattern():
    """线程池模式"""
    from concurrent.futures import ThreadPoolExecutor
    
    with ThreadPoolExecutor(max_workers=2) as executor:
        results = list(executor.map(lambda x: x*2, range(3)))
        print(f"results: {results}")


def pipeline_pattern():
    """流水线模式"""
    def stage1(x): return x * 2
    def stage2(x): return x + 1
    def stage3(x): print(f"result: {x}")
    
    pipeline = stage1 | stage2 | stage3
    pipeline(5)


if __name__ == "__main__":
    print("=" * 50)
    print("55. 并发模式")
    print("=" * 50)
    print("--- producer-consumer ---")
    producer_consumer()
    print("--- reader-writer ---")
    reader_writer()
    print("--- thread-pool ---")
    thread_pool_pattern()
    print("--- pipeline ---")
    pipeline_pattern()
    print("=" * 50)