---
title: "How to Design an Industry-Standard Audit System"
slug: "audit-system-design"
date: 2024-04-15T16:44:40+08:00
categories: [Software Architecture]
tags: [audit]
aliases: [/posts/audit-system-design/]
description: ""
---
An audit trail is a service within a system that records critical security information such as user behavior logs and control component activity logs. Logs are typically arranged in chronological order, recording "who did what and when."

Below is the Kubernetes official documentation's description of its audit service:

> Kubernetes auditing provides a security-relevant, time-ordered set of records documenting the sequence of activities that affected the system by individual users, by applications using the Kubernetes API, and by the control plane itself.
>
> The audit feature enables cluster administrators to answer the following questions:
>
> - What happened?
> - When did it happen?
> - Who initiated it?
> - On what (which) objects did the activity occur?
> - Where was it observed?
> - Where was it initiated from?
> - What are the subsequent actions taken on the activity?

## What Capabilities Should an Audit System Have?

1. Log content is tamper-proof.
2. Log chain structure is complete: individual log entries cannot be arbitrarily added or removed.
3. Compatibility: clients sending logs should avoid invasive designs.
4. The system's encryption service should be initialized as early as possible to reduce unprotected log exposure.
5. Service restart/shutdown should not cause audit log inconsistency. If a service is shut down under emergency conditions, the audit logs should remain verifiable.
6. Key security: encryption keys (used to compute integrity checks) should be stored in a dedicated key store and reside in memory for the shortest possible time.
7. Performance: ability to verify protected logs within seconds.
8. Log rotation friendliness: audit logs should be compatible with typical log rotation strategies of distributed systems.
9. Observability: logs should be easily parsed (machine-readable) and human-readable. Compatible with mainstream log processor formats, with dimensions designed to facilitate future filtering and screening.

## Related Industry Standards

Common industry standards related to auditing include IEC 62443 and NIST SP 800-92. Below are the audit-related sections in IEC.

| Industry Standard        | Section | Security Level |
| ------------------------ | ------- | -------------- |
| IEC 62443-4-2:2019      | CR2.8   | SL-C 1         |
| IEC 62443-4-2:2019      | CR6.1   | SL-C 1         |
| IEC 62443-4-2:2019      | CR6.2   | SL_C 2         |
| IEC 62443-4-2:2019      | CR1.13  | SL_C 1         |
| IEC 62443-4-2:2019      | CR2.9   | SL_C 1         |
| IEC 62443-4-2:2019      | CR2.10  | SL_C 1         |
| IEC 62443-4-2:2019      | CR3.7   | SL_C 1         |
| IEC 62443-4-2:2019      | CR3.9   | SL_C 2         |

## What Protocols or Standards Should Audit Log Format Follow?

For locally running software, Syslog typically has better system compatibility. For projects using ELK to collect logs, CEF is more suitable. In other cases, custom JSON is recommended.

Below is a comparison of the three formats (protocols).

### [Common Event Format (CEF)](https://docs.elastic.co/en/integrations/cef)

A log format used by Elastic-Search, designed based on event-sourcing principles. The advantage is less redundant information, suitable for building monitoring systems in conjunction with the ELK stack. Its transport is based on the Syslog protocol while extending readable key-value pairs. The text-based design also allows CEF-format logs to be written to files. Overall, it is the most balanced of these formats in terms of readability, efficiency, and standardization.

### [Syslog](https://datatracker.ietf.org/doc/html/rfc5424)

Syslog is the default audit log format for Linux operating systems, typically using its RFC 5424 version. Most SIEM[^1] systems support importing this format.
The Syslog protocol has great adaptability, and mTLS-based Syslog transport can maximize system security while remaining compatible with traditional software. However, for microservices, implementing and maintaining the standard protocol is costly. Therefore, services like AWS CloudTrail and OpenTelemetry have opted for the simpler HTTPS + JSON format.

[^1]: SIEM stands for Security Information and Event Management. <https://www.microsoft.com/en-us/security/business/security-101/what-is-siem>

### [JSON Lines](https://jsonlines.org/)

Most SaaS products use JSON—it's simple and efficient. JSON has the characteristic of more redundant information, but the structure is easy to parse. For example, below are the fields in the log model mentioned in the [OpenTelemetry official documentation](https://opentelemetry.io/docs/specs/otel/logs/data-model/):

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
| Attributes           | Additional structured information.           |

## What Security Requirements Apply to Audit Logs?

For audit logs, security requirements are higher than for general log systems.

Security can typically be considered from three dimensions: Confidentiality, Integrity, and Availability.

### Confidentiality

Attackers can exploit system security vulnerabilities to obtain special privileges and then view certain audit logs.

The following measures can be taken:

- Encrypt logs: use encryption technology to protect logs, ensuring that only authorized users can access and modify them.
- Access control: restrict access to log-sending and log-receiving interfaces.
- Sensitive information filtering: do not record user sensitive information in logs, such as passwords, certificates, etc.

### Integrity

Attackers can exploit system security vulnerabilities to modify or delete certain audit logs.

In addition to the encryption and access control mentioned above, the following measures can also be taken:

- Integrity checks[^2]: add hash values to log entries so that any tampering or truncation can be quickly detected during log verification.
- Regular backups: regularly back up logs to prevent attackers from deleting or modifying all log entries.

**Log file limitations**: in addition to limiting the size of log files, it's typically necessary to limit the number of backups, maximum backup days, etc. Below are the parameters in Kubernetes for log file storage:

- `--audit-log-path` specifies the log file path used to write audit events. If this flag is not specified, the log backend is disabled.
- `--audit-log-maxage` defines the maximum number of days to retain old audit log files.
- `--audit-log-maxbackup` defines the maximum number of audit log files to retain.
- `--audit-log-maxsize` defines the maximum size (in megabytes) of audit log files before rotation.

[^2]: For log encryption, the server typically adds an additional checksum chain to logs for verification. You can refer to Amazon's implementation of [server-side encryption (SSE-S3)](https://docs.aws.amazon.com/AmazonS3/latest/userguide/UsingServerSideEncryption.html).

### Availability

Attackers can attack the audit trail service, causing the audit trail service to run out of memory, disk space, etc.

The audit service should cache audit-related context, such as the mapping between service names and IDs, event IDs and descriptions, etc. When different services send messages to the audit service, the message structure should be designed with minimal length as a principle. The audit service's policy should allow users to configure log levels, filter rules, etc., to reduce system burden.

## Log Export

In addition to exporting file-format logs, the audit service usually needs to support export to third-party systems. We typically refer to third-party services that analyze and store logs as SIEM (Security Information and Event Management). In Kubernetes, the module that exports logs to third-party web services is called a webhook.

Exporting to third-party systems can typically use the standard Syslog format or JSON Lines, which has the widest support. Additionally, you need to consider log truncation, and the configuration of third-party systems' batch and stream processing. You can refer to [this Kubernetes document](https://kubernetes.io/zh-cn/docs/tasks/debug/debug-cluster/audit/#webhook-backend).

## Architecture Designs of Open-Source Projects

Due to different design focuses, each of the following open-source projects needs careful consideration of its advantages and disadvantages, whether its features meet your needs, and whether the system environment is distributed or monolithic.

### Auditd

![auditd-architecture](/images/audit-system-design/Linux-Auditd-Architecture.png)

The default audit service for most Linux systems, when paired with tools like rsyslog, can solve local device log collection, viewing, and filtering. rsyslog's string template-based log format configuration can meet the integration needs of users using different SIEM systems.

- Advantages: process-based communication, standard log format, easy export. Excellent performance.
- Disadvantages: the process model is not suitable for network services.

### AWS Cloud Trail and Kubernetes

![aws log](/images/audit-system-design/aws-audit.png)

AWS CloudTrail adopts a model where application services actively push audit events. Users can set policies for designing tracking services, and the collected logs flow as needed into subsequent batch and stream processing toolchains.

Kubernetes's log collection is similar to AWS's implementation, also based on a centralized service, but this architecture is not designed solely for audit logs. It follows many Kubernetes declarative design philosophies and is well worth studying.

![kubernetes log](/images/audit-system-design/k8s-audit.png)

For example, Kubernetes has stages specifically designed for auditing:

> Each request can be recorded with its associated stages. The defined stages are:
>
> - RequestReceived - The stage corresponds to the event generated when the audit handler receives a request, and before delegating to the remaining handlers.
> - ResponseStarted - The event is generated after the response message headers are sent, but before the response message body is sent. Only long-running requests (such as watch) generate this stage.
> - ResponseComplete - When the response message body is complete and no more data needs to be transmitted.
> - Panic - Generated when a panic occurs.

[Kubernetes audit events](https://kubernetes.io/zh-cn/docs/tasks/debug/debug-cluster/audit/) use a different message structure from the Event API[^3].

In summary, the cloud platform's audit service design can be summarized as:

- Advantages: microservice design, more flexible JSON format logs, centralized log collection service easily integrates with more application services and exports to open-source data processing tools.
- Disadvantages: distributed architecture requires higher storage, server-side encryption, communication security, and integrity.

[^3]: [Kubernetes audit event structure definition](https://kubernetes.io/zh-cn/docs/reference/config-api/apiserver-audit.v1/#audit-k8s-io-v1-Event)

### OpenTelemetry

![OpenTel](/images/audit-system-design/opentel.png)

OpenTelemetry is currently the most mainstream logging framework in cloud-native environments. It supports both invasive (SDK) and non-invasive (Agent) log collection modes. The Collector design allows some log processing work to be done on the log sender side.

- Advantages: microservice design, supports infrastructure like Kubernetes, multi-language and multi-platform SDK and extensibility. Comprehensive security and integrity considerations. Suitable for small and medium-sized enterprises.
- Disadvantages: in most cases, log collection still requires invasive modification of code inside the app. Log collection tools don't support languages like Go well (as of this writing).

## Summary

An audit trail refers to the time-ordered records of all operations or events affecting the system, used to track system activity and verify whether violations have occurred.

Audit logs should have the following characteristics:

- Tamper-proof (encrypted storage, integrity verification)
- High performance (fast verification)
- Observability (machine/human readable)
- Security (confidentiality, availability, integrity)

Common audit log formats include Syslog, CEF, and JSON, with the main differences being redundant information, readability, and compatibility with log collection systems.

Audit logs have high security requirements:

- Confidentiality: only authorized users can access, achieved through access control
- Availability: prevent deletion or destruction by attackers, achieved through resource limits, multi-replica storage, etc.
- Integrity: prevent tampering or truncation, achieved through encryption, integrity verification, etc.

Some typical audit log system architectures:

- Native Linux log programs such as Auditd, rsyslog
- Cloud products like AWS
- OpenTelemetry
