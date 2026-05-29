"""
Perlin Noise Utils - 使用示例

展示 Perlin 噪声的各种应用场景：
1. 基础噪声生成
2. 地形生成
3. 纹理生成
4. 程序化动画
5. 数据可视化
"""

import sys
import os
import math

# 添加模块路径 - 支持从多个位置运行
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
workspace_dir = os.path.dirname(parent_dir)

# 尝试不同的路径
for path in [parent_dir, workspace_dir]:
    if path not in sys.path:
        sys.path.insert(0, path)

# 尝试导入
try:
    from perlin_noise_utils.mod import (
        PerlinNoise,
        perlin_noise,
        generate_terrain,
        render_terrain_ascii
    )
except ImportError:
    from Python.perlin_noise_utils.mod import (
        PerlinNoise,
        perlin_noise,
        generate_terrain,
        render_terrain_ascii
    )


def example_basic_noise():
    """示例 1: 基础噪声生成"""
    print("=" * 60)
    print("示例 1: 基础噪声生成")
    print("=" * 60)
    
    noise = PerlinNoise(seed=42)
    
    # 1D 噪声
    print("\n1D Perlin Noise (波形图):")
    for i in range(30):
        x = i * 0.2
        val = noise.noise1d(x)
        # 转换为正数用于显示
        bar_len = int((val + 1) * 15)
        bar = '█' * bar_len
        print(f"  x={x:4.1f}: {bar}")
    
    # 2D 噪声
    print("\n2D Perlin Noise (灰度图):")
    for y in range(15):
        row = ""
        for x in range(40):
            val = noise.noise2d(x * 0.1, y * 0.1)
            # 映射到 ASCII 字符
            char_idx = int((val + 1) * 5)
            chars = " .:-=+*#%@"
            row += chars[min(char_idx, len(chars) - 1)]
        print(f"  {row}")
    
    # 3D 噪声
    print("\n3D Perlin Noise (切片):")
    z = 0
    for y in range(10):
        row = ""
        for x in range(30):
            val = noise.noise3d(x * 0.15, y * 0.15, z)
            chars = " .:-=+*#%@"
            char_idx = int((val + 1) * 5)
            row += chars[min(char_idx, len(chars) - 1)]
        print(f"  {row}")


def example_terrain_generation():
    """示例 2: 地形生成"""
    print("\n" + "=" * 60)
    print("示例 2: 地形生成")
    print("=" * 60)
    
    # 使用不同参数生成地形
    configs = [
        {"name": "岛屿", "seed": 42, "scale": 40, "octaves": 6, "persistence": 0.5, "sea_level": 0.45},
        {"name": "大陆", "seed": 123, "scale": 80, "octaves": 4, "persistence": 0.6, "sea_level": 0.35},
        {"name": "山脉", "seed": 456, "scale": 30, "octaves": 8, "persistence": 0.7, "sea_level": 0.3},
    ]
    
    for config in configs:
        print(f"\n{config['name']}地形 (seed={config['seed']}, scale={config['scale']}):")
        noise = PerlinNoise(
            seed=config['seed'],
            octaves=config['octaves'],
            persistence=config['persistence']
        )
        terrain = noise.generate_terrain_map(
            50, 20,
            scale=config['scale'],
            sea_level=config['sea_level']
        )
        print(render_terrain_ascii(terrain))


def example_heightmap_analysis():
    """示例 3: 高度图分析"""
    print("\n" + "=" * 60)
    print("示例 3: 高度图分析")
    print("=" * 60)
    
    noise = PerlinNoise(seed=42, octaves=6, persistence=0.5)
    heightmap = noise.generate_heightmap_normalized(100, 100, scale=50)
    
    # 统计分析
    flat = [v for row in heightmap for v in row]
    min_h = min(flat)
    max_h = max(flat)
    avg_h = sum(flat) / len(flat)
    
    # 计算标准差
    variance = sum((v - avg_h) ** 2 for v in flat) / len(flat)
    std_dev = math.sqrt(variance)
    
    print(f"\n高度图统计 (100x100):")
    print(f"  最小值: {min_h:.4f}")
    print(f"  最大值: {max_h:.4f}")
    print(f"  平均值: {avg_h:.4f}")
    print(f"  标准差: {std_dev:.4f}")
    
    # 高度分布
    buckets = [0] * 10
    for v in flat:
        idx = min(int(v * 10), 9)
        buckets[idx] += 1
    
    print("\n高度分布:")
    for i, count in enumerate(buckets):
        pct = count / len(flat) * 100
        bar = '█' * int(pct / 2)
        print(f"  {i*10:3d}-{(i+1)*10:3d}%: {bar} ({pct:.1f}%)")


def example_fractal_effects():
    """示例 4: 分形效果对比"""
    print("\n" + "=" * 60)
    print("示例 4: 分形效果对比")
    print("=" * 60)
    
    noise = PerlinNoise(seed=42)
    
    effects = [
        ("基础 Perlin", lambda x, y: noise.noise2d(x, y)),
        ("fBm (低倍频)", lambda x, y: noise.fractal_brownian_motion_2d(x, y, octaves=2)),
        ("fBm (高倍频)", lambda x, y: noise.fractal_brownian_motion_2d(x, y, octaves=8)),
        ("湍流", lambda x, y: noise.turbulence_2d(x, y)),
        ("脊状", lambda x, y: noise.ridged_multifractal_2d(x, y)),
    ]
    
    for name, func in effects:
        print(f"\n{name}:")
        for y in range(12):
            row = ""
            for x in range(35):
                val = func(x * 0.2, y * 0.2)
                # 归一化到 0-1
                if name == "湍流":
                    norm_val = min(val / 2, 1)  # 湍流非负
                else:
                    norm_val = (val + 1) / 2
                char_idx = int(norm_val * 9)
                chars = " .:-=+*#%@"
                row += chars[min(char_idx, 9)]
            print(f"  {row}")


def example_animation_path():
    """示例 5: 程序化动画路径"""
    print("\n" + "=" * 60)
    print("示例 5: 程序化动画路径")
    print("=" * 60)
    
    noise = PerlinNoise(seed=42)
    
    # 模拟一个粒子在噪声场中的运动
    print("\n粒子运动轨迹 (30帧):")
    
    # 起始位置
    x, y = 50.0, 50.0
    path = [(int(x), int(y))]
    
    for frame in range(30):
        # 使用噪声计算运动方向
        angle = noise.noise2d(x * 0.1, y * 0.1) * math.pi * 2
        speed = 3.0
        
        x += math.cos(angle) * speed
        y += math.sin(angle) * speed
        
        # 边界反弹
        x = max(0, min(100, x))
        y = max(0, min(100, y))
        
        path.append((int(x), int(y)))
    
    # 绘制轨迹
    grid = [[' ' for _ in range(60)] for _ in range(30)]
    for i, (px, py) in enumerate(path):
        gx = int(px * 0.6)
        gy = int(py * 0.3)
        if 0 <= gx < 60 and 0 <= gy < 30:
            if i == 0:
                grid[gy][gx] = 'S'  # 起点
            elif i == len(path) - 1:
                grid[gy][gx] = 'E'  # 终点
            else:
                grid[gy][gx] = '.'
    
    for row in grid:
        print(f"  |{''.join(row)}|")
    
    print("\n  S = 起点, E = 终点")


def example_seamless_texture():
    """示例 6: 无缝纹理生成"""
    print("\n" + "=" * 60)
    print("示例 6: 无缝纹理生成")
    print("=" * 60)
    
    noise = PerlinNoise(seed=42)
    
    print("\n无缝平铺噪声 (可重复的纹理):")
    
    # 生成可平铺的噪声
    size = 30
    tile_size = 1.0
    
    texture = []
    for y in range(size):
        row = ""
        for x in range(size):
            # 使用平铺噪声
            val = noise.tileable_noise_2d(x / size, y / size, tile_size, tile_size)
            norm_val = (val + 1) / 2
            chars = " ░▒▓█"
            char_idx = int(norm_val * 4)
            row += chars[min(char_idx, 4)]
        texture.append(row)
    
    # 显示两次以演示平铺效果
    print("\n原始纹理:")
    for row in texture:
        print(f"  {row}{row}")  # 重复一次显示平铺效果
    
    print("\n(注意左右边缘的连续性)")


def example_wood_texture():
    """示例 7: 木纹纹理生成"""
    print("\n" + "=" * 60)
    print("示例 7: 木纹纹理生成")
    print("=" * 60)
    
    noise = PerlinNoise(seed=42)
    
    print("\n程序化木纹纹理:")
    
    for y in range(25):
        row = ""
        for x in range(50):
            # 木纹算法：使用距离中心的同心圆 + 扭曲
            cx, cy = 25, 12
            dx = x - cx
            dy = y - cy
            
            # 基础木纹（同心圆）
            dist = math.sqrt(dx * dx + dy * dy)
            ring = math.sin(dist * 0.5)
            
            # 添加噪声扭曲
            twist = noise.noise2d(x * 0.1, y * 0.1) * 0.5
            
            # 组合
            wood_val = math.sin(ring * 3 + twist * 2)
            
            # 映射到木纹颜色
            norm_val = (wood_val + 1) / 2
            chars = " .,:;+=*#%@"
            char_idx = int(norm_val * 9)
            row += chars[min(char_idx, 9)]
        print(f"  {row}")


def example_cloud_generation():
    """示例 8: 云层生成"""
    print("\n" + "=" * 60)
    print("示例 8: 云层生成")
    print("=" * 60)
    
    noise = PerlinNoise(seed=42, octaves=8, persistence=0.5)
    
    print("\n程序化云层:")
    
    for y in range(20):
        row = ""
        for x in range(60):
            # 使用 fBm 生成云层
            val = noise.fractal_brownian_motion_2d(x * 0.05, y * 0.05)
            
            # 阈值处理，让云更蓬松
            norm_val = (val + 1) / 2
            
            if norm_val < 0.4:
                char = ' '  # 天空
            elif norm_val < 0.5:
                char = '░'  # 淡云
            elif norm_val < 0.6:
                char = '▒'  # 中云
            elif norm_val < 0.7:
                char = '▓'  # 浓云
            else:
                char = '█'  # 厚云
            
            row += char
        print(f"  {row}")


def example_marble_texture():
    """示例 9: 大理石纹理"""
    print("\n" + "=" * 60)
    print("示例 9: 大理石纹理")
    print("=" * 60)
    
    noise = PerlinNoise(seed=42)
    
    print("\n程序化大理石纹理:")
    
    for y in range(25):
        row = ""
        for x in range(50):
            # 大理石算法：正弦波 + 湍流
            turbulence = noise.turbulence_2d(x * 0.05, y * 0.05, octaves=4)
            marble = math.sin(x * 0.1 + turbulence * 5)
            
            norm_val = (marble + 1) / 2
            chars = " .,:;+=*#%@"
            char_idx = int(norm_val * 9)
            row += chars[min(char_idx, 9)]
        print(f"  {row}")


def example_quick_functions():
    """示例 10: 便捷函数使用"""
    print("\n" + "=" * 60)
    print("示例 10: 便捷函数")
    print("=" * 60)
    
    # 快速生成噪声
    print("\n使用 perlin_noise() 快捷函数:")
    print(f"  1D: perlin_noise(0.5) = {perlin_noise(0.5):.4f}")
    print(f"  2D: perlin_noise(0.5, 0.5) = {perlin_noise(0.5, 0.5):.4f}")
    print(f"  3D: perlin_noise(0.5, 0.5, 0.5) = {perlin_noise(0.5, 0.5, 0.5):.4f}")
    
    # 快速生成地形
    print("\n使用 generate_terrain() 快速生成地形:")
    heightmap, terrain = generate_terrain(40, 15, seed=42, scale=30)
    print(render_terrain_ascii(terrain))


def main():
    """运行所有示例"""
    print("\n" + "=" * 60)
    print("Perlin Noise Utils - 使用示例")
    print("=" * 60)
    
    example_basic_noise()
    example_terrain_generation()
    example_heightmap_analysis()
    example_fractal_effects()
    example_animation_path()
    example_seamless_texture()
    example_wood_texture()
    example_cloud_generation()
    example_marble_texture()
    example_quick_functions()
    
    print("\n" + "=" * 60)
    print("所有示例完成!")
    print("=" * 60)


if __name__ == "__main__":
    main()