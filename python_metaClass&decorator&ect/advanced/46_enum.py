"""
第46章: 枚举与常量
=============================

枚举与常量管理.
- enum
- 常量定义
- 标志
"""

import enum


class Color(enum.Enum):
    RED = 1
    GREEN = 2
    BLUE = 3


class AutoName(enum.Enum):
    A = enum.auto()
    B = enum.auto()
    C = enum.auto()


class Flag(enum.Enum):
    READ = enum.auto()
    WRITE = enum.auto()
    EXEC = enum.auto()


def enum_demo():
    """枚举演示"""
    print(f"Color.RED: {Color.RED}")
    print(f"Color.RED.name: {Color.RED.name}")
    print(f"Color.RED.value: {Color.RED.value}")


def enum_iterate():
    """枚举迭代"""
    for color in Color:
        print(f"{color.name}: {color.value}")


def enum_compare():
    """枚举比较"""
    c1 = Color.RED
    c2 = Color.RED
    print(f"c1 == c2: {c1 == c2}")


def flag_demo():
    """标志演示"""
    perm = Flag.READ | Flag.WRITE
    print(f"READ|WRITE: {perm}")
    print(f"READ in perm: {Flag.READ in perm}")


def constant_module():
    """常量模块"""
    MAX_SIZE = 100
    DEFAULT_TIMEOUT = 30
    print(f"MAX_SIZE: {MAX_SIZE}")


if __name__ == "__main__":
    print("=" * 50)
    print("46. 枚举与常量")
    print("=" * 50)
    enum_demo()
    print()
    enum_iterate()
    print()
    enum_compare()
    print()
    flag_demo()
    print()
    constant_module()
    print("=" * 50)