---
title: VCO 参数选取及仿真
toc: true
comments: true
date: 2021-05-08 16:05:26
updated: 2021-05-08 16:05:26
categories: PLL
tags: [IC_design, Analog, PLL]
description: VCO 参数选取及仿真
---

# 参数计算与选取

## 电感的等效并联电阻 $R_P$

> <LC 振荡回路等效电路图>

可以使用 DC 仿真及计算一个大概的 $R_S$，然后通过公式计算出等效并联电阻 $R_P$：
$$
R_P  \approx \frac{Q_L^2}{R_S} \\
\approx \frac{L^2\omega^2}{R_S}
$$
根据 DC 仿真，得到 $R_S= 1.98\Omega$，设定 $f=2.4G$，电感 $L = 4nH$，得到 $R_P = 122\Omega$。

## 负阻管 $g_m$

$g_m$ 的选取需要保证满足：
$$
R_P>1/g_m
$$
为了更容易起振，选择 $g_m > 2/R_P$，因此需要 $g_m > 16mS$。

## 电容

LC 振荡器的频率为：
$$
f=\frac{1}{2\pi\sqrt{LC}}
$$
电感 $L = 4nH$，$f=2.4G$，则电容 $C\approx 1.1p$。

假设 $K_{VCO} = 10MHz/V$，则可变电容的变化范围：
$$
\Delta C = \frac{1}{L(2\pi f_1)^2} -\frac{1}{L(2\pi f_2)^2} \approx \frac{1}{L(2\pi)^2}\frac{2\Delta f}{f^3} \approx 1fF 
$$

# Output Frequency, Output Power, Phase Noise 仿真

> 仿真过程参考了 `SpectreRF Workshop VCO Design Using SpectreRF`，该文件位于 *<SPECTRE Install dir>/tools.lnx86/spectre/examples/SpectreRF_workshop/rfworkshop.tar.Z*

## 电路原理图

![vco-schematic](https://pic.zhouyuqian.com/img/20210727172519.png)

电路原理图如上图所示，可变电容部分使用了三个可变电容并联并给不同的偏置的方法，用来提高可变电容的线性度，其结构如下图所示。

<img src="https://pic.zhouyuqian.com/img/20210727172647.png" alt="image-20210509152604001" style="zoom:33%;" />

> 开关电容阵列结构还没有做好

## pss+pnoise 仿真设置

pss 仿真设置如下图所示：

<img src="https://pic.zhouyuqian.com/img/20210727172740.png" alt="pss1" style="zoom:33%;" />

<img src="https://pic.zhouyuqian.com/img/20210727172754.png" alt="pss2" style="zoom:33%;" />

**Beat Frequency:** 设置 VCO 的工作频率；

**Number of harmonics : ** 设置为 10；

**stop time (stab) :** 设置为 120n；

**Oscillator : ** 勾选 Oscillator，分别设置 node+ 和 node- 为 VCO 的正负输出端口；

**Sweep : ** 可以设置变容二极管的控制电压扫描范围；

pnoise 仿真设置如下：

<img src="https://pic.zhouyuqian.com/img/20210727172815.png" alt="pnoise" style="zoom:33%;" />

**Sweeptype : **设置为 relative；

**Output Frequency Sweep Range : ** 设置为 1K - 10M；

**Noise Type : **选择 time average - ALL

## 仿真结果查看

### 瞬态输出

选择 **Results — Direct Plot — Main Form — tstab**

<img src="https://pic.zhouyuqian.com/img/20210727172835.png" alt="tstab" style="zoom:33%;" />

![tstab](https://pic.zhouyuqian.com/img/20210727172520.svg)

### 输出功率

<img src="https://pic.zhouyuqian.com/img/20210727172851.png" alt="power_tb" style="zoom:33%;" />

选择 **Different Nets (specify R)** 并设置好负载，输出选择 **dBm**。

![power](https://pic.zhouyuqian.com/img/20210727172521.svg)

### Phase Noise

<img src="https://pic.zhouyuqian.com/img/20210727172927.png" style="zoom:33%;" />

![phasenoise](https://pic.zhouyuqian.com/img/20210727172522.svg)

### AM noise / PM noise

<img src="https://pic.zhouyuqian.com/img/20210727172956.png" alt="AM" style="zoom:33%;" />

<img src="https://pic.zhouyuqian.com/img/20210727173012.png" alt="PM" style="zoom:33%;" />

![AMPMnoise](https://pic.zhouyuqian.com/img/20210727172523.svg)

### 频率随 Vctrl 变化及 KVCO

<img src="https://pic.zhouyuqian.com/img/20210727173031.png" alt="vrtrl" style="zoom:33%;" />

KVCO 使用 `deriv` 函数计算得到。

![vctrl](https://pic.zhouyuqian.com/img/20210727172524.svg)

# 电路优化

> 1. 调节电流，让振荡器工作在电压受限区和电流受限区之间；
> 2. 相位噪声优化；

