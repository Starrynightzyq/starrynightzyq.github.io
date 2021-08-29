---
title: Proxmox VE 安装
toc: true
comments: true
date: 2021-08-28 00:38:20
updated: 2021-08-28 00:38:20
categories: Geek
tags: [Geek, PVE]
description:
---

# What's Proxmox VE

**Proxmox Virtual Environment** is an open source server virtualization management solution based on QEMU/KVM and LXC. You can manage virtual machines, containers, highly available clusters, storage and networks with an integrated, easy-to-use web interface or via CLI. Proxmox VE code is licensed under the GNU Affero General Public License, version 3. The project is developed and maintained by [Proxmox Server Solutions GmbH](https://www.proxmox.com/).

<!--more-->

# 安装

> Ref:
>
> https://zhuanlan.zhihu.com/p/62084071
>
> https://einverne.github.io/post/2020/03/proxmox-install-and-setup.html

# 安装 win10

> Ref:
>
> https://zhuanlan.zhihu.com/p/62492187

## 显卡直通

> Ref：[PVE下安装Windows10并直通核显、键盘鼠标、声卡等设备详细步骤](https://www.simaek.com/archives/69/)

# 安装 linux

> Ref:
>
> https://post.smzdm.com/p/a78egn7o/
>
> [server](p3terx.com/archives/docker-aria2-pro.html)

## ubuntu--vg-ubuntu--lv 磁盘扩容

> Ref: https://serverfault.com/questions/953174/how-do-i-expand-the-roots-volume-size

First, you can use `lvextend` to extend the size of the logical volume, to fill up the remaining space:

```
sudo lvextend --extents +100%FREE /dev/mapper/ubuntu--vg-ubuntu--lv
```

Now, you can resize the filesystem in that logical volume.

```
sudo resize2fs /dev/mapper/ubuntu--vg-ubuntu--lv
```

Finally, you can see the end result:

```
sudo df -h /
```

## 安装qemu-guest-agent

- 参考https://pve.proxmox.com/wiki/Qemu-guest-agent
- https://foxi.buduanwang.vip/virtualization/pve/530.html/

```bash
apt-get install qemu-guest-agent
apt-get install spice-vdagent
```

然后打开 “数据中心->pve->VMname->选项->QEMU Guest Agent”

# 安装 openmediavault

> Ref:
>
> https://www.d3tt.com/view/239

## omv 磁盘丢失

OMV 断电后，没有卸载文档，直接将磁盘从omv硬盘接口取下，重启后提示 磁盘丢失。

> Ref: https://www.jianshu.com/p/5a78668b0670

## **omv-extras**

> Ref: https://zhuanlan.zhihu.com/p/357495418

## omv decker

> Ref: https://zhuanlan.zhihu.com/p/360126067

# pve删除lvm扩容步骤

> Ref: 
>
> https://www.jianshu.com/p/bdb83531c56d
>
> https://wp.gxnas.com/10402.html

# 防火墙

> Ref:
>
> https://www.pianshen.com/article/72122018797/
>
> https://foxi.buduanwang.vip/virtualization/pve/508.html/

# SPICE远程连接

> Ref:
>
> https://i.opat.vip/738.html

# Proxmox VE直通硬盘（全盘映射方式）

> Ref:
>
> https://wangxingcs.com/2020/0227/1411/
