"""
第7章: 装饰器模式实际应用场景
=================================

展示装饰器在实际项目中的高级应用.
"""

from functools import wraps, lru_cache
from typing import Callable, Any, Dict, List, Optional
import time
import asyncio
import hashlib
import json


# ============== Web框架风格装饰器 ==============

def route(path: str, methods: List[str] = None):
    """
    Web路由装饰器 - 类似Flask的路由系统
    
    用法:
        @route('/user', methods=['GET'])
        def get_user():
            ...
    """
    methods = methods or ['GET']
    
    def decorator(func: Callable) -> Callable:
        func.route_path = path
        func.route_methods = methods
        
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        
        wrapper.route_path = path
        wrapper.route_methods = methods
        return wrapper
    
    return decorator


def before_request(func: Callable) -> Callable:
    """请求前处理装饰器"""
    func._before_request = True
    return func


def after_request(func: Callable) -> Callable:
    """请求后处理装饰器"""
    func._after_request = True
    return func


class FlaskLikeApp:
    """简化的Flask风格应用"""
    
    routes = {}
    before_handlers = []
    after_handlers = []
    
    @classmethod
    def register(cls, path: str, methods: List[str]):
        def decorator(func: Callable):
            cls.routes[(path, tuple(methods))] = func
            print(f"[Flask] 注册路由: {path} -> {func.__name__}")
            return func
        return decorator
    
    @classmethod
    def before_request(cls, func: Callable):
        cls.before_handlers.append(func)
        print(f"[Flask] 注册前置处理器: {func.__name__}")
        return func
    
    @classmethod
    def after_request(cls, func: Callable):
        cls.after_handlers.append(func)
        print(f"[Flask] 注册后置处理器: {func.__name__}")
        return func
    
    @classmethod
    def run(cls, path: str, method: str = 'GET'):
        key = (path, (method,))
        if key in cls.routes:
            for handler in cls.before_handlers:
                handler()
            
            result = cls.routes[key]()
            
            for handler in cls.after_handlers:
                handler()
            
            return result
        return "404 Not Found"


# ============== API版本控制装饰器 ==============

def version(api_version: str):
    """
    API版本控制装饰器
    
    用法:
        @version('v1')
        def get_data():
            return {'data': 'v1'}
        
        @version('v2')
        def get_data():
            return {'data': 'v2', 'extra': 'field'}
    """
    def decorator(func: Callable) -> Callable:
        func.api_version = api_version
        return func
    
    return decorator


class APIVersionManager:
    """API版本管理器"""
    
    versions: Dict[str, Dict[str, Callable]] = {
        'v1': {},
        'v2': {},
        'v3': {},
    }
    
    @classmethod
    def register(cls, version: str):
        def decorator(func: Callable):
            cls.versions[version][func.__name__] = func
            return func
        return decorator
    
    @classmethod
    def get(cls, name: str, version: str = 'v1') -> Any:
        if name in cls.versions[version]:
            return cls.versions[version][name]
        return None
    
    @classmethod
    def call(cls, name: str, version: str, *args, **kwargs) -> Any:
        func = cls.get(name, version)
        if func:
            return func(*args, **kwargs)
        return {'error': 'not found'}


# ============== 缓存策略装饰器 ==============

class CacheStrategy:
    """缓存策略 - 支持多种过期策略"""
    
    def __init__(self, ttl: float = 60, key_prefix: str = ''):
        self.ttl = ttl
        self.key_prefix = key_prefix
        self._cache = {}
    
    def make_key(self, func: Callable, args: tuple) -> str:
        key = f"{self.key_prefix}:{func.__name__}:{args}"
        return hashlib.md5(key.encode()).hexdigest()
    
    def __call__(self, func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            key = self.make_key(func, args)
            now = time.time()
            
            if key in self._cache:
                value, timestamp = self._cache[key]
                if now - timestamp < self.ttl:
                    print(f"[CacheStrategy] 缓存命中: {key}")
                    return value
            
            result = func(*args, **kwargs)
            self._cache[key] = (result, now)
            print(f"[CacheStrategy] 缓存写入: {key}")
            return result
        
        wrapper.clear = lambda: self._cache.clear()
        return wrapper


# ============== 限流装饰器 ==============

class TokenBucket:
    """令牌桶算法实现"""
    
    def __init__(self, rate: float, capacity: int):
        self.rate = rate  # 每秒产生多少令牌
        self.capacity = capacity  # 桶容量
        self.tokens = capacity
        self.last_time = time.time()
    
    def consume(self, tokens: int = 1) -> bool:
        now = time.time()
        elapsed = now - self.last_time
        self.tokens = min(self.capacity, self.tokens + elapsed * self.rate)
        self.last_time = now
        
        if self.tokens >= tokens:
            self.tokens -= tokens
            return True
        return False


def rate_limit(rate: float, capacity: int):
    """
    限流装饰器 - 使用令牌桶算法
    
    参数:
        rate: 每秒处理的请求数
        capacity: 桶容量
    """
    bucket = TokenBucket(rate, capacity)
    
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not bucket.consume():
                raise RuntimeError("请求过于频繁,请稍后重试")
            return func(*args, **kwargs)
        return wrapper
    
    return decorator


# ============== 异步装饰器 ==============

def async_retry(times: int = 3, delay: float = 1.0):
    """异步重试装饰器"""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs):
            last_error = None
            for attempt in range(1, times + 1):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    last_error = e
                    if attempt < times:
                        await asyncio.sleep(delay)
            raise last_error
        return wrapper
    return decorator


def async_timeout(seconds: float):
    """异步超时装饰器"""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                return await asyncio.wait_for(
                    func(*args, **kwargs),
                    timeout=seconds
                )
            except asyncio.TimeoutError:
                raise TimeoutError(f"操作超时 ({seconds}秒)")
        return wrapper
    return decorator


async def fetch_data(url: str) -> str:
    """模拟异步获取数据"""
    await asyncio.sleep(0.5)
    return f"Data from {url}"


# ============== 性能分析装饰器 ==============

class Profiler:
    """性能分析器 - 记录函数执行统计"""
    
    stats = {}
    
    @classmethod
    def profile(cls, func: Callable) -> Callable:
        if func.__name__ not in cls.stats:
            cls.stats[func.__name__] = {
                'calls': 0,
                'total_time': 0,
                'min_time': float('inf'),
                'max_time': 0,
            }
        
        @wraps(func)
        def wrapper(*args, **kwargs):
            start = time.perf_counter()
            result = func(*args, **kwargs)
            elapsed = time.perf_counter() - start
            
            stat = cls.stats[func.__name__]
            stat['calls'] += 1
            stat['total_time'] += elapsed
            stat['min_time'] = min(stat['min_time'], elapsed)
            stat['max_time'] = max(stat['max_time'], elapsed)
            
            return result
        
        wrapper.get_stats = lambda: cls.stats[func.__name__].copy()
        return wrapper
    
    @classmethod
    def report(cls):
        print("\n=== 性能报告 ===")
        for name, stat in cls.stats.items():
            avg = stat['total_time'] / stat['calls'] if stat['calls'] > 0 else 0
            print(f"{name}:")
            print(f"  调用次数: {stat['calls']}")
            print(f"  平均耗时: {avg*1000:.2f}ms")
            print(f"  最小耗时: {stat['min_time']*1000:.2f}ms")
            print(f"  最大耗时: {stat['max_time']*1000:.2f}ms")


# ============== 权限RBAC装饰器 ==============

class Role:
    """角色定义"""
    ADMIN = 'admin'
    USER = 'user'
    GUEST = 'guest'


class Permission:
    """权限检查器"""
    
    _permissions = {
        'admin': ['read', 'write', 'delete'],
        'user': ['read', 'write'],
        'guest': ['read'],
    }
    
    @classmethod
    def check(cls, role: str, permission: str) -> bool:
        return permission in cls._permissions.get(role, [])


def require_permission(permission: str):
    """权限要求装饰器"""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            user = kwargs.get('user')
            if user and Permission.check(user.get('role', ''), permission):
                return func(*args, **kwargs)
            raise PermissionError(f"需要权限: {permission}")
        return wrapper
    return decorator


# ============== 事件驱动装饰器 ==============

class Event:
    """简单的事件系统"""
    
    _handlers = {}
    
    @classmethod
    def on(cls, event_name: str):
        def decorator(func: Callable):
            if event_name not in cls._handlers:
                cls._handlers[event_name] = []
            cls._handlers[event_name].append(func)
            return func
        return decorator
    
    @classmethod
    def emit(cls, event_name: str, *args, **kwargs):
        if event_name in cls._handlers:
            for handler in cls._handlers[event_name]:
                handler(*args, **kwargs)


# ============== 插件系统 ==============

class Plugin:
    """插件管理器"""
    
    _plugins = []
    
    @classmethod
    def register(cls, name: str):
        def decorator(cls_type):
            cls._plugins.append((name, cls_type))
            print(f"[Plugin] 注册: {name}")
            return cls_type
        return decorator
    
    @classmethod
    def get_plugins(cls):
        return cls._plugins.copy()


# ============== 测试运行 ==============

if __name__ == "__main__":
    print("=" * 50)
    print("7. 装饰器实际应用场景")
    print("=" * 50)
    
    # 测试1: Web路由
    print("\n--- 测试: Web路由 ---")
    
    @FlaskLikeApp.register('/user', ['GET'])
    def get_user():
        return {"name": "Alice", "age": 30}
    
    FlaskLikeApp.before_request(lambda: print("  -> 验证请求"))
    FlaskLikeApp.after_request(lambda: print("  -> 记录日志"))
    
    result = FlaskLikeApp.run('/user', 'GET')
    print(f"响应: {result}")
    
    # 测试2: API版本控制
    print("\n--- 测试: API版本控制 ---")
    
    @APIVersionManager.register('v1')
    def get_user_v1():
        return {"name": "Alice"}
    
    @APIVersionManager.register('v2')
    def get_user_v2():
        return {"name": "Alice", "email": "alice@example.com"}
    
    print(f"v1: {APIVersionManager.call('get_user', 'v1')}")
    print(f"v2: {APIVersionManager.call('get_user', 'v2')}")
    
    # 测试3: 限流
    print("\n--- 测试: 限流 ---")
    
    @rate_limit(rate=2, capacity=2)
    def api_call():
        return "响应"
    
    for i in range(5):
        try:
            api_call()
            print(f"请求{i+1}: 成功")
        except RuntimeError as e:
            print(f"请求{i+1}: {e}")
    
    # 测试4: 异步装饰器
    print("\n--- 测试: 异步装饰器 ---")
    
    @async_retry(times=3, delay=0.1)
    async def unstable_fetch():
        if True:  # 模拟
            return "数据"
        raise ValueError("失败")
    
    result = asyncio.run(unstable_fetch())
    print(f"异步结果: {result}")
    
    # 测试5: 性能分析
    print("\n--- 测试: 性能分析 ---")
    
    @Profiler.profile
    def slow_task():
        time.sleep(0.01)
        return "完成"
    
    for _ in range(3):
        slow_task()
    
    Profiler.report()
    
    print("\n" + "=" * 50)
    print("装饰器实际应用学习完成!")
    print("=" * 50)