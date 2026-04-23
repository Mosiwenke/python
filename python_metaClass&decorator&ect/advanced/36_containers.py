"""
第36章: 容器与数据结构
=============================

Python容器与数据结构.
- collections
- deque
- defaultdict
- Counter
"""

import collections
import heapq
from typing import Any


# ============== deque ==============

def deque_demo():
    """deque演示"""
    d = collections.deque([1, 2, 3])
    d.append(4)
    d.appendleft(0)
    print(f"deque: {list(d)}")


# ============== defaultdict ==============

def defaultdict_demo():
    """defaultdict演示"""
    d = collections.defaultdict(list)
    d["a"].append(1)
    d["a"].append(2)
    print(f"defaultdict: {dict(d)}")


# ============== Counter ==============

def counter_demo():
    """Counter演示"""
    c = collections.Counter("hello world")
    print(f"Counter: {c}")
    print(f"最常见: {c.most_common(2)}")


# ============== OrderedDict ==============

def ordereddict_demo():
    """OrderedDict"""
    d = collections.OrderedDict()
    d["a"] = 1
    d["b"] = 2
    print(f"OrderedDict: {d}")


# ============== namedtuple ==============

def namedtuple_demo():
    """namedtuple"""
    Point = collections.namedtuple("Point", ["x", "y"])
    p = Point(1, 2)
    print(f"namedtuple: {p}")
    print(f"x: {p.x}, y: {p.y}")


# ============== heapq ==============

def heapq_demo():
    """堆"""
    heap = [3, 1, 4, 1, 5]
    heapq.heapify(heap)
    print(f"堆: {heap}")
    print(f"最小: {heapq.heappop(heap)}")


if __name__ == "__main__":
    print("=" * 50)
    print("36. 容器与数据结构")
    print("=" * 50)
    
    print("\n--- 1. deque ---")
    deque_demo()
    
    print("\n--- 2. defaultdict ---")
    defaultdict_demo()
    
    print("\n--- 3. Counter ---")
    counter_demo()
    
    print("\n--- 4. OrderedDict ---")
    ordereddict_demo()
    
    print("\n--- 5. namedtuple ---")
    namedtuple_demo()
    
    print("\n--- 6. heapq ---")
    heapq_demo()
    
    print("\n" + "=" * 50)
    print("容器学习完成!")
    print("=" * 50)