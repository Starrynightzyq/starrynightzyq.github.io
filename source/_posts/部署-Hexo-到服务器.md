---
title: 部署 Hexo 到服务器
toc: true
date: 2020-07-09 13:38:24
categories: hexo
updated: 2021-08-16 14:53:48
tags: [hexo, GEEK, 美化]
description:
---

# 部署到服务器

> Ref:
>
> [Hexo博客进阶：将Hexo部署到云服务器](https://qianfanguojin.github.io/2020/03/03/Hexo博客进阶：将Hexo部署到云服务器/)
>
> [**将Hexo部署到自己的服务器上**](https://www.cnblogs.com/jie-fang/p/13445939.html)

# no-www和www跳转

> Ref:
>
> [nginx实现no-www和www跳转](https://www.jianshu.com/p/cec753473ec9)

# 强制 HTTPs 跳转

## ~~首先查看 Nginx 是否有 SSL 支持模块~~

使用命令：

~~~bash
nginx -V
~~~

看输出中是否有：

~~~
configure arguments:
...
--with-http_ssl_module
...
~~~

如果没有，则需要重新编译 nginx，增加 SSL 支持模块，参考[为nginx添加SSL支持模块](https://www.codelast.com/原创-为nginx添加ssl支持模块/)。

## 安装 Nginx

参考：[北海骆驼-Nginx的编译安装并支持ssl](https://blog.csdn.net/qq_40015566/article/details/90169882)

# 申请&下载证书（略）

# 上传证书

在 Nginx 的安装目录 */etc/nginx/* 下创建 cert 目录，并将证书文件（SSL Key 和 CSR 文件）上传到 cert 目录中。

> 可以用 `whereis nginx` 查看 Nginx 安装目录

# 配置 Nginx

修改默认配置文件 */etc/nginx/sites-available/default* :

~~~tcl
server {

    # SSL configuration
    #
    listen 443 ssl default_server;
    listen [::]:443 ssl default_server;
    #

    # 定义服务器的默认网站根目录位置
    root /var/www/hexo;
    
    # ssl
    ssl on;
    ssl_certificate cert/1_example.com_bundle.crt;
    ssl_certificate_key cert/2_example.com.key;
    ssl_session_timeout 5m;
    ssl_protocols TLSv1 TLSv1.1 TLSv1.2;
    ssl_ciphers ECDHE-RSA-AES128-GCM-SHA256:HIGH:!aNULL:!MD5:!RC4:!DHE;
    ssl_prefer_server_ciphers on;

    # Add index.php to the list if you are using PHP
    index index.html index.htm index.nginx-debian.html;

    server_name example.com;

    location / {
        # First attempt to serve request as file, then
        # as directory, then fall back to displaying a 404.
        try_files $uri $uri/ =404;
    }

}

# 重定向，强制 https & no-www 访问
server {
    listen *:80;
    listen *:443 ssl; 
    listen [::]:80;
    listen [::]:443 ssl; 
    server_name www.example.com;
    return 301 https://example.com$request_uri;
}

server {
    listen *:80;
    listen [::]:80;
    server_name example.com;
    return 301 https://example.com$request_uri;
}
~~~

修改配置后，使用如下命令，检查配置是否正确：

~~~bash
nginx -t
~~~

最后重启 Nginx。

<!--more-->

> 这里需要注意下，导入新的证书后需要重启而不是重载，nginx -s reload是普通修改配置重载。

> ## Nginx日常操作命令
>
> - `nginx -t` 测试配置文件
> - `nginx -s reload` 修改配置后重载生效
> - `nginx -s reopen` 重新打开日志文件
> - `nginx -s stop` 快速停止
> - `nginx -s quit`
> - 查看 Nginx 进程 `ps -ef | grep nginx`

# 参考资料

1. [Hexo博客进阶：将Hexo部署到云服务器](https://qianfanguojin.github.io/2020/03/03/Hexo博客进阶：将Hexo部署到云服务器/)

2. [nginx配置ssl实现https访问 小白文](https://juejin.im/post/5c0144036fb9a04a102f046a)
3. [nginx实现no-www和www跳转](https://www.jianshu.com/p/cec753473ec9)









