"""
第38章: 面向对象设计原则
=============================

SOLID设计原则.
- 单一职责
- 开闭原则
- 里氏替换
- 接口隔离
- 依赖倒置
"""

from abc import ABC, abstractmethod
from typing import List


# ============== 单一职责 ==============

class User:
    """用户类"""
    name: str = ""
    email: str = ""


class UserRepository:
    """用户仓库 - 单一职责"""
    def save(self, user: User): pass
    def get(self, id): pass


class UserService:
    """用户服务 - 单一职责"""
    def __init__(self, repo: UserRepository):
        self.repo = repo
    
    def register(self, user: User):
        self.repo.save(user)


def sr_demo():
    """单一职责"""
    repo = UserRepository()
    service = UserService(repo)
    print("单一职责: 分离关注点")


# ============== 开闭原则 ==============

class Shape(ABC):
    """形状"""
    @abstractmethod
    def area(self): pass


class Circle(Shape):
    def __init__(self, r): self.r = r
    def area(self): return 3.14 * self.r ** 2


class Rectangle(Shape):
    def __init__(self, w, h): self.w, self.h = w, h
    def area(self): return self.w * self.h


def ocp_demo():
    """开闭 - 对扩展开放,对修改关闭"""
    shapes: List[Shape] = [Circle(1), Rectangle(2, 3)]
    total = sum(s.area() for s in shapes)
    print(f"总面积: {total}")


# ============== 里氏替换 ==============

class Bird:
    def fly(self): pass


class Duck(Bird):
    def fly(self): print("鸭子飞")


def lsp_demo():
    """里氏替换 - 子类替换父类"""
    def make_fly(bird: Bird): bird.fly()
    make_fly(Duck())


# ============== 接口隔离 ==============

class Printer:
    def print(self): pass


class Scanner:
    def scan(self): pass


class AllInOne(Printer, Scanner):
    def print(self): pass
    def scan(self): pass


def isp_demo():
    """接口隔离 - 使用小接口"""
    print("接口隔离: 分离大接口")


# ============== 依赖倒置 ==============

class Message:
    content: str = ""


class IMessageSender(ABC):
    @abstractmethod
    def send(self, msg): pass


class EmailSender(IMessageSender):
    def send(self, msg): print(f"发送: {msg.content}")


class Notification:
    def __init__(self, sender: IMessageSender):
        self.sender = sender
    
    def notify(self, msg):
        self.sender.send(msg)


def dip_demo():
    """依赖倒置 - 依赖抽象"""
    sender = EmailSender()
    notif = Notification(sender)
    notif.notify(Message())


if __name__ == "__main__":
    print("=" * 50)
    print("38. 面向对象设计原则")
    print("=" * 50)
    sr_demo()
    ocp_demo()
    lsp_demo()
    isp_demo()
    dip_demo()
    print("=" * 50)