"""
第2章: 类装饰器
==============

类装饰器用于修改或包装类行为.
可以添加方法、属性,或修改类的定义.

关键概念:
- type() 动态创建类
- __new__ 方法拦截类创建
- classmethod/staticmethod vs 实例方法
"""

from functools import wraps
from typing import Type, Callable, Any, Dict


# ============== 简单的类装饰器 ==============

def add_method(cls: Type) -> Type:
    """
    简单的类装饰器 - 给类添加新方法
    
    原理:
    1. 接收类作为参数
    2. 定义一个新方法
    3. 将方法添加到类中
    4. 返回修改后的类
    """
    def new_method(self):
        return f"我是通过装饰器添加的方法! original_class: {self.__class__.__name__}"
    
    cls.new_method = new_method
    return cls


@add_method
class SimpleClass:
    def __init__(self, value: int):
        self.value = value
    
    def get_value(self) -> int:
        return self.value


# ============== 自动注册类装饰器 ==============

class_registry: Dict[str, Type] = {}

def register(name: str):
    """
    类注册装饰器 - 将类自动注册到全局注册表中
    
    常用于:
    - 插件系统
    - 命令模式注册
    - 工厂模式
    """
    def decorator(cls: Type) -> Type:
        class_registry[name] = cls
        cls.registered_name = name
        return cls
    return decorator


@register("plugin_a")
class PluginA:
    def run(self):
        return "Plugin A running"


@register("plugin_b") 
class PluginB:
    def run(self):
        return "Plugin B running"


# ============== Singleton 单例装饰器 ==============

def singleton(cls: Type) -> Type:
    """
    单例模式装饰器
    
    原理: 拦截类的__new__方法,确保只创建一次实例
    """
    instances = {}
    
    @wraps(cls)
    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    
    # 替换类的__new__方法
    original_new = cls.__new__
    
    def __new__(cls, *args, **kwargs):
        if cls not in instances:
            instances[cls] = super().__new__(cls)
        return instances[cls]
    
    cls.__new__ = __new__
    return cls


@singleton
class Database:
    def __init__(self):
        print("初始化数据库连接...")
        self.connected = True


# ============== 惰性计算属性 ==============

class lazy_property:
    """
    惰性计算属性装饰器 (作为类装饰器使用)
    
    第一次访问时计算,之后缓存结果
    类似于 Django 的 cached_property
    """
    def __init__(self, func: Callable):
        self.func = func
        self.attr_name = None
    
    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        
        # 获取属性名 (如果没有被赋值,从函数名获取)
        if self.attr_name is None:
            self.attr_name = self.func.__name__
        
        # 计算值并缓存到实例上
        value = self.func(obj)
        setattr(obj, self.attr_name, value)
        return value


class DataLoader:
    def __init__(self, data_source: str):
        self.data_source = data_source
        print(f"初始化: {data_source}")
    
    @lazy_property
    def expensive_data(self):
        """模拟昂贵的计算"""
        print("正在加载大量数据...")
        import time
        time.sleep(0.1)
        return f"数据��自: {self.data_source}"


# ============== 抽象方法检查 ==============

def abstract_checker(cls: Type) -> Type:
    """
    抽象方法检查器
    
    检查所有抽象方法是否都被实现
    """
    abstract_methods = set()
    
    # 首先收集抽象方法
    for attr_name in dir(cls):
        attr = getattr(cls, attr_name)
        if hasattr(attr, '__is_abstract__'):
            abstract_methods.add(attr_name)
    
    # 验证
    original_init = cls.__init__
    
    @wraps(original_init)
    def new_init(self, *args, **kwargs):
        missing = []
        for method_name in abstract_methods:
            if not hasattr(self, method_name) or getattr(self, method_name) is None:
                missing.append(method_name)
        
        if missing:
            raise TypeError(f"类 {cls.__name__} 缺少抽象方法: {missing}")
        
        return original_init(self, *args, **kwargs)
    
    cls.__init__ = new_init
    return cls


def abstract(func: Callable) -> Callable:
    """标记方法为抽象方法"""
    func.__is_abstract__ = True
    return func


@abstract_checker
class Animal:
    @abstract
    def speak(self):
        pass
    
    def __init__(self):
        print("动物初始化")


# ============== 自动实现接口方法 ==============

def implement_interface(interface_cls: Type):
    """
    接口实现装饰器
    
    自动为类填充接口的默认实现
    如果类没有实现接口方法,使用接口的默认实现
    """
    def decorator(cls: Type) -> Type:
        # 获取接口中定义的方法
        interface_methods = {
            name: getattr(interface_cls, name)
            for name in dir(interface_cls)
            if callable(getattr(interface_cls, name, None)) and not name.startswith('_')
        }
        
        # 为类添加未实现的方法
        for name, method in interface_methods.items():
            if not hasattr(cls, name):
                setattr(cls, name, method)
        
        return cls
    return decorator


class IProvider:
    def get_data(self):
        return "默认数据"
    
    def process(self, data):
        return f"处理: {data}"


@implement_interface(IProvider)
class CustomProvider:
    def get_data(self):
        return "自定义数据"


# ============== 测试运行 ==============

if __name__ == "__main__":
    print("=" * 50)
    print("2. 类装饰器")
    print("=" * 50)
    
    # 测试1: 简单类装饰器
    print("\n--- 测试: add_method ---")
    obj = SimpleClass(10)
    print(obj.new_method())
    
    # 测试2: 类注册
    print("\n--- 测试: register ---")
    print(f"注册的类: {class_registry}")
    print(f"PluginA: {class_registry['plugin_a'].registered_name}")
    
    # 测试3: Singleton
    print("\n--- 测试: singleton ---")
    db1 = Database()
    db2 = Database()
    print(f"db1 is db2: {db1 is db2}")
    
    # 测试4: 惰性属性
    print("\n--- 测试: lazy_property ---")
    loader = DataLoader("远程服务器")
    print("第一次访问:")
    data1 = loader.expensive_data
    print(f"data: {data1}")
    print("第二次访问:")
    data2 = loader.expensive_data
    print("第二次没有打印 '正在加载...'")
    
    # 测试5: 自动接口实现
    print("\n--- 测试: implement_interface ---")
    provider = CustomProvider()
    print(f"get_data: {provider.get_data()}")
    print(f"process: {provider.process('test')}")
    
    print("\n" + "=" * 50)
    print("类装饰器学习完成!")
    print("=" * 50)