"""
第42章: CLI应用开发
=============================

命令行应用开发.
- argparse
--click
- typer
"""

import sys


def argparse_demo():
    """argparse演示"""
    print("argparse: 命令行参数解析")


def sysargv_demo():
    """sys.argv演示"""
    print(f"脚本名: {sys.argv[0]}")
    print(f"参数: {sys.argv[1:]}")


if __name__ == "__main__":
    print("=" * 50)
    print("42. CLI应用开发")
    print("=" * 50)
    argparse_demo()
    sysargv_demo()
    print("=" * 50)