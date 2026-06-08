# 全站语言统一为中文

## 背景
sund.site 多处系统文本为英文（导航栏、文章计数、搜索、页脚、日期格式），与 `lang=zh-CN` 的声明不符。

## 改动清单

### 1. hugo.toml — 配置中文化
- `description` → `"Steve Sun 的博客"`
- `copyright` → `"版权所有 © 2013-2026, Steve Sun"`
- 新增 `dateFormat = "2006-01-02"`

### 2. content/_index.md — 首页正文
- `"My Side Projects"` → `"个人项目"`
- `"Contact Me"` → `"联系我"`
- 前三句英文保留（内容意图，可个性化定制）

### 3. content/friends.md — 朋友页标题
- `title: "Friends"` → `title: "朋友"`

### 4. layouts/partials/nav.html — 导航栏（新建覆盖）
- `"Home"` → `"首页"`
- `"Blog"`（实际 Posts）→ `"文章"`
- 导航项名全部中文

### 5. layouts/partials/footer.html — 页脚（新建覆盖）
- `"Subscribe via RSS"` → `"订阅 RSS"`
- `"say hello"` / `"email"` → `"发送邮件"`
- `"Made with Hugo Bear Neo"` → `"由 Hugo Bear Neo 驱动"`
- `"Sitemap"` → `"站点地图"`

### 6. layouts/_default/list.html — 文章列表页（新建覆盖）
- 搜索占位符 `"Search..."` → `"搜索..."`
- 文章计数 `"There are 74 pieces."` → `"共 74 篇"`
- 筛选文本 `"Filtering for"` → `"筛选："`
- `"Remove filter"` → `"清除筛选"`
- `"No posts yet"` → `"暂无文章"`
- JS 动态计数也改为中文格式

## 验收条件
1. 导航栏显示「首页」「文章」「朋友」
2. `/posts/` 页搜索框占位符为「搜索...」
3. `/posts/` 页显示「共 74 篇」
4. 页脚显示「订阅 RSS」「由 Hugo Bear Neo 驱动」「站点地图」
5. 文章日期格式为 `2026-06-07`
6. 首页「个人项目」「联系我」
7. `hugo build` 无报错
