---
title: "Research on Python Dependency Management Tools"
slug: "python-packaging"
date: 2023-01-19T08:05:27+08:00
categories: [Python]
tags: [python]
aliases: [/posts/python-packaging/]
---
## TL;DR

If you're working on an engineering project, [poetry](https://python-poetry.org/) is currently the best solution. But if you don't like Python's virtualenv, give [pdm](https://pdm.fming.dev/latest/) a try.

## The Mess That Is Python

Python's dependency management tool, `pip`, has long been a target of complaints from developers. From my perspective, `pip` has three fatal flaws:

- It cannot solve the issue of Python dependency environment isolation
- The dependency file `requirements.txt` is not truly plug-and-play
- Packaging and deployment are very cumbersome, requiring manual configuration

### The Environment Isolation Problem

Python's dependency libraries can be installed either globally on the system or in the user directory (`/home/${USER}/.local`). But if you're managing multiple Python projects at the same time, you need to split each project's dependencies into separate folders.

The traditional approach is to use virtualenv to create isolated Python binaries and a project-specific virtual environment for dependencies (a "virtual environment" isn't a virtual machine—it's a command environment bound to a terminal session). The downsides of this approach are:

- Developers constantly have to ask themselves, "Which project directory am I in? Do I need to switch into this virtual environment?"
- virtualenv only solves environment isolation; it doesn't synchronize dependency file updates or handle packaging and publishing.

### The Dependency Installation Problem

Python's earliest way of managing dependencies was to manually run `pip install xxx` to install them, and then `pip freeze` to export the dependency list to a `requirements.txt` file. But this text file is quite confusing.

- Unlike Node.js, there's no easy way to upgrade or downgrade a dependency version and have it automatically sync to the text file.
- It flatly lists all first- and second-level dependencies (i.e., the dependencies of dependencies). Because some Python packages depend on the C libraries installed on the system, running `pip install -r requirements.txt` on different systems can produce inconsistent results, often with errors.

### The Packaging and Deployment Problem

Python generally uses `wheel` to package binaries. It only solves the packaging problem; the environment dependencies are handled by pip and setuptools, so even when using wheel, you still have to worry about environment isolation and dependency management.

Additionally, due to compatibility issues between Python versions and the uncontrollable forces of low-level implementation, wheel builds can fail inexplicably.

## Existing Solutions

Over time, a number of tools have appeared: `pipx`, `pipenv`, `conda`, `poetry`, and the more recent `pdm` I've come across. They all address Python's pain points to some degree. This article:

[How to improve Python packaging, or why fourteen tools are at least twelve too many](https://chriswarrick.com/blog/2023/01/15/how-to-improve-python-packaging)

compares the pros and cons of various tools. The conclusion is that poetry and pdm are the most appropriate tools at present. And pdm is currently the only dependency management tool that supports [PEP 582](https://peps.python.org/pep-0582/).

### What Is PEP 582

> This PEP proposes to add to Python a mechanism to automatically recognize a `__pypackages__` directory and prefer importing packages installed in this location over user or global site-packages. This will avoid the steps to create, activate or deactivate "virtual environments". Python will use the `__pypackages__` from the base directory of the script when present.

The purpose of this PEP is to manage Python dependencies in a single `__pypackages__` folder, similar to `node_modules` in Node.js. Users no longer need to create virtual environments to isolate dependency packages. Python will automatically recognize and install dependencies.

> Updated July 2, 2023: The PEP 582 proposal has been rejected. PDM still supports it for now, but it's not recommended for developers to use this feature.

### PDM

PDM implements PEP 582! This means we no longer have to think about virtual environments when solving Python dependency issues.

#### Initialize a Project

```shell
pdm init
```

PDM will then ask a few questions. Be sure to choose **not to use a virtual environment**, so PDM uses the PEP 582 solution by default, generating a `__pypackages__` folder in the project similar to Node.js's `node_modules`.

The rest of the operations are very similar to Node.js's npm.

After adding a dependency, PDM will automatically update the `pyproject.toml` file.

```shell
pdm add requests
```

#### Install Project Dependencies

```shell
pdm install
```

#### Run the Project

First, add the following to `pyproject.toml`:

```shell
[tool.pdm.scripts]
start = "flask run -p 54321"
```

Then run:

```shell
pdm run start
```

#### Build and Publish

```shell
pdm build
pdm publish
```

## Summary

If you're doing scientific research, use `conda`.

If you're working on an engineering project, `poetry` is currently the most widely adopted solution in the industry and is usually a solid dependency management tool. But if you don't like Python's virtualenv, `pdm` is the better choice.
