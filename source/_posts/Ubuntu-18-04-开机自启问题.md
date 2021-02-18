---
title: Ubuntu 18.04 开机自启问题
toc: true
date: 2020-03-11 18:07:19
categories: GEEK
updated: 2020-03-12 15:22:31tags: [GEEK, Linux]
description:
---

Ubuntu 18.04 使用 systemctl 命令来替换了 service 和 chkconfig 的功能。主要是开机启动比以前复杂多了。systemd 默认读取 `/etc/systemd/system/` 下的配置文件，该目录下的文件会链接 `/lib/systemd/system/` 下的文件。

<!-- more -->

执行 `ls /lib/systemd/system` 可以看到有很多启动脚本，其中就有我们需要的 `rc.local.service`

打开脚本内容（如果没有就创建）：

~~~bash
#  This file is part of systemd.
#
#  systemd is free software; you can redistribute it and/or modify it
#  under the terms of the GNU Lesser General Public License as published by
#  the Free Software Foundation; either version 2.1 of the License, or
#  (at your option) any later version.

# This unit gets pulled automatically into multi-user.target by
# systemd-rc-local-generator if /etc/rc.local is executable.
[Unit]
Description=/etc/rc.local Compatibility
Documentation=man:systemd-rc-local-generator(8)
ConditionFileIsExecutable=/etc/rc.local
After=network.target

[Service]
Type=forking
ExecStart=/etc/rc.local start
TimeoutSec=0
RemainAfterExit=yes
GuessMainPID=no
~~~

**一般正常的启动文件主要分成三部分**

> [Unit] 段: 启动顺序与依赖关系
> [Service] 段: 启动行为,如何启动，启动类型
> [Install] 段: 定义如何安装这个配置文件，即怎样做到开机启动

可以看出，/etc/rc.local 的启动顺序是在网络后面，但是显然它少了 Install 段，也就没有定义如何做到开机启动，所以显然这样配置是无效的。 因此我们就需要在后面帮他加上 [Install] 段:

```bash
[Install]  
WantedBy=multi-user.target  
Alias=rc-local.service
```

所以完整的 `rc.local.service` 文件是这样的：

~~~bash
[Unit]
Description=/etc/rc.local Compatibility
Documentation=man:systemd-rc-local-generator(8)
ConditionFileIsExecutable=/etc/rc.local
After=network.target

[Service]
Type=forking
ExecStart=/etc/rc.local start
TimeoutSec=0
RemainAfterExit=yes
GuessMainPID=no

[Install]
WantedBy=multi-user.target
Alias=rc-local.service
~~~

这里需要注意一下，ubuntu-18.04 server 版默认是没有 /etc/rc.local 这个文件的，需要自己创建：

```bash
sudo touch /etc/rc.local
```

然后把你需要启动脚本写入 /etc/rc.local ，我们不妨写一些测试的脚本放在里面，以便验证脚本是否生效.

```bash
#!/bin/sh -e
#
# rc.local
#
# This script is executed at the end of each multiuser runlevel.
# Make sure that the script will "exit 0" on success or any other
# value on error.
#
# In order to enable or disable this script just change the execution
# bits.
#
# By default this script does nothing.
echo "看到这行字，说明添加自启动脚本成功。" > /usr/local/test.log
exit 0
```

记得给加上执行权限：

```bash
sudo chmod +x /etc/rc.local
```

前面我们说 systemd 默认读取 /etc/systemd/system 下的配置文件, 所以还需要在 /etc/systemd/system 目录下创建软链接：

~~~bash
ln -s /lib/systemd/system/rc.local.service /etc/systemd/system/
~~~

还有最后一步，启用服务、启动服务并检查状态

~~~
sudo systemctl enable rc-local.service
sudo systemctl start rc-local.service
sudo systemctl status rc-local.service
~~~

重启并检查test.log文件

`cat /usr/local/test.log`

