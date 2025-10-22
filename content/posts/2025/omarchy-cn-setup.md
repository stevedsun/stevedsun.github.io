---
title: "Omarchy 一些中文环境下的设置"
date: 2025-10-22T23:21:21+08:00
categories: [随笔]
tags: ["Linux"]
aliases: [/posts/omarchy-cn-setup/]
description: ""
---

最近把家里电脑装上了 DHH 的 [Omarchy](https://omarchy.org/)（一个基于 Hyprland 桌面环境的 Arch Linux 发行版）。

装完后有一些需要改造的配置记录在这篇文章中，供大家参考。

## 4K 显示器设置

修改系统菜单 Setup - Monitor，按照你自己显示器的分辨率，根据配置文件中的注释设置参数，比如我的显示器 27 寸 4k：

```conf
env = GDK_SCALE,1.75
monitor=,preferred,auto,1.875
```

额外为 QT 软件添加缩放设置

```conf
env = QT_AUTO_SCREEN_SCALE_FACTOR,1
env = QT_SCALE_FACTOR,1.75
```

## 中文输入法

参考 [Fcitx 最佳配置实践](https://manateelazycat.github.io/2024/12/17/fcitx-best-config/)。文章中“安装 emacs-rime”这一章节如果不使用 emacs 可以忽略。

## 终端字体修改设置

系统自带字体在终端环境下对中文都不太友好。我喜欢用`Maple Mono`这个字体，可以安装 AUR 包`maple-mono-nf-cn`这个库。然后在`~/.config/alacritty/alacritty.toml`中修改字体设置：

```toml
[font]
normal = { family = "Maple Mono NF CN" }
bold = { family = "Maple Mono NF CN" }
italic = { family = "Maple Mono NF CN" }
size = 12
```

## 键盘默认的 numlock 关闭

Omarchy 安装后会默认开启小键盘的 numlock，可以在系统菜单 Setup - Input 中设置：

```conf
numlock_by_default = false
```

## Neovim 的一些设置

Neovim 默认使用了 Lazyvim，我在`~/.config/nvim/lua/config/options.lua`里添加了一些配置，可以参考注释选择性添加：

```lua
-- 修复中文字体在终端里有下划线的问题
vim.opt.spelllang = { "en", "cjk" }

-- 在 markdown 文件中关闭语法检查
vim.api.nvim_create_autocmd("FileType", {
 pattern = "markdown",
 callback = function()
  vim.diagnostic.enable(false)
 end,
})
```

然后创建`~/.config/nvim/lua/plugins/flush.lua`并添加内容，恢复 Vim 默认的 normal 模式下 s 键的功能：

```lua
return {
  {
    "folke/flash.nvim",
    keys = {
      { "s", mode = { "n", "x", "o" }, false },
    },
  },
}
```
