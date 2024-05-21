---
title: "Python Fabric库无法启动后台进程的问题和解决办法"
date: 2016-10-19T16:25:51
categories: [Python]
tags: [python]
description: "近期在调试fabric执行远程脚本时遇到的问题和产生原因"
aliases: [/posts/py-fabric/]
---

## 问题和处理方法

Python 的 Fabric 库能够方便的远程操作 Linux 主机执行命令或传输文件。其实现方式就是底层实现 ssh 协议，例如执行下面代码的 run 方法，在目标主机上启动一个 zabbix 后台服务：

```python
from fabric import api
from fabric.tasks import Task


class Zabbix(Task):
    def run(self, kwargs):
        with api.settings(host_string='192.168.1.2', user='root', password='123456'):
            api.run('service zabbix_agentd start')
```

但是这样操作后虽然 Fabric 的 output 返回结果打印是启动成功，但是 ssh 登录目标主机，却不见 zabbix_agentd 进程，这说明没有真正启动起来。

我查询了 Fabric 文档，发现需要在 api.run 里添加参数`pty=False`。

```python
            api.run('service zabbix_agentd start'， pty=False)
```

这样就成功启动了后台进程。

## 原因

### 什么是 pty？

pty 是 pseudo-tty，众所周知 tty 是 Linux 支持输入与输出的终端设备，在 shell 下执行`ps`可以查看每个进程对应的 tty 设备号，如`ttys0001`。

pty 是为了解决远程连接时一方不希望对方直接 ssh 连接到主机上而诞生的「虚拟设备」，即伪 tty，其原理是在远程主机和本地之间同时启动 pty 端口连接终端，可以类比进程间的通道，pty 两端同时执行输入输出操作，如同本地直接连接到远程主机。但是一旦断开本地与远程主机的连接，pty 就会结束所有刚才的进程。

根据网上的资料，Github 仓库的 ssh 连接就采用 pty， Github 不希望用户创建一个可与它的主机交互的 ssh 连接，所以采用这种模式。

Fabric 在默认情况下就采用 pty ，所以想要用 fabric 登录目标主机启动后台进程，必须加上 `pty=False`。

## 参考资料

<https://github.com/fabric/fabric/issues/395>
<http://ytliu.info/blog/2013/09/28/ttyde-na-xie-shi-er/>
<http://7056824.blog.51cto.com/69854/276610>
