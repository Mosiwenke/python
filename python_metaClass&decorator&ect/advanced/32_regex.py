"""
第32章: 正则表达式
=============================

Python正则表达式.
- re模块
- 匹配
- 替换
"""

import re
from typing import List, Optional


# ============== 基础匹配 ==============

def basic_match():
    """基础匹配"""
    pattern = r"hello"
    text = "hello world"
    
    match = re.search(pattern, text)
    if match:
        print(f"匹配: {match.group()}")


# ============== 正则模式 ==============

def regex_patterns():
    """正则模式"""
    patterns = [
        (r"\d+", "数字"),
        (r"\w+", "单词"),
        (r"\s+", "空白"),
    ]
    
    for pattern, desc in patterns:
        text = "hello 123 world"
        matches = re.findall(pattern, text)
        print(f"{desc}: {matches}")


# ============== 替换 ==============

def replace_demo():
    """替换"""
    text = "hello world"
    result = re.sub(r"world", "python", text)
    print(f"替换: {result}")


# ============== 分割 ==============

def split_demo():
    """分割"""
    text = "a,b,c"
    parts = re.split(r",", text)
    print(f"分割: {parts}")


# ============== 编译 ==============

def compile_demo():
    """编译"""
    pattern = re.compile(r"\d+")
    matches = pattern.findall("abc123def456")
    print(f"匹配: {matches}")


# ============== 测试运行 ==============

if __name__ == "__main__":
    print("=" * 50)
    print("32. 正则表达式")
    print("=" * 50)
    
    print("\n--- 1. 基础匹配 ---")
    basic_match()
    
    print("\n--- 2. 正则模式 ---")
    regex_patterns()
    
    print("\n--- 3. 替换 ---")
    replace_demo()
    
    print("\n--- 4. 分割 ---")
    split_demo()
    
    print("\n--- 5. 编译 ---")
    compile_demo()
    
    print("\n" + "=" * 50)
    print("正则表达式学习完成!")
    print("=" * 50)