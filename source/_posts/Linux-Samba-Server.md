---
title: Linux Samba Server
toc: true
date: 2020-03-15 23:00:44
categories: Linux
updated: 2020-03-21 14:04:35tags: [GEEK, Linux]
description:
---

在 Linux 下搭建 Samba Server，以 Ubuntu 18.04 为例。

> Samba is a free and open-source re-implementation of the [SMB/CIFS network file sharing protocol](https://docs.microsoft.com/en-us/windows/desktop/FileIO/microsoft-smb-protocol-and-cifs-protocol-overview) that allows end users to access files, printers, and other shared resources.

<!-- more -->

> **reference:** https://linuxize.com/post/how-to-install-and-configure-samba-on-ubuntu-18-04/

# 安装 Samba

~~~bash
sudo apt update
sudo apt install samba
~~~

安装完成后，Samba 服务会自动开启，可以用如下命令检查其状态：

~~~bash
sudo systemctl status smbd
~~~

结果类似这样：

~~~
● smbd.service - Samba SMB Daemon
   Loaded: loaded (/lib/systemd/system/smbd.service; enabled; vendor preset: enabled)
   Active: active (running) since Sun 2020-03-15 22:16:30 CST; 49min ago
     Docs: man:smbd(8)
           man:samba(7)
           man:smb.conf(5)
 Main PID: 1434 (smbd)
   Status: "smbd: ready to serve connections..."
    Tasks: 4 (limit: 4915)
   CGroup: /system.slice/smbd.service
           ├─1434 /usr/sbin/smbd --foreground --no-process-group
           ├─1436 /usr/sbin/smbd --foreground --no-process-group
           ├─1437 /usr/sbin/smbd --foreground --no-process-group
           └─1439 /usr/sbin/smbd --foreground --no-process-group

3月 15 22:16:30 fitz-MS-7B00 systemd[1]: Starting Samba SMB Daemon...
3月 15 22:16:30 fitz-MS-7B00 systemd[1]: Started Samba SMB Daemon.
~~~

# 配置防火墙

If you have a firewall running on your Ubuntu system you’ll need to allow incoming UDP connections on ports `137` and `138` and TCP connections on ports `139` and `445`.

~~~bash
sudo ufw allow 'Samba'
~~~

# 创建 Samba 用户和目录

1. 创建 Samba 根目录 (暂且这么说吧)：

   ~~~bash
   sudo mkdir /samba
   ~~~

   设置用户组，将 `/samba` 目录的用户组改为 `sambashare`：

   ~~~
   sudo chgrp sambashare /samba
   ~~~

2. 创建 Samba 普通用户：

   首先创建一个名为 `josh` 的用户：

   ~~~bash
   sudo useradd -M -d /samba/josh -s /usr/sbin/nologin -G sambashare josh
   ~~~

   > - `-M` -do not create the user’s home directory. We’ll manually create this directory.
   > - `-d /samba/josh` - set the user’s home directory to `/samba/josh`.
   > - `-s /usr/sbin/nologin` - disable shell access for this user.
   > - `-G sambashare` - add the user to the `sambashare` group.

   创建该用户的 `home` 目录：

   ~~~bash
   sudo mkdir /samba/josh
   sudo chown josh:sambashare /samba/josh
   sudo chmod 2770 /samba/josh
   ~~~

   > `chmod` 命令说明：
   >
   > This command here will add the setgid bit to the `/samba/josh` directory so the newly created files in this directory will inherit the group of the parent directory. This way, no matter which user creates a new file, the file will have group-owner of `sambashare`. For example, if you don’t set the directory’s permissions to `2770` and the `sadmin` user creates a new file the user `josh` will not be able to read/write to this file.

   将用户添加到 Samba 数据库中，同时设置的 Samba 密码：

   ~~~bash
   sudo smbpasswd -a josh
   ~~~

   在 Samba 中启用该用户：

   ~~~bash
   sudo smbpasswd -e josh
   ~~~

3. 创建 Samba 管理员用户：

   过程与创建普通用户类似。

   首先创建名为 `sadmin` 的用户：

   ~~~bash
   sudo useradd -M -d /samba/users -s /usr/sbin/nologin -G sambashare sadmin
   ~~~

   设置密码并启用该用户：

   ~~~bash
   sudo smbpasswd -a sadmin
   sudo smbpasswd -e sadmin
   ~~~

   创建用户的 `home` 目录 (同时也是 Samba 共享目录)：

   ~~~bash
   sudo mkdir /samba/users
   sudo chown sadmin:sambashare /samba/users
   sudo chmod 2770 /samba/users
   ~~~

# 配置 Samba 共享：

编辑文件 `/etc/samba/smb.conf` ，加入如下内容：

~~~
[users]
    path = /samba/users
    browseable = yes
    read only = no
    force create mode = 0660
    force directory mode = 2770
    valid users = @sambashare @sadmin

[josh]
    path = /samba/josh
    browseable = no
    read only = no
    force create mode = 0660
    force directory mode = 2770
    valid users = josh @sadmin
~~~

> - `[users]` and `[josh]` - The names of the shares that you will use when logging in.
> - `path` - The path to the share.
> - `browseable` - Whether the share should be listed in the available shares list. By setting to `no` other users will not be able to see the share.
> - `read only` - Whether the users specified in the `valid users` list are able to write to this share.
> - `force create mode` - Sets the permissions for the newly created files in this share.
> - `force directory mode` - Sets the permissions for the newly created directories in this share.
> - `valid users` - A list of users and groups that are allowed to access the share. Groups are prefixed with the `@` symbol.

最后重启 Samba 服务：

~~~
sudo systemctl restart smbd
sudo systemctl restart nmbd
~~~



