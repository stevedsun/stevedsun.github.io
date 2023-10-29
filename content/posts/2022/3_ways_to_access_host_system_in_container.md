---
title: "3 Ways to Access Host System in a Docker Container"
date: 2022-08-08T20:04:00+08:00
categories: [Kubernetes]
tags: [docker]
aliases: [/posts/3_ways_to_access_host_system_in_container/]
---

When we are using Docker, we always access the host system by mounting the host folders as a volume. But sometimes we can not do that due to deployment reasons or security limits.

There are three workaround ways to access the host system.

## 1. Mount `docker.socks` into container

`docker.socks` is a Unix socket that Docker Engine API listens on. You can mount `/var/run/docker.socks` file to your container and call Docker Engine API through this socket.

For instance, If I want to get docker information by calling that API:

```bash
curl -s --unix-socket /var/run/docker.sock http://localhost/info
```

You can refer to [Docker Engine API](https://docs.docker.com/engine/api/v1.41/) to find more useful details.

## 2. Using PID mode `host`

By default, Docker uses the Linux PID namespace to isolate containers' filesystem view. It means if two processes have the same PID, they will share the filesystem permission.

Docker has a startup parameter `--pid=host` to change the PID namespace to its host process's namespace. You can use this parameter to make your docker container have the same privilege as the host process.

> When using `--pid=host`, you can list host system's processes by `ps -ef`.

## 3. By `docker --privileged`

It is the last way you can access the host system, but it is not recommended for most cases.
