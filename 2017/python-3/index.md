# 《Python源码剖析》第三部分——Python虚拟机进阶


## Python 环境初始化

进程启动后创建PyInterpreterObject，PyInterpreterObject里面维护了全局module映射表`interp->modules`，该表默认初始化为__buildin__模块，

## Python 的 import 机制

> Python虚拟机在执行“import A”时，会为package A创建一个module对象，同时会在该module维护的dict中添加两个表示元信息的属性：__name__和__path__。而Python虚拟机从A/__init__.py中执行“import mod1”时，也会为mod1创建一个module对象，同时也会设置__name__属性，但是这时就不设置__path__属性了。


> package是由module聚合而成。更清楚的表述是：module属于一个package。我们不能说，module1属于module2。我们前面已经看到，module的路径实际上是一种树状结构，从图14-11中可以看到，在这个树状结构中，module的父节点只能是package，而不可能是另一个module。

## GIL
Python虚拟机使用一个全局解释器锁（Global Interpreter Lock，GIL）来互斥线程对python虚拟机的使用。

注意这里GIL是解释器一级的互斥锁，也就是同一时间只能有一个线程占用python解释器。所以**GIL是用来让操作系统中分配的多个线程互斥的使用python解释器的，是建立在系统线程调度基础之上的一套C API互斥机制**，是比操作系统线程资源更大粒度的锁。

Python的线程是基于操作系统原生线程的，所以python的线程不是「虚拟出来的」。

> 那么究竟Python会在众多的等待线程中选择哪一个幸运儿呢？答案是，不知道。没错，对于这个问题，Python完全没有插手，而是交给了底层的操作系统来解决。也就是说，Python借用了底层操作系统所提供的线程调度机制来决定下一个进入Python解释器的线程究竟是谁。

GIL在C里对应的结构：

```c
[thread_nt.h]
typedef struct NRMUTEX {
    LONG   owned ;
    DWORD  thread_id ;
    HANDLE hevent ;
} NRMUTEX, *PNRMUTEX ;
```
其中`owned`初始化为-1，表示锁可用，否则为不可用。`thread_id`代表线程id，最后一个是平台相关的变量，win32上是一个event内核对象。

## 多线程 - 标准调度

> 当Python启动时，是并不支持多线程的。换句话说，Python中支持多线程的数据结构以及GIL都是没有创建的，Python之所以有这种行为是因为大多数的Python程序都不需要多线程的支持

书中指出，由于python的多线程标准调度机制是有代价的，所以默认单线程不初始化GIL。

1. 主线程启动后，会用`ident = PyThread_start_new_thread(t_bootstrap, (void*) boot);`函数调用操作系统内核接口创建子线程，然后主线程挂起等待`obj.done`。注意，此时主线程中持有GIL。
2. 主线程等待的这段时间里，子线程将自己的线程id等信息设置好，通知内核对象`obj.done`，唤醒等待中的主线程。此刻，主线程和子线程都同时由操作系统调度，但是主线程一直持有着GIL。
3. 子线程继续执行后进入python解释器，发现需要等待获取GIL。此时子线程主动将自己挂起(而不是由操作系统挂起)。这样就进入了两个线程通过GIL调度的阶段。
4. 主线程被唤醒后，继续执行，直到python内置的时钟计时器`_Py_Ticker`结束才将自己挂起，让出GIL(`_Py_Ticker`会在每次执行一条字节码后自动减1，初始默认为100)。

通过上面4步，python的两个线程就完成了从系统调度上升到python标准GIL调度的流程。

## 阻塞调度

如同上面流程介绍的，标准调度是python使用软件时钟调度线程，那么有时候python的线程会自我阻塞，比如`raw_input()`、`sleep()`等函数，这时python就会使用阻塞调度的方式。

1. 主线程调用`sleep(1)`后，调用`Py_BEGIN_ALLOW_THREADS`立刻释放GIL，然后调用操作系统的sleep操作。此时主线程就由操作系统自动管理。
2. 子线程拿到GIL。此时主线程和子线程同时可被操作系统调度。操作系统在执行一段时间子线程后会挂起，调度主线程，发现主线程sleep没结束就挂起主线程，就继续唤醒子线程执行。
3. 当主线程sleep结束，操作系统唤醒主线程。主线程调用`Py_END_ALLOW_THREADS`再次申请GIL，重新进入python标准调度流程。

**可见python在保证线程安全的前提下，允许线程在某些时刻脱离GIL标准调度流程。**

其中`Py_BEGIN_ALLOW_THREADS`和`Py_END_ALLOW_THREADS`两个负责释放和等待GIL的宏的实现如下。

```c
[ceval.h]
#define Py_BEGIN_ALLOW_THREADS { \
            PyThreadState *_save; \
            _save = PyEval_SaveThread();
#define Py_END_ALLOW_THREADS    PyEval_RestoreThread(_save); \
         }

[ceval.c]
PyThreadState* PyEval_SaveThread(void)
{
    PyThreadState *tstate = PyThreadState_Swap(NULL);
    if (interpreter_lock)
        PyThread_release_lock(interpreter_lock);
    return tstate;
}

void PyEval_RestoreThread(PyThreadState *tstate)
{
    if (interpreter_lock) {
        int err = errno;
        PyThread_acquire_lock(interpreter_lock, 1);
        errno = err;
    }
    PyThreadState_Swap(tstate);
}
```

## 用户级互斥

用户级的互斥锁利用操作系统的互斥机制实现，同时要考虑防止和GIL形成死锁。所以过程与阻塞调度类似需要使用`Py_BEGIN_ALLOW_THREADS`和`Py_END_ALLOW_THREADS`这两个宏。

1. 线程a调用lock对象加锁，lock对象内部调用系统互斥机制，同时执行`Py_BEGIN_ALLOW_THREADS`释放GIL防止死锁。
2. 线程b获得GIL，执行到某处释放锁，lock对象内部调用系统机制释放锁，同时底层调用了`Py_END_ALLOW_THREADS`等待GIL。
3. 线程a被系统唤醒，获取GIL，一气呵成。

## 子线程的销毁

> 在线程的全部计算完成之后，Python将销毁线程。需要注意的是，Python主线程的销毁与子线程的销毁是不同的，因为主线程的销毁动作必须要销毁Python的运行时环境，而子线程的销毁则不需要进行这些动作。

## 内存管理

大块内存管理直接调用C的malloc和free接口，小块内存分配则由python的内存池管理机制调度。

### 小块内存管理的对象

Python的内存块叫block，每个block大小不同，都是8的整数倍。管理block的叫pool，一个pool是4K。pool管理**相同大小**的一堆block。pool对象的szindex变量保存了这个pool对应的block大小。

> ，一个pool可能管理了100个32个字节的block，也可能管理了100个64个字节的block，但是绝不会有一个管理了50个32字节的block和50个64字节的block的pool存在

Python对于内存块的管理类似对象的策略，每次内存分配一整个block，回收时先将不用的Block加入闲置的队列里等待重新利用，不是直接回收。(惰性回收策略)

管理多个pool的数据对象是arena。下图可见，pool结构是一次性分配好一块内存，而arena则是通过指针连向一块pool。

![](https://i.loli.net/2021/03/05/2duvofnkP9LEO8x.jpg)

而python维护一个名叫arenas的数组，数组元素就是arena对象。arena之间通过由两条链表相连。它们分别是：

- *unused_arena_objects* 是单向量表，指向未分配pool的arena
- *usable_arenas* 是双向链表，表示已经分配了pool的arena

![](https://i.loli.net/2021/03/05/duFq5I6lWACjQyw.jpg)


> 当一个arena的area_object没有与pool集合建立联系时，这时的arena处于“未使用”状态；一旦建立了联系，这时arena就转换到了“可用”状态。对于每一种状态，都有一个arena的链表。“未使用”的arena的链表表头是unused_arena_objects、arena与arena之间通过nextarena连接，是一个单向链表；而“可用”的arena的链表表头是usable_arenas、arena与arena之间通过nextarena和prevarena连接，是一个双向链表。

**Pool是python管理内存的对象，arena虽然更上层，但是arena内的pool集合可能管理32字节的block，也可能管理64字节的block，所以arena无法决定销毁和分配内存。Python仍然以pool为单位管理内存开销。(pool有size概念，arena没有size概念)**

Pool有三种状态full、empty和used。其中full不需要连接起来，其他两种状态会被freepools和usedpools连接起来方便管理。

![](https://i.loli.net/2021/03/05/mZr1P7ocQYbpCFB.jpg)

### arena的分配

arena可以指向32位pool集合，也可以指向64位pool集合。分配内存的过程如下：

1. 先在usable_arenas链表上找可用的arena，然后找到符合要求的pool
2. 如果没有可用的arena，则从arenas数组里摘下来新的arena，放在usable_arenas里，然后初始化pool
3. 从usedpools链表里找可用的blocks
4. usedpools没有可用的pool，就从freepools链表分配一个empty状态的pool

### Python编译时指定内存上限

> 当Python在WITH_MEMORY_LIMITS编译符号打开的背景下进行编译时，Python内部的另一个符号会被激活，这个名为SMALL_MEMORY_LIMIT的符号限制了整个内存池的大小，同时，也就限制了可以创建的arena的个数。在默认情况下，不论是Win32平台，还是unix平台，这个编译符号都是没有打开的，所以通常Python都没有对小块内存的内存池的大小做任何的限制。

### 小块内存管理的流程

*(此部分摘自书中代码注释)*

1. 如果申请的内存小于SMALL_REQUEST_THRESHOLD，使用Python的小块内存的内存池。否则，转向malloc
2. 根据申请内存的大小获得对应的size class index
3. 如果usedpools中可用的pool，使用这个pool来分配block
4. 分配结束后，如果pool中的block都被分配了，将pool从usedpools中摘除
5. 如果usedpools中没有可用的pool，从usable_arenas中获取pool
6. 如果usable_arenas中没有就“可用”的arena，开始申请arena
7. 从usable_arenas的第一个arena中获取一个pool
8. 获取pool成功，进行init pool的动作，将pool放入used_pools中，并返回分配得到的block
9. 获取pool失败，对arena中的pool集合进行初始化，然后转入goto到init pool的动作处，初始化一个特定的pool

### Python 2.5对多次分配小内存造成内存泄漏的处理

在2.5之前版本，Python的arena从来不释放pool。这就造成反复分配小内存后造成的arena太多而内存无法回收。

2.5之后的处理办法：arena有两种状态，unused和usable。上文已经介绍过。

1. 如果arena中所有的pool都是empty的，释放pool集合占用的内存。arena变成unused状态，从usable_arenas剔除
2. 如果arena初始化了新的pool，arena变成usable状态，从usable_arenas链表中顺序查找位置插入该arena。注意，usable_arenas是有序链表(按照arena中pool的个数排序，pool多的arena排前边，pool少的排后边)
3. 这样，再有分配内存的请求时，先从usable_arenas表头顺序查，排在前边pool多的arena就被利用的充分，pool少的arena就更有可能变成unused状态，容易被释放掉。达到节省内存的目的

### 内存池全景

![](https://i.loli.net/2021/03/05/1Lh6u4awv8ZyQ9H.jpg)

## Python垃圾回收机制

除了计数器，python还是使用了标记-清除，分代回收机制。

### 标记 - 清除

#### 三色模型

根据系统内所有对象的引用情况建立有向图，沿着有向图从根开始的逐层染色，黑色代表该节点所有引用都检查过了，灰色表示节点是可达的，当所有灰色节点都变为黑色，检查结束。

![](https://i.loli.net/2021/03/05/2a1kYDnyT4fBQxP.jpg)

### Python 中的标记清除

Python的对象由三大部分组成，PyGC_Head，PyObject_Head和本体。其中PyObject_Head里存计数器用来标记当前节点是否可回收，但是对于循环引用的情况，就需要PyGC_Head里的refs，python会根据一些触发条件进行三色模型的标记，某个对象的「可达次数」标记在PyGC_Head里，当这个可达次数为0时，代表对象不可达，也就需要回收之。PyGC_Head之间有一条双向链表连接了所有对象，将他们纳入内存回收管理系统里。

![](https://i.loli.net/2021/03/05/UT5ry697VXINBQp.jpg)

#### 流程

1. 在垃圾收集的第一步，就是遍历可收集对象链表，将每个对象的gc.gc_ref值设置为其ob_refcnt值。
2. 接下来的动作就是要将环引用从引用中摘除。
3. 有一些container对象的`PyGC_Head.gc.gc_ref`还不为0，这就意味着存在对这些对象的外部引用，这些对象，就是开始标记 - 清除算法的root object集合。

### 分代回收

 > 这种以空间换时间的总体思想是：将系统中的所有内存块根据其存活时间划分为不同的集合，每一个集合就称为一个“代”，垃圾收集的频率随着“代”的存活时间的增大而减小，也就是说，活得越长的对象，就越可能不是垃圾，就应该越少去收集。

![](https://i.loli.net/2021/03/05/mQuPrwyD73ZjhBv.jpg)

> Python采用了三代的分代收集机制，如果当前收集的是第1代，那么在开始垃圾收集之前，Python会将比其“年轻”的所有代的内存链表（当然，在这里只有第0代）整个地链接到第1代内存链表之后，这个操作是通过gc_list_merge实现的。

### 总结

1. 将比当前处理的“代”更年轻的“代”的链表合并到当前“代”中
2. 在待处理链表上进行打破循环的模拟，寻找root object
3. 将待处理链表中的unreachable object转移到unreachable链表中，处理完成后，当前“代”中只剩下reachable object了
4. 如果可能，将当前“代”中的reachable object合并到更老的“代”中
5. 对于unreachable链表中的对象，如果其带有`__del__`函数，则不能安全回收，需要将这些对象收集到finalizers链表中，因此，这些对象引用的对象也不能回收,也需要放入finalizers链表中
6. 处理弱引用（weakref），如果可能，调用弱引用中注册的callback操作
7. 对unreachable链表上的对象进行垃圾回收操作
8. 将含有`__del__`操作的实例对象收集到Python内部维护的名为garbage的链表中，同时将finalizers链表中所有对象加入old链表中

**注意，如果对象拥有`__del__`方法，就不能通过垃圾回收来自动回收**，所以要慎重使用这个方法。


