---
title: "Omarchy: Some Setup Tweaks for a Chinese-Language Environment"
slug: "omarchy-cn-setup"
date: 2025-10-22T23:21:21+08:00
categories: [Essays]
tags: ["Linux"]
aliases: [/posts/omarchy-cn-setup/]
description: ""
---

I recently installed DHH's [Omarchy](https://omarchy.org/) (an Arch Linux distribution based on the Hyprland desktop environment) on my home computer.

After installation, there were a few configuration tweaks I needed to make. I'm recording them in this post for reference.

## 4K Monitor Settings

Modify the system menu Setup - Monitor, and set the parameters based on your own display's resolution, following the comments in the configuration file. For example, my 27-inch 4K display:

```conf
env = GDK_SCALE,1.75
monitor=,preferred,auto,1.875
```

Add additional scaling settings for QT applications:

```conf
env = QT_AUTO_SCREEN_SCALE_FACTOR,1
env = QT_SCALE_FACTOR,1.75
```

## Chinese Input Method

Refer to [Fcitx Best Configuration Practices](https://manateelazycat.github.io/2024/12/17/fcitx-best-config/). The section titled "Installing emacs-rime" in that article can be skipped if you don't use emacs.

## Terminal Font Settings

The default system fonts aren't very friendly to Chinese in the terminal. I like the `Maple Mono` font, which you can install via the AUR package `maple-mono-nf-cn`. Then modify the font settings in `~/.config/alacritty/alacritty.toml`:

```toml
[font]
normal = { family = "Maple Mono NF CN" }
bold = { family = "Maple Mono NF CN" }
italic = { family = "Maple Mono NF CN" }
size = 12
```

## Disable NumLock by Default

Omarchy enables NumLock on the numpad by default after installation. You can change this in the system menu Setup - Input:

```conf
numlock_by_default = false
```

## A Few Neovim Settings

Neovim uses Lazyvim by default. I added a few lines to `~/.config/nvim/lua/config/options.lua`—feel free to pick what you need based on the comments:

```lua
-- Fix the issue of Chinese characters showing underlines in the terminal
vim.opt.spelllang = { "en", "cjk" }

-- Disable syntax checking in markdown files
vim.api.nvim_create_autocmd("FileType", {
 pattern = "markdown",
 callback = function()
  vim.diagnostic.enable(false)
 end,
})
```

Then create `~/.config/nvim/lua/plugins/flush.lua` with the following content to restore Vim's default behavior for the `s` key in normal mode:

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
