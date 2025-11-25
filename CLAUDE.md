# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

Overview
- This repository is a Hugo static site (personal blog) using a remote module theme: github.com/rokcso/hugo-bearblog-neo. Site config is in [hugo.toml](hugo.toml). Content lives under the `content/` folder (posts in `content/posts/`). Templates are in `layouts/`. Static files are in `static/` and optional asset pipeline files may be under `assets/`.

Common commands
- Install Hugo (extended) per the README: https://gohugo.io/installation/
- Update Hugo modules: hugo mod get -u  (README.md:15-18)
- Build site (production): hugo --minify (used by CI) (.github/workflows/deploy.yml:23-24)
- Build site (local): hugo (README.md:15-18)
- Run dev server: hugo server (README.md:28-30)
- Create a new post (helper script): ./new post-title (README.md:22-24) or use new.sh which runs `hugo new posts/2025/$1.md` (new.sh:1-2)

Notes on tests/lint
- There are no test or linting tools configured (no package.json, no Makefile, no test suite). Do not assume availability of node/npm-based workflows. If you need static checks, propose adding them and get user approval.

High-level architecture
- Site generator: Hugo (config in [hugo.toml](hugo.toml): lines show baseURL, module import of the remote theme, params and permalinks). The repo imports a theme as a module: github.com/rokcso/hugo-bearblog-neo (hugo.toml:11-14).
- Content: `content/` — posts live in `content/posts/` (examples: content/posts/2025/*.md). Use Hugo front matter to add metadata.
- Layouts: `layouts/` — custom templates include `_default/single.html` (layouts/_default/single.html) and partials like `layouts/partials/custom_head.html`.
  - Note: `layouts/_default/single.html` contains inline JS for the optional post upvote feature which consults `.Site.Params.upvoteURL` and `.Site.Params.upvote` (layouts/_default/single.html:25-84, 93-126).
- Static assets: `static/` — images, CSS, JS served as-is.
- Modules/assets: `assets/` (if present) used for Hugo Pipes; check before assuming SCSS processing.
- Deploy: GitHub Pages via GitHub Actions. Workflow: `.github/workflows/deploy.yml` builds with `hugo --minify` and deploys using peaceiris/actions-gh-pages (deploy.yml:17-30).

Developer hints for Claude Code
- When asked to modify content, edit files under `content/` (content/posts/...). For adding a new post, prefer running the provided `new.sh` or `hugo new` commands rather than creating files by hand unless the user asks.
- When editing templates, check for use of `.Site.Params` in [hugo.toml](hugo.toml) and preserve expected front matter keys like `title`, `date`, `tags`, `toc`, and `upvote`.
- Be conservative: do not add Node-based or language-specific tooling unless the user requests it. The repo expects Hugo-only workflow.
- CI behavior: The `.github/workflows/deploy.yml` runs on push to `master` and uses Hugo v0.150.1 extended; keep that in mind for features requiring Hugo extended (SCSS, image processing).

Important file references (examples)
- Site config: [hugo.toml](hugo.toml)
- README: [README.md](README.md)
- Deploy workflow: [.github/workflows/deploy.yml](.github/workflows/deploy.yml)
- Post templates: [layouts/_default/single.html](layouts/_default/single.html)
- Custom head partial: [layouts/partials/custom_head.html](layouts/partials/custom_head.html)
- New post helper: [new.sh](new.sh)
- Content folder: [content/](content/)

If a CLAUDE.md already exists, update it instead of overwriting. When making content or template changes, prefer small, narrowly-scoped edits and run a local `hugo server` check. Ask the user before introducing tests, linters, or additional CI steps.
