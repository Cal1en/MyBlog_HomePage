---
title: '[网站搭建工作流] 如何转换语雀Markdown文档'
date: 2026-05-01 11:36:01
updated: 2026-05-01 11:36:01
categories: 
  - 网站搭建
sticky: 99
---
# 如何转换语雀Markdown文档

## 导出语雀Markdown文档

导出语雀Markdown文档的时候需要勾选以下选项：
![](/img/网站搭建工作流/如何转换语雀Markdown文档/1.png)

## 代码

```c
    //转换语雀的图片
    node download_images.js "source\_posts\路径\你的文章名字.md"

    //转换格式
    python build_zhihu_markdown.py "你的文档路径.md"
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