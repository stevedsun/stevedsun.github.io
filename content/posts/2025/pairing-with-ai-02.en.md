---
title: "Pairing with AI for Coding—Pain Points"
slug: "pairing-with-ai-02"
date: 2025-03-23T00:00:01+08:00
categories: [AI]
tags: [vibe coding]
aliases: [/posts/ai-promgramming/]
description: ""
---

When pairing with AI for coding, you often run into situations where large models fail to execute tasks correctly. The most common are:

- Endless task loops
- Models unable to fix environment issues
- Models losing context in the second half of a long task

## A Few Lessons from My Use

For my own use, I often pair Cline with GitHub Copilot. What I really like about Cline is its `Checkpoint restore` feature, which lets you re-edit the prompt and resume execution at the point where something went wrong. This lets me call different models for the same task and observe how each handles the problem.

For planning (Plan), I usually use Deepseek-R1, Gemini 2.0 Flash Thinking, or Claude 3.7. Among these, only Claude 3.7 can produce a relatively accurate plan; the others are more or less prone to going off-track. For example, Deepseek-R1 likes to do extra work—when you ask it to translate Chinese, it calls an MCP translation service instead of translating it itself.

From a cost perspective, Gemini 2.0 Flash Thinking is a fast and economical model for simple problems. For complex problems, going straight to Claude 3.7 may be easier to keep costs under control.

For task execution (Act), Deepseek-V3 is very inconsistent—it often gets stuck in loops or loses context. Claude is too expensive, while Gemini 2.0 Flash is a relatively accurate and cost-effective model. The domestic Qwen series doesn't fully support Function Calling, and Cline doesn't support them either, so I can't test them for now.

## Tackling the Tricky Problems of AI Coding

I recently read the article [AI Blindspots](https://ezyang.github.io/ai-blindspots/). The author systematically catalogs the problems encountered in AI programming and shares his thinking. It was very inspiring to me. I used an Agent to translate it into Chinese and then polished it by hand—you can read it here: [AI Programming Blindspots](https://sund.notion.site/AI-1be8ce9d275d80649a29e541d310d5c5).

In summary, the three key points to solving AI problems are still: more accurate prompts, more complete context, and a smaller problem scope.

I believe that as technology evolves, programming paradigms will undergo earth-shaking changes. If refactoring becomes this easy, should Martin Fowler's *Refactoring* get a new edition for the AI era? If documentation is no longer read by people but fed to models as context, what should documentation look like? Will providing a vectorized documentation interface for large models to call become the new normal in future programming frameworks?

I look forward to the future.
