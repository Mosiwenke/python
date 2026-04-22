"""
第3章: 带参数的装饰器 & 装饰器堆叠
=====================================

这一章展示如何创建可以接收参数的装饰器,
以及如何堆叠多个装饰器.

关键技术:
- 双层/三层嵌套函数
- 装饰器执行顺序
- 构建可配置的装饰器工厂
"""

from functools import wraps
from typing import Callable, List, Any
import time
import functools


# ============== 带参数的装饰器 ==============

def repeat(times: int = 1, delay: float = 0):
    """
    带参数的装饰器 - 重复执行函数
    
    参数:
        times: 重复次数
        delay: 每次执行间隔(秒)
    
    结构: 三层嵌套
        - 外层: 接收装饰器参数
        - 中层: 接收被装饰的函数
        - 内层: 实际的包装函数
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            results = []
            for i in range(times):
                if delay > 0 and i > 0:
                    time.sleep(delay)
                result = func(*args, **kwargs)
                results.append(result)
            return results
        return wrapper
    return decorator


@repeat(times=3, delay=0.1)
def greet(name: str) -> str:
    return f"Hello, {name}!"


# ============== 条件装饰器 ==============

def conditional(condition: bool):
    """
    条件装饰器 - 根据条件决定是否执行装饰器
    
    用法:
        @conditional(False)  -> 函数保持原样
        @conditional(True) -> 函数被包装
    """
    def decorator(func: Callable) -> Callable:
        if not condition:
            return func  # 返回原函数
        
        @wraps(func)
        def wrapper(*args, **kwargs):
            print(f"[conditional] 执行条件成立: {func.__name__}")
            return func(*args, **kwargs)
        return wrapper
    return decorator


@conditional(True)
def conditional_function():
    return "执行了!"


# ============== 装饰器堆叠 ==============

def uppercase(func: Callable) -> Callable:
    """转换为大写"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs).upper()
    return wrapper


def strip(func: Callable) -> Callable:
    """去除首尾空格"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs).strip()
    return wrapper


def add_exclamation(func: Callable) -> Callable:
    """添加感叹号"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs) + "!"
    return wrapper


# 装饰器堆叠 - 从下往上执行
# 实际执行顺序: add_exclamation -> strip -> uppercase -> text
@add_exclamation
@strip
@uppercase
def text():
    return "   hello world   "


# ============== 验证参数装饰器 ==============

def validate(**validators):
    """
    参数验证装饰器
    
    参数:
        validators: 参数名 -> 验证函数的映射
    
    示例:
        @validate(age=lambda x: x >= 0)
        def set_age(age):
            ...
    """
    def decorator(func: Callable) -> Callable:
        sig = functools.signature(func)
        
        @wraps(func)
        def wrapper(*args, **kwargs):
            # 绑定参数
            bound = sig.bind(*args, **kwargs)
            bound.apply_defaults()
            
            # 验证
            for param_name, validator in validators.items():
                if param_name in bound.arguments:
                    value = bound.arguments[param_name]
                    if not validator(value):
                        raise ValueError(
                            f"参数 '{param_name}' 验证失败: {value}"
                        )
            
            return func(*args, **kwargs)
        return wrapper
    return decorator


@validate(
    age=lambda x: x >= 0,
    name=lambda x: len(x) > 0
)
def create_user(name: str, age: int) -> dict:
    return {"name": name, "age": age}


# ============== 速率限制装饰器 ==============

class RateLimiter:
    """速率限制器"""
    
    def __init__(self, max_calls: int, period: float):
        self.max_calls = max_calls
        self.period = period
        self.calls: List[float] = []
    
    def __call__(self, func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            now = time.time()
            # 清理过期的调用记录
            self.calls = [
                t for t in self.calls
                if now - t < self.period
            ]
            
            if len(self.calls) >= self.max_calls:
                wait_time = self.period - (now - self.calls[0])
                raise RuntimeError(
                    f"速率限制: 最多 {self.max_calls} 次调用 / {self.period}秒"
                    f", 需要等待 {wait_time:.2f}秒"
                )
            
            self.calls.append(now)
            return func(*args, **kwargs)
        return wrapper


@RateLimiter(max_calls=3, period=10)
def api_request() -> str:
    return "API响应"


# ============== 权限检查装饰器 ==============

class MockUser:
    def __init__(self, name: str, roles: List[str]):
        self.name = name
        self.roles = roles


_current_user = MockUser("Alice", ["user"])


def requires_permission(*permissions):
    """
    权限检查装饰器
    
    参数:
        permissions: 需要的权限列表
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            user = kwargs.get('user') or _current_user
            
            missing = [
                perm for perm in permissions
                if perm not in user.roles
            ]
            
            if missing:
                raise PermissionError(
                    f"缺少权限: {missing}"
                )
            
            return func(*args, **kwargs)
        return wrapper
    return decorator


@requires_permission("admin", "editor")
def manage_settings(user=None):
    return "设置已更新"


# ============== 缓存装饰器工厂 ==============

def memoize(maxsize: int = 128):
    """
    缓存装饰器工厂
    
    可配置缓存大小的LRU缓存
    """
    cache = {}
    cache_order = []
    
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            key = str(args) + str(kwargs)
            
            if key in cache:
                return cache[key]
            
            result = func(*args, **kwargs)
            
            # LRU: 添加到末尾
            cache[key] = result
            cache_order.append(key)
            
            # 超过最大size时删除最老的
            if len(cache) > maxsize:
                oldest = cache_order.pop(0)
                del cache[oldest]
            
            return result
        
        # 添加缓存清除方法
        wrapper.clear_cache = lambda: (cache.clear(), cache_order.clear())
        wrapper.cache_info = lambda: {"size": len(cache), "maxsize": maxsize}
        
        return wrapper
    return decorator


@memoize(maxsize=3)
def expensive_computation(x: int) -> int:
    time.sleep(0.05)  # 模拟耗时
    return x * x


# ============== 测试运行 ==============

if __name__ == "__main__":
    print("=" * 50)
    print("3. 带参数装饰器 & 装饰器堆叠")
    print("=" * 50)
    
    # 测试1: 重复装饰器
    print("\n--- 测试: repeat ---")
    results = greet("World")
    for i, r in enumerate(results, 1):
        print(f"第{i}次: {r}")
    
    # 测试2: 装饰器堆叠
    print("\n--- 测试: 装饰器堆叠 ---")
    print(f"结果: '{text()}'")
    print("执行顺序: uppercase -> strip -> add_exclamation")
    
    # 测试3: 参数验证
    print("\n--- 测试: validate ---")
    print(create_user("Bob", 25))
    try:
        create_user("", -5)
    except ValueError as e:
        print(f"验证失败: {e}")
    
    # 测试4: 速率限制
    print("\n--- 测试: RateLimiter ---")
    for i in range(3):
        try:
            result = api_request()
            print(f"请求{i+1}: {result}")
        except RuntimeError as e:
            print(f"请求{i+1}: 限制 - {e}")
    
    # 测试5: 权限检查
    print("\n--- 测试: requires_permission ---")
    admin_user = MockUser("Admin", ["admin", "editor"])
    manage_settings(user=admin_user)
    try:
        manage_settings(user=_current_user)
    except PermissionError as e:
        print(f"权限错误: {e}")
    
    # 测试6: 可配置缓存
    print("\n--- 测试: memoize ---")
    print(f"计算(2): {expensive_computation(2)}")
    print(f"计算(2): {expensive_computation(2)} (命中缓存)")
    print(f"计算(3): {expensive_computation(3)}")
    print(f"缓存信息: {expensive_computation.cache_info()}")
    
    print("\n" + "=" * 50)
    print("带参数装饰器学习完成!")
    print("=" * 50)