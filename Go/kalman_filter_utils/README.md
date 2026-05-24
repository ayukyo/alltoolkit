# Kalman Filter Utilities

卡尔曼滤波器工具集，提供信号处理、传感器融合、导航系统等领域的最优估计算法。

## 功能特性

- **1D Kalman Filter** - 一维卡尔曼滤波器，适用于单变量追踪
- **N-D Kalman Filter** - 多维卡尔曼滤波器，适用于位置、速度等多状态追踪
- **Extended Kalman Filter (EKF)** - 扩展卡尔曼滤波器，适用于非线性系统
- **Unscented Kalman Filter (UKF)** - 无迹卡尔曼滤波器，更强的非线性处理能力
- **Moving Average Filter** - 移动平均滤波器，简单实用的平滑方法
- **Exponential Smoothing Filter** - 指数平滑滤波器，加权平均方法
- 零外部依赖（纯 Go 实现）
- 线程安全操作
- 泛型支持（Go 1.18+）

## 常见应用场景

- 传感器数据滤波与平滑
- GPS/IMU 传感器融合
- 金融时间序列分析
- 计算机视觉中的目标追踪
- 导航系统
- 信号处理
- IoT 数据过滤

## 快速开始

### 一维卡尔曼滤波器

```go
package main

import (
    "fmt"
    "github.com/yourpackage/kalman_filter_utils"
)

func main() {
    // 创建温度追踪卡尔曼滤波器
    // 初始温度: 25°C, 初始不确定度: 1
    // 过程噪声: 0.1 (温度缓慢变化)
    // 测量噪声: 0.5 (传感器有中度噪声)
    kf := kalman_filter_utils.NewKalmanFilter1D(25.0, 1.0, 0.1, 0.5)

    // 模拟带噪声的温度读数
    measurements := []float64{24.5, 25.2, 24.8, 25.1, 24.9}

    for _, m := range measurements {
        estimate := kf.Update(m)
        fmt.Printf("测量值: %.1f°C, 估计值: %.2f°C\n", m, estimate)
    }
}
```

### 多维卡尔曼滤波器

```go
package main

import (
    "fmt"
    kalman_filter_utils "github.com/yourpackage/kalman_filter_utils"
)

func main() {
    // 二维位置追踪
    initialState := []float64{0.0, 0.0} // 起点
    kf := kalman_filter_utils.NewKalmanFilterND(initialState, 1.0, 0.1, 0.5)

    // 位置测量
    measurements := [][]float64{
        {1.0, 0.5},
        {1.5, 1.0},
        {2.0, 1.5},
        {2.5, 2.0},
    }

    for _, m := range measurements {
        state := kf.Update(m)
        fmt.Printf("位置: [%.2f, %.2f]\n", state[0], state[1])
    }
}
```

### 扩展卡尔曼滤波器 (EKF)

```go
package main

import (
    kalman_filter_utils "github.com/yourpackage/kalman_filter_utils"
)

func main() {
    // 定义非线性状态转移函数
    stateFunc := func(state []float64) []float64 {
        // 例如: x = x + v*dt
        return []float64{state[0] + state[1], state[1]}
    }

    // 定义测量函数
    measureFunc := func(state []float64) []float64 {
        return []float64{state[0]} // 只测量位置
    }

    // 定义雅可比矩阵
    jacobianF := func(state []float64) [][]float64 {
        return [][]float64{
            {1.0, 1.0},
            {0.0, 1.0},
        }
    }

    jacobianH := func(state []float64) [][]float64 {
        return [][]float64{
            {1.0, 0.0},
        }
    }

    initialState := []float64{0.0, 1.0} // 位置=0, 速度=1
    ekf := kalman_filter_utils.NewExtendedKalmanFilter(
        initialState, 1.0, 0.1, 0.5,
        stateFunc, measureFunc, jacobianF, jacobianH,
    )

    // 更新滤波器
    measurement := []float64{1.0}
    state := ekf.Update(measurement)
}
```

### 移动平均滤波器

```go
package main

import (
    "fmt"
    kalman_filter_utils "github.com/yourpackage/kalman_filter_utils"
)

func main() {
    // 3 点移动平均
    maf := kalman_filter_utils.NewMovingAverageFilter(3)

    for _, v := range []float64{10.0, 20.0, 15.0, 25.0, 20.0} {
        smoothed := maf.Update(v)
        fmt.Printf("%.1f -> %.2f\n", v, smoothed)
    }
    // 输出:
    // 10.0 -> 10.00
    // 20.0 -> 15.00
    // 15.0 -> 15.00
    // 25.0 -> 20.00
    // 20.0 -> 20.00
}
```

### 指数平滑滤波器

```go
package main

import (
    "fmt"
    kalman_filter_utils "github.com/yourpackage/kalman_filter_utils"
)

func main() {
    // alpha = 0.3 (较平滑)
    esf := kalman_filter_utils.NewExponentialSmoothingFilter(0.3)

    for _, v := range []float64{100.0, 120.0, 110.0, 130.0} {
        smoothed := esf.Update(v)
        fmt.Printf("%.1f -> %.2f\n", v, smoothed)
    }
    // 输出:
    // 100.0 -> 100.00
    // 120.0 -> 106.00
    // 110.0 -> 107.20
    // 130.0 -> 112.04
}
```

## API 参考

### KalmanFilter1D

| 方法 | 描述 |
|------|------|
| `NewKalmanFilter1D(initialState, initialCovariance, processNoise, measurementNoise)` | 创建一维卡尔曼滤波器 |
| `Update(measurement)` | 用新测量值更新滤波器 |
| `Predict()` | 仅预测（无测量时） |
| `GetState()` | 获取当前状态估计 |
| `GetCovariance()` | 获取当前误差协方差 |
| `SetProcessNoise(q)` | 设置过程噪声 (Q) |
| `SetMeasurementNoise(r)` | 设置测量噪声 (R) |
| `Reset()` | 重置到初始状态 |
| `BatchUpdate(measurements)` | 批量处理测量值 |

### KalmanFilterND

| 方法 | 描述 |
|------|------|
| `NewKalmanFilterND(initialState, initialCovariance, processNoise, measurementNoise)` | 创建多维卡尔曼滤波器 |
| `Update(measurement)` | 用测量向量更新 |
| `Predict()` | 仅预测 |
| `GetState()` | 获取状态向量 |
| `SetStateTransition(f)` | 设置状态转移矩阵 |
| `SetObservation(h)` | 设置观测矩阵 |

### ExtendedKalmanFilter

| 方法 | 描述 |
|------|------|
| `NewExtendedKalmanFilter(initialState, initialCovariance, processNoise, measurementNoise, stateFunc, measureFunc, jacobianF, jacobianH)` | 创建 EKF |
| `Update(measurement)` | 更新滤波器 |
| `GetState()` | 获取状态 |

### UnscentedKalmanFilter

| 方法 | 描述 |
|------|------|
| `NewUnscentedKalmanFilter(initialState, initialCovariance, processNoise, measurementNoise, stateFunc, measureFunc, config)` | 创建 UKF |
| `Update(measurement)` | 更新滤波器 |
| `GetState()` | 获取状态 |

### 辅助滤波器

| 类型 | 描述 |
|------|------|
| `MovingAverageFilter` | 移动平均滤波器 |
| `ExponentialSmoothingFilter` | 指数平滑滤波器 |
| `SmoothKalman()` | 批量平滑函数 |

## 参数选择指南

### 过程噪声 (Q)
- **低值 (0.01)**：输出平滑，响应缓慢，适用于稳定系统
- **高值 (1.0)**：响应快，跟随测量变化，适用于快速变化系统

### 测量噪声 (R)
- **低值**：信任测量值，适用于高精度传感器
- **高值**：信任模型预测，适用于低精度传感器

### 平滑因子 (alpha)
- **低值 (0.1)**：平滑输出，适用于长期趋势分析
- **高值 (0.9)**：快速响应，适用于短期变化检测

## 数学原理

卡尔曼滤波器是最优线性估计器，通过以下步骤工作：

1. **预测步骤**：
   - 状态预测：`x = F * x`
   - 协方差预测：`P = F * P * F' + Q`

2. **更新步骤**：
   - 卡尔曼增益：`K = P * H' * (H * P * H' + R)^(-1)`
   - 状态更新：`x = x + K * (z - H * x)`
   - 协方差更新：`P = (I - K * H) * P`

其中：
- `x` = 状态向量
- `P` = 误差协方差矩阵
- `F` = 状态转移矩阵
- `H` = 观测矩阵
- `Q` = 过程噪声协方差
- `R` = 测量噪声协方差
- `K` = 卡尔曼增益
- `z` = 测量值

## 测试

```bash
cd kalman_filter_utils
go test -v
```

## 性能

- 一维滤波器：10000 次更新约 1ms
- 多维滤波器：取决于状态维度
- 线程安全：支持并发更新

## 许可证

MIT License

## 作者

AllToolkit Contributors