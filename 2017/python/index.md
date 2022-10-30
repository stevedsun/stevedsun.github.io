# 《Python源码剖析》第一部分——Python对象基础


## Python的对象初始化

> 在Python中，对象就是为C中的结构体在堆上申请的一块内存，一般来说，对象是不能被静态初始化的，并且也不能在栈空间上生存。唯一的例外就是类型对象，Python中所有的内建的类型对象（如整数类型对象，字符串类型对象）都是被静态初始化的。

python 的对象不像 C 是分配在栈、堆、data segment等位置，而是全部分配在堆上！只有python内置类型在初始化时候才是被C语言层静态初始化。

PyObject内部就两样：引用计数器、类型对象指针。

类型对象的定义：

```c
typedef struct _typeobject {
    PyObject_VAR_HEAD
    char *tp_name; /* For printing, in format "<module>.<name>" */
    int tp_basicsize, tp_itemsize; /* For allocation */

    /* Methods to implement standard operations */
    destructor tp_dealloc;
    printfunc tp_print;
    ……
    /* More standard operations (here for binary compatibility) */
    hashfunc tp_hash;
    ternaryfunc tp_call;
    ……
} PyTypeObject;
```

`PyObject_VAR_HEAD`是可变类型的头信息，其中除了`PyObject_HEAD`的内容外，额外添加了一个代表该对象元素数量的整型。从上边代码可见，python的类型也是一个可变对象。

## Python的多态

Python中所有类型在初始化后，在C语言层面都使用同一种指针`PyObject *`，所以python实现多态就非常容易。任何函数的参数都是一个PyObject类型指针，也就不存在编译器需要判断函数参数类型。

## Python对象内存池

Python为了避免频繁的释放对象，采用了内存池的机制，在对象引用计数为0时，不会释放内存，而是将内存交还给内存池供python重新分配使用。**每一种python类型，都有特定的内存池机制。**

## 整数对象

-5至257之间的小整数，存储在「小整数数组」里，这个数组Python自动创建，每次创建一个小整数，就指向这个数组里对应的PyIntObject值并把PyIntObject的计数加1。(因此在-5到257之间的数实际指向同一片内存空间，整数-5和-5的内存地址肯定是一样的)

大整数则由一个叫`block_list`的链表管理，每次分配一个大整数就在`free_list`(一个指向空闲内存block的指针)里拿出一个节点并把`free_list`后移一个`block`。关于`free_list`是如何把尚未分配的内存和已被释放的内存链接起来的，可以参见书中113页的插图理解。

值得注意的是，python用于分配给整型的堆内存是不会自行销毁的，而是不断复用。也就是说，**同一时间如果同时使用的整型太多，会消耗大量内存，并且这些内存在python关闭之前一直被python持有着。**

## 字符串对象

```c
typedef struct {
    PyObject_VAR_HEAD
    long ob_shash;
    int ob_sstate;
    char ob_sval[1];
} PyStringObject;
```

在Python源码中的注释显示，预存字符串的hash值(为了节省字符串比较的时间)和这里的intern机制将Python虚拟机的执行效率提升了20%。

**intern机制** 将新建的字符串缓存在一个PyDictObject里，相同的字符串共用同一内存。

单一字符的字符串，除了用intern缓存外，还会缓存在系统自带的一个字符串缓冲池里：

```c
static PyStringObject *characters[UCHAR_MAX + 1]; 
```

**`+`操作符和`join`的效率问题** `+`连接n个操作符会创建n-1次临时空间，`join`会直接处理一个list里的字符串，只分配一次内存。节省开销。

## 列表对象

参见C++ vector对象的存储方式。

## 字典对象

Python使用散列表(时间复杂度O(1))而非红黑树(时间复杂度O(logN))来存储map结构。

**Hash冲突(碰撞)**不同的值映射到相同的键时，就产生了冲突。一般解决办法有：

- 开链法(哈希桶)：
![](https://i.loli.net/2021/03/05/bQuAwlOTUIXkJ7x.gif)

- 开放定址法：
hash一次没有命中就再hash一次，直到找到为止……(二次探测)

小于8个元素的Dict，python使用PyDIctObject内部的smalltable数组保存元素内容。

PyDictObject对String类型的key做了特殊对待——简化了计算hash函数的过程(正常情况下key值是一个`PyObject *`对象，需要做大量类型判断，但是对PyStringObject就省了)。

**装载率(使用的空间/预先分配的空间)**大于2/3时，hash冲突的概率会急速升高，这时python就会动态分配更多的空间。与其他类型一样，如果装载率太小，也会自动缩减分配的空间。

> 在确定新的table的大小时，通常选用的策略是时新的table中entry的数量是现在table中Active态entry数量的4倍，选用4倍是为了使table中处于Active态的entry的分布更加稀疏，减少插入元素时的冲突概率……所以当table中Active态的entry数量非常大时，Python只会要求2倍的空间，这次又是以执行速度来交换内存空间。

注意这段话，执行速度和内存大小是反比关系，划分的空间越大，执行一次查找就越费时，所以分配的内存空间不是越大越好。

PyDictObject也使用了同PyListObject一样的缓冲池方式。参考列表对象部分内容。

_**笔者总结：从上面的各种类型的处理规律可以总结出Python遵循的原则：小变量缓存，大变量尽量整块分配内存，回收变量时不释放内存而是尽量复用，预分配的空间既要满足需要又不能太大(太大就缩减)**_



