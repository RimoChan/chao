import sys
import inspect
import threading
from concurrent.futures import ThreadPoolExecutor
from typing import Callable


_无 = object()


_易位 = {
    '__add__': '__radd__',
    '__sub__': '__rsub__',
    '__mul__': '__rmul__',
    '__matmul__': '__rmatmul__',
    '__truediv__': '__rtruediv__',
    '__floordiv__': '__rfloordiv__',
    '__mod__': '__rmod__',
    '__pow__': '__rpow__'
}

_pool = ThreadPoolExecutor(2**31)

def 用(x):
    if isinstance(x, list):
        return [用(i) for i in x]
    if isinstance(x, tuple):
        return tuple(用(i) for i in x)
    if isinstance(x, dict):
        return {k: 用(v) for k, v in x.items()}
    if isinstance(x, 符号):
        assert x._引用 is not _无
        return x._引用
    return x


def _批量解引用(解):
    for i in range(128):
        解a = []
        解b = []
        for i in 解:
            if isinstance(i, (list, tuple)):
                解b += [j for j in i]
            elif isinstance(i, dict):
                解b += [j for j in i.values()]
            elif isinstance(i, 符号) and i._引用 is _无:
                解a.append(i)
        解 = 解a + 解b
        if not 解b:
            break
    [*_pool.map(lambda x: x._解引用(), 解)]


class 符号:
    __slots__ = ('_名字', '_来源', '_引用', '_锁')
    def __init__(self, 名字=None, *, 来源=None, 引用=_无):
        self._名字 = 名字
        self._来源 = 来源
        self._引用 = 引用
        self._锁 = threading.Lock()
    def _古代魔法(method: str):
        def _f(self, *li, **d):
            return 符号(来源=(self, method, li, d))
        return _f
    def _现代魔法(method: str):
        def _f(self):
            self._解引用()
            return getattr(self._引用, method)()
        return _f
    def _解引用(self):
        with self._锁:
            if self._引用 is not _无:
                return
            if self._来源 is None:
                raise ValueError(f'<符号 {self._名字}>未定义。')
            a, method, li, d = self._来源
            _批量解引用([i for i in (li + tuple(d.values()) + (a, ))])
            用a = 用(a)
            # self._引用 = getattr(用a, method)(*[用(i) for i in li], **{k: 用(v) for k, v in d.items()})
            self._引用 = getattr(用a.__class__, method)(用a, *[用(i) for i in li], **{k: 用(v) for k, v in d.items()})
            if self._引用 is NotImplemented and method in _易位:
                assert len(li) == 1 and not d
                用li0 = 用(li[0])
                self._引用 = getattr(用li0.__class__, _易位[method])(用li0, 用a)
            assert not isinstance(self._引用, 符号), f'解引用{显现(self)}出现了问题 (调用{method}，输入{显现(li)} {显现(d)})。'
    def __index__(self):
        self._解引用()
        return self._引用.__index__()
    for _k in ('__call__', '__getitem__', '__getattr__', '__iter__', '__neg__') + ('__lt__', '__le__', '__eq__', '__ne__', '__gt__', '__ge__') + tuple(_易位.keys()) + tuple(_易位.values()):
        locals()[_k] = _古代魔法(_k)
    for _k in ('__index__', '__iter__', '__bool__', '__str__'):
        locals()[_k] = _现代魔法(_k)
    L = tuple(locals().keys())
    def __getattribute__(self, k):
        if k in 符号.__slots__ + 符号.L:
            return super().__getattribute__(k)
        return 符号(来源=(self, '__getattribute__', (k,), {}))


def 显现(x):
    数学 = {
        '__add__': '+',
        '__sub__': '-',
        '__mul__': '*',
        '__matmul__': '@',
        '__truediv__': '/',
        '__floordiv__': '//',
        '__mod__': '%',
        '__pow__': '**',
    }
    def _显现(x):
        if not isinstance(x, 符号):
            return repr(x)
        if x._来源 is None:
            return x._名字
        a, method, li, d = x._来源
        if method in 数学:
            assert len(li) == 1 and not d
            return f'({_显现(a)}{数学[method]}{repr(li[0])})'
        li_s = ','.join(map(repr, li))
        d_s = ','.join(f'{k}={repr(v)}' for k, v in d.items())
        all_s = ','.join(filter(None, (li_s, d_s)))
        if not all_s or all_s[0] != '(' or all_s[-1] != ')':
            all_s = f'({all_s})'
        if method == '__call__':
            return f'{_显现(a)}{all_s}'
        else:
            return f'{_显现(a)}.{method}{all_s}'
    符号.__repr__ = _显现
    r = _显现(x)
    del 符号.__repr__
    return r


_module锁 = {}


def 超(f: Callable):
    signature = inspect.signature(f)
    module = sys.modules[f.__module__]
    _module锁.setdefault(f.__module__, threading.Lock())
    def 新f(*li, **d):
        with _module锁[f.__module__]:
            b = __builtins__.copy()
            b.update(module.__dict__)
            幻影 = {k: 符号(k, 引用=v) for k, v in b.items()}
            原 = module.__dict__.copy()
            for k, v in 幻影.items():
                module.__dict__[k] = v
            输入 = {k: 符号(k) for k in signature.parameters}
            for k, v in signature.bind(*li, **d).arguments.items():
                assert not isinstance(v, 符号)
                输入[k]._引用 = v
            res = f(**输入)
            # print('显现', 显现(res))
            for k in 幻影:
                if k in 原:
                    module.__dict__[k] = 原[k]
                else:
                    del module.__dict__[k]
        _批量解引用([res])
        return 用(res)
    return 新f
