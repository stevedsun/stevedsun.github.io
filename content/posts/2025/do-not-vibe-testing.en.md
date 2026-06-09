---
title: "Why You Shouldn't Let AI Generate Your Unit Tests"
slug: "do-not-vibe-testing"
date: 2025-05-01T09:27:36+08:00
categories: [AI]
tags: [vibe coding, testing]
aliases: [/posts/do-not-vibe-testing/]
description: "Auto-generating unit tests with AI raises coverage without raising quality, and risks replacing the human thinking that makes tests valuable in the first place."
---

Recently I heard Hailong Zhang, founder of Gru.ai, mention in a [podcast](https://www.xiaoyuzhoufm.com/episode/671c9a42eb46cd6655da1e6f?s=eyJ1IjogIjVlN2M2M2UzYjNjNWJjYTVmNjQxMTJkNCJ9) that automatically generating unit tests is the main direction they are pursuing in AI coding.

Gru.ai's website has these two lines:

> Forget about unit testing – get covered automatically
> Harness the expertise of AI engineers to boost your team's testing efficiency while reducing costs and ensuring top-notch quality.

Zhang's insights on AI coding are inspiring. I am skeptical, though, of the claim that using AI to write tests cuts cost and boosts efficiency. I think they themselves weren't fully confident when writing the second line — they couldn't help tacking on "ensuring top-notch quality" for reassurance.

Unit tests are the concretization of requirements. They are the smallest-grained, closest-to-the-code constraint tool in the entire testing system. Unit tests are used not only to check whether code meets requirements, but more often to detect corner cases — because what makes a program reliable is that it doesn't break at the boundaries. That is also what distinguishes an experienced engineer from a junior one.

But what Gru.ai is doing is using **AI to raise unit test coverage**. As we all know, higher coverage does not equal higher testing efficiency, let alone higher quality.

Letting AI automatically write runnable unit tests from a single prompt is very tempting for junior developers. It's like a shooter trying to improve their accuracy by firing the gun first and then drawing the bullseye around the bullet hole.

The purpose of improving test coverage is to push human engineers to think carefully about edge cases. Using AI to help humans generate tests as a time-saver is perfectly fine, and Gru.ai instead tells us to "forget about unit testing, get covered automatically." But the AI usually doesn't know the edge cases unless a human explicitly tells it. So how does the AI infer the edge cases on its own? And how do we know the AI's inferred edge cases are correct? If the AI tests the code, who tests the AI?

If products like Cursor embody the Silicon Valley imagination of vibe coding, then Gru.ai embodies the Chinese programmers' "rosy expectations" of vibe testing.
