"""
第15章: typing模块泛型与协议
==============================

Python类型提示系统的高级用法.
- 泛型
- 协议(Protocol)
- 类型别名
- 类型守卫
"""
from typing import (
    TypeVar, Generic, Protocol, Callable, 
    Union, Optional, List, Dict, Set, Tuple,
    Any, Iterator, Iterable, Awaitable,
    runtime_checkable, TypedDict
)


# ============== 泛型基础 ==============

T = TypeVar('T')
U = TypeVar('U')


class Container(Generic[T]):
    """泛型容器"""
    
    def __init__(self, value: T):
        self.value = value
    
    def get(self) -> T:
        return self.value


def generic_demo():
    """泛型演示"""
    int_container = Container(42)
    str_container = Container("hello")
    
    print(f"int: {int_container.get()}")
    print(f"str: {str_container.get()}")


# ============== 多类型参数 ==============

class Pair(Generic[T, U]):
    """多类型参数"""
    
    def __init__(self, first: T, second: U):
        self.first = first
        self.second = second
    
    def to_tuple(self) -> Tuple[T, U]:
        return (self.first, self.second)


def multi_type_demo():
    """多类型演示"""
    pair = Pair(1, "one")
    print(f"pair: {pair.to_tuple()}")


# ============== 泛型函数 ==============

def first_element(items: Iterable[T]) -> Optional[T]:
    """获取第一个元素"""
    for item in items:
        return item
    return None


def generic_func_demo():
    """泛型函数演示"""
    print(f"list: {first_element([1, 2, 3])}")
    print(f"str: {first_element('hello')}")
    print(f"empty: {first_element([])}")


# ============== 协议基础 ==============

class Sized(Protocol):
    """大小协议"""
    def __len__(self) -> int: ...


class Drawable(Protocol):
    """可绘制协议"""
    def draw(self) -> None: ...


class Circle:
    """圆形"""
    
    def __init__(self, radius: float):
        self.radius = radius
    
    def __len__(self):
        return 1
    
    def draw(self):
        print(f"绘制圆形: 半径{self.radius}")


class Square:
    """方形"""
    
    def __init__(self, side: float):
        self.side = side
    
    def draw(self):
        print(f"绘制方形: 边长{self.side}")


def draw_all(items: List[Drawable]):
    """绘制所有图形"""
    for item in items:
        item.draw()


def protocol_demo():
    """协议演示"""
    draw_all([Circle(1.0), Square(2.0)])


# ============== 运行时协议 ==============

@runtime_checkable
class Comparable(Protocol):
    """可比较协议"""
    def __eq__(self, other: object) -> bool: ...


class Point:
    """点"""
    
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Point):
            return NotImplemented
        return self.x == other.x and self.y == other.y


def runtime_checkable_demo():
    """运行时协议演示"""
    p1 = Point(1, 2)
    p2 = Point(1, 2)
    p3 = Point(3, 4)
    
    print(f"p1 == p2: {p1 == p2}")
    print(f"isinstance: {isinstance(p1, Comparable)}")


# ============== 泛型约束 ==============

CT = TypeVar('CT', bound='Comparable')


def find_max(items: List[CT]) -> Optional[CT]:
    """找最大值"""
    if not items:
        return None
    max_item = items[0]
    for item in items[1:]:
        if item > max_item:
            max_item = item
    return max_item


# ============== 类型别名 ==============

IntList = List[int]
StrDict = Dict[str, str]
Matrix = List[List[float]]


def process_list(items: IntList) -> IntList:
    """处理整数列表"""
    return [x * 2 for x in items]


NewMatrix = Tuple[IntList, ...]


def type_alias_demo():
    """类型别名演示"""
    matrix: Matrix = [[1.0, 2.0], [3.0, 4.0]]
    print(f"matrix: {matrix}")
    
    result = process_list([1, 2, 3])
    print(f"result: {result}")


# ============== Union和Optional ==============

def process_value(value: Union[int, str, float]) -> str:
    """处理多种类型"""
    return f"值: {value}"


def optional_demo():
    """Optional演示"""
    result = process_value(42)
    result = process_value("hello")
    print(f"结果: {result}")


# ============== TypedDict ==============

class UserDict(TypedDict):
    """用户字典类型"""
    id: int
    name: str
    email: Optional[str]


def typed_dict_demo():
    """TypedDict演示"""
    user: UserDict = {
        "id": 1,
        "name": "Alice",
        "email": "alice@example.com"
    }
    print(f"user: {user}")


# ============== Callable ==============

Operation = Callable[[int, int], int]


def apply(op: Operation, a: int, b: int) -> int:
    """应用操作"""
    return op(a, b)


def callable_demo():
    """Callable演示"""
    add = lambda x, y: x + y
    multiply = lambda x, y: x * y
    
    print(f"add: {apply(add, 3, 5)}")
    print(f"multiply: {apply(multiply, 3, 5)}")


# ============== 泛型类方法 ==============

class Stack(Generic[T]):
    """泛型栈"""
    
    def __init__(self):
        self._items: List[T] = []
    
    def push(self, item: T):
        self._items.append(item)
    
    def pop(self) -> T:
        return self._items.pop()
    
    def is_empty(self) -> bool:
        return len(self._items) == 0


def stack_demo():
    """栈演示"""
    stack: Stack[int] = Stack()
    stack.push(1)
    stack.push(2)
    print(f"pop: {stack.pop()}")


# ============== 协变与逆变 ==============

class Base:
    """基类"""
    pass


class Derived(Base):
    """子类"""
    pass


Coords = Tuple[Base, ...]
DerivedCoords = Tuple[Derived, ...]


def variance_demo():
    """变体演示"""
    print("协变: 子类元组可赋值给基类元组")
    print("逆变: 基类函数引用可赋值给子类函数")


# ============== 类型守卫函数 ==============

def is_string_list(value: object) -> bool:
    """类型守卫"""
    return isinstance(value, list) and all(isinstance(x, str) for x in value)


def process_mixed(items: List[Any]):
    """处理混合类型"""
    if is_string_list(items):
        print("字符串列表:")
        for item in items:
            print(f"  {item.upper()}")
    else:
        print("其他类型")


def type_guard_demo():
    """类型守卫演示"""
    process_mixed(["a", "b", "c"])
    process_mixed([1, 2, 3])


# ============== Literal类型 ==============

from typing import Literal


def color_mode(mode: Literal["RGB", "RGBA", "CMYK"]) -> str:
    """颜色模式"""
    return f"模式: {mode}"


def literal_demo():
    """Literal演示"""
    result = color_mode("RGB")
    print(f"结果: {result}")


# ============== 测试运行 ==============

if __name__ == "__main__":
    print("=" * 50)
    print("15. typing模块泛型与协议")
    print("=" * 50)
    
    # 测试1: 泛型基础
    print("\n--- 1. 泛型基础 ---")
    generic_demo()
    
    # 测试2: 多类型
    print("\n--- 2. 多类型参数 ---")
    multi_type_demo()
    
    # 测试3: 泛型函数
    print("\n--- 3. 泛型函数 ---")
    generic_func_demo()
    
    # 测试4: 协议
    print("\n--- 4. 协议 ---")
    protocol_demo()
    
    # 测试5: 运行时协议
    print("\n--- 5. 运行时协议 ---")
    runtime_checkable_demo()
    
    # 测试6: 类型别名
    print("\n--- 6. 类型别名 ---")
    type_alias_demo()
    
    # 测试7: Optional
    print("\n--- 7. Union/Optional ---")
    optional_demo()
    
    # 测试8: TypedDict
    print("\n--- 8. TypedDict ---")
    typed_dict_demo()
    
    # 测试9: Callable
    print("\n--- 9. Callable ---")
    callable_demo()
    
    # 测试10: 泛型栈
    print("\n--- 10. 泛型类 ---")
    stack_demo()
    
    # 测试11: 变体
    print("\n--- 11. 协变与逆变 ---")
    variance_demo()
    
    # 测试12: 类型守卫
    print("\n--- 12. 类型守卫 ---")
    type_guard_demo()
    
    # 测试13: Literal
    print("\n--- 13. Literal ---")
    literal_demo()
    
    print("\n" + "=" * 50)
    print("typing模块学习完成!")
    print("=" * 50)