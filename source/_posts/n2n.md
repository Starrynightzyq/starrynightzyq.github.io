---
title: n2n 安装及使用
toc: true
comments: true
date: 2022-07-16 10:00:55
updated: 2022-08-29 10:00:55
categories: Geek
tags: [Geek, n2n]
description: 内网穿透工具，相比于 tinc 部署更加方便
---

# N2N 介绍

## N2N 的一些相关概念

N2N 官方对里面的角色有一些定义，在开始部署前，了解这些定义，能够帮助你快速理解这个软件的使用。

1. SuperNode 超级节点

   SuperNode 相当与注册中心, 它会记录边缘节点的连接信息，告诉各个边缘节点如何去找到其它的边缘节点。如果超级节点发生故障，那么边缘节点之间将不能正常的进行通信。在整个N2N网络中必须至少拥有一个SuperNode。

2. Edge 边缘节点

   边缘节点是指所有通过 SuperNode 组网而成的节点，无论你处于哪个位置哪种网络环境下，edge节点之间都能进行通信。
   一台计算机可以拥有多个edge, 局域网根据子网掩码来决定两台机器是否处于同一个网段，而edge需要添加一组账号密码，在N2N 里面称作 GroupName 和 password ，Group0 和 Group 1 里面的 10.0.0.1 是不一样的。

## 项目地址

**目前最常用的版本**，也是官方N2N项目重启后，在各路大神的贡献下，一直在维护并不断完善的版本

项目：https://github.com/ntop/n2n

# 安装 (3.0-stable)

## Ubuntu

1. 安装编译工具

   ~~~bash
   sudo apt-get install cmake libssl-dev
   sudo apt-get install build-essential
   ~~~

2. 编译、安装 N2N

   ~~~bash
   git clone https://github.com/ntop/n2n.git
   cd n2n
   git checkout 3.0-stable
   ./autogen.sh
   ./configure
   make
   sudo make install
   ~~~

## OpenWrt

在github找到一个别人编译好的

https://github.com/csrutil/n2n

~~~bash
wget https://github.com/csrutil/n2n/releases/download/3.0.0/n2n-edge_3.0.0-1_aarch64_generic.ipk
opkg install ./n2n-edge_3.0.0-1_aarch64_generic.ipk
~~~

## Mac (macOS Big Sur 11.6.6)

安装必要的软件：

~~~bash
brew tap homebrew/cask
brew install tuntap --cask
brew install openssl
brew install cmake
~~~

下载 n2n 的源码

~~~bash
git clone https://github.com/ntop/n2n.git
git checkout 3.0-stable
~~~

编译&安装

~~~bash
cd n2n
mkdir -p build
cd build
cmake ..
make
sudo make install
~~~

> 在 `make install` 的过程中遇到如下错误：
>
> ~~~bash
> CMake Error at cmake_install.cmake:79 (file):
>   file INSTALL cannot copy file
>   "/Users/zhouyuqian/MyDocuments/my_scripts/n2n/build/doc/edge.8.gz" to
>   "/usr/share/man/man8/edge.8.gz": Read-only file system.
> ~~~
>
> 需要手动将 `cmake_install.cmake` 文件中的 `/usr/share/`替换为 `/usr/local/share/`

# 使用（网对网）

## SuperNode

1. 编辑配置文件 `/etc/n2n/supernode.conf` 

   ~~~bash
   -p=1234
   ~~~

   > -p=1234 是supernode的服务端口，防火墙中要放行该端口的tcp和upd

2. 编辑systemctl的启动文件

   ~~~bash
   sudo vim /lib/systemd/system/edge.service
   ~~~

   ~~~bash
   [Unit]
   Description=n2n supernode process
   After=network-online.target syslog.target
   Wants=network-online.target
   
   [Service]
   Type=simple
   ExecStart=/usr/sbin/supernode /etc/n2n/supernode.conf -f
   Restart=on-abnormal
   RestartSec=5
   
   [Install]
   WantedBy=multi-user.target
   Alias=
   ~~~

3. 启动

   ~~~
   sudo systemctl enable supernode
   sudo systemctl start supernode
   ~~~

   or（测试时使用）
   
   ~~~bash
   sudo supernode /etc/n2n/supernode.conf -v -f
   ~~~

## Edge

1. n2n的虚拟网卡必须指定IP

2. 路由器的局域网网段必须不一样，比如A路由器192.168.31.0/24，B路由器192.168.12.0/24

3. 必须把n2n的虚拟网卡添加进防火墙n2n（网络>>>接口，添加新接口，不配置协议，防火墙区域指定n2n）

4. 新建防火墙规则：

   
   
   

### openwrt路由器A (所在局域网192.168.31.0/24)

Edit `/etc/n2n/edge.conf` and add the following

~~~bash
-d=n2n0
-c=n2n_net0
-k=<encryption key>
-a=10.10.10.3/24
-p=53001
-l=<super node ip>:<port>
-r
-n=192.168.12.0/24:10.10.10.2
~~~

> -d: TAP device name (网卡名)
>
> -c: n2n community name the edge belongs to
>
> -k: encryption key (ASCII)
>
> -a: 设置此N2N网络中，本机的IP地址
>
> -p: fixed local UDP port and optionally bind to the
>
> -l: supernode ip address or name, and port

启动n2n

~~~bash
edge /etc/n2n/edge.conf -f
~~~

or

~~~bash
/etc/init.d/edge enable
/etc/init.d/edge start
~~~

### openwrt路由器B (所在局域网192.168.12.0/24)

Edit `/etc/n2n/supernode.conf` and add the following

~~~bash
-d=n2n0
-c=n2n_net0
-k=<encryption key>
-a=10.10.10.2/24
-p=53001
-l=<super node ip>:<port>
-r
-n=192.168.31.0/24:10.10.10.3
~~~

### Mac

创建conf文件 `/etc/n2n/edge.conf`，内容如下：

~~~bash
-c=n2n_net0
-k=<encryption key>
-a=10.10.10.4/24
-p=53001
-l=<super node ip>:<port>
~~~

启动 n2n

~~~bash
sudo edge /etc/n2n/edge.conf
# or
sudo edge /etc/n2n/edge.conf -f 
~~~

创建启动脚本 `n2nup.sh`

~~~bash
#!/bin/bash

DelRoute(){
    sudo route delete 10.10.10.0/24
    sudo route delete 192.168.12.0/24
    sudo route delete 192.168.31.0/24
}

SetRoute(){
    sudo route -n add -net 192.168.12.0 -netmask 255.255.255.0 10.10.10.2
    # sudo route -n add -net 192.168.31.0 -netmask 255.255.255.0 10.10.10.3
}

CheckStatus(){
    if [ `grep -c "OK" "/var/log/n2n/edge.log"` -ne '0' ]
    then
        echo "OK"
        return 1
    else
        echo "wait for connection"
        return 0
    fi
}

DelRoute
sudo edge /etc/n2n/edge.conf -f > /var/log/n2n/edge.log  2>&1 &
while :
do
    CheckStatus
    if [ $? == '0' ];then
        sleep 2
    else
        break
    fi
done
sleep 2
SetRoute
~~~

创建停止脚本 `n2ndown.sh`

~~~bash
#!/bin/bash
sudo route delete 10.10.10.0/24
sudo route -v delete -net 192.168.12.0 -gateway 10.10.10.2
sudo route -v delete -net 192.168.31.0 -gateway 10.10.10.3
ps -A | grep n2n | grep -v grep | grep -v n2ndown | awk '{print $1}' | xargs -n 1 sudo kill -9
~~~

### Ubuntu

~~~bash
sudo vim /lib/systemd/system/edge.service.
~~~

~~~bash
[Unit]
Description=n2n edge process
After=network-online.target syslog.target
Wants=network-online.target

[Service]
Type=simple
ExecStart=/usr/sbin/edge /etc/n2n/edge.conf -f
Restart=on-abnormal
RestartSec=5

[Install]
WantedBy=multi-user.target
Alias=edge.service
~~~

