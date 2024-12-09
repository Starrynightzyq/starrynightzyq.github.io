---
title: 使用 GitHub Actions 自动发布 Hexo 博客
toc: true
comments: false
date: 2024-12-09 19:30:00
updated: 2024-12-09 20:13:00
categories: hexo
tags: [hexo, github-actions]
description:
---

# 前言

由于换了电脑，重新搭建 hexo 博客环境还是蛮麻烦的，尤其是好多依赖都是国外网站，下载很慢，因此就想使用 Github Actions 自动发布博客。

实现的目标：本地撰写 Mardown 格式的文章，提交到 Github 仓库，由 Github Actions 自动构建，部署到 Github Pages。

# 设置 Github Actions

假设我们有两个 Github 仓库，分别用于存放博客源代码和博客静态资源（存放博客静态资源的仓库名字通常为 `usrname.github.io`）。存放博客源代码的仓库下文称 `src` 仓库，存放博客静态资源的仓库下文称为 `prd` 仓库。

## 1. 设置密钥

为了确保 Github Actions 能够正确部署博客，需要在 Github 仓库中设置密钥。

首先在本地生成密钥对：

```bash
ssh-keygen -t rsa -C "your_email@example.com" -f hexo-dedeploy-key
```

一路回车，当前目录就生成了 hexo-dedeploy-key 和 hexo-dedeploy-key.pub 两个文件。

然后我们来设置 `src` 仓库的 repository secrets：

进入 `src` 仓库，选择 Settings -> Secrets and variables -> Actions -> New repository secret，Name 为 `HEXO_DEPLOY_PRI`，secrets 填 `hexo-dedeploy-key` 文件的内容。

接着设置 `prd` 仓库的 deployment keys：

进入 `prd` 仓库，选择 Settings -> Deploy keys -> Add deploy key，Title 为 `HEXO_DEPLOY_PUB`，Key 填 `hexo-dedeploy-key.pub` 文件的内容。

## 2. Github Actions 文件

在 `src` 仓库中，创建 `.github/workflows/deploy.yml` 文件，内容如下：

```yaml
name: Deploy hexo blog

on:
  push:
    branches:
    - hexo

env:
  GIT_USER: starrynightzyq[bot]
  GIT_EMAIL: starrynightzyq[bot]@gmail.com

jobs:
  build:
    name: Build with node ${{ matrix.node-version }} on ${{ matrix.os }}
    runs-on: ubuntu-latest
    if: github.event.repository.owner.id == github.event.sender.id

    strategy:
      matrix:
        os: [ubuntu-latest]
        node-version: [16.x]

    steps:
      - name: Checkout
        uses: actions/checkout@v4
      - name: Use Node.js ${{ matrix.node-version }}
        uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node-version }}
      - name: Install SSH key
        uses: shimataro/ssh-key-action@v2
        with:
          key: ${{ secrets.HEXO_DEPLOY_PRI }}
          name: id_rsa
          known_hosts: 'github.com'
          if_key_exists: replace
      - name: Configuration environment
        run: |
          sudo timedatectl set-timezone "Asia/Shanghai"
          git config --global user.name $GIT_USER
          git config --global user.email $GIT_EMAIL
      - name: Setup pandoc
        uses: nikeee/setup-pandoc@v1
      - name: Install dependencies
        run: |
          npm install
      - name: Deploy hexo
        run: |
          npm run publish
```

配置好之后，我们提交代码到 `src` 仓库，Github Actions 就会自动构建博客，并将博客部署到 `prd` 仓库。

# Github Actions 的注意点

## 1. 设置 ssh key

网上的教程中看到的方法都是直接修改系统的 ssh key，但是 Github Actions 是在虚拟机中运行的，所以修改系统 ssh key 是没有意义的。

错误的方法：

```yaml
- name: Install SSH key
  env:
    HEXO_DEPLOY_PRI: ${{secrets.HEXO_DEPLOY_PRI}}
  run: |
    mkdir -p ~/.ssh/
    echo "$HEXO_DEPLOY_PRI" | tr -d '\r' > ~/.ssh/id_rsa
    chmod 600 ~/.ssh/id_rsa
    ssh-keyscan github.com >> ~/.ssh/known_hosts
```

正确的方法：

```yaml
- name: Install SSH key
  uses: shimataro/ssh-key-action@v2
  with:
    key: ${{ secrets.HEXO_DEPLOY_PRI }}
    name: id_rsa
    known_hosts: 'github.com'
    if_key_exists: replace
```

## 2. 配置 pandoc

pandoc 是一个将 Markdown 转换为各种格式的命令行工具，它使用 Lua 脚本来扩展 Markdown 的语法。在 Github Actions 中，我们可以使用 npm 安装 pandoc，也可以使用 pandoc-action 安装 pandoc。我用的是 pandoc-action：

```yaml
- name: Setup pandoc
  uses: njzk2/pandoc-action@v1
```

# 遇到的问题

## 1. npm ERR! request to https://registry.npm.taobao.org/yargs/download/... failed, reason: certificate has expired

在执行 `npm install` 这一步时，报错：

```
npm ERR! code CERT_HAS_EXPIRED
npm ERR! errno CERT_HAS_EXPIRED
npm ERR! request to https://registry.npm.taobao.org/yargs/download/yargs-3.10.0.tgz?cache=0&sync_timestamp=1594421075416&other_urls=https%3A%2F%2Fregistry.npm.taobao.org%2Fyargs%2Fdownload%2Fyargs-3.10.0.tgz failed, reason: certificate has expired
```

这是因为之前本地 deploy 时，使用了淘宝的镜像，但是taobao 的镜像已经过期了，所以需要更新镜像。由于我们是在 Github Actions 中，所以只需要删除 package-lock.json 文件重新 check in 即可。

## 2. err: TypeError: tab.repeat is not a function

执行 `hexo g` 命令时，报出如下错误：

```
FATAL {
  err: TypeError: tab.repeat is not a function
```

是 `_config.yml` 文件中 highlight 配置错误（ tab_replace 值写法错误）

错误写法：

```yml
highlight:
  enable: true
  line_number: true
  auto_detect: true
  tab_replace: true
```

正确写法：

```yml
highlight:
  enable: true
  line_number: true
  auto_detect: true
  tab_replace: '    '
```

## 3. Error: R][hexo-renderer-pandoc] pandoc exited with code null.

在执行 `hexo g` 命令时，报出如下错误：

```
Error: R][hexo-renderer-pandoc] pandoc exited with code null.
```

这是因为在 next 主题中将公式渲染器跟换为 hexo-renderer-pandoc，该渲染器需要有 pandoc 的后端渲染程序支持，所以需要安装 pandoc。在 Github Actions 中，可以加入下面的步骤：

```
    steps:
    ...
    - name: Setup pandoc
      uses: nikeee/setup-pandoc@v1
```


# Refrerence

[1]. [使用 GitHub Actions 自动发布 Hexo 博客](https://alanlee.fun/2024/07/05/deploy-hexo-with-github-action/)

[2]. [利用 Github Actions 自动部署 Hexo 博客](https://sanonz.github.io/2020/deploy-a-hexo-blog-from-github-actions/)

[3]. [使用 Github Action + Vercel 为 Hexo 的 Pandoc 渲染器提供支持](https://hui-shao.com/hexo-github-action-vervel/)

[4]. [淘宝镜像的https证书过期](https://www.cnblogs.com/ll666/p/18089299)

[5]. [Hexo 7.3.0 使用 hexo server 报错“TypeError: tab.repeat is not a function at \node_modules\hexo-util\dist\highlight.js:73:44”如何解决](https://yijile.com/zh/hexo-7-3-0-server-type-error-highlight-tab-replace/)
