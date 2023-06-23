---
title: "Kong网关极简入门"
date: 2023-06-23T10:36:36+08:00
categories: [Cloud Native Computing]
tags: [kong, gateway]
aliases: [/posts/kong-gateway/]
description: "Kong gateway 基础知识"
---

## 基本概念

> Kong Gateway is a Lua application running in Nginx. Kong Gateway is distributed along with OpenResty, which is a bundle of modules that extend the lua-nginx-module.

Kong 是一个基于 Nginx 上运行的 Lua 程序。它改善了 Nginx 基于静态配置的缺点，可以动态添加插件和热部署。

![](/images/kong-gateway/Kong.png)

## Kong 的基础模块

**Service**是后端服务的抽象。

**Routes**是 client 到后端服务的路由规则的抽象。如，为不同的 client 设置不同的认证规则。

Kong 的 routes 有两种模式 `traditional_compat` 和 `expressions` 。

- `traditional_compat` ：旧的基于通配符等匹配优先级的模式。
- `expressions` ：新的基于表达式的匹配模式。

**Upstreams**是一个运维对象，在 Services 和真正的后台 API 服务之间，用来负载均衡。

**Plugins**是用 lua 或 go 编写的插件，分为 Kong 官方提供的插件和第三方插件。

## Kong 的工作原理

Kong 支持三类协议：HTTP/HTTPS，TCL/TLS 和 GRPC/GRPCS。每种协议由不同的参数组成：

- `http`: `methods`, `hosts`, `headers`, `paths` (and `snis`, if `https`)
- `tcp`: `sources`, `destinations` (and `snis`, if `tls`)
- `grpc`: `hosts`, `headers`, `paths` (and `snis`, if `grpcs`)

Kong 支持按 HTTP header、URL、method、源地址、目标地址、[Server Name Indication](https://en.wikipedia.org/wiki/Server_Name_Indication) 来路由请求。

Kong 默认以[RFC 3986](https://tools.ietf.org/html/rfc3986)协议对请求的路径处理。

### Kong 匹配规则的优先级

按最多匹配的规则来路由。

> The rule is: **when evaluating a request, Kong Gateway first tries to match the
> routes with the most rules**.

当所有匹配规则检查完，Kong 会通过下层的 Nginx 模块发送请求。Response 返回之后，Kong 再经过`header_filter`和`body_filter`两个 hook 来修改 response header 和 body。

### 对 WebSocket 的支持

有两种配置方式来路由 wss 请求：

- HTTP(S) services and routes：把 wss 流量当作不透明的字节流。
- WS(S) services and routes (**企业版功能**)：可以更好的用 websocket 插件控制流量。

### 负载均衡

Kong 支持两类负载均衡方式

- 基于 DNS （服务注册和发现是静态的）
- 基于哈希环的动态负载均衡（服务注册发现由 Kong 管理，可以动态增删）

这部分跟 Nginx 类似。

### 健康检查

- **active checks**（心跳检查）
- **passive checks**（被动检查，即断路器，根据流量检查）
