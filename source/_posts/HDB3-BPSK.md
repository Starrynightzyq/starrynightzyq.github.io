---
title: HDB3&BPSK
toc: true
date: 2018-12-24 10:06:33
categories: 课设
updated: 2019-01-24 21:49:57tags: [HDB3, BPSK, FPGA, 通信原理]
description: 音频AD采集->HDB3编码->BPSK调制->传输
---

# 可行性分析

## 需要的资源

- ADC；
- DDS；
- DAC；

## 实现

根据上述要求，选择EGo1板卡。

- ADC可使用Artix7芯片自带的XADC；

  > http://xilinx.eetrend.com/d6-xilinx/blog/2014-02/6676.html
  >
  > https://forums.xilinx.com/t5/Xcell-Daily-Blog-Archived/Adam-Taylor-s-MicroZed-Chronicles-Part-104-XADC-with-Real-World/ba-p/659668
  >
  > https://zhuanlan.zhihu.com/p/44495333

  [Zynq AXI XADC App Note](https://xilinx-wiki.atlassian.net/wiki/spaces/A/pages/18842057/Zynq+AXI+XADC+App+Note)

- DDS可使用xilinx的DDS IP核；

  > https://zhuanlan.zhihu.com/p/36929424

- DAC可使用板卡上的DAC0832芯片；

  > https://e-elements.readthedocs.io/zh/ego1_v2.1/EGo1.html#dac

# HDB3 编码

[参考](https://wenku.baidu.com/view/24b7bc227fd5360cba1adb6c)