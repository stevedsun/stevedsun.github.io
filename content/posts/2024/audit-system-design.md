---
title: "如何设计一个符合工业标准的审计系统"
date: 2024-04-15T16:44:40+08:00
categories: [Cloud Native Computing]
tags: [audit]
aliases: [/posts/audit-system-design/]
description: ""
---

审计追踪（Audit Trail）是指一个系统中用于记录用户行为日志、控制组件的活动日志等关键安全信息的服务。日志通常以时间顺序排列，记录了“谁在什么时间做了什么”。

下面是 Kubenetes 官方文档对其审计服务的描述：

> Kubernetes 审计（Auditing） 功能提供了与安全相关的、按时间顺序排列的记录集，记录每个用户、使用 Kubernetes API 的应用以及控制面自身引发的活动。
>
> 审计功能使得集群管理员能够回答以下问题：
>
> - 发生了什么？
> - 什么时候发生的？
> - 谁触发的？
> - 活动发生在哪个（些）对象上？
> - 在哪观察到的？
> - 它从哪触发的？
> - 活动的后续处理行为是什么？

## 审计系统应该具备哪些能力？

1. 日志内容不可篡改。
2. 日志链结构完整：不可任意添加或删除单独的日志条目。
3. 兼容性：发送日志的客户端应该避免侵入式设计。
4. 系统的加密服务应该尽早初始化，以减少未受保护的日志。
5. 服务重启/关闭不应导致审核日志不一致。如果服务因紧急情况而关闭，审计日志应该是可验证的。
6. 密钥安全性：加密密钥（用于计算完整性检查）应存储在专用密钥存储中，并在内存中驻留最短的时间。
7. 性能：能够在几秒钟内验证受保护日志。
8. 日志轮换友好性：审核日志应与分布式系统典型的日志轮换策略兼容。
9. 可观测性：日志易于被解析（machine-readable）、人类可读（human-readable）。兼容主流日志处理程序的格式，维度设计便于日后做过滤筛选。

## 涉及的行业标准

与审计相关的，常见的工业标准有 IEC62443、NIST SP 800-92。下面是 IEC 中涉及到审计相关的章节。

| 工业标准           | 章节   | 安全级别 |
| ------------------ | ------ | -------- |
| IEC 62443-4-2:2019 | CR2.8  | SL-C 1   |
| IEC 62443-4-2:2019 | CR6.1  | SL-C 1   |
| IEC 62443-4-2:2019 | CR6.2  | SL_C 2   |
| IEC 62443-4-2:2019 | CR1.13 | SL_C 1   |
| IEC 62443-4-2:2019 | CR2.9  | SL_C 1   |
| IEC 62443-4-2:2019 | CR2.10 | SL_C 1   |
| IEC 62443-4-2:2019 | CR3.7  | SL_C 1   |
| IEC 62443-4-2:2019 | CR3.9  | SL_C 2   |

## 审计日志的格式应遵循哪些协议或标准？

对于本地运行的软件，通常 Syslog 具有更好的系统兼容性。对于使用 ELK 采集日志的项目更适合用 CEF，其他情况建议使用自定义的 JSON。

下面是三种格式（协议）的对比。

### [Common Event Format (CEF)](https://docs.elastic.co/en/integrations/cef)

Elastic-Search 使用的、一种基于 Event-souring 思想设计的日志格式。优点是冗余信息少，适合配合 ELK 体系构建监控系统。

### [Syslog](https://datatracker.ietf.org/doc/html/rfc5424)

Syslog 是 Linux 操作系统默认的审计日志格式，通常采用其 RFC5424 版本。大部分 SIEM[^1] 系统都支持这种格式的导入。
Syslog 协议适配性很好，基于 mTLS 的 Syslog 传输可以在兼容传统软件的同时，最大程度保证系统的安全性。但是对于微服务来说，实现和维护标准协议成本较高。所以如 AWS CloudTrail, OpenTelemetry 等都选择更简单的 HTTPS + JSON 格式。

[^1]: SIEM 是安全信息和事件管理(Security Information and Event Management)的缩写。<https://www.microsoft.com/en-us/security/business/security-101/what-is-siem>

### JSON

大部分 SaaS 产品都是用 JSON，简单高效。例如，下面是[OpenTelemetry 官方文档](https://opentelemetry.io/docs/specs/otel/logs/data-model/)提到的日志模型中的字段：

| Field Name           | Description                                  |
| -------------------- | -------------------------------------------- |
| Timestamp            | Time when the event occurred.                |
| ObservedTimestamp    | Time when the event was observed.            |
| TraceId              | Request trace id.                            |
| SpanId               | Request span id.                             |
| TraceFlags           | W3C trace flag.                              |
| SeverityText         | The severity text (also known as log level). |
| SeverityNumber       | Numerical value of the severity.             |
| Body                 | The body of the log record.                  |
| Resource             | Describes the source of the log.             |
| InstrumentationScope | Describes the scope that emitted the log.    |
| Attributes           | Additional information about the event.      |

下面是 K8s apiserver 关于 Audit 消息格式定义的例子：

```json
{
  "apiVersion": "audit.k8s.io/v1",
  "kind": "Event",
  "level": "Metadata",
  "auditID": "12345678-1234-1234-1234-1234567890ab",
  "stage": "ResponseComplete",
  "requestURI": "/api/v1/namespaces/default/pods",
  "verb": "get",
  "user": {
    "username": "admin",
    "uid": "1234",
    "groups": ["system:masters"],
    "extra": {
      "someKey": ["someValue"]
    }
  },
  "sourceIPs": ["192.168.1.1"],
  "userAgent": "kubectl/v1.20.0 (linux/amd64) kubernetes/abcdef",
  "objectRef": {
    "resource": "pods",
    "namespace": "default",
    "name": "my-pod",
    "uid": "abcdef12-3456-7890-abcd-ef1234567890",
    "apiVersion": "v1",
    "resourceVersion": "12345",
    "subresource": "status"
  },
  "responseStatus": {
    "metadata": {},
    "status": "Success",
    "code": 200
  },
  "requestObject": {
    "metadata": {
      "name": "my-pod",
      "namespace": "default"
    },
    "spec": {
      "containers": [
        {
          "name": "my-container",
          "image": "my-image"
        }
      ]
    }
  },
  "responseObject": {
    "metadata": {
      "name": "my-pod",
      "namespace": "default",
      "resourceVersion": "12345"
    },
    "spec": {
      "containers": [
        {
          "name": "my-container",
          "image": "my-image"
        }
      ]
    },
    "status": {
      "phase": "Running"
    }
  },
  "requestReceivedTimestamp": "2023-05-21T12:34:56Z",
  "stageTimestamp": "2023-05-21T12:34:57Z",
  "annotations": {
    "authorization.k8s.io/decision": "allow",
    "authorization.k8s.io/reason": "RBAC: allowed by RoleBinding \"admin-binding\""
  }
}
```

## 对于安全性有哪些要求？

对于审计日志来说，安全性要求会被一般日志系统更高。

安全性，通常可以从机密性（Confidentiality），完整性（Integrity），可用性（Availability）三个维度来考量。

### 机密性

攻击者可以通过系统的安全漏洞，获取特殊权限，进而查看某些审计日志。

可以采取以下措施：

- 加密日志：使用加密技术对日志进行保护，确保只有授权用户能够访问和修改日志。
- 访问控制：限制对发送、接收日志接口的访问权限。
- 敏感信息过滤：不应该在日志中记录用户敏感信息，如密码、证书等。

### 完整性

攻击者可以通过系统的安全漏洞，修改、删除某些审计日志。

除了上面提到的加密和权限控制，还可以采取以下措施：

- 完整性检查[^2]：在日志条目中添加哈希值，以便在验证日志时能够快速检测到任何篡改或截断。
- 定期备份：定期备份日志，以防止攻击者删除或修改所有的日志条目。

[^2]: 对于日志的加密，一般在服务端会对日志额外添加 checksum 链来校验。可以参考亚马逊的实现 [server-side encryption (SSE-S3)](https://docs.aws.amazon.com/AmazonS3/latest/userguide/UsingServerSideEncryption.html).

### 可用性

攻击者可以攻击审计追踪服务，导致审计追踪服务内存、磁盘空间不足等。

- 设置最大用量限制：对内存、磁盘等服务器资源做出限制。
- 监测和响应：及时监测系统资源指标和日志的变化，并对异常活动进行响应。

**审计上下文**：记录审计日志会显著增加系统内存和流量的使用。所以审计服务应该缓存审计相关的上下文，如服务名称和 ID 的映射关系、事件 ID 和描述等。不同服务向审计服务发送消息时应以最小长度为原则设计消息结构。审计服务的策略中应该允许用户配置日志级别，过滤规则等以减少系统负担。

## 开源项目的架构设计

由于设计侧重点不同，下面提供的每种开源项目都需要慎重考虑其优点和不足，其特性是否满足自身需要、系统的环境是分布式还是单体应用。

### Auditd

大部分 Linux 默认的审计服务，配合 rsyslog 等工具，可以解决本地设备的日志采集、查看、过滤。 rsyslog 基于字符串 template 的日志格式配置可以满足使用不同 SIEM 系统的用户集成的需要。

- 优点：基于进程通信，标准日志格式，易于导出。性能优异。
- 不足：进程模型不适用于网络服务。

### AWS Cloud Trail 和 Kubenetes

![aws log](/images/audit-system-design/aws-audit.png)

AWS 的 Cloud Trail 采用应用服务主动推送审计事件的模式，用户可以为设计追踪服务设置策略，收集到的日志会分别按需流入后续的批处理和流处理工具链中。

K8s 的日志收集与 AWS 实现类似，也是基于中心化的服务，但是这套架构设计并非只为审计日志一种情况设计。它遵循了很多 K8s 声明式设计的理念，非常值得学习。

例如 K8s 专门为审计设计的 stage：

> 每个请求都可被记录其相关的阶段（stage）。已定义的阶段有：
>
> - RequestReceived - 此阶段对应审计处理器接收到请求后， 并且在委托给其余处理器之前生成的事件。
> - ResponseStarted - 在响应消息的头部发送后，响应消息体发送前生成的事件。 只有长时间运行的请求（例如 watch）才会生成这个阶段。
> - ResponseComplete - 当响应消息体完成并且没有更多数据需要传输的时候。
> - Panic - 当 panic 发生时生成。

![k8s log](/images/audit-system-design/k8s-audit.png)

[K8s 审计事件](https://kubernetes.io/zh-cn/docs/tasks/debug/debug-cluster/audit/) 使用和 Event API 不同的消息结构[^3]。

综上，云平台的审计服务设计可以总结为：

- 优点：微服务设计，JSON 格式日志更灵活，中心化的日志收集服务易于集成更多应用服务和导出到开源数据处理工具。
- 不足：分布式架构对存储、服务端加密、通信安全性和完整性要求更高。

[^3]: [K8s 审计事件结构定义](https://kubernetes.io/zh-cn/docs/reference/config-api/apiserver-audit.v1/#audit-k8s-io-v1-Event)

### OpenTelemetry

![OpenTel](/images/audit-system-design/opentel.png)

OpenTelemetry 是现在云原生最主流的日志框架。可以支持侵入式（SDK）、非侵入式（Agent）两种日志采集模式。Collector 的设计可以让一部分日志处理的工作放在日志发送端完成。

- 优点：微服务设计，支持 K8s 等基础设施，多语言多平台提供了 SDK 和扩展能力。有完善的安全、完整性考虑。适合中小企业。
- 不足：大部分情况下日志采集依然需要侵入到 App 内部修改代码。日志收集工具对 Go 等语言支持不够好（截至本文编辑时）。

## 小结

审计追踪（Audit Trail）是指系统记录下所有影响操作或事件的时间顺序记录,用于追踪系统活动，核查是否存在违规行为。

审计日志应具备以下特性:

- 不可篡改(加密存储、完整性校验)
- 高性能(快速验证)
- 可观测性(机器/人类可读)
- 安全性(保密性、可用性、完整性)

常见的审计日志格式有 Syslog、CEF、JSON 等,主要区别在于冗余信息、可读性和与日志收集系统的兼容性。

审计日志具有较高的安全性要求：

- 机密性：只有授权用户可访问,通过访问控制实现
- 可用性：防止被攻击者删除或破坏,通过限制资源使用、多副本存储等实现
- 完整性：防止被篡改或截断,通过加密、完整性校验等实现

一些典型的审计日志系统架构：

- Auditd(Linux 默认) + rsyslog 等工具，基于进程通信
- AWS CloudTrail 等云产品方案
- Kubernetes 架构
- OpenTelemetry 开源框架
