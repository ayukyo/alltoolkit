# Photography Utils - 摄影计算工具 📷

**专业的摄影曝光、景深、视角、闪光灯计算工具**

## 功能概览

- **曝光值计算** - EV 计算、等效曝光调整、曝光推荐
- **景深计算** - 景深范围、超焦距计算
- **视角计算** - 水平/垂直/对角视角、等效焦距
- **闪光灯计算** - 闪光距离、闪光指数 (GN)
- **阳光16法则** - 不同光照条件曝光估计
- **黄金时刻/蓝调时刻** - 最佳拍摄时机判断
- **镜头分类** - 根据焦距分类镜头类型
- **安全快门** - 防抖手抖模糊快门计算
- **星空摄影** - 500法则、NPF法则

## 快速开始

```python
from photography_utils.mod import (
    calculate_ev, calculate_dof, calculate_angle_of_view,
    calculate_hyperfocal, sunny_16, calculate_500_rule
)

# 计算曝光值
ev = calculate_ev(2.8, 1/125, 100)  # f/2.8, 1/125s, ISO 100

# 计算景深
dof = calculate_dof(50, 2.8, 3)  # 50mm f/2.8 对焦 3米

# 计算超焦距
h = calculate_hyperfocal(35, 8)  # 35mm f/8

# 阳光16法则
shutter, iso, ev = sunny_16("sunny", 16, 100)

# 星空摄影最大曝光
max_exp = calculate_500_rule(24)  # 24mm 镜头
```

## 详细功能

### 1. 曝光值计算

```python
# 计算曝光值 (EV)
ev = calculate_ev(aperture, shutter_speed, iso)

# 根据 EV 推荐曝光设置
settings = ev_to_settings(15, 100)  # EV 15, ISO 100

# 等效曝光调整
# 保持曝光不变，改变其中一个参数
result = adjust_exposure(2.8, 1/125, 100, aperture=4.0)  # 光圈改为 f/4
result = adjust_exposure(2.8, 1/125, 100, shutter=1/250)  # 快门改为 1/250s
result = adjust_exposure(2.8, 1/125, 100, iso=400)  # ISO 改为 400
```

### 2. 景深计算

```python
# 基础景深计算
dof = calculate_dof(50, 2.8, 3, "full_frame")
print(f"近对焦: {dof.near_focus}m")
print(f"远对焦: {dof.far_focus}m")
print(f"总景深: {dof.total_dof}m")
print(f"超焦距: {dof.hyperfocal}m")

# 超焦距计算
h = calculate_hyperfocal(35, 8, "full_frame")
# 在超焦距对焦时，景深从 h/2 延伸到无穷远

# 支持的传感器尺寸
# full_frame, aps_c, aps_c_canon, micro_four_thirds, 
# medium_format, 1_inch, smartphone
```

### 3. 视角计算

```python
# 计算视角
aov = calculate_angle_of_view(50, "full_frame")
print(f"水平视角: {aov.horizontal}°")
print(f"垂直视角: {aov.vertical}°")
print(f"对角视角: {aov.diagonal}°")

# 等效焦距转换
eq = calculate_equivalent_focal_length(35, "aps_c")  # APS-C 35mm -> 约 53mm

# 获取裁剪系数
cf = get_crop_factor("aps_c")  # 约 1.53x
```

### 4. 闪光灯计算

```python
# 计算闪光距离
dist = calculate_flash_distance(36, 4, 100)  # GN 36, f/4, ISO 100 -> 9m

# 计算所需闪光指数
gn = calculate_guide_number(10, 4, 100)  # 10m, f/4 -> GN 40

# 计算所需光圈
ap = calculate_flash_aperture(36, 9, 100)  # GN 36, 9m -> f/4
```

### 5. 阳光16法则

```python
# 不同光照条件
shutter, iso, ev = sunny_16("sunny", 16, 100)     # 晴天
shutter, iso, ev = sunny_16("overcast", 8, 100)   # 阴天
shutter, iso, ev = sunny_16("sunset", 4, 100)     # 日落

# 支持的条件: sunny, slight_overcast, overcast, heavy_overcast, sunset
```

### 6. 黄金时刻/蓝调时刻

```python
# 判断是否为黄金时刻 (太阳高度 0-6°)
is_golden, desc = is_golden_hour(3)  # True

# 判断是否为蓝调时刻 (太阳高度 -4 到 6°)
is_blue, desc = is_blue_hour(-2)  # True
```

### 7. 镜头分类

```python
# 根据焦距分类镜头
classify_lens(14)   # "鱼眼"
classify_lens(24)   # "广角"
classify_lens(50)   # "标准"
classify_lens(85)   # "人像"
classify_lens(200)  # "长焦"

# 支持指定传感器尺寸
classify_lens(35, "aps_c")  # 转换等效焦距后分类
```

### 8. 安全快门

```python
# 计算安全快门 (防止手抖模糊)
safe = calculate_safe_shutter(50)  # 约 1/50s

# 考虑防抖
safe = calculate_safe_shutter(200, "full_frame", 4)  # 4档防抖
```

### 9. 星空摄影

```python
# 500法则 - 防止星星拖尾
max_exp = calculate_500_rule(24)  # 24mm -> 约 20s

# NPF法则 - 更精确 (考虑像素间距)
max_exp = calculate_npf_rule(24, 1.4, 4.8)  # 24mm f/1.4, 4.8μm 像素
```

### 10. 格式化工具

```python
# 快门格式化
format_shutter_speed(1/125)  # "1/125"
format_shutter_speed(1.5)    # "1.5s"

# 光圈格式化
format_aperture(2.8)  # "f/2.8"

# 焦距格式化
format_focal_length(50)  # "50mm"
```

## 常数与参考值

### 传感器尺寸

| 名称 | 尺寸 (mm) | 裁剪系数 |
|------|----------|----------|
| full_frame | 36 x 24 | 1.0x |
| aps_c | 23.5 x 15.6 | 1.53x |
| aps_c_canon | 22.2 x 14.8 | 1.62x |
| micro_four_thirds | 17.3 x 13.0 | 2.0x |
| medium_format | 44 x 33 | 0.68x |
| 1_inch | 13.2 x 8.8 | 2.7x |

### 标准光圈值

1.0, 1.2, 1.4, 1.8, 2.0, 2.5, 2.8, 3.2, 3.5, 4.0, 4.5, 5.0, 5.6, 6.3, 7.1, 8.0, 9.0, 10, 11, 13, 14, 16, 18, 20, 22

### 标准快门速度

1/8000s ~ 30s

### 标准 ISO

50 ~ 102400

## 应用场景

### 人像摄影

```python
# 85mm f/1.8 人像
dof = calculate_dof(85, 1.8, 2)
# 景深约 5cm，实现浅景深效果

safe = calculate_safe_shutter(85)
# 安全快门约 1/85s
```

### 风光摄影

```python
# 24mm f/11 风光
h = calculate_hyperfocal(24, 11)
dof = calculate_dof(24, 11, h)
# 景深从 h/2 到无穷远，最大化景深
```

### 体育摄影

```python
# 200mm f/2.8 体育
safe = calculate_safe_shutter(200)
# 安全快门约 1/200s

result = adjust_exposure(2.8, 1/500, 100, shutter=1/1000)
# 快门更快时调整光圈
```

### 星空摄影

```python
# 14mm f/1.8 星空
max_exp = calculate_500_rule(14)
# 最大曝光约 35s

settings = exposure_recommendation(-5, "aperture", 1.8, 3200)
# EV -5 推荐: 高 ISO、大光圈、长曝光
```

## API 参考

### 曝光计算

| 函数 | 参数 | 返回值 |
|------|------|--------|
| `calculate_ev` | aperture, shutter, iso | EV 值 |
| `ev_to_settings` | ev, iso | ExposureSettings 列表 |
| `adjust_exposure` | base settings, target | ExposureSettings |
| `exposure_recommendation` | ev, priority, value | ExposureSettings |

### 景深计算

| 函数 | 参数 | 返回值 |
|------|------|--------|
| `calculate_dof` | focal, aperture, distance, sensor | DepthOfField |
| `calculate_hyperfocal` | focal, aperture, sensor | 超焦距 (米) |

### 视角计算

| 函数 | 参数 | 返回值 |
|------|------|--------|
| `calculate_angle_of_view` | focal, sensor | AngleOfView |
| `calculate_equivalent_focal_length` | focal, source, target | 等效焦距 |
| `get_crop_factor` | sensor | 裁剪系数 |

### 闪光灯计算

| 函数 | 参数 | 返回值 |
|------|------|--------|
| `calculate_flash_distance` | gn, aperture, iso | 距离 (米) |
| `calculate_guide_number` | distance, aperture, iso | GN |
| `calculate_flash_aperture` | gn, distance, iso | 光圈 |

## 测试

```bash
python photography_utils_test.py
```

测试覆盖:
- 曝光值计算 (ISO 修正、等效曝光)
- 景深计算 (光圈影响、传感器影响、超焦距)
- 视角计算 (不同焦距、等效焦距)
- 闪光灯计算 (距离、GN、ISO)
- 阳光16法则
- 黄金时刻/蓝调时刻判断
- 镜头分类
- 安全快门 (防抖影响)
- 星空摄影 (500/NPF 法则)
- 边界情况处理

## 许可证

MIT License

---

**最后更新**: 2026-05-18
**作者**: AllToolkit 自动生成