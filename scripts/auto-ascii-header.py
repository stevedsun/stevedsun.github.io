#!/usr/bin/env python3
"""
auto-ascii-header.py
自动为 Hugo 博客文章生成 ASCII Art 头图（900×383px，微信公众号头条封面规格）

用法:
  python3 auto-ascii-header.py "文章标题" [--slug SLUG] [--tags TAG1,TAG2] [--date YYYY-MM-DD]

示例:
  python3 auto-ascii-header.py "AI Agent 工具对比" --slug ai-agent-tool-comparison --tags "AI,MCP,Skill"
"""

import argparse
import os
import sys
import subprocess
from pathlib import Path

# ─── 规格常量 ───────────────────────────────────────────────
WIDTH  = 900
HEIGHT = 383
OUTPUT_DIR = Path(__file__).parent.parent / "static" / "images"

# 微信公众号头条封面关键安全区（中心 383×383）
SAFE_CENTER_X = WIDTH  // 2   # 450
SAFE_CENTER_Y = HEIGHT // 2   # 191

# CRT Green Phosphor 配色
BG_COLOR         = "#070d07"
PHOSPHOR         = "#39ff14"
PHOSPHOR_BRIGHT  = "#7fff00"
PHOSPHOR_DIM     = "#1a8a0a"
DARK_ACCENT      = "#0d440d"

# Google Fonts
FONT_IMPORT   = """@import url('https://fonts.googleapis.com/css2?family=VT323&family=Share+Tech+Mono&display=swap');"""
FONT_MONO     = "'Share Tech Mono', 'Courier New', monospace"
FONT_CRT      = "'VT323', 'Courier New', monospace"

# ─── HTML 模板 ──────────────────────────────────────────────
CSS = f"""
<style>
{FONT_IMPORT}
:root {{
  --bg: {BG_COLOR};
  --phosphor: {PHOSPHOR};
  --phosphor-dim: {PHOSPHOR_DIM};
  --phosphor-bright: {PHOSPHOR_BRIGHT};
}}
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{
  background: var(--bg);
  font-family: {FONT_MONO};
  width: {WIDTH}px;
  height: {HEIGHT}px;
  overflow: hidden;
  position: relative;
}}
.scanlines {{
  position: absolute; inset: 0;
  background: repeating-linear-gradient(to bottom, transparent 0px, transparent 2px, rgba(0,0,0,0.15) 2px, rgba(0,0,0,0.15) 4px);
  pointer-events: none; z-index: 10;
}}
.noise-layer {{
  position: absolute; inset: 0;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)' opacity='0.05'/%3E%3C/svg%3E");
  opacity: 0.05; pointer-events: none; z-index: 5;
}}
.main {{
  position: absolute; inset: 0; z-index: 1;
  display: flex; flex-direction: column;
  justify-content: center;
  padding: 20px 28px; gap: 0;
}}
.title-row {{
  font-family: {FONT_MONO};
  font-size: 26px;
  color: var(--phosphor-bright);
  text-shadow: 0 0 10px var(--phosphor-bright), 0 0 25px var(--phosphor);
  letter-spacing: 0.05em;
  white-space: nowrap; overflow: hidden;
  animation: flicker 4s infinite;
  margin-bottom: 2px;
}}
@keyframes flicker {{
  0%, 100% {{ opacity: 1; }}
  92% {{ opacity: 1; }} 93% {{ opacity: 0.82; }}
  94% {{ opacity: 1; }} 96% {{ opacity: 0.88; }} 97% {{ opacity: 1; }}
}}
.subtitle-row {{
  font-family: {FONT_MONO};
  font-size: 12px; color: var(--phosphor-dim);
  letter-spacing: 0.1em; margin-bottom: 8px;
}}
.decor-row {{ font-size: 10px; white-space: pre; overflow: hidden; line-height: 1.2; }}
.decor-row.dim {{ color: {DARK_ACCENT}; }}
.data-row {{
  display: flex; align-items: center; gap: 20px;
  margin-top: 6px; font-size: 13px; letter-spacing: 0.04em;
}}
.label {{ color: var(--phosphor-dim); }}
.value {{ color: var(--phosphor-bright); text-shadow: 0 0 7px var(--phosphor-bright); }}
.err {{ color: #ff4444; text-shadow: 0 0 7px #ff4444; }}
.bar {{ font-size: 11px; letter-spacing: 0; }}
.matrix-art {{
  position: absolute; right: 20px; top: 50%;
  transform: translateY(-50%);
  font-size: 8px; line-height: 1.1;
  color: var(--phosphor); letter-spacing: 0;
  white-space: pre; text-shadow: 0 0 5px var(--phosphor);
  text-align: right; opacity: 0.65;
}}
.bottom-row {{
  position: absolute; bottom: 10px; left: 28px; right: 28px;
  display: flex; justify-content: space-between; align-items: center;
  font-size: 10px; color: var(--phosphor-dim);
  border-top: 1px solid {DARK_ACCENT}; padding-top: 7px;
}}
.tag {{
  border: 1px solid var(--phosphor-dim); padding: 1px 4px;
  font-size: 9px; color: var(--phosphor-dim); margin-right: 5px;
}}
.tag.bright {{ border-color: var(--phosphor); color: var(--phosphor); }}
.corner {{
  position: absolute; color: var(--phosphor-dim);
  font-size: 12px; opacity: 0.5;
}}
.corner.tl {{ top: 7px; left: 10px; }}
.corner.tr {{ top: 7px; right: 10px; }}
.corner.bl {{ bottom: 7px; left: 10px; }}
.corner.br {{ bottom: 7px; right: 10px; }}
</style>
"""

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="zh">
<head>
<meta charset="UTF-8">
<title>{title}</title>
{CSS}
</head>
<body>
<div class="scanlines"></div>
<div class="noise-layer"></div>
<div class="corner tl">┌─</div>
<div class="corner tr">─┐</div>
<div class="corner bl">└─</div>
<div class="corner br">─┘</div>

<div class="main">
  <div class="title-row"> {title} </div>
  <div class="subtitle-row">{subtitle} // {date} //</div>
  <div class="decor-row dim">{"░" * 80}</div>
  <div class="decor-row">{"▓" * 80}</div>
  <div class="data-row">
    <span class="label">SYS:</span>
    <span class="value">RETRO-ASCII-ART</span>
    <span class="label">// MODE:</span>
    <span class="value">CRT-PHYSPHOR</span>
    <span class="label">// DIM:</span>
    <span class="value">{WIDTH}×{HEIGHT}</span>
  </div>
  <div class="data-row">
    <span class="label">ARTIFACT:</span>
    <span class="bar">{"█" * 16}░{"░" * 8}</span>
    <span class="value">67%</span>
    <span class="label">// {tags_str}</span>
  </div>
</div>

<div class="matrix-art">
{"██ ██ ██ ██ ██ ██"}
{"  ████████  ████"}
{"    ██  ██  ██"}
{"  ████  ████"}
{"    ██  ██"}
{"  ████████████"}
</div>

<div class="bottom-row">
  <span>sund.site // AI ANXIETY GENERATOR</span>
  <span>{tags_html}</span>
</div>
</body>
</html>"""

# ─── 主函数 ─────────────────────────────────────────────────

def generate_html(title: str, slug: str, tags: list, date: str) -> str:
    """生成 HTML 内容"""
    tags_str = " // ".join(tags[:4])
    tags_html = "".join(
        f'<span class="tag bright">#{t.strip()}</span>' for t in tags[:4]
    )
    subtitle = " // ".join(tags[:2]) if tags else "CRT-BANNER"

    html = HTML_TEMPLATE.format(
        title=title,
        subtitle=subtitle,
        date=date,
        tags_str=tags_str,
        tags_html=tags_html,
        CSS=CSS,
        WIDTH=WIDTH,
        HEIGHT=HEIGHT,
    )
    return html


def save_html(html: str, slug: str) -> Path:
    """保存 HTML 到 /tmp/"""
    path = Path(f"/tmp/{slug}-header-900x383.html")
    path.write_text(html, encoding="utf-8")
    return path


def capture_screenshot(html_path: Path, output_png: Path) -> bool:
    """用 chromium 截图（通过浏览器工具）"""
    # 构建 URL
    url = f"file://{html_path.resolve()}"
    try:
        import hermes_tools
        hermes_tools.browser_navigate(url=url)
        # 截图另存
        # 注意：这里需要截图保存到 output_png
        # 实际实现中通过截图工具处理
        return True
    except Exception as e:
        print(f"[WARN] 截图失败: {e}，请手动从浏览器保存")
        return False


def save_to_blog(slug: str, output_dir: Path = None):
    """将已生成的截图复制到博客 static/images/{slug}/"""
    if output_dir is None:
        output_dir = OUTPUT_DIR
    img_dir = output_dir / slug
    img_dir.mkdir(parents=True, exist_ok=True)
    src = Path(f"/tmp/{slug}-header-900x383.html")
    if src.exists():
        print(f"[INFO] HTML 已保存在: {src}")
    dst = img_dir / "header-900x383.png"
    print(f"[INFO] 头图目录: {img_dir}/")
    print(f"[INFO] 提示: 请用浏览器打开 {src} 然后截图保存到 {dst}")
    return dst


def main():
    parser = argparse.ArgumentParser(description="生成 ASCII Art 博客头图（900×383）")
    parser.add_argument("title", help="文章标题")
    parser.add_argument("--slug", "-s", help="文章 slug（默认：从标题生成）")
    parser.add_argument("--tags", "-t", default="", help="标签，逗号分隔")
    parser.add_argument("--date", "-d", default="", help="日期 YYYY-MM-DD（默认：今天）")
    args = parser.parse_args()

    import datetime
    title = args.title
    slug  = args.slug or title.lower().replace(" ", "-").replace("—", "-").replace(":", "").strip()
    tags  = [t.strip() for t in args.tags.split(",") if t.strip()]
    date  = args.date or datetime.date.today().strftime("%Y.%m.%d")

    print(f"╔═══ ASCII Art 头图生成器 ═══╗")
    print(f"║ 标题: {title}")
    print(f"║ Slug: {slug}")
    print(f"║ 标签: {', '.join(tags) or '无'}")
    print(f"║ 日期: {date}")
    print(f"║ 尺寸: {WIDTH}×{HEIGHT}px")
    print(f"╚══════════════════════════════╝")

    # 1. 生成 HTML
    html = generate_html(title, slug, tags, date)
    html_path = save_html(html, slug)
    print(f"[OK] HTML → {html_path}")

    # 2. 截图
    # 用户需要手动从浏览器截图，或调用截图 API
    save_to_blog(slug)

    print("\n[下一步]")
    print(f"  1. 浏览器打开: file://{html_path.resolve()}")
    print(f"  2. 截图（确保 900×383 或等比）")
    print(f"  3. 保存到: {OUTPUT_DIR / slug / 'header-900x383.png'}")
    print(f"  4. 重新构建博客: cd {Path(__file__).parent.parent} && hugo")


if __name__ == "__main__":
    main()
