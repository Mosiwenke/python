"""
第56章: 实用工具函数
=============================

实用工具函数.
- 工具函数
- 辅助函数
"""

from typing import List, Dict, Any


def chunk_list(lst: List, n: int) -> List[List]:
    """分块"""
    return [lst[i:i+n] for i in range(0, len(lst), n)]


def flatten(lst: List[Any]) -> List:
    """扁平化"""
    result = []
    for item in lst:
        if isinstance(item, list):
            result.extend(flatten(item))
        else:
            result.append(item)
    return result


def group_by(lst: List[Dict], key: str) -> Dict:
    """分组"""
    result = {}
    for item in lst:
        k = item.get(key)
        result.setdefault(k, []).append(item)
    return result


def deduplicate(lst: List) -> List:
    """去重保持顺序"""
    seen = set()
    result = []
    for item in lst:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result


def retry(max_attempts: int = 3, delay: float = 1.0):
    """重试装饰器"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts - 1:
                        raise
            return None
        return wrapper
    return decorator


def memoize(func):
    """记忆化"""
    cache = {}
    def wrapper(*args):
        if args not in cache:
            cache[args] = func(*args)
        return cache[args]
    return wrapper


def once(func):
    """只执行一次"""
    result = [None]
    def wrapper(*args):
        if result[0] is None:
            result[0] = func(*args)
        return result[0]
    return wrapper


if __name__ == "__main__":
    print("=" * 50)
    print("56. 实用工具")
    print("=" * 50)
    print(f"chunk: {chunk_list([1,2,3,4,5], 2)}")
    print(f"flatten: {flatten([1,[2,[3]],4])}")
    print(f"group: {group_by([{'k':1,'v':1},{'k':2,'v':2},{'k':1,'v':3}], 'k')}")
    print(f"dedup: {deduplicate([1,2,1,3,2])}")
    print("=" * 50)