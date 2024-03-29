---
title: ZFS on Ubuntu
toc: true
comments: true
date: 2021-04-02 10:16:20
updated: 2021-04-02 10:16:20
categories: GEEK
tags: [GEEK, Linux]
description: ZFS 文件系统安装过程
---

# 安装

> https://openzfs.github.io/openzfs-docs/Getting%20Started/Ubuntu/index.html#installation
>
> https://manpages.debian.org/unstable/zfsutils-linux/zfs-mount-generator.8.en.html

# 创建 zpool

先查看硬盘的 id

~~~bash
ls -al /dev/disk/by-id
~~~

创建了一个名为 tank 的新池，mirror格式

~~~bash
sudo zpool create tank mirror /dev/disk/by-id/xxxxxxx1 /dev/disk/by-id/xxxxxxx2
~~~

查看存储池列表

~~~
zfs list
~~~

![截屏2021-04-02 上午10.24.51](https://pic.zhouyuqian.com/img/20210727233648.png)

查看存储池的状态信息

~~~bash
zpool status tank
~~~

![截屏2021-04-02 上午10.26.21](https://pic.zhouyuqian.com/img/20210727233649.png)

## 其他命令：

显示 ZFS 存储池命令历史记录
`zpool history`

查看 ZFS 存储池的 I/O 统计信息
`zpool iostat`

销毁存储池
`zpool destroy zpoolname`

向存储池添加设备
`zpool add tank c2t1d0 #向存储池tank中添加设备`

## 数据压缩

数据压缩默认是关闭的，使用如下命令打开：

~~~bash
zfs set compression=lz4 tank
~~~

# ZFS 文件系统

## 创建文件系统

~~~bash
zfs create tank/home
sudo zfs create -o mountpoint=/home/EDA tank/EDA
~~~

在 tank 中创建了一个名为 home 的文件系统，如果新文件系统创建成功，则 ZFS 会自动挂载该文件系统。

## 销毁文件系统

~~~bash
zfs destroy tank/home # 销毁tank/home 文件系统
~~~

如果要销毁的文件系统处于繁忙状态而无法取消挂载，则 zfs destroy 命令将失败。要销毁活动文件系统，请使用 -f 选项。由于此选项可取消挂载、取消共享和销毁活动文件系统，从而导致意外的应用程序行为，因此请谨慎使用此选项。

## 重命名文件系统

~~~bash
zfs rename tank/test2 tank/testrename # 将文件系统 tank/test2 重命名为 /tankrename
~~~

## ~~~将 ZFS 文件系统挂载到 /home~~~

~~~bash
sudo rsync -avh /home/* /tank/home
sudo rm -rf /home
sudo zfs set mountpoint=/home tank/home
~~~

使用 zfs-mount-generator 工具

> https://manpages.ubuntu.com/manpages/focal/man8/zfs-mount-generator.8.html

## 迁移用户目录

用 `zfs list` 命令可以看到用户目录是在 `rpool/USERDATA` 下的：

![截屏2021-04-02 下午3.19.58](https://pic.zhouyuqian.com/img/20210727233650.png)

我想把他们迁移到 HDD 硬盘的存储池 `tank` 里，直接修改挂载点的方法是不行的，新建一个用户后挂载点还会在原来的 `rpool/USERDATA` 下，在[此处](https://github.com/ubuntu/zsys/issues/132)找到了方法。

- create your pool2/USERDATA/ with the same dataset name than on the first pool
- ensure you have the same properties and **user properties** set on that dataset
- do a zfs send/recv between the 2 datasets
  Then, once ready, remove the second dataset.
- If you delete rpool/USERDATA, then the new users will be created under secondarypool/USERDATA!

1. 创建快照

   ~~~bash
   sudo zfs snapshot -r rpool/USERDATA@now
   ~~~

2. send/recv

   ~~~bash
   sudo zfs send -R rpool/USERDATA@now | sudo zfs receive -F tank/USERDATA
   ~~~

   这时可以看到 `tank/USERDATA` 和 `rpool/USERDATA` 的结构是相同的：

   ![截屏2021-04-02 下午3.32.16](https://pic.zhouyuqian.com/img/20210727233651.png)

3. 删除原来的 `rpool/USERDATA`：

   ~~~
   sudo zfs destroy -r -f rpool/USERDATA
   ~~~

   这个时候可以会提示 `umount: /home/fitz: target is busy.`，因为我想在就是在这个用户下操作的，所以删不掉这个目录，不过 `rpool/USERDATA/root_*` 已经删掉了，因此此时退出当前用户，换 root 登录，再次执行上面的命令，就可以把 `rpool/USERDATA` 全删掉了。

   现在再新建一个用户，可以看到新用户的目录是在 `tank/USERDATA` 下的。

# 快照和克隆

> https://www.howtoing.com/how-to-use-snapshots-clones-and-replication-in-zfs-on-linux
>
> https://docs.oracle.com/cd/E26926_01/html/E25826/gbchp.html

- 创建快照

  ~~~bash
  zfs snapshot tank/home/matt@friday
  ~~~

  创建一个 `tank/home/matt` 的快照，其名称为 `friday`。

  `-r` 选项可为所有后代文件系统创建快照。

- 列出快照

  ~~~bash
  zfs list -t snapshot
  ~~~

- 回滚快照

  ~~~bash
  zfs rollback tank/home/matt@tuesday
  ~~~

  将 `tank/home/matt` 文件系统回滚到 `tuesday` 快照

  **要回滚到早期快照，必须销毁所有的中间快照。可以通过指定 `-r` 选项销毁早期的快照。**

- 确定 ZFS 快照的差异 (`zfs diff`)

  可以使用 `zfs diff` 命令确定 ZFS 快照的差异。

  ~~~bash
  zfs diff tank/home/tim@snap1 tank/home/tim@snap2
  ~~~

- 删除快照

  ~~~bash
  zfs destory <-r> <snapshot name>
  ~~~
  
- 删除多个快照 [ref](https://qastack.cn/server/340837/how-to-delete-all-but-last-n-zfs-snapshots)

  ```bash
  zfs list -t snapshot -o name | grep ^tank@Auto | tac | tail -n +16 | xargs -n 1 zfs destroy -r 
  ```

  - 使用`zfs list -t snaphot -o name`输出快照列表（仅限`zfs list -t snaphot -o name`
  - 通过`grep ^tank@Auto`只保留那些与`tank@Auto`匹配的文件
  - 用`tac`反转列表（先前从最旧到最新）
  - 将输出限制为第16个最早的结果，并跟随`tail -n +16`
  - 然后用`xargs -n 1 zfs destroy -vr`

  按照相反的顺序删除快照据说更有效率。

  或按照与创build相反的顺序进行sorting

  ```
   zfs list -t snapshot -o name -S creation | grep ^tank@Auto | tail -n +16 | xargs -n 1 zfs destroy -vr 
  ```

  使用`...|xargs -n 1 echo`testing它
  
  
# 自动快照

https://blog.vgot.net/archives/zfsnap.html

https://serverfault.com/questions/855895/how-to-set-the-number-of-snapshots-zfs-auto-snapshot-should-retain

http://knowledgebase.45drives.com/kb/setting-up-zfs-auto-snapshots-in-linux/

https://www.yafa.moe/post/use-zfs-backup-system/#%E5%AE%9A%E6%9C%9F%E5%A4%87%E4%BB%BD

1. 安装 [zfs-auto-snapshot](https://github.com/zfsonlinux/zfs-auto-snapshot)

	~~~bash
	sudo apt-get install zfs-auto-snapshot
	~~~
2. 默认情况下，它每15分钟为每个数据集创建一个快照，并保存长达1年的快照。但是，您可以通过将 `com.sun:auto-snapshot` 数据集属性设置为 `false` 来禁用特定数据集的快照：

   ~~~bash
   sudo zfs set com.sun:auto-snapshot=false tank/tmp
   ~~~

3. 您还可以使用 `com.sun:auto-snapshot:...` 属性来调整自动快照行为。例如，每天为 `tank/backup` 数据集保存快照31天：

   ~~~bash
   sudo zfs set com.sun:auto-snapshot=true tank/backup
   sudo zfs set com.sun:auto-snapshot:monthly=false tank/backup
   sudo zfs set com.sun:auto-snapshot:weekly=false tank/backup
   sudo zfs set com.sun:auto-snapshot:daily=true tank/backup
   sudo zfs set com.sun:auto-snapshot:hourly=false tank/backup
   sudo zfs set com.sun:auto-snapshot:frequent=false tank/backup
   ~~~

   获取 `com.sun:auto-snapshot:...` 属性：

   ~~~bash
   zfs get com.sun:auto-snapshot <name>
   ~~~

4. 默认情况下，脚本保存：

   - 每15分钟快照一次，保留4个快照
   - 每小时每小时快照，保留24个快照
   - 每天的快照，保留31个快照
   - 每周每周快照，保留7个快照
   - 每月每月快照，保留12个快照

# ~~备份整个系统&恢复~~

> https://www.thegeekdiary.com/how-to-backup-and-restore-zfs-root-pool-in-solaris-10/



> Reference:
>
> https://wiki2.xbits.net:4430/storage:zfs:zfs%E6%89%8B%E5%86%8C#zfs_send_receive
>
> https://aws.amazon.com/cn/blogs/china/architecture-and-practice-of-shared-storage-system-based-on-zfs-for-eda-scenario/

# 迁移

> Ref: https://docs.oracle.com/cd/E24847_01/html/819-7065/gbchy.html

- 弹出

  ~~~bash
  zpool export tank
  ~~~

- 导入

  ~~~bash
  zpool import # 查看可导入的 pool，实际上不会执行任何操作
  ~~~

  ~~~bash
  zpool import <pool_name> # 导入 pool
  ~~~

  

