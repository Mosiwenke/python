"""
第19章: 装饰器模式与设计模式
=============================

Python中装饰器模式和常用设计模式的实现.
- 装饰器模式
- 单例模式
- 工厂模式
- 观察者模式
- 策略模式
"""

from functools import wraps
from typing import Callable, Any, List, Dict, Optional
import time


# ============== 装饰器模式 ==============

class Component:
    """组件接口"""
    
    def operation(self) -> str:
        raise NotImplementedError


class ConcreteComponent(Component):
    """具体组件"""
    
    def operation(self) -> str:
        return "ConcreteComponent"


class Decorator(Component):
    """装饰器基类"""
    
    def __init__(self, component: Component):
        self._component = component
    
    def operation(self) -> str:
        return self._component.operation()


class ConcreteDecorator(Decorator):
    """具体装饰器"""
    
    def operation(self) -> str:
        return f"({self._component.operation()})"


class TimingDecorator(Decorator):
    """计时装饰器"""
    
    def operation(self) -> str:
        start = time.perf_counter()
        result = self._component.operation()
        elapsed = time.perf_counter() - start
        return f"{result} [{elapsed:.3f}s]"


class LoggingDecorator(Decorator):
    """日志装饰器"""
    
    def operation(self) -> str:
        print("调用 operation")
        result = self._component.operation()
        print(f"结果: {result}")
        return result


def decorator_pattern_demo():
    """装饰器模式演示"""
    component = ConcreteComponent()
    
    decorated = ConcreteDecorator(component)
    print(f"基本装饰: {decorated.operation()}")
    
    timed = TimingDecorator(component)
    print(f"计时: {timed.operation()}")
    
    logged = LoggingDecorator(component)
    logged.operation()


# ============== 单例模式 ==============

class Singleton:
    """单例类"""
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if not self._initialized:
            self._initialized = True
            self._data = {}


class SingletonMeta(type):
    """单例元类"""
    _instances: Dict[type, object] = {}
    
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class Database(metaclass=SingletonMeta):
    """数据库单例"""
    
    def __init__(self):
        self.connected = False
    
    def connect(self):
        self.connected = True


def singleton_demo():
    """单例演示"""
    s1 = Singleton()
    s2 = Singleton()
    print(f"同一个实例: {s1 is s2}")
    
    db1 = Database()
    db2 = Database()
    print(f"同一个数据库: {db1 is db2}")


# ============== 工厂模式 ==============

class Product:
    """产品"""
    
    def execute(self) -> str:
        raise NotImplementedError


class ProductA(Product):
    def execute(self) -> str:
        return "ProductA"


class ProductB(Product):
    def execute(self) -> str:
        return "ProductB"


class Factory:
    """��厂"""
    
    _products: Dict[str, type] = {}
    
    @classmethod
    def register(cls, name: str, product_class: type):
        cls._products[name] = product_class
    
    @classmethod
    def create(cls, name: str) -> Product:
        if name not in cls._products:
            raise ValueError(f"未知产品: {name}")
        return cls._products[name]()


Factory.register("A", ProductA)
Factory.register("B", ProductB)


def factory_demo():
    """工厂演示"""
    product_a = Factory.create("A")
    product_b = Factory.create("B")
    print(f"产品A: {product_a.execute()}")
    print(f"产品B: {product_b.execute()}")


# ============== 观察者模式 ==============

class Observer:
    """观察者"""
    
    def update(self, event: str, data: Any):
        raise NotImplementedError


class Subject:
    """主题"""
    
    def __init__(self):
        self._observers: List[Observer] = []
    
    def attach(self, observer: Observer):
        self._observers.append(observer)
    
    def detach(self, observer: Observer):
        self._observers.remove(observer)
    
    def notify(self, event: str, data: Any):
        for observer in self._observers:
            observer.update(event, data)


class ConcreteObserver(Observer):
    """具体观察者"""
    
    def __init__(self, name: str):
        self.name = name
    
    def update(self, event: str, data: Any):
        print(f"[{self.name}] 收到: {event} - {data}")


class EventBus(Subject):
    """事件总线"""
    
    def __init__(self):
        super().__init__()
        self._events: Dict[str, List[Callable]] = {}
    
    def subscribe(self, event: str, callback: Callable):
        if event not in self._events:
            self._events[event] = []
        self._events[event].append(callback)
    
    def publish(self, event: str, data: Any = None):
        if event in self._events:
            for callback in self._events[event]:
                callback(data)
        self.notify(event, data)


def observer_pattern_demo():
    """观察者模式演示"""
    subject = Subject()
    
    observer1 = ConcreteObserver("观察者1")
    observer2 = ConcreteObserver("观察者2")
    
    subject.attach(observer1)
    subject.attach(observer2)
    
    subject.notify("事件A", {"data": 123})
    
    subject.detach(observer1)
    subject.notify("事件B", "更多数据")


# ============== 策略模式 ==============

class Strategy:
    """策略接口"""
    
    def execute(self, data: Any) -> Any:
        raise NotImplementedError


class StrategyA(Strategy):
    def execute(self, data: Any) -> Any:
        return f"策略A: {data} * 2"


class StrategyB(Strategy):
    def execute(self, data: Any) -> Any:
        return f"策略B: {data.upper()}"


class Context:
    """上下文"""
    
    def __init__(self, strategy: Strategy):
        self._strategy = strategy
    
    def set_strategy(self, strategy: Strategy):
        self._strategy = strategy
    
    def execute_strategy(self, data: Any) -> Any:
        return self._strategy.execute(data)


def strategy_demo():
    """策略模式演示"""
    context = Context(StrategyA())
    print(context.execute_strategy("hello"))
    
    context.set_strategy(StrategyB())
    print(context.execute_strategy("hello"))


# ============== 适配器模式 ==============

class Adaptee:
    """被适配者"""
    
    def specific_request(self) -> str:
        return "adaptee request"


class Target:
    """目标接口"""
    
    def request(self) -> str:
        raise NotImplementedError


class Adapter(Target):
    """适配器"""
    
    def __init__(self, adaptee: Adaptee):
        self._adaptee = adaptee
    
    def request(self) -> str:
        return f"适配器: {self._adaptee.specific_request()}"


def adapter_demo():
    """适配器演示"""
    adaptee = Adaptee()
    adapter = Adapter(adaptee)
    print(adapter.request())


# ============== 代理模式 ==============

class RealSubject:
    """真实主题"""
    
    def request(self) -> str:
        time.sleep(0.1)
        return "真实请求"


class ProxySubject:
    """代理主题"""
    
    def __init__(self):
        self._real_subject = None
    
    def request(self) -> str:
        if self._real_subject is None:
            self._real_subject = RealSubject()
        return self._real_subject.request()


def proxy_demo():
    """代理模式演示"""
    proxy = ProxySubject()
    print(proxy.request())


# ============== 命令模式 ==============

class Command:
    """命令"""
    
    def execute(self):
        raise NotImplementedError


class ConcreteCommand(Command):
    """具体命令"""
    
    def __init__(self, receiver, action):
        self._receiver = receiver
        self._action = action
    
    def execute(self):
        self._receiver.action(self._action)


class Receiver:
    """接收者"""
    
    def action(self, data):
        print(f"执行: {data}")


class CommandInvoker:
    """调用者"""
    
    def __init__(self):
        self._commands: List[Command] = []
    
    def add_command(self, command: Command):
        self._commands.append(command)
    
    def execute_commands(self):
        for command in self._commands:
            command.execute()


def command_demo():
    """命令模式演示"""
    receiver = Receiver()
    command = ConcreteCommand(receiver, "测试")
    
    invoker = CommandInvoker()
    invoker.add_command(command)
    invoker.execute_commands()


# ============== 测试运行 ==============

if __name__ == "__main__":
    print("=" * 50)
    print("19. 装饰器模式与设计模式")
    print("=" * 50)
    
    # 测试1: 装饰器模式
    print("\n--- 1. 装饰器模式 ---")
    decorator_pattern_demo()
    
    # 测试2: 单例模式
    print("\n--- 2. 单例模式 ---")
    singleton_demo()
    
    # 测试3: 工厂模式
    print("\n--- 3. 工厂模式 ---")
    factory_demo()
    
    # 测试4: 观察者模式
    print("\n--- 4. 观察者模式 ---")
    observer_pattern_demo()
    
    # 测试5: 策略模式
    print("\n--- 5. 策略模式 ---")
    strategy_demo()
    
    # 测试6: 适配器模式
    print("\n--- 6. 适配器模式 ---")
    adapter_demo()
    
    # 测试7: 代理模式
    print("\n--- 7. 代理模式 ---")
    proxy_demo()
    
    # 测试8: 命令模式
    print("\n--- 8. 命令模式 ---")
    command_demo()
    
    print("\n" + "=" * 50)
    print("设计模式学习完成!")
    print("=" * 50)