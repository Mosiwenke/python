"""
第27章: I/O与文件操作
=============================

Python输入输出与文件操作.
- 文件读写
- 目录操作
- 路径处理
- 流操作
"""

import os
import io
import tempfile
import shutil
from typing import List


# ============== 文件读写 ==============

def file_read_write():
    """文件读写"""
    with open("test_file.txt", "w") as f:
        f.write("Hello World")
    
    with open("test_file.txt", "r") as f:
        content = f.read()
        print(f"读取: {content}")
    
    os.remove("test_file.txt")


# ============== 路径操作 ==============

def path_operations():
    """路径操作"""
    path = "/home/user/file.txt"
    
    print(f"basename: {os.path.basename(path)}")
    print(f"dirname: {os.path.dirname(path)}")
    print(f"exists: {os.path.exists(path)}")
    print(f"isfile: {os.path.isfile(path)}")
    print(f"isdir: {os.path.isdir(path)}")


# ============== 目录操作 ==============

def directory_operations():
    """目录操作"""
    os.makedirs("test_dir/sub_dir", exist_ok=True)
    
    print(f"目录内容: {os.listdir('test_dir')}")
    
    os.rmdir("test_dir/sub_dir")
    os.rmdir("test_dir")


# ============== tempfile ==============

def tempfile_demo():
    """临时文件"""
    with tempfile.NamedTemporaryFile(delete=False) as f:
        f.write(b"temp data")
        print(f"临时文件: {f.name}")
    
    os.remove(f.name)
    
    temp_dir = tempfile.mkdtemp()
    print(f"临时目录: {temp_dir}")
    os.rmdir(temp_dir)


# ============== shutil ==============

def shutil_demo():
    """shutil演示"""
    os.makedirs("backup/src")
    with open("backup/src/file.txt", "w") as f:
        f.write("data")
    
    shutil.copy("backup/src/file.txt", "backup/dst.txt")
    print(f"复制成功")
    
    shutil.rmtree("backup")


# ============== io模块 ==============

def io_demo():
    """io模块"""
    buffer = io.StringIO()
    buffer.write("Hello")
    buffer.write(" World")
    
    buffer.seek(0)
    print(f"读取: {buffer.read()}")


# ============== 二进制文件 ==============

def binary_file():
    """二进制文件"""
    data = bytes([0, 1, 2, 3, 255])
    
    with open("binary.bin", "wb") as f:
        f.write(data)
    
    with open("binary.bin", "rb") as f:
        content = f.read()
        print(f"读取: {list(content)}")
    
    os.remove("binary.bin")


# ============== 测试运行 ==============

if __name__ == "__main__":
    print("=" * 50)
    print("27. I/O与文件操作")
    print("=" * 50)
    
    print("\n--- 1. 文件读写 ---")
    file_read_write()
    
    print("\n--- 2. 路径操作 ---")
    path_operations()
    
    print("\n--- 3. 目录操作 ---")
    directory_operations()
    
    print("\n--- 4. tempfile ---")
    tempfile_demo()
    
    print("\n--- 5. shutil ---")
    shutil_demo()
    
    print("\n--- 6. io ---")
    io_demo()
    
    print("\n--- 7. 二进制文件 ---")
    binary_file()
    
    print("\n" + "=" * 50)
    print("I/O学习完成!")
    print("=" * 50)