---
title: MAC开发问题记录
toc: true
date: 2020-03-04 13:49:06
categories: GEEK
tags: [GEEK, MAC]
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

