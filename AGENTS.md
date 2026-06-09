# stevedsun.github.io — Hugo blog at sund.site

## Project info
- **Hugo** v0.150.1, module-based theme: `github.com/rokcso/hugo-bearblog-neo`
- **No** themes/ directory — theme comes from go.mod Hugo Module
- **Config**: `hugo.toml`
- **Content**: `/content/posts/YYYY/slug.md` — date-based URL: `/posts/:year/:slug`
- **Deploy**: GitHub Pages via GitHub Actions (.github/workflows/)
- **Live**: https://sund.site

## Key layout files
| File | Purpose |
|------|---------|
| `layouts/_default/single.html` | Article page (overrides theme, adds Giscus comments, related posts) |
| `layouts/_default/list.html` | Posts list (overrides theme, Chinese UI, M.D date format) |
| `layouts/index.html` | Homepage (renders content + recent 5 posts) |
| `layouts/partials/custom_head.html` | Custom OG/Twitter tags + JSON-LD for posts |
| `layouts/partials/seo_tags.html` | Prevents duplicate OG/Twitter output for post pages |
| `layouts/partials/nav.html` | Navigation bar (Chinese labels) |
| `layouts/partials/footer.html` | Footer (Chinese text) |
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
- Date format: `M.D` (e.g. `6.7`)
- Images hosted on `https://raw.githubusercontent.com/stevedsun/blog-img/main/`
- Comments: Giscus (GitHub Discussions)
- Tags are Chinese + English mixed

## Bilingual post rule — mandatory check before every new post

This site uses **Hugo native multilingual** (not inline mixing). Both languages share `contentDir = "content"`; English files use the `.en.md` suffix convention.

### File layout

| Language | File | Example |
|----------|------|---------|
| Chinese (default) | `content/posts/YYYY/slug.md` | `content/posts/2025/how-to-deal-with-elders.md` |
| English | `content/posts/YYYY/slug.en.md` | `content/posts/2025/how-to-deal-with-elders.en.md` |

### Rules

1. Every new `.md` post (Chinese) — check if it's a **translation** (译文, e.g. Chinese version of an English original). If NOT a translation, you MUST create the English counterpart as `.en.md`.
2. English counterpart: same `slug`, same `date`, same `categories`/`tags` if applicable. `title` and `description` in English.
3. If the post is already a translation — do nothing.
4. Do NOT modify existing `.en.md` files for non-bilingual posts — only create new ones for new originals.
