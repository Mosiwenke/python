"""
第16章: 序列化与反序列化
==============================

Python数据序列化工具.
- pickle
- json
- marshal
- shelve
- 自定义序列化
"""

import pickle
import json
import marshal
import shelve
import base64
import ast
from typing import Any, List, Dict
from dataclasses import dataclass, asdict


# ============== Pickle ==============

class User:
    def __init__(self, id: int, name: str, email: str):
        self.id = id
        self.name = name
        self.email = email
    
    def __repr__(self):
        return f"User(id={self.id}, name={self.name}, email={self.email})"


class _CustomClass:
    def __init__(self, value: int):
        self.value = value
    
    def __getstate__(self):
        return {"value": self.value * 2}
    
    def __setstate__(self, state):
        self.value = state["value"] // 2


def pickle_basic():
    """Pickle基本用法"""
    data = {"name": "Alice", "age": 30}
    
    pickled = pickle.dumps(data)
    unpickled = pickle.loads(pickled)
    
    print(f"原始: {data}")
    print(f"解码: {unpickled}")


def pickle_objects():
    """Pickle对象"""
    user = User(1, "Alice", "alice@example.com")
    
    pickled = pickle.dumps(user)
    restored = pickle.loads(pickled)
    
    print(f"原始: {user}")
    print(f"恢复: {restored}")


def pickle_custom():
    """自定义Pickle"""
    obj = _CustomClass(10)
    pickled = pickle.dumps(obj)
    restored = pickle.loads(pickled)
    
    print(f"原始: {obj.value}")
    print(f"恢复: {restored.value}")


def pickle_protocols():
    """Pickle协议版本"""
    data = [1, 2, 3]
    
    for protocol in range(pickle.HIGHEST_PROTOCOL + 1):
        pickled = pickle.dumps(data, protocol=protocol)
        print(f"协议{protocol}: {len(pickled)} bytes")


# ============== JSON ==============

def json_basic():
    """JSON基本用法"""
    data = {"name": "Alice", "age": 30, "active": True}
    
    json_str = json.dumps(data)
    parsed = json.loads(json_str)
    
    print(f"JSON: {json_str}")
    print(f"解析: {parsed}")


def json_pretty():
    """格式化JSON"""
    data = {"users": [{"id": 1, "name": "Alice"}]}
    
    pretty = json.dumps(data, indent=2, sort_keys=True)
    print(pretty)


def json_custom():
    """自定义JSON编码"""
    
    class UserEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj, User):
                return {"id": obj.id, "name": obj.name}
            return super().default(obj)
    
    user = User(1, "Bob", "bob@example.com")
    json_str = json.dumps(user, cls=UserEncoder)
    print(f"JSON: {json_str}")


def json_object_hook():
    """自定义解码"""
    json_str = '{"id": 1, "name": "Charlie"}'
    
    def parse_user(dct):
        if "id" in dct and "name" in dct:
            return User(dct["id"], dct["name"], "")
        return dct
    
    parsed = json.loads(json_str, object_hook=parse_user)
    print(f"解析: {parsed}")


def json_datetime():
    """日期时间处理"""
    import datetime
    
    data = {
        "event": "party",
        "time": datetime.datetime.now().isoformat()
    }
    
    json_str = json.dumps(data)
    parsed = json.loads(json_str)
    print(f"JSON: {json_str}")


# ============== Marshal ==============

def marshal_basic():
    """Marshal基本用法"""
    code = compile("print('hello')", "<string>", "exec")
    
    marshalled = marshal.dumps(code)
    restored = marshal.loads(marshalled)
    
    exec(restored)


def marshal_versions():
    """Marshal版本"""
    data = {"key": "value"}
    
    for version in range(marshal.version + 1):
        try:
            marshalled = marshal.dumps(data, version=version)
            print(f"版本{version}: {len(marshalled)} bytes")
        except Exception as e:
            print(f"版本{version}: 错误")


# ============== Shelve ==============

def shelve_demo():
    """Shelf演示"""
    with shelve.open("testshelf") as shelf:
        shelf["user1"] = {"name": "Alice", "age": 30}
        shelf["user2"] = {"name": "Bob", "age": 25}
        
        print(f"user1: {shelf['user1']}")
        print(f"keys: {list(shelf.keys())}")
        
        del shelf["user1"]
        print(f"after delete: {list(shelf.keys())}")


# ============== Base64编码 ==============

def base64_demo():
    """Base64编码"""
    data = b"Hello, World!"
    
    encoded = base64.b64encode(data)
    decoded = base64.b64decode(encoded)
    
    print(f"原始: {data}")
    print(f"编码: {encoded}")
    print(f"解码: {decoded}")


# ============== 自定义序列化 ==============

class Serializable:
    """可序列化基类"""
    
    def serialize(self) -> Dict:
        return asdict(self)
    
    @classmethod
    def deserialize(cls, data: Dict):
        return cls(**data)


@dataclass
class Product(Serializable):
    """产品"""
    id: int
    name: str
    price: float


def custom_serial_demo():
    """自定义序列化"""
    product = Product(1, "Widget", 9.99)
    
    json_str = json.dumps(product.serialize())
    restored = Product.deserialize(json.loads(json_str))
    
    print(f"原始: {product}")
    print(f"恢复: {restored}")


# ============== 深度复制 ==============

def deep_copy_demo():
    """深度复制"""
    original = {"name": "Alice", "scores": [1, 2, 3]}
    
    copied = pickle.loads(pickle.dumps(original))
    copied["scores"].append(4)
    
    print(f"原始: {original}")
    print(f"复制: {copied}")


# ============== 性能对比 ==============

def performance_demo():
    """性能对比"""
    import time
    
    data = {"key": "value", "numbers": list(range(1000))}
    
    start = time.perf_counter()
    for _ in range(1000):
        _ = pickle.dumps(data)
    pickle_time = time.perf_counter() - start
    
    start = time.perf_counter()
    for _ in range(1000):
        _ = json.dumps(data)
    json_time = time.perf_counter() - start
    
    print(f"Pickle: {pickle_time:.3f}s")
    print(f"JSON: {json_time:.3f}s")


# ============== 安全反序列化 ==============

class RestrictedUnpickler(pickle.Unpickler):
    """安全的反序列化器"""
    
    ALLOWED_CLASSES = {
        "__main__": {"User"},
        "typing": {"List", "Dict"},
    }
    
    def find_class(self, module, name):
        if module in self.ALLOWED_CLASSES:
            if name in self.ALLOWED_CLASSES[module]:
                return super().find_class(module, name)
        raise pickle.UnpicklingError(f"不允许的类: {module}.{name}")


def safe_unpickle():
    """安全反序列化"""
    import io
    
    data = pickle.dumps(User(1, "Test", "test@example.com"))
    stream = io.BytesIO(data)
    
    restricked = RestrictedUnpickler(stream).load()
    print(f"恢复: {restricked}")


# ============== 测试运行 ==============

if __name__ == "__main__":
    print("=" * 50)
    print("16. 序列化与反序列化")
    print("=" * 50)
    
    # 测试1: Pickle
    print("\n--- 1. Pickle基本用法 ---")
    pickle_basic()
    pickle_objects()
    
    # 测试2: 自定义Pickle
    print("\n--- 2. 自定义Pickle ---")
    pickle_custom()
    
    # 测试3: JSON
    print("\n--- 3. JSON基本用法 ---")
    json_basic()
    json_pretty()
    
    # 测试4: 自定义JSON
    print("\n--- 4. 自定义JSON ---")
    json_custom()
    json_object_hook()
    
    # 测试5: Marshal
    print("\n--- 5. Marshal ---")
    marshal_basic()
    
    # 测试6: Shelve
    print("\n--- 6. Shelve ---")
    shelve_demo()
    
    # 测试7: Base64
    print("\n--- 7. Base64 ---")
    base64_demo()
    
    # 测试8: 自定义序列化
    print("\n--- 8. 自定义序列化 ---")
    custom_serial_demo()
    
    # 测试9: 深度复制
    print("\n--- 9. 深度复制 ---")
    deep_copy_demo()
    
    # 测试10: 性能
    print("\n--- 10. 性能对比 ---")
    performance_demo()
    
    # 测试11: 安全
    print("\n--- 11. 安全反序列化 ---")
    safe_unpickle()
    
    import os
    if os.path.exists("testshelf.db"):
        os.remove("testshelf.db")
    if os.path.exists("testshelf.dir"):
        os.remove("testshelf.dir")
    if os.path.exists("testshelf.bak"):
        os.remove("testshelf.bak")
    if os.path.exists("testshelf.dat"):
        os.remove("testshelf.dat")
    
    print("\n" + "=" * 50)
    print("序列化学习完成!")
    print("=" * 50)