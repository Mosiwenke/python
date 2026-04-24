"""
第51章: 函数式编程进阶
=============================

函数式编程进阶.
- functools
- operator
- partial
- singledispatch
"""

from functools import *
from operator import *


def reduce_demo():
    """reduce"""
    result = reduce(lambda a, b: a + b, [1, 2, 3, 4, 5])
    print(f"reduce sum: {result}")


def partial_demo():
    """partial"""
    def power(base, exp): return base ** exp
    
    square = partial(power, exp=2)
    print(f"square(5): {square(5)}")


def lru_cache_demo():
    """LRU缓存"""
    @lru_cache(maxsize=128)
    def fib(n):
        if n < 2: return n
        return fib(n-1) + fib(n-2)
    
    print(f"fib(20): {fib(20)}")
    print(f"cache: {fib.cache_info()}")


def singledispatch_demo():
    """单分发"""
    @singledispatch
    def process(x): return f"obj: {x}"
    
    @process.register(int)
    def process_int(x): return f"int: {x*2}"
    
    @process.register(str)
    def process_str(x): return f"str: {x.upper()}"
    
    print(process(1))
    print(process("hi"))
    print(process([1,2]))


def wraps_demo():
    """wraps"""
    def outer(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        return wrapper
    
    @outer
    def hello():
        """hello doc"""
        return "hello"
    
    print(f"name: {hello.__name__}")
    print(f"doc: {hello.__doc__}")


def cmp_to_key_demo():
    """cmp_to_key"""
    from functools import cmp_to_key
    
    def compare(a, b):
        return (a > b) - (a < b)
    
    sorted([3, 1, 2], key=cmp_to_key(compare))
    print("sorted")


if __name__ == "__main__":
    print("=" * 50)
    print("51. 函数式编程进阶")
    print("=" * 50)
    reduce_demo()
    partial_demo()
    lru_cache_demo()
    singledispatch_demo()
    wraps_demo()
    cmp_to_key_demo()
    print("=" * 50)