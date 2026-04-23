"""
第39章: 常用算法与数据结构
=============================

Python常用算法与数据结构.
- 排序
- 搜索
- 栈/队列
"""

from typing import List, Optional


# ============== 排序 ==============

def sorting():
    """排序"""
    data = [3, 1, 4, 1, 5]
    sorted_data = sorted(data, reverse=True)
    print(f"排序: {sorted_data}")
    
    data.sort()
    print(f"原地: {data}")


# ============== 二分搜索 ==============

import bisect


def binary_search():
    """二分搜索"""
    data = [1, 2, 3, 4, 5]
    index = bisect.bisect_left(data, 3)
    print(f"位置: {index}")


# ============== 队列 ==============

from collections import deque


def queue_ops():
    """队列"""
    q = deque([1, 2, 3])
    q.append(4)
    q.popleft()
    print(f"队列: {list(q)}")


# ============== 栈 ==============

def stack_ops():
    """栈"""
    stack = [1, 2, 3]
    stack.append(4)
    stack.pop()
    print(f"栈: {stack}")


# ============== 测试运行 ==============

if __name__ == "__main__":
    print("=" * 50)
    print("39. 常用算法与数据结构")
    print("=" * 50)
    sorting()
    binary_search()
    queue_ops()
    stack_ops()
    print("=" * 50)