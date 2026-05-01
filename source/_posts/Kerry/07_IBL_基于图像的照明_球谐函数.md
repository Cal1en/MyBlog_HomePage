---
title: "[ASE入门] 07 IBL 基于图像的照明 球谐函数"
date: 2026-04-13 08:00:00
updated:
categories: 
  - 技术美术
  - Unity
  - ASE入门
---

{% note danger %}
用于**IBL**的`CubeMap`纹理大小只需要`512 x 512`即可。

{% endnote %}

# Pre-filtered Mipmaps
## 间接光镜面反射
首先我们需要知道，粗糙的物体表面的光泽度很小，也就是说我们观察不到明显的高光区域；光滑的物体表面的光泽度高，因此我们能观察到明显且集中的高光区域。那么我们在使用`CubeMap`的时候应该如何模拟物体表面的粗糙部分呢？

我们首先需要将`CubeMap`贴图的`卷积型`切换为 **`镜面（光泽反射）`**，这样Unity就会自动使用一系列复杂的算法生成`Pre-filtered Mipmaps`并保存到本地，这些`Mipmaps`随着`Mip`等级增加而变得越来越模糊，我们可以使用 **`texCUBElod()`**函数以及**粗糙度**来**采样这些模糊的**`CubeMap`**来表现出粗糙的表面**：

```csharp
_Roughness("Roughness", Range(0,1)) = 0

//...
    
    float mip_level = _Roughness * 6.0;		//通常MipMap最高等级大于等于7 但是我们一般只使用
                                            //前6个层级，因为最后的几个层级过于粗糙
                                            //丢失了大量细节，因此我们只使用[0,6]级
    half4 color_cubemap = texCUBElod(_CubeMap, float4(reflect_dir, mip_level));
```

同理，如果我们要采样反射探针的`CubeMap`，我们可以使用`UNITY_SAMPLE_TEXCUBE_LOD(unity_SpecCube0, reflect_dir, mip_level)`函数。

{% note danger %}
为了得到更好的不同层级之间的`MipMap`之间的过渡效果，我们最好将`CubeMap`设置为`三线性`插值。

{% endnote %}

## 间接光漫反射
我们可以将`CubeMap`贴图的`卷积型`切换为 **`漫反射（发光）`**，这样生成的`Pre-filtered Mipmaps`就可以用于表现物体的漫反射颜色，其余上述高光颜色的区别在于，前者**并不会随着摄像机视角的变化而发生变化**，因此在采样漫反射`CubeMap`的时候，我们并不能直接使用反射方向进行采样，而是需要**直接使用物体表面法线方向进行采样**。

`half4 color_cubemap = texCUBElod(_CubeMap, float4(**normal_dir**, mip_level));`
{% note danger %}
实际上我们一般不会直接使用`CubeMap`作为间接光的漫反射，而是会使用`SH球谐函数`，以此来减少性能消耗。

{% endnote %}

# 球谐函数
<details class="lake-collapse"><summary id="u82dd783e"><span class="ne-text">球谐函数</span></summary><h1 id="wNt3V"><span class="ne-text">球谐函数（Spherical Harmonics）全解析：从数学到实时漫反射渲染</span></h1><h2 id="grnns"><span class="ne-text">第一章：问题的根源——为什么需要球谐函数？</span></h2><p id="u6fc06222" class="ne-p"><span class="ne-text">在实时渲染中，计算**间接漫反射（Indirect Diffuse）**是一个物理上的噩梦。<br /></span><span class="ne-text">间接漫反射的本质是：物体表面某一个点，接收到了来自整个半球方向（360度）所有环境光的能量，并按照 Lambert 漫反射定律（即余弦衰减 </span><span id="dSx3O" class="ne-math"><img src="https://cdn.nlark.com/yuque/__latex/9ea75f81d86aba0a8edef5ae31825155.svg"></span><span class="ne-text">）进行加权求和。</span></p><p id="u443c8db8" class="ne-p"><span class="ne-text">用数学公式表达就是：</span></p><p id="u58a1eddb" class="ne-p" style="text-align: center"><span id="nIS08" class="ne-math"><img src="https://cdn.nlark.com/yuque/__latex/2aa75aacde400d37fd2f6b936600bfac.svg"></span></p><ul class="ne-ul"><li id="ub9241015" data-lake-index-type="0"><span id="GVn1t" class="ne-math"><img src="https://cdn.nlark.com/yuque/__latex/8e8d4af86c328cb4ddffb8572a3377aa.svg"></span><span class="ne-text"> 是来自各个方向 </span><span id="azikT" class="ne-math"><img src="https://cdn.nlark.com/yuque/__latex/79ce3c7a71877c2ff01695e38ade43ca.svg"></span><span class="ne-text"> 的环境光亮度（Environment Radiance）。</span></li><li id="ud03ffefa" data-lake-index-type="0"><span id="LOYkv" class="ne-math"><img src="https://cdn.nlark.com/yuque/__latex/5b1c87170ef54424cbcf2bd4bedcdf1b.svg"></span><span class="ne-text"> 是漫反射的余弦权重。</span></li><li id="u930dfefd" data-lake-index-type="0"><span id="tGcdS" class="ne-math"><img src="https://cdn.nlark.com/yuque/__latex/693ed1b54833a2d88ef1c879438d7b60.svg"></span><span class="ne-text"> 代表对整个半球进行积分。</span></li></ul><p id="u7397a49e" class="ne-p"><strong><span class="ne-text">痛点在于：</span></strong><span class="ne-text"> 实时计算这个积分太慢了。每帧对几百万个像素，每个像素去采样几百次环境光，显卡会瞬间崩掉。</span></p><p id="u0cf9fe59" class="ne-p"><span class="ne-text">我们需要的技术必须满足两点：</span></p><ol class="ne-ol"><li id="ua3a122e7" data-lake-index-type="0"><strong><span class="ne-text">极度压缩</span></strong><span class="ne-text">：把 360 度的环境光信息存进极小的内存里。</span></li><li id="ua0d0ac4b" data-lake-index-type="0"><strong><span class="ne-text">瞬间计算</span></strong><span class="ne-text">：把昂贵的积分运算变成简单的代数运算。</span></li></ol><p id="ue760333d" class="ne-p"><strong><span class="ne-text">球谐函数（SH）就是为此而生的数学救星。</span></strong></p><hr id="A10S5" class="ne-hr"><h2 id="y4pjS"><span class="ne-text">第二章：数学基石——正交基底（Basis Functions）</span></h2><p id="u0786e726" class="ne-p"><span class="ne-text">球谐函数的核心原理是</span><strong><span class="ne-text">基底展开（Basis Expansion）</span></strong><span class="ne-text">。这就像我们在二维平面上用 </span><span id="Tik4M" class="ne-math"><img src="https://cdn.nlark.com/yuque/__latex/c46a4f714c448013d665c58180ee9478.svg"></span><span class="ne-text"> 坐标表示任何位置，或者在信号处理用傅里叶变换（正弦波）拟合声音。</span></p><h3 id="E9wxN"><span class="ne-text">1. 什么是基底？</span></h3><p id="uabfa5b34" class="ne-p"><span class="ne-text">想象一个完美的球面。球谐函数定义了一套分布在球面上的“标准形状”，记为 </span><span id="eQT8z" class="ne-math"><img src="https://cdn.nlark.com/yuque/__latex/62d485d5fb43a206659d02ffec844d49.svg"></span><span class="ne-text">。</span></p><ul class="ne-ul"><li id="ua5343dc5" data-lake-index-type="0"><strong><span class="ne-text">0阶（L0）</span></strong><span class="ne-text">：一个圆球，代表</span><strong><span class="ne-text">平均亮度</span></strong><span class="ne-text">。</span></li><li id="ue1cdb958" data-lake-index-type="0"><strong><span class="ne-text">1阶（L1）</span></strong><span class="ne-text">：三个哑铃形（分别指向 </span><span id="m8Ei6" class="ne-math"><img src="https://cdn.nlark.com/yuque/__latex/836fb2345ac6c510917638bf387ba90a.svg"></span><span class="ne-text">），代表</span><strong><span class="ne-text">光照的方向性</span></strong><span class="ne-text">（哪边亮，哪边暗）。</span></li><li id="u0ac38176" data-lake-index-type="0"><strong><span class="ne-text">2阶（L2）</span></strong><span class="ne-text">：五个更复杂的形状（梅花形、甜甜圈形），代表</span><strong><span class="ne-text">光照的高频细节</span></strong><span class="ne-text">。</span></li></ul><h3 id="IKnoL"><span class="ne-text">2. 正交性（Orthogonality）—— 关键特性</span></h3><p id="u2477a808" class="ne-p"><span class="ne-text">这是球谐函数最重要的数学特性。任意两个基底函数 </span><span id="sDYFj" class="ne-math"><img src="https://cdn.nlark.com/yuque/__latex/99f45a182fbbb1d1f79bea448076630f.svg"></span><span class="ne-text"> 和 </span><span id="n0Y9p" class="ne-math"><img src="https://cdn.nlark.com/yuque/__latex/911cf5f511cadcab4242eb583bcd76b9.svg"></span><span class="ne-text"> 在球面上做乘法积分，结果要么是 1（如果 </span><span id="pX1AL" class="ne-math"><img src="https://cdn.nlark.com/yuque/__latex/1e58c2eeee42be12a8f4332686ef0544.svg"></span><span class="ne-text">），要么是 0（如果 </span><span id="PXCEm" class="ne-math"><img src="https://cdn.nlark.com/yuque/__latex/8845df1ba20ecc59cd02e5f23ee51e7e.svg"></span><span class="ne-text">）。<br /></span><strong><span class="ne-text">这意味着：每一个基底捕捉的信息是互不重叠、绝对独立的。</span></strong><span class="ne-text"> 这是一个极其完美的信号分解工具。</span></p><hr id="y2k4L" class="ne-hr"><h2 id="oUFJh"><span class="ne-text">第三章：具体的物理过程——投影（Projection）</span></h2><p id="u04655e76" class="ne-p"><span class="ne-text">当我们说“烘焙环境光到球谐函数”时，我们具体在做什么？</span></p><h3 id="ilqBA"><span class="ne-text">1. 采样与积分</span></h3><p id="ud816517a" class="ne-p"><span class="ne-text">计算机把环境图（CubeMap）里的每一个像素 </span><span id="nKdaJ" class="ne-math"><img src="https://cdn.nlark.com/yuque/__latex/8e8d4af86c328cb4ddffb8572a3377aa.svg"></span><span class="ne-text"> 拿出来，和每一个基底函数 </span><span id="AcNd4" class="ne-math"><img src="https://cdn.nlark.com/yuque/__latex/0bc0fc6598c5c9d78ba876b8db23288d.svg"></span><span class="ne-text"> 进行点对点的乘法，然后求和：</span></p><p id="u5d6e8629" class="ne-p" style="text-align: center"><span id="FPTdF" class="ne-math"><img src="https://cdn.nlark.com/yuque/__latex/a0784cbe514e44cbbb09d95755f85f19.svg"></span></p><p id="u4ec71043" class="ne-p"><span class="ne-text">这个过程叫做</span><strong><span class="ne-text">投影（Projection）</span></strong><span class="ne-text">。</span></p><ul class="ne-ul"><li id="ue66a7eab" data-lake-index-type="0"><span id="nhbMV" class="ne-math"><img src="https://cdn.nlark.com/yuque/__latex/38b5152cd62b55b08f9bc8e2f02f91a4.svg"></span><span class="ne-text"> 就是</span><strong><span class="ne-text">系数（Coefficients）</span></strong><span class="ne-text">。</span></li><li id="ub539cc37" data-lake-index-type="0"><span class="ne-text">如果你用的是 3 阶 SH，你就会得到 9 个系数（RGB 三个通道就是 27 个数）。</span></li></ul><p id="ud5e7d6cb" class="ne-p"><strong><span class="ne-text">物理意义：</span></strong><span class="ne-text"> 系数 </span><span id="xakca" class="ne-math"><img src="https://cdn.nlark.com/yuque/__latex/38b5152cd62b55b08f9bc8e2f02f91a4.svg"></span><span class="ne-text"> 告诉你，当前的场景环境光里，“0号形状”占多少，“1号形状”占多少……</span></p><hr id="mFabw" class="ne-hr"><h2 id="tdhwi"><span class="ne-text">第四章：间接漫反射的灵魂——球面卷积（Spherical Convolution）</span></h2><p id="ub25ea3ec" class="ne-p"><strong><span class="ne-text">这是你一直想听到的、具体到骨髓的原理。</span></strong></p><p id="uf642908b" class="ne-p"><span class="ne-text">为什么算完了环境光的 SH 系数，就能立刻得到漫反射？<br /></span><span class="ne-text">因为漫反射的本质是环境光 </span><span id="Dkx4u" class="ne-math"><img src="https://cdn.nlark.com/yuque/__latex/8e8d4af86c328cb4ddffb8572a3377aa.svg"></span><span class="ne-text"> 与余弦核 </span><span id="hP7Nq" class="ne-math"><img src="https://cdn.nlark.com/yuque/__latex/dd8a30367c6b9f7b2909fa32af4c7402.svg"></span><span class="ne-text"> 的</span><strong><span class="ne-text">卷积</span></strong><span class="ne-text">。</span></p><h3 id="SRxJL"><span class="ne-text">1. 卷积定理的奇迹</span></h3><p id="u438a978f" class="ne-p"><span class="ne-text">在空间域（直接算像素）里，卷积是地狱级的运算。<br /></span><span class="ne-text">但根据</span><strong><span class="ne-text">卷积定理</span></strong><span class="ne-text">：</span><strong><span class="ne-text">空间域的卷积 = 频域的乘法。</span></strong></p><ul class="ne-ul"><li id="u1585204b" data-lake-index-type="0"><span class="ne-text">我们将</span><strong><span class="ne-text">环境光</span></strong><span class="ne-text">投影到 SH 空间，得到系数 </span><span id="bypI8" class="ne-math"><img src="https://cdn.nlark.com/yuque/__latex/dbf660ad764421dce02b2472e1407ad2.svg"></span><span class="ne-text">。</span></li><li id="u9a7d1a34" data-lake-index-type="0"><span class="ne-text">我们将**余弦核（漫反射模型）**也投影到 SH 空间，得到系数 </span><span id="ywe7D" class="ne-math"><img src="https://cdn.nlark.com/yuque/__latex/e7433bd2b13e63f9632bdff125d45751.svg"></span><span class="ne-text">。</span></li></ul><p id="ub1c68198" class="ne-p"><strong><span class="ne-text">最终的漫反射结果就是这两组系数的乘积再加和！</span></strong></p><p id="u87ce3963" class="ne-p" style="text-align: center"><span id="TiFut" class="ne-math"><img src="https://cdn.nlark.com/yuque/__latex/fa3439636ad4c72a12b514570246c145.svg"></span></p><p id="ub93e5d60" class="ne-p"><span class="ne-text">这里的 </span><span id="jyfvI" class="ne-math"><img src="https://cdn.nlark.com/yuque/__latex/0f5199a2f3a6ea526fbfa90eeaec7f8f.svg"></span><span class="ne-text"> 是一组固定的常数（Lambertian Kernel 权重），它们在数学上被证明是：</span></p><ul class="ne-ul"><li id="ucc2e61b9" data-lake-index-type="0"><span id="O6xeo" class="ne-math"><img src="https://cdn.nlark.com/yuque/__latex/603f990492776956050e8a0feb2cef86.svg"></span></li><li id="u973211b7" data-lake-index-type="0"><span id="IjxyW" class="ne-math"><img src="https://cdn.nlark.com/yuque/__latex/fd0256bd3d054cd5f47a73fc91ce3a18.svg"></span></li><li id="ucad22423" data-lake-index-type="0"><span id="hqXjm" class="ne-math"><img src="https://cdn.nlark.com/yuque/__latex/096659c974cf10aa0a8d2533de064438.svg"></span></li></ul><p id="u2cd33921" class="ne-p"><strong><span class="ne-text">这就是具体原理：</span></strong><span class="ne-text"> Unity 在 CPU 烘焙时，已经把环境光系数乘上了这组 </span><span id="jtfTg" class="ne-math"><img src="https://cdn.nlark.com/yuque/__latex/0f5199a2f3a6ea526fbfa90eeaec7f8f.svg"></span><span class="ne-text"> 系数。</span><strong><span class="ne-text">传给 Shader 的那 27 个数，其实已经是“漫反射光场”的系数了。</span></strong></p><hr id="Xo3co" class="ne-hr"><h2 id="ePgGr"><span class="ne-text">第五章：Shader 端的重建——9个函数与7个变量</span></h2><p id="u612b7b81" class="ne-p"><span class="ne-text">现在进入你之前最愤怒的那个细节：</span><strong><span class="ne-text">为什么是 7 个 float4？</span></strong></p><h3 id="wN3I3"><span class="ne-text">1. 代数展开</span></h3><p id="u484c105b" class="ne-p"><span class="ne-text">在 Shader 里，我们要用法线 </span><span id="TRAA0" class="ne-math"><img src="https://cdn.nlark.com/yuque/__latex/eca3235d6ba0bf02b93ba2347daf1f19.svg"></span><span class="ne-text"> 来还原光照。<br /></span><span class="ne-text">具体的基函数公式（笛卡尔坐标系）是：</span></p><ul class="ne-ul"><li id="u3cd251fa" data-lake-index-type="0"><span class="ne-text">L0: 常数</span></li><li id="uf97dd815" data-lake-index-type="0"><span class="ne-text">L1: </span><span id="bna43" class="ne-math"><img src="https://cdn.nlark.com/yuque/__latex/836fb2345ac6c510917638bf387ba90a.svg"></span></li><li id="udb192df7" data-lake-index-type="0"><span class="ne-text">L2: </span><span id="zuBSe" class="ne-math"><img src="https://cdn.nlark.com/yuque/__latex/42c00e5168de6946d58ac95948b7ddbd.svg"></span></li></ul><h3 id="zwP2O"><span class="ne-text">2. 暴力重组（为什么 9 变 7）</span></h3><p id="u55b7ae40" class="ne-p"><span class="ne-text">为了让 GPU 算得最快，Unity 对这些多项式进行了</span><strong><span class="ne-text">项的合并</span></strong><span class="ne-text">和</span><strong><span class="ne-text">常数项的消解</span></strong><span class="ne-text">。</span></p><ul class="ne-ul"><li id="uedaf5d0b" data-lake-index-type="0"><strong><span class="ne-text">第一步（L0 + L1）</span></strong><span class="ne-text">：<br /></span><span class="ne-text">包含 </span><span id="NnQP0" class="ne-math"><img src="https://cdn.nlark.com/yuque/__latex/fc7298c0f09c142729570c2bc96fbd1d.svg"></span><span class="ne-text">。这些项刚好对应 </span><span id="PXDmy" class="ne-math"><img src="https://cdn.nlark.com/yuque/__latex/12378338197317af735d86298acd2ab9.svg"></span><span class="ne-text">。<br /></span><span class="ne-text">Unity 用 </span><strong><span class="ne-text">3 个 </span></strong><code class="ne-code"><span class="ne-text">float4</span></code><strong><span class="ne-text"> (unity_SHAr/g/b)</span></strong><span class="ne-text"> 存它们。每一路颜色用一个 </span><code class="ne-code"><span class="ne-text">dot</span></code><span class="ne-text"> 指令算完。</span></li><li id="uab03b8df" data-lake-index-type="0"><strong><span class="ne-text">第二步（L2 的一部分）</span></strong><span class="ne-text">：<br /></span><span class="ne-text">包含 </span><span id="ztLUI" class="ne-math"><img src="https://cdn.nlark.com/yuque/__latex/cc582e042aa8ce3eb0385f83b246e3bf.svg"></span><span class="ne-text">。这些项对应 </span><span id="RpcIW" class="ne-math"><img src="https://cdn.nlark.com/yuque/__latex/0ca096995934f42a49142ea87be2aef4.svg"></span><span class="ne-text">。<br /></span><span class="ne-text">Unity 同样用 </span><strong><span class="ne-text">3 个 </span></strong><code class="ne-code"><span class="ne-text">float4</span></code><strong><span class="ne-text"> (unity_SHBr/g/b)</span></strong><span class="ne-text"> 存它们。</span></li><li id="u58fdac15" data-lake-index-type="0"><strong><span class="ne-text">第三步（L2 的最后孤儿项）</span></strong><span class="ne-text">：<br /></span><span class="ne-text">也就是 </span><span id="T5AeK" class="ne-math"><img src="https://cdn.nlark.com/yuque/__latex/1ee1ef0b65bdc82c0483030d8e81d64c.svg"></span><span class="ne-text"> 对应的 </span><span id="Ikbb2" class="ne-math"><img src="https://cdn.nlark.com/yuque/__latex/2aceb2d640ad96085d1985fd8281b6f8.svg"></span><span class="ne-text">。因为它在 RGB 三路都要算，且计算极其简单。<br /></span><span class="ne-text">Unity 决定不浪费 3 个变量，而是用 </span><strong><span class="ne-text">1 个 </span></strong><code class="ne-code"><span class="ne-text">float4</span></code><strong><span class="ne-text"> (unity_SHC)</span></strong><span class="ne-text"> 横向存储 RGB 的 </span><span id="sByLz" class="ne-math"><img src="https://cdn.nlark.com/yuque/__latex/1ee1ef0b65bdc82c0483030d8e81d64c.svg"></span><span class="ne-text"> 系数。</span></li></ul><p id="u1c03d32c" class="ne-p"><strong><span class="ne-text">最终加总：</span></strong><span id="BieR3" class="ne-math"><img src="https://cdn.nlark.com/yuque/__latex/e75e40c6ed1c43f46d7e41a61e8980b4.svg"></span><strong><span class="ne-text">。</span></strong><span class="ne-text"><br /></span><span class="ne-text">这就是 9 个基函数利用</span><strong><span class="ne-text">线性叠加性</span></strong><span class="ne-text">和</span><strong><span class="ne-text">常数合并</span></strong><span class="ne-text">，在 7 个变量里完美重建漫反射的整个逻辑。</span></p><hr id="pLGXJ" class="ne-hr"><h2 id="Xen2L"><span class="ne-text">第六章：总结——你到底在看什么？</span></h2><p id="u1d798d6c" class="ne-p"><span class="ne-text">当你看着一个模型被周围环境柔和地照亮时，你实际上在看一场数学骗局：</span></p><ol class="ne-ol"><li id="ude71ab7f" data-lake-index-type="0"><strong><span class="ne-text">CPU</span></strong><span class="ne-text"> 把几百万像素的环境图，分解成了 9 个</span><strong><span class="ne-text">正交基底</span></strong><span class="ne-text">的系数，并顺手做完了</span><strong><span class="ne-text">球面卷积</span></strong><span class="ne-text">（乘了 </span><span id="ozrLE" class="ne-math"><img src="https://cdn.nlark.com/yuque/__latex/0f5199a2f3a6ea526fbfa90eeaec7f8f.svg"></span><span class="ne-text">）。</span></li><li id="u8cbf9815" data-lake-index-type="0"><strong><span class="ne-text">GPU</span></strong><span class="ne-text"> 拿到了这 27 个“已经算了一半”的系数，通过 </span><strong><span class="ne-text">7 条极其高效的向量指令</span></strong><span class="ne-text">，根据你的法线方向，实时地把那个简化的环境场给还原了出来。</span></li></ol><p id="ubcdef1ac" class="ne-p"><strong><span class="ne-text">四个字核心原理：球面卷积。</span></strong><span class="ne-text"><br /></span><strong><span class="ne-text">数学本质：正交基底展开。</span></strong><span class="ne-text"><br /></span><strong><span class="ne-text">工程实操：7 变量压缩排布。</span></strong></p><p id="u303b2531" class="ne-p"><br></p></details>

我们曾在前向渲染路径中提到过，球谐光照是在`ForwardBase`中进行渲染的，因此如果我们需要使用球谐函数光照的话，我们需要在`Tags{"LightMode"="ForwardBase"}`的`Pass`中调用 **`ShadeSH9`**函数，Unity会根据**天空盒的自发光**计算出球谐函数参量，即可获得球谐光照（间接光漫反射）：

```csharp
Tags{"LightMode"="ForwardBase"}
CGPROGRAM
#pragma vertex vert
#pragma fragment frag
#pragma multi_compile_fwdbase
//...
    half3 env_color = ShadeSH9(float4(normal_dir, 1));
    half3 final_color = env_color * ao * _Tint.rgb * _Expose;
```

	此处我们使用的是三阶球谐函数，其需要使用9个参量：

+ **0阶（L0）**：**一**个圆球，代表**平均亮度**。
+ **1阶（L1）**：**三**个哑铃形（分别指向 $x, y, z$），代表**光照的方向性**（哪边亮，哪边暗）。
+ **2阶（L2）**：**五**个更复杂的形状（梅花形、甜甜圈形），代表**光照的高频细节**。

## 光照探针（组）
除了使用`ShadeSH9`函数来获得这9个参数以外，我们还可以使用光照探针组配合光照烘焙来获取：我们首先需要在场景中放置光照探针组，并编辑光照探测器的数量（复制）与位置：

<!-- 这是一张图片，ocr 内容为： -->
![](/img/Kerry/07_IBL_基于图像的照明_球谐函数/1776683194363-ffe249d6-a006-4c4e-ac08-ad91029c3538.png)

然后在照明面板中勾选`烘焙全局照明`，并生成光照：

<!-- 这是一张图片，ocr 内容为： -->
![](/img/Kerry/07_IBL_基于图像的照明_球谐函数/1776683241168-b74d41f1-b6b0-4568-bddc-be1e62376eaf.png)

这样一来，Unity将会根据场景中模式为`已烘焙`的光源信息计算出每个光照探测器所在位置处的球谐函数参量，并存入每个光照探测器中，然后Unity会根据当前物体与其周围最近的四个光照探测器中存储的球谐函数参量进行插值运算，从而得到该物体处的球谐函数参量。

如果想观察到当前物体正在使用哪四个光照探测器，可以在`照明 - 环境 - 工作流设置 - 光照探测器可视化`中选择`All Probes No Cells`。

<!-- 这是一张图片，ocr 内容为： -->
![](/img/Kerry/07_IBL_基于图像的照明_球谐函数/1776683474130-665f9d90-87af-4cb4-910e-a8548855755a.png)

```csharp
Shader "IBL"
{
	Properties
	{
		//_MainTex ("Texture", 2D) = "white" {}
		_CubeMap("Cube Map",Cube) = "white"{}
		_Tint("Tint",Color) = (1,1,1,1)
		_Expose("Expose",Float) = 1.0
		_Rotate("Rotate",Range(0,360)) = 0
		_NormalMap("Normal Map",2D) = "bump"{}
		_NormalIntensity("Normal Intensity",Float) = 1.0
		_AOMap("AO Map",2D) = "white"{}
		_AOAdjust("AO Adjust",Range(0,1)) = 1
		_RoughnessContrast("Roughness Contrast",Range(0.01,4)) = 1
		//_RoughnessBrightness("Roughness Brightness",Float) = 1
		_RoughnessMin("Rough Min",Range(0,1)) = 0
		_RoughnessMax("Rough Max",Range(0,1)) = 1
		_Roughness("Roughness", Range(0,30)) = 0
		_RoughnessMap("RoughnessMap", 2D) = "black"{}
	}
	SubShader
	{
		Tags { "RenderType"="Opaque" }
		LOD 100

		Pass
		{
            Tags{"LightMode"="ForwardBase"}
			CGPROGRAM
			#pragma vertex vert
			#pragma fragment frag
			#pragma multi_compile_fwdbase

			//#include "Lighting.cginc"
			//#include "AutoLight.cginc"
			#include "UnityCG.cginc"

			struct appdata
			{
				float4 vertex : POSITION;
				float2 texcoord : TEXCOORD0;
				float3 normal : NORMAL;
				float4 tangent : TANGENT;
			};

			struct v2f
			{
				float2 uv : TEXCOORD0;
				float4 pos : SV_POSITION;
				float3 normal_world : TEXCOORD1;
				float3 pos_world : TEXCOORD2;
				float3 tangent_world : TEXCOORD3;
				float3 binormal_world : TEXCOORD4;
			};

			//sampler2D _MainTex;
			//float4 _MainTex_ST;
			samplerCUBE _CubeMap;
			float4 _CubeMap_HDR;
			float4 _Tint;
			float _Expose;

			sampler2D _NormalMap;
			float4 _NormalMap_ST;
			float _NormalIntensity;
			sampler2D _AOMap;
			float _AOAdjust;
			float _Rotate;
			float _Roughness;
			sampler2D _RoughnessMap;
			float _RoughnessContrast;
			//float _RoughnessBrightness;
			float _RoughnessMin;
			float _RoughnessMax;

			float3 RotateAround(float degree, float3 target)
			{
				float rad = degree * UNITY_PI / 180;
				float2x2 m_rotate = float2x2(cos(rad), -sin(rad),
					sin(rad), cos(rad));
				float2 dir_rotate = mul(m_rotate, target.xz);
				target = float3(dir_rotate.x, target.y, dir_rotate.y);
				return target;
			}

			inline float3 ACES_Tonemapping(float3 x)
			{
				float a = 2.51f;
				float b = 0.03f;
				float c = 2.43f;
				float d = 0.59f;
				float e = 0.14f;
				float3 encode_color = saturate((x*(a*x + b)) / (x*(c*x + d) + e));
				return encode_color;
			};

			v2f vert (appdata v)
			{
				v2f o;
				o.pos = UnityObjectToClipPos(v.vertex);
				o.uv = v.texcoord * _NormalMap_ST.xy + _NormalMap_ST.zw;
				o.pos_world = mul(unity_ObjectToWorld, v.vertex).xyz;
				o.normal_world = normalize(mul(float4(v.normal, 0.0), unity_WorldToObject).xyz);
				o.tangent_world = normalize(mul(unity_ObjectToWorld, float4(v.tangent.xyz, 0.0)).xyz);
				o.binormal_world = normalize(cross(o.normal_world, o.tangent_world)) * v.tangent.w;
				return o;
			}
			
			half4 frag (v2f i) : SV_Target
			{
				half3 normal_dir = normalize(i.normal_world);
				half3 normaldata = UnpackNormal(tex2D(_NormalMap,i.uv));
				normaldata.xy = normaldata.xy* _NormalIntensity;
				normaldata.z = sqrt(1 - saturate(dot(normaldata.xy, normaldata.xy)));

				half3 tangent_dir = normalize(i.tangent_world);
				half3 binormal_dir = normalize(i.binormal_world);
				normal_dir = normalize(tangent_dir * normaldata.x
					+ binormal_dir * normaldata.y + normal_dir * normaldata.z);

				half ao = tex2D(_AOMap, i.uv).r;
				ao = lerp(1.0,ao, _AOAdjust);
				half3 view_dir = normalize(_WorldSpaceCameraPos.xyz - i.pos_world);
				half3 reflect_dir = reflect(-view_dir, normal_dir);

				reflect_dir = RotateAround(_Rotate, reflect_dir);
				
				//float roughness = tex2D(_RoughnessMap, i.uv);
				//roughness = saturate(pow(roughness, _RoughnessContrast) * _RoughnessBrightness);
				//roughness = lerp(_RoughnessMin, _RoughnessMax, roughness);
				//roughness = roughness * (1.7 - 0.7 * roughness);
				//float mip_level = roughness * 6.0;

				//float roughness = lerp(_RoughnessMin, _RoughnessMax, saturate(pow(tex2D(_RoughnessMap, i.uv).r, _RoughnessContrast) * _Roughness));
				//roughness = roughness * (1.7 - 0.7 * roughness);	//将粗糙度变为斜率逐渐降低的缓出函数
				//float mip_level = roughness * 6.0;

				//half4 color_cubemap = texCUBElod(_CubeMap, float4(normal_dir, mip_level));
				//half3 env_color = DecodeHDR(color_cubemap, _CubeMap_HDR);//确保在移动端能拿到HDR信息
				//half3 final_color = env_color * ao * _Tint.rgb * _Expose;

				half3 env_color = ShadeSH9(float4(normal_dir, 1));
				half3 final_color = env_color * ao * _Tint.rgb * _Expose;

				//half3 final_color_linear = pow(final_color, 2.2);
				//final_color = ACES_Tonemapping(final_color);
				//half3 final_color_gamma = pow(final_color, 1.0 / 2.2);
				
				return float4(final_color,1.0);
			}
			ENDCG
		}
	}
}

```

