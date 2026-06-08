# stevedsun.github.io — Hugo blog at sund.site

## Project info
- **Hugo** v0.150.1, module-based theme: `github.com/rokcso/hugo-bearblog-neo`
- **No** themes/ directory — theme comes from go.mod Hugo Module
- **Config**: `hugo.toml`
- **Content**: `/content/posts/YYYY/slug.md` — date-based URL: `/posts/:year/:slug`
- **Deploy**: manual `hugo` build, served via Vercel (GitHub Pages origin)
- **Live**: https://sund.site

## Key layout files
| File | Purpose |
|------|---------|
| `layouts/_default/single.html` | Article page (overrides theme, adds Giscus comments) |
| `layouts/partials/custom_head.html` | `<head>` injection: custom fonts, OG/Twitter tags, Chroma styles, KaTeX, Mermaid, GA |
| `layouts/partials/third-party-scripts.html` | KaTeX + Mermaid CDN scripts |
| `layouts/partials/chroma-styles.html` | Code highlight CSS |
| `layouts/_default/_markup/render-codeblock-mermaid.html` | Mermaid render hook |

## Article frontmatter
```yaml
title: string
date: ISO-8601 with timezone
draft: false
slug: "kebab-case"
categories: [string...]
tags: [string...]
description: "summary text"
```

No `images`, `featured_image`, `cover` fields. All images are inline Markdown `![](url)`.

## Conventions
- Language: zh-CN
- Images hosted on `https://raw.githubusercontent.com/stevedsun/blog-img/main/`
- Comments: Giscus (GitHub Discussions)
- Tags are Chinese + English mixed
