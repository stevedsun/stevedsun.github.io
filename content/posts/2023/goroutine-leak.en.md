---
title: "Common Patterns of Go Memory Leaks"
slug: "goroutine-leak"
date: 2023-06-27T14:46:59+08:00
categories: [Go]
tags: [go, memory leak]
aliases: [/posts/goroutine-leak/]
description: ""
---
While investigating a Go memory leak at work recently, I came across [this blog post by Uber](https://www.uber.com/blog/leakprof-featherlight-in-production-goroutine-leak-detection/), which shares several common goroutine memory leak patterns. I've organized my notes on goroutine issues here, hoping more people searching for this topic will find this article and quickly track down memory leaks.

## Causes of Goroutine Memory Leaks

Memory leaks in Go are usually caused by incorrect use of goroutines and channels. For example:

1. Opening a connection (e.g., gRPC) inside a goroutine but forgetting to close it
2. Failing to release a global variable's object inside a goroutine
3. Reading from a channel inside a goroutine, but no one is writing to it, so it blocks
4. Writing to an unbuffered channel inside a goroutine, but the read end of the channel is closed by another goroutine, causing a block
5. Writing to a buffered channel inside a goroutine, but the channel's buffer is already full

These cases are usually tangled up in complex code logic and are very hard to spot through debugging. As a result, the following **most error-prone patterns** have emerged in everyday work.

## Common Goroutine Memory Leak Patterns

### Premature Function Return

A goroutine wants to write to a channel, but the other end exits unexpectedly, so the code that reads from the channel never runs.

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

In this code, the main process returns at `if a > 0`, so the write to the channel never happens and the goroutine blocks.

A way to fix this is to convert the unbuffered channel to a buffered channel with capacity 1.

```go
c := make(chan error, 1)
```

A buffered channel won't block even if no one reads from it.

### The Timeout Leak

This is a problem we ran into at work, often encountered when running an async operation that might time out.

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

In this code, once the timeoutOption operation times out, it signals the select, and the program exits, leaving the goroutine blocked on its write to `done` and unable to exit.

The fix is the same as the previous pattern: replace the unbuffered channel with a buffered one.

### The NCast Leak

This happens when a channel has only one reader but multiple writers.

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

This also applies to "multiple writers, one reader." The fix is to size the channel's buffer to match the number of writers or readers.

```go
c := make(chan any, len(items))
```

### Channel Iteration Misuse

Go supports the ["Range over channels"](https://gobyexample.com/range-over-channels) feature, which lets you use `range` to loop over a channel's contents.

But once there's nothing to read, `range` waits for a write to the channel. If the `range` happens to be inside a goroutine, that goroutine will be blocked.

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

The fix is to explicitly close the channel.

```go
wg := &sync.WaitGroup{}
c := make(chan any, 1)
defer close(c)
//...
```

This way, once the WaitGroup is done, the main program closes the channel, allowing the `range` inside the async goroutine to exit its wait.

## Summary

Goroutine memory leaks are the most common form of memory leak in Go, and they usually come hand-in-hand with incorrect use of goroutines and channels. Special channel constructs like `select` and `range` make blocking even more subtle and harder to spot, which raises the difficulty of debugging memory leaks.

When writing goroutines and debugging memory leak issues, pay particular attention to channel operations—especially the four patterns listed in this article: premature function return, the timeout leak, the NCast leak, and channel iteration misuse.
