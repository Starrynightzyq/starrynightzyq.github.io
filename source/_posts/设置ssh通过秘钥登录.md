---
title: 设置ssh通过秘钥登录
toc: true
date: 2020-04-25 23:53:08
categories: GEEK
updated: 2020-12-17 14:47:23tags: [GEEK, Linux]
description:
---

无论是个人的 VPS 还是企业允许公网访问的服务器，如果开放 22 端口的 SSH 密码登录验证方式，被众多黑客暴力猜解捅破菊花也可能是经常发生的惨剧。企业可以通过防火墙来做限制，普通用户也可能借助修改 22 端口和强化弱口令等方式防护，但目前相对安全和简单的方案则是让 SSH 使用密钥登录并禁止口令登录。

<!--more-->

# 本地电脑的设置（client）

生成 rsa 秘钥对

~~~bash
ssh-keygen -t rsa -C "youremail@example.com"
~~~

会在 *~/.ssh/* 目录下生成 *id_rsa* 和 *id_rsa.pub* 两个文件，分别为私钥和公钥。

# 服务器端的设置（server）

1. 在 */<username>/.ssh/* 目录下，创建文件 *authorized_keys*：

   ~~~bash
   touch /<username>/.ssh/authorized_keys
   ~~~

2. 将 client 的公钥里的内容复制到 server 的 *authorized_keys* 中（server 的 *authorized_keys* 中可以存放多个 client 的公钥，之间用换行隔开就行）。

3. 修改 */<username>/.ssh* 的权限为 700, *authorized_keys* 的权限为 600 或者更严格的 400，否则登录的时候会提示`server refuse you key`:

   ~~~bash
   chmod 700 /<username>/.ssh
   chmod 600 /<username>/.ssh/authorized_keys
   ~~~

4. 修改 ssh 的配置，使其允许秘钥登录：

   编辑 */etc/ssh/sshd_config* 文件，修改如下内容：

   ~~~
   RSAAuthentication yes
   PubkeyAuthentication yes
   AuthorizedKeysFile      .ssh/authorized_keys
   ~~~

   另外，请留意 root 用户能否通过 SSH 登录，最好进制 root 用户通过 SSH 登录：

   ```
   PermitRootLogin no
   ```

5. 重启 SSH 服务：

   ```bash
   service sshd restart
   ```

   这时查看一下是否可以使用秘钥登录，如果可以就可以禁用密码登录

6. 修改 ssh 的配置，禁用密码登录：

   编辑 */etc/ssh/sshd_config* 文件，修改如下内容：

   ~~~
   PasswordAuthentication no
   ~~~

7. 最后重启 SSH 服务：

   ~~~bash
   service sshd restart
   ~~~

   