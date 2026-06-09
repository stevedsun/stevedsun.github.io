---
title: "Pairing with AI for Programming — Testing"
slug: "pairing-with-ai-01"
date: 2024-12-11T17:02:43+08:00
categories: [Software Architecture]
tags: [ai, unit-test]
aliases: [/posts/pairing-with-ai-01/]
description: ""
---

The future paradigm of software development will be human-AI collaborative programming. This is already an indisputable fact in the software industry. Programming tools like Windsurf, Cursor, and Copilot have, on one hand, improved development efficiency; on the other hand, they've made code more black-boxed, less readable, and harder to maintain.

I try to briefly discuss which software development practices are more suitable for improving the observability and maintainability of AI-generated code in the AI era. All articles titled "Pairing with AI for Programming" are just thoughts to get the conversation started, not a systematic methodology. I welcome readers' corrections for any mistakes.

## What Are the Common Problems with Using AI to Write Code?

**Observability problem: AI's implementation is incomplete and often requires manual modification of fragments**

The biggest problem with AI-generated code is that it often introduces subtle errors that are not easily noticed by humans. When humans use prompts to modify code, due to the difficulty of observing AI's behavior, even after fixing a bug, it may lead to other regression issues (causing errors in existing logic).

**Context problem: lacking global context, fragmented code lacks connections**

Due to token limits or economic considerations, many editors will optimize the input content, which can easily lead large models to misunderstand local context. They are unable to handle business logic across functional modules. Especially when the project becomes large, complex modules often depend on other modules, and adjusting business logic requires refactoring several code files.

## Solution Approach

The core problems of AI-written code can be summarized as low maintainability caused by lack of observability and lack of context. To address these two problems, we need to first review how traditional software processes make code more observable and maintainable.

### Human-Led Unit Testing

Unit tests are the specification for code. Complex business logic usually requires reading a lot of code to understand. But experienced programmers will look at the unit tests first. Good unit tests will completely write the module's expected inputs and outputs into the test cases. In [Unit Testing Principles, Practices, and Patterns](https://www.amazon.com/Unit-Testing-Principles-Practices-Patterns/dp/1617296279), the author believes good unit tests should have:

- **Protection against regressions**. That is, tests can prevent previously fixed issues from recurring in regression testing.
- **Resistance to refactoring**. That is, after code refactoring, tests can correctly identify whether the refactoring has affected existing functionality.
- **Fast feedback**. That is, unit tests are easy to run, and when issues are found, they can be quickly located.
- **Easy to maintain**. The maintainability of tests, unlike business code, is reflected in correctly handling dependencies and shared code.

The ultimate purpose of these principles is to ensure that the system under test behaves as expected.

When AI and humans collaborate on code, I personally believe that in writing unit tests, humans should lead (80%) and AI assist (20%), because unit tests define "the behavior I expect."

Once unit tests are complete, they in turn guide the AI to implement the actual business code. At this point, human involvement decreases and AI takes the lead. Humans repeatedly run unit tests, while passing the test results along with the prompt to the AI, helping AI fix program issues.

### Writing AI-Friendly Tests Requires Good Module Design

When writing good tests, you also need to pay attention to correctly splitting modules. A good test typically gives an input and verifies whether the expected result is output. If a module depends on too many external environments for branching logic, the test output will heavily depend on external state. This reduces the module's observability.

The following two pieces of experience can help you write good code:

1. When writing tests, test the result of the behavior, not the steps. When writing business code, ask AI to clearly write out the steps.

   The "unit" of a unit test doesn't have to be a single class or function. It can be a group of operations completing an atomic piece of business logic. (Of course, there are different schools of thought supporting class-level testing, but that's not the focus of this article.) To make AI-generated business code refactor-resistant, you should verify the result of the AI's behavior, not every implementation step. Coupling test code with implementation steps means that business modifications will break existing tests, making the "expected behavior" constantly have to be modified along with the "specific implementation."

   When AI starts writing business logic, you should drive it step by step, during which humans can correct the AI's code logic for a particular step. But be careful not to break the test logic.

2. Stateless code (functional) is the easiest to test

   Because its output is invariant. Core code should be kept as stateless as possible, with state and external system dependencies placed in the application service layer. Deep and hard-to-understand core logic should be placed in the domain service layer. The details here can refer to DDD (Domain Driven Design) thinking.

   ![functional_core.png](/images/pairing-with-ai-01/functional_core.png)

## Summary

This article, as the beginning of a series on human-AI collaborative programming, attempts from a testing perspective to alleviate the observability issues of AI-generated code.

In future articles, I hope to discuss, from an architectural design perspective, how to design AI-friendly architectures that are easy to maintain context for.

The content of the article will continue to be updated over time, and discussion is welcome.
