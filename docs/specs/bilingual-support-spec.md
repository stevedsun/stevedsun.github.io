# 双语支持 — 技术方案

## 概述

利用 Hugo 内置多语言（i18n）模式，将 2023+ 的 32 篇文章双语化。中文（zh）保持默认语言无 URL 前缀，英文（en）使用 `/en/` 前缀。通过文件名后缀关联翻译对（`slug.md` = 中文，`slug.en.md` = 英文）。UI 文字通过 Hugo `i18n/` 翻译文件管理。

---

## 1. Hugo 配置变更

### hugo.toml 修改

```toml
# 替换单行 languageCode
languageCode = "zh-CN"

# 新增 languages 块
defaultContentLanguage = "zh"

[languages]
  [languages.zh]
    lang = "zh"
    languageName = "中文"
    weight = 1
    contentDir = "content"
    title = "Steve Sun"
    description = "Steve Sun 的博客"
    copyright = "版权所有 © 2013-2026, Steve Sun"

  [languages.en]
    lang = "en"
    languageName = "English"
    weight = 2
    contentDir = "content"
    title = "Steve Sun"
    description = "Steve Sun's Blog"
    copyright = "© 2013-2026, Steve Sun"
```

注意：
- `defaultContentLanguage = "zh"` — zh 为默认语言，URL 不加 `/zh/` 前缀
- `languageCode` 保持 `zh-CN`（用于 RSS `<language>` 标签）
- `weight` 控制语言顺序
- 两个语言的 `contentDir` 都指向 `content`（同一目录，通过文件名后缀区分）
- `disableKinds` 和 `permalinks` 保持不动，所有语言共享

---

## 2. i18n 翻译文件

新建 `i18n/zh.yaml` 和 `i18n/en.yaml`。

### i18n/zh.yaml

```yaml
home: "首页"
posts: "文章"
search_placeholder: "搜索..."
post_count: "共 %d 篇"
recent_posts: "最近文章"
subscribe_rss: "订阅 RSS"
or_email: "或 发送邮件"
contact_email: "通过 发送邮件 与我联系"
powered_by: "由 Hugo Bear Neo 驱动"
copyright: "版权所有 © 2013-2026, Steve Sun"
sitemap: "站点地图"
related_posts: "相关文章"
no_posts: "暂无文章"
clear_filter: "清除筛选"
filter: "筛选"
language_zh: "中文"
language_en: "English"
switch_language: "English"
giscus_lang: "zh-CN"
```

### i18n/en.yaml

```yaml
home: "Home"
posts: "Posts"
search_placeholder: "Search..."
post_count: "%d posts"
recent_posts: "Recent Posts"
subscribe_rss: "Subscribe RSS"
or_email: "or Send Email"
contact_email: "Send Email"
powered_by: "Powered by Hugo Bear Neo"
copyright: "© 2013-2026, Steve Sun"
sitemap: "Sitemap"
related_posts: "Related Posts"
no_posts: "No posts yet"
clear_filter: "Clear filter"
filter: "Filter"
language_zh: "中文"
language_en: "English"
switch_language: "中文"
giscus_lang: "en"
```

---

## 3. Layout 修改

### 3.1 新增: layouts/partials/language-switcher.html

文章页专用的语言切换器。放在标题和日期下方、正文上方。

```html
{{ if .IsTranslated }}
<div class="language-switcher" style="margin: 1em 0;">
  {{ range .Translations }}
  <a href="{{ .Permalink }}"
     class="lang-btn"
     hreflang="{{ .Language.Lang }}">
    {{ if eq .Language.Lang "zh" }}中文{{ else }}English{{ end }}
  </a>
  {{ end }}
</div>
{{ end }}
```

不在文章页（首页、列表页等）时，用全局切换导航。

### 3.2 修改: layouts/partials/nav.html

文字使用 `{{ i18n "home" }}` 和 `{{ i18n "posts" }}`，增加语言选择器。

```html
<a href="{{ "" | relURL }}">{{ i18n "home" }}</a>
{{ range .Site.Menus.main }}
<a href="{{ .URL }}">{{ .Name }}</a>
{{ end }}
{{ $postsPage := .Site.GetPage "/posts" }}
{{ if $postsPage }}
<a href="{{ "posts/" | relURL }}">{{ i18n "posts" }}</a>
{{ end }}
<span class="lang-nav">
  {{ range $.Site.Home.AllTranslations }}
    <a href="{{ .Permalink }}"
       class="lang-link{{ if eq .Language.Lang $.Language.Lang }} active{{ end }}"
       hreflang="{{ .Language.Lang }}">
      {{ if eq .Language.Lang "zh" }}中文{{ else }}EN{{ end }}
    </a>
  {{ end }}
</span>
```

### 3.3 修改: layouts/partials/footer.html

所有硬编码中文文字替换为 `{{ i18n "..." }}`：

```html
{{ if ne .Site.Params.Footer.hideRSSAndEmail true }}
{{ if and ( ne .Site.Params.RSS.enableRSS false ) .Site.Params.Author.email }}
{{ i18n "subscribe_rss" }} <a href="/index.xml">RSS</a> {{ i18n "or_email" }} <a href="mailto:{{ .Site.Params.Author.email }}">。</a>
<br />
{{ end }}
{{ if and ( ne .Site.Params.RSS.enableRSS false ) (not .Site.Params.Author.email) }}
{{ i18n "subscribe_rss" }} <a href="/index.xml">RSS</a>。
<br />
{{ end }}
{{ end }}

{{ if ne .Site.Params.Footer.hideMadeWithLine true }}{{ i18n "powered_by" }}
<br />
{{ end }}

{{ if ne .Site.Params.Footer.hideCopyright true }}
{{ i18n "copyright" }}
{{ end }}
{{ if ne .Site.Params.Footer.hideSitemap true }}
🗺️ <a href="/sitemap.xml">{{ i18n "sitemap" }}</a>。
{{ end }}
```

### 3.4 修改: layouts/_default/single.html

1. 标题和日期之后、`<content>` 之前插入 `{{ partial "language-switcher.html" . }}`
2. "相关文章"标题改为 `{{ i18n "related_posts" }}`
3. Giscus `data-lang` 改为动态：`data-lang="{{ i18n "giscus_lang" }}"`

### 3.5 修改: layouts/_default/list.html

1. 搜索框 placeholder 改为 `placeholder="{{ i18n "search_placeholder" }}"`
2. JS 中的 `共 ${visiblePosts} 篇` 改为 `${visiblePosts} {{ i18n "post_count" 0 | safeJS }}` 或用占位符  
   **注意**：JS 内的 i18n 需要额外处理，建议用 Hugo 模板变量：`const countText = '{{ i18n "post_count" }}'.replace('%d', visiblePosts);`
3. Hugo 模板中的 `共 {{ len $visiblePages }} 篇` 改为 `{{ i18n "post_count" (len $visiblePages) }}`
4. "暂无文章" → `{{ i18n "no_posts" }}`
5. "筛选" → `{{ i18n "filter" }}`，"清除筛选" → `{{ i18n "clear_filter" }}`

### 3.6 修改: layouts/index.html

"最近文章" → `{{ i18n "recent_posts" }}`

---

## 4. SEO 标签（custom_head.html）

### 4.1 og:locale 动态化

```html
{{ $locale := "zh_CN" }}
{{ if eq .Language.Lang "en" }}{{ $locale = "en_US" }}{{ end }}
<meta property="og:locale" content="{{ $locale }}" />
```

### 4.2 增加 hreflang alternate 标签

在 `<head>` 中（custom_head.html 或其他位置）添加：

```html
{{ if .IsTranslated }}
  {{ range .Translations }}
  <link rel="alternate" hreflang="{{ .Language.Lang }}" href="{{ .Permalink }}" />
  {{ end }}
  <link rel="alternate" hreflang="{{ .Language.Lang }}" href="{{ .Permalink }}" />
{{ else }}
  <link rel="alternate" hreflang="zh" href="{{ .Permalink }}" />
  {{ if ge .Date.Year 2023 }}
  {{/* 2023+ posts without translation get zh-only hreflang */}}
  {{ end }}
{{ end }}
<!-- x-default for language-agnostic -->
<link rel="alternate" hreflang="x-default" href="{{ .Site.BaseURL }}" />
```

### 4.3 JSON-LD 用当前语言的 URL

JSON-LD 中的 `"@id": .Permalink` 已经使用了当前语言的 URL，无需修改。英文文章的 `.Permalink` 自动包含 `/en/` 前缀。

---

## 5. 浏览器语言自动检测

在 `custom_head.html` 末尾（或 `layouts/partials/` 中新增 `lang-detect.html` 然后 include）添加：

```html
<script>
(function() {
  var preferredLang = localStorage.getItem('preferredLang');
  if (preferredLang) return; // 用户已手动选择过，跳过自动检测

  var navLang = (navigator.language || navigator.userLanguage || '').substring(0, 2).toLowerCase();
  var currentLang = '{{ .Language.Lang }}';

  // 浏览器是英文但页面不是英文 → 跳转英文版
  if (navLang === 'en' && currentLang !== 'en') {
    {{ if .IsTranslated }}
      {{ range .Translations }}
        {{ if eq .Language.Lang "en" }}
          window.location.href = '{{ .Permalink }}';
        {{ end }}
      {{ end }}
    {{ else }}
      // 文章无英文版 → 不跳转
    {{ end }}
  }
})();
</script>
```

注意：
- 首次访问时检测 `navigator.language`
- 用户手动切换后写入 `localStorage.setItem('preferredLang', 'zh'/'en')`
- 语言切换按钮点击时不仅要跳转 URL，还要先写 `localStorage`
- 仅对 2023+ 有英文版的文章生效

---

## 6. 内容翻译清单

### 创建 .en.md 文件

为每个文件在**同级目录**创建英文版本：

```
content/posts/2023/2023-year-summary.md          → content/posts/2023/2023-year-summary.en.md
content/posts/2023/goroutine-leak.md             → content/posts/2023/goroutine-leak.en.md
...（共 32 对）
```

### 英文文件 frontmatter

```yaml
---
title: "English Title"
date: 2023-12-25T13:05:52+08:00
categories: [Essay]
tags: [english-tag]
description: "English description"
---
```

关键规则：
- `date` 保持不变（与中文版相同的发布时间）
- `slug` 不需要设置（Hugo 自动从文件名取 slug，`.en.md` 后缀不影响 slug）
- `tags` 应为英文
- `description` 应为英文
- Hugo 通过文件名前缀匹配翻译对：`2023-year-summary.en.md` ↔ `2023-year-summary.md`

---

## 7. 边界情况

### 7.1 2023 年前的文章（2017-2022）

- 这些文章的 `.md` 文件保持不变
- 不创建 `.en.md` 版本
- 在 `language-switcher.html` 中，`{{ if .IsTranslated }}` 对这些文章为 false，不显示切换按钮
- URL 不变，RSS GUID 不变

### 7.2 RSS

- 默认语言（zh）的 RSS 在 `/index.xml`，只含中文文章
- 英文 RSS 在 `/en/index.xml`，只含英文文章
- `/index.xml` 的 `<language>` 为 `zh-CN`（不变）
- 不需要额外配置，Hugo 内置行为

### 7.3 Giscus 评论

- Giscus 使用 `data-mapping="pathname"`，同一文章的 `pathname` 在不同语言下不同（`/posts/...` vs `/en/posts/...`）
- 这意味着评论系统按语言隔离——中文文章的评论和英文文章的评论是独立的
- `data-lang` 动态设置，中文用 `zh-CN`，英文用 `en`

### 7.4 相关文章

- Hugo `Related` 默认按语言隔离，中文文章只返回中文相关文章，英文只返回英文
- 此行为无需特别配置

### 7.5 首页和列表页

- 首页 `index.html` 中 `where .Site.RegularPages "Section" "posts"` 按语言隔离
- 列表页同理，`.Pages` 按当前语言范围
- 中文访问 `/` 看到中文文章列表，英文访问 `/en/` 看到英文文章列表

### 7.6 部署

- GitHub Actions 使用 `hugo --minify`，多语言模式下自动生成两种语言的静态文件
- 无需修改 workflow 文件
- 构建产物在 `public/` 下：`public/index.html`（中文首页）、`public/en/index.html`（英文首页），以此类推

---

## 8. 文件修改清单

| 文件 | 操作 | 说明 |
|------|------|------|
| `hugo.toml` | 修改 | 添加 `[languages]` 块 |
| `i18n/zh.yaml` | 新建 | 中文 UI 翻译 |
| `i18n/en.yaml` | 新建 | 英文 UI 翻译 |
| `layouts/partials/language-switcher.html` | 新建 | 文章页语言切换器 |
| `layouts/partials/nav.html` | 修改 | i18n 化 + 全局语言切换 |
| `layouts/partials/footer.html` | 修改 | i18n 化 |
| `layouts/_default/single.html` | 修改 | 插入 language-switcher、相关文章标题 i18n、Giscus lang 动态化 |
| `layouts/_default/list.html` | 修改 | 搜索框、post count、空状态 i18n |
| `layouts/index.html` | 修改 | "最近文章" i18n |
| `layouts/partials/custom_head.html` | 修改 | og:locale 动态化、增加 hreflang、增加语言检测 JS |
| `content/posts/YYYY/<slug>.en.md` × 32 | 新建 | 英文文章翻译 |
