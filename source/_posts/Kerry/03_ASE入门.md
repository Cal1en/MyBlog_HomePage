---
title: "[ASE入门] 03 ASE基本操作"
date: 2026-04-05 08:00:00
updated:
categories: 
  - 技术美术
  - Unity
  - ASE入门
---

# 快捷键


`1 + 左键`：一维`float`节点

`5 + 左键`：`Color`节点



`A + 左键`：`Add`

`E + 左键`：`Pow()`节点

`Z + 左键`：`Swizzle`节点

`T + 左键`：`Texture`节点

`M + 左键`：`Multiply`；

`R + 左键`：`Register Local Var`节点；

`V + 左键`：`Append`节点，用于**组合向量分量**。

`. + 左键`：`dot`节点

`o + 左键`：`One Minus`节点，即`1 - 输入值`

`选中节点 + C键`：添加注释

# 节点
+ **`Register Local Var`**：用于临时存储变量值的节点。将变量值存储到自定义变量名的变量中，然后使用**`Get Local Var`**节点选中对应的变量名，即可调用该变量值；
+ **`Swizzle`**：获取向量的各分量；
+ **`Relay`**：预览节点；
+ **`Texture Coordinates`**：`uv`坐标。我们需要将其`Reference`设置为对应的贴图名称之后，我们才能够在材质面板中调整该贴图的缩放和平移。

# `Properties`设置
+ **暴露变量：** 我们需要先在ASE中添加所需的变量节点，然后将他的属性设置为`Property`，即可将其设置为`Properties`中的变量。

<!-- 这是一张图片，ocr 内容为： -->
![](/img/Kerry/03_ASE入门/1775399577719-c4d84f91-f5a3-49dc-b054-f65cada9fdaa.png)

# 流光+扫光效果
## 边缘光
### `Fresnel()`
我们使用类似于**菲涅尔边缘光**的方法来实现：

$(1 - v \cdot  n)^ {RimPower}$ 是一种最简单的边缘光，即原先 $v \cdot n$ 在视角方向与法线方向重合时最强，我们使用`1`减去该值，即可使得视角方向与边缘方向重合时最亮，并控制幂指数`RimPower`来调节边缘光范围。

然后我们可以将其加上`RimBias`，即 $(1 - v \cdot  n)^ {RimPower} + RimBias$，其中$RimBias \in [0,1]$，以此来调节物体整体的亮度下限。

而后将其乘以`RimScale`用于控制整体强度，即：

$$RimScale \times ((1 - v \cdot  n)^ {RimPower} + RimBias)$$

至此，我们完成了最基础的菲涅尔边缘光。我们可以直接调用`Unity Shader`中的 **`Fresnel()`** 函数来实现上述所有过程。

<!-- 这是一张图片，ocr 内容为： -->
![](/img/Kerry/03_ASE入门/1775460205538-f33ce8cd-9079-445d-9ebb-ae57675344ec.png)

![](/img/Kerry/03_ASE入门/1775460299404-5e962845-0917-4d32-b36f-3c4cb93af440.jpeg)

{% note info %}
注意上述最终结果可能会超过1。

{% endnote %}

### `SmoothStep()`
我们可以使用`SmoothStep()`函数略微调整一下上述计算方式：我们将$(1 - v \cdot  n)$带入`SmoothStep()`，并自定义两个`Float`属性变量`RimMin` `RimMax`作为`SmoothStep()`的上下界，即：

+ `SmoothStep(RimMin, RimMax, 1-v·n)`
+ 当$(1 - v \cdot  n)$小于`RimMin`时返回0，大于`RimMax`时返回1，在$[RimMin, RimMax]$区间内使用**埃尔米特插值法**过渡。

![](/img/Kerry/03_ASE入门/1775467479590-b56fee28-7ead-4d86-b504-336a4d296998.jpeg)

{% note info %}
其优点在于可以只使用两个变量`RimMin` `RinMax`控制所有边缘光所需的效果。

{% endnote %}

### 上色
然后我们只需要将上述菲涅尔算子作为边缘光和漫反射光的插值因子即可，即：

+ `Lerp(InnerColor, RimColor, Fresnel())`

同时，我们还需要将该菲涅尔算子作为输出颜色的透明度，即可让物体中心透明，边缘处不透明，并引入`RimIntensity`作为边缘颜色`RimColor`的强度值：

![](/img/Kerry/03_ASE入门/1775468507692-aae1aba6-822d-42c1-9075-f7d20f4f3ca9.jpeg)

## 扫光
扫光效果指的是类似安检门扫描的激光在水平方向上从上向下扫描的效果，本质上就是利用时间变量`Time`（在ASE中为`Time`节点，在`ShaderLab`中为`Time.y`变量）对一张扫光贴图进行采样，然后将采样结果和上述边缘光结果进行叠加。

但是这样直接用`uv + Time`的做法得到的结果只是沿着模型的纹理坐标系（展uv）进行连续采样，并不是在世界空间中从上到下的水平采样，因此我们需要使用`WorldPosition`节点获取世界坐标的$xy$，然后让$y$加上`Time * Speed`即可：

<!-- 这是一张图片，ocr 内容为： -->
![](/img/Kerry/03_ASE入门/1775475613964-2f0476b7-2eae-41f6-8dc5-53ce2d41f80a.png)

![](/img/Kerry/03_ASE入门/1775476263720-2210d6cf-bbdc-4025-88c5-0dd5f090bdd4.jpeg)

但是**直接使用世界坐标**的话，当物体在场景中上下移动时，**扫光效果并不会跟随物体一起上下移动**，因此我们需要使用相对坐标系：我们**将物体的模型空间中心点**$(0,0,0,0)$**转换到世界空间下，再让原先的物体各顶点的世界空间坐标减去该中心点的世界坐标**，即可得到物体上各顶点坐标的相对坐标值，该坐标系为相对坐标系，因此扫光效果将会跟随物体一起移动。

我们可以使用 **`Transform Position`节点来转换坐标空间**：

![](/img/Kerry/03_ASE入门/1775476795127-7bbc1150-c665-4150-a1ba-8970442eea6a.jpeg)

最后将采样结果乘以`FlowIntensity`来控制强度即可：

<!-- 这是一张图片，ocr 内容为： -->
![](/img/Kerry/03_ASE入门/1775477632179-3394c059-0858-4cd5-822f-e341990a065e.png)

## 添加表面细节
由于我们使用菲涅尔算子作为最终渲染结果的透明度通道，因此**渲染出来的物体的靠近中心的部分没有细节**，甚至可能是完全透明的，如果我们需要添加细节的话，可以**使用漫反射贴图的某一个颜色分量**，或使用**法线贴图**。这里我们使用前者：

我们将该分量添加到菲涅尔算子经过`SmoothStep()`后的结果中，并使用`saturate()`截断，将该结果作为漫反射颜色和边缘色的插值因子，这样该分量就会以偏向边缘色的颜色添加到最终的渲染结果中。

<!-- 这是一张图片，ocr 内容为： -->
![](/img/Kerry/03_ASE入门/1775478717612-29c0e506-2a88-4ed3-9104-de308a548c0a.png)

<!-- 这是一张图片，ocr 内容为： -->
![](/img/Kerry/03_ASE入门/1775478740436-4f91333d-7895-4238-aa66-90f64a1dc3bb.png)

## 调整整体透明度
如果物体整体的透明度过低，可以在菲涅尔算子截断后的结果中再加一个`InnerAlpha`后再次截断，即可调整物体整体的透明度：

<!-- 这是一张图片，ocr 内容为： -->
![](/img/Kerry/03_ASE入门/1775479217769-ca2d17cb-7e66-4dbe-98ca-72ece79ce425.png)

## 调整扫光密度
我们通过调整扫光效果所使用的相对坐标系来调整扫光密度：我们只需要将相对坐标值乘以一个`FlowTilling`系数来扩大/缩小各顶点之间的“高度差”，即可调整扫光密度：

## 开启深度写入的半透明效果
在`Unity Shader`中，我们可以通过使用一个**开启深度写入但是关闭颜色输入的`Pass`** 来避免复杂模型自身与自身透明度混合出现错误的问题，在ASE中，我们可以通过勾选`Depth`选项中的 **`Extra Detph Pass`** 来自动添加该`Pass`。

<!-- 这是一张图片，ocr 内容为： -->
![](/img/Kerry/03_ASE入门/1775480748529-c65a4a4e-c6bd-4db1-8d80-a54eff2710d3.png)

## 调整阴影
ASE默认使用的是表面着色器，因此我们也可以向表面着色器**添加可选额外参数**：我们只需要在 **`Additional Surface Options`** 中加入`addshadow`，即可让Unity自动创建对应的阴影`Pass`。

<!-- 这是一张图片，ocr 内容为： -->
![](/img/Kerry/03_ASE入门/1775481517450-bbba087e-3d50-4d8d-a302-98c49a933b6f.png)

## 结果
![](/img/Kerry/03_ASE入门/1775484013149-ae1f7020-3171-4c26-92b9-d1dd9a9ffb86.jpeg)

## 使用`ShaderLab`代码
```csharp
Shader "CS01_03/Scan_code"
{
    Properties
    {
        _MainTex ("Texture", 2D) = "white" {}
        _RimMin("RimMin", Range(-1, 1)) = -1
        _RimMax("RimMax", Range(0, 2)) = 1.43
        _TexPower("TexPower", Range(0,8)) = 4

        _InnerColor("InnerColor", Color) = (1,1,1,1)
        _RimColor("RimColor", Color) = (1,1,1,1)
        _RimIntensity("RimIntensity", Range(0,8)) = 1

        _FlowEmiss("FlowEmiss", 2D) = ""{}
        _FlowTilling("FlowTilling", Float) = 1
        _Speed("Speed", Vector) = (0,1,0,0) 
        _FlowIntensity("FlowIntensity", Range(0,5)) = 1

        _InnerAlpha("InnerAlpha", Range(0,1)) = 0
    }
    SubShader
    {
        Tags { "RenderType"="Transparent" "Queue"="Transparent" "IgnoreProjector"="True"}
        LOD 100

        Pass
        {
            ZWrite On
            ColorMask 0
        }

        Pass
        {
            Blend SrcAlpha One
            ZWrite Off

            CGPROGRAM
            #pragma vertex vert
            #pragma fragment frag

            #include "UnityCG.cginc"

            struct v2f
            {
                float2 uv : TEXCOORD0;
                float4 pos : SV_POSITION;
                float3 worldNormal : TEXCOORD1;
                float3 worldPos : TEXCOORD2;
                float3 WorldPivot :TEXCOORD3;
            };

            sampler2D _MainTex;
            float4 _MainTex_ST;
            half _RimMin;
            half _RimMax;
            half _TexPower;

            fixed4 _InnerColor;
            fixed4 _RimColor;
            half _RimIntensity;

            sampler2D _FlowEmiss;
            half _FlowTilling;
            half2 _Speed;
            half _FlowIntensity;

            half _InnerAlpha;

            v2f vert (appdata_full v)
            {
                v2f o;
                o.pos = UnityObjectToClipPos(v.vertex);
                o.uv = TRANSFORM_TEX(v.texcoord, _MainTex);
                o.worldNormal = UnityObjectToWorldNormal(v.normal);
                o.worldPos = mul(unity_ObjectToWorld, v.vertex);
                o.WorldPivot = mul(unity_ObjectToWorld, fixed4(0,0,0,1));
                return o;
            }

            fixed4 frag (v2f i) : SV_Target
            {
                half3 worldNormal = normalize(i.worldNormal);
                half3 viewDir = normalize(UnityWorldSpaceViewDir(i.worldPos));
                half fresnel = smoothstep(_RimMin, _RimMax, 1 - saturate(dot(viewDir, worldNormal)));
                //主纹理的r通道
                fixed emiss = tex2D(_MainTex, i.uv).r;
                emiss = pow(emiss, _TexPower);
                //最终的菲涅尔算子
                fresnel = saturate(fresnel + emiss);

                half3 rimColor = lerp(_InnerColor, _RimColor * _RimIntensity, fresnel);

                half2 uv_flow = (i.worldPos.xy - i.WorldPivot.xy) * _FlowTilling + (_Time.y * _Speed.xy);
                fixed3 flowColor = tex2D(_FlowEmiss, uv_flow) * _FlowIntensity;

                half alpha = saturate(fresnel + _InnerAlpha);
                
                return fixed4(rimColor + flowColor, alpha);
            }
            ENDCG
        }
    }
    Fallback "Diffuse"
}

```

# 薄膜干涉
## Matcap：Material Capture
`Matcap`技术指的是通过观察空间的法线坐标对一张“材质球”贴图采样：

+ 材质球图片的中心正朝向摄像机，其观察空间法线坐标为$(0,0,-1)$；
+ 材质球图片的最上方朝向观察空间的正上方，坐标为$(0,1,0)$；
+ 显然最下方坐标为$(0,-1,0)$;
+ 最右方坐标为$(1,0,0)$

综上，我们可以得到结论：材质球图片恰好可以使用观察空间坐标的$xy$分量进行采样，我们只需要将其从$[-1,1]$范围转换到$[0,1]$区间即可。

`Matcap`技术的优势在于**无需计算光照以及物体表面的材质信息**，我们可以直接从事先渲染并制作的材质球图片中采样，即可直接获得所需的光照与材质，**没有性能开销**；

但缺点也同样出自这一点：使用`Matcap`渲染的物体表面效果会始终跟随摄像机视角，即不管从什么方向看向该物体**其高光、倒影等渲染效果都始终朝向摄像机**。

## Matcap实现
首先我们需要将物体表面发现从世界空间转换到观察空间中，即调用`View Martix`节点，将其与`World Normal`节点相乘（注意顺序），然后使用`Swizzle`节点获取其$xy$分量，然后将其从$[-1,1]$转换到$[0,1]$区间后对`Matcap`进行采样，并使用`MatcapIntensity`参数控制强度，然后将其与漫反射材质相乘；

我们有可能还需要同时采样多张`Matcap`，然后将他们的效果相加：

<!-- 这是一张图片，ocr 内容为： -->
![](/img/Kerry/03_ASE入门/1775737400486-a93c9edd-3797-4bd6-a2b6-05d7c395958a.png)

## 添加薄膜干涉色彩
所谓的薄膜干涉色彩与`Matcap`类似：法线正朝向摄像机的物体表面呈现某种颜色，然后随着$ (n \cdot v) $的减小而发生颜色的渐变，这种渐变并不是线性的，因此我们需要使用渐变纹理来采样颜色，然后将采样的结果与上述`Matcap`与漫反射的结果相乘：

<!-- 这是一张图片，ocr 内容为： -->
![](/img/Kerry/03_ASE入门/1775737732542-f231fd0f-cc72-4944-8b15-1a0a4dc633c2.png)

## 添加法线贴图
我们只需要将法线贴图连上`World Normal`节点即可。

## 简易后处理
我们使用`Post-Process`包来实现后处理效果：我们为摄像机添加`Post-process Layer`和`Post-process Volume`组件，并调整生效层级，开启`ACES色调映射`：

<!-- 这是一张图片，ocr 内容为： -->
![](/img/Kerry/03_ASE入门/1775737985175-0b736da0-39d2-4b24-981f-abe700552f68.png)





## 结果
<!-- 这是一张图片，ocr 内容为： -->
![](/img/Kerry/03_ASE入门/1775737809232-bed7e82d-3acf-4744-a391-9394d71377bd.png)

<!-- 这是一张图片，ocr 内容为： -->
![](/img/Kerry/03_ASE入门/1775737821872-86d89809-8357-4548-b729-fc60ac24a0f7.png)

## 代码
```csharp
Shader "Unlit/Matcap_code"
{
    Properties
    {
        _MainTex ("Texture", 2D) = "white" {}
        _MatCap("Matcap", 2D) = ""{}
        _MatCapIntensity("MatCapIntensity", Float) = 3
        _MatCapAdd("MatcapAdd", 2D) = ""{}
        _MatCapAddIntensity("MatCapAddIntensity", Float) = 3

        _RampTex("RampTex", 2D) = ""{}
    }
    SubShader
    {
        Tags { "RenderType"="Opaque" }
        LOD 100

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
                float3 worldNormal : TEXCOORD1;
                float3 worldPos : TEXCOORD2;
            };

            sampler2D _MainTex;
            float4 _MainTex_ST;
            sampler2D _MatCap;
            sampler2D _MatCapAdd;
            half _MatCapIntensity;
            half _MatCapAddIntensity;

            sampler2D _RampTex;

            v2f vert (appdata_full v)
            {
                v2f o;
                o.vertex = UnityObjectToClipPos(v.vertex);
                o.uv.xy = TRANSFORM_TEX(v.texcoord, _MainTex);
                o.worldNormal = normalize(UnityObjectToWorldNormal(v.normal));
                o.worldPos = mul(unity_ObjectToWorld, v.vertex);
                return o;
            }

            fixed4 frag (v2f i) : SV_Target
            {
                //Base Matcap
                half3 worldNormal = normalize(i.worldNormal);
                half2 viewNormal = mul(UNITY_MATRIX_V, float4(worldNormal, 0)).xy;
                half2 uv_matcap = (viewNormal + float2(1,1)) * 0.5;
                fixed3 matcap_color = tex2D(_MatCap, uv_matcap) * _MatCapIntensity;

                //Diffuse
                fixed3 diffuse_color = tex2D(_MainTex, i.uv);

                //Ramp
                half3 viewDir = normalize(UnityWorldSpaceViewDir(i.worldPos));
                half2 uv_ramp = half2(saturate(1 - dot(viewDir, worldNormal)), 0.5);
                fixed3 ramp_color = tex2D(_RampTex, uv_ramp);

                fixed3 matcapAdd_color = tex2D(_MatCapAdd, uv_matcap) * _MatCapAddIntensity;

                return fixed4(diffuse_color * ramp_color * matcap_color + matcapAdd_color, 1);
            }
            ENDCG
        }
    }
}
```

# 藤蔓生长
## 原理
藤蔓生长本质上属于**顶点动画**，同时我们还需要使用**透明度测试**来剔除掉未生长出的部分，然后使用`Local Vertex Offset`（顶点修改函数）制作藤蔓尖端的收口效果，即将尖端处的顶点沿法线方向向内偏移。

## 开启透明度测试
我们需要在左侧`Blend Mode`窗口内调整`Render Queue`为`Alpha Test`，ASE将会自动为我们生成并暴露一个名为`Mask Clip Value`的参数作为透明度测试的阈值，即`clip(x - MaskClipValue)`。

## 生长效果
一般来说，藤蔓等长条状模型的v轴是沿着物体的中轴线分布的，因此我们可以通过v轴$ [0,1] $的取值范围作为透明度测试的参数。

由于我们希望用于控制生长长度的`Grow`参数能够正比于生长长度，因此我们采用如下方案：

我们先使用`1 - v`，这样生长长度与`uv`的映射关系就变为了$[1,0]$，即顶端为0，底部为1，然后将`1 - v + Grow`，这样我们就可以利用贴图平铺的特性，将其映射到$[2,1]$区间，并设置`Mask Clip Value = 1`，这样当`Grow`为0时，藤蔓将全部被剔除（$[1,0]$），随着`Grow`逐渐增大，由于根部值最大，因此藤蔓会逐渐从根部向尖端生长，尖端处值始终为1（透明度测试），即可实现生长效果。

## 尖端收口效果
我们可以利用`Local Vertex Offset`将尖端处的顶点沿法线方向反向向内偏移。因此首要问题是如何保证只有尖端处的顶点向内偏移，而其余部分保持不变。

显然，由于我们设置`Mask Clip Value = 1`，因此尖端处的值始终为1，并沿着生长方向向根部逐渐增加，因此我们可以通过`SmoothStep(1, GrowMax, 1 - v + Grow)`并通过调整`GrowMax`来划分尖端收口的范围。

由于上述得到的值是从顶端向根部递增，而收口效果应该是由顶端向根部递减，因此我们还需要调用`One Minus`节点，将其乘以顶点法线，再乘以`-0.01`表示沿法线方向向内并调整数量级，最后乘以`Expand`来人工调整收口效果即可。

最后我们还可以附加一个整体的顶点膨胀/收缩效果来调整藤蔓粗细。

<!-- 这是一张图片，ocr 内容为： -->
![](/img/Kerry/03_ASE入门/1775821635610-29f611ba-80e9-4da1-89aa-da8b09819e92.png)

## 结果
<!-- 这是一张图片，ocr 内容为： -->
![](/img/Kerry/03_ASE入门/1775822030724-a0a810b7-a534-4bad-8cc9-5073547731e2.png)

<!-- 这是一张图片，ocr 内容为： -->
![](/img/Kerry/03_ASE入门/1775822044834-6aa2433a-31f1-4d42-878b-986e5e81388a.png)<!-- 这是一张图片，ocr 内容为： -->
![](/img/Kerry/03_ASE入门/1775822052043-ac1007a0-0077-4efd-b7bd-2e3ed998442f.png)

## 代码
```csharp
Shader "Unlit/CS01_05_vine_Code"
{
    Properties
    {
        _MainTex ("Texture", 2D) = "white" {}
        _Grow("Grow", Range(0,1)) = 0
        _GrowMin("GrowMin", Float) = 1
        _GrowMax("GrowMax", Float) = 1.3
        _MaskClipValue("Mask Clip Value", Float) = 1
        _Expand("Expand", Float) = 1
        _Scale("Scale", Float) = 0
    }
    SubShader
    {
        Tags { "RenderType"="Opaque" }
        LOD 100

        Pass
        {
            CGPROGRAM
            #pragma vertex vert
            #pragma fragment frag

            #include "UnityCG.cginc"

            struct v2f
            {
                float2 uv : TEXCOORD0;
                float4 pos : SV_POSITION;
            };

            sampler2D _MainTex;
            half _Grow;
            half _GrowMin;
            half _GrowMax;
            half _MaskClipValue;
            half _Expand;
            half _Scale;

            v2f vert (appdata_full v)
            {
                v2f o;
                half offset = (1 - smoothstep(_GrowMin, _GrowMax, 1 - v.texcoord.y + _Grow)) * _Expand - _Scale;
                v.vertex.xyz -= offset * 0.01 * v.normal;
                o.pos = UnityObjectToClipPos(v.vertex);
                o.uv = v.texcoord;
                
                return o;
            }

            fixed4 frag (v2f i) : SV_Target
            {
                //透明度测试
                clip(1 - i.uv.y + _Grow - _MaskClipValue);
                fixed4 col = tex2D(_MainTex, i.uv);
                return col;
            }
            ENDCG
        }
    }
}

```

## `Local Vertex Offset`
我们可以通过向`Local Vertex Offset`传递顶点偏移值来完成顶点的膨胀/收缩，但有的时候我们希望使用一些更加自定义的效果，比如直接设定当前顶点的坐标，此时我们可以在左侧`General`面板中找到`Vertex Output`，将其从`Relative`修改成`Absolute`，此时原先的`Local Vertex Offset`就会变成`Local Vertex Position`，我们就可以直接设置顶点的模型空间坐标。

<!-- 这是一张图片，ocr 内容为： -->
![](/img/Kerry/03_ASE入门/1775824472967-6beb5244-c3b5-4ed7-a7fd-9e83a55c70bd.png)<!-- 这是一张图片，ocr 内容为： -->
![](/img/Kerry/03_ASE入门/1775824479422-0f9bea3a-a69e-4be6-b116-bcc5dab8007c.png)

# 魔镜
## 模板测试`Stencil`
**模板测试**的顺序**介于透明度测试和深度测试中间**，其**原理与深度测试**类似：通过设置当前物体片元的`Reference`值，将其与模板缓冲区中的值进行比较，然后我们可以自定义比较的规则`Comparison`、通过模板测试`Pass`、未通过模板测试`Fail`、以及**模板测试通过但是未通过深度测试`ZFail`**之后的操作，同时我们**还可以为模型的正背面分别设定不同的操作，我们只需要关闭背面剔除即可**。

## 为镜面添加模板测试
### 镜面设置
为了渲染镜面后方的物体，我们需要**关闭镜面的颜色写入**，即`ColorMask 0`；同时还需要**关闭深度写入**，以免遮挡后方的模型；

我们只需要将镜面的 **`Reference`设置为1**，并将 **`Comparison`设置为`Always`**，将 **`Pass Front`设置为`Replace`**，即通过模板测试就将`Reference`写入模板缓冲区中；

同时我们还需要保证镜面的渲染顺序在魔镜中的模型之前，这样镜面的模板`Reference`值就会被优先写入模板缓冲区中。但是我们又不希望镜面的渲染顺序晚于场景中的其他物体，否则离摄像机更近的物体会被镜面遮挡而被剔除。因此我们需要让**镜面的渲染顺序晚于不透明物体和透明度测试的物体**，即将渲染队列设置为`>2450`即可。

我们可以先将`Render Queue`设置为`Alpha Test`，此时渲染队列为`2450`，然后我们再设置左侧`General`面板中的 **`Queue Index`** 为`10`，这样渲染队列就为`RenderQueue + QueueIndex = 2460`。

### 模型设置
然后我们将魔镜中的模型 **`Reference`同样设置为1**，将 **`Comparsion`设置为`Equal`**，即只有和模板缓冲区中的值（1）相同的片元才会被渲染出来，**`Pass Front`可以保留默认的`Keep`**，因为`Reference`都是1；

同样的，我们需要让镜面中的模型晚于不透明物体、透明度测试以及镜面渲染，因此我们设置`Render Queue`为`Alpha Test`，`Queue Index`为20。

### “天空盒”
注意到，**由于镜面和魔镜中的模型均晚于不透明物体渲染，这导致不透明物体同样会出现在魔镜中**。

我们可以通过深度测试的方式来解决：我们**导入一个小型的“天空盒”，即一个渲染内表面的球体**，我们同样为其打开模板测试，设置`Reference = 1`，`Comparison = Equal`，然后设置`Render Queue = 2465`，即**保证其晚于镜面渲染，同时早于魔镜内的模型渲染，这样魔镜内的模型就能遮盖住天空盒**；

同时我们还需要**设置天空盒的深度测试，将其`Ztest Mode`设置为`Always`**，即总是通过深度测试，这样天空盒就能遮盖住外部的不透明物体了，同时我们将天空盒的缩放拉大，这样我们就可以近似将天空盒的深度看做无限远。

{% note danger %}
+ **为什么魔镜的天空盒的`Ztest Mode`为`Always`但是却不会遮盖住魔镜与摄像机之间的不透明物体**：虽然模版测试的顺序在深度测试之前，但是我们可以手动设置`ZTest Fail`，即通过模板测试但是未通过深度测试时的操作，该操作默认为`Keep`，即保留模板缓冲区中原有的值，因此，**虽然<u>镜面</u>通过了模板测试，但是镜面没能通过深度测试，触发`Ztest Fail = Keep`**，因此被遮盖的部分并没有写入模板缓冲区中，因此被遮挡部分的天空盒也就无法通过模板测试，进而也就不会被渲染出来了。

{% endnote %}

## 结果
<!-- 这是一张图片，ocr 内容为： -->
![](/img/Kerry/03_ASE入门/1775914637905-15a79e04-e280-4e0d-a73d-a8c67aac00da.png)

## `Shader`替换
在替换材质球的`Shader`文件的时候，如果**两个`Shader`的`Properties`属性<u>变量名称</u>不一致的话**，我们就需要重新上贴图，相反，Unity就会自动保留材质球上已赋有的贴图。

