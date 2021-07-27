---
title: RISC-V SOC Design (1)
toc: true
date: 2020-03-27 21:39:24
categories: RISC-V
updated: 2020-03-27 22:28:32
tags: [RISC-V, FPGA, 毕业设计]
description:
---

使用 vivado blockdesign 搭建，比较直观

![ibex_bd](https://pic.zhouyuqian.com/img/20210727194616.png)

<!--more-->

# Memory Map

SOC 搭建参考了 SiFive SOC，因此在 Memory Map 上尽量一致，方便软件移植。

| Base        | Top         | Attr. | Description | Notes                   |
| ----------- | ----------- | ----- | ----------- | ----------------------- |
| 0x1001_2000 | 0x1001_2FFF | RW  A | GPIO        | On-Chip Peripherals     |
| 0x1001_3000 | 0x1001_3FFF | RW  A | UART 0      | On-Chip Peripherals     |
| 0x8000_0000 | 0x8000_FFFF | RWXCA | ITCM        | On-Chip Volatile Memory |
| 0x9000_0000 | 0x9000_FFFF | RWXCA | DTCM        | On-Chip Volatile Memory |

# 设计思路

## ITCM

一般盘片机在启动时，会将 instruction 从 FLASH 读入片上 RAM，然后程序在片上 RAM 中运行，因此启动时会有一个程序加载的过程，即从片外存储 load 到片上存储，因此这里暂时先用 ITCM 模拟这个过程，启动时，将程序从 ITCM load 到 DTCM 中，这个过程需要程序配合。

在 load 的过程中，ITCM 在一些时刻会同时被数据总线和指令总线读取，因此 ITCM 使用双端口 RAM。

## CORE

这里使用的是 [ibex](https://github.com/lowRISC/ibex)，该 core 有单独的数据总线和指令总线，但是为一种私有总线，为了通用，将其转为 AXI4 总线。

