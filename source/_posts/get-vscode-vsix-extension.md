---
title: 获取 VSCode VSIX 扩展
toc: true
comments: true
date: 2025-03-06 17:09:31
updated: 2025-03-06 20:01:36
categories: GEEK
tags: [VSCode]
description: 在官方的扩展市场中已经不提供直接下载 VSCode .vsix 的 link 了，本文介绍了一种获取 VSCode Extansion 的离线安装包的方法
---

# 前言

在官方的扩展市场中已经不提供直接下载 .vsix 的 link 了，本文介绍了一种获取 VSCode Extansion 的离线安装包的方法。该方法来自[oscar999](https://oscar.blog.csdn.net/)分享的文章[获取VS Code扩展指定版本的安装档(.vsix)的方式](https://blog.csdn.net/oscar999/article/details/145193849)。

# .vsix 获取

可以通过 VS Code 官方拓展市场的 API 接口 **`https://marketplace.visualstudio.com/_apis/public/gallery/extensionquery`** 获取 .vsix 文件，我们可以用 [PostMan](https://web.postman.co/) 来调用这个 API。

具体步骤：

1. 创建一个 POST 类型的请求，地址设为：`https://marketplace.visualstudio.com/_apis/public/gallery/extensionquery`
2. 在 Header 中添加如下参数：
   
   `Accept`: `application/json;api-version=6.0-preview.1`
   
   `Content-Type`: `application/json`

   ![header](https://pic.zhouyuqian.com/img/202503061954757.png)
   
   > `application/json` 指定了客户端希望接收的响应内容类型为JSON格式。`api-version=6.0-preview.1`指定客户端希望使用的API版本。
   >
   > `Content-Type: application/json`明确告诉服务器，客户端发送的请求体（如果有的话）是JSON格式的
3. Body 类型选 raw -- JSON，在 Body 中输入如下内容：
   ```json
   {
   "filters": [
       {
       "criteria": [
           { "filterType": 7, "value": "GitHub.github-vscode-theme" }
       ]
       }
   ],
   "flags": 103
   }
   ```

   ![Body](https://pic.zhouyuqian.com/img/202503061955457.png)

   其中 `"value": "GitHub.github-vscode-theme"` 是要下载的扩展的标识符，可以通过 VS Code 的扩展市场的链接最后的 `itemName` 找到对应的标识符。

   ![itemName](https://pic.zhouyuqian.com/img/202503061952292.png)

4. 点击 Send，在 Body 中会看到返回的 JSON 数据。

   找到其中 `assetType` 为 `Microsoft.VisualStudio.Services.VSIXPackage` 就是对应版本的 vsix 文件，`source` 为下载地址。

   ![Result](https://pic.zhouyuqian.com/img/202503061955958.png)

5. 下载链接的文件，得到一个文件名为 `Microsoft.VisualStudio.Services.VSIXPackage` 的文件，将其后缀改为 `.vsix`，即可安装了。

# .vsix 安装

![vsix 安装](https://pic.zhouyuqian.com/img/202503061953571.png)

# Reference

[1] [获取VS Code扩展指定版本的安装档(.vsix)的方式](https://blog.csdn.net/oscar999/article/details/145193849)