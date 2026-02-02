# AGENTS.md

## 概览
- 该仓库是使用 Hugo 搭建的静态站点（个人博客）

## 常用命令
- 按 README 安装 Hugo（extended）：https://gohugo.io/installation/
- 更新 Hugo 模块：hugo mod get -u（README.md:15-18）
- 本地构建站点：hugo（README.md:15-18）
- 运行开发服务器：hugo server（README.md:28-30）
- 新建文章（辅助脚本）：./new post-title（README.md:22-24）或使用 new.sh，它执行 `hugo new posts/2025/$1.md`（new.sh:1-2）

## Available Skills
- create-article: 交互式创建新的文章，使用 Hugo 前言区添加元数据（标题、日期、标签等）。
- proofead: 能够校对和编辑 Markdown 文章内容，确保语法正确、格式一致。

## 架构
- 站点生成器：Hugo（配置见 [hugo.toml](hugo.toml)：包含 baseURL、远程主题模块导入、参数和永久链接）。仓库以模块方式引入主题：github.com/rokcso/hugo-bearblog-neo（hugo.toml:11-14）。
- 内容：`content/` —— 文章存放于 `content/posts/`（示例：content/posts/2025/*.md）。使用 Hugo 前言区添加元数据。
- 布局：`layouts/` —— 自定义模板包括 `_default/single.html`（layouts/_default/single.html）以及 `layouts/partials/custom_head.html` 等局部模板。
  - 注意：`layouts/_default/single.html` 包含可选的文章点赞功能的内联 JS，会读取 `.Site.Params.upvoteURL` 和 `.Site.Params.upvote`（layouts/_default/single.html:25-84, 93-126）。
- 静态资源：`static/` —— 图片、CSS、JS 直接按原样提供。
- 模块/资产：`assets/`（如存在）用于 Hugo Pipes；在假定有 SCSS 处理前请确认。
- 部署：通过 GitHub Actions 部署至 GitHub Pages。工作流 `.github/workflows/deploy.yml` 使用 `hugo --minify` 构建并通过 peaceiris/actions-gh-pages 发布（deploy.yml:17-30）。

## 开发提示
- 修改内容时，编辑 `content/` 下的文件（content/posts/...）。添加新文章时，优先使用提供的 `new.sh` 或 `hugo new` 命令，除非用户要求手动创建。
- 编辑模板时，请检查 [hugo.toml](hugo.toml) 中 `.Site.Params` 的使用，并保持 `title`、`date`、`tags`、`toc`、`upvote` 等预期前言区键。
- 保持保守：除非用户请求，不要添加基于 Node 或其他语言的工具链。仓库预期仅使用 Hugo 工作流。
- CI 行为：`.github/workflows/deploy.yml` 在 push 到 `master` 时运行，并使用 Hugo v0.150.1 extended；涉及 Hugo extended（如 SCSS、图像处理）特性的功能需注意。

## 重要文件参考（示例）
- 站点配置：[hugo.toml](hugo.toml)
- README：[README.md](README.md)
- 文章模板：[archetypes/default.md](archetypes/default.md)
- 部署工作流：[.github/workflows/deploy.yml](.github/workflows/deploy.yml)
- 新建文章助手：[new.sh](new.sh)
- 内容目录：[content/](content/)
