"""
第6章: 描述符协议 (Descriptor Protocol)
========================================

描述符是Python中属性访问的底层机制.
任何定义了 __get__, __set__, __delete__ 其中一个的类都是描述符.

核心概念:
- __get__: 属性访问
- __set__: 属性设置
- __delete__: 属性删除
- property 内部就是使用描述符实现的
"""

from typing import Any, Callable, Optional
import time


# ============== 基础描述符 ==============

class Descriptor:
    """
    基础描述符 - 展示描述符的基本结构
    
    所有描述符方法第一个参数是 self(描述符实例)
    第二个参数是 obj(被访问的实例) 或 objtype(类)
    """
    
    def __get__(self, obj, objtype=None):
        print(f"[Descriptor.__get__] 访问属性")
        return "描述符值"
    
    def __set__(self, obj, value):
        print(f"[Descriptor.__set__] 设置值: {value}")
    
    def __delete__(self, obj):
        print(f"[Descriptor.__delete__] 删除属性")


class MyClass:
    descriptor = Descriptor()


# ============== 属性验证描述符 ==============

class ValidatedAttribute:
    """
    属性验证描述符
    
    在设置属性时自动验证值的合法性
    """
    
    def __init__(self, name: str, validator: Callable[[Any], bool]):
        self.name = name
        self.validator = validator
        self.attr_name = f'_{name}'
    
    def __get__(self, obj, objtype=None):
        return getattr(obj, self.attr_name)
    
    def __set__(self, obj, value):
        if not self.validator(value):
            raise ValueError(
                f"属性 {self.name} 验证失败: {value}"
            )
        setattr(obj, self.attr_name, value)


class Person:
    name = ValidatedAttribute('name', lambda x: isinstance(x, str) and len(x) > 0)
    age = ValidatedAttribute('age', lambda x: isinstance(x, int) and 0 <= x <= 150)
    
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age


# ============== 只读属性描述符 ==============

class ReadOnly:
    """只读属性描述符 - 设置后不能修改"""
    
    def __init__(self, name: str, default: Any = None):
        self.name = name
        self.attr_name = f'_{name}'
        self.default = default
    
    def __get__(self, obj, objtype=None):
        value = getattr(obj, self.attr_name, self.default)
        if value is None:
            raise AttributeError(f"只读属性 {self.name} 未设置")
        return value
    
    def __set__(self, obj, value):
        if hasattr(obj, self.attr_name):
            raise AttributeError(f"只读属性 {self.name} 不能修改")
        setattr(obj, self.attr_name, value)


class Config:
    api_key = ReadOnly('api_key')
    
    def __init__(self, api_key: str):
        self.api_key = api_key


# ============== 惰性计算描述符 ==============

class Lazy:
    """
    惰性计算描述符 - 第一次访问时计算
    
    类似于 Django 的 cached_property
    """
    
    def __init__(self, func: Callable):
        self.func = func
        self.attr_name = f'_lazy_{func.__name__}'
    
    def __get__(self, obj, objtype=None):
        if not hasattr(obj, self.attr_name):
            print(f"[Lazy] 首次计算: {self.func.__name__}")
            value = self.func(obj)
            setattr(obj, self.attr_name, value)
        return getattr(obj, self.attr_name)


class DataService:
    @Lazy
    def large_data(self):
        """模拟大��数据加载"""
        return list(range(1000))


# ============== 类型检查描述符 ==============

class TypeChecked:
    """
    类型检查描述符
    
    确保属性是指定类型
    """
    
    def __init__(self, expected_type: type):
        self.expected_type = expected_type
    
    def __set__(self, obj, value):
        if not isinstance(value, self.expected_type):
            raise TypeError(
                f"期望 {self.expected_type.__name__}, 实际 {type(value).__name__}"
            )
        setattr(obj, f'_{self.expected_type.__name__}_{id(self)}', value)


class TypedClass:
    string_prop = TypeChecked(str)
    int_prop = TypeChecked(int)


# ============== 日志描述符 ==============

class Logged:
    """
    日志描述符 - 记录属性访问和修改
    
    展示描述符如何拦截所有属性操作
    """
    
    def __init__(self, name: str):
        self.name = name
        self.attr_name = f'_{name}'
        self._track_changes = {}
    
    def __get__(self, obj, objtype=None):
        value = getattr(obj, self.attr_name, '<未设置>')
        print(f"[Logged] 读取 {self.name} = {value}")
        return value
    
    def __set__(self, obj, value):
        old_value = getattr(obj, self.attr_name, '<未设置>')
        print(f"[Logged] 修改 {self.name}: {old_value} -> {value}")
        
        # 记录变更历史
        if obj not in self._track_changes:
            self._track_changes[obj] = []
        self._track_changes[obj].append((old_value, value))
        
        setattr(obj, self.attr_name, value)


class Tracked:
    username = Logged('username')
    email = Logged('email')


# ============== 单位转换描述符 ==============

class UnitConverter:
    """
    单位转换描述符
    
    自动在内部单位和显示单位之间转换
    """
    
    def __init__(self, name: str, to_base: Callable, from_base: Callable):
        self.name = name
        self.to_base = to_base    # 显示单位 -> 内部单位
        self.from_base = from_base  # 内部单位 -> 显示单位
        self.attr_name = f'_{name}_base'
    
    def __get__(self, obj, objtype=None):
        base_value = getattr(obj, self.attr_name, 0)
        return self.from_base(base_value)
    
    def __set__(self, obj, value):
        base_value = self.to_base(value)
        setattr(obj, self.attr_name, base_value)


class Temperature:
    celsius = UnitConverter(
        'celsius',
        to_base=lambda c: c,  # 摄氏度就是内部单位
        from_base=lambda c: c
    )
    
    fahrenheit = UnitConverter(
        'fahrenheit',
        to_base=lambda f: (f - 32) * 5 / 9,
        from_base=lambda c: c * 9 / 5 + 32
    )
    
    kelvin = UnitConverter(
        'kelvin',
        to_base=lambda k: k - 273.15,
        from_base=lambda k: k + 273.15
    )


# ============== 范围限制描述符 ==============

class Range:
    """
    范围限制描述符 - 限制数值在指定范围内
    """
    
    def __init__(self, name: str, min_val: float = None, max_val: float = None):
        self.name = name
        self.min_val = min_val
        self.max_val = max_val
        self.attr_name = f'_{name}'
    
    def __get__(self, obj, objtype=None):
        return getattr(obj, self.attr_name)
    
    def __set__(self, obj, value):
        if self.min_val is not None and value < self.min_val:
            raise ValueError(f"{self.name} 不能小于 {self.min_val}")
        if self.max_val is not None and value > self.max_val:
            raise ValueError(f"{self.name} 不能大于 {self.max_val}")
        setattr(obj, self.attr_name, value)


class Score:
    health = Range('health', 0, 100)
    mana = Range('mana', 0, 100)


# ============== 模拟 property 实现 ==============

class MyProperty:
    """
    手动实现 @property 装饰器的效果
    
    展示 property 内部机制
    """
    
    def __init__(self, fget: Callable = None, fset: Callable = None, fdel: Callable = None):
        self.fget = fget
        self.fset = fset
        self.fdel = fdel
    
    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        if self.fget is None:
            raise AttributeError("未定义 getter")
        return self.fget(obj)
    
    def __set__(self, obj, value):
        if self.fset is None:
            raise AttributeError("未定义 setter")
        self.fset(obj, value)
    
    def __delete__(self, obj):
        if self.fdel is None:
            raise AttributeError("未定义 deleter")
        self.fdel(obj)
    
    def setter(self, fset: Callable):
        """支持 @property.setter 语法"""
        return MyProperty(self.fget, fset, self.fdel)
    
    def deleter(self, fdel: Callable):
        """支持 @property.deleter 语法"""
        return MyProperty(self.fget, self.fset, fdel)


class Circle:
    def __init__(self, radius: float):
        self._radius = radius
    
    @MyProperty
    def radius(self):
        return self._radius
    
    @radius.setter
    def radius(self, value):
        if value < 0:
            raise ValueError("半径不能为负")
        self._radius = value
    
    @property
    def area(self):
        return 3.14159 * self._radius ** 2


# ============== 描述符优先级 ==============

class Priority:
    """测试描述符优先级"""
    
    data = '类属性'


class InstanceData:
    """实例属性描述符"""
    
    def __get__(self, obj, objtype=None):
        return "描述符返回值"
    
    def __set__(self, obj, value):
        print(f"描述符拦截设置: {value}")


class PriorityTest:
    descriptor = InstanceData()
    data = '类属性'


# ============== 测试运行 ==============

if __name__ == "__main__":
    print("=" * 50)
    print("6. 描述符协议")
    print("=" * 50)
    
    # 测试1: 基础描述符
    print("\n--- 测试: 基础描述符 ---")
    obj = MyClass()
    print(f"访问: {obj.descriptor}")
    obj.descriptor = "新值"
    print(f"设置后: {obj.descriptor}")
    
    # 测试2: 属性验证
    print("\n--- 测试: ValidatedAttribute ---")
    person = Person("Alice", 30)
    print(f"Person: {person.name}, {person.age}")
    try:
        person.age = -5
    except ValueError as e:
        print(f"验证失败: {e}")
    
    # 测试3: 只读属性
    print("\n--- 测试: ReadOnly ---")
    config = Config("secret-key-123")
    print(f"api_key: {config.api_key}")
    try:
        config.api_key = "new-key"
    except AttributeError as e:
        print(f"错误: {e}")
    
    # 测试4: 惰性计算
    print("\n--- 测试: Lazy ---")
    service = DataService()
    print("第一次访问:")
    data1 = service.large_data
    print(f"长度: {len(data1)}")
    print("第二次访问:")
    data2 = service.large_data
    print("没有重新计算")
    
    # 测试5: 温度转换
    print("\n--- 测试: UnitConverter ---")
    temp = Temperature()
    temp.celsius = 0
    print(f"0°C = {temp.fahrenheit:.2f}°F = {temp.kelvin:.2f}K")
    temp.fahrenheit = 32
    print(f"32°F = {temp.celsius:.2f}°C")
    
    # 测试6: 范围限制
    print("\n--- 测试: Range ---")
    score = Score()
    score.health = 100
    print(f"health: {score.health}")
    try:
        score.health = -10
    except ValueError as e:
        print(f"错误: {e}")
    
    # 测试7: 优先级
    print("\n--- 测试: 描述符优先级 ---")
    # 实例属性 > 描述符 > 类属性
    print(f"PriorityTest.data: {PriorityTest.data}")
    
    print("\n" + "=" * 50)
    print("描述符协议学习完成!")
    print("=" * 50)