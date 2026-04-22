"""
第1章: 基础函数装饰器
====================

装饰器是Python中最常见的元编程形式.
本质上是一个接收函数作为参数并返回新函数的函数.

关键概念:
- @decorator 语法糖
- functools.wraps 保持原函数元信息
- 闭包
"""

from functools import wraps
import time
from typing import Callable, Any


# ============== 最简单的装饰器 ==============

def simple_decorator(func: Callable) -> Callable:
    """
    最简单的装饰器 - 在函数执行前后添加行为
    
    原理:
    1. 接收原函数作为参数
    2. 定义一个wrapper包装函数
    3. 在wrapper中添加额外逻辑
    4. 返回wrapper函数(替代原函数)
    """
    @wraps(func)  # 保持原函数的 __name__, __doc__ 等元信息
    def wrapper(*args, **kwargs):
        print(f"[装饰器] 执行前: {func.__name__}")
        result = func(*args, **kwargs)
        print(f"[装饰器] 执行后: {func.__name__}")
        return result
    return wrapper


@simple_decorator
def say_hello(name: str) -> str:
    """问候函数"""
    return f"Hello, {name}!"


# ============== 计时装饰器 ==============

def timer(func: Callable) -> Callable:
    """测量函数执行时间"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"[timer] {func.__name__} 执行耗时: {elapsed:.6f}秒")
        return result
    return wrapper


@timer
def slow_function():
    """模拟慢函数"""
    time.sleep(0.1)
    return "完成"


# ============== 日志装饰器 ==============

def logger(func: Callable) -> Callable:
    """记录函数调用日志"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"[调用] {func.__name__}(args={args}, kwargs={kwargs})")
        result = func(*args, **kwargs)
        print(f"[返回] {func.__name__} -> {result}")
        return result
    return wrapper


@logger
def add(a: int, b: int) -> int:
    """加法函数"""
    return a + b


# ============== 缓存装饰器 (Memoization) ==============

def cache(func: Callable) -> Callable:
    """
    简单缓存装饰器
    
    注意: 只能缓存可哈希的参数
    实际项目中可使用 functools.lru_cache
    """
    memo = {}
    
    @wraps(func)
    def wrapper(*args, **kwargs):
        # 将参数转换为可哈希的key
        key = args  # tuple, 可哈希
        if key in memo:
            print(f"[cache] 命中缓存: {key}")
            return memo[key]
        result = func(*args, **kwargs)
        memo[key] = result
        print(f"[cache] 新增缓存: {key}")
        return result
    return wrapper


@cache
def fibonacci(n: int) -> int:
    """斐波那契数列 - 有缓存后效率大幅提升"""
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)


# ============== 调试装饰器 ==============

def debug(func: Callable) -> Callable:
    """
    调试装饰器 - 显示函数详细信息
    
    展示Python函数的内省(introspection)能力
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        # 函数签名
        import inspect
        sig = inspect.signature(func)
        print(f"[debug] 函数: {func.__name__}")
        print(f"[debug] 签名: {sig}")
        print(f"[debug] 参数绑定:")
        
        # 绑定参数
        bound = sig.bind(*args, **kwargs)
        bound.apply_defaults()
        for name, value in bound.arguments.items():
            print(f"  {name} = {value}")
        
        result = func(*args, **kwargs)
        print(f"[debug] 返回值: {result}")
        return result
    return wrapper


@debug
def greet(message: str, times: int = 1) -> str:
    """问候函数"""
    return " ".join([message] * times)


# ============== 重试装饰器 ==============

def retry(max_attempts: int = 3, delay: float = 1.0):
    """
    重试装饰器工厂
    
    这个装饰器需要接受参数,所以需要两层嵌套:
    - 外层: 接收装饰器参数
    - 内层: 接收函数并返回包装函数
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(1, max_attempts + 1):
                try:
                    result = func(*args, **kwargs)
                    if attempt > 1:
                        print(f"[retry] 第{attempt}次尝试成功")
                    return result
                except Exception as e:
                    last_exception = e
                    if attempt < max_attempts:
                        print(f"[retry] 第{attempt}次失败: {e}, {delay}秒后重试...")
                        time.sleep(delay)
            print(f"[retry] 最大重试次数{max_attempts}次已用完")
            raise last_exception
        return wrapper
    return decorator


@retry(max_attempts=3, delay=0.5)
def unstable_function(should_fail: bool = False) -> str:
    """模拟不稳定的函数"""
    if should_fail:
        raise ValueError("不稳定!")
    return "成功"


# ============== 测试运行 ==============

if __name__ == "__main__":
    print("=" * 50)
    print("1. 基础函数装饰器")
    print("=" * 50)
    
    # 测试1: 简单装饰器
    print("\n--- 测试: simple_decorator ---")
    result = say_hello("World")
    print(f"结果: {result}")
    
    # 测试2: 计时装饰器
    print("\n--- 测试: timer ---")
    slow_function()
    
    # 测试3: 日志装饰器
    print("\n--- 测试: logger ---")
    add(3, 5)
    
    # 测试4: 缓存装饰器
    print("\n--- 测试: cache (fibonacci) ---")
    print(f"fibonacci(10) = {fibonacci(10)}")
    print(f"(再次调用会命中缓存)")
    print(f"fibonacci(10) = {fibonacci(10)}")
    
    # 测试5: 调试装饰器
    print("\n--- 测试: debug ---")
    greet("Hi", times=2)
    
    # 测试6: 重试装饰器
    print("\n--- 测试: retry ---")
    unstable_function(should_fail=False)
    try:
        unstable_function(should_fail=True)
    except ValueError as e:
        print(f"异常被正确抛出: {e}")
    
    print("\n" + "=" * 50)
    print("装饰器基础学习完成!")
    print("=" * 50)