---
title: VCO 中电感的选取及仿真
toc: true
comments: true
date: 2021-05-08 15:19:11
updated: 2021-05-08 15:19:11
categories: PLL
tags: [IC_design, Analog, PLL]
description: VCO 中电感的选取及仿真
---

本次设计使用的是 TSMC65 工艺，使用的电感是工艺库中提供的中心抽头差分电感，因此可以使用 TIF (TSMC Inductor Finder) 功能来找到合适的电感。TIF 的使用可以参考工艺库中的文档：`TIF_User_Guide.pdf`、`TIF_tutorial.pdf`。

这里使用的电感参数如下图所示：

<img src="https://pic.zhouyuqian.com/img/20210727182509.png" alt="ind" style="zoom:50%;" />

根据 TIF 的结果，其电感值在 2.4GHz 的频率下为 3.9 nH，我们可以使用 S 参数仿真来看一下电感的 L-Q 曲线。

仿真的电路图如下（方法来自 [eetop-depend135](http://bbs.eetop.cn/forum.php?mod=redirect&goto=findpost&ptid=292661&pid=6034926)）：

![schematic](https://pic.zhouyuqian.com/img/20210727182450.png)

SP 仿真的设置如下：

![sp](https://pic.zhouyuqian.com/img/20210727182451.png)

这里注意频率的扫描范围不要从 0 开始，不然后面计算电感值时会出现除以 0 的现象，导致无法计算出电感值。

电感的 L 和 Q 计算公式分别为：
$$
L= imag(1/Y11)/(2*\pi * freq)
$$

$$
Q = -imag(Y11)/real(Y11)
$$

cadence ADE 中没有提供一个方便的获取扫描频率的函数，参考 [eetop-ctlvip](http://bbs.eetop.cn/forum.php?mod=redirect&goto=findpost&ptid=702628&pid=9612242) 的方法，使用 xval 来获取 freq，具体的公式如下：
$$
L=\rm{(imag((1 / ypm('sp 1 1))) / (2 * pi * xval(imag(ypm('sp 1 1)))))}
$$

$$
Q = \rm{((- imag(ypm('sp 1 1))) / real(ypm('sp 1 1)))}
$$

运行仿真，得到 L-Q 曲线如下图所示：

![L-Q](https://pic.zhouyuqian.com/img/20210727182452.svg)

这个曲线和 TIF 的结果是一致的。