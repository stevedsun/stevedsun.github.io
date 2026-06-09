# 双语支持 — Bilingual Support

## 需求描述

博客 sund.site 当前全站中文（zh-CN）。需要为 2023 年及之后的文章（约 32 篇）增加英文版本，形成一个中英双语的博客站点。

核心使用场景：
- **中文用户**访问时看到中文文章，URL 无语言前缀（保持现状）
- **英文用户**访问时自动切换到英文版
- 文章标题下方显示语言切换按钮，用户可随时手动切换中/英文版本
- 导航栏、页脚、文章列表页等 UI 文字随语言切换
- RSS 订阅者不受影响

## 已有上下文

- **Hugo v0.134.2**，模块主题 `github.com/rokcso/hugo-bearblog-neo`
- **当前配置**：`languageCode = "zh-CN"`，无多语言设置
- **内容结构**：`content/posts/YYYY/slug.md`，URL 格式 `/posts/:year/:slug`
- **自定义布局**：`layouts/_default/single.html`（含 Giscus 评论、相关文章）、`layouts/_default/list.html`（搜索、按年分组）、`layouts/index.html`（首页最近文章）、`layouts/partials/nav.html`（中文导航）、`layouts/partials/footer.html`（中文页脚）、`layouts/partials/custom_head.html`（OG/JSON-LD/Google Analytics）
- **部署**：GitHub Pages（GitHub Actions → `peaceiris/actions-gh-pages`）

### RSS 影响已排除

保留 `zh` 为默认语言、不加 URL 前缀。现有文章 URL 不变 → RSS `<guid>` 不变 → 订阅者零干扰。主 RSS `/index.xml` 只含中文文章，英文文章独立出现在 `/en/index.xml`。

### 需要双语化的 32 篇文章

**2023（5 篇）**：2023-year-summary、goroutine-leak、go-server-side-events、python-packaging、user-story-mapping

**2024（9 篇）**：audit-system-design、go-dependency-inject、leshan、metrics-project-retro、pairing-with-ai-01、restful-api-cookbook、ricoh_gr2_sharing、symbiosis、windows-efficient-setup

**2025（12 篇）**：ai-e2e-testing、ast-chunk、build-deepwiki、do-not-vibe-testing、ext-judging、go-performance、hand-on-enablement、how-to-deal-with-elders、omarchy-cn-setup、pairing-with-ai-02、retro-kernel-panic、super-communicator

**2026（6 篇）**：ai-agent-tool-comparison-mcp-transitional、how-i-use-hermes-agent、how-to-make-an-agent、running-an-ai-native-engineering-org、why-your-ai-first-strategy-translation、you-can-just-say-it

## 验收条件（AC）

### AC1: Hugo 多语言配置
- [ ] `hugo.toml` 中配置 `languages.zh` 和 `languages.en` 两个块
- [ ] `zh` 为默认语言（`defaultContentLanguage`），URL 无 `/zh/` 前缀
- [ ] `en` 语言 URL 前缀为 `/en/`
- [ ] 构建通过：`hugo --minify` 无错误

### AC2: 文章内容双语
- [ ] 32 篇 2023+ 文章各有一个 `.en.md` 英文版本
- [ ] 英文文章与中文文章通过文件名关联（`slug.en.md` ↔ `slug.md`），Hugo 自动识别为翻译对
- [ ] 英文文章 URL 为 `/en/posts/:year/:slug`
- [ ] 中文文章 URL 保持 `/posts/:year/:slug` 不变
- [ ] 2023 年之前的文章不产生英文版本，访问时保持现状

### AC3: 语言切换按钮
- [ ] 每篇文章标题下方显示语言切换按钮（"English" / "中文"）
- [ ] 当前语言版本用高亮/实心样式标识
- [ ] 点击切换到另一种语言的对应文章
- [ ] 切换按钮在移动端可用（触摸友好）

### AC4: 浏览器语言自动检测
- [ ] 首次访问时，JS 检测 `navigator.language`，若为英文系（en/...）则自动跳转到对应英文文章
- [ ] 用户手动切换后，选择存入 `localStorage`，后续访问不再自动跳转
- [ ] `localStorage` 键名为 `preferredLang`
- [ ] 中文用户（或浏览器语言非英文）不受影响，不产生额外跳转

### AC5: 导航和页脚双语
- [ ] 导航栏文字随语言切换："首页" ↔ "Home"、"文章" ↔ "Posts"
- [ ] 页脚文字随语言切换："订阅 RSS" ↔ "Subscribe RSS" / "站点地图" ↔ "Sitemap"
- [ ] 导航栏增加语言切换入口（全局切换，不限于文章页）

### AC6: 列表页和首页双语
- [ ] 文章列表页标题随语言切换
- [ ] 搜索框占位文字随语言切换："搜索..." ↔ "Search..."
- [ ] "共 N 篇" 文字随语言切换
- [ ] 首页"最近文章"标题随语言切换
- [ ] 按年份分组时，年份号码不翻译

### AC7: SEO 标签
- [ ] HTML `<head>` 中输出 `<link rel="alternate" hreflang="zh" href="...">` 和 `<link rel="alternate" hreflang="en" href="...">`
- [ ] `<meta property="og:locale">` 根据当前语言正确设置
- [ ] 英文文章对应的 JSON-LD 中 `@id` 使用英文 URL

### AC8: RSS 不受影响
- [ ] `/index.xml` 仍只包含中文文章，GUID 不变，URL 不变
- [ ] `/en/index.xml` 生成并只包含英文文章
- [ ] `/index.xml` 中 `<language>` 为 `zh-CN`

### AC9: 2023 年前的文章兼容
- [ ] 2023 年前的文章仍可访问，URL 不变
- [ ] 2023 年前的文章不显示语言切换按钮（只有中文版本）
- [ ] 2023 年前的文章不产生英文版本

### AC10: 构建和部署
- [ ] `hugo --minify` 构建成功，无任何 warning
- [ ] GitHub Actions 部署后，站点可正常访问
- [ ] 中文文章路径 `/posts/:year/:slug` 可访问
- [ ] 英文文章路径 `/en/posts/:year/:slug` 可访问
