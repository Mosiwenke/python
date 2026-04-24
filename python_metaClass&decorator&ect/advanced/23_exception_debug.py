"""
第23章: 异常处理与调试
=============================

Python异常处理和调试技术.
- 异常捕获
- traceback
- 调试技巧
- 日志
"""

import traceback
import sys
import logging
from typing import Optional, Callable


# ============== 基础异常 ==============

def basic_exception():
    """基础异常"""
    try:
        result = 1 / 0
    except ZeroDivisionError as e:
        print(f"除零错误: {e}")
    except Exception as e:
        print(f"其他错误: {e}")
    finally:
        print("finally执行")


def multiple_except():
    """多个异常"""
    try:
        value = int("abc")
    except ValueError as e:
        print(f"值错误: {e}")
    except TypeError as e:
        print(f"类型错误: {e}")


# ============== raise ==============

def raise_demo():
    """raise演示"""
    def validate_age(age):
        if age < 0:
            raise ValueError("年龄不能为负")
        if age > 150:
            raise ValueError("年龄超出范围")
        return age
    
    try:
        validate_age(-5)
    except ValueError as e:
        print(f"验证失败: {e}")


# ============== 自定义异常 ==============

class ValidationError(Exception):
    """验证错误"""
    def __init__(self, field: str, message: str):
        self.field = field
        self.message = message
        super().__init__(f"{field}: {message}")


class DatabaseError(Exception):
    """数据库错误"""
    pass


def custom_exception_demo():
    """自定义异常演示"""
    raise ValidationError("email", "格式无效")


# ============== traceback ==============

def traceback_demo():
    """traceback演示"""
    try:
        result = 1 / 0
    except Exception:
        traceback.print_exc()
        print("---")
        traceback.print_exc(file=open("error.log", "w"))
        print("已写入error.log")


# ============== 断言 ==============

def assertion_demo():
    """断言演示"""
    def divide(a, b):
        assert b != 0, "除数不能为零"
        return a / b
    
    try:
        divide(10, 0)
    except AssertionError as e:
        print(f"断言失败: {e}")


# ============== try-except-else ==============

def try_else_demo():
    """try-except-else"""
    try:
        result = int("42")
    except ValueError:
        print("转换失败")
    else:
        print(f"成功: {result}")


# ============== 异常链 ==============

def exception_chaining():
    """异常链"""
    try:
        try:
            int("abc")
        except ValueError as e:
            raise TypeError("类型错误") from e
    except TypeError as e:
        print(f"异常: {e}")
        print(f"原因: {e.__cause__}")


# ============== logging ==============

def logging_demo():
    """日志演示"""
    logging.basicConfig(level=logging.DEBUG)
    
    logger = logging.getLogger(__name__)
    logger.debug("调试信息")
    logger.info("信息")
    logger.warning("警告")
    logger.error("错误")
    logger.critical("严重")


# ============== 调试技巧 ==============

def debug_技巧():
    """调试技巧"""
    import pdb
    
    def buggy_function(n):
        result = 0
        for i in range(n):
            result += i
        return result
    
    result = buggy_function(5)
    print(f"结果: {result}")


# ============== 警告 ==============

import warnings


def warning_demo():
    """警告演示"""
    warnings.warn("这是一个警告")
    warnings.warn("过期警告", DeprecationWarning)


# ============== contextlib ==============

from contextlib import suppress


def suppress_demo():
    """suppress演示"""
    with suppress(FileNotFoundError, KeyError):
        open("nonexistent.txt").read()
    print("异常被忽略")


# ============== 测试运行 ==============

if __name__ == "__main__":
    print("=" * 50)
    print("23. 异常处理与调试")
    print("=" * 50)
    
    print("\n--- 1. 基础异常 ---")
    basic_exception()
    
    print("\n--- 2. 多个异常 ---")
    multiple_except()
    
    print("\n--- 3. raise ---")
    raise_demo()
    
    print("\n--- 4. traceback ---")
    try:
        traceback_demo()
    except:
        pass
    
    print("\n--- 5. 断言 ---")
    assertion_demo()
    
    print("\n--- 6. try-except-else ---")
    try_else_demo()
    
    print("\n--- 7. 异常链 ---")
    exception_chaining()
    
    print("\n--- 8. logging ---")
    logging_demo()
    
    print("\n--- 9. 警告 ---")
    warning_demo()
    
    print("\n--- 10. suppress ---")
    suppress_demo()
    
    print("\n" + "=" * 50)
    print("异常处理学习完成!")
    print("=" * 50)