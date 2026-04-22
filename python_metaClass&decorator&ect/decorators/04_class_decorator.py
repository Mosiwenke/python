"""
第4章: 类方式的装饰器
=====================

使用类来实现装饰器,利用Python的__call__方法.
这种方式可以保存状态,比函数装饰器更灵活.

关键技术:
- __call__: 让类的实例可调用
- __get__: 实现描述符协议
- 状态保存
"""

from functools import wraps
from typing import Callable, Any
import time


# ============== 类装饰器基础 ==============

class MyDecorator:
    """
    类装饰器 - 通过类的__call__方法实现
    
    优势:
    - 可以保存状态
    - 可以配置参数
    - 更面向对象的设计
    """
    
    def __init__(self, func: Callable):
        """在装饰时保存原函数"""
        self.func = func
        self.call_count = 0
        
        # 使用wraps保持元信息
        self.__wrapped__ = func
        self.__name__ = func.__name__
        self.__doc__ = func.__doc__
    
    def __call__(self, *args, **kwargs):
        """调用时执行包装逻辑"""
        self.call_count += 1
        print(f"[MyDecorator] 第{self.call_count}次调用: {self.__name__}")
        
        start = time.perf_counter()
        result = self.func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        
        print(f"[MyDecorator] 执行耗时: {elapsed:.4f}秒")
        return result


@MyDecorator
def my_function():
    """被装饰的函数"""
    time.sleep(0.05)
    return "完成"


# ============== 可配置参数的类装饰器 ==============

class TimedRetry:
    """
    可配置参数的类装饰器
    
    参数:
        times: 重试次数
        delay: 重试间隔(秒)
    """
    
    def __init__(self, times: int = 3, delay: float = 1.0):
        self.times = times
        self.delay = delay
    
    def __call__(self, func: Callable):
        """返回一个新的包装函数"""
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_error = None
            
            for attempt in range(1, self.times + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_error = e
                    if attempt < self.times:
                        print(f"[TimedRetry] 第{attempt}次失败, {self.delay}秒后重试...")
                        time.sleep(self.delay)
            
            raise last_error
        
        return wrapper


@TimedRetry(times=3, delay=0.5)
def unstable_api(should_fail: bool = False) -> str:
    """模拟不稳定的API"""
    import random
    if should_fail or random.random() < 0.5:
        raise ConnectionError("网络不稳定")
    return "API响应"


# ============== 计数器装饰器 ==============

class Counter:
    """
    计数装饰器 - 统计函数调用次数
    """
    
    _global_counts = {}  # 类变量,所有实例共享
    
    def __init__(self, name: str = None):
        self.name = name
    
    def __call__(self, func: Callable) -> Callable:
        self._global_counts[func.__name__] = 0
        
        @wraps(func)
        def wrapper(*args, **kwargs):
            self._global_counts[func.__name__] += 1
            return func(*args, **kwargs)
        
        # 添加获取计数的方法
        wrapper.get_count = lambda: self._global_counts[func.__name__]
        wrapper.reset = lambda: self._global_counts.update({func.__name__: 0})
        
        return wrapper


@Counter("api_calls")
def call_api():
    return "响应"


# ============== 缓存装饰器 (类实现) ==============

class Cache:
    """
    缓存装饰器 - 使用类实现可以更灵活地管理缓存
    
    特性:
    - 可以清除特定缓存
    - 可以查看缓存信息
    - 可以设置过期时间
    """
    
    def __init__(self, ttl: float = None):
        """
        参数:
            ttl: 缓存过期时间(秒), None表示永不过期
        """
        self.ttl = ttl
        self._cache = {}
        self._timestamps = {}
    
    def __call__(self, func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            key = str(args) + str(kwargs)
            now = time.time()
            
            # 检查缓存
            if key in self._cache:
                # 检查过期
                if self.ttl is None or now - self._timestamps[key] < self.ttl:
                    print(f"[Cache] 命中缓存: {key}")
                    return self._cache[key]
                else:
                    print(f"[Cache] 缓存过期: {key}")
            
            # 执行并缓存
            result = func(*args, **kwargs)
            self._cache[key] = result
            self._timestamps[key] = now
            print(f"[Cache] 新增缓存: {key}")
            
            return result
        
        # 清除缓存方法
        wrapper.clear = lambda: (
            self._cache.clear(), 
            self._timestamps.clear()
        )
        
        # 获取缓存信息
        wrapper.info = lambda: {
            "size": len(self._cache),
            "keys": list(self._cache.keys())
        }
        
        return wrapper


@Cache(ttl=2)
def get_weather(city: str) -> str:
    """模拟天气API"""
    time.sleep(0.1)
    import random
    weathers = ["晴", "多云", "雨"]
    return f"{city}: {random.choice(weathers)}"


# ============== 状态机装饰器 ==============

class StateMachine:
    """
    状态机装饰器 - 控制函数调用状态
    
    可以定义状态转换规则
    """
    
    def __init__(self, initial: str, transitions: dict):
        """
        参数:
            initial: 初始状态
            transitions: 状态转换规则
            {
                "start": ["running"],
                "running": ["finished", "failed"],
                ...
            }
        """
        self.state = initial
        self.transitions = transitions
        self.history = [initial]
    
    def __call__(self, func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            # 这里简化: 假设调用会改变到下一个状态
            allowed = self.transitions.get(self.state, [])
            
            if not allowed:
                raise RuntimeError(
                    f"状态 {self.state} 不允许任何转换"
                )
            
            result = func(*args, **kwargs)
            
            # 假设返回的状态名
            if isinstance(result, str):
                new_state = result
                if new_state in allowed:
                    self.state = new_state
                    self.history.append(new_state)
                    print(f"[StateMachine] 状态转换: {self.history[-2]} -> {new_state}")
                else:
                    raise RuntimeError(
                        f"不允许的转换: {self.state} -> {new_state}"
                    )
            
            return result
        
        wrapper.get_state = lambda: self.state
        wrapper.get_history = lambda: self.history.copy()
        
        return wrapper


@StateMachine(
    initial="idle",
    transitions={
        "idle": ["running"],
        "running": ["success", "failed"],
        "success": ["idle"],
        "failed": ["idle"]
    }
)
def process_task() -> str:
    """模拟任务处理"""
    return "success"


# ============== 节流装饰器 (类实现) ==============

class Throttle:
    """
    节流装饰器 - 限制函数调用频率
    
    参数:
        min_interval: 最小调用间隔(秒)
    """
    
    def __init__(self, min_interval: float):
        self.min_interval = min_interval
        self.last_call = 0
    
    def __call__(self, func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            now = time.time()
            
            if now - self.last_call < self.min_interval:
                wait = self.min_interval - (now - self.last_call)
                print(f"[Throttle] 节流中, 等待 {wait:.2f}秒")
                time.sleep(wait)
            
            self.last_call = time.time()
            return func(*args, **kwargs)
        
        return wrapper


@Throttle(min_interval=1.0)
def throttled_api():
    return "API响应"


# ============== 测试运行 ==============

if __name__ == "__main__":
    print("=" * 50)
    print("4. 类方式的装饰器")
    print("=" * 50)
    
    # 测试1: 类装饰器基础
    print("\n--- 测试: MyDecorator ---")
    my_function()
    my_function()
    print(f"调用次数: {my_function.call_count}")
    
    # 测试2: 可配置参数
    print("\n--- 测试: TimedRetry ---")
    for _ in range(5):
        try:
            result = unstable_api(should_fail=False)
            print(f"成功: {result}")
            break
        except ConnectionError:
            print("失败,重试...")
    
    # 测试3: 计数器
    print("\n--- 测试: Counter ---")
    call_api()
    call_api()
    print(f"调用次数: {call_api.get_count()}")
    
    # 测试4: 缓存
    print("\n--- 测试: Cache ---")
    print(get_weather("北京"))
    print(get_weather("北京"))
    time.sleep(2.5)  # 等待缓存过期
    print(get_weather("北京"))
    print(f"缓存信息: {get_weather.info()}")
    
    # 测试5: 节流
    print("\n--- 测试: Throttle ---")
    throttled_api()
    throttled_api()  # 会等待
    
    print("\n" + "=" * 50)
    print("类方式装饰器学习完成!")
    print("=" * 50)