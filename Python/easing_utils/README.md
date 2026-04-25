# Easing Utilities - 动画缓动函数工具集

零外部依赖的缓动函数库，纯 Python 标准库实现。

## 功能概述

提供完整的缓动函数实现，用于创建平滑自然的动画过渡效果。

### 支持的缓动类型

| 类型 | 说明 | 特点 |
|------|------|------|
| `linear` | 线性匀速 | 无加速度变化 |
| `quad` | 二次方 | 平滑，适合一般过渡 |
| `cubic` | 三次方 | 更柔和的开始/结束 |
| `quart` | 四次方 | 明显的缓入/缓出效果 |
| `quint` | 五次方 | 极其柔和的过渡 |
| `sine` | 正弦 | 波浪式平滑过渡 |
| `expo` | 指数 | 极端的缓入/缓出 |
| `circ` | 圆形 | 圆弧式变化 |
| `elastic` | 弹性 | 弹簧式振荡效果 |
| `back` | 回弹 | 超出后回弹 |
| `bounce` | 弹跳 | 球落地弹跳效果 |

### 缓动模式

每种类型支持四种模式：
- `in`: 开始慢，结束快
- `out`: 开始快，结束慢
- `in_out`: 开始和结束慢，中间快
- `out_in`: 开始和结束快，中间慢

## 快速开始

### 基本使用

```python
from easing_utils.mod import ease

# 使用 ease() 统一接口
value = ease(0.5, 'quad', 'out')  # 结果: 0.75

# 使用字符串或枚举
value = ease(0.5, EasingType.CUBIC, EasingMode.IN_OUT)
```

### 值插值

```python
from easing_utils.mod import interpolate

# 在两个值之间插值
result = interpolate(0, 100, 0.5, 'quad', 'out')  # 75.0

# 线性插值
result = interpolate(0, 100, 0.5)  # 50.0
```

### 生成动画帧

```python
from easing_utils.mod import generate_animation_frames

# 生成从 0 到 100 的 10 帧动画
frames = generate_animation_frames(0, 100, 10, 'quad', 'out')
# [0.0, 36.0, 64.0, 84.0, 96.0, 99.0, ...]
```

### CSS 兼容

```python
from easing_utils.mod import get_css_easing, cubic_bezier

# 使用 CSS 标准缓动
ease_fn = get_css_easing('ease-in-out')
value = ease_fn(0.5)

# 自定义贝塞尔曲线
custom_ease = cubic_bezier(0.25, 0.1, 0.25, 1.0)
value = custom_ease(0.5)
```

## API 参考

### 核心函数

#### `ease(t, easing_type, mode)`
应用缓动函数计算值。

```python
ease(0.5, 'cubic', 'out')  # 0.875
```

#### `get_easing_function(easing_type, mode)`
获取缓动函数引用。

```python
fn = get_easing_function('quad', 'out')
fn(0.5)  # 0.75
```

### 插值函数

#### `interpolate(start, end, t, easing_type, mode)`
在两个值之间进行缓动插值。

#### `interpolate_2d(start, end, t, easing_type, mode)`
二维点插值。

#### `interpolate_3d(start, end, t, easing_type, mode)`
三维点插值。

#### `interpolate_list(values, t, easing_type, mode)`
多点插值（路径动画）。

### 动画序列

#### `generate_animation_frames(start, end, frames, easing_type, mode)`
生成动画帧序列。

#### `generate_animation_frames_2d(start, end, frames, easing_type, mode)`
生成二维动画帧序列。

### 组合缓动

#### `chain_easing(t, easing_configs)`
链式组合多种缓动效果。

```python
chain_easing(0.75, [
    (0.5, 'quad', 'out'),
    (0.5, 'bounce', 'out')
])
```

#### `blend_easing(t, easing_type1, easing_type2, blend_factor)`
混合两种缓动效果。

### 分析工具

#### `compare_easings(t, modes)`
比较所有缓动类型在给定进度下的值。

#### `create_easing_curve(easing_type, mode, samples)`
创建缓动曲线数据点。

#### `get_easing_extremes(easing_type, mode)`
获取缓动函数的极值。

### CSS 兼容

#### `get_css_easing(name)`
获取 CSS 标准缓动函数（linear, ease, ease-in, ease-out, ease-in-out）。

#### `cubic_bezier(x1, y1, x2, y2)`
创建自定义三次贝塞尔缓动函数。

## 使用场景

### UI 动画

- 模态框淡入缩放
- 滑动切换动画
- 进度条平滑增长
- 按钮点击反馈

### 游戏开发

- 角色平滑移动
- 弹跳效果
- 弹性跳跃动画

### 数据可视化

- 图表动画过渡
- 数值平滑变化

### 网页动画

- CSS 动画替代
- 自定义缓动曲线

## 特性

- ✅ 零外部依赖
- ✅ 11 种缓动类型
- ✅ 4 种缓动模式
- ✅ CSS cubic-bezier 兼容
- ✅ 2D/3D 点插值支持
- ✅ 动画帧序列生成
- ✅ 链式和混合缓动
- ✅ 完整的测试覆盖

## 文件结构

```
easing_utils/
├── mod.py              # 主模块
├── easing_utils_test.py # 测试文件
├── README.md           # 说明文档
└── examples/
    └── usage_examples.py # 使用示例
```

## 运行测试

```bash
python easing_utils_test.py
```

## 运行示例

```bash
python examples/usage_examples.py
```

## 版本历史

- 2026-04-25: 初始版本，完整缓动函数库

---

作者: AllToolkit  
日期: 2026-04-25  
许可证: MIT