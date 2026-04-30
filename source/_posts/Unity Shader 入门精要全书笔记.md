---
title: (legacy) Unity Shader 入门精要全书笔记
date: 2026-04-30 15:00:00
layout: 
---


>前言：本人原先是通过语雀进行的笔记的记录，但是语雀所导出的Markdown格式兼容性实在是太差了，同时也没有办法导出图片以及语雀的画板，我正在尽力修正该网页的Markdown格式问题，并考虑按照书本的章节将该博客分为多个部分再上传。为了您的浏览体验，编者推荐诸位移步至https://www.yuque.com/cal1en/tata/fzwtz4u3mkcdpysa?singleDoc# 《Unity Shader入门精要 公开版》以查阅编者的完整版笔记。
>~~_这个网页相比语雀最大的好处就是**不卡**_~~

---

>~~欢迎来到新手村/教学关卡~~
> 计算机图形学第一定律：如果它看起来是对的，那么它就是对的。
>


+ Unity中的渲染管线和图形学中的渲染管线基本上指的是相同的概念，但是具体实现和细节方面可能存在一些差异
+ Unity的渲染管线建立在图形学的基础上，但是它具有自己的实现和拓展
+ Unity提供了一个高度可配置和可拓展的框架，允许开发者根据需求自定义渲染流程

# 渲染管线
## 什么是渲染管线 
+ **渲染管线（渲染流水线）**

它是**计算机图形学**中用于将**三维场景**转换为**最终屏幕所见图像**的过程；由**一系列的阶段和操作**组成，每个阶段都负责执行特定的任务，逐步处理输入的集合数据和纹理信息，最终生成可视化图像的过程。

{% note info %}
渲染管线（流水线）就是**将数据分阶段的变为屏幕图像的过程**

{% endnote %}

## 渲染管线的三个阶段
渲染管线（流水线）本质：**<u>将数据处理为屏幕图像</u>**

### 应用阶段
1. 把不可见的物体数据剔除
2. 准备好模型相关数据（顶点、法线、切线、贴图、着色器等等）
3. 将数据加载到显存中
4. 设置渲染状态（设置网格需要使用那个着色器、材质、光源属性等等）
5. 调用DrawCall（CPU通知GPU使用相关的数据和渲染状态进行渲染）

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/63937386/1770651868941-ceb779cc-7723-4bbd-b8c6-4a385ef89ec4.png)

#### 为什么DrawCall多了会影响性能
主要的性能的瓶颈是**CPU**造成的：每次调用DrawCall之前，CPU需要向GPU发送很多内容，包括数据、状态、命令等等。**如果DrawCall过多**，CPU就会把大量的时间花费在**提交DrawCall**上，造成CPU过载，让玩家感受到卡顿

#### 如何减少DrawCall
使用**批处理**，可以有效的减少DrawCall，从而提升性能表现：

1. 合并网格（可以将静态物体合并网格）
2. 共用材质（在不同网格之间共用一种材质）
3. 合并图集（2D游戏和UI中，可以将多张图片合并为一张大图）

### 几何阶段
#### 图元
在渲染管线中，**图元**是指几何数据的基本单元，它**是构成几何体的最小可绘制的单元，**图元可以是**点、线、三角形**，在渲染管线的**几何阶段**，**顶点数据会被组合为图元**。

这些图元将在后续的**光栅化阶段转换为像素**，最终呈现在屏幕上。

#### 几何阶段的作用
渲染管线的几何阶段主要由GPU主导，因此我们无法拥有绝对的控制权，但是GPU为我们开放了部分控制权

+ 几何阶段主要做的事情是**根据应用阶段输入的数据信息进行顶点坐标转换以及裁剪不可见图元等工作**
+ 在渲染管线（流水线）的几何阶段，最主要做的工作就是：**对顶点进行处理，并进行坐标转换，裁剪画面外的图元、将模型的顶点从其本地坐标转换到最终的屏幕坐标中**

对于我们来说，我们只要在顶点着色器中进行一些操作就可以带来不同的表现效果的体现，比如：水波纹、布料等等

![画板](https://cdn.nlark.com/yuque/0/2026/jpeg/63937386/1770730452779-c1c1a0ba-6f4d-4644-84f6-b3c2e1129e41.jpeg)

##### 顶点着色器
它处理来自应用阶段由CPU传递过来的顶点相关数据，输入进来的每一个顶点都会调用一次顶点着色器中的逻辑

+ 顶点着色器需要完成的工作主要有：
    1. **坐标变换**：顶点变换、法线变换、纹理坐标变换等
    2. **顶点属性处理**：顶点的其他属性进行处理，比如顶点颜色、透明度、切线向量等，可以用于实现顶点动画、着色、光照等效果
    3. **顶点插值**：计算顶点属性的插值值

...

##### 曲面细分着色器、几何着色器
均为可选的着色器，并且需要硬件和驱动程序的支持才能使用

##### 裁剪
裁剪阶段会自动的将不在视野内和部分在视野内的图元（点、线、三角形）进行裁剪，我们可以进行一些配置，但是一般我们不需要进行任何处理，渲染管线会自动帮助我们进行处理

##### 屏幕映射
将输入的三维坐标系下的图元坐标转换到屏幕坐标系中

### 光栅化阶段
#### 片元
在渲染管线中，片元是指**在光栅化阶段生成的像素或像素片段**；片元是渲染管线中进行像素级别操作和计算的**基本单位**；**每个片元代表了屏幕上的一个像素，并且具有位置信息和与之相关的属性**，比如：颜色、深度值、法线等等。

#### 光栅化阶段的作用
渲染管线的光栅化阶段同样由GPU主导，同样我们无法拥有绝对的控制权，同样GPU为我们开放了部分控制权。

+ 光栅化阶段主要做的事情是**根据几何阶段输入的信息计算每个图元覆盖哪些像素，以及为这些像素计算他们的颜色等等工作**
+ 在渲染管线（流水线）的光栅化阶段，最主要做的工作就是**对片元（像素）进行最终处理、确定片元（像素）最终是否渲染到屏幕上，并且确定其的最终渲染的颜色效果**

对于我们来说，我们只要在片元着色器中进行一些处理就可以带来不同的表现效果的体现，比如：逼真的水面效果、火焰、黑白、模糊等等效果

![画板](https://cdn.nlark.com/yuque/0/2026/jpeg/63937386/1770733681738-128a551f-da17-4e8e-8881-ff681fbde7a6.jpeg)

##### 三角形设置
几何阶段输入到光栅化阶段的数据主要是三角形网格的顶点信息，我们得到的只是三角形网格每条边的两个端点信息；如果想要得到整个三角形网格对像素的覆盖情况，就必须计算每条边上的像素坐标，为了能计算三角形边界像素的坐标信息，我们必须**得到三角形边界的表示方式（三角形由哪几个顶点围成）**。

+ 在**三角形设置**这个小阶段，**GPU主要做的事情就是计算三角形网格的表示数据。**

##### 三角形遍历
该阶段主要根据三角形设置中计算出的三角形网格数据，检查每个像素是否被一个三角形网格所覆盖，如果覆盖的话，就会生成一个片元（包含屏幕坐标、深度、法线等等信息），这个阶段也被成为<strong><u>扫描变换</u></strong>。

+ 在**三角形遍历**这个小阶段，**GPU主要做的事情就是根据三角形网格信息得到被它们覆盖的片元序列。**

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/63937386/1770734060821-ed1ae7a0-0a0f-4ed4-a9fd-a26a4801e9fb.png)

##### 片元着色器
+ 主要完成对三角形遍历输入的片元序列中的每个片元（像素）的着色计算和属性处理：

  1. **光照计算：** 计算片元的光照效果
  2. **纹理映射：** 根据片元在纹理中的位置，对纹理进行采样，将纹理颜色映射到片元上，实现表面贴图效果
  3. **材质属性处理：** 根据材质的属性，比如颜色、透明度、反射率等，计算片元的最终颜色和透明度
  4. **阴影计算：** 根据光源等信息，计算片元是否处于阴影中，影响其最终颜色

等等

##### 逐片元操作（输出合并阶段）
+ 主要完成对片元着色器输出数据（最终颜色、法线、纹理坐标、深度等）进行各种处理和计算：

  1. 决定每个片元的可见性，比如**深度测试**、模板测试
  2. 如果通过了所有测试，需要把片元的颜色值和已经存储在颜色缓冲区的颜色进行合并（混合）

等等

# Shader
## 什么是Shader
Shader的中文意思是**着色器**，是一种**用于描述如何渲染图形和计算图形外观的程序，主要用于控制图形的颜色、光照、纹理和其他视觉效果**。

着色器通常由着色器语言编写，这些着色器语言提供了指令和语法，用于编写描述光照、纹理映射、阴影、反射等图形外观的代码。

{% note info %}
Shader就是着色器，是用于编写图形表现效果的程序代码

**Shader开发本质**就是对渲染管线（流水线）中上一阶段传递过来的数据进行**自定义处理**后，再传递给下一阶段。通过自定义处理，让图形图像最终能够以我们想要的方式显示到屏幕上

{% endnote %}

## Shader和渲染管线的关系
渲染管线（流水线）的基本概念是将数据分阶段的变为屏幕图像的过程，而**Shader开发就是针对其中某些阶段的自定义开发**，从而决定图形图像最终呈现到屏幕上的表现效果。

在Untiy中，我们学习的Shader开发主要针对渲染管线中的两个小阶段：

+ 几何阶段：**顶点着色器**
+ 光栅化阶段：**片元着色器**

## 图形接口程序
图形接口程序（OpenGL、DX等）主要是**用于控制和管理渲染管线流程**的。通过图形接口程序提供的API，我们就可以配置和操作渲染管线中的某些阶段。通过设置输入数据、控制图形处理、应用各种渲染效果，最终实现图形渲染和呈现。图形接口程序充当了开发者和图形硬件之间的中间层，将开发者的渲染命令和设置转化为硬件能够理解和执行的指令。

{% note info %}
图形接口程序（OpenGL、DX等）提供了对渲染管线（流水线）的控制和管理功能，它是开发者和硬件打交道的**中间层**

{% endnote %}

1. OpenGL（跨平台，几乎所有平台都能使用）
2. DirectX（针对微软相关平台，微软的Windows）
3. Metal（针对苹果相关平台，苹果的MacOS）
4. WebGL (针对网页相关）

### 图形接口程序和Shader的关系
图形接口程序(OpenGL、DX等）为Shader开发提供了各种API，Shader开发。我们需要针对不同的图形接口程序使用不同的Shader开发语言来调用相关API。

图形接口程序会将Shader程序和渲染管线的各个阶段连接起来，它会把我们的数据和指令传递给硬件（GPU等），从而实现图形渲染的最终呈现。

### 不同图形接口程序对Shader开发的影响
+ **使用的着色器语言不同**

OpenGL: GLSL (OpenGL Shading Language)

DirectX: HLSL (High-Level Shading Language)

Metal: MSL (Metal Shading Language)

WebGL: GLSL ES (OpenGL ES Shading Language)

+ **坐标系原点不同**

OpenGL、WebGL、Metal: 原点位于屏幕左下角

DX：原点位于屏幕左上角（注意：最新的DX12可以改为左下角原点）

# 数学
## 齐次坐标
齐次坐标是一种在计算机图形学中常用的表示坐标的方式。它是通过引入一个额外的维度来扩展传统的笛卡尔坐标系，就是将一个原本是$n$维的向量或矩阵用$n+1$维来表示，让我们可以更方便的进行几何变换和矩阵运算。

+ 举例：

三维空间中有一个向量或点（x，y，z），它对应的齐次坐标就是给它加一维，变成

(x，y，z，w),“其中w值的改变可以让它有具有不同的含义。

### 为什么要使用齐次坐标进行矩阵运算
+ 三维空间中的$(x, y,z)$，它既可以表示点，也可以表示向量。那么我们可以利用齐次坐标给它加一维，变成$(x,y,z,w)$。其中，$w=1$时代表一个点，$w=0$时代表一个向量。这样我们就可以明确它是点还是向量了。
+ **3x3矩阵**是不能直接表示平移变换，它**只能表示线性变换**，也就是**只能描述对象的旋转、缩放等线性变换**，而**不能描述对象的平移**。平移涉及到改变对象在空间中的位置，包括移动对象的原点。因此，我们需要引入一个额外的维度来表示平移操作，所以我们使用齐次坐标来将3x3矩阵加一个维度变为4x4的矩阵

{% note info %}
**3x3矩阵**一般称为**线性矩阵**，主要处理**线性变换**（主要进行旋转、缩放等线性变换）

**4x4矩阵**一般称为**仿射矩阵**，主要处理**仿射变换**（线性变换+平移变换）

{% endnote %}

## 变换矩阵
### 基础变换矩阵的构成规则
$$
\begin{bmatrix}
M_{11} & M_{12} & M_{13} & t_1 \\
M_{21} & M_{22} & M_{23} & t_2 \\
M_{31} & M_{32} & M_{33} & t_3 \\
0      & 0      & 0      & 1
\end{bmatrix}

\Rightarrow \begin{bmatrix} M^{3 \times 3} & t^{3 \times 1} \\ 0^{1 \times 3} & 1 \end{bmatrix}
$$

+ 矩阵的$M^{3 \times 3}$部分用于**表示旋转和缩放变换**
+ 矩阵的$t^{3\times1}$部分用于**表示平移**
+ 矩阵的$0^{1\times3}$部分始终为**零矩阵**
+ 矩阵的右下角元素**始终为1**

### 平移矩阵
$$
\begin{bmatrix}
M^{3 \times 3} & t^{3 \times 1} \\
0^{1 \times 3} & 1
\end{bmatrix}
\Rightarrow
\begin{bmatrix}
1 & 0 & 0 & t_x \\
0 & 1 & 0 & t_y \\
0 & 0 & 1 & t_z \\
0 & 0 & 0 & 1
\end{bmatrix}
$$

$$
\text{逆矩阵} = 
{
\begin{bmatrix}
1 & 0 & 0 & -t_x \\
0 & 1 & 0 & -t_y \\
0 & 0 & 1 & -t_z \\
0 & 0 & 0 & 1
\end{bmatrix}}
$$

#### 向量平移
+ 使用向量的齐次坐标进行计算，**w为0，代表是一个向量**

$$
\begin{bmatrix}
1 & 0 & 0 & t_x \\
0 & 1 & 0 & t_y \\
0 & 0 & 1 & t_z \\
0 & 0 & 0 & 1
\end{bmatrix}
\begin{bmatrix}
x \\ y \\ z \\ 0
\end{bmatrix}
=
\begin{bmatrix}
x \\ y \\ z \\ 0
\end{bmatrix}
$$

从该计算可以发现，向量的平移结果是不会有任何变化的。原因是因为向量其实没有位置属性，向量是由方向和大小组合的几何对象，不管它在空间当中如何移动，它代表的方向和大小都是不会变化的，相当于在任意位置都是彼此平行的，长度不变的。因此，对向量进行平移变换，不会改变向量。

#### 点平移
+ 使用向量的齐次坐标进行计算，**w为1，代表是一个点**

$$
\begin{bmatrix}
1 & 0 & 0 & t_x \\
0 & 1 & 0 & t_y \\
0 & 0 & 1 & t_z \\
0 & 0 & 0 & 1
\end{bmatrix}
\begin{bmatrix}
x \\ y \\ z \\ 1
\end{bmatrix}
=
\begin{bmatrix}
x + t_x \\ y + t_y \\ z + t_z \\ 1
\end{bmatrix}
$$

从该计算便可以看出为什么3x3的矩阵无法表示平移，而需要使用齐次坐标4x4的矩阵：点的x，y，z分量分别增加了一个位置偏移，在几何图像中的效果就是，将点$(x,y,z)$在3D空间中平移了了$(t_x,t_y,t_z)$个单位。

### 旋转矩阵
+ 绕х轴旋转β度

$$
\begin{bmatrix}
1 & 0 & 0 & 0 \\
0 & \cos\beta & -\sin\beta & 0 \\
0 & \sin\beta & \cos\beta & 0 \\
0 & 0 & 0 & 1
\end{bmatrix}
$$

+ 绕у轴旋转β度

$$
\begin{bmatrix}
\cos\beta & 0 & \sin\beta & 0 \\
0 & 1 & 0 & 0 \\
-\sin\beta & 0 & \cos\beta & 0 \\
0 & 0 & 0 & 1
\end{bmatrix}
$$

+ 绕z轴旋转ß度

$$
\begin{bmatrix}
\cos\beta & -\sin\beta & 0 & 0 \\
\sin\beta & \cos\beta & 0 & 0 \\
0 & 0 & 1 & 0 \\
0 & 0 & 0 & 1
\end{bmatrix}
$$

{% note info %}
旋转矩阵是正交矩阵，**因此x、y、z轴的旋转矩阵的逆矩阵是它们的转置矩阵**，我们可以利用旋转矩阵的逆矩阵来进行还原旋转：

假设P点绕某个轴的旋转矩阵R进行了旋转变换，得到了P’，如果我们想将P’还原为P，则只需要用R的转置矩阵乘以P’即可得到结果P

{% endnote %}

### 缩放矩阵
$$
\begin{bmatrix}
k_x & 0 & 0 & 0 \\
0 & k_y & 0 & 0 \\
0 & 0 & k_z & 0 \\
0 & 0 & 0 & 1
\end{bmatrix}
$$

$$
\text{逆矩阵}=
\begin{bmatrix}
\frac{1}{k_x} & 0 & 0 & 0 \\
0 & \frac{1}{k_y} & 0 & 0 \\
0 & 0 & \frac{1}{k_z} & 0 \\
0 & 0 & 0 & 1
\end{bmatrix}
$$

{% note info %}
注意：$k_x=k_y=k_z$时，称为**统一缩放**，否则称为**非统一缩放**。

{% endnote %}

+ **对点的缩放**（一般是构成模型的顶点），相当于就是在缩放模型大小。
+ **对向量的缩放**，统一缩放时只会改变向量的大小（模长），不会改变向量的方向；**非统一缩放时不仅会改变大小，可能还会改变向量的方向**

### 复合运算
约定**先缩放、再旋转、最后平移**。

{% note info %}
主要原因是**缩放和旋转两步显然会影响平移的大小和方向**；而**旋转又会影响非均匀缩放**的结果（缩放轴会被旋转改变）。

{% endnote %}

## 坐标空间
### 什么是坐标空间
坐标空间是一个用于**描述和定位物体位置**的数学概念。它一般由一个基础参照物（原点）和轴线（相互垂直的轴线）组成。常见的坐标空间包括二维平面坐标空间和三维空间。在三维空间中，通常决定一个原点（0,0,0）并使用三个坐标轴（通常是x轴、y轴和z轴）来描述点的位置。

### 坐标空间的组成
+ 坐标原点位置
+ 3个坐标轴的方向（三维坐标系中）

### 为什么需要不同的坐标空间
+ 世界坐标系
+ 物体坐标系
+ 屏幕坐标系
+ ...

**不同的问题需要不同的坐标系来描述和解决特定的空间问题，帮助我们更方便的完成需求**

### 坐标空间之间的关系
在Unity中，世界坐标空间相当于我们的基础坐标空间，Unity中其他的大部分坐标空间，都是世界坐标空间的子坐标空间。这些子坐标空间的原点和轴向的相关表示数据，都是基于世界坐标空间的。因此，在Unity中坐标空间之间会形成一种层级结构，大部分坐标空间都是另一个坐标空间的子空间。所以，**Unity中的坐标空间的变换实际上就是父空间和子空间之间对点或向量进行变换。**

### 坐标空间的变换
在Shader开发中为了方便我们制作模型、使用模型、渲染模型，也存在很多不同的坐标空间，比如**模型空间、世界空间、观察空间、裁剪空间、屏幕空间**。我们这里的坐标空间的变换主要是指在渲染管线中，将坐标数据在这几种空间当中进行变换计算（利用矩阵相关知识）。

+ 举例：

在设计模型时，使用的是模型空间（所有的顶点、法线等等相关数据都是基于模型空间坐标系的）当我们将模型导入到Unity后，最终能够被我们在屏幕上看到，这里面的就经历了我们看不到的坐标空间变换：

$模型空间\Rightarrow世界空间\Rightarrow观察空间\Rightarrow裁剪空间\Rightarrow屏幕空间$

#### 父子变换
那么我们现在假设一个父坐标空间为$F$，子坐标空间为$S$。

我们已知$S$坐标空间的原点位置和3个单位坐标轴（基于$F$坐标空间的数据表达）

对于坐标空间转换我们一般会有以下两种需求：

1. 把子坐标空间$S$下的点或向量$A_s$转换到父坐标空间$F$中为$A_f$
2. 把父坐标空间$F$下的点或向量$B_f$转换到子坐标空间$S$中为$B_s$

如果用矩阵来表示的话：

$$
\begin{aligned}
A_f &= M_{s \to f} A_s \\
B_s &= M_{f \to s} B_f
\end{aligned}
$$

+ $M_{s \to f}$代表从子坐标空间到父坐标空间的变换矩阵
+ $M_{f \to s}$是$M_{s \to f}$的**逆矩阵**，代表父到子的变换矩阵

{% note info %}
也就是说我们只要知道$M_{s \to f}$和$M_{f \to s}$的其中一个矩阵，另一个矩阵都可以通过求逆矩阵得到对应的结果

{% endnote %}

#### 子空间到父空间的变换矩阵
即将子空间中用子空间坐标系表示的点/向量用父空间坐标系来表示。

{% note info %}
推导$M_{s-f}$，也就是子坐标空间到父坐标空间的变换矩阵

**已知：**  
子坐标空间$S$的原点为 $O_s$（基于$F$父坐标空间的数据表示）  
子坐标空间$S$的$x、y、z$轴的方向向量$X_s、Y_s、Z_s$（基于$F$父坐标空间的数据表示）

**目的：**  
把子坐标空间下的点$P(a,b,c)$变换到父坐标空间$F$中

**利用向量和点相关知识可以通过以下做法，达到目的：**

$P_f = O_s + a X_s + b Y_s + c Z_s$



{% endnote %}

$$
\begin{aligned}
{\color{red} P_f} &= {\color{green} O_s + a X_s + b Y_s + c Z_s} \\
&= {\color{green} (X_{O_s}, Y_{O_s}, Z_{O_s}) + a(X_{X_s}, Y_{X_s}, Z_{X_s}) + b(X_{Y_s}, Y_{Y_s}, Z_{Y_s}) + c(X_{Z_s}, Y_{Z_s}, Z_{Z_s})} \\
&= {\color{green} (X_{O_s}, Y_{O_s}, Z_{O_s}) + (a X_{X_s}, a Y_{X_s}, a Z_{X_s}) + (b X_{Y_s}, b Y_{Y_s}, b Z_{Y_s}) + (c X_{Z_s}, c Y_{Z_s}, c Z_{Z_s})} \\
&= {\color{green} (X_{O_s}, Y_{O_s}, Z_{O_s}) + (a X_{X_s} + b X_{Y_s} + c X_{Z_s}, a Y_{X_s} + b Y_{Y_s} + c Y_{Z_s}, a Z_{X_s} + b Z_{Y_s} + c Z_{Z_s})} \\
&= {\color{green} (X_{O_s}, Y_{O_s}, Z_{O_s}) + \begin{pmatrix} X_{X_s} & X_{Y_s} & X_{Z_s} \\ Y_{X_s} & Y_{Y_s} & Y_{Z_s} \\ Z_{X_s} & Z_{Y_s} & Z_{Z_s} \end{pmatrix} \begin{pmatrix} a \\ b \\ c \end{pmatrix}} \\
&= {\color{green} (X_{O_s}, Y_{O_s}, Z_{O_s}) + \begin{pmatrix} | & | & | \\ X_s & Y_s & Z_s \\ | & | & | \end{pmatrix} \begin{pmatrix} a \\ b \\ c \end{pmatrix}} \\
&= {\color{green} (X_{O_s}, Y_{O_s}, Z_{O_s}, 1) + \begin{pmatrix} | & | & | & 0 \\ X_s & Y_s & Z_s & 0 \\ | & | & | & 0 \\ 0 & 0 & 0 & 1 \end{pmatrix} \begin{pmatrix} a \\ b \\ c \\ 1 \end{pmatrix}} \\
&= {\color{green} \begin{pmatrix} 1 & 0 & 0 & X_{O_s} \\ 0 & 1 & 0 & Y_{O_s} \\ 0 & 0 & 1 & Z_{O_s} \\ 0 & 0 & 0 & 1 \end{pmatrix} \begin{pmatrix} | & | & | & 0 \\ X_s & Y_s & Z_s & 0 \\ | & | & | & 0 \\ 0 & 0 & 0 & 1 \end{pmatrix} \begin{pmatrix} a \\ b \\ c \\ 1 \end{pmatrix}} \\
&= {\color{green} \begin{pmatrix} | & | & | & X_{O_s} \\ X_s & Y_s & Z_s & Y_{O_s} \\ | & | & | & Z_{O_s} \\ 0 & 0 & 0 & 1 \end{pmatrix} \begin{pmatrix} a \\ b \\ c \\ 1 \end{pmatrix}} \\
&= {\color{green} \begin{pmatrix} | & | & | & | \\ X_s & Y_s & Z_s & O_s \\ | & | & | & | \\ 0 & 0 & 0 & 1 \end{pmatrix} \begin{pmatrix} a \\ b \\ c \\ 1 \end{pmatrix}}
\end{aligned}
$$

+ 该变换矩阵它的**前三列**分别是子坐标空间**相对父坐标空间**的x、y、z轴的**方向向量**
+ **第四列**是子坐标空间相对父坐标空间的**原点**

{% note info %}
如果子空间存在缩放，只需要用x、y、z轴向的**单位向量＊对应轴的缩放因子**即可

例如子空间被放大了两倍，则缩放因子为2（轴变长了2倍，相当于坐标缩小两倍）

{% endnote %}

![画板](https://cdn.nlark.com/yuque/0/2026/jpeg/63937386/1770801069683-fb6d1b42-fa78-4c98-9653-e93f2ee06608.jpeg)

{% note warning %}
注意，左乘（矩阵 × **列向量**）= 右乘（**行向量** × 转置矩阵）

{% endnote %}

### 模型空间
**模型空间**(model space)也被成为**对象空间**(object space)或**局部空间**(local space)，它一般指3D模型的局部坐标系，每个模型都有自己独立的坐标空间。模型空间的主要意义是方便我们建模，模型的顶点等数据都是基于模型空间表达的。

{% note info %}
注意：

在Unity中当模型移动或旋转时，模型空间坐标系也会随着变换，因为此时的**模型坐标空间是世界坐标空间的子空间**

{% endnote %}

#### 模型空间变换
模型空间变换指的主要是**将模型空间中的点或向量通过矩阵乘法计算，变换为相对于世界坐标空间下数据。**

$相对世界坐标系的位置 = 平移矩阵\times旋转矩阵\times缩放矩阵\times模型空间坐标的列矩阵$

+ 其中平移、旋转、缩放矩阵中的具体变换值都是**相对于世界空间下的数据**

{% note info %}
原理：

认为一开始模型坐标空间和世界坐标空间重合，模型发生缩放、旋转、平移变换时，模型空间下的点和向量也应该发生相同的变换。

{% endnote %}

### 观察空间
观察空间（viewspace）也被称为摄像机空间（camera space)。观察空间的主要意义是摄像机决定了渲染的视角和视野。

{% note info %}
在模型空间的x、y、z轴，对应的是模型的右、上、前三个方向，这是因为Unity中的**模型空间遵循左手坐标系原则**。但是Unity中的**观察空间遵循右手坐标系原则**，因此它的坐标轴方向有所不同。

+ **观察空间中的x、y、z轴的正方向分别对应摄像机的右、上、后方，以此来匹配OpenGL（即Z轴方向相反，朝向后方）。**

{% endnote %}

#### 观察空间变换概念
观察空间变换指的主要是将模型空间中的点或向量从世界空间中变换到观察空间中。它是顶点变换的第二步，即将数据从世界空间变换到观察空间。

+ 观察空间变换也可以称为观察变换（view transform）

#### 如何进行观察空间变换
将顶点在世界空间下的坐标变换到观察空间下有以下两种方式：

1. **坐标空间变换规则：**$M_{f \to s}$矩阵（显然观察空间（摄像机）是世界空间的子空间，因此是**父到子空间**）
2. **逆向变换观察空间：**让观察空间和世界坐标空间重合**（重合时观察空间下的点或向量的数据表达和世界空间下的数据表达是相同的）**

##### 坐标空间变换规则
1. 通过Unity.Tramsform获取观察空间（摄像机）的轴向和原始位置（相对世界坐标系，因此要注意**Z轴的方向需要进行反向处理**）；
2. 得到子到父的变换矩阵，并对其**求解逆矩阵**，得到父到子的变换矩阵；
3. 利用父到子的变换矩阵$M_{f \to s}$和目标点进行矩阵运算。

##### **逆向变换观察空间**
1. 通过Unity.Transform获取摄像机的世界空间坐标、旋转、缩放信息；
2. 根据这些信息**计算摄像机逆向变换（先平移、再旋转、最后缩放）的矩阵**，使其能够与世界坐标系原点重合（即**重置变换**）
3. 由于观察空间和世界坐标系Z轴方向相反，因此我们需要对Z轴取反（即乘以$\begin{bmatrix} 1 & 0 & 0 & 0 \\ 0 & 1 & 0 & 0 \\ 0 & 0 & -1 & 0 \\ 0 & 0 & 0 & 1 \end{bmatrix}$），此时观察空间和世界坐标系完全重合（相同） 
4. 用该变换矩阵和点进行乘法运算得到最终结果。（将世界坐标系乘以该矩阵，相当于对世界空间中的所有点做了摄像机的反变换，相当于摄像机不动，而世界空间发生了“逆变换”，以此来达到“看上去”摄像机发生了正变换一样，好比行驶中的汽车中能看到窗外的风景好像在向后倒退，如果汽车原地不动，我们控制风景向后倒退，则会产生同样的效果。）

### 齐次裁剪空间
#### 视椎体
摄像机的视锥体是在三维空间中表示摄像机可见区域的虚拟体积，它类似一个六面体的形状，根据摄像机的属性和投影方式而定。**视锥体定义了摄像机在场景中能够看到的物体区域，超出这个区域的物体将在渲染时被裁减掉，从而提高渲染性能。**

视锥体主要包含几种重要部分：**远近裁剪平面和左、右、上、下裁剪平面**

+ **透视投影**中，视锥体类似一个金字塔形状，远裁剪面比近裁剪面大，所以产生透视效果
+ **正交投影**中，视锥体类似于长方体的形状，远近裁剪平面大小一致，不会产生透视效果

{% note info %}
如果直接使用视锥体定义的空间来进行裁剪，那不同的视锥体就需要不同的处理过程，而且对于透视投影的视锥体来说，判断顶点是否在范围内相对较麻烦。因此，我们希望用更通用、便捷的方式来进行裁剪工作，就需要将观察空间（摄像机空间）中的数据转换到**齐次裁剪空间**中。

{% endnote %}

#### 齐次裁剪空间的定义
齐次裁剪空间是一个三维空间，是在计算机图形学中用于在图形渲染过程中进行裁剪和投影的。它的坐标范围为（1，-1，-1）到（1，1，1），超出这个范围的坐标在渲染时会被裁减掉，只会保留范围内的坐标。

#### 裁剪空间变换——正交投影变换
##### 正交投影变换参数
Projection：该参数为Orthographic时，为正交摄像机

Size：视锥体竖直方向上高度的一半

Clipping Planes：裁剪平面

Near：近裁剪面离摄像机的距离

Far：远裁剪面离摄像机的距离

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/63937386/1770884830642-aa401ede-9374-4e4f-90b1-6f9e01ffedd0.png)

由于$Size$**表示视锥体竖直方向上高度的一半**，因此：

$\color{red}{\text{近裁剪面高} = \text{远裁剪面高} = 2 \times \text{Size}}$

令Aspect表示游戏窗口的宽高比（例如16:9，16:10等），可以得到：

$$
\begin{aligned}
& \text{Aspect} = \text{宽} : \text{高} = \text{宽} / \text{高} \\
& {\color{red} \text{近裁剪面宽} = \text{远裁剪面宽} = \text{Aspect} \times 2 \times \text{Size}}
\end{aligned}
$$

##### 正交投影变换矩阵
1. <u><font style="color:#DF2A3F;">将</font></u><u><font style="color:#DF2A3F;"><b>视锥体中心</b></font></u><u><font style="color:#DF2A3F;">位移到</font></u><u><font style="color:#DF2A3F;"><b>观察空间原点中心</b></font></u>

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/63937386/1770886893908-d3bacd57-f075-4813-8f47-4c7bf138a624.png)

我们已知远近裁剪面离摄像机的距离为 $Near$ 和 $Far$ 而观察空间中$z$方向是摄像机后方 因此可知视锥体中心点的$z$坐标为 $\frac{(-Near) + (-Far)}{2}$ 知道了视锥体中心点的$z$坐标，那么我们只需要将视锥体平移 $-\frac{(-Near) + (-Far)}{2}$ 个单位即可 所以，该平移矩阵为： 

$\begin{bmatrix} 1 & 0 & 0 & 0 \\ 0 & 1 & 0 & 0 \\ 0 & 0 & 1 & -\frac{(-Near) + (-Far)}{2} \\ 0 & 0 & 0 & 1 \end{bmatrix} = \begin{bmatrix} 1 & 0 & 0 & 0 \\ 0 & 1 & 0 & 0 \\ 0 & 0 & 1 & \frac{Far + Near}{2} \\ 0 & 0 & 0 & 1 \end{bmatrix}$



2. <u><font style="color:#DF2A3F;">将长方体视锥体的xyz坐标范围</font></u><u><font style="color:#DF2A3F;"><b>映射到（-1，1）长宽高为2的正方体</b></font></u><u><font style="color:#DF2A3F;">中</font></u>

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/63937386/1770963187796-65488108-0948-4615-b41e-44770c5337e7.png)

这一步的变换其实就是一个缩放变换，因此我们可以得到这一步的缩放变换矩阵为：

$$
\begin{bmatrix}
\frac{1}{\text{Aspect} * \text{Size}} & 0 & 0 & 0 \\
0 & \frac{1}{\text{Size}} & 0 & 0 \\
0 & 0 & -\frac{2}{\text{Far} - \text{Near}} & 0 \\
0 & 0 & 0 & 1
\end{bmatrix}
$$

{% note info %}
我们现在得到了两步的对应**平移矩阵**和**缩放矩阵**，我们将其进行**乘法计算**后，便可以得到将摄像机视锥体的正交投影空间转换到齐次坐标裁剪空间时的**变换矩阵：**

$$
\begin{aligned}
&\begin{bmatrix}
\frac{1}{\text{Aspect} * \text{Size}} & 0 & 0 & 0 \\
0 & \frac{1}{\text{Size}} & 0 & 0 \\
0 & 0 & -\frac{2}{\text{Far} - \text{Near}} & 0 \\
0 & 0 & 0 & 1
\end{bmatrix}
*
\begin{bmatrix}
1 & 0 & 0 & 0 \\
0 & 1 & 0 & 0 \\
0 & 0 & 1 & \frac{\text{Far} + \text{Near}}{2} \\
0 & 0 & 0 & 1
\end{bmatrix} \\
&=
\begin{bmatrix}
\frac{1}{\text{Aspect} * \text{Size}} & 0 & 0 & 0 \\
0 & \frac{1}{\text{Size}} & 0 & 0 \\
0 & 0 & -\frac{2}{\text{Far} - \text{Near}} & -\frac{\text{Far} + \text{Near}}{\text{Far} - \text{Near}} \\
0 & 0 & 0 & 1
\end{bmatrix}
\end{aligned}
$$

{% endnote %}

#### 裁剪空间变换——透视投影变换
##### 透视投影变换参数
Projection：该参数为Perspective时，为透视摄像机

FOV（FieldofView）：决定视锥开口角度

Clipping Planes：裁剪平面

Near：近裁剪面离摄像机的距离

Far：远裁剪面离摄像机的距离

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/63937386/1770964600300-054f3a9c-1a53-4678-802e-c646558f5c48.png)

$$
\begin{aligned}
\text{近裁剪面高} &= 2 * Near * \tan\left(\frac{FOV}{2}\right) \\
\text{远裁剪面高} &= 2 * Far * \tan\left(\frac{FOV}{2}\right)
\end{aligned}
$$

$$
\begin{aligned}
\text{近裁剪面宽} &= \text{Aspect} * \text{近裁剪面高} = \text{Aspect} * 2 * \text{Near} * \tan\left(\frac{FOV}{2}\right) \\
\text{远裁剪面宽} &= \text{Aspect} * \text{远裁剪面高} = \text{Aspect} * 2 * \text{Far} * \tan\left(\frac{FOV}{2}\right)
\end{aligned}
$$

##### 透视投影变换矩阵
1. <u><font style="color:#DF2A3F;">将透视视锥体变成一个</font></u><u><font style="color:#DF2A3F;"><b>长方体，同时满足以下三个特性：</b></font></u>
+ **近裁剪面**上的所有点保持不变

{% note info %}
近裁剪面上的点 $(x, y, Near, 1)$ 变换后还是 $(x, y, Near, 1)$

$$
\text{变换矩阵 } M \times \begin{bmatrix} x \\ y \\ -Near \\ 1 \end{bmatrix} = \begin{bmatrix} x \\ y \\ -Near \\ 1 \end{bmatrix} \tag{1}
$$

其中，$x$和$y$等于$0$时，相当于就是近裁剪面的中心点，也满足下面的等式：

$$
\text{变换矩阵 } M \times \begin{bmatrix} 0 \\ 0 \\ -Near \\ 1 \end{bmatrix} = \begin{bmatrix} 0 \\ 0 \\ -Near \\ 1 \end{bmatrix}\tag{2}
$$

{% endnote %}

+ 远裁剪面的**z值不变**，远裁剪面的**中心点不变**

{% note info %}
相当于$z$轴与远裁剪面的交点$(0, 0, Far, 1)$变换后仍为$(0, 0, Far, 1)$。

$$
\text{变换矩阵 } M \times \begin{bmatrix} 0 \\ 0 \\ -Far \\ 1 \end{bmatrix} = \begin{bmatrix} 0 \\ 0 \\ -Far \\ 1 \end{bmatrix} \tag{3}
$$

{% endnote %}

+ **远裁剪面宽高映射成近裁剪面的宽高**

{% note info %}
<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/63937386/1770968662261-738f8dad-45e9-46c2-a66e-3ea2028bc228.png)

通过此推导我们发现，视锥体内的所有点的$x$、$y$坐标都经过了同样的缩放，缩放因子为：$\frac{-Near}{z}$

其中$Near$是近裁剪面离摄像机的距离，$z$为视锥体中点的$z$坐标

因此我们已推导出：

$$
\text{变换矩阵 } M \times \begin{Bmatrix} 
x \\[5pt] 
y \\[5pt] 
z \\[5pt] 
1 
\end{Bmatrix} = 
\begin{Bmatrix} 
x \frac{-Near}{z} \\[5pt] 
y \frac{-Near}{z} \\[5pt] 
\text{未知} \\[5pt] 
1 
\end{Bmatrix} \tag{4}
$$

{% endnote %}

由于四维齐次坐标中乘以或者除以一个非零的数（标量），所映射的三维坐标始终是同一个坐标，因此：

$$
\begin{gather*}
\begin{bmatrix} x \frac{-Near}{z} \\[5pt] y \frac{-Near}{z} \\[5pt] \text{未知} \\[5pt] 1 \end{bmatrix} 
\Rightarrow 
\begin{bmatrix} x \frac{-Near}{z} \\[5pt] y \frac{-Near}{z} \\[5pt] \text{未知} \\[5pt] 1 \end{bmatrix} \times (-z)
\Rightarrow 
\begin{bmatrix} xNear \\[5pt] yNear \\[5pt] \text{未知} \\[5pt] -z \end{bmatrix} \\[25pt]
\text{变换矩阵 } M \times \begin{bmatrix} x \\[5pt] y \\[5pt] z \\[5pt] 1 \end{bmatrix} = \begin{bmatrix} xNear \\[5pt] yNear \\[5pt] \text{未知} \\[5pt] -z \end{bmatrix} 
\Rightarrow \text{变换矩阵 } M = \begin{bmatrix} Near & 0 & 0 & 0 \\[5pt] 0 & Near & 0 & 0 \\[5pt] ? & ? & ? & ? \\[5pt] 0 & 0 & -1 & 0 \end{bmatrix}
\end{gather*}
$$

由于**第三行的前两个元素不应当影响到坐标**$x$**和**$y$，因此可以假设为0，得到以下矩阵：

$$
\color{red}\text{变换矩阵 } M = 
\begin{bmatrix}
Near & 0 & 0 & 0 \\[5pt]
0 & Near & 0 & 0 \\[5pt]
0 & 0 & a & b \\[5pt]
0 & 0 & -1 & 0
\end{bmatrix}
$$

将该矩阵代入$(2)$式中，可以得到$-a Near + b = -{Near}^2$；

将该矩阵代入$(3)$式中，可以得到$-a Far + b = -{Far}^2$。

求解该二元一次方程组，可以得到：$\begin{cases} a = Far + Near \\ b = Far \times Near \end{cases}$，由此可得到变换矩阵$M$：

$$
\text{变换矩阵 } M = 
\begin{bmatrix}
Near & 0 & 0 & 0 \\[5pt]
0 & Near & 0 & 0 \\[5pt]
0 & 0 & Far + Near & Far \cdot Near \\[5pt]
0 & 0 & -1 & 0
\end{bmatrix}
$$



2. <u><font style="color:#DF2A3F;">将视锥体中心位移到观察空间原点中心</font></u>

$$
\text{平移矩阵} =

\begin{bmatrix}
1 & 0 & 0 & 0 \\[5pt]
0 & 1 & 0 & 0 \\[5pt]
0 & 0 & 1 & \frac{Far + Near}{2} \\[5pt]
0 & 0 & 0 & 1
\end{bmatrix}
$$

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/63937386/1770983863274-02b4ed16-7f65-4d25-aaed-1d3f790a6111.png)



3. <u><font style="color:#DF2A3F;">将长方体视锥体的xyz坐标范围映射到（-1，1）长宽高为2的正方体中</font></u>

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/63937386/1770984297873-60f10359-1c5d-4c71-9994-4fe070762326.png)

由上式得**缩放矩阵**为：$\color{red}\begin{bmatrix} \frac{1}{\text{Aspect} \times \text{Near} \times \tan\left(\frac{FOV}{2}\right)} & 0 & 0 & 0 \\[5pt] 0 & \frac{1}{\text{Near} \times \tan\left(\frac{FOV}{2}\right)} & 0 & 0 \\[5pt] 0 & 0 & -\frac{2}{Far - Near} & 0 \\[5pt] 0 & 0 & 0 & 1 \end{bmatrix}$

{% note info %}
将前三个矩阵作矩阵乘法运算，得到**透视投影变换矩阵**为：

$\begin{bmatrix} \frac{1}{\text{Aspect} \times \tan\left(\frac{FOV}{2}\right)} & 0 & 0 & 0 \\[5pt] 0 & \frac{1}{\tan\left(\frac{FOV}{2}\right)} & 0 & 0 \\[5pt] 0 & 0 & -\frac{Far + Near}{Far - Near} & -\frac{2 \cdot Far \cdot Near}{Far - Near} \\[5pt] 0 & 0 & -1 & 0 \end{bmatrix}$

{% endnote %}

#### 如何决定顶点是否被裁剪
+ **正交摄像机：**$\begin{cases} -1 \le x \le 1 \\ -1 \le y \le 1 \\ -1 \le z \le 1 \end{cases}$
+ **透视摄像机：**$\begin{cases} -w \le x \le w \\ -w \le y \le w \\ -w \le z \le w \end{cases}$

### MVP矩阵
MVP矩阵指的是用于从模型空间变换到裁剪空间的矩阵，即$Model ~View ~Projection$的缩写，对应Unity中的`UNITY_MATRIX_MVP`矩阵或`UnityObjectToClipPos()`函数。

### NDC空间
<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/63937386/1770995006338-fba565ce-9383-40ae-b130-fdd0023fa7d5.png)

### 屏幕空间
屏幕空间的主要意义是屏幕空间中对应的位置信息是真正的像素位置，而不是虚拟的三维坐标。有了相对屏幕空间的坐标位置，才能准确的控制屏幕上像素点的显示效果。

#### 屏幕空间变换
将三维坐标$(x,y,z)$中的x，y分量映射到屏幕上，而z分量一般会被用于**深度缓冲**，之后用于深度测试等（决定是否被遮挡等）

1. <u><font style="color:#DF2A3F;"><b>透视除法</b></font></u>

假设裁剪空间中的点为$(X_{\text{clip}}, Y_{\text{clip}}, Z_{\text{clip}}, W_{\text{clip}})$，进行透视除法：

$$
\begin{gather*}

\left( \frac{X_{\text{clip}}}{W_{\text{clip}}}, \frac{Y_{\text{clip}}}{W_{\text{clip}}}, \frac{Z_{\text{clip}}}{W_{\text{clip}}}, \frac{W_{\text{clip}}}{W_{\text{clip}}} \right)
\end{gather*}
$$

+ 对于**正交投影**来说$W$为1，所以除以1后，$xyz$也不会改变
+ 对于**透视投影**来说$W$为任意值，所以除以$W$后，$xyz$的范围将在-1到1之间，$W$为1



2. <u><font style="color:#DF2A3F;"><b>找到齐次裁剪空间和屏幕空间的映射关系</b></font></u>

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/63937386/1770995420397-37aa4716-9a75-4667-9488-430a722089f6.png)









$$
\begin{aligned}
X_{\text{屏}} &= \frac{\text{Width}}{2} \times X_{\text{齐}} + \frac{\text{Width}}{2} \\[10pt]
Y_{\text{屏}} &= \frac{\text{Height}}{2} \times Y_{\text{齐}} + \frac{\text{Height}}{2}
\end{aligned}
$$

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/63937386/1770995481123-f40f2125-6675-4984-91c4-26aca1f9ce75.png)<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/63937386/1770995494913-a8bb36a2-f533-41be-be6b-a55ffe7e143e.png)

{% note info %}
将第一步中的透视除法结果带入上式，即可得到**屏幕空间变换**的公式：

$$
\begin{gather*}
\begin{aligned}
{\color{red} X_{\text{屏}} =} & \ \frac{\text{Width}}{2} \times X_{\text{齐}} + \frac{\text{Width}}{2} = \frac{\text{Width}}{2} \times \frac{Xclip}{Wclip} + \frac{\text{Width}}{2} \\[10pt]
& {\color{red} = \frac{\text{Width} \times Xclip}{2 \times Wclip} + \frac{\text{Width}}{2}}
\end{aligned} \\[30pt]
\begin{aligned}
{\color{red} Y_{\text{屏}} =} & \ \frac{\text{Height}}{2} \times Y_{\text{齐}} + \frac{\text{Height}}{2} = \frac{\text{Height}}{2} \times \frac{Yclip}{Wclip} + \frac{\text{Height}}{2} \\[10pt]
& {\color{red} = \frac{\text{Height} \times Yclip}{2 \times Wclip} + \frac{\text{Height}}{2}}
\end{aligned}
\end{gather*}
$$

+ $Z_{clip}$会被存入深度缓冲中（不同硬件商存储方式可能不同），之后用于深度测试等计算；
+ $W_{clip}$也会被保留下来，用于之后进行一些计算才做，比如透视校正差值

{% endnote %}

# ShaderLab
## ShaderLab的基本结构
```plain
Shader "路径/着色器名称"
{
  Properties
  {
    //材质面板属性
  }

  SubShader
  {
    //顶点 片元...着色器
  }

  SubShader
  {
    //上述着色器的更加精简的版本
    //如果上一个着色器运行失败，就依次向下运行，寻找可用的子着色器
  }

  //...可以有n个子着色器代码块
  
  Fallback "备用的Shader"	//可以省略
}
```

## ShaderLab的属性
### 属性的基本语法
```c
_Name("Display Name", type) = defaultValue[{options}]
```

+ Name：属性名字，规则是需要在前面加一个下划线，方便在之后获取
+ DisplayName：材质面板上显示的名字
+ type：属性的类型
+ defaultValue：将shader指定给材质的时候初始化的默认值

### 数值类型
1. 整型 `Int`
2. 浮点型`Float`
3. 范围浮点型 `Range(min, max)`

{% note info %}
注意：UnityShader中的数值类型属性基本都是浮点型（`Float`）数据，虽然提供了整数（`Int`），但是**编译时最终都会转换为浮点型**，因此我们更多的使用的还是`Float`类型

{% endnote %}

4. 颜色 `Color` (R, G, B, A) 其中RGBA均为0~1
5. 向量 `Vector` (x, y, z, w) 其中xyzw取值没有限制

### 纹理类型
```c
_Name("Display Name", type) = "defaulttexture"{}
```

1. 2D纹理：`2D`。最常用的纹理，漫反射贴图，法线贴图均属于2D纹理；
2. 2DArray纹理：`2DArray`。纹理数组，允许在纹理中存储多层图像数据，每层看做一个2D图像，一般使用脚本创建，较少使用；
3. Cube map texture纹理：`Cube`。立方体纹理，由前后左右上下6张有联系的2D贴图拼成的立方体，比如天空盒和反射探针；
4. 3D纹理：`3D`。一般使用脚本创建，极少使用。

{% note info %}
纹理类型的默认值：

+ 不写：默认贴图为空
+ white：默认白色贴图（RGBA: 1, 1, 1, 1）
+ black：默认黑色贴图（RGBA: 0, 0, 0, 1）
+ gray：默认灰色贴图（RGBA: 0.5, 0.5, 0.5, 1）
+ bump：默认凸贴图（RGBA: 0.5, 0.5, 1, 1），一般用于法线贴图默认贴图
+ red：默认红色贴图（RGBA: 1, 0, 0, 1）

关于默认值后面的`{}`，固定写法，老版本中括号内可的生成，但是新版本中没有该功能了

{% endnote %}

## SubShader 子着色器
### SubShader的基本结构
```c
SubShader
{
    //渲染标签
    Tags{ "标签名1" = "标签值1" "标签名2" = "标签值2" ...}

    //渲染状态

    //渲染通道
    Pass
    {
        //第一个渲染通道
    }

    Pass
    {
        //第二个渲染通道
    }

    ...
}
```

{% note info %}
注意：在Subshader中每定义一个渲染通道Pass，就会让物体执行一次渲染。n个Pass，就会有n次渲染，在实现一些**复杂渲染效果时需要使用多个Pass进行组合实现**，但是我们要尽量减少它的数量，**更多的Pass会增加性能消耗**

{% endnote %}

### 渲染状态
以上这些状态不仅可以在SubShader语句块中声明，Pass渲染通道语句块中也可以声明这些渲染状态。

+ 在SubShader语句块中使用会影响之后的所有渲染通道Pass
+ 在Pass语句块中使用只会影响当前Pass渲染通道，不会影响其他的Pass

#### 剔除
`Cull Back` 背面剔除

`Cull Front` 正面剔除

`Cull Off` 不剔除，即双面渲染

#### 深度测试
<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/63937386/1771055103536-1c7d57b2-a67f-4e73-ad38-0591c153073a.png)

+ **深度测试：** 在渲染场景之前，深度缓冲会被初始化为最大深度值。如果当前片元的深度值大于等于当前深度缓冲区的值，就舍弃该片元（判断条件可以手动配置）

`ZTest Less`：小于当前深度缓冲中的值，就通过测试，写入到深度缓冲中

`ZTest Greater`：大于当前深度缓冲中的值

`ZTest LEqual`：**小于等于** 当前深度缓冲中的值 **（默认）**

`ZTest GEqual`：大于等于当前深度缓冲中的值

`ZTest Equal`：等于当前深度缓冲中的值

`ZTest NotEqual`：不等于当前深度缓冲中的值

`ZTest Always`：始终通过深度测试写入深度缓冲

+ **深度写入（深度缓冲）：** 如果片元通过了深度测试，且开发者开启了深度写入，则原有的深度值会被当前片元的深度值覆盖。

`ZWrite On` **写入深度缓冲（默认）**

`ZWrite Off` 不写入深度缓冲

{% note danger %}
**透明和半透明的物体一般不写入深度缓冲**，原因在于一旦写入深度缓冲，则透明物体背后的物体将会被剔除；半透明物体同样需要背后的物体进行透明度混合。

由于透明和半透明的渲染顺序排在最后，因此他们同样会因为深度测试而被正常剔除。

{% endnote %}



#### 混合 P16
<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/63937386/1771058983067-0629ab6d-53b9-4200-a6a6-cbc6edd47b81.png)

+ **混合：** 颜色的叠加，开发者可以设定混合的方式。

`Blend One One`：线性减淡

`Blend SrcAlpha OneMinusSrcAlpha`：正常透明混合

`Blend OneMinusDstColor One`：滤色

`Blend DstColor Zero`：正片叠底

`Blend DstColor SrcColor`：X光片效果

`Blend One OneMinusSrcAlpha`：透明度混合

**默认不开启混合**

#### Early-Z
{% note danger %}
从逻辑上来说，模板测试、深度测试和混合应该在片元着色器之后进行，但这会导致大量**性能的浪费**，即GPU已经对所有的片元完成了片元着色器中的渲染操作，但是最后其中的大部分片元都无法通过深度测试。因此GPU会尽可能在片元着色器之前完成这些测试，这种技术也被称为 **Early-Z**。

{% endnote %}

为了最大化利用Early-Z技术，游戏引擎在渲染不透明物体时，会尽可能按照物体包围盒中心的距离，由近及远的顺序来渲染，这样较远的物体片元在进入片元着色器前就会被深度测试剔除。

但是Early-Z并不能解决所有由于深度测试等排在片元着色器之后带来的额外性能消耗问题，为了减少`DrawCall`，游戏引擎会选择合批（`Batching`）渲染物体，既将使用了同一个材质的多个物体同时渲染，以此来减少`DrawCall`；同时物体也可能会相互重叠，这些情况还是需要依赖于深度测试来进行判断，尽管还是有多余的性能消耗，但是相比于不使用Early-Z，它带来的性能优化实际上已经非常可观了。

#### 其他渲染状态
+ `LOD`：设置LOD级别，即在不同距离下使用不同的渲染方式处理；
+ `ColorMask`：设置颜色通道的写入蒙版，默认蒙版为RGBA。

## Pass 渲染通道
### Pass 命名
```c
Pass{
    Name MyPass
}
```

我们对Pass命名的主要目的在于**可以利用`UsePass`命令在其他Shader当中复用该Pass的代码**，只需要在其他shader当中使用`UsePass "Shader路径/Pass名"`即可

```c
UsePass "Shader路径/Shader名/MYPASS"
```

{% note info %}
注意：Unity内部会把Pass名称转换为大写字母，因此在**使用UsePass命令时必须使用大写形式的名字**

{% endnote %}

### 渲染标签
Pass中的渲染标签语法和subShader中相同，但是**SubShader语句块中的渲染标签不能在Pass中使用，Pass有自己独有的渲染标签**

---

+ **LightMode**

指定了该Pass应该在哪个阶段执行，可以将着色器代码分配给适当的渲染阶段，以实现所需的效果

```c
Tags{ "LightMode" = "标签值" }
```

`Always`：始终渲染；不应用光照

`ForwardBase`：在前向渲染中使用；应用环境光、主方向光、顶点/SH光源和光照贴图

`ForwardAdd`：在前向渲染中使用；应用附加的每像素光源（每个光源有一个通道）

`Deferred`：在延迟渲染中使用；渲染G缓冲区

`ShadowCaster`：将对象深度渲染到阴影贴图或深度纹理中

`MotionVectors`：用于计算每对象运动矢量

`PrepassBase`：在旧版延迟光照中使用；渲染法线和镜面反射指数

`PrepassFinal`：在旧版延迟光照中使用；通过组合纹理、光照和反光来渲染最终颜色

`Vertex`：当对象不进行光照贴图时在旧版顶点光照渲染中使用；应用所有顶点光源

`VertexLMRGBM`：当对象不进行光照贴图时在旧版顶点光照渲染中使用；在光照贴图为RGBM编码的平台上（PC和游戏主机）

`VertexLM`：当对象不进行光照贴图时在旧版顶点光照渲染中使用；在光照贴图为双LDR编码的平台上（移动平台）



+ **RequireOptions**

用于指定当满足某些条件时才渲染该Pass。

```c
Tags{ "RequireOptions" = "标签值" }
```

目前Unity仅支持`Tags{ "RequireOptions" = "SoftVegetation" }`：仅当Quality窗口中开启了SoftVegetation时才渲染此通道

+ **PassFlags**

可指示一些标志来更改渲染管线向Pass传递的数据类型与方式。

```c
Tags{ "PassFlags" = "标签值" }
```

目前Unity仅支持`Tags{ "PassFlags" = "OnlyDirectional" }`，在ForwardBase向前渲染的通道类型中使用时，此标志的作用是仅允许主方向光和环境光/光照探针数据传递到着色器，这意味着非重要光源的数据将不会传递到顶点光源或球谐函数着色器变量

### 渲染状态
SubShader中的渲染状态同样适用于Pass。

需要注意的是：如果**在SubShader语句块中使用会影响之后的所有的Pass**；如果**在Pass语句块中使用只会影响当前Pass渲染通道，不会影响其他的Pass**

**<u>Pass中允许使用固定渲染管线着色器的命令。</u>**

### GrabPass 命令
我们可以利用GrabPass命令把即将绘制对象前的屏幕内容抓取到纹理中。

```c
//将绘制该对象之前的屏幕抓取到_BackgroundTexture中
GrabPass{
    "_BackgroundTexture"
}
```

+ 该命令**一般写在某个Pass前**，在之后的Pass代码中可以利用BackgroundTexture变量进行处理

### 多个Pass的执行顺序
需要注意的是，如果有多个 `Pass`，Unity 会按照从上到下的顺序依次执行这些 **Pass**。但是需要注意的是，<font style="color:#DF2A3F;"><b>除非后续的 Pass 开启了混合，否则后续的 Pass 无法拿到前面的 Pass 的渲染结果</b></font>，也就是后续的 `Pass` 无法在前面的 `Pass` 的渲染结果上继续进行计算。所有的 **Pass** 均只能获得 **Properties** 属性中的数值，而没有办法拿到其他 `Pass` 中定义的变量、返回值等。<font style="color:#DF2A3F;"><b>后续执行的 Pass 将会直接覆盖前面的 Pass 的渲染结果。</b></font>

<font style="color:#000000;"><b>如果我们需要后续执行的 Pass 能够获得前面的 Pass 的渲染结果，需要使用 C# 代码创建临时渲染纹理（见 14.6.2）。</b></font>

## 表面着色器
**表面着色器**（Surface Shader）是Unity自己创造的一种着色器代码类型，即 _"Standard Surface Shader"_，它的本质是对顶点/片元着色器的一层封装，优点在于它帮助我们处理了很多光照细节，我们**可以直接使用而无需自己计算实现光照细节**，但是 **渲染的消耗较大，可控性较低。** 其特点在于：

1. 表面着色器相关代码在**SubShader语句块**中（**并非Pass**）的`CGPROGRAM`和`ENDCG`之间
2. **无需使用多个Pass**，Unity会在内部帮助我们去处理
3. **代码量较少，可控性较低，性能消耗较高**
4. 适用于处理需要和各种光源打交道的着色器（**主机、PC平台时更适用，移动平台需要考虑性能消耗**）

## CG/HLSL
### Shader和CG/HLSL的关系
Unity Shader是用ShaderLab语言编写的，但是在表面着色器和顶点/片元着色器中，我们可以在ShaderLab的内部嵌套CG/HLSL语言来编写，同时由于CG和DirectX9风格的HLSL从写法上来说几乎是同一种语言，因此我们认为**在Unity中CG和HLSL是等价的。**

### CG变量的基本数据类型
`uint`：32位无符号整形

`int`：32位整形

`float`：32位浮点数	符号：`f`

`half`：16位浮点数	符号：`h`

`fixed`：12位浮点数

`bool`：布尔类型

`string`：字符串

+ `sampler`纹理对象句柄：用于处理纹理（Texture）数据的数据类型，主要区别是纹理的维度和类型

`sampler`：通用的纹理采样器，可以用于处理各种不同维度和类型的纹理

`sampler1D`：用于一维纹理，通常用于对一维纹理进行采样，例如从左到右的渐变色

`sampler2D`：用于二维纹理，最常见的纹理类型之一。它用于处理二维图像纹理，例如贴图

`sampler3D`：用于三维纹理，通常用于体积纹理，例如体积渲染

`samplerCUBE`：用于立方体纹理，通常用于处理环境映射等需要立方体贴图的情况

`samplerRECT`：用于处理矩形纹理，通常用于一些非标准的纹理映射需求



+ 矩阵：以`int`为例，有`intnxm`，其中`n`和`m`均在[1, 4]区间，矩阵中的元素均用逗号隔开

```c
int2x3 mInt2x3 = {1, 2, 3,
                  4, 5, 6};
```

+ `bool`类型的特殊使用：

```c
float3 a = float3(0.5, 0.0, 1.0);
float3 b = float3(0.6, -0.1, 0.9);
bool3 c = а < b;

//运算后c的结果为bool3(true, false, false)
```

### 运算符
+ **逻辑运算**

CG语言中不存在逻辑判断中的“**短路**”操作。

+ **数学运算**

CG语言中取余符号`%`只能用于对整数取余。

### 流程控制语句
CG语言应尽可能少的使用循环语句，利用**GPU的并行性**来替代循环。

### 自定义函数
#### 无返回值的函数
```c
void name(in 参数类型 参数名, out 参数类型 参数名)
{
    //函数体
}

```

+ `void`：以`void`开头，表示没有返回值
+ `name`：函数的名称
+ `in`：表示是输入参数，表示由函数外部传递给函数内部，**内部不会修改该参数**，只会使用该参数进行计算，允许有多个
+ `out`：表示是输出参数，表示由函数内部传递给函数的调用者，在函数内部必须对该参数值进行初始化或修改，允许有多个

{% note info %}
`in`和`out`都可以省略，但是会降低代码的可读性和可维护性。

{% endnote %}

```csharp
void test(in fixed inF, out fixed outF)
{
    outF = inF + 10;
}

...

fixed f = 10;
fixed f2;

test(f, f2);
```

#### 有返回值的函数
```csharp
type name(in 参数类型 参数名)
{
    //函数体
    return 返回值;
}
```

+ `type`：返回值类型
+ `return`：返回指定类型的数据

{% note info %}
有返回值的函数中同样可以使用`out`，但**一般不会出现需要多个返回值的情况**，对于顶点/片元着色器只会使用单返回值的方式进行处理。

{% endnote %}

### 顶点/片元着色器
#### 基本结构
```csharp
Pass
{
    CGPROGRAM
    //编译指令
    //指明顶点着色器所对应的函数名
    #pragma vertex myVert
    //指明片元着色器所对应的函数名
    #pragma fragment myFrag

    //由于顶点着色器需要向片元着色器传递顶点数据，因此需要有返回值
    //POSITION 模型空间中的顶点坐标（输入）
    //SV_POSITION 裁剪空间中的顶点坐标（输出）
    float4 myVert(float4 v:POSOTION) : SV_POSITION
    {
        //将顶点从模型空间转换到裁剪空间
        //同样可以使用新版本的 UnityObjectToClipPos(v)
        return mul(UNITY_MATRIX_MVP, v);
    }

    //SV_Target 将输出值（颜色）存储到渲染目标中，此处为默认的帧缓存中
    fixed4 myFrag() : SV_Target
    {
        return fixed4(1, 0, 0, 1);
    }

    ENDCG
}
```

#### 顶点/片元着色器通信
顶点着色器获取数据以及向片元着色器传递数据均可以通过结构体的形式来一次性传递多个参数。

##### 顶点着色器获取数据
```csharp
struct a2v //Application to Vertex
{
    float4 vertex : POSITION;
    float3 normal : NORMAL;
    float2 uv : TEXCOORD0;
}

float4 vert(a2v data) : SV_POSITION
{
    ...
}
```

##### 向片元着色器传递数据
{% note danger %}
**片元着色器中的输入**实际上是把**顶点着色器的输出**进行**插值**后得到的结果。

{% endnote %}

{% note info %}
**顶点着色器的输出结构中必须包含一个语义为SV_POSITION的变量**，否则，渲染器将无法得到裁剪空间中的顶点坐标，也就无法把顶点渲染到屏幕上。

{% endnote %}

```csharp
struct a2v //Application to Vertex
{
    float4 vertex : POSITION;
    float3 normal : NORMAL;
    float2 uv : TEXCOORD0;
}

struct v2f //Vertex to Fragment
{
    float4 position : SV_POSITION;
    float3 normal : NORMAL;
    float2 uv : TEXCOORD0;
}

v2f vert(a2v data) : SV_POSITION
{
    v2f v2fData;
    v2fData.position = UnityObjectToClipPos(data.vertex);
    //省略对于 normal 和 uv 的处理
    v2fData.normal = data.normal;
    v2fData.uv = data.uv;

    return v2fData;
}

fixed4 frag(v2f data) : SV_Target
{
    ...
}
```

### 语义/插值寄存器
<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/63937386/1771141749397-7409c392-17c3-42db-85ce-e2df679e28a2.png)

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/63937386/1771141860346-ce7c0288-be70-42d1-8758-d73346e1d527.png)

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/63937386/1771141870258-ccace201-c690-4699-ace5-d72478d79a07.png)

### 使用ShaderLab（Properties中定义的）属性
我们需要在CG代码中定义**名称与属性完全相同且类型匹配的变量**，即可获取`Properties`中的属性值。

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/63937386/1771157889234-65a2e37b-bd8c-4ec3-9d52-e2f9286a955d.png)

### CG 内置文件
<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/63937386/1771158768631-52bfa745-9a88-466d-8b0d-d75764b80013.png)

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/63937386/1771158778000-98fc5b92-eafe-4211-8355-2fd8582a5bf4.png)

+ <font style="color:#DF2A3F;background-color:#FBDE28;"><b>纹理坐标指的是当前顶点的uv坐标值。</b></font>

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/63937386/1771158785721-ef6a2e3d-b6db-4106-9135-908c0fa59ecf.png)

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/63937386/1771319108278-947ab792-2471-48fa-a370-994f760f395f.png)

+ `unity_ObjectToWorld` = `UNITY_MATRIX_M`：从模型空间变换到世界空间（后者较新）

# 光照模型
## 颜色相乘和相加的区别
颜色相乘用于颜色的相互混合，例如材质的颜色和光照的颜色；

颜色相加用于光照的叠加，例如多盏光源或者漫反射和高光反射的叠加；

颜色相乘最终会趋向于黑色，这和现实中的颜色混合相符；

颜色相加最终会趋向于白色，现实中多盏光源叠加也确实会让物体更亮。

## 逐顶点光照和逐片元光照
### 逐顶点光照
**逐顶点光照**只会在顶点上进行光照计算，而顶点之间的其他区域会通过插值的方式计算。

+ **优点：** 计算量较小，适合需要**性能优化**的场景；
+ **缺点：** 照明效果不够精细，颜色插值不足以捕捉到细微的照明变化

### 逐片元光照
**逐片元光照**会在每个像素（片元）上进行光照计算。

+ **优点：** 逐片元光照提供了更高的清晰度，适用于PC和主机游戏；
+ **缺点：** 计算量较大，性能要求高。

## 漫反射
### Lambert 漫反射
**漫反射**（DiffuseReflection）是光线撞击一个物体表面后以各个方向均匀地反射出去的过程，在漫反射下，光线以无规律的方式散射，而不像镜面反射那样按照特定的角度反射。这种散射导致了物体表面看起来均匀而不闪烁的效果。

#### 兰伯特光照模型
兰伯特光照模型认为**漫反射光的强度仅与光源方向和反射点处表面法线的夹角的余弦成正比。**

$\color{red}c_\text{diffuse} = (c_\text{light} \cdot m_\text{diffuse}) \max(0, n \cdot l)$

+ $n$表示物体表面法线的单位向量；	
+ $I$为指向光源的单位向量；		
+ $m_\text{diffuse}$为材质的漫反射颜色；
+ $c_\text{light}$是光源颜色。				

{% note info %}
由于$n$和$I$均为单位向量，因此它们的点乘表示光源方向和法线方向的夹角的余弦值。

$n \cdot I = |n| |I| \cos \theta = 1 \cdot 1 \cdot \cos \theta = \cos \theta$

由于漫反射强度显然不能是负值，因此我们使用$max$来保证当余弦值小于零时直接取零，以此来防止物体被后也被光源照亮，以及物体被背后的光源照亮。但这显然**会导致物体的背后呈现出完全的黑色，且没有亮度变化的细节，因此我们会添加环境光来防止阴影处全黑。**

{% endnote %}

##### 逐顶点光照
<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/63937386/1771396391150-ca0d9c49-c3c4-4f31-964d-8d86fb3d967c.png)

```c
Shader "Unlit/Lambert"
{
    Properties
    {
        _Color ("Color", Color) = (1,1,1,1)
    }
    SubShader
    {
        Tags { "LightMode"="ForwardBase" } //处理不透明物体的光照渲染

        Pass
        {
            CGPROGRAM
            #pragma vertex vert
            #pragma fragment frag

            #include "UnityCG.cginc"
            #include "Lighting.cginc"

            fixed4 _Color;

            struct v2f
            {
                fixed3 color : COLOR;
                float4 vertex : SV_POSITION;
            };

            v2f vert (appdata_base v)	//不必写SV_POSITION语义，因为在v2f结构体中已经包括了
            {
                v2f v2fData;

                v2fData.vertex = UnityObjectToClipPos(v.vertex);

                float3 normal = UnityObjectToWorldNormal(v.normal);
                float3 lightDir = normalize(_WorldSpaceLightPos0.xyz);

                fixed3 diffuse = _LightColor0.rgb * _Color.rgb * max(0, dot(normal, lightDir));

                v2fData.color = diffuse + UNITY_LIGHTMODEL_AMBIENT.rgb;

                return v2fData;
            }

            fixed4 frag (v2f i) : SV_Target
            {
                return fixed4(i.color.rgb, 1);
            }
            ENDCG
        }
    }
}
```

+ `UnityObjectToWorldNormal()`用于将法线**从模型空间转化到世界空间**，同时**会将法线自动归一化**
+ `_WorldSpaceLightPos0`表示光源$0$在世界坐标系中的位置，同时由于光源方向是一个向量，因此同时可直接用于**表示一个从原点指向光源位置的向量，即光源方向。**
+ `_LightColor0`在Lighting.cginc内置文件中，表示**光源的颜色**

##### 逐片元光照
<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/63937386/1771396412484-39de19a8-c166-4f66-a436-c9748207bb06.png)

```c
Shader "Unlit/LambertF"
{
    Properties
    {
        _Color ("Color", Color) = (1,1,1,1)
    }
    SubShader
    {
        Tags { "LightMode"="ForwardBase" }

        Pass
        {
            CGPROGRAM
            #pragma vertex vert
            #pragma fragment frag

            #include "UnityCG.cginc"
            #include "Lighting.cginc"

            struct v2f
            {
                float3 normal : NORMAL;
                float4 vertex : SV_POSITION;
            };

            fixed4 _Color;

            v2f vert (appdata_base v)
            {
                v2f o;

                o.vertex = UnityObjectToClipPos(v.vertex);
                o.normal = UnityObjectToWorldNormal(v.normal);

                return o;
            }

            fixed4 frag (v2f i) : SV_Target
            {
                float3 lightDir = normalize(_WorldSpaceLightPos0.xyz);
                float3 normal = normalize(i.normal); //重新归一化法线

                fixed3 diffuse = _Color.rgb * _LightColor0.rgb * max(0, dot(normal, lightDir));

                return fixed4((diffuse + UNITY_LIGHTMODEL_AMBIENT.rgb).rgb, 1);
            }
            ENDCG
        }
    }
}
```

{% note danger %}
**重新归一化法线**是因为在插值过程中法线的模长会被改变，因此需要重新归一化

{% endnote %}

### Half Lambert 漫反射
**兰伯特光照模型**的缺点在于**模型的背光区域看上去像一个平面，没有亮暗变化**，因此 Valve 在兰伯特光照模型的基础上进行改进，并在 **《半条命》** 中提出了 **半兰伯特光照模型**。

半兰伯特光照模型中的**模型背光面同样有明暗变化**，但是它**没有任何物理依据**，仅仅是一个视觉加强技术。

$\mathbf{c}_\text{diffuse} = (\mathbf{c}_\text{light} \cdot \mathbf{m}_\text{diffuse}) (\alpha (\hat{\mathbf{n}} \cdot \mathbf{l}) + \beta)$

其中$\alpha$和$\beta$常取0.5，即：

$\mathbf{c}_\text{diffuse} = (\mathbf{c}_\text{light} \cdot \mathbf{m}_\text{diffuse}) (0.5 \times (\hat{\mathbf{n}} \cdot \mathbf{l}) + 0.5)$

从公式中可以看出，$(0.5 \times (\hat{\mathbf{n}} \cdot \mathbf{l}) + 0.5)\in [0,1]$，因此模型背光面同样具有亮暗变化。

#### 逐顶点光照
```c
Shader "Unlit/Half Lambert"
{
    Properties
    {
        _Color ("Color", Color) = (1,1,1,1)
    }
    SubShader
    {
        Tags { "LightMode"="ForwardBase" }

        Pass
        {
            CGPROGRAM
            #pragma vertex vert
            #pragma fragment frag

            #include "UnityCG.cginc"
            #include "Lighting.cginc"

            fixed4 _Color;

            struct v2f
            {
                fixed3 color : COLOR;
                float4 vertex : SV_POSITION;
            };

            v2f vert (appdata_base v)
            {
                v2f o;

                o.vertex = UnityObjectToClipPos(v.vertex);

                float3 normal = UnityObjectToWorldNormal(v.normal);
                float3 lightDir = normalize(_WorldSpaceLightPos0.xyz);

                fixed3 diffuse = _LightColor0.rgb * _Color.rgb * (dot(normal, lightDir) * 0.5 + 0.5);

                o.color = diffuse + UNITY_LIGHTMODEL_AMBIENT.rgb;

                return o;
            }

            fixed4 frag (v2f i) : SV_Target
            {
                return fixed4(i.color, 1);
            }
            ENDCG
        }
    }
}

```

#### 逐片元光照
<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/63937386/1771396447608-4c10be38-9fc0-47b4-9b1d-8255e35b67be.png)<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/63937386/1771396474489-babae3c7-fb6b-40f9-be1d-3a8da495dfd2.png)

```c
Shader "Unlit/Half LambertF"
{
    Properties
    {
        _Color ("Color", Color) = (1,1,1,1)
    }
    SubShader
    {
        Tags { "LightMode"="ForwardBase" }

        Pass
        {
            CGPROGRAM
            #pragma vertex vert
            #pragma fragment frag

            #include "UnityCG.cginc"
            #include "Lighting.cginc"

            fixed4 _Color;

            struct v2f
            {
                float3 normal : NORMAL;
                float4 vertex : SV_POSITION;
            };

            v2f vert (appdata_base v)
            {
                v2f o;

                o.vertex = UnityObjectToClipPos(v.vertex);
                o.normal = UnityObjectToWorldNormal(v.normal);

                return o;
            }

            fixed4 frag (v2f i) : SV_Target
            {
                float3 lightDir = normalize(_WorldSpaceLightPos0.xyz);

                float3 worldNormal = normalize(i.normal); //插值后归一化

                fixed3 diffuse = _LightColor0.rgb * _Color.rgb * (dot(worldNormal, lightDir) * 0.5 + 0.5);

                fixed3 color = diffuse + UNITY_LIGHTMODEL_AMBIENT.rgb;

                return fixed4(color, 1);
            }
            ENDCG
        }
    }
}

```

## 高光反射
### Phong 高光反射
Phong式高光反射光照模型认为高光反射的颜色和**光源的反射方向以及观察者位置方向向量夹角的余弦成正比**，并且**通过对余弦值取n次幂来表示光泽度**（或反光度）。

$c_\text{specular} = (c_\text{light} \cdot m_\text{specular}) \max(0, \hat{\mathbf{v}} \cdot \hat{\mathbf{r}})^{m_\text{gloss}}$

+ $\hat{\mathbf{v}}$：归一化后的视角方向向量；
+ $\hat{\mathbf{r}}$：归一化后的反射方向向量；
+ $m_\text{gloss}$：光泽度。值越大，高光点越集中。

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/63937386/1771316726577-4efb8108-7d1d-4c23-8ed7-6f0fc879efbe.png)

#### 逐顶点光照
<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/63937386/1771396338857-cd3ee318-b2fb-4f63-96bc-cfae32b203e7.png)

```c
Shader "Unlit/Phong"
{
    Properties
    {
        _SpecularColor ("SpecularColor", Color) = (1,1,1,1)
        _SpecularNum("SpecularNum", Range(0,20)) = 0.5
    }
    SubShader
    {
        Tags { "LightMode"="ForwardBase" }

        Pass
        {
            CGPROGRAM
            #pragma vertex vert
            #pragma fragment frag

            #include "UnityCG.cginc"
            #include "Lighting.cginc"

            struct v2f
            {
                fixed3 color : COLOR;
                float4 vertex : SV_POSITION;
            };

            fixed4 _SpecularColor;
            float _SpecularNum;

            v2f vert (appdata_base v)
            {
                v2f o;
                o.vertex = UnityObjectToClipPos(v.vertex);

                float3 lightDir = normalize(_WorldSpaceLightPos0.xyz);
                float3 normal = UnityObjectToWorldNormal(v.normal);

                float3 worldPos = mul(UNITY_MATRIX_M, v.vertex);

                //视角方向向量和光源方向向量不一样，和摄像机位置以及顶点位置都有关
                float3 viewDir = normalize(_WorldSpaceCameraPos.xyz - worldPos);

                float3 reflectDir = normalize(reflect(-lightDir, normal));

                fixed3 specular = _LightColor0.rgb * _SpecularColor.rgb * pow(max(0, dot(viewDir, reflectDir)), _SpecularNum);
                
                o.color = specular;

                return o;
            }

            fixed4 frag (v2f i) : SV_Target
            {

                return fixed4(i.color, 1);
            }
            ENDCG
        }
    }
}
```

+ `reflect()`：根据光线入射方向向量（**从光源指向顶点**）计算反射方向向量，**两个向量都需要归一化**。

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/63937386/1771318929237-9a671e47-b42b-4ba6-a973-fd05427c00ba.png)

#### 逐片元光照
<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/63937386/1771396286911-0f6e3796-89d6-499b-b1ce-94668720cebb.png)

```c
Shader "Unlit/Phong_SpecularF"
{
    Properties
    {
        _SpecularColor("SpecularColor", Color) = (1,1,1,1)
        _SpecularNum("SpecularNum", Range(0,20)) = 4
    }
    SubShader
    {
        Tags { "LightMode"="ForwardBase" }

        Pass
        {
            CGPROGRAM
            #pragma vertex vert
            #pragma fragment frag

            #include "UnityCG.cginc"
            #include "Lighting.cginc"

            fixed4 _SpecularColor;
            float _SpecularNum;

            struct v2f
            {
                float3 worldNormal : NORMAL;
                float3 worldPos : TEXCOORD0;
                float4 vertex : SV_POSITION;
            };

            v2f vert (appdata_base v)
            {
                v2f o;

                //这三个元素只有顶点着色器能够获取，因此需要在顶点着色器中处理后再传给片元着色器
                o.vertex = UnityObjectToClipPos(v.vertex);
                o.worldNormal = UnityObjectToWorldNormal(v.normal);
                o.worldPos = mul(unity_ObjectToWorld, v.vertex);

                return o;
            }

            fixed4 frag (v2f i) : SV_Target
            {
                float3 worldNormal = normalize(i.worldNormal);
                float3 lightDir = normalize(_WorldSpaceLightPos0.xyz);

                float3 reflectDir = normalize(reflect(-lightDir, worldNormal));

                float3 viewDir = normalize(_WorldSpaceCameraPos.xyz - i.worldPos);

                fixed3 specular = _LightColor0.rgb * _SpecularColor.rgb * pow( max( 0, dot(viewDir, reflectDir)), _SpecularNum);

                return fixed4(specular, 1);
            }
            ENDCG
        }
    }
}
```

### Blinn-Phong 高光反射
**Blinn-Phong式高光反射**光照模型是对Phong式高光反射光照模型的改进，Phong式高光反射模型需要防止摄像机方向向量$\hat{\mathbf{v}}$和反射方向$\hat{\mathbf{r}}$之间的夹角为负数，因此同样使用了`max`函数，这导致当夹角为90°时，高光周围会出现明显的断层，过度不够柔和。Blinn-Phong通过引入**半程向量**$\hat{\mathbf{h}}$来解决这一问题。

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/63937386/1771394071930-2b0b17a5-9d9b-4d60-993c-46ffddf6dc50.png)

半程向量$\hat{\mathbf{h}}$为**归一化后的视角方向**$\hat{\mathbf{v}}$**和光源方向**$\hat{\mathbf{I}}$**的角平分线方向（当视角方向和光源方向相反时为零向量）**，其公式如下：

$\hat{\mathbf{h}} = \frac{\hat{\mathbf{v}} + \hat{\mathbf{l}}}{|\hat{\mathbf{v}} + \hat{\mathbf{l}}|}$

Blinn-Phong使用该半程向量$\hat{\mathbf{h}}$与法线$\hat{\mathbf{n}}$之间的夹角来进行计算：

$c_{\text{specular}} = (c_{\text{light}} \cdot m_{\text{specular}}) \max(0, \hat{\mathbf{n}} \cdot \hat{\mathbf{h}})^{m_{\text{gloss}}}$

{% note danger %}
当视角方向$\hat{\mathbf{v}}$和反射光线方向重合时夹角为0；但是出现90°的情况需要根据实际情况讨论，尤其是当视角方向和光源方向夹角大于90°时（即看向物体背后时），高光强度依然很有可能不是零，甚至能够从物体接近180°的背后看见高光，这显然不符合实际，因此在实际使用时，我们常会对该公式进行**物理上的修正**：

$c_{\text{specular}} = (c_{\text{light}} \cdot m_{\text{specular}}) \max(0, \hat{\mathbf{n}} \cdot \hat{\mathbf{h}})^{m_{\text{gloss}}} \times \max(0, \hat{\mathbf{n}} \cdot \hat{\mathbf{I}})$

{% endnote %}

#### Blinn-Phong和Phong高光反射的区别
+ **Blinn-Phong**的高光散射较为均匀，**高光点较大，适合更加平滑的表面**；而**Phong**的高光散射较为锐利，**高光点较集中，适合更加粗糙的表面**；
+ **Blinn-Phong**在一些情况下**更加符合实际**场景；
+ **Blinn-Phong**使用了视角方向$\hat{\mathbf{v}}$和光源方向$\hat{\mathbf{I}}$来计算，这两个向量都是已知量，因此**计算更快**；**Phong**则需要先计算出反射向量，因此**计算较慢。**

#### 逐顶点光照
<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/63937386/1771396361079-4038aa2e-6996-40b7-abe9-fd4670332a0c.png)

```c
Shader "Unlit/Blinn_Phong"
{
    Properties
    {
        _SpecularColor("SpecularColor", Color) = (1,1,1,1)
        _Gloss("Gloss", Range(0,20)) = 16
    }
    SubShader
    {
        Pass
        {
            Tags { "LightMode"="ForwardBase" }
            CGPROGRAM
            #pragma vertex vert
            #pragma fragment frag
            #include "UnityCG.cginc"
            #include "Lighting.cginc"
            struct v2f
            {
                fixed3 color : COLOR;
                float4 vertex : SV_POSITION;
            };
            fixed4 _SpecularColor;
            float _Gloss;
            v2f vert (appdata_base v)
            {
                v2f o;
                o.vertex = UnityObjectToClipPos(v.vertex);
                
                float3 worldNormal = UnityObjectToWorldNormal(v.normal); 
                float3 lightDir = normalize(_WorldSpaceLightPos0.xyz);
                float3 worldPos = mul(unity_ObjectToWorld, v.vertex);
                float3 viewDir = normalize(_WorldSpaceCameraPos.xyz - worldPos);
                float3 halfDir = normalize(lightDir + viewDir); 
                o.color = _LightColor0.rgb * _SpecularColor.rgb * pow(max(0, dot(worldNormal, halfDir)), _Gloss);
                return o;
            }
            fixed4 frag (v2f i) : SV_Target
            {
                return fixed4(i.color, 1);
            }
            ENDCG
        }
    }
}
```

#### 逐片元光照
<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/63937386/1771396223048-d1fdbf55-5949-4755-a94c-90a3fc0aeb6d.png)

```c
Shader "Unlit/Blinn_Phong_SpecularF"
{
    Properties
    {
        _SpecularColor("SpecularColor", Color) = (1,1,1,1)
        _Gloss("Gloss", Range(0,20)) = 16
    }
    SubShader
    {
        Pass
        {
            Tags { "LightMode"="ForwardBase" }
            CGPROGRAM
            #pragma vertex vert
            #pragma fragment frag
            #include "UnityCG.cginc"
            #include "Lighting.cginc"
            struct v2f
            {
                float3 worldPos : TEXCOORD0;
                float3 worldNormal : NORMAL;
                float4 vertex : SV_POSITION;
            };
            fixed4 _SpecularColor;
            float _Gloss;
            v2f vert (appdata_base v)
            {
                v2f o;
                o.vertex = UnityObjectToClipPos(v.vertex);               
                o.worldNormal = UnityObjectToWorldNormal(v.normal); 
                o.worldPos = mul(unity_ObjectToWorld, v.vertex);
                return o;
            }
            fixed4 frag (v2f i) : SV_Target
            {
                float3 WorldNormal = normalize(i.worldNormal);
                float3 lightDir = normalize(_WorldSpaceLightPos0.xyz);
                float3 viewDir = normalize(_WorldSpaceCameraPos.xyz - i.worldPos);
                float3 halfDir = normalize(lightDir + viewDir); 
                fixed3 specular = _LightColor0.rgb * _SpecularColor.rgb * pow(max(0, dot(WorldNormal, halfDir)), _Gloss);
                return fixed4(specular, 1);
            }
            ENDCG
        }
    }
}

```

## 环境光
环境光可以通过 "Windows - Rendering - Lighting" 的 "Environment" 页签设置，可以选择来源自 "Skybox" 或是指定 "Color"的环境光，也可以设置为 "Gradient" 模式，此时环境光将会由以下三种光线混合得到：

+ "unity_AmbientSky"（周围的天空环境光）
+ "unity_AmbientEquator"（周围的赤道环境光）
+ "unity_AmbientGround"（周围的地面环境光）

## Phong 光照模型
$物体表面光照颜色 = Lambert漫反射 + Phong高光反射 + 环境光$

### 逐顶点光照
<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/63937386/1771396541193-f2cedd8e-d5fc-49d3-a0a2-e91932339ed0.png)

```c
Shader "Unlit/Phong"
{
    Properties
    {
        _Color ("Color", Color) = (1,1,1,1)

        _SpecularColor("SpecularColor", Color) = (1,1,1,1)
        _SpecularNum("SpecularNum", Range(0,20)) = 4
    }
    SubShader
    {
        Tags { "Lighting"="ForwardBase" }

        Pass
        {
            CGPROGRAM
            #pragma vertex vert
            #pragma fragment frag

            #include "UnityCG.cginc"
            #include "Lighting.cginc"

            struct v2f
            {
                fixed3 color : COLOR;
                float4 vertex : SV_POSITION;
            };

            fixed4 _Color;

            fixed4 _SpecularColor;
            float _SpecularNum;

            v2f vert (appdata_base v)
            {
                v2f o;

                o.vertex = UnityObjectToClipPos(v.vertex);

                float3 worldNormal = UnityObjectToWorldNormal(v.normal);
                float3 lightDir = normalize(_WorldSpaceLightPos0.xyz);
                fixed3 diffuse = _LightColor0.rgb * _Color.rgb * max(0, dot(lightDir, worldNormal));

                float3 reflectDir = normalize(reflect(-lightDir, worldNormal));
                float3 worldPos = mul(unity_ObjectToWorld, v.vertex);
                float3 viewDir = normalize(_WorldSpaceCameraPos.xyz - worldPos);
                fixed3 specular = _LightColor0.rgb * _SpecularColor.rgb * pow( max(0, dot(viewDir, reflectDir)), _SpecularNum);

                o.color = UNITY_LIGHTMODEL_AMBIENT.rgb + diffuse + specular;

                return o;
            }

            fixed4 frag (v2f i) : SV_Target
            {
                return fixed4(i.color, 1);
            }
            ENDCG
        }
    }
}

```

### 逐片元光照
<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/63937386/1771396557733-84e3a911-a7bf-49e0-be8e-602670fa05e4.png)

```c
Shader "Unlit/PhongF"
{
    Properties
    {
        _DiffuseColor("DiffuseColor", Color) = (1,1,1,1)
        _SpecularColor("SpecularColor", Color) = (1,1,1,1)
        _Gloss("Gloss", Range(0,20)) = 16
    }
    SubShader
    {
        Pass
        {
            Tags { "LightMode"="ForwardBase" }

            CGPROGRAM
            #pragma vertex vert
            #pragma fragment frag

            #include "UnityCG.cginc"
            #include "Lighting.cginc"

            struct v2f
            {
                float3 worldNormal : NORMAL;
                float3 worldPos : TEXCOORD0;
                float4 vertex : SV_POSITION;
            };

            fixed4 _DiffuseColor;
            fixed4 _SpecularColor;
            float _Gloss;

            v2f vert (appdata_base v)
            {
                v2f o;

                o.vertex = UnityObjectToClipPos(v.vertex);
                o.worldNormal = UnityObjectToWorldNormal(v.vertex);
                o.worldPos = mul(unity_ObjectToWorld, v.vertex);

                return o;
            }

            fixed4 frag (v2f i) : SV_Target
            {
                float3 lightDir = normalize(_WorldSpaceLightPos0.xyz);
                float3 worldNormal = normalize(i.worldNormal);
                fixed3 diffuse = _LightColor0.rgb * _DiffuseColor.rgb * max(0, dot(lightDir, worldNormal));

                float3 reflectDir = normalize(reflect(-lightDir, worldNormal));
                float3 viewDir = normalize(_WorldSpaceCameraPos.xyz - i.worldPos);
                fixed3 specular = _LightColor0.rgb * _SpecularColor * pow(max(0, dot(viewDir, reflectDir)), _Gloss);

                fixed3 color = UNITY_LIGHTMODEL_AMBIENT.rgb + diffuse + specular;

                return fixed4(color, 1);
            }
            ENDCG
        }
    }
}

```

## Blinn-Phong光照模型
$物体表面光照颜色 = Lambert漫反射 + Blinn\text{-}Phong高光反射 + 环境光$

### 逐顶点光照
<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/63937386/1771398418842-61fa706c-d48b-42a0-b054-9443c01df13b.png)

```c
Shader "Unlit/Blinn_Phong"
{
    Properties
    {
        _Color ("Color", Color) = (1,1,1,1)
        _SpecularColor("SpecularColor", Color) = (1,1,1,1)
        _SpecularNum("SpecularNum", Range(0,20)) = 16
    }
    SubShader
    {
        Tags { "Lighting"="ForwardBase" }
        Pass
        {
            CGPROGRAM
            #pragma vertex vert
            #pragma fragment frag
            #include "UnityCG.cginc"
            #include "Lighting.cginc"
            struct v2f
            {
                fixed3 color : COLOR;
                float4 vertex : SV_POSITION;
            };
            fixed4 _Color;
            fixed4 _SpecularColor;
            float _SpecularNum;
            fixed3 getLambertColor(in float3 objNormal)
            {
                float3 worldNormal = UnityObjectToWorldNormal(objNormal);
                float3 lightDir = normalize(_WorldSpaceLightPos0.xyz);
                fixed3 diffuse = _LightColor0.rgb * _Color.rgb * max(0, dot(lightDir, worldNormal));
                return diffuse;
            }
            fixed3 getSpecularColor(in float3 objNormal, in float4 objVertex)
            {
                
                float3 worldNormal = UnityObjectToWorldNormal(objNormal);
                float3 worldPos = mul(unity_ObjectToWorld, objVertex);
                float3 lightDir = normalize(UnityWorldSpaceLightDir(worldPos));

                float3 viewDir = normalize(UnityWorldSpaceViewDir(worldPos));
                float3 halfDir = normalize(viewDir + lightDir);
                fixed3 specular = _LightColor0.rgb * _SpecularColor.rgb * pow( max(0, dot(worldNormal, halfDir)), _SpecularNum);
                return specular;
            }
            v2f vert (appdata_base v)
            {
                v2f o;
                o.vertex = UnityObjectToClipPos(v.vertex);
                fixed3 diffuse = getLambertColor(v.normal);
                fixed3 specular = getSpecularColor(v.normal, v.vertex);
                o.color = UNITY_LIGHTMODEL_AMBIENT.rgb + diffuse + specular;
                return o;
            }
            fixed4 frag (v2f i) : SV_Target
            {
                return fixed4(i.color, 1);
            }
            ENDCG
        }
    }
}

```

### 逐片元光照
<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/63937386/1771398445020-d22722bc-6ea3-401e-a5e2-4ae53c19d36f.png)

```c
Shader "Unlit/Blinn_PhongF"
{
    Properties
    {
        _DiffuseColor("DiffuseColor", Color) = (1,1,1,1)
        _SpecularColor("SpecularColor", Color) = (1,1,1,1)
        _Gloss("Gloss", Range(0,20)) = 16
    }
    SubShader
    {
        Pass
        {
            Tags { "LightMode"="ForwardBase" }
            CGPROGRAM
            #pragma vertex vert
            #pragma fragment frag
            #include "UnityCG.cginc"
            #include "Lighting.cginc"
            struct v2f
            {
                float3 worldNormal : NORMAL;
                float3 worldPos : TEXCOORD0;
                float4 vertex : SV_POSITION;
            };
            fixed4 _DiffuseColor;
            fixed4 _SpecularColor;
            float _Gloss;
            v2f vert (appdata_base v)
            {
                v2f o;
                o.vertex = UnityObjectToClipPos(v.vertex);
                o.worldNormal = UnityObjectToWorldNormal(v.vertex);
                o.worldPos = mul(unity_ObjectToWorld, v.vertex);
                return o;
            }
            fixed3 getLambertFColor(in float3 worldNormal)
            {
                float3 lightDir = normalize(_WorldSpaceLightPos0.xyz);
                float3 WorldNormal = normalize(worldNormal);
                fixed3 diffuse = _LightColor0.rgb * _DiffuseColor.rgb * max(0, dot(lightDir, WorldNormal));

                return diffuse;
            }
            fixed3 getSpecularFColor(in float3 worldNormal, in float3 worldPos)
            {
                float3 WorldNormal = normalize(worldNormal);
                float3 lightDir = normalize(UnityWorldSpaceLightDir(worldPos));
                float3 viewDir = normalize(UnityWorldSpaceViewDir(worldPos));
                float3 halfDir = normalize(lightDir + viewDir);
                fixed3 specular = _LightColor0.rgb * _SpecularColor * pow(max(0, dot(WorldNormal, halfDir)), _Gloss);   
                
                return specular;
            }
            fixed4 frag (v2f i) : SV_Target
            {
                fixed3 diffuse = getLambertFColor(i.worldNormal);
                fixed3 specular = getSpecularFColor(i.worldNormal, i.worldPos);
                fixed3 color = UNITY_LIGHTMODEL_AMBIENT.rgb + diffuse + specular;
                return fixed4(color, 1);
            }
            ENDCG
        }
    }
}
```

# 纹理
## UV坐标系
在OpenGL中，纹理空间的原点位于左下角；

在DirectX中，原点位于左上角；

Unity使用的纹理空间是符合OpenGL的传统的，即**原点位于纹理左下角。u表示水平轴，v表示垂直轴。**

uv坐标均是被**归一化**后的，以此来适配不同大小的纹理图片，例如256*256、1024*1024等。每一个$[0, 1]$区间代表一张纹理图片，如图所示。

**只有顶点中会记录uv坐标信息**，因此数据在传递进片元着色器前同样会进行**插值**运算。

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/63937386/1771399923133-8a5d1dc3-784c-46c0-b179-e4e0517a331a.png)

## 纹理属性
1. Texture Type（纹理图片类型）和Texture Shape（纹理图片类型）决定了我们是否能在shader当中获取正确数据
2. Create from Grayscale（从灰度创建）：用于高度纹理

`Bumpiness`（颠簸值）控制凹凸程度

Filtering（过滤模式）决定计算凹凸程度的算法

`Sharp`：滤波生成法线

`Smooth`：平滑的生成法线

3. Wrap Mode（循环模式）决定了缩放偏移的表现效果

`Repeat`：在区块中重复纹理

`Clamp`：拉伸纹理的边缘

`Mirror`：在每个整数边界上镜像纹理以创建重复图案

`MirrorOnce`：镜像纹理一次，然后将拉伸边缘纹理

`Per-axis`：单独控制如何在u轴和v轴上包裹纹理

3. Filter Mode（过滤模式）决定了放大缩小纹理时看到的图片质量

`Point`：纹理在靠近时变为像素块状

`Bilinear`：纹理在靠近时变得模糊

`Trilinear`：与Bilinear类似，但纹理也在不同的Mip级别之间模糊

过滤模式在开启MipMaps根据实际表现选择，可以达到不同的表现效果

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/63937386/1771402116887-4eebab2f-eb2f-48db-b1c4-305647b0b2af.png)

## 单张纹理
### 单张纹理采样
```c
Shader "Unlit/SingleTexture"
{
    Properties
    {
        _MainTex ("Texture", 2D) = "" {}
    }
    SubShader
    {
        Pass
        {
            CGPROGRAM
            #pragma vertex vert
            #pragma fragment frag
            
            #include "UnityCG.cginc"

            sampler2D _MainTex;

            //获取纹理平移缩放属性的固定命名方式 纹理名_ST
            float4 _MainTex_ST;	//S表示Scale缩放；T表示Translation平移

            v2f_img vert (appdata_base v)
            {
                v2f_img o; 
                o.pos = UnityObjectToClipPos(v.vertex);
                
                //o.uv = TRANSFORM_TEX(v.texcoord.xy, _MainTex);
                o.uv = v.texcoord.xy * _MainTex_ST.xy + _MainTex_ST.zw;	//xy代表缩放；zw代表平移
                
                return o;
            } 

            fixed4 frag (v2f_img i) : SV_Target
            {
                //这里的i.uv已经经过了插值运算
                fixed4 col = tex2D(_MainTex, i.uv);

                return col;
            }
            ENDCG
        }
    }
}
```

### 单张纹理采样 + Blinn-Phong
```c
Shader "Unlit/SingleTexture_BlinnPhong"
{
    Properties
    {
        _MainTex ("Texture", 2D) = "" {}
        _DiffuseColor("DiffuseColor", Color) = (1,1,1,1)
        _SpecularColor("SpecularColor", Color) = (1,1,1,1)
        _Gloss("Gloss", Range(0, 20)) = 16
    }
    SubShader
    {
        Pass
        {
            Tags{"LightMode" = "ForwardBase"}

            CGPROGRAM
            #pragma vertex vert
            #pragma fragment frag

            #include "UnityCG.cginc"
            #include "Lighting.cginc"

            struct v2f
            {
                float2 uv : TEXCOORD0;
                float4 vertex : SV_POSITION;
                float3 worldPos : TEXCOORD1;
                float3 worldNormal : NORMAL;
            };

            sampler2D _MainTex;
            float4 _MainTex_ST;
            fixed4 _DiffuseColor;
            fixed4 _SpecularColor;
            float _Gloss;

            v2f vert (appdata_base v)
            {
                v2f o;
                o.vertex = UnityObjectToClipPos(v.vertex);
                o.uv = TRANSFORM_TEX(v.texcoord, _MainTex);

                o.worldNormal = UnityObjectToWorldNormal(v.normal);
                o.worldPos = mul(unity_ObjectToWorld, v.vertex);
                return o;
            }

            fixed4 frag (v2f i) : SV_Target
            {
                //纹理颜色需要和物体漫反射颜色进行乘法叠加得到反射率
                fixed3 albedo = tex2D(_MainTex, i.uv).rgb * _DiffuseColor.rgb;

                float3 WorldNormal = normalize(i.worldNormal);
                float3 lightDir = normalize(UnityWorldSpaceLightDir(i.worldPos));
                float3 viewDir = normalize(UnityWorldSpaceViewDir(i.worldPos));

                float3 halfDir = normalize(lightDir + viewDir);

                fixed3 diffuse = _LightColor0.rgb * albedo * max(0, dot(lightDir, WorldNormal));
                fixed3 specular = _LightColor0.rgb * _SpecularColor * pow(max(0, dot(halfDir, WorldNormal)), _Gloss);
                
                //为了避免渲染效果偏灰色，我们使用环境光照乘以反射率得到环境光部分
                fixed3 color = UNITY_LIGHTMODEL_AMBIENT.rgb * albedo + diffuse + specular;

                return fixed4(color, 1);
            }
            ENDCG
        }
    }
}
```

+ `albedo`：反射率，指物体漫反射颜色与纹理颜色的叠加，即最终的材质颜色。

{% note danger %}
**环境光之所以需要乘以反射率**，是因为物体的背光面一般会呈现黑色和物体本身颜色的叠加，而环境光是场景中经过多次反射，最终均匀照射到物体上的微弱光线，**这部分光线颜色中并不包含物体本身的颜色，因此叠加的环境光大概率会遮盖部分物体本身的颜色**，但是根据物理规律，既然环境光照射到物体上，那么环境光的反射光自然应该带有物体本身的颜色（反射率），因此我们认为**环境光应该是`UNITY_LIGHTMODEL_AMBIENT.rgb`与反射率的叠加**。

同样，**金属物体的高光分量同样需要乘以反射率**：金属表面有大量的自由电子，光线几乎完全无法进入物体内部，导致**金属几乎没有漫反射**，金属的高光来自表面的金属电子，它们会吸收特定频率的光，剩余的自然光分量颜色的混合即为金属的颜色，这部分光线组成了金属的彩色高光；非金属物体在被光线照射时，部分光线进入了物体内部，通过折射和散射获得了物体的颜色，最终反射出物体形成漫反射，剩下的光线未能进入物体内部，未能接触到物体颜色，在表面直接形成高光反射，因此**非金属物体的高光反射一般只和光源颜色有关，不用乘以反射率。**

{% endnote %}

## 凹凸映射
纹理除了可以用来进行颜色映射外，另外一种常见的应用就是进行**凹凸映射**。凹凸映射使用一张纹理来修改模型表面的法线，让我们**不需要增加顶点**，而**让模型看起来有凹凸效果**。

实现凹凸映射主要由两种方法：**高度纹理**（height map）/高度映射（height mapping）和**法线纹理**（normal map）/法线映射（normal mapping）

### 高度纹理
高度纹理贴图一般简称高度图，它存储了模型表面上每个点的高度信息。通常它**使用灰度图像**，其中不同的灰度值表示不同高度。**较亮区域通常对应向外凸起的点，较暗的区域对应向内凹陷的点。** 它主要用于模拟物体表面的位移。

存储规则：我们使用 rgba 来进行存储，图片中的像素点各自的 **RGB 值是相同的，都表示高度值**，A 值一般情况下为 1。**高度值** 范围一般为 0~1，**0 代表最低，1 代表最高**。

+ **优点：** 可以通过高度图很明确地知道模型表面的凹凸情况
+ **缺点：** 无法在Shader中直接得到模型表面点的法线信息，需要通过额外的计算得到，因此**会增加性能消耗**，所以我们几乎很少使用高度纹理，**一般都会使用法线纹理。**

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/63937386/1771403987299-f3194f96-6449-4bd0-875c-7e7195cc1b0e.png)

### 法线纹理
法线纹理贴图存储了**模型表面上每个点的法线方向**。

存储规则：图片中的**RGB值分别存储法线的X、Y、Z分量值**，A值可以用于存储其他信息，比如材质光滑度等。

+ **优点：** 可以直接获取法线信息，简单处理后就能够参与光照计算，性能表现更好
+ **缺点：** 无法从法线纹理贴图中直观地看出模型表面的凹凸情况

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/63937386/1771426277223-b5802e36-5195-48fc-9f41-8a91aed02c80.png)

由于方向是相对于坐标空间来描述的，因此根据相对坐标系的不同，法线纹理的存储方式分为以下两种：

1. 基于**模型空间**的法线纹理
2. 基于**切线空间**的法线纹理

#### 如何从法线纹理贴图中读取法线信息
顶点的法线向量为单位向量，因此$x,y,z \in [-1,1]$，而像素（RGBA）范围在$[0,1]$之间，因此在使用像素的颜色信息来存储法线分量时需要建立如下映射关系：

$\text{pixel} = \frac{\text{normal} + 1}{2} \in [0,1]$

这就要求在从像素中取出法线分量信息时需要进行上式的逆运算：

$\text{normal} = \text{pixel} \times 2 - 1 \in [-1,1]$

这步逆运算可以通过Unity提供的内置函数`UnpackNormal`来完成，该函数同时还会自动对法线进行解压运算（Unity会根据不同平台对法线纹理进行压缩）

{% note warning %}
Unity `DXT5` 贴图压缩方式中，**A 通道** 的精度最高，其次是 **G 通道**。而法线方向的 $x$ 方向上的差异最为明显，因此 `DXT5` 压缩方式使用 `A` 通道来存储法线 $x$，使用 `G` 通道来存储法线 $y$，而法线 $z$ 可以直接通过计算得到（法线模长为 1）。因此，**一张法线贴图实际上只需要使用 `AG` 通道，剩余的两个通道我们通常会用来存储金属度和粗糙度。**

由于不同压缩方式会采用不同的通道来存储法线 $xy$，因此 Unity 提供了 `UnpackNormal()` 函数来自动判断不同的压缩方式对应的法线分量，同时自动完成从 $[0,1]$ 区间到 $[-1,1]$ 区间的转换。

{% endnote %}

##### 基于模型空间的法线纹理
模型数据中自带的法线数据显然是定义在模型空间中的，因此**最直接的存储法线贴图数据的方式**就是将修改后的法线数据同样基于模型空间存储。

由于模型空间中每个点的法线方向各异，例如$(0,1,0)$经过映射后对应$RGB(0.5,1,0.5)$（浅绿色），$(0,-1,0)$经过映射后对应$RGB(0.5,0,0.5)$（紫色），因此模型空间下的法线纹理看起来是“**五颜六色**”的。



<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/63937386/1771426277223-b5802e36-5195-48fc-9f41-8a91aed02c80.png)

##### 基于切线空间的法线纹理
模型顶点的**切线空间**（tangent space）的**原点就是该顶点本身**；$z$**轴是顶点的法线方向**$(n)$，$x$**轴是顶点的切线方向**$(t)$，$y$轴可以**通过法线和切线叉积得到**，也被称为**副切线**（bitangent，$b$）或**副法线**。

{% note warning %}
**切线空间坐标系是<font style="color:#DF2A3F;"><b>右手坐标系</b></font>。**

{% endnote %}





<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/63937386/1771430178653-eb01b36f-351c-4358-87d5-85f7383b6a22.png)

在切线空间中，如果模型顶点的法线不需要修改，那么它自然会与$z$轴重合，即$(0,0,1)$，映射到像素的结果为$(0.5,0.5,1)$（浅蓝色），通常模型的大部分法线和模型本身法线保持一致，因此切线空间下的法线纹理呈现出**大片的浅蓝色**，只有需要修改法线的部分呈现出其他的颜色。

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/63937386/1771426277223-b5802e36-5195-48fc-9f41-8a91aed02c80.png)

##### 为什么切线空间更加常用
在实际使用法线纹理时，**基于切线空间的法线纹理更加常用**，原因有以下几点：

+ **可以用于不同模型：** 模型空间下的法线是绝对法线信息，只适用于创建时的模型，不能用于其他模型
+ **方便处理模型变形：** 同上
+ **可以复用：** 例如一个砖块，6个面贴图都是一样的，可以只用一张法线贴图即可用于6个面
+ **可以压缩：** 可以只存储两个轴的分量
+ **方便制作UV动画：** UV坐标改变可以实现凹凸移动效果，模型空间下的法线显然无法适配
+ 等等

#### 法线信息如何参与光照计算
##### 在切线空间中进行光照计算
在切线空间中进行光照计算，需要将光照方向和视角方向变换到切线空间中进行计算，这部分变换可以直接在**顶点着色器**中完成，**计算量较小，效率更高。**

但是在切线空间中处理光照方向和视角方向等全局信息容易产生错误，由于GPU的插值过程是一个线性变换，只适用于例如世界空间这样的全局静止坐标系，而切线空间的坐标轴方向会随着模型表面发生旋转，这会导致当两个顶点的切线坐标轴方向不一致时，顶点与顶点之间的线性插值不够准确，因此**视觉效果可能不够准确**。**但是如果没有全局效果的要求，我们依然优先在切线空间中进行光照计算。**

{% note danger %}
一般情况下，我们不会将光照方向和视角方向直接从世界空间变换到切线空间，原因在于，如果要求出世界空间到切线空间的矩阵，这是一个父到子的矩阵，即子到父矩阵的逆矩阵，而子坐标空间，即切线空间的坐标轴（顶点的切线$T$，副切线$B$，法线$N$）向量是定义在模型空间中的   ($\color{red}\text{切线空间} \xrightarrow{父} \text{模型空间} \xrightarrow{父} \text{世界空间}$），因此我们需要将$TBN$三个向量分别乘以模型空间变换到世界空间的矩阵（**3次矩阵乘法**），然后构建世界空间变换到切线空间的矩阵，最后将视角方向和光照方向向量乘以该矩阵，**每个顶点需要进行4次矩阵乘法；**（如果只变换$TB$向量，通过叉乘求出$N$，总共需要3次矩阵乘法）

而如果我们**先将光照方向和视角方向乘以世界空间变换到模型空间的矩阵**（**1次矩阵乘法**），再使用模型顶点中自带的$TBN$向量**构建从模型空间变换到切线空间的变换矩阵**（这是一个父到子空间的变换矩阵，由于$TBN$是三个互相垂直的单位向量，因此该矩阵为正交矩阵，即**该变换矩阵的逆矩阵就是它的转置矩阵**），最后将模型空间中的光照和视角方向向量**乘以该矩阵**（**1次矩阵乘法**），即可将光照和视角方向向量变换到切线空间中，**每个顶点只需要进行2次矩阵乘法，能够节省一半的计算量**，因此我们选择后者进行光照和视角方向的坐标空间变换。

{% endnote %}

{% note danger %}
需要注意的是，顶点的切线数据是一个`float4`类型的变量，`.w`一般等于`±1`，用于标识副切线的“方向”：由于**叉积的结果遵循右手定则**，同时我们**规定**$\bf{B = N \times T}$，因此副切线$B$的方向在一般情况下是唯一确定的，但是为了节省贴图空间，美术资源通常会使用UV镜像，例如角色的左脸和右脸可能会共用同一块UV区域，**在UV镜像中，原本的右手坐标系会被镜像成左手坐标系**，此时我们需要引入`.w = -1`来标识镜像的UV区域。综上，我们**需要将叉积的结果乘以`v.tangent.w`来获得正确的副切线方向**。

{% endnote %}

```c
Shader "Unlit/NormalMapTangentSpace"
{
    Properties
    {
        _MainTex ("Texture", 2D) = "" {}
        _BumpMap("BumpMap", 2D) = ""{}
        _BumpScale("BumpScale", Range(0,1)) = 1
        _DiffuseColor("DiffuseColor", Color) = (1,1,1,1)
        _SpecularColor("SpecularColor", Color) = (1,1,1,1)
        _Gloss("Gloss", Range(0,20)) = 16
    }
    SubShader 
    {
        Pass
        {
            Tags{"LightMode" = "ForwardBase"}

            CGPROGRAM
            #pragma vertex vert
            #pragma fragment frag

            #include "UnityCG.cginc"
            #include "Lighting.cginc"

            struct v2f
            {
                float4 uv : TEXCOORD0;//xyTex, zwBump
                float4 vertex : SV_POSITION;
                float3 lightDir : TEXCOORD1; //切线空间下
                float3 viewDir : TEXCOORD2; //切线空间下
            };

            sampler2D _MainTex;
            float4 _MainTex_ST;
            sampler2D _BumpMap;
            float4 _BumpMap_ST;
            float _BumpScale;
            fixed4 _DiffuseColor;
            fixed4 _SpecularColor;
            float _Gloss;

            v2f vert (appdata_full v)
            {
                v2f o;
                o.vertex = UnityObjectToClipPos(v.vertex);

                //使用xy来记录颜色纹理 zw来记录法线纹理
                //实际上颜色纹理和法线纹理通常会使用同一组纹理坐标以减少插值寄存器
                o.uv.xy = TRANSFORM_TEX(v.texcoord, _MainTex);
                o.uv.zw = TRANSFORM_TEX(v.texcoord, _BumpMap);

                float3 binormal = cross(normalize(v.normal), normalize(v.tangent.xyz)) * v.tangent.w;
                
                //模型空间变换到切线空间的矩阵
                float3x3 rotation = float3x3(v.tangent.xyz, 
                                             binormal, 
                                             v.normal);
                //TANGENT_SPACE_ROTATION;

                o.lightDir = mul(rotation, ObjSpaceLightDir(v.vertex));
                o.viewDir = mul(rotation, ObjSpaceViewDir(v.vertex));
                return o;
            }

            fixed4 frag (v2f i) : SV_Target
            {
                float4 packedNormal = tex2D(_BumpMap, i.uv.zw);
                float3 tangentNormal = UnpackNormal(packedNormal);
                tangentNormal *= _BumpScale;

                //将乘以凹凸程度_BumpScale后的法线重新归一化
                tangentNormal.z = sqrt(1 - saturate(dot(tangentNormal.xy,tangentNormal.xy)));

                float3 tangentLightDir = normalize(i.lightDir);
                float3 tangentViewDir = normalize(i.viewDir);
                fixed3 albedo = tex2D(_MainTex, i.uv.xy) * _DiffuseColor.rgb;
                fixed3 diffuse = _LightColor0.rgb * albedo * max(0, dot(tangentLightDir, tangentNormal));
                
                float3 halfDir = normalize(tangentViewDir + tangentLightDir);
                fixed3 specular = _LightColor0.rgb * _SpecularColor.rgb * pow(max(0, dot(halfDir, tangentNormal)), _Gloss);

                fixed3 color = UNITY_LIGHTMODEL_AMBIENT.rgb * albedo + diffuse + specular;

                return fixed4(color, 1);
            }
            ENDCG
        }
    }
}
```

+ `ObjSpaceLightDir(v.vertex)`：模型空间下的光照方向；
+ `ObjSpaceViewDir(v.vertex)`：模型空间下的视角方向；
+ `UnpackNormal`：提取并解压法线信息；
+ `saturate(value)`：将 `value` 限制在 $[0,1]$ 区间，即当 `value < 0` 返回 `0`；`value > 1` 返回 `1`；`0 ≤ value ≤ 1` 返回 `value` 本身（相当于 `max(0, dot(normal, lightDir))`）。
+ `TANGENT_SPACE_ROTATION`：相当于嵌入如下代码：

```c
float3 binormal = cross(v.normal, v.tangent.xyz)* v.tangent.w;
float3x3 rotation = float3x3(v.tangent.xyz, binormal, v.normal);
```

{% note warning %}
+ `tangentNormal.z = sqrt(1 - saturate(dot(tangentNormal.xy,tangentNormal.xy)));`：

我们使用`_BumpScale`来调整物体表面的凹凸程度，并将调整后的法线应用于光照计算中，但是用于光照计算中的法线是单位向量，需要被归一化。这意味着我们**不能直接将`tangentNormal.xyz`全部乘以`_BumpScale`**，否则会被归一化抵消；也就是说，我们**不能用法线的模长来衡量凹凸程度**，而应该**使用法线的倾斜程度来描述凹凸程度的大小**。

**法线倾斜越剧烈，意味着该处表面起伏越大**。用于描述法线在上下左右四个方向上的倾斜情况的是`tangentNormal.xy`，因此我们选择只**将`tangentNormal.xy`乘以`_BumpScale`来扩大法线的倾斜程度**。同时我们还需要保证法线的归一化，因此使用 $\bf{z = \sqrt{1 - (x^2 + y^2)}}$ 来计算`tangent.z`。显然，`tangentNormal.xy`越大，`tangentNormal.z`越小，法线倾斜角越大，符合实际。但是当`_BumpScale`很大时，会出现$x^2 + y^2 > 1$的情况，即根号中为负数，这意味着法线朝向物体表面内侧，这是不符合常理的，因此我们**使用`saturate`将结果截取到** $[0,1]$ **区间**。这样一来，不管`_BumpScale`如何变化，当`tangent.z = 0`时凹凸程度最大，`tangent.z = 1`时凹凸程度最小。

{% endnote %}

##### 在世界空间中进行光照计算
在世界空间中进行光照计算，由于法线纹理贴图采样是像素级别的，因此必须在片元着色器中完成，这意味着我们需要在片元着色器中将采样得到的法线数据变换到世界空间中，由于变换发生在**片元着色器**中，**计算量较大，效率较低。**

在世界空间中进行光照计算显然不会遇到因线性插值带来的准确性问题，因此可以更容易地应用于全局效果的计算，**通用性更强**。

{% note info %}
将法线方向变换到世界空间中，需要计算切线空间到世界空间的变换矩阵，这是一个子到父空间的变换矩阵，因此我们只需要**将 $TBN$ 变换到世界空间中，即乘以模型空间变换到世界空间的矩阵，即可求出切线空间到世界空间的变换矩阵。**

{% endnote %}

{% note warning %}
由于将$TBN$变换到世界空间中的操作是在片元着色器中完成了，这意味着我们需要将变换矩阵传入片元着色器，由于GPU的插值寄存器以`float4`为基本单位，直接使用`float3x3`来存储变换矩阵的话会浪费插值寄存器的空间，即占用三个完整的插值寄存器，但是最后一个插值寄存器有三个空位没有被利用。

因此，我们**使用三个独立的`float4`变量来分别存放`TBN.x`、`TBN.y`、`TBN.z`以及`WorldPos.xyz`，以此来减少插值寄存器的使用数量（`-float3 WorldPos`）**。然后在片元着色器中重新组合成`float3x3`类型的变换矩阵，同时我们不选择直接显式声明一个`float3x3`类型的变量来存放变换矩阵，而是直接在`mul()`函数中临时声明，即`mul(float3x3(i.TtoW0.xyz, i.TtoW1.xyz, i.TtoW2.xyz), tangentNormal)`，编译器在处理时会直接从插值寄存器中取值并参与运算，并不会开辟一块`float3x3`的内存空间，即不会带来额外的内存损失。

{% endnote %}

```c
Shader "Unlit/NormalMapWorldSpace"
{
    Properties
    {
        _MainTex ("Texture", 2D) = "white" {}
        _BumpMap("BumpMap", 2D) = "bump"{}
        _BumpScale("BumpScale", Range(0,1)) = 1
        _DiffuseColor("DiffuseColor", Color) = (1,1,1,1)
        _SpecularColor("SpecularColor", Color) = (1,1,1,1)
        _Gloss("Gloss", Range(0,20)) = 16
    }
    SubShader
    {
        Pass
        {
            Tags{"LightMode" = "ForwardBase"}

            CGPROGRAM
            #pragma vertex vert
            #pragma fragment frag

            #include "UnityCG.cginc"
            #include "Lighting.cginc"

            struct v2f
            {
                float4 uv : TEXCOORD0;
                float4 vertex : SV_POSITION;
                float4 TtoW0 : TEXCOORD2;
                float4 TtoW1 : TEXCOORD3;
                float4 TtoW2 : TEXCOORD4;
            };

            sampler2D _MainTex;
            float4 _MainTex_ST;
            sampler2D _BumpMap;
            float4 _BumpMap_ST;
            float _BumpScale;
            fixed4 _DiffuseColor;
            fixed4 _SpecularColor;
            float _Gloss;

            v2f vert (appdata_full v)
            {
                v2f o;
                o.vertex = UnityObjectToClipPos(v.vertex);
                o.uv.xy = TRANSFORM_TEX(v.texcoord, _MainTex);
                o.uv.zw = TRANSFORM_TEX(v.texcoord, _BumpMap);

                float3 worldPos = mul(unity_ObjectToWorld, v.vertex);

                float3 worldNormal = UnityObjectToWorldNormal(v.normal);
                float3 worldTangent = UnityObjectToWorldDir(v.tangent);
                float3 worldBinormal = cross(normalize(worldTangent), normalize(worldNormal)) * v.tangent.w;

                o.TtoW0 = float4(worldTangent.x, worldBinormal.x, worldNormal.x, worldPos.x);
                o.TtoW1 = float4(worldTangent.y, worldBinormal.y, worldNormal.y, worldPos.y);
                o.TtoW2 = float4(worldTangent.z, worldBinormal.z, worldNormal.z, worldPos.z);

                return o;
            }

            fixed4 frag (v2f i) : SV_Target
            {
                float3 worldPos = float3(i.TtoW0.w, i.TtoW1.w, i.TtoW2.w);
                fixed3 lightDir = normalize(UnityWorldSpaceLightDir(worldPos));
                fixed3 viewDir = normalize(UnityWorldSpaceViewDir(worldPos));

                float4 packedNormal = tex2D(_BumpMap, i.uv.zw);
                float3 tangentNormal = UnpackNormal(packedNormal);
                tangentNormal.xy *= _BumpScale;
                tangentNormal.z = sqrt(1 - saturate(dot(tangentNormal.xy, tangentNormal.xy)));

                float3 worldTangentNormal = mul(float3x3(i.TtoW0.xyz, i.TtoW1.xyz, i.TtoW2.xyz), tangentNormal);

                fixed3 albedo = tex2D(_MainTex, i.uv.xy) * _DiffuseColor.rgb;
                fixed3 diffuse = _LightColor0.rgb * albedo * max(0, dot(lightDir, worldTangentNormal));
                
                float3 halfDir = normalize(lightDir + viewDir);
                fixed3 specular = _LightColor0.rgb * _SpecularColor.rgb * pow(max(0, dot(halfDir, worldTangentNormal)), _Gloss);

                fixed3 color = UNITY_LIGHTMODEL_AMBIENT.rgb * albedo + diffuse + specular;

                return fixed4(color, 1);
            }
            ENDCG
        }
    }
}
```

+ `UnityWorldSpaceLightDir`：自动判断光源类型，返回光源方向向量（未归一化）。

{% note warning %}
注意：光源类型分为点光源和线光源，两者的光源方向的计算方式不同，后者由于光线为平行光，其在世界坐标系中的光源方向恒定，不会因顶点位置的不同而改变，因此可以直接用`_WorldSpaceLightPos0.xyz`作为光源方向向量；但是前者的光源方向显然会根据顶点位置的不同而变化，因此需要使用`_WorldSpaceLightPos0.xyz - worldPos`作为光源的方向向量。因此在实际使用中，我们通常会使用`UnityWorldSpaceLightDir`来自动判断光源类型并返回光源方向向量（未归一化）。

{% endnote %}

## 渐变纹理
Valve在游戏《军团要塞2》中提出了一种基于**冷到暖色调（cool-to-warm tones）**的着色技术，通过**控制漫反射光照结果**使得物体的轮廓线（明暗交界处）更加明显，得到**插画风格的渲染效果**。

**渐变纹理**使用**半兰伯特**光照模型公式中的$(0.5 \times (\hat{\mathbf{n}} \cdot \hat{\mathbf{l}}) + 0.5)$作为uv坐标从渐变纹理中取出颜色。为了使得物体的轮廓线更加明显，渐变纹理大多使用突变，即**没有平滑过渡的色调组成的色块**，通过颜色上的突变来模拟卡通风格的渲染。

$$
uv = (0.5 \times (\hat{\mathbf{n}} \cdot \hat{\mathbf{l}}) + 0.5,\ 0.5 \times (\hat{\mathbf{n}} \cdot \hat{\mathbf{l}}) + 0.5)
$$

$$
albedo = \mathbf{c}_\text{light} \times \mathbf{m}_\text{diffuse} \times \mathrm{tex2D}(\_RampTex, uv)
$$

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/63937386/1771827949634-08d05ffa-7c31-4bc0-96ba-63fcb75060d4.png)

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/63937386/1771828043232-4cc09390-4e14-4569-9326-bf8118b8fcf6.png)

```c
Shader "Unlit/RampTexture"
{
    Properties
    {
        _RampTex ("RampTex", 2D) = "" {}
        _DiffuseColor("DiffuseColor", Color) = (1,1,1,1)
        _SpecularColor("SpecularColor", Color) = (1,1,1,1)
        _Gloss("Gloss", Range(8, 256)) = 16
    }
    SubShader
    {
        Pass
        {
            Tags { "LightMode"="ForwardBase" }
            CGPROGRAM
            #pragma vertex vert
            #pragma fragment frag
            #include "UnityCG.cginc"
            #include "Lighting.cginc"
            struct v2f
            {
                float4 vertex : SV_POSITION;
                float3 worldPos : TEXCOORD0;
                float3 worldNormal : NORMAL;
            };
            sampler2D _RampTex;
            float4 _RampTex_ST;
            fixed4 _DiffuseColor;
            fixed4 _SpecularColor;
            float _Gloss;
            v2f vert (appdata_base v)
            {
                v2f o;
                o.vertex = UnityObjectToClipPos(v.vertex);
                o.worldPos = mul(unity_ObjectToWorld, v.vertex);
                o.worldNormal = UnityObjectToWorldNormal(v.normal);
                return o;
            }
            fixed4 frag (v2f i) : SV_Target
            {

                float3 lightDir = normalize(UnityWorldSpaceLightDir(i.worldPos));
                float3 viewDir = normalize(UnityWorldSpaceViewDir(i.worldPos));
                float3 WorldNormal = normalize(i.worldNormal);
                
                fixed halfLambert = dot(lightDir, WorldNormal) * 0.5 + 0.5;
                fixed3 diffuseColor = _LightColor0.rgb * _DiffuseColor.rgb * tex2D(_RampTex, fixed2(halfLambert, halfLambert));
                
                float3 halfDir = normalize(lightDir + viewDir);
                fixed3 specularColor = _LightColor0.rgb * _SpecularColor.rgb * pow(max(0, dot(halfDir, WorldNormal)), _Gloss);
                fixed3 color = UNITY_LIGHTMODEL_AMBIENT.rgb + diffuseColor + specularColor;
                return fixed4(color, 1);
            }
            ENDCG
        }
    }
}
```

+ 渐变纹理中一般都会包含阴影的颜色，因此环境光`UNITY_LIGHTMODEL_AMBIENT.rgb`无需乘以`albedo`。

### 黑点问题
+ **Wrap Mode 黑点问题：**

可以看出，左图（使用`Repeat`模式）中在高光区域有一些黑点。这是由浮点精度造成的，当我们使用`fixed2(halfLambert, halfLambert)`对渐变纹理进行采样时，虽然理论上`halfLambert`的值在$[0,1]$之间，但可能会有1.00001这样的值出现。如果我们使用的是`Repeat`模式，此时就会舍弃整数部分，只保留小数部分，得到的值就是0.00001，对应了渐变图中最左边的值，即黑色。因此，就会出现图中这样在高光区域反而有黑点的情况。**我们只需要把渐变纹理的`WrapMode`设为`Clamp`模式就可以解决这种问题。**

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/63937386/1771831915816-ccd71bfd-ff40-4667-92e9-bcd48c3c06df.png)

## 遮罩纹理
遮罩纹理通常用于控制或限制某些效果的显示范围，它允许我们可以保护某些区域，使它们免于某些修改。

我们通过采样得到遮罩纹理的纹素值，然后使用其中某个（或某几个）通道的值来与某种表面属性进行相乘，这样，当该通道的值为0时，可以保护表面不受该属性的影响，例如控制某些区域透明，某些区域不透明，或是调整不同区域高光的亮度强弱等等。总而言之，**使用遮罩纹理可以让美术人员更加精准（像素级别）地控制模型表面的各种性质。**

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/63937386/1771834296491-5012bc3a-1c73-4adf-9b7d-93cc2aa46b8d.png)

{% note info %}
一般来说，大部分**遮罩纹理的RGB值均相同**，我们可以随意取用RGB中的其中一个分量。

{% endnote %}

```c
Shader "Unlit/MaskTexture"
{
    Properties
    {
        _MainTex ("Texture", 2D) = "" {}
        _BumpMap("BumpMap", 2D) = ""{}
        _BumpScale("BumpScale", Range(0,1)) = 1
        _DiffuseColor("DiffuseColor", Color) = (1,1,1,1)
        _SpecularColor("SpecularColor", Color) = (1,1,1,1)
        _SpecularMask("SpecularMask", 2D) = ""{}
        _SpecularScale("SpecularScale", Range(0,1)) = 1
        _Gloss("Gloss", Range(0,20)) = 16
    }
    SubShader 
    {
        Pass
        {
            Tags{"LightMode" = "ForwardBase"}

            CGPROGRAM
            #pragma vertex vert
            #pragma fragment frag

            #include "UnityCG.cginc"
            #include "Lighting.cginc"

            struct v2f
            {
                float4 uv : TEXCOORD0;//xyTex, zwBump
                float4 vertex : SV_POSITION;
                float3 lightDir : TEXCOORD1; //切线空间下
                float3 viewDir : TEXCOORD2; //切线空间下
            };

            sampler2D _MainTex;
            float4 _MainTex_ST;
            sampler2D _BumpMap;
            float4 _BumpMap_ST;
            float _BumpScale;
            fixed4 _DiffuseColor;
            fixed4 _SpecularColor;
            sampler2D _SpecularMask;
            float4 _SpecularMask_ST;
            float _SpecularScale;
            float _Gloss;

            v2f vert (appdata_full v)
            {
                v2f o;
                o.vertex = UnityObjectToClipPos(v.vertex);
                o.uv.xy = TRANSFORM_TEX(v.texcoord, _MainTex);
                o.uv.zw = TRANSFORM_TEX(v.texcoord, _BumpMap);

                float3 binormal = cross(normalize(v.tangent), normalize(v.normal)) * v.tangent.w;
                float3x3 rotation = float3x3(v.tangent.xyz, binormal, v.normal);
                //TANGENT_SPACE_ROTATION;

                o.lightDir = mul(rotation, ObjSpaceLightDir(v.vertex));
                o.viewDir = mul(rotation, ObjSpaceViewDir(v.vertex));
                return o;
            }

            fixed4 frag (v2f i) : SV_Target
            {
                float4 packedNormal = tex2D(_BumpMap, i.uv.zw);
                float3 tangentNormal = UnpackNormal(packedNormal);
                tangentNormal.xy *= _BumpScale;
                tangentNormal.z = sqrt(1 - saturate(dot(tangentNormal.xy,tangentNormal.xy)));

                float3 tangentLightDir = normalize(i.lightDir);
                float3 tangentViewDir = normalize(i.viewDir);
                fixed3 albedo = tex2D(_MainTex, i.uv.xy) * _DiffuseColor.rgb;
                fixed3 diffuse = _LightColor0.rgb * albedo * max(0, dot(tangentLightDir, tangentNormal));
                
                float3 halfDir = normalize(tangentViewDir + tangentLightDir);
                
                fixed specularMask = tex2D(_SpecularMask, i.uv.xy).r * _SpecularScale;
                
                fixed3 specular = _LightColor0.rgb * _SpecularColor.rgb * pow(max(0, dot(halfDir, tangentNormal)), _Gloss) * specularMask;
                fixed3 color = UNITY_LIGHTMODEL_AMBIENT.rgb * albedo + diffuse + specular;

                return fixed4(color, 1);
            }
            ENDCG
        }
    }
}
```

# 透明
## 渲染顺序
+ **渲染标签-渲染队列：** 决定了不同种类的物体的渲染顺序

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/63937386/1771835402648-891852a7-4e69-4341-96e7-9581a0f2c0bb.png)

由渲染队列可以看出，游戏引擎会：

+ **先渲染所有不透明物体，并开启它们的深度测试和深度写入。**
+ **把半透明物体按它们距离摄像机的远近进行排序，然后按照从后往前的顺序渲染这些半透明物体，并开启它们的深度测试，但<font style="color:#DF2A3F;"><b>关闭深度写入</b></font>。**

{% note info %}
之所以要关闭深度写入，原因在于**需要防止离摄像机近的物体完全遮挡并剔除离摄像机远的物体**，尽管无法在不分割网格的情况下正确实现透明度混合。

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/63937386/1771915224797-988762b9-6e81-41ae-981c-f4c912102283.png)<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/63937386/1771915233763-381a706b-02d0-4750-a57b-b18ebcaf3bb2.png)

+ 如果**开启深度写入**会得到以下错误结果：

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/63937386/1771915290431-ef365181-af35-4fe9-9282-4c25766a9538.png)

{% endnote %}

但是单纯根据半透明物体的远近来决定渲染顺序的结果依然不一定正确，因为这里的**排序是根据物体的远近而不是片元的远近**，例如在**物体循环重叠或部分遮挡**时，通常需要使用**分割网格**的方式来处理半透明混合的颜色，或者使用**开启深度写入的半透明效果**来模拟（性能消耗较高）

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/63937386/1771837386658-d28a8585-4b64-499f-857f-9f25f2a50d96.png)

## 颜色混合
颜色混合中使用到的RGBA分别来自**片元着色器的输出**和颜色缓冲区。

### 颜色相加
```c
//写法1
Blend 源因子 目标因子, 源透明因子 目标透明因子

//写法2
Blend 源因子 目标因子
```

我们将当前片元中的颜色记为$S$，将颜色缓冲区的颜色记为$D$，混合后的输出颜色记为$O$

+ **写法1：**

$$
\begin{aligned}
\ O_{rgb} &= \text{源因子} \times S_{rgb} + \text{目标因子} \times D_{rgb} \\[10pt]
\ O_a &= \text{源透明因子} \times S_a + \text{目标透明因子} \times D_a
\end{aligned}
$$

+ **写法2：**

$$
\begin{aligned}
O_{rgb} &= \text{源因子} \times S_{rgb} + \text{目标因子} \times D_{rgb} \\[10pt]
O_a &= \text{源因子} \times S_a + \text{目标因子} \times D_a
\end{aligned}
$$

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/63937386/1771847052182-19237b91-0a7c-439f-aac5-9380ce2286da.png)

### 其他混合操作
```c
BlendOp BlendOperation
Blend SrcFactor DstFactor //此处使用上述写法1和2均可
...
```

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/63937386/1771847115869-d28ce761-ffbe-4f0b-9c82-98174c98cf57.png)

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/63937386/1771847128996-16c28523-4c32-467f-8057-f23a3bd5816b.png)

## 透明度测试`clip()`
在游戏开发中，某些物体的透明需求可能比较“极端”：它们的**某些部位完全透明**，而**其余部位完全不透明**，因此并不需要半透明效果。针对这种场景，我们需要使用**透明度测试**。

透明度测试和深度测试的原理较为相似：**只要一个片元的透明度不满足判断条件（通常是当透明度小于某个阈值时），那么这个片元就会直接被舍弃。** 被舍弃的片元将不会再进行任何处理，也不会对颜色缓冲产生任何影响；其余片元依旧按照不透明物体的处理方式进行处理。

我们使用CG的内置函数`clip()`来进行透明度测试：

`clip()`具有以下重载类型：`void clip(float4 x); void clip(float3 x); void clip(float2 x); void clip(float1 x); void clip(float x);`

`clip()`的定义如下（以`float4`为例）：

```c
void clip(float4 x)	//传入的x一般是 当前片元的透明度 - 阈值，即 透明度 < 阈值
{
    if (any(x < 0))	//any指的是x的rgba中的任意一个分量小于0，结果即为true
        discard;	//剔除该片元 类似于直接break
}
```

```c
Shader "Unlit/AlphaTest"
{
    Properties
    {
        _MainTex ("Texture", 2D) = "" {}
        _DiffuseColor("DiffuseColor", Color) = (1,1,1,1)
        _SpecularColor("SpecularColor", Color) = (1,1,1,1)
        _Gloss("Gloss", Range(0, 20)) = 16

        _Cutoff("Cutoff", Range(0, 1)) = 0
    }
    SubShader
    {
        Tags{"Queue"="AlphaTest" "IgnoreProjector"="True" "RenderType"="TransparentCutout"}
        Pass
        {
            Tags{"LightMode" = "ForwardBase"}

            CGPROGRAM
            #pragma vertex vert
            #pragma fragment frag

            #include "UnityCG.cginc"
            #include "Lighting.cginc"

            struct v2f
            {
                float2 uv : TEXCOORD0;
                float4 vertex : SV_POSITION;
                float3 worldPos : TEXCOORD1;
                float3 worldNormal : NORMAL;
            };

            sampler2D _MainTex;
            float4 _MainTex_ST;
            fixed4 _DiffuseColor;
            fixed4 _SpecularColor;
            float _Gloss;

            fixed _Cutoff;

            v2f vert (appdata_base v)
            {
                v2f o;
                o.vertex = UnityObjectToClipPos(v.vertex);
                o.uv = TRANSFORM_TEX(v.texcoord, _MainTex);

                o.worldNormal = UnityObjectToWorldNormal(v.normal);
                o.worldPos = mul(unity_ObjectToWorld, v.vertex);
                return o;
            }

            fixed4 frag (v2f i) : SV_Target
            {
                clip(tex2D(_MainTex, i.uv).a - _Cutoff);

                fixed3 albedo = tex2D(_MainTex, i.uv).rgb * _DiffuseColor.rgb;

                float3 WorldNormal = normalize(i.worldNormal);
                float3 lightDir = normalize(UnityWorldSpaceLightDir(i.worldPos));
                float3 viewDir = normalize(UnityWorldSpaceViewDir(i.worldPos));

                float3 halfDir = normalize(lightDir + viewDir);

                fixed3 diffuse = _LightColor0.rgb * albedo * max(0, dot(lightDir, WorldNormal));
                fixed3 specular = _LightColor0.rgb * _SpecularColor * pow(max(0, dot(halfDir, WorldNormal)), _Gloss);
                fixed3 color = UNITY_LIGHTMODEL_AMBIENT.rgb * albedo + diffuse + specular;

                return fixed4(color, 1);
            }
            ENDCG
        }
    }
}
```

{% note info %}
透明度测试的Shader都应该在`SubShader`中设置以下标签：`Tags{"Queue"="AlphaTest" "IgnoreProjector"="True" "RenderType"="TransparentCutout"}`：

+ `Tags{"IgnoreProjector"="True"}`：投影器`Projector`是Unity中的一种特殊光源，其功能与URP中的`Decal`贴花系统相同，它用于在场景中投射纹理或简单的几何形状来模拟光照、阴影或其他视觉效果，例如在物体表面添加弹孔，血迹、脚印等。显然**开启了透明度测试的物体一般不应接收`Projector`，否则物体完全透明的部分上也会被添加弹孔、血迹这类贴花**，这显然是视觉错误。
+ `Tags{"RenderType"="TransparentCutout"}`：用于将Shader**分类**，以便于**实现着色器替换**，同时使摄像机正确处理片元剔除以及阴影的投射。

{% endnote %}

{% note warning %}
**透明度测试将会强制关闭Early-Z功能**，因为我们需要在片元着色器中判断片元是否需要被剔除，而Early-Z会在片元着色器之前完成深度测试等剔除操作，这会将我们需要的片元也剔除掉，因此**一旦Shader中使用了`clip()`和`discard`指令，GPU就会强制关闭Early-Z。**

{% endnote %}

## 透明度混合
```c
Shader "Unlit/AlphaBlend"
{
    Properties
    {
        _MainTex ("Texture", 2D) = "" {}
        _DiffuseColor("DiffuseColor", Color) = (1,1,1,1)
        _SpecularColor("SpecularColor", Color) = (1,1,1,1)
        _Gloss("Gloss", Range(0, 20)) = 16

        _AlphaScale("AlphaScale", Range(0, 1)) = 1
    }
    SubShader
    {
        Tags { "Queue" = "Transparent" "IgnoreProjector" = "True" "RenderType" = "Transparent"}
        Pass
        {
            Tags{"LightMode" = "ForwardBase"}

            //关闭深度写入
            ZWrite Off
            Blend SrcAlpha OneMinusSrcAlpha

            CGPROGRAM
            #pragma vertex vert
            #pragma fragment frag

            #include "UnityCG.cginc"
            #include "Lighting.cginc"

            struct v2f
            {
                float2 uv : TEXCOORD0;
                float4 vertex : SV_POSITION;
                float3 worldPos : TEXCOORD1;
                float3 worldNormal : NORMAL;
            };

            sampler2D _MainTex;
            float4 _MainTex_ST;
            fixed4 _DiffuseColor;
            fixed4 _SpecularColor;
            float _Gloss;

            fixed _AlphaScale;

            v2f vert (appdata_base v)
            {
                v2f o;
                o.vertex = UnityObjectToClipPos(v.vertex);
                o.uv = TRANSFORM_TEX(v.texcoord, _MainTex);

                o.worldNormal = UnityObjectToWorldNormal(v.normal);
                o.worldPos = mul(unity_ObjectToWorld, v.vertex);
                return o;
            }

            fixed4 frag (v2f i) : SV_Target
            {
                fixed4 texColor = tex2D(_MainTex, i.uv);
                fixed3 albedo = tex2D(_MainTex, i.uv).rgb * _DiffuseColor.rgb;

                float3 WorldNormal = normalize(i.worldNormal);
                float3 lightDir = normalize(UnityWorldSpaceLightDir(i.worldPos));
                float3 viewDir = normalize(UnityWorldSpaceViewDir(i.worldPos));

                float3 halfDir = normalize(lightDir + viewDir);

                fixed3 diffuse = _LightColor0.rgb * albedo * max(0, dot(lightDir, WorldNormal));
                fixed3 specular = _LightColor0.rgb * _SpecularColor * pow(max(0, dot(halfDir, WorldNormal)), _Gloss);
                fixed3 color = UNITY_LIGHTMODEL_AMBIENT.rgb * albedo + diffuse + specular;

                return fixed4(color.rgb, texColor.a * _AlphaScale);
            }
            ENDCG
        }
    }
}
```

## 开启深度写入的半透明效果
**关闭深度写入**后，如7.1节中所讲，如果**模型网格中相互交叉重叠的结构，会得到错误的半透明效果**（如右图所示），这是因为Unity无法判断片元的远近，也无法进行深度测试，因此**Unity只会按照模型中的三角形的索引顺序进行绘制**，由于片元没有记录深度值，因此后绘制的片元将会直接覆盖前面的片元，从而导致如右图的错误结果。我们可以选择分割网格，但是当模型过于复杂的时候这显然是不切实际的，因此我们仍然需要选择开启深度写入。



<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/63937386/1771916492658-0201a84a-2470-4507-88e7-2c4a9c18dc0e.png)

但是**直接开启深度写入依然会产生渲染错误**，如右图所示，这是因为**Unity在绘制物体的时候会按照三角形的索引顺序先后绘制**，即按照索引顺序逐个写入深度缓冲并进行深度测试，**如果先绘制的片元更靠近摄像机**，那么该片元背后的还**未被绘制的片元就会无法通过深度测试**而直接被剔除；如果**先绘制的片元离摄像机更远**，那么**该片元前方更靠近摄像机的片元便能正常写入深度缓冲**，并通过深度测试，**正确完成透明度混合**。因此右图中并不是所有区域都发生了渲染错误。

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/63937386/1771916353649-d8bd677e-4b38-459a-b22b-0bd046cd7c72.png)

因此，为了得到正确的渲染结果，我们需要使用两个`Pass`通道：**第一个`Pass`通道开启深度写入，但是关闭颜色写入（`ColorMask 0`）**，这样每个片元都会进行深度写入和深度测试，得到正确的深度缓冲区；**第二个`Pass`通道关闭深度写入**，以免污染上一个`Pass`获得的正确的深度缓冲区，并按照深度缓冲区中的深度进行透明度混合。

这样得到的**渲染结果依然还是有瑕疵**，也就是较远的片元会被直接剔除，无法与较近的片元完成透明度混合；同时**多使用一个`Pass`会导致性能的额外消耗。**

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/63937386/1771917807996-bbe46a0d-463c-427f-8e1b-8f65e8614bb1.png)

```c
Shader "Unlit/AlphaBlendZWrite"
{
    Properties
    {
        _MainTex ("Texture", 2D) = "white" {}
        _DiffuseColor("DiffuseColor", Color) = (1,1,1,1)
        _SpecularColor("SpecularColor", Color) = (1,1,1,1)
        _Gloss("Gloss", Range(0, 20)) = 16

        _AlphaScale("AlphaScale", Range(0, 1)) = 1
    }
    SubShader
    {
        Tags { "Queue" = "Transparent" "IgnoreProjector" = "True" "RenderType" = "Transparent"}
        Pass
        {
            ZWrite On
            ColorMask 0
        }
        Pass
        {
            Tags{"LightMode" = "ForwardBase"}

            ZWrite Off
            Blend SrcAlpha OneMinusSrcAlpha

            CGPROGRAM
            #pragma vertex vert
            #pragma fragment frag

            #include "UnityCG.cginc"
            #include "Lighting.cginc"

            struct v2f
            {
                float2 uv : TEXCOORD0;
                float4 vertex : SV_POSITION;
                float3 worldPos : TEXCOORD1;
                float3 worldNormal : NORMAL;
            };

            sampler2D _MainTex;
            float4 _MainTex_ST;
            fixed4 _DiffuseColor;
            fixed4 _SpecularColor;
            float _Gloss;

            fixed _AlphaScale;

            v2f vert (appdata_base v)
            {
                v2f o;
                o.vertex = UnityObjectToClipPos(v.vertex);
                o.uv = TRANSFORM_TEX(v.texcoord, _MainTex);

                o.worldNormal = UnityObjectToWorldNormal(v.normal);
                o.worldPos = mul(unity_ObjectToWorld, v.vertex);
                return o;
            }

            fixed4 frag (v2f i) : SV_Target
            {
                fixed4 texColor = tex2D(_MainTex, i.uv);
                fixed3 albedo = tex2D(_MainTex, i.uv).rgb * _DiffuseColor.rgb;

                float3 WorldNormal = normalize(i.worldNormal);
                float3 lightDir = normalize(UnityWorldSpaceLightDir(i.worldPos));
                float3 viewDir = normalize(UnityWorldSpaceViewDir(i.worldPos));

                float3 halfDir = normalize(lightDir + viewDir);

                fixed3 diffuse = _LightColor0.rgb * albedo * max(0, dot(lightDir, WorldNormal));
                fixed3 specular = _LightColor0.rgb * _SpecularColor * pow(max(0, dot(halfDir, WorldNormal)), _Gloss);
                fixed3 color = UNITY_LIGHTMODEL_AMBIENT.rgb * albedo + diffuse + specular;

                return fixed4(color.rgb, texColor.a * _AlphaScale);
            }
            ENDCG
        }
    }
}
```

+ `ColorMask 0`：不写入颜色；
+ `ColorMask R`：只写入颜色的R通道；
+ `ColorMask RGB`：只写入RGB通道，以此类推。

## 双面渲染的透明效果
在现实生活中，如果一个物体是透明的，意味着我们不仅可以透过它看到其他物体的样子，也可以看到它内部的结构。但在前面实现的透明效果中，无论是透明度测试还是透明度混合，我们都**无法观察到正方体内部及其背面的形状，导致物体看起来就好像只有半个一样**。这是因为，默认情况下**渲染引擎剔除了物体背面**（相对于摄像机的方向）的渲染图元，而**只渲染了物体的正面**。如果我们想要得到双面渲染的效果，可以使用`Cull`指令来控制需要剔除哪个面的渲染图元：

+ `Cull Back`：背面剔除（默认）；
+ `Cull Front`：正面剔除；
+ `Cull Off`：不剔除

{% note warning %}
请注意，**这里的剔除指的并不是深度测试的剔除，而是背面剔除**，例如游戏引擎不会渲染一个平面的背面，是针对某个物体本身；而深度测试的剔除是针对场景中的所有物体，以及某个物体本身。

深度测试的剔除和背面剔除并不是同一个功能，`Cull`指令只能控制背面剔除。见 4.3.2。

{% endnote %}

###  双面渲染的透明度测试
只需要添加`Cull Off`即可。

```c
Shader "Unlit/AlphaTestBothSided"
{
    Properties
    {
        _MainTex ("Texture", 2D) = "" {}
        _Color("DiffuseColor", Color) = (1,1,1,1)
        _SpecularColor("SpecularColor", Color) = (1,1,1,1)
        _Gloss("Gloss", Range(0, 20)) = 16

        _Cutoff("Cutoff", Range(0, 1)) = 0
    }
    SubShader
    {
        Tags{"Queue"="AlphaTest" "IgnoreProjector"="True" "RenderType"="TransparentCutout"}
        Pass
        {
            Cull Off

            Tags{"LightMode" = "ForwardBase"}

            CGPROGRAM
            #pragma vertex vert
            #pragma fragment frag

            #include "UnityCG.cginc"
            #include "Lighting.cginc"

            struct v2f
            {
                float2 uv : TEXCOORD0;
                float4 vertex : SV_POSITION;
                float3 worldPos : TEXCOORD1;
                float3 worldNormal : NORMAL;
            };

            sampler2D _MainTex;
            float4 _MainTex_ST;
            fixed4 _Color;
            fixed4 _SpecularColor;
            float _Gloss;

            fixed _Cutoff;

            v2f vert (appdata_base v)
            {
                v2f o;
                o.vertex = UnityObjectToClipPos(v.vertex);
                o.uv = TRANSFORM_TEX(v.texcoord, _MainTex);

                o.worldNormal = UnityObjectToWorldNormal(v.normal);
                o.worldPos = mul(unity_ObjectToWorld, v.vertex);
                return o;
            }

            fixed4 frag (v2f i) : SV_Target
            {
                clip(tex2D(_MainTex, i.uv).a - _Cutoff);

                fixed3 albedo = tex2D(_MainTex, i.uv).rgb * _Color.rgb;

                float3 WorldNormal = normalize(i.worldNormal);
                float3 lightDir = normalize(UnityWorldSpaceLightDir(i.worldPos));
                float3 viewDir = normalize(UnityWorldSpaceViewDir(i.worldPos));

                float3 halfDir = normalize(lightDir + viewDir);

                fixed3 diffuse = _LightColor0.rgb * albedo * max(0, dot(lightDir, WorldNormal));
                fixed3 specular = _LightColor0.rgb * _SpecularColor * pow(max(0, dot(halfDir, WorldNormal)), _Gloss);
                fixed3 color = UNITY_LIGHTMODEL_AMBIENT.rgb * albedo + diffuse + specular;

                return fixed4(color, 1);
            }
            ENDCG
        }
    }
    
}
```

### 双面渲染的透明度混合效果（关闭深度写入）
关闭了片元剔除之后，这意味着我们需要着重注意片元的渲染顺序：由于一般的透明度混合Shader需要关闭深度写入，这也就意味着**正方体的正面和背面会被同时画出来**，而由于**深度测试被关闭**，因此**Unity无法判断正方体的正背面的遮挡关系**，因此**无法进行深度测试的剔除**，只会根据三角形的索引顺序进行绘制，后绘制的片元会直接覆盖先绘制的片元，导致错误的渲染结果。

因此，我们需要手动**控制正背面的渲染顺序**，即使用两个`Pass`，**第一个`Pass`渲染正方体的背面（剔除正面）**，**第二个`Pass`渲染正面（剔除背面）**，Unity会按顺序先后执行两个`Pass`，得到正确的渲染结果。

```c
Shader "Unlit/AlphaBlendBothSided"
{
    Properties
    {
        _MainTex ("Texture", 2D) = "" {}
        _DiffuseColor("DiffuseColor", Color) = (1,1,1,1)
        _SpecularColor("SpecularColor", Color) = (1,1,1,1)
        _Gloss("Gloss", Range(0, 20)) = 16

        _AlphaScale("AlphaScale", Range(0, 1)) = 1
    }
    SubShader
    {
        Tags { "Queue" = "Transparent" "IgnoreProjector" = "True" "RenderType" = "Transparent"}
        Pass
        {
            Cull Front

            Tags{"LightMode" = "ForwardBase"}

            ZWrite Off
            Blend SrcAlpha OneMinusSrcAlpha

            CGPROGRAM
            #pragma vertex vert
            #pragma fragment frag

            #include "UnityCG.cginc"
            #include "Lighting.cginc"

            struct v2f
            {
                float2 uv : TEXCOORD0;
                float4 vertex : SV_POSITION;
                float3 worldPos : TEXCOORD1;
                float3 worldNormal : NORMAL;
            };

            sampler2D _MainTex;
            float4 _MainTex_ST;
            fixed4 _DiffuseColor;
            fixed4 _SpecularColor;
            float _Gloss;

            fixed _AlphaScale;

            v2f vert (appdata_base v)
            {
                v2f o;
                o.vertex = UnityObjectToClipPos(v.vertex);
                o.uv = TRANSFORM_TEX(v.texcoord, _MainTex);

                o.worldNormal = UnityObjectToWorldNormal(v.normal);
                o.worldPos = mul(unity_ObjectToWorld, v.vertex);
                return o;
            }

            fixed4 frag (v2f i) : SV_Target
            {
                fixed4 texColor = tex2D(_MainTex, i.uv);
                fixed3 albedo = tex2D(_MainTex, i.uv).rgb * _DiffuseColor.rgb;

                float3 WorldNormal = normalize(i.worldNormal);
                float3 lightDir = normalize(UnityWorldSpaceLightDir(i.worldPos));
                float3 viewDir = normalize(UnityWorldSpaceViewDir(i.worldPos));

                float3 halfDir = normalize(lightDir + viewDir);

                fixed3 diffuse = _LightColor0.rgb * albedo * max(0, dot(lightDir, WorldNormal));
                fixed3 specular = _LightColor0.rgb * _SpecularColor * pow(max(0, dot(halfDir, WorldNormal)), _Gloss);
                fixed3 color = UNITY_LIGHTMODEL_AMBIENT.rgb * albedo + diffuse + specular;

                return fixed4(color.rgb, texColor.a * _AlphaScale);
            }
            ENDCG
        }
        Pass
        {
            Cull Back

            Tags{"LightMode" = "ForwardBase"}

            ZWrite Off
            Blend SrcAlpha OneMinusSrcAlpha

            CGPROGRAM
            #pragma vertex vert
            #pragma fragment frag

            #include "UnityCG.cginc"
            #include "Lighting.cginc"

            struct v2f
            {
                float2 uv : TEXCOORD0;
                float4 vertex : SV_POSITION;
                float3 worldPos : TEXCOORD1;
                float3 worldNormal : NORMAL;
            };

            sampler2D _MainTex;
            float4 _MainTex_ST;
            fixed4 _DiffuseColor;
            fixed4 _SpecularColor;
            float _Gloss;

            fixed _AlphaScale;

            v2f vert (appdata_base v)
            {
                v2f o;
                o.vertex = UnityObjectToClipPos(v.vertex);
                o.uv = TRANSFORM_TEX(v.texcoord, _MainTex);

                o.worldNormal = UnityObjectToWorldNormal(v.normal);
                o.worldPos = mul(unity_ObjectToWorld, v.vertex);
                return o;
            }

            fixed4 frag (v2f i) : SV_Target
            {
                fixed4 texColor = tex2D(_MainTex, i.uv);
                fixed3 albedo = tex2D(_MainTex, i.uv).rgb * _DiffuseColor.rgb;

                float3 WorldNormal = normalize(i.worldNormal);
                float3 lightDir = normalize(UnityWorldSpaceLightDir(i.worldPos));
                float3 viewDir = normalize(UnityWorldSpaceViewDir(i.worldPos));

                float3 halfDir = normalize(lightDir + viewDir);

                fixed3 diffuse = _LightColor0.rgb * albedo * max(0, dot(lightDir, WorldNormal));
                fixed3 specular = _LightColor0.rgb * _SpecularColor * pow(max(0, dot(halfDir, WorldNormal)), _Gloss);
                fixed3 color = UNITY_LIGHTMODEL_AMBIENT.rgb * albedo + diffuse + specular;

                return fixed4(color.rgb, texColor.a * _AlphaScale);
            }
            ENDCG
        }
    }
}
```

# 复杂光照
## 渲染路径
在Unity里，**渲染路径**(Rendering Path)决定了光照是如何应用到UnityShader中的，即如何在Shader中访问光源数据。

大多数情况下，一个项目只使用一种渲染路径，因此我们可以为整个项目设置渲染时的渲染路径。我们可以通过在Unity的Edit → Project SettingsPlayer → Other Settings → Rendering Path中选择项目所需的渲染路径。默认情况下，该设置选择的是前向渲染路径，但有时，我们希望可以使用多个渲染路径，例如摄像机A渲染的物体使用前向渲染路径，而摄像机B渲染的物体使用延迟渲染路径。这时，我们可以在每个摄像机的渲染路径设置中设置该摄像机使用的渲染路径，以覆盖Project Settings中的设置。

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/63937386/1771922202192-d97f3994-6ad4-4f3f-85ba-7a730927592b.png)

在上面的设置中，如果选择了Use Player Settings，那么这个摄像机会使用 Project Settings 中

的设置；否则就会覆盖掉ProjectSettings中的设置。

在内置渲染管线中，**渲染路径主要分为以下三种**：

+ **前向渲染路径**（Forward Rendering Path）：默认的标准渲染方式，适用于相对简单的场景和较少的光源。
+ **延迟渲染路径**（Deferred Rendering Path）：可以处理较复杂的场景，有大量光源时可以提供更好的性能。
+ **顶点照明渲染路径**（Vertex Lit Rendering Path）：**已弃用**，适用于性能受限的场景。

{% note info %}
当显卡不支持当前选定的渲染路径时，将会自动使用低一级的渲染路径，例如，如果一个GPU不支持延迟渲染，那么Unity就会使用前向渲染。

{% endnote %}

### LightMode标签
`Tags{"LightMode"}`用于指明该`Pass`匹配的渲染路径，即告诉Unity的渲染管线当前`Pass`应该在哪个阶段被调用。**Shader中所使用的内置变量应与`LightMode`匹配**，Unity每个渲染阶段只会填充该阶段对应的内置变量。

如果`LightMode`错误，Unity将无法自动填充Shader中所使用的内置变量，例如`_LightColor0`；同时`LightMode`需要和摄像机的Rendering Path匹配，否则可能无法正常渲染，因为摄像机只会渲染Render Path所对应的`Pass`。

如果未设置`LightMode`，那么Unity将会认为该`Pass`使用顶点照明渲染路径，一些内置变量将不会被赋值，计算结果也可能出错。

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/63937386/1771925512691-a7d1f20a-0ed3-471a-8a59-15739d2f258a.png)

### 前向渲染路径
前向渲染路径有3种处理光照的方式：**逐顶点处理（中等质量光源）、逐像素处理（高质量光源）、球谐函数(Spherical Harmonics, SH)处理（低质量光源）。** 之所以需要这么分类，是因为如果场景中的逐像素光源数量很多，那么需要执行的`Pass`的数目也会很大，需要大量的性能。因此渲染引擎通常会限制每个物体的逐像素光照的数目。

在前向渲染中，当我们渲染一个物体时，如果Render Mode为Auto的话，Unity会根据场景中各个光源的设置以及这些光源对物体的影响程度（例如距离该物体的远近、光源强度等）对这些光源自动进行一个**重要度排序**。其中，一定数目的光源会按**逐像素**的方式处理，然后最多有**4个光源**按**逐顶点**的方式处理，**剩下的光源**可以**按SH方式处理**。Unity使用的重要性判断规则如下：

+ 场景中**最亮的平行光**总是按**逐像素**处理的。
+ 渲染模式被设置成 **Not Important** 的光源，会按**逐顶点或者SH处理**。
+ 渲染模式被设置成 **Important** 的光源，会按**逐像素**处理。
+ 如果根据以上规则得到的逐像素光源数量小于Quality Setting中的逐像素光源数量（**Pixel Light Count**)，会有更多的光源以逐像素的方式进行渲染。

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/63937386/1771932657010-f2b14fd5-8c5a-4505-bc02-1e51dd512117.png)<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/63937386/1771932674580-047c8eb6-c4d9-4fcb-a73a-77cc673a22d5.png)

前向渲染分为以下两种`Pass`进行光照计算：

#### 基础渲染通道 Base Pass
```c
Pass
{
    Tags{ "LightMode" = "ForwordBase" }
    #pragma multi_compile_fwdbase
    //...
}
```

基础渲染通道用于处理主要的光照效果，用于计算**逐像素的平行光**以及**所有逐顶点和SH光源**，实现**漫反射、高光反射、自发光、阴影、光照纹理**等效果。

+ `Base Pass`默认支持阴影

#### 附加渲染通道 Additional Pass
```c
Pass
{
    Tags{ "LightMode" = "ForwordAdd" }
    Blend One One
    #pragma multi_compile_fwdadd
    //...
}
```

{% note warning %}
`Blend`的作用是将当前`Pass`的颜色与颜色缓冲区中的颜色进行混合计算，在透明度混合时，颜色缓冲区中的颜色是半透明物体背后的片元的颜色，**附加渲染通道中颜色缓冲区的颜色是上一个`Pass`，也就是`Base Pass`所计算出的颜色，即将基础渲染通道和附加渲染通道的颜色进行混合。**

{% endnote %}

{% note info %}
`#pragma multi_compile_fwdbase`和`#pragma multi_compile_fwdadd`编译指令用于获取光照变量。

{% endnote %}

附加渲染通道用于处理一些附加的光照效果，主要用于计算**其他影响物体的逐像素光源**，这些光源每个都会执行一次该`Pass`，可用于实现**描边、轮廓、辉光**等。

+ `Additional Pass`默认**不支持阴影**，可以通过添加`#pragma multi_compile_fwdadd_fullshadows`开启阴影。

#### 前向渲染可使用的内置光照变量和函数
<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/63937386/1771934602939-fbf0d60f-b56b-49d1-a663-000aef9c2932.png)

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/63937386/1771934722093-657ac5b8-5fa4-4310-9cd1-1d01633d1773.png)

### 顶点照明渲染路径
顶点照明渲染路径顾名思义，它**只支持逐顶点光照**，而**不支持逐像素光照**，阴影、法线纹理、高精度高光反射等均无法实现，Unity只会填充逐顶点相关的光源变量，而不会填充逐像素光照变量。由于只使用逐顶点光照，因此顶点照明渲染路径**对硬件配置要求最少、运算性能最高、同时得到的效果最差。**

顶点照明渲染路径最多只会记录8个光源的数据，会根据光源类型、强度、距离等因素来决定。

+ **所有可以在顶点照明渲染路径中实现的功能都可以在前向渲染路径中完成**，因此顶点照明渲染路径已经被弃用（legacy）。

#### 顶点照明渲染路径可使用的内置变量和函数
<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/63937386/1771940854769-67c8ab2f-e782-4854-9505-38812b417d47.png)

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/63937386/1771940865437-432b9f8f-26fb-44c3-89e0-219c2e02f9d3.png)

### 延迟渲染路径
**前向渲染的问题**是，如果场景中有大量实时光源，那么该物体就需要执行多个`Pass`，每个`Pass`计算一个光照的结果，最后将这些光照结果通过颜色缓冲区进行混合。由于**每执行一个`Pass`就需要重新渲染一遍物体，这会导致大量的性能消耗，但是其中的很多运算都是重复的**，因此我们需要使用**延迟渲染路径**。

**延迟渲染路径对光源的数量没有限制**，并且所有灯光都**可以使用逐像素渲染**，它支持法线纹理、阴影等等效果的处理；但是它**不能处理半透明物体**，并且**不支持真正的抗锯齿**，这些**会自动使用前向渲染路径**。

延迟渲染通常只需要 **两个`Pass`** 即可完成物体的渲染：

首先，场景中的每个物体将会调用他们各自的`Shader Pass`，但是**不进行任何的光照计算**，只通过深度缓冲判断片元的可见性，如果该片元不可见就直接剔除，不再参与后续计算；**如果该片元可见**，我们就将它的**反照率、金属度、法线、自发光、深度**属性存储到**G缓冲区（G-buffer）**，其中G是英文Geometry的缩写；

所谓的G-Buffer实际上就是大小等于屏幕空间的`Render Texture`；

在第二个`Pass`中，我们根据G缓冲区中的片元信息**进行真正的光照计算**，同时通常只能使用Unity内置的Standard光照模型。但是我们并不需要重新渲染一遍每个物体：我们会直接从G-Buffer中的`Render Texture`中获取信息，将平行光直接绘制在屏幕正前方的一块2D几何体中；Unity会对剩下的点光源分别绘制一个3D的球体，半径为点光源的衰减半径，然后将他投影到屏幕空间中，根据深度图计算顶点是否位于球体范围内，然后根据其他G-Buffer信息计算光照颜色；聚光灯则是使用3D椎体；然后各个光源的结果在帧缓冲里叠加，**不再需要进行顶点变换、遮挡剔除等重复操作，因此效率极高。**

由此可见，**延迟渲染将场景的复杂度和屏幕空间大小解耦，计算复杂度为O(n+n)**。

#### 延迟渲染路径可使用的内置变量和函数
<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/63937386/1771945240517-ca3880d0-16db-49a3-ace6-8bcc6b98b4ac.png)

## 光源类型
### 如何在Shader中判断光源类型
+ `_DIRECTIONAL_LIGHT`：平行光；
+ `_POINT_LIGHT`：点光源；
+ `_SPOT_LIGHT`：聚光灯。

```c
#ifdef USING_DIRECTIONAL_LIGHT
    //平行光逻辑
#elif defined(POINT)
    //点光源逻辑
#elif defined(SPOT)
    //聚光灯逻辑
#else
    //其他逻辑
#endif
```

## 光照衰减
光照衰减通常指的是在渲染过程中考虑光线在空间中传播时的减弱效应，即光照亮度随着物体离光源的距离增加而衰减。常见的光照衰减计算方式有：

+ **线性衰减：** 光照衰减与光源到物体的距离成正比；
+ **平方衰减：**光照衰减与光源到物体的距离的平方成正比，这**更加符合现实世界中光照的特性**。

### Unity Shader中的光照衰减
Unity**内置管线**中为了提升性能，**一般不会直接通过数学公式计算光照衰减**，而是使用一张纹理作为**查找表**（LUT，Lookup Table），该纹理中存储了衰减值相关的数据，我们通过在片元着色器中对其采样来计算逐像素光照的衰减。

该查找表对应Unity Shader中的内置纹理变量`_LightTexture0`（如果光源存在灯光遮罩`cookie`，则对应内置变量`_LightTextureB0`），Unity会预先计算相关衰减数据并存入到该纹理中，以此来**避免重复计算，提升性能表现。** 其对角线上的纹理颜色值，表明了光源空间中不同位置的点对应的衰减值：

+ **起点**$(0,0)$表示**和光源重合**的点的衰减值（**0**）；
+ **终点**$(1,1)$表示在光源空间中**离光源距离最远**的点的衰减值（**1**）。

我们首先对`_LightTexture0`进行采样，然后使用`UNITY_ATTEN_CHANNEL`来获得衰减值所在分量，因为项目设置不同，纹理的压缩方式也不同，所存储的分量也不同，因此我们需要使用`UNITY_ATTEN_CHANNEL`宏。

```c
tex2D(_LightTexture0, uv).UNITY_ATTEN_CHANNEL;
```

#### 光源空间变换矩阵
由于`_LightTexture0`纹理中存放的衰减数据是在光源空间中的，即坐标原点为光源位置，因此我们需要使用Unity自带的光源空间变换矩阵`unity_WorldToLight`（老版本为`_LightMatrix0`），将顶点坐标从世界空间转换到光源空间中。

```c
mul(unity_WorldToLight, float4(worldPos, 1));	//注意unity_WorldToLight是一个4x4的矩阵
```

{% note warning %}
**光源空间变换矩阵**实际上是一个**透视投影变换矩阵**，**和摄像机的投影矩阵原理相同**，因为我们同样可以把光源看做摄像机。

{% endnote %}

### 点光源衰减计算
点光源无需使用光源遮罩`cookie`，因此我们可以直接使用`_LightTexture0`，我们已经知道了如何从该纹理中提取衰减值，但是我们还需要求出对该纹理采样时的uv坐标，由于`_LightTexture0`中的数据存放在光源空间中，因此uv坐标同样需要转换进光源空间，由此可得：

```c
float3 lightCoord = mul(unity_WorldToLight, float4(WorldPos, 1)).xyz;
```

`lightCoord`指的是顶点在光源空间中经过“**规范化**”后的坐标，规范化指的是将`lightCoord`的模长，即顶点与光源位置（原点）的距离重映射到$[0,1]$区间：若顶点正好位于光源位置（原点），则`LightCoord`模长为0；若顶点位于光源半径的边缘，其模长为1。

我们在8.3的开头提到过，现实世界中光照的衰减特性更符合平方衰减，即**光照衰减与距离的平方成正比**，为了**构造距离的平方**，我们使用如下方式：

```c
fixed atten = tex2D(_LightTexture0, dot(lightCoord, lightCoord).xx).UNITY_ATTEN_CHANNEL;
```

`dot(lightCoord, LightCoord)`是通过点乘得到模长，即$x^2 + y^2 + z^2 = \text{distance}^2$，`.xx`是为了构造`float2`uv坐标，即$(\text{distance}^2, \text{distance}^2)$。衰减值在原点$(0,0)$时为0，在光照边缘$(1,1)$时为1，满足衰减值和距离的平方成正比。

### 聚光灯衰减计算
为了模拟聚光灯的区域性，Unity将会默认为聚光灯提供`cookie`，因此聚光灯的光照纹理`_LightTexture0`中存储的是`cookie`的遮罩范围纹理信息，`_LightTextureB0`中存储的才是衰减值。

之所以需要使用`_LightTexture0`和`_LightTextureB0`，是因为聚光灯的衰减体现在两个方向上：聚光灯的朝向为光源空间的$z$轴，$z$值越大，距离光源中心越远，衰减值越大；同时，$xy$坐标的绝对值越大，代表顶点距离$z$轴中心越远，在光源的横截面方向上同样需要衰减，距离$z$轴中心越远，衰减值越大。前者的衰减值存储在`_LightTextureB0`中，后者的衰减值存储在`_LightTexture0`中。

聚光灯的衰减计算如下：

<!-- 这是一张图片，ocr 内容为： -->
![聚光灯Cookie纹理](https://cdn.nlark.com/yuque/0/2026/png/63937386/1772008223864-c9ab28cd-dbd4-40bd-a978-a80575ca0982.png)

```c
float4 lightCoord = mul(unity_WorldToLight, float4(i.WorldPos, 1));

fixed atten = (lightCoord.z > 0) * 	//第一步
                tex2D(_LightTexture0, lightCoord.xy / lightCoord.w + 0.5).w *	//第二步
                tex2D(_LightTextureB0, dot(lightCoord.xyz, lightCoord.xyz).rr).UNITY_ATTEN_CHANNEL;	//第三步
```

+ `lightCoord`在此处为`float4`类型，因为我们需要`w`参与后续的透视计算；
+ `lightCoord.z > 0`用来判断聚光灯是否朝向该顶点；

{% note warning %}
点光源无需这一步，因为点光源的光线向四周发散，而聚光灯的光线仅朝向$z$轴。

{% endnote %}

{% note warning %}
+ `tex2D(_LightTexture0, lightCoord.xy / lightCoord.w + 0.5).w`：`_LightTexture0`纹理可以看做位于$z=1$处的圆锥横截面，**类似于透视裁剪空间变换**，我们需要将空间中的顶点位置映射到这张纹理上，**通过顶点在纹理中的位置获取顶点在**$xy$**方向上的衰减值**。`lightCoord.w`代表顶点在光源空间中的$z$值，根据**相似三角形**可得（坐标$y$同理）：

$\frac{\text{点在纹理上的偏移 } x'}{\text{纹理的深度 } 1} = \frac{\text{点在空间中的偏移 } x}{\text{点的深度 } w}$

由此可得$x' = \frac{x}{w}$

显然，这样获得的顶点在纹理上的偏移$x'$和$y'$是**以纹理中心**$(0.5, 0.5)$**作为坐标原点**的，而**纹理原点实际上位于坐标左下角**，因此我们**需要将**$x'$**和**$y'$**向左下平移**，得到`lightCoord.xy / lightCoord.w + 0.5`。此处计算有部分简化，详细见[此处链接](https://blog.csdn.net/Jaihk662/article/details/112202944)

同时`_LightTexture0`的衰减信息存放在`.w`通道中。

{% endnote %}

+ `tex2D(_LightTextureB0, dot(lightCoord.xyz, lightCoord.xyz).rr).UNITY_ATTEN_CHANNEL`：需要注意由于`lightCoord`为`float4`类型，而我们只需要`.xyz`坐标即可。`.rr`和`.xx`用法相同。

### 光源衰减综合实现
```c
Shader "Unlit/ForwardRendering"
{
    Properties
    {
        _DiffuseColor ("DiffuseColor", Color) = (1,1,1,1)
        _SpecularColor("SpecularColor", Color) = (1,1,1,1)
        _Gloss("Gloss", Range(8, 256)) = 16
    }
    SubShader
    {
        Pass
        {
            Tags { "LightMode"="ForwardBase" }

            CGPROGRAM
            #pragma vertex vert
            #pragma fragment frag

            #include "UnityCG.cginc"
            #include "Lighting.cginc"

            struct v2f
            {
                float3 worldPos : TEXCOORD0;
                float3 worldNormal : NORMAL;
                float4 vertex : SV_POSITION;
            };

            fixed4 _DiffuseColor;
            fixed4 _SpecularColor;
            float _Gloss;

            v2f vert (appdata_full v)
            {
                v2f o;
                o.vertex = UnityObjectToClipPos(v.vertex);
                o.worldNormal = UnityObjectToWorldNormal(v.normal);
                o.worldPos = mul(unity_ObjectToWorld, v.vertex);
                return o;
            }

            fixed4 frag (v2f i) : SV_Target
            {
                float3 WorldNormal = normalize(i.worldNormal);
                float3 viewDir = normalize(UnityWorldSpaceViewDir(i.worldPos));

                float3 lightDir = normalize(UnityWorldSpaceLightDir(i.worldPos));

                fixed3 diffuseColor = _LightColor0.rgb * _DiffuseColor.rgb * max(0, dot(lightDir, WorldNormal));

                float3 halfDir = normalize(lightDir + viewDir);
                fixed3 specularColor = _LightColor0.rgb * _SpecularColor.rgb * pow(max(0, dot(WorldNormal, halfDir)), _Gloss);

                fixed3 color = UNITY_LIGHTMODEL_AMBIENT.rgb + diffuseColor + specularColor;
                return fixed4(color, 1);
            }
            ENDCG
        }
        Pass
        {
            Tags { "LightMode"="ForwardAdd" }

            Blend One One

            CGPROGRAM
            #pragma vertex vert
            #pragma fragment frag
            #pragma multi_compile_fwdadd

            #include "UnityCG.cginc"
            #include "Lighting.cginc"
            #include "AutoLight.cginc"

            struct v2f
            {
                float3 worldPos : TEXCOORD0;
                float3 worldNormal : NORMAL;
                float4 vertex : SV_POSITION;
            };

            fixed4 _DiffuseColor;
            fixed4 _SpecularColor;
            float _Gloss;

            v2f vert (appdata_full v)
            {
                v2f o;
                o.vertex = UnityObjectToClipPos(v.vertex);
                o.worldNormal = UnityObjectToWorldNormal(v.normal);
                o.worldPos = mul(unity_ObjectToWorld, v.vertex);
                return o;
            }

            fixed4 frag (v2f i) : SV_Target
            {
                float3 WorldNormal = normalize(i.worldNormal);
                float3 viewDir = normalize(UnityWorldSpaceViewDir(i.worldPos));

                #ifdef USING_DIRECTIONAL_LIGHT
                    float3 lightDir = normalize(UnityWorldSpaceLightDir(i.worldPos));
                #else
                    float3 lightDir = normalize(_WorldSpaceLightPos0.xyz - i.worldPos);
                #endif

                fixed3 diffuseColor = _LightColor0.rgb * _DiffuseColor.rgb * max(0, dot(lightDir, WorldNormal));

                float3 halfDir = normalize(lightDir + viewDir);
                fixed3 specularColor = _LightColor0.rgb * _SpecularColor.rgb * pow(max(0, dot(WorldNormal, halfDir)), _Gloss);

                #ifdef USING_DIRECTIONAL_LIGHT
                    fixed atten = 1;
                #else
                    #if defined(POINT)
                        float3 lightCoord = mul(unity_WorldToLight, float4(i.worldPos, 1));
                        fixed atten = tex2D(_LightTexture0, dot(lightCoord, lightCoord).xx).UNITY_ATTEN_CHANNEL;
                    #elif defined(SPOT)
                        float4 lightCoord = mul(unity_WorldToLight, float4(i.worldPos, 1));
                        fixed atten = (lightCoord.z > 0) * tex2D(_LightTexture0, lightCoord.xy / lightCoord.w + 0.5).w *
                                                           tex2D(_LightTextureB0, dot(lightCoord, lightCoord).xx).UNITY_ATTEN_CHANNEL;
                    #else
                        fixed atten = 1;
                    #endif
                #endif
                return fixed4((diffuseColor + specularColor) * atten, 1);
            }
            ENDCG
        }
    }
}

```

## 阴影
### Shadow Mapping
**Shadow Mapping技术**简单来说，就是**将摄像机放在和光源重合的位置上**，**记录从该摄像机（光源）出发能够看见的场景中距离最近的表面的位置（深度信息）**，显然该光源的阴影区域就是摄像机看不见的地方，因此这一步和深度测试类似，我们使用一个`LightMode`标签为`ShadowCaster`的`Pass`来将顶点从世界空间变换到光源空间中，寻找距离最近的顶点的深度信息，并**将深度信息存放至一张阴影映射纹理中（深度纹理）**，深度值将会被规范化到$[0,1]$区间，0最近，在RGB中为黑色，1最远，用白色表示。

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/63937386/1772032267711-df811e18-0fcc-4cb9-98f3-31dedd3e16a2.png)

**在正常渲染的`Pass`中**，我们首先也要**将顶点从世界空间变换到光源空间中**，并使用**该顶点的`xy`分量在阴影映射纹理中进行采样**，获取该`xy`坐标对应的最小深度值，并与该顶点的深度值进行比较，**如果该顶点的深度值大于阴影映射纹理的深度值（通常由`z`分量得到），那么该顶点就位于阴影中。**

### Screenspace Shadow Map
**屏幕空间的阴影映射技术（Screenspace Shadow Map）** 是基于 Shadow Mapping 的改进。Shadow Mapping 的缺点在于，它在正常渲染的`Pass`中进行阴影的运算，但是当场景中有物体相互重叠时，Early-Z 无法生效，依然需要依赖于片元着色器之后的深度测试进行片元剔除（见4.3.2.4），这也意味着我们会对需要被剔除的片元进行阴影运算（深度比较），导致 Overdraw。

因此，Screenspace Shadow Map引入了**阴影图**来避免多余的深度比较运算，Unity还是会调用`LightMode`为`ShadowCaster`的`Pass`来生成阴影映射纹理，同时还会生成一张以“玩家”摄像机视角（不是光源视角）的深度纹理图（**Z-Prepass技术**），记录场景中最近的片元深度，并通过阴影映射纹理和深度纹理合成阴影图（Unity自动调用内部`Pass`执行）：即如果摄像机的深度纹理图中的片元转换到光源空间中的深度大于阴影映射纹理图中的深度，那么这个片元就是可见且位于阴影中的，**阴影图包含了屏幕空间中所有可见的阴影区域**，因此当我们需要渲染阴影时，只要将待判断的顶点坐标在顶点着色器中从模型空间变换到屏幕空间中，然后在片元着色器中使用变换后的坐标对阴影图采样，即可判断该顶点是否位于阴影中。

### 开启阴影投射和阴影接收
Unity中可以通过设置`Mesh Renderer`组件中的`Cast Shadows`和`Receive Shadows`属性来开启和关闭阴影投射和阴影接收：

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/63937386/1772094823098-e93c5f43-7b58-457f-be40-8d95f71a7480.png)

开启阴影投射`Cast Shadows`后，Unity就会将该物体加入光源的阴影映射纹理的计算中，同时，我们还需要前文所提到的`LightMode`标签为`ShadowCaster`的`Pass`来获得阴影映射纹理：

```c
Pass {
    Name "ShadowCaster"
    Tags { "LightMode" = "ShadowCaster" }

    CGPROGRAM
    #pragma vertex vert
    #pragma fragment frag
        //
    #pragma multi_compile_shadowcaster
    #include "UnityCG.cginc"

    struct v2f {
        V2F_SHADOW_CASTER;
    };

    v2f vert(appdata_base v)
    {
        v2f o;
        TRANSFER_SHADOW_CASTER_NORMALOFFSET(o)
        return o;
    }

    float4 frag(v2f i) : SV_Target
    {
        SHADOW_CASTER_FRAGMENT(i)
    }
    ENDCG
}
```

+ `V2F_SHADOW_CASTER`：定义了一系列用于向片元着色器传递阴影投射顶点的相关变量；
+ `TRANSFER_SHADOW_CASTER_NORMALOFFSET(o)`：将顶点从模型空间转换到裁剪空间；考虑法线偏移以减轻阴影失真；
+ `SHADOW_CASTER_FRAGMENT(i)`：将深度值写入阴影映射纹理；
+ `#pragma multi_compile_shadowcaster`：存储了上述阴影计算相关的宏。

{% note warning %}
阴影投射的相关代码建议直接使用`Fallback`调用，**无需手动实现`ShadowCaster Pass`**。

{% endnote %}

```c
Shader "Notes/SimpleShadowReceiver"
{
    Properties {
        _Color ("Main Color", Color) = (1,1,1,1)
    }
    SubShader
    {
        Pass
        {
            // 1. 必须设置正确的 LightMode
            Tags { "LightMode" = "ForwardBase" }

            CGPROGRAM
            #pragma vertex vert
            #pragma fragment frag
            
            // 关键：这条指令会让 Unity 编译出处理阴影所需的多个变体
            #pragma multi_compile_fwdbase

            #include "UnityCG.cginc"
            #include "Lighting.cginc"
            // 2. 包含图片中提到的内置文件
            #include "AutoLight.cginc"

            struct v2f {
                float4 pos : SV_POSITION;
                // 3. 声明阴影坐标变量，参数是下一个可用的插值寄存器索引
                SHADOW_COORDS(0)
            };

            v2f vert (appdata_base v) {
                v2f o;
                o.pos = UnityObjectToClipPos(v.vertex);
                
                // 4. 在顶点着色器中计算并传递阴影坐标数据
                TRANSFER_SHADOW(o);
                
                return o;
            }

            fixed4 frag (v2f i) : SV_Target {
                // 5. 在片元着色器中采样阴影贴图并计算衰减值
                // shadow 为 0 表示在阴影中（黑），为 1 表示不在阴影中
                fixed shadow = SHADOW_ATTENUATION(i);

                // 简单的可视化：将阴影衰减应用到颜色上
                return fixed4(_Color.rgb * shadow, 1.0);
            }
            ENDCG
        }
    }
    // 6. 必须有 Fallback，否则物体无法产生阴影投影（ShadowCaster）
    FallBack "Specular"
}
```

+ `SHADOW_COORDS()`：声明了一个用于对阴影纹理进行采样的坐标；传入的参数是下一个可用的插值寄存器`TEXCOORD`的索引值；
+ `TRANSFER_SHADOW()`：该宏会**自动判断应该使用SM还是SSSM技术**，并**将顶点从模型空间转换到光源空间或屏幕空间（取决于使用哪种阴影投射技术）**，并存入上一个宏中定义的变量，同时该宏会在内部使用传入顶点着色器的结构体和顶点着色器的返回结构体，**前一个结构体（`appdata_base`）中顶点的命名必须是`vertex`；后一个结构体（`v2f`）顶点位置命名必须是`pos`；**
+ `SHADOW_ATTENUATION()`：该宏在片元着色器中使用，会根据传入的顶点着色器的返回结构体`v2f`中的阴影纹理坐标变量对阴影映射纹理或阴影图进行采样，并将采样得到的深度值和片元的深度值进行比较，计算出一个`fixed3`类型的阴影衰减值，最后将衰减值和（漫反射 + 高光反射）的结果相乘即可。

{% note info %}
这个`Shader`只对基础渲染通道`Base Pass`进行了阴影计算，即只计算了最亮的逐像素平行光和其他的逐顶点和SH光源，为了得到完整的渲染结果，我们还需要对`Additional Pass`进行阴影计算。

{% endnote %}

### 光照衰减和阴影综合实现
#### 不透明物体
`AutoLight.cginc`中的`UNITY_LIGHT_ATTENUATION`宏将会统一计算光照衰减和阴影衰减`SHADOW_ATTENUATION()`，该宏需要传入三个参数：

```c
UNITY_LIGHT_ATTENUATION(atten, i, i.worldPos);
```

**第一个参数我们不需要声明**，`UNITY_LIGHT_ATTENUATION`会自动帮我们声明，并将光照衰减值和阴影衰减值相乘后存储在`atten`中；后续两个参数是顶点着色器返回的结构体和世界坐标，用来计算光源空间下的坐标。

`UNITY_LIGHT_ATTENUATION`会自动判断光源类型、是否使用`cookie`等，因此我们完全无需手动计算光照衰减和阴影衰减。

```c
Shader "Unlit/Shadow"
{
    Properties
    {
        _DiffuseColor ("DiffuseColor", Color) = (1,1,1,1)
        _SpecularColor("SpecularColor", Color) = (1,1,1,1)
        _Gloss("Gloss", Range(8, 256)) = 16
    }
    SubShader
    {
        Pass
        {
            Tags { "LightMode"="ForwardBase" }

            CGPROGRAM
            #pragma vertex vert
            #pragma fragment frag
            #pragma multi_compile_fwdbase

            #include "UnityCG.cginc"
            #include "Lighting.cginc"
            #include "AutoLight.cginc"

            struct v2f
            {
                float3 worldPos : TEXCOORD0;
                float3 worldNormal : NORMAL;
                float4 pos : SV_POSITION;
                SHADOW_COORDS(1)
            };

            fixed4 _DiffuseColor;
            fixed4 _SpecularColor;
            float _Gloss;

            v2f vert (appdata_full v)
            {
                v2f o;
                o.pos = UnityObjectToClipPos(v.vertex);
                o.worldNormal = UnityObjectToWorldNormal(v.normal);
                o.worldPos = mul(unity_ObjectToWorld, v.vertex);
                TRANSFER_SHADOW(o);
                return o;
            }

            fixed4 frag (v2f i) : SV_Target
            {
                float3 WorldNormal = normalize(i.worldNormal);
                float3 viewDir = normalize(UnityWorldSpaceViewDir(i.worldPos));

                float3 lightDir = normalize(UnityWorldSpaceLightDir(i.worldPos));

                fixed3 diffuseColor = _LightColor0.rgb * _DiffuseColor.rgb * max(0, dot(lightDir, WorldNormal));

                float3 halfDir = normalize(lightDir + viewDir);
                fixed3 specularColor = _LightColor0.rgb * _SpecularColor.rgb * pow(max(0, dot(WorldNormal, halfDir)), _Gloss);

                UNITY_LIGHT_ATTENUATION(atten, i, i.worldPos);

                fixed3 color = UNITY_LIGHTMODEL_AMBIENT.rgb + (diffuseColor + specularColor) * atten;
                return fixed4(color, 1);
            }
            ENDCG
        }
        Pass
        {
            Tags { "LightMode"="ForwardAdd" }

            Blend One One

            CGPROGRAM
            #pragma vertex vert
            #pragma fragment frag

            //添加如下编译指令来生成点光源和聚光灯的阴影Shader变体
            #pragma multi_compile_fwdadd_fullshadows

            #include "UnityCG.cginc"
            #include "Lighting.cginc"
            #include "AutoLight.cginc"

            struct v2f
            {
                float3 worldPos : TEXCOORD0;
                float3 worldNormal : NORMAL;
                float4 pos : SV_POSITION;
                SHADOW_COORDS(1)
            };

            fixed4 _DiffuseColor;
            fixed4 _SpecularColor;
            float _Gloss;

            v2f vert (appdata_full v)
            {
                v2f o;
                o.pos = UnityObjectToClipPos(v.vertex);
                o.worldNormal = UnityObjectToWorldNormal(v.normal);
                o.worldPos = mul(unity_ObjectToWorld, v.vertex);
                TRANSFER_SHADOW(o)
                return o;
            }

            fixed4 frag (v2f i) : SV_Target
            {
                float3 WorldNormal = normalize(i.worldNormal);
                float3 viewDir = normalize(UnityWorldSpaceViewDir(i.worldPos));

                #ifdef USING_DIRECTIONAL_LIGHT
                    float3 lightDir = normalize(UnityWorldSpaceLightDir(i.worldPos));
                #else
                    float3 lightDir = normalize(_WorldSpaceLightPos0.xyz - i.worldPos);
                #endif

                fixed3 diffuseColor = _LightColor0.rgb * _DiffuseColor.rgb * max(0, dot(lightDir, WorldNormal));

                float3 halfDir = normalize(lightDir + viewDir);
                fixed3 specularColor = _LightColor0.rgb * _SpecularColor.rgb * pow(max(0, dot(WorldNormal, halfDir)), _Gloss);

                UNITY_LIGHT_ATTENUATION(atten, i, i.worldPos)

                return fixed4((diffuseColor + specularColor) * atten, 1);
            }
            ENDCG
        }
        
    }
    Fallback "Specular"
}

```

#### 透明度测试
相较于不透明的物体的`Shader`，我们只需要**修改`Fallback`的内置`Shader`即可**。同时需要注意，我们需要在自己的`Shader`中为调用的`Fallback Shader`声明变量名为`_Cutoff`的透明度阈值属性和`_Color`漫反射颜色属性。

```c
Shader "Unlit/AlphaTestWithShadow"
{
    Properties
    {
        _MainTex ("Texture", 2D) = "" {}
        _Color("DiffuseColor", Color) = (1,1,1,1)
        _SpecularColor("SpecularColor", Color) = (1,1,1,1)
        _Gloss("Gloss", Range(0, 20)) = 16

        _Cutoff("Cutoff", Range(0, 1)) = 0
    }
    SubShader
    {
        Tags{"Queue"="AlphaTest" "IgnoreProjector"="True" "RenderType"="TransparentCutout"}
        Pass
        {
            Cull Off

            Tags{"LightMode" = "ForwardBase"}

            CGPROGRAM
            #pragma vertex vert
            #pragma fragment frag
            #pragma multi_compile_fwdbase

            #include "UnityCG.cginc"
            #include "Lighting.cginc"
            #include "AutoLight.cginc"

            struct v2f
            {
                float2 uv : TEXCOORD0;
                float4 pos : SV_POSITION;
                float3 worldPos : TEXCOORD1;
                float3 worldNormal : NORMAL;
                SHADOW_COORDS(2)
            };

            sampler2D _MainTex;
            float4 _MainTex_ST;
            fixed4 _Color;
            fixed4 _SpecularColor;
            float _Gloss;

            fixed _Cutoff;

            v2f vert (appdata_base v)
            {
                v2f o;
                o.pos = UnityObjectToClipPos(v.vertex);
                o.uv = TRANSFORM_TEX(v.texcoord, _MainTex);

                o.worldNormal = UnityObjectToWorldNormal(v.normal);
                o.worldPos = mul(unity_ObjectToWorld, v.vertex);

                TRANSFER_SHADOW(o)
                return o;
            }

            fixed4 frag (v2f i) : SV_Target
            {
                clip(tex2D(_MainTex, i.uv).a - _Cutoff);

                fixed3 albedo = tex2D(_MainTex, i.uv).rgb * _Color.rgb;

                float3 WorldNormal = normalize(i.worldNormal);
                float3 lightDir = normalize(UnityWorldSpaceLightDir(i.worldPos));
                float3 viewDir = normalize(UnityWorldSpaceViewDir(i.worldPos));

                float3 halfDir = normalize(lightDir + viewDir);

                fixed3 diffuse = _LightColor0.rgb * albedo * max(0, dot(lightDir, WorldNormal));
                fixed3 specular = _LightColor0.rgb * _SpecularColor * pow(max(0, dot(halfDir, WorldNormal)), _Gloss);

                UNITY_LIGHT_ATTENUATION(atten, i, i.worldPos)
                fixed3 color = UNITY_LIGHTMODEL_AMBIENT.rgb * albedo + (diffuse + specular) * atten;

                return fixed4(color, 1);
            }
            ENDCG
        }
    }
    Fallback "Transparent/Cutout/VertexLit"
}
```

同时，由于`Fallback Shader`中的阴影相关`Pass`并没有关闭背面剔除，导致有很多片元未能加入阴影映射纹理的计算过程中，因此直接应用上述`Shader`得到的渲染结果是错误的。我们有两种解决办法：一是手写带有`Cull Off`的`LightMode`为`ShadowCaster`的`Pass`，或者我们可以直接**将物体设置为双面渲染**，即可**将背面也加入阴影映射纹理的计算中**。

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/63937386/1772172528284-830433c0-e564-455b-a193-fa2baeec1096.png)

#### 透明度混合
由于透明度混合需要**关闭深度写入**，这导致在计算阴影映射纹理时，我们无法从光源的视角出发直接判断出各半透明物体的遮挡关系，因此我们需要在光源空间中从后往前渲染半透明物体才能获得正确的阴影映射纹理，但是这样计算出的阴影缺乏真实感：我们无法判断光线经过了几层半透明物体，也不知道每层半透明物体吸收了过少光，折射角度是多少等等，这**会导致阴影计算变得非常复杂**，因此，Unity自带的**半透明物体的`Fallback Shader`并不会提供投射和接收阴影的`Pass`。**

如果想强制生成半透明物体的阴影，我们可以选择将`Fallback Shader`设置为不透明物体的`Shader`，使用不透明物体的阴影计算方式来强制生成，但是这样的效果很不真实。

```c
Shader "Unlit/AlphaBlendWithShadow"
{
    Properties
    {
        _MainTex ("Texture", 2D) = "" {}
        _DiffuseColor("DiffuseColor", Color) = (1,1,1,1)
        _SpecularColor("SpecularColor", Color) = (1,1,1,1)
        _Gloss("Gloss", Range(0, 20)) = 16

        _AlphaScale("AlphaScale", Range(0, 1)) = 1
    }
    SubShader
    {
        Tags { "Queue" = "Transparent" "IgnoreProjector" = "True" "RenderType" = "Transparent"}
        Pass
        {
            Cull Front

            Tags{"LightMode" = "ForwardBase"}

            ZWrite Off
            Blend SrcAlpha OneMinusSrcAlpha

            CGPROGRAM
            #pragma vertex vert
            #pragma fragment frag

            #include "UnityCG.cginc"
            #include "Lighting.cginc"

            struct v2f
            {
                float2 uv : TEXCOORD0;
                float4 vertex : SV_POSITION;
                float3 worldPos : TEXCOORD1;
                float3 worldNormal : NORMAL;
            };

            sampler2D _MainTex;
            float4 _MainTex_ST;
            fixed4 _DiffuseColor;
            fixed4 _SpecularColor;
            float _Gloss;

            fixed _AlphaScale;

            v2f vert (appdata_base v)
            {
                v2f o;
                o.vertex = UnityObjectToClipPos(v.vertex);
                o.uv = TRANSFORM_TEX(v.texcoord, _MainTex);

                o.worldNormal = UnityObjectToWorldNormal(v.normal);
                o.worldPos = mul(unity_ObjectToWorld, v.vertex);
                return o;
            }

            fixed4 frag (v2f i) : SV_Target
            {
                fixed4 texColor = tex2D(_MainTex, i.uv);
                fixed3 albedo = tex2D(_MainTex, i.uv).rgb * _DiffuseColor.rgb;

                float3 WorldNormal = normalize(i.worldNormal);
                float3 lightDir = normalize(UnityWorldSpaceLightDir(i.worldPos));
                float3 viewDir = normalize(UnityWorldSpaceViewDir(i.worldPos));

                float3 halfDir = normalize(lightDir + viewDir);

                fixed3 diffuse = _LightColor0.rgb * albedo * max(0, dot(lightDir, WorldNormal));
                fixed3 specular = _LightColor0.rgb * _SpecularColor * pow(max(0, dot(halfDir, WorldNormal)), _Gloss);
                fixed3 color = UNITY_LIGHTMODEL_AMBIENT.rgb * albedo + diffuse + specular;

                return fixed4(color.rgb, texColor.a * _AlphaScale);
            }
            ENDCG
        }
        Pass
        {
            Cull Back

            Tags{"LightMode" = "ForwardBase"}

            ZWrite Off
            Blend SrcAlpha OneMinusSrcAlpha

            CGPROGRAM
            #pragma vertex vert
            #pragma fragment frag

            #include "UnityCG.cginc"
            #include "Lighting.cginc"

            struct v2f
            {
                float2 uv : TEXCOORD0;
                float4 vertex : SV_POSITION;
                float3 worldPos : TEXCOORD1;
                float3 worldNormal : NORMAL;
            };

            sampler2D _MainTex;
            float4 _MainTex_ST;
            fixed4 _DiffuseColor;
            fixed4 _SpecularColor;
            float _Gloss;

            fixed _AlphaScale;

            v2f vert (appdata_base v)
            {
                v2f o;
                o.vertex = UnityObjectToClipPos(v.vertex);
                o.uv = TRANSFORM_TEX(v.texcoord, _MainTex);

                o.worldNormal = UnityObjectToWorldNormal(v.normal);
                o.worldPos = mul(unity_ObjectToWorld, v.vertex);
                return o;
            }

            fixed4 frag (v2f i) : SV_Target
            {
                fixed4 texColor = tex2D(_MainTex, i.uv);
                fixed3 albedo = tex2D(_MainTex, i.uv).rgb * _DiffuseColor.rgb;

                float3 WorldNormal = normalize(i.worldNormal);
                float3 lightDir = normalize(UnityWorldSpaceLightDir(i.worldPos));
                float3 viewDir = normalize(UnityWorldSpaceViewDir(i.worldPos));

                float3 halfDir = normalize(lightDir + viewDir);

                fixed3 diffuse = _LightColor0.rgb * albedo * max(0, dot(lightDir, WorldNormal));
                fixed3 specular = _LightColor0.rgb * _SpecularColor * pow(max(0, dot(halfDir, WorldNormal)), _Gloss);
                fixed3 color = UNITY_LIGHTMODEL_AMBIENT.rgb * albedo + diffuse + specular;

                return fixed4(color.rgb, texColor.a * _AlphaScale);
            }
            ENDCG
        }
    }
    Fallback "VertexLit"
}
```

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/63937386/1772175003878-8ab9a50d-3538-4c7b-aa99-41c19898810f.png)

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/63937386/1772175018682-a29c31a3-904d-4cdf-a4d3-dd6b9f4669b4.png)

# 标准Unity Shader
## 标准漫反射Shader - Phong光照模型
```c
Shader "Unlit/BumpedDiffuse"
{
    Properties
    {
        _MainTex ("Texture", 2D) = "white" {}
        _BumpMap("BumpMap", 2D) = "bump"{}
        _BumpScale("BumpScale", Range(0,1)) = 1
        _DiffuseColor("DiffuseColor", Color) = (1,1,1,1)
    }
    SubShader
    {
        Tags { "RenderType" = "Opaque" "Queue" = "Geometry"}
        Pass
        {
            Tags{"LightMode" = "ForwardBase"}

            CGPROGRAM
            #pragma vertex vert
            #pragma fragment frag
            #pragma multi_compile_fwdbase

            #include "UnityCG.cginc"
            #include "Lighting.cginc"
            #include "AutoLight.cginc"  

            struct v2f
            {
                float4 uv : TEXCOORD0;
                float4 pos : SV_POSITION;
                float3 worldPos : TEXCOORD1;
                float3x3 rotation : TEXCOORD2;
                SHADOW_COORDS(5)
            };

            sampler2D _MainTex;
            float4 _MainTex_ST;
            sampler2D _BumpMap;
            float4 _BumpMap_ST;
            float _BumpScale;
            fixed4 _DiffuseColor;

            v2f vert (appdata_full v)
            {
                v2f o;
                o.pos = UnityObjectToClipPos(v.vertex);
                o.uv.xy = TRANSFORM_TEX(v.texcoord, _MainTex);
                o.uv.zw = TRANSFORM_TEX(v.texcoord, _BumpMap);

                o.worldPos = mul(unity_ObjectToWorld, v.vertex);

                float3 worldNormal = UnityObjectToWorldNormal(v.normal);
                float3 worldTangent = UnityObjectToWorldDir(v.tangent);
                float3 worldBinormal = cross(normalize(worldTangent), normalize(worldNormal)) * v.tangent.w;

                o.rotation = float3x3(worldTangent.x, worldBinormal.x, worldNormal.x,
                                      worldTangent.y, worldBinormal.y, worldNormal.y,
                                      worldTangent.z, worldBinormal.z, worldNormal.z);

                TRANSFER_SHADOW(o)

                return o;
            }

            fixed4 frag (v2f i) : SV_Target
            {
                fixed3 lightDir = normalize(UnityWorldSpaceLightDir(i.worldPos));
                //fixed3 viewDir = normalize(UnityWorldSpaceViewDir(i.worldPos));

                float4 packedNormal = tex2D(_BumpMap, i.uv.zw);
                float3 tangentNormal = UnpackNormal(packedNormal);
                tangentNormal.xy *= _BumpScale;
                tangentNormal.z = sqrt(1 - saturate(dot(tangentNormal.xy, tangentNormal.xy)));

                float3 worldTangentNormal = mul(i.rotation, tangentNormal);

                fixed3 albedo = tex2D(_MainTex, i.uv.xy) * _DiffuseColor.rgb;
                fixed3 diffuse = _LightColor0.rgb * albedo * max(0, dot(lightDir, worldTangentNormal));

                UNITY_LIGHT_ATTENUATION(atten, i, i.worldPos)

                fixed3 color = UNITY_LIGHTMODEL_AMBIENT.rgb * albedo + diffuse * atten;

                return fixed4(color, 1);
            }
            ENDCG
        }
        Pass
        {
            Tags{"LightMode" = "ForwardAdd"}

            Blend One One

            CGPROGRAM
            #pragma vertex vert
            #pragma fragment frag
            #pragma multi_compile_fwdadd_fullshadows

            #include "UnityCG.cginc"
            #include "Lighting.cginc"
            #include "AutoLight.cginc"  

            struct v2f
            {
                float4 uv : TEXCOORD0;
                float4 pos : SV_POSITION;
                float3 worldPos : TEXCOORD1;
                float3x3 rotation : TEXCOORD2;
                SHADOW_COORDS(5)
            };

            sampler2D _MainTex;
            float4 _MainTex_ST;
            sampler2D _BumpMap;
            float4 _BumpMap_ST;
            float _BumpScale;
            fixed4 _DiffuseColor;

            v2f vert (appdata_full v)
            {
                v2f o;
                o.pos = UnityObjectToClipPos(v.vertex);
                o.uv.xy = TRANSFORM_TEX(v.texcoord, _MainTex);
                o.uv.zw = TRANSFORM_TEX(v.texcoord, _BumpMap);

                o.worldPos = mul(unity_ObjectToWorld, v.vertex);

                float3 worldNormal = UnityObjectToWorldNormal(v.normal);
                float3 worldTangent = UnityObjectToWorldDir(v.tangent);
                float3 worldBinormal = cross(normalize(worldTangent), normalize(worldNormal)) * v.tangent.w;

                o.rotation = float3x3(worldTangent.x, worldBinormal.x, worldNormal.x,
                                      worldTangent.y, worldBinormal.y, worldNormal.y,
                                      worldTangent.z, worldBinormal.z, worldNormal.z);

                TRANSFER_SHADOW(o)

                return o;
            }

            fixed4 frag (v2f i) : SV_Target
            {
                fixed3 lightDir = normalize(UnityWorldSpaceLightDir(i.worldPos));
                //fixed3 viewDir = normalize(UnityWorldSpaceViewDir(i.worldPos));

                float4 packedNormal = tex2D(_BumpMap, i.uv.zw);
                float3 tangentNormal = UnpackNormal(packedNormal);
                tangentNormal.xy *= _BumpScale;
                tangentNormal.z = sqrt(1 - saturate(dot(tangentNormal.xy, tangentNormal.xy)));

                float3 worldTangentNormal = mul(i.rotation, tangentNormal);

                fixed3 albedo = tex2D(_MainTex, i.uv.xy) * _DiffuseColor.rgb;
                fixed3 diffuse = _LightColor0.rgb * albedo * max(0, dot(lightDir, worldTangentNormal));

                UNITY_LIGHT_ATTENUATION(atten, i, i.worldPos)

                fixed3 color = UNITY_LIGHTMODEL_AMBIENT.rgb * albedo + diffuse * atten;

                return fixed4(color, 1);
            }
            ENDCG
        }
    }
    Fallback "Diffuse"
}

```

## 标准高光反射Shader - Blinn-Phong光照模型
```c
Shader "Unlit/BumpedSpecular"
{
        Properties
    {
        _MainTex ("Texture", 2D) = "white" {}
        _BumpMap("BumpMap", 2D) = "bump"{}
        _BumpScale("BumpScale", Range(0,1)) = 1
        _DiffuseColor("DiffuseColor", Color) = (1,1,1,1)
        _SpecularColor("SpecularColor", Color) = (1,1,1,1)
        _Gloss("Gloss", Range(0,20)) = 16
    }
    SubShader
    {
        Tags{"RenderType" = "Opaque" "Queue" = "Geometry"}
        Pass
        {
            Tags{"LightMode" = "ForwardBase"}

            CGPROGRAM
            #pragma vertex vert
            #pragma fragment frag
            #pragma multi_compile_fwdbase

            #include "UnityCG.cginc"
            #include "Lighting.cginc"
            #include "AutoLight.cginc"

            struct v2f
            {
                float4 uv : TEXCOORD0;
                float4 pos : SV_POSITION;
                float3 worldPos : TEXCOORD1;
                float3x3 rotation : TEXCOORD2;
                SHADOW_COORDS(5)
            };

            sampler2D _MainTex;
            float4 _MainTex_ST;
            sampler2D _BumpMap;
            float4 _BumpMap_ST;
            float _BumpScale;
            fixed4 _DiffuseColor;
            fixed4 _SpecularColor;
            float _Gloss;

            v2f vert (appdata_full v)
            {
                v2f o;
                o.pos = UnityObjectToClipPos(v.vertex);
                o.uv.xy = TRANSFORM_TEX(v.texcoord, _MainTex);
                o.uv.zw = TRANSFORM_TEX(v.texcoord, _BumpMap);

                o.worldPos = mul(unity_ObjectToWorld, v.vertex);

                float3 worldNormal = UnityObjectToWorldNormal(v.normal);
                float3 worldTangent = UnityObjectToWorldDir(v.tangent);
                float3 worldBinormal = cross(normalize(worldTangent), normalize(worldNormal)) * v.tangent.w;

                o.rotation = float3x3(worldTangent.x, worldBinormal.x, worldNormal.x,
                                      worldTangent.y, worldBinormal.y, worldNormal.y,
                                      worldTangent.z, worldBinormal.z, worldNormal.z);

                TRANSFER_SHADOW(o)

                return o;
            }

            fixed4 frag (v2f i) : SV_Target
            {
                fixed3 lightDir = normalize(UnityWorldSpaceLightDir(i.worldPos));
                fixed3 viewDir = normalize(UnityWorldSpaceViewDir(i.worldPos));

                float4 packedNormal = tex2D(_BumpMap, i.uv.zw);
                float3 tangentNormal = UnpackNormal(packedNormal);
                tangentNormal.xy *= _BumpScale;
                tangentNormal.z = sqrt(1 - saturate(dot(tangentNormal.xy, tangentNormal.xy)));

                float3 worldTangentNormal = mul(i.rotation, tangentNormal);

                fixed3 albedo = tex2D(_MainTex, i.uv.xy) * _DiffuseColor.rgb;
                fixed3 diffuse = _LightColor0.rgb * albedo * max(0, dot(lightDir, worldTangentNormal));
                
                float3 halfDir = normalize(lightDir + viewDir);
                fixed3 specular = _LightColor0.rgb * _SpecularColor.rgb * pow(max(0, dot(halfDir, worldTangentNormal)), _Gloss);

                UNITY_LIGHT_ATTENUATION(atten, i, i.worldPos)

                fixed3 color = UNITY_LIGHTMODEL_AMBIENT.rgb * albedo + (diffuse + specular) * atten;

                return fixed4(color, 1);
            }
            ENDCG
        }
        Pass
        {
            Tags{"LightMode" = "ForwardAdd"}

            Blend One One

            CGPROGRAM
            #pragma vertex vert
            #pragma fragment frag
            #pragma multi_compile_fwdadd_fullshadows

            #include "UnityCG.cginc"
            #include "Lighting.cginc"
            #include "AutoLight.cginc"

            struct v2f
            {
                float4 uv : TEXCOORD0;
                float4 pos : SV_POSITION;
                float3 worldPos : TEXCOORD1;
                float3x3 rotation : TEXCOORD2;
                SHADOW_COORDS(5)
            };

            sampler2D _MainTex;
            float4 _MainTex_ST;
            sampler2D _BumpMap;
            float4 _BumpMap_ST;
            float _BumpScale;
            fixed4 _DiffuseColor;
            fixed4 _SpecularColor;
            float _Gloss;

            v2f vert (appdata_full v)
            {
                v2f o;
                o.pos = UnityObjectToClipPos(v.vertex);
                o.uv.xy = TRANSFORM_TEX(v.texcoord, _MainTex);
                o.uv.zw = TRANSFORM_TEX(v.texcoord, _BumpMap);

                o.worldPos = mul(unity_ObjectToWorld, v.vertex);

                float3 worldNormal = UnityObjectToWorldNormal(v.normal);
                float3 worldTangent = UnityObjectToWorldDir(v.tangent);
                float3 worldBinormal = cross(normalize(worldTangent), normalize(worldNormal)) * v.tangent.w;

                o.rotation = float3x3(worldTangent.x, worldBinormal.x, worldNormal.x,
                                      worldTangent.y, worldBinormal.y, worldNormal.y,
                                      worldTangent.z, worldBinormal.z, worldNormal.z);

                TRANSFER_SHADOW(o)

                return o;
            }

            fixed4 frag (v2f i) : SV_Target
            {
                fixed3 lightDir = normalize(UnityWorldSpaceLightDir(i.worldPos));
                fixed3 viewDir = normalize(UnityWorldSpaceViewDir(i.worldPos));

                float4 packedNormal = tex2D(_BumpMap, i.uv.zw);
                float3 tangentNormal = UnpackNormal(packedNormal);
                tangentNormal.xy *= _BumpScale;
                tangentNormal.z = sqrt(1 - saturate(dot(tangentNormal.xy, tangentNormal.xy)));

                float3 worldTangentNormal = mul(i.rotation, tangentNormal);

                fixed3 albedo = tex2D(_MainTex, i.uv.xy) * _DiffuseColor.rgb;
                fixed3 diffuse = _LightColor0.rgb * albedo * max(0, dot(lightDir, worldTangentNormal));
                
                float3 halfDir = normalize(lightDir + viewDir);
                fixed3 specular = _LightColor0.rgb * _SpecularColor.rgb * pow(max(0, dot(halfDir, worldTangentNormal)), _Gloss);

                UNITY_LIGHT_ATTENUATION(atten, i, i.worldPos)

                fixed3 color = UNITY_LIGHTMODEL_AMBIENT.rgb * albedo + (diffuse + specular) * atten;

                return fixed4(color, 1);
            }
            ENDCG
        }
    }
    Fallback "Specular"
}

```

# 立方体纹理
立方体纹理（Cubemap）是一种特殊的纹理类型，包含6个独立的二维纹理，分别对应一个立方体的六个面，常应用于**环境映射、天空盒、全景图**等。

+ **环境映射（Environment Mapping）：** 用立方体纹理存储周围环境的图像，并应用于某个物体来模拟反射周围环境的效果；
+ **天空盒（Skybox）：** 我们将天空盒图片使用立方体纹理进行存储，并将这六个面映射到一个立方体的内表面，即可模拟天空、远景等环境；

## 立方体纹理的采样
立方体纹理属于**三维纹理**，因此不能使用二维纹理的形式进行采样，我们需要**使用三维纹理坐标对立方体纹理进行采样**：该三维纹理坐标**表示一个三维的方向向量**，该向量从立方体的中心出发，**与立方体表面的交点即为采样的结果。**

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/63937386/1772178639613-949f1911-8547-4bc7-9097-f204dc860d5b.png)

## 立方体纹理的优缺点
:::color2
立方体纹理的**优点**在于：

+ **多用途：** 可以有效地模拟环境反射和全景效果，如反射、折射、天空盒、环境光照等；
+ **无缝连接：** 立方体纹理的六个面直接没有可见的接缝处，减少了视觉瑕疵；
+ **兼容性好：** 大多数现代图形硬件均支持立方体纹理。

:::

{% note danger %}
**缺点**在于：

+ **内存开销：** 一个立方体纹理需要六张2D纹理，且对图像的分辨率有较高的要求，内存占用高；
+ **透视变形：** 使用六个平面来近似球形环境，有时会出现透视变形的问题；
+ **通用性：** 当场景发生变化时，我们需要重新生成立方体纹理；
+ **凹面体：** 立方体纹理不能反射使用了该立方体纹理的物体本身，无法模拟多次反射的结果，因此我们应尽可能减少使用凹面体，因为凹面体会反射自身。

{% endnote %}

## 动态生成立方体纹理
天空盒的立方体纹理显然是提前制作好直接导入Unity的，而场景中具有反射属性的物体所需的立方体纹理自然是需要在场景中创建并生成的，否则物体在场景中的位置不同，所需的反射贴图也不同，因此我们需要在物体所在的位置上动态生成立方体纹理。

对于场景展示类的物体，我们不需要实时生成立方体纹理，只需要在编辑器中创建一次即可，因此我们结合Unity编辑器拓展`EditorWindow`和`Camera.RenderToCubemap()`方法来在对应位置生成立方体纹理。

```csharp
using System.Collections;
using System.Collections.Generic;
using UnityEditor;
using UnityEngine;

public class Lesson74_RenderToCubeMap : EditorWindow
{
    private GameObject obj;
    private Cubemap cubeMap;

    [MenuItem("立方体纹理动态生成/打开生成窗口")]
    static void OpenWindow()
    {
        Lesson74_RenderToCubeMap window = EditorWindow.GetWindow<Lesson74_RenderToCubeMap>("立方体纹理生成窗口");
        window.Show();
    }

    private void OnGUI()
    {
        GUILayout.Label("关联对应位置对象");
        //用于关联对象的控件
        obj = EditorGUILayout.ObjectField(obj, typeof(GameObject), true) as GameObject;
        GUILayout.Label("关联对应立方体纹理");
        //用于关联立方体纹理的控件
        cubeMap = EditorGUILayout.ObjectField(cubeMap, typeof(Cubemap), false) as Cubemap;
        //点击按钮后 就去执行生成逻辑
        if(GUILayout.Button("生成立方体纹理"))
        {
            if(obj == null || cubeMap == null)
            {
                EditorUtility.DisplayDialog("提醒", "请先关联对应对象和立方体贴图", "确认");
                return;
            }
            //动态的生成立方体纹理
            GameObject tmpObj = new GameObject("临时对象");
            tmpObj.transform.position = obj.transform.position;
            Camera camera = tmpObj.AddComponent<Camera>();
            //关键方法，可以马上生成6张2D纹理贴图 用于立方体纹理
            camera.RenderToCubemap(cubeMap);
            DestroyImmediate(tmpObj);	//Destroy会在下一帧删除
        }
    }
}
```

## 反射
**立方体纹理的六个平面上的2D纹理是朝向内部**的，因此如果我们需要使用立方体纹理来模拟物体的反射效果，我们只需要**使用视角向量作为入射光线的方向，计算出反射光线的方向，再使用该方向向量对立方体纹理采样**，即可获得反射的颜色。

{% note danger %}
立方体纹理的六个平面朝向内部，相当于将物体放置在立方体的中心，将立方体纹理看做天空盒，因此物体表面的反射效果实际上就是**将摄像机放在物体表面并看向反射光线的位置**。

{% endnote %}

```csharp
Shader "Unlit/Reflection"
{
    Properties
    {
        _Cube ("CubeMap", Cube) = "" {}
        _Reflectivity("Reflectivity", Range(0, 1)) = 1
    }
    SubShader
    {
        Tags { "RenderType"="Opaque" "Queue" = "Geometry"}

        Pass
        {
            Tags { "LightMode"="ForwardBase" }

            CGPROGRAM
            #pragma vertex vert
            #pragma fragment frag

            #include "UnityCG.cginc"
            #include "Lighting.cginc"

            struct v2f
            {
                float3 reflectDir : TEXCOORD0;
                float4 vertex : SV_POSITION;
            };

            samplerCUBE _Cube;
            fixed _Reflectivity;

            v2f vert (appdata_base v)
            {
                v2f o;
                o.vertex = UnityObjectToClipPos(v.vertex);
                float3 worldPos = mul(unity_ObjectToWorld, v.vertex);
                float3 worldNormal = UnityObjectToWorldNormal(v.normal);
                float3 viewDir = normalize( UnityWorldSpaceViewDir(worldPos));
                o.reflectDir = reflect(-viewDir, worldNormal);

                return o;
            }

            fixed4 frag (v2f i) : SV_Target
            {
                fixed4 cubeColor = texCUBE(_Cube, i.reflectDir);

                return cubeColor * _Reflectivity;
            }
            ENDCG
        }
    }
}
```

### 带有漫反射和阴影的反射效果
```csharp
Shader "Unlit/ReflectionWithDiffusion"
{
    Properties
    {
        _Color("Color", Color) = (1,1,1,1)
        _ReflectColor("ReflectColor", Color) = (1,1,1,1)
        _Cube ("CubeMap", Cube) = "" {}
        _Reflectivity("Reflectivity", Range(0, 1)) = 1
    }
    SubShader
    {
        Tags { "RenderType"="Opaque" "Queue" = "Geometry"}

        Pass
        {
            Tags { "LightMode"="ForwardBase" }

            CGPROGRAM
            #pragma vertex vert
            #pragma fragment frag
            #pragma multi_compile_fwdbase

            #include "UnityCG.cginc"
            #include "Lighting.cginc"
            #include "AutoLight.cginc"

            struct v2f
            {
                float3 reflectDir : TEXCOORD0;
                float3 worldNormal : NORMAL;
                float3 worldPos : TEXCOORD1;
                float4 pos : SV_POSITION;
                SHADOW_COORDS(2)
            };

            fixed4 _Color;
            fixed4 _ReflectColor;
            samplerCUBE _Cube;
            fixed _Reflectivity;

            v2f vert (appdata_base v)
            {
                v2f o;
                o.pos = UnityObjectToClipPos(v.vertex);
                o.worldPos = mul(unity_ObjectToWorld, v.vertex);
                o.worldNormal = UnityObjectToWorldNormal(v.normal);
                float3 viewDir = normalize( UnityWorldSpaceViewDir(o.worldPos));
                o.reflectDir = reflect(-viewDir, o.worldNormal);
                TRANSFER_SHADOW(o)
                return o;
            }

            fixed4 frag (v2f i) : SV_Target
            {
                float3 lightDir = normalize(UnityWorldSpaceLightDir(i.worldPos));
                float3 WorldNormal = normalize(i.worldNormal);
                fixed3 diffuseColor = _LightColor0.rgb * _Color.rgb * max(0, dot(lightDir, WorldNormal));

                fixed3 cubeColor = texCUBE(_Cube, i.reflectDir) * _ReflectColor.rgb;
                UNITY_LIGHT_ATTENUATION(atten, i, i.worldPos)

                fixed3 color = UNITY_LIGHTMODEL_AMBIENT.rgb + lerp(diffuseColor, cubeColor, _Reflectivity) * atten;
                return fixed4(color, 1);
            }
            ENDCG
        }
    }
    Fallback "Reflective/VertexLit"
}

```

## 折射
折射方向的计算可以使用**斯涅尔定律（Snell's Law）**：

$ \eta_1 \sin \theta_1 = \eta_2 \sin \theta_2
 $

其中$\eta_1$和$\eta_2$分别是两个介质的**折射率。**

通常来说，我们会**直接使用折射方向作为对立方体纹理采样的方向向量**，但是这并不符合物理规律，因为入射光线会在物体上表面发生一次折射，穿过物体后会在物体的下表面再发生一次折射，但是这样计算较为复杂，而且一次折射在视觉效果上已经足够优秀，因此**通常我们只模拟第一次折射**。

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/63937386/1772283241980-7f0b2325-1446-4266-b1ee-4210cd4d84b7.png)

```csharp
Shader "Unlit/Refraction"
{
    Properties
    {
        _RefractIn("RefractIn", Range(1, 2)) = 1
        _RefractOut("RefractOut", Range(1, 2)) = 1.3
        _Cube("Cube", Cube) = ""{}
        _RefractAmount("RefractAmount", Range(0, 1)) = 1
    }
    SubShader
    {
        Tags { "RenderType"="Opaque" "Queue" = "Geometry"}

        Pass
        {
            CGPROGRAM
            #pragma vertex vert
            #pragma fragment frag

            #include "UnityCG.cginc"

            struct v2f
            {
                float3 refractDir: TEXCOORD0;
                float4 pos : SV_POSITION;
            };

            float _RefractIn;
            float _RefractOut;
            samplerCUBE _Cube;
            fixed _RefractAmount;

            v2f vert (appdata_base v)
            {
                v2f o;
                o.pos = UnityObjectToClipPos(v.vertex);
                float3 worldNormal = UnityObjectToWorldNormal(v.normal);
                float3 worldPos = mul(unity_ObjectToWorld, v.vertex);
                float3 viewDir = normalize(UnityWorldSpaceViewDir(worldPos));
                o.refractDir = refract(-viewDir, worldNormal, _RefractIn / _RefractOut);

                return o;
            }

            fixed4 frag (v2f i) : SV_Target
            {
                fixed4 cubeColor = texCUBE(_Cube, i.refractDir) * _RefractAmount;
                return cubeColor;
            }
            ENDCG
        }
    }
}
```

+ `refract(-viewDir, worldNormal, _RefractIn / _RefractOut)`：`_RefractIn`为**入射介质**折射率，`_RefractOut`为**射入的介质**的折射率。

### 带有漫反射和阴影的折射效果
```csharp
Shader "Unlit/RefractionWithDiffusion"
{
    Properties
    {
        _RefractRatio("RefractRatio", Range(0.1, 1)) = 0.5
        _Cube("Cube", Cube) = ""{}
        _RefractAmount("RefractAmount", Range(0, 1)) = 1
        _Color("Color", Color) = (1,1,1,1)
        _RefractColor("RefractColor", Color) = (1,1,1,1)
    }
    SubShader
    {
        Tags { "RenderType"="Opaque" "Queue" = "Geometry"}

        Pass
        {
            Tags { "LightMode" = "ForwardBase" }
            CGPROGRAM
            #pragma vertex vert
            #pragma fragment frag
            #pragma multi_compile_fwdbase

            #include "UnityCG.cginc"
            #include "Lighting.cginc"
            #include "AutoLight.cginc"

            struct v2f
            {
                float3 refractDir: TEXCOORD0;
                float4 pos : SV_POSITION;
                float3 worldNormal : NORMAL;
                float3 worldPos :TEXCOORD1;
                SHADOW_COORDS(2)
            };

            float _RefractRatio;
            samplerCUBE _Cube;
            fixed _RefractAmount;
            fixed4 _Color;
            fixed4 _RefractColor;

            v2f vert (appdata_base v)
            {
                v2f o;
                o.pos = UnityObjectToClipPos(v.vertex);
                o.worldNormal = UnityObjectToWorldNormal(v.normal);
                o.worldPos = mul(unity_ObjectToWorld, v.vertex);
                TRANSFER_SHADOW(o)
                return o;
            }

            fixed4 frag (v2f i) : SV_Target
            {
                float3 WorldNormal = normalize(i.worldNormal);
                float3 viewDir = normalize(UnityWorldSpaceViewDir(i.worldPos));
                float3 lightDir = normalize(UnityWorldSpaceLightDir(i.worldPos));
                float3 refractDir = refract(-viewDir, WorldNormal, _RefractRatio);
                fixed3 cubeColor = texCUBE(_Cube, refractDir) * _RefractColor;

                fixed3 diffuseColor = _LightColor0.rgb * _Color.rgb * max(0, dot(WorldNormal, lightDir));

                UNITY_LIGHT_ATTENUATION(atten, i, i.worldPos)

                fixed3 color = UNITY_LIGHTMODEL_AMBIENT.rgb + lerp(diffuseColor, cubeColor, _RefractAmount) * atten;

                return fixed4(color, 1);
            }
            ENDCG
        }
    }
    Fallback "Reflective/VertexLit"
}

```

## 菲涅耳反射
在实际渲染中，我们通常会使用**菲涅尔反射**来控制反射程度。菲涅尔反射描述了一种光学现象，即光线在照射到物体表面时，一部分发生反射，一部分进入物体内部，发生折射或散射。被反射的光和入射光之间存在一定的比率关系，这个比率关系可以通过**菲涅耳等式**进行计算。

{% note info %}
一个经常使用的例子是，当你站在湖边，直接低头看脚边的水面时，你会发现水几乎是透明的，你可以直接看到水底的小鱼和石子：但是，当你抬头看远处的水面时，会发现几乎看不到水下的情景，而只能看到水面反射的环境。这就是所谓的菲涅耳效果。事实上，不仅仅是水、玻璃这样的反光物体具有菲涅耳效果，几乎任何物体都或多或少包含了菲涅耳效果，这是基于物理的渲染中非常重要的一项高光反射计算因子

{% endnote %}

我们通常**使用菲涅尔等式来计算菲涅尔反射，其效果比一般的反射更加真实**。视角方向越接近法线方向，物体表面的反射越弱，表面的颜色越接近物体自身的漫反射颜色（大部分光线都进入物体发生折射和散射）；视角越远离法线方向，物体表面的反射就越强，因此**菲涅尔反射会在物体的边缘产生较强的亮度与反射光**，能够勾勒出物体的轮廓（**菲涅尔边缘光**）。由于现实中的菲涅尔等式计算非常复杂，因此我们常使用两种菲涅尔近似等式来进行计算：

+ **Schlick菲涅尔近似等式：**

$F_{\text{schlick}}(\mathbf{v}, \mathbf{n}) = F_0 + (1 - F_0)(1 - \mathbf{v} \cdot \mathbf{n})^5$

其中，$F_0$是一个反射系数，用于控制菲涅耳反射的强度，$\mathbf{v}$是视角方向，$\mathbf{n}$是表面法线。

{% note info %}
当光线垂直入射某介质时，即入射角$\theta$为0度，此时$F_{\text{schlick}}(\mathbf{v}, \mathbf{n}) = F_0$，因此$\bf{{F_0}}$**表示垂直入射某介质时的反射率**，我们可以像折射率一样，通过**查阅对应材质的物体在现实世界中的反射率**，并将该反射率带入公式中计算即可。

{% endnote %}

```csharp
Shader "Unlit/Fresnel"
{
    Properties
    {
        _Cube ("CubeMap", Cube) = "" {}
        _FresnelScale("FresnelScale", Range(0, 1)) = 0.5
    }
    SubShader
    {
        Tags { "RenderType"="Opaque" "Queue" = "Geometry"}

        Pass
        {
            Tags { "LightMode"="ForwardBase" }

            CGPROGRAM
            #pragma vertex vert
            #pragma fragment frag

            #include "UnityCG.cginc"
            #include "Lighting.cginc"

            struct v2f
            {
                float3 reflectDir : TEXCOORD0;
                float4 pos : SV_POSITION;
                float3 worldNormal : NORMAL;
                float3 viewDir : TEXCOORD1;
            };

            samplerCUBE _Cube;
            fixed _FresnelScale;

            v2f vert (appdata_base v)
            {
                v2f o;
                o.pos = UnityObjectToClipPos(v.vertex);
                float3 worldPos = mul(unity_ObjectToWorld, v.vertex);
                o.worldNormal = UnityObjectToWorldNormal(v.normal);
                o.viewDir = normalize( UnityWorldSpaceViewDir(worldPos));
                o.reflectDir = reflect(-o.viewDir, o.worldNormal);

                return o;
            }

            fixed4 frag (v2f i) : SV_Target
            {
                float3 WorldNormal = normalize(i.worldNormal);
                float3 ViewDir = normalize(i.viewDir);
                fixed4 cubeColor = texCUBE(_Cube, i.reflectDir);
                
                fixed fresnel = _FresnelScale + (1 - _FresnelScale) * pow((1 - dot(WorldNormal, ViewDir)), 5);

                return cubeColor * fresnel;
            }
            ENDCG
        }
    }
}

```

```csharp
Shader "Unlit/FresnelWithDiffusion"
{
    Properties
    {
        _Color("Color", Color) = (1,1,1,1)
        _Cube ("CubeMap", Cube) = "" {}
        _FresnelScale("FresnelScale", Range(0, 1)) = 0.5
    }
    SubShader
    {
        Tags { "RenderType"="Opaque" "Queue" = "Geometry"}

        Pass
        {
            Tags { "LightMode"="ForwardBase" }

            CGPROGRAM
            #pragma vertex vert
            #pragma fragment frag
            #pragma multi_compile_fwdbase

            #include "UnityCG.cginc"
            #include "Lighting.cginc"
            #include "AutoLight.cginc"

            struct v2f
            {
                float3 reflectDir : TEXCOORD0;
                float3 worldNormal : NORMAL;
                float3 worldPos : TEXCOORD1;
                float3 viewDir : TEXCOORD2;
                float4 pos : SV_POSITION;
                
                SHADOW_COORDS(3)
            };

            fixed4 _Color;
            samplerCUBE _Cube;
            fixed _FresnelScale;

            v2f vert (appdata_base v)
            {
                v2f o;
                o.pos = UnityObjectToClipPos(v.vertex);
                o.worldPos = mul(unity_ObjectToWorld, v.vertex);
                o.worldNormal = UnityObjectToWorldNormal(v.normal);
                o.viewDir = normalize( UnityWorldSpaceViewDir(o.worldPos));
                o.reflectDir = reflect(-o.viewDir, o.worldNormal);
                TRANSFER_SHADOW(o)
                return o;
            }

            fixed4 frag (v2f i) : SV_Target
            {
                float3 ViewDir = normalize(i.viewDir);
                float3 lightDir = normalize(UnityWorldSpaceLightDir(i.worldPos));
                float3 WorldNormal = normalize(i.worldNormal);
                fixed3 diffuseColor = _LightColor0.rgb * _Color.rgb * max(0, dot(lightDir, WorldNormal));

                fixed3 cubeColor = texCUBE(_Cube, i.reflectDir);
                UNITY_LIGHT_ATTENUATION(atten, i, i.worldPos)

                fixed fresnel = _FresnelScale + (1 - _FresnelScale) * pow(1 - dot(WorldNormal, ViewDir), 5);

                fixed3 color = UNITY_LIGHTMODEL_AMBIENT.rgb + lerp(diffuseColor, cubeColor, saturate(fresnel)) * atten;

                return fixed4(color, 1);
            }
            ENDCG
        }

    }
    Fallback "Reflective/VertexLit"
}
```

+ **Empricial菲涅尔近似等式：**

$F_{\text{Empricial}}(\mathbf{v}, \mathbf{n}) = \max(0, \min(1, \text{bias} + \text{scale} \times (1 - \mathbf{v} \cdot \mathbf{n})^{\text{power}}))$

其中，$\text{bias、scale、power}$为控制项。

# 渲染纹理
摄像机除了可以将三维场景渲染到颜色缓冲，最终呈现到屏幕上以外，还可以将场景渲染到一个中间缓冲中，即**渲染目标纹理（Render Target Texture, RTT）**，除了可以设置摄像机的输出位置为渲染纹理以外，还可以通过代码创建并关联渲染纹理：

+ `GrabPass`：在`Unity Shader`中，我们可以在`Pass`渲染通道中使用`GrabPass`指令来捕获当前屏幕内容并将其保存为纹理，以便在后续的渲染过程中使用；
+ `OnRenderImage`：在继承了`MonoBehaviour`的脚本中，我们可以使用`OnRenderImage`来获取摄像机渲染完成的图像，该函数一般用于实现自定义的图像后处理效果，即将摄像机渲染完成的图像进行二次处理。

## 简易镜面效果
即**将摄像机渲染的画面渲染到渲染纹理中，再在`Shader`中将该渲染纹理左右翻转后渲染输出**即可。但是这种镜面效果较为简陋：**镜子的画面不会随着观察位置的变化而变化**。

```csharp
Shader "Unlit/Mirror"
{
    Properties
    {
        _MainTex ("Texture", 2D) = "" {}
    }
    SubShader
    {
        Pass
        {
            CGPROGRAM
            #pragma vertex vert
            #pragma fragment frag
            
            #include "UnityCG.cginc"

            sampler2D _MainTex;
            float4 _MainTex_ST;

            v2f_img vert (appdata_base v)
            {
                v2f_img o; 
                o.pos = UnityObjectToClipPos(v.vertex);
                //o.uv = TRANSFORM_TEX(v.uv, _MainTex);
                o.uv = v.texcoord.xy * _MainTex_ST.xy + _MainTex_ST.zw;
                o.uv.x = 1 - o.uv.x;
                return o;
            } 

            fixed4 frag (v2f_img i) : SV_Target
            {
                fixed4 col = tex2D(_MainTex, i.uv);

                return col;
            }
            ENDCG
        }
    }
    Fallback "Diffuse"
}

```

## 玻璃效果
如果只使用透明效果来实现玻璃的话并不够真实，因为现实中的玻璃不仅仅是透明的，还具有反射和折射等光学效果，因此我们将使用渲染纹理来制作玻璃效果。

当我们在`Shader`中定义了一个`GrabPass`后，Unity会把当前屏幕的图像绘制在一张纹理中，以便我们在后续的`Pass`中访问它。我们通常会使用`GrabPass`来实现诸如玻璃等透明材质的模拟，与使用简单的透明混合不同，使用`GrabPass`可以让我们对该物体后面的图像进行更复杂的处理，例如使用法线来模拟折射效果，而不再是简单的和原屏幕颜色进行混合。

我们需要在渲染玻璃效果之前先捕获当前屏幕的内容，所以我们需要保证玻璃对象能够滞后渲染，否则我们无法得到正确的“透过玻璃看到的图像”。因此，我们需要将`SubShader`中的**渲染队列`Queue`设置为`Transparent`，`RenderType`设置为`Opaque`**，即可保证玻璃对象和半透明物体一样在最后渲染，并保证着色器替换的正确性。

```csharp
Shader "Unlit/GlassRefraction"
{
    Properties
    {
        _MainTex("MainTex", 2D) = ""{}
        _Cube ("CubeMap", Cube) = "" {}
        _RefractAmount("RefractAmount", Range(0, 1)) = 1
    }
    SubShader
    {
        Tags { "RenderType"="Opaque" "Queue" = "Transparent"}

        //使用它来捕获当前屏幕内容 
        GrabPass{}

        Pass
        {
            Tags { "LightMode"="ForwardBase" }

            CGPROGRAM
            #pragma vertex vert
            #pragma fragment frag

            #include "UnityCG.cginc"
            #include "Lighting.cginc"

            struct v2f
            { 
                float3 reflectDir : TEXCOORD0;
                float4 vertex : SV_POSITION;
                float4 grabPos : TEXCOORD1;
                float2 uv : TEXCOORD2;
            };

            sampler2D _MainTex;
            float4 _MainTex_ST;
            samplerCUBE _Cube;
            fixed _RefractAmount;
            sampler2D _GrabTexture;

            v2f vert (appdata_base v)
            {
                v2f o;
                o.vertex = UnityObjectToClipPos(v.vertex);
                o.grabPos = ComputeScreenPos(o.vertex);
                o.uv = TRANSFORM_TEX(v.texcoord, _MainTex);

                float3 worldPos = mul(unity_ObjectToWorld, v.vertex);
                float3 worldNormal = UnityObjectToWorldNormal(v.normal);
                float3 viewDir = normalize( UnityWorldSpaceViewDir(worldPos));
                o.reflectDir = reflect(-viewDir, worldNormal);

                return o;
            }

            fixed4 frag (v2f i) : SV_Target
            {
                //将玻璃颜色和反射颜色进行叠加
                fixed4 reflectColor = texCUBE(_Cube, i.reflectDir) * tex2D(_MainTex, i.uv);

                float2 offset = 1 - _RefractAmount; 

                //自定义折射光线偏移效果
                i.grabPos.xy = i.grabPos.xy - offset * 0.1;

                //屏幕坐标转换到uv坐标系 透视除法
                fixed2 screenUV = i.grabPos.xy / i.grabPos.w;   
                fixed4 grabColor = tex2D(_GrabTexture, screenUV); 

                //将反射颜色和折射颜色进行叠加，使用_RefractAmount控制两者的比例
                fixed4 color =  reflectColor * (1 - _RefractAmount) + grabColor * _RefractAmount; 

                return color;
            }
            ENDCG
        }
    }
}

```

+ `GrabPass{}`：**大括号中为空，Unity会默认将抓取到的屏幕内容写入一个名为`_GrabTexture`的纹理变量中，我们需要在`Shader`中手动声明`sampler2D _GrabTexture`来使用抓取的渲染纹理；或者我们可以在大括号中写入自定义的变量名，例如`GrabPass{ "_RefractionTex" }`，然后声明对应名称的变量即可使用抓取的渲染纹理。**
+ `ComputeGrabScreenPos`：**该函数需要传入顶点的裁剪空间位置，返回值为`float4`类型：**

`.xy`表示屏幕空间的`xy`坐标，同时该函数会自动判断不同平台间的`y`轴方向差异，自动翻转`y`轴；

`z`值没有发生变化，依然是传入的裁剪空间坐标的`z`值，即裁剪空间中顶点的深度；

`w`的坐标等于观察空间中该点到相机平面的垂直距离，用于透视除法，即`xy`除以`w`后会映射到$[0,1]$的范围内，用于对`_GrabTexture`进行`uv`采样。

### 带法线纹理的玻璃效果
{% note warning %}
显然，如果玻璃表面的法线纹理偏移越大，光线透过玻璃的扭曲效果就越明显，而法线纹理的偏移体现在法线方向与切线空间的`z`轴方向之间的偏移（见6.4.2.2.1），因此，我们将**使用`tangent.xy`作为折射的偏移量，并引入`_Distortion`参数来调整偏移量的大小。**

但是由于我们需要将偏移量`offset`与`i.grabPos.xy`相加，而`i.grabPos.xy`还需要与`i.grabPos.w`作透视除法，如果玻璃距离摄像机很远，即`i,grabPos.w`很大，这时如果我们直接将`offset`与`i.grabPos.xy`相加后再除以`i,grabPos.w`，那么`offset`将会变得很小，导致折射效果变得很弱，因此我们先将`offset * i.grabPos.z`后再与`i.grabPos.xy`相加，然后再除以`i.grabPos.w`，这样距离因素就可以被`i.grabPos.z`抵消，以减小玻璃和摄像机之间的距离对玻璃的折射效果的影响。

由裁剪空间变换矩阵可以得到：$z = \frac{Far}{Far - Near} \cdot z_{view} - \frac{Far \cdot Near}{Far - Near}$，$w = z_{view}$，其中$z_{view}$物体在观察空间里的真实深度（距离相机的物理距离）。因此，当物体位于远裁剪平面，$z = w = Far$，此时`i.grabPos.z / i.grabPos.w = 1`，当物体位于近剪裁平面，$z = 0, w = Near$，此时`i.grabPos.z / i.grabPos.w = 0`，因此当摄像机和玻璃之间的距离变化时，玻璃的折射效果会发生变化，更加真实。

{% endnote %}

```csharp
Shader "Unlit/GlassRefractionWithNormal"
{
    Properties
    {
        _MainTex("MainTex", 2D) = ""{}
        _BumpMap("BumpMap", 2D) = ""{}
        _Cube ("CubeMap", Cube) = "" {}
        _RefractAmount("RefractAmount", Range(0, 1)) = 1

        //控制折射扭曲程度
        _Distortion("Distortion", Range(0, 10)) = 0
    }
    SubShader
    {
        Tags { "RenderType"="Opaque" "Queue" = "Transparent"}

        //使用它来捕获当前屏幕内容 
        GrabPass{}

        Pass
        {
            Tags { "LightMode"="ForwardBase" }

            CGPROGRAM
            #pragma vertex vert
            #pragma fragment frag

            #include "UnityCG.cginc"
            #include "Lighting.cginc"

            struct v2f
            { 
      
                float4 vertex : SV_POSITION;
                float4 grabPos : TEXCOORD1;
                float4 uv : TEXCOORD2;

                float4 TtoW0 : TEXCOORD3;
                float4 TtoW1 : TEXCOORD4;
                float4 TtoW2 : TEXCOORD5;
            };

            sampler2D _MainTex;
            float4 _MainTex_ST;
            samplerCUBE _Cube;
            fixed _RefractAmount;
            sampler2D _GrabTexture;

            sampler2D _BumpMap;
            float4 _BumpMap_ST;

            float _Distortion;

            v2f vert (appdata_full v)
            {
                v2f o;
                o.vertex = UnityObjectToClipPos(v.vertex);
                o.grabPos = ComputeScreenPos(o.vertex);
                o.uv.xy = TRANSFORM_TEX(v.texcoord, _MainTex);
                o.uv.zw = TRANSFORM_TEX(v.texcoord, _BumpMap);

                float3 worldPos = mul(unity_ObjectToWorld, v.vertex);
                float3 worldNormal = UnityObjectToWorldNormal(v.normal);
                float3 viewDir = normalize( UnityWorldSpaceViewDir(worldPos));

                float3 worldTangent = UnityObjectToWorldDir(v.tangent);
                float3 worldBinormal = cross(normalize(worldNormal), normalize(worldTangent)) * v.tangent.w;

                o.TtoW0 = float4(worldTangent.x, worldBinormal.x, worldNormal.x, worldPos.x);
                o.TtoW1 = float4(worldTangent.y, worldBinormal.y, worldNormal.y, worldPos.y);
                o.TtoW2 = float4(worldTangent.z, worldBinormal.z, worldNormal.z, worldPos.z);
                return o;
            }

            fixed4 frag (v2f i) : SV_Target
            {
                float3 worldPos = float3(i.TtoW0.w, i.TtoW1.w, i.TtoW2.w);
                fixed3 viewDir = normalize(UnityWorldSpaceViewDir(worldPos));

                float4 packedNormal = tex2D(_BumpMap, i.uv.zw);
                float3 tangentNormal = UnpackNormal(packedNormal);

                //这里我们不使用_BumpScale来控制法线偏移量，而是默认法线偏移与法线贴图相同

                float3 worldNormal = float3(dot(i.TtoW0, tangentNormal), dot(i.TtoW1, tangentNormal), dot(i.TtoW2, tangentNormal));

                float3 reflectDir = reflect(-viewDir, normalize(worldNormal));

                fixed4 reflectColor = texCUBE(_Cube, reflectDir) * tex2D(_MainTex, i.uv);

                //切线空间下的法线的xy坐标反映出了法线贴图中的法线与默认法线的偏移程度
                //因此我们使用切线空间下的法线的xy坐标作为折射的偏移量
                //并使用_Distortion变量来具体控制
                float2 offset = tangentNormal.xy * _Distortion;

                i.grabPos.xy = offset * i.grabPos.z + i.grabPos.xy;     //深度越深，折射效果越明显
                
                fixed2 screenUV = i.grabPos.xy / i.grabPos.w;   //屏幕坐标转换到uv坐标系 透视除法
                fixed4 grabColor = tex2D(_GrabTexture, screenUV); 

                fixed4 color =  reflectColor * (1 - _RefractAmount) + grabColor * _RefractAmount; 

                return color;
            }
            ENDCG
        }
    }
}

```

# 程序纹理
**程序纹理（Procedural Texture）**指的是那些由计算机生成的图像，我们通常使用一些特定的算法来创建个性化图案或非常真实的自然元素，例如木头、石子等。使用程序纹理的好处在于我们可以使用各种参数来控制纹理的外观，而这些属性不仅仅是那些颜色属性，甚至可以是完全不同类型的图案属性，这使得我们可以得到更加丰富的动画和视觉效果。

生成程序纹理有以下两种方式：

+ 通过C#脚本生成纹理后传递给`Shader`；
+ 直接在`Shader`代码中自定义逻辑生成纹理。

## 程序纹理的优势
由于程序纹理是由代码动态生成的，因此程序纹理无需内存空间存储，同时可以在生成时任意调整输出的分辨率，也可以自由调整参数，实时更改纹理外观；同时通过适当的函数设计，可以生成无缝平铺的纹理。

自由度高，可控性强。

## 黑白棋盘格
国际象棋的棋盘格的颜色规则为：若**格子的行列编号同奇同偶则为白色，不同则为黑色。**

### 使用C#代码动态生成
{% note warning %}
`Texture2D`的原点在左下角。**

{% endnote %}

```csharp
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class ProceduralTexture : MonoBehaviour
{
    //宽高
    [SerializeField] private int textureWidth = 256;
    [SerializeField] private int textureHeight = 256;

    //国际象棋棋盘格的行列数
    [SerializeField] private int tileCount = 8;

    //棋盘格的两种颜色
    [SerializeField] private Color color1 = Color.black;
    [SerializeField] private Color color2 = Color.white;

    private void Start()
    {
        UpdateTexture();
    }
    public void UpdateTexture()
    {
        //生成对应宽高的2D纹理对象
        Texture2D tex = new Texture2D(textureWidth, textureHeight);

        for (int y = 0; y < textureHeight; y++)
        {
            for (int x = 0; x < textureWidth; x++)
            {
                //利用int向下取整
                if (x / (textureWidth / tileCount) % 2 == y / (textureHeight / tileCount) % 2)
                {
                    tex.SetPixel(x, y, color1);
                }
                else
                {
                    tex.SetPixel(x, y, color2);
                }
            }
        }

        tex.Apply(); //应用像素变化

        //Render 是 Mesh Render 等渲染器的父类
        Renderer renderer = this.GetComponent<Renderer>();
        if (renderer != null)
        {
            renderer.sharedMaterial.mainTexture = tex;
        }
    }
}

```

{% note warning %}
`renderer.sharedMaterial.mainTexture = tex;`：

+ `sharedMaterial`：指的是本地文件中存储的`Material`文件，即该代码会直接修改本地的材质球文件，其余同样使用了该材质球的物体同样会被修改材质；如果使用`.material`，Unity会在内存中创建一份原材质的副本，在游戏停止运行后自动销毁，但是若长时间运行且多次修改材质球，可能会导致内存泄漏和额外的性能消耗，因此推荐使用`.sharedMaterial`；
+ `mainTexture`：该代码会直接修改指向的材质球所使用的`Shader`文件中的`_MainTex`主纹理，即`Shader`中主纹理必须使用`_MainTex`命名，否则无法修改。

{% endnote %}

### 使用Shader代码动态生成程序纹理
```csharp
Shader "Unlit/ProceduralTexture"
{
    Properties
    {
        _TileCount("TileCount", int) = 8
        _Color1("Color1", Color) = (1,1,1,1)
        _Color2("Color2", Color) = (0,0,0,1)
    }
    SubShader
    {
        Tags { "RenderType"="Opaque" }

        Pass
        {
            CGPROGRAM
            #pragma vertex vert
            #pragma fragment frag

            #include "UnityCG.cginc"

            struct v2f
            {
                float2 uv : TEXCOORD0;
                float4 vertex : SV_POSITION;
            };

            int _TileCount;
            fixed4 _Color1;
            fixed4 _Color2;

            v2f vert (appdata_base v)
            {
                v2f o;
                o.vertex = UnityObjectToClipPos(v.vertex);
                o.uv = v.texcoord;

                return o;
            }

            fixed4 frag (v2f i) : SV_Target
            {
                //将uv缩放到0-_TileCount
                float2 uv = i.uv * _TileCount;

                //向下取整
                float2 posIndex = floor(uv);
                float value = (posIndex.x + posIndex.y) % 2;

                return lerp(_Color1, _Color2, value);      
            }
            ENDCG
        }
    }
}

```

+ `float value = (posIndex.x + posIndex.y) % 2;`：两个奇数或者两个偶数相加结果显然都是偶数，一奇一偶相加结果为奇数，因此可以使用该性质作为判断颜色的条件；
+ `erp(_Color1, _Color2, value);`：显然`value`的值只会是0或1，因此我们可以利用`lerp`，将其作为类似`if`的条件判断语句使用；

{% note warning %}
+ `float2 uv = i.uv * _TileCount;``float2 posIndex = floor(uv);`：

第一句代码将整张材质的uv从$[0,1]$缩放到了$[0,\text{\_TileCount}]$区间，即每个像素点对应的uv值被缩放了`_TileCount`倍，然后通过`floor`函数对**每个像素点各自的uv坐标值**向下取整，或者说是对u值和v值分别向下取整，从而将uv网格化。

{% endnote %}

# 动态效果
## 内置时间变量
<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/63937386/1772442142795-417900ad-0a2f-424c-ba96-8007461fb9f2.png)

+ `dt`代表的是帧间隔时间；
+ `smoothDt`是平滑处理过的时间间隔，对帧间隔时间进行某种平滑算法处理之后的结果。



通过时间控制颜色的变化可以得到渐变、闪烁等效果；

利用时间控制顶点在某个方向上移动可以得到波动的效果；

利用时间变化来动态改变纹理坐标可以得到水流、云彩、序列帧动画等；

利用时间动态修改法线方向，可以得到风吹草动的效果；

利用时间改变物体缩放比例，可以得到脉动、跳动的效果；

利用时间控制物体透明度，可以得到淡入淡出、闪烁等效果。

## 序列帧动画
图集序列帧动画播放顺序为从左到右、从上到下。

uv坐标原点在图片左下角。

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/63937386/1772442900049-d32a7e13-d697-4700-bacf-f6723a1be6c7.png)

{% note warning %}
由于序列帧常带有透明通道，即`png`图像，因此我们需要将其看做半透明物体，并使用`Blend SrcAlpha OneMinusSrcAlpha`进行混合，即 

$原像素透明度 * 原像素颜色 + (1-原像素透明度) * 背景像素颜色$

{% endnote %}

```csharp
Shader "Unlit/ImageSequenceAnimation"
{
    Properties
    {
        _MainTex ("Texture", 2D) = "white" {}
        _Rows("Rows", int) = 8
        _Columns("Columns", int) = 8
        _Speed("Speed", float) = 1
    }
    SubShader
    {
        Tags { "RenderType"="Transparent" "Queue" = "Transparent" "IgnoreProjector" = "True"}

        Pass
        {
            //使用透明度混合
            ZWrite Off
            Blend SrcAlpha OneMinusSrcAlpha

            CGPROGRAM
            #pragma vertex vert
            #pragma fragment frag

            #include "UnityCG.cginc"

            struct v2f
            {
                float2 uv : TEXCOORD0;
                float4 vertex : SV_POSITION;
            };

            sampler2D _MainTex;

            float _Rows;
            float _Columns;
            float _Speed;

            v2f vert (appdata_base v)
            {
                v2f o;
                o.vertex = UnityObjectToClipPos(v.vertex);
                o.uv = v.texcoord;
                return o;
            }

            fixed4 frag (v2f i) : SV_Target
            {
                float frameIndex = floor(_Time.y * _Speed) % (_Rows * _Columns);
                float2 frameUV = float2(frameIndex % _Columns / _Columns, 1 - (floor(frameIndex / _Columns) + 1) / _Rows);
                float2 size = float2(1 / _Columns, 1 / _Rows);
                float2 uv = i.uv * size + frameUV;

                return tex2D(_MainTex, uv);
            }
            ENDCG
        }
    }
}
```

+ `float frameIndex = floor(_Time.y * _Speed) % (_Rows * _Columns);`：总序列帧数为`_Rows * _Columns`，因此`floor(_Time.y) % (_Rows * Columns)`表示当前序列帧的序号，同时速度为1帧/秒，即播放完序列帧动画需要`(_Rows * Columns)`秒；因此我们引入`_Speed`变量，播放速度可以表示为`_Speed`帧/秒。

{% note warning %}
我们并不是直接对整张序列帧图集进行采样，而是需要先获取每个小序列帧的左下角位置，然后对每个小序列帧进行采样。

{% endnote %}

+ `frameIndex % _Columns`表示当前序列帧位于第几列，因此`frameIndex % _Columns / _Columns`表示**当前的小序列帧的u轴原点**，`floor(frameIndex / _Columns)`表示当前序列帧位于第几行（从上往下数），但是这样计算v轴的原点会位于小序列帧的左上角，由于**uv坐标系原点在左下角**，因此需要使用`1 - (floor(frameIndex / _Columns) + 1) / _Rows`来表示**当前的小序列帧的v轴原点**。

{% note warning %}
+ `float2 size = float2(1 / _Columns, 1 / _Rows);float2 uv = i.uv * size + frameUV;`：

`size`表示**每个小序列帧的大小**，`frameUV`表示**每个小序列帧的左下角**，相当于将uv坐标系先缩放为小序列帧的大小，再将缩放后的uv坐标系的原点移动至`frameUV`处，即**对每个小序列帧依次采样**。

{% endnote %}

## 滚动的背景
我们将基于`frac`函数来实现滚动的背景。`frac`函数内部的计算规则为`frac(x) = x - floor(x)`，即用于保证不论是向u轴正半轴采样还是**向负半轴采样**，都能从每张**平铺的纹理图**的左下角沿u轴正方向取值。

{% note info %}
即u值超过1时重新从0开始采样；u值小于0是重新从1开始采样。

{% endnote %}

{% note info %}
和序列帧一样，这类图片常带有透明通道，即`png`图像，因此我们需要将其看做半透明物体，并使用`Blend SrcAlpha OneMinusSrcAlpha`进行混合，即 

$原像素透明度 * 原像素颜色 + (1-原像素透明度) * 背景像素颜色$

{% endnote %}

```csharp
Shader "Unlit/ScrollingBackground"
{
    Properties
    {
        _MainTex ("Texture", 2D) = "white" {}
        _ScrollSpeedU("ScrollSpeedU", float) = 0.5
        _ScrollSpeedV("ScrollSpeedV", float) = 0.5
    }
    SubShader
    {
        Tags { "RenderType"="Transparent" "Queue" = "Transparent" "IgnoreProjector" = "True"}

        Pass
        {
            ZWrite Off
            Blend SrcAlpha OneMinusSrcAlpha

            CGPROGRAM
            #pragma vertex vert
            #pragma fragment frag

            #include "UnityCG.cginc"

            struct v2f
            {
                float2 uv : TEXCOORD0;
                float4 vertex : SV_POSITION;
            };

            sampler2D _MainTex;
            float4 _MainTex_ST;
            float _ScrollSpeedU;
            float _ScrollSpeedV;

            v2f vert (appdata_base v)
            {
                v2f o;
                o.vertex = UnityObjectToClipPos(v.vertex);
                o.uv = TRANSFORM_TEX(v.texcoord, _MainTex);
                return o;
            }

            fixed4 frag (v2f i) : SV_Target
            {
                float2 scrollUV = frac(i.uv + float2(_Time.y * _ScrollSpeedU, _Time.y * _ScrollSpeedV)); 

                return tex2D(_MainTex, scrollUV);
            }
            ENDCG
        }
    }
}

```

+ 显然，`_Time.y * i.uv.x`表示横向每秒钟平移一张纹理图的长度。

## 顶点动画（水流波浪）
要实现波浪效果，实际上就是让物体的每个顶点按照正弦函数的规律依次发生向上和向下的偏移，因此我们使用以下公示来得到每个顶点在y轴方向上的偏移量：

$\text{某轴位置偏移量} = \sin(\text{\_Time.y} \times \text{波动频率} + \text{顶点某轴坐标} \times \text{波长的倒数}) \times \text{波动幅度}$

```csharp
Shader "Unlit/VertexAnimation"
{
    Properties
    {
        _MainTex ("Texture", 2D) = "white" {}
        _Color("Color", Color) = (1,1,1,1)

        _WaveAmplitude("WaveAmplitude", Float) = 1
        _WaveFrequency("WaveFrequency", Float) = 1

        //建议直接传入波长的倒数 以减少计算量
        _InvWaveLength("_InvWaveLength", Float) = 1
        _Speed("Speed", Float) = 1
    }
    SubShader
    {
        Tags { "RenderType"="Transparent" "Queue" ="Transparent" "IgnoreProjector" = "True" "DisableBatching" ="True"}

        Pass
        {
            ZWrite Off
            Blend SrcAlpha OneMinusSrcAlpha

            CGPROGRAM
            #pragma vertex vert
            #pragma fragment frag

            #include "UnityCG.cginc"

            struct appdata
            {
                float4 vertex : POSITION;
                float2 uv : TEXCOORD0;
            };

            struct v2f
            {
                float2 uv : TEXCOORD0;
                float4 vertex : SV_POSITION;
            };

            sampler2D _MainTex;
            float4 _MainTex_ST;
            float4 _Color;
            float _WaveAmplitude;
            float _WaveFrequency;
            float _InvWaveLength;
            float _Speed;

            v2f vert (appdata_base v)
            {
                v2f o;
                float4 offset;

                //偏移所在的坐标轴方向可以通过观察模型自身坐标轴方向得到
                offset.x = sin(_Time.y * _WaveFrequency + v.vertex.z * _InvWaveLength) * _WaveAmplitude;
                offset.yzw = float3(0, 0, 0);
                o.vertex = UnityObjectToClipPos(v.vertex + offset);
                o.uv = TRANSFORM_TEX(v.texcoord, _MainTex);

                //如果有波浪纹理的话，此处可以控制波浪纹理的移动速度
                o.uv += float2(0, _Time.y * _Speed);
                return o;
            }

            fixed4 frag (v2f i) : SV_Target
            {
                fixed4 col = tex2D(_MainTex, i.uv);

                return col * _Color;
            }
            ENDCG
        }
    }
}

```

{% note info %}
需要注意的是，上述半透明物体不会产生于阴影，如果需要**产生正常的阴影**，则需要手动实现`ShadowCaster Pass`，并**同样添加顶点动画相关逻辑**，否则阴影将静止不动。

{% endnote %}

{% note info %}
Unity的批处理`Batching`会将场景中被标记为`static`的静态物体、使用了同一种材质的物体、网格完全一致的物体合并网格同时渲染以减少DrawCall，但是合并网格会导致模型丢失模型空间的顶点数据，而顶点动画又依赖于模型空间的顶点数据，因此我们需要使用`"DisableBatching" = "True"`来为顶点动画的物体**关闭批处理**。

如果需要开启批处理，我们可以在需要添加顶点动画的物体上挂载一个C#脚本，并添加如下代码：

这段代码首先获取了物体的网格体，并从中获取物体顶点数组，而后创建了一个长度为顶点数量了`Color`数组，并遍历所有顶点，将每个顶点的模型空间位置存储在`Color`数组中，最后将该数组赋值给物体网格，而后我们可以**通过`Shader`中的`appdata`（传入顶点着色器的）结构体中的语义为`COLOR`的变量获取上述传入的顶点模型空间坐标。**

但要注意的是，我们**一般不会使用`COLOR`通道**，因为它的长度只有8位，当物体体积较大，长度坐标大于255时，我们将无法获取到这些顶点，因此我们**通常会使用uv通道**，即`TEXCOORD`语义，这些通道使用32位存储，精度较高。

{% endnote %}

```csharp
MeshFilter meshFilter = GetComponent<MeshFilter>();
if (meshFilter != null)
{
    //获取网格
    Mesh mesh = meshFilter.mesh;
    //获取顶点
    Vector3[] vertices = mesh.vertices;
    //创建颜色数组
    Color[] colors = new Color[vertices.Length];

    for (int i = 0; i < vertices.Length; i++)
    {
        // 将模型空间位置存储在顶点颜色中
        colors[i] = new Color(vertices[i].x, vertices[i].y, vertices[i].z, 1);
    }

    mesh.colors = colors;
}
```

## 广告牌技术
**广告牌技术（Billboarding）**指根据视角方向来旋转一个被纹理着色的多边形，使得该多边形看起来一直面对着摄像机（**全向广告牌**），或者固定该多边形的一个轴，只在二维平面内旋转并始终指向摄像机的方向（**轴对齐广告牌**）。

要实现广告牌效果，关键在于让物体持续向视角方向旋转，也就是**基于世界空间构建一个全新的模型空间坐标系**，该坐标系始终指向视角方向，然后让物体使用构建的坐标系作为全新的模型空间坐标系即可。构建坐标系需要三个基向量：

### 全向广告牌
<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/63937386/1772458523838-6411b633-2279-4eb4-b1d9-48a998f4b60e.png)

全向广告牌始终指向视角方向，因此我们所需要构建的坐标系中，**物体的法线（新坐标系的**$z'$**轴）应该始终指向摄像机**，因此我们可以得到：

$z'轴方向向量 = 摄像机坐标 - 物体原点(0,0,0)$

同时，物体始终正对着摄像机，意味着**构建的坐标系的**$x'$**轴方向应该始终指向屏幕的正右方**，但是我们无法直接获取屏幕正右方所对应的世界空间中的方向向量，因此，我们先**使用世界空间中朝向正上方的方向向量**$\hat{y} =(0,1,0)$，显然$\hat{y}$和$z'$所构成的平面垂直于水平面，因此我们可以通过**叉积**来求得$x'$轴方向向量：

$x'轴方向向量 = \hat{y} \times z'$

此时我们已经求出了正确的$x'$和$z'$两个坐标轴的方向向量，且两个方向向量互相垂直，因此我们可以再用叉积求得正确的$y'$轴方向向量：

$y'轴方向向量 = z' \times x'$

至此，我们已经计算出了一个$z$轴始终指向摄像机的全新坐标系的三个基向量，接下来便是应用物体的旋转。这里的旋转并不是类似旋转矩阵的旋转效果，而是不断地让物体应用新的坐标系，即**将物体上的每个顶点的**$\bf{xyz}$**坐标值（偏移值）应用在新的坐标系中**，同时我们认为模型将围绕着其原先的模型空间原点$(0,0,0)$旋转，由此可以得到：

$$
\begin{aligned}
\text{偏移量} &= \text{原顶点坐标} - (0,0,0) \\[1pt]
\text{新顶点坐标} &= (0,0,0) + x' \times \text{偏移量}.x + y' \times \text{偏移量}.y + z' \times \text{偏移量}.z
\end{aligned}
$$

{% note warning %}
请注意，我们**通常会选择使用Unity中的`Quad`四边形来作为广告牌的物体**，而不是用`Plane`平面，这是因为`Quad`的顶点默认定义在**$XY$**平面上**，而`Plane`的顶点默认定义在`XZ`平面上**，显然前者才符合我们的算法；同时，`Quad`只有4个顶点，2个三角形；`Plane`有121个顶点，200个三角形，性能开销过大，**因此我们通常使用`Quad`。

{% endnote %}

```csharp
Shader "Unlit/Billboarding"
{
    Properties
    {
        _MainTex ("Texture", 2D) = "white" {}
        _Color("Color", Color) = (1,1,1,1)
        _VerticalBillboarding("VerticalBillboarding", Range(0, 1)) = 1
    }
    SubShader
    {
        Tags { "RenderType"="Transparent" "Queue" ="Transparent" "IgnoreProjector" ="True" "DisableBatching"="True"}

        Pass
        {
            ZWrite Off
            Blend SrcAlpha OneMinusSrcAlpha

            //关闭背面剔除以防止极端情况
            Cull Off

            CGPROGRAM
            #pragma vertex vert
            #pragma fragment frag

            #include "UnityCG.cginc"

            struct v2f
            {
                float2 uv : TEXCOORD0;
                float4 vertex : SV_POSITION;
            };

            sampler2D _MainTex;
            float4 _MainTex_ST;
            fixed4 _Color;
            float _VerticalBillboarding;

            v2f vert (appdata_base v)
            {
                v2f o;
                float3 center = float3(0, 0, 0);
                float3 cameraInObjectPos = mul(unity_WorldToObject, float4(_WorldSpaceCameraPos, 1));
                float3 normalDir = cameraInObjectPos - center;

                //使用_VerticalBillboarding来线性切换轴对齐广告牌
                normalDir.y *= _VerticalBillboarding;
                normalDir = normalize(normalDir);

                //处理当视角方向平行于世界空间y轴的极端情况
                float3 upDir = abs(normalDir.y) > 0.999 ? float3(0, 0, 1) : float3(0, 1, 0);
                float3 rightDir = normalize(cross(upDir, normalDir));
                upDir = normalize(cross(normalDir, rightDir));

                float3 centerOffset = v.vertex.xyz - center;
                float3 newVertexPos = center + rightDir * centerOffset.x + upDir * centerOffset.y + normalDir * centerOffset.z;

                o.vertex = UnityObjectToClipPos(float4(newVertexPos, 1));
                o.uv = TRANSFORM_TEX(v.texcoord, _MainTex);
                return o;
            }

            fixed4 frag (v2f i) : SV_Target
            {
                fixed4 col = tex2D(_MainTex, i.uv);

                return col * _Color;
            }
            ENDCG
        }
        
    }
    Fallback "Transparent/VertexLit"
}
```

{% note info %}
+ `float3 upDir = abs(normalDir.y) > 0.999 ? float3(0, 0, 1) : float3(0, 1, 0);`：**当摄像机位于广告牌正上/下方时**，此时$z'$轴的方向和从广告牌原点出发向上方的$(0,1,0)$向量方向平行，此时**两者叉积结果为零向量**，无法计算出向右的$x'$，因此在接近极端情况，即归一化后的法线的`y`值接近1时，这意味着法线与y轴即将重合，此时我们**更换上方向为其他任意不与广告牌法线方向（摄像机方向）重合的向量（通常使用**$\bf{(0,1,0)}$**）**，均可计算出$x'$向量，以保证广告牌能被正常渲染，但缺点在于广告牌的正上方和屏幕正上方并不重合，即**渲染出的结果可能是东倒西歪的**。

若要避免这种情况，我们可以**使用观察空间变换矩阵的行向量**，即`float3 rightDir = UNITY_MATRIX_V[0].xyz;``float3 upDir = UNITY_MATRIX_V[1].xyz;`，因为观察空间变换矩阵的作用是将世界空间中的顶点变换到观察空间中，因此观察空间变换矩阵的逆矩阵（即原矩阵的行向量）表示将观察空间中的顶点变换到世界空间中，即**逆矩阵中的列向量为基于世界空间表示的观察空间的**$xyz$**轴的方向向量**，即以摄像机为原点的坐标系，因此这里的$xyz$轴表示屏幕的正右、上、前方。

{% endnote %}

### 轴对齐广告牌
轴对齐广告牌一般会固定模型空间中的$y$轴方向始终固定，因此我们只需要让物体在$xz$轴旋转，即在计算$z'$时将$z'.y$设置为0即可。

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/63937386/1772522886812-80e14df1-93dd-4742-96e3-a0161b36fcf8.png)

# 屏幕后处理效果
## 使用C#代码修改材质参数
```csharp
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Lesson99 : MonoBehaviour
{
    public Color color;
    [Range(0,1)]
    public float fresnelScale;
    private Material material;

    // Start is called before the first frame update
    void Start()
    {
        //获取对象的渲染器
        Renderer renderer = GetComponent<Renderer>();
        if(renderer != null)
        {
            //sharedMaterial和material的区别
            //sharedMaterial:一个是改一个都变
            //material:一个是改一个不会影响其它使用相同材质球的对象
            //得到主材质球
            material = renderer.material;//renderer.sharedMaterial;
            //得到所有的材质球
            Material[] materials = renderer.sharedMaterials; //renderer.materials;
            //修改颜色
            material.color = color;
            //修改主纹理
            material.mainTexture = Resources.Load<Texture2D>("路径");

            if (material.HasColor("_Color"))
            {
                material.SetColor("_Color", color);
                print(material.GetColor("_Color"));
            }

            if (material.HasFloat("_FresnelScale"))
                material.SetFloat("_FresnelScale", fresnelScale);

            //修改渲染队列
            material.renderQueue = 2000;

            //修改材质球使用的shader
            material.shader = Shader.Find("Unlit/Lesson80_Fresnel");

            material.SetTextureOffset("_MainTex", new Vector2(0.5f, 0.5f));
            material.SetTextureScale("_MainTex", new Vector2(0.5f, 0.5f));
        }
    }
}

```

## 基本原理
屏幕后处理，顾名思义，通常指的是在渲染完整个场景得到屏幕图像后，再对这个图像进行一系列操作，实现各种屏幕特效。使用这种技术，可以为游戏画面添加更多的艺术效果，例如景深(Depth ofField)、运动模糊(MotionBlur)等。

我们通过调用函数的方式，获取渲染完毕后的画面信息，并将获取到的画面作为自定义`Shader`的主纹理，通过`Shader`中的代码实现自定义效果。

### OnRenderImage函数
`void OnRenderImage(RenderTexture source, RenderTexture destination)`：当我们在脚本中声明此函数后，Unity会把**当前渲染得到的图像**存储在**第一个参数**对应的源渲染纹理中，通过函数中的一系列操作后，再把**目标渲染纹理**，即第二个参数对应的渲染纹理**显示到屏幕**上。

该函数**类似生命周期函数**，Unity会在每一帧的特定顺序调用该函数，同时它**必须挂在含有`Camera`组件的 `GameObject`上**才能生效。

如果我们不需要对场景中的半透明物体进行后处理，即在所有不透明物体渲染完毕之后立刻调用该函数，只需要在函数前添加`[ImageEffectOpaque]`属性即可。

在`OnRenderImage`函数中，我们通常会使用`Graphics.Blit`函数来完成对渲染纹理的处理。

### Graphics.Blit
该函数有多种重载类型，我们列举两个最常用的：

+ `Graphics.Blit(source, destination);`：表示直接将源纹理复制给目标渲染纹理；
+ `Graphics.Blit (Texture source, RenderTexture dest, Material mat, int pass= -1);`：`source`源纹理会被传递给`mat`材质中`Shader`中名为`_MainTex`的纹理属性用于进行处理，然后**将结果写入目标纹理中**；`pass`参数**默认值为-1**，表示会**依次调用`Shader`内的所有`Pass`进行处理**，否则，只会**调用给定索引的`Pass`。

```csharp
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class PostTest : MonoBehaviour
{
    public Material testMat;

    private void OnRenderImage(RenderTexture source, RenderTexture destination)
    {
        Graphics.Blit(source, destination, testMat);
    }
}
```

## 屏幕后处理基类
### 为什么我们要创建后处理基类
显然如果我们需要实现屏幕后处理效果，每次都需要：

+ 编写一个继承自`MonoBehaviour`的自定义C#脚本；
+ 在外部手动关联材质球；
+ 在类内实现`OnRenderImage`函数，并调用`Graphics.Blit`函数；

因此，我们可以将这些共同点抽象到一个基类中去完成。

同时，基类还可以负责在代码中动态创建材质球，我们只需要在`Inspector`中手动指定需要使用的`Shader`即可；我们也需要检查Unity是否支持传入的`Shader`。

### 后处理基类
+ `Shader.isSupported`：返回值为`bool`类型，用于判断`Shader`是否被支持且能正常运行；
+ `[ExecuteInEditMode]`特性：使脚本在编辑器模式下也能执行；
+ `[RequireComponent(typeof(组件名))]`特性：指定某个脚本所依赖的组件，它确保当你将脚本附加到游戏对象时，所需的组件也会自动添加到该游戏对象中；
+ `HideFlags`枚举：材质球包含一个`HideFlags`枚举类型的属性，其中我们需要使用`HideFlags.DontSave`，即**对象不会被保存到场景中，不会在构建中保存，也不会在编辑器中保存**，因为我们的代码中会动态创建材质球，但是我们并不需要将它保存下来。

{% note info %}
`HideFlags.None`: 对象是完全可见和可编辑的。这是默认值。

`HideFlags.HideInHierarchy`: 对象在层级视图（Hierarchy）中被隐藏，但仍然存在于场景中。

`HideFlags.HideInInspector`: 对象在检查器（Inspector）中被隐藏，但仍然存在于层级视图中。

`HideFlags.DontSaveInEditor`: 对象不会被保存到场景中。适用于编辑器模式，不会影响播放模式。

`HideFlags.NotEditable`: 对象在检查器中是只读的，不能被修改。

`HideFlags.DontSaveInBuild`: 对象不会被包含在构建（Build）中。

`HideFlags.DontUnloadUnusedAsset`: 对象在资源清理（Resources.UnloadUnusedAssets）时不会被卸载，即使它没有被引用。

`HideFlags.DontSave`: 对象不会被保存到场景中，不会在构建中保存，也不会在编辑器中保存。这是 DontSaveInEditor | DontSaveInBuild | DontUnloadUnusedAsset 的组合。

`HideFlags.HideAndDontSave`: 对象在层级视图中被隐藏，不在检查器中显示，且不会被保存到场景、不会在构建中保存，也不会在资源清理时被卸载。这是最常用的组合标识，常用于隐藏脚本生成的临时资源。 它是 HideInHierarchy | HideInInspector | DontSave 的组合。

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/63937386/1772712084109-f306f1b6-2221-4ac5-9eb2-4626673a8f41.png)

{% endnote %}

```csharp
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

[ExecuteInEditMode]
[RequireComponent (typeof(Camera))]
public class PostEffectBase : MonoBehaviour
{
    public Shader shader;
    private Material _material;

    protected Material material
    {
        //在读取material变量时会调用get
        //第一次调用时会动态创建_material
        //后续调用时只要Shader不发生变化，会直接返回_material
        get
        {
            if ( shader == null || !shader.isSupported)
                return null;
            else
            {
                if ( _material != null && _material.shader == shader)
                    return _material;
                else
                {
                    _material = new Material(shader);
                    _material.hideFlags = HideFlags.DontSave;
                    return _material;
                }
            }
        }
    }
    protected virtual void OnRenderImage(RenderTexture source, RenderTexture destination)
    {
        //在子类中重写 用于调整并向Shader传入属性值等
        UpdateProperty();
        //判断材质球是否为空
        if (material != null)
        {
            Graphics.Blit (source, destination, material);
        }
        else
        {
            Graphics.Blit (source, destination);
        }
    }

    protected virtual void UpdateProperty() { }
}

```

## 调整屏幕亮度、饱和度和对比度
### 亮度
我们可以**通过增加像素的RGB值来增加亮度，通过减小RGB值来降低亮度**。我们通常会将每个像素的颜色乘以一个亮度变量来改变颜色，即：

$最终颜色 = 原始颜色 \times 亮度变量$

其中，当亮度变量大于1，图像变亮；亮度变量小于1，图像变暗。

### 饱和度
**画面的饱和度越低，颜色越接近灰度颜色，即黑白图像**，因此我们可以使用插值函数`lerp`，**在灰度颜色和原始颜色之间进行插值运算**，其中灰度颜色的计算方式为（加权平均）：

$L = 0.2126 \times R + 0.7152 \times G + 0.0722 \times B$

根据上式计算出的灰度值$L$组成一个灰度颜色$(L,L,L)$，并引入饱和度变量作为插值系数：

$最终颜色 = \text{lerp}( 灰度颜色, 原始颜色, 饱和度变量 ) \\[5pt] \text{lerp}计算原理：\color{red}最终颜色 = 灰度颜色 + (原始颜色 − 灰度颜色) \times 饱和度变量$

根据上式可以得到，当饱和度变量大于1时，颜色的RGB值会超出原始范围，从而使颜色更加饱和。

### 对比度
**对比度**指的是**图像最亮的区域和最暗的区域之间的亮度差异**，因此我们可以通过**将每个像素的颜色和中性灰色**$\bf(0.5,0.5,0.5)$**进行插值**（显然**中性灰色不存在亮部和暗部的亮度差异，即对比度为0**）

$最终颜色 = \text{lerp}( 中性灰色, 原始颜色, 对比度变量 )$

对比度变量大于1时，颜色的RGB值超出原始范围，从而使颜色亮部更亮，暗部更暗，从而增加对比度。

### 调整画面亮度、饱和度和对比度实现
{% note info %}
屏幕后处理`Shader`默认需要设置为**始终通过深度测试、关闭背面剔除、关闭深度写入**，即`ZTest Always``Cull Off``Zwrite Off`，因为**屏幕后处理效果实际上是在场景中绘制了一个与屏幕同宽同高的四边形面片**，**我们需要该面片总是被完整渲染出来**；同时如果我们开启`[ImageEffectOpaque]`，意味着半透明物体会在该四边形面片渲染完成之后再被渲染，它们会受到该面片的深度写入的影响，因此需要关闭深度写入。

{% endnote %}

```csharp
Shader "Unlit/BrightnessSaturationContrast"
{
    Properties
    {
        _MainTex ("Texture", 2D) = "white" {}
        _Brightness("Brightness", Float) = 1
        _Saturation("Saturation", Float) = 1
        _Contrast("Contrast", Float) = 1
    }
    SubShader
    {
        Tags { "RenderType"="Opaque" }

        Pass
        {
            ZTest Always
            Cull Off
            ZWrite Off

            CGPROGRAM
            #pragma vertex vert
            #pragma fragment frag

            #include "UnityCG.cginc"

            struct v2f
            {
                float2 uv : TEXCOORD0;
                float4 vertex : SV_POSITION;
            };

            sampler2D _MainTex;
            float4 _MainTex_ST;
            float _Brightness;
            float _Saturation;
            float _Contrast;

            v2f vert (appdata_base v)
            {
                v2f o;
                o.vertex = UnityObjectToClipPos(v.vertex);
                o.uv = TRANSFORM_TEX(v.texcoord, _MainTex);

                return o;
            }

            fixed4 frag (v2f i) : SV_Target
            {
                //从捕获的主纹理中采样
                fixed4 col = tex2D(_MainTex, i.uv);
                //调整亮度
                fixed3 finalColor = col * _Brightness;

                //计算灰度值
                fixed saturation = 0.2126 * col.r + 0.7152 * col.g + 0.0722 * col.b;
                //灰度颜色
                fixed3 saturationColor = fixed3(saturation, saturation, saturation);
                //调整饱和度
                finalColor = lerp(saturationColor, finalColor, _Saturation);

                //中性灰色
                fixed3 contrast = fixed3(0.5, 0.5, 0.5);
                //调整对比度
                finalColor = lerp(contrast, finalColor, _Contrast);

                return fixed4(finalColor, col.a);
            }
            ENDCG
        }
    }
}
```

```csharp
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class BrightnessSaturationContrast : PostEffectBase
{
    [Range(0, 2)] public float Brightness = 1;
    [Range(0, 2)] public float Saturation = 1;
    [Range(0, 2)] public float Contrast = 1;

    protected override void UpdateProperty()
    {
        if (material != null)
        {
            material.SetFloat("_Brightness", Brightness);
            material.SetFloat("_Saturation", Saturation);
            material.SetFloat("_Contrast", Contrast);
        }
    }
}

```

## 边缘检测
见数字图像处理（bushi）

边缘检测的原理是利用一些**边缘检测算子**对图像进行**卷积(convolution)**操作。

### 原理
在图像处理中，卷积操作指的就是使用一个**卷积核(kernel)**对一张图像中的每个像素进行一系列操作。卷积核通常是一个四方形网格结构（例如2×2、3×3的方形区域)，该区域内每个方格都有一个权重值。当对图像中的某个像素进行卷积时，我们会把卷积核的中心放置于该像素上，**翻转核**之后再依次计算核中每个元素和其覆盖的图像像素值的乘积并求和，得到的结果就是该位置的新像素值。

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/63937386/1772541876097-90ebd2c6-c48b-4c04-ac32-43e0677dee3c.png)

{% note info %}
在数学层面，卷积的定义要求**翻转核**，即将卷积核**绕中心点进行水平翻转和垂直翻转**。这是为了满足交换律（即$f * g = g * f$），在信号处理等理论严谨的领域，必须执行这一步。但是在`Shader`编写中，我们通常直接使用**互相关（Cross-correlation）**，互相关和卷积唯一的区别就是不翻转核，也就是**直接省略翻转核的步骤**，因为大多数常用的滤镜（卷积）核（如高斯模糊、均值模糊）都是中心对称的，翻转核并不会影响结果；如果卷积核是不对称的，我们通常会直接按照“不翻转”后的逻辑去设计权值，所以也就省去了翻转的步骤。

{% endnote %}

	如果相邻像素之间存在差别明显的颜色、亮度、纹理等属性，我们就会认为它们之间应该有一条边界。这种相邻像素之间的差值可以用**梯度（gradient）**来表示，我们将图像的灰度值与边缘检测算子（一些特殊的卷积核）进行卷积操作，得到的结果就是梯度值。可以想象得到，**边缘处的梯度绝对值会比较大**。以下是一些常用的边缘检测算子：

$$
\begin{aligned}
\text{Roberts: } \quad G_x &= \begin{bmatrix} -1 & 0 \\ 0 & 1 \end{bmatrix}, & G_y &= \begin{bmatrix} 0 & -1 \\ 1 & 0 \end{bmatrix} \\[20pt]
\text{Prewitt: } \quad G_x &= \begin{bmatrix} -1 & -1 & -1 \\ 0 & 0 & 0 \\ 1 & 1 & 1 \end{bmatrix}, & G_y &= \begin{bmatrix} -1 & 0 & 1 \\ -1 & 0 & 1 \\ -1 & 0 & 1 \end{bmatrix} \\[20pt]
\color{red}\text{Sobel: } \quad G_x &\color{red}= \begin{bmatrix} -1 & -2 & -1 \\ 0 & 0 & 0 \\ 1 & 2 & 1 \end{bmatrix}, & \color{red}G_y &\color{red}= \begin{bmatrix} -1 & 0 & 1 \\ -2 & 0 & 2 \\ -1 & 0 & 1 \end{bmatrix}
\end{aligned}
$$

显然，我们需要计算像素与像素之间在水平方向和垂直方向上的差异，因此我们需要**计算水平梯度和垂直梯度**，在数学上，最终的梯度应等于两者的平方和的平方根，即：

$G = \sqrt{G_x^2 + G_y^2}$

但是上式包含了开平方的操作，这意味着**我们需要对图像上的每一个像素执行开平方，性能消耗较大**，因此，在`Shader`计算中，我们**常使用绝对值之和代替**：

$G = |G_x| + |G_y|$

这是因为边缘的梯度绝对值较大，因此不论使用平方和的平方根，还是绝对值之和，我们都能在图像中的边缘区域获得较大的梯度结果值。

获得了每个像素的梯度值之后，我们可以使用插值函数，利用梯度作为插值系数，得到添加了描边的图像结果：

$\color{red}\text{添加描边后的颜色} = \text{lerp}(\text{原始像素颜色}, \text{边缘颜色}, \text{梯度值})$

同时我们希望能够手动控制描边效果的强度，因此我们继续引入强度系数作为插值系数：

$\color{red}\text{最终颜色} = \text{lerp(原始像素颜色，添加描边后的颜色， 描边强度)}$

### 边缘检测实现
由于我们需要使用卷积核与当前像素的周围8个像素的灰度值相乘，因此我们需要在`Shader`中获取当前像素的周围8个像素。我们可以使用Unity提供的`float4 纹理名_TexelSize`来获取对应纹理的每个纹素（像素）的大小，其中的`.xyzw`分别代表：

`.x`表示`1/纹理宽度`；

`.y`表示`1/纹理高度`；

`.z`表示纹理宽度；

`.w`表示纹理高度。

我们可以提前**计算出每个片元周围的8个像素在纹理图中采样的uv坐标**，由于uv坐标是归一化的，因此我们只要偏移`1/纹理宽度``1/纹理高度`即可，并存储在顶点信息中（结构体中），虽然这一步是以片元为单位的，但实际上我们**可以在顶点着色器中完成**，因为屏幕后处理的顶点着色器本质上**只需要计算四边形的4个顶点**中的信息，**能够节约大量的性能**，因此我们可以计算出这4个顶点各自周围的8个像素的uv坐标，而**其余的片元可以通过线性插值自动完成**，例如图片宽度为1920，最左侧的两个顶点计算出的他们左侧的片元的采样坐标的u值应该等于-1/1920，同理，最右侧的两个顶点计算出的他们左侧的片元的采样坐标的u值应该等于1-1/1920，因此中间的其他片元将会在$[-1/1920, 1-1/1920]$中间线性插值，而线性系数（图像宽度）又将这个区间分成了1920分，意味着每两个片元之间的插值正好为1/1920。

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/63937386/1772545663662-68b91663-a290-442f-b520-b5d105ed5e51.png)

```csharp
Shader "Unlit/OnlyEdge"
{
    Properties
    {
        _MainTex ("Texture", 2D) = "white" {}
        _EdgeColor("EdgeColor", Color) = (0,0,0,0)

        _Background("Background", Range(0, 1)) = 1
        _BackgroundColor("BackgroundColor", Color) = (1,1,1,1)
    }
    SubShader
    {
        Tags { "RenderType"="Opaque" }

        Pass
        {
            ZTest Always
            Cull Off
            ZWrite Off

            CGPROGRAM
            #pragma vertex vert
            #pragma fragment frag

            #include "UnityCG.cginc"

            struct v2f
            {
                //这里相当于使用了9个插值寄存器，非常浪费，一个插值寄存器只存了两个数值
                half2 uv[9] : TEXCOORD0;
                float4 vertex : SV_POSITION;
            };

            sampler2D _MainTex;
            half4 _MainTex_TexelSize;
            fixed4 _EdgeColor;
            fixed _Background;
            fixed4 _BackgroundColor;

            v2f vert (appdata_base v)
            {
                v2f o;
                o.vertex = UnityObjectToClipPos(v.vertex);
                half2 uv = v.texcoord;
                o.uv[0] = uv + _MainTex_TexelSize.xy * half2(-1, -1);
                o.uv[1] = uv + _MainTex_TexelSize.xy * half2(0, -1);
                o.uv[2] = uv + _MainTex_TexelSize.xy * half2(1, -1);
                o.uv[3] = uv + _MainTex_TexelSize.xy * half2(-1, 0);
                o.uv[4] = uv + _MainTex_TexelSize.xy * half2(0, 0);
                o.uv[5] = uv + _MainTex_TexelSize.xy * half2(1, 0);
                o.uv[6] = uv + _MainTex_TexelSize.xy * half2(-1, 1);
                o.uv[7] = uv + _MainTex_TexelSize.xy * half2(0, 1);
                o.uv[8] = uv + _MainTex_TexelSize.xy * half2(1, 1);

                return o;
            } 

            fixed calcLuminance(fixed4 color)
            {
                return 0.2126 * color.r + 0.7152 * color.g + 0.0722 * color.b;
            }

            half Sobel(v2f o)
            {
                half Gx[9] = {-1, -2, -1, 
                               0, 0, 0,
                               1, 2, 1};
                half Gy[9] = {-1, 0, 1,
                              -2, 0, 2,
                              -1, 0, 1};
                half edgeX = 0;
                half edgeY = 0;
                half L;
                for (int i = 0; i < 9; i++)
                {
                    L = calcLuminance(tex2D(_MainTex, o.uv[i]));
                    edgeX += L * Gx[i];
                    edgeY += L * Gy[i];
                }

                return abs(edgeX) + abs(edgeY);
            }

            fixed4 frag (v2f i) : SV_Target
            {
                half edge = Sobel(i);

                fixed4 edgeColor = lerp(tex2D(_MainTex, i.uv[4]), _EdgeColor, edge);

                return lerp(tex2D(_MainTex, i.uv[4]), edgeColor, _Background);
            }
            ENDCG
        }
    }

    Fallback Off
}

```

```csharp
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class _EdgeDetection : PostEffectBase
{
    public Color EdgeColor;
    public Color BackgroundColor;
    [Range(0f, 1f)] public float Background;

    protected override void UpdateProperty()
    {
        if (material != null)
        {
            material.SetColor("_EdgeColor", EdgeColor);
            material.SetColor("_BackgroundColor", BackgroundColor);
            material.SetFloat("_Background", Background);
        }
    }
}

```

### 纯色背景（仅边缘描边）实现
我们不止可以在原图中添加描边，**还可以将原图像的梯度值应用于其他图片，例如纯色背景**，因为梯度值的大小变化对应了原图像的边缘位置，所以我们可以手动指定描边颜色并在纯色背景中“勾勒”出原图像的边缘：

$\color{red}\text{最终颜色} = \text{lerp(纯色背景颜色，描边颜色， 梯度)}$

```csharp
Shader "Unlit/_EdgeDetection"
{
    Properties
    {
        _MainTex ("Texture", 2D) = "white" {}
        _EdgeColor("EdgeColor", Color) = (0,0,0,0)

        _Background("Background", Range(0, 1)) = 1
        _BackgroundColor("BackgroundColor", Color) = (1,1,1,1)
    }
    SubShader
    {
        Tags { "RenderType"="Opaque" }

        Pass
        {
            ZTest Always
            Cull Off
            ZWrite Off

            CGPROGRAM
            #pragma vertex vert
            #pragma fragment frag

            #include "UnityCG.cginc"

            struct v2f
            {
                half2 uv[9] : TEXCOORD0;
                float4 vertex : SV_POSITION;
            };

            sampler2D _MainTex;
            half4 _MainTex_TexelSize;
            fixed4 _EdgeColor;
            fixed _Background;
            fixed4 _BackgroundColor;

            v2f vert (appdata_base v)
            {
                v2f o;
                o.vertex = UnityObjectToClipPos(v.vertex);
                half2 uv = v.texcoord;
                o.uv[0] = uv + _MainTex_TexelSize.xy * half2(-1, -1);
                o.uv[1] = uv + _MainTex_TexelSize.xy * half2(0, -1);
                o.uv[2] = uv + _MainTex_TexelSize.xy * half2(1, -1);
                o.uv[3] = uv + _MainTex_TexelSize.xy * half2(-1, 0);
                o.uv[4] = uv + _MainTex_TexelSize.xy * half2(0, 0);
                o.uv[5] = uv + _MainTex_TexelSize.xy * half2(1, 0);
                o.uv[6] = uv + _MainTex_TexelSize.xy * half2(-1, 1);
                o.uv[7] = uv + _MainTex_TexelSize.xy * half2(0, 1);
                o.uv[8] = uv + _MainTex_TexelSize.xy * half2(1, 1);

                return o;
            } 

            fixed calcLuminance(fixed4 color)
            {
                return 0.2126 * color.r + 0.7152 * color.g + 0.0722 * color.b;
            }

            half Sobel(v2f o)
            {
                half Gx[9] = {-1, -2, -1, 0, 0, 0, 1, 2, 1};
                half Gy[9] = {-1, 0, 1, -2, 0, 2, -1, 0, 1};
                half edgeX = 0;
                half edgeY = 0;
                half L;
                for (int i = 0; i < 9; i++)
                {
                    L = calcLuminance(tex2D(_MainTex, o.uv[i]));
                    edgeX += L * Gx[i];
                    edgeY += L * Gy[i];
                }

                return abs(edgeX) + abs(edgeY);
            }

            fixed4 frag (v2f i) : SV_Target
            {
                half edge = Sobel(i);

                fixed4 edgeColor = lerp(tex2D(_MainTex, i.uv[4]), _EdgeColor, edge);
                
                //只保留边缘颜色，其余颜色置为背景色
                fixed4 onlyEdgeColorWithBackground = lerp(_BackgroundColor, _EdgeColor, edge);

                return lerp(edgeColor, onlyEdgeColorWithBackground, _Background);
            }
            ENDCG
        }
    }

    Fallback Off
}
```

## 高斯模糊
### 原理
**高斯模糊**同样利用了卷积计算，它使用的卷积核名为**高斯核**。高斯核是一个正方形大小的滤波核，其中每个元素的计算都是基于下面的**高斯方程**：

$G(x, y) = \frac{1}{2\pi\sigma^2} e^{-\frac{x^2 + y^2}{2\sigma^2}}$

其中，$\sigma$是标准方差（一般取值为1），$x$和$y$分别对应了当前位置到卷积核中心的整数距离。

显然，如果直接在`Shader`中直接计算高斯方程，性能消耗极大，因此，我们可以提前计算出高斯核中各个位置坐标对应的数值：

$$
\begin{bmatrix}
0.0029 & 0.0131 & 0.0215 & 0.0131 & 0.0029 \\
0.0131 & 0.0586 & 0.0965 & 0.0586 & 0.0131 \\
0.0215 & 0.0965 & 0.1592 & 0.0965 & 0.0215 \\
0.0131 & 0.0586 & 0.0965 & 0.0586 & 0.0131 \\
0.0029 & 0.0131 & 0.0215 & 0.0131 & 0.0029
\end{bmatrix}
$$

从上述矩阵中可以看出，高斯方程很好地模拟了邻域每个像素对当前处理像素的影响程度一一距离越近，影响越大；高斯核的维度越高，模糊程度越大。但同时我们也需要注意，**高斯方程直接计算出的结果并没有经过归一化**，即系数之和不为1，**这会向图像引入额外的亮度或暗度**，因此我们需要对该矩阵进行**归一化**：

$$
\color{red}
5 \times 5 \ 高斯核 =
\begin{bmatrix}
0.0030 & 0.0133 & 0.0219 & 0.0133 & 0.0030 \\
0.0133 & 0.0596 & 0.0983 & 0.0596 & 0.0133 \\
0.0219 & 0.0983 & 0.1621 & 0.0983 & 0.0219 \\
0.0133 & 0.0596 & 0.0983 & 0.0596 & 0.0133 \\
0.0030 & 0.0133 & 0.0219 & 0.0133 & 0.0030
\end{bmatrix}
$$

但是卷积核的维度越高，所需的计算量就越大，以一个$N \times N$的高斯核为例，假设图片的宽和高为$W$和$H$，那么就需要$N \times N \times W \times H$次采样，当$N$的大小不断增大，采样次数会变得非常巨大，幸运的是，我们可以将二维高斯方程拆分成两个一维函数，从而将计算复杂度从$O(N^2)$降到了$O(N)$：

$ G(x, y) = \frac{1}{2\pi\sigma^2} e^{-\frac{x^2+y^2}{2\sigma^2}} = G(x) \cdot G(y) = \left( \frac{1}{\sqrt{2\pi}\sigma} e^{-\frac{x^2}{2\sigma^2}} \right) \cdot \left( \frac{1}{\sqrt{2\pi}\sigma} e^{-\frac{y^2}{2\sigma^2}} \right)
\\
 $

$$
\color{red}

\begin{aligned}
G(x) &= \frac{1}{\sqrt{2\pi}\sigma} e^{-\frac{x^2}{2\sigma^2}} \quad \Rightarrow \quad \begin{bmatrix} 0.0545 & 0.2442 & 0.4026 & 0.2442 & 0.0545 \end{bmatrix} \\[-5pt]
G(y) &= \frac{1}{\sqrt{2\pi}\sigma} e^{-\frac{y^2}{2\sigma^2}} \quad \Rightarrow \quad \begin{bmatrix} 0.0545 \\ 0.2442 \\ 0.4026 \\ 0.2442 \\ 0.0545 \end{bmatrix}
\end{aligned}
$$

我们分别计算出这两个一维函数各自的卷积核，$G(x)$负责水平方向的梯度计算，$G(y)$负责垂直方向的梯度计算，而后先后**使用两个`Pass`来分别完成两个方向上的滤波。

{% note info %}
之所以**不使用一个`Pass`来完成，是因为在同一个`Pass`中，我们只能对源屏幕纹理中的颜色进行采样，也就是只能对原图采样，因此**第二次一维滤波时我们并没有办法获得前一次一维滤波**的结果，因此我们需要使用两个`Pass`，这样在C#代码中，我们就可以将第一次一维滤波的结果存储在一个临时的渲染纹理中，再让第二个`Pass`采样该临时渲染纹理。

{% endnote %}

{% note info %}
我们并不需要存储完整的两个一维卷积核，因为其中的很多数值都是重复的，每种数值只需要存储一次即可，这样可以节省一些变量定义所需的的内存空间。

{% endnote %}

我们希望能够手动控制高斯模糊的强度，的确，我们可以使用维数更高的高斯核，但是这样会带来更大的计算量，因此，我们常使用以下三种方式来控制高斯模糊的强度：

{% note info %}
+ **控制源纹理大小：**我们可以**将第一个`Pass`的渲染目标设置为一个较小的渲染纹理**，以此来减少画面的信息量，即可增强模糊效果，该方法又被称为**降采样**：`Pass`的运行次数取决于输出目标（画布）的大小**，因此较小的渲染纹理减少了片元着色器的运行次数，性能消耗降低；由于输出画布小于输入纹理，因此输出画布上的每一个像素将由输入纹理中该uv坐标位置周围的几个像素进行线性插值得到。**我们常使用双线性插值`FilterMode.Bilinear`，但是**过小的纹理大小还是会导致图像像素化**；
+ **多次执行`Shader`：**我们可以在`OnRenderImage`函数中多次执行`Shader`，使其在上一次模糊的基础上再次进行采样；
+ **控制采样间隔距离：**我们不一定只采样当前像素周围的像素，例如我们可以选择`uv + float2(0, -1) * texelSize * _BlurSize`的采样方式，之前我们采样时并没有引入`_BlurSize`变量，因此默认采样间隔为1，现在我们可以通过**控制采样间隔来改变采样半径**，以此来控制模糊效果。但是过大的采样半径会导致像素与像素之间不再连续，颜色差异增大，导致出现虚影，因此采样半径不宜过大。

{% endnote %}

### 高斯模糊实现
{% note info %}
+ `CGINCLUDE`：定义一段通用的代码块，这段代码会被自动包含到该文件后续所有的`CGPROGRAM`块中。编译器会自动把`CGINCLUDE`和`ENDCG`之间的所有内容，复制粘贴到该`Shader`文件中每一个`CGPROGRAM`块的开头。

{% endnote %}

```csharp
Shader "Unlit/GaussianBlur"
{
    Properties
    {
        _MainTex ("Texture", 2D) = "white" {}
        _BlurSize ("BlurSize", Range(1, 5)) = 1
    }
    SubShader
    {
        
        Tags { "RenderType"="Opaque" }

        ZTest Always
        Cull Off
        ZWrite Off

        CGINCLUDE

        #include "UnityCG.cginc"

        sampler2D _MainTex;
        half4 _MainTex_TexelSize;
        float _BlurSize;

        struct v2f
        {
            half2 uv[5] : TEXCOORD0;
            float4 vertex : SV_POSITION;
        };

        v2f vertBlurHorizontal (appdata_base v)
        {
            v2f o;
            o.vertex = UnityObjectToClipPos(v.vertex);

            half2 uv = v.texcoord;
            o.uv[0] = uv;
            o.uv[1] = uv + half2(1,0) * _MainTex_TexelSize.x * _BlurSize;
            o.uv[2] = uv + half2(-1,0) * _MainTex_TexelSize.x * _BlurSize;
            o.uv[3] = uv + half2(2,0) * _MainTex_TexelSize.x * _BlurSize;
            o.uv[4] = uv + half2(-2,0) * _MainTex_TexelSize.x * _BlurSize;
            return o;
        }

        v2f vertBlurVertical (appdata_base v)
        {
            v2f o;
            o.vertex = UnityObjectToClipPos(v.vertex);

            half2 uv = v.texcoord;
            o.uv[0] = uv;
            o.uv[1] = uv + half2(0,1) * _MainTex_TexelSize.y * _BlurSize;
            o.uv[2] = uv + half2(0,-1) * _MainTex_TexelSize.y * _BlurSize;
            o.uv[3] = uv + half2(0,2) * _MainTex_TexelSize.y * _BlurSize;
            o.uv[4] = uv + half2(0,-2) * _MainTex_TexelSize.y * _BlurSize;
            return o;
        }

        fixed4 frag (v2f i) : SV_Target
        {
            float weight[3] = {0.4026, 0.2442, 0.0545};
            fixed4 col = tex2D(_MainTex, i.uv[0]) * weight[0] + 
                         tex2D(_MainTex, i.uv[1]) * weight[1] +
                         tex2D(_MainTex, i.uv[2]) * weight[1] +
                         tex2D(_MainTex, i.uv[3]) * weight[2] +
                         tex2D(_MainTex, i.uv[4]) * weight[2];

            return col;
        }
        ENDCG

        Pass
        {
            CGPROGRAM
            #pragma vertex vertBlurHorizontal
            #pragma fragment frag

            ENDCG
        }

        Pass
        {
            CGPROGRAM
            #pragma vertex vertBlurVertical
            #pragma fragment frag

            ENDCG
        }
    }
}
```

{% note info %}
+ `RenderTexture.GetTemporary(width, height, depthBuffer)`：**获取一个临时的`RenderTexture`对象，用来存储第一个`Pass`的结果。`depthBuffer`通常传入0，表示不需要进行深度测试。**相较于每次都创建一张纹理贴图，使用该方法可以节约内存开销。

使用该方法返回的临时纹理对象还需要使用`RenderTexture.ReleaseTemporary(对象)`来释放之前分配的缓存。

{% endnote %}

```csharp
using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class GaussianBlurTest : PostEffectBase
{
    [Range(1.0f, 5.0f)] //采样间隔
    [SerializeField] private float blurSampleRadius = 1f;

    [Range(1, 8)]   //降采样 纹理大小 = 源纹理大小/downSample
    [SerializeField] private int downSample = 1;

    [Range(0, 5)]   //迭代次数
    [SerializeField] private int iterations = 0;
    protected override void OnRenderImage(RenderTexture source, RenderTexture destination)
    {
        if(material != null)
        {
            //两种设置采样半径的方法均可
            //material.SetFloat("_BlurSize", blurSampleRadius);

            RenderTexture buffer0 = RenderTexture.GetTemporary(source.width / downSample, source.height / downSample, 0);
            buffer0.filterMode = FilterMode.Bilinear;
            Graphics.Blit(source, buffer0);

            for (int i = 0; i < iterations; i++)
            {
                //让采样半径受迭代次数的影响，这样得到的模糊效果会更加强烈
                material.SetFloat("_BlurSize", 1 + i * blurSampleRadius);

                RenderTexture buffer1 = RenderTexture.GetTemporary(source.width / downSample, source.height / downSample, 0);
                Graphics.Blit(buffer0, buffer1, material, 0);
                RenderTexture.ReleaseTemporary(buffer0);

                //引用类型传递
                buffer0 = buffer1;
                buffer1 = RenderTexture.GetTemporary(source.width / downSample, source.height / downSample, 0);
                Graphics.Blit(buffer0, buffer1, material, 1);
                RenderTexture.ReleaseTemporary(buffer0);

                //buffer1是局部变量，因此还是需要使用buffer0来保存该轮的渲染结果
                buffer0 = buffer1;

                {
                    //以下的写法同样可行 但是频繁对一个RenderTexture对象进行读写读操作容易出bug

                    //RenderTexture buffer1 = RenderTexture.GetTemporary(source.width / downSample, source.height / downSample, 0);
                    //buffer1.filterMode = FilterMode.Bilinear;

                    //Graphics.Blit(buffer0, buffer1, material, 0);
                    //Graphics.Blit(buffer1, buffer0, material, 1);

                    //RenderTexture.ReleaseTemporary(buffer1);
                }
            }
            Graphics.Blit(buffer0, destination);
            RenderTexture.ReleaseTemporary(buffer0);
        }
        else
        {
            Graphics.Blit(source, destination);
        }
    }
}
```

{% note warning %}
`BlurSize`可以是小数**，这是因为当uv坐标恰好落在两个像素对应的采样点中间时，**GPU会自动计算出当前uv坐标距离周围像素的采样点之间的距离，自动进行线性插值，**因此我们可以使用`float`类型的`BlurSize`来更加精细的控制高斯模糊的程度。

{% endnote %}

## Bloom泛光效果
### 原理
**Bloom效果**的主要目的是模拟现实世界中强光源在相机镜头或人眼中造成的**光晕或泛光现象**，使得画面中较亮的区域“扩散”到周围的区域，造成一种朦胧的效果。

Bloom的实现原理非常简单：

我们首先根据一个阀值**提取出图像中的较亮区域**，把它们**存储在一张渲染纹理中**；再利用**高斯模糊**对这张渲染纹理进行模糊处理，**模拟光线扩散**的效果；最后再**将其和原图像进行混合（加法运算）**，得到最终的效果。

亮度阈值实际上就是先前学习过的灰度值，即`L = 0.2126 * color.r + 0.7152 * color.g + 0.0722 * color.b;`，我们只需要**将每个像素的亮度与亮度阈值相减，并将结果截断到**$[0,1]$**区间即可**（Unity中RGB位于$[0,1]$区间，除非开启了HDR），这样**可以保证图像中亮度接近亮度阈值的地方不会出现明显的边缘。**

### Bloom实现
{% note warning %}
+ `UNITY_UV_STARTS_AT_TOP`：**当我们把当前画面渲染到一张临时的`RenderTexture` 中时，**在某些平台（尤其是 DirectX）上**，当开启了抗锯齿（MSAA）或者在使用特定的屏幕抓取操作时，**Unity 渲染出的这张`RenderTexture`会发生上下颠倒**。也就是当uv原点不在左下角而在左上角时，该宏返回`true`；Unity会自动修正`_MainTex`纹理，其他纹理则需要手动修正。
+ `_MainTex_TexelSize.y < 0.0`：这是 Unity 的一个特殊约定。当 Unity 发现当前的 `RenderTexture` 在当前 API 下是颠倒的时候，它会把 <font style="color:#DF2A3F;"><b>_MainTex_TexelSize.y</b></font> 设为负数，作为一个“信号”传给 `Shader`。
+ `o.uv.w = 1.0 - o.uv.w`：**由于`_Bloom`纹理可能发生$y$轴（即`w`）上下颠倒，因此`_MainTex`和`_Bloom`需要两套uv坐标进行采样。这里的 uv.zw 存储的是用于采样 _Bloom 纹理的坐标，因此`w`对应$y$轴。

{% endnote %}

```csharp
Shader "Unlit/Bloom"
{
    Properties
    {
        _MainTex ("Texture", 2D) = "white" {}
        _Bloom ("Bloom", 2D) = "" {}
        _LuminanceThreshold("LuminanceThreshold", Float) = 0.5
        _BlurSize("BlurSize", Float) = 1
    }
    SubShader
    {
        Tags { "RenderType"="Opaque" }

        ZTest Always
        Cull Off
        ZWrite Off

        CGINCLUDE

        #include "UnityCG.cginc"

        sampler2D _MainTex;
        sampler2D _Bloom;
        float _LuminanceThreshold;

        //提供给高斯模糊Pass使用
        half4 _MainTex_TexelSize;
        float _BlurSize;

        struct v2f
        {
            float2 uv : TEXCOORD0;
            float4 vertex : SV_POSITION;
        };

        fixed luminance(fixed4 color)
        {
            return 0.2126 * color.r + 0.7152 * color.g + 0.0722 * color.b;
        }

        ENDCG

        //提取亮部
        Pass
        {
            CGPROGRAM
            #pragma vertex vert
            #pragma fragment frag

            v2f vert(appdata_base v)
            {
                v2f o;
                o.vertex = UnityWorldToClipPos(v.vertex);
                o.uv = v.texcoord;

                return o;
            }

            fixed4 frag(v2f i) : SV_Target
            {
                fixed4 color = tex2D(_MainTex, i.uv);
                //使用亮度减去阈值的数值作为亮部提取的"程度"
                fixed val = saturate(luminance(color) - _LuminanceThreshold);

                return color * val;
            }
            ENDCG
        }

        //复用高斯模糊的两个Pass
        UsePass "Unlit/GaussianBlur/GAUSSIAN_BLUR_HORIZONTAL"
        UsePass "Unlit/GaussianBlur/GAUSSIAN_BLUR_VERTICAL"

        //用于合成的Pass
        Pass
        {
            CGPROGRAM
            #pragma vertex vertBloom
            #pragma fragment fragBloom

            struct v2fBloom
            {
                float4 pos : SV_POSITION;

                //xy存储源纹理 zw存储经过高斯模糊后的亮部纹理
                half4 uv : TEXCOORD0;
            };

            v2fBloom vertBloom(appdata_base v)
            {
                v2fBloom o;
                o.pos = UnityWorldToClipPos(v.vertex);
                o.uv.xy = v.texcoord;
                o.uv.zw = v.texcoord;

                #if UNITY_UV_STARTS_AT_TOP
                if(_MainTex_TexelSize.y < 0)
                    o.uv.w = 1 - o.uv.w;
                #endif

                return o;
            }

            fixed4 fragBloom(v2fBloom i) : SV_Target
            {
                return tex2D(_MainTex, i.uv.xy) + tex2D(_Bloom, i.uv.zw);
            }

            ENDCG
        }
    }
}

```

```csharp
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class BloomTest : PostEffectBase
{
    #region 提取亮部
    [Range(0f, 4f)]
    [SerializeField] private float luminanceThreshold = 1f;
    #endregion

    #region 高斯模糊
    [Range(1.0f, 5.0f)] //采样间隔
    [SerializeField] private float blurSampleRadius = 1f;

    [Range(1, 8)]   //降采样 纹理大小 = 源纹理大小/downSample
    [SerializeField] private int downSample = 1;

    [Range(0, 5)]   //迭代次数
    [SerializeField] private int iterations = 0;
    #endregion

    protected override void OnRenderImage(RenderTexture source, RenderTexture destination)
    {
        if (material != null)
        {
            material.SetFloat("_LuminanceThreshold", luminanceThreshold);

            //设置高斯模糊纹理缩放
            RenderTexture brightArea = RenderTexture.GetTemporary(source.width / downSample, source.height / downSample, 0);
            //提取亮部
            Graphics.Blit(source, brightArea, material, 0);

            #region 高斯模糊
            brightArea.filterMode = FilterMode.Bilinear;

            for (int i = 0; i < iterations; i++)
            {
                //让采样半径受迭代次数的影响，这样得到的模糊效果会更加强烈
                material.SetFloat("_BlurSize", 1 + i * blurSampleRadius);

                RenderTexture buffer1 = RenderTexture.GetTemporary(source.width / downSample, source.height / downSample, 0);
                Graphics.Blit(brightArea, buffer1, material, 1);
                RenderTexture.ReleaseTemporary(brightArea);

                //引用类型传递
                brightArea = buffer1;
                buffer1 = RenderTexture.GetTemporary(source.width / downSample, source.height / downSample, 0);
                Graphics.Blit(brightArea, buffer1, material, 2);
                RenderTexture.ReleaseTemporary(brightArea);

                //buffer1是局部变量，因此还是需要使用brightArea来保存该轮的渲染结果
                brightArea = buffer1;
            }
            //高斯模糊的结果位于brightArea中
            #endregion

            //向Shader提供经过高斯模糊处理过后的亮部区域
            material.SetTexture("_Bloom", brightArea);
            RenderTexture.ReleaseTemporary(brightArea);

            //此时的shader已经获取到了所有所需的属性
            //我们可以直接将源纹理传入，并调用最后一个Pass进行合成操作
            Graphics.Blit(source, destination, material, 3);
        }
        else
        {
            Graphics.Blit(source, destination);
        }
    }
}
```

## 运动模糊
### 原理
当一个物体以较高速度移动时，由于人眼或摄像机的曝光时间过长，该物体会在图像中留下模糊的运动轨迹。这种效果游戏、动画、电影中被广泛应用，以增加视觉真实性和动感。**运动模糊**效果可以让物体运动看起来更加真实平滑，但在计算机产生的图像中，由于不存在曝光这一物理现象，渲染出来的图像往往都棱角分明，缺少运动模糊。

运动模糊的实现有多种方法。一种实现方法是利用一块**累积缓存（accumulation buffer）**来混合多张连续的图像。**当物体快速移动产生多张图像后，我们取它们之间的平均值作为最后的运动模糊图像。**然而，这种暴力的方法对**性能的消耗很大**，因为想要获取多张帧图像往往意味着我们需要在同一帧里渲染多次场景。另一种应用广泛的方法是创建和使用**速度缓存（velocity buffer）**，这个缓存中**存储了各个像素当前的运动速度，然后利用该值来决定模糊的方向和大小。**

在本节中，我们将**使用类似上述第一种方法**的实现来模拟运动模糊的效果。我们**不需要在一帧中把场景渲染多次，但需要保存之前的渲染结果，不断把当前的渲染图像叠加到之前的渲染图像中**，从而产生一种运动轨迹的视觉效果。这种方法与原始的利用累计缓存的方法相比**性能更好**，但**模糊效果可能会略有影响**。

在使用`Graphics.Blit(源纹理，目标纹理，材质)`方法时，我们可以**将目标纹理看做颜色缓冲区**，即如果目标纹理中包含内容，则**目标纹理中的颜色为颜色缓冲区中的颜色**。因此我们完全可以利用该方法，配合`Shader`代码将两张图片信息进行混合处理，从而实现运动模糊效果。它的主要混合思路是使用两个`Pass`：

+ 第一个`Pass`只**负责混合RGB通道**，同时根据模糊程度决定混合的比例；

{% note warning %}
混合比例通过`Blend ArcAlpha OneMinusSrcAlpha`控制，即**通过第一个`Pass`的片元着色器返回的透明度`_BlurAmount`来控制混合的比例。**

假设混合比例`_BlurAmount`为10%，即每一次都只保留当前画面的10%，则：

$\text{最终颜色} = \text{当前画面} \times 10\% + \text{颜色缓冲区} \times 90\%$

渲染下一帧时，我们又可以得到：

$$
\begin{aligned}
\text{最终颜色} &= \text{当前画面} \times 10\% + (\text{上一帧画面} \times 10\%  + \text{上一帧的颜色缓冲区} \times 90\% )\times 90\% \\[10pt]
&= \text{当前画面} \times 10\% + {\color{red}(\text{上一帧画面} \times 10\% \times 90\%)} + ...
\end{aligned}
$$

从中可以看出，每一帧在后续渲染中的留存值为$\_{BlurAmount} \times 0.9^n$，其中$n$表示后续渲染的总帧数，**因此每一帧在画面中的留存部分将会不断减少，形成类似淡出的效果，即运动模糊的“残影”来源。**

{% endnote %}

+ 第二个`Pass`只**负责将A通道设置为当前采样的屏幕纹理的A通道**。

{% note warning %}
屏幕纹理的透明度实际上和屏幕上的物体透明度有关，即**半透明物体所在区域的屏幕纹理区域的透明度不为1**，因此我们需要**使用第二个`Pass`来不断强制更新运动模糊的结果的透明度，使其与当前采样得到的屏幕纹理的透明度保持一致**。

{% endnote %}

### 运动模糊实现
在编辑器中观察运动模糊，残影可能不会迅速消失，原因在于**编辑器模式下帧率较低**，运行后即可看到正常的效果。

{% note warning %}
我们在**运动模糊实现**的时候常常会**避免背景是天空盒**，因为**天空盒的透明度为0**，**物体在经过背景是天空盒的位置时**<font style="color:#DF2A3F;"><b>会留下无法消除的残影</b></font>，原因在于当物体离开以天空盒为背景的区域时，第二个`Pass`会将该位置的透明度更新为0（天空盒），而`Graphics.Blit`函数为了节省性能，并不会绘制透明度为0的区域**，因此背景为天空盒的区域像素将不会更新，始终保留物体的残影。

{% endnote %}

```csharp
Shader "Unlit/MotionBlur"
{
    Properties
    {
        _MainTex ("Texture", 2D) = "white" {}
        _BlurAmount ("_BlurAmount", Float) = 0.5
    }
    SubShader
    {
        Tags { "RenderType"="Opaque" }

        ZTest Always
        Cull Off
        ZWrite Off

        CGINCLUDE
        #include "UnityCG.cginc"

        sampler2D _MainTex;
        float _BlurAmount;

        struct v2f
        {
            float2 uv : TEXCOORD0;
            float4 vertex : SV_POSITION;
        };

        v2f vert (appdata_base v)
        {
            v2f o;
            o.vertex = UnityObjectToClipPos(v.vertex);
            o.uv = v.texcoord;

            return o;
        }

        ENDCG

        //1. 用于混合RGB通道
        Pass
        {
            Blend SrcAlpha OneMinusSrcAlpha
            ColorMask RGB

            CGPROGRAM
            #pragma vertex vert
            #pragma fragment fragRGB

            fixed4 fragRGB (v2f i) : SV_Target
            {
                fixed3 col = tex2D(_MainTex, i.uv).rgb;

                return fixed4(col, _BlurAmount);
            }
            ENDCG
        }

        //2. 用于覆写A通道
        Pass
        {
            Blend One Zero
            ColorMask A

            CGPROGRAM
            #pragma vertex vert
            #pragma fragment fragA

            fixed4 fragA (v2f i) : SV_Target
            {
                fixed4 col = tex2D(_MainTex, i.uv);

                return col;
            }
            ENDCG
        }
    }
}
```

{% note warning %}
之所以**不使用`RenderTexture.GetTemporary`，而是直接声明一个`RenderTexture`用来存储之前的渲染结果，是因为**前者的生命周期只在1帧内，无法做到跨帧传递数据。**

{% endnote %}

```csharp
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class MotionBlurTest : PostEffectBase
{
    //显然当Shader中_BlurAmount = 0时，当画面留存比例为0%
    //此时画面将不再更新，我们需要避免这种情况
    [Range(0f, 0.9f)]
    [SerializeField] private float blurAmount = 0.5f;

    private RenderTexture accumulationTex;

    protected override void OnRenderImage(RenderTexture source, RenderTexture destination)
    {
        if(material != null)
        {
            //初始化 或 屏幕分辨率变化引起的重新初始化
            if( accumulationTex == null ||
                accumulationTex.width != source.width ||
                accumulationTex.height != source.height)
            {
                DestroyImmediate(accumulationTex);

                accumulationTex = new RenderTexture(source.width, source.height, 0);
                //我们不需要让accumulationTex显示在层级中，也不需要保存在场景中
                accumulationTex.hideFlags = HideFlags.HideAndDontSave;
                //由于后续计算中，我们需要将累积纹理中的内容作为颜色缓冲区参与计算
                //因此在初始化时累积纹理中应具有当前帧的屏幕纹理
                Graphics.Blit(source, accumulationTex);
            }
            //我们希望模糊程度和blurAmount成正比
            material.SetFloat("_BlurAmount", 1f - blurAmount);
            //按序执行两个Pass
            Graphics.Blit(source, accumulationTex, material);

            Graphics.Blit(accumulationTex, destination);
        }
        else
        {
            Graphics.Blit(source, destination);
        }
    }

    private void OnDisable()
    {
        DestroyImmediate(accumulationTex);
    }
}
```

# 使用深度和法线纹理
之前我们学习的屏幕后处理效果都只是在屏幕颜色图像上进行各种操作来实现的。然而，很多时候我们不仅需要当前屏幕的颜色信息，还**希望得到深度和法线信息**。例如，**在进行边缘检测时，直接利用颜色信息会使检测到的边缘信息受物体纹理和光照等外部因素的影响，得到很多我们不需要的边缘点。**一种更好的方法是，我们可以在深度纹理和法线纹理上进行边缘检测，这些图像不会受纹理和光照的影响，而仅仅保存了当前渲染物体的模型信息，通过这样的方式检测出来的边缘更加可靠。

+ 屏幕空间深度纹理：用于存储屏幕图像中每个像素深度信息的纹理
+ 屏幕空间法线纹理：用于存储屏幕图像中每个像素法线信息的纹理

## 获取深度和法线纹理
我们需要让Unity知道我们需要使用深度纹理和法线纹理，我们可以使用C#代码来设置`Camera`组件的`depthTextureMode`枚举类型即可：

```csharp
private void Start()
{
    //获取深度纹理 (一张纹理)
    Camera.main.depthTextureMode = DepthTextureMode.Depth;

    //获取深度+法线纹理 (一张纹理)
    Camera.main.depthTextureMode = DepthTextureMode.DepthNormals;

    //获取深度纹理 和 深度+法线纹理 (两张纹理)
    Camera.main.depthTextureMode = DepthTextureMode.Depth | DepthTextureMode.DepthNormals;
}
```

{% note warning %}
在内置渲染管线中，Unity没有单独的法线纹理，只有“深度+法线”纹理；在URP中有单独的法线纹理。

{% endnote %}

	而后，我们可以在`Shader`中直接声明对应变量`sampler2D **_CameraDepthTexture**;``sampler2D **_CameraDepthNormalsTexture**;`（一般RG通道存储法线，BA通道存深度）**，同时**该C#脚本会自动在`Inspector`窗口中生成一个获取`Shader`的区域，我们将声明了上述变量的`Shader`提供给该脚本即可获取。**

在获取到了深度和法线纹理之后，我们还需要对它们采样才能够获得深度值和法线值：

+ **深度值采样：**

```csharp
fixed4 frag (v2f i) : SV_Target
{
    // 使用基本深度纹理采样 得到的结果是非线性的
    float depth = SAMPLE_DEPTH_TEXTURE(_CameraDepthTexture, i.uv);
    
    // 将非线性的深度值 转换到观察空间下 (返回的是实际距离，单位通常为米)
    float viewDepth = LinearEyeDepth(depth);
    
    // 将非线性的深度值 转换到 [0, 1] 区间内的线性深度值
    float linearDepth = Linear01Depth(depth);

    // 示例：返回线性深度作为颜色显示
    return fixed4(linearDepth, linearDepth, linearDepth, 1.0);
}
```

{% note info %}
由于在某些平台上（例如PSP2和PS3）直接使用`tex2D`函数对深度纹理采样会出现问题，因此Unity为我们提供了SAMPLE_DEPTH_TEXTURE宏来自动处理平台间的差异。

{% endnote %}

{% note warning %}
之所以**直接对深度纹理采样得到的结果是非线性的**，是因为**深度纹理来自于顶点变换后的NDC坐标空间的**$Z$**分量（即下面的**$z/w$**）**：

（由于$Z$分量位于$[-1,1]$，而纹理使用$[0,1]$区间存储，因此Unity会使用$0.5 \times Z + 0.5$进行转换以得到最终的深度值。）

我们在**顶点着色器中将顶点变换到了裁剪空间**，而后**Unity又会将裁剪空间变换到NDC坐标空间**，即对视椎体进行透视除法，“压缩”成一个单位长度的正方体，其中由**裁剪空间（投影空间）变换矩阵**可以得到：$z = \frac{Far}{Far - Near} \cdot z_{view} - \frac{Far \cdot Near}{Far - Near}$，$w = z_{view}$，而我们在NDC空间中得到的最终深度为透视除法的结果，即$z/w$，显然$w$位于分母上，因此$z$与$w$成反比，而$w$表示物体距离摄像机的真实距离，因此$z/w$在$w$较小，即离摄像机较近时变化快，离摄像机较远时变化慢，因此我们得到的深度纹理中的深度值并不是线性变化的，因此我们需要进一步处理。

+ `LinearEyeDepth`：将深度值反变换到观察空间下，即**对上述非线性的投影空间变换矩阵进行反变换**，这样就抵消了非线性的影响，得到的结果为顶点在观察空间下的$z$坐标；
+ `Linear01Depth`：该函数通过一些数学手段恢复了深度值在$[0,1]$区间内的线性比例。

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/63937386/1772716459634-26a7f04a-79d7-451f-908d-878eefa97d63.png)

{% endnote %}

+ **法线信息采样：**

{% note info %}
**法线纹理中的信息是**<font style="color:#DF2A3F;"><b>观察空间下的法线</b></font>从$[-1,1]$区间变换到纹理的$[0,1]$之后的结果，转换公式为$(\text{观察空间下法线}+1) \times 0.5$。

{% endnote %}

```csharp
fixed4 frag (v2f i) : SV_Target
{
    // 用于存储深度值的变量
    float depth;
    // 用于存储法线的变量
    float3 normals;

    // 对深度+法线纹理进行采样 (其中xy是法线信息，zw是深度信息)
    float4 depthNormal = tex2D(_CameraDepthNormalsTexture, i.uv);

    // UnityCG.cginc 内置文件中的方法 用于得到深度值(0~1)和法线信息(观察空间下)
    // 相当于一次处理深度和法线
    DecodeDepthNormal(depthNormal, depth, normals);

    // --- 以下是可选的单独解码方式 ---

    // 单独得到深度 (从 zw 分量解码)
    depth = DecodeFloatRG(depthNormal.zw);

    // 单独得到法线 (从 xy 分量解码)
    normals = DecodeViewNormalStereo(depthNormal);
    
    // 示例：返回颜色（这里仅作占位，实际逻辑根据需求编写）
    return fixed4(normals, 1.0);
}
```

	深度和法线纹理的获取有以下两种方式：一是延迟渲染路径中的`G-Buffer`缓冲区，二是使用一个单独的`Pass`渲染得到的：

+ 当我们**只需要一张单独的深度纹理**时，Unity会直接获取`G-Buffer`，或者使用着色器替换技术，寻找所有`"RenderType" = "Opaque"`且渲染队列小于等于2500（`Background=1000``Geometry=2000``AlphaTest=2450`）的物体，并使用他们的`ShadowCaster Pass`来得到**深度纹理（即阴影映射纹理）**，**<u>因此我们必须为物体设置正确的</u>`<u>RenderType</u>`<u>标签，并且必须有</u>`<u>ShadowCaster Pass</u>`
+ 当我们选择**生成深度+法线纹理**时，Unity 会创建一张和屏幕分辨率相同、精度为32位（每个通道为8位）的纹理，其中观察空间下的法线信息会被编码进纹理的R和G通道，而深度信息会被编码进B和A通道。法线信息的获取在延迟渲染中是可以非常容易就得到的，Unity只需要合并深度和法线缓存即可。而在**前向渲染**中，默认情况下是不会创建法线缓存的，因此**Unity底层使用了一个单独的`Pass`把整个场景再次渲染一遍**来完成。这个`Pass`被包含在Unity内置的一个`Unity Shader`中,我们可以在内置的`builtin_shaders-xxx/DefaultResources/Camera-DepthNormalTexture.shader`文件中找到这个用于渲染深度和法线信息的`Pass`。

{% note warning %}
显然深度+法线纹理的精度较低，因为每个纹理只能使用16位的精度。

{% endnote %}

{% note warning %}
`DecodeFloatRG`将会自动调用`Linear01Depth`将结果线性化。

{% endnote %}

{% note info %}
+ `DecodeDepthNormal`：**相当于在内部执行了`DecodeFloatRG`和`DecodeViewNormalStereo`
+ `DecodeViewNormalStereo`会自动将法线从$[0,1]$转换到$[-1,1]$

{% endnote %}

## 查看深度纹理信息
越靠近近裁剪平面，深度值越接近0为黑色，越靠近远裁剪平面为白色。

```csharp
Shader "Unlit/GetDepthTexture"
{
    Properties
    {
        _MainTex ("Texture", 2D) = "white" {}
    }
    SubShader
    {
        Pass
        {
            CGPROGRAM
            #pragma vertex vert
            #pragma fragment frag

            #include "UnityCG.cginc"

            struct v2f
            {
                float2 uv : TEXCOORD0;
                float4 vertex : SV_POSITION;
            };

            sampler2D _MainTex;
            float4 _MainTex_ST;
            sampler2D _CameraDepthTexture;

            v2f vert (appdata_base v)
            {
                v2f o;
                o.vertex = UnityObjectToClipPos(v.vertex);
                o.uv = TRANSFORM_TEX(v.texcoord, _MainTex);
                return o;
            }

            fixed4 frag (v2f i) : SV_Target
            {
                float depth = SAMPLE_DEPTH_TEXTURE(_CameraDepthTexture, i.uv);
                fixed linearDepth = Linear01Depth(depth);
                return fixed4(linearDepth, linearDepth, linearDepth, 1);
            }
            ENDCG
        }
    }
}

```

```csharp
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class GetDepthTexture : PostEffectBase
{
    private void Start()
    {
        Camera.main.depthTextureMode = DepthTextureMode.Depth;
    }
}
```

## 查看法线纹理信息
```csharp
Shader "Unlit/GetNormalTexture"
{
    Properties
    {
        _MainTex ("Texture", 2D) = "white" {}
    }
    SubShader
    {
        Pass
        {
            CGPROGRAM
            #pragma vertex vert
            #pragma fragment frag

            #include "UnityCG.cginc"

            struct v2f
            {
                float2 uv : TEXCOORD0;
                float4 vertex : SV_POSITION;
            };

            sampler2D _MainTex;
            float4 _MainTex_ST;
            sampler2D _CameraDepthNormalsTexture;

            v2f vert (appdata_base v)
            {
                v2f o;
                o.vertex = UnityObjectToClipPos(v.vertex);
                o.uv = TRANSFORM_TEX(v.texcoord, _MainTex);
                return o;
            }

            fixed4 frag (v2f i) : SV_Target
            {
                float depth;
                float3 normals;
                float4 depthNormal = tex2D(_CameraDepthNormalsTexture, i.uv);
                DecodeDepthNormal(depthNormal, depth, normals);

                //单独得到深度
                //depth = DecodeFloatRG(depthNormal.zw);
                //单独得到法线
                //normals = DecodeViewNormalStereo(depthNormal);
                return fixed4(normals * 0.5 + 0.5, 1);
            }
            ENDCG
        }
    }
}
```

```csharp
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class GetNormalTexture : PostEffectBase
{
    private void Start()
    {
        Camera.main.depthTextureMode = DepthTextureMode.DepthNormals;
    }
}
```

## 深度纹理实现运动模糊
### 原理
在14.8节中，我们讲到实现运动模糊有两种方法，一是使用累积缓存，我们在14.8节中使用的就是类似的方法；二是使用速度缓存，本节中我们将结合深度纹理来实现基于速度缓存的运动模糊。

**我们需要获取每个像素的移动速度，并使用该速度乘以用于控制采样距离的`_BlurSize`在屏幕纹理中多次采样取平均值即可。**

实现该种运动模糊的关键在于获取每个像素的移动速度，我们的确可以先获得场景中每个物体的速度，并将他们渲染到一张速度映射图中，但这需要修改场景中所有物体的`Shader`，因此我们将使用以下的方法来代替：

获取像素运动速度的关键在于获取像素对应的世界空间中的顶点位置，而由15.1节可知，深度纹理是NDC空间坐标的$Z$值进行$\bf{Z \times 0.5 + 0.5}$变换后的结果，我们可以使用$\color{red}观察空间变换矩阵 \times 裁剪空间变换矩阵$的**逆矩阵对顶点在NDC空间的坐标进行反变换，即可获得世界空间中的顶点坐标**，但我们还缺少NDC空间的$XY$坐标，而纹理的uv坐标与NDC坐标空间存在着明显的线性映射关系：前者的取值范围为$[-1,1]$，后者为$[0,1]$，因此**我们可以通过**$uv \times 2 - 1$**来获得NDC的**$XY$**坐标，并与深度纹理中的**$Z$**坐标结合成完整的NDC坐标**，参与上述反变换。

{% note info %}
**完整的NDC空间**$\rightarrow$**世界空间的变换如下**：Unity为我们提供了观察空间和裁剪空间的变换矩阵，因此我们可以将他们相乘并取逆矩阵，但是我们原先从裁剪空间变换到NDC空间时，我们是将裁剪空间中的$xyz$坐标统一除以$w$进行**透视除法**得到的，因此**理论上在进行上述反变换前，我们还需要将NDC空间中的**$XYZ$**坐标乘以**$w$**才能获得裁剪空间中的坐标**，并使用裁剪空间中的坐标参与反变换。但问题在于我们只能获得NDC中的$XYZ$坐标，无法获得裁剪空间中的$w$坐标，因此我们选择直接使用NDC空间中的$XYZ$坐标参与反变换，并制定NDC坐标的$W=1$，这样**在经过**_**观察*裁剪**_**反变换之后，获得的世界空间坐标的**$w'$**即为原先在裁剪空间中的**$w$**的倒数**，因此我们**只要将结果的**$x'y'z'$**全部除以**$w'$**，相当于乘以了**$w$**，即可获得正确结果。**

{% endnote %}

**	**得到了该顶点在世界空间中的坐标之后，我们就可以使用<font style="color:#DF2A3F;"><b>上一帧</b></font>的$\color{red}观察空间变换矩阵 \times 裁剪空间变换矩阵$对它进行正变换，得到该顶点在前一帧的NDC空间坐标，然后我们就可以**将两帧坐标相减**，得到该像素在画面上移动的速度（`float2`）。

{% note info %}
由这一步可知，<font style="color:#DF2A3F;"><b>这种运动模糊的实现方式只适用于场景中的物体静止，只有摄像机运动的情况</b></font>，如果摄像机静止而场景中的物体移动，我们是无法看到运动模糊的效果的，原因在于我们只对每一帧的像素使用_**观察*裁剪**_的逆矩阵求得世界坐标，又使用上一帧的_**观察*裁剪**_矩阵将它变换会NDC空间，在这个过程中变量只有_**观察*裁剪**_矩阵，而忽略了世界空间坐标的位移，由于_**<u>观察*裁剪矩阵</u>**_<u>只和摄像机在世界空间中的坐标有关</u>，因此当摄像机静止时，_**观察*裁剪矩阵**_不会发生变化，因此速度差始终为0.

{% endnote %}

### 实现
由于`ShaderLab Properties`中并没有矩阵类型的变量，而我们又需要从C#代码中传入摄像机的_**观察*裁剪**_矩阵，因此实际上我们只需要在`CG`语句中声明矩阵变量即可，同样可以通过C#传入，而无需在`Properties`中声明。

```csharp
Shader "Unlit/MotionBlurWithDepthTexture"
{
    Properties
    {
        _MainTex ("Texture", 2D) = "white" {}
        _BlurSize ("_BlurSize", Float) = 0.5
    }
    SubShader
    {
        ZTest Always
        Cull Off
        ZWrite Off

        Pass
        {
            CGPROGRAM
            #pragma vertex vert
            #pragma fragment frag

            #include "UnityCG.cginc"

            struct v2f
            {
                float2 uv : TEXCOORD0;
                float2 uv_depth : TEXCOORD1;
                float4 vertex : SV_POSITION;
            };

            sampler2D _MainTex;
            half4 _MainTex_TexelSize;
            fixed _BlurSize;
            sampler2D _CameraDepthTexture;
            float4x4 _ClipToWorldMatrix;
            float4x4 _PrevWorldToClipMatrix;

            v2f vert (appdata_base v)
            {
                v2f o;
                o.vertex = UnityObjectToClipPos(v.vertex);
                o.uv = v.texcoord;
                o.uv_depth = v.texcoord;

                //防止不同平台间的差异导致v轴方向相反
                #if UNITY_UV_STARTS_AT_TOP
                    if(_MainTex_TexelSize.y < 0)
                        o.uv_depth.y = 1 - o.uv_depth.y;
                #endif
                return o;
            }

            fixed4 frag (v2f i) : SV_Target
            {
                float depth = SAMPLE_DEPTH_TEXTURE(_CameraDepthTexture, i.uv_depth);

                float4 nowClipPos = float4(i.uv.x*2-1, i.uv.y*2-1, depth*2-1, 1);

                float4 worldPos = mul(_ClipToWorldMatrix, nowClipPos);
                worldPos /= worldPos.w;

                float4 oldClipPos = mul(_PrevWorldToClipMatrix, worldPos);
                //变换回NDC空间
                oldClipPos /= oldClipPos.w;

                //注意我们的速度应该在uv坐标下的[0,1]区间中
                //而NDC坐标位于[-1,-1]区间，因此要除以2
                float2 velocity = (nowClipPos.xy - oldClipPos.xy) / 2;

                fixed2 uv = i.uv;
                fixed4 col = fixed4(0,0,0,0);
                for (int it = 0; it < 3; it++)
                {
                    col += tex2D(_MainTex, uv);
                    uv += velocity * _BlurSize;
                }
                col /= 3;

                return col;
            }
            ENDCG
        }
    }
}

```

{% note danger %}
+ `uv_depth`：**由于我们这里**需要将uv变换到世界空间**中，而且**Unity不会自动判断并修复除主纹理以外的其他纹理的v轴方向**，因此我们需要为**深度纹理**手动区分不同平台间v轴方向的差异，**否则变换得到的世界空间坐标就会是错误的**，因此我们需要使用`UNITY_UV_STARTS_AT_TOP`进行判断，并使用修正后的`uv_depth`单独对深度纹理采样，**Unity已经将`o.uv`和`_MainTex`的方向进行修正过了**，因此我们需要额外定义`o.uv_depth`用于对深度纹理采样。

{% endnote %}

```csharp
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class MotionBlurWithDepthTextureTest : PostEffectBase
{
    [Range(0.0f, 1.0f)]
    [SerializeField] private float blurSize = 0.5f;

    private Matrix4x4 prevWorldToClipMatrix;

    //在脚本激活时进行初始化
    private void OnEnable()
    {
        Camera.main.depthTextureMode = DepthTextureMode.Depth;
        prevWorldToClipMatrix = Camera.main.projectionMatrix * Camera.main.worldToCameraMatrix;
    }

    protected override void OnRenderImage(RenderTexture source, RenderTexture destination)
    {
        if(material != null)
        {
            material.SetFloat("_BlurSize", blurSize);
            material.SetMatrix("_PrevWorldToClipMatrix", prevWorldToClipMatrix);
            //计算当前帧的裁剪空间变换矩阵
            Matrix4x4 currWorldToClipMatrix = Camera.main.projectionMatrix * Camera.main.worldToCameraMatrix;
            //保留当前帧的裁剪空间变换矩阵 用于下一帧
            prevWorldToClipMatrix = currWorldToClipMatrix;
            //传入逆矩阵
            material.SetMatrix("_ClipToWorldMatrix", currWorldToClipMatrix.inverse);
            
            Graphics.Blit(source, destination, material);
        }
        else
        {
            Graphics.Blit(source, destination);
        }
    }
}

```

+ `Camera.main.projectionMatrix`：投影（裁剪）变换矩阵；
+ `Camera.main.worldToCameraMatrix`：视角（观察）变换矩阵。
+ `.inverse`：逆矩阵。

## 全局雾效
### Unity中的雾效参数
Unity自带的全局雾效可通过`Window->Rendering->Lighting`窗口中的`Environment`页签中开启，同时场景中的物体的`Shader`必须添加以下代码：

+ 编译指令`#pragma multi_compile_fog`；
+ 内置文件`#include "UnityCG.cginc"`；
+ `v2f`结构体中需要加入用于计算雾效坐标信息(通常是计算深度信息)的宏`UNITY_FOG_COORDS(数字)`，括号中需要填入下一个可用的`TEXCOORD`寄存器序号；
+ 顶点着色器中需要加入用于计算雾效数据的宏`UNITY_TRANSFER_FOG( v2f结构体, v2f结构体.vertex);`
+ 片元着色器中需要加入应用雾效的宏`UNITY_APPLY_FOG(v2f结构体.fogCoord, 原始颜色);`

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/63937386/1773050719420-fbf22a38-4e88-4a93-a5c6-f82d1a4521c6.png)

其中，`Mode`决定了雾的雾效系数（**能见度**）$f$，作为混合原始颜色（物体的颜色）和雾的颜色的混合系数：

$\color{red}最终的颜色 = （1-f）\times 雾的颜色 + f \times 原始颜色$

**雾效系数**$f$**越小，雾的颜色在最终的颜色中的占比就越大，能见度越低，雾就越浓。**

雾效系数$f$的计算公式分为`Mode`中的`Linear`(**线性**)、`Exponential`(**指数**)、`Exponential Squared`(**指数的平方**)三种，记$z$为观察空间下的$z$轴绝对值：

+ `Linear`：$f = \frac{d_{max} - |z|}{d_{max} - d_{min}}$，其中$d_{max}$和$d_{min}$分别表示受雾影响的最小距离和最大距离；

{% note danger %}
当$|z|=d_{max}$时，$f=0$，此时能见度为0，即完全呈现雾的颜色，因此**在雾的起点**$start$**处，能见度为1，在雾的“终点”**$end$**处，能见度为0。**

{% endnote %}

+ `Exponential`：$f = e^{-d \cdot |z|}$，其中$d$为控制雾的浓度的参数；
+ `Exponential Squared`：$f = e^{-(d \cdot |z|)^2}$，其中$d$为控制雾的浓度的参数，又称为指数雾的浓度参数（**Density**）。

但是这种方法的缺点在于，我们不仅**需要为场景中所有物体添加相关的渲染代码**，而且能够**实现的效果也非常有限：Unity自带的全局雾效只会随着顶点在观察空间中的**$z$**值的大小而变化**，即在同一个垂直平面上，雾效的效果是完全一致的，因此当我们需要对雾效进行一些个性化操作时，例如使用基于高度的雾效等，仅仅使用Unity内置的雾效就变得不再可行，因此，我们将使用基于屏幕后处理和深度纹理的全局雾效。

### 基于深度纹理的全局雾效
#### 原理
上面提到，物体的深度$|z|$越大，能见度$f$就越小，物体的颜色就会更多的被雾的颜色所覆盖，因此我们可以尝试用与实现运动模糊相近的方式，同样利用视角*投影矩阵将像素变换到世界空间中，但是**在片元着色器中进行矩阵乘法会导致大量的性能消耗**，因此我们将使用以下的方式来获得像素在世界空间中的坐标：

{% note danger %}
之所以**不直接使用`LinearEyeDepth`和`Linear01Depth`，是因为这样的话我们同样只能根据像素的$z$值来计算雾效，**效果和Unity内置的雾效没有什么区别**，但是当我们获得了像素在世界空间下的坐标，我们就能**计算出每个像素与摄像机之间的物理距离，计算出的雾效就会更加可控与逼真。**

{% endnote %}

	由于我们的已知量只有像素在深度纹理中的深度值，我们使用`LinearEyeDepth`函数将其转换到观察空间，这样一来，由于观察空间是世界空间的子空间，因此我们可以**将该深度看做世界空间下相对于摄像机的偏移量**，但是获得的深度只是**像素所在平面距离摄像机的距离**，**并非像素与摄像机间的距离（欧氏距离）**，因此，我们可以想办法<font style="color:#DF2A3F;"><b>求出在不同方向上像素与摄像机的欧氏距离和深度</b></font>$z$<font style="color:#DF2A3F;"><b>值之间的比例关系</b></font>，即可求得像素与摄像机之间的欧氏距离：

$\color{red}\text{像素与摄像机间的物理距离} = linearDepth \times 方向向量 \times \frac{distance}{depth}$

	因此，我们可以**将上述结果看做像素在世界空间下相对于摄像机的偏移量**，计算出像素在世界空间中的坐标，即：

$\color{red}\text{像素在世界空间中的坐标} = 摄像机世界坐标 + 像素与摄像机间的物理距离$

显然**关键在于求出不同方向上的像素与摄像机的欧氏距离与观察空间深度**$z$**的比例关系**，即$\color{red}方向向量 \times \frac{distance}{depth}$，我们**将这个向量记为**$\color{red}Ray$，虽然我们不能直接求出世界空间中任意点的`Ray`，但是**近裁剪平面的四个角的顶点处的`Ray`很容易就能被求出来：<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/63937386/1773063079170-2f400ebb-6cc2-43db-9b70-74fab68de7c7.png)

为了方便计算，我们**先计算两个辅助向量**：记$toTop$和$toRight$分别为从近裁剪平面中心指向（摄像机）正上方和正右方的向量，则：

$$
\begin{aligned}
\text{halfHeight} &= \text{Near} \times \tan \left( \frac{\text{FOV}}{2} \right) \\
\text{toTop} &= \text{camera.up} \times \text{halfHeight} \\
\text{toRight} &= \text{camera.right} \times \text{halfHeight} \times \text{aspect}
\end{aligned}
$$

其中，$halfHeight$为近裁剪平面高度的一半，$aspect$为屏幕的宽高比，$camera.up$和$camera.right$分别指向摄像机的正上方和正右方。

得到$toTop$和$toRight$之后，我们就可以**通过向量的矢量加减法获得近裁剪平面四个角的顶点处相对于摄像机的向量**了：

$$
\begin{aligned}
左上角 \ TL &= \text{camera.forward} \times \text{Near} + \text{toTop} - \text{toRight} \\
左下角 \ TR &= \text{camera.forward} \times \text{Near} + \text{toTop} + \text{toRight} \\
右上角 \ BL &= \text{camera.forward} \times \text{Near} - \text{toTop} - \text{toRight} \\
右下角 \ BR &= \text{camera.forward} \times \text{Near} - \text{toTop} + \text{toRight}
\end{aligned}
$$

此时，由于$TL$$TR$$BL$$BR$**四个向量的长度等于四个顶点与摄像机间的距离**，同时**四个顶点的**$z$**值深度等于近裁剪平面与摄像机间的距离**，均为已知量，因此我们可以**求出这四个向量方向上的像素与摄像机的欧式距离**$dist$**和观察空间深度**$depth$**之间的关系**，以$TL$为例：

$\frac{depth}{dist} = \frac{Near}{|TL|}$

我们将该式带入${Ray}_{TL} = 方向向量 \times \frac{distance}{depth}$中得：

${Ray}_{TL} = \frac{TL}{|TL|} \times \frac{distance}{depth} = \frac{TL}{|TL|} \times \frac{|TL|}{Near}  = \overrightarrow{\bf{TL}} \times \frac{|TL|}{Near}= \frac{TL}{Near}$

同理可得：

${Ray}_{TR} = \overrightarrow{\bf{TR}} \times \frac{|TR|}{Near}= \frac{TR}{Near}$

${Ray}_{BL} = \overrightarrow{\bf{BL}} \times \frac{|BL|}{Near}= \frac{BL}{Near}$

${Ray}_{BR} = \overrightarrow{\bf{BR}} \times \frac{|BR|}{Near}= \frac{BR}{Near}$

我们可以<u><font style="color:#DF2A3F;"><b>将上述计算结果传递给顶点着色器，顶点着色器为这四个顶点选择各自的</b></font></u>$Ray$<u><font style="color:#DF2A3F;"><b>，然后传递给片元着色器，在这个过程中，</b></font></u>$Ray$<u><font style="color:#DF2A3F;"><b>将会被线性插值</b></font></u>，因此**平面上的每个像素都可以通过线性插值获得它们各自的**$Ray$**，我们将其记为**$\color{red}\bf{interpolatedRay}$**(interpolated: 插值的)**，并将它们带入开头的计算式中，即可计算出像素在世界空间中的坐标：

$\color{red}\text{像素在世界空间中的坐标} = \text{摄像机的世界空间坐标} + linearDepth \times interpolatedRay$

接下来，我们就可以使用一开始提到的雾效的计算公式计算出最终的颜色了。

#### 实现
我们将使用`Mode = Linear`的方来实现一种特殊的雾效：高度雾。

```csharp
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class FogWithDepthTextureTest : PostEffectBase
{
    [SerializeField] private Color fogColor = Color.gray;

    //雾效的浓度
    [Range(0.0f, 3.0f)]
    [SerializeField] private float fogDensity = 1f;

    //雾效起始距离(能见度为1)
    [SerializeField] private float fogStart = 0f;
    //雾效终点距离(能见度为0)
    [SerializeField] private float fogEnd = 100f;

    //我们使用一个4x4的矩阵来一次性向Shader传递4个顶点的Ray向量
    private Matrix4x4 rayMatrix;

    private void OnEnable()
    {
        Camera.main.depthTextureMode = DepthTextureMode.Depth;
    }

    //注意这里我们重写的是UpdateProperty函数
    protected override void UpdateProperty()
    {
        if(material != null)
        {
            //获取FOV
            float fov = Camera.main.fieldOfView / 2;
            //获取近裁剪平面距离
            float near = Camera.main.nearClipPlane;
            //获取窗口宽高比
            float aspect = Camera.main.aspect;

            //计算halfHeight = Near * tan(FOV / 2)
            float halfHeight = near * Mathf.Tan(fov * Mathf.Deg2Rad / 2);
            //计算toTop
            Vector3 toTop = Camera.main.transform.up * halfHeight;
            //计算toRight
            Vector3 toRight = Camera.main.transform.right * halfHeight * aspect;

            //计算TL TR BL BR
            Vector3 TL = Camera.main.transform.forward * near + toTop - toRight;
            Vector3 TR = Camera.main.transform.forward * near + toTop + toRight;
            Vector3 BL = Camera.main.transform.forward * near - toTop - toRight;
            Vector3 BR = Camera.main.transform.forward * near - toTop + toRight;

            //计算Ray_TL TR BL BR
            //由于四个向量的模长相等，因此我们记scale = magnitude / near
            float scale = TL.magnitude / near;
            //TL = TL.normalized * TL.magnitude / near;
            TL = TL.normalized * scale;
            TR = TR.normalized * scale;
            BL = BL.normalized * scale;
            BR = BR.normalized * scale;

            //为了便于在Shader中通过uv坐标来判断当前在处理4个顶点中的哪个顶点
            //也为了便于在顶点着色器中判断不同平台间纹理坐标的翻转问题	
            //我们将使用特定顺序(逆时针方向)来依次向矩阵中存放这四个向量
            //然后在Shader中使用同样的顺序来取出即可
            rayMatrix.SetRow(0, BL);
            rayMatrix.SetRow(1, BR);
            rayMatrix.SetRow(2, TR);
            rayMatrix.SetRow(3, TL);

            //传递属性
            material.SetColor("_FogColor", fogColor);
            material.SetFloat("_FogDensity", fogDensity);
            material.SetFloat("_FogStart", fogStart);
            material.SetFloat("_FogEnd", fogEnd);
            material.SetMatrix("_RayMatrix", rayMatrix);
        }
    }
}

```

{% note danger %}
之所以要按照“**左下 右下 右上 左上**”的逆时针存储方式，是**为了便于用`UNITY_UV_STARTS_AT_TOP`宏**判断深度纹理是否上下翻转**时，我们可以使用`index = 3 - index;`（**0-左下 1-右下 2-右上 3-左上**）来直接将上下两侧顶点与向量间的对应关系翻转。

{% endnote %}

```csharp
Shader "Unlit/FogWithDepthTexture"
{
    Properties
    {
        _MainTex ("Texture", 2D) = "white" {}
        _FogColor ("FogColor", Color) = (1,1,1,1)
        _FogDensity ("FogDensity", Float) = 1
        _FogStart ("FogStart", Float) = 0
        _FogEnd ("FogEnd", Float) = 10
    }
    SubShader
    {
        ZWrite Off
        ZTest Always
        Cull Off

        Pass
        {
            CGPROGRAM
            #pragma vertex vert
            #pragma fragment frag

            #include "UnityCG.cginc"

            struct v2f
            {
                float2 uv : TEXCOORD0;
                float2 uv_depth : TEXCOORD1;
                //传递到片元着色器之前将会进行线性插值运算
                float4 Ray : TEXCOORD2;
                float4 vertex : SV_POSITION;
            };

            sampler2D _MainTex;
            half4 _MainTex_TexelSize;
            sampler2D _CameraDepthTexture;

            fixed4 _FogColor;
            half _FogDensity;
            float _FogStart;
            float _FogEnd;
            //0左下 1右下 2右上 3左上 逆时针
            float4x4 _RayMatrix;


            v2f vert (appdata_base v)
            {
                v2f o;
                o.vertex = UnityObjectToClipPos(v.vertex);
                o.uv = v.texcoord;
                o.uv_depth = v.texcoord;

                //通过当前顶点的uv坐标来判断是哪个角上的顶点
                int index = 0;
                if(v.texcoord.x < 0.5 && v.texcoord.y < 0.5)
                    index = 0;
                else if(v.texcoord.x > 0.5 && v.texcoord.y < 0.5)
                    index = 1;
                else if(v.texcoord.x > 0.5 && v.texcoord.y > 0.5)
                    index = 2;
                else if(v.texcoord.x < 0.5 && v.texcoord.y > 0.5)
                    index = 3;
                //为每个角上的顶点选择它们各自的向量
                o.Ray = _RayMatrix[index];

                #if UNITY_UV_STARTS_AT_TOP
                if(_MainTex_TexelSize.y < 0)
                {
                    //这里就能体现出为什么需要逆时针存储4个向量
                    index = 3 - index;
                    o.uv_depth = 1 - o.uv_depth;
                }
                #endif

                return o;
            }

            fixed4 frag (v2f i) : SV_Target
            {
                //观察空间中的z分量
                float4 linearDepth = LinearEyeDepth(SAMPLE_DEPTH_TEXTURE(_CameraDepthTexture, i.uv_depth));
                //计算世界空间中的坐标
                float3 worldPos = _WorldSpaceCameraPos + linearDepth * i.Ray;
                //计算能见度
                float f = (_FogEnd - worldPos.y) / (_FogEnd - _FogStart);
                //使用浓度参数来控制最高能见度的大小
                f = saturate(f * _FogDensity);

                fixed4 col = tex2D(_MainTex, i.uv);
                col.rgb = lerp(_FogColor.rgb, col.rgb, f);

                return col;
            }
            ENDCG
        }
    }
}
```

## 基于深度和法线纹理的边缘检测算法
### 原理
在14.5节中，我们曾**使用Sobel算子对屏幕图像进行边缘检测**，实现描边的效果。但是，这种直接利用颜色信息进行边缘检测的方法会产生很多我们不希望得到的边缘线，得到的结果更贴近**2D素描画**的效果，如果我们只希望得到真正意义上的**场景中的物体的轮廓线**，我们就**需要使用深度和法线纹理进行边缘检测**，这些图像不会受纹理和光照的影响，而仅仅保存了当前渲染物体的模型信息，通过这样的方式检测出来的边缘更加可靠。

{% note info %}
当然，2D场景一般只能使用传统的边缘检测算法，毕竟2D场景中的物体一般来说并没有深度和法线上的差异

{% endnote %}

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/63937386/1773144206079-68b376ed-e32b-4a48-9a1c-88df0cdc1284.png)

之所以原先使用Sobel算子，是因为画面中的细节部分很多，我们希望过滤并平滑画面中的噪声，但是深度与法线纹理中并不存在噪声，因此我们可以**使用Roberts算子**来进行边缘检测。

$G_x = \begin{bmatrix} -1 & 0 \\ 0 & 1 \end{bmatrix}, \quad G_y = \begin{bmatrix} 0 & -1 \\ 1 & 0 \end{bmatrix}$

与原先在二维上比较像素之间的灰度值大小来实现的边缘检测不同，**基于深度和法线纹理的边缘检测更加靠近三维**：我们将使用Roberts算子来**比较对角线方向上像素的深度和法线值**，如果深度值或者法线值**大于我们所设定的阈值，那么就认为该中心像素处存在边缘**；同时，我们再次引入`_SampleDistance`变量来**控制采样间距：间距越大，对角线上的差异就越大，描边效果就越粗。**

### 实现
```csharp
Shader "Unlit/EdgeDetectionWithDepthAndNormal"
{
    Properties
    {
        _MainTex ("Texture", 2D) = "white" {}
        _EdgeAmount("EdgeAmount", Range(0,1)) = 1
        _EdgeColor("EdgeColor", Color) = (0,0,0,0)
        _BackgroundColor("BackgroundColor", Color) = (1,1,1,1)
        _SampleDistance("SampleDistance", Float) = 1
        //灵敏度
        _SenstivityDepth("SenstivityDepth", Float) = 1
        _SenstivityNormal("SenstivityNormal", Float) = 1
        //阈值
        _Diff("Diff", Float) = 0.1
    }
    SubShader
    {
        ZWrite Off
        Cull Off
        ZTest Always

        Pass
        {
            CGPROGRAM
            #pragma vertex vert
            #pragma fragment frag

            #include "UnityCG.cginc"

            struct v2f
            {
                //参与Roberts算子计算的采样点
                half2 uv[5] : TEXCOORD0;
                float4 vertex : SV_POSITION;
            };

            sampler2D _MainTex;
            half4 _MainTex_TexelSize;
            sampler2D _CameraDepthNormalsTexture;
            fixed _EdgeAmount;
            fixed4 _EdgeColor;
            fixed4 _BackgroundColor;
            float _SampleDistance;
            float _SenstivityDepth;
            float _SenstivityNormal;
            half _Diff;

            v2f vert (appdata_base v)
            {
                v2f o;
                o.vertex = UnityObjectToClipPos(v.vertex);
                //中心点
                half2 uv = v.texcoord;
                o.uv[0] = uv;
                o.uv[1] = uv + half2(-1,1) * _MainTex_TexelSize.xy * _SampleDistance;
                o.uv[2] = uv + half2(1,-1) * _MainTex_TexelSize.xy * _SampleDistance;
                o.uv[3] = uv + half2(1,1) * _MainTex_TexelSize.xy * _SampleDistance;
                o.uv[4] = uv + half2(-1,-1) * _MainTex_TexelSize.xy * _SampleDistance;

                return o;
            }

            //用于比较两个点的深度和法线值
            //返回1 代表两点深度和法线均接近
            //返回0 深度或法线值差异大于阈值
            half CheckSame(half4 sample1, half4 sample2)
            {
                //获得两个点的深度和法线
                float depth1 = DecodeFloatRG(sample1.zw);
                float depth2 = DecodeFloatRG(sample2.zw);
                float normal1 = sample1.xy;
                float normal2 = sample2.xy;

                //法线的差异计算
                    //我们并不需要使用DecodeViewNormalStereo来解码法线(区间转换)
                    //我们只需要知道两条法线之间的差异即可
                float2 normalDiff = abs(normal1 - normal2) * _SenstivityNormal;
                //判断法线差值大小(法线xy坐标之和是否小于_Diff)
                int isSameNormal = (normalDiff.x + normalDiff.y) < _Diff;

                //深度的差异计算
                float depthDiff = abs(depth1 - depth2) * _SenstivityDepth;
                //判断深度差值大小(深度差值是否小于_Diff%)
                int isSameDepth = depthDiff < _Diff * depth1;

                return isSameDepth * isSameNormal ? 1 : 0;
            }

            fixed4 frag (v2f i) : SV_Target
            {
                //xy为法线 zw为深度
                half4 sampleTL = tex2D(_CameraDepthNormalsTexture, i.uv[1]);
                half4 sampleBR = tex2D(_CameraDepthNormalsTexture, i.uv[2]);
                half4 sampleTR = tex2D(_CameraDepthNormalsTexture, i.uv[3]);
                half4 sampleBL = tex2D(_CameraDepthNormalsTexture, i.uv[4]);

                //判断当前像素是否位于边缘
                int edge = CheckSame(sampleTL, sampleBR) * CheckSame(sampleTR, sampleBL);

                //原图叠加边缘的颜色
                fixed4 EdgeAndOrignalCol = lerp(_EdgeColor, tex2D(_MainTex, i.uv[0]), edge);
                //背景颜色叠加边缘的颜色
                fixed4 EdgeAndBGCol = lerp(_EdgeColor, _BackgroundColor, edge);

                return lerp(EdgeAndOrignalCol, EdgeAndBGCol, _EdgeAmount);
            }
            ENDCG
        }
    }
}
```

```csharp
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class EdgeDetectionWithDepthAndNormalTest : PostEffectBase
{
    [Range(0,1)]
    [SerializeField] private float edgeAmount = 1.0f;

    [SerializeField] private Color edgeColor = Color.black;
    [SerializeField] private Color backgroundColor = Color.white;
    [SerializeField] private float sampleDistance = 1f;
    [SerializeField] private float senstivityDepth = 1f;
    [SerializeField] private float senstivityNormal = 1f;
    [SerializeField] private float diff = 0.1f;
    private void OnEnable()
    {
        //使用|=来避免关闭其他脚本可能正在使用的深度纹理
        Camera.main.depthTextureMode |= DepthTextureMode.DepthNormals;
    }
    protected override void UpdateProperty()
    {
        if(material != null)
        {
            material.SetFloat("_EdgeAmount", edgeAmount);
            material.SetColor("_EdgeColor", edgeColor);
            material.SetColor("_BackgroundColor", backgroundColor);
            material.SetFloat("_SampleDistance", sampleDistance);
            material.SetFloat("_SenstivityDepth", senstivityDepth);
            material.SetFloat("_SenstivityNormal", senstivityNormal);
            material.SetFloat("_Diff", diff);
        }
    }
}

```

{% note info %}
+ `Camera.main.depthTextureMode **|=** DepthTextureMode.DepthNormals;`：注意这里要**使用`|=`来**避免关闭其他脚本（后处理效果）可能需要使用的法线纹理**。

{% endnote %}

# 实践（一）
## 流光效果Glint
### 原理
 通常用于给材质增加一种闪光或光线移动的效果，使物体表面看起来像是有光在流动。  

我们只需要利用Unity内置的时间变量`_Time`，让UV坐标沿着一个固定的方向持续递增， 然后用偏移后的UV坐标对纹理贴图进行采样，就可以得到流动的效果了。  

### 实现
我们需要调整纹理的缩放，因为我们的面片在x方向上被缩放了，因此纹理uv也同样需要缩放。

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/63937386/1773151979900-ffa0790a-7c4c-4051-a50d-fd9851814e49.png)

```csharp
Shader "Unlit/Glint"
{
    Properties
    {
        _MainTex ("Texture", 2D) = "white" {}
        _Color("Color", Color) = (1,1,1,1)
        _Speed("Speed", Float) = 1
    }
    SubShader
    {
        Tags{ "RenderType" = "Transparent" "Queue" = "Transparent" }

        //透明颜色混合
        Blend One One
        Cull Off

        Pass
        {
            CGPROGRAM
            #pragma vertex vert
            #pragma fragment frag

            #include "UnityCG.cginc"

            struct v2f
            {
                float2 uv : TEXCOORD0;
                float4 vertex : SV_POSITION;
            };

            sampler2D _MainTex;
            float4 _MainTex_ST;
            fixed4 _Color;
            float _Speed;

            v2f vert (appdata_base v)
            {
                v2f o;
                o.vertex = UnityObjectToClipPos(v.vertex);
                o.uv = TRANSFORM_TEX(v.texcoord, _MainTex);
                return o;
            }

            fixed4 frag (v2f i) : SV_Target
            {
                i.uv = float2(i.uv.x + _Time.x * _Speed, i.uv.y);
                return tex2D(_MainTex, i.uv) * _Color;
            }
            ENDCG
        }
    }
}

```

## 过程式几何轮廓线
与前面的边缘检测效果得到的物体边缘不同，我们只希望得到物体最外侧的轮廓线，而不是物体的边缘，因此，我们将使用一种新的方式来进行轮廓线的渲染。

### 原理
轮廓线效果本质上就是对物体外侧边缘的描边效果，因此我们在这里采用一种**简单“取巧”**的方式：

我们**使用两个`Pass`来渲染模型**，在**第一个`Pass`的顶点着色器**中，我们将物体的**每一个顶点沿着法线方向向外偏移挤出**，相当于放大模型，然后**在片元着色器中返回物体描边的颜色**，这样渲染出来的结果就可以充当描边的背景颜色；而后**第二个`Pass`直接正常渲染模型**即可，同时**第一个`Pass`需要关闭深度写入**，否则第二个`Pass`渲染的像素将无法通过边缘检测，因为第一个`Pass`渲染出的物体更大，会盖住后者。

这样第二个`Pass`渲染出的物体就会盖住第一个`Pass`的背景，并在外侧留下“轮廓”。

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/63937386/1773228436126-5f96b26d-3204-47f0-9f11-72b6f2c08496.png)

但是由于第一个`Pass`关闭了深度写入，因此该物体背后的其他物体将会覆盖掉边缘线，所以我们需要将**该`Shader`的渲染队列设置为`Transparent`，使其晚于其他几何体渲染即可。

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/63937386/1773228626800-bf05f0fb-e7d8-4d35-8fc5-ea0d439692a2.png)

{% note warning %}
但这种通过沿法线方向挤出的方式获得的轮廓线并**不适合如立方体这种带有“硬边缘”的几何体**：硬边缘出的顶点并不相互连接，例如立方体的一个角实际上由三个顶点组成，这是因为在硬边缘处的法线并不连续，因为立方体一个角上的顶点同时属于三个面，这意味着这个顶点需要同时具备三个方向的法线来正确渲染光照，这显然是不现实的，因此，建模软件将会将这个顶点拆分成三个坐标相同但法线方向不同的顶点，以此来完成法线方向在硬边缘处的突变。

同时，这三个顶点并不相互连接：一方面，这三个顶点各自属于不同的面片，因此并不存在同时包括这三个顶点的面片索引；另一方面，如果这三个顶点相互连接，那么最终参与光照渲染的法线方向将会是插值后的方向，这显然也是错误的，因此这三个顶点相互分离。

同理，立方体的硬边缘处实际上都是由多个坐标相同、法线方向不同、不相互连接的顶点构成，因此立方体的六个面实际上是相互分离的，**因此在沿法线方向挤出时，这六个面将会相互分离，彼此之间会出现空隙，因此得到的轮廓线在六个角附近将会出现缺口。**

综上，这种<font style="color:#DF2A3F;"><b>过程式几何轮廓线并不是渲染轮廓线的最优解</b></font>，我们会在卡通风格渲染实现中继续优化算法，但是**依然避免不了硬边缘的问题**。

{% endnote %}

### 实现
我们在`BumpedDiffuse Shader`的基础上添加上述第一个`Pass`：

```csharp
Shader "Unlit/ProceduralOutline"
{
    Properties
    {
        _MainTex ("Texture", 2D) = "white" {}
        _BumpMap("BumpMap", 2D) = "bump"{}
        _BumpScale("BumpScale", Range(0,1)) = 1
            _DiffuseColor("DiffuseColor", Color) = (1,1,1,1)
            _Outline("Outline", Float) = 0.1
            _OutlineColor("OutlineColor", Color) = (0,0,0,0)
        }
    SubShader
    {
        Tags { "RenderType" = "Opaque" "Queue" = "Transparent"}
        Pass
        {
            ZWrite Off

                CGPROGRAM
                #pragma vertex vert
                #pragma fragment frag

                #include "UnityCG.cginc"

                struct v2f
                {
                    float4 pos : SV_POSITION;
                };

            sampler2D _MainTex;
            float _Outline;
            fixed4 _OutlineColor;

            v2f vert(appdata_base v)
            {
                v2f o;
                //注意这里不要污染v.vertex.w
                o.pos = UnityObjectToClipPos(float4(v.vertex.xyz + _Outline * normalize(v.normal), v.vertex.w));

                return o;
            }
            fixed4 frag (v2f i) : SV_Target
            {
                return fixed4(_OutlineColor.rgb, 1);
            }

            ENDCG
            }
        Pass
        {
            Tags{"LightMode" = "ForwardBase"}

            CGPROGRAM
                #pragma vertex vert
                #pragma fragment frag
                #pragma multi_compile_fwdbase

                #include "UnityCG.cginc"
                #include "Lighting.cginc"
                #include "AutoLight.cginc"  

                struct v2f
                {
                    float4 uv : TEXCOORD0;
                    float4 pos : SV_POSITION;
                    float3 worldPos : TEXCOORD1;
                    float3x3 rotation : TEXCOORD2;
                    SHADOW_COORDS(5)
                    };

            sampler2D _MainTex;
            float4 _MainTex_ST;
            sampler2D _BumpMap;
            float4 _BumpMap_ST;
            float _BumpScale;
            fixed4 _DiffuseColor;

            v2f vert (appdata_full v)
            {
                v2f o;
                o.pos = UnityObjectToClipPos(v.vertex);
                o.uv.xy = TRANSFORM_TEX(v.texcoord, _MainTex);
                o.uv.zw = TRANSFORM_TEX(v.texcoord, _BumpMap);

                o.worldPos = mul(unity_ObjectToWorld, v.vertex);

                float3 worldNormal = UnityObjectToWorldNormal(v.normal);
                float3 worldTangent = UnityObjectToWorldDir(v.tangent);
                float3 worldBinormal = cross(normalize(worldTangent), normalize(worldNormal)) * v.tangent.w;

                o.rotation = float3x3(worldTangent.x, worldBinormal.x, worldNormal.x,
                                      worldTangent.y, worldBinormal.y, worldNormal.y,
                                      worldTangent.z, worldBinormal.z, worldNormal.z);

                TRANSFER_SHADOW(o)

                    return o;
            }

            fixed4 frag (v2f i) : SV_Target
            {
                fixed3 lightDir = normalize(UnityWorldSpaceLightDir(i.worldPos));
                //fixed3 viewDir = normalize(UnityWorldSpaceViewDir(i.worldPos));

                float4 packedNormal = tex2D(_BumpMap, i.uv.zw);
                float3 tangentNormal = UnpackNormal(packedNormal);
                tangentNormal.xy *= _BumpScale;
                tangentNormal.z = sqrt(1 - saturate(dot(tangentNormal.xy, tangentNormal.xy)));

                float3 worldTangentNormal = mul(i.rotation, tangentNormal);

                fixed3 albedo = tex2D(_MainTex, i.uv.xy) * _DiffuseColor.rgb;
                fixed3 diffuse = _LightColor0.rgb * albedo * max(0, dot(lightDir, worldTangentNormal));

                UNITY_LIGHT_ATTENUATION(atten, i, i.worldPos)

                fixed3 color = UNITY_LIGHTMODEL_AMBIENT.rgb * albedo + diffuse * atten;

                return fixed4(color, 1);
            }
            ENDCG
        }
        Pass
        {
            Tags{"LightMode" = "ForwardAdd"}

            Blend One One

            CGPROGRAM
            #pragma vertex vert
            #pragma fragment frag
            #pragma multi_compile_fwdadd_fullshadows

            #include "UnityCG.cginc"
            #include "Lighting.cginc"
            #include "AutoLight.cginc"  

            struct v2f
            {
                float4 uv : TEXCOORD0;
                float4 pos : SV_POSITION;
                float3 worldPos : TEXCOORD1;
                float3x3 rotation : TEXCOORD2;
                SHADOW_COORDS(5)
            };

            sampler2D _MainTex;
            float4 _MainTex_ST;
            sampler2D _BumpMap;
            float4 _BumpMap_ST;
            float _BumpScale;
            fixed4 _DiffuseColor;

            v2f vert (appdata_full v)
            {
                v2f o;
                o.pos = UnityObjectToClipPos(v.vertex);
                o.uv.xy = TRANSFORM_TEX(v.texcoord, _MainTex);
                o.uv.zw = TRANSFORM_TEX(v.texcoord, _BumpMap);

                o.worldPos = mul(unity_ObjectToWorld, v.vertex);

                float3 worldNormal = UnityObjectToWorldNormal(v.normal);
                float3 worldTangent = UnityObjectToWorldDir(v.tangent);
                float3 worldBinormal = cross(normalize(worldTangent), normalize(worldNormal)) * v.tangent.w;

                o.rotation = float3x3(worldTangent.x, worldBinormal.x, worldNormal.x,
                                      worldTangent.y, worldBinormal.y, worldNormal.y,
                                      worldTangent.z, worldBinormal.z, worldNormal.z);

                TRANSFER_SHADOW(o)

                return o;
            }

            fixed4 frag (v2f i) : SV_Target
            {
                fixed3 lightDir = normalize(UnityWorldSpaceLightDir(i.worldPos));
                //fixed3 viewDir = normalize(UnityWorldSpaceViewDir(i.worldPos));

                float4 packedNormal = tex2D(_BumpMap, i.uv.zw);
                float3 tangentNormal = UnpackNormal(packedNormal);
                tangentNormal.xy *= _BumpScale;
                tangentNormal.z = sqrt(1 - saturate(dot(tangentNormal.xy, tangentNormal.xy)));

                float3 worldTangentNormal = mul(i.rotation, tangentNormal);

                fixed3 albedo = tex2D(_MainTex, i.uv.xy) * _DiffuseColor.rgb;
                fixed3 diffuse = _LightColor0.rgb * albedo * max(0, dot(lightDir, worldTangentNormal));

                UNITY_LIGHT_ATTENUATION(atten, i, i.worldPos)

                fixed3 color = UNITY_LIGHTMODEL_AMBIENT.rgb * albedo + diffuse * atten;

                return fixed4(color, 1);
            }
            ENDCG
        }
    }
    Fallback "Diffuse"
}

```

## 遮挡透视描边效果
### 原理
我们希望能够让被遮挡的物体能够显现出类似透视描边的效果，但是没有被遮挡的物体能够正常显示，显然，我们需要使用多个`Pass`来渲染物体：

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/63937386/1773322146640-dd5e4388-18b6-41b6-bbcf-48e65f781449.png)

**第一个`Pass`用来渲染被其他物体遮挡住的部分**：我们可以自定义最终渲染的效果，这里我们将**通过使用菲涅尔反射率**$F_{\text{schlick}}(\mathbf{v}, \mathbf{n}) = F_0 + (1 - F_0)(1 - \mathbf{v} \cdot \mathbf{n})^5$**来实现描边效果**，因为菲涅尔反射率在视线方向和法线方向接近时较小，两者差异较大时较大，因此在物体边缘法线垂直于视角方向处反射率较大，因此我们可以使用菲涅尔反射率作为自定义颜色的透明度。

（我们也可以不使用其他的自定义效果，**只控制输出颜色的透明度，即可实现透视效果**）

同时**第一个`Pass`需要设置`Ztest Greater`，这样就可以不被深度测试剔除并正常渲染，**同时需要关闭深度写入**，否则第一个`Pass`因为`Ztest Greater`会通过深度测试而将深度写入缓冲区，那么第二个`Pass`由于没有设置深度测试，即默认`ZTest LEqual`（小于等于），将会直接通过深度测试，导致被遮挡的部分也被正常渲染出来，违反了遮挡剔除结果。****

{% note warning %}
需要注意的是，这种方法显然只适合法线方向从物体中心向边缘平滑过渡，直到与视角垂直的物体，例如球体，因为只有这种情况下我们才能得到平滑过渡的菲涅尔反射率。**立方体这类同一个表面上的法线方向全部相同的物体显然不适合这种利用菲涅尔反射率的自定义渲染效果。**

{% endnote %}

	**第二个`Pass`只需要直接正常渲染模型即可**。

{% note warning %}
**这两个`Pass`的顺序并不能前后调换**：如果先使用第二个`Pass`，那么物体的深度将会正常写入，而后第一个`Pass`在渲染时，由于深度测试时`Ztest Greater`，这会导致在未遮挡的部分处，物体的被正面遮挡住的部分（例如甜甜圈的内圈）也会被直接渲染出来，造成错误的遮挡关系。

{% endnote %}

### 实现
```c
Shader "Unlit/BlockOutline"
{
    Properties
    {
        _MainTex ("Texture", 2D) = "white" {}
        _FresnelScale("FresnelScale", Range(0,2)) = 1
        //调整描边粗细
        _FresnelN("FresnelN", Range(0,5)) = 5
        _FresnelColor("FresnelColor", Color) = (1,1,1,1)
    }
    SubShader
    {
        Tags { "RenderType"="Opaque" }

        Pass
        {
            ZTest Greater
            ZWrite Off
            Blend SrcAlpha OneMinusSrcAlpha

            CGPROGRAM
            #pragma vertex vert
            #pragma fragment frag

            #include "UnityCG.cginc"

            struct v2f
            {
                float4 vertex : SV_POSITION;
                float3 viewDir : TEXCOORD0;
                float3 worldNormal : TEXCOORD1;
            };

            //第一个Pass不需要主纹理采样
            float _FresnelN;
            float _FresnelScale;
            fixed4 _FresnelColor;

            v2f vert (appdata_base v)
            {
                v2f o;
                o.vertex = UnityObjectToClipPos(v.vertex);
                o.viewDir = normalize(WorldSpaceViewDir(v.vertex));
                o.worldNormal = normalize(UnityObjectToWorldNormal(v.normal));
                return o;
            }

            fixed4 frag (v2f i) : SV_Target
            {
                fixed alpha = _FresnelScale + (1 - _FresnelScale) * pow(1 - dot(normalize(i.viewDir), normalize(i.worldNormal)), _FresnelN);

                return fixed4(_FresnelColor.rgb, alpha);
            }
            ENDCG
        }

        Pass
        {
            CGPROGRAM
            #pragma vertex vert
            #pragma fragment frag

            #include "UnityCG.cginc"

            struct v2f
            {
                float2 uv : TEXCOORD0;
                float4 vertex : SV_POSITION;
            };

            sampler2D _MainTex;
            float _Alpha;

            v2f vert (appdata_base v)
            {
                v2f o;
                o.vertex = UnityObjectToClipPos(v.vertex);
                o.uv = v.texcoord;
                return o;
            }

            fixed4 frag (v2f i) : SV_Target
            {
                fixed4 col = tex2D(_MainTex, i.uv);
                return col;
            }
            ENDCG
        }
    }
}

```

```c
Shader "Unlit/XRay"
{
    Properties
    {
        _MainTex ("Texture", 2D) = "white" {}
        _Alpha("Alpha", Float) = 0.5
    }
    SubShader
    {
        Tags { "RenderType"="Opaque" }

        Pass
        {
            ZTest Greater
            ZWrite Off
            Blend SrcAlpha OneMinusSrcAlpha

            CGPROGRAM
            #pragma vertex vert
            #pragma fragment frag

            #include "UnityCG.cginc"

            struct v2f
            {
                float2 uv : TEXCOORD0;
                float4 vertex : SV_POSITION;
            };

            sampler2D _MainTex;
            float _Alpha;

            v2f vert (appdata_base v)
            {
                v2f o;
                o.vertex = UnityObjectToClipPos(v.vertex);
                o.uv = v.texcoord;
                return o;
            }

            fixed4 frag (v2f i) : SV_Target
            {
                fixed4 col = tex2D(_MainTex, i.uv);
                return fixed4(col.rgb, _Alpha);
            }
            ENDCG
        }

        Pass
        {
            CGPROGRAM
            #pragma vertex vert
            #pragma fragment frag

            #include "UnityCG.cginc"

            struct v2f
            {
                float2 uv : TEXCOORD0;
                float4 vertex : SV_POSITION;
            };

            sampler2D _MainTex;
            float _Alpha;

            v2f vert (appdata_base v)
            {
                v2f o;
                o.vertex = UnityObjectToClipPos(v.vertex);
                o.uv = v.texcoord;
                return o;
            }

            fixed4 frag (v2f i) : SV_Target
            {
                fixed4 col = tex2D(_MainTex, i.uv);
                return col;
            }
            ENDCG
        }
    }
}

```

## 物体切割效果
### 原理
物体切割效果指的是通过向`Shader`传入一个世界空间中的坐标来控制物体被切割的部分，未被切割的部分将会被双面渲染，同时两面使用不同的材质，以此来呈现出被切开的效果。

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/63937386/1773401291192-5941fa30-648f-4e3e-8201-5fc054afe2d6.png)

`Shader`在接收到C#脚本传入的世界空间坐标之后，可以**在片元着色器中判断当前片元的世界坐标和传入的世界坐标的位置关系**，然后使用`clip`函数进行剔除；同时`Unity Shader`提供了一个语义`VFACE`，只能在片元着色器中使用，**该语义对应的变量为1时表示当前片元为正面，反之为反面**，因此在**关闭背面剔除**之后，模型的正反面就可以使用不同的材质了，同时**该语义还需要添加编译指令`#pragma target 3.0 或 4.0 、5.0`，以此来保证该语义对不同着色器版本的兼容性。

### 实现
```csharp
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

[ExecuteAlways]
public class ObjectCuttingTest : MonoBehaviour
{
    private Material material;
    [SerializeField] private GameObject cuttingObject;
    private void Start()
    {
        material = GetComponent<Renderer>().sharedMaterial;
    }
    private void Update()
    {
        if(material != null && cuttingObject != null)
        {
            material.SetVector("_CuttingPos", cuttingObject.transform.position);
        }
    }
}

```

```csharp
Shader "Unlit/ObjectCutting"
{
    Properties
    {
        _MainTex ("Texture", 2D) = "white" {}
        //模型内侧/背面
        _BackTex ("BackTex", 2D) = "white" {}
        //切割方向 0-x 1-y 2-z
        _CutDir("CutDir", Range(0,2)) = 0
        //是否翻转切割方向 0-不翻转 1-翻转
        _Invert("Invert", Range(0,1)) = 0
        //切割的位置
        _CuttingPos("CuttingPos", Vector) = (0,0,0,0)
    }
    SubShader
    {
        Tags { "RenderType"="Opaque" }
        Cull Off

        Pass
        {
            CGPROGRAM
            #pragma vertex vert
            #pragma fragment frag
            #pragma target 3.0

            #include "UnityCG.cginc"

            struct v2f
            {
                float2 uv : TEXCOORD0;
                float3 worldPos : TEXCOORD1;
                float4 vertex : SV_POSITION;
            };

            sampler2D _MainTex;
            sampler2D _BackTex;
            float4 _MainTex_ST;
            float4 _BackTex_ST;
            fixed _CutDir;
            fixed _Invert;
            float4 _CuttingPos;

            v2f vert (appdata_base v)
            {
                v2f o;
                o.vertex = UnityObjectToClipPos(v.vertex);
                o.uv = TRANSFORM_TEX(v.texcoord, _MainTex);
                o.worldPos = mul(unity_ObjectToWorld, v.vertex).xyz;
                return o;
            }

            fixed4 frag (v2f i, fixed face : VFACE) : SV_Target
            {
                fixed4 col = face > 0 ? tex2D(_MainTex, i.uv) : tex2D(_BackTex, i.uv);
                bool shouldBeCliped;
                if(_CutDir == 0)
                    shouldBeCliped = step(_CuttingPos.x, i.worldPos.x);
                else if(_CutDir == 2)
                    shouldBeCliped = step(_CuttingPos.z, i.worldPos.z);
                else
                    shouldBeCliped = step(_CuttingPos.y, i.worldPos.y);
                
                if(_Invert)
                    shouldBeCliped = !shouldBeCliped;
                clip(shouldBeCliped - 1);   //clip传入的参数小于0就会被剔除

                return col;
                    
            }
            ENDCG
        }
    }
}

```

{% note warning %}
+ `step`：`step(edge, x)` **的逻辑非常简单：如果 $x < edge$，返回 **0.0**；如果 $x \ge edge$，返回 **1.0**，即：

$f(edge, x) = \begin{cases} 0 & x < edge \\ 1 & x \ge edge \end{cases}$

我们**常使用`step`函数来避免使用`if`语句**，因为**后者可能导致性能下降**，而前者是纯数学运算，对GPU较为友好。

{% endnote %}

## 书本翻页效果
### 原理
我们将针对`Uniry Plane`（**大小为`10 x 10`）来实现书页的翻页效果，但由于物体的旋转中心位于几何中心，这意味着我们直接对顶点应用旋转矩阵会导致平面围绕着中心转动，但是**书本翻页时的旋转轴应当在`Plane`的边缘处**，因此我们将使用以下方式：

我们没有办法直接更改物体的旋转中心的位置，因此我们只能使用其他的方式。在顶点着色器中，我们可以**在旋转前**前将所有顶点整体向理论上的旋转轴的位置方向**水平平移**，**使得物体的轴心相对移动到边缘处**，此时**再使用旋转矩阵**，即可获得翻页的正确效果，但此时顶点的位置全都发生了水平方向的偏移，因此我们可以将旋转得到的结果应用之前平移偏移量的相反数，即可**将物体的轴心相对移动回几何中心**，同时应用了正确的翻页旋转效果。

同时，书页需要一定的起伏感，因此我们可以使用**三角函数**，为每个顶点添加偏移效果 。

{% note warning %}
注意，我们**需要先应用平移，然后再使用三角函数，并应用旋转，最后再往回平移**。如果先使用三角函数再应用平移的话，这意味着三角函数的原点还在物体的几何中心处，并不在书页的边缘处，这会导致书页的边缘不贴合旋转轴；先应用平移的话**，三角函数的原点（x）就会在书页的边缘处**，因此可以得到正确的起伏效果。

{% endnote %}

### 实现
```csharp
Shader "Unlit/PageTurning"
{
    Properties
    {
        _MainTex ("Texture", 2D) = "white" {}
        _BackTex ("BackTex", 2D) = "white" {}
        _AngleProgress("AngleProgress", Range(0,180)) = 0
        //y轴弯曲程度
        _WeightX("WeightX", Range(0,1)) = 1
        //x轴收缩程度
        _WeightY("WeightY", Range(0,1)) = 1
        _WaveLength("WaveLength", Range(0.01,4)) = 0.01
        //平移距离
        _MoveDis("MoveDis", Float) = 0
    }
    SubShader
    {
        Tags { "RenderType"="Opaque" }
        Cull Off

        Pass
        {
            CGPROGRAM
            #pragma vertex vert
            #pragma fragment frag
            #pragma target 3.0

            #include "UnityCG.cginc"

            struct v2f
            {
                float2 uv : TEXCOORD0;
                float4 vertex : SV_POSITION;
            };

            sampler2D _MainTex;
            sampler2D _BackTex;
            float _AngleProgress;
            fixed _WeightX;
            fixed _WeightY;
            float _WaveLength;
            float _MoveDis;


            v2f vert (appdata_base v)
            {
                v2f o;
                float s, c;
                //计算当前角度对应的sin cos值
                sincos(radians(_AngleProgress), s, c);
                //围绕z轴旋转
                float4x4 rotationM =  {c, -s, 0, 0,
                                       s, c, 0, 0, 
                                       0, 0, 1, 0,
                                       0, 0, 0, 1};

                //先应用平移 然后再应用起伏和旋转 最后往回平移
                v.vertex.x += _MoveDis;
                //起伏程度 0和180处起伏最小 90处起伏最大
                float weight = 1 - abs(90 - _AngleProgress) / 90;
                //y轴起伏程度
                v.vertex.y += sin(v.vertex.x / _WaveLength) * weight * _WeightY;
                //x轴收缩
                v.vertex.x -= v.vertex.x * weight * _WeightX;

                
                //平移后再旋转
                float4 position = mul(rotationM, v.vertex);
                position.x -= _MoveDis;

                o.vertex = UnityObjectToClipPos(position);
                o.uv = v.texcoord;
                return o;
            }

            fixed4 frag (v2f i, fixed face : VFACE) : SV_Target
            {
                fixed4 col = face > 0 ? tex2D(_MainTex, i.uv) : tex2D(_BackTex, i.uv);

                return col;
            }
            ENDCG
        }
    }
}
```

+ `sincos(radians(_AngleProgress), s, c);`定义两个`float`变量并传入变量名，该函数会自动根据传入的**弧度**计算`sin`与`cos`，并填入对应变量中

# 非真实感渲染
## 卡通风格渲染(NPR)
### 原理
**卡通风格渲染效果**主要由两部分组成：一是“**分明的明暗变化**”；二是“**黑色的线条描边**”，前者我们曾在6.5节渐变纹理中提到过，其主要技术为**基于色调的着色技术（tone-based shading）**：通过使用**半兰伯特漫反射系数**对一张色调纹理进行采样，即可获得色调分界较为明显的着色效果；但不同的是，我们还需要加入**高光效果**：`Blinn-Phong`的高光反射效果通过半角向量和表面法线之间的夹角来决定高光的亮度，能够获得较为平滑的高光反射，但是在卡通风格渲染中，我们将**使用一块分界明显的纯色区域作为高光部分**，因此，我们将引入一个高光阈值变量，当**半角向量与表面法线的点乘大于该阈值（点乘越大，夹角越小）**时，就渲染高光颜色。

后者我们曾在16.2节中学习过较为简易的“**过程式几何轮廓线**”，但是我们也曾解释过这种轮廓线并非最优解，并且这种轮廓线只会显示物体最外侧的轮廓线，而无法显示其他的边缘线，因此我们将对过程式几何轮廓线进行改进，但要注意的是，**我们依然无法避免硬边缘所带来的问题**：

我们将同样**使用两个`Pass`来渲染对象**，**第一个`Pass`渲染只渲染物体的背面并将顶点沿法线方向挤出**，而非全部的顶点，同时**开启深度写入和默认的深度测试**，这样的话正面的其他边缘就不会被第二个`Pass`的渲染结果所覆盖；**第二个`Pass`只需要正常渲染正面**即可。

### 实现
```csharp
Shader "Unlit/Cartoon"
{
Properties
    {
        _MainTex ("Texture", 2D) = "" {}
        _RampTex ("RampTex", 2D) = "" {}
        _BumpMap("BumpMap", 2D) = ""{}
        _BumpScale("BumpScale", Range(0,1)) = 1
        _DiffuseColor("DiffuseColor", Color) = (1,1,1,1)
        _SpecularColor("SpecularColor", Color) = (1,1,1,1)
        _SpecThreshold("SpecThreshold", Range(0, 1)) = 0.5
        _OutlineColor("OutlineColor", Color) = (0,0,0,0)
        _OutlineWidth("OutlineWidth", Range(0, 0.015)) = 0.01
    }
    SubShader 
    {
        Pass
        {
            Cull Front

            CGPROGRAM
            #pragma vertex vert
            #pragma fragment frag

            #include "UnityCG.cginc"

            struct v2f
            {
                float4 vertex : SV_POSITION;               
            };

            fixed4 _OutlineColor;
            float _OutlineWidth;

            v2f vert(appdata_base v)
            {
                v2f o;

                o.vertex = UnityObjectToClipPos(float4(v.vertex.xyz + normalize(v.normal).xyz * _OutlineWidth, v.vertex.w));
            
                return o;
            }

            fixed4 frag(v2f i) : SV_Target
            {
                return fixed4(_OutlineColor.rgb, 1);
            }

            ENDCG
        }

        Pass
        {
            Tags{"LightMode" = "ForwardBase"}

            CGPROGRAM
            #pragma vertex vert
            #pragma fragment frag
            #pragma multi_compile_fwdbase

            #include "UnityCG.cginc"
            #include "Lighting.cginc"
            #include "AutoLight.cginc"

            struct v2f
            {
                float4 uv : TEXCOORD0;//xyTex, zwBump
                float4 pos : SV_POSITION;
                float3 lightDir : TEXCOORD1; //切线空间下
                float3 viewDir : TEXCOORD2; //切线空间下
                float3 worldPos : TEXCOORD3;
                SHADOW_COORDS(4)
            };

            sampler2D _MainTex;
            sampler2D _RampTex;
            float4 _MainTex_ST;
            sampler2D _BumpMap;
            float4 _BumpMap_ST;
            float _BumpScale;
            fixed4 _DiffuseColor;
            fixed4 _SpecularColor;
            float _SpecThreshold;

            v2f vert (appdata_full v)
            {
                v2f o;
                o.pos = UnityObjectToClipPos(v.vertex);
                o.worldPos = mul(unity_ObjectToWorld, v.vertex);
                o.uv.xy = TRANSFORM_TEX(v.texcoord, _MainTex);
                o.uv.zw = TRANSFORM_TEX(v.texcoord, _BumpMap);

                float3 binormal = cross(normalize(v.tangent), normalize(v.normal)) * v.tangent.w;
                float3x3 rotation = float3x3(v.tangent.xyz, binormal, v.normal);
                //TANGENT_SPACE_ROTATION;

                //阴影
                TRANSFER_SHADOW(o);

                o.lightDir = mul(rotation, ObjSpaceLightDir(v.vertex));
                o.viewDir = mul(rotation, ObjSpaceViewDir(v.vertex));
                return o;
            }

            fixed4 frag (v2f i) : SV_Target
            {
                float4 packedNormal = tex2D(_BumpMap, i.uv.zw);
                float3 tangentNormal = UnpackNormal(packedNormal);
                tangentNormal.xy *= _BumpScale;
                tangentNormal.z = sqrt(1 - saturate(dot(tangentNormal.xy,tangentNormal.xy)));

                float3 tangentLightDir = normalize(i.lightDir);
                float3 tangentViewDir = normalize(i.viewDir);

                //光照衰减
                //由于_RampTexture中越靠左 即uv小的地方表示暗部 uv越大的地方表示亮部
                //因此我们可以让halfLambert * atten来表示光照衰减
                UNITY_LIGHT_ATTENUATION(atten, i, i.worldPos);
                fixed halfLambert = dot(tangentLightDir, tangentNormal) * 0.5 + 0.5;
                halfLambert *= atten;
                
                fixed3 albedo = tex2D(_MainTex, i.uv.xy) * _DiffuseColor.rgb;
                fixed3 diffuse = _LightColor0.rgb * albedo * tex2D(_RampTex, fixed2(halfLambert, halfLambert));
                
                float3 halfDir = normalize(tangentViewDir + tangentLightDir);
                //dot(halfDir, tangentNormal)在0-1之间，因此_SpecThreshold的Range也应该设置为0-1
                fixed spec = dot(halfDir, tangentNormal);
                fixed w = fwidth(spec) * 2.0;
                fixed3 specular = _SpecularColor.rgb * step(_SpecThreshold, spec) * lerp(0, 1, smoothstep(-w, w, spec));
                fixed3 color = UNITY_LIGHTMODEL_AMBIENT.rgb * albedo + diffuse + specular;

                return fixed4(color, 1);
            }
            ENDCG
        }
    }
    Fallback "Diffuse"
}

```

### 抗锯齿
由于我们使用了`step`函数，这会导致高光边缘产生锯齿状效果，因此我们需要使用抗锯齿方法。

+ `fixed w = **fwidth**(spec) * 2.0;`：通过计算当前像素与相邻像素之间`spec`的变化率，得到`spec`边缘的过渡区域的宽度，`2.0`是经验系数；
+ `lerp(0, 1, **smoothstep**(-w, w, spec)`：`smoothstep`在`spec < -w`时返回0，`spec > w`时返回1，并在$spec \in [-w,w]$区间内平滑插值（**埃尔米特插值法，即两端斜率较小，中段斜率较大**），以此在高光边缘进行平滑过渡。

## 素描风格渲染
### 原理
在素描画中，物体的亮部与暗部并不是通过画笔的颜色决定的，毕竟素描画只能使用黑色铅笔，因此，**素描画的亮部与暗部实际上是通过笔画的密度所决定的**：**亮部笔画的密度较小**，因此画纸的颜色（白色）占主体；**暗部笔画的密度高**，导致画纸大面积“被涂黑”。因此，素描风格的渲染方式同样不能只靠顶点的颜色来绘制亮部和暗部，我们将采取和素描画类似的方式来进行渲染：

我们将**使用多张素描纹理**，这些纹理中的**笔画线条密度依次增大**，我们将他们按照笔画密度排序并依次提供给`Shader`，在计算漫反射系数时，原先我们使用`lightDir`和`worldNormal`的点乘来进行计算，这使得漫反射的结果位于$[0,1]$区间，那么我们只需要**将该点乘乘以素描纹理的数量，将其扩展到**$[0,Total+1]$**区间**，我们就可以**将漫反射的结果所在区间平均划分为**$Total+1$**个区间**，第一个区间使用纯白色（即纹理笔画密度为0）表示最亮的部分，其余每个区间代表着不同亮度的素描纹理并对他们依次采样，但是如果每一部分区间只对应一个纹理，那么纹理与纹理之间无法平滑过渡，因此我们让**每一部分区间对应两张纹理**，即$[0,1]$对应最亮和次亮的纹理，$[1,2]$对应次亮和中亮的纹理，以此类推，每一部分区间总权重为1，并**按照漫反射系数的大小进行权重分配**，该技术又被称为**多纹理交叉淡化 (Cross-fading between textures) **，具体细节将在代码中展示。

同时**素描还需要描边效果**，我们将直接复用17.1节中的描边`Pass`。

{% note info %}
这种使用多张素描纹理的渲染方式又被称为**色调艺术映射(Tonal Art Map, TAM)**，这些素描纹理的多级渐远纹理(mipmaps)与一般纹理所使用的降采样方式不同，我们需要保持笔触之间的间隔，以便更真实地模拟素描效果。<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/63937386/1773575536390-327e9330-6093-4bb0-b4b0-66017fe1e402.png)

{% endnote %}

### 实现
```csharp
Shader "Unlit/Sketch"
{
    Properties
    {
        //整体颜色
        _MainColor ("MainColor", Color) = (1,1,1,1)
        //纹理整体缩放(密度)
        _TileFactor("TileFactor", Float) = 1
        //六张素描纹理
        _Hatch0("Hatch0", 2D) = ""{}
        _Hatch1("Hatch1", 2D) = ""{}
        _Hatch2("Hatch2", 2D) = ""{}
        _Hatch3("Hatch3", 2D) = ""{}
        _Hatch4("Hatch4", 2D) = ""{}
        _Hatch5("Hatch5", 2D) = ""{}
        //描边Pass所需参数
        _OutlineColor("OutlineColor", Color) = (0,0,0,0)
        _OutlineWidth("OutlineWidth", Range(0, 0.015)) = 0.01
    }
    SubShader
    {
        Tags { "RenderType"="Opaque" "LightMode" = "ForwardBase"}

        //Untiy内部会将名称全部转成大写形式
        UsePass "Unlit/Cartoon/OUTLINE"

        Pass
        {
            CGPROGRAM
            #pragma vertex vert
            #pragma fragment frag
            #pragma multi_compile_fwdbase

            #include "UnityCG.cginc"
            #include "Lighting.cginc"
            #include "AutoLight.cginc"

            fixed4 _MainColor;
            float _TileFactor;
            sampler2D _Hatch0;
            sampler2D _Hatch1;
            sampler2D _Hatch2;
            sampler2D _Hatch3;
            sampler2D _Hatch4;
            sampler2D _Hatch5;

            struct v2f
            {
                float2 uv : TEXCOORD0;
                float4 pos : SV_POSITION;
                //分别代表6张纹理的权重
                fixed3 hatchWeights012 : TEXCOORD1;
                fixed3 hatchWeights345 : TEXCOORD2;
                //用于计算光照衰减
                float3 worldPos : TEXCOORD3;
                SHADOW_COORDS(4)
            };            

            v2f vert (appdata_base v)
            {
                v2f o;
                o.pos = UnityObjectToClipPos(v.vertex);
                o.worldPos = mul(unity_ObjectToWorld, v.vertex);
                TRANSFER_SHADOW(o);

                //xy代表纹理缩放 通过乘以_TileFactor来控制
                o.uv = v.texcoord.xy * _TileFactor;

                float3 lightDir = normalize(WorldSpaceLightDir(v.vertex));
                float3 worldNormal = normalize(UnityObjectToWorldNormal(v.normal));

                //将漫反射区间拓展到0-7 多余的1个区间用来表示最亮的区域(纯白色)
                float diff = saturate(dot(lightDir, worldNormal)) * 7;

                //初始化纹理权重
                o.hatchWeights012 = fixed3(0,0,0);
                o.hatchWeights345 = fixed3(0,0,0);

                if(diff > 6.0)
                {
                    //最亮的部分 保留纹理权重为0 直接使用白色 
                }
                else if(diff > 5.0)
                {
                    //使用0号纹理和MainColor的混合权重
                    //diff - 5为0号纹理的权重，剩余部分直接使用白色
                    o.hatchWeights012.x = diff - 5.0;
                }
                else if(diff > 4.0)
                {
                    //使用0号纹理和1号纹理的混合权重
                    //diff - 4为0号纹理的权重，1 - o.hatchWeights012.x为1号纹理的权重
                    //白色权重为0
                    o.hatchWeights012.x = diff - 4.0;
                    o.hatchWeights012.y = 1 - o.hatchWeights012.x;
                }
                else if(diff > 3.0)
                {
                    //使用1号纹理和2号纹理的混合权重
                    o.hatchWeights012.y = diff - 3.0;
                    o.hatchWeights012.z = 1 - o.hatchWeights012.y;
                }
                else if(diff > 2.0)
                {
                    //使用2号纹理和3号纹理的混合权重
                    o.hatchWeights012.z = diff - 2.0;
                    o.hatchWeights345.x = 1 - o.hatchWeights012.z;
                }
                else if(diff > 1.0)
                {
                    //使用3号纹理和4号纹理的混合权重
                    o.hatchWeights345.x = diff - 1.0;
                    o.hatchWeights345.y = 1 - o.hatchWeights345.x;
                }
                //注意这里包括物体背面 即else if(diff >= 0)
                else
                {
                    //使用4号纹理和5号纹理的混合权重
                    o.hatchWeights345.y = diff;
                    o.hatchWeights345.z = 1 - o.hatchWeights345.y;
                }

                return o;
            }

            fixed4 frag (v2f i) : SV_Target
            {
                fixed4 hatchColor0 = tex2D(_Hatch0, i.uv) * i.hatchWeights012.x;
                fixed4 hatchColor1 = tex2D(_Hatch1, i.uv) * i.hatchWeights012.y;
                fixed4 hatchColor2 = tex2D(_Hatch2, i.uv) * i.hatchWeights012.z;
                fixed4 hatchColor3 = tex2D(_Hatch3, i.uv) * i.hatchWeights345.x;
                fixed4 hatchColor4 = tex2D(_Hatch4, i.uv) * i.hatchWeights345.y;
                fixed4 hatchColor5 = tex2D(_Hatch5, i.uv) * i.hatchWeights345.z;

                //一并处理白色的权重
                //如果当前处于最亮的部分，那么白色权重为1
                //如果当前需要和0号纹理混合权重，那么白色的权重等于1-i.hatchWeight012.x
                //如果当前是第i和i+1号纹理混合权重，那么白色的权重为0
                //综上，我们可以这样来合并计算白色的权重：
                fixed4 whiteColor = fixed4(1,1,1,1) * (1 - i.hatchWeights012.x - i.hatchWeights012.y - i.hatchWeights012.z
                                                 - i.hatchWeights345.x - i.hatchWeights345.y - i.hatchWeights345.z);
                //同理，我们也可以合并计算hatch的颜色
                fixed4 hatchColor = hatchColor0 + hatchColor1 + hatchColor2 + hatchColor3 + hatchColor4 + hatchColor5;
                //合并颜色
                fixed4 col = (whiteColor + hatchColor) * _MainColor;
                //计算衰减
                UNITY_LIGHT_ATTENUATION(atten, i, i.worldPos);

                return fixed4(col.rgb * atten, 1);
            }
            ENDCG
        }
    }
    Fallback "Diffuse"
}
```

# 噪声
## 噪声的原理
**噪声**是一种**由数学算法公式生成**的有规则性或可控的随机数据，不会突然跳跃或变化，而是呈现出逐渐过渡的效果，适合模拟自然现象；同时我们**可以通过调整算法的输入参数来调整噪声的表现形式**；我们也**可以生成三维及以上维度的噪声**；但要注意的是噪声值在不改变输入参数的情况下将**会呈周期性出现**，这要求我们通过调整噪声的范围或修改算法来避免。

常用的噪声算法有：

+ Perlin Noise（柏林噪声）：适合生成自然现象的纹理（比如云、火焰、地形）；
+ Simplex Noise（简单噪声）：Perlin Noise的优化版，更适合实时计算，适用于体积云、流体动画等；
+ Random Function（随机噪声/白噪音）：计算简单，适合生成粒子效果或星空背景；
+ Fractal Noise（分形噪声）：将多层PerlinNoise或SimplexNoise叠加，生成复杂效果，适用于高细节地形、云层、火焰等效果；
+ Worley Noise（沃利噪声）：生成类似“细胞”的纹理，适用于模拟裂纹或有机表面

## 如何在Unity中使用噪声
Unity提供了一些噪声API，例如`Mathf.PerlinNoise()`，但是种类非常少；`Shader Graph`中提供了噪声节点**，但由于我们正在学习`CG/HLSL`，因此我们选择使用最普遍的方式，即**使用预先生成的噪声纹理**，这样就可以省去噪声算法的计算带来的性能消耗，即用空间换时间。

### 使用`Mathf.PerlinNoise()`
```csharp
using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEditor;

using System.IO;

public class PerlinNoiseTextureTool : EditorWindow
{
    //纹理宽高
    private int tWidth = 512;
    private int tHeight = 512;
    //纹理缩放
    private int tScale = 20;
    //纹理名称
    private string tName = "PerlinNoiseTexture";
    [MenuItem("柏林噪声纹理生成工具/打开")]
    public static void ShowWindow()
    {
        GetWindow<PerlinNoiseTextureTool>("柏林噪声纹理生成工具");
    }

    private void OnGUI()
    {
        GUILayout.Label("柏林噪声纹理设置");
        tWidth = EditorGUILayout.IntField("纹理宽度", tWidth);
        tHeight = EditorGUILayout.IntField("纹理高度", tHeight);
        tScale = EditorGUILayout.IntField("纹理缩放", tScale);
        tName = EditorGUILayout.TextField("纹理名称", tName);

        if (GUILayout.Button("生成柏林噪声纹理"))
        {
            Texture2D texture = new Texture2D(tWidth, tWidth);

            //逐像素写入纹理
            for(int y = 0; y < tHeight; y++)
            {
                for(int x = 0; x < tWidth; x++)
                {
                    float col = Mathf.PerlinNoise((float)x/tWidth * tScale, (float)y/tHeight * tScale);
                    texture.SetPixel(x, y, new Color(col, col, col));
                }
            }
            texture.Apply();

            //存储纹理
            File.WriteAllBytes("Assets/Scripts/Noise/" + tName + ".png", texture.EncodeToPNG());
            AssetDatabase.Refresh();

            EditorUtility.DisplayDialog("提示", "柏林噪声纹理已生成", "确定");
        }
    }
}
```

## 消融效果
### 原理
消融（dissolve）效果常见于游戏中的角色死亡、地图烧毁等效果。在这些效果中，消融往往从不同的区域开始，并向看似随机的方向扩张，最后整个物体都将消失不见。

消融效果本质上就是**噪声纹理和透明度测试的结合**：我们使用噪声纹理中RGB的任一分量与一个控制消融程度的阈值相比较，如果小于阈值，我们就使用`clip()`函数将他对应的像素剔除掉，剔除的像素就是被“烧毁”的区域。

消融的部分的边缘还需要额外处理，例如火焰消融效果的边缘会有火焰和灰烬的颜色，这些颜色我们将使用渐变纹理的方式，并通过线性插值将其映射到边缘处。线性插值的权重使用`smoothstep`进行计算，使得颜色能够在边缘的一定范围内（边缘宽度）从源颜色向边缘颜色平滑过渡。

### 实现
```csharp
Shader "Unlit/Dissolve"
{
    Properties
    {
        _MainTex ("Texture", 2D) = "" {}
        //噪声纹理
        _NoiseTex("NoiseTex", 2D) = ""{}
        //边缘颜色
        _Gradient("Gradient", 2D) = ""{}
        _BumpMap("BumpMap", 2D) = ""{}
        _BumpScale("BumpScale", Range(0,1)) = 1

        //消融程度
        _Dissolve("Dissolve", Range(0,1)) = 0
        //边缘宽度
        _EdgeRange("EdgeRange", Range(0,1)) = 0

        _DiffuseColor("DiffuseColor", Color) = (1,1,1,1)
        _SpecularColor("SpecularColor", Color) = (1,1,1,1)
        _Gloss("Gloss", Range(0,20)) = 16
    }
    SubShader 
    {
        Pass
        {
            Tags{"LightMode" = "ForwardBase"}

            CGPROGRAM
            #pragma vertex vert
            #pragma fragment frag
            #pragma multi_compile_fwdbase

            #include "UnityCG.cginc"
            #include "Lighting.cginc"
            #include "AutoLight.cginc"

            struct v2f
            {
                float4 uv : TEXCOORD0;//xyTex, zwBump
                float2 uv_noise : TEXCOORD3; //噪声纹理uv
                float4 pos : SV_POSITION;
                float3 lightDir : TEXCOORD1; //切线空间下
                float3 viewDir : TEXCOORD2; //切线空间下
                float3 worldPos : TEXCOORD4;
                SHADOW_COORDS(5)
                
            };

            sampler2D _MainTex;
            float4 _MainTex_ST;
            sampler2D _BumpMap;
            float4 _BumpMap_ST;
            float _BumpScale;
            fixed4 _DiffuseColor;
            fixed4 _SpecularColor;
            float _Gloss;

            sampler2D _NoiseTex;
            float4 _NoiseTex_ST;
            sampler2D _Gradient;
            fixed _Dissolve;
            fixed _EdgeRange;

            v2f vert (appdata_full v)
            {
                v2f o;
                o.pos = UnityObjectToClipPos(v.vertex);

                o.uv.xy = TRANSFORM_TEX(v.texcoord, _MainTex);
                o.uv.zw = TRANSFORM_TEX(v.texcoord, _BumpMap);
                o.uv_noise = TRANSFORM_TEX(v.texcoord, _NoiseTex);

                float3 binormal = cross(normalize(v.normal), normalize(v.tangent.xyz)) * v.tangent.w;
                
                //模型空间变换到切线空间的矩阵
                float3x3 rotation = float3x3(v.tangent.xyz, 
                                             binormal, 
                                             v.normal);
                //TANGENT_SPACE_ROTATION;

                o.lightDir = mul(rotation, ObjSpaceLightDir(v.vertex));
                o.viewDir = mul(rotation, ObjSpaceViewDir(v.vertex));
                o.worldPos = mul(unity_ObjectToWorld, v.vertex);
                TRANSFER_SHADOW(o);
                return o;
            }

            fixed4 frag (v2f i) : SV_Target
            {
                float4 packedNormal = tex2D(_BumpMap, i.uv.zw);
                float3 tangentNormal = UnpackNormal(packedNormal);
                tangentNormal *= _BumpScale;
                tangentNormal.z = sqrt(1 - saturate(dot(tangentNormal.xy,tangentNormal.xy)));

                float3 tangentLightDir = normalize(i.lightDir);
                float3 tangentViewDir = normalize(i.viewDir);
                
                fixed burn = tex2D(_NoiseTex, i.uv_noise).r;
                
                //保证消融效果最大时物体被完全剔除
                clip(_Dissolve == 1 ? -1 : burn - _Dissolve);

                //消融权重
                fixed t = 1 - smoothstep(0, _EdgeRange, burn - _Dissolve);
                //在渐变纹理中横向采样
                fixed3 burnColor = tex2D(_Gradient, fixed2(t, 0.5)).rgb;

                fixed3 albedo = tex2D(_MainTex, i.uv.xy) * _DiffuseColor.rgb;
                fixed3 diffuse = _LightColor0.rgb * albedo * max(0, dot(tangentLightDir, tangentNormal));
                
                float3 halfDir = normalize(tangentViewDir + tangentLightDir);
                fixed3 specular = _LightColor0.rgb * _SpecularColor.rgb * pow(max(0, dot(halfDir, tangentNormal)), _Gloss);

                UNITY_LIGHT_ATTENUATION(atten, i, i.worldPos);

                fixed3 color = UNITY_LIGHTMODEL_AMBIENT.rgb * albedo + diffuse*atten + specular;

                fixed3 finalColor = lerp(color, burnColor, t * step(0.0001, _Dissolve));

                return fixed4(finalColor, 1);
            }
            ENDCG
        }

        Pass {
            Tags { "LightMode" = "ShadowCaster" }

            CGPROGRAM
            #pragma vertex vert
            #pragma fragment frag
                //
            #pragma multi_compile_shadowcaster
            #include "UnityCG.cginc"

            sampler2D _NoiseTex;
            float4 _NoiseTex_ST;
            fixed _Dissolve;


            struct v2f {
                V2F_SHADOW_CASTER;
                float2 uv_noise : TEXCOORD0; //噪声纹理uv
            };

            v2f vert(appdata_base v)
            {
                v2f o;
                o.uv_noise = TRANSFORM_TEX(v.texcoord, _NoiseTex);
                TRANSFER_SHADOW_CASTER_NORMALOFFSET(o)
                return o;
            }

            float4 frag(v2f i) : SV_Target
            {
                fixed burn = tex2D(_NoiseTex, i.uv_noise).r;
                //保证消融效果最大时物体被完全剔除
                clip(_Dissolve == 1 ? -1 : burn - _Dissolve);

                SHADOW_CASTER_FRAGMENT(i)
            }
            ENDCG
        }
    }
    Fallback "Diffuse"
}
```

+ `t * step(0.0001, _Dissolve)`：由于`t = 1 - smoothstep(0, _EdgeRange, burn - _Dissolve)`，这意味着当`burn < _EdgeRange`时，`t`的最小值实际上不等于0，这意味着消融进度为0时，消融的权重不一定是零。因此，我们**使用`step`来保证在消融进度为0时，物体一定使用源颜色渲染**。

{% note info %}
使用透明度测试的物体的阴影需要特别处理，如果仍然使用普通的阴影`Pass`，那么**被剔除的区域仍然会向其他物体投射阴影**，造成“穿帮”。为了让物体的阴影也能配合透明度测试产生正确的效果，我们需要自定义一个投射阴影的`Pass`。

{% endnote %}

## 水波效果
### 原理
我们曾在11.2.1节中制作了带法线纹理的玻璃效果，水波效果的实现方式与其十分相像，只不过水波的法线纹理是从**噪声纹理**中获取的，而且会随着时间的变化而不断平移。同时，我们将加入**菲涅尔反射**来控制原先带法线纹理的玻璃效果的折射程度，使得水面的反射与折射更加真实。

但是如果只单纯在噪声纹理的基础上使用`_Time.y`时间变量，这样得到的效果仅仅是水面在某个方向上整体平移，效果非常假，因此，我们将使用**双重采样**的方式，**对噪声纹理进行两次采样**，然后让他们**朝相反的方向移动**，并将两次采样的结果叠加，这样得到的结果就会出现明显的波浪感，即波峰与波谷。

### 实现
```csharp
Shader "Unlit/WaterWave"
{
    Properties
    {
        _MainTex("MainTex", 2D) = ""{}
        _WaveMap("WaveMap", 2D) = ""{}
        _Cube ("CubeMap", Cube) = "" {}

        //控制折射扭曲程度
        _Distortion("Distortion", Range(0, 10000)) = 0

        _WaveSpeedX("WaveSpeedX", Range(-0.1, 0.1)) = 0.01
        _WaveSpeedY("WaveSpeedY", Range(-0.1, 0.1)) = 0.01

        //菲涅尔反射系数
        _FresnelScale("FresnelScale", Range(0,1)) = 1
    }
    SubShader
    {
        Tags { "RenderType"="Opaque" "Queue" = "Transparent"}

        //使用它来捕获当前屏幕内容 
        GrabPass{}

        Pass
        {
            Tags { "LightMode"="ForwardBase" }

            CGPROGRAM
            #pragma vertex vert
            #pragma fragment frag

            #include "UnityCG.cginc"
            #include "Lighting.cginc"

            struct v2f
            { 
      
                float4 vertex : SV_POSITION;
                float4 grabPos : TEXCOORD1;
                float4 uv : TEXCOORD2;

                float4 TtoW0 : TEXCOORD3;
                float4 TtoW1 : TEXCOORD4;
                float4 TtoW2 : TEXCOORD5;
            };

            sampler2D _MainTex;
            float4 _MainTex_ST;
            samplerCUBE _Cube;
            sampler2D _GrabTexture;
            float4 _GrabTexture_TexelSize;

            sampler2D _WaveMap;
            float4 _WaveMap_ST;

            float _Distortion;
            fixed _WaveSpeedX;
            fixed _WaveSpeedY;

            fixed _FresnelScale;

            v2f vert (appdata_full v)
            {
                v2f o;
                o.vertex = UnityObjectToClipPos(v.vertex);
                o.grabPos = ComputeScreenPos(o.vertex);
                o.uv.xy = TRANSFORM_TEX(v.texcoord, _MainTex);
                o.uv.zw = TRANSFORM_TEX(v.texcoord, _WaveMap);

                float3 worldPos = mul(unity_ObjectToWorld, v.vertex);
                float3 worldNormal = UnityObjectToWorldNormal(v.normal);
                float3 viewDir = normalize( UnityWorldSpaceViewDir(worldPos));

                float3 worldTangent = UnityObjectToWorldDir(v.tangent);
                float3 worldBinormal = cross(normalize(worldNormal), normalize(worldTangent)) * v.tangent.w;

                o.TtoW0 = float4(worldTangent.x, worldBinormal.x, worldNormal.x, worldPos.x);
                o.TtoW1 = float4(worldTangent.y, worldBinormal.y, worldNormal.y, worldPos.y);
                o.TtoW2 = float4(worldTangent.z, worldBinormal.z, worldNormal.z, worldPos.z);
                return o;
            }

            fixed4 frag (v2f i) : SV_Target
            {
                float3 worldPos = float3(i.TtoW0.w, i.TtoW1.w, i.TtoW2.w);
                fixed3 viewDir = normalize(UnityWorldSpaceViewDir(worldPos));

                //float4 packedNormal = tex2D(_WaveMap, i.uv.zw);
                //float3 tangentNormal = UnpackNormal(packedNormal);
                
                //水波移动速度
                float2 speed = _Time.y * fixed2(_WaveSpeedX, _WaveSpeedY);
                //双重采样
                //注意需要先解压再相加，否则会变成纹理颜色直接相加
                float3 tangentNormal1 = UnpackNormal(tex2D(_WaveMap, i.uv.zw + speed)).rgb; 
                float3 tangentNormal2 = UnpackNormal(tex2D(_WaveMap, i.uv.zw - speed)).rgb; 
                float3 tangentNormal = normalize(tangentNormal1 + tangentNormal2);

                float3 worldNormal = float3(dot(i.TtoW0.xyz, tangentNormal), dot(i.TtoW1.xyz, tangentNormal), dot(i.TtoW2.xyz, tangentNormal));

                float3 reflectDir = reflect(-viewDir, normalize(worldNormal));
                //让水面的材质也进行平移
                fixed4 reflectColor = texCUBE(_Cube, reflectDir) * tex2D(_MainTex, i.uv + speed);
                //为了让_Distortion在不同分辨率的屏幕下表现一致
                float2 offset = tangentNormal.xy * _Distortion * _GrabTexture_TexelSize.xy;

                i.grabPos.xy = offset * i.grabPos.z + i.grabPos.xy;     //深度越深，折射效果越明显
                
                fixed2 screenUV = i.grabPos.xy / i.grabPos.w;   //屏幕坐标转换到uv坐标系 透视除法
                fixed4 grabColor = tex2D(_GrabTexture, screenUV); 

                float fresnel = _FresnelScale + (1 - _FresnelScale) * pow(1 - saturate(dot(viewDir, worldNormal)), 4);

                //在视角方向垂直于水面时显示水下的颜色 在平行于水面时显示反射的颜色
                fixed4 color =  reflectColor * fresnel + grabColor * (1 - fresnel); 

                return color;
            }
            ENDCG
        }
    }
}

```

{% note info %}
在双重采样时，**必须要先使用`UnpackedNormal`解压法线，然后再将两次采样的法线相加并归一化**，因为我们在6.2.4.1节中讲过，`UnpackedNormal`本质上是将法线从纹理颜色的$[0,1]$区间转换到$[-1,1]$区间，如果我们先将法线先相加再解压，相加后的结果颜色位于$[0,2]$区间，这显然是不合理的，同时，哪怕我们先对相加后的颜色进行归一化使其恢复到$[0,1]$区间，但是**对颜色进行归一化本来就是不合理的，毕竟颜色分量本质上不是向量，对其进行归一化将会破坏颜色分量的混合关系。**

{% endnote %}

## 噪声雾效
### 原理
我们曾在15.5节中实现了基于高度的全局雾效，但是那种雾效的浓度之和高度有关，换句话说，雾的浓度是随着高度的变化而均匀变化的，而如果我们想让**雾效能够随着时间的变化而不断飘动，同时雾的浓度也呈现一定的不均匀性**，那么我们就可以引入噪声纹理来辅助实现。

{% note warning %}
注意由于我们需要使用uv偏移，因此使用的噪声纹理在平铺模式下两侧能够相连。

{% endnote %}

噪声纹理中的数据位于$[0,1]$区间，为了让雾的浓度能够在原先的基础上增减，因此我们将**该区间减去0.5**，得到$noise = [-0.5, 0.5]$区间，同时在对噪声纹理采样时同样使用$uv + speed$来实现雾效的移动效果，然后将得到的**能见度**$f$**乘以**$1 + noise$，即可实现雾效的不均匀变化。

{% note warning %}
之所以让噪声纹理的采样数据先减去0.5再加上1，而不是直接加上0.5，是因为**工业界普遍使用**$1$**作为乘法变化的基准**，也就是$f \times 1$表示能见度$f$不变，$f \times 0.9$表示变小，以此类推，因此我们使用$f \times (1 + noise)$来表示噪声纹理对能见度$f$的变化。

{% endnote %}

### 实现
```csharp
Shader "Unlit/NoiseFog"
{
    Properties
    {
        _MainTex ("Texture", 2D) = "white" {}
        _FogColor ("FogColor", Color) = (1,1,1,1)
        _FogDensity ("FogDensity", Float) = 1
        _FogStart ("FogStart", Float) = 0
        _FogEnd ("FogEnd", Float) = 10

        _NoiseTex("NoiseTex", 2D) = ""{}
        _NoiseAmount("NoiseAmount", Float) = 1
        _FogSpeedX("FogSpeedX", Float) = 0.1
        _FogSpeedY("FogSpeedY", Float) = 0.1
    }
    SubShader
    {
        ZWrite Off
        ZTest Always
        Cull Off

        Pass
        {
            CGPROGRAM
            #pragma vertex vert
            #pragma fragment frag

            #include "UnityCG.cginc"

            struct v2f
            {
                float2 uv : TEXCOORD0;
                float2 uv_depth : TEXCOORD1;
                //传递到片元着色器之前将会进行线性插值运算
                float4 Ray : TEXCOORD2;
                float4 vertex : SV_POSITION;
            };

            sampler2D _MainTex;
            half4 _MainTex_TexelSize;
            sampler2D _CameraDepthTexture;

            fixed4 _FogColor;
            half _FogDensity;
            float _FogStart;
            float _FogEnd;
            //0左下 1右下 2右上 3左上 逆时针
            float4x4 _RayMatrix;

            sampler2D _NoiseTex;
            float _NoiseAmount;
            float _FogSpeedX;
            float _FogSpeedY;

            v2f vert (appdata_base v)
            {
                v2f o;
                o.vertex = UnityObjectToClipPos(v.vertex);
                o.uv = v.texcoord;
                o.uv_depth = v.texcoord;

                //通过当前顶点的uv坐标来判断是哪个角上的顶点
                int index = 0;
                if(v.texcoord.x < 0.5 && v.texcoord.y < 0.5)
                    index = 0;
                else if(v.texcoord.x > 0.5 && v.texcoord.y < 0.5)
                    index = 1;
                else if(v.texcoord.x > 0.5 && v.texcoord.y > 0.5)
                    index = 2;
                else if(v.texcoord.x < 0.5 && v.texcoord.y > 0.5)
                    index = 3;
                //为每个角上的顶点选择它们各自的向量
                o.Ray = _RayMatrix[index];

                #if UNITY_UV_STARTS_AT_TOP
                if(_MainTex_TexelSize.y < 0)
                {
                    //这里就能体现出为什么需要逆时针存储4个向量
                    index = 3 - index;
                    o.uv_depth = 1 - o.uv_depth;
                }
                #endif

                return o;
            }

            fixed4 frag (v2f i) : SV_Target
            {
                //观察空间中的z分量
                float4 linearDepth = LinearEyeDepth(SAMPLE_DEPTH_TEXTURE(_CameraDepthTexture, i.uv_depth));
                //计算世界空间中的坐标
                float3 worldPos = _WorldSpaceCameraPos + linearDepth * i.Ray;

                //计算移动速度
                float2 speed = _Time.y * float2(_FogSpeedX, _FogSpeedY);
                //在噪声纹理中采样
                float noise = (tex2D(_NoiseTex, i.uv + speed).r - 0.5) * _NoiseAmount;

                //计算能见度
                float f = (_FogEnd - worldPos.y) / (_FogEnd - _FogStart);
                //使用浓度参数来控制最高能见度的大小
                //并添加噪声效果
                f = saturate(f * _FogDensity * (1 + noise));

                fixed4 col = tex2D(_MainTex, i.uv);
                col.rgb = lerp(_FogColor.rgb, col.rgb, f);

                return col;
            }
            ENDCG
        }
    }
}

```

```csharp
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class NoiseFogTest : PostEffectBase
{
    [SerializeField] private Color fogColor = Color.gray;

    //雾效的浓度
    [Range(0.0f, 3.0f)]
    [SerializeField] private float fogDensity = 1f;

    //雾效起始距离(能见度为1)
    [SerializeField] private float fogStart = 0f;
    //雾效重点距离(能见度为0)
    [SerializeField] private float fogEnd = 100f;

    //噪声纹理
    [SerializeField] private Texture2D noiseTex = null;
    //噪声程度
    [Range(0f, 3f)] [SerializeField] private float noiseAmount = 1f;
    //噪声移动速度
    [Range(-0.5f, 0.5f)] [SerializeField] private float fogSpeedX = 0.1f;
    [Range(-0.5f, 0.5f)] [SerializeField] private float fogSpeedY = 0.1f;

    //我们使用一个4x4的矩阵来一次性向Shader传递4个顶点的Ray向量
    private Matrix4x4 rayMatrix;

    private void OnEnable()
    {
        Camera.main.depthTextureMode = DepthTextureMode.Depth;
    }

    protected override void UpdateProperty()
    {
        if (material != null)
        {
            //获取FOV
            float fov = Camera.main.fieldOfView / 2;
            //获取近裁剪平面距离
            float near = Camera.main.nearClipPlane;
            //获取窗口宽高比
            float aspect = Camera.main.aspect;

            //计算halfHeight = Near * tan(FOV / 2)
            float halfHeight = near * Mathf.Tan(fov * Mathf.Deg2Rad / 2);
            //计算toTop
            Vector3 toTop = Camera.main.transform.up * halfHeight;
            //计算toRight
            Vector3 toRight = Camera.main.transform.right * halfHeight * aspect;

            //计算TL TR BL BR
            Vector3 TL = Camera.main.transform.forward * near + toTop - toRight;
            Vector3 TR = Camera.main.transform.forward * near + toTop + toRight;
            Vector3 BL = Camera.main.transform.forward * near - toTop - toRight;
            Vector3 BR = Camera.main.transform.forward * near - toTop + toRight;

            //计算Ray_TL TR BL BR
            //由于四个向量的模长相等，因此我们记scale = magnitude / near
            float scale = TL.magnitude / near;
            //TL = TL.normalized * TL.magnitude / near;
            TL = TL.normalized * scale;
            TR = TR.normalized * scale;
            BL = BL.normalized * scale;
            BR = BR.normalized * scale;

            //为了便于在Shader中通过uv坐标来判断当前在处理4个顶点中的哪个顶点
            //我们将使用特定顺序来依次向矩阵中存放这四个向量
            //然后在Shader中使用同样的顺序来取出即可
            rayMatrix.SetRow(0, BL);
            rayMatrix.SetRow(1, BR);
            rayMatrix.SetRow(2, TR);
            rayMatrix.SetRow(3, TL);

            //传递属性
            material.SetColor("_FogColor", fogColor);
            material.SetFloat("_FogDensity", fogDensity);
            material.SetFloat("_FogStart", fogStart);
            material.SetFloat("_FogEnd", fogEnd);
            material.SetMatrix("_RayMatrix", rayMatrix);

            material.SetTexture("_NoiseTex", noiseTex);
            material.SetFloat("_FogSpeedX", fogSpeedX);
            material.SetFloat("_FogSpeedY", fogSpeedY);
            material.SetFloat("_NoiseAmount", noiseAmount);
        }
    }
}

```

# 自定义材质球`Inspector`面板显示
{% note warning %}
注意，<font style="color:#DF2A3F;"><b>使用</b></font>`<font style="color:#DF2A3F;"><b>UnityEditor</b></font>`<font style="color:#DF2A3F;"><b>头文件的脚本不能参与游戏的打包</b></font>，因此我们需要将他们放置在`Assets/Editor`文件夹中。

{% endnote %}

## `ShaderGUI`类
如果我们想要自定义某个`Shader`所对应的材质球的`Inspector`面板中显示的内容，我们需要声明一个继承于`ShaderGUI`类的C#脚本，并通过重写`OnGUI`函数来实现相关逻辑，如下所示：

```csharp
using System.Collections;
using System.Collections.Generic;
using UnityEditor;
using UnityEngine;

public class CustomShaderInspector : ShaderGUI
{
    public override void OnGUI(MaterialEditor materialEditor, MaterialProperty[] properties)
    {
        base.OnGUI(materialEditor, properties);
    }
}
```

	如果我们希望让我们的`Shader`文件对应的材质球应用该继承于`ShaderGUI`类所自定义的有关`Inspector`面板的修改，我们需要在`Shader`的最后添加`CustomEditor "类名"`来应用修改，如下所示：

```csharp
Shader "Unlit/CustomShaderInspector"
{
    Properties
    {

    }
    SubShader
    {

    }
    //应用修改
    CustomEditor "CustomShaderInspector"
}

```

### 基本方法
```csharp
Shader "Unlit/CustomShaderInspector"
{
    Properties
    {
        _MainTex ("Texture", 2D) = "white" {}
        _TestFloat ("Float", Float) = 1
    }
    SubShader
    {
        Tags { "RenderType"="Opaque" }

        Pass
        {
            CGPROGRAM
            #pragma vertex vert
            #pragma fragment frag

            #include "UnityCG.cginc"

            struct v2f
            {
                float2 uv : TEXCOORD0;
                float4 vertex : SV_POSITION;
            };

            sampler2D _MainTex;
            float4 _MainTex_ST;
            float _TestFloat;

            v2f vert (appdata_base v)
            {
                v2f o;
                o.vertex = UnityObjectToClipPos(v.vertex);
                o.uv = TRANSFORM_TEX(v.texcoord, _MainTex);
                return o;
            }

            fixed4 frag (v2f i) : SV_Target
            {
                fixed4 col = tex2D(_MainTex, i.uv);
                return col;
            }
            ENDCG
        }
    }
    //应用修改
    CustomEditor "CustomShaderInspector"
}

```

```csharp
using System.Collections;
using System.Collections.Generic;
using UnityEditor;
using UnityEngine;

public class CustomShaderInspector : ShaderGUI
{
    private bool isShow = true;

    public override void OnGUI(MaterialEditor materialEditor, MaterialProperty[] properties)
    {
        //默认显示方式
        //base.OnGUI(materialEditor, properties);

        //MaterialEditor materialEditor 有关材质球Inspector的相关信息与方法
        //MaterialProperty[] properties Shader中的Properties属性

        //OnGUI函数内同样可以使用编辑器拓展相关内容
        if (GUILayout.Button(isShow ? "隐藏所有属性设置" : "显示所有属性设置"))
        {
            isShow = !isShow;
        }

        //获取当前材质球
        Material material = materialEditor.target as Material;

        //重置材质属性
        if (GUILayout.Button("重置所有属性设置"))
        {
            material.SetTexture("_MainTex", null);
            material.SetFloat("_TestFloat", 0);
        }

        //设置渲染队列
        material.renderQueue = EditorGUILayout.IntField("渲染队列", material.renderQueue);

        //控制属性在Inspector中显示
        if (isShow)
        {
            //foreach (var property in properties)
            //{
            //    //property.name: Shader中定义的属性的变量名
            //    //property.displayName: Shader中定义的属性在Inspector中显示的名称
            //    if (property.name == "_TestFloat")
            //    {
            //        //使用自定义的滑动条来设置TestFloat的值与显示名称
            //        property.floatValue = EditorGUILayout.Slider("自定义TestFloat", property.floatValue, -1f, 1f);
            //    }
            //    else
            //    {
            //        //ShaderProperty() 将对应的Properties在Inspector中显示为自定义的名称
            //        materialEditor.ShaderProperty(property, property.displayName);
            //    }
            //}

            //如果我们有大量需要自定义显示的属性
            //我们可以使用FindProperty()方法
            //即从properties数组中找到名为_TestFloat的属性并返回
            MaterialProperty property = FindProperty("_TestFloat", properties);

            //使用自定义的滑动条来设置TestFloat的值与显示名称
            property.floatValue = EditorGUILayout.Slider("自定义TestFloat", property.floatValue, -1f, 1f);

            MaterialProperty mainTex = FindProperty("_MainTex", properties);
            materialEditor.ShaderProperty(mainTex, mainTex.displayName);
        }
    }
}
```

+ `MaterialProperty property`中可以通过调用其成员变量名来获取并设置属性值，调用的成员变量视该属性类型而定。其成员变量如下所示：`colorValue``floatValue``hasMixedValue``intValue``textureValue``vectorValue`。

## `Shader`关键字
### 关键字命名规则
通常**使用大写字母和下划线分隔**（_大写单词_大写单词...），比如：`_Test_Keyword`

### 全局关键字
全局关键字指的是Unity自带的关键字，所有`Shader`中均可直接调用。

### 局部`Shader`关键字
声明局部关键字有两种方式：

+ `#pragma **shader_feature** 关键字1 关键字2 关键字3....`：该编译指令声明的关键字，**只有在关键字启用时**才会生成对应Shader变体；**编译更快，Shader文件更小**，适用开关功能较少的场景；
+ `#pragma **multi_compile** 关键字1 关键字2 关键字3....`：该编译指令声明的关键字，不管是否启用都会生成对应Shader变体；编译更长，Shader文件更大，适用需要完整覆盖的功能。

### 关键字使用规则
```csharp
#if defined(关键词名)
 ....
#elif defined(关键词名)
 ....
#else
 ....
#endif
```

### 启用和禁用关键字
```csharp
//C#
Shader.EnableKeyword("关键字名");
Shader.DisableKeyword("关键字名");
```

### 条件分支和`Shader`变体的区别
条件分支语句(`if - else`)在执行时会有一定的性能开销；`Shader`变体(`#if define`)并不会在执行时带来额外的性能开销，但是会增加编译时间并占用更多的空间，即**用空间换时间**。

如果在运行过程中，我们的判断条件会随着游戏流程不断变化，那么就选择使用条件分支语句；如果不会发生改变，就使用`Shader`变体。

## `MaterialPropertyDrawer`类
上面提到的`ShaderGUI`类是用于自定义整个材质面板的，而`MaterialPropertyDrawer`是用于自定义某一个属性。即对其中一个属性进行更加精细化的自定义封装。

我们一般有两种使用方式，一是在`ShaderGUI`子类中声明一个`MaterialPropertyDrawer`子类对象，然后重写并调用`MaterialPropertyDrawer.OnGUI`函数；二是独立使用`MaterialPropertyDrawer.OnGUI`函数。

注意，<font style="color:#DF2A3F;"><b>继承于</b></font>`<font style="color:#DF2A3F;"><b>MaterialPropertyDrawer</b></font>`<font style="color:#DF2A3F;"><b>的子类的类名必须以</b></font>`<font style="color:#DF2A3F;"><b>Drawer</b></font>`<font style="color:#DF2A3F;"><b>结尾</b></font>，我们会在19.2.2中讲解原因。

### 配合`ShaderGUI`使用
```csharp
using System.Collections;
using System.Collections.Generic;
using UnityEditor;
using UnityEngine;

public class CustomShaderInspector : ShaderGUI
{
    private bool isShow = true;

    //新建用于设置Float类型属性的MaterialPropertyDrawer类对象
    //并使用构造函数传入初始值
    private TestMaterialPropertyDrawer floatDrawer = new TestMaterialPropertyDrawer(-2, 2);

    public override void OnGUI(MaterialEditor materialEditor, MaterialProperty[] properties)
    {
        //OnGUI函数内同样可以使用编辑器拓展相关内容
        if (GUILayout.Button(isShow ? "隐藏所有属性设置" : "显示所有属性设置"))
        {
            isShow = !isShow;
        }

        //获取当前材质球
        Material material = materialEditor.target as Material;

        //重置材质属性
        if (GUILayout.Button("重置所有属性设置"))
        {
            material.SetTexture("_MainTex", null);
            material.SetFloat("_TestFloat", 0);
        }

        //设置渲染队列
        material.renderQueue = EditorGUILayout.IntField("渲染队列", material.renderQueue);

        //控制属性在Inspector中显示
        if (isShow)
        {
            foreach (var property in properties)
            {
                if (property.name == "_TestFloat")
                {
                    //使用MaterialPropertyDrawer类来设置TestFloat的值与显示名称
                    //EditorGUILayout.GetControlRect(): 向Unity LayOut自动布局系统申请一块空间并返回坐标
                    //即直接使用自动布局系统
                    floatDrawer.OnGUI(EditorGUILayout.GetControlRect(), property, property.displayName, materialEditor);
                }
                else
                {
                    materialEditor.ShaderProperty(property, property.displayName);
                }
            }
        }
    }
}
```

```csharp
using System.Collections;
using System.Collections.Generic;
using UnityEditor;
using UnityEngine;

public class TestMaterialPropertyDrawer : MaterialPropertyDrawer
{
    private float sliderMin;
    private float sliderMax;

    //使用构造函数传递初始值
    public TestMaterialPropertyDrawer(float sliderMin, float sliderMax)
    {
        this.sliderMin = sliderMin;
        this.sliderMax = sliderMax;
    }

    //这个OnGUI函数使用的是非布局模式，因此我们需要传入空间的Rect坐标位置
    //string label: 该属性在Shader中定义的在Inspector面板中的显示名称
    public override void OnGUI(Rect position, MaterialProperty prop, string label, MaterialEditor editor)
    {
        //base.OnGUI(position, prop, label, editor);

        //prop.type: Shader中的属性变量类型，值为MaterialProperty.PropType枚举类型
        //如果传入OnGUI的属性不是Float类型 就直接return
        if (prop.type != MaterialProperty.PropType.Float)
        {
            EditorGUILayout.LabelField(label, "请使用数值类型");
            return;
        }

        //使用滑动条控件设置数值
        prop.floatValue = EditorGUILayout.Slider(label, prop.floatValue, sliderMin, sliderMax);
    }
}
```

### 独立使用
通常独立使用`MaterialPropertyDrawer`这种方式更加常用，其使用方法如下：

我们需要**在需要使用`MaterialPropertyDrawer`类的`Shader`属性前添加`[类名()]`，同时填入的`类名`需要删除末尾的`Drawer`字符，`Unity`会自动为我们添加<font style="color:#DF2A3F;"><b>，因此继承自</b></font>`<font style="color:#DF2A3F;"><b>MaterialPropertyDrawer</b></font>`<font style="color:#DF2A3F;"><b>的子类的类名都应使用</b></font>`<font style="color:#DF2A3F;"><b>Drawer</b></font>`<font style="color:#DF2A3F;"><b>结尾。</b></font>同时此处填入的`类名`实际上是构造函数，因此我们可以使用重载的构造函数来传递数值。**

**但是独立使用`Unity`会报错，有bug。**

```csharp
Shader "Unlit/CustomShaderInspector"
{
    Properties
    {
        _MainTex ("Texture", 2D) = "white" {}
        _TestFloat ("Float", Float) = 1
        [TestMaterialProperty(-2.0, 2.0)] _TestFloat2 ("Float2", Float) = 1
    }
    SubShader
    {
        Tags { "RenderType"="Opaque" }

        Pass
        {
            CGPROGRAM
            #pragma vertex vert
            #pragma fragment frag

            #include "UnityCG.cginc"

            struct v2f
            {
                float2 uv : TEXCOORD0;
                float4 vertex : SV_POSITION;
            };

            sampler2D _MainTex;
            float4 _MainTex_ST;
            float _TestFloat;
            float _TestFloat2;

            v2f vert (appdata_base v)
            {
                v2f o;
                o.vertex = UnityObjectToClipPos(v.vertex);
                o.uv = TRANSFORM_TEX(v.texcoord, _MainTex);
                return o;
            }

            fixed4 frag (v2f i) : SV_Target
            {
                fixed4 col = tex2D(_MainTex, i.uv);
                return col;
            }
            ENDCG
        }
    }
    //应用修改
    //CustomEditor "CustomShaderInspector"
}

```

### `ToggleDrawer`类
该类继承自`MaterialPropertyDrawer`类，可以在`Shader`属性中声明**带有`[Toggle]`或`[Toggle(自定义关键字)]`前缀的属性**，其值类型为`Float`，同时在`Inspector`窗口中将会显示一个**勾选框**，**确认勾选则该属性值为1，反之则为0**，我们可以利用这一特性**配合条件分支语句或`Shader`变体**，即可用于开关`Shader`中的某些特效等。

```csharp
Shader "Unlit/TestToggleDrawer"
{
    Properties
    {
        _MainTex ("Texture", 2D) = "white" {}
        //使用变量
        [Toggle] _ShowTex("ShowTex", Float) = 1
        //使用自定义关键字
        [Toggle(_SHOWBLACK)] _ShowBlack("ShowBlack", Float) = 1
    }
    SubShader
    {
        Tags { "RenderType"="Opaque" }

        Pass
        {
            CGPROGRAM
            #pragma vertex vert
            #pragma fragment frag

            //使用自定义关键字
            #pragma shader_feature _SHOWBLACK

            #include "UnityCG.cginc"

            struct v2f
            {
                float2 uv : TEXCOORD0;
                float4 vertex : SV_POSITION;
            };

            sampler2D _MainTex;
            float4 _MainTex_ST;

            //相当于bool变量
            fixed _ShowTex;

            v2f vert (appdata_base v)
            {
                v2f o;
                o.vertex = UnityObjectToClipPos(v.vertex);
                o.uv = TRANSFORM_TEX(v.texcoord, _MainTex);
                return o;
            }

            fixed4 frag (v2f i) : SV_Target
            {
                fixed4 col = fixed4(1,1,1,1);

                //条件分支判断
                if(_ShowTex)
                    col = tex2D(_MainTex, i.uv);

                //Shader变体
                #ifdef _SHOWBLACK
                    col = fixed4(0,0,0,0);
                #endif

                return col;
            }
            ENDCG
        }
    }
}
```

### `EnumDrawer`类
该类同样继承自`MaterialPropertyDrawer`类，类似于枚举类型，我们可以在`Shader`的`Float`类型的属性前加上`[Enum(枚举显示名称1, 值1, 枚举显示名称2, 值2, ...)]`，这样我们就可以在`Inspector`窗口中通过**枚举类型的下拉列表**来切换该属性的属性值。

（`枚举显示名称`不需要是字符串）

```csharp
Shader "Unlit/EnumDrawer"
{
    Properties
    {
        _MainTex ("Texture", 2D) = "white" {}
        
        //声明枚举类型
        [Enum(ShowBlack, 0, ShowWhite, 1, ShowTex, 2)] _Show("Show", Float) = 0
    }
    SubShader
    {
        Tags { "RenderType"="Opaque" }

        Pass
        {
            CGPROGRAM
            #pragma vertex vert
            #pragma fragment frag

            #include "UnityCG.cginc"

            struct v2f
            {
                float2 uv : TEXCOORD0;
                float4 vertex : SV_POSITION;
            };

            sampler2D _MainTex;
            float4 _MainTex_ST;

            //相当于枚举类型变量
            fixed _Show;

            v2f vert (appdata_base v)
            {
                v2f o;
                o.vertex = UnityObjectToClipPos(v.vertex);
                o.uv = TRANSFORM_TEX(v.texcoord, _MainTex);
                return o;
            }

            fixed4 frag (v2f i) : SV_Target
            {
                fixed4 col = fixed4(1,1,1,1);

                //枚举判断
                switch(_Show)
                {
                    //ShowBlack
                    case 0:
                        col = fixed4(0,0,0,0);
                        break;
                    //ShowWhite
                    case 1:
                        col = fixed4(1,1,1,1);
                        break;
                    //ShowTex
                    case 2:
                        col = tex2D(_MainTex, i.uv);
                        break;
                }

                return col;
            }
            ENDCG
        }
    }
}
```

#### `KeywordEnumDrawer`类
该类同样继承自`MaterialPropertyDrawer`类，与`EnumDrawer`类不同的是，该类主要是通过关键字实现枚举类型，其使用前缀如下：

`[KeywordEnum(显示名1, 显示名2, ...)] 属性名("显示名称", Float) = 0`

在使用该前缀时，`Shader`将会自动生成对应的关键字，我们只**需要在编译指令中声明**（**Unity会自动转成大写，因此需要使用大写声明**）关键字的形式如下：

`_属性名_显示名1`、`_属性名_显示名2`、...

不过我们也可以在`KeywordEnumDrawer`使用`EnumDrawer`中通过属性变量直接进行`switch`的方法。

```csharp
Shader "Unlit/KeywordDrawer"
{
    Properties
    {
        _MainTex ("Texture", 2D) = "white" {}
        
        //声明枚举类型
        [KeywordEnum(Black, White, Tex)] _Show("Show", Float) = 0
    }
    SubShader
    {
        Tags { "RenderType"="Opaque" }

        Pass
        {
            CGPROGRAM
            #pragma vertex vert
            #pragma fragment frag

            //声明关键字 使用全大写 _属性名_显示名
            #pragma shader_feature _SHOW_BLACK _SHOW_WHITE _SHOW_TEX

            #include "UnityCG.cginc"

            struct v2f
            {
                float2 uv : TEXCOORD0;
                float4 vertex : SV_POSITION;
            };

            sampler2D _MainTex;
            float4 _MainTex_ST;

            //相当于枚举类型变量
            //fixed _Show;

            v2f vert (appdata_base v)
            {
                v2f o;
                o.vertex = UnityObjectToClipPos(v.vertex);
                o.uv = TRANSFORM_TEX(v.texcoord, _MainTex);
                return o;
            }

            fixed4 frag (v2f i) : SV_Target
            {
                fixed4 col = fixed4(1,1,1,1);
                
                //枚举判断
                #ifdef _SHOW_BLACK
                    col = fixed4(0,0,0,0);
                #elif defined(_SHOW_WHITE)
                    col = fixed4(1,1,1,1);
                #elif defined(_SHOW_TEX)
                    col = tex2D(_MainTex, i.uv);
                #endif

                //同样可以使用属性值来判断
                //switch(_Show)
                //{
                //    //ShowBlack
                //    case 0:
                //        col = fixed4(0,0,0,0);
                //        break;
                //    //ShowWhite
                //    case 1:
                //        col = fixed4(1,1,1,1);
                //        break;
                //    //ShowTex
                //    case 2:
                //        col = tex2D(_MainTex, i.uv);
                //        break;
                //}

                return col;
            }
            ENDCG
        }
    }
}

```

### `PowerSliderDrawer`类
该类同样继承自`MaterialPropertyDrawer`类，它可以在`Inspector`中通过一个**指数滑块**来调整对应的属性值，其使用方式如下：

`[PowerSlider(指数)] 属性名("显示名称", Range(最小值, 最大值)) = 默认值`

其对应的计算公式为：

$属性值 = 滑块位置^{指数}$

### `IntRangeDrawer`类
该类同样继承自`MaterialPropertyDrawer`类，它可以在`Inspector`中通过一个**整数滑块**，即滑块的属性值只能是整数，以此来调整对应的属性值，其使用方式如下：

`[IntRange] 属性名("显示名称", Range(最小值, 最大值)) = 默认值`

## `Shader`属性的特性
常用的`Shader`属性的特性如下：

+ `HideInInspector`：可以添加到**任意属性**前，用于在`Inspector`窗口中隐藏该属性；
+ `NoScaleOffset`：可添加到**2D纹理贴图属性**前，用于在`Inspecter`窗口中隐藏偏移，即`Tiling`和`Offser`选项；
+ `Normal`：可添加到**2D纹理贴图属性**前，用于检测当前纹理是否被设置为**法线贴图**，如果不是将会弹出提示；
+ `HDR`：可添加到**2D纹理贴图属性或颜色属性**前，可以开启`HDR`效果，即颜色分量上限能够大于1；



+ `[Space]`或`Space(数值)`：可以在某一个属性前添加对应数值的空白行；
+ `[Header(文本标题)]`：添加标题文字。

# 表面着色器
## 基本结构
我们曾在4.5节中简单介绍了一下表面着色器，在这里，我们将详细讲述表面+光照着色器与顶点+片元着色器的不同。

顶点+片元着色器这种类型对于硬件十分友好，但是这种分类不符合人类的思考方式。因此表面+光照着色器被提了出来，其中，**表面着色器定义了模型表面的反射率、法线和高光等**，光照模型则选择是使用兰伯特还是`Blinn-Phong`等模型。而**光照着色器负责计算光照衰减、阴影等**。这样，绝大部分时间我们**只需要和表面着色器打交道**，例如，混合纹理和颜色等。**光照模型可以是提前定义好的**，我们只需要选择哪种预定义的光照模型即可。而光照着色器一旦由系统实现后，更不会被轻易改动，从而大大减轻了`Shader`编写者的工作量。

{% note warning %}
表面+光照着色器只是对于顶点+片元着色器的**“封装”**，Unity本质上还是依靠顶点+片元着色器来运行的，例如表面着色器函数实际上是在片元着色器中运行的。

{% endnote %}

以下是一个Unity自带的`BumpedDiffuse`的表面着色器：

```csharp
Shader "Custom/Lesson135"
{
    Properties
    {
        _Color ("Color", Color) = (1,1,1,1)
        _MainTex ("Albedo (RGB)", 2D) = "white" {}
        _BumpMap("BumpMap", 2D) = "white"{}
        _BumpScale("BumpScale", Range(0,1)) = 1
    }
    SubShader
    {
        Tags { "RenderType"="Opaque" }

        CGPROGRAM

        #pragma surface surf Lambert
        #pragma target 3.0

        sampler2D _MainTex;
        sampler2D _BumpMap;
        float _BumpScale;//凹凸程度
        fixed4 _Color;

        struct Input
        {
            float2 uv_MainTex;
            float2 uv_BumpMap;
        };

        void surf (Input IN, inout SurfaceOutput o)
        {
            fixed4 tex = tex2D (_MainTex, IN.uv_MainTex);
            o.Albedo = tex.rgb * _Color;
            o.Alpha = tex.a * _Color.a;
            
            //乘以凹凸程度的系数
            float3 tangentNormal = UnpackNormal(tex2D(_BumpMap, IN.uv_BumpMap));
            tangentNormal.xy *= _BumpScale;
            tangentNormal.z = sqrt(1.0 - saturate(dot(tangentNormal.xy, tangentNormal.xy)));
            o.Normal = tangentNormal;
        }
        ENDCG
    }
    FallBack "Diffuse"
}

```

	不难发现，表面着色器的代码是直接写在`SubShader`中，而无需撰写`Pass`，因为Unity会自动帮我们调用或生成当前编译指令所需的光照模型的`Pass`，从而大大减少了代码量。

## 编译指令
编译指令最重要的作用是指明该表面着色器使用的**表面函数**和**光照函数**，其基本格式如下：

+ `#pragma surface 表面函数名 光照模型 可选额外参数`

### 表面函数
表面函数与顶点/片元着色器中的“顶点/片元函数”类似，名称可以自定义，但是函数的参数与返回值不同，如下所示（表面函数默认名为`surf`）：

+ `void surf (Input IN, inout SurfaceOutput o)`
+ `void surf (Input IN, inout SurfaceOutputStandard o)`
+ `void surf (Input IN, inout SurfaceOutputStandardSpecular o)`

其中，`Input IN`为前文定义的输入结构体，用于获得各类表面属性；`SurfaceOutput``SurfaceOutputStandard``SurfaceOutputStandardSpecular`为Unity内置的用于输出的结构体，我们会将计算得到的结果存储在这些结构体中。**针对不同的光照模型，我们需要选择不同的输出结构体，因为我们需要使用特定的结构体来向光照函数传递数据**。

### 光照函数
Unity内置了基于物理的光照模型函数`Standard`和`StandardSpecular`以及简单的非基于物理的光照模型函数`Lambert`和`BlinnPhong`。同时我们也可以使用下面的代码自定义光照函数：

```csharp
// 用于不依赖视角的光照模型，例如漫反射
half4 Lighting<Name> (SurfaceOutput s, half3 lightDir, half atten);

// 用于依赖视角的光照模型，例如高光反射
half4 Lighting<Name> (SurfaceOutput s, half3 lightDir, half3 viewDir, half atten);

//使用时需要将<Name>替换为我们自定义的名称，例如LightingMyLambert，然后在编译指令后添加<Name>
//即：#pragma surface surf MyLambert
```

### 可选额外参数
#### 自定义修改函数
表面着色器支持定义**顶点修改函数**来自定义顶点属性，其定义如下所示：

```csharp
void 顶点函数名 (inout appdata_full v)
{
    //修改顶点属性
}
```

使用方法：

+ `#pragma surface 表面函数名 光照模型 vertex:顶点函数名`



表面着色器也支持**最后的颜色修改函数**来修改即将绘制到屏幕上的颜色，其定义如下所示：

```csharp
void 颜色修改函数名 (Input IN, SurfaceOutput o, inout fixed4 color)
{
    //修改即将绘制到屏幕上的颜色color
}
```

使用方法：

+ `#pragma surface 表面函数名 光照模型 finalcolor:颜色修改函数名`

{% note info %}
注意，`#pragma surface 表面函数名 光照模型`后可接多个`可选额外参数`如：

+ `#pragma surface 表面函数名 光照模型 vertex:顶点函数名 finalcolor:颜色修改函数名`

{% endnote %}

#### 阴影
我们可以通过编译指令来控制阴影的投射，例如`addshadow`可以自动为表面着色器**生成一个阴影投射的`Pass`，这样的好处是我们无需使用`Fallback`，同时如果我们使用**顶点修改函数**制作了**顶点动画或透明度测试**，`addshadow`生成的阴影投射`Pass`将会**自动调用顶点修改函数中的逻辑来生成与顶点动画/透明度测试匹配的阴影**；

`fullforwardshadows`参数可以**开启前向渲染路径中所有光源类型的阴影**（默认情况下Unity只会开启最重要的平行光的阴影）；

`noshadow`参数用于禁用阴影。

#### 透明度混合和透明度测试
`alpha`参数可用于**开启透明度混合**，Unity将会**自动添加`Blend`以及关闭深度写入**，但是并不会修改`Tags`，因此我们仍需要**手动添加透明度混合的`Tags`。同时该参数也会**开启`SurfaceOutput`系列输出结构体中的`Alpha`参数**，我们可以用该参数作为透明度进行`Blend`混合；

`alphatest:参数名`用于**开启透明度测试**，Unity将会使用该变量作为**透明度阈值**来剔除片元，我们可以自己定义这个变量。

#### 光照
+ `noambient`不使用任何环境光和光照探针；
+ `novertexlights`不使用任何逐顶点光照；
+ `noforwardadd`去掉所有前向渲染中的额外pass，只会支持一个逐像素平行光，其他光源按照逐顶点或SH来计算；
+ `nofog`关闭雾效处理；
+ `nolightmap`关闭光照烘焙处理。

#### 控制代码生成
默认情况下，表面着色器自动生成的代码包含前向渲染路径、延迟渲染路径使用的`Pass`，这会让`Shader`文件较大，如果我们明确表面着色器只会在某些渲染路径中使用，可以使用以下指令来明确告诉Unity，不需要为某些渲染路径生成代码：

+ `exclude_path:deferred`(排除延迟渲染路径)
+ `exclude_path:forward`（排除前向渲染路径）
+ `exclude_path:prepass`（排除预通道渲染路径）

## 输入输出结构体
### `Input`
前文提到，我们需要自定义`Input`结构体作为表面着色器函数的输入参数，但是`Input`结构体的定义与顶点着色器函数的传入结构体有所不同，后者通过语义来传入数值，而前者只需要按照Unity的命名规范列出所需参数即可，即我们需要用到哪些参数，就在`Input`结构体中写出对应的参数变量名称，如下表所示：

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/63937386/1775291641092-9183a7e6-248a-400e-b52c-abcc0d4e68fc.png)

{% note warning %}
+ `INTERNAL_DATA`：**只有在使用法线贴图时，我们才需要添加该宏。原因在于，上表中的相关参数都是在顶点着色器中进行计算的，而使用法线贴图意味着我们需要在片元着色器中提取切线空间中的法线（即表面着色器中添加`o.Normal = UnpackNormal()`相关逻辑，而表面着色器又运行在片元着色器中），显然，**我们需要根据片元着色器中提取的切线空间法线计算出我们需要的世界空间法线，而不能直接使用顶点着色器中计算的模型本身的法线**（模型空间转换到世界空间），因此我们需要向片元着色器传入$TBN$矩阵来将切线空间中的法线转换到世界空间中，而`INTERNAL_DATA`宏表示**$TBN$**向量**，而后我们在表面着色器中**使用`WorldRefectionVector()`和`WorldNormalVector()`函数即可自动调用该**$TBN$**向量**，并完成切线空间到世界空间法线的计算（`WorldRefectionVector()`将会更进一步，直接算出反射方向）。

{% endnote %}

除此以外，如果我们还需要对主纹理、法线纹理等进行采样，我们只需要在`Input`结构体中添加`uv纹理变量名`即可，例如主纹理变量名为`_MainTex`，对应的`uv`坐标为`uv_MainTex`。

**	**同时，如果我们需要自定义一些变量来实现特殊的渲染效果，我们**也可以在`Input`结构体中自己声明相应的自定义变量**，然后在顶点修改函数和表面着色器函数中调用即可。

### `SurfaceOutput`
`SurfaceOutput`系列的结构体在`Lighting.cginc`中定义，我们只需要直接调用即可。

`SurfaceOutput`主要用于**非基于物理的渲染**，例如`Lambert`或`Blinn-Phong`等。

```csharp
struct SurfaceOutput {
    fixed3 Albedo;    // 漫反射颜色 (基础颜色)
    fixed3 Normal;    // 切线空间下的法线方向
    fixed3 Emission;  // 自发光颜色
    half Specular;    // 高光指数 (控制高光区域的大小，值越大高光越集中)
    fixed Gloss;      // 高光强度 (控制高光的亮度/遮罩)
    fixed Alpha;      // 透明度
};
```

{% note info %}
+ **自发光：`c.rgb += o.Emission;`

{% endnote %}

### `SurfaceOutputStandard`
`SurfaceOutputStandard`适用于**基于物理的渲染（PBR）**，用于渲染**金属**表面，对应`Standard`光照函数。

```csharp
struct SurfaceOutputStandard
{
    fixed3 Albedo;      // 基础颜色 (对于非金属是漫反射色，对于金属是高光反射色)
    fixed3 Normal;      // 切线空间下的法线方向 (如果你修改了法线)
    half3 Emission;     // 自发光颜色
    half Metallic;      // 金属度：0 代表非金属(绝缘体)，1 代表纯金属
    half Smoothness;    // 光滑度：0 代表绝对粗糙，1 代表绝对光滑(如镜面)
    half Occlusion;     // 环境光遮蔽 (AO)：控制间接光照的衰减，默认值为 1 (无遮蔽)
    fixed Alpha;        // 透明度
};
```

{% note warning %}
+ **金属度：<font style="color:rgb(25, 27, 31);"><b>光照射在金属表面会反射是因为金属表面的自由电子能够吸收光子的能量并将其转化为电子的动能。而电子进入激发态之后会在极短的时间内重新回到基态，此时它们会释放出与原先吸收的光子相同频率的光子，形成</b></font><font style="color:rgb(25, 27, 31);">镜面反射</font><font style="color:rgb(25, 27, 31);"><b>。而</b></font><font style="color:rgb(25, 27, 31);">漫反射</font><font style="color:rgb(25, 27, 31);"><b>指的是光子进入物体内部，经过一系列反射或折射后再反射出来，因此光子将会附带上物体表面的颜色，同时反射方向也完全随机。因此</b></font><font style="color:rgb(25, 27, 31);">纯金属导体表面只有镜面反射</font><font style="color:rgb(25, 27, 31);"><b>，但是由于一般的金属表面都有部分被氧化，因此我们需要金属度以及</b></font><font style="color:rgb(25, 27, 31);">金属度贴图</font><font style="color:rgb(25, 27, 31);"><b>来更加细致的调整。</b></font><font style="color:rgb(25, 27, 31);">金属度指的是漫反射和镜面反射的比例，0表示只有漫反射，1表示只有镜面反射。</font>**
+ <font style="color:rgb(25, 27, 31);"><b>粗糙度/光滑度：</b></font><font style="color:rgb(25, 27, 31);">一般的物体表面不是绝对光滑的，而是粗糙的，因此我们需要使用光滑度来模拟物体表面的微小起伏，</font><font style="color:rgb(25, 27, 31);"><b>这种微小起伏会导致光线的散射，导致高光范围大，但是反射模糊柔和；绝对光滑的平面高光范围小，但是反射清晰锐利。</b></font>
+ <font style="color:rgb(25, 27, 31);"><b>镜面反射：</b></font><font style="color:rgb(25, 27, 31);">Unity通过</font><font style="color:rgb(25, 27, 31);"><b>Reflection Probe（反射探针）</b></font><font style="color:rgb(25, 27, 31);">来自动生成用于镜面反射的立方体贴图。Unity在游戏运行时或烘焙时，会自动在它的位置拍下周围360度的环境，并在显存里生成一张</font>`<font style="color:rgb(25, 27, 31);">Cubemap</font>`<font style="color:rgb(25, 27, 31);">并自动调用。</font>

{% endnote %}

### `SurfaceOutputSpecular`
`SurfaceOutputSpecular`适用于**基于物理的渲染（PBR）**，用于渲染**非金属**表面，对应`StandardSpecular`光照函数。

```csharp
struct SurfaceOutputStandardSpecular
{
    fixed3 Albedo;      // 漫反射颜色
    fixed3 Specular;    // 高光颜色 (RGB向量，区别于旧版SurfaceOutput中的单通道标量)
    fixed3 Normal;      // 切线空间下的法线方向 (如果你修改了法线)
    half3 Emission;     // 自发光颜色
    half Smoothness;    // 光滑度：0 代表粗糙，1 代表光滑
    half Occlusion;     // 环境光遮蔽 (AO)：默认值为 1
    fixed Alpha;        // 透明度
};
```

## 表面着色器的渲染计算流水线
<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/63937386/1775302773330-00d5fe20-1be5-405b-8725-e2350aa6350d.png)

## 表面着色器使用法线贴图
```csharp
Shader "Custom/SurfaceBumped"
{
    Properties
    {
        _Color ("Color", Color) = (1,1,1,1)
        _MainTex ("Albedo (RGB)", 2D) = "white" {}
        _BumpTex ("BumpTex", 2D) = ""{}
    }
    SubShader
    {
        Tags { "RenderType"="Opaque" }
        LOD 200

        CGPROGRAM
        #pragma surface surf Standard fullforwardshadows
        #pragma target 3.0

        sampler2D _MainTex;
        sampler2D _BumpTex;

        struct Input
        {
            float2 uv_MainTex;
            float2 uv_BumpTex;
        };

        fixed4 _Color;

        void surf (Input IN, inout SurfaceOutputStandard o)
        {
            o.Albedo = tex2D(_MainTex, IN.uv_MainTex).rgb * _Color.rgb;
            //o.Alpha = tex2D(_MainTex, IN.uv_MainTex).a * _Color.a;

            o.Normal = UnpackNormal(tex2D(_BumpTex, IN.uv_BumpTex));
        }
        ENDCG
    }
    FallBack "Diffuse"
}

```

## 表面着色器实现顶点膨胀
```csharp
Shader "Custom/NormalExtrusion"
{
    Properties
    {
        _Color ("Color", Color) = (1,1,1,1)
        _MainTex ("Albedo (RGB)", 2D) = "white" {}
        _BumpTex ("BumpTex", 2D) = ""{}
        _Expansion("Expansion", Float) = 0
    }
    SubShader
    {
        Tags { "RenderType"="Opaque" }
        LOD 200

        CGPROGRAM
        //由于顶点膨胀需要适配的阴影Pass 因此需要添加addshadow
        #pragma surface surf Standard fullforwardshadows vertex:vert addshadow finalcolor:col
        #pragma target 3.0

        sampler2D _MainTex;
        sampler2D _BumpTex;

        struct Input
        {
            float2 uv_MainTex;
            float2 uv_BumpTex;
        };

        fixed4 _Color;
        //顶点膨胀程度
        float _Expansion;

        void surf (Input IN, inout SurfaceOutputStandard o)
        {
            o.Albedo = tex2D(_MainTex, IN.uv_MainTex).rgb;
            //o.Alpha = tex2D(_MainTex, IN.uv_MainTex).a * _Color.a;

            o.Normal = UnpackNormal(tex2D(_BumpTex, IN.uv_BumpTex));
        }

        void vert(inout appdata_full v)
        {
            v.vertex.xyz += v.normal * _Expansion;
        }

        void col(Input IN, SurfaceOutputStandard o, inout fixed4 color)
        {
            color *= _Color;
        }
        ENDCG
    }
    FallBack "Diffuse"
}

```

## 动态液体效果
```csharp
Shader "Custom/DynamicLiquid"
{
    Properties
    {
        //液体颜色
        _Color ("Color", Color) = (1,1,1,1)
        //高光颜色
        _Specular("Specular", Color) = (0,0,0,0)
        //光滑度
        _Smoothness("Smoothness", Range(0,1)) = 0
        //液体高度
        _Height("Height", Float) = 0

        //波纹变化速度
        _Speed("Speed", Float) = 1
        //波动幅度
        _WaveAmplitude("WaveAmplitude", Float) = 1
        //波动频率
        _WaveFrequency("WaveFrequency", Float) = 1
        //波长倒数
        _InvWaveLength("InvWaveLength", Float) = 1
    }
    SubShader
    {
        Tags { "RenderType"="Transparent" "Queue"="Transparent" "IgnoreProjector"="True"}
        LOD 200

        CGPROGRAM
        #pragma surface surf StandardSpecular addshadow vertex:vert alpha:fade
        #pragma target 3.0

        struct Input
        {
            float2 uv_MainTex;
            //当前像素点在世界空间中的位置
            float3 worldPos;
            //物体几何中心在世界空间中的位置
            float3 centerPos;
        };

        fixed4 _Color;
        fixed4 _Specular;
        half _Smoothness;
        float _Height;
        float _Speed;
        float _WaveAmplitude;
        float _WaveFrequency;
        float _InvWaveLength;

        void vert(inout appdata_full v, out Input IN)
        {
            //初始化Input结构体
            UNITY_INITIALIZE_OUTPUT(Input, IN);
            //将物体中心点转换到世界空间
            IN.centerPos = mul(unity_ObjectToWorld, fixed4(0,0,0,1)).xyz;
        }

        void surf (Input IN, inout SurfaceOutputStandardSpecular o)
        {
            //当前液面高度
            float liquidHeight = IN.centerPos.y - IN.worldPos.y + _Height * 0.01;

            //波纹偏移
            float waveOffset = _WaveAmplitude * sin(_WaveFrequency * _Time.y + IN.worldPos.x * _InvWaveLength);
            liquidHeight += waveOffset;

            //剔除高于液面高度的液体体积
            //需要被剔除的部分liquidHeight为0
            liquidHeight = step(0, liquidHeight);
            //clip函数只有在参数小于0时才会剔除，因此我们需要减去0.001让liquidHeight小于0
            clip(liquidHeight - 0.001);

            o.Albedo = _Color.rgb;
            o.Specular = _Specular.rgb;
            o.Smoothness = _Smoothness;
            o.Alpha = _Color.a;
        }
        ENDCG
    }
    //FallBack "Diffuse"
}

```

# 基于物理的渲染(PBS)
## 次表面散射
**次表面散射光**指的是光线在进入**非金属物体**表面后，会在物体表面内部发生多次折射，最终散射出物体。

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/63937386/1775370293010-5f7b9410-744b-4d31-b20b-b5d7d0dad727.png)

但这同时也意味着，当光线照射到非金属表面的某一个点时，**会有光线从距离该点处一小段距离开外的其他点反射出物体**，如下图所示：

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/63937386/1775370571295-abd21b5c-451c-4aa8-9287-724d32523ee7.png)

**当屏幕像素大小大于次表面散射点和当前顶点之间的距离时，我们就可以忽略两者之间的距离，认为光的反射全都发生在当前顶点处（局部着色渲染）**，如下图所示：

<!-- 这是一张图片，ocr 内容为： -->
![](https://cdn.nlark.com/yuque/0/2026/png/63937386/1775370690477-37c20bf5-daa7-459d-9b88-d9c1c115b369.png)

反之，如果**屏幕像素大小小于次表面散射点和当前顶点之间的距离，我们就需要使用次表面散射渲染技术。**
