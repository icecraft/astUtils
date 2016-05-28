from functools import wraps
import logging
import inspect


def logWrap(func):
    @wraps(func)
    def wrap(*args, **kwargs):
        logging.error('now enter')
        res = func(*args, **kwargs)
        logging.error('now exit')
        return res
    return wrap


class CustomAttr:
    def __init__(self, obj, wrapFunc=logWrap):
        self.attr = "a custom function attribute"
        self.obj = obj
        self.wrapFunc = wrapFunc
        self._instance = None
        
    def __call__(self, *args, **kwargs):
        self._instance = self.obj(*args, **kwargs)
        return self
        
    def __getattr__(self, attr):
        attr_1 = getattr(self._instance, attr)
        if inspect.ismethod(attr_1):
            return self.wrapFunc(attr_1)
        else:
            return attr_1     

        
def methodWrap(wrapFunc):
    """ 
伯乐在线：Python高级特性（2）：Closures、Decorators和functools
有用 setattr 实现的类方法的装饰器
""" 
    def decorator(cls):
        return CustomAttr(cls, wrapFunc)
    return decorator


def pp(*args, **kwargs):
    print args, kwargs

    
@methodWrap(logWrap)
class B(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def ad1(self, x):
        return x + 1

