---
title: "Monitoring System Project Retrospective"
slug: "metrics-project-retro"
date: 2024-10-24T15:52:22+08:00
categories: [Software Architecture]
tags: [edge-computing]
aliases: [/posts/metrics-project-retro/]
description: ""
---

This article is a retrospective of a large chunk of my work over the past 3 years. As the project's architect, I'll also reflect on some issues left over from the early stages of the project and share my personal approach to solving them.

## The Project Relies Heavily on an Open-Source Component, Over-Customized

Our project is a collection/monitoring system for logs and software/hardware performance metrics that runs on edge devices. Considering the performance of edge computing devices (IPCs), when selecting open-source components, we emphasized being lightweight and supporting a rich set of output standards. In the early days, the department architect chose Fluent-Bit as the core component. Fluent-Bit is an open-source, lightweight, mildly extensible data collector written in C. It was originally used for log collection and has gradually evolved into a full-featured Agent. Compared to the popular [OpenTelemetry](https://github.com/open-telemetry), Fluent-Bit is more out-of-the-box and lighter, but harder to modify and extend.

At the very beginning, the whole team had no experience with monitoring systems, so we dug quite a few pitfalls when designing the system. First, users had to perform overly cumbersome operations on the UI, having to sequentially configure the output target (address, port, protocol, format, encryption method, etc.), the type of metrics to collect, and finally click "Apply" manually.

After several iterations, we appropriately simplified the operational logic. But like most programs running on industrial PCs, users typically don't actively modify the configuration on the UI after initial setup. End users care more about system resource usage and stability. So initially, the team designed this project as a heavy-interaction consumer-facing product—which was a lesson learned.

Second, to accommodate the UI design flow (for example, allowing users to create multiple different configuration items to different target addresses), the backend developers came up with complex workarounds. Because Fluent-Bit is a single-process event-driven model with only a single configuration file, every time the configuration file is modified, the Fluent-Bit process must be restarted. This created a risk of **data loss during restarts** for a stable-running monitoring system. Additionally, if **a newly added configuration item is wrong, it can cause the entire generated configuration file to fail, leading to issues like the Fluent-Bit process hanging**.

To solve these problems, the backend engineers came up with various tricks using Fluent-Bit's parameters. For example, using different tags to route different user configuration items, configuring parameters and filter rules separately for each configuration item. Another example was setting the cache data packet size and cache timeout to 0, so that after Fluent-Bit restarts, it would first try to resend the data cached in the file system, indirectly preventing user data loss.

These tricks not only increased maintenance difficulty but, from the user's perspective, did not bring any real value improvement.

In retrospect, **if the early UI design had been changed to a separate configuration page, it would have simplified the operational flow and reduced the complexity of business code.**

Third, the core project's dependency on Fluent-Bit made it very difficult to migrate to other open-source components. Combined with Fluent-Bit's high update frequency, the company's security compliance requirements meant our team had to upgrade Fluent-Bit periodically, while also doing regression testing for all configuration options. Adding to this, Fluent-Bit has very poor customizability; while it supports implementing Output plugins in Go, Input plugins can only be written in C. As a result, to collect data from internal applications, we had to use its TCP and HTTP plugins as intermediaries, deploying multiple Agents to collect data from different internal services. This made later integration testing even more difficult.

Overall, Fluent-Bit's performance basically met expectations, but various small bugs (for example, the pgsql plugin would block the entire process when the target was unreachable) were not taken seriously by the open-source community maintainers, and the code we submitted to the open-source community was rejected for various reasons. If I had to choose again, I would lean toward using other more extensible open-source components.

## Unfamiliarity with Go Led to Chaotic Project Structure

The second challenge the team faced was unfamiliarity with Go. Most of the development members only had Java development experience, so naturally, they wrote Go like Java. Due to the limitations of the framework (Go-Gin), problems arose frequently during development.

The first problem came from object orientation and dependency inversion. Dependency inversion is not unfamiliar to those using Java Spring, but implementing dependency inversion in Go requires using Interface encapsulation, combined with the Go-Mock library for unit testing. Team members unfamiliar with the language's features often incorrectly encapsulated abstractions, or simply nested functions inside functions, writing [spaghetti code](https://zh.wikipedia.org/zh-sg/%E9%9D%A2%E6%9D%A1%E5%BC%8F%E4%BB%A3%E7%A0%81). This fully exposed the fact that most domestic Java programmers have not actually received good OOP training. Engineering practices like unit testing and integration testing are also formalistic. Software quality in most enterprises still relies on manual verification by testers.

The second problem is that Go discourages over-abstraction. For things like generics and exception handling, you have to repeat trivial code snippets step by step, which causes Sonar static checks to fail often. Inexperienced colleagues would then use various clever tricks to evade static checks. This also demonstrates the necessity of regular code reviews for development teams.

Fourth, Go is actually a programming language with a less-than-complete community. Many of its frameworks (like the most popular gorm, which is actually a personal project), and tools mature in the Java toolchain like Flyway, need to be replaced by combining multiple open-source projects in Go. So Go is only suitable for developing projects of medium or smaller scale, or for performance-critical platform core components. (Domestically) it isn't suitable for complex business scenarios.

## API Granularity Too Fine, Resource Objects Not Properly Abstracted

In the early days, the team was plagued by management chaos: architecturally, business models weren't properly abstracted, and resource objects were broken into too many small pieces; management-wise, tasks were decomposed too simplistically, with each colleague individually responsible for a module, leading to dedicated APIs designed for every business process, creating heavy maintenance pressure. Fortunately, with few business scenarios, automated testing could ensure interface reliability to some extent.

At first, when doing automated integration testing, we still used BDD form, writing tests based on business operations. Later, we gradually realized that for this kind of monitoring system, the real user operation logic is actually very simple—what's complex are the exceptions that may arise from different types of data, different Input, and Output configurations. So we switched to data-driven testing, using configuration files to comprehensively test different types of Fluent-Bit configurations.

In summary, the modifications to Fluent-Bit configuration could actually be implemented entirely with 3~4 broad APIs. In addition to the over-designed flow mentioned earlier, the uncertainty in the early project stages caused developers to over-focus on loose coupling while ignoring maintainability.

## Flawed Pipeline Design

Initially, the project followed the integration testing and deployment pattern of other teams in the department, putting Python-written test cases and project deployment scripts in a separate Gitlab repo. The result was that every time the project was deployed, someone had to manually go to a webpage to modify the version number to trigger the pipeline. From a continuous integration perspective, having business code and test cases separated meant that every commit had to be submitted to a different repo, and in case of conflicts, multiple integration tests had to be run separately (long time, slow feedback).

Later, we made some adjustments, merging multiple small modules into a [Monorepo](https://zh.wikipedia.org/wiki/Monorepo), while putting some API-related integration tests inside the backend code to reduce the number of commits and make atomic commits easier.

However, the deployment problem remained unresolved, because there were too many modules on the edge platform, system integration required cooperation from multiple teams, deployment and release cycles were long, and there were too many points of failure. For this situation, the department's technical lead set strict processes for code submission, testing, review, and documentation updates, but the root problem was still ambiguous team responsibilities, the department's teams spanning multiple countries and time zones, and the lack of a unified scheduling and communication mechanism. These problems can only be gradually alleviated by management, or as the business converges, reducing and diverting project teams.

## Summary

Overall, many of the problems our team encountered stemmed from a lack of project and technical team management experience in the project's early stages. Not understanding the business vision, they brought their experience in making consumer-facing SaaS products to the industrial sector, applying familiar development paradigms to manufacturing. Of course, to be honest, on the business side, the department has many long processes, and business leaders can only feel around blindly; user feedback has to first reach the Support team, then be reported upward, and only finally reach the development team. This meant that the products we developed took at least 3-6 months to receive effective feedback. Iteration cycles were too long, and R&D worked in isolation.
