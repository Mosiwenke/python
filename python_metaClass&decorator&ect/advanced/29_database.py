"""
第29章: 数据库交互
=============================

Python数据库交互基础.
- SQLite
- 连接池
- ORM概念
"""

import sqlite3
from typing import List, Optional


# ============== SQLite基础 ==============

def sqlite_basic():
    """SQLite基础"""
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()
    
    cursor.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT)")
    cursor.execute("INSERT INTO users (name) VALUES ('Alice')")
    cursor.execute("INSERT INTO users (name) VALUES ('Bob')")
    
    conn.commit()
    
    cursor.execute("SELECT * FROM users")
    for row in cursor.fetchall():
        print(f"用户: {row}")
    
    conn.close()


# ============== 参数化查询 ==============

def parameterized_query():
    """参数化查询"""
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()
    
    cursor.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT)")
    cursor.execute("INSERT INTO users (name) VALUES (?)", ("Alice",))
    cursor.execute("INSERT INTO users (name) VALUES (?)", ("Bob",))
    
    cursor.execute("SELECT * FROM users WHERE name = ?", ("Alice",))
    print(f"查询结果: {cursor.fetchone()}")
    
    conn.close()


# ============== 游标操作 ==============

def cursor_operations():
    """游标操作"""
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()
    
    cursor.execute("CREATE TABLE data (value TEXT)")
    values = [("a",), ("b",), ("c",)]
    cursor.executemany("INSERT INTO data (value) VALUES (?)", values)
    
    conn.commit()
    
    cursor.execute("SELECT * FROM data")
    for row in cursor:
        print(f"行: {row}")
    
    conn.close()


# ============== 上下文管理器 ==============

def context_manager_demo():
    """上下文管理器"""
    with sqlite3.connect(":memory:") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        print(f"结果: {cursor.fetchone()}")


# ============== 测试运行 ==============

if __name__ == "__main__":
    print("=" * 50)
    print("29. 数据库交互")
    print("=" * 50)
    
    print("\n--- 1. SQLite基础 ---")
    sqlite_basic()
    
    print("\n--- 2. 参数化查询 ---")
    parameterized_query()
    
    print("\n--- 3. 游标操作 ---")
    cursor_operations()
    
    print("\n--- 4. 上下文管理器 ---")
    context_manager_demo()
    
    print("\n" + "=" * 50)
    print("数据库交互学习完成!")
    print("=" * 50)