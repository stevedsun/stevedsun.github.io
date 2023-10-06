---
title: "Go 内存泄漏常见模式"
date: 2023-06-27T14:46:59+08:00
categories: [Go]
tags: [go, memory leak]
aliases: [/posts/goroutine-leak/]
description: ""
---

最近在工作中排查 Go 语言内存泄漏问题时，发现[这篇 Uber 写的博客](https://www.uber.com/blog/leakprof-featherlight-in-production-goroutine-leak-detection/)，其中分享了几种常见的 goroutine 内存泄漏模式，于是把整理了 goroutine 的相关问题，希望更多人搜索到到这篇文章，帮助大家快速定位内存泄漏问题。

## Goroutine 内存泄漏的原因

Go 语言的内存泄漏通常因为错误地使用 goroutine 和 channel。例如以下几种情况：

1. 在 goroutine 里打开一个连接（如 gRPC）但是忘记 close
2. 在 goroutine 里的全局变量对象没有释放
3. 在 goroutine 里读 channel， 但是没有写入端，而被阻塞
4. 在 goroutine 里写入无缓冲的 channel，但是由于 channel 的读端被其他协程关闭而阻塞
5. 在 goroutine 里写入有缓冲的 channel，但是 channel 缓冲已满

这几种情况，通常掺杂在复杂的代码里逻辑里，很难调试发现问题。因此衍生出以下几种日常工作中**最容易出现问题的模式**。

## 常见 Goroutine 内存泄漏模式

### Premature Function Return /功能过早返回

一个 goroutine 要写入 channel，但是在另一个端意外退出导致 channel 读取的代码没有执行。

```go
func Example() {
    a := 1
    c := make(chan error)
    go func() {
        c <- err
        return
    }()

    // do something

    if a > 0 {
        return
    }

    // do something

    err := <-c
}
```

代码中主进程在`if a > 0` 处 return，导致 channel 无法写入而被阻塞。

解决这种问题的一个思路是把无缓冲 channel 转化为缓冲大小为 1 的 channel。

```go
c := make(chan error, 1)
```

有缓冲 channel 即使没有读取操作，也不会阻塞。

### The Timeout Leak /超时泄漏

这是我们工作中遇到的问题，经常需要执行一个可能超时的异步操作时被使用。

```go
func Example() {
    timeoutOption := SomeTimeoutOption()
    done := make(chan any)
    go func() {
        done <- result
    }()

    select {
        case <- done:
            return
        case <- timeoutOption.Timeout():
            return
    }
}

```

在这段代码里，一旦 timeoutOption 操作超时，就会通知 select，接着程序退出，于是 goroutine 写入 done 的操作被阻塞而无法退出。

解决思路同上一个模式，用有缓冲 channel 替代无缓冲 channel。

### The NCast Leak /多端读写泄漏

如果 channel 的读端只有一个，但是写端有多个，就会发生这种情况。

```go
func Example() {
    c := make(chan any)
    for _, i := range items {
        go func(c chan any) {
            c <- result
        }(c)
    }
    data := <- c
    return
}

```

这种情况也适用于“多个写端一个读端”的情况，解决方法是把 channel 设置成和写或读数量一致的缓冲数。

```go
c := make(chan any, len(items))
```

### Channel Iteration Misuse /通道迭代误用

Go 支持一种特性 ["Range over channels"](https://gobyexample.com/range-over-channels), 可以用 range 来循环读取 channel 的内容。

但是一旦读取不到内容，range 就会等待 channel 的写入，而 range 如果正好在 goroutine 内部，这个 goroutine 就会被阻塞。

```go
func Example() {
    wg := &sync.WaitGroup{}
    c := make(chan any, 1)

    for _, i := items {
        wg.Add(1)
        go func() {
            c <- data
        }()
    }

    go func() {
        for data := range c {
            wg.Done()
        }
    }()

    wg.Wait()
}
```

解决这个问题的方式手动定义关闭 channel。

```go
wg := &sync.WaitGroup{}
c := make(chan any, 1)
defer close(c)
//...
```

这样在 WaitGroup 全部结束后，主程序会关闭 channel，从而让异步的 goroutine 内部的 range 退出循环等待。

## 小结

Goroutine 内存泄漏是 Go 语言最容易发生的内存泄漏情况，它通常伴随着错误地使用 goroutine 和 channel。而 channel 的特殊用法如 select 和 range 又让 channel 阻塞变得更加隐蔽不易发现，进而增加排查内存泄漏的难度。

在写 goroutine 和调试内存泄漏问题时，要重点关注 channel 相关的操作，尤其涉及到文中列举的四类模式：功能过早返回、超时泄漏、多端读写泄漏、通道迭代误用。

[![Buy Me A Coffee](https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png?width=217px)](https://www.buymeacoffee.com/stevedsun)
