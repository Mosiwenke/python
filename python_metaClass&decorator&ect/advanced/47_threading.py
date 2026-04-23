"""
第47章: 多线程与同步原语
=============================

多线程与同步原语.
- threading
- Lock
- RLock
- Semaphore
- Event
"""

import threading
import time


def thread_creation():
    """线程创建"""
    def worker():
        print("Worker")
    
    t = threading.Thread(target=worker)
    t.start()
    t.join()


def lock_demo():
    """锁演示"""
    lock = threading.Lock()
    
    with lock:
        print("Acquired lock")
    
    print("Released lock")


def rlock_demo():
    """可重入锁"""
    lock = threading.RLock()
    
    with lock:
        print("First acquire")
        with lock:
            print("Second acquire")


def semaphore_demo():
    """信号量"""
    sem = threading.Semaphore(2)
    
    with sem:
        print("Acquired 1")
    print("Released 1")


def event_demo():
    """事件"""
    event = threading.Event()
    
    def setter():
        time.sleep(0.1)
        event.set()
    
    t = threading.Thread(target=setter)
    t.start()
    event.wait()
    print("Event received")


def threading_local():
    """线程局部存储"""
    data = threading.local()
    data.value = "thread-local"
    print(f"value: {data.value}")


if __name__ == "__main__":
    print("=" * 50)
    print("47. 多线程同步")
    print("=" * 50)
    print("--- thread ---")
    thread_creation()
    print("--- lock ---")
    lock_demo()
    print("--- rlock ---")
    rlock_demo()
    print("--- semaphore ---")
    semaphore_demo()
    print("--- event ---")
    event_demo()
    print("--- local ---")
    threading_local()
    print("=" * 50)