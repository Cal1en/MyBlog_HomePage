---
title: "[角色渲染] 终末地角色渲染复刻"
date: 2026-08-12 13:00:00
updated:
categories: 
  - 技术美术
  - Unity
  - 角色渲染
sticky: 101
---

<style>
/* 仅在本篇文章中取消正文段落的首行缩进 */
.post-content .markdown-body p {
  text-indent: 0;
}
</style>

本文已上传知乎，推荐在知乎阅读本文以获得最佳的浏览体验：https://zhuanlan.zhihu.com/p/2070844065663415772

> *渲染管线：Unity URP*  
> 本文参考：

[【unity urp】从零模仿复刻实现自己的终末地人物卡通渲染](https://zhuanlan.zhihu.com/p/2028819446546932894)

[【Unity URP】从零开始仿终末地莱万汀渲染学习记录](https://zhuanlan.zhihu.com/p/2054958065078871199)

[https://zhuanlan.zhihu.com/p/2013370672647268314](https://zhuanlan.zhihu.com/p/2013370672647268314)

[https://zhuanlan.zhihu.com/p/1972323352069797451](https://zhuanlan.zhihu.com/p/1972323352069797451)

> 集百家之所长这一块（）  
> 有一说一本文真的是笔记而不是批注吗（？）  
> 万分感谢上述大大大大大佬的分享！  
>   
> **效果展示：**

[https://link.zhihu.com/?target=https%3A//www.bilibili.com/video/BV18tNM69EwS/](https://link.zhihu.com/?target=https%3A//www.bilibili.com/video/BV18tNM69EwS/)

## 前言

这是笔者为了学习角色渲染而接触的第一个该方向的项目，我也不知道一上来就逮着《终末地》的角色渲染学是不是难度跨度太大了（**是的**），毕竟笔者也只是一个刚接触技术美术的小白，因此**文章里难免会出现许多错误**，以及大量“面向美术效果设计”的奇怪 tricks (?)，不过**我会在这些 tricks 出现的位置标注出我认为更加正确的做法，供各位读者参考**（不直接改掉这些 tricks 一方面是想记录一下自己的思路历程，另一方面是效果展示视频都已经发到 b 站了，懒得改了QAQ）

由于该项目对于笔者的难度很高，有很多东西笔者都是第一次见，跟何况终末地还是 PBR + NPR，因此这份笔记的内容将会极其详细，部分地方甚至会有些“弱智”，我会在这些部分标注“**可跳过**”，还请各位谅解。

综上，这份笔记**仅供各位参考**，在美术效果上确实能大致还原终末地的角色渲染，但肯定不能落地到项目应用中。（如果把后文提到的我“擅自”添加的这一堆 tricks 换掉估计还有点戏）

## 资源整理

（有一说一各位老大导入素材的时候看到这么多纹理图片啥的真的不会两眼一黑嘛）

***所有美术资产均仅用于学习用途，如有侵权请联系***

### 整理贴图名称

经观察，各类贴图的用途均使用贴图名称末尾的“下划线 + 用途缩写”的方式进行标注，如下所示：

-   `_D`：基础色 `AlbedoTex`，其 `A` 通道有额外用途，不同身体部位的`A`通道用途也不同，后文将会提到；
-   `_P`：`ORMTex`，当然叫这个名字只是因为大家好像都这么叫，但是贴图颜色通道和用途自然不一定是按照 ORM 排列的，其用途如下所示：

| 通道 | 用途 |
| ----- | ----- |
| R | Metallic |
| G | Reflectivity |
| B | AO |
| A | Smoothness |

-   `_N`：不必多说，N 开头十有八九都是法线贴图，其 `RG` 通道对应法线 `XY` 分量，`Z`分量需要解压计算。还需要注意的是，头发部分的法线贴图的 `BA` 通道并不为空，还存储了另一套平滑法线，后文将会提到其用途；
-   `_E`：自发光贴图；
-   `_RD`：Ramp 图，NPR 中不可或缺的一部分，用于调整明暗部分以及过渡区域的颜色，使角色表面具有卡通感的明暗过渡。其 `A` 通道同样有特殊用途，后文将会详细解释；
-   `_RS`：也许是 Refine Specular 的缩写？用于调整高光颜色。

主要的贴图就是这些，脸部的贴图和 lut 图之类的我们后文再单独列出。

### 材质插槽名称

如果各位使用的是从模之屋下载的模型的话，模型中的材质名称使用的是日语罗马音，使用 AI 进行名称转译后结果如下：

-   `0.men`：`面`，脸部；
-   `1.me`：`目`，眼睛；
-   `2.meHL`：`目HL`，眼部高光；
-   `3.mejiro`：`目白`，眼白；
-   `4.mekage`：`目影`，眼部阴影；
-   `5.matsugemayu`：`睫眉`，睫毛与眉毛；
-   `6.kounai`：`口内`，口腔内部；
-   `7._`：`发`，头发。此处有可能是因为直接使用了简体字，导致被替换成了`_`；
-   `8._kage`：`发影`，头发阴影；
-   `9.hada`：`肌`，皮肤；
-   `10.Cloth1`：衣服；
-   `11.hyoujou`：`表情`，表情贴图；

## 基础数据处理

由于笔者使用的是 ASE，所以干脆直接截图吧，为了弥补观感，后续的公式将尽可能使用 LaTeX 来表示。

-   BaseColor

![](/img/角色渲染/Unity_URP_拉完了的终末地角色渲染复刻笔记/003.jpg)

-   ORM

![](/img/角色渲染/Unity_URP_拉完了的终末地角色渲染复刻笔记/004.jpg)

*`F0` 这块连复杂了，直接用 $F0 = lerp(0.04 \times Reflectivity, BaseColorRaw, Metallic)$ 就好。*

> 可跳过： *`F0` 后续会参与镜面反射计算，决定反射光强与颜色，而金属没有漫反射，只存在镜面反射，其镜面反射的颜色就是其 `BaseColorRaw` 本身。*

-   Normal

![](/img/角色渲染/Unity_URP_拉完了的终末地角色渲染复刻笔记/005.png)

## 直接光漫反射

*我们先以衣服的 Shader 为例介绍一下 Shader 的基本结构：*

传统 NPR 是通过**基于色调的着色技术（tone-based shading）** 对一张色调贴图，即 Ramp 图进行采样，获得色调分界较为明显的着色效果，从而呈现出卡通风格。

我们曾在《入门精要》中见到过较为简单的 NPR 案例，其中角色的着色完全来自于 Ramp 图中的颜色，但对于终末地这类 PBR + NPR 的角色渲染来说，角色的基本着色自然来自于直接光漫反射，因此，我们可以通过**对直接光漫反射进行颜色分层来得到 NPR 的效果**，而颜色分层自然与角色表面的明暗部位有关，也就是 AO 和阴影部分，同时为了更加细腻的控制明暗分层，我们还需要用到前文所提到的 Ramp 图对漫反射颜色进行修正，以及使用 Ramp 图 `A` 通道来控制明暗区域的分布。

> 阴影使用的是这套方案：  
> Per-Object Shadow 高精度阴影：[https://zhuanlan.zhihu.com/p/612448813](https://zhuanlan.zhihu.com/p/612448813)

### Ramp 图采样

> 可跳过

-   **背光补偿**

传统 Ramp 图采样使用的是半兰伯特系数，即 $uv = (0.5 + 0.5 \times NoL, 0.5)$ 对 Ramp 图进行采样，显然，**这种采样方式得到的结果在逆光状态下，角色将会处于近乎全黑的状态**，同时丢失大量明暗部分的细节。

那么如何添加补光呢？我们可以从对 Ramp 图采样的本质来看：

我们为什么要使用半兰伯特系数来进行采样？是因为我们需要将 NoL 从 $[-1,1]$ 区间转化到 $[0,1]$ 区间，以此才能够对一张贴图进行采样；

那我们为什么要使用 NoL？是因为当光源正对当前顶点时 $NoL = 1$，背对光源，即逆光时 $NoL = -1$，同时 NoL 还能在正对光源与背对光源两种情况之间平滑过渡；

那么现在我们需要对物体背对光源时添加补光，我们肯定不能将 NoL 或者半兰伯特系数整体提高，那样的话物体将会直接丢失最暗部的细节，更何况人眼在感知暗部变化方面远比亮部变化要更加敏感得多。因此，更好的方法是在不抬升 NoL 两端，即保证 $NoL = ±1$ 时仍能正确采样到 Ramp 图的最亮与最暗部的情况下，抬升采样函数的中间部分。

这是什么意思？我们不妨先假设最终采样的 uv 为：

$$uv = (0.5 \times F(x) + 0.5,0.5)，F(x) \in [-1,1]$$

读者不妨先把这里的 $F(x)$ 看做是 $F(x) = x$ ，其中 $x = NoL$，此时相当于我们直接使用半兰伯特系数对 Ramp 图进行采样，但是现在 $F(x)$ 在 $[-1,1]$ 区间内是线性变化的，我们希望在不改变函数左右的两个端点，即 $NoL = ±1$ 时的函数值的情况下，抬升这个函数的中间部分，而该函数的中间部分恰好对应的是 Ramp 图中明暗变化的中间交界处，如果我们能在背光时抬升中间部分，即将采样 Ramp 图中的位置向右（亮部）偏移，在正对光源时还原中间部分，不就能够仅在背光时提亮角色了吗？

明白了这一点之后，我们就可以先尝试构造出一个函数与 $F(x)$ 相加，这个函数需要满足在 $x = ±1$ 时值为 0，以此来避免影响最亮和最暗部；还需要满足在 $x = 0$ 处的数值大于 0，以此来抬升 $F(x)$ 的中间部分，还需要在 $x \in [-1,1]$ 区间内平滑过渡。

根据参考文章，我们可以使用 $1 - {NoL}^2$ ，即 $1 - x^2$ ，该抛物线完美满足上述特性，只不过在 $x = 0$ 处函数值为 1，我们肯定不希望逆光时角色表面还会出现最亮部，因此我们可以使用 $0.5(1 - x^2)$ ，并将其与 $F(x)$ 相加，即逆光时角色表面的最亮部亮度恰好为 Ramp 图 $u =0.75$ 的位置，**如果读者希望角色背光时能够能亮一些，不妨尝试将上式中的 0.5 增大一些**，笔者后续也确实碰到了逆光时亮度不足的问题，但是当时没想起来还能调整这个系数，所以使用了一些奇思妙想的 tricks，*读者不妨尝试一下此处的方法*。

简单来说，我们只是在原先的 NoL 的基础上，加上了一个 $1-{NoL}^2$ 作为补光的因子，但这个因子不需要一直存在，只需要在背光时出现即可，我们可**将其乘以一个背光补偿系数** $BackLight$。

那么如何判断当前是否处于逆光状态呢？很简单，我们只需要比较摄像机和主光源的朝向即可，两者同向时为正对光源，反向时为背对光源。但是参考文章中并没有直接使用这两个向量，而是取了 XZ 平面上的水平分量做点积：诸位可以设想一下如果摄像机和光源处于人物同一侧，且光源从靠近人物头顶的方向向下打，而摄像机从下向上观察人物，此时有可能会出现摄像机与光源方向之间的夹角大于 90 度的情况，但此时摄像机与光源处于人物的同一侧，并不需要补光，因此我们只需要使用两者的水平分量计算夹角来判断背光即可。

*`CameraForwardWS` 指的是`UNITY_MATRIX_V[2].xyz` ，也就是摄像机的正后方，读者请注意其与 `ViewDir` 的区别。*

$$CameraForwardXZ=normalize(CameraForwardWS.xz)$$

$$MainLightDirXZ=normalize(MainLightDir.xz)$$

$$BackLightDirection=saturate(−dot(CameraForwardXZ,MainLightDirXZ))$$

但是由于我们忽略掉了 y 分量，这导致**摄像机在接近人物头顶时会触发边界情况**，也就是上述的 xz 分量有可能均接近 0。参考文章中通过引入摄像机方向向量的 y 分量来控制会触发背光补偿的摄像机相对人物的俯仰角区间：

$$BackLightCamera=smoothstep(0,1,saturate(0.75 - |{CameraForwardWS.y}| ))$$

想要搞清楚这个式子的含义，诸位只需要画一画函数图像即可，俯仰角区间可以使用反三角函数计算一下，此处不再赘述。

最后我们再引入一个可人为控制的背光补偿强度 $BackLightStrength$ ，得到最终的背光补偿系数：

$$BackLgiht = BackLightDirection \times BackLightCamera \times BackLightStrength$$

上述计算方式来自参考文章中，但是笔者基于自身有限的理解，认为此处可能还是存在着一些边界情况没有解决，仅供参考：如果光源来自人物的正上方，$MainLightDirXZ$ 分量还是会接近 0；换个角度看，如果光源来自人物的正上方，这种情况下貌似也不需要添加背光补偿了（？）。读者不妨动手修改一下上述公式，修改的方法有很多种也很简单，此处不做过多赘述。

综上所述，Ramp 图的采样 uv 为：

$$NoLRefine = clamp(NoL + 0.5(1 - {NoL}^2) \times BackLight, -1, 1)$$

$$uv = (0.5 \times NoLRefine + 0.5, 0.5)$$

![BackLight](/img/角色渲染/Unity_URP_拉完了的终末地角色渲染复刻笔记/006.jpg)![uv_Ramp](/img/角色渲染/Unity_URP_拉完了的终末地角色渲染复刻笔记/007.png)

-   **`A` 通道的二次采样**

基于笔者有限的理解，Ramp 图的 `A` 通道可以看做是一条用于控制颜色分层位置的灰度曲线，我们使用上述采样方式得到的结果如下：

![](/img/角色渲染/Unity_URP_拉完了的终末地角色渲染复刻笔记/008.gif)

顺便在这里再放一张 AO 的结果：

![](/img/角色渲染/Unity_URP_拉完了的终末地角色渲染复刻笔记/009.jpg)

之所以要在这里放上 AO 的结果，是因为这两张图中有些部位依然是成片的纯白色，哪怕将两者叠加后依然会出现，在不考虑场景阴影的情况下，这种成片的纯白色意味着这些部位的立体感会略有缺失，参考文章中通过使用法线和 `CameraForward` 的点积对 Ramp 图进行了**第二次采样**来弥补了这一点，也就是在边缘部分做了一个暗部遮罩来提升立体感：

![](/img/角色渲染/Unity_URP_拉完了的终末地角色渲染复刻笔记/010.jpg)

读者可能会问，为什么我们不使用 NoV 而是使用 `CameraForward` 参与计算？读者不妨思考一下 `ViewDir` 和 `CameraForward` 的区别，后者更加适合用于卡通渲染。

![](/img/角色渲染/Unity_URP_拉完了的终末地角色渲染复刻笔记/011.jpg)

### 三层漫反射

-   **能量守恒**

一般情况下，普通非金属材质的反射率约为 4%，即入射光沿物体法线方向照射时，有 4% 的能量被分配给镜面反射，剩余 96% 的能量分配给漫反射，我们可以用一个系数来同时表示金属材质与非金属材质的漫反射能量：

$$EnergyDiffuse = 0.96(1 - Metallic)$$

其中 $(1 - Metallic)$ 用于表示金属表面不包含漫反射项。

> 可跳过： 这里是简化后的 PBR 处理，对应`OneMinusReflectivityMetallic`函数，其原公式为 $(1 - Fresnel)(1 - Metallic)$ 。

-   **第一层漫反射（亮部）**

第一层漫反射的计算公式如下：

$$DiffuseColorLight = BaseColorRaw \times EnergyDiffuse$$

-   **第二层漫反射（暗部）**

我们通过在 $BaseColor$ 的基础上给予一个人为控制的衰减比例来控制第二层漫反射的基础颜色，同时还需要添加一定的饱和度衰减。

$$BaseColorDarkRaw = BaseColorRaw \times \_AlbedoDarkStrength$$

$$BaseColorDark = lerp(Luminance(BaseColorDarkRaw), BaseColorDarkRaw, \_AlbedoDarkSaturation)$$

最后乘以漫反射能量：

$$DiffuseColorDark = BaseColorDark \times EnergyDiffuse$$

-   **第三层漫反射（极暗）**

此处我们直接在第二层漫反射的基础上给予一个 0.65 的衰减即可：

$$DiffuseColorDarkInDark = 0.65 \times DiffuseColorDark$$

-   **组合**

所谓组合，实际上就是确认上述三层漫反射各自所在的角色表面区域。此处的组合方式主要是基于美术效果的设计。我们先看暗部与极暗部分的组合：

有哪些因素能够影响明暗部位呢？自然是 AO，场景阴影，以及我们上文提到的 Ramp 图的 `A` 通道，由于我们需要增添立体感，所以此处使用的是第二次采样 Ramp 图的结果 $RampNoF$。那么有哪些部分需要在暗部的基础上变得更加暗呢？自然是这些因素**叠加出现的位置**，因此我们可以将这几个因素相乘，得到这些需要额外压暗的区域：

$$AoShadowNoFRamp = AO \times ShadowScene \times RampNoF$$

但是终末地的美术设计貌似不希望极暗部出现在向光侧，因此我们还要才此基础上添加 Ramp 图第一次采样的结果 $RampNoLRemap$ ，而后基于此在暗部与极暗部间线性插值：

$$DarkLayerMask = AoShadowNoFRamp + RampNoLRemap$$

$$DiffuseColorDarkFinal =  lerp(DiffuseColorDarkInDark, DiffuseColorDark, DarkLayerMask)$$

最后便是亮部与暗部的组合，我们依然会用到 AO、阴影以及 Ramp 图，只不过这次用的是第一次采样的结果 $RampNoLRemap$ ，但是我们最好不要直接将它们相乘，毕竟 NPR 渲染的明暗边界较为清晰，所以我们将使用 `min` 的方式组合上述因素：

$$MinShadowEffect = min(min(AO, ShadowScene), RampNoLRemap)$$

最后得到三层漫反射的结果：

$$MainDiffuseBRDF = lerp(DiffuseColorDarkFinal, DiffuseColorLight, MinShadowEffect)$$

### 叠加 Ramp 颜色

我原本也以为 Ramp 图的颜色是直接与上述结果相乘来着，结果做到最后才发现颜色很奇怪，有些地方明显偏黑/灰。

参考文章中指出，终末地此处还做了一些特殊的美术设计，他们使用“色度”（Chroma）做了一步加权计算：**色度指的是当前颜色通道中的最大值与最小值之差**，用于衡量当前颜色偏离灰度的程度，即：

$$RampChroma = max(RampRGB.r, RampRGB.g, RampRGB.b) - min(RampRGB.r, RampRGB.g, RampRGB.b)$$

> *上一次见到色度这个词还是在学《数字视音频基础》的时候。* 色度并不等同于饱和度，两者意义相近，但计算方式不同：  
> $$饱和度 = \frac{色度}{颜色通道中的最大值}$$

而后终末地以色度作为 Ramp 图颜色的权重：

$$RampColorEffect = lerp(1, RampRGB, RampChroma)$$

$$MainDiffuseBRDF\_ramp = MainDiffuseBRDF \times RampColorEffect$$

-   **亮度补偿**

终末地之所以采用上述美术设计，大概是为了**削弱** Ramp 的颜色影响，仅为漫反射提供一定的颜色倾向，同时尽可能不破坏原有的明暗关系。

但无论是直接将 Ramp 图颜色直接与漫反射相乘，还是采用上述美术设计，漫反射的颜色亮度都会改变，因此我们还需要计算亮度补偿。

这部分比较简单，我们只需要计算出添加 Ramp 图颜色前后的漫反射结果的比值，同时防止该比值在 Ramp 颜色过暗时太大，然后将该比值乘回计算色度加权后的漫反射颜色，即可得到最终结果：

$$LC = clamp(\frac{Luminance(MainDiffuseBRDF)}{max(Luminance(MainDiffuseBRDF\_Ramp), 0.01)}, 0, 1.5)$$

$$MainDiffuseBRDF\_RampControlled = MainDiffuseBRDF\_ramp \times LC$$

### 日光强度

这部分也是参考文章中所提到的（大佬们真的太强了），终末地中的角色存在着**弱日光/日光直射状态**间的切换，这里的代码我就不做太多阐述了，毕竟也是一种美术方面的设计，各位如果想深究原理的话可移步至参考文章查看。

我们首先将三层漫反射颜色中的亮部颜色的饱和度提升 1.2 倍（大概是为了防止后续乘以暗处光源颜色后过灰？），然后通过前文提到的 $AoShadowNoFRamp$ 控制暗部颜色和提升饱和度后的亮部颜色之间的过渡（毕竟是弱日光状态，应该也用不上极暗部），最后将这里得到的弱日光状态下的颜色与 $MainDiffuseBRDF\_RampControlled$ 之间使用日光强度 $\_DayStrength$ 控制过渡即可，得到 $MainDiffuseBRDF\_Final$ 。

![](/img/角色渲染/Unity_URP_拉完了的终末地角色渲染复刻笔记/012.jpg)

### 光源计算

在得到 $MainDiffuseBRDF\_Final$ 后，我们还需要计算光源颜色，将这两者相乘后即可得到最终的直接光漫反射颜色。

-   **拆解主光颜色与主光强度**

为了便于**单独调整主光颜色或主光强度**，我们可以先将主光颜色除以主光亮度，得到$MainLightColorNormalized$，而后设置两个人为控制的变量 $\_IsNeedSelfLight$ 与 $\_SelfLightIntensity$ 来单独控制主光强度：

$$MainLIghtColorNormalized = \frac{\_MainLightColor.rgb}{max(Luminance(\_MainLightColor.rgb),  0.001)}$$

$$MainLightIntensity = lerp(max(Luminance(\_MainLightColor.rgb), 0.001), \_SelfLightIntensity, \_IsNeedSelfLight)$$

-   **根据明暗区域调整主光颜色**

之所以要单独拆解主光颜色，是因为我们希望能够自定义亮部与暗部区域各自的主光颜色。亮部区域的主光颜色依然为 $MainLightColorNormalized$，暗部区域的颜色则由人工控制，我们一方面希望暗部区域的主光颜色能够降低 $MainDiffuseBRDF\_Final$ 的亮度，另一方面不希望它改变原有的色相，因此此处我们使用的是灰度色，并使用 $MinShadowEffect$ 控制明暗部分主光颜色的过渡：

$$MainLightDarkNormalized = Luminance(MainLightColorNormalized \times \_MainLightColor\_dark).xxx$$

$$MainLightColor = lerp(MainLightDarkNormalized, MainLightColorNormalized, MinShadowEffect) \times MainLightIntensity$$

-   **顶部补光**

终末地中还存在着一盏从角色正上方向下照射的顶光光源，我们可以通过观察诸如角色胸部下方的区域阴影得到该结论。

![](/img/角色渲染/Unity_URP_拉完了的终末地角色渲染复刻笔记/013.jpg)

$$OtherLightResultRaw = \_OtherLightColor.rgb \times OtherLightNoL$$

而后我们设置两个参数，分别控制弱日光状态和日光直射状态下的顶光强度（弱日光状态下只存在顶光照射，日光直射状态下主光与顶光均存在，也是一种美术效果上的设计），得到最终的光源颜色 $MainLightColor\_Final$：

$$LightColorDark = OtherlightResultRaw \times \_OtherLightResultStrength\_dark$$

$$LightColorLight = MainLightColor + OtherLightResultRaw \times \_OtherLightResultStrength\_light$$

$$MainLightColor\_Final = lerp(LightColorDark, LightColorLight, \_DayStrength)$$

-   **漫反射最终结果**

$$MainDiffuseResult = MainLightColor\_Final \times MainDiffuseBRDF\_Final$$

## 直接光镜面反射

### `SpecularBRDF`

`SpecularBRDF` 表示角色表面对直接光产生镜面反射的能力，在具体介绍计算方式前，我们先来回顾一下 PBR 镜面反射模型，然后在讲讲终末地在此基础所做的修改。

-   **微表面镜面反射原理**

PBR 渲染基于三大原则：能量守恒、**微表面理论**（Microfacet Theory）以及使用真实物理参数。其中的微表面模型认为，即使物体表面看上去整体平滑，但微观上仍由大量朝向不同的微平面组成，每个微平面均满足理想镜面反射（反射角 = 入射角），只有当微平面的法线方向恰好能够将光线反射向摄像机时，才会产生高光。

根据 Cook-Torrance 镜面反射模型，标准镜面反射需要关注以下三个部分：

$$SpecularBRDF = NormalDistribution \times Visbility \times Fresnel$$

-   `NormalDistribution`：有多少微表面能够产生漫反射，即法线方向与半角向量重合的微表面的密度；
-   `Visbility`：这些微表面是否被其他微表面阻挡；
-   `Fresnel`：这些微表面能够反射多少光，即到达微表面的光有多少产生了镜面反射。

当然这个式子写法是简化过的，其原来的写法如下：

$$SpecularBRDF = \frac{D \times F \times G}{4 \times NoL \times NoV}$$

其中 $D、F、G$ 项对应上述三项，我们只是将 $G$ 项与分母合称为 `Visbility` 便于理解。

-   **$D$ 项：`GGX` 高光**

显然，我们只需要求出上述的 $D、F、G$ 三项即可。

我们常说的 `GGX` 高光实际上就是上述的 $D$ 项，是一种微表面法线分布函数，用于计算在给定方向 `h`（半角向量）时有多少比例的微表面法线指向 `h` 方向，其计算公式如下：

$$D_{GGX}(h)= \frac{\alpha^2}{\pi({NoH}^2 \times (\alpha^2 - 1) + 1)^2}$$

其中 $\alpha$ 为粗糙度 `Roughness` 的平方。但最终计算时我们忽略了分母中的 $\pi$ ，通过后续调整强度的方式来进行修正，即：

$$SpecularD= \frac{\alpha^2}{({NoH}^2 \times (\alpha^2 - 1) + 1)^2}$$

-   **$V$ 项：基于标准 `Smith GGX` 的近似**

我们将上述的 $G$ 项与 Cook-Torrance 的分母合并称作 $V$ 项。`Smith GGX` 是一个 $G$ 项的公式，将其与分母结合整理后，得到完整的 `Smith GGX Visbility` 公式如下：

$$V_{SmithGGX} = \frac{0.5}{NoL \sqrt{ {NoV}^2(1 - \alpha^2) + \alpha^2} + NoV \sqrt{ {NoL}^2(1 - \alpha^2) + \alpha^2} }$$

但这个公式实在是太耗性能了，因此我们需要对其进行相当程度的简化：

首先我们舍弃了光源方向对微表面遮挡的影响，即认为 $NoL = 1$ ，原因在于我们将会自定义一个风格化的半角向量用于后续计算高光，这个半角向量一定程度上削弱了主光的影响，得到初步简化后的公式：

$$V_{SmithGGX}' = \frac{0.5}{\sqrt{ {NoV}^2(1 - \alpha^2) + \alpha^2} + NoV }$$

显然我们还需要想办法优化 $\sqrt{ {NoV}^2(1 - \alpha^2) + \alpha^2}$ ，该项最“便宜”的一个上界为 ${NoV} + \alpha$ （比较一下两者的平方） ，代入上式后得到最终的 $V$ 项：

$$SpecularV = \frac{0.5}{2NoV + {Roughness}^2 + 0.0001}$$

当然这两步近似非常激进，会压低高光的亮度，但是在尽可能保留美术效果的同时大量节约了性能消耗。

-   **$F$ 项：高光重映射**

传统的 $F$ 项通常使用 Schlick Fresnel：

$$Fresnel = F0 + (1 - F0)(1 - VoH)^5$$

但是终末地并没有直接这么做：由于 $F0$ 中带有颜色信息，$F$ 项通常决定了高光的颜色。终末地可能是出于为了能够便于调整不同区域的高光颜色，以及性能优化的角度出发，他们使用了一张 $F0$ 的重映射贴图，如下所示：

![](/img/角色渲染/Unity_URP_拉完了的终末地角色渲染复刻笔记/014.jpg)

我们只需要将 $F0$ 与采样结果相乘，即可得到最终的 $F$ 项：

$$F0\_refined = F0 \times RefineF0Color$$

那么应该如何采样这张贴图呢？根据参考文章，这张图类似于 IBL 的二维查找表，我们先来看看横坐标：

$$RefineF0U = SpecularD \times {Roughness}^2$$

之所以要使用 $SpecularD$ ，是因为它只与 $NoH$ 相关，能够描述当前像素距离高光中心的远近程度，值越大越靠近高光中心，其取值范围为 $[\alpha^2, \frac{1}{\alpha^2}]$，那么为什么还要乘以 `Roughness2` 呢？我们不妨观察一下如下两条函数曲线（取 $\alpha = 0.5^2$）：

![](/img/角色渲染/Unity_URP_拉完了的终末地角色渲染复刻笔记/015.jpg)

左图为 $SpecularD$ ，右图为 $SpecularD \times {Roughness}^2$ ，我们可以将横坐标看做 $NoH \in [0,1]$ ，纵坐标则对应 U 轴，很明显，左图是取不到 U 值较小的区域的，同时在 $NoH \in [0.9, 1]$ 范围内会出现重复采样，高光中心颜色的动态范围缺失，而右图明显优于左图。

纵坐标的公示如下：

$$RefinedF0V = roughness \times (1 - AO)$$

这个公式的话笔者就没有什么好解释的了，笔者猜测这也算是美术效果方面的实现？也就是环境遮蔽越强，表面越粗糙，纵坐标越大，采样的高光颜色越鲜艳。换句话说，越粗糙遮蔽越强的区域需要更强的美术调色以避免失去颜色层次。

> 笔者写到这里才发现自己的这张高光重映射图和参考文章里的图**上下颠倒**了，当时还以为是素材里没给小陈的图，所以演示视频里的渲染效果是**不包含这部分**的，这下真是汗流浃背了QAQ  
> 这也侧面印证了整理笔记的重要性  
>   
> 采样高光重映射图的效果如下：

![](/img/角色渲染/Unity_URP_拉完了的终末地角色渲染复刻笔记/016.jpg)

最后，我们得到了 `SpecularBRDF`：

$$SpecularBRDF = SpecularD \times Specular V \times F0\_refined$$

-   **风格化半角向量**

上文中我们提到，终末地使用了一种二次元风格化的半角向量用于高光计算，传统的半角向量由 `LightDir` 和 `ViewDir` 计算得出，我们需要调整这两个向量：

`ViewDir` ：这玩意比较简单，我们前文已经提到过，可以使用 `CameraForward` 向量替代 `ViewDir`，获得更加二次元的光照结果；

`LightDir`：我们先前提到过弱日光状态与日光直射状态，当角色处于弱日光状态下时，理论上来说，此时主光对于角色的影响很小，这就意味着我们需要在 `LightDir` 中为主光增添权重，那么应该如何衡量这种权重呢？换句话说，当角色处于弱日光状态下时，`LightDir` 的方向应该取决于什么呢？答案是相机方向，也就是 `CameraForward`。终末地通过 `CameraForward` 和真实主光源方向 `MainLightDir` 构建了一个混合光源方向，混合的过程我想应该也是美术效果上的实现，所以没法解释太多：

我们首先要在 `CameraForward` 的基础上构建一个全新的相机光源方向：

$$ForwardLightDirY = lerp(0.5, MainLightDir.y, \_DayStrength)$$

$$ForwardLightDir = normalize(CameraForward.x, ForwardLightDir.y, CameraForward.z)$$

不难看出，在日光直射状态，相机光源的俯仰角由主光源控制，而在弱日光状态下，相机光源处于水平方向上。而后我们将这个相机光源方向与真实主光源方向进行加权混合：

$$EffectiveLightDir = \frac{2ForwardLightDir + \_DayStrength \times MainLightDir}{2 + \_DayStrength}$$

这是一个加权平均，至于为什么让相机光源的权重大于真实主光源的权重，应当就是美术上的设计了。

最后我们只需要像正常计算 `HalfDir` 那样加上 `ViewDirFinal` 即可（`CameraForward` ）：

$$HalfDirNew = normalize(ViewDirFinal + \frac{2ForwardLightDir + \_DayStrength \times MainLightDir}{2 + \_DayStrength})$$

化简后得到最终的计算公式：

$$HalfDirNew = normalize((2 + \_DayStrength) \times ViewDirFinal + {2ForwardLightDir + \_DayStrength \times MainLightDir})$$

### 计算高光结果`MainSpecularResult`

计算完毕 `SpecularBRDF` 之后，我们还需要考虑场景中的灯光颜色、阴影、AO 和高光强度对于高光的影响。标准的 Cook-Torrance 高光结果如下所示：

$$DirectSpecular = IncomingLight \times SpecularBRDF \times NoL \times Shadow$$

> 接下来的计算与该式不完全一致，我们省略了 $NoL$ 项，读者可以思考一下原因所在。

-   **明暗部遮罩**

这里我们同样需要考虑弱日光/日光直射状态：

$$SpecularShadowEffect = lerp(AoShadowNoFRamp, MinShadowEffect, \_DayStrength)$$

简单来说，弱日光状态下，高光主要由相机光源，也就是我们上面计算的风格化半角向量决定，因此此时的明暗遮罩也使用与相机方向相关的 `RampNoF` ，同时 `AoShadowNoFRamp` 是暗部因素相乘的结果，得到的结果更暗，符合弱日光状态的需求；日光直射状态就直接使用 `MinShadowEffect`，此时高光重新受到主光影响，因此使用包含 `RampNoLRemap` 的 `MinShadowEffect`。

而后我们通过如下的方式来手动调控明暗遮罩的强度：

$$SelfAoShadowEffect = lerp(\_SelfAoShadowStrength, 1, SpecularShadowEffect)$$

但是 `SpecularShadowEffect` 很有可能会将颜色拉到全黑，因此我们需要对其进行一定的重映射：

$$SpecularLightMask = SpecularShadowEffect \times 0.5 + 0.5$$

也就是保证至少保留一半的高光（$[0,1] \rightarrow [0.5,1]$），而后同时使用 `SelfAoShadowEffect` 和 `SpecularLightMask` 两层遮罩，前者负责控制暗部高光最低保留量，后者让高光进入暗部时更加柔和。

-   **组合结果**

由此我们得到最终的直接光镜面反射结果：

$$\begin{aligned} MainSpecularResult &= MainLightColor\_Final \times SpecularBRDF \times SpecularLightMask \\&\times SelfAoShadowEffect \times \_SpecularStrength \end{aligned}$$

## 间接光镜面反射

我并没有添加间接光漫反射，主要是因为不加这块最终的渲染效果也已经尚可，明暗部颜色已经受到了 Ramp 图严格的控制。不过终末地中肯定是存在间接光漫反射的，笔者猜测这种漫反射尤其体现在色调上的修改，读者不妨比对一下终末地中的角色位于景玉谷竹林内外色调的变化。

间接光高光部分使用的是参考文章中的代码，这段代码完全不是我这种新手小白能看得懂的QAQ，我将其复制粘贴过来供各位参考，回头有空的话再回来补一下分析（已补）：

```text
// IBL高光计算
    float roughness4 = roughness2 * roughness2;
    float roughness6 = roughness4 * roughness2;
    float NoV2 = NoV * NoV;
    float NoV3 = NoV2 * NoV;
    float fit_A = 3.32707 * NoV + 0.0365463;
    float fit_B = -9.04755 * NoV + 9.0632;
    float IBLspecular_brdf1 = fit_A + fit_B * roughness2;

    float fitX = 3.59685 * NoV2 - 1.36772 * NoV3 + 1.0;
    float fitY = 9.22949 * NoV3 - 16.3174 * NoV2 + 9.04401;
    float fitZ = -20.2123 * NoV3 + 19.7886 * NoV2 + 5.56589;
    float3 nvFactors = float3(fitX, fitY, fitZ);
    float IBLspecular_brdf2 = dot(nvFactors, float3(1, roughness2, roughness6));

    float IBLspecular_brdf = IBLspecular_brdf1/IBLspecular_brdf2; 

    // IBL高光函数计算继续 拟合Lut图查找部分 DFG拟合板块
    float scale_fit_part1 = dot(float2(-1.28514, 1.0), float2(NoV, 0.990440011));
    float scale_fit_part2 = dot(float2(1.0, -0.75591), float2(1.29678, NoV));
    float env_scale = dot(float2(scale_fit_part1, scale_fit_part2), float2(1, roughness2));
    float bias_fit_x = dot(float3(2.92338, 59.4188, 1.0), float3(NoV, NoV3, 1.0));
    float bias_fit_y = dot(float3(1.0, -27.0302, 222.592), float3(20.3225, NoV, NoV3));
    float bias_fit_z = dot(float3(626.130, 316.627, 1.0), float3(NoV, NoV3, 121.563004));
    float bias_denominator = dot(float3(bias_fit_x, bias_fit_y, bias_fit_z), float3(1,roughness2,roughness6));
    float env_bias = env_scale / bias_denominator;

    float3 IBLspecular_brdf_final = IBLspecular_brdf * F0 + env_bias;
    float IBLspecular_brdf_final_noF0 = IBLspecular_brdf  + env_bias;
    // 把IBL的传统预积分过程，拟合成了一个标准数学函数
    

    // IBL高光补充项 多级弹射补偿 前面是单次弹射的函数拟合
    float directionalAlbedo = IBLspecular_brdf_final_noF0;
    // 计算多级弹射补偿因子 (Kulla-Conty Approximation)
    // 目的：找回在微表面缝隙中经过多次弹射后才射出的光线
    float energyLossFactor = (1.0 - directionalAlbedo) / directionalAlbedo;
    // 补偿颜色主要受 F0 影响
    float3 ms_compensation = F0 * energyLossFactor;
    // 最终的 IBL BRDF = 基础项 + 补偿项
    // 这能显著提升粗糙材质在高光下的饱和度和亮度
    float3 final_ibl_brdf = IBLspecular_brdf_final * (1.0 + ms_compensation);

    // IBL高光 light部分获取
    float3 reflectDir = reflect(-viewDir, normalWS);
    reflectDir.x = -reflectDir.x;
    // reflectDir.y = -reflectDir.y;
    reflectDir.z = -reflectDir.z;

    // 旋转环境贴图
    float angle = _EnvRotation * 0.0174532925; // 将角度转换为弧度 (PI/180)
    float s, c;
    sincos(angle, s, c); // 同时获得正弦和余弦

    float3 rotatedDir;
    rotatedDir.x = reflectDir.x * c - reflectDir.z * s; // 旋转 X
    rotatedDir.y = reflectDir.y;                       // Y 保持不变
    rotatedDir.z = reflectDir.x * s + reflectDir.z * c; // 旋转 Z
    
    float envMap_level = log2(max(0.01, roughness));
    envMap_level = envMap_level * 1.2 + 5.0;
    float3 envMap_color = SAMPLE_TEXTURECUBE_LOD(_EnvMap, sampler_LinearRepeat, rotatedDir, envMap_level);
    envMap_color *= _EnvColor;
    
    // IBL高光结果获取
    float3 indirLightSpecular = envMap_color * final_ibl_brdf * _EnvLightStrength ;
```

> 补：由于笔者个人很不喜欢纯粹的代数推导，因此我将以下的解释尽可能翻译成了人话，可能会出现多处“学术”错误，还请各位谅解

*GPT：上述代码是基于 Split-Sum Approximation 的 GGX 镜面 IBL：用一组有理函数代替传统的 DFG LUT，再额外加入简化的多次散射能量补偿。这组拟合系数来自《Ray Tracing Gems》第 32 章的环境 BRDF 近似，NVIDIA NRD 中也有对应实现，使用了 GGX 和 Schlick 菲涅尔近似。*

间接光镜面反射的求解需要使用渲染方程，当然在实时渲染中我们肯定不会直接做积分，而是用各种手段近似求解。此处我们使用的是 Split-Sum IBL（写法上做了一定简化）：

$$L_{o}^{spec} = {PrefilterdEnv}(ReflectDir,Roughness) \times EnvironmentBRDF(NoV, Roughness, F0)$$

其中前半部分用于计算环境提供了什么光，我们将通过 `CubeMap` 获取； 后半部分表示材质会反射多少光，也就是代码前半段所计算的内容。

-   $\bf{EnvironmentBRDF}$：

该项原先的计算公式为一个半球积分：

$$EnvironmentBRDF = \int_{\Omega^+} f_{spec}(L, V) \, NoL \, d\omega_L$$

我们使用的是 Cook-Torrance 模型，代入后结果如下：

$$EnvironmentBRDF = \int_{\Omega^+} \frac{D_{GGX} F_{Schlick} G_{Smith} }{4 \, NoL \, NoV} \, NoL \, d\omega_L$$

显然我们需要 $NoV、NoL、NoH、VoH$ 等一系列参数，还需要做积分，但实际上我们只需要用到 $NoV$ 以及 `Roughness` ，因为在传统做法中，我们会通过预积分的方式提前生成一张 DFG LUT，这是一张二维查找表，生成时会针对每一组 $NoV$ 和 `Roughness` 计算 $D$ 项和 $G$ 项的积分结果，最后通过 $uv = (NoV, Roughness)$ 采样。而 $F$ 项使用的是 Schlick Fresnel：

$$F = F_0 + (1 - F_0)(1 - {VoH})^5$$

该项对于 $F_0$ 来说是线性的，我们可以将其代回到上式中，开始逐步化简：

令 $W = \frac{D_{GGX} \ G_{Smith} }{4NoL \ NoV} NoL$，$F_c = (1 - VoH)^5)$，$F_0$ 作为常数项可以提取到积分外面：

$$EnvironmentBRDF = \int_{\Omega^+} W(F_0(1 - F_c) + F_c) \ d \omega_L  = F_0\int_{\Omega^+} W(1 - F_c) \ d\omega_L + \int_{\Omega^+} W \ F_c \ d\omega_L$$

我们将前后两部分积分分别命名为 `Scale` 和 `Bias` ，得到最终化简后的结果：

$$EnvironmentBRDF = F0 \times Scale + Bias$$

以上是传统做法，终末地的做法则是将 DFG LUT 换成了一个输入为 $(NoV, Roughness)$ 的数学函数，计算出原先应当从 DFG LUT 返回的 `Scale` 与 `Bias` ，这也就是为什么代码前半段有大量的常数的原因，他们都是拟合函数公式中的系数，最后计算出 `float3 IBLspecular_brdf_final = IBLspecular_brdf * F0 + env_bias;`。

-   **Kulla-Conty 能量补偿**

Kulla-Conty 是一种用于微表面模型的能量补偿近似算法，旨在通过经验公式快速估算并补全因忽略‌**微平面多次散射**‌而导致的能量损失，使粗糙材质在实时渲染中保持近似能量守恒。‘

那么我们怎么才能知道能量损失了多少呢？

我们回到最开头的公式：

$$L_{o}^{spec} = {PrefilterdEnv}(ReflectDir,Roughness) \times EnvironmentBRDF(NoV, Roughness, F0)$$

等号左边就是间接光高光的结果，右边的 $PrefilterdEnv$ 是环境光的输入，相当于入射到微表面的总能量，那这两个量的比值，也就是 $EnvironmentBRDF$ ，不就是输出能量与输入能量之间的比值吗？

$F_0 = 1$ 时，微表面为理想镜面，所有入射能量均用于反射，此时的 $EnvironmentBRDF$ （下称 $E$ ），即 `Scale + Bias`，就是用于反射的能量比例，$1 - E$ 即为损失的能量比例。我们将该比例进行归一化 $\frac{1 - E}{E}$ ，也就是计算损失的能量相对于目前保留下来的能量有多大，最后与 $F0$ 相乘来补偿强度与颜色，将结果加一之后乘回先前的 $EnvironmentBRDF$ 。

```text
float3 IBLspecular_brdf_final = IBLspecular_brdf * F0 + env_bias;
    float IBLspecular_brdf_final_noF0 = IBLspecular_brdf  + env_bias;
    // 把IBL的传统预积分过程，拟合成了一个标准数学函数
    
    // IBL高光补充项 多级弹射补偿 前面是单次弹射的函数拟合
    float directionalAlbedo = IBLspecular_brdf_final_noF0;
    // 计算多级弹射补偿因子 (Kulla-Conty Approximation)
    // 目的：找回在微表面缝隙中经过多次弹射后才射出的光线
    float energyLossFactor = (1.0 - directionalAlbedo) / directionalAlbedo;
    // 补偿颜色主要受 F0 影响
    float3 ms_compensation = F0 * energyLossFactor;
    // 最终的 IBL BRDF = 基础项 + 补偿项
    // 这能显著提升粗糙材质在高光下的饱和度和亮度
    float3 final_ibl_brdf = IBLspecular_brdf_final * (1.0 + ms_compensation);
```

接下来的部分就是采样环境贴图了，此处不再过多阐述。

## 边缘光

欢迎来到笔者奇思妙想最多的一部分，各位最好还是直接移步至 [https://zhuanlan.zhihu.com/p/2054958065078871199](https://zhuanlan.zhihu.com/p/2054958065078871199) 看这位大佬的边缘光，我直到开始做头发的边缘光的时候才发觉不对劲（先前也已经发现有不对劲的地方了，但是被我用各种奇奇怪怪的 tricks 掩盖过去了，但是头发我是真没招了，这也是为什么我的演示视频里没有打开头发的边缘光的原因），但是当时我还不知道有**深度边缘光**这种东西QAQ，大佬们真的太强了。

因此还是先推荐各位移步至这位大佬的帖子，以下内容仅在不开启角色展示界面的边缘高光的情况下能够保持正确性，仅作为思路历程的展示，仅供各位参考。

> 深思熟虑之后我还是选择照着参考文章里讲吧，免得我的 tricks 给各位带偏了（）  
> 那我前面为啥还要叠这么多甲

我的 tricks 主要是对光源方向进行了一些奇奇怪怪的修正，各位还是就用正常的 $NoV$ 就好，不过需要注意的是此处依然使用的是 `CameraForward` 作为 `ViewDir`。

### NoV 边缘光

接下来我们来计算一下 $NoV$ 边缘光的范围，下面的参数我想应该也是美术效果上的实现：

$$RimStart = 0.8 - 0.6 \times \_RimLightArea$$

$$RimEnd = 0.9 - 0.4 \times \_RimLightArea$$

$$RimMask = smoothstep(RimStart, RimEnd, 1 - NoV)$$

然后是边缘光的颜色，我们让其在白光的基础上受到一定的直接光漫反射亮部的影响：

$$RimDiffuseColor = lerp(0.25, DiffuseColorLight, \_RimLightDiffuseColorEffect)$$

最后乘以人工控制的边缘光颜色、边缘光强度以及阴影即可。阴影的部分没有 Ramp 图 `A` 通道，我们会在最后单独添加这部分。

$$\begin{aligned} RimLightNoVResult &= min(AO, ShadowScene) \times RimMask \times \_RimLightColor \\&\times \_RimLightStrength \times RimDiffuseColor \end{aligned}$$

### 基于光照的边缘光

终末地中的边缘光除了会受到视角影响外，还会受到光源方向的影响，我们将只使用主光的 XZ 分量作为光源方向，以此来保证角色边缘光具有稳定的左右分布，不会因为主光高度而大幅上下移动：

$$RimLightNoLxzDir = normalize(MainLightDir.x, 0, MainLightDir.z)$$

同时，终末地中的这部分边缘光主要来自朝向主光的一侧，另一侧几乎完全没有，因此我们需要对这里的 $NoLxz$ 做一定的修改：

$$NoLxzRefine = (-0.5{NoLxz}^2 + NoLxz + 0.5) \times \_DayStrength$$

之所以这个修改能够起效，读者只需要观察一下函数图像即可，该结果在朝向水平主光的一侧为 1（日光直射状态），完全背对主光一侧为 -1。因此，这部分“重映射”既负责增加向光侧的边缘光，还负责压暗另一侧的 $NoV$ 边缘光。

但是 $NoLxzRefine$ 的范围有些太大了，相当于整个向光面，因此我们还需要计算一个美术效果方面的遮罩：

$$NoVMask = smoothstep(0, 1, saturate((0.4 - NoV) \times 5))$$

此处的参数设置同时还考虑了与 $NoV$ 边缘光之间的衔接，读者可以自行思考一下。

而后我们需要计算边缘光的颜色，这部分边缘光与主光相关，因此要考虑光源的颜色以及 `_DayStrength`：

$$RimMainLightColor = lerp(1, MainLightColorNormalized \times MainLightIntensity, \_DayStrength)$$

$$RimNoLxzDiffuseColor = lerp(0.25, DiffuseColorLight, \_RimLightNoLxzDiffuseColorEffect)$$

最后结果如下：

$$\begin{aligned} RimLightNoLxzResult &= RimMainLightColor \times NoLxzRefine \times NoVMask \\ &\times \_RimLightNoLxzStrength \times RimNoLxzDiffuseColor \\&\times min(AO, ShadowScene) \end{aligned}$$

最后我们将两部分边缘光相加，使用 `max` 是因为 `NoLxzRefine` 可能为负数，然后乘以 `RampNoLRemap` ，也就是使用 Ramp 图来划定最后的明暗范围，应当也是美术上的实现：

$$RimLightFinal = max(RimLightNoVResult + RimLightNoLxzResult, 0) \times RampNoLRemap$$

至此，Shader 的基本模块搭建完成。

## 皮肤

我们需要添加 SSS 效果、修改暗部着色逻辑并移除 IBL 高光。

### SSS

这块没有什么好说的，我们只需要实现一下 SSS 效果即可。

![](/img/角色渲染/Unity_URP_拉完了的终末地角色渲染复刻笔记/017.jpg)

### 基于 LUT 图的暗部着色

我们原先计算漫反射暗部的颜色是通过人工给予一个 `_AlbedoDarkStrength` ，再进行饱和度衰减得到的，而终末地提供了一张 LUT 图，我们可以将采样的结果作为 `BaseColorDark` 参与暗部颜色计算：

![](/img/角色渲染/Unity_URP_拉完了的终末地角色渲染复刻笔记/018.jpg)

## 脸部

依旧是 tricks 最多的一集，我们需要使用 SDF、修改暗部着色、添加 SSS、处理脸部与脖子之间的接缝、处理阴影过渡、添加嘴唇高光、删除 IBL以及修改边缘光逻辑。

### SDF

SDF 图的采样没什么好说的，还是老样子，先传入面部的前、上、右侧三个方向向量，然后用主光方向和面部右侧方向的点乘来判断左右。

```text
float lightRight = dot(_FaceRight, MainLightDir); 
float lightForward = dot(MainLightDir, _FaceForward); 
float3 MainLightDirXZFaceDir = normalize( float3(lightRight, 0.000061, lightForward) );

float SdfUvFlag = step(0.0, MainLightDirXZFaceDir.x);
```

我们将采样结果命名为 `SDFValue`，我与参考文章中使用的都是 `SDFValue = (SDFTex.r + SDFTex.g) * 0.5` ，原因在于 SDF 的 `RG` 通道的阴影阈值“强度”不一样：

![](/img/角色渲染/Unity_URP_拉完了的终末地角色渲染复刻笔记/019.jpg)

各位也可以换一种方法：将 `SDFTex.r` （左图）用于光源在角色背后的情况，将 `SDFTex.g` 用于光源位于角色正面的情况，然后将两者的结果使用 `smoothstep` 进行过渡。

同时，终末地在此处也加入了一定的背光补偿，也就是根据摄像机和光照方向之间的夹角计算背光程度，通过 `faceNoL` 计算补偿量：

```text
float faceNoL = MainLightDirXZFaceDir.z;

float2 cameraXZ = normalize(CameraForwardWS.xz); 
float2 lightXZ = normalize(MainLightDirXZ.xz);
float backLight = saturate(-dot(cameraXZ, lightXZ)) * saturate(-faceNoL);
float compensation = -0.5 * faceNoL * faceNoL + 0.5;

faceNoL = faceNoL + backLight * compensation;
```

此时 `faceNoL` 位于 $[-1,1]$ 区间，我们还得转化到 SDF 阈值的 $[0,1]$ 区间：

```text
float threshold = saturate(faceNoL * -0.5 + 0.5 + _SDFShadowOffset);
```

> 懒得敲 LaTeX 了

但是如果我们直接用 `step` 来做阈值计算的话未免太生硬了，我们还需要构造一下左右边界：

```text
float sdfMin = max(threshold * 2.0 - 1.0, 0.0);
float sdfMax = min(threshold * 2.0, 1.0);

float sdfSmooth = smoothstep(sdfMin, sdfMax, SDFValue);
```

最后得到 `SDFNoL` ，由于 $NoL \in [-1,1]$ ，因此我们还需要转化一下：

```text
float SDFNoL = sdfSmooth * 2 - 1;
```

### 脸与脖子的接缝处处理

这是笔者第一次遇见这种问题，也就是由于脸部和皮肤的光照计算不同的原因，导致在脸部和脖子之间面片的交界处会出现很明显的接缝。不过处理方式也很简单，终末地为我们提供了一张贴图 `SDFRefineTex.g` 用于处理这个问题：

![](/img/角色渲染/Unity_URP_拉完了的终末地角色渲染复刻笔记/020.jpg)

该贴图的 `G` 通道标记出了脸与脖子之间的过渡区域，我们只需要利用该贴图在 `SDFNoL` 和皮肤所使用的 $NoL$ 之间线性插值，然后再用该结果去采样 Ramp 图即可：

```text
float NoL = dot(NormalWS, lightDir);
float FaceRampNoL = lerp(SDFNoL, NoL, SDFRefine.g);

float rampU = FaceRampNoL * 0.5 + 0.5; 
float4 ramp = tex2D(_RampTex, float2(rampU, 0.5));
```

### 嘴唇高光

终末地专门做了一张嘴唇高光的贴图，直接采样然后加进 `MainSpecularResult` 里就好：

```text
float3 lipSpecular = tex2D(_LipSpecularTex, uv).r * _LipSpecularColor.rgb * _LipSpecularStrength;
```

### 边缘光

终末地通过 `SDFTex` 和 `SDFRefineTex` 为我们定义好了一套脸部的边缘光：

首先，我们需要计算一个基于 `_FaceRight` `_FaceUp` `_FaceForward` 的头部法线（面部法线肯定不能直接用），换句话说，我们希望该法线以这三个方向作为坐标轴，那么我们只需要计算出面部的每个像素对应的坐标/权重即可。

显然，和基本边缘光一样，我们不希望主光的高度会对边缘光产生影响，因此我们只需要计算 `_FaceRight` 和 `FaceForward` 的权重。两者的权重由 `SDFTex.b` 控制：

```text
float sdfNormalFSWeight = _SDFTex.b * 2 - 1;
float3 sdfNormalFS = float3(sdfNormalFSWeight, 0.000001, 1 - abs(sdfNormalFSWeight));
sdfNormalFS = normalize(sdfNormalFS);
```

当然我们现在还没法使用这条法线，我们还得把他转换到世界空间：

```text
float3 sdfNormalWS = sdfNormalFS.x * _FaceRight 
		   + sdfNormalFS.y * _FaceUp 
		   + sdfNormalFS.z * _FaceForward; 
					     
sdfNormalWS = normalize(sdfNormalWS);
```

别忘了我们还要处理脸部和脖子之间的接缝区域：

```text
float3 normalWS = lerp(sdfNormalWS, normalWS, SDFRefineTex.g);
```

然后我们再用这个法线向量去计算 $NoV$ 即可，同时还要对边缘光宽度做一定的控制，此处和 SDF 阴影过渡区域的计算方法一致：

```text
float rimStart = 0.8 - 0.6 * _RimLightArea; 
float rimEnd = 0.9 - 0.4 * _RimLightArea;

float fresnel = 1.0 - NoV;

float rimArea = smoothstep(rimStart, rimEnd, fresnel);
```

我们还需要加上 `SDFRefineTex.a` 里的边缘光区域遮罩：

```text
float finalRimArea = lerp(rimArea, SDFRefineTex.a, _RimMaskStrength);
```

但是现在的边缘光会在左右脸同时出现，我们希望它只出现在向光的一侧：

```text
float3 cameraRight = normalize(cross(float3(0, 1, 0),CameraForwardWS));
float sideMask = saturate(dot(-cameraRight,faceRimNormalWS));
```

最后再根据 `_FaceForward` 和 `CameraForward` 的点积制作一个转到侧面渐隐的效果即可，笔者还根据这个点积制作了一个场景阴影和 SDF 阴影之间的 `lerp` 过渡，算是一些锦上添花的内容，此处不再赘述。

## 头发

头发这块可以说是笔者做的最拉的一部分，还有很大的改进空间，写出来怕被大家伙笑话hhh，深思熟虑之后还是选择跳过这部分（肯定不是因为我太懒）。

推荐大家去看看这位大佬的头发 Shader 实现 [https://zhuanlan.zhihu.com/p/2054958065078871199](https://zhuanlan.zhihu.com/p/2054958065078871199) 。

刘海阴影的处理走的是 [https://zhuanlan.zhihu.com/p/1972323352069797451](https://zhuanlan.zhihu.com/p/1972323352069797451) 这位大佬的方案，换到 Unity 里自然就是模板测试了。

## 眼睛

### 视差偏移

首先我们需要使用视差偏移制作一下虹膜视差效果，这是因为角膜在外层，虹膜位于角膜内部。因此从侧面看眼睛时，虹膜应该相对角膜表面发生位移，也就是一个向内凹陷的效果。我们只需要算一下采样 BaseColor 的 uv 即可：

![](/img/角色渲染/Unity_URP_拉完了的终末地角色渲染复刻笔记/021.jpg)

### 法线

但实际上眼球是一个向外凸出的半球形，眼睛上的高光形状不应该遵循平面面片的法线，我们希望能够模拟出角膜向外凸出的效果，然后再去制作高光。

也就是说，我们希望以眼球的中心点为圆心，创建一个球面法线。我们可以从 uv 入手：圆心自然位于 $uv = (0.5,0.5)$ 的区域（BaseColor 就是这样画的），那么眼球就是一个半径为 0.5 的球体而已，计算比较简单：

```text
float2 centerUV = frac(uv) - float2(0.5, 0.5); 
float2 diskXY = centerUV * 2.0; 
float radius2 = dot(diskXY, diskXY); 

float z = max(sqrt(max(1.0 - min(radius2, 1.0), 0.0)), 1e-19);
```

为了简化计算，上述代码将圆心平移到了原点，并将半径扩大为 1，也就是单位圆/球，便于计算法线。我们将每个像素的 uv 代入上述代码计算出放缩后的 uv 坐标，而原点与 单位球上与该放缩后的点的 uv 坐标相同的点 之间的连线便是该像素的球形法线方向（这话好绕）。该法线是通过 uv 求出的，自然位于切线空间中，我们再引入一定的放缩系数来控制法线的强度：

```text
float3 curvedNormalTS = float3( diskXY * 0.125 * _CorneaBumpStrength, z );
```

同时，我们还得通过半径判断当前像素是否位于 uv 单位圆/球中，外部的像素还是默认法线：

```text
float3 curvedNormalTS = float3(diskXY * 0.125 * _CorneaBumpStrength, z); 
float outsideCircle = step(0.25, dot(centerUV, centerUV)); 
float3 corneaNormalTS = lerp(curvedNormalTS, float3(0, 0, 1), outsideCircle);
```

> `outsideCircle` 的计算有一些数学上的小巧思，避免了开方运算。  
> 同时也可以用于调色：单位圆内部为眼球，外部则为高光点，我们可以使用 `outsideCircle` 作为遮罩对两部分单独调色，此处不再赘述。

最后把该法线转换回世界空间即可，后续用该法线参与漫反射和 MatCap 计算。MatCap 采样这块没有什么特别的 tricks，不再过多阐述。

### 眼部阴影

终末地给了一张贴图专门用来制作眼部阴影的透明度过渡，这块笔者做的比较随意：

![](/img/角色渲染/Unity_URP_拉完了的终末地角色渲染复刻笔记/022.jpg)![](/img/角色渲染/Unity_URP_拉完了的终末地角色渲染复刻笔记/023.jpg)

## 眉毛

这块做的有些放飞自我了，比较随意。我们主要需要制作“眼透”效果，也就是眉毛与睫毛能够透过头发展示，这块主要使用的是 [https://www.bilibili.com/video/BV17fBFB4EFX/](https://link.zhihu.com/?target=https%3A//www.bilibili.com/video/BV17fBFB4EFX/) 这套方案：我们利用 `Vertex Offset` 让眉毛整体向摄像机偏移即可，但是当摄像机转到角色侧面的时候很容易穿模，笔者这里依旧使用了 `_FaceForward` 和 `CameraForward` 之间的点积，用于控制刘海的透明度，让眉毛能够在摄像机转到会导致穿模的角度前“消失”即可。

但是从角色正面观察，笔者还是觉得单纯地让眉毛移动到刘海前的效果不太好看，毕竟被眉毛遮挡的区域透明度应该略低才对。笔者这里又使用了模板测试，使用两个 Pass，一个 Pass 负责渲染没被头发遮挡的区域，另一个 Pass 渲染被遮挡的区域，同时单独调整这部分的透明度（包括上述的防穿模手段）。

> 这里纯粹是根据笔者个人的审美做的，游戏里被刘海遮挡的部分透明度依然很高，下图中的透明度较低。

![](/img/角色渲染/Unity_URP_拉完了的终末地角色渲染复刻笔记/024.jpg)

## 描边

描边使用的就是最基本的法线外扩，不过稍微做了一点修改：

一是普通的法线外扩是移动模型在模型空间中的位置，但是为了能够便于直接控制屏幕上看到的描边宽度，笔者将其转换进了裁剪空间：

```text
float4 positionCS = TransformObjectToHClip(input.positionOS.xyz);
float3 smoothNormalVS = normalize(mul(UNITY_MATRIX_IT_MV, float4(smoothNormalOS, 0.0)).xyz);

float4 projectedNormalCS =
    mul(
        UNITY_MATRIX_P,
        float4(smoothNormalVS, 0.0)
    );

float2 outlineDirection = normalize(projectedNormalCS.xy);

//...

//positionCS.xy += outlineOffset;
```

二是做了一下屏幕比例的修正，毕竟用的是裁剪空间，横向和纵向的相同数值，在宽屏上不对应相同的像素距离：

```text
float aspectRatio = abs( _ScaledScreenParams.x / _ScaledScreenParams.y ); 
outlineDirection.x /= aspectRatio;
```

三是透视补偿，也就是防止摄像机离角色越远描边越细：

```text
float depthClamp = min(positionCS.w, 20.0); 

//远近距离控制
float distanceFactor = smoothstep( 1.0, 12.0, positionCS.w ); 
float distanceRefine = lerp( 1.0, _ZMinRefine, distanceFactor ); 

float2 outlineOffset = outlineDirection 
					 * _OutlineWidth 
					 * depthClamp 
					 * distanceRefine 
					 * 0.01; 

positionCS.xy += outlineOffset;
```

最后加了一个参数来调整深度，防止 Z-Fighting：

```text
#if defined(UNITY_REVERSED_Z)
    positionCS.z -= _ZBias;
#else
    positionCS.z += _ZBias;
#endif
```

## 后处理

终末地用的是 LUT 调色，但是笔者没搞到这张调色图，只能做一些基本后处理了：

![](/img/角色渲染/Unity_URP_拉完了的终末地角色渲染复刻笔记/025.jpg)

## 效果展示

[https://link.zhihu.com/?target=https%3A//www.bilibili.com/video/BV18tNM69EwS/](https://link.zhihu.com/?target=https%3A//www.bilibili.com/video/BV18tNM69EwS/)

## 结语

很感谢诸位能看到这里，这是一篇拉完了的终末地渲染复刻笔记，也算是阶段性学习的总结，其中肯定包含了不少错误与笔者不成熟的观点，欢迎各位的批评与指正。

再次感谢各位愿意分享与传播知识的大佬们！

希望我不成熟的见解也能够传递出几处可供读者学习的知识叭。祝各位诸事顺利！

> **LaTeX 真的好丑啊，早知道全用代码块了！！**
