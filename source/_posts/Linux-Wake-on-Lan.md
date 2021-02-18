---
title: Linux Wake on Lan
toc: true
date: 2020-04-04 22:08:59
categories: GEEK
updated: 2020-04-09 18:02:44tags: [Linux, GEEK]
description:
---

# Wake on Lan 原理

局域网唤醒（“ WOL”）使用称为魔术包的特殊设计的帧实现，该帧发送到网络中的所有计算机，其中包括要唤醒的计算机。魔术包包含目标计算机的MAC地址，每个网卡内置的标识号（“ NIC”）或计算机中的其他以太网设备，使其能够在网络上被唯一识别和寻址。局域网唤醒功能需要计算机包含能够在系统关闭电源时以低功耗模式“侦听”传入数据包的网络设备。如果收到指向设备 MAC 地址的魔术包，则 NIC 会以与按电源按钮相同的方式向计算机的电源或主板发出信号，以启动系统唤醒。

魔术包在[数据链路层](https://en.wikipedia.org/wiki/Data_link_layer)（[OSI 模型](https://en.wikipedia.org/wiki/OSI_model)中的第 2 层）上发送，并在发送时使用网络[广播地址](https://en.wikipedia.org/wiki/Broadcast_address)广播到给定网络上的所有连接的设备；IP地址（OSI 模型中的第 3 层）未使用。

由于局域网唤醒是基于广播技术构建的，因此它通常只能在当前网络子网中使用。但是，也有一些例外情况，只要适当的配置和硬件（包括跨 Internet 的远程唤醒），局域网唤醒实际上就可以在任何网络上运行。

为了使局域网唤醒工作，部分网络接口需要保持打开状态。这消耗了少量的待机功率，远低于正常工作功率。通常将链路速度降低到可能的最低速度，以免浪费功率（例如，千兆以太网 NIC 仅保持10 Mbit / s的链路）。在不需要时禁用LAN唤醒可以非常轻微地减少已关闭但仍插入电源插座的计算机的功耗。

## Magic Packet

Magic Packet 是一个广播帧（frame），透过端口 7 或端口 ***9*** 进行发送，且可以用无连接（Connectionless protocol）的通讯协议（如UDP、IPX）来传递，不过一般而言多是用 UDP。

Magic Packet 首先是连续 6 个字节的 “FF”（十六进制），其次是目标计算机的 48 位 MAC 地址的 16 次重复（有时还会带出 4 字节或 6 字节的密码），总共102个字节。

# 注意事项

1. 局域网被唤醒的IP地址是广播地址：192.168.x.255，端口为 9，路由器收到后通过广播，数据包一定可以发送该局域网内待唤醒的这台机器；

2. 公网唤醒我们无办法填写具体的内网地址，只能配置路由器的公网 IP，然后通过数据转发到具体的电脑 IP 地址，由于不是广播地址，也由于路由器 ARP 映射表在电脑关机后一定时间会丢失，所以路由器没有办法知道哪个 IP 是MAC所对应那台机器，所以魔术包被丢弃，所以要么增加 ARP 绑定，要么添加端口转发规则到广播地址 (192.168.x.255 和 端口 9)。

   > [广播地址](https://en.wikipedia.org/wiki/Broadcast_address)计算方法:
   >
   > `<IP>` | (~ `<net mask>`)
   >
   > 如：`192.168.0.11` | (~ `255.255.255.0`) = `192.168.0.255`

<!--more-->



> 启动者(电脑A) -----------> 被远程开启的电脑(电脑B)

# 被远程开启的电脑(电脑B) 设置

1. 在主板 BIOS 中将 *Wake On Land / Wake On PCI(E)* 设为 Enable；

2. 在 Linux 系统中安装 ethtool：

   ~~~bash
   sudo apt-get install ethtool
   ~~~

3. 查看 WOL 是否打开：

   ~~~bash
   sudo ethtool <网卡名称>
   ~~~

   例如：

   ~~~bash
   sudo ethtool eno1
   ~~~

   如果没有发现 *Wake-on: g*，说明网络唤醒没打开

4. 打开 WOL：

   ~~~bash
   sudo ethtool -s <网卡名称> wol g
   ~~~

   例如：

   ~~~bash
   sudo ethtool -s eno1 wol g
   ~~~

   然后再用 `sudo ethtool <网卡名称>` 查看 WOL 是否打开，看到 *Wake-on: g*，说明 WOL 已经打开了。

# 启动者(电脑A) 设置

这里只说 A 电脑也是 Linux 的情况，因为其他平台上的 WOL 软件很多，Android、Mac、路由器上都有。

1. 安装 wakeonlan：

   ~~~bash
   sudo apt-get install wakeonlan
   ~~~

2. 启动 B 电脑：

   ~~~bash
   wakeonlan < B 电脑配好 WOL 的网卡的 MAC 地址>
   ~~~

   例如：

   ~~~bash
   wakeonlan 4c:cc:6a:f5:ab:84
   ~~~



> Reference: 
>
> https://en.wikipedia.org/wiki/Wake-on-LAN
>
> https://zhuanlan.zhihu.com/p/29100480