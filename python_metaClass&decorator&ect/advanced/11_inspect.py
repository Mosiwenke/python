"""
第11章: inspect模块高级用法 & 代码自省
=========================================

inspect模块用于获取Python对象的信息.
是元编程和调试工具的核心.
"""

import inspect
import dis
import os
import sys
import types
from typing import Callable, List, Any, Optional


# ============== 获取函数信息 ==============

def inspect_function():
    """检查函数信息"""
    
    def greet(name: str, greeting: str = "Hello") -> str:
        """问候函数"""
        return f"{greeting}, {name}!"
    
    print(f"函数名: {greet.__name__}")
    print(f"__name__: {greet.__name__}")
    print(f"__doc__: {greet.__doc__}")
    print(f"__module__: {greet.__module__}")
    print(f"__defaults__: {greet.__defaults__}")
    print(f"__code__: {greet.__code__}")
    
    # 签名
    sig = inspect.signature(greet)
    print(f"签名: {sig}")
    print(f"参数:")
    for name, param in sig.parameters.items():
        print(f"  {name}: default={param.default}, annotation={param.annotation}")


# ============== 获取类信息 ==============

def inspect_class():
    """检查类信息"""
    
    class Person:
        """人类"""
        
        def __init__(self, name: str, age: int):
            self.name = name
            self.age = age
        
        def greet(self) -> str:
            return f"Hello, I'm {self.name}"
        
        @classmethod
        def create(cls, name: str) -> 'Person':
            return cls(name, 0)
        
        @staticmethod
        def utility():
            return "utility"
    
    print(f"类名: {Person.__name__}")
    print(f"__doc__: {Person.__doc__}")
    print(f"__module__: {Person.__module__}")
    
    # 方法
    print(f"\n方法:")
    for name, method in inspect.getmembers(Person, predicate=inspect.ismethod):
        if not name.startswith('_'):
            print(f"  {name}")
    
    # 属性
    print(f"\n属性:")
    for name, attr in inspect.getmembers(Person, predicate=inspect.isclass):
        print(f"  {name}")


# ============== 获取源代码 ==============

def get_source():
    """获取源代码"""
    
    def example():
        # 示例函数
        x = 1
        y = 2
        return x + y
    
    try:
        source = inspect.getsource(example)
        print("源代码:")
        print(source)
    except TypeError as e:
        print(f"无法获取: {e}")
    
    # 获取定义源代码的行号
    lines, start = inspect.getsourcelines(example)
    print(f"\n行号: {start}")
    print(f"行数: {len(lines)}")


# ============== 获取模块信息 ==============

def get_module_info():
    """获取模块信息"""
    
    # 当前模块
    current = inspect.getmodule(inspect)
    print(f"当前模块: {current}")
    
    # 模块文件
    print(f"模块文件: {inspect.getfile(inspect)}")
    
    # 内置模块
    print(f"\n内置模块:")
    for name in ['os', 'sys', 'dis'][:3]:
        mod = sys.modules.get(name)
        if mod:
            print(f"  {name}: {inspect.getfile(mod)}")


# ============== 签名操作 ==============

def signature_operations():
    """签名操作"""
    
    def math_op(a: int, b: int, *, power: int = 1) -> int:
        return (a + b) ** power
    
    sig = inspect.signature(math_op)
    
    # 绑定参数
    bound = sig.bind(2, 3, power=2)
    print(f"绑定参数: {bound.arguments}")
    
    # 应用默认值
    bound.apply_defaults()
    print(f"应用默认值: {bound.arguments}")
    
    # 调用
    result = sig.bind(**bound.arguments)
    print(f"调用: {result}")
    
    # 交换参数
    new_sig = sig.replace(parameters=[
        sig.parameters['b'],
        sig.parameters['a'],
        sig.parameters['power'],
    ])
    print(f"交换后签名: {new_sig}")


# ============== 类的自省 ==============

def class_introspection():
    """类自省"""
    
    class Base:
        def method(self):
            pass
    
    class Derived(Base):
        def method(self):
            pass
    
    # MRO
    print(f"MRO: {inspect.getmro(Derived)}")
    
    # 基类
    print(f"基类: {Derived.__bases__}")
    
    # 成员
    print(f"\n成员:")
    for name in dir(Derived):
        if not name.startswith('_'):
            obj = getattr(Derived, name)
            print(f"  {name}: {type(obj).__name__}")


# ============== 帧和跟踪 ==============

def frame_operations():
    """帧操作"""
    
    def level1():
        return inspect.currentframe()
    
    def level2():
        frame = level1()
        print(f"帧: {frame}")
        print(f"文件名: {frame.f_code.co_filename}")
        print(f"行号: {frame.f_lineno}")
        print(f"局部变量: {list(frame.f_locals.keys())}")
        
        # 调用栈
        stack = inspect.getouterframes(frame)
        print(f"\n调用栈:")
        for frame_info in stack:
            print(f"  {frame_info.function}: line {frame_info.lineno}")
    
    level2()


# ============== 生成器检查 ==============

def generator_info():
    """检查生成器"""
    
    def gen():
        yield 1
        yield 2
        yield 3
    
    g = gen()
    
    print(f"是否是生成器: {inspect.isgenerator(g)}")
    print(f"是否是生成器函数: {inspect.isgeneratorfunction(gen)}")
    print(f"下一步: {next(g)}")
    print(f"下一步: {next(g)}")
    print(f"GI_FRAME: {g.gi_frame}")
    print(f"GI_CODE: {g.gi_code}")


# ============== 协程检查 ==============

def coroutine_info():
    """检查协程"""
    
    async def async_func():
        return 42
    
    print(f"是否是协程函数: {inspect.iscoroutinefunction(async_func)}")
    
    # asyncio.iscoroutinefunction
    import asyncio
    print(f"asyncio.iscoroutinefunction: {asyncio.iscoroutinefunction(async_func)}")


# = ============= = 测试运行 = ============= =

if __name__ == "__main__":
    print("=" * 50)
    print("11. inspect模块高级用法")
    print("=" * 50)
    
    # 测试1: 函数信息
    print("\n--- 1. 函数信息 ---")
    inspect_function()
    
    # 测试2: 类信息
    print("\n--- 2. 类信息 ---")
    inspect_class()
    
    # 测试3: 源代码
    print("\n--- 3. 源代码 ---")
    get_source()
    
    # 测试4: 签名操作
    print("\n--- 4. 签名操作 ---")
    signature_operations()
    
    # 测试5: 类自省
    print("\n--- 5. 类自省 ---")
    class_introspection()
    
    # 测试6: 帧操作
    print("\n--- 6. 帧操作 ---")
    frame_operations()
    
    # 测试7: 生成器
    print("\n--- 7. 生成器 ---")
    generator_info()
    
    # 测试8: 协程
    print("\n--- 8. 协程 ---")
    coroutine_info()
    
    print("\n" + "=" * 50)
    print("inspect模块学习完成!")
    print("=" * 50)