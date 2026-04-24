"""
第53章: 类型注解与Protocol
=============================

类型注解进阶.
- typing.Protocol
- typing.TypeVar
- typing.Generic
- 类型检查
"""

from typing import *


def protocol_demo():
    """Protocol"""
    class Drawable(Protocol):
        def draw(self): ...
    
    class Circle:
        def draw(self): print("circle")
    
    def render(d: Drawable): d.draw()
    
    render(Circle())


def generic_demo():
    """Generic"""
    T = TypeVar('T')
    
    class Box(Generic[T]):
        def __init__(self, v: T): self.value = v
        def get(self) -> T: return self.value
    
    b = Box[int](5)
    print(f"value: {b.get()}")


def typevar_demo():
    """TypeVar"""
    T = TypeVar('T')
    
    def first(lst: List[T]) -> T:
        return lst[0]
    
    print(f"first: {first([1,2,3])}")


def typing_cast():
    """cast"""
    from typing import cast
    
    x: Any = "hello"
    y = cast(str, x)
    print(f"cast: {y}")


def new_type():
    """NewType"""
    from typing import NewType
    
    UserId = NewType('UserId', int)
    
    def get_user(uid: UserId) -> str:
        return f"user_{uid}"
    
    print(get_user(UserId(123)))


def literal_demo():
    """Literal"""
    from typing import Literal
    
    def status(s: Literal["ok", "error"]): print(s)
    
    status("ok")


if __name__ == "__main__":
    print("=" * 50)
    print("53. 类型注解进阶")
    print("=" * 50)
    protocol_demo()
    print()
    generic_demo()
    typevar_demo()
    typing_cast()
    new_type()
    literal_demo()
    print("=" * 50)