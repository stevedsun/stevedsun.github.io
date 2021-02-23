---
title: "macbook安装ubuntu"
date: 2013-01-04T00:00:00
tags: [Mac,Linux]
description: ""
---

__注意，ubuntu和xubuntu安装上有一定差别，请严格按照你选择的系统版本流程安装__

### ubuntu
### 准备工作
##### 分区
这一步可以用命令行实现，也可以在mac下直接用磁盘工具分区，初学者建议后者。有经验的朋友可以在网上查询diskutils的用法，这是mac提供的分区工具

使用磁盘工具，打开左侧最上边磁盘位置（不是macosx，而是整个硬盘）的选项，右边会出现`分区`标签。选择分区，你可以用鼠标拖动轻松将macos的一部分划分给ubuntu使用。分区格式可以选择mac日志文件。其实选什么都一样，等会还要重新格式化。

#### 把iso镜像转化为苹果电脑识别的img镜像

    hdiutil convert /path/to/ubuntu.iso -format UDRW -o /path/to/target.img

命令中`path/to/ubuntu.iso`是你下载的iso路径，`path/to/target.img`自然是你要保存成img的路径

#### 插入U盘，刻录镜像
先运行如下命令查询你U盘的设备名

    diskutil list

这里假设U盘是disk1，执行

    diskutil unmountDisk /dev/disk1

接下来执行命令刻录，

    sudo dd if=/path/to/downloaded.img of=/dev/disk1 bs=1m

ubuntu官网针对上一条命令可能出现的两种错误提示给出了解决办法：

1. If you see the error dd: Invalid number '1m', you are using GNU dd. Use the same command but replace bs=1m with bs=1M.

2. If you see the error dd: /dev/disk1: Resource busy, make sure the disk is not in use. Start the 'Disk Utility.app' and unmount (don't eject) the drive.

好了，刻完就可以重启安装了。重启后按住`option`会看到一个refit命名的移动设备图标，点进去就开始安装了。

#### 安装过程
安装过程可以参考网上其他人的帖子。一般有两种方式

1. 选择`ubuntu和mac os x共存`，系统会自动被安装到空闲分区。
2. 选择`其他选项`，可以自己手动分区，我一般是选这个来手动分区。

假设你选了`其他选项`就会进入分区的窗口，这时你就会看到所有磁盘分区的情况，刚才在mac下给ubuntu预先分好一块空闲分区也在其中，名字可能叫disk02，或者disk03什么的。
接下来要进行四次分区。这一段分区方法参考了百度经验上一个网友的教程，我进行了2处修改，原帖地址<http://jingyan.baidu.com/article/60ccbceb18624464cab197ea.html>

第一次分区：

    点你刚才留出来的“空闲”分区，点“+”，进行如下设置：
    挂载点：“/”
    大小：22000MB
    新分区的类型：主分区
    新分区的位置：空间起始位置
    用于：EXT4日志文件系统

第二次分区：

    “空闲”处，继续点“+”，如下设置，
    挂载点：（不设置）
    大小：4096MB
    新分区的类型：逻辑分区
    新分区的位置：空间起始位置
    用于：交换空间

第三次分区：

    “空闲”处，继续点“+”，如下设置，
    挂载点：/boot
    大小：200MB
    新分区的类型：逻辑分区
    新分区的位置：空间起始位置
    用于：EXT4日志文件系统

第四次分区：

    “空闲”处，继续点“+”，如下设置，
    挂载点：/home
    大小：（剩余全部空间，剩下显示多少，就多少）
    新分区的类型：逻辑分区
    新分区的位置：空间起始位置
    用于：EXT4日志文件系统

分区设置完毕后，下方还有一项“安装启动引导器的设备”，macbookpro用户需要选择/boot这个分区所在磁盘位置。

### 开机引导程序rEFIT
安装完ubuntu，重启在mac下下载安装rEFIt。安装好后在终端里输入`/efi/refit/. enable-always.sh`启动rEFIt。重启，你就会看到ubuntu的选项。



### Xubuntu(估计Lubuntu和Kubuntu也应该适用，仅是猜想。)
### 准备工作
#### 如何刻录镜像到移动设备
这个问题很重要，如果你下载了iso格式的Xubuntu系统镜像，
你需要将该镜像不经过任何转换的完整刻录到移动设备或光盘上
（我使用的是unetbootin 这个软件，开源，跨平台，操作简便）。
注意，绝对不可以将iso格式转换成img（mac镜像）后刻录。
这样会导致ubuntu部分版本无法安装grub引导器。

#### 开机引导程序rEFIt
安装完的系统无法被mac直接引导，所以需要安装rEFIt引导。如果不想要安装它，
可以参考下边附录1里的安装方法。重新修改引导文件。

#### 安装过程

1. 在官网下载xubuntu镜像，使用uneetbootin刻录到设备
 上(mac版的unetbootin貌似刻录iso有问题，可以在windows上下载该软件使用)。
2. 重启，开机界面按住`option`键，有个windows命名的移动设备图标，选中进入。
3. 安装过程不敷述, 装后重启
4. 从mac进入，安装rEFIt，在shell里运行`/efi/refit/. enable-always.sh`启动rEFIt
5. 重启，出现两个图标，苹果代表mac，企鹅代表linux。至此，完成安装过程。


## ubuntu或Xubuntu安装后的一些配置
打开系统配置文件，

    sudo gedit /etc/rc.local

在exit 0 前边加入下边对应的语句,
默认关闭功能键Fn:

    echo 2 > /sys/module/hid_apple/parameters/fnmode

设置默认亮度(数字2565可以修改任意亮度)（xubuntu下不起作用，原因未知）

    echo  2565 > /sys/class/backlight/intel_backlight/brightness

设置键盘灯亮度（数字1代表亮度):

    echo 1 > /sys/class/leds/smc::kbd_backlight/brightness

### 附录1
<https://help.ubuntu.com/community/MacBookPro11-1/Saucy>

