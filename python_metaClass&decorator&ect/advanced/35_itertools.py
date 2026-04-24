"""
第35章: 迭代器工具
=============================

Python itertools更多工具.
- 更多itertools
- 更多工具函数
"""

import itertools
import operator
from functools import reduce


# ============== accumulate ==============

def accumulate_demo():
    """accumulate"""
    data = [1, 2, 3, 4, 5]
    result = list(itertools.accumulate(data))
    print(f"累加: {result}")
    
    result2 = list(itertools.accumulate(data, operator.mul))
    print(f"累乘: {result2}")


# ============== product ==============

def product_demo():
    """笛卡尔积"""
    result = list(itertools.product([1, 2], [3, 4]))
    print(f"笛卡尔积: {result}")


# ============== permutations ==============

def permutations_demo():
    """排列"""
    result = list(itertools.permutations([1, 2, 3], 2))
    print(f"排列: {result}")


# ============== combinations ==============

def combinations_demo():
    """组合"""
    result = list(itertools.combinations([1, 2, 3], 2))
    print(f"组合: {result}")


# ============== combinations_with_replacement ==============

def combinations_wr_demo():
    """带重复组合"""
    result = list(itertools.combinations_with_replacement([1, 2], 2))
    print(f"组合: {result}")


# ============== 测试运行 ==============

if __name__ == "__main__":
    print("=" * 50)
    print("35. 迭代器工具")
    print("=" * 50)
    
    print("\n--- 1. accumulate ---")
    accumulate_demo()
    
    print("\n--- 2. product ---")
    product_demo()
    
    print("\n--- 3. permutations ---")
    permutations_demo()
    
    print("\n--- 4. combinations ---")
    combinations_demo()
    
    print("\n--- 5. combinations_with_replacement ---")
    combinations_wr_demo()
    
    print("\n" + "=" * 50)
    print("迭代器工具学习完成!")
    print("=" * 50)