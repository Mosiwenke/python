from unittest import TestCase


def my_func(*args, **kwargs):
    print(type(args), type(kwargs))
    print(args, kwargs)


def my_func2(args, kwargs):
    print(type(args), type(kwargs))
    print(args, kwargs)


class TestFunc(TestCase):
    def test_func(self, args=(1, 2, 3), kwargs=None):
        if kwargs is None:
            kwargs = {"a": 1, "b": 2}
        my_func(args, kwargs)
        my_func(args=args, kwargs=kwargs)
        my_func(*args, **kwargs)
        my_func2(args, kwargs)
        my_func2(args=args, kwargs=kwargs)
        # self.assertRaises其实实现的手动重载(函数式使用和上下文管理器使用, 只取决于assertRaises的args是否为空
        self.assertRaises(Exception, my_func2, *args, **kwargs)  # 这里的*args是把args解包了, 后续有callable_obj, *args = args
        with self.assertRaises(Exception) as context:
            my_func2(*args, **kwargs)
        self.assertIn("my_func2() got an unexpected keyword argument 'a'", str(context.exception))
