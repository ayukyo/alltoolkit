"""
Bitmap Utils 使用示例

演示位图的各种用法：
- 基本操作
- 布隆过滤器模式
- 权限管理
- 集合运算
- 大规模数据处理
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import Bitmap, SparseBitmap, create_bitmap, bitmap_from_string


def example_basic_operations():
    """基本操作示例"""
    print("\n" + "=" * 50)
    print("示例1: 基本位操作")
    print("=" * 50)
    
    # 创建位图
    bm = Bitmap(32)
    print(f"创建32位位图: {bm}")
    
    # 设置位
    bm.set(0)
    bm.set(5)
    bm.set(10)
    bm.set(15)
    print(f"设置位 0, 5, 10, 15: {bm}")
    
    # 清除位
    bm.clear(5)
    print(f"清除位 5: {bm}")
    
    # 翻转位
    bm.flip(0)
    print(f"翻转位 0: {bm}")
    
    # 通过索引操作
    bm[20] = True
    print(f"设置位 20: {bm}")
    
    # 统计
    print(f"设置的位数: {bm.count_set()}")
    print(f"清除的位数: {bm.count_clear()}")
    print(f"第一个设置位: {bm.find_first_set()}")
    print(f"第一个清除位: {bm.find_first_clear()}")


def example_range_operations():
    """范围操作示例"""
    print("\n" + "=" * 50)
    print("示例2: 范围操作")
    print("=" * 50)
    
    bm = Bitmap(64)
    
    # 设置范围
    bm.set_range(10, 20)
    print(f"设置范围 [10, 20): {bm}")
    
    # 清除范围
    bm.set_range(15, 18, False)
    print(f"清除范围 [15, 18): {bm}")
    
    # 翻转范围
    bm.flip_range(10, 15)
    print(f"翻转范围 [10, 15): {bm}")
    
    # 统计范围
    print(f"被设置的位数: {bm.count_set()}")


def example_bitmap_operations():
    """位图运算示例"""
    print("\n" + "=" * 50)
    print("示例3: 位图运算")
    print("=" * 50)
    
    # 创建两个位图
    bm1 = bitmap_from_string("11110000")
    bm2 = bitmap_from_string("11001100")
    
    print(f"位图1: {bm1.to_bit_string()}")
    print(f"位图2: {bm2.to_bit_string()}")
    
    # AND 运算
    and_result = bm1 & bm2
    print(f"AND:  {and_result.to_bit_string()}")
    
    # OR 运算
    or_result = bm1 | bm2
    print(f"OR:   {or_result.to_bit_string()}")
    
    # XOR 运算
    xor_result = bm1 ^ bm2
    print(f"XOR:  {xor_result.to_bit_string()}")
    
    # NOT 运算
    not_result = ~bm1
    print(f"NOT1: {not_result.to_bit_string()}")
    
    # 差集
    diff_result = bm1 - bm2
    print(f"差集: {diff_result.to_bit_string()}")


def example_permission_management():
    """权限管理示例"""
    print("\n" + "=" * 50)
    print("示例4: 权限管理")
    print("=" * 50)
    
    # 定义权限位
    PERMISSIONS = {
        'READ': 0,
        'WRITE': 1,
        'DELETE': 2,
        'ADMIN': 3,
        'EXECUTE': 4,
        'SHARE': 5,
    }
    
    # 创建用户权限
    user_permissions = Bitmap(6)
    
    # 授予权限
    user_permissions.set(PERMISSIONS['READ'])
    user_permissions.set(PERMISSIONS['WRITE'])
    user_permissions.set(PERMISSIONS['EXECUTE'])
    
    print(f"用户权限: {user_permissions}")
    
    # 检查权限
    def has_permission(perm_bitmap, perm_name):
        return perm_bitmap[PERMISSIONS[perm_name]]
    
    print(f"有读取权限: {has_permission(user_permissions, 'READ')}")
    print(f"有删除权限: {has_permission(user_permissions, 'DELETE')}")
    print(f"有管理权限: {has_permission(user_permissions, 'ADMIN')}")
    
    # 创建角色权限模板
    admin_role = create_bitmap(6, [0, 1, 2, 3, 4, 5])  # 所有权限
    viewer_role = create_bitmap(6, [0])  # 只读
    
    # 合并权限
    user_permissions |= viewer_role
    print(f"合并查看角色后: {user_permissions}")
    
    # 检查是否是管理员角色的子集
    print(f"是否是管理员: {user_permissions.is_subset(admin_role)}")


def example_bloom_filter_pattern():
    """布隆过滤器模式示例"""
    print("\n" + "=" * 50)
    print("示例5: 布隆过滤器模式（简化版）")
    print("=" * 50)
    
    # 简化的布隆过滤器演示
    class SimpleBloomFilter:
        def __init__(self, size=1000):
            self.bitmap = Bitmap(size)
            self.size = size
        
        def _hash(self, item, seed):
            """简单哈希函数"""
            h = hash(str(item) + str(seed))
            return abs(h) % self.size
        
        def add(self, item):
            """添加元素"""
            for seed in range(3):  # 使用3个哈希函数
                idx = self._hash(item, seed)
                self.bitmap.set(idx)
        
        def might_contain(self, item):
            """检查可能包含（可能有假阳性）"""
            for seed in range(3):
                idx = self._hash(item, seed)
                if not self.bitmap[idx]:
                    return False
            return True
        
        def count_bits(self):
            """统计设置的位数"""
            return self.bitmap.count_set()
    
    # 创建布隆过滤器
    bf = SimpleBloomFilter(100)
    
    # 添加元素
    items = ["apple", "banana", "cherry"]
    for item in items:
        bf.add(item)
        print(f"添加: {item}")
    
    print(f"\n设置的位数: {bf.count_bits()}")
    
    # 检查元素
    print("\n检查元素:")
    for item in ["apple", "banana", "grape", "orange"]:
        result = bf.might_contain(item)
        status = "可能在" if result else "不在"
        print(f"  {item}: {status}")


def example_set_operations():
    """集合操作示例"""
    print("\n" + "=" * 50)
    print("示例6: 集合操作")
    print("=" * 50)
    
    # 使用位图表示集合
    set_a = create_bitmap(16, [0, 2, 4, 6, 8, 10])
    set_b = create_bitmap(16, [1, 2, 3, 5, 7, 9, 11])
    
    print(f"集合A: {sorted(set_a.to_list())}")
    print(f"集合B: {sorted(set_b.to_list())}")
    
    # 并集
    union = set_a | set_b
    print(f"并集: {sorted(union.to_list())}")
    
    # 交集
    intersection = set_a & set_b
    print(f"交集: {sorted(intersection.to_list())}")
    
    # 差集
    diff = set_a - set_b
    print(f"A-B差集: {sorted(diff.to_list())}")
    
    # 对称差（XOR）
    sym_diff = set_a ^ set_b
    print(f"对称差: {sorted(sym_diff.to_list())}")


def example_large_scale_data():
    """大规模数据处理示例"""
    print("\n" + "=" * 50)
    print("示例7: 大规模数据处理")
    print("=" * 50)
    
    # 创建大位图（100万位 = 125KB）
    large_bm = Bitmap(1_000_000)
    
    # 设置一些位
    for i in range(0, 1_000_000, 1000):
        large_bm.set(i)
    
    print(f"位图大小: {len(large_bm):,} 位")
    print(f"设置的位数: {large_bm.count_set():,}")
    print(f"内存占用: 约 {len(large_bm) // 8:,} 字节")
    
    # 迭代所有设置的位
    first_10 = []
    for i, bit in enumerate(large_bm.iter_set_bits()):
        first_10.append(bit)
        if i >= 9:
            break
    print(f"前10个设置位: {first_10}")
    
    # 序列化
    data = large_bm.to_bytes()
    print(f"序列化后大小: {len(data):,} 字节")
    
    # 反序列化
    restored = Bitmap.from_bytes(data, 1_000_000)
    print(f"反序列化成功: {restored.count_set():,} 位被设置")


def example_sparse_bitmap():
    """稀疏位图示例"""
    print("\n" + "=" * 50)
    print("示例8: 稀疏位图")
    print("=" * 50)
    
    # 创建稀疏位图（100万位，但只设置少量位）
    sparse = SparseBitmap(1_000_000)
    
    # 设置少量位
    positions = [100, 50000, 999999]
    for pos in positions:
        sparse.set(pos)
    
    print(f"位图大小: {len(sparse):,} 位")
    print(f"设置的位数: {sparse.count_set()}")
    print(f"设置的位置: {sorted(sparse.iter_set_bits())}")
    
    # 转换为密集位图
    dense = sparse.to_bitmap()
    print(f"转换为密集位图后: {dense.count_set()} 位被设置")
    
    # 从密集位图转换
    bm = Bitmap(1000)
    bm.set(100)
    bm.set(500)
    sparse2 = SparseBitmap.from_bitmap(bm)
    print(f"从密集位图转换后: {sorted(sparse2.iter_set_bits())}")


def example_feature_flags():
    """功能开关示例"""
    print("\n" + "=" * 50)
    print("示例9: 功能开关管理")
    print("=" * 50)
    
    # 定义功能开关
    FEATURES = {
        'new_ui': 0,
        'dark_mode': 1,
        'analytics': 2,
        'beta_features': 3,
        'notifications': 4,
        'auto_save': 5,
    }
    
    # 创建功能开关配置
    config = Bitmap(6)
    
    # 启用功能
    config.set(FEATURES['new_ui'])
    config.set(FEATURES['dark_mode'])
    config.set(FEATURES['auto_save'])
    
    print("当前启用的功能:")
    for name, bit in FEATURES.items():
        status = "✓ 启用" if config[bit] else "✗ 禁用"
        print(f"  {name}: {status}")
    
    # 导出配置
    config_hex = config.to_hex_string()
    print(f"\n配置导出 (hex): {config_hex}")
    
    # 导入配置
    restored = Bitmap.from_hex_string(config_hex, 6)
    print(f"配置导入后相同: {config == restored}")


def example_run_encoding():
    """游程编码示例"""
    print("\n" + "=" * 50)
    print("示例10: 游程迭代")
    print("=" * 50)
    
    # 创建有连续模式的位图
    bm = bitmap_from_string("111000111100001111")
    
    print(f"位图: {bm.to_bit_string()}")
    print("游程分解:")
    
    for start, end, value in bm.iter_runs():
        run_type = "1" if value else "0"
        length = end - start
        print(f"  位置 [{start:2d}, {end:2d}): {run_type} (长度 {length})")


def example_serialization():
    """序列化示例"""
    print("\n" + "=" * 50)
    print("示例11: 序列化与反序列化")
    print("=" * 50)
    
    # 创建位图
    bm = create_bitmap(32, [0, 7, 15, 23, 31])
    
    print(f"原始位图: {bm.to_bit_string()}")
    
    # 不同序列化格式
    print("\n序列化格式:")
    print(f"  二进制字符串: {bm.to_bit_string()}")
    print(f"  十六进制:     {bm.to_hex_string()}")
    print(f"  整数:         {bm.to_int()}")
    print(f"  字节长度:     {len(bm.to_bytes())} 字节")
    
    # 从不同格式恢复
    bm1 = Bitmap.from_bit_string(bm.to_bit_string())
    bm2 = Bitmap.from_hex_string(bm.to_hex_string(), 32)
    bm3 = Bitmap.from_int(bm.to_int(), 32)
    
    print("\n反序列化验证:")
    print(f"  从二进制恢复: {bm1 == bm}")
    print(f"  从十六进制恢复: {bm2 == bm}")
    print(f"  从整数恢复: {bm3 == bm}")


def example_weekday_tracking():
    """星期追踪示例"""
    print("\n" + "=" * 50)
    print("示例12: 星期追踪")
    print("=" * 50)
    
    DAYS = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
    
    # 工作日
    workdays = create_bitmap(7, [0, 1, 2, 3, 4])
    # 周末
    weekends = create_bitmap(7, [5, 6])
    
    # 某人的工作安排
    schedule = create_bitmap(7, [0, 1, 3, 4, 5])  # 周一、周二、周四、周五、周六工作
    
    print("工作日:", [DAYS[i] for i in workdays.to_list()])
    print("周末:", [DAYS[i] for i in weekends.to_list()])
    print("某人的工作安排:", [DAYS[i] for i in schedule.to_list()])
    
    # 分析
    workday_work = schedule & workdays
    weekend_work = schedule & weekends
    
    print(f"\n工作日工作天数: {workday_work.count_set()}")
    print(f"周末工作天数: {weekend_work.count_set()}")
    
    # 加班天数（周末工作）
    overtime = weekends & schedule
    print(f"加班天数: {sorted(overtime.to_list())}")
    
    # 休息天数（不工作的日）
    rest = ~schedule
    print(f"休息天数: {[DAYS[i] for i in rest.to_list()]}")


def main():
    """运行所有示例"""
    print()
    print("╔" + "═" * 48 + "╗")
    print("║" + " Bitmap Utils 使用示例 ".center(48) + "║")
    print("╚" + "═" * 48 + "╝")
    
    example_basic_operations()
    example_range_operations()
    example_bitmap_operations()
    example_permission_management()
    example_bloom_filter_pattern()
    example_set_operations()
    example_large_scale_data()
    example_sparse_bitmap()
    example_feature_flags()
    example_run_encoding()
    example_serialization()
    example_weekday_tracking()
    
    print("\n" + "=" * 50)
    print("所有示例运行完成!")
    print("=" * 50 + "\n")


if __name__ == "__main__":
    main()