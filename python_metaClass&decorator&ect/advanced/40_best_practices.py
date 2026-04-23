"""
第40章: Python最佳实践与常见陷阱
=============================

Python最佳实践与常见陷阱.
- 常见错误
- 性能陷阱
- 编码习惯
"""

import warnings


# ============== 常见陷阱 ==============

def common_pitfalls():
    """常见陷阱"""
    a = [1, 2, 3]
    b = a
    b.append(4)
    print(f"引用陷阱: {a}")  # a也被修改
    
    a = [1, 2, 3]
    b = a.copy()
    b.append(4)
    print(f"修复: {a}")  # a不变


# ============== 默认可变参数 ==============

def mutable_default(default=[]):
    """可变默认参数陷阱"""
    default.append(1)
    return default


def mutable_pitfall():
    """可变默认"""
    print(f"调用1: {mutable_default()}")
    print(f"调用2: {mutable_default()}")


# ============== 延迟绑定 ==============

def late_binding():
    """延迟绑定"""
    funcs = [lambda: i for i in range(3)]
    
    for f in funcs:
        print(f"延迟: {f()}")
    
    funcs = [lambda i=i: i for i in range(3)]
    for f in funcs:
        print(f"修复: {f()}")


# ============== 性能陷阱 ==============

def performance_pitfall():
    """性能陷阱"""
    s = ""
    for i in range(100):
        s += str(i)
    
    s = "".join(str(i) for i in range(100))
    print("使用join")


# ============== None比较 ==============

def None_comparison():
    """None比较"""
    x = None
    if x is None:
        print("is None")
    
    if x == None:
        print("== None")
        warnings.warn("用is比较None")


if __name__ == "__main__":
    print("=" * 50)
    print("40. Python最佳实践与常见陷阱")
    print("=" * 50)
    
    print("\n--- 1. 常见陷阱 ---")
    common_pitfalls()
    
    print("\n--- 2. 可变默认 ---")
    mutable_pitfall()
    
    print("\n--- 3. 延迟绑定 ---")
    late_binding()
    
    print("\n--- 4. 性能陷阱 ---")
    performance_pitfall()
    
    print("\n--- 5. None比较 ---")
    None_comparison()
    
    print("\n" + "=" * 50)
    print("学习完成!")
    print("=" * 50)