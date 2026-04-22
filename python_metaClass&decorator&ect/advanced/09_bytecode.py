"""
第9章: 字节码操作与反汇编
=====================================

探索Python的底层字节码机制.
使用dis模块查看和分析字节码.
"""

import dis
import dis as bytecode
import opcode
import sys
import time


# ============== 查看字节码 ==============

def greet(name: str) -> str:
    """简单的问候函数"""
    message = "Hello, " + name + "!"
    return message


# ============== 生成器表达式字节码 ==============

def list_comprehension():
    """列表推导式"""
    return [x * 2 for x in range(10)]


def generator_expression():
    """生成器表达式"""
    return (x * 2 for x in range(10))


# ============== 闭包字节码 ==============

def outer():
    """外层函数"""
    count = 0
    
    def inner():
        """内层函数 - 闭包"""
        nonlocal count
        count += 1
        return count
    
    return inner


# ============== 类字节码 ==============

class MyClass:
    """测试类的字节码"""
    
    def __init__(self, value: int):
        self.value = value
    
    def method(self):
        return self.value * 2


# ============== 异步字节码 ==============

asyncio = None
try:
    import asyncio
except ImportError:
    pass

async def async_example():
    """异步函数"""
    if asyncio:
        await asyncio.sleep(0)
    return "async"


# ============== 自定义字节码操作 ==============

def custom_operation():
    """测试各种操作码"""
    a = 1
    b = 2
    c = a + b
    d = a * b
    e = a ** b
    f = a % b
    return c, d, e, f


# ============== 测试运行 ==============

if __name__ == "__main__":
    import dis
    import ast
    
    print("=" * 50)
    print("9. 字节码操作")
    print("=" * 50)
    
    # 测试1: 查看函数字节码
    print("\n--- 1. 简单函数字节码 ---")
    dis.dis(greet)
    
    # 测试2: 列表推导式 vs 生成器
    print("\n--- 2. 列表推导式 vs 生成器 ---")
    print("列表推导式:")
    dis.dis(list_comprehension)
    print("生成器表达式:")
    dis.dis(generator_expression)
    
    # 测试3: 闭包
    print("\n--- 3. 闭包字节码 ---")
    inner_func = outer()
    dis.dis(inner_func)
    
    # 测试4: 类方法
    print("\n--- 4. 类方法字节码 ---")
    print("__init__:")
    dis.dis(MyClass.__init__)
    print("method:")
    dis.dis(MyClass.method)
    
    # 测试5: 操作码表
    print("\n--- 5. 操作码信息 ---")
    print(f"Python版本: {sys.version}")
    print(f"操作码数量: {len(opcode.opname)}")
    
    # 显示一些常用操作码
    print("\n常用操作码:")
    for i, name in enumerate(opcode.opname[:20]):
        print(f"  {i}: {name}")
    
    # 测试6: 字节码分析
    print("\n--- 6. 分析字节码 ---")
    code = compile("1 + 2", "<string>", "eval")
    dis.dis(code)
    
    # 测试7: 查看AST
    print("\n--- 7. AST节点 ---")
    tree = ast.parse("x = 1 + 2")
    print(ast.dump(tree))
    
    # 测试8: 协程
    print("\n--- 8. 协程字节码 ---")
    
    async def simple_async():
        return 42
    
    dis.dis(simple_async)
    
    # 测试9: 高级操作
    print("\n--- 9. 高级操作 ---")
    
    def fib_fast(n: int) -> int:
        """快速斐波那契"""
        a, b = 0, 1
        for _ in range(n):
            a, b = b, a + b
        return b
    
    dis.dis(fib_fast)
    
    # 测试10: 反汇编其他可调用对象
    print("\n--- 10. Lambda字节码 ---")
    add = lambda x, y: x + y
    dis.dis(add)
    
    print("\n" + "=" * 50)
    print("字节码操作学习完成!")
    print("=" * 50)