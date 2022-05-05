---
title: UVM+VCS+Verdi 基本平台搭建
toc: true
comments: true
date: 2022-05-05 18:14:00
updated: 2022-05-05 19:18:04
categories: UVM
tags: [UVM, IC_design]
description:
---

这几天在学习 UVM，一般公司里都有一个完整的验证环境，但是对于个人而言，环境可能就是一道屏障，下文将一步一步的举例子说明 UVM+VCS+Verdi 的 liunx 平台搭建过程（假设你已经安装好 VCS 和 Verdi，安装可以参考我的这篇文章 [6. Synopsys VCS+Verdi](https://zhouyuqian.com/2021/03/07/VirtuosoOnUbuntu/#synopsys-vcsverdi) ）。

<!--more-->

> PS: 我用的版本是：VCS 2016.06, Verdi 2016.06

## 准备 UVM 库

我是从这里下载的：[uvm-1.1d.tar.gz](https://bbs.eetop.cn/forum.php?mod=attachment&aid=NjE3MDIzfDVhN2IzNTZmfDE2NTE3NDQzOTh8MTc3MDcyNHw0ODEyNDM%3D) [uvm-1.1a.tar.gz](https://bbs.eetop.cn/forum.php?mod=attachment&aid=NjE3MDIyfGI4MmNhNWQyfDE2NTE3NDQzOTh8MTc3MDcyNHw0ODEyNDM%3D).

把 *uvm-1.1a.tar.gz* 放在linux系统中，放入后在进行解压。得到 *uvm-1.1a* 文件夹，该路径是库所在路径，放在什么地方无所谓。

在 *~/.bashrc* 文件中添加 `UVM_HOME` 变量：

> PS: **注意** bash 和 csh 的写法是不同的，根据自己的 shell 添加对应的环境变量

~~~bash
# bash or zsh
export UVM_HOME=/usr/synopsys/uvm_lib/uvm-1.1a
# csh or tcsh
setenv UVM_HOME /usr/synopsys/uvm_lib/uvm-1.1
~~~

在 `$(UVM_HOME)/examples` 目录下有一个 *Makefile.vcs* 文件，该文件对于所有验证平台公用，里面主要是对 UVM 库进行编译，自己写的 make 文件里面需要 include 这个文件。

## The first example

将 `$(UVM_HOME)/examples/integrated/ubus/examples` 文件夹复制到别的地方，然后进入这个新复制的文件夹，输入命令：

~~~bash
make -f Makefile.vcs
~~~

因为我 VCS 的环境需要在 make 脚本里配置，所以我对 *Makefile.vcs* 做了一些修改，修改后的脚本如下：

~~~Makefile
export LD_LIBRARY_PATH=${VERDI_HOME}/share/PLI/VCS/LINUX64
include $(UVM_HOME)/examples/Makefile.vcs

VCS += -full64 \
	   -cpp /usr/local/gcc-4.8.5/bin/g++-4.8.5 \
	   -cc /usr/local/gcc-4.8.5/bin/gcc-4.8.5

all: comp run

comp:
	$(VCS) +incdir+../sv \
		ubus_tb_top.sv

run:
	$(SIMV) +UVM_TESTNAME=test_2m_4s
	$(CHECK)
~~~

如果出现如下图的结果，则说明平台已经搭建成功了。

![](https://pic.zhouyuqian.com/img/202205051904944.png)

## More examples

下一篇介绍 axi-uvm 环境的搭建，基于 [marcoz001/axi-uvm](https://github.com/marcoz001/axi-uvm).

## Reference

[1] [UVM+VCS+Verdi基本平台搭建](https://bbs.eetop.cn/thread-481243-1-1.html)

[2] [UVM学习-仿真环境的搭建](https://zhuanlan.zhihu.com/p/138405443)

