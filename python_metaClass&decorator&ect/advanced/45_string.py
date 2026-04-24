"""
第45章: 字符串处理与格式化
=============================

字符串处理与格式化.
- f-string
- format
- 模板
"""

import string


def fstring_demo():
    """f-string"""
    name = "Alice"
    age = 30
    print(f"Name: {name}, Age: {age}")
    print(f"Age+1: {age + 1}")
    print(f"{{literal}}: {{age}}")


def format_demo():
    """format"""
    print("{:>10}".format("right"))
    print("{:<10}".format("left"))
    print("{:^10}".format("center"))
    print("{:.3f}".format(3.14159))


def string_template():
    """模板"""
    template = string.Template("Hello $name!")
    result = template.substitute(name="World")
    print(result)


def bytes_demo():
    """字节串"""
    b = b"hello"
    print(f"bytes: {b}")
    print(f"decode: {b.decode()}")


def encoding_demo():
    """编码"""
    s = "你好"
    print(f"utf-8编码: {len(s.encode('utf-8'))}")


if __name__ == "__main__":
    print("=" * 50)
    print("45. 字符串处理")
    print("=" * 50)
    fstring_demo()
    print()
    format_demo()
    print()
    string_template()
    print()
    bytes_demo()
    print()
    encoding_demo()
    print("=" * 50)