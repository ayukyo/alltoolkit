"""
四元数工具模块示例

演示四元数的各种用途：
1. 基本旋转操作
2. 向量旋转
3. 插值动画
4. 欧拉角转换
5. 相机 LookRotation
"""

import math
from quaternion_utils import (
    Quaternion, identity, from_axis_angle, from_euler, from_two_vectors,
    lerp, slerp, angle_between, look_rotation, random_rotation,
    rotation_x, rotation_y, rotation_z
)


def example_basic_rotation():
    """基本旋转示例"""
    print("=" * 50)
    print("示例 1: 基本旋转")
    print("=" * 50)
    
    # 绕 Z 轴旋转 90 度
    angle = math.pi / 2
    q = rotation_z(angle)
    
    print(f"四元数: {q}")
    print(f"是否单位四元数: {q.is_unit()}")
    
    # 旋转 X 轴向量
    v = (1, 0, 0)
    rotated = q.rotate_vector(v)
    print(f"\n旋转 {math.degrees(angle):.1f}° 后:")
    print(f"  原向量: {v}")
    print(f"  旋转后: ({rotated[0]:.4f}, {rotated[1]:.4f}, {rotated[2]:.4f})")
    
    # 转换为轴角
    axis, angle_out = q.to_axis_angle()
    print(f"\n轴角表示:")
    print(f"  轴: ({axis[0]:.4f}, {axis[1]:.4f}, {axis[2]:.4f})")
    print(f"  角度: {math.degrees(angle_out):.1f}°")


def example_euler_angles():
    """欧拉角转换示例"""
    print("\n" + "=" * 50)
    print("示例 2: 欧拉角转换")
    print("=" * 50)
    
    # 创建欧拉角（度）
    roll_deg = 30   # 绕 X 轴
    pitch_deg = 45  # 绕 Y 轴
    yaw_deg = 60    # 绕 Z 轴
    
    # 转换为弧度
    roll = math.radians(roll_deg)
    pitch = math.radians(pitch_deg)
    yaw = math.radians(yaw_deg)
    
    # 创建四元数
    q = from_euler(roll, pitch, yaw, 'XYZ')
    print(f"欧拉角: roll={roll_deg}°, pitch={pitch_deg}°, yaw={yaw_deg}°")
    print(f"四元数: {q}")
    
    # 转换回欧拉角
    roll2, pitch2, yaw2 = q.to_euler_angles('XYZ')
    print(f"\n转换回欧拉角:")
    print(f"  roll: {math.degrees(roll2):.2f}°")
    print(f"  pitch: {math.degrees(pitch2):.2f}°")
    print(f"  yaw: {math.degrees(yaw2):.2f}°")
    
    # 转换为旋转矩阵
    matrix = q.to_rotation_matrix()
    print(f"\n旋转矩阵:")
    for row in matrix:
        print(f"  [{row[0]:7.4f}, {row[1]:7.4f}, {row[2]:7.4f}]")


def example_interpolation():
    """插值示例 - 动画"""
    print("\n" + "=" * 50)
    print("示例 3: 插值动画")
    print("=" * 50)
    
    # 起始和结束姿态
    q_start = identity()
    q_end = rotation_z(math.pi)  # 180度
    
    print("从无旋转到绕 Z 轴旋转 180° 的插值:")
    print("\nt值\t角度(°)\t\t旋转后的向量 (1,0,0)")
    print("-" * 50)
    
    v = (1, 0, 0)
    for t in [0.0, 0.25, 0.5, 0.75, 1.0]:
        q = slerp(q_start, q_end, t)
        rotated = q.rotate_vector(v)
        angle = angle_between(q_start, q)
        print(f"{t:.2f}\t{math.degrees(angle):6.1f}°\t\t({rotated[0]:6.3f}, {rotated[1]:6.3f}, {rotated[2]:6.3f})")


def example_look_rotation():
    """LookRotation 示例 - 相机朝向"""
    print("\n" + "=" * 50)
    print("示例 4: 相机 LookRotation")
    print("=" * 50)
    
    # 目标方向
    targets = [
        ("正前方 (Z+)", (0, 0, 1)),
        ("右边 (X+)", (1, 0, 0)),
        ("上方 (Y+)", (0, 1, 0)),
        ("斜上方", (1, 1, 1)),
    ]
    
    print("不同朝向的四元数:")
    for name, direction in targets:
        q = look_rotation(direction)
        euler = q.to_euler_angles('XYZ')
        print(f"\n{name}: 方向 {direction}")
        print(f"  四元数: w={q.w:.4f}, x={q.x:.4f}, y={q.y:.4f}, z={q.z:.4f}")
        print(f"  欧拉角: roll={math.degrees(euler[0]):.1f}°, pitch={math.degrees(euler[1]):.1f}°, yaw={math.degrees(euler[2]):.1f}°")


def example_rotation_composition():
    """旋转组合示例"""
    print("\n" + "=" * 50)
    print("示例 5: 旋转组合")
    print("=" * 50)
    
    # 先绕 X 转 90°，再绕 Y 转 90°
    q1 = rotation_x(math.pi / 2)
    q2 = rotation_y(math.pi / 2)
    
    # 组合旋转（注意顺序：先 q1 后 q2，写成 q2 * q1）
    q_combined = q2 * q1
    
    print("旋转组合:")
    print(f"  q1 (X轴 90°): {q1}")
    print(f"  q2 (Y轴 90°): {q2}")
    print(f"  q_combined:   {q_combined}")
    
    # 验证：旋转向量
    v = (1, 0, 0)
    
    # 方法1：分别旋转
    v_step1 = q1.rotate_vector(v)
    v_step2 = q2.rotate_vector(v_step1)
    
    # 方法2：组合旋转
    v_direct = q_combined.rotate_vector(v)
    
    print(f"\n验证:")
    print(f"  原向量: {v}")
    print(f"  分步旋转: ({v_step2[0]:.4f}, {v_step2[1]:.4f}, {v_step2[2]:.4f})")
    print(f"  组合旋转: ({v_direct[0]:.4f}, {v_direct[1]:.4f}, {v_direct[2]:.4f})")


def example_two_vectors():
    """从两向量创建旋转示例"""
    print("\n" + "=" * 50)
    print("示例 6: 从两向量创建旋转")
    print("=" * 50)
    
    cases = [
        ("X轴 → Y轴", (1, 0, 0), (0, 1, 0)),
        ("Y轴 → Z轴", (0, 1, 0), (0, 0, 1)),
        ("对角线", (1, 0, 0), (1, 1, 0)),
    ]
    
    for name, v1, v2 in cases:
        q = from_two_vectors(v1, v2)
        rotated = q.rotate_vector(v1)
        
        # 计算角度
        angle = angle_between(identity(), q)
        
        print(f"\n{name}:")
        print(f"  原向量: {v1}")
        print(f"  目标向量: {v2}")
        print(f"  旋转后: ({rotated[0]:.4f}, {rotated[1]:.4f}, {rotated[2]:.4f})")
        print(f"  旋转角度: {math.degrees(angle):.1f}°")


def example_random_rotations():
    """随机旋转示例"""
    print("\n" + "=" * 50)
    print("示例 7: 随机旋转")
    print("=" * 50)
    
    print("生成 5 个随机均匀分布的旋转:")
    for i in range(5):
        q = random_rotation()
        euler = q.to_euler_angles('XYZ')
        print(f"\n随机旋转 {i+1}:")
        print(f"  四元数: w={q.w:.4f}, x={q.x:.4f}, y={q.y:.4f}, z={q.z:.4f}")
        print(f"  欧拉角: ({math.degrees(euler[0]):.1f}°, {math.degrees(euler[1]):.1f}°, {math.degrees(euler[2]):.1f}°)")


def example_gimbal_comparison():
    """对比四元数与欧拉角的优势"""
    print("\n" + "=" * 50)
    print("示例 8: 四元数 vs 欧拉角")
    print("=" * 50)
    
    print("四元数的优势:")
    print("1. 无万向节锁 (Gimbal Lock)")
    print("2. 插值平滑")
    print("3. 组合简单")
    print("4. 数值稳定")
    
    # 演示：90度俯仰角（接近万向节锁）
    pitch_90 = math.pi / 2 - 0.01  # 略小于 90 度
    q = from_euler(0.3, pitch_90, 0.5)
    
    print(f"\n俯仰角接近 90° 时:")
    print(f"  输入: roll=17.2°, pitch=89.4°, yaw=28.6°")
    
    euler_out = q.to_euler_angles()
    print(f"  输出: roll={math.degrees(euler_out[0]):.1f}°, pitch={math.degrees(euler_out[1]):.1f}°, yaw={math.degrees(euler_out[2]):.1f}°")
    print("  (欧拉角可能有翻转，但四元数本身完全有效)")


if __name__ == '__main__':
    example_basic_rotation()
    example_euler_angles()
    example_interpolation()
    example_look_rotation()
    example_rotation_composition()
    example_two_vectors()
    example_random_rotations()
    example_gimbal_comparison()
    
    print("\n" + "=" * 50)
    print("所有示例完成!")
    print("=" * 50)