---
title: "AI Agent Tool Comparison: Why MCP Is Just a Transitional Solution"
slug: "ai-agent-tool-comparison-mcp-transitional"
date: 2026-04-20T12:37:00+08:00
categories: [AI]
tags: [AI Agent, MCP, Skill, Tool Calling]
aliases: [/posts/ai-agent-tool-comparison-mcp-transitional/]
description: "Why MCP's protocol layer can't carry the semantics AI agents need, and how Agent Skills offer a more natural way to package capabilities."
---

![](https://raw.githubusercontent.com/stevedsun/blog-img/main/ai-agent-mcp-header-900x383.png)

If you've built AI Agents, you've likely used MCP and may have come across the concept of Agent Skills. We don't need to re-explain what they are—the question this post answers is: **when both can achieve "letting AI call tools," why I think MCP is a transitional approach that will be phased out**.

---

## The Fundamental Limitation of MCP: The Protocol Layer Can't Carry Semantics

MCP's design logic is: give AI a structured tool-calling protocol where tool discovery, invocation, and parsing all follow a fixed format.

The problem is that **this protocol is designed for humans, not for AI**.

JSON Schema can define parameter types and return value structures, but it cannot convey things like: why this parameter usually takes this value, what prerequisites a tool needs to work, or what its failure modes look like. This context is what AI most needs when making decisions in real scenarios, but the MCP protocol layer simply cannot carry it.

The result: tool-calling capabilities built with MCP depend heavily on prompt engineering—you need to supplement in the prompt what the protocol definition doesn't include. This shows the protocol layer has a gap, and that gap can't be fixed by improving the schema, because it's fundamentally a semantic-loss problem, not a format problem.

Another practical issue is maintenance cost. Every new capability requires a separate MCP server—you need to maintain server code, schema definitions, and network connections. When the protocol version updates, all servers may need to change too. For individual developers or small teams, this complexity is a significant burden.

---

## Why Skill Is Closer to What AI Actually Needs

Agent Skill uses Markdown as the core format for capability packaging—using human language to describe what a capability is, when to use it, and how to use it, with scripts and reference templates attached.

When AI reads a Skill document, it gets more than "this tool's name and accepted parameters"—it gets the full decision context: when to use it, when not to, how to handle edge cases. This information was always meant for human developers; now it goes directly to AI without secondary translation.

**For engineers**, using the file system as the foundation for Skill management brings an extra benefit: this workflow aligns perfectly with an engineer's daily work. Git manages the Skill directory, naturally supporting version control, branching, and PR reviews. AI reads whatever documentation it needs, with no need to understand any protocol layer or maintain a running server process.

**For ordinary users**, the advantage of Skill is even more direct. Today's Agents are getting more complete, and "harness engineering" has emerged—users don't need to understand technical details, just describe what capabilities they need. Installing a Skill might be a one-liner: AI automatically reads the Skill document, understands what the capability does and how to configure it, then automatically handles dependency installation, API configuration, and permission verification—tasks that previously required a technical person. For users, a Skill is a manual for a capability, and the Agent is the executor who reads the manual and gets it done. MCP can't do this because it requires users to first understand servers, schemas, and protocol versions—these are engineer language, not user language.

Skill's semantic packaging makes this "zero-barrier installation" possible. When capabilities are described in human-language documents, the Agent can truly make those technical decisions on the user's behalf. The thicker the protocol layer, the higher this delegation cost—and Skill compresses this layer to the minimum.

|              | MCP                          | Agent Skill              |
| ------------ | ---------------------------- | ------------------------ |
| Adding a new tool | Write server + schema + config | Write a Markdown file    |
| Semantic expressiveness | Limited by JSON Schema  | Free-form Markdown       |
| Context information | Needs prompt engineering supplement | Written in the doc, read directly by AI |
| Protocol version maintenance | Required          | Not required             |
| Installation for ordinary users | Need to understand server and protocol concepts | Agent reads doc, auto-configures |
| Caller configuration | Need to configure server connection | Read files directly      |

---

## MCP's Cloud Advantage Is a False Premise

One often-cited advantage of MCP is cloud deployment—the server runs independently and multiple Agents can share it.

This advantage is real, but it belongs to the "network call" capability category, not to the MCP protocol itself. Agent Skill can be built entirely on REST API calls, and scripts in Skill documents can call any HTTP endpoint. On cloud deployment, Skill doesn't fall short.

For SaaS services that already have REST APIs, the comparison becomes even clearer:

- With MCP: write a server that wraps the REST API, maintain the schema, keep in sync with MCP protocol versions
- With Skill: write a Markdown document that clearly describes what the API does and how to call it, and AI reads it and uses it directly

**MCP requires you to maintain an extra protocol system and server process, while Skill covers all these needs at lower cost.** When a simpler solution can do all the same things, the complex one should step aside.

---

## Skill's Form Is Also Evolving

But I have to admit that Markdown + file system may not be the end state either.

This approach has an unsolved problem: **the dynamism of Skill**. When a Skill's external API dependencies change, or when it needs real-time state, how do static documents in the file system keep up? The current solution is to rely on scripts and templates, but the script execution environment, security boundaries, and state management all lack standard answers.

Additionally, dependency relationships between Skills, priority ordering, and decision logic when multiple Skills apply to one request are all open questions.

My judgment: **Skill will evolve, possibly no longer centered on static files in the file system**, with some more dynamic mechanism for capability registration and discovery emerging. But that mechanism will most likely be a continuation of the Skill design philosophy, not a return to MCP's protocol design direction.

---

## Closing Thoughts

MCP isn't a bad design. It took an important first step in AI tool calling, turning "AI connecting to the external world" from impossible to possible.

But there's still distance between "possible" and "right." When we discover a way to package capabilities that better fits how AI thinks, the transitional approach should exit the stage.

Is Agent Skill the final answer? I'm not sure. But it's closer to what AI truly needs—semantics, context, flexibility, and a calling experience with no extra protocol layer. This packaging is friendly to engineers and even more friendly to ordinary users, because it hides technical complexity inside the document layer, letting the Agent handle things users shouldn't have to think about.

This direction of exploration deserves to be taken seriously.

Finally, here's my 2025 dissection (roast) of the MCP concept.

![](/images/ai-agent-tool-comparison-mcp-transitonal/x-mcp-thread.jpg)
