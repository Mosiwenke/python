"""
第44章: 进程与系统信息
=============================

进程与系统信息.
- os/sys模块
- 环境变量
- 平台信息
"""

import os
import sys
import platform


def os_demo():
    """os模块"""
    print(f"os.name: {os.name}")
    print(f"os.getcwd: {os.getcwd()}")


def sys_demo():
    """sys模块"""
    print(f"sys.version: {sys.version}")
    print(f"sys.platform: {sys.platform}")
    print(f"sys.executable: {sys.executable}")


def platform_demo():
    """platform"""
    print(f"platform: {platform.platform()}")
    print(f"python_version: {platform.python_version()}")


def env_vars():
    """环境变量"""
    print(f"HOME: {os.environ.get('HOME', '')}")
    print(f"PATH: {os.environ.get('PATH', '')[:50]}...")


def process_info():
    """进程信息"""
    print(f"pid: {os.getpid()}")


if __name__ == "__main__":
    print("=" * 50)
    print("44. 进程与系统信息")
    print("=" * 50)
    os_demo()
    sys_demo()
    platform_demo()
    env_vars()
    process_info()
    print("=" * 50)