# Ambient Noise Generator Utilities

环境噪音生成器 - 生成各种类型的噪音和环境声音，用于专注、睡眠、放松等场景。

## 功能特点

### 噪音类型
- **白噪音** - 所有频率能量相等，类似静电声
- **粉噪音** - 每倍频程能量减半，类似雨声，最适合睡眠
- **棕色噪音** - 每倍频程能量减少6dB，类似瀑布声
- **蓝噪音** - 每倍频程能量增加3dB，声音更尖锐
- **紫噪音** - 每倍频程能量增加6dB，非常尖锐
- **灰噪音** - 心理声学补偿，听起来更均匀

### 环境声音
- 小雨 / 大雨 / 雷雨
- 海浪（平静/中等/汹涌）
- 风声（轻/中等/强）
- 森林 / 夜晚环境
- 壁炉 / 瀑布 / 溪流
- 咖啡馆 / 飞机客舱

### 其他功能
- 噪音混合和叠加
- 淡入淡出效果
- 音量调整
- WAV 文件导出
- 文件大小估算

## 使用示例

### 基础噪音生成

```python
from ambient_noise_utils import generate_noise, save_wav_file, apply_fade

# 生成 30 秒粉噪音
samples = generate_noise('pink', 30 * 44100, amplitude=0.5, seed=42)

# 应用淡入淡出
samples = apply_fade(samples, fade_in_seconds=2.0, fade_out_seconds=3.0)

# 保存为 WAV 文件
save_wav_file(samples, 'pink_noise.wav')
```

### 环境音生成

```python
from ambient_noise_utils import generate_ambient_sound, generate_rain_sound

# 生成 10 分钟雨声
rain = generate_rain_sound(600, intensity='medium')

# 生成海浪声
ocean = generate_ambient_sound('ocean_waves', 300)  # 5分钟
```

### 使用生成器类

```python
from ambient_noise_utils import AmbientNoiseGenerator

# 创建「雨夜壁炉」场景
generator = (
    AmbientNoiseGenerator()
    .add_ambient('heavy_rain', 60.0, 0.5)      # 1小时大雨
    .add_ambient('fireplace', 60.0, 0.35)      # 壁炉声
    .normalize()
    .apply_fade(3.0, 5.0)
)

# 保存为 WAV
generator.save_wav('rainy_night.wav')

# 查看信息
print(generator.info())
```

### 噪音混合

```python
from ambient_noise_utils import mix_noises, layer_ambient_sounds

# 混合粉噪音和棕色噪音
mixed = mix_noises([('pink', 0.4), ('brown', 0.3)], 30.0)

# 叠加多层环境音
scene = layer_ambient_sounds([
    ('light_rain', 0.5),
    ('wind', 0.3),
    ('night_ambience', 0.2)
], 60.0)
```

## API 参考

### 噪音生成函数

- `generate_white_noise(num_samples, amplitude, seed)` - 生成白噪音
- `generate_pink_noise(num_samples, amplitude, seed)` - 生成粉噪音
- `generate_brown_noise(num_samples, amplitude, seed)` - 生成棕色噪音
- `generate_blue_noise(num_samples, amplitude, seed)` - 生成蓝噪音
- `generate_violet_noise(num_samples, amplitude, seed)` - 生成紫噪音
- `generate_grey_noise(num_samples, amplitude, seed)` - 生成灰噪音
- `generate_noise(noise_type, num_samples, amplitude, seed)` - 通用噪音生成

### 环境音生成函数

- `generate_ambient_sound(ambient_type, duration_seconds, ...)` - 生成环境音
- `generate_rain_sound(duration, intensity)` - 生成雨声
- `generate_ocean_sound(duration, wave_intensity)` - 生成海浪声
- `generate_wind_sound(duration, strength)` - 生成风声
- `generate_fire_sound(duration, crackling)` - 生成火焰声

### 效果函数

- `apply_fade(samples, fade_in_seconds, fade_out_seconds)` - 应用淡入淡出
- `apply_volume(samples, volume)` - 调整音量
- `mix_noises(configs, duration)` - 混合噪音
- `layer_ambient_sounds(layers, duration)` - 叠加环境音

### WAV 文件函数

- `samples_to_wav_bytes(samples)` - 转换为 WAV 字节数据
- `save_wav_file(samples, filepath)` - 保存为 WAV 文件
- `load_wav_file(filepath)` - 加载 WAV 文件

### 工具函数

- `list_noise_types()` - 列出所有噪音类型
- `list_ambient_types()` - 列出所有环境音类型
- `get_noise_info(noise_type)` - 获取噪音信息
- `get_ambient_info(ambient_type)` - 获取环境音信息
- `estimate_file_size(duration)` - 估算文件大小
- `format_duration(seconds)` - 格式化时长
- `format_file_size(bytes)` - 格式化文件大小

### AmbientNoiseGenerator 类

```python
class AmbientNoiseGenerator:
    def add_noise(noise_type, duration, amplitude) -> self
    def add_ambient(ambient_type, duration, amplitude) -> self
    def apply_fade(fade_in, fade_out) -> self
    def normalize() -> self
    def set_volume(volume) -> self
    def set_seed(seed) -> self
    def get_samples() -> List[float]
    def to_wav_bytes() -> bytes
    def save_wav(filepath) -> int
    def clear() -> self
    def info() -> dict
```

## 运行测试

```bash
python test_ambient_noise_utils.py
```

## 运行示例

```bash
python examples.py
```

## 应用场景

1. **专注工作** - 粉噪音或咖啡馆环境音
2. **睡眠辅助** - 棕色噪音、雨声或海浪声
3. **冥想放松** - 森林、溪流或夜晚环境音
4. **掩蔽噪音** - 白噪音或大雨声
5. **ASMR创作** - 各种环境音叠加

## 零外部依赖

本模块仅使用 Python 标准库：
- `struct` - WAV 文件格式处理
- `math` - 数学计算
- `random` - 随机数生成
- `datetime` - 时间处理

## 文件格式

默认生成标准 WAV 格式：
- 采样率：44100 Hz
- 位深度：16-bit PCM
- 声道：单声道
- 可自定义 8/16/24/32-bit，单声道/立体声

---

**Author**: AllToolkit Contributors  
**License**: MIT  
**Date**: 2026-05-20