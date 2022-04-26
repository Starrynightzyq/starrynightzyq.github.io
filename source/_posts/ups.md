---
title: QNAP NAS 添加 ups 后推送关机通知到其他设备
categories: NAS
tags:
  - GEEK
  - NAS
description: 为了防止硬盘受到停电影响而挂掉，为家里的威联通 nas 配备了ups，同时设置为网络 ups，以通知其他设备关机
toc: true
comments: true
date: 2022-02-25 12:49:49
updated: 2022-02-25 14:40:49
---

# QNAP 设置

将 UPS 通过 USB 线连接到 QNAP，设置如图所示：

![qnap-ups](https://pic.zhouyuqian.com/img/202202251256160.png)

# PVE 设置

1. 打开 PVE 的 shell，安装 NUT 客户端：

   ~~~bash
   apt-get install nut -y
   ~~~

2. 配置 NUT 客户端：

   配置 `nut.conf` 文件：

   ~~~bash
   vim /etc/nut/nut.conf
   ~~~

   移动光标找到 `MODE` 参数项，将 `MODE=` 后面修改成如下参数：

   ~~~json
   MODE=netclient
   ~~~

   配置 `upsmon.conf` 文件：

   ~~~bash
   vim /etc/nut/upsmon.conf
   ~~~

   找到 `MONITOR` 在下方增加一行：

   ~~~json
   MONITOR qnapups@<NAS IP> 1 admin 123456 slave
   ~~~

   > 这里坑出现了，大部分 ups 的服务器以 ups 开头（包括群晖），然而 qnap 不是，他是以 **qnapups** 开头。。。。😑
   >
   > 用户名为 `admin`，密码默认为 `123456`

3. 启动nut-client服务，并设置自动启动

   ~~~bash
   systemctl restart nut-client && systemctl enable nut-client
   ~~~

4. 测试是否成功连接UPS服务器

   ~~~bash
   $ upsc qnapups@192.168.12.10
   Init SSL without certificate database
   battery.charge: 79
   battery.charge.low: 20
   battery.runtime: 1801
   battery.type: PbAc
   device.mfr: EATON
   device.model: SANTAK TG-BOX 850
   device.serial: Blank
   device.type: ups
   driver.name: usbhid-ups
   driver.parameter.pollfreq: 30
   driver.parameter.pollinterval: 2
   driver.parameter.port: /dev/ttyS1
   driver.parameter.synchronous: no
   driver.version: 2.7.4
   driver.version.data: MGE HID 1.39
   driver.version.internal: 0.41
   input.transfer.high: 264
   input.transfer.low: 184
   outlet.1.desc: PowerShare Outlet 1
   outlet.1.id: 1
   outlet.1.status: on
   outlet.1.switchable: no
   outlet.desc: Main Outlet
   outlet.id: 0
   outlet.switchable: yes
   output.frequency.nominal: 50
   output.voltage: 230.0
   output.voltage.nominal: 220
   ups.beeper.status: enabled
   ups.delay.shutdown: 20
   ups.delay.start: 30
   ups.firmware: 02.08.0010
   ups.load: 13
   ups.mfr: EATON
   ups.model: SANTAK TG-BOX 850
   ups.power.nominal: 850
   ups.productid: ffff
   ups.serial: Blank
   ups.status: OL
   ups.timer.shutdown: 0
   ups.timer.start: 0
   ups.type: offline / line interactive
   ups.vendorid: 0463
   ~~~

   or

   ~~~bash
   $ systemctl status nut-client
   ...
   ... Started Network UPS Tools - power device monitor and shutdown controller.
   ...
   ~~~



# Reference

1. https://www.purefish.cc/pve-synology-ups.html
2. https://blog.cyida.com/posts/ZEK5W9/
3. https://www.lxg2016.com/54516.html
4. **https://post.smzdm.com/p/av7o5r9n/**
5. **[https://blog.pengandfan.com/2021/09/10/qnap-nas添加ups后推送关机通知到其他设备](https://blog.pengandfan.com/2021/09/10/qnap-nas%E6%B7%BB%E5%8A%A0ups%E5%90%8E%E6%8E%A8%E9%80%81%E5%85%B3%E6%9C%BA%E9%80%9A%E7%9F%A5%E5%88%B0%E5%85%B6%E4%BB%96%E8%AE%BE%E5%A4%87/)**

