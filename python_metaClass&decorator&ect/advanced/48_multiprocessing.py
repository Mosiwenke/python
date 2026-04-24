"""
第48章: 多进程编程
=============================

多进程编程.
- multiprocessing
- Process
- Pool
- Queue
"""

import multiprocessing
import time


def process_basic():
    """基本进程"""
    def worker(n):
        print(f"Process {n}")
    
    p = multiprocessing.Process(target=worker, args=(1,))
    p.start()
    p.join()


def pool_demo():
    """进程池"""
    with multiprocessing.Pool(2) as pool:
        results = pool.map(lambda x: x*2, [1, 2, 3])
        print(f"results: {results}")


def queue_demo():
    """队列"""
    q = multiprocessing.Queue()
    q.put(1)
    q.put(2)
    print(f"get: {q.get()}")
    print(f"get: {q.get()}")


def pipe_demo():
    """管道"""
    parent, child = multiprocessing.Pipe()
    parent.send("message")
    print(f"receive: {child.recv()}")


def manager_demo():
    """共享内存"""
    mgr = multiprocessing.Manager()
    shared = mgr.dict()
    shared["key"] = "value"
    print(f"dict: {dict(shared)}")


def value_demo():
    """共享值"""
    val = multiprocessing.Value('i', 0)
    val.value += 1
    print(f"value: {val.value}")


if __name__ == "__main__":
    print("=" * 50)
    print("48. 多进程编程")
    print("=" * 50)
    print("--- basic ---")
    process_basic()
    print("--- pool ---")
    pool_demo()
    print("--- queue ---")
    queue_demo()
    print("--- pipe ---")
    pipe_demo()
    print("--- manager ---")
    manager_demo()
    print("--- value ---")
    value_demo()
    print("=" * 50)