---
title: "RESTful Web Service Cookbook 笔记"
date: 2024-07-13T16:12:34+08:00
categories: [Cloud Native Computing]
tags: [api]
aliases: [/posts/restful-api-cookbook/]
description: ""
---

[RESTful Web Service Cookbook](https://www.oreilly.com/library/view/restful-web-services/9780596809140/) 是一本简短、精炼的 RESTful 接口设计指南。这篇文章（笔记）用来记录这本书中提到的重点。

> 因为 RESTful 对后端开发来说实在太熟悉不过，所以我会省略掉那些习以为常的约定，只记录书中提到的、大多数开发者没有注意到的细节。

## HTTP Method

### GET

进行**安全**与**幂等**的信息获取。

### POST

执行的目标是一个资源集合（工厂），而不是具体的 URI。

适用场景：

- 创建新的资源,把资源作为一个工厂。
- 通过一个控制器资源来修改一个或多个资源。
- 执行需要大数据输入（参数较多）的查询。
- **在其他 HTTP 方法看上去不合适时，执行不安全或非幂等的操作**。

解决方案：

- 将一个已存在的资源标识为创建新资源的工厂。虽然您可以把任意资源用做工厂,但常见的做法是使用一个集合资源。
- 让客户端向工厂资源提交附有需要创建资源的表述的 POST 请求。通过可选支持的 **Slug** 头, 客户端可以向服务器建议一个名字,作为被创建资源的 URI 的一部分。
- 资源创建之后,返回响应码 **201(Created)**,并在 **Location** 头中包含新创建资源的 URI。
- 如果响应正文包含了新创建资源的完整表述,那么在 **Content-Location** 头中包含新创建资源的 URI。

### PUT

仅在客户端可以控制 URI 的构成时,才使用 PUT 方法创建新资源。**（换句话说，PUT 也可以创建资源，但是仅限于客户端可以指定 URI）**

## 确定资源对象的粒度

应该以适合客户端使用模式的方式来设计资源,而不是基于现有的数据库或对象模型。

- 可缓存性
- 减小修改频率
- 可变性——分离可变和不可变数据

### 如何设计复合资源?

**复合资源**降低了统一接口的可见性,因为它们的表述中包含了和其他资源相重叠的数据。

- 如果符合资源使用**频率不高**，可以考虑用**缓存**替代。
- 考虑网络开销，复合资源会不会降低服务端吞吐量，增大延时。

## HTTP Body

以 JSON 格式的 Body 为例：

1. 最好包含一个指向 self 的链接
2. 如果分页，最好包含下一页的链接
3. 如果分页，要指示集合的大小（总数）
4. 如果查询对象是本地化的，添加一个属性来表示本地化内容的语言

```json
{
  "name": "John",
  "id": "urn:example:user:1234",
  "link": {
    "rel": "self",
    "href": "http://www.example.org/person/john"
  },
  "address": {
    "id": "urn:example:address:4567",
    "link": {
      "rel": "self",
      "href": "http://www.example.org/person/john/address"
    }
  }
}
```

## HTTP Response

1. 对于客户端错误，返回 4xx 状态码 + Date （错误发生的时间）。
2. 对于服务端错误，返回 5xx 状态码 + Date （错误发生的时间）。
3. Body 中要描述错误，如果有外部文档和链接可参考，在 Header 提供一个 Link 头或直接把链接写在 Body 里。
4. 为了后期追踪或分析，在服务器上记录了错误日志，应该提供一个可以找到该错误的标识符或链接。

## 设计查询结构

### 设计查询请求

1. 为了缓存和性能，尽量避免范围查询。解决方法包括：
   - 使用预定义查询
   - 也可以使用 HTTP Header： Range
2. 避免使用通用语言（SQL、XPATH）的查询。
3. 避免 URI 和数据存储方式的紧耦合（前端把后端当作数据库）。
4. 对于参数较多，可以考虑使用 POST（因为 URI 长度有最大限制）
   - POST 接口的缺点是丧失了缓存能力
   - POST 请求是不可缓存的，所以 Cache-Control 和 Expires 头无济于事
   - 解决缓存问题，可以让 POST 创建一个临时资源，把 link 返回前端，前端下次用 GET 获取该资源

### 设计查询响应结果

1. 返回集合。添加合理的缓存过期头。
2. 如果没有结果，应该返回**空集合**。