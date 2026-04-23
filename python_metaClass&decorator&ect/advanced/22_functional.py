"""
第22章: 函数式编程
=============================

Python函数式编程特性.
- map/filter/reduce
- lambda
- functools
- operator
- partial
"""

from functools import reduce, partial, lru_cache, wraps, singledispatch
import operator
from typing import Callable, List, Any, Optional


# ============== map ==============

def map_demo():
    """map演示"""
    numbers = [1, 2, 3, 4, 5]
    
    squared = list(map(lambda x: x ** 2, numbers))
    print(f"平方: {squared}")
    
    strings = list(map(str, numbers))
    print(f"字符串: {strings}")


# ============== filter ==============

def filter_demo():
    """filter演示"""
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    
    evens = list(filter(lambda x: x % 2 == 0, numbers))
    print(f"偶数: {evens}")
    
    greater = list(filter(lambda x: x > 5, numbers))
    print(f">5: {greater}")


# ============== reduce ==============

def reduce_demo():
    """reduce演示"""
    from functools import reduce
    
    numbers = [1, 2, 3, 4, 5]
    
    total = reduce(lambda a, b: a + b, numbers)
    print(f"总和: {total}")
    
    product = reduce(lambda a, b: a * b, numbers)
    print(f"乘积: {product}")
    
    max_val = reduce(lambda a, b: a if a > b else b, numbers)
    print(f"最大值: {max_val}")


# ============== lambda ==============

def lambda_demo():
    """lambda演示"""
    add = lambda x, y: x + y
    print(f"add: {add(3, 5)}")
    
    greater = lambda a, b: a if a > b else b
    print(f"greater: {greater(10, 20)}")
    
    is_even = lambda x: x % 2 == 0
    print(f"is_even(4): {is_even(4)}")


# ============== operator ==============

def operator_demo():
    """operator演示"""
    print(f"add: {operator.add(3, 5)}")
    print(f"mul: {operator.mul(3, 5)}")
    print(f"pow: {operator.pow(2, 3)}")
    print(f"neg: {operator.neg(5)}")
    print(f"not_: {operator.not_(True)}")
    print(f"truth: {operator.truth([])}")
    print(f"is_: {operator.is_(1, 1)}")
    print(f"is_not: {operator.is_not(1, 2)}")
    
    print(f"attrgetter: {operator.attrgetter('__name__')(str)}")
    print(f"itemgetter: {operator.itemgetter(1)([1,2,3])}")
    
    inc = operator.inc(5)
    print(f"inc: {inc}")
    
    dec = operator.dec(5)
    print(f"dec: {dec}")


# ============== partial ==============

def power(base, exponent):
    """幂函数"""
    return base ** exponent


def partial_demo():
    """partial演示"""
    square = partial(power, exponent=2)
    cube = partial(power, exponent=3)
    
    print(f"square(5): {square(5)}")
    print(f"cube(5): {cube(5)}")
    
    def multiply(a, b, c=1):
        return a * b * c
    
    triple = partial(multiply, c=3)
    print(f"triple(2, 3): {triple(2, 3)}")


# ============== lru_cache ==============

@lru_cache(maxsize=None)
def fib(n):
    """斐波那契 - 缓存"""
    if n < 2:
        return n
    return fib(n - 1) + fib(n - 2)


def cache_demo():
    """缓存演示"""
    import time
    
    start = time.perf_counter()
    for i in range(20):
        fib(i)
    elapsed = time.perf_counter() - start
    print(f"fib(20): {fib(20)}, 耗时: {elapsed:.6f}s")
    
    print(f"cache_info: {fib.cache_info()}")
    
    fib.cache_clear()


# ============== singledispatch ==============

@singledispatch
def process(data):
    """通用处理"""
    return f"处理: {data}"


@process.register(int)
def process_int(data):
    return f"整数: {data * 2}"


@process.register(str)
def process_str(data):
    return f"字符串: {data.upper()}"


@process.register(list)
def process_list(data):
    return f"列表: {len(data)}"


def singledispatch_demo():
    """单分发演示"""
    print(process(10))
    print(process("hello"))
    print(process([1, 2, 3]))
    print(process(3.14))


# ============== compose ==============

def compose(*funcs: Callable) -> Callable:
    """函数组合"""
    def composed(x):
        result = x
        for func in reversed(funcs):
            result = func(result)
        return result
    return composed


def compose_demo():
    """组合演示"""
    f = compose(
        lambda x: x + 1,
        lambda x: x * 2,
        lambda x: x - 1
    )
    
    print(f"compose: {f(5)}")
    
    f2 = compose(
        str.upper,
        lambda s: s.strip(),
        lambda s: s + " world"
    )
    print(f"compose2: {f2('  hello')}")


# ============== currying ==============

def curry(func: Callable) -> Callable:
    """柯里化"""
    import inspect
    sig = inspect.signature(func)
    params = list(sig.parameters.keys())
    arity = len(params)
    
    @wraps(func)
    def curried(*args):
        if len(args) >= arity:
            return func(*args[:arity])
        
        def next_func(*more):
            return curried(*(args + more))
        
        return next_func
    
    return curried


@curry
def add_three(a, b, c):
    return a + b + c


def curry_demo():
    """柯里化演示"""
    print(f"add_three(1)(2)(3): {add_three(1)(2)(3)}")
    print(f"add_three(1, 2)(3): {add_three(1, 2)(3)}")
    print(f"add_three(1, 2, 3): {add_three(1, 2, 3)}")


# ============== 偏函数 ==============

def modulo(divisor, dividend):
    return dividend % divisor


def modulo_demo():
    """偏函数演示"""
    is_even = partial(modulo, divisor=2)
    print(f"is_even(4): {is_even(4)}")
    print(f"is_even(5): {is_even(5)}")
    
    is_divisible_by_3 = partial(modulo, divisor=3)
    print(f"is_divisible_by_3(9): {is_divisible_by_3(9)}")


# ============== 函数式过滤 ==============

def functional_filter():
    """函数式过滤"""
    data = [
        {"name": "Alice", "age": 25},
        {"name": "Bob", "age": 30},
        {"name": "Charlie", "age": 20},
    ]
    
    adults = list(filter(lambda x: x["age"] >= 21, data))
    print(f"成年人: {adults}")
    
    names = list(map(lambda x: x["name"], data))
    print(f"名字: {names}")


# ============== 函数式映射 ==============

def functional_map():
    """函数式映射"""
    data = [1, 2, 3, 4, 5]
    
    result = list(map(lambda x: x ** 2, data))
    print(f"平方: {result}")
    
    pairs = [(1, 2), (3, 4), (5, 6)]
    added = list(map(lambda x: x[0] + x[1], pairs))
    print(f"相加: {added}")
    
    zipped = list(zip([1, 2, 3], ["a", "b", "c"]))
    print(f"zip: {zipped}")


# ============== 函数式归约 ==============

def functional_reduce():
    """函数式归约"""
    from functools import reduce
    
    data = [1, 2, 3, 4, 5]
    
    total = reduce(operator.add, data)
    print(f"总和: {total}")
    
    max_val = reduce(lambda a, b: a if a > b else b, data)
    print(f"最大值: {max_val}")
    
    join = reduce(lambda a, b: f"{a}{b}", ["a", "b", "c", "d"])
    print(f"连接: {join}")


# ============== 函数式工具 ==============

def functional_tools():
    """函数式工具"""
    from functools import partial
    
    double = partial(operator.mul, 2)
    triple = partial(operator.mul, 3)
    
    numbers = list(range(1, 6))
    
    doubled = list(map(double, numbers))
    tripled = list(map(triple, numbers))
    
    print(f"原始: {numbers}")
    print(f"double: {doubled}")
    print(f"triple: {tripled}")
    
    evens = list(filter(lambda x: x % 2 == 0, doubled))
    print(f"偶数: {evens}")


# ============== 测试运行 ==============

if __name__ == "__main__":
    print("=" * 50)
    print("22. 函数式编程")
    print("=" * 50)
    
    # 测试1: map
    print("\n--- 1. map ---")
    map_demo()
    
    # 测试2: filter
    print("\n--- 2. filter ---")
    filter_demo()
    
    # 测试3: reduce
    print("\n--- 3. reduce ---")
    reduce_demo()
    
    # 测试4: lambda
    print("\n--- 4. lambda ---")
    lambda_demo()
    
    # 测试5: operator
    print("\n--- 5. operator ---")
    operator_demo()
    
    # 测试6: partial
    print("\n--- 6. partial ---")
    partial_demo()
    
    # 测试7: lru_cache
    print("\n--- 7. lru_cache ---")
    cache_demo()
    
    # 测试8: singledispatch
    print("\n--- 8. singledispatch ---")
    singledispatch_demo()
    
    # 测试9: compose
    print("\n--- 9. compose ---")
    compose_demo()
    
    # 测试10: curry
    print("\n--- 10. curry ---")
    curry_demo()
    
    # 测试11: modulo
    print("\n--- 11. modulo ---")
    modulo_demo()
    
    # 测试12: 函数式过滤
    print("\n--- 12. 函数式过滤 ---")
    functional_filter()
    
    # 测试13: 函数式映射
    print("\n--- 13. 函数式映射 ---")
    functional_map()
    
    # 测试14: 函数式归约
    print("\n--- 14. 函数式归约 ---")
    functional_reduce()
    
    # 测试15: 函数式工具
    print("\n--- 15. 函数式工具 ---")
    functional_tools()
    
    print("\n" + "=" * 50)
    print("函数式编程学习完成!")
    print("=" * 50)