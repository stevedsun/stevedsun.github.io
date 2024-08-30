---
title: "Windows Efficient Setup"
date: 2024-08-31T00:23:37+08:00
categories: [Efficiency]
tags: [Windows, Omakub]
aliases: [/posts/windows-efficient-setup/]
description: "Setup an efficient development environment on Windows"
---

Last month I read DHH's blog post [Introducing Omakub](https://world.hey.com/dhh/introducing-omakub-354db366). Omakub is a project that helps you to setup your Ubuntu machine by running a single command. DHH composed a list of tools he uses on his Ubuntu.

In spirit of the post, I decided to setup my Windows machine efficiently like Omakub.

You can find the full setup script [here](https://gist.github.com/stevedsun/319f0c05b02e739207743dd441b6239a).

Following is the keyboard Layout I am using.

## Keyboard Layout

**Tool**: AutoHotKey, PowerToys

| Shortcut      | Description                  |
| ------------- | ---------------------------- |
| Alt + Number  | Switch between Apps          |
| Win + Number  | Switch between Desktops      |
| Caplock       | Switch between Input Methods |
| Caplock(hold) | Switch between Upper/Lower   |

1. Download [VirtualDesktopAccessor.dll](https://github.com/Ciantic/VirtualDesktopAccessor/releases/tag/2024-01-25-windows11)
2. Put the `.dll` and `.ahk` files in one folder, create a shortcut for `Config.ahk`.
3. Copy the shortcut to path `C:\Users\<YourName>\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup` to make it auto startup.
4. Install `PowerToys`, remap `LWin` and `LAlt`.
5. (Optional) Turn off window animation in windows settings.

## The Problem of Windows' Shortcuts

As we know, the Windows shortcut is very limited when switching between apps and desktops. For users who are not English native speakers, switching input method when typing is also not a good experience.

Comparing with Windows, MacOS has a very powerful shortcut system. You can always use `cmd + q` to close a window, `caplock` to switch between input methods.

DHH moved the MacOS' advantages to Linux. The Windows users can also refer to the Omakub project and build a more powerful development environment.
