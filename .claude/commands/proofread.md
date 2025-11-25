# /proofread <path>

Description

对指定的 Hugo Markdown 文件（content/posts 下）执行格式与语言校对，生成问题清单与 patch。默认 dry-run：生成变更提案并展示 diff；用户确认后可就地覆盖原文件（或按 --backup 生成备份）。

用法示例

/proofread content/posts/2025/example.md [--backup]

可选参数：
- --backup    若提供，保留原文件为 <file>.ai-backup.md

流程（hooks / flow）

1. 前置：验证 path 存在且位于 content/posts/ 下。
2. EnterPlanMode：建立 ToDo 列表以追踪发现的问题与修复动作。
3. Explore（子代理）：快速扫描文件，定位可能的异常段落（例如：中英混排、异常标点、疑似错别字段）。
4. Task：对全文执行详尽校对，输出：问题清单（行号 + 类型）、每处的修复建议、以及可直接 apply 的 patch 或完整修复后的 Markdown。
5. TodoWrite：列出修改动作（dry-run），并将变更保存在 ToDo 中供预览。
6. 后置：展示 diff，询问用户是否 apply；若确认：就地覆盖原文件（并在需要时写入备份）。

实现注意事项

- 校对重点：中/英文间距、全半角标点、错别字、语法病句、Markdown 标题/列表/代码块格式、图片/链接路径有效性（可选）。
- 默认行为为 dry-run，用户需显式确认 apply。

交互示例（伪）：
- 用户：/proofread content/posts/2025/draft.md
- 系统：扫描并输出问题清单 + 预览修复 → 用户确认 apply → 系统就地覆盖文件并返回修改摘要

---

Notes: 本文件为命令实现草案，细化时在 hooks 中调用 Explore/Task/EnterPlanMode/TodoWrite。