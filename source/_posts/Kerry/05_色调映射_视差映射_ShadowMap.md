---
title: "[ASE入门] 05 色调映射 视差映射 ShadowMap"
date: 2026-04-09 08:00:00
updated:
categories: 
  - 技术美术
  - Unity
  - ASE入门
---

# 色调映射
## 原理
一般情况下（内置管线），Unity输出的亮度信息被限制在$ [0,1] $区间，但是我们计算出的最终的颜色范围很有可能大于这个范围，这意味着场景中最亮和最暗的区域可能出现大面积的纯白色和纯黑色，我们称这种图像为LDR（Low-Dynamic Range）。

利用色调映射（Tone-Mapping）技术，我们可以将HDR（High-Dynamic Range），即高动态范围的图像，也就是颜色范围大于$ [0,1] $区间的颜色，重映射到$ [0,1] $区间，即**我们可以通过色调映射，使得LDR显示器也能模拟HDR的信息**。

{% note danger %}
+ `ACES标准曲线`：

$$f(x) = \text{clamp} \left( \frac{2.51x^2 + 0.03x}{2.43x^2 + 0.59x + 0.14}, 0, 1 \right)$$

{% endnote %}

```csharp
// 输入参数 x 是未经处理的 HDR 颜色
inline float3 ACESFilm(float3 x)
{
    float a = 2.51f;
    float b = 0.03f;
    float c = 2.43f;
    float d = 0.59f;
    float e = 0.14f;
    
    return saturate((x*(a*x+b))/(x*(c*x+d)+e));
}
```

## 线性空间与伽马空间
人眼天生对于暗部变化更加敏感，因此，我们通常使用伽马空间（sRGB/Gamma）来存储贴图，这些贴图均被提亮处理过，他们的亮度约为原亮度的$ 1/2.2 $次幂，这样贴图就能使用更多的存储空间来存储暗部的细节。

但是所有光照的计算公式几乎都只在线性空间下成立，因此，如果我们在`Project Setting - Player - Color Space`中选择`Linear`的话，我们在调用`tex2D`函数时，Unity就会自动帮助我们将采样得到的颜色从伽马空间转换到线性空间，即`pow(texColor, 2.2)`，以此来进行后续的线性计算。

由于老式的CRT显示器在输出颜色时，每升高一倍的电压，其亮度会变成原先的$2.2$次幂，亮部会变得更暗，这是由于其物理特性所导致的，这种物理特性使得显示器能够使用更多的电压去绘制暗部，其暗部细节会更加丰富，符合人眼特性。现代的显示器虽然不再具有这种物理特性，但是依然会模仿CRT显示器输出$2.2$次幂的亮度。

但是一般情况下，我们通过线性空间计算出的光照结果已经是正确的了，无需输出$2.2$次幂的亮度，因此，Unity会自动将我们`return`的结果转换回伽马空间，即`pow(Color, 1/2.2)`，这正好与显示器的“压暗”特性相抵消。

因此，**Unity会在计算之前先将采样颜色从伽马空间转换到线性空间，最后将计算出的结果从线性空间转换回伽马空间。**

# 视差映射
法线贴图的缺点在于，当我们的视线方向越靠近平面的切线方向时，由于我们法线贴图不会改变物体表面的几何结构，因此从侧面看上去，物体的表面依然是水平的，不会有任何起伏，显得非常假。我们可以通过使用**深度图（置换贴图）**来偏移顶点的位置，但是这种做法对于性能消耗太大，因此，我们需要使用视差偏移技术。 

之所以使用深度图而不是高度图，是因为我们如果我们使用高度图来模拟物体表面的凸起，即原几何体表面作为凹陷的最低点，那么和法线贴图一样，在侧面看上去物体表面还是平整的，依然会穿帮；

而如果我们使用深度图，一方面便于下述的陡峭视差映射的实现，另一方面，使用深度图意味着物体表面是凸起的最高点，所有的细节都是向物体内部凹陷的，也就是所有的视错觉都发生在物体的内部，不会超出几何体的边界，因此从侧面观察效果更好。

## 快速视差映射
<!-- 这是一张图片，ocr 内容为： -->
![](/img/Kerry/05_色调映射_视差映射_ShadowMap/1776168482160-a6e4c209-ec46-4879-af42-7f0fe9cc5ea0.png)

如图所示，假设上端的黑粗实线表示物体表面，而红线表示我们想要模拟的物体表面的凹凸效果，也就是深度图（每个顶点的深度），最下方的黑细实线表示漫反射贴图。**我们的视线看向表面上的$A$点时，实际上我们希望我们能够看到$B$点的颜色**，毕竟红线才是我们希望模拟出的物体表面，因此我们需要想办法得到$B$点的`uv`坐标。

快速视差映射指的是，使用$A$点的深度值作为`uv`偏移值的主要参数，并将视线方向转换到切线空间，并在视线方向上继续偏移一小段距离计算出$P$点的`uv`坐标，以此来近似$B$点的`uv`坐标。

**`float2 uv_B = uv - tex2D(_Depth, uv) * viewDir_tangent.xy * _Parallax * 0.01;`**

其中`_Parallax`为可调权重。

{% note danger %}
在上式中，我们只使用到了视线方向的$xy$分量，而没有使用$z$分量，**这是因为我们只需要使用$xy$分量来确定在`uv`坐标系中的偏移方向**（由于切线方向就是$u$轴，因此我们可以使用切线空间来偏移`uv`）；

实际上从纯数学角度来看，上式实际上需要添加视线方向的$z$分量，修正后如下所示：

`float2 uv_B = uv - tex2D(_Depth, uv) * viewDir_tangent.xy / viewDir_tangent.z * _Parallax * 0.01;`

修正后，该结果更加拟真，如下图所示：

<!-- 这是一张图片，ocr 内容为： -->
![](/img/Kerry/05_色调映射_视差映射_ShadowMap/1776171417359-84ec698a-4f8e-4c34-860d-4b16daed54bd.png)

显然，如果我们想要求出$P$点的`uv`偏移量$Offset$，我们可以通过相似三角形得出，即：

$$Offset = \frac {(x, y)}{z} \times {Depth}_P$$

这种算法显然非常严谨，但是在实际应用中，由于当我们从侧面看物体时，视线方向的$z$分量过小甚至接近0，导致$Offset$极大，从而导致采样严重拉伸。因此，**在实际应用中，我们并不会直接添加`/ viewDir_tangent.z`，通常我们会添加`(/ max(viewDir_tangent.z, 0.05))`以防止边缘拉伸。**

{% endnote %}

但是快速视差映射的缺点也很明显，**当物体深度图过于陡峭时，会出现非常大的误差**：

<!-- 这是一张图片，ocr 内容为： -->
![](/img/Kerry/05_色调映射_视差映射_ShadowMap/1776171845450-aeb04058-bdae-45b9-8c82-a22f5955c42a.png)

## 陡峭视差映射
为了解决在深度图过于陡峭时引起的误差问题，我们需要使用陡峭误差映射技术。

<!-- 这是一张图片，ocr 内容为： -->
![](/img/Kerry/05_色调映射_视差映射_ShadowMap/1776173024820-9a76a185-bdc4-4f9e-8dc3-2df3217ede7a.png)

陡峭误差映射指的是，我们事先给深度图从0到1进行平均分层，然后采用**射线步进**的方式寻找交点：当**当前层的采样点的深度值大于当前层的深度的时候，说明我们恰好经过了视线方向与物体表面的交点。** 我们使用当前采样点来直接近似结果。

```csharp
// _MaxLayerNum("MaxLayerNum", Range(32, 40)) = 32
// _MinLayerNum("MinLayerNum", Range(8, 10)) = 8

float2 uv_parallax = i.uv;

float layerNum = lerp(_MaxLayerNum, _MinLayerNum, saturate(viewDir_tangent.z));
float layerDepth = 1 / layerNum;
float2 uv_delta = viewDir_tangent.xy / layerNum * _Parallax / max(viewDir_tangent.z, 0.05) * 0.01;

float2 uv_curr = i.uv;
float CurrentLayerDepth = 0;
float CurrentTexDepth = 1 - tex2D(_ParallaxMap, uv_curr).r;

[loop]
while(CurrentLayerDepth < CurrentTexDepth)
{
    uv_curr -= uv_delta;
    CurrentTexDepth = 1 - tex2D(_ParallaxMap, uv_curr).r;
    CurrentLayerDepth += layerDepth;
}

uv_parallax = uv_curr;
```

{% note danger %}
+ **`[loop]`：** 由于`Unity Shader`会自动将循环拆解成内联的代码，例如需要3次循环，Unity就会将循环体复制3次，但是由于这类`while`循环的循环次数不明确，因此Unity会报错，所以我们需要在`while`前手动添加`[loop]`来标记这是一个循环，以此来避免报错。

{% endnote %}

但是这种效果是建立在离散分层的基础上，这意味着**渲染的结果会出现“梯田效应”**。

<!-- 这是一张图片，ocr 内容为： -->
![](/img/Kerry/05_色调映射_视差映射_ShadowMap/1776175417819-5ceee8ff-ed59-472c-8553-2bdf82f453f6.png)

## 视差遮蔽映射Parallax Occlusion Mapping
<!-- 这是一张图片，ocr 内容为： -->
![](/img/Kerry/05_色调映射_视差映射_ShadowMap/1776175601680-c9d8cd82-3273-41a1-931a-142bbd9bdbdd.png)<!-- 这是一张图片，ocr 内容为： -->
![](/img/Kerry/05_色调映射_视差映射_ShadowMap/1776175670261-de0ee2f0-b953-44aa-895e-9ef1b7685083.png)

为了解决上述的离散分层问题，我们可以在最后阶段采用线性插值来近似求解，即：

`Lerp(uv_T3, uv_T2, Weight);`

其中`Weight`同样可以通过相似三角形得到：

$$Weight = \frac{ {Depth}_P }{ {Depth_A} - LayerDepth + {Depth}_P }$$

```csharp
float2 uv_parallax = i.uv;

float layerNum = lerp(_MaxLayerNum, _MinLayerNum, saturate(viewDir_tangent.z));
float layerDepth = 1 / layerNum;
float2 uv_delta = viewDir_tangent.xy / layerNum * _Parallax / max(viewDir_tangent.z, 0.05) * 0.01;

float2 uv_curr = i.uv;
float CurrentLayerDepth = 0;
float CurrentTexDepth = 1 - tex2D(_ParallaxMap, uv_curr).r;

[loop]
while(CurrentLayerDepth < CurrentTexDepth)
{
    uv_curr -= uv_delta;
    CurrentTexDepth = 1 - tex2D(_ParallaxMap, uv_curr).r;
    CurrentLayerDepth += layerDepth;
}

float2 uv_pre = uv_curr + uv_delta;
float curr = abs(CurrentTexDepth - CurrentLayerDepth);
float pre = abs((1 - tex2D(_ParallaxMap, uv_pre).r - (CurrentLayerDepth - layerDepth)));
float weight = curr / (curr + pre);

uv_parallax = lerp(uv_curr, uv_pre, weight);
```

## 性能局限性
一般来说，我们需要限制`Shader`中`tex2D`的使用次数，当使用次数大于8，意味着大量的性能消耗，同时我们也应当尽量避免使用循环，因此上述代码性能消耗量非常大，需要谨慎使用。

# 阴影
## 传统Shadow Mapping的局限性
> **Shadow Mapping技术**简单来说，就是**将摄像机放在和光源重合的位置上**，**记录从该摄像机（光源）出发能够看见的场景中距离最近的表面的位置（深度信息）**，显然该光源的阴影区域就是摄像机看不见的地方，因此这一步和深度测试类似，我们使用一个`LightMode`标签为`ShadowCaster`的`Pass`来将顶点从世界空间变换到光源空间中，寻找距离最近的顶点的深度信息，并**将深度信息存放至一张阴影映射纹理中（深度纹理）**
>

为了获得`Shadow Map`，Unity会在平行光的光源方向上放置一台摄像机，用于记录光源方向上各像素的深度。Unity将“玩家”摄像机画面中的顶点转换到光源空间中，光源空间本质上是一个特殊的观察空间，然后通过裁剪空间以及NDC坐标空间转换，我们得到了归一化后的顶点坐标，和运动模糊中的做法相反，我们使用$xy$分量作为`uv`与`Shadow Map`中的采样结果作比较，以此来判断像素是否位于阴影中。

但上述做法的前提是，我们需要在光源方向上找到一个合适的位置来放置光源摄像机。传统的Shadow Mapping技术中，**Unity会计算出一个能包含场景中的所有物体的巨大AABB包围盒**，摄像机的位置必须足够远，以此来确保能够包含整个包围盒。但是这样做的缺点在于，当场景中的物体间距很大时，摄像机的位置会变得非常远，这使得**生成的`Shadow Map`中很有可能只用几个像素来表示一个几何体**，这样的精度显然是远远不够的，**生成的阴影会有很严重的像素化边缘**，几乎完全不可用。

我们可以在`Project Setting - Graphic`的层设置中的`Layer 3`中关闭默认设置，即可关闭级联阴影，此时我们就能观察到传统Shadow Mapping技术的糟糕结果。

<!-- 这是一张图片，ocr 内容为： -->
![](/img/Kerry/05_色调映射_视差映射_ShadowMap/1776262776006-2c29f8f2-c0a4-457e-9f1e-c9159bfeab54.png)

## 级联阴影
为了解决上述问题，我们需要使用级联阴影。上述传统Shadow Mapping的缺点在于不论远近，都使用同一张`Shadow Map`。级联阴影类似于`Mip Map`技术，为不同远近的几何体生成不同的`Shadow Map`：

我们一般使用**二倍递增分布**来确定每一级`Shadow Map`覆盖的距离：以四层级联为例，那么第0-3级级联分别为6.7%、13.3%、26.7%、53.3%，这样做的好处是每一级级联`Shadow Map`对应世界空间中的边长是前一级的两倍，覆盖的物理面积变为前一级的四倍，符合人眼的视觉规律，视觉上不会发生跳变。

我们为每一个层级都划分一个**包围球**，八个顶点为视椎体与两个层级之间裁剪平面的交点，然后计算这个包围球的圆心和半径，每个级联的光源摄像机的方向向量与平行光保持一致，而**平移由圆心决定**，即每个级联的光源摄像机都必须确保能够对准各自的包围球的圆心；**半径用于计算光源摄像机的裁剪平面的大小**（**平行光的光源摄像机显然是正交而不是透视的**，因此**其远近裁剪平面为边长均等于包围球直径的正方形**），以此来获得各级联的`Shadow Map`。

{% note danger %}
之所以使用包围球而不是包围盒，是因为我们在**转动视角**的时候，传递到光源空间中的八个顶点之间的距离会不断发生变化，这意味着光源摄像机的裁剪平面大小也在不断发生变化，从而导致`Shadow Map`中每个像素代表的世界空间中的几何距离也在不断发生跳变，因此产生的阴影就会不断闪烁。

{% endnote %}

<!-- 这是一张图片，ocr 内容为： -->
![](/img/Kerry/05_色调映射_视差映射_ShadowMap/1776336118834-1155d5ec-322d-4c9a-8ede-ed5ea84bf5d9.svg)

