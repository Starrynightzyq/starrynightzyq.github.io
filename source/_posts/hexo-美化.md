---
title: hexo 美化
toc: true
date: 2020-03-06 13:15:51
categories: hexo
updated: 2021-03-16 22:36:23
tags: [hexo, GEEK, 美化]
description: 美化hexo及next主题
---

# 安装/升级next主题

安装

~~~
git clone https://github.com/theme-next/hexo-theme-next themes/next
~~~

升级

~~~
git clone https://github.com/theme-next/hexo-theme-next themes/next-reloaded
~~~

在 Hexo 的主配置文件中设置主题：

~~~yaml
...
theme: next-reloaded
...
~~~

更新语言配置

从 v6.0.3 版本起，`zh-Hans` 改名为 `zh-CN`：https://github.com/theme-next/hexo-theme-next/releases/tag/v6.0.3

需要修改 Hexo 主配置文件 `_config.yml` 里的 `language` 配置

# 设置主题的Scheme

Next自带了几种外观，在**主题目录**下的`_config.yml`里找到`scheme`，我比较喜欢Mist：

~~~yaml
#scheme: Muse
scheme: Mist
#scheme: Pisces
#scheme: Gemini
~~~

# 菜单设置

在**主题目录**下的`_config.yml`里找到`menu`：

~~~yaml
menu:
  home: / || home
  # about: /about/ || user
  tags: /tags/ || tags
  categories: /categories/ || th
  archives: /archives/ || archive
  #schedule: /schedule/ || calendar
  #sitemap: /sitemap.xml || sitemap
  # commonweal: /404/ || heartbeat
~~~

- 新添加的菜单需要翻译对应的中文

  打开`hexo/theme/next/languages/zh-CN.yml`，在menu下自定义，如：

  ~~~yaml
  menu:
    resources: 资源
  ~~~

- `hexo new page "categories"`

  此时在根目录的`source`文件夹下会生成一个categories文件，文件中有一个`index.md`文件，修改内容如下

  ~~~markdown
  ---
  title: 分类
  date: 2017-12-14 13:05:38
  type: "categories"
  comments: false
  ---
  ~~~

# 设定站点建立时间

在**主题目录**下的`_config.yml`里找到`since`：

~~~yaml
footer:
  # Specify the date when the site was setup. If not defined, current year will be used.
  since: 2018
~~~

# 设置头像

在**主题目录**下的`_config.yml`里找到`avatar`：

~~~yaml
# Sidebar Avatar
avatar:
  # Replace the default image and set the url here.
  url: /images/avatar.jpg # 图标
  # If true, the avatar will be dispalyed in circle.
  rounded: true # 圆形图标
  # If true, the avatar will be rotated with the cursor.
  rotated: true # 图标旋转
~~~

**注意：**图片地址在`./themes/next-reloaded/source/images/`下

# 网站图标设置

下载16x16以及32x32大小的**PNG格式图标**，置于`/themes/next/source/images/`下

在**主题目录**下的`_config.yml`里找到`favicon`：

~~~yaml
favicon:
  small: /images/favicon-16x16-kite.png
  medium: /images/favicon-32x32-kite.png
  apple_touch_icon: /images/apple-touch-icon-kite.png
  safari_pinned_tab: /images/logo-kite.svg
  #android_manifest: /images/manifest.json
  #ms_browserconfig: /images/browserconfig.xml
~~~

# 文章底部标签显示的优化

修改`/themes/next/layout/_macro/post.swig`，搜索 `rel="tag">#`，将 `#` 换成 `<i class="fa fa-tag"></i>`

# 主页文章添加阴影效果

现在使用自定义CSS的办法：
在主题目录下的`_config.yml`或`next.yml`中，设置

```
custom_file_path:
  style: source/_data/styles.styl
```

然后，将自定义CSS放进`hexo/source/_data/styles.styl`文件中即可

打开`hexo/source/source/_data/styles.styl`，添加以下代码：

~~~css
// 主页文章添加阴影效果
.post {
   margin-top: 60px;
   margin-bottom: 60px;
   padding: 25px;
   background:rgba(255,255,255,0.9) none repeat scroll !important;
   -webkit-box-shadow: 0 0 5px rgba(202, 203, 203, .5);
   -moz-box-shadow: 0 0 5px rgba(202, 203, 204, .5);
}
~~~

# 自动更换背景图片

> https://www.jianshu.com/p/30bf702f533c

打开`hexo/source/source/_data/styles.styl`，添加以下代码：

~~~
//页面背景
body {
    background:url(https://source.unsplash.com/random/1600x900);
    background-repeat: no-repeat;
    background-attachment:fixed;
    background-size:100% 100%;
    background-position:50% 50%;
}
.main-inner { 
    margin-top: 60px;
    padding: 60px 60px 60px 60px;
    background: #fff;
    opacity: 0.8;
    min-height: 500px;
}
~~~

background:url为图片路径，也可以使用本地地址，如 `/images/background.jpg`,地址在 `hexo/themes/next/source/images` 下
background-repeat：若果背景图片不能全屏，那么是否平铺显示，充满屏幕
background-attachment：背景是否随着网页上下滚动而滚动，fixed为固定
background-size：图片展示大小，这里设置100% 100%的意义为：如果背景图片不能全屏，那么是否通过拉伸的方式将背景强制拉伸至全屏显示。

# 顶部加载条

修改主题配置文件，找到`pace`改为`true`，并从上面提供的样式中选择一种填入`pace_theme`中就可以了：

```yaml
# Progress bar in the top during page loading.
# Dependencies: https://github.com/theme-next/theme-next-pace
# For more information: https://github.com/HubSpot/pace
pace:
  enable: true
  # Themes list:
  # big-counter | bounce | barber-shop | center-atom | center-circle | center-radar | center-simple
  # corner-indicator | fill-left | flat-top | flash | loading-bar | mac-osx | material | minimal
  theme: minimal
```

# 浏览页面的时候显示当前浏览进度

打开 `themes/next/_config.yml` ,搜索关键字 `scrollpercent` ,把 `false` 改为 `true`。

```yaml
# Scroll percent label in b2t button
  scrollpercent: true
```

如果想把 `top`按钮放在侧边栏,打开 `themes/next/_config.yml` ,搜索关键字 `b2t` ,把 `false` 改为 `true`。

```yaml
# Back to top in sidebar
  b2t: true

  # Scroll percent label in b2t button
  scrollpercent: true
```

# 文章顶部显示更新时间(默认打开)

打开主题配置文件 `_config.yml` ,搜索关键字 `updated_at` 设置为 `true` ：

```text
# Post meta display settings
post_meta:
  item_text: true
  created_at: true
  updated_at:
    enable: true
    another_day: true
  categories: true
```

**最新版本的next默认打开了这个选项**

# 修改内容区域的宽度

我们用Next主题是发现在电脑上阅读文章时内容两边留的空白较多，这样在浏览代码块时经常要滚动滚动条才能阅读完整，体验不是很好，下面提供修改内容区域的宽度的方法。 NexT 对于内容的宽度的设定如下：

- 700px，当屏幕宽度 < 1600px
- 900px，当屏幕宽度 >= 1600px
- 移动设备下，宽度自适应

如果你需要修改内容的宽度，同样需要编辑样式文件。 在Mist和Muse风格可以用下面的方法：

编辑主题的 `source/css/_variables/base.styl` 文件，新增变量：

```text
// 修改成你期望的宽度
$content-desktop = 700px

// 当视窗超过 1600px 后的宽度
$content-desktop-large = 900px
```

当你使用Pisces风格时可以用下面的方法：

```text
header{ width: 90%; }
.container .main-inner { width: 90%; }
.content-wrap { width: calc(100% - 260px); }
```

# 如何设置「阅读全文」？

在首页显示一篇文章的部分内容，并提供一个链接跳转到全文页面是一个常见的需求。 NexT 提供三种方式来控制文章在首页的显示方式。 也就是说，在首页显示文章的摘录并显示 **阅读全文** 按钮，可以通过以下方法：

1. 在文章中使用 `<!-- more -->` 手动进行截断，Hexo 提供的方式 **推荐**

2. 在文章的 [front-matter](https://hexo.io/docs/front-matter.html) 中添加 `description`，并提供文章摘录

3. 自动形成摘要，在 **主题配置文件** 中添加：

   ```
   auto_excerpt:
     enable: true
     length: 150
   ```

   默认截取的长度为 `150` 字符，可以根据需要自行设定

建议使用 `<!-- more -->`（即第一种方式），除了可以精确控制需要显示的摘录内容以外， 这种方式也可以让 Hexo 中的插件更好的识别。

# 404 页面

使用方法，新建 404.html 页面，放到主题的 `source` 目录下，内容如下：

~~~html
<!DOCTYPE HTML>
<html>
<head>
  <meta http-equiv="content-type" content="text/html;charset=utf-8;"/>
  <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1" />
  <meta name="robots" content="all" />
  <meta name="robots" content="index,follow"/>
  <link rel="stylesheet" type="text/css" href="https://qzone.qq.com/gy/404/style/404style.css">
</head>
<body>
  <script type="text/plain" src="http://www.qq.com/404/search_children.js"
          charset="utf-8" homePageUrl="/"
          homePageName="回到我的主页">
  </script>
  <script src="https://qzone.qq.com/gy/404/data.js" charset="utf-8"></script>
  <script src="https://qzone.qq.com/gy/404/page.js" charset="utf-8"></script>
</body>
</html>
~~~

**注意：**本地测试没有效果，需要发布

# 博客压缩

1. gulp 压缩

   > 参考:
   >
   > https://zhuanlan.zhihu.com/p/28447279
   >
   > https://leaferx.online/2017/06/16/use-gulp-to-minimize/

2. [Hexo-all-minifier](https://github.com/chenzhutian/hexo-all-minifier)

   > 参考：[Hexo博客优化之压缩加速](https://blog.cython.top/hexo-opt1.html)

# 代码框设置

打开主题配置文件 `_config.yml` , 搜索关键字 `codeblock`

~~~yaml
codeblock:
  # Code Highlight theme
  # Available values: normal | night | night eighties | night blue | night bright | solarized | solarized dark | galactic
  # See: https://github.com/chriskempson/tomorrow-theme
  highlight_theme: night
  # Add copy button on codeblock
  copy_button:
    enable: true
    # Show text copy result.
    show_result: default
    # Available values: default | flat | mac
    style: mac
~~~

# PAJX

该项功能的作用是：跳转到同网站另一个页面的时候，前后两个页面相同的元素不再重复加载，进而节省了加载的时间，加快访问速度。该项功能依赖官方提供的 [PJAX 插件](https://github.com/theme-next/theme-next-pjax)。

~~~yaml
# Easily enable fast Ajax navigation on your website.
# Dependencies: https://github.com/theme-next/theme-next-pjax
pjax: true
~~~

# 图片加载

实现该功能的基础是在文章中[插入图片](https://guanqr.com/tech/website/hexo-theme-next-customization/#图片)。该项功能的效果是：点击文中插图，图片能够放大，有幻灯片的效果。目前 NexT 提供了两款插件 fancybox 和 mediumzoom，两款插件开启一个即可。两款插件的效果不同，各有各的特点，我推荐使用 mediumzoom。

~~~yaml
# FancyBox is a tool that offers a nice and elegant way to add zooming functionality for images.
# For more information: https://fancyapps.com/fancybox
fancybox: false

# A JavaScript library for zooming images like Medium.
# Do not enable both `fancybox` and `mediumzoom`.
# For more information: https://github.com/francoischalifour/medium-zoom
mediumzoom: true
~~~

> PS: 本地图片无法加载问题
>
> reference: https://blog.csdn.net/xjm850552586/article/details/84101345

# 段落标题添加锚点

使用 NexT 官方制作的一个锚点插件：[hexo-theme-next-anchor](https://github.com/theme-next/hexo-theme-next-anchor)。

~~~bash
npm install hexo-theme-next-anchor --save
~~~

在主题的配置文件 `_config.yml` 中添加：

~~~yaml
anchor:
  enable: true
  color: '#0e83cd'
  position: right # If left, anchors will always be visible.
  margin: 7px 
  text: '#'
  icon:
    # If true, the `text` option will be ignored.
    enable: false 
    # By default, NexT has built-in FontAwesome support.
    # This option means `font-family: FontAwesome`, so DO Not change it.
    # Also you can choose ForkAwesome, but that's another story.
    font: FontAwesome
    content: \f0c1 # CSS content for FontAwesome & ForkAwesome.
~~~

# 鼠标点击浮出爱心效果

> Reference：https://tding.top/archives/58cff12b.html

在 *themes/next/source/js/* 目录下新建文件：*clicklove.js*，填入如下内容：

~~~js
!function(e,t,a){function n(){c(".heart{width: 10px;height: 10px;position: fixed;background: #f00;transform: rotate(45deg);-webkit-transform: rotate(45deg);-moz-transform: rotate(45deg);}.heart:after,.heart:before{content: '';width: inherit;height: inherit;background: inherit;border-radius: 50%;-webkit-border-radius: 50%;-moz-border-radius: 50%;position: fixed;}.heart:after{top: -5px;}.heart:before{left: -5px;}"),o(),r()}function r(){for(var e=0;e<d.length;e++)d[e].alpha<=0?(t.body.removeChild(d[e].el),d.splice(e,1)):(d[e].y--,d[e].scale+=.004,d[e].alpha-=.013,d[e].el.style.cssText="left:"+d[e].x+"px;top:"+d[e].y+"px;opacity:"+d[e].alpha+";transform:scale("+d[e].scale+","+d[e].scale+") rotate(45deg);background:"+d[e].color+";z-index:99999");requestAnimationFrame(r)}function o(){var t="function"==typeof e.onclick&&e.onclick;e.onclick=function(e){t&&t(),i(e)}}function i(e){var a=t.createElement("div");a.className="heart",d.push({el:a,x:e.clientX-5,y:e.clientY-5,scale:1,alpha:1,color:s()}),t.body.appendChild(a)}function c(e){var a=t.createElement("style");a.type="text/css";try{a.appendChild(t.createTextNode(e))}catch(t){a.styleSheet.cssText=e}t.getElementsByTagName("head")[0].appendChild(a)}function s(){return"rgb("+~~(255*Math.random())+","+~~(255*Math.random())+","+~~(255*Math.random())+")"}var d=[];e.requestAnimationFrame=function(){return e.requestAnimationFrame||e.webkitRequestAnimationFrame||e.mozRequestAnimationFrame||e.oRequestAnimationFrame||e.msRequestAnimationFrame||function(e){setTimeout(e,1e3/60)}}(),n()}(window,document);
~~~

然后修改 */themes/next/layout/_layout.swig*，在末尾 body 中添加：

~~~html
  <!-- 页面点击小红心 -->
  <!-- <script type="text/javascript" src="/js/jquery-3.3.1.min.js"></script> -->
  <script type="text/javascript" src="/js/clicklove.js"></script>
~~~

![clicklove](https://pic.zhouyuqian.com/img/20210727182411.png)

# 修改字体大小

> reference: https://theme-next.iissnan.com/faqs.html#custom-font

在 next 主题配置文件 *_config.yml* 中启用 *variables.styl*：

~~~yaml
# Define custom file paths.
# Create your custom files in site directory `source/_data` and uncomment needed files below.
custom_file_path:
  #head: source/_data/head.swig
  #header: source/_data/header.swig
  #sidebar: source/_data/sidebar.swig
  #postMeta: source/_data/post-meta.swig
  #postBodyEnd: source/_data/post-body-end.swig
  #footer: source/_data/footer.swig
  #bodyEnd: source/_data/body-end.swig
  variable: source/_data/variables.styl
  #mixin: source/_data/mixins.styl
  style: source/_data/styles.styl
~~~

在站点目录下的 *source/_data/* 文件夹下新建 *variables.styl*，填写如下内容：

~~~css
// 标题，修改成你期望的字体族
$font-family-headings = Georgia, sans

// 修改成你期望的字体族
$font-family-base = "Microsoft YaHei", Verdana, sans-serif

// 代码字体
$code-font-family = "Input Mono", "PT Mono", Consolas, Monaco, Menlo, monospace

// 正文字体的大小
$font-size-base = 16px

// 代码字体的大小
$code-font-size = 13px
~~~

# 侧边栏社交链接设置

> Ref：
>
> [添加阿里图标支持](https://guanqr.com/tech/website/hexo-theme-next-customization/#contents:添加阿里图标支持)

# 评论系统-Valine

> Ref:
>
> [为你的Hexo加上评论系统-Valine](https://blog.csdn.net/blue_zy/article/details/79071414)
>
> [Valine评论系统](https://blog.csdn.net/weixin_43405525/article/details/99228698?utm_medium=distribute.pc_relevant_t0.none-task-blog-BlogCommendFromMachineLearnPai2-1.compare&depth_1-utm_source=distribute.pc_relevant_t0.none-task-blog-BlogCommendFromMachineLearnPai2-1.compare)
>
> [Hexo博客进阶：为Next主题添加Valine评论系统](https://qianfanguojin.github.io/2019/07/23/Hexo博客进阶：为Next主题添加Valine评论系统/)
>
> [Valine评论系统详解(匹配QQ头像)](https://lovelijunyi.gitee.io/posts/e52c.html)

# 评论邮件通知-[Valine-Admin](https://github.com/DesertsP/Valine-Admin)

Valine Admin 是 [Valine 评论系统](https://deserts.io/diy-a-comment-system/)的扩展和增强，主要实现评论邮件通知、评论管理、垃圾评论过滤等功能。支持完全自定义的邮件通知模板。基于Akismet API实现准确的垃圾评论过滤。此外，使用云函数等技术解决了免费版云引擎休眠问题，支持云引擎自动唤醒，漏发邮件自动补发。兼容云淡风轻及Deserts维护的多版本Valine。

# 文章结语

> Ref:
>
> [文章结束处添加感谢阅读的提示](https://xian6ge.cn/posts/6d7ed114/#1-%E6%96%87%E7%AB%A0%E7%BB%93%E6%9D%9F%E5%A4%84%E6%B7%BB%E5%8A%A0%E6%84%9F%E8%B0%A2%E9%98%85%E8%AF%BB%E7%9A%84%E6%8F%90%E7%A4%BA)

# 数学公式

> Ref:
>
> [next主题的文档](https://github.com/theme-next/hexo-theme-next/blob/master/docs/MATH.md)
> [Hexo Next主题渲染 Latex 公式的配置方法](https://roro4ever.github.io/2019/12/01/hexo-Next%E4%B8%BB%E9%A2%98%E6%B8%B2%E6%9F%93-latex-%E5%85%AC%E5%BC%8F%E7%9A%84%E9%85%8D%E7%BD%AE%E6%96%B9%E6%B3%95/hexo-next%E4%B8%BB%E9%A2%98%E6%B8%B2%E6%9F%93-latex-%E5%85%AC%E5%BC%8F%E7%9A%84%E9%85%8D%E7%BD%AE%E6%96%B9%E6%B3%95/)

办法就是替换Hexo的渲染器，比如在博客目录下执行：

```bash
npm un hexo-renderer-marked --save
npm i hexo-renderer-pandoc --save # or hexo-renderer-kramed
```

~~hexo-renderer-kramed 渲染器也有缺点，它不支持行内 latex 公式。解决办法是有的，要么在行内自己加上转义符号，要么修改渲染规则。渲染器作者建议是用`把公式标注成代码块，参见[此处](https://duskcloudxu.github.io/2018/07/14/hexo-renderer-kramed与mathJax的兼容问题及解决方法/)。~~

hexo-renderer-pandoc 支持行内数学公式，不用转义。

---

行内数学公式（样式）：

~~~latex
`$f(x) = x^{2/3}+e/3*(\pi-x^2)^{1/2}*sin(a*\pi*x)$`
~~~

行内数学公式（测试）：`$f(x) = x^{2/3}+e/3*(\pi-x^2)^{1/2}*sin(a*\pi*x)$`

---

行间数学公式（样式）：

~~~latex
$$
f(x) = x^{2/3}+e/3*(\pi-x^2)^{1/2}*sin(a*\pi*x)
$$
~~~

行内数学公式（测试）：
$$
f(x) = x^{2/3}+e/3*(\pi-x^2)^{1/2}*sin(a*\pi*x)
$$
~~PS: 行内数学公式使用时需要用 ` 转义。~~

# 自定义 404 页面

自定义含有小游戏的404页面

> https://chennq.com/Hexo/20190922-hexo_next_404page.html
>
> https://www.jianshu.com/p/1b819734538f

NGINX 404 配置

> https://leyar.me/create-404-page/
>
> https://zhuanlan.zhihu.com/p/269456060