---
title: "为什么不应该让AI生成单元测试"
date: 2025-05-01T09:27:36+08:00
categories: [随笔]
tags: []
aliases: [/posts/do-not-vibe-testing/]
description: ""
---

最近听到 Gru.ai 创始人张海龙老师在一档[播客节目](https://www.xiaoyuzhoufm.com/episode/671c9a42eb46cd6655da1e6f?s=eyJ1IjogIjVlN2M2M2UzYjNjNWJjYTVmNjQxMTJkNCJ9)中提到自动生成 Unit Testing 是他们在做 AI Coding 的主要方向。

Gru.ai 官网上有这么两句话：

> Forget about unit testing – get covered automatically (忘记单元测试 - 自动覆盖)
> Harness the expertise of AI engineers to boost your team's testing efficiency while reducing costs and ensuring top-notch quality. (利用 AI 工程师的专业知识来提高团队的测试效率，同时降低成本并确保一流的质量。)

张海龙老师在 AI Coding 方向的洞见让我很有启发。我只是对用 AI 写测试降本增效这种说法，持怀疑态度。我想他们在写第二句话时还有点不自信，最后还要画蛇添足补充一句 ensuring top-notch quality（确保一流质量）。

单元测试是需求的具象化。是整个测试体系中最小粒度、最贴近代码实现的约束工具。单元测试不仅被用来检查代码是否满足需求，更多时候，被用来检测边界条件（Corner Case），因为一段程序是否可靠，最重要的是在边界条件下它不会出错。这也是有经验的人类工程师区别于初级工程师的特点。

但是 Gru.ai 在做的，是用**AI 提高单元测试覆盖率， 众所周知，覆盖率提高不等价于测试效率提高，更不等于质量提高**。

用一句提示词让 AI 自动帮你写出可以运行的单元测试。这对初级程序员来说非常具有诱惑力。好比一个射击运动员为了提高射击准确度，每次先开枪，然后在子弹坑附近画上靶子。

提升测试覆盖率的目的，是让人类工程师充分考虑边界条件。AI 辅助人类生成测试是一种节省时间的做法，这无可厚非，而 Gru.ai 却让我们「忘记单元测试，自动覆盖」。但 AI 大多时候不清楚边界条件，除非人类显式地告诉它。那么 AI 如何自动推断边界条件？我们又如何确信 AI 推断的边界条件是正确的？AI 测试了代码，谁来测试 AI ？

如果说 Cursor 这类 AI Coding 产品凝聚了硅谷程序员们对 Vibe Coding 的想象，那么 Gru.ai 就是中国程序员们对 Vibe Testing 的「美好期望」。
