---
title: "How I Use Hermes Agent to Write Code"
date: 2026-06-07T10:00:00+08:00
draft: false
slug: "how-i-use-hermes-agent"
categories: [AI, Engineering]
tags: [AI, Hermes Agent, Codex CLI, AI Agent, Engineering Management, Software Development]
description: "I run two Hermes Agents in parallel—one writes code, one acts as PO. The core discipline: Hermes never writes code. Three-layer gate defense, dual-track workflow, tunnel reuse—a methodology grown from hard-won experience."
---

![](https://raw.githubusercontent.com/stevedsun/blog-img/main/how-i-use-hermes-agent-header-900x383.png)

I run two Hermes Agents in parallel.

One is called Super Juaner and handles daily conversation and information retrieval. The other is called Code Juaner and works exclusively on software engineering. Two independent Telegram bots, independent configurations, independent session databases.

Running two Agents separately is for context and environment isolation.

**Core discipline: Code Juaner never writes code.**

All coding is delegated to Codex CLI for execution. Code Juaner only does the Product Owner work: writing requirement definitions, making architecture decisions, and accepting deliverables. Codex is the implementer: reads the spec, writes code, runs tests.

| Role | Output | Responsibility |
|------|------|------|
| Code Juaner (Hermes PO) | Feature doc + acceptance | Requirement definition, architecture decisions, quality control |
| Codex CLI (Implementer) | Code + tests | Technical solution, coding implementation, self-testing |

The flow is simple. The user says "I need a feature." Code Juaner writes a feature doc containing only the requirement description and verifiable acceptance criteria. Every acceptance criterion must be verifiable—"clicking changes the URL to /zh/monaco" rather than "navigation is correct." Then Codex reads the doc, plan mode produces a technical spec, and build mode implements plus tests. Code Juaner accepts each criterion one by one; if all pass, deploy; if there are issues, summarize and send back.

Code Juaner never reads code files, never finishes reading code to tell Codex how to write. For project-level questions, delegate to Codex plan mode for investigation. Codex timeout means reporting back directly and waiting for next instructions.

The acceptance standard is that `npm run build` passing is only the minimum bar. For behavior changes, walk through the full user path in the browser before marking complete.

## The Three-Layer Gate

Discipline sounds simple but is easy to forget in practice. The model drifts in long conversations—after thirty turns, it may think it can write code and start modifying files directly. I built three layers of defense.

**Layer 1: System prompt (hardest, unbypassable)**

Locked in `config.yaml`: all coding must be delegated to Codex CLI for execution, never write code yourself, report and wait after Codex fails. Injected every turn, can't be avoided.

The system prompt's lifecycle in Hermes is longer than SOUL.md; it doesn't reset between conversations, so it better prevents forgetting after long conversations. Even if the model starts drifting after dozens of turns, this terminal instruction is still there.

**Layer 2: SOUL.md + personality (loaded at session start)**

SOUL.md defines personality and creed: terse, conclusion-first, type-safety > runtime correctness > performance optimization. But its effective range is the start of each conversation, weaker than the system prompt.

SOUL loads a `development-workflow` skill I co-developed with Super Juaner, which defines pre-checks when picking up code: must load the workflow skill first before making decisions, don't skip. This file hosts my entire coding discipline as an initial activation guide.

**Layer 3: Plugin gate (physical interception, unbypassable)**

Two plugins intercept Code Juaner's source code read/write. `write-code-gate` blocks `write_file` and `patch` on source files like `.ts`, `.tsx`, `.py` and returns refusal. `read-code-gate` blocks `read_file` and `search_files` on source files. Non-source files like `.md`, `.yaml`, `.toml` pass through.

The blocked extensions cover 30+ common languages. Exempt paths include `.hermes/`, `node_modules/`, `.next/` and other non-project directories.

Plugins are loaded via Hermes's `pre_tool_call` hook, take effect at session start, and remain available after gateway restarts.

The three layers increase in hardness from outside to inside; when rules conflict, the hardest layer wins. The system prompt is a sticky note; the plugin is a locked door.

These practices aren't new. Most of them are decades of accumulated software engineering—separation of roles, clear responsibilities, acceptance-first—just wearing a new skin in the AI era and landing in a new way.

## Dual-Track Workflow

Take different tracks based on task nature.

**Track A: New project or feature from zero to one**

Full pipeline: Feature Doc → Plan → Build → Verify → Fix (loop).

Phase one: Code Juaner writes the feature doc. Phase two: Codex plan produces the technical spec, including file list, implementation plan, data structures, and test cases. Phase three: Codex build reads the spec, implements all files, runs tests. Phase four: Code Juaner accepts each criterion.

Acceptance walks through five layers: data layer (type definitions, state management), logic layer (hooks, reducers), presentation layer (component rendering, interaction binding), config layer (static config, data loading), browser verification (route checks, localStorage confirmation, screenshot comparison).

**Track B: Bug fixes or feature modifications**

Most projects go through Track B. Skipping the feature doc only applies to single-file, pure styling, copy changes, or minor config tweaks. Multi-file changes, those involving data persistence, state machines, or new components must write a feature doc plus spec before dispatching Codex.

When delegating to Codex, give only the goal and acceptance criteria, not the implementation plan. Codex reads the code and designs by itself.

## Preview Tunnel

In-progress websites need to be previewed on mobile. I use Cloudflare Tunnel to expose the local Next.js dev server to the public internet; Cloudflare assigns a temporary `trycloudflare.com` domain, open it in a mobile browser to preview.

Early on I stopped and restarted the tunnel after every change, which triggered Cloudflare rate limits. Each stop and restart assigned a new URL, requiring me to reopen it on the phone—annoying.

Later I wrote a `tunnel-manager.sh` script. The first start runs `cloudflared` as a background daemon; subsequent builds only restart the next server, not touching the tunnel. The tunnel daemon is reused across preview sessions; it only rebuilds on machine restart or `cloudflared` crash. The same URL persists through the entire development cycle, eliminating a lot of repetitive operations.

## Git plus Vercel Deployment

Hit one silent pitfall: Vercel's GitHub integration checks whether the commit author email is a real GitHub account email. When it doesn't match, the CLI reports "Your deployment failed" and `vercel inspect` shows `Builds: [0ms]`—the build never started, no logs at all.

Fix: use the system git identity for commit, and rebase to reset the author if there's a mismatch.

Deployment uses Vercel CLI with `--no-wait` to avoid timeout blocking. GitHub Actions' `deploy.yml` triggers automatically on push to the `main` branch.

## Some Reflections

After all those specific practices, let me share some thoughts.

AI writing code has developed too fast. At the start of the year I was still manually writing every line; by mid-year I already had a pipeline that can independently complete features, acceptance, and deployment. What I do has shifted from writing code to defining rules, setting boundaries, and accepting results.

The engineer's role is changing. You used to be a bricklayer, placing bricks one by one. Now you're a rancher: set up the fences, put out enough feed, and let the herd graze and grow. The software industry is shifting from construction to animal husbandry.

This trend will only accelerate. Better models mean simpler harnesses, cheaper execution costs. You don't need to be the best programmer—you need to be the best rule-maker. Define clearly what's allowed, what's not allowed, and what counts as done—leave the rest to the agent.

The time I spend defining boundaries has a much higher return than the time I spend on actual coding. That's the most surprising discovery.
