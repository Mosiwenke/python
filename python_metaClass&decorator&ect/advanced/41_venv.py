"""
第41章: 虚拟环境与打包
=============================

虚拟环境与打包.
- venv
- setuptools
- 打包
"""

try:
    import venv
    print("venv可用")
except:
    print("venv不可用")


def pip_list():
    """查看包"""
    try:
        import pkg_resources
        print(f"已安装包数量: {len(pkg_resources.working_set)}")
    except:
        pass


if __name__ == "__main__":
    print("=" * 50)
    print("41. 虚拟环境与打包")
    print("=" * 50)
    pip_list()
    print("=" * 50)