"""
第25章: 性能优化
=============================

Python性能优化技术.
- 算法优化
- 缓存
- 生成器
- 内联
"""

import time
import functools
from typing import List, Callable


# ============== 时间测量 ==============

def time_measurement():
    """时间测量"""
    start = time.perf_counter()
    result = sum(range(1000000))
    elapsed = time.perf_counter() - start
    print(f"耗时: {elapsed:.4f}s")


# ============== 算法优化 ==============

def algorithm_optimization():
    """算法优化"""
    n = 100
    
    start = time.perf_counter()
    result = 0
    for i in range(n):
        result += i
    elapsed1 = time.perf_counter() - start
    
    start = time.perf_counter()
    result = n * (n - 1) // 2
    elapsed2 = time.perf_counter() - start
    
    print(f"循环: {elapsed1:.6f}s")
    print(f"公式: {elapsed2:.6f}s")


# ============== 局部变量 ==============

def local_variables():
    """局部变量"""
    n = 100000
    
    def with_global():
        result = 0
        for i in range(n):
            result += i
        return result
    
    def with_local():
        result = 0
        n_local = n
        for i in range(n_local):
            result += i
        return result
    
    start = time.perf_counter()
    with_global()
    t1 = time.perf_counter() - start
    
    start = time.perf_counter()
    with_local()
    t2 = time.perf_counter() - start
    
    print(f"全局: {t1:.6f}s")
    print(f"局部: {t2:.6f}s")


# ============== list comprehension ==============

def list_comprehension():
    """列表推导"""
    n = 10000
    
    start = time.perf_counter()
    result = []
    for i in range(n):
        result.append(i * 2)
    t1 = time.perf_counter() - start
    
    start = time.perf_counter()
    result = [i * 2 for i in range(n)]
    t2 = time.perf_counter() - start
    
    print(f"循环: {t1:.6f}s")
    print(f"推导: {t2:.6f}s")


# ============== set查找 ==============

def set_lookup():
    """set查找"""
    n = 10000
    data = list(range(n))
    lookup_set = set(data)
    lookup_list = data
    
    target = n - 1
    
    start = time.perf_counter()
    while target in lookup_list:
        break
    t1 = time.perf_counter() - start
    
    start = time.perf_counter()
    while target in lookup_set:
        break
    t2 = time.perf_counter() - start
    
    print(f"list: {t1:.6f}s")
    print(f"set: {t2:.6f}s")


# ============== join ==============

def join_optimization():
    """join优化"""
    strings = ["a"] * 10000
    
    start = time.perf_counter()
    result = ""
    for s in strings:
        result += s
    t1 = time.perf_counter() - start
    
    start = time.perf_counter()
    result = "".join(strings)
    t2 = time.perf_counter() - start
    
    print(f"+: {t1:.6f}s")
    print(f"join: {t2:.6f}s")


# ============== lru_cache ==============

@lru_cache(maxsize=None)
def fib_cached(n):
    """斐波那契缓存"""
    if n < 2:
        return n
    return fib_cached(n - 1) + fib_cached(n - 2)


def caching():
    """缓存"""
    n = 20
    
    start = time.perf_counter()
    fib_cached(n)
    t1 = time.perf_counter() - start
    
    fib_cached.cache_clear()
    
    start = time.perf_counter()
    fib_cached(n)
    t2 = time.perf_counter() - start
    
    print(f"不缓存: {t1:.6f}s")
    print(f"缓存: {t2:.6f}s")


# ============== 生成器 ==============

def generator_optimization():
    """生成器优化"""
    n = 100000
    
    def list_version():
        return [i for i in range(n)]
    
    def generator_version():
        for i in range(n):
            yield i
    
    start = time.perf_counter()
    result = sum(list_version())
    t1 = time.perf_counter() - start
    
    start = time.perf_counter()
    result = sum(generator_version())
    t2 = time.perf_counter() - start
    
    print(f"列表: {t1:.6f}s")
    print(f"生成器: {t2:.6f}s")


# ============== __slots__ ==============

class WithDict:
    """有__dict__"""
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z


class WithSlots:
    """有__slots__"""
    __slots__ = ['x', 'y', 'z']
    
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z


def slots_optimization():
    """__slots__优化"""
    n = 100000
    
    def create_with_dict():
        return [WithDict(i, i + 1, i + 2) for i in range(n)]
    
    def create_with_slots():
        return [WithSlots(i, i + 1, i + 2) for i in range(n)]
    
    start = time.perf_counter()
    create_with_dict()
    t1 = time.perf_counter() - start
    
    start = time.perf_counter()
    create_with_slots()
    t2 = time.perf_counter() - start
    
    print(f"dict: {t1:.6f}s")
    print(f"slots: {t2:.6f}s")


# ============== 批量操作 ==============

def batch_operations():
    """批量操作"""
    data = list(range(10000))
    
    def loop():
        result = []
        for x in data:
            result.append(x * 2)
        return result
    
    def map_version():
        return list(map(lambda x: x * 2, data))
    
    start = time.perf_counter()
    loop()
    t1 = time.perf_counter() - start
    
    start = time.perf_counter()
    map_version()
    t2 = time.perf_counter() - start
    
    print(f"循环: {t1:.6f}s")
    print(f"map: {t2:.6f}s")


# ============== 测试运行 ==============

if __name__ == "__main__":
    print("=" * 50)
    print("25. 性能优化")
    print("=" * 50)
    
    print("\n--- 1. 时间测量 ---")
    time_measurement()
    
    print("\n--- 2. 算法优化 ---")
    algorithm_optimization()
    
    print("\n--- 3. 局部变量 ---")
    local_variables()
    
    print("\n--- 4. 列表推导 ---")
    list_comprehension()
    
    print("\n--- 5. set查找 ---")
    set_lookup()
    
    print("\n--- 6. join ---")
    join_optimization()
    
    print("\n--- 7. 缓存 ---")
    caching()
    
    print("\n--- 8. 生成器 ---")
    generator_optimization()
    
    print("\n--- 9. __slots__ ---")
    slots_optimization()
    
    print("\n--- 10. 批量操作 ---")
    batch_operations()
    
    print("\n" + "=" * 50)
    print("性能优化学习完成!")
    print("=" * 50)