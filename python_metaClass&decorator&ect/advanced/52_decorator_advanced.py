"""
第52章: 装饰器模式与实现
=============================

装饰器深入实现.
- 类装饰器
- 函数装饰器
- 装饰器参数
- 堆叠
"""

from functools import wraps


def simple_decorator(func):
    """简单装饰器"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        print("before")
        result = func(*args, **kwargs)
        print("after")
        return result
    return wrapper


@simple_decorator
def greet():
    print("greet!")


def param_decorator(prefix):
    """参数化装饰器"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            print(f"{prefix}: ", end="")
            return func(*args, **kwargs)
        return wrapper
    return decorator


@param_decorator("INFO")
def say():
    print("say something")


def class_decorator(cls):
    """类装饰器"""
    original_init = cls.__init__
    
    @wraps(original_init)
    def new_init(self, *args, **kwargs):
        print(f"init {cls.__name__}")
        original_init(self, *args, **kwargs)
    
    cls.__init__ = new_init
    return cls


@class_decorator
class MyClass:
    def __init__(self): pass


def stack_decorators():
    """装饰器堆叠"""
    def deco1(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            print("1")
            return f(*args, **kwargs)
        return wrapper
    
    def deco2(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            print("2")
            return f(*args, **kwargs)
        return wrapper
    
    @deco1
    @deco2
    def func(): print("func")
    
    func()


def method_decorator():
    """方法装饰器"""
    class Decorator:
        def __init__(self, func):
            self.func = func
            wraps(func)(self)
        
        def __call__(self, *args, **kwargs):
            return self.func(*args, **kwargs)
        
        def __get__(self, obj, cls):
            return wraps(self.func)(lambda *a, **kw: self(obj, *a, **kw))
    
    class MyClass:
        @Decorator
        def method(self): return "method"
    
    obj = MyClass()
    print(f"call: {obj.method()}")


if __name__ == "__main__":
    print("=" * 50)
    print("52. 装饰器深入")
    print("=" * 50)
    print("--- simple ---")
    greet()
    print("--- param ---")
    say()
    print("--- class ---")
    obj = MyClass()
    print("--- stack ---")
    stack_decorators()
    print("--- method ---")
    method_decorator()
    print("=" * 50)