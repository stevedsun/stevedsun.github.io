---
name: create-article
description: 创建新文章或博客内容。支持从主题生成大纲、交互式引导写作、或基于用户想法扩展成完整文章。
---

## When to use

当用户需要创建一篇新文章时，可使用此技能。该技能通过多轮交互式提问，帮助用户确定文章主题、受众、语气和篇幅等要素，并生成结构化的大纲和开头段落。最终，用户可以选择将生成的内容写入指定的文件路径。

## How to use

遵循 `archetypes/default.md` 的 front matter。默认生成提案并展示 diff，用户确认后再写入文件（就地写入 content/posts/YYYY/slug.md）。

### hooks / flow
1. 前置：若未传主题，则多轮询问用户：主题、受众、语气、篇幅（由命令文件的前置 hooks 负责）。
2. 参考`<skill-dir>/references`获取文章示例，参考`<skill-dir>/style.md`的文章风格，根据用户需要模仿对应文章风格。
3. 进入计划模式，建立 ToDo 列表。
4. 基于主题拆分出结构化大纲，返回 3-5 小节要点。
5. 基于大纲生成三条标题建议、最终选定标题、2-3 个 tags、category（从 CATEGORIES.md 选择）、以及 2-3 句文章开头。输出可解析的 Markdown 或 JSON 以便后续处理。
   - 从仓库根读取 CATEGORIES.md 来选择 category 建议。
   - tags 自动抽取 2-3 个，可由用户手动增删。
6. 列出要写入的文件与变更（front matter + 内容）作为 dry-run 提案。
7. 后置：展示 diff，并提示用户执行 /ai-apply（或在交互中确认）将提案写入仓库。


## 实现注意事
- 写文件时默认使用 `content/posts/<YYYY>/<slug>.md` 结构；若 new.sh 存在，可调用 new.sh 创建文件然后编辑。
- 正文的内容只需生成各个章节标题和正文第一段开头。
- 写入与 commit：默认仅写入文件（经用户确认），不会自动 commit。用户可选择手动 commit 或使用 --auto-commit（需显式授权）。

## 交互示例
- 用户："写一篇文章，标题为：用 Claude Code 改造博客"
- 系统：多轮询问受众/语气/长度 → 生成markdown小标题大纲与开头一段 → 展示提案（front matter + 内容）→ 提示用户确认写入