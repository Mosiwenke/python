"""
第12章: 更深入的元编程技术
=====================================

高级元编程技术,探索Python的边界能力.
"""

import types
import sys
import weakref
import gc
import inspect
import operator
import functools
from typing import Any, Callable, Dict


# ============== 弱引用 ==============

class WeakCallback:
    """使用弱引用的回调"""
    
    def __init__(self, callback: Callable):
        self._callback = callback
        self._ref = weakref.ref(callback)
    
    def __call__(self, *args, **kwargs):
        cb = self._ref()
        if cb is not None:
            return cb(*args, **kwargs)
        return None


# ============== 弱引用缓存 ==============

class WeakCache:
    """弱引用缓存"""
    
    def __init__(self, maxsize: int = 128):
        self.maxsize = maxsize
        self._cache = weakref.WeakValueDictionary()
        self._order = []
    
    def get(self, key: Any) -> Any:
        return self._cache.get(key)
    
    def set(self, key: Any, value: Any):
        if len(self._cache) >= self.maxsize:
            oldest = self._order.pop(0)
            self._cache.pop(oldest, None)
        
        self._cache[key] = value
        self._order.append(key)


# ============== 一等函数 ==============

def higher_order():
    """一等函数 - 函数作为参数和返回值"""
    
    def add(a, b):
        return a + b
    
    def multiply(a, b):
        return a * b
    
    def apply_operation(op: Callable, a: int, b: int) -> int:
        return op(a, b)
    
    def create_adder(n: int) -> Callable:
        """返回加n的函数"""
        def adder(x):
            return x + n
        return adder
    
    print(f"apply_operation(add, 2, 3) = {apply_operation(add, 2, 3)}")
    print(f"apply_operation(multiply, 2, 3) = {apply_operation(multiply, 2, 3)}")
    
    add5 = create_adder(5)
    print(f"add5(10) = {add5(10)}")


# ============== 闭包高级 ==============

def closure_advanced():
    """高级闭包用法"""
    
    def make_logger(name: str):
        """创建日志记录器"""
        logs = []
        
        def log(message: str):
            logs.append(f"[{name}] {message}")
            return logs[-1]
        
        def get_logs():
            return logs.copy()
        
        def clear():
            logs.clear()
        
        # 闭包携带多个函数
        log.get_logs = get_logs
        log.clear = clear
        return log
    
    log = make_logger("TEST")
    log("启动")
    log("运行中")
    print(f"日志: {log.get_logs()}")
    log.clear()
    print(f"清空后: {log.get_logs()}")


# ============== 容器闭包 (多个函数共享状态) ==============

def make_counter():
    """创建计数器"""
    count = [0]  # 使用可变对象保持状态
    
    def increment():
        count[0] += 1
        return count[0]
    
    def decrement():
        count[0] -= 1
        return count[0]
    
    def get():
        return count[0]
    
    def reset():
        count[0] = 0
    
    return {
        'inc': increment,
        'dec': decrement,
        'get': get,
        'reset': reset,
    }


# ============== 操作符模块 ==============

def operator_examples():
    """操作符模块的使用"""
    
    # operator.attrgetter
    class Person:
        def __init__(self, name: str, age: int):
            self.name = name
            self.age = age
    
    people = [Person("Bob", 30), Person("Alice", 25)]
    
    # 按age排序
    people.sort(key=operator.attrgetter('age'))
    print(f"排序结果: {[(p.name, p.age) for p in people]}")
    
    # operator.itemgetter
    data = [{'name': 'a', 'score': 90}, {'name': 'b', 'score': 80}]
    scores = list(map(operator.itemgetter('score'), data))
    print(f"分数: {scores}")
    
    # operator.methodcaller
    strings = ["hello", "WORLD", "Test"]
    uppered = list(map(operator.methodcaller('upper'), strings))
    print(f"大写: {uppered}")


# ============== 缓存和记忆化 ==============

memoized = {}

def memoize(func: Callable) -> Callable:
    """记忆化装饰器"""
    
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        key = (args, tuple(sorted(kwargs.items())))
        if key not in memoized:
            memoized[key] = func(*args, **kwargs)
        return memoized[key]
    
    wrapper.clear_cache = lambda: memoized.clear()
    return wrapper


@memoize
def fib(n: int) -> int:
    if n < 2:
        return n
    return fib(n-1) + fib(n-2)


# ============== 类作为函数 ==============

class CallableClass:
    """可调用的类"""
    
    def __init__(self, multiplier: int):
        self.multiplier = multiplier
    
    def __call__(self, x: int) -> int:
        return x * self.multiplier


# ============== 元组解包 ==============

def tuple_unpack():
    """元组解包在函数返回值中的使用"""
    
    def get_stats(numbers):
        return len(numbers), sum(numbers), sum(numbers) / len(numbers)
    
    numbers = [1, 2, 3, 4, 5]
    count, total, average = get_stats(numbers)
    print(f"数量: {count}, 总和: {total}, 平均: {average}")


# ============== 函数组合 ==============

def compose(*funcs: Callable) -> Callable:
    """函数组合"""
    
    def composed(x):
        result = x
        for func in reversed(funcs):
            result = func(result)
        return result
    
    return composed


# ============== 自动柯里化 ==============

def curry(func: Callable) -> Callable:
    """自动柯里化"""
    sig = inspect.signature(func)
    params = list(sig.parameters.keys())
    arity = len(params)
    
    @functools.wraps(func)
    def curried(*args):
        if len(args) >= arity:
            return func(*args[:arity])
        
        @functools.wraps(func)
        def next_curried(*more):
            return curried(*(args + more))
        
        return next_curried
    
    return curried


# ============== 测试运行 ==============

if __name__ == "__main__":
    print("=" * 50)
    print("12. 更深入的元编程技术")
    print("=" * 50)
    
    # 测试1: 闭包高级
    print("\n--- 1. 高级闭包 ---")
    closure_advanced()
    
    # 测试2: 容器闭包
    print("\n--- 2. 容器闭包 ---")
    counter = make_counter()
    for _ in range(3):
        counter['inc']()
    print(f"计数: {counter['get']()}")
    counter['reset']()
    print(f"重置: {counter['get']()}")
    
    # 测试3: 操作符模块
    print("\n--- 3. 操作符模块 ---")
    operator_examples()
    
    # 测试4: 记忆化
    print("\n--- 4. 记忆化 ---")
    import time
    start = time.perf_counter()
    result = fib(20)
    elapsed = time.perf_counter() - start
    print(f"fib(20) = {result}, 耗时: {elapsed:.6f}秒")
    fib.clear_cache()
    
    # 测试5: 类作为函数
    print("\n--- 5. 可调用类 ---")
    doubler = CallableClass(2)
    print(f"doubler(5) = {doubler(5)}")
    
    # 测试6: 函数组合
    print("\n--- 6. 函数组合 ---")
    f = compose(lambda x: x + 1, lambda x: x * 2)
    print(f"compose: (1 + 1) * 2 = {f(1)}")
    
    # 测试7: 柯里化
    print("\n--- 7. 柯里化 ---")
    @curry
    def add_three(a, b, c):
        return a + b + c
    
    print(f"add_three(1)(2)(3) = {add_three(1)(2)(3)}")
    print(f"add_three(1, 2)(3) = {add_three(1, 2)(3)}")
    
    print("\n" + "=" * 50)
    print("深入元编程学习完成!")
    print("=" * 50)