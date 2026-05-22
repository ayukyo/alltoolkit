# Ambient Noise Utils - 环境噪音生成工具

零依赖的环境噪音生成模块，支持多种噪音类型和自然环境音效，可生成 WAV 格式音频文件。

## 功能特性

- ✅ **多种噪音类型** - 白噪音、粉噪音、棕色噪音、蓝噪音、紫噪音、灰噪音
- ✅ **自然环境音** - 雨声、海浪、风声、壁炉、森林等 12+ 种预设
- ✅ **噪音混合** - 支持多层叠加和混合
- ✅ **音频处理** - 淡入淡出、音量调整、归一化
- ✅ **WAV 导出** - 支持 8/16/24/32 位深度
- ✅ **零外部依赖** - 仅使用 Python 标准库

## 安装

```python
# 直接复制 mod.py 到项目中使用
from ambient_noise_utils import generate_pink_noise, generate_ambient_sound
```

## 快速开始

### 生成基础噪音

```python
from mod import generate_noise, DEFAULT_SAMPLE_RATE

# 生成 10 秒粉噪音（适合睡眠/专注）
samples = generate_noise('pink', 10 * DEFAULT_SAMPLE_RATE, amplitude=0.5)

# 噪音类型
# 'white'  - 白噪音（所有频率能量相等）
# 'pink'   - 粉噪音（-3dB/octave，类似雨声）
# 'brown'  - 棕色噪音（-6dB/octave，类似瀑布）
# 'blue'   - 蓝噪音（+3dB/octave，更尖锐）
# 'violet' - 紫噪音（+6dB/octave，非常尖锐）
# 'grey'   - 灰噪音（心理声学补偿）
```

### 生成环境音效

```python
from mod import generate_ambient_sound

# 生成 30 秒小雨声
rain = generate_ambient_sound('light_rain', 30.0)

# 环境音预设
# 'light_rain'     - 小雨（适合专注）
# 'heavy_rain'     - 大雨（适合掩蔽）
# 'ocean_waves'    - 海浪
# 'wind'           - 风声
# 'fireplace'      - 壁炉（带噼啪声）
# 'forest'         - 森林
# 'stream'         - 溪流
# 'night_ambience' - 夜晚
# 'cafe'           - 咖啡馆
```

### 便捷生成函数

```python
from mod import generate_rain_sound, generate_ocean_sound, generate_wind_sound

# 雨声（支持强度调节）
light_rain = generate_rain_sound(30.0, intensity='light')
heavy_rain = generate_rain_sound(30.0, intensity='heavy')

# 海浪声（支持浪强度）
calm_ocean = generate_ocean_sound(60.0, wave_intensity='calm')
rough_ocean = generate_ocean_sound(60.0, wave_intensity='rough')

# 风声
light_wind = generate_wind_sound(15.0, strength='light')
strong_wind = generate_wind_sound(15.0, strength='strong')
```

### 混合噪音

```python
from mod import mix_noises, layer_ambient_sounds

# 混合粉噪音和棕色噪音
mixed = mix_noises([('pink', 0.4), ('brown', 0.3)], duration_seconds=30.0)

# 叠加环境音（雨声 + 声炉）
combo = layer_ambient_sounds([('light_rain', 0.5), ('fireplace', 0.3)], 30.0)
```

### 音频处理

```python
from mod import apply_fade, apply_volume

# 应用淡入淡出（避免突然开始/结束）
faded = apply_fade(samples, fade_in_seconds=1.0, fade_out_seconds=2.0)

# 调整音量
quieter = apply_volume(samples, 0.5)  # 50% 音量
louder = apply_volume(samples, 1.5)   # 150% 音量
```

### 导出到 WAV 文件

```python
from mod import save_wav_file, samples_to_wav_bytes

# 保存为 WAV 文件（默认 16-bit, 44100Hz）
save_wav_file(samples, 'output.wav')

# 获取 WAV 字节数据（可用于流式传输）
wav_bytes = samples_to_wav_bytes(samples)

# 支持不同位深度
save_wav_file(samples, 'output_24bit.wav', bits_per_sample=24)
```

### 使用生成器类

```python
from mod import AmbientNoiseGenerator

# 创建生成器
generator = AmbientNoiseGenerator()

# 链式调用添加噪音和处理
generator.set_seed(42)                        # 设置随机种子（可重复）
generator.add_ambient('light_rain', 30.0, 0.5) # 添加雨声
generator.add_ambient('fireplace', 30.0, 0.3)  # 添加壁炉声
generator.normalize()                         # 归一化音量
generator.apply_fade(1.0, 2.0)               # 淡入淡出

# 导出
generator.save_wav('ambient_mix.wav')

# 查看信息
info = generator.info()
print(f"时长: {info['duration']}秒")
print(f"文件大小: {info['file_size']}字节")
```

## 噪音类型说明

| 类型 | 频率特性 | 听感 | 适用场景 |
|------|----------|------|----------|
| white | 平坦 | 静电声 | 掩蔽、测试 |
| pink | -3dB/oct | 自然雨声 | 睡眠、专注 |
| brown | -6dB/oct | 低沉瀑布 | 深度睡眠 |
| blue | +3dB/oct | 较尖锐 | 特殊效果 |
| violet | +6dB/oct | 高频为主 | 特殊效果 |
| grey | 心理声学补偿 | 听感均匀 | 专业音频 |

## 环境音预设

| 预设 | 中文名 | 描述 | 基础噪音 |
|------|--------|------|----------|
| light_rain | 小雨 | 轻柔雨滴 | pink |
| heavy_rain | 大雨 | 密集雨声 | brown |
| ocean_waves | 海浪 | 拍岸声 | brown |
| wind | 风声 | 风吹树叶 | brown |
| fireplace | 声炉 | 柴火燃烧 | brown |
| forest | 森林 | 鸟鸣+风 | pink |
| stream | 溪流 | 流水声 | pink |
| waterfall | 瀑布 | 水流冲击 | brown |
| night_ambience | 夜晚 | 宁静环境 | brown |
| cafe | 咖啡馆 | 人声嗡嗡 | pink |
| airplane | 飞机客舱 | 低频嗡嗡 | brown |

## API 参考

### 噪音生成函数

```python
generate_white_noise(num_samples, amplitude=1.0, seed=None)
generate_pink_noise(num_samples, amplitude=1.0, seed=None)
generate_brown_noise(num_samples, amplitude=1.0, seed=None)
generate_blue_noise(num_samples, amplitude=1.0, seed=None)
generate_violet_noise(num_samples, amplitude=1.0, seed=None)
generate_grey_noise(num_samples, amplitude=1.0, seed=None)
generate_noise(noise_type, num_samples, amplitude=1.0, seed=None)
```

### 环境音生成函数

```python
generate_ambient_sound(ambient_type, duration_seconds, sample_rate=44100, 
                       amplitude_override=None, seed=None)
generate_rain_sound(duration_seconds, intensity='medium', seed=None)
generate_ocean_sound(duration_seconds, wave_intensity='medium', seed=None)
generate_wind_sound(duration_seconds, strength='moderate', seed=None)
generate_fire_sound(duration_seconds, crackling=True, seed=None)
```

### 混合与处理函数

```python
mix_noises(noise_configs, duration_seconds, sample_rate=44100, seed=None)
layer_ambient_sounds(layers, duration_seconds, sample_rate=44100, seed=None)
apply_fade(samples, fade_in_seconds=0.0, fade_out_seconds=0.0, sample_rate=44100)
apply_volume(samples, volume)
```

### WAV 文件函数

```python
samples_to_wav_bytes(samples, sample_rate=44100, bits_per_sample=16, num_channels=1)
save_wav_file(samples, filepath, sample_rate=44100, bits_per_sample=16, num_channels=1)
load_wav_file(filepath)  # 返回 (samples, sample_rate, bits, channels)
```

### 工具函数

```python
get_noise_info(noise_type)        # 获取噪音类型信息
get_ambient_info(ambient_type)    # 获取环境音信息
list_noise_types()                # 列出所有噪音类型
list_ambient_types()              # 列出所有环境音预设
calculate_duration(num_samples)   # 计算时长（秒）
calculate_num_samples(duration)   # 计算样本数
estimate_file_size(duration)      # 估算 WAV 文件大小
format_duration(seconds)          # 格式化时长显示
format_file_size(bytes)           # 格式化文件大小显示
```

## 默认参数

- **采样率**: 44100 Hz
- **位深度**: 16-bit
- **声道数**: 1 (单声道)

## 测试

```bash
python ambient_noise_utils_test.py
```

**测试覆盖：**
- 90 个测试用例
- 100% 通过率 ✅

## 许可证

MIT License

---

**最后更新**: 2026-05-23