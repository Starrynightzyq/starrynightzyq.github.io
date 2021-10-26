---
title: tinc 安装
toc: true
comments: true
date: 2021-08-29 14:02:19
updated: 2021-10-26 09:35:19
categories: Geek
tags: [Geek, tinc]
description: 
---

# What is tinc?

tinc is a Virtual Private Network (VPN) daemon that uses tunnelling and encryption to create a secure private network between hosts on the Internet. tinc is Free Software and licensed under the [GNU General Public License](https://www.gnu.org/licenses/old-licenses/gpl-2.0.html) version 2 or later. Because the VPN appears to the IP level network code as a normal network device, there is no need to adapt any existing software. This allows VPN sites to share information with each other over the Internet without exposing any information to others.

<!--more-->

# Install

> Ref:
>
> [Starrynightzyq/tinc-config](https://github.com/Starrynightzyq/tinc-config)
>
> https://blog.lvaohui.top/article/202101251558/
>
> Mac: https://chanix.github.io/TincCookbook/examples/4-HowToInstallTincOnMacOSMojave.html
>
> Ansible 部署(快速部署大规模的 tinc 网络): [https://wener.me/notes/howto/network/tinc-multi-path-failover](https://wener.me/notes/howto/network/tinc-multi-path-failover/#ansible-%E9%83%A8%E7%BD%B2)

# Use

~~~
debug: tincd -n netname -d5 -D
start command: sudo tincd -n netname
stop command: sudo tincd -n netname -k
use systemctl enable tinc@netname to enable individual networks
~~~

