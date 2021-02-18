---
title: Config static IP address on Ubuntu 18.04
toc: true
date: 2020-03-21 14:14:19
categories: Linux
updated: 2020-03-21 17:30:13tags: [Linux, GEEK]
description:
---

Netplan network configuration had been first introduced to Ubuntu 18.04 LTS Bionic Beaver. It is available to all new Ubuntu 18.04 installations.

<!-- more -->

当前的 `netplan` 配置文件在 `/etc/netplan/` 目录下，查看当前的配置文件：

~~~bash
cat /etc/netplan/01-network-manager-all.yaml
~~~

> 这里的 `01-network-manager-all.yaml` 桌面版和服务器版的名字不一样

结果如下：

~~~yaml
# This file describes the network interfaces available on your system
# For more information, see netplan(5).
network:
  version: 2
  renderer: NetworkManager
  ethernets:
    eno1:
      dhcp4: yes
~~~

可以看到默认的 IP 配置是 DHCP，将其改为静态 IP：

~~~yaml
# Let NetworkManager manage all devices on this system
network:
  version: 2
  renderer: networkd
  ethernets:
    eno1:
      dhcp4: no
      dhcp6: no
      addresses: [192.168.0.100/24, ]       # IP 地址/子网掩码长度
      gateway4:  192.168.0.1                # 网关
      nameservers:
              addresses: [8.8.8.8, 8.8.4.4] # DNS 服务器
~~~

然后是配置生效：

~~~bash
sudo netplan apply
~~~

或者：

~~~bash
sudo netplan --debug apply
~~~

