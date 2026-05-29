"""
Perlin Noise Utils - 零依赖 Perlin 噪声生成工具

实现经典 Perlin 噪声算法，支持 1D/2D/3D 噪声生成，
以及分形布朗运动（fBm）用于自然地形生成等场景。

Features:
- 1D, 2D, 3D Perlin 噪声
- 分形布朗运动（Fractal Brownian Motion）
- 湍流函数（Turbulence）
- 可平铺噪声
- 可配置的持久度、倍频程、振幅
- 零外部依赖
"""

import math
from typing import List, Tuple, Optional, Callable


class PerlinNoise:
    """
    Perlin 噪声生成器
    
    实现经典的 Perlin 噪声算法，支持多维度噪声生成和高级噪声组合。
    
    Example:
        >>> noise = PerlinNoise(seed=42)
        >>> value = noise.noise2d(0.5, 0.5)  # 获取 2D 噪声值
        >>> terrain = noise.fractal_brownian_motion_2d(10, 10, octaves=4)
    """
    
    # Perlin 梯度向量（用于3D噪声）
    GRADIENTS_3D = [
        (1,1,0), (-1,1,0), (1,-1,0), (-1,-1,0),
        (1,0,1), (-1,0,1), (1,0,-1), (-1,0,-1),
        (0,1,1), (0,-1,1), (0,1,-1), (0,-1,-1),
    ]
    
    def __init__(self, seed: int = 0, octaves: int = 4, persistence: float = 0.5):
        """
        初始化 Perlin 噪声生成器
        
        Args:
            seed: 随机种子，用于生成置换表
            octaves: 默认倍频程数量（影响细节层次）
            persistence: 持久度，控制每个倍频程的振幅衰减（0-1）
        """
        self.seed = seed
        self.octaves = octaves
        self.persistence = persistence
        
        # 生成置换表（Permutation Table）
        self._permutation = self._generate_permutation(seed)
        self._p = self._permutation + self._permutation  # 复制一份用于溢出处理
        
        # 2D 梯度向量（预计算8个方向）
        self._gradients_2d = [
            (math.sqrt(2), 0), (-math.sqrt(2), 0),
            (0, math.sqrt(2)), (0, -math.sqrt(2)),
            (1, 1), (-1, 1), (1, -1), (-1, -1)
        ]
        
    def _generate_permutation(self, seed: int) -> List[int]:
        """
        根据种子生成置换表
        
        使用线性同余生成器（LCG）生成 0-255 的随机排列。
        """
        # 初始化 0-255 的列表
        perm = list(range(256))
        
        # Fisher-Yates 洗牌算法，使用种子生成的随机数
        # 使用简单的 LCG 作为随机数生成器
        lcg_seed = seed if seed != 0 else 1
        
        for i in range(255, 0, -1):
            # LCG: next = (current * 1103515245 + 12345) & 0x7fffffff
            lcg_seed = (lcg_seed * 1103515245 + 12345) & 0x7fffffff
            j = lcg_seed % (i + 1)
            perm[i], perm[j] = perm[j], perm[i]
            
        return perm
    
    def _fade(self, t: float) -> float:
        """
        缓动函数（Ease Curve）
        
        使用 6t^5 - 15t^4 + 10t^3 曲线平滑插值，
        确保边界处的导数为0，产生更自然的过渡。
        """
        return t * t * t * (t * (t * 6 - 15) + 10)
    
    def _lerp(self, a: float, b: float, t: float) -> float:
        """线性插值"""
        return a + t * (b - a)
    
    def _gradient_1d(self, hash_val: int, x: float) -> float:
        """计算 1D 梯度"""
        # 根据 hash 值选择梯度方向
        h = hash_val & 1
        gradient = 1 if h == 0 else -1
        return gradient * x
    
    def _gradient_2d(self, hash_val: int, x: float, y: float) -> float:
        """计算 2D 梯度"""
        # 选择预计算的梯度向量
        h = hash_val & 7
        gx, gy = self._gradients_2d[h]
        return gx * x + gy * y
    
    def _gradient_3d(self, hash_val: int, x: float, y: float, z: float) -> float:
        """计算 3D 梯度"""
        h = hash_val & 11
        gx, gy, gz = self.GRADIENTS_3D[h]
        return gx * x + gy * y + gz * z
    
    def noise1d(self, x: float) -> float:
        """
        生成 1D Perlin 噪声
        
        Args:
            x: 输入坐标
            
        Returns:
            噪声值，范围约 [-1, 1]
            
        Example:
            >>> noise = PerlinNoise(seed=42)
            >>> noise.noise1d(0.0)  # 固定值
            >>> noise.noise1d(1.5)  # 平滑过渡
        """
        # 找到单位格子
        xi = int(math.floor(x)) & 255
        x_rel = x - math.floor(x)
        
        # 计算缓动曲线
        u = self._fade(x_rel)
        
        # 从置换表获取哈希值
        a = self._p[xi]
        b = self._p[xi + 1]
        
        # 计算梯度贡献
        n0 = self._gradient_1d(a, x_rel)
        n1 = self._gradient_1d(b, x_rel - 1)
        
        # 插值
        return self._lerp(n0, n1, u)
    
    def noise2d(self, x: float, y: float) -> float:
        """
        生成 2D Perlin 噪声
        
        Args:
            x: X 坐标
            y: Y 坐标
            
        Returns:
            噪声值，范围约 [-1, 1]
            
        Example:
            >>> noise = PerlinNoise(seed=42)
            >>> value = noise.noise2d(0.5, 0.5)
            >>> value = noise.noise2d(100, 200)
        """
        # 找到单位格子
        xi = int(math.floor(x)) & 255
        yi = int(math.floor(y)) & 255
        
        x_rel = x - math.floor(x)
        y_rel = y - math.floor(y)
        
        # 计算缓动曲线
        u = self._fade(x_rel)
        v = self._fade(y_rel)
        
        # 从置换表获取哈希值
        aa = self._p[self._p[xi] + yi]
        ab = self._p[self._p[xi] + yi + 1]
        ba = self._p[self._p[xi + 1] + yi]
        bb = self._p[self._p[xi + 1] + yi + 1]
        
        # 计算梯度贡献
        n00 = self._gradient_2d(aa, x_rel, y_rel)
        n01 = self._gradient_2d(ab, x_rel, y_rel - 1)
        n10 = self._gradient_2d(ba, x_rel - 1, y_rel)
        n11 = self._gradient_2d(bb, x_rel - 1, y_rel - 1)
        
        # 双线性插值
        nx0 = self._lerp(n00, n10, u)
        nx1 = self._lerp(n01, n11, u)
        
        return self._lerp(nx0, nx1, v)
    
    def noise3d(self, x: float, y: float, z: float) -> float:
        """
        生成 3D Perlin 噪声
        
        Args:
            x: X 坐标
            y: Y 坐标
            z: Z 坐标
            
        Returns:
            噪声值，范围约 [-1, 1]
            
        Example:
            >>> noise = PerlinNoise(seed=42)
            >>> value = noise.noise3d(1.0, 2.0, 3.0)
        """
        # 找到单位格子
        xi = int(math.floor(x)) & 255
        yi = int(math.floor(y)) & 255
        zi = int(math.floor(z)) & 255
        
        x_rel = x - math.floor(x)
        y_rel = y - math.floor(y)
        z_rel = z - math.floor(z)
        
        # 计算缓动曲线
        u = self._fade(x_rel)
        v = self._fade(y_rel)
        w = self._fade(z_rel)
        
        # 从置换表获取哈希值
        aaa = self._p[self._p[self._p[xi] + yi] + zi]
        aab = self._p[self._p[self._p[xi] + yi] + zi + 1]
        aba = self._p[self._p[self._p[xi] + yi + 1] + zi]
        abb = self._p[self._p[self._p[xi] + yi + 1] + zi + 1]
        baa = self._p[self._p[self._p[xi + 1] + yi] + zi]
        bab = self._p[self._p[self._p[xi + 1] + yi] + zi + 1]
        bba = self._p[self._p[self._p[xi + 1] + yi + 1] + zi]
        bbb = self._p[self._p[self._p[xi + 1] + yi + 1] + zi + 1]
        
        # 计算梯度贡献
        n000 = self._gradient_3d(aaa, x_rel, y_rel, z_rel)
        n001 = self._gradient_3d(aab, x_rel, y_rel, z_rel - 1)
        n010 = self._gradient_3d(aba, x_rel, y_rel - 1, z_rel)
        n011 = self._gradient_3d(abb, x_rel, y_rel - 1, z_rel - 1)
        n100 = self._gradient_3d(baa, x_rel - 1, y_rel, z_rel)
        n101 = self._gradient_3d(bab, x_rel - 1, y_rel, z_rel - 1)
        n110 = self._gradient_3d(bba, x_rel - 1, y_rel - 1, z_rel)
        n111 = self._gradient_3d(bbb, x_rel - 1, y_rel - 1, z_rel - 1)
        
        # 三线性插值
        nx00 = self._lerp(n000, n100, u)
        nx01 = self._lerp(n001, n101, u)
        nx10 = self._lerp(n010, n110, u)
        nx11 = self._lerp(n011, n111, u)
        
        nxy0 = self._lerp(nx00, nx10, v)
        nxy1 = self._lerp(nx01, nx11, v)
        
        return self._lerp(nxy0, nxy1, w)
    
    def fractal_brownian_motion_1d(
        self, 
        x: float, 
        octaves: Optional[int] = None,
        persistence: Optional[float] = None,
        lacunarity: float = 2.0,
        amplitude: float = 1.0,
        frequency: float = 1.0
    ) -> float:
        """
        1D 分形布朗运动（Fractal Brownian Motion）
        
        通过叠加多个不同频率和振幅的噪声层，生成更复杂的自然效果。
        
        Args:
            x: 输入坐标
            octaves: 倍频层数（更多 = 更精细）
            persistence: 持久度（每层振幅衰减）
            lacunarity: 间隙度（每层频率增长）
            amplitude: 初始振幅
            frequency: 初始频率
            
        Returns:
            组合噪声值
            
        Example:
            >>> noise = PerlinNoise(seed=42)
            >>> # 更平滑的地形
            >>> value = noise.fractal_brownian_motion_1d(x, octaves=4, persistence=0.5)
        """
        octaves = octaves if octaves is not None else self.octaves
        persistence = persistence if persistence is not None else self.persistence
        
        total = 0.0
        amp = amplitude
        freq = frequency
        max_value = 0.0
        
        for _ in range(octaves):
            total += self.noise1d(x * freq) * amp
            max_value += amp
            amp *= persistence
            freq *= lacunarity
            
        return total / max_value if max_value > 0 else 0
    
    def fractal_brownian_motion_2d(
        self, 
        x: float, 
        y: float,
        octaves: Optional[int] = None,
        persistence: Optional[float] = None,
        lacunarity: float = 2.0,
        amplitude: float = 1.0,
        frequency: float = 1.0
    ) -> float:
        """
        2D 分形布朗运动（Fractal Brownian Motion）
        
        用于生成地形高度图、云层、大理石纹理等自然效果。
        
        Args:
            x: X 坐标
            y: Y 坐标
            octaves: 倍频层数（更多 = 更精细）
            persistence: 持久度（每层振幅衰减，接近0更平滑，接近1更粗糙）
            lacunarity: 间隙度（每层频率增长，通常为2）
            amplitude: 初始振幅
            frequency: 初始频率
            
        Returns:
            组合噪声值，范围约 [-1, 1]
            
        Example:
            >>> noise = PerlinNoise(seed=42)
            >>> # 生成地形高度
            >>> height = noise.fractal_brownian_motion_2d(x, y, octaves=6, persistence=0.5)
        """
        octaves = octaves if octaves is not None else self.octaves
        persistence = persistence if persistence is not None else self.persistence
        
        total = 0.0
        amp = amplitude
        freq = frequency
        max_value = 0.0
        
        for _ in range(octaves):
            total += self.noise2d(x * freq, y * freq) * amp
            max_value += amp
            amp *= persistence
            freq *= lacunarity
            
        return total / max_value if max_value > 0 else 0
    
    def fractal_brownian_motion_3d(
        self,
        x: float,
        y: float,
        z: float,
        octaves: Optional[int] = None,
        persistence: Optional[float] = None,
        lacunarity: float = 2.0,
        amplitude: float = 1.0,
        frequency: float = 1.0
    ) -> float:
        """
        3D 分形布朗运动
        
        用于生成3D纹理、体积云等效果。
        
        Args:
            x, y, z: 3D 坐标
            octaves: 倍频层数
            persistence: 持久度
            lacunarity: 间隙度
            amplitude: 初始振幅
            frequency: 初始频率
            
        Returns:
            组合噪声值
        """
        octaves = octaves if octaves is not None else self.octaves
        persistence = persistence if persistence is not None else self.persistence
        
        total = 0.0
        amp = amplitude
        freq = frequency
        max_value = 0.0
        
        for _ in range(octaves):
            total += self.noise3d(x * freq, y * freq, z * freq) * amp
            max_value += amp
            amp *= persistence
            freq *= lacunarity
            
        return total / max_value if max_value > 0 else 0
    
    def turbulence_2d(
        self,
        x: float,
        y: float,
        octaves: Optional[int] = None,
        lacunarity: float = 2.0,
        amplitude: float = 1.0,
        frequency: float = 1.0
    ) -> float:
        """
        2D 湍流函数（Turbulence）
        
        通过对噪声取绝对值后叠加，产生类似湍流、火焰、
        大理石纹理的效果。
        
        Args:
            x, y: 2D 坐标
            octaves: 倍频层数
            lacunarity: 间隙度
            amplitude: 初始振幅
            frequency: 初始频率
            
        Returns:
            湍流噪声值
            
        Example:
            >>> noise = PerlinNoise(seed=42)
            >>> marble = abs(noise.turbulence_2d(x, y, octaves=6))
        """
        octaves = octaves if octaves is not None else self.octaves
        
        total = 0.0
        amp = amplitude
        freq = frequency
        
        for _ in range(octaves):
            total += abs(self.noise2d(x * freq, y * freq)) * amp
            amp *= 0.5
            freq *= lacunarity
            
        return total
    
    def ridged_multifractal_2d(
        self,
        x: float,
        y: float,
        octaves: Optional[int] = None,
        lacunarity: float = 2.0,
        offset: float = 1.0,
        gain: float = 2.0
    ) -> float:
        """
        2D 脊状多重分形（Ridged Multifractal）
        
        生成带有"脊状"特征的地形，适合山脉、峡谷等场景。
        通过反转噪声值产生尖锐的山脊效果。
        
        Args:
            x, y: 2D 坐标
            octaves: 倍频层数
            lacunarity: 间隙度
            offset: 偏移值（控制脊的高度）
            gain: 增益（控制细节强度）
            
        Returns:
            脊状噪声值
        """
        octaves = octaves if octaves is not None else self.octaves
        
        total = 0.0
        freq = 1.0
        weight = 1.0
        
        for _ in range(octaves):
            signal = self.noise2d(x * freq, y * freq)
            # 取绝对值并反转，产生脊状效果
            signal = offset - abs(signal)
            signal *= signal  # 平方增强效果
            total += signal * weight
            weight = min(1.0, signal * gain)
            freq *= lacunarity
            
        return total
    
    def tileable_noise_2d(
        self,
        x: float,
        y: float,
        tile_width: float = 1.0,
        tile_height: float = 1.0
    ) -> float:
        """
        可平铺的 2D 噪声
        
        生成无缝平铺的噪声，适合纹理贴图。
        
        Args:
            x, y: 2D 坐标
            tile_width: 平铺宽度（周期）
            tile_height: 平铺高度（周期）
            
        Returns:
            平铺噪声值
            
        Example:
            >>> noise = PerlinNoise(seed=42)
            >>> # 生成 256x256 的可平铺噪声
            >>> for y in range(256):
            ...     for x in range(256):
            ...         value = noise.tileable_noise_2d(x/256, y/256, 1, 1)
        """
        # 使用 3D 噪声在球面上采样，实现平铺
        # 这是一个简化版本，通过 4 角混合实现
        nx = x / tile_width
        ny = y / tile_height
        
        # 计算权重
        wx = (1 - math.cos(nx * 2 * math.pi)) / 2
        wy = (1 - math.cos(ny * 2 * math.pi)) / 2
        
        # 混合四个角
        n00 = self.noise2d(nx * tile_width, ny * tile_height)
        n10 = self.noise2d(nx * tile_width + tile_width, ny * tile_height)
        n01 = self.noise2d(nx * tile_width, ny * tile_height + tile_height)
        n11 = self.noise2d(nx * tile_width + tile_width, ny * tile_height + tile_height)
        
        # 双线性插值
        nx0 = n00 * (1 - wx) + n10 * wx
        nx1 = n01 * (1 - wx) + n11 * wx
        
        return nx0 * (1 - wy) + nx1 * wy
    
    def generate_heightmap(
        self,
        width: int,
        height: int,
        scale: float = 100.0,
        octaves: Optional[int] = None,
        persistence: Optional[float] = None,
        offset_x: float = 0.0,
        offset_y: float = 0.0
    ) -> List[List[float]]:
        """
        生成高度图
        
        用于地形生成、灰度纹理等场景。
        
        Args:
            width: 宽度
            height: 高度
            scale: 缩放因子（越大越平滑）
            octaves: 倍频层数
            persistence: 持久度
            offset_x, offset_y: 偏移量
            
        Returns:
            2D 高度数组，值范围约 [-1, 1]
            
        Example:
            >>> noise = PerlinNoise(seed=42)
            >>> heightmap = noise.generate_heightmap(256, 256, scale=50)
        """
        octaves = octaves if octaves is not None else self.octaves
        persistence = persistence if persistence is not None else self.persistence
        
        heightmap = []
        for y in range(height):
            row = []
            for x in range(width):
                nx = (x + offset_x) / scale
                ny = (y + offset_y) / scale
                value = self.fractal_brownian_motion_2d(
                    nx, ny, octaves=octaves, persistence=persistence
                )
                row.append(value)
            heightmap.append(row)
            
        return heightmap
    
    def generate_heightmap_normalized(
        self,
        width: int,
        height: int,
        scale: float = 100.0,
        octaves: Optional[int] = None,
        persistence: Optional[float] = None,
        offset_x: float = 0.0,
        offset_y: float = 0.0
    ) -> List[List[float]]:
        """
        生成归一化高度图（0-1 范围）
        
        Args:
            width, height: 尺寸
            scale: 缩放因子
            octaves: 倍频层数
            persistence: 持久度
            offset_x, offset_y: 偏移量
            
        Returns:
            2D 高度数组，值范围 [0, 1]
        """
        heightmap = self.generate_heightmap(
            width, height, scale, octaves, persistence, offset_x, offset_y
        )
        
        # 归一化到 [0, 1]
        min_val = min(min(row) for row in heightmap)
        max_val = max(max(row) for row in heightmap)
        range_val = max_val - min_val
        
        if range_val == 0:
            return [[0.5 for _ in range(width)] for _ in range(height)]
        
        return [
            [(v - min_val) / range_val for v in row]
            for row in heightmap
        ]
    
    def generate_terrain_map(
        self,
        width: int,
        height: int,
        scale: float = 100.0,
        octaves: Optional[int] = None,
        persistence: Optional[float] = None,
        sea_level: float = 0.4
    ) -> List[List[str]]:
        """
        生成地形类型图
        
        根据高度值分配地形类型：深水、浅水、沙滩、草地、森林、山地、雪峰。
        
        Args:
            width, height: 尺寸
            scale: 缩放因子
            octaves: 倍频层数
            persistence: 持久度
            sea_level: 海平面高度（0-1）
            
        Returns:
            2D 地形类型数组，值为：
            - 'deep_water' : 深水
            - 'shallow_water' : 浅水
            - 'beach' : 沙滩
            - 'grass' : 草地
            - 'forest' : 森林
            - 'mountain' : 山地
            - 'snow' : 雪峰
            
        Example:
            >>> noise = PerlinNoise(seed=42)
            >>> terrain = noise.generate_terrain_map(100, 100)
            >>> print(terrain[50][50])  # 'forest'
        """
        heightmap = self.generate_heightmap_normalized(
            width, height, scale, octaves, persistence
        )
        
        terrain_map = []
        for row in heightmap:
            terrain_row = []
            for h in row:
                if h < sea_level - 0.1:
                    terrain_row.append('deep_water')
                elif h < sea_level:
                    terrain_row.append('shallow_water')
                elif h < sea_level + 0.05:
                    terrain_row.append('beach')
                elif h < 0.55:
                    terrain_row.append('grass')
                elif h < 0.7:
                    terrain_row.append('forest')
                elif h < 0.85:
                    terrain_row.append('mountain')
                else:
                    terrain_row.append('snow')
            terrain_map.append(terrain_row)
            
        return terrain_map


def perlin_noise(
    x: float, 
    y: float = 0, 
    z: float = 0, 
    seed: int = 0
) -> float:
    """
    快捷函数：生成 Perlin 噪声
    
    根据提供的坐标数量自动选择维度。
    
    Args:
        x: X 坐标
        y: Y 坐标（可选，仅用于 2D/3D）
        z: Z 坐标（可选，仅用于 3D）
        seed: 随机种子
        
    Returns:
        噪声值
        
    Example:
        >>> perlin_noise(0.5)  # 1D
        >>> perlin_noise(0.5, 0.5)  # 2D
        >>> perlin_noise(0.5, 0.5, 0.5)  # 3D
    """
    noise = PerlinNoise(seed=seed)
    if z != 0:
        return noise.noise3d(x, y, z)
    elif y != 0:
        return noise.noise2d(x, y)
    else:
        return noise.noise1d(x)


def generate_terrain(
    width: int,
    height: int,
    seed: int = 0,
    scale: float = 100.0,
    octaves: int = 6,
    persistence: float = 0.5,
    sea_level: float = 0.4
) -> Tuple[List[List[float]], List[List[str]]]:
    """
    快捷函数：生成地形
    
    一次性生成高度图和地形类型图。
    
    Args:
        width, height: 尺寸
        seed: 随机种子
        scale: 缩放因子
        octaves: 倍频层数
        persistence: 持久度
        sea_level: 海平面高度
        
    Returns:
        (高度图, 地形类型图)
        
    Example:
        >>> heightmap, terrain = generate_terrain(256, 256, seed=42)
    """
    noise = PerlinNoise(seed=seed, octaves=octaves, persistence=persistence)
    heightmap = noise.generate_heightmap_normalized(width, height, scale)
    terrain = noise.generate_terrain_map(width, height, scale, octaves, persistence, sea_level)
    return heightmap, terrain


# ASCII 艺术地形渲染
TERRAIN_CHARS = {
    'deep_water': '≈',
    'shallow_water': '~',
    'beach': '.',
    'grass': ',',
    'forest': '♣',
    'mountain': '▲',
    'snow': '¤'
}


def render_terrain_ascii(terrain: List[List[str]], chars: Optional[dict] = None) -> str:
    """
    将地形图渲染为 ASCII 艺术字符串
    
    Args:
        terrain: 地形类型图
        chars: 自定义字符映射（可选）
        
    Returns:
        ASCII 艺术字符串
        
    Example:
        >>> heightmap, terrain = generate_terrain(40, 20)
        >>> print(render_terrain_ascii(terrain))
    """
    chars = chars or TERRAIN_CHARS
    lines = []
    for row in terrain:
        line = ''.join(chars.get(cell, '?') for cell in row)
        lines.append(line)
    return '\n'.join(lines)


if __name__ == "__main__":
    # 简单演示
    print("Perlin Noise Utils Demo")
    print("=" * 50)
    
    # 创建噪声生成器
    noise = PerlinNoise(seed=42, octaves=6, persistence=0.5)
    
    # 生成 1D 噪声序列
    print("\n1D Perlin Noise:")
    for i in range(10):
        val = noise.noise1d(i * 0.1)
        bar = '█' * int((val + 1) * 20)
        print(f"  {i*0.1:.1f}: {bar}")
    
    # 生成 ASCII 地形
    print("\n2D Terrain Map (ASCII):")
    terrain = noise.generate_terrain_map(60, 20, scale=30)
    print(render_terrain_ascii(terrain))
    
    # 打印统计信息
    heightmap = noise.generate_heightmap_normalized(100, 100, scale=50)
    flat = [v for row in heightmap for v in row]
    print(f"\nHeightmap statistics (100x100):")
    print(f"  Min: {min(flat):.3f}")
    print(f"  Max: {max(flat):.3f}")
    print(f"  Avg: {sum(flat)/len(flat):.3f}")