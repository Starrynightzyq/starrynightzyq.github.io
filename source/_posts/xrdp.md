---
title: xrdp
toc: true
comments: true
date: 2021-04-02 18:35:51
updated: 2021-11-09 12:40:51
categories: GEEK
tags: [GEEK, Linux]
description: 安装 Xrdp
---

> reference：
>
> https://www.myfreax.com/how-to-install-xrdp-on-ubuntu-18-04/
>
> https://blog.csdn.net/weixin_45579994/article/details/112381567

# 安装 Xrdp

安装 xfce 桌面环境：

~~~
sudo apt-get install xfce4 xfce4-goodies xorg dbus-x11 x11-xserver-utils
~~~

或者安装 xubuntu 环境：

~~~bash
sudo apt-get install xubuntu-desktop
~~~

再安装 xrdp：

~~~
sudo apt-get install xrdp
sudo systemctl status xrdp
~~~

默认情况下，Xrdp 使用`/etc/ssl/private/ssl-cert-snakeoil.key`,它仅仅对“ssl-cert” 用户组成语可读。运行下面的命令，将`xrdp`用户添加到这个用户组：

```javascript
sudo adduser xrdp ssl-cert
```

重启 Xrdp 服务，使得修改生效：

```javascript
sudo systemctl restart xrdp
```

# ~~配置Xrdp~~

Xrdp配置文件位于 `/etc/xrdp` 目录中。对于基本的 Xrdp 连接，我们只需要配置 Xrdp 即可使用 Xfce。为此，打开以下文件：

`/etc/xrdp/xrdp.ini`

在文件末尾添加以下行：

```bash
exec startxfce4
```

保存文件并重新启动Xrdp服务：

```bash
sudo systemctl restart xrdp
```

# 配置 Xrdp（new）

```shell
echo xfce4-session > ~/.xsession
```

# 配置防火墙

默认情况下，Xrdp侦听所有接口上的端口`3389`。如果您在Ubuntu服务器上运行[防火墙](https://www.myfreax.com/how-to-setup-a-firewall-with-ufw-on-ubuntu-18-04/)（应始终这样做），则需要添加一条规则，以启用Xrdp端口上的流量。

要允许从特定的IP地址或IP范围访问Xrdp服务器，在此示例`192.168.1.0/24`中，请运行以下命令：

```bash
sudo ufw allow from 192.168.1.0/24 to any port 3389
```

如果您想允许从任何地方访问（出于安全原因强烈建议），请运行：

```bash
sudo ufw allow 3389
```

为了提高安全性，您可以考虑将Xrdp设置为仅在本地主机上侦听，并创建一个[ SSH隧道](https://www.myfreax.com/how-to-setup-ssh-tunneling/)，该隧道将安全地将流量从端口`3389`上的本地计算机转发到同一端口上的服务器。另一个安全选项是[安装OpenVPN ](https://www.myfreax.com/how-to-set-up-an-openvpn-server-on-ubuntu-18-04/)并通过专用网络连接到Xrdp服务器。

# 提高安全性：SSH Tunnel

在 client 上运行：

~~~bash
ssh -L 3380:localhost:3389 xrdp-server
~~~

表示通过 ssh tunnel 将本地的 3380 端口转发到远程服务器的 3389 端口。此时服务器上可以配置防火墙，关闭 3389 端口，只留下 ssh 端口。

在 client 上连接的时候服务器地址填写：

~~~
localhost:3380
~~~

# 问题： 远程桌面黑屏
解决方法：

```javascript
cd ~
touch .xsession
echo xfce4-session > ~/.xsession
sudo chown username:username .xsession
```

如果还是黑屏，重启一下试试。

# 问题2：键盘鼠标没反应

> https://github.com/neutrinolabs/xorgxrdp/issues/164

The fix for me was to add Option "CoreKeyboard" and Option "CorePointer" to the inputdevices in /etc/X11/xrdp/xorg.conf since the inputdevices in the serverlayout section are apparently ignored so no core pointer and keyboard exists, which leads to forced default devices. No idea why this is suddenly the case, it worked fine on ubuntu 18.04, but broke for me in 20.04.

```bash
Section "InputDevice"
    Identifier "xrdpKeyboard"
    Driver "xrdpkeyb"
    Option "CoreKeyboard"
EndSection

Section "InputDevice"
    Identifier "xrdpMouse"
    Driver "xrdpmouse"
    Option "CorePointer"
EndSection
```

# 问题3：“色彩管理设备” / “color managed device” 弹窗

> https://blog.csdn.net/wu_weijie/article/details/108481456

创建文件 */etc/polkit-1/localauthority/50-local.d/45-allow-colord.pkla* 并写入内容：

~~~shell
[Allow Colord all Users]
Identity=unix-user:*
Action=org.freedesktop.color-manager.create-device;org.freedesktop.color-manager.create-profile;org.freedesktop.color-manager.delete-device;org.freedesktop.color-manager.delete-profile;org.freedesktop.color-manager.modify-device;org.freedesktop.color-manager.modify-profile
ResultAny=no
ResultInactive=no
ResultActive=yes
~~~

