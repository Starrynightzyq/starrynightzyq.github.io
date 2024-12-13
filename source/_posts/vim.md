---
title: Vim 命令记录
toc: true
comments: true
date: 2021-09-27 20:05:45
updated: 2024-12-13 17:43:03
categories: Geek
tags: [Geek, Vim]
description:
---

<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/9/9f/Vimlogo.svg/1024px-Vimlogo.svg.png" alt="Vim" style="zoom:33%;" />

<!--more-->

# 键盘操作

## 移动光标

### 简单的移动

`h`, `j`, `k`, `l`

配合数字：

`2j` 表示向下移动2行

### 利用查找

`/hello`

向后查找关键词 hello，回车就到了后面第一个 hello 处。

`?hello`

向前查找关键词 hello。

### 以word为单位进行移动

`w`, `b`

同理，配合数字:

`2w` 表示向后移动2个word；

`2b` 表示向前移动2个word；

`2e` 表示向后移动2个word，但是会移动到word字符之后。

如果想忽略标点符号的word，就用大写

`W`, `B`, `E`

### 移动到行首行尾（适合行内移动）

`^` 表示移动到行首第一个word，即行首有空格的情况，不会移动到空格之前，而是移动到空格之后，第一个word之前；

`0` 表示移动到行首；即行首有空格的情况，会移动到空格之前；

`$` 表示移动到行末；即行末有空格的情况，会移动到空格之后；

如果想移动到行末最后一个非空白的字符处，就输入命令 `$b`。一般来说，写代码，行末不会有空格存在的。这条应用没多大意义。

### 移动到文本开头和文本结尾（适合大范围移动）

`gg` 表示移动到文本开头；

`G` 表示移动到文本结尾；

### 利用行号移动到某一行（适合大范围移动）

`:123` 表示移动到第123行；

## 翻页

### 整页翻页

`ctrl-f` f 就是 forword

`ctrl-b` b 就是 backward

### 翻半页
`ctrl-d` d 就是 down

`ctrl-u` u 就是 up

## 插入

`i` 实现的是在光标之前的插入；

`I` 大写的i实现在光标所在行的最前面插入；

`a` 实现在光标后插入；

`A` 实现在光标所在行的行尾插入；

`o` 实现在光标所在行的上方插入新行；

`O` 是现在光标坐在行的下方插入新行；

## 窗口分割

### 分屏启动 vim

1. 使用大写的 O 参数来垂直分屏。

   ```bash
   vim -On file1 file2 ...
   ```

2. 使用小写的 o 参数来水平分屏。

   ```bash
   vim -on file1 file2 ...
   ```

### 关闭分屏

1. 关闭当前窗口。

   ```
   Ctrl+W c
   ```

2. 关闭当前窗口，如果只剩最后一个了，则退出Vim。

   ```
   Ctrl+W q
   ```

### 分屏

1. 上下分割当前打开的文件。

   ```
   Ctrl+W s
   ```

2. 上下分割，并打开一个新的文件。

   ```
   :sp filename
   ```

3. 左右分割当前打开的文件。

   ```
   Ctrl+W v
   ```

4. 左右分割，并打开一个新的文件。

   ```
   :vsp filename
   ```

### 移动光标

Vim 中的光标键是 `h`, `j`, `k`, `l` (左，上，下，右)，要在各个屏间切换，只需要先按一下 `Ctrl+W`

1. 把光标移到

   右边的屏。

   ```
   Ctrl+W l
   ```

2. 把光标移到

   左边的屏中。

   ```
   Ctrl+W h
   ```

3. 把光标移到

   上边的屏中。

   ```
   Ctrl+W k
   ```

4. 把光标移到

   下边的屏中。

   ```
   Ctrl+W j
   ```

5. 把光标移到

   下一个的屏中。

   ```
   Ctrl+W w
   ```

### 移动分屏

这个功能还是使用了Vim的光标键，只不过都是大写。当然了，如果你的分屏很乱很复杂的话，这个功能可能会出现一些非常奇怪的症状。

1. 向右移动。

   ```
   Ctrl+W L
   ```

2. 向左移动

   ```
   Ctrl+W H
   ```

3. 向上移动

   ```
   Ctrl+W K
   ```

4. 向下移动

   ```
   Ctrl+W J
   ```

### 屏幕尺寸

下面是改变尺寸的一些操作，主要是高度，对于宽度你可以使用 `Ctrl+W <` 或是 `Ctrl+W >`，但这可能需要最新的版本才支持。

1. 让所有的屏都有一样的高度。

   ```
   Ctrl+W =
   ```

2. 增加高度。

   ```
   Ctrl+W +
   ```

   ~~~bash
   :reszie -5
   ~~~

3. 减少高度。

   ```
   Ctrl+W -
   ```

   ~~~bash
   :reszie +5
   ~~~

4. 改变宽度

   ~~~bash
   :vertical reszie +5
   ~~~


## 全局替换

~~~bash
:%s/old/new/g
~~~

## 多行注释

### 插入注释

用 `v` 进入virtual模式；

用上下键选中需要注释的行数；

按 `Control+v`（win下面 `ctrl+q`）进入列模式；

按大写 `I` 进入插入模式，输入注释符 "#" 或者是 "//"，然后立刻按下 `ESC`（两下）。

### 取消注释

`Ctrl + v` 进入块选择模式，选中你要删除的行首的注释符号，注意 "//" 要选中两个，选好之后按 `d` 即可删除注释。

## 撤销 & 反撤销

`u` 撤销；

`Ctrl + r` 反撤销；

## 快速删除

| 命令 | 注释                                     |
| ---- | ---------------------------------------- |
| x    | 删除光标所在后面的字符                   |
| X    | 删除光标所在前面的字符                   |
| d+e  | 删除光标所在位置到本单词末尾             |
| d+E  | 删除光标所在位置到本单词末尾包括标点符号 |
| d+b  | 删除光标所在位置到前面单词               |
| d+B  | 删除光标所在位置到前面单词包括标点符号   |
| d+d  | 删除一整行                               |
| d+0  | 删除光标所在位置到本行开头               |
| d+$  | 删除光标所在位置到本行末尾               |

## 复制

| 命令 | 注释                |
| ---- | ------------------- |
| yy   | 复制当前行          |
| nyy  | 从当前行开始复制n行 |
| dd   | 剪切当前行          |

## 移动行

| 命令 | 注释                |
| ---- | ------------------- |
| :m +1 | 下移 1 行 |
| :m -2 | 向上移动 1 行 |
|:m 3 |将行移动到第 3 行之后|

> PS：
>
> 可以用 `v` 选中多行后再移动

## 查看保存的版本和已编辑的相同文件的差异

`:w !diff % -`

## 重新载入文件/刷新文件

> 在 git 提交后，可以用这个命令刷新文件，刷新 gitdiff 的高亮

1. 重新载入当前文件：

    ~~~bash
    :e
    :e! # 放弃当前修改，强制重新载入
    ~~~

2. 重新载入所有打开的文件：

    ~~~bash
    :bufdo e
    :bufdo !e # 放弃当前修改，强制重新载入
    ~~~

# 配置

## 关闭 gVim 的声音、闪烁

在 `~/.vimrc` 中添加如下配置：

~~~vim
set vb t_vb=
au GuiEnter * set t_vb=
~~~

就要在 vim 中使用命令 `:help vb` 查看 visual bell 的帮助。

> ref: [windows下关闭gvim叮叮叮和闪屏](https://blog.csdn.net/zcube/article/details/44131925)

# [vim-plug](https://github.com/junegunn/vim-plug)

> Reference:
>
> https://vimjc.com/vim-plug.html

## Install

~~~bash
curl -fLo ~/.vim/autoload/plug.vim --create-dirs \
    https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim
~~~

## 安装插件

安装插件，只需要将插件写在 *.vimrc* 内，然后在 vim 中使用 `:PlugInstall` 命令即可：

~~~bash
# source ~/.vim/vim-init/init.vim
call plug#begin('~/.vim/plugged')
Plug 'HonkW93/automatic-verilog'
call plug#end()
~~~

## 删除插件

删除插件，只需要将写在 *.vimrc* 配置文件内的插件删除，重启 vim 并执行命令 `:PlugClean` 即可：

```bash
call plug#begin('~/.vim/plugged')
call plug#end()
```

保存在 vim 中使用 `:PlugClean`:

# [vim-init](https://github.com/Starrynightzyq/vim-init)

轻量级 Vim 配置框架，来自 [skywind3000](https://github.com/skywind3000/vim-init)，添加了 [automatic-verilog](https://github.com/Starrynightzyq/automatic-verilog)。

