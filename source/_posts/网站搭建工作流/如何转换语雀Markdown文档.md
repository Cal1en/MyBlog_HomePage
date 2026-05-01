---
title: '[网站搭建工作流] 如何转换语雀Markdown文档'
date: 2026-05-01 11:36:01
updated: 2026-05-01 11:36:01
categories: 
  - 网站搭建
---
# 如何转换语雀Markdown文档

## 导出语雀Markdown文档

导出语雀Markdown文档的时候需要勾选以下选项：
![](/img/网站搭建工作流/如何转换语雀Markdown文档/1.png)

## 下载语雀的图片

```c
    node download_images.js "source\_posts\路径\你的文章名字.md"
```

## 将语雀的高亮块转换成`note`

```c
//color1
{% note info %}
//color2
{% note success %}
//color3
{% note warning %}
//color4
{% note danger %}
{% endnote %}
```