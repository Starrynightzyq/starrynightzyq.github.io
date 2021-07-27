---
title: Cadence IC617 on Ubuntu
categories: Software
tags:
  - Software
  - IC_design
description: >-
  在 Ubuntu20.04 上安装 Cadence IC617 & MMSIM151 & calibre2015 &
  INCISIVE152 & ADS2020U2，理论上也适用于其他的 Ubuntu 或 Linux 系统.
toc: true
comments: true
date: 2021-03-07 17:12:33
updated: 2021-04-11 10:46:00
---

# Cadence Reference

[1.0] [Ubuntu20.04 安装Cadence IC617(HotFix)，Spectre，Calibre，Xceliummain](https://zhuanlan.zhihu.com/p/354374816)

[1.1] [ubuntu18.04安装cadence virtuoso](https://my.oschina.net/propagator/blog/3166272)

[1.2] [在 CentOS7 下安装 Cadence IC验证平台 INCISIVE152](https://blog.csdn.net/yy345730585/article/details/90407408)

可能出现的问题及解决方法：

[2] [...install.ixl/mgc_install: No such file or directory](http://bbs.eetop.cn/thread-877866-1-1.html)

[3] [ERROR: The OA2.2 library directory (/home/hushuai/cadence/installs/IC616/oa_v22.43.018/lib/linux_rhel40_gcc44x_32/opt) does not seem to exist.](http://bbs.eetop.cn/thread-400786-1-1.html)

[4] [*WARNING* Unable to find font name: "-*-courier-medium-r-*-*-12-*".](http://bbs.eetop.cn/thread-325949-1-1.html)

[6] [*ld: /usr/lib/x86_64-linux-gnu/crti.o: unrecognized relocation (0x2a) in section `.init'](http://bbs.eetop.cn/archiver/tid-635921.html)

[7] [/usr/include/math.h:27:36: fatal error: bits/libc-header-start.h: No such file or directory](https://blog.csdn.net/qq_19734597/article/details/102943559)

[8] [WARNING The glibc version of this host does not appear to be a Cadence supported version.](http://bbs.eetop.cn/thread-768205-1-1.html)

~~~bash
# 准备工作
sudo apt-get install ksh csh openjdk-8-jre openjdk-8-jdk xterm libncursesw5-dev libxtst6:i386 libxi6:i386 libstdc++6 lib32stdc++6 python net-tools xfonts-75dpi xfonts-100dpi
# 
wget http://ftp.br.debian.org/debian/pool/main/g/glibc/multiarch-support_2.28-10_amd64.deb
sudo dpkg -i multiarch-support_2.28-10_amd64.deb
wget http://launchpadlibrarian.net/183708483/libxp6_1.0.2-2_amd64.deb
sudo dpkg -i libxp6_1.0.2-2_amd64.deb
# 查看Java安装情况
java -version
# 配置Java环境变量
export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64
export JRE_HOME=$JAVA_HOME/jre
export CLASSPATH=$JAVA_HOME/lib:$JRE_HOME/lib:$CLASSPATH
export PATH=$JAVA_HOME/bin:$JRE_HOME/bin:$PATH
# 添加redhat-release 骗过cadence
sudo echo "Red Hat Enterprise Linux release 6.12" > /etc/redhat-release
sudo chmod 777 /etc/redhat-release
##创建临时文件夹
sudo ln -s /tmp /usr/tmp
##软链接
##sudo ln -s /usr/bin/mawk /bin/awk
##sudo ln -s /usr/bin/basename /bin/basename
sudo ln -s /lib/x86_64-linux-gnu/libncursesw.so.5.9 /lib/libtermcap.so.2
sudo ln -s /lib/x86_64-linux-gnu/libcrypto.so.1.1 /lib/x86_64-linux-gnu/libcrypto.so.6
~~~



# ADS Reference

[1] [快递：Linux安装ADS2020update2.0及破解](http://bbs.eetop.cn/thread-880091-1-1.html)

[2] [ubuntu 上装 ADS 2015](http://bbs.eetop.cn/thread-560408-1-1.html)

~~~bash
sudo ./pubkey_verify
sudo ./pubkey_verify -y
~~~

然后再安装license

~~~bash
# sh:1:lmutil:not found  sh:1:lmgrd:not found
sudo apt-get isntall lsb-core
~~~

# ADS Dynamic Link

> http://literature.cdn.keysight.com/litweb/pdf/ads2008/dynlnkug/ads2008/Getting_Started_with_RFIC_Dynamic_Link.html
>
> http://edadownload.software.keysight.com/eedl/ads/2011/pdf/dynlnkug.pdf
>
> https://zhuanlan.zhihu.com/p/355213307

在 ADS 和 Cadence 都正确安装且可以正常打开的情况下：

首先要在 *.cdsinit* 文件里添加：

~~~bash
load("/opt/ADS2020_update2/idf/config/.cdsinit")
~~~

然后：

~~~bash
source $HPEESOF_DIR/bin/setCSF.ksh
~~~

然后启动 virtuoso，在CIW中可发现ADS已成功加载：

![截屏2021-04-20 下午4.40.58](https://pic.zhouyuqian.com/img/20210727233512.png)

在 schematic 中选择 Launch-ADS Dynamic Link，就会弹出ADS窗口：

![截屏2021-04-20 下午4.43.01](https://pic.zhouyuqian.com/img/20210727233513.png)

# Modelsim

## Prepare install files

Unwaper this three files and you will get `Mentor Graphics ModelSim SE 2020.4 Linux64`

~~~
Mentor_Graphics_ModelSim_SE_2020.4_Linux64.part1_Downloadly.ir
Mentor_Graphics_ModelSim_SE_2020.4_Linux64.part2_Downloadly.ir
Mentor_Graphics_ModelSim_SE_2020.4_Linux64.part3_Downloadly.ir
~~~

## 安装

~~~bash
chmod +x modelsim-2020.4_Downloadly.ir.aol # 修改权限
sudo ./modelsim-2020.4_Downloadly.ir.aol # 安装
~~~

> **注意：只安装 64 位的部分！**

## 生成 license file

使用 wine 运行 `MentorKG.exe` 文件，首先要安装 wine：

~~~bash
sudo apt-get install wine
~~~

在成功安装Wine之后，需要在第一次使用之前使用下面的命令初始化wine配置文件：

~~~bash
sudo winecfg
~~~

然后 patch，`<Modelsim install path>` 在我的电脑上为 `/opt/ModelSim`：

~~~bash
sudo cp MentorKG.exe <Modelsim install path>/modeltech/linux_x86_64 # 复制 MentorKG.exe 到 modelsim 安装目录下
sudo wine MentorKG.exe -patch .
~~~

保存生成的 license 为 `license.dat`，并选择文件编码格式为 `Unicode(UTF-8)`，位置 `/opt/ModelSim/license.dat`

## Patch

ref:http://bbs.eetop.cn/thread-888767-1-1.html

把 sfk 和 patch_calibre2011_linux 文件拷贝到 modelsim 的安装路径下(同级有modeltech和_msidata文件夹)

~~~bash
sudo cp patch_calibre2011_linux sfk /opt/ModelSim
sudo chmod 755 patch_calibre2011_linux sfk    #chmod patch 和 sfk文件权限均为755
sudo ./patch_calibre2011_linux    #执行本命令，其实就是调用了一次sfk
~~~

> 报错：
>
> ~~~bash
> ./sfk: error while loading shared libraries: libstdc++.so.5: cannot open shared object file: No such file or directory
> ~~~
>
> ~~~bash
> locate libstdc++.so.5  #发现系统中还真的没这个运行库
> # 这是一个古老的库 所以安装 
> # sudo apt-get install libstdc++5
> sudo apt-get install libstdc++5:i386
> ~~~
>
> ~~~bash
> sfk rep -yes -bin /41574989CF41564589C6415541544189D455534889FB4881ECF8000000488B8798020000/4831c0c3CF41564589C6415541544189D455534889FB4881ECF8000000488B8798020000/ -dir .
> sfk rep -yes -bin /41574989CF41564589C6415541544189D455534889FB4881ECF8000000488B8798020000/4831c0c3CF41564589C6415541544189D455534889FB4881ECF8000000488B8798020000/ -dir .
> sfk rep -yes -bin /CC88D700000000001300000000000000000000000700070000000000210005007C6B610100000000000000000000000000000000000000000000000000000000A0D2D700000000000BFFFFFF00000000/CC88D7000000000013000000FFFFFFFF000000000700070000000000210005007C6B610100000000000000000000000000000000000000000000000000000000A0D2D700000000000BFFFFFF00000000/ -dir . -file vcom
> ~~~
>
> 最后的log中出现 2 changed 就成功了。

## 修改环境变量

~~~bash
# modelsim
export MTI_VCO_MODE=64
export LM_LICENSE_FILE=/opt/ModelSim/license.dat
export PATH=$PATH:/opt/ModelSim/modeltech/linux_x86_64
~~~

执行 `vsim`

> PS: 要修改网卡名称为 eth0
>
> > sudo vim /etc/default/grub 
> >
> > 找到GRUB_CMDLINE_LINUX=""
> >
> > 改为GRUB_CMDLINE_LINUX="net.ifnames=0 biosdevname=0"
> >
> > 然后sudo grub-mkconfig -o /boot/grub/grub.cfg
>
> **重启**后，网卡名称就会变成了eth0



> dash 改为 bash
>
> ~~~bash
> sudo dpkg-reconfigure dash # 选 No
> ~~~



# HFSS

> https://www.cfd-online.com/Forums/ansys/199190-ansys-18-2-ubuntu-16-04-installation-guide.html

~~~bash
$ sudo ./install -silent -install_dir /opt/ansys_inc
[sudo] password for meow: 
### Warning: Dependency package bzip2-libs is not installed.
### Warning: Dependency package expat is not installed.
### Warning: Dependency package fontconfig is not installed.
### Warning: Dependency package freetype is not installed.
### Warning: Dependency package giflib is not installed.
### Warning: Dependency package glib2 is not installed.
### Warning: Dependency package glibc is not installed.
### Warning: Dependency package libdrm is not installed.
### Warning: One of the following alternate dependencies are not installed: libjpeg libjpeg-turbo
### Warning: Dependency package libpng is not installed.
### Warning: Dependency package libselinux is not installed.
### Warning: Dependency package libtiff is not installed.
### Warning: Dependency package libX11 is not installed.
### Warning: Dependency package libXau is not installed.
### Warning: Dependency package libxcb is not installed.
### Warning: Dependency package libXdamage is not installed.
### Warning: Dependency package libXext is not installed.
### Warning: Dependency package libXfixes is not installed.
### Warning: Dependency package libXft is not installed.
### Warning: Dependency package libXmu is not installed.
### Warning: Dependency package libXp is not installed.
### Warning: Dependency package libXrender is not installed.
### Warning: Dependency package libXt is not installed.
### Warning: Dependency package libXxf86vm is not installed.
### Warning: Dependency package mesa-dri-drivers is not installed.
### Warning: Dependency package mesa-libGL is not installed.
### Warning: Dependency package mesa-libGLU is not installed.
### Warning: Dependency package nss-softokn-freebl is not installed.
### Warning: Dependency package zlib is not installed.
/mnt/hgfs/IC_Design/share/HFSS/ELECTRONICS_180_LINX64/Electronics_180_linx64/Linux/install.exe: error while loading shared libraries: libpng12.so.0: cannot open shared object file: No such file or directory
~~~

## 安装必要的软件

~~~bash
sudo apt install xterm lsb csh ssh rpm xfonts-base xfonts-100dpi xfonts-100dpi-transcoded xfonts-75dpi xfonts-75dpi-transcoded xfonts-cyrillic libmotif-common mesa-utils libxm4 libxt6 libxext6 libxi6 libx11-6 libsm6 libice6  libxxf86vm1 libpng16-16 libtiff5 gcc g++ libstdc++6 libstdc++5
~~~

~~~bash
# libpng12-0
wget http://ppa.launchpad.net/linuxuprising/libpng12/ubuntu/pool/main/libp/libpng/libpng12-0_1.2.54-1ubuntu1.1+1~ppa0~focal_amd64.deb
sudo dpkg -i libpng12-0_1.2.54-1ubuntu1.1+1~ppa0~focal_amd64.deb
~~~

~~~bash
# libxp
wget ftp.us.debian.org/debian/pool/main/libx/libxp/libxp6_1.0.2-2_amd64.deb
sudo dpkg -i libxp6_1.0.2-2_amd64.deb
~~~

## 更新索引

~~~bash
# updatedb 用来创建或更新 slocate/locate 命令所必需的数据库文件
# updatedb 命令的执行过程较长，因为在执行时它会遍历整个系统的目录树，并将所有的文件信息写入 slocate/locate 数据库文件中
# Update the database with:
sudo updatedb
~~~

## 创建超链接

~~~bash
sudo ln -s /usr/lib/x86_64-linux-gnu/libGL.so.1 /usr/lib/libGL.so
sudo ln -s /usr/lib/x86_64-linux-gnu/libGL.so.1 /usr/lib/libGL.so.1
sudo ln -s /usr/lib/x86_64-linux-gnu/libGLU.so.1 /usr/lib/libGLU.so
sudo ln -s /usr/lib/x86_64-linux-gnu/libXm.so.4 /usr/lib/libXm.so
sudo ln -s /usr/lib/x86_64-linux-gnu/libXm.so.4 /usr/lib/libXm.so.3
sudo ln -s /usr/lib/x86_64-linux-gnu/libXp.so.6 /usr/lib/libXp.so
sudo ln -s /usr/lib/x86_64-linux-gnu/libXt.so.6 /usr/lib/libXt.so
sudo ln -s /usr/lib/x86_64-linux-gnu/libXext.so.6 /usr/lib/libXext.so
sudo ln -s /usr/lib/x86_64-linux-gnu/libXi.so.6 /usr/lib/libXi.so
sudo ln -s /usr/lib/x86_64-linux-gnu/libX11.so.6 /usr/lib/libX11.so
sudo ln -s /usr/lib/x86_64-linux-gnu/libSM.so.6 /usr/lib/libSM.so
sudo ln -s /usr/lib/x86_64-linux-gnu/libICE.so.6 /usr/lib/libICE.so
sudo ln -s /lib/x86_64-linux-gnu/libgcc_s.so.1 /lib/libgcc.so
sudo ln -s /lib/x86_64-linux-gnu/libc.so.6 /lib/libc.so
sudo ln -s /lib/x86_64-linux-gnu/libc.so.6 /lib64/libc.so.6
~~~

## 将默认 sh 改为 bash

~~~bash
# Change the command interpreter for shell scripts:
sudo dpkg-reconfigure dash
# Then answer "No" to the question.
~~~

## 安装

~~~bash
# install
# sudo ./INSTALL  -silent -install_dir /opt/ansys_inc
sudo ./INSTALL
~~~

安装位置选择 */opt/ansys_inc*

## 破解

将破解文件夹复制到 */opt/ansys_inc* 覆盖原来的文件

~~~bash
sudo cp -r ansys_inc /opt
~~~

## 修改权限

~~~bash
sudo chown -R $USER:$USER ~/.ansys
sudo chown -R $USER:$USER ~/.config
sudo chown -R 777 /ansys_inc/v202/aisol/WBMWRegistry/
~~~

## 修改通配符不匹配

修改 */opt/ansys_inc/v202/CFX/bin/cfx5arch*

大约在 196 行处有：

~~~bash
if test -n "$libc_file"; then
case `basename $libc_file | sed 's/\.so//g'` in
glibc-*|libc-[0123].*) # this is almost certainly a glibc version
~~~

在这下面加上：

~~~bash
libc_file_tmp=`echo $libc_file | sed -e 's/x86_64-linux-gnu//g'`
~~~

然后将:

~~~bash
libc_version=`echo $libc_file | sed -e 's/^[^-]*-//' -e 's/\.so//g'`
~~~

改为：

~~~bash
libc_version=`echo $libc_file_tmp | sed -e 's/^[^-]*-//' -e 's/\.so//g'`
~~~

![截屏2021-04-09 下午5.14.46](https://pic.zhouyuqian.com/img/20210727233514.png)

## Since ptrace is used to monitor intelmpi CFX run, set the permission for all the users, just edit

编辑 */etc/sysctl.d/10-kernel-hardening.conf *

加入：

~~~bash
kernel.yama.ptrace_scope = 0
~~~

/etc/sysctl.d/10-ptrace.conf

~~~bash
kernel.yama.ptrace_scope = 1
->
kernel.yama.ptrace_scope = 0
~~~

/proc/sys/kernel/yama/ptrace_scope

~~~bash
1
->
0
~~~



## 编辑 *.bashrc* 文件

~~~bash
#ANSYS
export PATH=$PATH:/opt/ansys_inc/v202/ansys/bin
#CFX
export PATH=$PATH:/opt/ansys_inc/v202/CFX/bin
#FLUENT
export PATH=$PATH:/opt/ansys_inc/v202/fluent/bin
#ICEM
export PATH=$PATH:/opt/ansys_inc/v202/icemcfd/linux64_amd/bin
#WORKBENCH
export PATH=$PATH:/opt/ansys_inc/v202/Framework/bin/Linux64
#TurboGrid
export PATH=$PATH:/opt/ansys_inc/v202/TurboGrid/bin
#ANSYS Sevice Manager
export PATH=$PATH:/opt/ansys_inc/shared_files/licensing/lic_admin
#polyflow
export PATH=$PATH:/opt/ansys_inc/v202/polyflow/bin
#more
alias wb2='/ansys_inc/v202/Framework/bin/Linux64/runwb2 -oglmesa'
export LD_LIBRARY_PATH=/opt/ansys_inc/v202/Framework/bin/Linux64/Mesa:$LD_LIBRARY_PATH
export LANG=en_US.UTF8
export FLUENT_ARCH='lnamd64'
~~~

