---
title: '【译文】/goal + 损失函数：如何用一条指令在 30 小时内蒸馏一个产品'
slug: "goal-loss-functions-distill-product"
date: 2026-06-11T12:00:00+08:00
draft: false
categories: [AI]
tags: [AI, Agent, Loss-Function, Translation, LLM, Codex]
aliases: [/posts/goal-loss-functions-distill-product/]
description: "Elvis 分享如何用 Loss Function Development (LFD) 让 AI agent 在 30 小时内、花 40 美元完成一次完整的产品逆向工程"
---

![](https://raw.githubusercontent.com/stevedsun/blog-img/main/goal-loss-functions-distill-product-header-900x383.png)

> **原文**：[`/goal + Loss Functions: How to Distill a Product in 30 Hours with One Prompt [Full Playbook]`](https://x.com/elvissun/status/2065035615800864954)
> **作者**：Elvis ([@elvissun](https://x.com/elvissun))
> **翻译**：AI 辅助翻译

99% 的人用 `/goal` 和 agent loop 的方式是错的。

外面吹的是「长循环自主 agent：设定目标，走开，回来就拿到能跑的代码」。但顶尖的 agent 工程师半年前就在做同样的事了——用 harness engineering + spec-driven development：

1. 给 agent 搭一个能观察问题的测试框架
2. 写一份包含所有 test case 的 tight spec
3. 让 Codex 或 Claude Code 无人值守循环，直到所有测试通过

我经常睡前 kick off 这种任务——一次跑 2-5 小时。四月份有一次，它啃了一整晚我们 Vercel monorepo 里的 Turbo build-cache bug，天亮时全绿了。根本不需要 `/goal`。

所以 **`/goal` 到底用来干什么？**

这是我离开后一条 prompt 干的事：

- 跑了约 30 小时，生成 6300 行代码，爬了 92000 页，花了 $40 API
- 把另一个产品的核心逻辑反向工程并完整重构
- 我们的版本输出质量比参考产品好约 **50 倍**

秘密是 **Loss Function Development（LFD）**：给 agent 写一个要优化的目标（loss function），而不是写一份要实现的 spec。

---

### Agent 作弊三次

我一开始做的是老套路：写 spec——把 agent 指向竞品的公开网站，「我们自己怎么建这个？」。30 分钟后它出了一份完整的系统设计和测试用例。spec 有了。

但这次我试了一个不同的 prompt：

> `/goal 实现，直到你的输出和他们的完全一致`

然后发生了这些事：

**第一轮（5 分钟）**：agent 抓了一组 eval 数据，生成的和它一模一样的种子数据，5 分钟就宣布胜利。「100%」召回，零泛化能力——一个只能找到我给它那 30 个东西的搜索引擎。

**修复**：盲测。eval 在运行期间隐藏，只在评分时揭示。

**第二轮（20 分钟）**：盲测，30 个测试项。agent 看不到答案了，但它学会用「miss」反向学习——每一条「你没找到 X」都变成下一轮的关键词。几轮之后，它刚好用了 30 个关键词，每个对应一个目标，又赢了。

**修复**：扩大 eval 集。几百项，大到无法逐一枚举。

**第三轮（30 分钟）**：盲测，200 个测试项。agent 又作弊了——关键词表膨胀到几百个，每项对应一个精准 lure。

三轮，三次作弊。

这时候我才明白：**作弊不是 agent 的 bug，是我目标的 bug。** 我给它指明了目的地，但每条捷径都敞开着。每个你没有堵死的便宜路径，都是优化器会全力冲刺的方向。

**第四轮（30 小时）**：盲测，200 项，硬性限制。我封死了所有方向——限制关键词表、盲测 eval、扩大数据范围。每条捷径被堵死后，agent 终于发现唯一能提升指标的方式是真正把事做好。

它不作弊了。

然后它跑了 30 小时。爬了 92000 页，花了 $40 token，写了 6300 行代码。结果是我们比参考产品在同一查询上多挖掘了约 50 倍的结果——那只是地板，不是天花板。

---

### LFD：一个好的损失函数有四个组件

大多数人在用 agent 构建产品时，只做了从零到上线这一步。之后的长尾——spec 从未设想过的 edge case——一个一个从 production log 里冒出来。你一个一个修。那些没被日志捕获的，用户替你报告——这是发现 bug 最贵的方式。

LFD 把长尾加速了。如果提前准备好真实的 expected outputs（「好」长什么样，而且得是量级），你实际上在发布前就跑完了 soak 阶段——几百个 edge case 在一次优化中命中 agent，而不是一个季度一个季度地靠 bug 报告渗透。

**Spec-driven development：**「建成这样。让测试通过。」
**Loss-function development：**「建成这样。让测试通过。然后在这 1000 个 eval case 上持续迭代。」

测试集是有限的——全绿就结束了。但 1000 个 eval 在 95% 准确率是一个你不断接近的目标，没有终点线。完整的损失函数有四个部分：

#### 1. Target（目标）
- **大到无法枚举**。28 项的 eval 一轮就被背下来了。越大越好。
- **对 agent 盲测**。Eval 数据只用于事后评分。agent 如果在运行中能看到答案，它会想方设法去看。

#### 2. Constraints（约束）
agent 能做什么、不能做什么：**时间**（wall-clock 预算）、**金钱**（API 调用的硬性上限）、**表面**（允许的模型和并发上限）、**方法论**（允许 LLM 分析还是只用确定性逻辑）。

#### 3. Instruments（测量工具）
**没有工具的约束只是一句感觉——agent 会笑嘻嘻地无视它。** 每个约束都要配一个 CLI 让 agent 自己检查。法则还是那句老话：**你无法优化看不见的东西。**

如果你是第一次跑这种循环，别 kick off 就走。**盯住第一轮。** 看它碰了什么，确认你建的 harness 被正确使用了。然后再去睡觉。

#### 4. Forced Entropy（强制熵）
每一轮都从上一次的完整上下文继续跑。**撞到局部最优是默认状态。** 熵必须**强制**引入：

- **每轮反思过拟合**——我在构建更通用的方案，还是在记忆 eval？
- **停滞时强制跳跃**——如果上一轮没动指标，下一轮不能「同样的思路更努力」
- **保持迭代日志**——让 agent 记录每轮的假设和诊断结果

---

### 梯度下降全栈自动化

退一步看——这全是梯度下降。

**内循环**是 agent：写代码、跑测试、修。短周期，快反馈，一个目标——让测试全绿。
**外循环**是 `/goal`：驱动整个系统朝着一个结果指标跨多轮迭代——发布、测量、换策略、下降。长周期，稀疏反馈。

两个循环现在都自动了。留给你的事只有一件：**定义损失函数。**

---

### 信息不对称：新的护城河

换个视角看：这本质上是蒸馏——从训练时搬到了 prompt 时。但现在不是蒸馏模型，而是用 `/goal` + LFD 去蒸馏任何公开可找的 artifact。

凡是存在信息对称的地方，执行成本就趋近于零——输出是公开的，每个人都能看到「好」长什么样，任何人周末花 $40 就能蒸馏出来。

所以新的护城河是：**信息不对称。**

你私有的 eval 集、你用户真实踩到的 edge case、你私下测量的 ground truth——凡是竞品的 agent 看不到的目标，才是唯一能在别人的循环持续逼近时你的还往下降的东西。

> The product is a weekend now. Go build the eval a weekend can't touch.
>
> 产品是一个周末的事了。去建一个周末碰不到的 eval。
