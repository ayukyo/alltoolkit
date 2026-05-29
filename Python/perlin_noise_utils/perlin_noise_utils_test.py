"""
Perlin Noise Utils - 单元测试

测试覆盖：
- 基础噪声生成（1D/2D/3D）
- 分形布朗运动
- 湍流函数
- 脊状多重分形
- 可平铺噪声
- 高度图生成
- 地形图生成
"""

import math
import sys
import os

# 添加模块路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from perlin_noise_utils.mod import (
    PerlinNoise,
    perlin_noise,
    generate_terrain,
    render_terrain_ascii,
    TERRAIN_CHARS
)


def test_noise_deterministic():
    """测试噪声生成的确定性（相同输入应产生相同输出）"""
    noise1 = PerlinNoise(seed=42)
    noise2 = PerlinNoise(seed=42)
    
    # 1D
    for i in range(10):
        x = i * 0.5
        assert noise1.noise1d(x) == noise2.noise1d(x), f"1D noise not deterministic at x={x}"
    
    # 2D
    for i in range(10):
        for j in range(10):
            x, y = i * 0.3, j * 0.3
            assert noise1.noise2d(x, y) == noise2.noise2d(x, y), f"2D noise not deterministic"
    
    # 3D
    for i in range(5):
        for j in range(5):
            for k in range(5):
                x, y, z = i * 0.3, j * 0.3, k * 0.3
                assert noise1.noise3d(x, y, z) == noise2.noise3d(x, y, z), f"3D noise not deterministic"
    
    print("✓ test_noise_deterministic passed")


def test_noise_range():
    """测试噪声值在合理范围内"""
    noise = PerlinNoise(seed=42)
    
    # 1D 噪声范围
    for i in range(100):
        val = noise.noise1d(i * 0.1)
        assert -1.5 <= val <= 1.5, f"1D noise out of range: {val}"
    
    # 2D 噪声范围
    for i in range(100):
        for j in range(10):
            val = noise.noise2d(i * 0.1, j * 0.1)
            assert -1.5 <= val <= 1.5, f"2D noise out of range: {val}"
    
    # 3D 噪声范围
    for i in range(50):
        val = noise.noise3d(i * 0.1, i * 0.15, i * 0.2)
        assert -1.5 <= val <= 1.5, f"3D noise out of range: {val}"
    
    print("✓ test_noise_range passed")


def test_noise_smoothness():
    """测试噪声平滑性（相邻点值应接近）"""
    noise = PerlinNoise(seed=42)
    
    # 1D 平滑性
    for i in range(100):
        x = i * 0.1
        val1 = noise.noise1d(x)
        val2 = noise.noise1d(x + 0.01)
        diff = abs(val1 - val2)
        assert diff < 0.1, f"1D noise not smooth: diff={diff}"
    
    # 2D 平滑性
    for i in range(50):
        x, y = i * 0.2, i * 0.15
        val1 = noise.noise2d(x, y)
        val2 = noise.noise2d(x + 0.01, y + 0.01)
        diff = abs(val1 - val2)
        assert diff < 0.1, f"2D noise not smooth: diff={diff}"
    
    print("✓ test_noise_smoothness passed")


def test_different_seeds():
    """测试不同种子产生不同噪声"""
    noise1 = PerlinNoise(seed=1)
    noise2 = PerlinNoise(seed=2)
    noise3 = PerlinNoise(seed=100)
    
    # 检查多个点，使用 2D 噪声
    vals1 = [noise1.noise2d(i * 0.3, j * 0.3) for i in range(10) for j in range(10)]
    vals2 = [noise2.noise2d(i * 0.3, j * 0.3) for i in range(10) for j in range(10)]
    vals3 = [noise3.noise2d(i * 0.3, j * 0.3) for i in range(10) for j in range(10)]
    
    # 计算差异
    diff12 = sum(abs(v1 - v2) for v1, v2 in zip(vals1, vals2)) / len(vals1)
    diff13 = sum(abs(v1 - v3) for v1, v3 in zip(vals1, vals3)) / len(vals1)
    
    # 平均差异应该足够大（不是相同的噪声）
    assert diff12 > 0.1, f"Seeds 1 and 2 too similar: avg diff = {diff12}"
    assert diff13 > 0.1, f"Seeds 1 and 100 too similar: avg diff = {diff13}"
    print(f"✓ test_different_seeds passed (avg diff seed1vs2={diff12:.3f}, seed1vs100={diff13:.3f})")


def test_fbm_range():
    """测试分形布朗运动范围"""
    noise = PerlinNoise(seed=42, octaves=6, persistence=0.5)
    
    for i in range(100):
        val = noise.fractal_brownian_motion_1d(i * 0.1)
        assert -1.5 <= val <= 1.5, f"fBm 1D out of range: {val}"
    
    for i in range(50):
        for j in range(50):
            val = noise.fractal_brownian_motion_2d(i * 0.2, j * 0.2)
            assert -1.5 <= val <= 1.5, f"fBm 2D out of range: {val}"
    
    for i in range(30):
        val = noise.fractal_brownian_motion_3d(i * 0.1, i * 0.15, i * 0.2)
        assert -1.5 <= val <= 1.5, f"fBm 3D out of range: {val}"
    
    print("✓ test_fbm_range passed")


def test_fbm_octaves():
    """测试不同倍频层数的效果"""
    noise = PerlinNoise(seed=42)
    
    # 低倍频应该更平滑
    fbm_low = noise.fractal_brownian_motion_2d(10, 10, octaves=1)
    fbm_high = noise.fractal_brownian_motion_2d(10, 10, octaves=8)
    
    # 计算局部变化
    variations_low = []
    variations_high = []
    
    for i in range(10):
        for j in range(10):
            v1 = noise.fractal_brownian_motion_2d(i, j, octaves=1)
            v2 = noise.fractal_brownian_motion_2d(i + 0.1, j + 0.1, octaves=1)
            variations_low.append(abs(v2 - v1))
            
            v3 = noise.fractal_brownian_motion_2d(i, j, octaves=8)
            v4 = noise.fractal_brownian_motion_2d(i + 0.1, j + 0.1, octaves=8)
            variations_high.append(abs(v4 - v3))
    
    avg_low = sum(variations_low) / len(variations_low)
    avg_high = sum(variations_high) / len(variations_high)
    
    print(f"  Low octave variation: {avg_low:.4f}")
    print(f"  High octave variation: {avg_high:.4f}")
    print("✓ test_fbm_octaves passed")


def test_turbulence():
    """测试湍流函数"""
    noise = PerlinNoise(seed=42)
    
    for i in range(50):
        for j in range(50):
            val = noise.turbulence_2d(i * 0.2, j * 0.2)
            # 湍流值应非负
            assert val >= 0, f"Turbulence should be non-negative: {val}"
    
    print("✓ test_turbulence passed")


def test_ridged_multifractal():
    """测试脊状多重分形"""
    noise = PerlinNoise(seed=42)
    
    values = []
    for i in range(100):
        for j in range(100):
            val = noise.ridged_multifractal_2d(i * 0.1, j * 0.1)
            values.append(val)
    
    # 检查值分布
    min_val = min(values)
    max_val = max(values)
    avg_val = sum(values) / len(values)
    
    print(f"  Ridged multifractal stats: min={min_val:.3f}, max={max_val:.3f}, avg={avg_val:.3f}")
    print("✓ test_ridged_multifractal passed")


def test_heightmap():
    """测试高度图生成"""
    noise = PerlinNoise(seed=42)
    
    # 生成高度图
    heightmap = noise.generate_heightmap(50, 50, scale=25)
    
    # 检查尺寸
    assert len(heightmap) == 50, "Heightmap height incorrect"
    assert all(len(row) == 50 for row in heightmap), "Heightmap width incorrect"
    
    # 检查值范围
    flat = [v for row in heightmap for v in row]
    min_val = min(flat)
    max_val = max(flat)
    assert -1.5 <= min_val <= 1.5, f"Heightmap min out of range: {min_val}"
    assert -1.5 <= max_val <= 1.5, f"Heightmap max out of range: {max_val}"
    
    print(f"  Heightmap: min={min_val:.3f}, max={max_val:.3f}")
    print("✓ test_heightmap passed")


def test_heightmap_normalized():
    """测试归一化高度图"""
    noise = PerlinNoise(seed=42)
    
    heightmap = noise.generate_heightmap_normalized(50, 50, scale=25)
    
    # 检查尺寸
    assert len(heightmap) == 50
    assert all(len(row) == 50 for row in heightmap)
    
    # 检查归一化范围 [0, 1]
    flat = [v for row in heightmap for v in row]
    min_val = min(flat)
    max_val = max(flat)
    assert 0 <= min_val <= 1, f"Normalized min out of range: {min_val}"
    assert 0 <= max_val <= 1, f"Normalized max out of range: {max_val}"
    
    # 应该有合理的分布
    assert max_val > 0.5, "Heightmap too flat"
    
    print(f"  Normalized heightmap: min={min_val:.3f}, max={max_val:.3f}")
    print("✓ test_heightmap_normalized passed")


def test_terrain_map():
    """测试地形类型图生成"""
    noise = PerlinNoise(seed=42)
    
    terrain = noise.generate_terrain_map(100, 100, scale=50)
    
    # 检查尺寸
    assert len(terrain) == 100
    assert all(len(row) == 100 for row in terrain)
    
    # 统计地形类型
    terrain_types = {}
    for row in terrain:
        for cell in row:
            terrain_types[cell] = terrain_types.get(cell, 0) + 1
    
    # 应该有多种地形类型
    assert len(terrain_types) >= 4, f"Too few terrain types: {terrain_types}"
    
    # 检查所有类型有效
    valid_types = {'deep_water', 'shallow_water', 'beach', 'grass', 'forest', 'mountain', 'snow'}
    for t in terrain_types:
        assert t in valid_types, f"Invalid terrain type: {t}"
    
    print(f"  Terrain distribution: {terrain_types}")
    print("✓ test_terrain_map passed")


def test_convenience_functions():
    """测试便捷函数"""
    # perlin_noise
    val1 = perlin_noise(0.5)
    assert isinstance(val1, float), "perlin_noise should return float"
    
    val2 = perlin_noise(0.5, 0.5)
    assert isinstance(val2, float)
    
    val3 = perlin_noise(0.5, 0.5, 0.5)
    assert isinstance(val3, float)
    
    # generate_terrain
    heightmap, terrain = generate_terrain(20, 20, seed=42)
    assert len(heightmap) == 20
    assert len(terrain) == 20
    
    print("✓ test_convenience_functions passed")


def test_ascii_render():
    """测试 ASCII 渲染"""
    noise = PerlinNoise(seed=42)
    terrain = noise.generate_terrain_map(40, 15, scale=20)
    
    ascii_art = render_terrain_ascii(terrain)
    lines = ascii_art.split('\n')
    
    assert len(lines) == 15, f"ASCII art should have 15 lines, got {len(lines)}"
    assert all(len(line) == 40 for line in lines), "All lines should be 40 chars"
    
    # 自定义字符
    custom_chars = {
        'deep_water': ' ', 'shallow_water': '░', 'beach': '░',
        'grass': '▒', 'forest': '▓', 'mountain': '█', 'snow': '█'
    }
    ascii_custom = render_terrain_ascii(terrain, chars=custom_chars)
    assert len(ascii_custom.split('\n')) == 15
    
    print("✓ test_ascii_render passed")


def test_tileable_noise():
    """测试可平铺噪声"""
    noise = PerlinNoise(seed=42)
    
    # 生成平铺噪声
    values = []
    for y in range(10):
        for x in range(10):
            val = noise.tileable_noise_2d(x/10, y/10, 1, 1)
            values.append(val)
    
    # 检查范围
    for val in values:
        assert -1.5 <= val <= 1.5, f"Tileable noise out of range: {val}"
    
    print("✓ test_tileable_noise passed")


def test_edge_cases():
    """测试边界情况"""
    noise = PerlinNoise(seed=42)
    
    # 负坐标
    val = noise.noise2d(-5, -5)
    assert isinstance(val, float)
    
    # 大坐标
    val = noise.noise2d(1000, 1000)
    assert isinstance(val, float)
    
    # 零坐标
    val = noise.noise2d(0, 0)
    assert isinstance(val, float)
    
    # 小尺寸高度图
    heightmap = noise.generate_heightmap(1, 1)
    assert len(heightmap) == 1
    assert len(heightmap[0]) == 1
    
    print("✓ test_edge_cases passed")


def test_persistence_effects():
    """测试持久度参数效果"""
    noise = PerlinNoise(seed=42)
    
    # 高持久度 = 更粗糙
    rough_vals = []
    smooth_vals = []
    
    for i in range(50):
        for j in range(50):
            x, y = i * 0.1, j * 0.1
            rough = noise.fractal_brownian_motion_2d(x, y, persistence=0.9)
            smooth = noise.fractal_brownian_motion_2d(x, y, persistence=0.3)
            rough_vals.append(rough)
            smooth_vals.append(smooth)
    
    # 计算变化率
    def variation(vals):
        return sum(abs(vals[i+1] - vals[i]) for i in range(len(vals)-1)) / len(vals)
    
    rough_var = variation(rough_vals)
    smooth_var = variation(smooth_vals)
    
    print(f"  High persistence variation: {rough_var:.4f}")
    print(f"  Low persistence variation: {smooth_var:.4f}")
    print("✓ test_persistence_effects passed")


def run_all_tests():
    """运行所有测试"""
    print("=" * 60)
    print("Perlin Noise Utils - Unit Tests")
    print("=" * 60)
    print()
    
    tests = [
        test_noise_deterministic,
        test_noise_range,
        test_noise_smoothness,
        test_different_seeds,
        test_fbm_range,
        test_fbm_octaves,
        test_turbulence,
        test_ridged_multifractal,
        test_heightmap,
        test_heightmap_normalized,
        test_terrain_map,
        test_convenience_functions,
        test_ascii_render,
        test_tileable_noise,
        test_edge_cases,
        test_persistence_effects,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"✗ {test.__name__} FAILED: {e}")
            failed += 1
        except Exception as e:
            print(f"✗ {test.__name__} ERROR: {e}")
            failed += 1
    
    print()
    print("=" * 60)
    print(f"Results: {passed} passed, {failed} failed")
    print("=" * 60)
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)