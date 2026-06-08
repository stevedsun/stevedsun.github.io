# Blog Site Optimization V1

## 需求描述

对 stevedsun.github.io（Hugo Bear Blog Neo 主题博客）进行 6 项优化：性能、SEO、PWA 配置、GA 迁移、代码组织、死代码清理。

## 已有上下文

Hugo 静态站，使用 `hugo-bearblog-neo` 主题（Go module，无 themes/ 目录）。
自定义覆盖文件：
- `layouts/partials/custom_head.html` — 包含全部 CSS（Chroma 语法高亮）+ KaTeX + Mermaid + GA4
- `layouts/_default/single.html` — 文章模板，含 Giscus 评论、upvote（已关闭）、TOC
- `hugo.toml` — 站点配置
- `static/site.webmanifest` — PWA manifest（name 为空）
- 缺失 `static/android-chrome-192x192.png` 和 `static/android-chrome-512x512.png`

## 验收条件（AC）

### AC-1: 性能 — 第三方 JS 按需加载
- [ ] KaTeX CSS+JS 仅在文章包含 `$$` 或 `$` 数学公式时加载（不全局加载）
- [ ] Mermaid JS 仅在文章包含 mermaid 代码块时加载（不全局加载）
- [ ] GA4 脚本保持全局加载（统计需要全局）

### AC-2: SEO — 完善元数据
- [ ] 首页 `<head>` 含完整的 Open Graph 标签（og:title, og:description, og:image, og:url, og:type）
- [ ] 文章页含 Twitter Card 标签（twitter:card, twitter:title, twitter:description, twitter:image）
- [ ] 每篇文章的 description 自动使用 frontmatter 中的 description 字段

### AC-3: PWA — 修复 site.webmanifest
- [ ] `site.webmanifest` name 和 short_name 设置为 "Steve Sun"
- [ ] Android Chrome 图标路径指向 `android-chrome-192x192.png` 和 `android-chrome-512x512.png`

### AC-4: GA4 — 使用 Hugo 内置配置
- [ ] 移除 `layouts/_internal/google_analytics_async.html` 文件
- [ ] `hugo.toml` 使用 Hugo 内置 `googleAnalytics = "G-XJJVVQ0LBH"` 配置项（而非 custom_head 手动引用）

### AC-5: 代码组织 — 拆分 custom_head.html
- [ ] Chroma 语法高亮 CSS 移到单独文件 `layouts/partials/chroma-styles.html`
- [ ] KaTeX + Mermaid 按需加载逻辑移到 `layouts/partials/third-party-scripts.html`
- [ ] 原有 `custom_head.html` 只做 import 和 GA4 条件加载

### AC-6: 清理 — 移除关闭的 upvote 死代码
- [ ] `layouts/_default/single.html` 中 `upvote = false` 时的整段 upvote HTML+JS 代码移除
- [ ] 保留 upvote 配置项但标记为废弃

### 全局 AC
- [ ] `hugo server` 构建成功，无报错
- [ ] 首页和文章页渲染正常
- [ ] Giscus 评论正常加载
- [ ] 自定义字体族正常应用
- [ ] Chroma 语法高亮（浅色/暗色）正常
