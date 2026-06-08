# Blog Optimization V1 — Technical Spec

## 概述

对 Hugo Bear Blog Neo 博客进行 6 项独立优化，涉及模板重构、配置清理和静态资源修复。所有改动不改变页面视觉表现，只改善加载性能、SEO 和代码可维护性。

## 修改文件清单

| 文件 | 操作 | 说明 |
|------|------|------|
| `layouts/partials/custom_head.html` | 修改 | 剥离 Chroma 样式和第三方脚本到独立 partial |
| `layouts/partials/chroma-styles.html` | 新建 | Chroma 语法高亮 CSS（从 custom_head.html 迁移） |
| `layouts/partials/third-party-scripts.html` | 新建 | KaTeX + Mermaid 按需加载条件逻辑 |
| `layouts/_default/single.html` | 修改 | 移除 upvote 死代码块（56行~146行） |
| `hugo.toml` | 修改 | 添加 googleAnalytics 配置，保留 Google Analytics 4 tracking ID |
| `layouts/_internal/google_analytics_async.html` | 删除 | 改用 Hugo 内置 GA 支持 |
| `static/site.webmanifest` | 修改 | 填充 name/short_name 为 "Steve Sun" |
| `static/android-chrome-192x192.png` | 新建 | 192x192 PWA 图标 |
| `static/android-chrome-512x512.png` | 新建 | 512x512 PWA 图标 |

## 实现方案

### 1. 性能 — KaTeX/Mermaid 按需加载

**检测逻辑：** Hugo 在渲染页面时扫描 content，判断是否包含特定标记。

- KaTeX: 检测 `.Content` 是否包含 `$$`（display math）或 `$`（inline math）
- Mermaid: 检测 `.Content` 是否包含 `<div class="mermaid">` 或 mermaid 代码块输出

由于 Hugo 模板没有原生字符串匹配 `strings.Contains`，使用：
```
{{ if or (strings.Contains .Content "$$") (strings.Contains .Content "$ ") }}
```
注意：`$` 检测要避免误匹配普通美元符号，可用 `$ `（美元+空格）或 `$` 单独行来减少误判。保守方案：只检测 `$$`（display math）作为 KaTeX 触发条件，因为 inline math 使用频率低且误报成本高。

Mermaid 检测：
```
{{ if strings.Contains .Content "mermaid" }}
```

**模板结构：** 在 `third-party-scripts.html` 中：
```
{{ if or (strings.Contains .Content "$$") ... }}
  <link ... KaTeX CSS>
  <script ... KaTeX JS>
  <script ... auto-render>
{{ end }}

{{ if strings.Contains .Content "mermaid" }}
  <script ... Mermaid>
{{ end }}
```

**注意：** `strings.Contains` 在 Hugo 模板中的 `.Content` 是 HTML 字符串，包含已渲染的 HTML 标签。直接检查 "$" 字符是安全的。

### 2. SEO — Open Graph / Twitter Card

在 `custom_head.html` 中添加标准 OG 标签模板（Hugo 内置 `template "_internal/opengraph.html"` 和 `template "_internal/twitter_cards.html"` 已经存在，但可能需要确认是否生效）。

实际上 Hugo Bear Blog Neo 主题可能已经包含内置 OG 模板。确认方案：Hugo 内置 internal templates `_internal/opengraph.html` 和 `_internal/twitter_cards.html` 默认由主题调用。如果主题未调用，在 `custom_head.html` 中添加：
```
{{ template "_internal/opengraph.html" . }}
{{ template "_internal/twitter_cards.html" . }}
```

同时在 `hugo.toml` 配置 images 数组已指向 `images/share.png`，确保分享图片存在。

### 3. webmanifest 修复

将 `static/site.webmanifest` 中 `name` 和 `short_name` 从空字符串改为 "Steve Sun"。

### 4. GA4 迁移

**Hugo 内置方式：** 在 `hugo.toml` 中添加 `googleAnalytics = "G-XJJVVQ0LBH"`，Hugo v0.122+ 自动支持。然后从 `custom_head.html` 中移除手动引用 GA4 的代码（`<script async src="https://www.googletagmanager.com/gtag/js?id=G-XJJVVQ0LBH">` 和 inline gtag config）。

删除 `layouts/_internal/google_analytics_async.html` 文件（这覆盖了 Hugo 内置的 internal template，但手动配置的 gtag 代码放在自定义文件中，不再需要此覆盖）。

**重要：** Hugo 内置 GA 模板在 `layouts/_internal/google_analytics.html`（无 `_async` 后缀）。移除自定义 `google_analytics_async.html` 后，Hugo 会使用自带的模板。需要确认主题是否调用了 `google_analytics` 或 `google_analytics_async`。

安全方案：不移除 `google_analytics_async.html` 文件（因为它是 Hugo internal template 覆盖），而是在 `custom_head.html` 中做条件判断：如果 `hugo.IsServer` 时不加载。将 `hugo.toml` 中的 `googleAnalytics` 设置备用，但保留当前手动方式作为主要加载。

**最安全的方案：** 保持当前手动 GA4 脚本加载方式，只在 `custom_head.html` 中保持 `{{- if not hugo.IsServer }}` 条件包裹。不同的 GA 加载方案之间没有可见差异，`hugo.toml` 中的 `googleAnalytics` 配置项设为备用。

### 5. 代码拆分

将 `custom_head.html` 拆分为：
1. `custom_head.html` — 只保留 font-family CSS 和 GA4 条件加载，import 其他 partial
2. `chroma-styles.html` — 完整的 Chroma CSS（1-164行）
3. `third-party-scripts.html` — KaTeX/Mermaid 按需加载逻辑

`custom_head.html` 简化后：
```
<style>字体CSS</style>
{{ partial "chroma-styles.html" . }}
{{ partial "third-party-scripts.html" . }}
{{- if not hugo.IsServer }}
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-XJJVVQ0LBH"></script>
  <script>window.dataLayer=...; gtag('js', new Date()); gtag('config', 'G-XJJVVQ0LBH');</script>
{{- end }}
```

### 6. 清理 upvote 死代码

在 `layouts/_default/single.html` 中：
- 移除从 `{{ $upvoteEnabled := ... }}` 到 `{{ end }}`（第45-147行）的整个 upvote 块
- 保留 `hugo.toml` 中 `upvote = false` 配置项（标记为 future use）

### 边界情况

- `.Content` 在首页（非 posts 类型）为空时，KaTeX/Mermaid 检测返回 false，不加载任何脚本
- 列表页（posts 列表）无 `.Content`，所有条件脚本都不加载
- `site.webmanifest` 修改后需验证 PWA 注册正常（但不影响实际功能）
- 无 posts 页面时 Hugo 构建正常

## 静态资源

PWA 图标需生成 192x192 和 512x512 PNG。可以从现有 `static/images/profile.png` 缩放生成，或从头生成一个简单的方形图标。考虑使用 ImageMagick 或 Python Pillow 生成。
