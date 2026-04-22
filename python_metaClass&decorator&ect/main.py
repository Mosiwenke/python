#!/usr/bin/env python3
"""
Python 元编程与装饰器学习项目
=============================
从基础到高级，系统学习装饰器和元编程技术

内容大纲:
- 1. 基础函数装饰器
- 2. 类装饰器
- 3. 带参数的装饰器
- 4. 装饰器堆叠
- 5. 类方式的装饰器
- 6. 元类 (Metaclass)
- 7. 描述符协议
- 8. 高级装饰器模式

模块说明:
- decorators/     : 各种装饰器实现
- metaclasses/   : 元类实现
- descriptors/   : 描述符实现
- examples/      : 使用示例
- tests/         : 测试用例
"""

import sys
import os

__version__ = "1.0.0"
__author__ = "Python Learner"

# 版本信息
VERSIONS = {
    "python": sys.version_info[:3],
    "project": __version__,
}

def check_environment():
    """检查运行环境"""
    print(f"Python 版本: {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
    print(f"平台: {sys.platform}")
    return True

if __name__ == "__main__":
    check_environment()
    print("\n欢迎学习 Python 元编程与装饰器!")
    print("请查看 decorators/ 目录下的模块开始学习")