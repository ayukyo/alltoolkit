"""
四元数工具模块测试

测试覆盖:
- 基本运算（加减乘除、共轭、逆、模）
- 旋转操作（向量旋转、轴角转换、欧拉角转换）
- 插值（线性插值、球面插值）
- 工具函数（角度计算、LookRotation、随机旋转）
"""

import math
import unittest
import sys
import os

# 添加父目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from quaternion_utils.quaternion import (
    Quaternion, identity, from_axis_angle, from_euler, from_rotation_matrix,
    from_two_vectors, lerp, slerp, squad, angle_between, angular_velocity,
    look_rotation, random_rotation, rotation_x, rotation_y, rotation_z
)


class TestQuaternionBasics(unittest.TestCase):
    """测试四元数基本功能"""
    
    def test_identity(self):
        """测试单位四元数"""
        q = identity()
        self.assertAlmostEqual(q.w, 1.0)
        self.assertAlmostEqual(q.x, 0.0)
        self.assertAlmostEqual(q.y, 0.0)
        self.assertAlmostEqual(q.z, 0.0)
        self.assertTrue(q.is_unit())
    
    def test_creation(self):
        """测试四元数创建"""
        q = Quaternion(1, 2, 3, 4)
        self.assertEqual(q.w, 1)
        self.assertEqual(q.x, 2)
        self.assertEqual(q.y, 3)
        self.assertEqual(q.z, 4)
    
    def test_magnitude(self):
        """测试模长计算"""
        q = Quaternion(1, 2, 2, 0)
        self.assertAlmostEqual(q.magnitude(), 3.0)
        
        # 单位四元数模长为1
        q2 = rotation_x(math.pi / 4)
        self.assertAlmostEqual(q2.magnitude(), 1.0)
    
    def test_normalize(self):
        """测试归一化"""
        q = Quaternion(2, 0, 0, 0)
        q_norm = q.normalize()
        self.assertAlmostEqual(q_norm.w, 1.0)
        self.assertAlmostEqual(q_norm.x, 0.0)
        self.assertTrue(q_norm.is_unit())
    
    def test_conjugate(self):
        """测试共轭"""
        q = Quaternion(1, 2, 3, 4)
        conj = q.conjugate()
        self.assertEqual(conj.w, 1)
        self.assertEqual(conj.x, -2)
        self.assertEqual(conj.y, -3)
        self.assertEqual(conj.z, -4)
    
    def test_inverse(self):
        """测试逆四元数"""
        q = Quaternion(1, 1, 1, 1)
        inv = q.inverse()
        # q * q^(-1) 应该是单位四元数
        result = q * inv
        self.assertAlmostEqual(result.w, 1.0, places=6)
        self.assertAlmostEqual(result.x, 0.0, places=6)
        self.assertAlmostEqual(result.y, 0.0, places=6)
        self.assertAlmostEqual(result.z, 0.0, places=6)
    
    def test_inverse_unit_quaternion(self):
        """测试单位四元数的逆等于共轭"""
        q = rotation_x(0.5)
        inv = q.inverse()
        conj = q.conjugate()
        self.assertAlmostEqual(inv.w, conj.w)
        self.assertAlmostEqual(inv.x, conj.x)
        self.assertAlmostEqual(inv.y, conj.y)
        self.assertAlmostEqual(inv.z, conj.z)
    
    def test_addition(self):
        """测试加法"""
        q1 = Quaternion(1, 2, 3, 4)
        q2 = Quaternion(5, 6, 7, 8)
        result = q1 + q2
        self.assertEqual(result.w, 6)
        self.assertEqual(result.x, 8)
        self.assertEqual(result.y, 10)
        self.assertEqual(result.z, 12)
    
    def test_subtraction(self):
        """测试减法"""
        q1 = Quaternion(5, 6, 7, 8)
        q2 = Quaternion(1, 2, 3, 4)
        result = q1 - q2
        self.assertEqual(result.w, 4)
        self.assertEqual(result.x, 4)
        self.assertEqual(result.y, 4)
        self.assertEqual(result.z, 4)
    
    def test_scalar_multiplication(self):
        """测试标量乘法"""
        q = Quaternion(1, 2, 3, 4)
        result = q * 2
        self.assertEqual(result.w, 2)
        self.assertEqual(result.x, 4)
        self.assertEqual(result.y, 6)
        self.assertEqual(result.z, 8)
        
        # 测试右乘
        result2 = 3 * q
        self.assertEqual(result2.w, 3)
        self.assertEqual(result2.x, 6)
    
    def test_quaternion_multiplication(self):
        """测试四元数乘法（Hamilton 乘积）"""
        q1 = Quaternion(1, 2, 3, 4)
        q2 = Quaternion(5, 6, 7, 8)
        result = q1 * q2
        
        # Hamilton 乘积正确计算
        # w = w1*w2 - x1*x2 - y1*y2 - z1*z2 = 1*5 - 2*6 - 3*7 - 4*8 = -60
        # x = w1*x2 + x1*w2 + y1*z2 - z1*y2 = 1*6 + 2*5 + 3*8 - 4*7 = 12
        # y = w1*y2 - x1*z2 + y1*w2 + z1*x2 = 1*7 - 2*8 + 3*5 + 4*6 = 30
        # z = w1*z2 + x1*y2 - y1*x2 + z1*w2 = 1*8 + 2*7 - 3*6 + 4*5 = 24
        self.assertEqual(result.w, -60)
        self.assertEqual(result.x, 12)
        self.assertEqual(result.y, 30)
        self.assertEqual(result.z, 24)
    
    def test_scalar_division(self):
        """测试标量除法"""
        q = Quaternion(2, 4, 6, 8)
        result = q / 2
        self.assertEqual(result.w, 1)
        self.assertEqual(result.x, 2)
        self.assertEqual(result.y, 3)
        self.assertEqual(result.z, 4)
    
    def test_negation(self):
        """测试取负"""
        q = Quaternion(1, 2, 3, 4)
        result = -q
        self.assertEqual(result.w, -1)
        self.assertEqual(result.x, -2)
        self.assertEqual(result.y, -3)
        self.assertEqual(result.z, -4)
    
    def test_equality(self):
        """测试相等比较"""
        q1 = Quaternion(1, 2, 3, 4)
        q2 = Quaternion(1, 2, 3, 4)
        q3 = Quaternion(1, 2, 3, 5)
        
        self.assertEqual(q1, q2)
        self.assertNotEqual(q1, q3)
    
    def test_dot_product(self):
        """测试点积"""
        q1 = Quaternion(1, 0, 0, 0)
        q2 = Quaternion(0.707, 0.707, 0, 0)
        dot = q1.dot(q2)
        self.assertAlmostEqual(dot, 0.707, places=3)


class TestRotation(unittest.TestCase):
    """测试旋转相关功能"""
    
    def test_axis_angle_conversion(self):
        """测试轴角转换"""
        # 绕 Z 轴旋转 90 度
        axis = (0, 0, 1)
        angle = math.pi / 2
        q = from_axis_angle(axis, angle)
        
        # 转换回轴角
        axis2, angle2 = q.to_axis_angle()
        
        self.assertAlmostEqual(axis2[2], 1.0, places=5)  # Z轴
        self.assertAlmostEqual(angle2, angle, places=5)
    
    def test_euler_angles_xyz(self):
        """测试欧拉角转换（XYZ顺序）"""
        roll, pitch, yaw = 0.5, 0.3, 0.8
        q = from_euler(roll, pitch, yaw, 'XYZ')
        
        # 转换回欧拉角
        roll2, pitch2, yaw2 = q.to_euler_angles('XYZ')
        
        self.assertAlmostEqual(roll, roll2, places=5)
        self.assertAlmostEqual(pitch, pitch2, places=5)
        self.assertAlmostEqual(yaw, yaw2, places=5)
    
    def test_euler_angles_zyx(self):
        """测试欧拉角转换（ZYX顺序）"""
        roll, pitch, yaw = 0.5, 0.3, 0.8
        q = from_euler(roll, pitch, yaw, 'ZYX')
        
        roll2, pitch2, yaw2 = q.to_euler_angles('ZYX')
        
        self.assertAlmostEqual(roll, roll2, places=5)
        self.assertAlmostEqual(pitch, pitch2, places=5)
        self.assertAlmostEqual(yaw, yaw2, places=5)
    
    def test_rotate_vector_simple(self):
        """测试简单向量旋转"""
        # 绕 Z 轴旋转 90 度
        q = rotation_z(math.pi / 2)
        
        # 旋转 X 轴向量
        v = (1, 0, 0)
        rotated = q.rotate_vector(v)
        
        # 应该得到 Y 轴方向
        self.assertAlmostEqual(rotated[0], 0.0, places=5)
        self.assertAlmostEqual(rotated[1], 1.0, places=5)
        self.assertAlmostEqual(rotated[2], 0.0, places=5)
    
    def test_rotate_vector_complex(self):
        """测试复杂向量旋转"""
        # 先绕 X 转 90 度，再绕 Y 转 90 度
        q = rotation_y(math.pi / 2) * rotation_x(math.pi / 2)
        
        v = (0, 0, 1)  # Z 轴
        rotated = q.rotate_vector(v)
        
        # 验证旋转结果
        self.assertAlmostEqual(abs(rotated[1]), 1.0, places=5)  # 应该在 Y 方向
    
    def test_rotation_matrix_conversion(self):
        """测试旋转矩阵转换"""
        # 创建一个四元数
        q = from_euler(0.3, 0.5, 0.7)
        
        # 转换为矩阵
        matrix = q.to_rotation_matrix()
        
        # 转换回来
        q2 = from_rotation_matrix(matrix)
        
        # 四元数 q 和 -q 表示相同旋转
        self.assertTrue(
            (q - q2).magnitude() < 0.001 or (q + q2).magnitude() < 0.001
        )
    
    def test_rotation_x(self):
        """测试 X 轴旋转"""
        q = rotation_x(math.pi / 4)
        self.assertTrue(q.is_unit())
        
        # 绕 X 轴旋转不应该改变 X 轴向量
        v = (1, 0, 0)
        rotated = q.rotate_vector(v)
        self.assertAlmostEqual(rotated[0], 1.0, places=5)
        self.assertAlmostEqual(rotated[1], 0.0, places=5)
        self.assertAlmostEqual(rotated[2], 0.0, places=5)
    
    def test_rotation_y(self):
        """测试 Y 轴旋转"""
        q = rotation_y(math.pi / 4)
        self.assertTrue(q.is_unit())
    
    def test_rotation_z(self):
        """测试 Z 轴旋转"""
        q = rotation_z(math.pi / 4)
        self.assertTrue(q.is_unit())
    
    def test_from_two_vectors(self):
        """测试从两向量创建旋转"""
        # 将 X 轴旋转到 Y 轴
        q = from_two_vectors((1, 0, 0), (0, 1, 0))
        
        v = (1, 0, 0)
        rotated = q.rotate_vector(v)
        
        self.assertAlmostEqual(rotated[0], 0.0, places=5)
        self.assertAlmostEqual(rotated[1], 1.0, places=5)
        self.assertAlmostEqual(rotated[2], 0.0, places=5)
    
    def test_from_two_vectors_parallel(self):
        """测试相同向量的旋转"""
        q = from_two_vectors((1, 0, 0), (1, 0, 0))
        
        # 应该是单位四元数
        self.assertTrue(q.is_unit())
        self.assertAlmostEqual(abs(q.w), 1.0, places=5)
    
    def test_from_two_vectors_opposite(self):
        """测试相反向量的旋转"""
        q = from_two_vectors((1, 0, 0), (-1, 0, 0))
        
        v = (1, 0, 0)
        rotated = q.rotate_vector(v)
        
        # 应该旋转180度
        self.assertAlmostEqual(rotated[0], -1.0, places=5)


class TestInterpolation(unittest.TestCase):
    """测试插值功能"""
    
    def test_lerp(self):
        """测试线性插值"""
        q1 = identity()
        q2 = rotation_z(math.pi / 2)
        
        # 中点
        q_mid = lerp(q1, q2, 0.5)
        self.assertTrue(q_mid.is_unit())
        
        # 起点和终点
        q_start = lerp(q1, q2, 0.0)
        q_end = lerp(q1, q2, 1.0)
        
        self.assertAlmostEqual(q_start.w, 1.0, places=5)
        # q_end 应该接近 q2
    
    def test_slerp(self):
        """测试球面线性插值"""
        q1 = identity()
        q2 = rotation_z(math.pi / 2)
        
        # 中点应该旋转45度
        q_mid = slerp(q1, q2, 0.5)
        
        # 验证角度
        angle = angle_between(q1, q_mid)
        expected_angle = math.pi / 4
        self.assertAlmostEqual(angle, expected_angle, places=5)
    
    def test_slerp_endpoints(self):
        """测试 slerp 端点"""
        q1 = identity()
        q2 = rotation_x(0.8)
        
        q_start = slerp(q1, q2, 0.0)
        q_end = slerp(q1, q2, 1.0)
        
        self.assertAlmostEqual((q1 - q_start).magnitude(), 0.0, places=5)
        self.assertAlmostEqual((q2 - q_end).magnitude(), 0.0, places=5)
    
    def test_slerp_shortest_path(self):
        """测试最短路径插值"""
        q1 = identity()
        # 一个接近-identity的四元数
        q2 = Quaternion(0.99, 0.1, 0, 0).normalize()
        
        # 不使用最短路径可能会走远路
        q_shortest = slerp(q1, q2, 0.5, shortest_path=True)
        
        self.assertTrue(q_shortest.is_unit())
    
    def test_slerp_opposite_quaternions(self):
        """测试对极四元数的 slerp"""
        # 对极四元数（表示相同旋转但符号相反）
        q1 = identity()
        q2 = -identity()
        
        # 应该不会崩溃
        q_mid = slerp(q1, q2, 0.5)
        self.assertTrue(q_mid.is_unit())


class TestUtilityFunctions(unittest.TestCase):
    """测试工具函数"""
    
    def test_angle_between(self):
        """测试四元数间角度计算"""
        q1 = identity()
        q2 = rotation_x(math.pi / 4)
        
        angle = angle_between(q1, q2)
        self.assertAlmostEqual(angle, math.pi / 4, places=5)
    
    def test_angular_velocity(self):
        """测试角速度计算"""
        q1 = identity()
        q2 = rotation_z(math.pi)  # 绕Z轴转180度
        dt = 1.0  # 1秒
        
        wx, wy, wz = angular_velocity(q1, q2, dt)
        
        # 应该是绕Z轴的角速度
        self.assertAlmostEqual(wx, 0.0, places=5)
        self.assertAlmostEqual(wy, 0.0, places=5)
        self.assertAlmostEqual(abs(wz), math.pi, places=5)
    
    def test_look_rotation(self):
        """测试 LookRotation"""
        # 看向 Z 轴正方向
        q = look_rotation((0, 0, 1))
        self.assertTrue(q.is_unit())
        
        # 验证：Z轴向量旋转后应该指向(0,0,1)
        # (默认forward方向取决于实现)
    
    def test_look_rotation_with_up(self):
        """测试带 up 向量的 LookRotation"""
        q = look_rotation((1, 0, 0), (0, 1, 0))
        self.assertTrue(q.is_unit())
    
    def test_random_rotation(self):
        """测试随机旋转"""
        # 生成多个随机四元数，验证都是单位四元数
        for _ in range(10):
            q = random_rotation()
            self.assertTrue(q.is_unit())
    
    def test_rotation_composition(self):
        """测试旋转组合"""
        # 两个90度旋转应该等于一个180度旋转
        q1 = rotation_z(math.pi / 2)
        q2 = rotation_z(math.pi / 2)
        
        q_combined = q2 * q1  # 注意顺序
        q_180 = rotation_z(math.pi)
        
        # 检查旋转效果
        v = (1, 0, 0)
        r1 = q_combined.rotate_vector(v)
        r2 = q_180.rotate_vector(v)
        
        self.assertAlmostEqual(r1[0], r2[0], places=5)
        self.assertAlmostEqual(r1[1], r2[1], places=5)
        self.assertAlmostEqual(r1[2], r2[2], places=5)


class TestEdgeCases(unittest.TestCase):
    """测试边界情况"""
    
    def test_zero_magnitude_inverse(self):
        """测试零四元数求逆"""
        q = Quaternion(0, 0, 0, 0)
        with self.assertRaises(ValueError):
            q.inverse()
    
    def test_zero_magnitude_normalize(self):
        """测试零四元数归一化"""
        q = Quaternion(0, 0, 0, 0)
        with self.assertRaises(ValueError):
            q.normalize()
    
    def test_invalid_t_value(self):
        """测试无效插值参数"""
        q1 = identity()
        q2 = rotation_x(1.0)
        
        with self.assertRaises(ValueError):
            lerp(q1, q2, -0.5)
        
        with self.assertRaises(ValueError):
            lerp(q1, q2, 1.5)
    
    def test_gimbal_lock_euler(self):
        """测试万向节锁情况的欧拉角转换"""
        # 俯仰角接近90度时可能发生万向节锁
        q = from_euler(0.5, math.pi / 2 - 0.001, 0.3)
        
        # 应该能转换回来，可能有一定误差
        r, p, y = q.to_euler_angles()
        
        # 由于万向节锁，可能不能精确恢复，但不应该崩溃
        self.assertIsInstance(r, float)
        self.assertIsInstance(p, float)
        self.assertIsInstance(y, float)
    
    def test_invalid_rotation_order(self):
        """测试无效的旋转顺序"""
        with self.assertRaises(ValueError):
            from_euler(0.1, 0.2, 0.3, 'ABC')
    
    def test_to_tuple_and_list(self):
        """测试元组和列表转换"""
        q = Quaternion(1, 2, 3, 4)
        
        t = q.to_tuple()
        self.assertEqual(t, (1, 2, 3, 4))
        
        l = q.to_list()
        self.assertEqual(l, [1, 2, 3, 4])
    
    def test_string_representation(self):
        """测试字符串表示"""
        q = Quaternion(1, 0, 0, 0)
        s = str(q)
        self.assertIn('1', s)
        
        q2 = Quaternion(1, 2, 3, 4)
        r = repr(q2)
        self.assertIn('Quaternion', r)


class TestNumericalStability(unittest.TestCase):
    """测试数值稳定性"""
    
    def test_small_angle_rotation(self):
        """测试小角度旋转"""
        q = rotation_x(1e-10)
        self.assertTrue(q.is_unit())
        
        v = (1, 0, 0)
        rotated = q.rotate_vector(v)
        
        self.assertAlmostEqual(rotated[0], 1.0, places=5)
    
    def test_large_angle_rotation(self):
        """测试大角度旋转"""
        q = rotation_z(100 * math.pi)  # 多圈
        self.assertTrue(q.is_unit())
        
        # 旋转多圈应该等效于不旋转
        v = (1, 0, 0)
        rotated = q.rotate_vector(v)
        
        self.assertAlmostEqual(rotated[0], 1.0, places=5)
        self.assertAlmostEqual(rotated[1], 0.0, places=5)
    
    def test_nearly_parallel_vectors(self):
        """测试接近平行的向量"""
        q = from_two_vectors(
            (1, 0, 0),
            (1, 1e-10, 0)
        )
        self.assertTrue(q.is_unit())


if __name__ == '__main__':
    unittest.main(verbosity=2)