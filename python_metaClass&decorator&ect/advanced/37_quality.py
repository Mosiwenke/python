"""
第37章: 代码质量工具
=============================

Python代码质量工具.
- typing.IO
- contextlib.abstractcontextmanager
- 装饰器工厂
"""

from typing import IO
from contextlib import contextmanager, abstractcontextmanager
from functools import wraps


# ============== IO类型 ==============

def io_type_demo():
    """IO类型"""
    def read_file(f: IO[str]) -> str:
        return f.read()
    
    print(f"IO[str] 参数")


# ============== abstractcontextmanager ==============

@abstractcontextmanager
class AbstractContext:
    """抽象上下文管理器"""
    def __enter__(self):
        return self
    
    def __exit__(self, *args):
        pass


def abstract_context_demo():
    """抽象上下文"""
    print("abstractcontextmanager")


# ============== 装饰器工厂模式 ==============

def decorator_factory():
    """装饰器工厂"""
    def make_decorator(prefix: str):
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                print(f"{prefix}: {func.__name__}")
                return func(*args, **kwargs)
            return wrapper
        return decorator
    
    @make_decorator("INFO")
    def hello():
        return "hello"
    
    print(hello())


# ============== 闭包工厂 ==============

def closure_factory():
    """闭包工厂"""
    def make_multiplier(n):
        def multiplier(x):
            return x * n
        return multiplier
    
    double = make_multiplier(2)
    triple = make_multiplier(3)
    
    print(f"double(5): {double(5)}")
    print(f"triple(5): {triple(5)}")


# ============== lru_cache高级 ==============

from functools import lru_cache


def lru_cache_advanced():
    """lru_cache高级"""
    @lru_cache(maxsize=128)
    def fib(n):
        if n < 2:
            return n
        return fib(n-1) + fib(n-2)
    
    info = fib.cache_info()
    print(f"缓存: {info}")


if __name__ == "__main__":
    print("=" * 50)
    print("37. 代码质量工具")
    print("=" * 50)
    
    print("\n--- 1. IO类型 ---")
    io_type_demo()
    
    print("\n--- 2. abstractcontextmanager ---")
    abstract_context_demo()
    
    print("\n--- 3. 装饰器工厂 ---")
    decorator_factory()
    
    print("\n--- 4. 闭包工厂 ---")
    closure_factory()
    
    print("\n--- 5. lru_cache ---")
    lru_cache_advanced()
    
    print("\n" + "=" * 50)
    print("代码质量工具学习完成!")
    print("=" * 50)