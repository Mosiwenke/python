"""
第26章: 模块与包管理
=============================

Python模块与包管理.
- import系统
- 包结构
- __init__.py
- 相对导入
"""

import sys
import os
import importlib
from typing import List


# ============== import基础 ==============

def import_basic():
    """import基础"""
    import json
    print(f"json模块: {json.__name__}")
    print(f"json版本: {json.__version__}")
    
    from collections import defaultdict
    print(f"defaultdict: {defaultdict}")


# ============== 模块搜索路径 ==============

def module_search_path():
    """模块搜索路径"""
    for path in sys.path[:3]:
        print(f"路径: {path}")


# ============== importlib ==============

def importlib_demo():
    """importlib演示"""
    math_module = importlib.import_module("math")
    print(f"pi: {math_module.pi}")
    print(f"sqrt: {math_module.sqrt(4)}")


# ============== 包结构 ==============

def package_structure():
    """包结构"""
    print("包结构:")
    print("  package/")
    print("    __init__.py")
    print("    module.py")
    print("    subpackage/")
    print("      __init__.py")


# ============== __all__ ==============

def all_demo():
    """__all__演示"""
    print("__all__控制导出")


# ============== 模块缓存 ==============

def module_cache():
    """模块缓存"""
    print(f"sys.modules数量: {len(sys.modules)}")
    
    import collections
    print(f"collections在缓存: {'collections' in sys.modules}")


# ============== reload ==============

def reload_demo():
    """reload演示"""
    import importlib
    import json
    
    reloaded = importlib.reload(json)
    print(f"重新加载: {reloaded}")


# ============== 包依赖 ==============

def package_dependencies():
    """包依赖"""
    import pip
    print(f"pip版本: {pip.__version__}")


# ============== 测试运行 ==============

if __name__ == "__main__":
    print("=" * 50)
    print("26. 模块与包管理")
    print("=" * 50)
    
    print("\n--- 1. import基础 ---")
    import_basic()
    
    print("\n--- 2. 模块搜索路径 ---")
    module_search_path()
    
    print("\n--- 3. importlib ---")
    importlib_demo()
    
    print("\n--- 4. 包结构 ---")
    package_structure()
    
    print("\n--- 5. __all__ ---")
    all_demo()
    
    print("\n--- 6. 模块缓存 ---")
    module_cache()
    
    print("\n--- 7. reload ---")
    reload_demo()
    
    print("\n--- 8. 包依赖 ---")
    package_dependencies()
    
    print("\n" + "=" * 50)
    print("模块与包管理学习完成!")
    print("=" * 50)