import time
import json

from 超 import 超


def _get_n(n):
    time.sleep(1)
    return n


@超
def f(x, y):
    xx = _get_n(x)
    yy = _get_n(y)
    return xx  * yy
assert f(1, 2) == 2
t = time.time()
assert f(3, 4) == 12
assert time.time() - t < 1.1
print('f pass')


@超
def f2(x):
    if x < 0:
        return -x
    return x
assert f2(-1) == 1
assert f2(1) == 1
assert f2(-1.5) == 1.5
print('f2 pass')


@超
def f3(x):
    s = 0
    for i in range(x):
        s += _get_n(i)
    return s
assert f3(0) == 0
t = time.time()
assert f3(10) == 45
assert time.time() - t < 1.1
print('f3 pass')


@超
def f4():
    0
assert f4() == None
print('f4 pass')


@超
def f5(li):
    return sum([*map(_get_n, li)]) + sum([_get_n(i**2) for i in li])
t = time.time()
assert f5([1,2,3]) == 6 + 14
assert time.time() - t < 1.1
print('f5 pass')


@超
def f6(x):
    return json.dumps([str(x)])
assert f6("x") == '["x"]'
print('f6 pass')


@超
def f7(x):
    return f'{_get_n(x)} {_get_n(x+1)} {_get_n(x+2)}'
t = time.time()
assert f7(1) == '1 2 3'
assert time.time() - t < 1.1
print('f7 pass')


@超
def f8(x):
    return [_get_n(x), _get_n(x+1), _get_n(x+2)]
t = time.time()
assert f8(4) == [4, 5, 6]
assert time.time() - t < 1.1
print('f8 pass')


@超
def f9(x):
    if x <= 1:
        return x
    return f9(x-1) + f9(x-2)
assert f9(13) == 233
print('f9 pass')
