---
title: "Python defaultdict结构作计数器的用法"
date: 2016-10-11T15:00:16
categories: [Python]
tags: [python]
description: ""
aliases: [/posts/py-defaultdict/]
---

在开发中经常需要用到计数器，当函数 foo 调用另一个函数 bar 时，为了确认调用 bar 之后处理的结果正确性，经常需要使用计数器来统计 bar 函数里处理成功了多少次。例如：

```python
def foo():
    success_num = bar()
    print success_num

def bar():
    n = 0
    # 假设这个任务要迭代100次.
    count = 100

    try:
        for i in count:
            # Do something.
            n += 1
    except:
        pass
    finally:
        return n
```

但是，这里需要定义多个计数器变量来保存计数。每多一个 bar 函数就要多定义两次计数器。有没有类似 C 语言指针一样的方法，可以在 foo 中定义后直接传给 bar，在 bar 里修改值呢。

众所周知，Python 的参数传值实际传的是变量的拷贝，但是对于像字典、列表等非基本数据结构，实际传给参数的是这个数据结构的指针地址，修改指针地址指向的实际值就可以在函数内外实现传递数据的效果了。那么利用这个特性，可以结合 python 标准库 collections 里的 defaultdict 结构来实现一个更方便的计数器：

```python
from collections import defaultdict

def foo():
    result = defaultdict(int)
    bar(result)
    print result

def bar(result):
    count = 100
    for i in count:
        try:
            # Do something.
            result['success'] += 1
        except:
            result['fail'] += 1
```

这样，变量`result`就是存有正确计数和错误计数的字典。
