"""
第30章: 测试驱动开发
=============================

Python测试基础.
- unittest
- pytest
- 模拟对象
"""

import unittest
from unittest.mock import Mock, patch, MagicMock


def add(a, b):
    return a + b


class TestAdd(unittest.TestCase):
    def test_add(self):
        self.assertEqual(add(1, 2), 3)


def basic_test():
    suite = unittest.TestLoader().loadTestsFromTestCase(TestAdd)
    runner = unittest.TextTestRunner(verbosity=0)
    runner.run(suite)


def mock_demo():
    mock = Mock()
    mock.method.return_value = 42
    result = mock.method()
    print(f"Mock结果: {result}")


def patch_demo():
    with patch("__main__.add", return_value=100):
        result = add(1, 2)
        print(f"patch结果: {result}")


if __name__ == "__main__":
    print("=" * 50)
    print("30. 测试驱动开发")
    print("=" * 50)
    
    print("\n--- 1. 基础测试 ---")
    basic_test()
    
    print("\n--- 2. Mock ---")
    mock_demo()
    
    print("\n--- 3. patch ---")
    patch_demo()
    
    print("\n" + "=" * 50)
    print("测试驱动开发学习完成!")
    print("=" * 50)