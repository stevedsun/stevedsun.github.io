---
title: "Go Server-Side Events"
slug: "go-server-side-events"
date: 2023-09-13T09:19:18+08:00
categories: [Go]
tags: [go, sse]
aliases: [/posts/go-server-side-events/]
description: ""
---
Server-Sent Events (**SSE**) is a technology that enables real-time communication between a web browser and a server. It allows the server to send updates or event notifications to the browser without the need for the browser to repeatedly make requests.

SSE is often used in applications that require real-time updates, such as chat applications, social media feeds, stock market tickers, or notification systems. It provides a lightweight and efficient way to deliver server-side updates to clients, improving responsiveness and reducing unnecessary network traffic.

Below is an example of SSE in the Go web framework [Gin](https://github.com/gin-gonic/gin):

The Gin API handler `SSEDemoGetStatus` will call `service.CheckStatus()` every 10 seconds and respond to the client with a message event.

```go
func SSEDemoGetStatus(c *gin.Context) {
	chanStream := make(chan interface{}, StreamBufferSize)
	clientGone := c.Writer.CloseNotify()

	go func() {
		defer close(chanStream)

		ticker := time.NewTicker(10*time.Second)
		defer ticker.Stop()
		for {
			status := service.CheckStatus()
			chanStream <- status

			select {
			case <-ticker.C:
				continue
			case <-clientGone:
				return
			}
		}
	}()

	c.Writer.Header().Set("Connection", "keep-alive")
	c.Writer.Header().Set("X-Accel-Buffering", "no")
	c.Writer.Header().Set("Cache-Control", "no-cache")
	c.Stream(func(w io.Writer) bool {
		if msg, ok := <-chanStream; ok {
			c.SSEvent("message", msg)
			return true
		}
		c.SSEvent("status", "Done")
		return false
	})
}

```

In this way, the client receives an HTTP request that establishes a TCP connection through which the server continuously sends data.

What must be noted are the HTTP headers. In my case, I need to tell the web server (e.g., Nginx) not to cache the TCP traffic. For the JavaScript [EventSource](https://developer.mozilla.org/en-US/docs/Web/API/EventSource) API, the header `Connection: keep-alive` is important.

A better place to put these headers is a Gin middleware function:

```go
func HeadersMiddleware() gin.HandlerFunc {
	return func(c *gin.Context) {
		c.Writer.Header().Set("Content-Type", "text/event-stream")
		c.Writer.Header().Set("Cache-Control", "no-cache")
		c.Writer.Header().Set("Connection", "keep-alive")
		c.Writer.Header().Set("Transfer-Encoding", "chunked")
		c.Next()
	}
}
```

For more details, please head over to [Gin SSE example](https://github.com/gin-gonic/examples/blob/master/server-sent-event/main.go).
