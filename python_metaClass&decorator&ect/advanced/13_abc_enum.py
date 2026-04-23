"""
第13章: abc.ABCMeta 抽象类与enum源码分析
==========================================

深入分析Python标准库中元编程的实际应用.
- abc模块: 抽象基类的实现原理
- enum模块: 枚举类型的实现原理
"""

import abc
import enum
import sys
from typing import Any, Type


# ============== abc模块原理分析 ==============

class AbstractBaseMeta(abc.ABCMeta):
    """
    分析ABCMeta的实现
    
    ABCMeta主要功能:
    1. 注册虚拟子类
    2. 检查抽象方法
    3. 抽象属性
    """
    
    def __new__(mcs, name, bases, namespace):
        cls = super().__new__(mcs, name, bases, namespace)
        return cls


class BaseAnimal(metaclass=AbstractBaseMeta):
    """抽象动物类"""
    
    @abc.abstractmethod
    def sound(self) -> str:
        """发出声音"""
        pass
    
    @property
    @abc.abstractmethod
    def name(self) -> str:
        """动物名称"""
        pass


class Dog(BaseAnimal):
    """狗实现"""
    
    def __init__(self, name: str):
        self._name = name
    
    def sound(self) -> str:
        return "汪!"
    
    @property
    def name(self) -> str:
        return self._name


class Cat(BaseAnimal):
    """猫实现"""
    
    def __init__(self, name: str):
        self._name = name
    
    def sound(self) -> str:
        return "喵!"
    
    @property
    def name(self) -> str:
        return self._name


# ============== 虚拟子类注册 ==============

class SimpleBase:
    """简单基类"""
    
    def process(self):
        return "processed"


class VirtualSubclass(SimpleBase):
    """被注册的虚拟子类"""
    
    def process(self):
        return "virtual processed"


AbstractBase = abc.ABCMeta('AbstractBase', (SimpleBase,), {})
AbstractBase.register(VirtualSubclass)


# ============== 抽象属性 ==============

class AbstractProperty(metaclass=abc.ABCMeta):
    """抽象属性示例"""
    
    @abc.abstractproperty
    def value(self) -> Any:
        pass


class ConcreteProperty:
    """具体实现"""
    
    def __init__(self, value: Any):
        self._value = value
    
    @property
    def value(self) -> Any:
        return self._value


# ============== 抽象类装饰器 ==============

def abstract_method(func):
    """自定义抽象方法装饰器"""
    return abc.abstractmethod(func)


class AbstractInterface(metaclass=abc.ABCMeta):
    """使用自定义抽象方法"""
    
    @abstract_method
    def execute(self):
        pass


# ============== enum模块原理分析 ==============

class EnumMeta(type):
    """
    分析EnumMeta的实现
    
    EnumMeta主要功能:
    1. 自动枚举成员
    2. 枚举迭代
    3. 枚举比较
    4. 枚举属性
    """
    
    _enum_names: tuple = ()
    _enum_values: dict = {}
    
    def __new__(mcs, name, bases, namespace, **kwargs):
        enum_names = kwargs.get('_enum_names', ())
        enum_values = kwargs.get('_enum_values', {})
        
        cls = super().__new__(mcs, name, bases, namespace)
        return cls
    
    def __getitem__(cls, member):
        return getattr(cls, member)
    
    def __iter__(cls):
        return iter(cls.__members__.values())
    
    def __len__(cls):
        return len(cls.__members__)


class Color(enum.Enum):
    """颜色枚举"""
    RED = 1
    GREEN = 2
    BLUE = 3


class Status(enum.Enum):
    """状态枚举"""
    PENDING = 'pending'
    ACTIVE = 'active'
    COMPLETED = 'completed'


# ============== IntEnum ==============

class Priority(enum.IntEnum):
    """整数枚举"""
    LOW = 1
    MEDIUM = 5
    HIGH = 10


# ============== Flag ==============

class Permission(enum.Flag):
    """权限标志"""
    READ = enum.auto()
    WRITE = enum.auto()
    EXECUTE = enum.auto()


# ============== 自定义枚举 ==============

class OrderedEnum(enum.Enum):
    """带顺序的枚举"""
    
    def __lt__(self, other):
        if isinstance(other, OrderedEnum):
            return self.value < other.value
        return NotImplemented


class Grade(OrderedEnum):
    """成绩等级"""
    A = 95
    B = 85
    C = 75
    D = 65
    F = 0


# ============== 枚举功能演示 ==============

class AutoName(enum.Enum):
    """自动名称枚举"""
    
    @property
    def description(self):
        return f"描述: {self.name}"


class Direction(AutoName):
    """方向"""
    NORTH = 'north'
    SOUTH = 'south'
    EAST = 'east'
    WEST = 'west'


# ============== 扩展枚举 ==============

class CustomEnum(enum.Enum):
    """自定义枚举方法"""
    
    def is_active(self):
        return self.name != 'INACTIVE'
    
    @classmethod
    def list_all(cls):
        return [m.name for m in cls]


class State(CustomEnum):
    """状态"""
    ACTIVE = 1
    INACTIVE = 0


# ============== 符号名与值映射 ==============

class SymbolEnum(enum.Enum):
    """符号名称映射"""
    
    @property
    def symbol(self):
        symbols = {
            'PLUS': '+',
            'MINUS': '-',
            'MULTIPLY': '*',
            'DIVIDE': '/',
        }
        return symbols.get(self.name, '')


class Operator(SymbolEnum):
    """运算符"""
    PLUS = 1
    MINUS = 2
    MULTIPLY = 3
    DIVIDE = 4


# ============== 测试运行 ==============

if __name__ == "__main__":
    print("=" * 50)
    print("13. abc与enum模块分析")
    print("=" * 50)
    
    # 测试1: 抽象类
    print("\n--- 1. 抽象类 ---")
    dog = Dog("旺财")
    print(f"狗: {dog.name} -> {dog.sound()}")
    
    cat = Cat("咪咪")
    print(f"猫: {cat.name} -> {cat.sound()}")
    
    # 测试2: 抽象属性
    print("\n--- 2. 抽象属性 ---")
    prop = ConcreteProperty(42)
    print(f"value: {prop.value}")
    
    # 测试3: 枚举基本用法
    print("\n--- 3. 枚举 ---")
    print(f"Color.RED: {Color.RED}")
    print(f"Color.RED.value: {Color.RED.value}")
    print(f"Color.RED.name: {Color.RED.name}")
    print(f"Color['RED']: {Color['RED']}")
    print(f"Color(1): {Color(1)}")
    
    # 测试4: 枚举迭代
    print("\n--- 4. 枚举迭代 ---")
    for color in Color:
        print(f"  {color.name} = {color.value}")
    
    # 测试5: IntEnum
    print("\n--- 5. IntEnum ---")
    priority = Priority.HIGH
    print(f"Priority.HIGH: {priority}")
    print(f"Priority.HIGH > Priority.LOW: {priority > Priority.LOW}")
    print(f"Priority.HIGH + 5: {priority + 5}")
    
    # 测试6: Flag
    print("\n--- 6. Flag ---")
    perm = Permission.READ | Permission.WRITE
    print(f"READ | WRITE: {perm}")
    print(f"READ in perm: {Permission.READ in perm}")
    
    # 测试7: 自定义枚举方法
    print("\n--- 7. 自定义枚举 ---")
    print(f"State.ACTIVE.is_active(): {State.ACTIVE.is_active()}")
    print(f"State.list_all(): {State.list_all()}")
    
    # 测试8: 符号枚举
    print("\n--- 8. 符号枚举 ---")
    op = Operator.PLUS
    print(f"Operator.PLUS.symbol: {op.symbol}")
    
    # 测试9: 枚举成员比较
    print("\n--- 9. 枚举比较 ---")
    print(f"Color.RED is Color.RED: {Color.RED is Color.RED}")
    print(f"Color.RED == Color.RED: {Color.RED == Color.RED}")
    
    # 测试10: 枚举dict
    print("\n--- 10. 枚举成员字典 ---")
    print(f"Color.__members__: {Color.__members__}")
    
    print("\n" + "=" * 50)
    print("abc与enum模块学习完成!")
    print("=" * 50)