---
title: Linux 权限问题
toc: true
date: 2020-03-10 17:44:43
categories: GEEK
tags: [GEEK, Linux]
description:
---

记录一下 Linux 下的用户、用户组、文件权限等基本知识，不能动不动就 777。

主要参考了 [一言不合就改成 777 权限？会出人命的！](https://juejin.im/post/5bad92cd6fb9a05cde1d6076)

<!-- more -->

# 基本操作

在 Linux 中，一个用户是可以属于多个组的，一个组也是可以包含多个用户的。

## 用户和用户组

1. 查看所有的用户：

   ~~~bash
cut -d':' -f 1 /etc/passwd
   ~~~

   结果

   ~~~bash
root
daemon
bin
sys
sync
...
sshd
   ~~~

2. 查看所有的用户组：

   ~~~bash
cut -d':' -f 1 /etc/group
   ~~~

   结果：

   ~~~
kmem
dialout
fax
voice
cdrom
floppy
...
lpadmin
   ~~~

结果基本是类似的，因为每个用户在被创建的时候都会自动创建一个同名的组作为其默认的用户组。

3. 查看一个用户所属的用户组，这里用 ubuntu 用户演示：

   ~~~bash
   groups ubuntu
   ~~~

   结果：

   ~~~
   ubuntu : ubuntu adm cdrom sudo dip plugdev lxd lpadmin sambashare
   ~~~

   这个用户被分配到了很多组下，比如同名的组 ubuntu，还有 sudo 组，另外还有一些其他的组。

   其中 sudo 组比较特殊，如果被分到了这个组里面就代表该账号拥有 root 权限，可以使用 sudo 命令。

4. 查看一个用户组里有哪些用户：

   ~~~bash
   members <group>
   ~~~

   不过这个命令不是自带的，需要额外安装 members 包

5. 一个比较有用的命令，就是 id 命令，它可以用来查看用户的所属组别，格式如下：

   ~~~
   id <username>
   ~~~

   这里有一个 gid，作为主工作组，后面还有个 groups，它列出了用户所在的所有组。主工作组只有一个，而后者的数量则不限。可以看到用户组的结果和使用 groups 命令看到的结果是一致的。

6. 何创建一个用户和怎样为用户分配组别

   添加用户：

   ~~~bash
   sudo adduser <username>
   ~~~

   添加组：

   ~~~bash
   sudo groupadd <group>
   ~~~

   把某个用户加入到某个组里面：

   ~~~bash
   sudo adduser <username> <group>
   ~~~

   或者使用 usermod 命令：

   ```bash
   sudo usermod -G <group> <username>
   ```

   如果要添加多个组的话，可以通过 -a 选项指定多个名称：

   ```bash
   sudo usermod -aG <group1,group2,group3..> <username>
   ```

## 文件权限管理

首先列出某个目录下文件的详细信息，命令如下：

~~~bash
ls -all
~~~

结果：

~~~
total 80
drwxr-xr-x   7 root root  4096 Jun 21 22:16 ./
drwxr-xr-x 103 root root  4096 Sep  4 18:04 ../
drwxr-xr-x   2 root root  4096 Jul 12  2017 conf.d/
-rw-r--r--   1 root root  1077 Feb 12  2017 fastcgi.conf
-rw-r--r--   1 root root  1007 Feb 12  2017 fastcgi_params
-rw-r--r--   1 root root  2837 Feb 12  2017 koi-utf
-rw-r--r--   1 root root  2223 Feb 12  2017 koi-win
-rw-r--r--   1 root root  3957 Feb 12  2017 mime.types
-rw-r--r--   1 root root  1505 Jun 21 20:24 nginx.conf
-rw-r--r--   1 root root 12288 Jun 21 20:44 .nginx.conf.swp
-rw-r--r--   1 root root   180 Feb 12  2017 proxy_params
-rw-r--r--   1 root root   636 Feb 12  2017 scgi_params
drwxr-xr-x   2 root root  4096 Jun 21 22:42 sites-available/
drwxr-xr-x   2 root root  4096 Jun 21 19:08 sites-enabled/
drwxr-xr-x   2 root root  4096 Jun 21 19:08 snippets/
-rw-r--r--   1 root root   664 Feb 12  2017 uwsgi_params
drwxr-xr-x   2 root root  4096 Jun 22 02:44 vhosts/
-rw-r--r--   1 root root  3071 Feb 12  2017 win-utf
~~~

一共包括七列：

- 第一列是文件的权限信息
- 第二列表示该文件夹连接的文件数
- 第三列表示文件所属用户
- 第四列表示文件所属用户组
- 第五列表示文件大小（字节）
- 第六列表示最后修改日期
- 第七列表示文件名

其中第一列的文件权限信息是非常重要的，它由十个字符组成：

- 第一个字符代表文件的类型，有三种，- 代表这是一个文件，d 代表这是一个文件夹，l 代表这是一个链接。
- 第 2-4 个字符代表文件所有者对该文件的权限，r 就是读，w 就是写，x 就是执行，如果是文件夹的话，执行就意味着查看文件夹下的内容，例如 rw- 就代表文件所有者可以对该文件进行读取和写入。
- 第 5-7 个字符代表文件所属组对该文件的权限，含义是一样的，如 r-x 就代表该文件所属组内的所有用户对该文件有读取和执行的权限。
- 第 8-10 个字符代表是其他用户对该文件的权限，含义也是一样的，如 r-- 就代表非所有者，非用户组的用户只拥有对该文件的读取权限。

1. 修改文件权限

   我们可以使用 chmod 命令来改变文件或目录的权限，有这么几种用法。

   一种是数字权限命名，rwx 对应一个二进制数字，如 101 就代表拥有读取和执行的权限，而转为十进制的话，r 就代表 4，w 就代表 2，x 就代表 1，然后三个数字加起来就和二进制数字对应起来了。如 7=4+2+1，这就对应着 rwx；5=4+1，这就对应着 r-x。所以，相应地 777 就代表了 rwxrwxrwx，即所有者、所属用户组、其他用户对该文件都拥有读取、写入、执行的权限，这是相当危险的！

   赋予权限的命令如下：

   ```
   sudo chmod <permission> <file>
   ```

   例如我要为一个 file.txt 赋予 777 权限，就写成：

   ```
   sudo chmod 777 file.txt
   ```

   另外我们也可以使用代号来赋予权限，代号有 u、g、o、a 四中，分别代表所有者权限，用户组权限，其他用户权限和所有用户权限，这些代号后面通过 + 和 - 符号来控制权限的添加和移除，再后面跟上权限类型就好，例如：

   ```
   sudo chmod u-x file.txt
   ```

   就是给所有者移除 x 权限，也就是执行权限。

   ```
   sudo chmod g+w file.txt
   ```

   就是为用户组添加 w 权限，即写入权限。

   另外如果是文件夹的话还可以对文件夹进行递归赋权限操作，如：

   ```
   sudo chmod -R 777 share
   ```

   就是将 share 文件夹和其内所有内容都赋予 777 权限。

2. 修改文件所属用户和所属用户组

   命令格式如下：

   ```bash
   sudo chown <username> <file> # 修改文件所属用户
   sudo chgrp <group> <file>    # 修改文件所属用户组
   ```

   另外同样可以使用 -R 来进行递归操作，如将 share 文件夹及其内所有内容的所有者都换成 cqc，命令如下：

   ```bash
   sudo chown -R cqc share/
   ```

