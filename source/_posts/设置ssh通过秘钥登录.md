---
title: 设置ssh通过秘钥登录
toc: true
date: 2020-04-25 23:53:08
categories: GEEK
updated: 2021-04-11 14:47:23
tags: [GEEK, Linux]
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

   

# more

## 查看登录记录

~~~bash
last -x -F
~~~

or

~~~bash
# 登录成功的记录
less /var/log/auth.log|grep 'Accepted' # Ubuntu
less /var/log/secure|grep 'Accepted' # Centos
# 登录失败
less /var/log/auth.log | grep "Connection closed"
~~~

## 换端口

修改文件 */etc/ssh/sshd_config*：

找到 Prot，改为想要的端口。

然后重启sshd服务：

~~~bash
sudo systemctl restart sshd
~~~

修改防火墙，放行新的端口，同时关闭旧端口：

~~~bash
sudo ufw allow 1122 # 放行新的端口
sudo ufw delete allow 22 # 禁止外部访问 22 端口 # or sudo ufw delete allow ssh
sudo ufw status # 查看防火墙状态
sudo ufw logging on # 打开防火墙日志，位于 /var/log/ufw.log
~~~

## ~~限制连续登录次数~~(好像使用秘钥登录后，这个就不用管了)

在 */etc/pam.d/sshd* 文件第一行（最前面）添加如下内容：

~~~bash
auth required pam_tally2.so deny=3 unlock_time=3600 even_deny_root root_unlock_time=3600
~~~

deny=3 表示尝试登录次数,超过3次后会执行后续动作,单位为秒
even_deny_root 对root也开启此限制

查看登录失败次数：

~~~bash
sudo pam_tally2 --user <user>
~~~

设置重复验证次数，默认6次

编辑 SSH 配置文件 */etc/ssh/sshd_­con­fig*：

在 ssh 配置文件中查找 #Max­Au­thTries 修改为：
Max­Au­thTries 3 #错误 3 次即断开连接

