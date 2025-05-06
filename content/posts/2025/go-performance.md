---
title: "Go服务端性能的一般解决思路"
date: 2025-05-06T10:35:41+08:00
categories: [Software Architecture]
tags: [Go]
aliases: [/posts/go-performance/]
description: ""
---

最近遇到一个性能问题，客户反馈，在他们的 IPC 设备后台有两个 Go 语言编写的服务进程占用内存一直在上涨，最大时候达到了总内存的 40% 。其中一个进程就是我们日志采集 Agent。

我首先怀疑是内存泄漏，因为过去发生过 goroutine 阻塞造成的内存泄漏（我在[Go 内存泄漏常见模式](/posts/2023/goroutine-leak/)中讨论过)，所以我先针对所有创建和释放 goroutine 的地方进行排查。

在上一次教训之后，我们对代码单元测试层面做了 goruntine 内存泄漏的检测——使用`go.uber.org/goleak`。只需要在单元测试开头加上一句:

```go
func TestXXX(t *testing.T) {
    defer goleak.VerifyNone(t)
    // ...
}
```

它就会在测试结束后自动检查是否有残留的 goroutine 协程。对于一些延迟执行的后台 goroutine 可以在单元测试里用 wait 或者 sleep 等待后台释放再结束测试用例。

经过第一轮排查可以排除代码本身 goroutine 造成的问题。于是我把注意力转向了另一个地方：定时任务。

根据客户反馈，在无任何前台操作的情况下，内存也会缓慢上升。

在我们代码里，使用了`github.com/robfig/cron/v3`这个第三方包，它的作用是编排定时任务。用法是

```go
c = cron.New()
c.AddFunc("@every 10s", callbackFunc)
```

这种结构定义一个定时任务。它的实现也基于 goroutine，所以我把 go 自带的 pprof 加入到 main.go 的依赖中，重新编译了项目二进制文件并部署到测试环境上（使用跟用户相同的硬件配置）。这样启动项目后就可以在特定端口获取内存信息。（关于 pprof，你可以参考 [Profiling Go Programs](https://go.dev/blog/pprof)）

我使用 pprof 的接口获取了不同时间间隔的 heap 数据

```go
curl -o heap.1.out http://127.0.0.1:6060/debug/pprof/heap
```

然后使用

```go
go tool pprof -http=:8099 -base heap.1.out heap.2.out
```

比较两次结果的差异，在 Web UI 上选择 In Use Space 选项，可以查看到哪些内存没有释放。

虽然经过第二轮排查，依然没有发现内存泄漏。但这一次我注意到服务中的一个定时任务会每隔 10 秒执行一次，执行过程中 CPU 占用率明显上升。在这个任务的代码里，它使用了`github.com/shirou/gopsutil/process`这个第三方库来查询系统进程 ID 和进程名等信息。

我查看它的源码后发现，这个库查询进程 ID 的方式，是把系统中所有的进程信息加载到内存中，然后匹配 ID 或者名称。因此，如果用户设备上的进程过多，就会每次查询时占用大量内存。

在一个 10 秒执行一次的定时任务中调用这个库，显然是非常低效的。

经过与客户进一步沟通，我们发现出现内存过高的两个进程中，另一个进程也有 CPU 占用过高的现象。于是我们让客户把 `top` 命令的截图发给我们。在看到截图的一瞬间，问题的真相就浮出水面了:

客户使用的 IPC 设备是性能比较低的版本，虽然内存较大，但 CPU 性能捉急。如果有多个进程同时执行后台任务，CPU 就会周期性打满，造成任务阻塞。而我们使用的第三方库基于 goroutine 来实现定时任务。在上一个任务被阻塞时，下一个任务依然会继续创建新的后台 goroutine，导致内存中的 goroutine 协程堆积地越来越多。

这是一个定时任务的 CPU 占用过高，间隔过短，造成的 goroutine 阻塞问题。

知道了原因，剩下的工作就是优化代码逻辑、更新版本、跟客户解释原因……

以上就是这次排查 Go 服务性能问题的过程，如果你也遇到类似情况，希望对你有所帮助。
