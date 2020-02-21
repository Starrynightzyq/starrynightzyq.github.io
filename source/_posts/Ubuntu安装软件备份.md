---
title: Ubuntu安装软件备份
toc: true
date: 2020-02-05 15:18:27
categories: GEEK
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

5. 安装oh-my-zsh插件

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

## 安装gnome-tweak-tool

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

# 主题&图标

我比较喜欢的是

- [Flatabulous](https://github.com/anmoljagetia/Flatabulous) 
- [arc-theme](https://github.com/horst3180/arc-theme)
- [flat-remix-gnome](https://github.com/daniruiz/flat-remix-gnome)