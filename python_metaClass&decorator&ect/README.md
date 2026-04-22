# Python 元编程与装饰器学习项目

这是一个用于探索 Python 元编程和装饰器边界能力的项目。

## 项目结构

```
project/
├── main.py              # 项目入口
├── __init__.py          # 包初始化
├── decorators/          # 装饰器模块
│   ├── 01_basic_decorators.py     # 基础函数装饰器
│   ├── 02_class_decorators.py     # 类装饰器
│   ├── 03_decorator_params.py   # 带参数装饰器
│   └── 04_class_decorator.py     # 类方式装饰器
└── metaclasses/         # 元类模块
    └── 05_metaclass.py          # 元类实现
```

## 学习内容

1. **基础函数装饰器** - `@decorator` 语法糖, `functools.wraps`
2. **类装饰器** - 修改类行为, 自动注册
3. **带参数装饰器** - 可配置装饰器
4. **装饰器堆叠** - 多个装饰器组合
5. **类方式装饰器** - 使用类实现装饰器
6. **元类** - 创建类的类
7. **描述符协议** - `__get__`, `__set__`, `__delete__`

## 运行示例

```bash
# 运行基础装饰器示例
python decorators/01_basic_decorators.py

# 运行类装饰器示例  
python decorators/02_class_decorators.py

# 运行元类示例
python metaclasses/05_metaclass.py
```

## 核心概念

- **装饰器**: 接收函数/类,返回包装后的函数/类
- **元类**: 创建类的类,控制类的创建行为
- **描述符**: 实现 `__get__`/`__set__` 的类属性

## 进一步学习

- 描述符协议详细实现
- 高级装饰器模式(装饰器类,装饰器工厂)
- `__slots__` 优化
- `abc.ABCMeta` 抽象类
- `enum.Enum` 源码分析