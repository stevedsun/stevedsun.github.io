---
title: "遇到 Linux 系统 Kernel Panic 了该如何应对"
date: 2025-07-19T01:06:32+08:00
categories: [随笔]
tags: [Linux]
aliases: [/posts/retro-kernel-panic/]
description: ""
---

晚上打开家里的零刻 Ser6 主机，赫然发现 Kernel Panic 了 😱。

![](https://fastly.jsdelivr.net/gh/stevedsun/blog-img/kernel-panic-screenshot.png)

这时候很多人就慌了，其实完全不必慌。只需要用一个 LiveUSB 启动盘修复一下。

不过我这个 Ubuntu 安装了一年多，一直很稳定，家里也没预备 LiveUSB，无奈只能掏出吃灰好几年的旧电脑，开机密码猜了半个多小时才进入系统……下载 Ubuntu ISO 文件，制作 LiveUSB。

下面是从 LiveUSB 启动后进入 Try Ubuntu，用 Terminal 排错的过程，供大家参考。

## 1. 找到根分区和 EFI 分区

```bash
lsblk -f
```

会返回类似如下结果，其中`vfat`格式是efi分区，`ext4`是系统根分区。

```
NAME        FSTYPE   LABEL  UUID                                 MOUNTPOINT
nvme0n1                                                          
├─nvme0n1p1 vfat           1234-5678                            /boot/efi
└─nvme0n1p2 ext4           955b06a9-983d-4e04-b2ef-60b559db46e6 
```

## 2. 用`fsck`修复分区错误

注意这一步及之后的步骤，分区的路径要用上一步你的系统中的分区路径。

先修复根分区：

```bash
sudo fsck -f /dev/nvme0n1p2
```

出现提示输入`y`允许，或者`a`全部允许。这一步我发现了一些错误并成功修复了。

接下来检查修复efi分区：

```bash
sudo fsck -f /dev/nvme0n1p1
```

我在这一步出现提示：

```
there are different between boot sector and it's backup：
1) Copy original to backup
2) Copy backup to original
3) No action
```

根据网上搜索到的结果，如果系统能正常进入grub，说明我原始扇区是好的，所以我选择 `1) Copy original to backup` 复制原始引导扇区到备份扇区。

## 3. 挂载原系统并重建 initramfs

下面这一步，要把原系统根分区挂载到当前 LiveUSB 系统里，同时为了执行必要的命令，要把 LiveUSB 系统的四个关键目录挂到原系统。

```bash
sudo mkdir -p /mnt/ubuntu
sudo mount /dev/nvme0n1p2 /mnt/ubuntu


sudo mount --bind /dev /mnt/ubuntu/dev
sudo mount --bind /proc /mnt/ubuntu/proc
sudo mount --bind /sys /mnt/ubuntu/sys
sudo mount --bind /run /mnt/ubuntu/run

sudo mount /dev/nvme0n1p1 /mnt/ubuntu/boot/efi
```

一顿操作后，就可以切换到原系统 root shell 了。

```bash
sudo chroot /mnt/ubuntu
```

然后是安装 grub 并重新为系统内核生成 initramfs 启动镜像。`grub-install`命令的参数要根据自己的系统设置。

```bash
grub-install --target=x86_64-efi --efi-directory=/boot/efi --bootloader-id=ubuntu
update-initramfs -c -k all
update-grub
```

最后，退出原系统 root shell，重启。

```bash
exit

sudo reboot
```

拔掉U盘进入原系统，我这时就可以正常登录了。

## 总结

1. 不要慌

2. 家中常备 Live USB

3. 用 `fsck` 命令修复分区错误

4. 用`mount`挂载原系统必要文件，进入原系统并重建 initramfs
