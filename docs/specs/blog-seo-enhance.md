# Tech Spec: Blog SEO & UX Enhancement

## 项目概览
Hugo v0.150.1 静态博客，模块化主题 `github.com/rokcso/hugo-bearblog-neo`，项目源码在 `/home/sundi/code/github/stevedsun.github.io/`。

## 改动文件清单

### 1. 每篇文章独立的 OG Image
**改动文件：** `layouts/partials/custom_head.html`
**实现方案：**
- 在 `<head>` 的 OG/Twitter 标签输出之前，检查页面类型：
  - 如果是单篇文章（.IsPage 且 .Section 为 "posts"）：
    - 从 .Content 中提取第一张 Markdown 图片 URL
    - 将提取到的图片 URL 注入到 Hugo 内置的 opengraph/twitter_cards 模板上下文
    - 若文章无图片，回退到默认图片
- 覆盖 Hugo 内置 `_internal/opengraph.html` 的行为：
  - 在调用 `{{ template "_internal/opengraph.html" . }}` 之前，设置 `.Params.images` 为文章首图
  - 或者在 `custom_head.html` 中自定义输出 OG/Twitter 标签，跳过内置模板

**推荐方案：** 自定义 OG/Twitter 标签输出（因为内置模板不支持动态注入 images），在 `custom_head.html` 中：
1. 写一个 partial 函数提取文章第一张图片
2. 手动拼接 `og:image` 和 `twitter:image` 标签
3. 非文章页面仍然使用 `_internal` 模板

### 2. 首页展示最近文章列表
**改动文件：** `layouts/index.html`（新建）
**实现方案：**
- 新建 `layouts/index.html` 覆盖主题默认首页模板
- 先渲染 `{{ .Content }}`（保留现有 `content/_index.md` 内容）
- 然后添加 `{{ range first 5 (where .Site.RegularPages "Section" "posts") }}` 输出最近 5 篇文章
- 每项显示：日期（YYYY-MM-DD 格式）+ 标题链接
- 格式：无序列表，与现有 /posts/ 风格一致

### 3. JSON-LD 结构化数据
**改动文件：** `layouts/partials/custom_head.html`
**实现方案：**
- 在 `custom_head.html` 中新增 JSON-LD 输出块
- 仅对 .IsPage 类型文章输出
- Schema 类型为 `Article`（或 `BlogPosting`）
- 字段：`headline`（title），`datePublished`，`dateModified`，`author.name`，`description`，`image`（取首图），`publisher`，`mainEntityOfPage`
- 使用 `jsonify` 函数确保合法 JSON 输出
- 包裹在 `<script type="application/ld+json">` 标签内

### 4. 文章底部相关推荐
**改动文件：** `layouts/_default/single.html`
**实现方案：**
- 在文章主体内容后面、评论区域之前，新增相关文章区域
- 使用 Hugo 内置 `.Related` 函数按 tags 匹配
- 限制最多 3 条
- 若无相关文章（`len .Related` 为 0），不渲染该区域
- 标题为 h2 "相关文章"，下方无序列表
- 每项只显示标题链接

### 辅助配置
**改动文件：** `hugo.toml`
- 新增 `[related]` 配置区块：
  ```toml
  [related]
  threshold = 80
  includeNewer = true
  [[related.indices]]
  name = "tags"
  weight = 100
  ```
- 为首页最近文章功能确认 Hugo 版本支持（已满足 v0.150.1）

## 不变的风险
- 主题是 Hugo Module 而非 themes/ 目录，自定义模板通过 `layouts/` 覆盖机制生效
- 当前 `custom_head.html` 同时用了 `_internal/opengraph.html` 和 `_internal/twitter_cards.html`，实现自定义 OG 后需移除对内置模板的调用来避免冗余输出
- `images/share.png` 文件不存在，需先创建一张默认 fallback 图片（纯色背景 + 博客名），或使用 CSS 背景色替代

## 验证方式
1. 本地 `hugo server` 启动，检查每篇文章 HTML 中 og:image 是否为文章首图 URL
2. 首页 `/` 显示最近 5 条文章
3. 每篇文章 HTML 中包含 `<script type="application/ld+json">` 块
4. 有标签的文章底部显示相关文章链接，无则隐藏
5. `npm run build` 无报错
