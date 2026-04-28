"""
Morton Code Utils - Morton编码工具（Z-order曲线）

用于空间索引的Morton编码/解码工具，将多维坐标映射到一维值。
广泛应用于数据库索引、地理空间查询、图像处理等领域。

特性：
- 2D和3D坐标的Morton编码/解码
- 支持不同位宽（16位、32位、64位）
- 相邻区域查询
- 范围编码支持
- 零外部依赖
"""

from typing import Tuple, List, Optional, Generator


def spread_bits_2d(x: int) -> int:
    """
    将整数的位分散开来，用于2D Morton编码。
    
    例如: 0b1101 -> 0b100010001
    
    Args:
        x: 输入整数（坐标的一个分量）
        
    Returns:
        分散后的整数
        
    Example:
        >>> spread_bits_2d(3)
        5
    """
    x &= 0x0000FFFF
    x = (x | (x << 8)) & 0x00FF00FF
    x = (x | (x << 4)) & 0x0F0F0F0F
    x = (x | (x << 2)) & 0x33333333
    x = (x | (x << 1)) & 0x55555555
    return x


def compact_bits_2d(x: int) -> int:
    """
    将分散的位压缩回来，用于2D Morton解码。
    
    Args:
        x: 分散后的整数
        
    Returns:
        压缩后的整数
        
    Example:
        >>> compact_bits_2d(5)
        3
    """
    x &= 0x55555555
    x = (x | (x >> 1)) & 0x33333333
    x = (x | (x >> 2)) & 0x0F0F0F0F
    x = (x | (x >> 4)) & 0x00FF00FF
    x = (x | (x >> 8)) & 0x0000FFFF
    return x


def spread_bits_3d(x: int) -> int:
    """
    将整数的位分散开来，用于3D Morton编码。
    
    Args:
        x: 输入整数（坐标的一个分量）
        
    Returns:
        分散后的整数
    """
    x &= 0x000003FF
    x = (x | (x << 16)) & 0xFF0000FF
    x = (x | (x << 8)) & 0x0300F00F
    x = (x | (x << 4)) & 0x030C30C3
    x = (x | (x << 2)) & 0x09249249
    return x


def compact_bits_3d(x: int) -> int:
    """
    将分散的位压缩回来，用于3D Morton解码。
    
    Args:
        x: 分散后的整数
        
    Returns:
        压缩后的整数
    """
    x &= 0x09249249
    x = (x | (x >> 2)) & 0x030C30C3
    x = (x | (x >> 4)) & 0x0300F00F
    x = (x | (x >> 8)) & 0xFF0000FF
    x = (x | (x >> 16)) & 0x000003FF
    return x


def encode_2d(x: int, y: int) -> int:
    """
    将2D坐标编码为Morton码。
    
    使用交替位方案：结果的偶数位来自y，奇数位来自x。
    坐标值范围为 [0, 2^16-1]（65535）。
    
    Args:
        x: X坐标（0-65535）
        y: Y坐标（0-65535）
        
    Returns:
        Morton码（最大64位，实际使用32位）
        
    Raises:
        ValueError: 坐标超出范围
        
    Example:
        >>> encode_2d(0, 0)
        0
        >>> encode_2d(1, 0)
        1
        >>> encode_2d(0, 1)
        2
        >>> encode_2d(1, 1)
        3
    """
    if x < 0 or x > 0xFFFF:
        raise ValueError(f"x坐标超出范围 [0, 65535]: {x}")
    if y < 0 or y > 0xFFFF:
        raise ValueError(f"y坐标超出范围 [0, 65535]: {y}")
    
    return (spread_bits_2d(y) << 1) | spread_bits_2d(x)


def decode_2d(morton_code: int) -> Tuple[int, int]:
    """
    将Morton码解码为2D坐标。
    
    Args:
        morton_code: Morton编码值
        
    Returns:
        (x, y) 坐标元组
        
    Raises:
        ValueError: Morton码为负数
        
    Example:
        >>> decode_2d(0)
        (0, 0)
        >>> decode_2d(1)
        (1, 0)
        >>> decode_2d(2)
        (0, 1)
        >>> decode_2d(3)
        (1, 1)
    """
    if morton_code < 0:
        raise ValueError(f"Morton码不能为负数: {morton_code}")
    
    x = compact_bits_2d(morton_code)
    y = compact_bits_2d(morton_code >> 1)
    return (x, y)


def encode_3d(x: int, y: int, z: int) -> int:
    """
    将3D坐标编码为Morton码。
    
    坐标值范围为 [0, 2^10-1]（1023）。
    
    Args:
        x: X坐标（0-1023）
        y: Y坐标（0-1023）
        z: Z坐标（0-1023）
        
    Returns:
        Morton码（最大30位）
        
    Raises:
        ValueError: 坐标超出范围
        
    Example:
        >>> encode_3d(0, 0, 0)
        0
        >>> encode_3d(1, 0, 0)
        1
        >>> encode_3d(0, 1, 0)
        2
        >>> encode_3d(0, 0, 1)
        4
    """
    if x < 0 or x > 0x3FF:
        raise ValueError(f"x坐标超出范围 [0, 1023]: {x}")
    if y < 0 or y > 0x3FF:
        raise ValueError(f"y坐标超出范围 [0, 1023]: {y}")
    if z < 0 or z > 0x3FF:
        raise ValueError(f"z坐标超出范围 [0, 1023]: {z}")
    
    return (spread_bits_3d(z) << 2) | (spread_bits_3d(y) << 1) | spread_bits_3d(x)


def decode_3d(morton_code: int) -> Tuple[int, int, int]:
    """
    将Morton码解码为3D坐标。
    
    Args:
        morton_code: Morton编码值
        
    Returns:
        (x, y, z) 坐标元组
        
    Raises:
        ValueError: Morton码为负数
        
    Example:
        >>> decode_3d(0)
        (0, 0, 0)
        >>> decode_3d(1)
        (1, 0, 0)
        >>> decode_3d(7)
        (1, 1, 1)
    """
    if morton_code < 0:
        raise ValueError(f"Morton码不能为负数: {morton_code}")
    
    x = compact_bits_3d(morton_code)
    y = compact_bits_3d(morton_code >> 1)
    z = compact_bits_3d(morton_code >> 2)
    return (x, y, z)


def encode_with_depth_2d(x: int, y: int, depth: int) -> int:
    """
    在指定深度编码2D坐标。
    
    深度决定了坐标范围：[0, 2^depth - 1]
    
    Args:
        x: X坐标
        y: Y坐标
        depth: 深度（1-32），决定坐标范围
        
    Returns:
        Morton码
        
    Raises:
        ValueError: 参数无效
    """
    if depth < 1 or depth > 32:
        raise ValueError(f"深度必须在 [1, 32] 范围内: {depth}")
    
    max_coord = (1 << depth) - 1
    if x < 0 or x > max_coord:
        raise ValueError(f"x坐标超出范围 [0, {max_coord}]: {x}")
    if y < 0 or y > max_coord:
        raise ValueError(f"y坐标超出范围 [0, {max_coord}]: {y}")
    
    return encode_2d(x, y)


def decode_with_depth_2d(morton_code: int, depth: int) -> Tuple[int, int]:
    """
    在指定深度解码2D Morton码。
    
    Args:
        morton_code: Morton编码值
        depth: 深度
        
    Returns:
        (x, y) 坐标元组
    """
    if depth < 1 or depth > 32:
        raise ValueError(f"深度必须在 [1, 32] 范围内: {depth}")
    
    x, y = decode_2d(morton_code)
    
    # 掩码到正确深度
    mask = (1 << depth) - 1
    return (x & mask, y & mask)


def get_neighbors_2d(x: int, y: int, include_diagonal: bool = True) -> List[Tuple[int, int]]:
    """
    获取2D坐标的邻居坐标。
    
    Args:
        x: X坐标
        y: Y坐标
        include_diagonal: 是否包含对角邻居
        
    Returns:
        邻居坐标列表
        
    Example:
        >>> get_neighbors_2d(5, 5, include_diagonal=False)
        [(4, 5), (6, 5), (5, 4), (5, 6)]
        >>> len(get_neighbors_2d(5, 5, include_diagonal=True))
        8
    """
    neighbors = []
    
    # 上下左右
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nx, ny = x + dx, y + dy
        if nx >= 0 and ny >= 0:  # 只检查非负，不设置上限
            neighbors.append((nx, ny))
    
    if include_diagonal:
        # 对角方向
        for dx, dy in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
            nx, ny = x + dx, y + dy
            if nx >= 0 and ny >= 0:
                neighbors.append((nx, ny))
    
    return neighbors


def get_neighbors_morton_2d(morton_code: int, include_diagonal: bool = True) -> List[int]:
    """
    获取Morton码的邻居Morton码。
    
    Args:
        morton_code: Morton编码值
        include_diagonal: 是否包含对角邻居
        
    Returns:
        邻居Morton码列表
        
    Example:
        >>> get_neighbors_morton_2d(0, include_diagonal=False)
        [1, 2]
    """
    x, y = decode_2d(morton_code)
    neighbors = get_neighbors_2d(x, y, include_diagonal)
    return [encode_2d(nx, ny) for nx, ny in neighbors]


def get_cell_level_2d(morton_code: int) -> int:
    """
    计算Morton码的层级（深度）。
    
    基于最高有效位的位置计算。
    
    Args:
        morton_code: Morton编码值
        
    Returns:
        层级深度
        
    Example:
        >>> get_cell_level_2d(0)
        0
        >>> get_cell_level_2d(1)
        1
        >>> get_cell_level_2d(15)
        2
    """
    if morton_code == 0:
        return 0
    
    level = 0
    while morton_code > 0:
        morton_code >>= 2
        level += 1
    return level


def get_parent_2d(morton_code: int) -> int:
    """
    获取父级Morton码。
    
    Args:
        morton_code: Morton编码值
        
    Returns:
        父级Morton码
        
    Example:
        >>> get_parent_2d(7)
        0
        >>> get_parent_2d(4)
        1
    """
    return morton_code >> 2


def get_children_2d(morton_code: int) -> List[int]:
    """
    获取所有子级Morton码。
    
    Args:
        morton_code: Morton编码值
        
    Returns:
        4个子级Morton码列表
        
    Example:
        >>> get_children_2d(0)
        [0, 1, 2, 3]
        >>> get_children_2d(1)
        [4, 5, 6, 7]
    """
    base = morton_code << 2
    return [base, base | 1, base | 2, base | 3]


def is_ancestor_2d(potential_ancestor: int, morton_code: int) -> bool:
    """
    检查一个Morton码是否是另一个的祖先。
    
    Args:
        potential_ancestor: 潜在的祖先Morton码
        morton_code: 子Morton码
        
    Returns:
        是否为祖先
        
    Example:
        >>> is_ancestor_2d(0, 7)
        True
        >>> is_ancestor_2d(1, 7)
        True
        >>> is_ancestor_2d(2, 7)
        False
    """
    if potential_ancestor == morton_code:
        return False
    
    # 计算潜在祖先的深度
    ancestor_level = get_cell_level_2d(potential_ancestor)
    code_level = get_cell_level_2d(morton_code)
    
    if ancestor_level >= code_level:
        return False
    
    # 将子码右移到祖先的级别进行比较
    shifted = morton_code >> (2 * (code_level - ancestor_level))
    return shifted == potential_ancestor


def range_to_morton_codes_2d(
    x_min: int, y_min: int, 
    x_max: int, y_max: int,
    max_depth: int = 16
) -> List[int]:
    """
    将2D范围转换为Morton码列表。
    
    生成覆盖指定矩形区域的所有Morton码。
    
    Args:
        x_min: X最小值
        y_min: Y最小值
        x_max: X最大值
        y_max: Y最大值
        max_depth: 最大深度
        
    Returns:
        Morton码列表
        
    Example:
        >>> codes = range_to_morton_codes_2d(0, 0, 1, 1, max_depth=1)
        >>> sorted(codes)
        [0, 1, 2, 3]
    """
    if x_min < 0 or y_min < 0 or x_max < 0 or y_max < 0:
        raise ValueError("坐标不能为负数")
    if x_min > x_max or y_min > y_max:
        raise ValueError("最小值不能大于最大值")
    
    codes = []
    for y in range(y_min, y_max + 1):
        for x in range(x_min, x_max + 1):
            try:
                code = encode_with_depth_2d(x, y, max_depth)
                codes.append(code)
            except ValueError:
                continue
    return codes


def morton_code_to_binary_string(morton_code: int, bits: int = 32) -> str:
    """
    将Morton码转换为二进制字符串表示。
    
    Args:
        morton_code: Morton编码值
        bits: 显示的位数
        
    Returns:
        二进制字符串
        
    Example:
        >>> morton_code_to_binary_string(5, bits=8)
        '00000101'
    """
    return format(morton_code, f'0{bits}b')


def compare_positions_2d(x1: int, y1: int, x2: int, y2: int) -> int:
    """
    比较两个2D位置的空间顺序（基于Morton码）。
    
    Args:
        x1, y1: 第一个位置
        x2, y2: 第二个位置
        
    Returns:
        -1: 位置1在位置2之前
        0: 位置相同
        1: 位置1在位置2之后
        
    Example:
        >>> compare_positions_2d(0, 0, 1, 0)
        -1
        >>> compare_positions_2d(1, 1, 1, 1)
        0
    """
    m1 = encode_2d(x1, y1)
    m2 = encode_2d(x2, y2)
    
    if m1 < m2:
        return -1
    elif m1 > m2:
        return 1
    return 0


def sort_positions_2d(positions: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
    """
    按Morton码顺序排列2D位置。
    
    Morton排序对于空间局部性优化很有用，
    可以提高缓存命中率和范围查询效率。
    
    Args:
        positions: 位置列表
        
    Returns:
        排序后的位置列表
        
    Example:
        >>> sort_positions_2d([(3, 0), (0, 0), (1, 1)])
        [(0, 0), (3, 0), (1, 1)]
    """
    return sorted(positions, key=lambda p: encode_2d(p[0], p[1]))


def get_morton_distance_2d(morton_code1: int, morton_code2: int) -> int:
    """
    计算两个Morton码之间的"距离"（绝对差）。
    
    注意：这不是真实的几何距离，只是Morton码值的差。
    Morton码差值可以用于快速排序和范围查询。
    
    Args:
        morton_code1: 第一个Morton码
        morton_code2: 第二个Morton码
        
    Returns:
        Morton码差的绝对值
        
    Example:
        >>> get_morton_distance_2d(5, 10)
        5
    """
    return abs(morton_code1 - morton_code2)


def get_quadrant_2d(x: int, y: int, center_x: int, center_y: int) -> int:
    """
    确定点相对于中心点所在的象限。
    
    Args:
        x, y: 点坐标
        center_x, center_y: 中心坐标
        
    Returns:
        象限编号 (0-3):
        - 0: 右下 (x >= cx, y < cy)
        - 1: 左下 (x < cx, y < cy)
        - 2: 右上 (x >= cx, y >= cy)
        - 3: 左上 (x < cx, y >= cy)
        
    Example:
        >>> get_quadrant_2d(5, 5, 10, 10)
        0
        >>> get_quadrant_2d(15, 5, 10, 10)
        0
        >>> get_quadrant_2d(5, 15, 10, 10)
        2
    """
    if x < center_x:
        if y < center_y:
            return 1  # 左下
        else:
            return 3  # 左上
    else:
        if y < center_y:
            return 0  # 右下
        else:
            return 2  # 右上


def morton_code_to_grid_position(morton_code: int, grid_size: int) -> Tuple[int, int]:
    """
    将Morton码转换为网格位置。
    
    Args:
        morton_code: Morton编码值
        grid_size: 网格大小（边长，必须是2的幂）
        
    Returns:
        (行, 列) 元组
        
    Raises:
        ValueError: grid_size不是2的幂
        
    Example:
        >>> morton_code_to_grid_position(0, 4)
        (0, 0)
        >>> morton_code_to_grid_position(3, 4)
        (1, 1)
    """
    if grid_size & (grid_size - 1) != 0:
        raise ValueError(f"网格大小必须是2的幂: {grid_size}")
    
    x, y = decode_2d(morton_code)
    
    # 对网格大小取模
    return (y % grid_size, x % grid_size)


def generate_morton_sequence_2d(count: int) -> Generator[Tuple[int, int], None, None]:
    """
    生成Morton顺序的2D坐标序列。
    
    按Morton码顺序生成坐标，从(0,0)开始。
    
    Args:
        count: 要生成的坐标数量
        
    Yields:
        (x, y) 坐标元组
        
    Example:
        >>> list(generate_morton_sequence_2d(4))
        [(0, 0), (1, 0), (0, 1), (1, 1)]
    """
    for morton_code in range(count):
        yield decode_2d(morton_code)


class MortonEncoder2D:
    """
    2D Morton编码器类。
    
    提供面向对象的Morton编码操作接口。
    
    Example:
        >>> encoder = MortonEncoder2D(depth=10)
        >>> code = encoder.encode(100, 200)
        >>> encoder.decode(code)
        (100, 200)
    """
    
    def __init__(self, depth: int = 16):
        """
        初始化编码器。
        
        Args:
            depth: 深度，决定坐标范围 [0, 2^depth - 1]
        """
        if depth < 1 or depth > 32:
            raise ValueError(f"深度必须在 [1, 32] 范围内: {depth}")
        
        self.depth = depth
        self.max_coord = (1 << depth) - 1
    
    def encode(self, x: int, y: int) -> int:
        """编码2D坐标为Morton码。"""
        return encode_with_depth_2d(x, y, self.depth)
    
    def decode(self, morton_code: int) -> Tuple[int, int]:
        """解码Morton码为2D坐标。"""
        return decode_with_depth_2d(morton_code, self.depth)
    
    def get_neighbors(self, morton_code: int, include_diagonal: bool = True) -> List[int]:
        """获取邻居Morton码。"""
        return get_neighbors_morton_2d(morton_code, include_diagonal)
    
    def get_parent(self, morton_code: int) -> int:
        """获取父级Morton码。"""
        return get_parent_2d(morton_code)
    
    def get_children(self, morton_code: int) -> List[int]:
        """获取子级Morton码列表。"""
        return get_children_2d(morton_code)
    
    def get_range_codes(
        self, 
        x_min: int, y_min: int, 
        x_max: int, y_max: int
    ) -> List[int]:
        """获取矩形范围内的Morton码。"""
        return range_to_morton_codes_2d(x_min, y_min, x_max, y_max, self.depth)
    
    def __repr__(self) -> str:
        return f"MortonEncoder2D(depth={self.depth}, max_coord={self.max_coord})"


class MortonEncoder3D:
    """
    3D Morton编码器类。
    
    提供面向对象的3D Morton编码操作接口。
    
    Example:
        >>> encoder = MortonEncoder3D(depth=8)
        >>> code = encoder.encode(10, 20, 30)
        >>> encoder.decode(code)
        (10, 20, 30)
    """
    
    def __init__(self, depth: int = 10):
        """
        初始化编码器。
        
        Args:
            depth: 深度，决定坐标范围 [0, 2^depth - 1]
        """
        if depth < 1 or depth > 10:
            raise ValueError(f"深度必须在 [1, 10] 范围内: {depth}")
        
        self.depth = depth
        self.max_coord = (1 << depth) - 1
    
    def encode(self, x: int, y: int, z: int) -> int:
        """编码3D坐标为Morton码。"""
        if x < 0 or x > self.max_coord:
            raise ValueError(f"x坐标超出范围 [0, {self.max_coord}]: {x}")
        if y < 0 or y > self.max_coord:
            raise ValueError(f"y坐标超出范围 [0, {self.max_coord}]: {y}")
        if z < 0 or z > self.max_coord:
            raise ValueError(f"z坐标超出范围 [0, {self.max_coord}]: {z}")
        
        return encode_3d(x, y, z)
    
    def decode(self, morton_code: int) -> Tuple[int, int, int]:
        """解码Morton码为3D坐标。"""
        return decode_3d(morton_code)
    
    def __repr__(self) -> str:
        return f"MortonEncoder3D(depth={self.depth}, max_coord={self.max_coord})"


if __name__ == "__main__":
    # 简单演示
    print("Morton Code Utils 演示")
    print("=" * 50)
    
    # 2D编码
    print("\n2D Morton编码:")
    for x in range(2):
        for y in range(2):
            code = encode_2d(x, y)
            print(f"  ({x}, {y}) -> {code}")
    
    # 3D编码
    print("\n3D Morton编码:")
    for x in range(2):
        for y in range(2):
            for z in range(2):
                code = encode_3d(x, y, z)
                print(f"  ({x}, {y}, {z}) -> {code}")
    
    # Morton排序
    print("\nMorton排序示例:")
    positions = [(3, 0), (0, 3), (1, 1), (0, 0), (2, 2)]
    sorted_pos = sort_positions_2d(positions)
    print(f"  原始: {positions}")
    print(f"  排序: {sorted_pos}")
    
    # 使用编码器类
    print("\n使用MortonEncoder2D类:")
    encoder = MortonEncoder2D(depth=10)
    code = encoder.encode(100, 200)
    x, y = encoder.decode(code)
    print(f"  encode(100, 200) = {code}")
    print(f"  decode({code}) = ({x}, {y})")
    print(f"  编码器: {encoder}")