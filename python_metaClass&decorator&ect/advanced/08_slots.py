"""
第8章: __slots__ 优化与内存管理
=====================================

__slots__ 是Python中用于优化内存和限制属性创建的机制.
"""

from typing import Any, Dict


# ============== __slots__ 基础 ==============

class WithoutSlots:
    """不使用 __slots__ 的类"""
    
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age


class WithSlots:
    """使用 __slots__ 的类"""
    
    __slots__ = ['name', 'age']
    
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age


# ============== __slots__ 进阶 ==============

class Animal:
    """基类 - 定义通用属性"""
    
    __slots__ = ['name', 'age']
    
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age


class Dog(Animal):
    """子类 - 自动继承 __slots__"""
    
    __slots__ = ['breed']  # 添加新属性
    
    def __init__(self, name: str, age: int, breed: str):
        super().__init__(name, age)
        self.breed = breed


class Cat(Animal):
    """子类 - 没有 __slots__ 会恢复 __dict__"""
    
    # 如果不定义 __slots__, 会恢复 __dict__
    def __init__(self, name: str, age: int, color: str):
        super().__init__(name, age)
        self.color = color  # 可


# ============== 只读属性 ==============

class ReadOnlyPerson:
    """使用 __slots__ 实现只读属性"""
    
    __slots__ = ['_name', '_age']
    
    def __init__(self, name: str, age: int):
        self._name = name
        self._age = age
    
    @property
    def name(self):
        return self._name
    
    @property
    def age(self):
        return self._age


# ============== __slots__ 方法 ==============

class Point:
    """使用 __slots__ 加方法"""
    
    __slots__ = ['x', 'y']
    
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y
    
    def __repr__(self):
        return f"Point({self.x}, {self.y})"
    
    def __eq__(self, other):
        if not isinstance(other, Point):
            return False
        return self.x == other.x and self.y == other.y
    
    def distance(self):
        return (self.x ** 2 + self.y ** 2) ** 0.5


# ============== __slots__ 与属性验证 ==============

class ValidatedPoint:
    """使用 __slots__ 加验证"""
    
    __slots__ = ['_x', '_y']
    
    def __init__(self, x: float, y: float):
        if x < 0 or y < 0:
            raise ValueError("坐标不能为负")
        self._x = x
        self._y = y
    
    @property
    def x(self):
        return self._x
    
    @property
    def y(self):
        return self._y
    
    @x.setter
    def x(self, value):
        if value < 0:
            raise ValueError("x不能为负")
        self._x = value


# ============== __slots__ 与类方法 ==============

class Counter:
    """带类方法的 __slots__ 类"""
    
    __slots__ = ['_count']
    _total = 0  # 类变量
    
    def __init__(self):
        self._count = 0
    
    def increment(self):
        self._count += 1
        Counter._total += 1
    
    @classmethod
    def get_total(cls):
        return cls._total


# ============== __slots__ 与多重继承 ==============

class MixinA:
    """混入类A"""
    
    __slots__ = ['a']
    
    def method_a(self):
        return "A"


class MixinB:
    """混入类B"""
    
    __slots__ = []  # 避免冲突
    
    def method_b(self):
        return "B"


class Combined(MixinA, MixinB):
    """组合多个混入"""
    
    __slots__ = ['c']
    
    def method_c(self):
        return "C"


# ============== 测试运行 ==============

if __name__ == "__main__":
    import sys
    
    print("=" * 50)
    print("8. __slots__ 优化")
    print("=" * 50)
    
    # 测试1: 内存对比
    print("\n--- 测试: 内存对比 ---")
    obj1 = WithoutSlots("Alice", 30)
    obj2 = WithSlots("Bob", 25)
    
    print(f"WithoutSlots: {sys.getsizeof(obj1)} bytes + {sys.getsizeof(obj1.__dict__)} bytes")
    print(f"WithSlots: {sys.getsizeof(obj2)} bytes")
    
    # 检查是否有 __dict__
    print(f"\nWithoutSlots 有 __dict__: {hasattr(obj1, '__dict__')}")
    print(f"WithSlots 有 __dict__: {hasattr(obj2, '__dict__')}")
    
    # 测试2: __slots__ 继承
    print("\n--- 测试: __slots__ 继承 ---")
    dog = Dog("Buddy", 3, "Labrador")
    print(f"Dog: {dog.name}, {dog.age}, {dog.breed}")
    
    cat = Cat("Whiskers", 2, "orange")
    print(f"Cat: {cat.name}, {cat.age}, {cat.color}")
    print(f"Cat 有 __dict__: {hasattr(cat, '__dict__')}")
    
    # 测试3: 只读属性
    print("\n--- 测试: 只读属性 ---")
    person = ReadOnlyPerson("Alice", 30)
    print(f"name: {person.name}, age: {person.age}")
    try:
        person.name = "Bob"  # 只读,不能修改
    except AttributeError as e:
        print(f"错误: 只读属性不能修改")
    
    # 测试4: 方法
    print("\n--- 测试: 方法 ---")
    p1 = Point(3, 4)
    p2 = Point(3, 4)
    print(f"p1: {p1}, distance: {p1.distance()}")
    print(f"p1 == p2: {p1 == p2}")
    
    # 测试5: 验证
    print("\n--- 测试: 验证 ---")
    try:
        vp = ValidatedPoint(-1, 2)
    except ValueError as e:
        print(f"验证失败: {e}")
    
    vp = ValidatedPoint(3, 4)
    print(f"ValidPoint: {vp.x}, {vp.y}")
    
    # 测试6: 多重继承
    print("\n--- 测试: 多重继承 ---")
    obj = Combined()
    obj.a = 1
    obj.c = 3
    print(f"method_a: {obj.method_a()}")
    print(f"method_b: {obj.method_b()}")
    print(f"method_c: {obj.method_c()}")
    
    # 测试__slots__数量
    print(f"\nCombined __slots__: {Combined.__slots__}")
    
    print("\n" + "=" * 50)
    print("__slots__ 学习完成!")
    print("=" * 50)