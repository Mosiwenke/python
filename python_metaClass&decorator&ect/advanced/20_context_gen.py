"""
第20章: 上下文管理器与生成器
=============================

Python上下文管理器和生成器的高级用法.
- 上下文管理器
- 生成器
- yield表达式
- itertools
"""

from contextlib import contextmanager, closing, suppress
import sys
import itertools
from typing import Iterator, Generator, Any, Callable


# ============== 上下文管理器基础 ==============

class FileManager:
    """文件管理器"""
    
    def __init__(self, filename: str, mode: str = "r"):
        self.filename = filename
        self.mode = mode
        self.file = None
    
    def __enter__(self):
        self.file = open(self.filename, self.mode)
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.file:
            self.file.close()
        return False


def context_manager_demo():
    """上下文管理器演示"""
    with FileManager("test.txt", "w") as fm:
        fm.file.write("Hello")
        print("写入成功")


# ============== contextmanager装饰器 ==============

@contextmanager
def managed_resource(name: str):
    """使用contextmanager"""
    print(f"获取资源: {name}")
    try:
        yield f"resource-{name}"
    finally:
        print(f"释放资源: {name}")


def contextmanager_demo():
    """contextmanager演示"""
    with managed_resource("test") as resource:
        print(f"使用: {resource}")


# ============== closing ==============

def closing_demo():
    """closing演示"""
    class Resource:
        def close(self):
            print("资源已关闭")
    
    with closing(Resource()) as res:
        print("使用资源")


# ============== suppress ==============

def suppress_demo():
    """suppress演示"""
    with suppress(FileNotFoundError):
        open("nonexistent.txt").read()
    print("异常被忽略")


# ============== 生成器基础 ==============

def simple_generator():
    """简单生成器"""
    yield 1
    yield 2
    yield 3


def generator_demo():
    """生成器演示"""
    gen = simple_generator()
    print(f"next: {next(gen)}")
    print(f"next: {next(gen)}")
    print(f"next: {next(gen)}")
    
    for i in simple_generator():
        print(f"yield: {i}")


# ============== 生成器函数 ==============

def fibonacci(n: int) -> Generator[int, None, None]:
    """斐波那契生成器"""
    a, b = 0, 1
    for _ in range(n):
        yield b
        a, b = b, a + b


def fib_demo():
    """斐波那契演示"""
    for i in fibonacci(10):
        print(i, end=" ")
    print()


# ============== yield from ==============

def chain_gen(*iterables):
    """链接生成器"""
    for it in iterables:
        yield from it


def yield_from_demo():
    """yield from演示"""
    result = list(chain_gen([1, 2], [3, 4], [5, 6]))
    print(f"链接: {result}")


# ============== 生成器表达式 ==============

def gen_expression_demo():
    """生成器表达式演示"""
    gen = (x * 2 for x in range(5))
    print(f"生成器: {list(gen)}")
    
    gen2 = (x for x in range(10) if x % 2 == 0)
    print(f"偶数: {list(gen2)}")


# ============== itertools ==============

def itertools_demo():
    """itertools演示"""
    print("count:")
    for i in itertools.count(5, 2):
        if i > 15:
            break
        print(i, end=" ")
    print()
    
    print("cycle:")
    cycle = itertools.cycle([1, 2, 3])
    for _ in range(8):
        print(next(cycle), end=" ")
    print()
    
    print("repeat:")
    repeated = itertools.repeat(42, 3)
    print(list(repeated))
    
    print("chain:")
    chained = itertools.chain([1, 2], [3, 4])
    print(list(chained))
    
    print("islice:")
    sliced = itertools.islice(range(10), 2, 8, 2)
    print(list(sliced))
    
    print("takewhile:")
    taken = itertools.takewhile(lambda x: x < 5, itertools.count())
    print(list(taken))
    
    print("dropwhile:")
    dropped = itertools.dropwhile(lambda x: x < 5, [1, 2, 6, 7, 8])
    print(list(dropped))
    
    print("filterfalse:")
    filtered = itertools.filterfalse(lambda x: x % 2 == 0, range(5))
    print(list(filtered))
    
    print("groupby:")
    for key, group in itertools.groupby("aaabbbcc"):
        print(f"{key}: {list(group)}")
    
    print("compress:")
    compressed = itertools.compress([1, 2, 3, 4], [1, 0, 1, 0])
    print(list(compressed))


# ============== 无限生成器 ==============

def infinite_generator():
    """无限生成器"""
    n = 0
    while True:
        yield n
        n += 1


def infinite_demo():
    """无限生成器演示"""
    gen = infinite_generator()
    print("前5个:")
    for _ in range(5):
        print(next(gen), end=" ")


# ============== 生成器发送值 ==============

def coroutine():
    """协程 - 可接收值"""
    while True:
        value = yield
        print(f"接收: {value}")


def send_demo():
    """send演示"""
    co = coroutine()
    next(co)
    
    co.send(1)
    co.send(2)
    co.send(3)
    co.close()


# ============== 生成器.throw() ==============

def gen_with_throw():
    """带异常的生成器"""
    try:
        yield 1
        yield 2
    except ValueError as e:
        yield f"异常: {e}"


def throw_demo():
    """throw演示"""
    gen = gen_with_throw()
    print(next(gen))
    print(gen.throw(ValueError, "错误信息"))
    try:
        next(gen)
    except StopIteration:
        print("完成")


# ============== 生成器.close() ==============

def close_demo():
    """close演示"""
    def gen():
        try:
            yield 1
        except GeneratorExit:
            print("生成器关闭")
    
    g = gen()
    next(g)
    g.close()
    print("已关闭")


# ============== 委托生成器 ==============

def delegating_gen():
    """委托生成器"""
    yield from range(3)
    yield from "abc"


def delegating_demo():
    """委托演示"""
    print(list(delegating_gen()))


# ============== 管道生成器 ==============

def pipeline():
    """管道生成器"""
    def source():
        for i in range(10):
            yield i
    
    def filter_even():
        for x in source():
            if x % 2 == 0:
                yield x
    
    def multiply():
        for x in filter_even():
            yield x * 2
    
    return list(multiply())


def pipeline_demo():
    """管道演示"""
    print(f"管道结果: {pipeline()}")


# ============== 测试运行 ==============

if __name__ == "__main__":
    print("=" * 50)
    print("20. 上下文管理器与生成器")
    print("=" * 50)
    
    # 测试1: 上下文管理器
    print("\n--- 1. 上下文管理器 ---")
    contextmanager_demo()
    
    # 测试2: closing
    print("\n--- 2. closing ---")
    closing_demo()
    
    # 测试3: suppress
    print("\n--- 3. suppress ---")
    suppress_demo()
    
    # 测试4: 生成器
    print("\n--- 4. 生成器 ---")
    generator_demo()
    
    # 测试5: 斐波那契
    print("\n--- 5. 斐波那契 ---")
    fib_demo()
    
    # 测试6: yield from
    print("\n--- 6. yield from ---")
    yield_from_demo()
    
    # 测试7: 生成器表达式
    print("\n--- 7. 生成器表达式 ---")
    gen_expression_demo()
    
    # 测试8: itertools
    print("\n--- 8. itertools ---")
    itertools_demo()
    
    # 测试9: 无限生成器
    print("\n--- 9. 无限生成器 ---")
    infinite_demo()
    
    # 测试10: send
    print("\n--- 10. 发送值 ---")
    send_demo()
    
    # 测试11: throw
    print("\n--- 11. throw ---")
    throw_demo()
    
    # 测试12: close
    print("\n--- 12. close ---")
    close_demo()
    
    # 测试13: 委托
    print("\n--- 13. 委托生成器 ---")
    delegating_demo()
    
    # 测试14: 管道
    print("\n--- 14. 管道 ---")
    pipeline_demo()
    
    print("\n" + "=" * 50)
    print("上下文管理器与生成器学习完成!")
    print("=" * 50)