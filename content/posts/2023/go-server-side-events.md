---
title: "Go Server Side Events"
date: 2023-09-13T09:19:18+08:00
categories: [Go]
tags: [go, sse]
aliases: [/posts/go-server-side-events/]
description: ""
---

Server-Sent Events (**SSE**) is a technology that enables real-time communication between a web browser and a server. It allows the server to send updates or event notifications to the browser without the need for the browser to repeatedly make requests.

SSE is often used in applications that require real-time updates, such as chat applications, social media feeds, stock market tickers, or notifications systems. It provides a lightweight and efficient way to deliver server-side updates to clients, improving responsiveness and reducing unnecessary network traffic.

Following is an example of SSE in golang framework [Gin](https://github.com/gin-gonic/gin):

The Gin API handler `SSEDemoGetStatus` will call `service.CheckStatus()` every 10 seconds and respond to client with message event.

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

In this way, the client side will receive an HTTP request that establishes an TCP connection that continuely sent data from server side.

What have to be noticed is the HTTP header. In my case, I need to tell web server (like Nginx) do not cache the TCP traffic. For the javascript [EventSource](https://developer.mozilla.org/en-US/docs/Web/API/EventSource) API, the header `Connection: keep-alive` is important.

A better place to put these headers is the Gin middleware function:

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

Looking for more details please move to [Gin SSE example](https://github.com/gin-gonic/examples/blob/master/server-sent-event/main.go).

[![Buy Me A Coffee](https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png?width=217px)](https://www.buymeacoffee.com/stevedsun)
