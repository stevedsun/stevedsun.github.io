---
title: "Python 依赖管理工具的研究"
date: 2023-01-19T08:05:27+08:00
categories: [Python]
tags: [python]
aliases: [/posts/python-packaging/]
---

## 太长不读

如果你从事工程项目，[poetry](https://python-poetry.org/) 是目前最好的方案，但是如果你不喜欢 Python 的 virtualenv，可以试试 [pdm](https://pdm.fming.dev/latest/)。

## 混乱的 Python

Python 的依赖管理工具 `pip` 一直被众多开发者吐槽。从我个人角度，`pip` 有三点致命缺陷：

- 无法解决 Python 依赖环境的隔离问题
- 依赖管理文件 `requirements.txt` 无法真正开箱即用
- 打包部署非常麻烦，需要手动配置

### 环境隔离问题

Python 的依赖库可以安装到系统全局，也可以安装到用户目录（`/home/${USER}/.local`）。但如果你同时管理多个 Python 项目，就需要将不同项目的依赖拆分到不同的文件夹分开管理。

传统方式是基于 virtualenv 创建隔离的 Python bin 文件和项目依赖的虚拟环境（所谓虚拟环境并不是虚拟机，只是个绑定 terminal session 的命令环境）。这种方式的缺点是：

- 开发者需要经常关注“我现在处于哪个项目目录？我需要切换到当前虚拟环境里吗？”之类的问题。
- virtualenv 只解决环境隔离，但是无法同步更新依赖文件、打包发布。

### 依赖安装问题

Python 管理依赖的手段，最早是手动执行`pip install xxx`来安装依赖，最后 `pip freeze` 来导出依赖列表到一个 `requirements.txt` 文件里。但是这个 txt 文件非常令人困惑。

- 不像 NodeJS 那么方便，想要升、降级某个依赖版本，无法自动同步到 txt 文件里。
- 平铺式地列出了所有一级、二级依赖包（即依赖包的依赖包）。因为 Python 某些依赖又基于系统上安装的 C 库版本，这就导致不同系统环境上执行 `pip install -r requirements.txt` 得到的效果并不一致，经常报错。

### 打包部署问题

Python 一般使用 `wheel` 打包二进制，它只解决打包问题，环境依赖是靠 pip 和 setuptools 完成，所以使用 wheel 你仍然要操心环境隔离和依赖管理问题。

另外基于 Python 各版本之间兼容性问题和底层实现上的不可抗拒力量，wheel 也经常会莫名其妙失败。

## 现有的解决方案

一直以来，出现过 `pipx`，`pipenv`， `conda`，`poetry` 以及我最近接触的 `pdm`。他们都在某种程度上解决了 Python 的问题，这篇文章：

[How to improve Python packaging, or why fourteen tools are at least twelve too many](https://chriswarrick.com/blog/2023/01/15/how-to-improve-python-packaging)

对比了各种工具的利弊。最后得出结论是 poetry 和 pdm 是目前最合适的工具。而 pdm 是目前唯一支持 [PEP 582](https://peps.python.org/pep-0582/) 的依赖管理工具。

### 什么是 PEP 582

> This PEP proposes to add to Python a mechanism to automatically recognize a `__pypackages__` directory and prefer importing packages installed in this location over user or global site-packages. This will avoid the steps to create, activate or deactivate “virtual environments”. Python will use the `__pypackages__` from the base directory of the script when present.

这个 PEP 的目的就是基于一个文件夹 `__pypackages__ `来管理 Python 的依赖，类似 nodejs 的`node_modules`，用户不需要再创建虚拟环境来隔离依赖包。Python 会自动识别和安装依赖。

### PDM

PDM 实现了 PEP 582！这让我们在解决 Python 依赖问题时不用再考虑虚拟环境。

#### 初始化项目

```shell
pdm init
```

之后 PDM 会问几个问题，记得选择**不使用虚拟机环境**，这样 PDM 就会默认使用 PEP 582 的解决方案，在项目下生成一个类似 NodeJS 的 `__pypackages__`。

剩下的操作就跟 NodeJS 的 npm 非常像了。

添加一个依赖之后，PDM 会自动更新`pyproject.toml`文件。

```shell
pdm add requests
```

#### 安装项目依赖

```shell
pdm install
```

#### 启动项目

先在 `pyproject.toml`里添加

```shell
[tool.pdm.scripts]
start = "flask run -p 54321"
```

然后执行

```shell
pdm run start
```

#### 打包部署

```shell
pdm build
pdm publish
```

## 总结

如果你从事科研工作，用 `conda`。

如果你从事工程项目，`poetry`是目前业内用的最多的方案，大多数情况下它是个不错的依赖管理工具。但是如果你不喜欢 Python 的 virtualenv，`pdm`是更好的选择。
