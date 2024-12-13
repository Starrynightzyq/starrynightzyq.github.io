---
title: hexo部署到vercel
toc: true
comments: true
date: 2024-12-13 14:57:19
updated: 2024-12-13 15:20:42
categories: hexo
tags: [hexo, vercel]
description: hexo部署到vercel
---

# 流程

~~~mermaid
flowchart LR
    src[hexo源码]
    action[环境部署、hexo生成 GitHub Actions 自动完成]
    static[静态页面仓库]
    vercel[vercel 自动抓取]
    src --push到GitHub--> action --action push--> static --被抓取--> vercel
~~~