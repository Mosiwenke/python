"""
第10章: 动态代码生成与编译
=====================================

Python可以在运行时动态生成和执行代码.
使用compile, exec, eval等内置函数.
"""

import sys
import types
import compileall
import dis


# ============== 基础动态编译 ==============

def basic_compile():
    """基础动态编译"""
    
    code_string = """
result = 1 + 2
message = f"计算结果: {result}"
"""
    
    compiled = compile(code_string, "<string>", "exec")
    
    local_vars = {}
    exec(compiled, {}, local_vars)
    
    print(f"result: {local_vars['result']}")
    print(f"message: {local_vars['message']}")


# ============== 动态函数创建 ==============

def create_function():
    """动态创建函数"""
    
    code_string = """
def dynamic_add(a, b):
    \"\"\"动态创建的加法函数\"\"\"
    return a + b
"""
    
    compiled = compile(code_string, "<string>", "exec")
    namespace = {}
    exec(compiled, namespace)
    
    func = namespace['dynamic_add']
    print(f"函数: {func}")
    print(f"调用: {func(3, 5)}")
    print(f"文档: {func.__doc__}")


# ============== 动态类创建 ==============

def create_class():
    """动态创建类"""
    
    code_string = """
class DynamicClass:
    def __init__(self, value):
        self.value = value
    
    def get_value(self):
        return self.value * 2
"""
    
    compiled = compile(code_string, "<string>", "exec")
    namespace = {}
    exec(compiled, namespace)
    
    cls = namespace['DynamicClass']
    obj = cls(10)
    print(f"类: {cls}")
    print(f"值: {obj.get_value()}")


# ============== 使用types创建函数 ==============

def create_function_with_types():
    """使用types模块创建函数"""
    
    args = ('a', 'b')
    body = 'return a + b'
    
    code = compile(f'def _temp({", ".join(args)}): {body}', '<string>', 'exec')
    
    namespace = {}
    exec(code, namespace)
    func = namespace['_temp']
    
    print(f"函数: {func}")
    print(f"调用: {func(2, 3)}")


# ============== Lambda工厂 ==============

def make_lambda(param_names: list, expression: str):
    """创建lambda表达式"""
    
    args = ', '.join(param_names)
    code = compile(f'lambda {args}: {expression}', '<string>', 'eval')
    
    return eval(code)


# ============== 动态方法添加 ==============

def add_method_to_class():
    """动态添加方法到类"""
    
    class MyClass:
        def __init__(self, value):
            self.value = value
    
    def new_method(self):
        return self.value * 10
    
    MyClass.new_method = new_method
    
    obj = MyClass(5)
    print(f"调用新方法: {obj.new_method()}")


# ============== 动态属性 ==============

def dynamic_property(func):
    """动态属性装饰器"""
    return property(func)


# ============== 代码模板 ==============

TEMPLATE_CLASS = """
class {class_name}:
    \"\"\"动态生成的类\"\"\"
    
    def __init__(self, {init_params}):
        {init_body}
    
    def {method_name}(self):
        return {method_body}
"""

TEMPLATE_FUNCTION = """
def {func_name}({params}):
    \"\"\"动态创建的函数\"\"\"
    {body}
"""


def generate_class(class_name: str, fields: dict) -> type:
    """根据字段动态生成类"""
    
    init_params = ', '.join(fields.keys())
    init_body = '\n        '.join([
        f'self.{k} = {k}'
        for k in fields.keys()
    ])
    
    code = TEMPLATE_CLASS.format(
        class_name=class_name,
        init_params=init_params,
        init_body=init_body,
        method_name='get_data',
        method_body='self.name, self.age'  # 返回元组
    )
    
    compiled = compile(code, '<string>', 'exec')
    namespace = {}
    exec(compiled, namespace)
    
    return namespace[class_name]


# ============== 运行时代码修改 ==============

def modify_code():
    """运行时修改代码"""
    
    original_code = compile("return 1 + 1", "<test>", "eval")
    print(f"原结果: {eval(original_code)}")
    
    new_code = compile("return 1 + 100", "<test>", "eval")
    print(f"修改后: {eval(new_code)}")


# ============== 安全执行 ==============

def safe_eval():
    """安全的eval - 只允许特定操作"""
    
    allowed_names = {
        'abs': abs,
        'min': min,
        'max': max,
        'sum': sum,
        'range': range,
        'len': len,
    }
    
    expressions = [
        "abs(-5)",
        "min(1, 2, 3)",
        "max(1, 2, 3)",
        "sum([1, 2, 3])",
    ]
    
    for expr in expressions:
        result = eval(expr, {"__builtins__": {}}, allowed_names)
        print(f"{expr} = {result}")


# ============== 测试运行 ==============

if __name__ == "__main__":
    print("=" * 50)
    print("10. 动态代码生成")
    print("=" * 50)
    
    # 测试1: 基础编译
    print("\n--- 1. 基础动态编译 ---")
    basic_compile()
    
    # 测试2: 动态函数
    print("\n--- 2. 动态函数创建 ---")
    create_function()
    create_function_with_types()
    
    # 测试3: Lambda工厂
    print("\n--- 3. Lambda工厂 ---")
    add = make_lambda(['x', 'y'], 'x + y')
    multiply = make_lambda(['x', 'y'], 'x * y')
    print(f"add(3, 4) = {add(3, 4)}")
    print(f"multiply(3, 4) = {multiply(3, 4)}")
    
    # 测试4: 动态类
    print("\n--- 4. 动态类创建 ---")
    User = generate_class('User', {'name': str, 'age': int})
    user = User("Alice", 30)
    print(f"User: {user.name}, {user.age}")
    print(f"get_data: {user.get_data()}")
    
    # 测试5: 动态方法
    print("\n--- 5. 动态方法 ---")
    add_method_to_class()
    
    # 测试6: 安全执行
    print("\n--- 6. 安全执行 ---")
    safe_eval()
    
    print("\n" + "=" * 50)
    print("动态代码生成学习完成!")
    print("=" * 50)