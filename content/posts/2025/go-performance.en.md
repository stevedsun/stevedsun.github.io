---
title: "A General Approach to Server-Side Performance Issues in Go"
slug: "go-performance"
date: 2025-05-06T10:35:41+08:00
categories: [Software Architecture]
tags: [Go]
aliases: [/posts/go-performance/]
description: ""
---

I recently ran into a performance issue. A customer reported that two Go-based service processes running in the background of their IPC device kept climbing in memory usage, peaking at 40% of total memory. One of those processes was our log-collection agent.

My first suspicion was a memory leak, because we'd had memory leaks caused by goroutine blocking in the past (I discussed this in [Common Patterns of Memory Leaks in Go](/posts/2023/goroutine-leak/)), so I started by reviewing everywhere we created and released goroutines.

After the last incident, we'd added goroutine leak detection at the unit-test level using `go.uber.org/goleak`. You only need to add a single line at the start of a test:

```go
func TestXXX(t *testing.T) {
    defer goleak.VerifyNone(t)
    // ...
}
```

It automatically checks for lingering goroutines after the test finishes. For background goroutines that run on a delay, you can use `wait` or `sleep` in the test to wait for them to be released before the test case ends.

The first round of investigation ruled out problems caused by goroutines in the code itself. So I turned my attention to another suspect: scheduled tasks.

According to the customer, memory would slowly climb even with no foreground activity.

In our code, we use the third-party package `github.com/robfig/cron/v3`, which orchestrates scheduled tasks. Usage looks like this:

```go
c = cron.New()
c.AddFunc("@every 10s", callbackFunc)
```

This structure defines a scheduled task. Its implementation is also based on goroutines, so I added Go's built-in pprof to the dependencies in `main.go`, rebuilt the project binary, and deployed it to a test environment using the same hardware configuration as the customer. This way, once the project started, I could pull memory information from a specific port. (For more on pprof, see [Profiling Go Programs](https://go.dev/blog/pprof).)

I used pprof's interface to grab heap data at different intervals:

```go
curl -o heap.1.out http://127.0.0.1:6060/debug/pprof/heap
```

Then used:

```bash
go tool pprof -http=:8099 -base heap.1.out heap.2.out
```

to compare the two results. In the web UI, I selected the In Use Space option, which let me see what memory hadn't been released.

Even after this second round, I still didn't find a memory leak. But this time I noticed that one of the scheduled tasks ran every 10 seconds, and CPU usage clearly spiked during execution. Looking at the code for this task, it used the third-party library `github.com/shirou/gopsutil/process` to query system process IDs and process names.

Looking at the library's source code, I found that the way it queries process IDs is by loading all process information on the system into memory and then matching the ID or name. So, if the customer's device has a lot of processes, each query consumes a large amount of memory.

Calling this library from a scheduled task that runs every 10 seconds is clearly very inefficient.

After further communication with the customer, we discovered that of the two high-memory processes, the other one also showed high CPU usage. So we had the customer send us a screenshot of the `top` command. The moment I saw the screenshot, the truth came into focus:

The customer's IPC device was a lower-performance version—while it had plenty of memory, the CPU was struggling. When multiple processes run background tasks simultaneously, the CPU periodically maxes out, causing tasks to block. And the third-party library we use implements scheduled tasks on top of goroutines. When the previous task is blocked, the next task still creates a new background goroutine, causing goroutines to pile up in memory.

This was a goroutine blocking problem caused by high CPU usage and overly short intervals in the scheduled tasks.

Once we knew the cause, the rest was straightforward: optimize the code logic, ship a new version, and explain the issue to the customer...

That's the full process of debugging this Go service performance issue. If you run into something similar, I hope this helps.
