"""
第5章: 元类 (Metaclass)
========================

元类是创建类的类.
Python中类本身也是对象,元类就是用来创建这些类对象的"类".

核心概念:
- type() 动态创建类
- __new__ 创建类对象
- __init__ 初始化类
- 元类继承
"""

from typing import Callable, Any, Type, Dict


# ============== 最简单的元类 ==============

class SimpleMeta(type):
    """
    最简单的元类 - 继承自type
    
    元类可以:
    - 拦截类创建
    - 修改类属性
    - 添加新方法
    """
    
    def __new__(mcs, name, bases, namespace):
        print(f"[SimpleMeta] 创建类: {name}")
        
        # 可以修改或添加属性
        namespace['created_by'] = 'SimpleMeta'
        
        # 创建类
        cls = super().__new__(mcs, name, bases, namespace)
        return cls


class MyClass(metaclass=SimpleMeta):
    """使用元类创建类"""
    
    def greet(self):
        return "Hello!"


# ============== 自动注册元类 ==============

class RegistryMeta(type):
    """
    自动注册元类 - 将创建的类自动注册
    
    类似于插件系统
    """
    
    _registry: Dict[str, Type] = {}
    
    def __new__(mcs, name, bases, namespace):
        cls = super().__new__(mcs, name, bases, namespace)
        
        # 自动注册 (排除基类)
        if name != 'Base':
            RegistryMeta._registry[name] = cls
            print(f"[RegistryMeta] 注册: {name}")
        
        return cls


class Base(metaclass=RegistryMeta):
    pass


class PluginA(Base):
    def run(self):
        return "PluginA"


class PluginB(Base):
    def run(self):
        return "PluginB"


# ============== Singleton 元类 ==============

class SingletonMeta(type):
    """
    单例元类 - 确保类只能创建一个实例
    
    与装饰器实现的单例相比,元类方式:
    - 更简洁
    - 可用于任何类
    """
    
    _instances: Dict[Type, object] = {}
    
    def __call__(cls, *args, **kwargs):
        if cls not in SingletonMeta._instances:
            print(f"[SingletonMeta] 创建单例: {cls.__name__}")
            instance = super().__call__(cls, *args, **kwargs)
            SingletonMeta._instances[cls] = instance
        return SingletonMeta._instances[cls]


class Database(metaclass=SingletonMeta):
    def __init__(self):
        print("初始化数据库...")
        self.connected = True


# ============== 抽象类元类 ==============

class AbstractMeta(type):
    """
    抽象类元类 - 强制必须实现某些方法
    
    使用方式:
        class MyAbstract(metaclass=AbstractMeta):
            required_methods = ['method1', 'method2']
    """
    
    def __new__(mcs, name, bases, namespace):
        cls = super().__new__(mcs, name, bases, namespace)
        
        if 'required_methods' in namespace:
            # 检查是否实现了抽象方法
            missing = []
            for method_name in namespace['required_methods']:
                if method_name not in namespace:
                    missing.append(method_name)
            
            if missing:
                raise TypeError(
                    f"类 {name} 必须实现抽象方法: {missing}"
                )
        
        return cls


class MyInterface(metaclass=AbstractMeta):
    required_methods = ['process', 'render']
    
    def process(self):
        pass
    
    def render(self):
        pass


# ============== 验证属性元类 ==============

class ValidatedMeta(type):
    """
    属性验证元类 - 自动验证类属性
    
    示例:
        class User(metaclass=ValidatedMeta):
            validators = {
                'name': lambda x: len(x) > 0,
                'age': lambda x: 0 <= x <= 150
            }
    """
    
    def __call__(cls, *args, **kwargs):
        instance = super().__call__(*args, **kwargs)
        
        # 验证属性
        validators = getattr(cls, 'validators', {})
        for attr_name, validator in validators.items():
            value = getattr(instance, attr_name, None)
            if not validator(value):
                raise ValueError(
                    f"属性 {attr_name} 验证失败: {value}"
                )
        
        return instance


class User(metaclass=ValidatedMeta):
    validators = {
        'name': lambda x: x and len(x) > 0,
        'age': lambda x: 0 <= x <= 150
    }
    
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age


# ============== 自动添加方法元类 ==============

class AutoMethodMeta(type):
    """
    自动添加方法元类
    
    根据某些规则自动生成方法
    """
    
    def __new__(mcs, name, bases, namespace):
        cls = super().__new__(mcs, name, bases, namespace)
        
        # 自动添加 getter/setter
        if hasattr(cls, '_fields'):
            for field in cls._fields:
                # 添加 getter
                if f'get_{field}' not in namespace:
                    namespace[f'get_{field}'] = make_getter(field)
                
                # 添加 setter
                if f'set_{field}' not in namespace:
                    namespace[f'set_{field}'] = make_setter(field)
        
        return cls


def make_getter(field: str):
    def getter(self):
        return getattr(self, f'_{field}')
    return getter


def make_setter(field: str):
    def setter(self, value):
        setattr(self, f'_{field}', value)
    return setter


class Person(metaclass=AutoMethodMeta):
    _fields = ['name', 'age']
    
    def __init__(self, name: str, age: int):
        self._name = name
        self._age = age


# ============== ORM风格元类 ==============

class ORM_meta(type):
    """
    简化版ORM元类 - 自动映射字典到对象
    """
    
    def __new__(mcs, name, bases, namespace):
        cls = super().__new__(mcs, name, bases, namespace)
        
        @classmethod
        def from_dict(cls, data: dict):
            instance = cls()
            for key, value in data.items():
                setattr(instance, key, value)
            return instance
        
        cls.from_dict = from_dict
        
        def to_dict(self):
            return {
                key: getattr(self, key)
                for key in dir(self)
                if not key.startswith('_')
            }
        
        cls.to_dict = to_dict
        
        return cls


class UserModel(metaclass=ORM_meta):
    pass


# ============== 代理自动生成元类 ==============

class ProxyMeta(type):
    """
    代理自动生成元类
    
    自动将方法调用转发到委托对象
    """
    
    def __new__(mcs, name, bases, namespace):
        cls = super().__new__(mcs, name, bases, namespace)
        
        def __getattr__(self, name):
            # 转发到 _delegate 属性
            delegate = self.__dict__.get('_delegate')
            if delegate:
                return getattr(delegate, name)
            raise AttributeError(f"没有委托对象")
        
        cls.__getattr__ = __getattr__
        
        return cls


class RealObject:
    def method(self):
        return "真实方法"


class Proxy(metaclass=ProxyMeta):
    def __init__(self, real: RealObject):
        self._delegate = real


# ============== 测试运行 ==============

if __name__ == "__main__":
    print("=" * 50)
    print("5. 元类 (Metaclass)")
    print("=" * 50)
    
    # 测试1: 简单元类
    print("\n--- 测试: SimpleMeta ---")
    obj = MyClass()
    print(f"created_by: {obj.created_by}")
    
    # 测试2: 自动注册元类
    print("\n--- 测试: RegistryMeta ---")
    print(f"注册的类: {list(RegistryMeta._registry.keys())}")
    
    # 测试3: Singleton 元类
    print("\n--- 测试: SingletonMeta ---")
    db1 = Database()
    db2 = Database()
    print(f"db1 is db2: {db1 is db2}")
    
    # 测试4: 自动方法生成
    print("\n--- 测试: AutoMethodMeta ---")
    person = Person("Alice", 30)
    print(f"name: {person.get_name()}")
    person.set_name("Bob")
    print(f"name after set: {person.get_name()}")
    
    # 测试5: ORM元类
    print("\n--- 测试: ORM_meta ---")
    user = UserModel()
    user.name = "Alice"
    user.age = 30
    print(f"to_dict: {user.to_dict()}")
    
    # from_dict
    user2 = UserModel.from_dict({"name": "Bob", "age": 25})
    print(f"from_dict: name={user2.name}, age={user2.age}")
    
    # 测试6: 代理元类
    print("\n--- 测试: ProxyMeta ---")
    real = RealObject()
    proxy = Proxy(real)
    print(f"proxy.method(): {proxy.method()}")
    
    print("\n" + "=" * 50)
    print("元类学习完成!")
    print("=" * 50)