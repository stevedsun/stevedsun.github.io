---
title: "为 Mac OS 10.15 开启 HiDPI，让 2K 显示器更舒适"
date: 2019-11-24T16:11:00+08:00
description: "本文教你强行开启 macbook 的 HiDPI 设置"
categories: [Efficiency]
tags: [Mac]
aliases: [/posts/MacBook-hidpi/]
---

以前手抖买了台 Dell P2416D 显示器，接上 Macbook 发现原生的分辨率设置在 2K 显示器上字体很小，换成 1080P 分辨率显示效果又特别模糊。上网查了一下发现可以为 Macbook 强行开启 HiDPI。下文的教程结合了 Github 上用户[ZeRo° Xu](https://github.com/xzhih) 在 [一键开启 HiDPI 脚本](https://github.com/xzhih/one-key-hidpi) 里的 [Github Issue](https://github.com/syscl/Enable-HiDPI-OSX/issues/49) 和一篇博文 [《为 mac 连接的 2k 显示器开启 HiDPI》](https://www.smslit.top/2019/01/02/mac_hidpi/)。

## 什么是 HiDPI

引用自 Github 用户 [ZeRo° Xu](https://github.com/xzhih) ：

> 它使用横纵 2 个物理像素也就是 4 个物理像素来显示 1 个像素区域，结果就是图像的细节得到翻倍、更清晰、边缘更平滑。
>
> 拿 13 寸的 MacBook Pro 举例，它的屏幕物理分辨率是 2560 x 1600，所以原生的 HIDPI 分辨率就是 1280x800。更高的一档 1440x900 hidpi 缩放分辨率，则是虚拟出一个 2880x1800 的分辨率，再进行软缩放输入。所以你能发现苹果的电脑总是有很高的分辨率。
>
> 好了，既然你的屏幕是 1080p，本身就没有那么多像素去合成 HIDPI，如果以原生的显示计算，你这屏幕的 1080p 分辨率应该是 960x540，这么低的分辨率你是没法用的，所以就有了这个脚本。
>
> 这个脚本的功能是虚拟出比你的屏幕物理分辨率更高的假分辨率，也就是你看到的 3360 x 1888，这样你就可以使用 1680 x 944 hidpi 这个缩放分辨率了。
>
> 如果你要开启 1080p 的 HIDPI 分辨率，就虚拟一个 3840 x 2160 的假分辨率，然后 MacOS 会使用 4 个像素来显示 1 个像素区域，也就是和你物理分辨率一样的 1080p 分辨率，开不开启看起来没任何区别，最大的效果就是显卡压力增大系统变卡、截图可以得到高分辨率图像。

## 自动配置 HiDPI

上文 [链接](https://github.com/xzhih/one-key-hidpi) 里提到一键配置脚本，你不妨先按照脚本的步骤开启 HiDPI 试试。但是脚本并没有适配所有显示器的情况（至少我的 Dell P2416D 使用后无效），所以就有了下面的步骤。

## 手动配置 HiDPI

本教程测试环境：

- 笔记本：MacBook Pro (Retina, 15-inch, Mid 2015)
- 显示器：Dell P2416D
- 操作系统：MacOS Catalina (Version 10.15.1)

### 0. 安装 RDM

相信很多人已经装过这个工具了，它是用来修改显示分辨率的，如果没装，请在[RDM 下载页面](https://avi.alkalay.net/software/RDM/)安装它。

### 1. 关闭 Mac 的 SIP

SIP 是苹果公司为防止你胡乱篡改系统文件用的保护机制，请先按照下面步骤把它关闭，以便后续操作：

1. 关机（最好先手机拍个照把这 4 步记录下来）
2. 按`command（⌘）+ R`+电源键开机，自动进入恢复模式
3. 选择上边菜单栏的`实用工具`中的`终端`
4. 输入命令`csrutil disable`

最后终端显示 「Successfully……」 等一大堆文字就说明你成功了。你可以输入`reboot`重启。等下文的全部设置都完成后，你如果想恢复 SIP，就重复步骤 1 到 3，在第 4 步输入`csrutil enable`就好了。

### 2. 开启 macOS 的 HiDPI 选项

再次重启后进入系统，打开终端输入

```
sudo defaults write /Library/Preferences/com.apple.windowserver.plist DisplayResolutionEnabled -bool true
```

### 3. 查询你的外接显示器的编号

这一步相当重要，先介绍两个命令

```
ioreg -l | grep "DisplayVendorID"
ioreg -l | grep "DisplayProductID"
```

这两条命令用来查询你的显示器供应商 ID `DisplayVendorID` 和产品 ID `DisplayProductID`。接下来你要找到你的显示器对应的`DisplayVendorID`和`DisplayProductID`：

1. 拔掉显示器的 HDMI 或者 DP 线
2. 分别输入上面两个命令之后`return(↩)`，每个命令会返回一个带有数字的结果。那个数字就是 macbook 默认的`DisplayVendorID`和`DisplayProductID`了
3. 接入显示器
4. 再分别输入那两个命令，每个命令会分别返回两条带有数字的结果。对比刚才 macbook 默认的结果，另一个数字就是你显示器的`DisplayVendorID`和`DisplayProductID`了
5. 把这两个数字分别转成对应的 16 进制数，用这个[进制转换工具](https://tool.oschina.net/hexconvert)

现在，回到桌面，新建一个文件夹命名为`DisplayVendorID-[你刚才查到的DisplayVendorID的16进制数]`，例如`DisplayVendorID-10ac`。

之后在这个刚建好的文件夹下增加一个文件，命名为`DisplayProductID-[你刚才查到的DisplayProductID的16进制数]`，例如`DisplayProductID-a0c3`。

### 4. 为你的显示器生成 plist 文件

到 [这个网站](https://comsysto.github.io/Display-Override-PropertyList-File-Parser-and-Generator-with-HiDPI-Support-For-Scaled-Resolutions/) ，在左侧的空里分别输入显示器型号，DisplayProductID 和 DisplayVendorID，注意填 16 进制的数字，并且检查下后边 10 进制的数字是不是和你刚才命令查到的一致。如果需要添加自己额外的分辨率，直接在下边新建一条分辨率配置就行。最后，复制右边生成 XML 格式文本，粘贴到刚才新建的文件里。（也可以直接从网站下载文件，去掉文件名后缀 `.plist` ）

<img src="https://tva1.sinaimg.cn/large/006y8mN6ly1g9bg60hippj30nm0rqwha.jpg" alt="显示器配置" style="zoom:50%;" />

XML 文件类似下边这样：

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>DisplayProductID</key>
    <integer>41156</integer>
    <key>DisplayVendorID</key>
    <integer>4268</integer>
    <key>scale-resolutions</key>
    <array>
        <data>AAAKAAAABaAAAAABACAAAA==</data>
        <data>AAAFAAAAAtAAAAABACAAAA==</data>
        <data>AAAPAAAACHAAAAABACAAAA==</data>
        <data>AAAHgAAABDgAAAABACAAAA==</data>
        <data>AAAMgAAABwgAAAABACAAAA==</data>
        <data>AAAGQAAAA4QAAAABACAAAA==</data>
        <data>AAAKAgAABaAAAAABACAAAA==</data>
        <data>AAAKrAAABgAAAAABACAAAA==</data>
        <data>AAAFVgAAAwAAAAABACAAAA==</data>
    </array>
</dict>
</plist>
```

### 4. 复制 plist 配置文件到系统配置目录

这一步就是把刚才新建的配置文件复制到你系统目录里，你直接复制通常会提示你系统目录是「只读」的，不允许你胡作非为。所以你先要在终端执行下面的命令：

```shell
sudo mount -uw /
```

这样，你就可以复制到系统的文件夹了。（这个命令重启后失效）

接下来打开系统文件夹`/System/Library/Displays/Contents/Resources/Overrides/`，你会发现一大堆跟你刚才文件夹命名相似的目录。把你新建的文件夹丢进去，和它们混在一起，假装它原来就是其中一员。重启。

### 5. 修改分辨率

重启之后又进入系统，首先打开 RDM，你会在菜单栏看见它：

<img src="https://tva1.sinaimg.cn/large/006y8mN6gy1g995pjfs3aj30io0h4gz1.jpg" alt="rdm-shot" style="zoom:50%;" />

Main Display 和 Display 2 就分别是你的外接显示器和 macbook 的显示器分辨率设置（位置有可能对掉，自己尝试一下）。带有 ⚡️ 符号的分辨率设置项就是开启 HiDPI 后新增出来的。如果你像我一样是 2K 显示器，可以给显示器选择`1920x1080⚡️`那个配置。是不是比原生分辨率的 UI 和字体更大更清晰了。

## 小结

本文教你强行开启 macbook 的 HiDPI 设置，并针对 2K 显示器新增了配置文件到系统配置目录里，最后用 RDM 自由设置适合你显示器的分辨率。至于 HiDPI 的原理，请自行搜索，此处不再赘述。

希望本文对你有帮助，也欢迎你留言反馈。
