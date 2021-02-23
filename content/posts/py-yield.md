---
title:  "Python yield关键字的底层实现"
date: 2016-12-28T18:00:00
tags: [python]
description: "总结一下yield关键字在C层面是如何实现的"
---

这几天面试被问到类似的问题，顺便看了看Python的源码，参考网上的教程，总结一下yield关键字在C层面是如何实现的。

## 举个栗子

我们先看一个python生成器函数的例子：

```python
from dis import dis

def func():
    i = 4
    yield i
    print i
    
dis(func)
a =func()
a.next()
a.next()
```
使用python的库dis可以直接查看python虚拟机运行的字节码。`dis(func)`的打印如下：

```
  6           0 LOAD_CONST               1 (4)
              3 STORE_FAST               0 (i)

  7           6 LOAD_FAST                0 (i)
              9 YIELD_VALUE         
             10 POP_TOP             

  8          11 LOAD_FAST                0 (i)
             14 PRINT_ITEM          
             15 PRINT_NEWLINE       
             16 LOAD_CONST               0 (None)
             19 RETURN_VALUE      
```
我们猜测其中第二列(代表字节码偏移量)为9的指令`YIELD_VALUE`就是yield关键字的执行代码，进入Python2.7.12源码目录，在解释器执行字节码的主函数`PyEval_EvalFrameEx`中找到了下面一段：


```c
          TARGET_NOARG(YIELD_VALUE)
          {
              retval = POP();
              f->f_stacktop = stack_pointer;
              why = WHY_YIELD;
              // 跳转到fast_yield处。fast_yield里处理了一下状态位然后返回结果
              goto fast_yield;
          }
```

其中`TARGET_NOARG`为封装了`case`语句的宏，这句话的意思是，如果字节码是`YIELD_VALUE`，就把栈顶元素赋值给`retval`，然后跳转到`fast_yield`处，`fast_yield`处代码进行了一些状态判断后直接返回了`retval`。

## 生成器是如何记录代码返回位置的

显然，如果这时候调用代码`a.next()`就会直接返回yield后边的表达式结果。这对应了上面C代码的`fast_yield`部分，那生成器怎么记录上次执行的位置并在下一次调用`a.next()`的时候从上次的位置继续执行的呢？

Python在解释代码时，是将代码块加载为一个叫PyFrameObject的对象，这个对象代表了当前运行的栈帧。PyFrameObject里有个`f_lasti`变量用于保存代码当前执行到了字节码的哪个位置。在第二次执行`a.next()`时，生成器对象把之前携带了`f_lasti`的PyFrameObject当参数传给`PyEval_EvalFrameEx`，在`PyEval_EvalFrameEx`里的执行一个JUMPTO就直接跳转到了上一次结束生成器时的字节码位置：

```c
PyObject *
PyEval_EvalFrameEx(PyFrameObject *f, int throwflag)
{
...
#define FAST_DISPATCH() \
          { \
      if (!lltrace && !_Py_TracingPossible) { \
          f->f_lasti = INSTR_OFFSET(); \
          goto *opcode_targets[*next_instr++]; \
      } \
      // 跳转到fast_next_opcode处
      goto fast_next_opcode; \
          }
...
fast_next_opcode:
          f->f_lasti = INSTR_OFFSET();
  
          /* line-by-line tracing support */
  
          if (_Py_TracingPossible &&
              tstate->c_tracefunc != NULL && !tstate->tracing) {
              ...
              /* Reload possibly changed frame fields */
              // 按照f->f_lasti中的偏移量跳转字节码
              JUMPTO(f->f_lasti);
}
```

其中`INSTR_OFFSET`宏正是字节码的偏移量。

```c
#define INSTR_OFFSET()  ((int)(next_instr - first_instr))

// co->co_code里保存的是字节码
first_instr = (unsigned char*) PyString_AS_STRING(co->co_code);
next_instr = first_instr + f->f_lasti + 1;
```

所以生成器对象每次执行结束都把字节码的偏移量记录下来，并把运行状态保存在PyFrameObject里，下一次运行时生成器时，python解释器直接按照偏移量寻找下一个字节码指令。

