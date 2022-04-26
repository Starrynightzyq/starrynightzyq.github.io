---
title: Linux 自动挂载磁盘
toc: true
date: 2020-03-15 22:17:19
categories: Linux
updated: 2020-03-21 14:04:35
tags: [GEEK, Linux]
description:
---

> 主要参考了：https://www.jianshu.com/p/ce31ae7da616

# 挂载点目录简介

1. Linux 常见的挂载目录结构：

   ![img](https://pic.zhouyuqian.com/img/20210727183057.jpg)

<!-- more -->

2. 常见挂载目录说明：

   `/` 根目录，存放系统命令和用户数据等（如果下面挂载点没有单独的分区，它们都将在根目录的分区中）
   `/boot` boot loader 的静态链接文件，存放与Linux启动相关的程序
   `/home` 用户目录，存放普通用户的数据
   `/tmp` 临时文件
   `/usr` 是Linux系统存放软件的地方,如有可能应将最大空间分给它
   `/usr/local` 自已安装程序安装在此
   `/var` 不断变化的数据，服务器的一些服务、日志放在下面
   `/opt` （Option可选的）附加的应用程序软件包
   `/bin` 基本命令执行文
   `/dev` 设备文件
   `/etc` 主机特定的系统配置
   `/lib` 基本共享库以及内核模块
   `/media` 用于移动介质的挂载点
   `/mnt` 用于临时挂载文件系统或者别的硬件设备（如光驱、软驱）
   `/proc` 系统信息的虚拟目录(2.4 和 2.6 内核)，这些信息是在内存中，由系统自己产生的
   `/root` root 用户的目录
   `/sbin` 基本系统命令执行文件
   `/sys` 系统信息的虚拟目录(2.6 内核)
   `/srv` 系统提供的用于 service 的数据
   `/usr/X1186` X-Windows目录，存放一些X-Windows的配置文件
   `/usr/include` 系统头文件，存储一些C语言的头文件
   `/usr/src` Linux内核源代码，Linux系统所安装的内核源代码都保存在此
   `/usr/bin` 对/bin目录的一些补充
   `/usr/sbin` 对/sbin目录的一些补充
   `/lost+found` 这个目录在大多数情况下都是空的。但是如果你正在工作突然停电，或是没有用正常方式关机，在你重新启动机器的时候，有些文件就会找不到应该存放的地方，对于这些文件，系统将他们放在这个目录下。

3. 什么 linux 的分区需要有挂载这个动作呢
   因为 linux 下一切皆文件！换句说法就是 linux 操作系统将系统中的一切都作为文件来管理。在 windows 中我们常见的硬件设备（打印机、网卡、声卡...）、磁盘分区等，在 linux 中统统都被视作文件，对设备、分区的访问就是读写对应的文件。

# 挂载分区

1. 临时挂载：

   ~~~bash
   $ mount /dev/sda3 /data   # sda3分区挂载在data目录下
   $ umount /data            # 卸载data目录下分区
   ~~~

2. 开机自动挂载：

   需要修改 `/etc/fstab`

   > fstab 是文件系统分配表的配置文件，该文件有着严格的语法格式限制，类似 crontab 一样，保存时也会对你的输入格式进行校验，请慎重使用，否则会有意想不到的问题发生。其一共有 6 个字段，空格分隔。

   **Sample:**

   ~~~bash
   UUID=8CBA-F92C /samba/users exfat         defaults     0          1
   <fs spec>      <fs file>    <fs vfstype>  <fs mntops>  <fs freq>  <fs passno>
   ~~~

   **参数说明：**
   `<fs spec>`：分区定位，可以给 UUID 或 LABEL，例如：UUID=6E9ADAC29ADA85CD或LABEL=software，建议不要用 `/dev/sda1` 这种格式，重新启动可能会导致磁盘顺序变化
   `<fs file>`：具体挂载点的位置，例如：`/samba/users`，必须是一个**已经存在的目录**，挂载后不会影响原先目录下的文件，卸载该分区后可以看到原先目录下的文件没有变化
   `<fs vfstype>`：挂载磁盘类型，linux 分区一般为 ext4，windows 分区一般为 ntfs
   `<fs mntops>`：挂载参数，一般为 defaults
   `<fs freq>`：磁盘检查，默认为0。能否被 dump 备份指令作用：在 Linux 当中，可以利用 dump 这个指令来进行系统的备份的。而 dump 指令则会针对 /etc/fstab 的设定值，去选择是否要将该 partition 进行备份的动作呢！ 0 代表不要做 dump 备份， 1 代表要进行 dump 的动作。 2 也代表要做 dump 备份动作， 不过，该 partition 重要度比 1 小。
   `<fs passno>`：磁盘检查，默认为0，不需要检查。是否以 fsck 检验扇区：开机的过程中，系统预设会以 fsck 检验我们的 partition 内的 filesystem 是否完整 (clean)。 不过，某些 filesystem 是不需要检验的，例如虚拟内存 swap ，或者是特殊档案系统， 例如 /proc 与 /sys 等等。所以，在这个字段中，我们可以设定是否要以 fsck 检验该 filesystem 喔。 0 是不要检验， 1 是要检验， 2 也是要检验，不过 1 会比较早被检验啦！ 一般来说，根目录设定为 1 ，其它的要检验的 filesystem 都设定为 2 就好了。

   **检查：**

   修改完 `/etc/fstab` 文件后，运行以下命令检查配置是否正确：

   ~~~bash
   sudo mount -a
   ~~~

   如果配置不正确可能会导致系统无法正常启动。

3. 常用命令：

   - 查看硬盘信息：

     ~~~
     sudo fdisk -l
     ~~~

   - 查看磁盘分区的 UUID：

     ~~~
     sudo blkid
     ~~~

   
# 自动挂载 smb

> ref：https://gythialy.github.io/How-to-Mount-a-SMB-Share-in-Ubuntu/

## 临时挂载

1. 安装 cifs-utils

   ~~~bash
   sudo apt-get install cifs-utils
   ~~~

2. 挂载

   ~~~bash
   sudo mount -t cifs //xx.xx.xx.x/share /mnt -o username=xx,password=xx,vers=1.0
   ~~~

## 开机自动挂载

1. 创建一个挂载点

   ```
   sudo mkdir /mnt/local_share
   ```

2. 创建文件保存 *~/.smbcredentials* 来保存 SMB 用户名和密码

   ```
   username=smb_share
   password=share_password
   ```

3. 在 */etc/fstab* 最后添加配置实现自动挂载

   ```
   # /etc/fstab
   /$smb_server/share /mnt/local_share cifs credentials=/home/$user/.smbcredentials,uid=1000,gid=1000,iocharset=utf8 0 0
   ```

   > PS：`$smb_server` 为 SMB 服务器地址，`$user` 为当前用户名，`uid/gid` 为当前用户的 `uid` 和 `gid`，可以通过 `id $(whoami)` 查看

4. 通过 `mount -a` 命令检查 fstab 文件是否有错，如果错误可能会导致无法开机。

# 挂载 NFS

首先需要安装：

~~~bash
sudo apt install nfs-common
~~~

## 临时挂载

~~~bash
sudo mkdir -p /nfs/general
sudo mount nfs_ip:/var/nfs/general /nfs/general
~~~

## 开机自动挂载

编辑 */etc/fstab*，在最后添加：

~~~bash
nfs_ip:/var/nfs/general /nfs/general nfs auto,nofail,noatime,nolock,intr,tcp,actimeo=1800 0 0
~~~

然后通过 `mount -a` 命令检查 fstab 文件是否有错，如果错误可能会导致无法开机。

