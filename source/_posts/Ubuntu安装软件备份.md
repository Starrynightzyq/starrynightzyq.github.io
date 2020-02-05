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

   - [zsh-autosuggestion](https://github.com/zsh-users/zsh-autosuggestions)

     ~~~bash
     git clone https://github.com/zsh-users/zsh-autosuggestions ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions
     ~~~

     ~~~sh
     plugins=( [plugins...] zsh-autosuggestion) # 修改~/.zshrc
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



# 文本编辑器：sublime text 3

