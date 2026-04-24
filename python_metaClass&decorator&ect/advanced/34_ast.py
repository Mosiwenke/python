"""
第34章: 抽象语法树(AST)
=============================

Python AST模块.
- ast模块
- 节点类型
- 遍历
"""

import ast
from typing import Any


# ============== 基础AST ==============

def basic_ast():
    """基础AST"""
    code = "x = 1 + 2"
    tree = ast.parse(code)
    print(f"树: {ast.dump(tree)}")


# ============== 节点遍历 ==============

def node_walk():
    """节点遍历"""
    code = """
x = 1
y = 2
"""
    tree = ast.parse(code)
    
    for node in ast.walk(tree):
        print(f"节点: {type(node).__name__}")


# ============== 编译 ==============

def compile_demo():
    """编译"""
    code = "print(1 + 2)"
    
    compiled = compile(code, "<string>", "exec")
    exec(compiled)


if __name__ == "__main__":
    print("=" * 50)
    print("34. 抽象语法树")
    print("=" * 50)
    
    print("\n--- 1. 基础AST ---")
    basic_ast()
    
    print("\n--- 2. 节点遍历 ---")
    node_walk()
    
    print("\n--- 3. 编译 ---")
    compile_demo()
    
    print("\n" + "=" * 50)
    print("AST学习完成!")
    print("=" * 50)