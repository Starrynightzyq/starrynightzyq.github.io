---
title: 自动追剧（or电影）
toc: true
comments: true
date: 2022-03-18 01:36:02
updated: 2022-03-18 01:36:02
categories: 懒人推动科技发展
tags: [GEEK]
description:
---



全自动观影流程

![automovie](https://pic.zhouyuqian.com/img/202204261123304.svg)

<!--more-->

## All

https://leishi.io/blog/posts/2021-12/home-nas-media-center

[软路由的用法（自动追剧配置）](https://post.smzdm.com/p/a5d22v7k/)

## Jackett

[UNRAID一篇就够！Jackett种子索引](https://post.smzdm.com/p/a0do2mnz/)

## qBittorrent

[BT下载教程 篇三：qBittorrent 全平台通用优化教程，适用于群晖 N1小钢炮](https://post.smzdm.com/p/ag827k26/)

https://hub.docker.com/r/johngong/qbittorrent

## Jellyfin

https://sspai.com/post/67763

[群晖 Docker 安装 Jellyfin 媒体服务器并开启 Intel Quick Sync 提升性能](https://blog.lishun.me/synology-docker-jellyfin-quicksync)

[解决 Docker 安装 Jellyfin 封面图和部分中文字幕变方块](https://blog.lishun.me/docker-jellyfin-chinese-fonts)

## My docker compose file

docker-compose.yml

~~~yaml
version: "3"

services:
  jackett:
    container_name: jackett
    image: linuxserver/jackett:latest
    environment:
      - PUID=1000
      - PGID=100
      - TZ=Asia/Shanghai
    ports:
      - 9117:9117
    volumes:
      - /share/homes/fitz/docker/jackett:/config
    restart: unless-stopped

  flaresolverr:
    container_name: flaresolverr
    image: ghcr.io/flaresolverr/flaresolverr:latest
    environment:
      - PUID=1000
      - PGID=100
      - TZ=Asia/Shanghai
      - LOG_LEVEL=info
    ports:
      - 8191:8191
    restart: unless-stopped

  radarr:
    container_name: radarr
    image: lscr.io/linuxserver/radarr:latest
    environment:
      - PUID=1000
      - PGID=100
      - TZ=Europe/London
    ports:
      - 7878:7878
    volumes:
      - /share/homes/fitz/docker/radarr:/config
      - /share/homes/fitz/DATA/aria2-completed/movies:/movies
      - /share/homes/fitz/DATA/aria2-downloads:/downloads
      - /share/OneDrive_SEU_NAS/media:/onedrive_media
    restart: unless-stopped

  sonarr:
    container_name: sonarr
    image: linuxserver/sonarr:latest
    environment:
      - PUID=1000
      - PGID=100
      - TZ=Asia/Shanghai
    ports:
      - 8987:8989
    volumes:
      - /share/homes/fitz/docker/sonarr:/config
      - /share/homes/fitz/DATA/aria2-completed/TV:/TV
      - /share/homes/fitz/DATA/aria2-downloads:/downloads
      - /share/OneDrive_SEU_NAS/media:/onedrive_media
    restart: unless-stopped

  chinesesubfinder:
    container_name: chinesesubfinder
    image: allanpk716/chinesesubfinder:latest
    environment:
      - PUID=1000
      - PGID=100
      - TZ=Asia/Shanghai
    ports:
      - 19035:19035
    volumes:
      - /share/homes/fitz/docker/chinesesubfinder/cache:/app/cache
      - /share/homes/fitz/docker/chinesesubfinder/config:/config
      - /share/homes/fitz/DATA/aria2-downloads:/downloads
      - /share/homes/fitz/DATA/aria2-completed/movies:/movies
      - /share/homes/fitz/DATA/aria2-completed/TV:/TV
      - /share/OneDrive_SEU_NAS/media:/onedrive_media
    restart: unless-stopped
    links:
      - emby
    depends_on:
      - emby

  qbittorrent:
    container_name: qbittorrent
    image: johngong/qbittorrent:latest
    environment:
      - QB_WEBUI_PORT=8989
      - QB_EE_BIN=false
      - QB_TRACKERS_UPDATE_AUTO=true
      - PUID=1000
      - PGID=100
      - UMASK=000
    ports:
      - 6882:6881
      - 6882:6881/udp
      - 8989:8989
    volumes:
      - /share/homes/fitz/docker/qbittorrent:/config
      - /share/homes/fitz/DATA/aria2-downloads:/Downloads
      - /share/homes/fitz/DATA/aria2-completed:/Completed
      - /share/OneDrive_SEU_NAS/media:/onedrive_media
    restart: unless-stopped
  
  ombi:
    image: lscr.io/linuxserver/ombi:latest
    container_name: ombi
    restart: unless-stopped
    environment:
      - PUID=1000
      - PGID=100
      - TZ=Asia/Shanghai
    volumes:
      - /share/homes/fitz/docker/ombi:/config
    ports:
      - 3579:3579
    dns:
      - 192.168.12.2
      - 223.5.5.5
    links:
      - emby
      - sonarr
      - radarr
    depends_on:
      - emby
      - sonarr
      - radarr

  emby:
    image: emby/embyserver
    container_name: emby
    # network_mode: host # Enable DLNA and Wake-on-Lan
    environment:
      - UID=1000 # The UID to run emby as (default: 2)
      - GID=100 # The GID to run emby as (default 2)
      - GIDLIST=100 # A comma-separated list of additional GIDs to run emby as (default: 2)
    volumes:
      - /share/homes/fitz/docker/emby:/config # Configuration directory
      - /share/aria2-complete/TV:/mnt/tvshows # Media directory
      - /share/aria2-complete/movies:/mnt/movies # Media directory
      - /share/OneDrive_SEU_NAS/media:/onedrive_media
    ports:
      - 8096:8096 # HTTP port
      # - 8920:8920 # HTTPS port
    dns:
      - 192.168.12.2
      - 223.5.5.5
    devices:
      - /dev/dri:/dev/dri # VAAPI/NVDEC/NVENC render nodes
    restart: unless-stopped
    
  jellyfin:
    container_name: jellyfin
    image: nyanmisaka/jellyfin:latest
    devices:
      - /dev/dri:/dev/dri
    environment:
      - PUID=1000
      - PGID=100
      - TZ=Asia/Shanghai
      - JELLYFIN_PublishedServerUrl=192.168.12.10
    volumes:
      - /share/homes/fitz/docker/jellyfin:/config
      - /share/aria2-complete/TV:/data/tvshows
      - /share/aria2-complete/movies:/data/movies
      - /share/OneDrive_SEU_NAS/media:/onedrive_media
    ports:
      - 8097:8096
      - 8920:8920 # HTTPS port
      - 7359:7359/udp
      - 1901:1900/udp
    dns:
      - 192.168.12.2
      - 223.5.5.5
    restart: unless-stopped
    # privileged: true
    # command:
    #   - sh
    #   - -c
    #   - |
    #       chmod -R 777 /dev/dri/renderD128
    #       chmod -R 777 /dev/dri/card0
    #       bash
    # tty: true
    # stdin_open: true
~~~

