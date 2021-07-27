---
title: 解决 Altium Designer 卡死问题
toc: true
date: 2020-07-01 21:32:46
categories: Altium-Designer
updated: 2020-07-02 02:11:14tags: [Altium-Designer, GEEK]
description:
---

最近用 Altium Designer 20 画了几个板子，经常卡死，真的让人崩溃，在排除电脑硬件问题及系统问题后，找到了 AD 软件自身的问题。

<!--more--->

目前网上主要有两种解决方案如下：

# 1. 禁止 AD 自动联网

## 第一步：关闭 AD 自动更新

点击右上角的设置小齿轮，然后在 System-> Account Management 中改为 "No,…”，如下图：

![ad1](https://pic.zhouyuqian.com/img/20210727173721.jpg)

在 System -> Installation 的 "Check frequency” 改为 “Never”，如下图：

![ad2](https://pic.zhouyuqian.com/img/20210727173722.jpg)

## 第二步：设置防火墙，禁止 AD 联网

这步就是设置防火墙禁止 AD 软件联网，方法比较简单，参考：[禁止Altium designer（其他软件同样适用）联网的配置操作](https://blog.csdn.net/qq_23957035/article/details/82492093)

# 2. 删除多余的库

这个方法的思路在于 AD 有时候库过多导致打开的时间过长，个人觉得用处不大。参考：[Altium教程：AD中pcb文件和库文件libraries卡死解决办法](https://www.bilibili.com/read/cv3488833/)



