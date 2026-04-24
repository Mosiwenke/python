"""
第21章: 数据类与属性
=============================

Python数据类(dataclass)和属性系统.
- dataclass
- field
- __post_init__
- 属性别名
"""

from dataclasses import dataclass, field, fields, asdict, astuple, replace, InitVar
from typing import List, Optional, Any, ClassVar


# ============== 基础数据类 ==============

@dataclass
class User:
    """用户数据类"""
    id: int
    name: str
    email: str = "unknown"


def basic_dataclass():
    """基础数据类演示"""
    user = User(1, "Alice", "alice@example.com")
    print(f"用户: {user}")
    print(f"id: {user.id}, name: {user.name}")


# ============== 带默认值 ==============

@dataclass
class Person:
    """带默认值"""
    name: str = "Unknown"
    age: int = 0


def default_demo():
    """默认值演示"""
    p1 = Person()
    p2 = Person("Bob", 25)
    print(f"p1: {p1}")
    print(f"p2: {p2}")


# ============== field ==============

@dataclass
class Product:
    """带field"""
    id: int
    name: str
    price: float = field(default=0.0, compare=False)
    tags: List[str] = field(default_factory=list)


def field_demo():
    """field演示"""
    p1 = Product(1, "Widget")
    p2 = Product(2, "Gadget", 9.99, ["sale"])
    print(f"p1: {p1}")
    print(f"p2: {p2}")
    
    for f in fields(Product):
        print(f"field: {f.name}, {f.type}")


# ============== __post_init__ ==============

@dataclass
class Rectangle:
    """矩形 - 后处理"""
    width: float
    height: float
    area: float = field(init=False)
    
    def __post_init__(self):
        self.area = self.width * self.height


def post_init_demo():
    """post_init演示"""
    r = Rectangle(5, 3)
    print(f"矩形: {r}")
    print(f"面积: {r.area}")


# ============== 工厂字段 ==============

@dataclass
class Company:
    """公司 - 工厂"""
    name: str
    employees: List[str] = field(default_factory=list)
    
    def add_employee(self, name: str):
        self.employees.append(name)


def factory_demo():
    """工厂演示"""
    c = Company("TechCorp")
    c.add_employee("Alice")
    c.add_employee("Bob")
    print(f"公司: {c}")


# ============== 不可变数据类 ==============

@dataclass(frozen=True)
class Point:
    """不可变点"""
    x: float
    y: float


def frozen_demo():
    """不可变演示"""
    p1 = Point(1, 2)
    print(f"点: {p1}")
    
    try:
        p1.x = 10
    except dataclasses.FrozenError:
        print("不可变,不能修改")


# ============== 排序 ==============

@dataclass(order=True)
class OrderedItem:
    """可排序"""
    id: int
    name: str = ""
    price: float = 0.0


def order_demo():
    """排序演示"""
    items = [
        OrderedItem(2, "B", 5.0),
        OrderedItem(1, "A", 3.0),
        OrderedItem(3, "C", 2.0),
    ]
    
    sorted_items = sorted(items)
    for item in sorted_items:
        print(item)


# ============== slots ==============

@dataclass(slots=True)
class SlotItem:
    """slots数据类"""
    id: int
    name: str


def slots_demo():
    """slots演示"""
    item = SlotItem(1, "Test")
    print(f"item: {item}")


# ============== asdict/astuple ==============

def conversion_demo():
    """转换演示"""
    user = User(1, "Alice", "alice@example.com")
    
    print(f"asdict: {asdict(user)}")
    print(f"astuple: {astuple(user)}")


# ============== replace ==============

def replace_demo():
    """replace演示"""
    user = User(1, "Alice", "alice@example.com")
    
    user2 = replace(user, name="Bob")
    print(f"原用户: {user}")
    print(f"新用户: {user2}")


# ============== InitVar ==============

@dataclass
class Database:
    """带InitVar"""
    url: str
    port: InitVar[int] = 5432
    connected: bool = field(default=False, init=False)
    
    def __post_init__(self, port: int):
        self.url = f"{self.url}:{port}"
        self.connected = True


def initvar_demo():
    """InitVar演示"""
    db = Database("postgresql")
    print(f"数据库: {db}")


# ============== 多继承 ==============

@dataclass
class BaseModel:
    """基类"""
    id: int
    created_at: str = "now"


@dataclass
class Event(BaseModel):
    """事件类"""
    title: str = ""


def inheritance_demo():
    """继承演示"""
    event = Event(1, title="Party")
    print(f"事件: {event}")


# ============== 混合字段类型 ==============

@dataclass
class MixedClass:
    """混合类型"""
    data: Any
    items: List[int] = field(default_factory=list)
    callback: Optional[callable] = None


def mixed_demo():
    """混合演示"""
    obj = MixedClass(data="test", items=[1, 2, 3])
    print(f"对象: {obj}")


# ============== 类变量 ==============

@dataclass
class Config:
    """配置类"""
    VERSION: ClassVar[str] = "1.0"
    name: str = ""
    
    @classmethod
    def get_version(cls) -> str:
        return cls.VERSION


def classvar_demo():
    """类变量演示"""
    print(f"版本: {Config.get_version()}")
    
    c1 = Config("test1")
    c2 = Config("test2")
    print(f"c1_VERSION: {c1.VERSION}")
    print(f"c2_VERSION: {c2.VERSION}")


# ============== 属性别名 ==============

@dataclass
class PersonInfo:
    """个人信息 - 别名"""
    first_name: str = ""
    last_name: str = ""
    
    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"


def property_demo():
    """属性演示"""
    p = PersonInfo("John", "Doe")
    print(f"全名: {p.full_name}")


# ============== 自定义字段验证 ==============

@dataclass
class ValidatedData:
    """验证数据"""
    id: int = 0
    name: str = ""
    email: str = ""
    
    def __post_init__(self):
        if not self.name:
            raise ValueError("name不能为空")
        
        if "@" not in self.email:
            raise ValueError("email无效")


def validation_demo():
    """验证演示"""
    try:
        data = ValidatedData(1, "", "invalid")
    except ValueError as e:
        print(f"错误: {e}")


# ============== 测试运行 ==============

if __name__ == "__main__":
    print("=" * 50)
    print("21. 数据类与属性")
    print("=" * 50)
    
    # 测试1: 基础
    print("\n--- 1. 基础数据类 ---")
    basic_dataclass()
    
    # 测试2: 默认值
    print("\n--- 2. 默认值 ---")
    default_demo()
    
    # 测试3: field
    print("\n--- 3. field ---")
    field_demo()
    
    # 测试4: post_init
    print("\n--- 4. post_init ---")
    post_init_demo()
    
    # 测试5: 工厂
    print("\n--- 5. 工厂字段 ---")
    factory_demo()
    
    # 测试6: 不可变
    print("\n--- 6. 不可变 ---")
    frozen_demo()
    
    # 测试7: 排序
    print("\n--- 7. 排序 ---")
    order_demo()
    
    # 测试8: slots
    print("\n--- 8. slots ---")
    slots_demo()
    
    # 测试9: 转换
    print("\n--- 9. asdict/astuple ---")
    conversion_demo()
    
    # 测试10: replace
    print("\n--- 10. replace ---")
    replace_demo()
    
    # 测试11: InitVar
    print("\n--- 11. InitVar ---")
    initvar_demo()
    
    # 测试12: 继承
    print("\n--- 12. 多继承 ---")
    inheritance_demo()
    
    # 测试13: 混合类型
    print("\n--- 13. 混合类型 ---")
    mixed_demo()
    
    # 测试14: 类变量
    print("\n--- 14. 类变量 ---")
    classvar_demo()
    
    # 测试15: 属性
    print("\n--- 15. 属性 ---")
    property_demo()
    
    # 测试16: 验证
    print("\n--- 16. 验证 ---")
    validation_demo()
    
    print("\n" + "=" * 50)
    print("数据类学习完成!")
    print("=" * 50)