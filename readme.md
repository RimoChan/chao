# 【超】Python魔法加速器！


大家遇到Python跑得很慢的时候，会想用多线程优化一下吗？

但是用手把代码改成多线程很麻烦！

好在聪明的莉沫酱发明了「超」，它可以在运行时自动将普通代码改成多线程代码！


## 样例

首先我们来看这一段代码，功能是计算两个数的和: 

```python
def f1(a):
    time.sleep(1)
    return a

def f2(a):
    time.sleep(1)
    return a

def f(x, y):
    xx = f1(x)
    yy = f2(y)
    return xx + yy
```

它显然需要执行2秒，太慢了！

接下来我们给`f`加上`超`，像是这样: 

```python
from 超 import 超
@超
def f(x, y):
    xx = f1(x)
    yy = f2(y)
    return xx + yy
t = time.time()
f(1, 2)
print(time.time() - t)  # 1.0019426345825195
```

现在它只需要执行1秒了！


## 原理

原理其实很简单，拥有`超`的函数在执行时会将函数可见的全局变量、函数输入、builtins全部替换成符号对象，然后用这些符号对象假装执行一次函数，直到遇到函数结束或者符号对象不支持的操作。遇到这些操作的时候，就把符号对象展开成普通对象，然后再继续运行，最后拿到结果就好了。

我们用上面的样例来理解一下: 

1. 首先执行`f(1, 2)`，但是这个时候输入被替换成了符号，所以实际上执行的是`f(符号x，符号y)`。

2. 进到函数里面，执行`xx = f1(x)`，但是这个时候`f1`也被替换成了符号，所以`xx`运行时的值是`符号f1.__call__(符号x)`。这个符号是复合符号，它跟踪了它是由哪几个符号组成的，因此未来可以把它还原成普通对象。

3. 接下来执行`yy = f2(y)`，同理，`yy`运行时的值是`符号f2.__call__(符号y)`。

4. 执行`return xx + yy`，又产生了一个复合符号`符号f1.__call__(符号x) + 符号f2.__call__(符号y)`。

5. 最终拿到这个复合符号后，它可以等价为一个有向无环图。在这里它更弱，是一棵树，`符号f1.__call__(符号x) + 符号f2.__call__(符号y)`的两个子节点是`符号f1.__call__(符号x)`和`符号f2.__call__(符号y)`，而`符号f1.__call__(符号x)`的子节点是`符号f1`和`符号x`。

6. 在有向无环图上的起点上填入真正的对象，比如`x=1`、`y=2`，然后尽可能地并行计算所有的路线，算完再把真正的结果`return`出来就好啦。


## 使用方法

首先使用pip安装: 

```
pip install git+https://github.com/RimoChan/chao.git
```

然后在代码里`from 超 import 超`，你要加速哪个函数就给它挂上`@超`就好了。

其他的样例可以看[test.py](test.py)。


## 限制

- 函数应当是无状态的。假如两个函数一个更新了全局变量，另一个去读，那最后拿到的结果可能是错误的。

- 只能优化延迟，不能优化CPU。即使平均到每一次执行，占用的CPU时间都是更多的。


## 已知BUG

1. 递归有时候会卡住，感觉像死锁了，但是我也不知道到底是哪里死的！


## 结束

就这样，我要回去睡觉了，大家88！
