"""
第24章: Python内部实现
=============================

探索Python的内部实现机制.
- 对象模型
- 内存管理
- 垃圾回收
- GIL
"""

import sys
import gc
import ctypes
from typing import Any


# ============== 对象模型 ==============

def object_model():
    """对象模型"""
    class MyClass:
        def __init__(self, value):
            self.value = value
    
    obj = MyClass(42)
    
    print(f"type: {type(obj)}")
    print(f"id: {id(obj)}")
    print(f"__dict__: {obj.__dict__}")
    print(f"__class__: {obj.__class__}")
    
    print(f"dir: {[x for x in dir(obj) if not x.startswith('_')]}")


# ============== 内存地址 ==============

def memory_address():
    """内存地址"""
    a = [1, 2, 3]
    b = a
    
    print(f"a id: {id(a)}")
    print(f"b id: {id(b)}")
    print(f"a is b: {a is b}")
    
    c = list(a)
    print(f"c id: {id(c)}")
    print(f"a is c: {a is c}")


# ============== sys.getsizeof ==============

def getsizeof_demo():
    """getsizeof演示"""
    print(f"int: {sys.getsizeof(0)}")
    print(f"int(100): {sys.getsizeof(100)}")
    print(f"str: {sys.getsizeof('')}")
    print(f"str(hello): {sys.getsizeof('hello')}")
    print(f"list: {sys.getsizeof([])}")
    print(f"list[1,2]: {sys.getsizeof([1, 2])}")
    print(f"dict: {sys.getsizeof({})}")
    print(f"dict{{1:2}}: {sys.getsizeof({1: 2})}")


# ============== 引用计数 ==============

def reference_count():
    """引用计数"""
    a = [1, 2, 3]
    print(f"引用计数: {sys.getrefcount(a)}")
    
    b = a
    print(f"引用计数(b): {sys.getrefcount(a)}")
    
    del b
    print(f"删除b后: {sys.getrefcount(a)}")


# ============== 垃圾回收 ==============

def garbage_collection():
    """垃圾回收"""
    print(f"垃圾回收阈值: {gc.get_threshold()}")
    print(f"垃圾回收计数: {gc.get_count()}")
    
    gc.collect()
    print(f"收集后计数: {gc.get_count()}")


# ============== __del__ ==============

class WithDel:
    """带__del__"""
    def __del__(self):
        print("对象被删除!")


def del_demo():
    """__del__演示"""
    obj = WithDel()
    del obj


# ============== 弱引用 ==============

import weakref


def weakref_demo():
    """弱引用演示"""
    class Target:
        pass
    
    obj = Target()
    ref = weakref.ref(obj)
    
    print(f"引用对象: {ref()}")
    del obj
    print(f"删除后: {ref()}")


# ============== slots内存 ==============

class WithoutSlots:
    """无slots"""
    def __init__(self, x, y):
        self.x = x
        self.y = y


class WithSlots:
    """有slots"""
    __slots__ = ['x', 'y']
    
    def __init__(self, x, y):
        self.x = x
        self.y = y


def slots_memory():
    """slots内存"""
    obj1 = WithoutSlots(1, 2)
    obj2 = WithSlots(1, 2)
    
    print(f"WithoutSlots: {sys.getsizeof(obj1)} + dict")
    print(f"WithSlots: {sys.getsizeof(obj2)}")
    
    print(f"obj1 has __dict__: {hasattr(obj1, '__dict__')}")
    print(f"obj2 has __dict__: {hasattr(obj2, '__dict__')}")


# ============== GIL ==============

def gil_demo():
    """GIL演示"""
    print(f"GIL存在: {True}")


# ============== 内省 ==============

def introspection():
    """内省"""
    class MyClass:
        pass
    
    obj = MyClass()
    
    print(f"isinstance: {isinstance(obj, MyClass)}")
    print(f"issubclass: {issubclass(MyClass, object)}")
    print(f"hasattr: {hasattr(obj, '__class__')}")
    print(f"getattr: {getattr(obj, '__class__')}")


# ============== 测试运行 ==============

if __name__ == "__main__":
    print("=" * 50)
    print("24. Python内部实现")
    print("=" * 50)
    
    print("\n--- 1. 对象模型 ---")
    object_model()
    
    print("\n--- 2. 内存地址 ---")
    memory_address()
    
    print("\n--- 3. getsizeof ---")
    getsizeof_demo()
    
    print("\n--- 4. 引用计数 ---")
    reference_count()
    
    print("\n--- 5. 垃圾回收 ---")
    garbage_collection()
    
    print("\n--- 6. __del__ ---")
    del_demo()
    
    print("\n--- 7. 弱引用 ---")
    weakref_demo()
    
    print("\n--- 8. slots内存 ---")
    slots_memory()
    
    print("\n--- 9. GIL ---")
    gil_demo()
    
    print("\n--- 10. 内省 ---")
    introspection()
    
    print("\n" + "=" * 50)
    print("Python内部实现学习完成!")
    print("=" * 50)