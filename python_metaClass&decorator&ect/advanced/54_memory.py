"""
第54章: 内存管理与垃圾回收
=============================

内存管理与垃圾回收.
- gc模块
- 弱引用
- 内存分析
- slot优化
"""

import gc
import sys
import weakref


def gc_demo():
    """gc"""
    print(f"gc threshold: {gc.get_threshold()}")
    print(f"gc count: {gc.get_count()}")


def manual_gc():
    """手动回收"""
    gc.collect()
    print("collected")


class Expensive:
    def __del__(self): print("deleted")


def weakref_demo():
    """弱引用"""
    obj = Expensive()
    ref = weakref.ref(obj)
    print(f"ref: {ref()}")
    del obj
    print(f"after del: {ref()}")


def getsizeof_demo():
    """sizeof"""
    print(f"int: {sys.getsizeof(0)}")
    print(f"list: {sys.getsizeof([])}")
    print(f"dict: {sys.getsizeof({})}")


class WithSlots:
    __slots__ = ['x', 'y']
    
    def __init__(self, x, y):
        self.x = x
        self.y = y


class WithoutSlots:
    def __init__(self, x, y):
        self.x = x
        self.y = y


def slots_compare():
    """slots对比"""
    s = WithSlots(1, 2)
    w = WithoutSlots(1, 2)
    print(f"with slots size: {sys.getsizeof(s)}")
    print(f"without slots size: {sys.getsizeof(w)} + dict")


def object_flags():
    """对象标志"""
    class Test: pass
    
    t = Test()
    print(f"flags: {sys.getflags(t) if hasattr(sys, 'getflags') else 'N/A'}")


if __name__ == "__main__":
    print("=" * 50)
    print("54. 内存管理")
    print("=" * 50)
    gc_demo()
    weakref_demo()
    getsizeof_demo()
    slots_compare()
    print()
    object_flags()
    print("=" * 50)