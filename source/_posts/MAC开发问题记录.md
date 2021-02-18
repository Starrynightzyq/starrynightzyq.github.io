---
title: MAC开发问题记录
toc: true
date: 2020-03-04 13:49:06
categories: GEEK
updated: 2020-03-06 17:17:01tags: [GEEK, MAC]
description: 记录 MAC 环境下开发遇到的问题

---

# opencv-python

- 问题描述

  ~~~
  QFactoryLoader::QFactoryLoader() checking directory path "/usr/local/Cellar/python/3.7.6_1/Frameworks/Python.framework/Versions/3.7/Resources/Python.app/Contents/MacOS/platforms" ...
  qt.qpa.plugin: Could not find the Qt platform plugin "cocoa" in ""
  This application failed to start because no Qt platform plugin could be initialized. Reinstalling the application may fix this problem.
  ~~~

- 解决方法

  ~~~
  pip3 uninstall opencv-python
  pip3 install opencv-python-headless
  ~~~

- 原因

  `opencv-python-headless` ：与 `opencv-python` 相同但没有GUI功能。适用于无界面系统。

# proxychains-ng

- 问题描述

  ~~~
  [proxychains] config file found: /Users/zhouyugan/.proxychains/proxychains.conf
  [proxychains] preloading /usr/local/Cellar/proxychains-ng/4.14/lib/libproxychains4.dylib
  [proxychains] DLL init: proxychains-ng 4.14
  dyld: warning: could not load inserted library '/usr/local/Cellar/proxychains-ng/4.14/lib/libproxychains4.dylib' into hardened process because no suitable image found.  Did find:
  	/usr/local/Cellar/proxychains-ng/4.14/lib/libproxychains4.dylib: code signature in (/usr/local/Cellar/proxychains-ng/4.14/lib/libproxychains4.dylib) not valid for use in process using Library Validation: mapped file has no cdhash, completely unsigned? Code has to be at least ad-hoc signed.
  	/usr/local/Cellar/proxychains-ng/4.14/lib/libproxychains4.dylib: stat() failed with errno=1
  Cloning into 'themes/next-reloaded'...
  dyld: warning: could not load inserted library '/usr/local/Cellar/proxychains-ng/4.14/lib/libproxychains4.dylib' into hardened process because no suitable image found.  Did find:
  	/usr/local/Cellar/proxychains-ng/4.14/lib/libproxychains4.dylib: code signature in (/usr/local/Cellar/proxychains-ng/4.14/lib/libproxychains4.dylib) not valid for use in process using Library Validation: mapped file has no cdhash, completely unsigned? Code has to be at least ad-hoc signed.
  	/usr/local/Cellar/proxychains-ng/4.14/lib/libproxychains4.dylib: stat() failed with errno=1
  ^C
  ~~~

- 解决方案

  ~~~
  brew install git
  ~~~

  ~~~
  export PATH=/usr/local/bin:/usr/local/bin:${PATH}
  ~~~

  查看一下使用的是哪个版本的 git

  ~~~bash
  $ which git
  /usr/local/bin/git
  ~~~

  