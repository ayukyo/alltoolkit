# Bezier Curve Utils - Go 贝塞尔曲线工具库

提供贝塞尔曲线的计算、评估和操作工具。纯 Go 实现，零外部依赖。

## 功能特性

### 曲线类型
- **线性贝塞尔曲线** (Linear Bezier, 2 控制点)
- **二次贝塞尔曲线** (Quadratic Bezier, 3 控制点)
- **三次贝塞尔曲线** (Cubic Bezier, 4 控制点)
- **任意阶贝塞尔曲线** (通过 De Casteljau 算法支持任意阶)

### 核心功能
- **点评估**: 在参数 t 处计算曲线上的点
- **导数计算**: 计算曲线的切向量 (一阶导数)
- **长度估算**: 通过自适应细分估算弧长
- **曲线细分**: 在指定参数处分割曲线
- **边界框**: 计算曲线的包围矩形
- **曲线扁平化**: 将曲线转换为多边形近似
- **距离计算**: 计算点到曲线的最小距离
- **直线交点**: 检测曲线与直线的交点

### 变换操作
- **平移** (Translate)
- **缩放** (Scale)
- **旋转** (Rotate)
- **反转** (Reverse)
- **阶数提升** (Elevate Degree)

### 特殊功能
- **缓动函数** (Easing Functions): 基于 CSS 标准的预定义缓动函数
- **圆弧近似**: 用二次贝塞尔曲线近似圆弧
- **圆形近似**: 用 4 条三次贝塞尔曲线近似圆
- **椭圆近似**: 用 4 条三次贝塞尔曲线近似椭圆

## 安装

```go
import "github.com/ayukyo/alltoolkit/Go/bezier_curve_utils"
```

## 快速开始

### 线性贝塞尔曲线

```go
package main

import (
    "fmt"
    "github.com/ayukyo/alltoolkit/Go/bezier_curve_utils"
)

func main() {
    // 创建线性贝塞尔曲线 (直线)
    lb := bezier_curve_utils.NewLinearBezier(
        bezier_curve_utils.Point{X: 0, Y: 0},
        bezier_curve_utils.Point{X: 100, Y: 100},
    )

    // 在 t=0.5 处评估
    pt := lb.EvaluateAt(0.5)
    fmt.Printf("Point at t=0.5: (%.2f, %..2f)\n", pt.X, pt.Y)
    // 输出: Point at t=0.5: (50.00, 50.00)

    // 计算长度
    length := lb.Length()
    fmt.Printf("Length: %.2f\n", length)
    // 输出: Length: 141.42
}
```

### 二次贝塞尔曲线

```go
// 创建抛物线形状的二次贝塞尔曲线
qb := bezier_curve_utils.NewQuadraticBezier(
    bezier_curve_utils.Point{X: 0, Y: 0},
    bezier_curve_utils.Point{X: 50, Y: 100},  // 控制点 (顶点)
    bezier_curve_utils.Point{X: 100, Y: 0},
)

// 计算边界框
bbox := qb.BoundingBox()
fmt.Printf("Bounds: X=[%.2f, %.2f], Y=[%.2f, %.2f]\n",
    bbox.Min.X, bbox.Max.X, bbox.Min.Y, bbox.Max.Y)

// 扁平化曲线
points := qb.Flatten(0.1)  // tolerance = 0.1
fmt.Printf("Flattened to %d points\n", len(points))
```

### 三次贝塞尔曲线

```go
// 创建 S 形曲线
cb := bezier_curve_utils.NewCubicBezier(
    bezier_curve_utils.Point{X: 0, Y: 0},
    bezier_curve_utils.Point{X: 0, Y: 100},
    bezier_curve_utils.Point{X: 100, Y: 100},
    bezier_curve_utils.Point{X: 100, Y: 0},
)

// 采样 10 个均匀分布的点
samples := cb.Samples(10)
for i, pt := range samples {
    fmt.Printf("Sample %d: (%.2f, %.2f)\n", i, pt.X, pt.Y)
}

// 分割曲线
left, right := cb.SplitAt(0.5)
fmt.Printf("Left curve starts at (%.2f, %.2f)\n",
    left.EvaluateAt(0).X, left.EvaluateAt(0).Y)
```

### 缓动函数

```go
// 使用预定义的缓动函数
t := 0.5

// 线性缓动
linearVal := bezier_curve_utils.EaseLinear.Ease(t)

// 加速缓动 (Ease In)
easeInVal := bezier_curve_utils.EaseIn.Ease(t)

// 减速缓动 (Ease Out)
easeOutVal := bezier_curve_utils.EaseOut.Ease(t)

// 加速后减速 (Ease In-Out)
easeInOutVal := bezier_curve_utils.EaseInOut.Ease(t)

// 自定义缓动函数 (CSS cubic-bezier 格式)
customEase := bezier_curve_utils.NewEasingFunction(0.42, 0, 0.58, 1)
customVal := customEase.Ease(t)
```

### 变换操作

```go
cb := bezier_curve_utils.NewCubicBezier(
    bezier_curve_utils.Point{X: 0, Y: 0},
    bezier_curve_utils.Point{X: 25, Y: 100},
    bezier_curve_utils.Point{X: 75, Y: 100},
    bezier_curve_utils.Point{X: 100, Y: 0},
)

// 平移
translated := cb.Translate(50, 50)

// 缩放
scaled := cb.Scale(2)

// 旋转 45 度
rotated := cb.Rotate(math.Pi / 4)

// 组合变换
result := cb.Scale(2).Rotate(math.Pi / 2).Translate(100, 100)
```

### 圆和椭圆近似

```go
// 用贝塞尔曲线近似圆
center := bezier_curve_utils.Point{X: 50, Y: 50}
radius := 40.0
circleCurves := bezier_curve_utils.ApproximateCircle(center, radius)

// 4 条三次贝塞尔曲线组成一个圆
for i, curve := range circleCurves {
    fmt.Printf("Curve %d: start (%.2f, %.2f), end (%.2f, %.2f)\n",
        i, curve.EvaluateAt(0).X, curve.EvaluateAt(0).Y,
        curve.EvaluateAt(1).X, curve.EvaluateAt(1).Y)
}

// 椭圆近似
ellipseCurves := bezier_curve_utils.ApproximateEllipse(center, 40, 20) // rx=40, ry=20
```

### 任意阶贝塞尔曲线

```go
// 创建 5 阶贝塞尔曲线 (6 控制点)
points := []bezier_curve_utils.Point{
    {X: 0, Y: 0},
    {X: 10, Y: 50},
    {X: 30, Y: 100},
    {X: 70, Y: 80},
    {X: 90, Y: 30},
    {X: 100, Y: 0},
}
bc, err := bezier_curve_utils.NewBezierCurve(points)
if err != nil {
    panic(err)
}

fmt.Printf("Curve degree: %d\n", bc.Degree())
pt := bc.EvaluateAt(0.5)
fmt.Printf("Point at t=0.5: (%.2f, %.2f)\n", pt.X, pt.Y)
```

### 直线交点检测

```go
qb := bezier_curve_utils.NewQuadraticBezier(
    bezier_curve_utils.Point{X: 0, Y: 0},
    bezier_curve_utils.Point{X: 50, Y: 100},
    bezier_curve_utils.Point{X: 100, Y: 0},
)

// 检测与水平线的交点
lineStart := bezier_curve_utils.Point{X: 0, Y: 50}
lineEnd := bezier_curve_utils.Point{X: 100, Y: 50}

intersections := qb.IntersectLine(lineStart, lineEnd)
for i, pt := range intersections {
    fmt.Printf("Intersection %d: (%.2f, %.2f)\n", i, pt.X, pt.Y)
}
```

## API 参考

### Point 结构

```go
type Point struct {
    X float64
    Y float64
}
```

### LinearBezier

```go
func NewLinearBezier(p0, p1 Point) *LinearBezier

func (lb *LinearBezier) EvaluateAt(t float64) Point
func (lb *LinearBezier) DerivativeAt(t float64) Point
func (lb *LinearBezier) Length() float64
func (lb *LinearBezier) Flatten(tolerance float64) []Point
func (lb *LinearBezier) BoundingBox() BoundingBox
func (lb *LinearBezier) SplitAt(t float64) (*LinearBezier, *LinearBezier)
func (lb *LinearBezier) DistanceToPoint(p Point) float64
func (lb *LinearBezier) IntersectLine(p0, p1 Point) []Point
func (lb *LinearBezier) Samples(n int) []Point
func (lb *LinearBezier) Reverse() *LinearBezier
func (lb *LinearBezier) Translate(dx, dy float64) *LinearBezier
func (lb *LinearBezier) Scale(factor float64) *LinearBezier
func (lb *LinearBezier) Rotate(angle float64) *LinearBezier
func (lb *LinearBezier) ElevateDegree() *QuadraticBezier
```

### QuadraticBezier

```go
func NewQuadraticBezier(p0, p1, p2 Point) *QuadraticBezier

// 相同方法 + ElevateDegree() -> *CubicBezier
```

### CubicBezier

```go
func NewCubicBezier(p0, p1, p2, p3 Point) *CubicBezier

// 相同方法 (无 ElevateDegree)
```

### BezierCurve (任意阶)

```go
func NewBezierCurve(points []Point) (*BezierCurve, error)

func (bc *BezierCurve) Degree() int
func (bc *BezierCurve) IsLinear(tolerance float64) bool
// 其他方法同上
```

### 缓动函数

```go
func NewEasingFunction(p1x, p1y, p2x, p2y float64) *EasingFunction
func (ef *EasingFunction) Ease(t float64) float64

// 预定义缓动函数
var EaseLinear *EasingFunction
var EaseIn *EasingFunction
var EaseOut *EasingFunction
var EaseInOut *EasingFunction
var EaseInCubic *EasingFunction
var EaseOutCubic *EasingFunction
var EaseInOutCubic *EasingFunction
var EaseInQuad *EasingFunction
var EaseOutQuad *EasingFunction
var EaseInOutQuad *EasingFunction
var EaseInSine *EasingFunction
var EaseOutSine *EasingFunction
var EaseInOutSine *EasingFunction
```

### 形状近似

```go
func ApproximateArc(center Point, radius, startAngle, endAngle float64) *QuadraticBezier
func ApproximateCircle(center Point, radius float64) []*CubicBezier
func ApproximateEllipse(center Point, rx, ry float64) []*CubicBezier
```

## 数学公式

### 线性贝塞尔曲线
```
B(t) = (1-t)P₀ + tP₁
```

### 二次贝塞尔曲线
```
B(t) = (1-t)²P₀ + 2(1-t)tP₁ + t²P₂
```

### 三次贝塞尔曲线
```
B(t) = (1-t)³P₀ + 3(1-t)²tP₁ + 3(1-t)t²P₂ + t³P₃
```

### 任意阶 (De Casteljau 算法)
递归计算，通过不断细分控制点直到只剩一个点。

## 测试

```bash
go test ./bezier_curve_utils/
```

## 应用场景

- **图形渲染**: SVG 路径、Canvas 绑定
- **动画**: 缓动函数、关键帧动画
- **游戏开发**: 移动路径、碰撞检测
- **UI 设计**: 曲线绘制、形状工具
- **字体渲染**: 字形轮廓处理
- **数据可视化**: 平滑曲线图表

## 性能说明

- 使用自适应细分算法，自动调整精度
- 边界框和交点检测使用扁平化近似，效率高
- 缓动函数使用 Newton-Raphson 方法求解，通常 4-8 次迭代即可收敛

## 许可证

MIT License