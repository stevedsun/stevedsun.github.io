---
title: "Python2 中字符类型的一些坑"
date: 2017-01-11T11:09:00
description: "Python 2.x 处理字符经常会出现意料之外的效果。其中最大的原因就是对`str`类型做了双重标准"
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

在Python2里，默认的字符类型是`str`，这个`str`和Python3的`str`完全不同，Python2的`str`类型是8位的ascii序列。Python2在处理`str`类型转换时遵循这样的规则：**如果被处理的`str`型变量值小于7位，就可以和`unicode`类型混用。可以做`+`连接，格式化等操作，同unicode享受同样的待遇。**

Python2在格式化字符时，会把`str`格式化为`str`，如果字符串里混入了`unicode`，就会把其他字符都转化为`unicode`。所以这道题里1处的a，b两个值混合后的字符就是一个unicode字符串，c和d单独格式化后仍保留了自己的格式。但是Python2在格式化代码位置4时，发现c是unicode而d不是，就会尝试按照上面的混用规则，格式化d为unicode类型，但是d的值`'中国'`显然是一个大于7位的`str`，因此Python2抛出UnicodeDecodeError。

在Python3里，`str`类型则变成了一个纯unicode字符，也就是说Python3里的`str`等价于Python2里的`unicode`类型。Python3里为了清晰明了，使用`bytes`代表8位ascii序列。除此之外，Python3严格禁止混用两种类型。

## 总结

* 使用Python2处理字符串，尤其是中文字符串，最好前边加上u
* Python2里不要混用`str`和`unicode`，如果处理文本时，先将全部数据格式化成unicode
* 能用Python3尽量不用Python2 ~~(废话)~~

## 参考资料：

* 《Effective Python》 Brett Slatkin.
* 不愿意透露姓名的某厂面试官



