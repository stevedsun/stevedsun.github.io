---
title: "AI Agent + Product Manager = QA Test Engineer"
slug: "ai-e2e-testing"
date: 2025-10-08T20:39:15+08:00
categories: [AI]
tags: [vibe coding, ai agent, testing]
aliases: [/posts/ai-e2e-testing/]
description: "Pairing an AI Agent with a product manager can replace a junior QA engineer for E2E UI testing — with far lower maintenance cost than hand-written test code."
---

In September, our company organized a discussion on applying AI in the workplace. I happened to be researching end-to-end testing at the time, so I tried OpenCode with Playwright, and the results were astonishingly good.

I chose OpenCode over other AI agent frameworks (such as Claude Code) because it can integrate with the company's enterprise GitHub Copilot account, which means we can use models like GPT-4 and Claude Sonnet without limits on the corporate intranet.

Playwright, built by Microsoft, is an automation testing framework that can drive browser APIs. Compared to Selenium, it is lighter, the community is more actively maintained, and it pairs better with large language models (there is an official MCP server). Playwright also bundles a webdriver, sparing a lot of environment configuration.

With OpenCode and the Playwright MCP server, and a few well-crafted prompt templates, you can run a complete set of web UI end-to-end test cases without writing a single line of test code. That would have been unthinkable in the past.

I have long believed that asking programmers to write E2E test code is laborious and more harmful than helpful. For edge cases and performance, unit tests and API tests cover more than 90% of the needs. The real value of E2E testing is in catching issues in UI interaction and integration. Using automated E2E test code to cover integration and UI scenarios carries an extremely high maintenance cost — every tiny UI tweak can break the test code — and statistically, more than half of the failing test cases in a test suite are not caused by functional defects at all, but by UI load latency, renamed frontend variables, slow test environments, and so on. For the real corner cases that threaten the integrated environment — for example, request retries caused by network interruptions, or out-of-range parameters from interface changes — writing E2E tests is less efficient than unit tests and API tests. For these reasons I have always encouraged the team to hire a full-time test engineer rather than reserving part of every sprint for developers to maintain E2E tests.

On the other hand, as a project lead, I care more about whether requirements are truly understood and delivered, and how to verify what the engineers actually built.

The arrival of AI agents has changed the agile workflow. With a combination like OpenCode + Playwright MCP server, the AI only needs to read user documentation to pick up the basics of UI operations. It can then open a browser, follow the natural-language description of a test case, and click through page elements step by step to complete an entire business flow. With a bit of guidance it can also produce the exact steps it took, the results, the issues it hit, and a complete test report. This is not far from hiring a junior QA engineer.

Because the maintenance cost drops dramatically (you only maintain a Markdown file describing the test cases), a lot of detailed UI test scenarios that were previously impractical can now be covered by an AI agent. Most importantly, this work does not depend on engineers at all — product managers, POs, or BAs can write test cases directly in natural language, closing the loop between writing user stories and verifying features, and removing the ambiguity that comes from requirements being relayed between business, engineering, and QA.

The [Toyota Production System](https://en.wikipedia.org/wiki/Toyota_Production_System) lists several sources of waste in production:

- Overproduction
- Waiting
- Unnecessary transport
- Over-processing
- Excess inventory
- Unnecessary motion
- Defects

AI agents address, to some extent, three of these wastes: "overproduction" (writing test code over and over), "waiting" (waiting from requirements to implementation to test cases before a feature can be verified), and "unnecessary transport" (business requirements being passed between different people).
