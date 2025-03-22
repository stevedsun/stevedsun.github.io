---
title: "与AI协作编程──痛点篇"
date: 2025-03-23T00:00:01+08:00
categories: [Software Architecture]
tags: [AI]
aliases: [/posts/ai-promgramming/]
description: ""
---

在与 AI 协作编程中，经常遇到一些大模型无法正确执行的情况。最常见的有：

- 任务死循环
- 模型无法修复环境问题
- 模型执行长任务后半段忘记上下文

## 一些使用经验

以我自己为例，我经常使用 Cline + Github Copilot 的组合。我很喜欢 Cline 的功能是 `Checkpoint restore`，它可以在执行错误的位置重新编辑提示词执行。这让我可以在相同的任务中调用不同的模型，观察他们处理问题的能力。

用作规划（Plan）的模型通常用 Deepseek-R1，Gemini 2.0 Flash Thinking，Claude 3.7。这里除了 Claude 3.7 能够比较准确给出计划外，其他模型多少都容易走「歪路」， 比如 Deepseek-R1 喜欢做一些多余的事情，让它翻译中文，它会调用 MCP 的翻译服务而不是自己翻译。

从经济角度考虑，解决简单问题 Gemini 2.0 Flash Thinking 是比较快速、经济的模型。复杂问题直接上 Claude 3.7 可能更容易控制成本。

用作执行任务（Act）的模型里，Deepseek-V3 表现非常不稳定，经常死循环或丢失上下文。Claude 太贵，而 Gemini 2.0 Flash 是相对准确且划算的模型。置于国产的 Qwen 系列模型不完全支持 Function Calling，Cline 也没有适配，所以暂时无法测试。

## AI 编程疑难杂症的应对方法

最近读到[AI Blindspots](https://ezyang.github.io/ai-blindspots/)这篇文章，作者系统性整理了 AI 编程中遇到的问题和他的思路。对我非常有启发。我用 Agent 把它翻译成了中文并人工做了润色，你可以在这里读到：[AI 编程的盲点](https://sund.notion.site/AI-1be8ce9d275d80649a29e541d310d5c5)。

概括起来，解决 AI 问题的核心要领还是三点：更准确的提示词、更完整的上下文、缩小问题规模。

相信随着技术的发展，编程范式会发生翻天覆地的变化。如果重构变得如此容易，那么马丁福勒的《重构》是否应该出一套 AI 时代下的新范式。如果文档不再是被人读，而是喂给模型当作上下文，那么文档的形态应该是什么样？是否提供一个向量化的文档接口供大模型调用，将是未来编程框架的新常态？

我对未来充满期待。
