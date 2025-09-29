---
title: svn 切换分支后合并一段时间内的 commit
toc: true
comments: true
date: 2025-09-29 09:45:57
updated: 2025-09-29 10:22:24
categories: svn
tags: [svn]
description: 当从一个branch切换到trunk时，如何将branch上自己提交的commit全部合并到trunk中
---

# 前提

从 trunk 创建一个 branch，然后在 branch 上进行开发，开发一段时间后，再切换回 trunk，这时需要把 branch 上自己提交的 commit 合并到 trunk 中。

# 方法

1. 获取 branch 上自己提交的 commit 的 id；
   
   可以通过 `svn log --stop-on-copy` 获取这个 branch 上所有的 commit log。

   在 branch 目录下执行如下命令，将获得的版本号记录下来：

   ```bash
   svn log --stop-on-copy | grep -A 2 "^r"  | grep -A 2 <your name>
   ```
   
   命令说明：

   - `svn log --stop-on-copy` 获取这个 branch 上所有的 commit log；
   - `grep -A 2 "^r"` 获取所有以 "r" 开头的行，即所有 commit 的 id 所在行， `-A 2` 表示获取该行之后的 2 行，即 commit log；
   - `grep -A 2 <your name>` 获取所有以 "\<your name\>" 开头的行，即所有自己提交的 commit 的 id 所在行， `-A 2` 表示获取该行之后的 2 行，即 commit log；

2. 通过 commit id 将 branch 上自己提交的 commit merge到 trunk 中；
   
   可以通过 `svn merge -c <commit id> <branch url> <trunk url>` 将 branch 上指定的 commit merge到 trunk 中。

   如果在第1步中获取到的 commit id 为 1234、1256、1289，在 trunk 目录下执行命令：

   ```bash
   svn merge -c 1234 -c 1256 -c 1289 <branch-url>
   ```

   命令说明：

   - `-c <commit id>` 表示指定要 merge 的 commit id；
   - `<branch-url>` 表示 branch 的 url，可以通过在 branch 目录下执行 `svn info` 命令获取；
