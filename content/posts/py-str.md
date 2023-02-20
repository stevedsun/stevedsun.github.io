---
title: "Python2 中字符类型的一些坑"
date: 2017-01-11T11:09:00
categories: [Python]
tags: [python]
description: "Python 2.x对str类型的双重标准"
---

## 问题

有一道面试题是这样的：

```python
a = u'China'
b = 'China'
c = u'中国'
d = '中国'
# 1
print '%s %s' % (a, b)
# 2
print '%s' % c
# 3
print '%s' % d
# 4
print '%s %s' % (c, d)
```

判断打印后的效果。

先说正确答案，只有最后一行会报错。

## 分析

在 Python2 里，默认的字符类型是`str`，这个`str`和 Python3 的`str`完全不同，Python2 的`str`类型是 8 位的 ascii 序列。Python2 在处理`str`类型转换时遵循这样的规则：**如果被处理的`str`型变量值小于 7 位，就可以和`unicode`类型混用。可以做`+`连接，格式化等操作，同 unicode 享受同样的待遇。**

Python2 在格式化字符时，会把`str`格式化为`str`，如果字符串里混入了`unicode`，就会把其他字符都转化为`unicode`。所以这道题里 1 处的 a，b 两个值混合后的字符就是一个 unicode 字符串，c 和 d 单独格式化后仍保留了自己的格式。但是 Python2 在格式化代码位置 4 时，发现 c 是 unicode 而 d 不是，就会尝试按照上面的混用规则，格式化 d 为 unicode 类型，但是 d 的值`'中国'`显然是一个大于 7 位的`str`，因此 Python2 抛出 UnicodeDecodeError。

在 Python3 里，`str`类型则变成了一个纯 unicode 字符，也就是说 Python3 里的`str`等价于 Python2 里的`unicode`类型。Python3 里为了清晰明了，使用`bytes`代表 8 位 ascii 序列。除此之外，Python3 严格禁止混用两种类型。

## 总结

- 使用 Python2 处理字符串，尤其是中文字符串，最好前边加上 u
- Python2 里不要混用`str`和`unicode`，如果处理文本时，先将全部数据格式化成 unicode
- 能用 Python3 尽量不用 Python2 ~~(废话)~~

## 参考资料：

- 《Effective Python》 Brett Slatkin.
- 不愿意透露姓名的某厂面试官
