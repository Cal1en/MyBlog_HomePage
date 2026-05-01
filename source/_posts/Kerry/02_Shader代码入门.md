---
title: "[ASE入门] 02 Shader代码入门"
date: 2026-04-05 08:00:00
updated:
categories: 
  - 技术美术
  - Unity
  - ASE入门
---
<!-- node download_images.js "source\_posts\你的文章名字.md" -->

# `EnumDrawer`类
## `Cull`选项 `UnityEngine.Rendering.CullMode`
我们可以在`Properties`中声明一个`Float`类型的变量，然后在变量名之前添加`[Enum(UnityEngine.Rendering.CullMode)]`，即可用该变量控制`Cull`类型，如下所示：

```csharp
Properites
{
    [Enum(UnityEngine.Rendering.CullMode)]_CullMode("CullMode", Float) = 2
}
    //...
Cull [_CullMode]
```

