---
title: GCC-4.8.5 编译安装
toc: true
comments: true
date: 2021-11-30 14:42:57
updated: 2021-12-03 21:07:00
categories: Software
tags:
  - Software
  - IC_design
description: 在 Ubuntu-20.04.3 上编译安装 GCC-4.8.5
---

## GCC-4.8.5 编译安装

> 1. [https://stackoverflow.com/questions/61945439/how-to-install-compiler-g-4-8-5-in-ubuntu-20-04](https://stackoverflow.com/questions/61945439/how-to-install-compiler-g-4-8-5-in-ubuntu-20-04)
> 2. [https://www.icode9.com/content-3-1202280.html](https://www.icode9.com/content-3-1202280.html)
> 3. [https://www.frank.fyi/archives/336_gcc-compile-error/](https://www.frank.fyi/archives/336_gcc-compile-error/)

参考第一篇：

~~~bash
# 下载gcc
wget http://ftp.gnu.org/gnu/gcc/gcc-4.8.5/gcc-4.8.5.tar.bz2
# 解压
tar -zxvf gcc-4.8.5.tar.bz2
# 修改 gcc-4.8.5 两处 bug
sed -i -e 's/__attribute__/\/\/__attribute__/g' gcc-4.8.5/gcc/cp/cfns.h
sed -i 's/struct ucontext/ucontext_t/g' gcc-4.8.5/libgcc/config/i386/linux-unwind.h
 
# 安装依赖三大件，会自动顺序安装gmp、mpfr、mpc
gcc-4.8.5/contrib/download_prerequisites
# 或者
sudo apt install make wget git gcc g++ lhasa libgmp-dev libmpfr-dev libmpc-dev flex bison gettext texinfo ncurses-dev autoconf rsync
 
# 创建编译目录 gcc-4.8.5-build
mkdir gcc-4.8.5-build
cd gcc-4.8.5-build
 
# 开始编译安装
$PWD/../gcc-4.8.5/configure --enable-languages=c,c++ --prefix=/usr/local/gcc-4.8.5 --enable-shared --enable-plugin --program-suffix=-4.8.5 --disable-multilib
make MAKEINFO="makeinfo --force" -j

# 编译完成后安装
sudo make install
~~~

编译的过程中会出现一些问题，主要参考了[第二篇文章](https://www.icode9.com/content-3-1202280.html)和[第三篇文章](https://www.frank.fyi/archives/336_gcc-compile-error/)。
