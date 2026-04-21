"""
四元数工具模块 (Quaternion Utilities)

提供完整的四元数操作功能，用于 3D 旋转计算。

主要功能:
- 四元数基本运算（加减乘、共轭、逆、模）
- 旋转操作（轴角、欧拉角、旋转矩阵转换）
- 向量旋转
- 球面线性插值 (SLERP)
- LookRotation（朝向指定方向）
- 随机旋转生成

使用示例:
    from quaternion_utils import Quaternion, from_euler, slerp
    
    # 创建绕 Z 轴旋转 90 度的四元数
    q = Quaternion.from_axis_angle((0, 0, 1), math.pi / 2)
    
    # 旋转向量
    rotated = q.rotate_vector((1, 0, 0))
    
    # 欧拉角转换
    q = from_euler(0.5, 0.3, 0.8, 'XYZ')
    roll, pitch, yaw = q.to_euler_angles()
    
    # 插值
    q_interp = slerp(q1, q2, 0.5)
"""

from .quaternion import (
    Quaternion,
    identity,
    from_axis_angle,
    from_euler,
    from_rotation_matrix,
    from_two_vectors,
    lerp,
    slerp,
    squad,
    angle_between,
    angular_velocity,
    look_rotation,
    random_rotation,
    rotation_x,
    rotation_y,
    rotation_z,
)

__version__ = '1.0.0'
__all__ = [
    'Quaternion',
    'identity',
    'from_axis_angle',
    'from_euler',
    'from_rotation_matrix',
    'from_two_vectors',
    'lerp',
    'slerp',
    'squad',
    'angle_between',
    'angular_velocity',
    'look_rotation',
    'random_rotation',
    'rotation_x',
    'rotation_y',
    'rotation_z',
]