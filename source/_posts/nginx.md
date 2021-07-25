---
title: Nginx 反向代理
toc: true
comments: true
date: 2021-07-24 09:50:30
updated: 2021-07-25 00:50:30
categories: GEEK
tags: [hexo, GEEK, 美化]
description: Nginx 反向代理, 实现不同二级域名访问指定端口
---

# Nginx 配置文件位置

Nginx 的配置文件默认在 `/etc/nginx/nginx.conf`，打开这个文件，可以看到：

~~~nginx
http {
    ......
    ##
    # Virtual Host Configs
    ##

    include /etc/nginx/conf.d/*.conf;
    include /etc/nginx/sites-enabled/*;
}
~~~

这表明默认情况下 nginx 会自动包含 `/etc/nginx/conf.d/*.conf` 和 `/etc/nginx/sites-enabled/*`。

默认情况下，在 `/etc/nginx/sites-enabled` 下有一个默认站点，这个站点也就是 nginx 安装之后的默认站点：

```bash
$ cd /etc/nginx/sites-enabled
$ ls -l
total 0
lrwxrwxrwx 1 root root 34 Oct  6 02:19 default -> /etc/nginx/sites-available/default
```

打开 `/etc/nginx/sites-available/default` 可以看到如下内容：

```bash
server {
        listen 80 default_server;
        listen [::]:80 default_server;

        root /var/www/html;
        index index.html index.htm index.nginx-debian.html;

        server_name _;
        location / {
                try_files $uri $uri/ =404;
        }
```

按照这个文档的建议：

~~~
In most cases, administrators will remove this file from sites-enabled/ and leave it as reference inside of sites-available where it will continue to be updated by the nginx packaging team.
~~~

最好是在 `/etc/nginx/sites-available/` 下建立站点的配置文件，这些站点就是所谓的"可用站点"。然后在 link 到 `/etc/nginx/sites-enabled` 下开启站点，这些开启的站点就是所谓"启用站点"。

通过建立链接来控制可用站点的启用。

# 虚拟主机

# 反向代理

在实际使用中，由于web服务器启动于不同进程，因此需要指定不同的端口，也就意味着必然有web应用要使用80之外的端口，这样在地址栏中就必须出现端口号，非常影响用户体验。

比较好的方式，通过使用不同的域名或者二级域名，然后通过nginx反向代理的方式转发请求给到实际负责处理的服务器。

## 创建虚拟主机 frp.zhouyuqian.com

目标：[http://frp.zhouyuqian.com](http://frp.zhouyuqian.com/) 应该指向当前机器上运行于 7500 端口的 frps 服务。

在 `/etc/nginx/sites-available/` 下新建 `frp.zhouyuqian.com` 文件，内容如下：

> http

```tcl
server {
    listen 80;

    server_name frp.zhouyuqian.com;

    location /
    {
        proxy_pass http://127.0.0.1:7500; # 转发规则
        proxy_set_header Host $proxy_host; # 修改转发请求头，让8080端口的应用可以受到真实的请求
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_pass_header Server;
        proxy_connect_timeout 3s;
        proxy_read_timeout 10s;
    }
}
```

> https

~~~
server {
    listen 443 ssl;

    server_name frp.zhouyuqian.com;

    ssl_certificate /etc/nginx/cert/1_frp.zhouyuqian.com_bundle.crt;
    ssl_certificate_key /etc/nginx/cert/2_frp.zhouyuqian.com.key;

    ssl_protocols TLSv1 TLSv1.1 TLSv1.2;
    ssl_prefer_server_ciphers on;
    # ssl_dhparam /etc/ssl/certs/dhparam.pem;
    ssl_ciphers 'ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-AES256-GCM-SHA384:DHE-RSA-AES128-GCM-SHA256:DHE-DSS-AES128-GCM-SHA256:kEDH+AESGCM:ECDHE-RSA-AES128-SHA256:ECDHE-ECDSA-AES128-SHA256:ECDHE-RSA-AES128-SHA:ECDHE-ECDSA-AES128-SHA:ECDHE-RSA-AES256-SHA384:ECDHE-ECDSA-AES256-SHA384:ECDHE-RSA-AES256-SHA:ECDHE-ECDSA-AES256-SHA:DHE-RSA-AES128-SHA256:DHE-RSA-AES128-SHA:DHE-DSS-AES128-SHA256:DHE-RSA-AES256-SHA256:DHE-DSS-AES256-SHA:DHE-RSA-AES256-SHA:AES128-GCM-SHA256:AES256-GCM-SHA384:AES128-SHA256:AES256-SHA256:AES128-SHA:AES256-SHA:AES:CAMELLIA:DES-CBC3-SHA:!aNULL:!eNULL:!EXPORT:!DES:!RC4:!MD5:!PSK:!aECDH:!EDH-DSS-DES-CBC3-SHA:!EDH-RSA-DES-CBC3-SHA:!KRB5-DES-CBC3-SHA';
    ssl_session_timeout 1d;
    ssl_session_cache shared:SSL:50m;
    ssl_stapling on;
    ssl_stapling_verify on;
    add_header Strict-Transport-Security max-age=15768000;

    location / {
        proxy_pass http://127.0.0.1:7500/; # 转发规则
        proxy_set_header Host $proxy_host; # 修改转发请求头，让8080端口的应用可以受到真实的请求
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_pass_header Server;
        proxy_connect_timeout 3s;
        proxy_read_timeout 10s;
        index  index.html index.htm;
    }
}

server {
    listen *:80;
    listen [::]:80;
    server_name frp.zhouyuqian.com;
    return 301 https://frp.zhouyuqian.com$request_uri;
}
~~~

将 `frp.zhouyuqian.com` 站点文件链接到 `/etc/nginx/sites-enabled/` 目录：

```bash
sudo ln -s /etc/nginx/sites-available/frp.zhouyuqian.com /etc/nginx/sites-enabled/frp.zhouyuqian.com
```

修改完成之后，使用命令检测配置修改结果并重新装载配置：

```bash
sudo nginx -t
sudo nginx -s reload
```

 > ## 加 `/` 与不加 `/`
 >
 > 在配置proxy_pass代理转发时，如果后面的url加 `/`，表示绝对根路径；如果没有 `/`，表示相对路径
 >
 > 例如
 >
 > 1. 加 `/`
 >
 > ```text
 > server_name shaochenfeng.com
 > location /data/ {
 >     proxy_pass http://127.0.0.1/;
 > }
 > ```
 >
 > 访问 [http://shaochenfeng.com/data/index.html](https://link.zhihu.com/?target=http%3A//shaochenfeng.com/data/index.html) 会转发到 http://127.0.0.1/index.html
 >
 > 2. 不加 `/`
 >
 > ```text
 > server_name shaochenfeng.com
 > location /data/ {
 >     proxy_pass http://127.0.0.1;
 > }
 > ```
 >
 > 访问 [http://shaochenfeng.com/data/index.html](https://link.zhihu.com/?target=http%3A//shaochenfeng.com/data/index.html) 会转发到 [http://127.0.0.1/data/index.html](https://link.zhihu.com/?target=http%3A//127.0.0.1/data/index.html)

# Reference

[1] https://skyao.gitbooks.io/learning-nginx/content/configure/reverse/action_no_port.html

[2] https://www.bioinfo-scrounger.com/archives/Nginx_configure/
