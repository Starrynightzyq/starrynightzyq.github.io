---
title: Ubuntu安装软件备份
toc: true
date: 2020-02-05 15:18:27
categories: GEEK
updated: 2021-08-28 15:21:15
tags: [Ubuntu, Linux, 软件]
description: 安装Ubuntu后要安装的一些软件
---

# shell：zsh

1. 安装zsh

   ~~~bash
   sudo apt-get install zsh
   ~~~

2. 查看shell列表

   ~~~bash
   cat /etc/shells
   ~~~

3. 切换shell为zsh

   ~~~bash
   chsh -s /bin/zsh
   ~~~

   **chsh 命令是改变登陆shell，需要重启才能看到效果。**

4. 安装[oh-my-zsh](https://ohmyz.sh/)

   ~~~bash
   sh -c "$(wget https://raw.github.com/ohmyzsh/ohmyzsh/master/tools/install.sh -O -)"
   ~~~

5. ~~安装oh-my-zsh插件~~

   - git # 自带

   - extract # 自带

     ~~~sh
     plugins=( [plugins...] extract) # 修改~/.zshrc
     ~~~

   - [autojump](https://github.com/wting/autojump)

     ~~~bash
     sudo apt-get install autojump # 安装
     ~~~

     ~~~sh
     plugins=( [plugins...] autojump) # 修改~/.zshrc
     ~~~

   - [zsh-autosuggestions](https://github.com/zsh-users/zsh-autosuggestions)

     ~~~bash
     git clone https://github.com/zsh-users/zsh-autosuggestions ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions
     ~~~

     ~~~sh
     plugins=( [plugins...] zsh-autosuggestions) # 修改~/.zshrc
     ~~~

   - [zsh-syntax-highlighting](https://github.com/zsh-users/zsh-syntax-highlighting)

     ~~~bash
     git clone https://github.com/zsh-users/zsh-syntax-highlighting.git ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting
     ~~~

     ~~~sh
     plugins=( [plugins...] zsh-syntax-highlighting) # 修改~/.zshrc
     ~~~

   - sublime
   
6. 安装oh-my-zsh插件 （new）

   ~~~bash
   sudo apt-get install autojump
   ~~~

   ~~~bash
   git clone https://github.com/zsh-users/zsh-autosuggestions ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions
   ~~~

   ~~~bash
   git clone https://github.com/zsh-users/zsh-syntax-highlighting.git ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting
   ~~~

   ~~~bash
   sed -i 's/ZSH_THEME="robbyrussell"/ZSH_THEME="ys"/g' ~/.zshrc
   ~~~

   ~~~bash
   sed -i 's/plugins=(git)/plugins=(git extract autojump zsh-autosuggestions zsh-syntax-highlighting)/g' ~/.zshrc
   ~~~

   ~~~bash
   source ~/.zshrc
   ~~~

# MarkDown编辑器：[Typaro](https://typora.io/)

~~~bash
# or run:
# sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys BA300B7755AFCFAE
wget -qO - https://typora.io/linux/public-key.asc | sudo apt-key add -

# add Typora's repository
sudo add-apt-repository 'deb https://typora.io/linux ./'
sudo apt-get update

# install typora
sudo apt-get install typora
~~~

# 中文输入法：搜狗输入法

> reference https://blog.csdn.net/lupengCSDN/article/details/80279177

1. 首先，安装Fcitx输入框架

   ~~~bash
   sudo apt-get install fcitx
   ~~~

2. 安装 [搜狗拼音](https://pinyin.sogou.com/linux/?r=pinyin)

   ~~~bash
   sudo dpkg -i sogou.deb 
   ~~~
   
   如果遇到依赖问题，执行
   
   ~~~bash
   sudo apt-get install -f
   ~~~
   
   后，重新安装。

**乱码问题**

~~~bash
fcitx -r # 重启fcitx框架
~~~

~~~bash
pidof fcitx|xargs kill
fcitx &
sogou-qimpanel &
~~~

~~~bash
cd ~/.config && rm -rf SogouPY* sogou*
reboot
~~~

``ctrl`` +``space``切换两次输入法

# 文本编辑器：[sublime text 3](https://www.sublimetext.com/docs/3/linux_repositories.html)

Install the GPG key:

```bash
wget -qO - https://download.sublimetext.com/sublimehq-pub.gpg | sudo apt-key add -
```

Ensure apt is set up to work with https sources:

```bash
sudo apt-get install apt-transport-https
```

Select the channel to use:

- Stable

  `echo "deb https://download.sublimetext.com/ apt/stable/" | sudo tee /etc/apt/sources.list.d/sublime-text.list `

- Dev

  `echo "deb https://download.sublimetext.com/ apt/dev/" | sudo tee /etc/apt/sources.list.d/sublime-text.list `

Update apt sources and install Sublime Text

```bash
sudo apt-get update
sudo apt-get install sublime-text
```

在`~/.zshrc` `plugins`里面添加`sublime`插件

~~~
plugins=( [plugins...] sublime) # 修改~/.zshrc
~~~

之后就可以用`subl`启动 sublime text 3 了

# 实时监控网速：NetSpeed

直接在``Ubuntu Software``里面搜索安装。

# 美化

Ubuntu 18.04 LTS与Ubuntu 16.04 LTS默认使用的桌面不一样，18.04为gnome3。

## ~~安装gnome-tweak-tool~~

~~~bash
sudo apt-get install gnome-tweak-tool
~~~

安装gnome-shell

> 参考http://ubuntuhandbook.org/index.php/2017/05/enable-shell-theme-in-gnome-tweak-tool-in-ubuntu/

~~~bash
sudo apt install chrome-gnome-shell
~~~

拓展：

[dash to dock](https://extensions.gnome.org/extension/307/dash-to-dock/)  优化 Ubuntu 默认的 dock

[User Themes](https://extensions.gnome.org/extension/19/user-themes/)    自定义 shell 主题

[Coverflow Alt-Tab](https://extensions.gnome.org/extension/97/coverflow-alt-tab/)  优化 Ubuntu 默认窗口切换动作

*[Gnome Global Application Menu](https://extensions.gnome.org/extension/1250/gnome-global-application-menu/)  将当前程序的菜单项提取到状态栏*

[NetSpeed](https://extensions.gnome.org/extension/104/netspeed/)    显示网速插件

[Clipboard Indicator](https://extensions.gnome.org/extension/779/clipboard-indicator/)  提供剪切板历史记录功能

*[Drop Down Terminal](https://extensions.gnome.org/extension/442/drop-down-terminal/)    可以从屏幕上快速弹出一个终端*

[Recent Items](https://extensions.gnome.org/extension/72/recent-items/)          快速打开最近打开过的文件

[Places Status Indicator](https://extensions.gnome.org/extension/8/places-status-indicator/)  利用下拉菜单快速打开驱动器上的常用位置

*[Dynamic Top Bar](https://extensions.gnome.org/extension/885/dynamic-top-bar/)      动态调整状态栏透明度*

[Hide top bar](https://extensions.gnome.org/extension/545/hide-top-bar/)    隐藏顶栏, 可以设置为鼠标靠近屏幕上边沿时显示顶栏

[Top Panel Workspace Scroll](Top Panel Workspace Scroll)    快速切换工作区

[Gravatar](https://extensions.gnome.org/extension/1015/gravatar/)    把你的 Ubuntu 用户头像设置成你的 Gravatar 头像.

[TopIcons Plus](https://extensions.gnome.org/extension/1031/topicons/)    将传统托盘图标移动到顶部面板 (Wine 程序救星)

按下 `Alt` + `F2`,输入 `r`，回车重启 gnome。

## 主题&图标

我比较喜欢的是

- [Flatabulous](https://github.com/anmoljagetia/Flatabulous) 
- [arc-theme](https://github.com/horst3180/arc-theme)
- [flat-remix-gnome](https://github.com/daniruiz/flat-remix-gnome)

## Ubuntu $\times$ KDE

### 安装 KDE

~~~bash
sudo apt-get install kubuntu-desktop
~~~

一路 OK，`Default display manager` 选 `sddm`，然后重启。

### 美化

监视器：[gotop](https://github.com/cjbassi/gotop)

终端：[konsole](https://konsole.kde.org/)

主题：[Orchis-kde](https://github.com/vinceliuice/Orchis-kde)

# 关闭图形化界面

> 参考 [Ubuntu桌面版关闭GUI环境](https://dslztx.github.io/blog/2017/08/27/Ubuntu桌面版关闭GUI环境/)

## **一、持久关闭**

查看当前的默认目标: 

~~~bash
systemctl get-default
~~~

执行以下命令，持久关闭Ubuntu桌面版的GUI环境（通过`Ctrl+Alt+F1-F6`快捷键进入命令行界面）：

```
sudo systemctl set-default multi-user.target
```

执行以下命令，持久开启Ubuntu桌面版的GUI环境（通过`Ctrl+Alt+F7`快捷键进入GUI界面）：

```
sudo systemctl set-default graphical.target
```

## **二、临时关闭**

执行以下命令，临时关闭Ubuntu桌面版的GUI环境：

```
sudo service lightdm stop
```

执行以下命令，临时开启Ubuntu桌面版的GUI环境：

```
sudo service lightdm start
```


参考文献： [1]https://askubuntu.com/questions/800239/how-to-disable-lightdmdisplay-manager-on-ubuntu-16-0-4-lts [2]https://askubuntu.com/questions/365719/i-have-to-restart-lightdm-after-run

> PS：
>
> 以上方法适用于 Ubuntu 和 Centos 7
>
> Centos 6 使用如下方法：
>
> 1. ## **临时关闭**
>
>    ~~~bash
>    init 3 # 临时关闭图形界面（XServer服务也会关闭）
>    ~~~
>
>    ~~~
>    # 再次开启图形界面用下面其中一个命令
>    init 5
>    startx
>    ~~~
>
> 2. ## 开机关闭
>
>    ```
>    vi /etc/inittab
>    ```
>
>    将
>
>    ```
>    id:5:initdefault:
>    ```
>
>    改成
>
>    ```
>    id:3:initdefault:
>    ```

# 增加 Swap 分区

1. 禁用 swap 功能

   ~~~
   sudo swapoff /swapfile
   ~~~

   这个命令执行之后，如果你用free命令查看的话会发现swap分区的大小变为了0。

2. 增加 /swapfile的大小：

   ```bash
   sudo dd if=/dev/zero of=/swapfile bs=1M count=30720 oflag=append conv=notrunc
   ```

   这个命令会在现有的/swapfile后面追加30GB，加上之前的2GB的swap分区，现在共有32个GB的swap分区了。

3. 设置这个文件为swap分区的挂载点：

   ```bash
   sudo mkswap /swapfile
   ```

4. 再次启用swap

   ~~~bash
   sudo swapon /swapfile
   ~~~


# 使用 screen 管理你的远程会话

1. 新建screen会话

   ~~~bash
   $ screen
   ~~~

   或者

   ~~~bash
   $ screen + command
   ~~~

2. 在已有screen会话中创建新的窗口

   `Ctrl`+`a` `c`

   Ctrl键+a键，之后再按下c键，screen 在该会话内生成一个新的窗口并切换到该窗口。

3. detached会话

   `C-a` `d`

4. 查看会话

   ~~~
   screen -ls
   ~~~

5. 恢复会话

   ~~~
   screen -r <screen_pid>
   ~~~

6. 清除dead会话

   ~~~
   screen -wipe
   ~~~

7. more

   C-a w 显示所有窗口列表
   C-a C-a 切换到之前显示的窗口
   C-a c 创建一个新的运行shell的窗口并切换到该窗口
   C-a n 切换到下一个窗口
   C-a p 切换到前一个窗口(与C-a n相对)
   C-a 0..9 切换到窗口0..9
   C-a a 发送 C-a到当前窗口
   C-a d 暂时断开screen会话
   C-a k 杀掉当前窗口

# 代替screen：tmux

> https://www.ruanyifeng.com/blog/2019/10/tmux.html

# 监测CPU温度：sensors

~~~
sudo apt-get install lm-sensors
~~~

使用

~~~
watch -n 2 sensors
~~~

> -n 2 表示每隔两秒刷新一次

# [MiniDLNA](https://help.ubuntu.com/community/MiniDLNA)

> 还没装好

# Samba

# Ubuntu下 firefox 无法观看视频的解决

提示缺少 flash 插件，此举解决的是html5的视频播放问题，flash不管了，谁还用flash啊。

~~~bash
sudo apt-get install ffmpeg
~~~

