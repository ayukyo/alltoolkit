"""
鞋码转换工具使用示例

展示如何使用 shoe_size_utils 模块进行：
1. 基本鞋码转换
2. 获取所有尺码
3. 根据脚长推荐鞋码
4. 尺码验证和比较
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from shoe_size_utils.mod import (
    ShoeSizeConverter,
    ShoeSize,
    SizeSystem,
    Gender,
    convert_shoe_size,
    get_all_sizes,
    get_foot_length_info,
    recommend_shoe_size,
    validate_shoe_size,
    compare_sizes,
    find_closest_size,
    COMMON_SIZE_CHART
)


def print_separator(title: str = ""):
    """打印分隔线"""
    if title:
        print(f"\n{'='*50}")
        print(f"  {title}")
        print('='*50)
    else:
        print('-' * 50)


def example_basic_conversion():
    """示例1: 基本鞋码转换"""
    print_separator("基本鞋码转换")
    
    # 使用便捷函数
    print("\n📐 欧洲码 42 转换为其他系统:")
    us_men = convert_shoe_size(42, "EU", "US_MEN")
    us_women = convert_shoe_size(42, "EU", "US_WOMEN")
    uk = convert_shoe_size(42, "EU", "UK")
    cn = convert_shoe_size(42, "EU", "CN")
    jp = convert_shoe_size(42, "EU", "JP")
    
    print(f"   EU 42 → US Men: {us_men}")
    print(f"   EU 42 → US Women: {us_women}")
    print(f"   EU 42 → UK: {uk}")
    print(f"   EU 42 → CN (毫米): {cn}")
    print(f"   EU 42 → JP (厘米): {jp}")
    
    # 反向转换
    print("\n📐 美国男码 9 转换为其他系统:")
    eu = convert_shoe_size(9, "US_MEN", "EU")
    uk = convert_shoe_size(9, "US_MEN", "UK")
    print(f"   US Men 9 → EU: {eu}")
    print(f"   US Men 9 → UK: {uk}")


def example_all_sizes():
    """示例2: 获取所有尺码"""
    print_separator("获取所有鞋码系统")
    
    sizes = get_all_sizes(42, "EU")
    
    print(f"\n📊 EU 42 对应的所有尺码:")
    print(f"   脚长: {sizes['cm']} 厘米")
    print(f"   ┌─────────────────────────┐")
    print(f"   │ 欧洲码 (EU):    {sizes['eu']:<8}│")
    print(f"   │ 美国男码 (US):  {sizes['us_men']:<8}│")
    print(f"   │ 美国女码 (US):  {sizes['us_women']:<8}│")
    print(f"   │ 英国码 (UK):    {sizes['uk']:<8}│")
    print(f"   │ 日本码 (JP):    {sizes['jp']:<8}│")
    print(f"   │ 中国码 (CN):    {sizes['cn']:<8}│")
    print(f"   │ 巴西码 (BR):    {sizes['br']:<8}│")
    print(f"   │ 韩国码 (KR):    {sizes['kr']:<8}│")
    print(f"   │ 墨西哥码 (MEX): {sizes['mex']:<8}│")
    print(f"   └─────────────────────────┘")


def example_foot_length():
    """示例3: 根据脚长查询"""
    print_separator("根据脚长查询鞋码")
    
    foot_length = 26.5  # 厘米
    
    print(f"\n📏 脚长 {foot_length} 厘米对应鞋码:")
    sizes = get_foot_length_info(foot_length)
    
    for name, value in sizes.items():
        print(f"   {name}: {value}")


def example_shoe_recommendation():
    """示例4: 购鞋建议"""
    print_separator("购鞋建议")
    
    foot_length = 26.5  # 厘米
    
    shoe_types = ["normal", "running", "sport", "high_heel", "boot"]
    
    print(f"\n👟 脚长 {foot_length} 厘米的购鞋建议:")
    for shoe_type in shoe_types:
        rec = recommend_shoe_size(foot_length, shoe_type)
        print(f"\n   【{shoe_type.upper()}】")
        print(f"   推荐EU码: {rec['推荐EU码']}")
        print(f"   说明: {rec['调整原因']}")


def example_size_validation():
    """示例5: 尺码验证"""
    print_separator("鞋码验证")
    
    test_sizes = [
        (42, "EU"),
        (8.5, "US_MEN"),
        (100, "EU"),    # 无效
        (-5, "UK"),      # 无效
        (265, "CN"),
    ]
    
    print("\n✅ 尺码验证测试:")
    for size, system in test_sizes:
        valid, msg = validate_shoe_size(size, system)
        status = "✓ 有效" if valid else "✗ 无效"
        print(f"   {system} {size}: {status}")
        if msg:
            print(f"         {msg}")


def example_size_comparison():
    """示例6: 尺码比较"""
    print_separator("尺码比较")
    
    comparisons = [
        (42, "EU", 8.5, "US_MEN"),
        (42, "EU", 42.5, "EU"),
        (39, "EU", 8, "UK"),
    ]
    
    print("\n⚖️ 尺码比较:")
    for s1, sys1, s2, sys2 in comparisons:
        result = compare_sizes(s1, sys1, s2, sys2)
        print(f"\n   {sys1} {s1} vs {sys2} {s2}")
        print(f"   {result['comparison']}")
        print(f"   差值: {result['difference_cm']} 厘米")


def example_find_closest():
    """示例7: 查找最接近尺码"""
    print_separator("查找最接近的标准尺码")
    
    foot_lengths = [26.3, 25.8, 27.2]
    
    print("\n🔍 查找最接近的标准尺码:")
    for cm in foot_lengths:
        eu_size, diff = find_closest_size(cm, "EU")
        us_size, _ = find_closest_size(cm, "US_MEN")
        print(f"\n   脚长 {cm} 厘米:")
        print(f"   最接近EU码: {eu_size} (差 {diff} 厘米)")
        print(f"   最接近US男码: {us_size}")


def example_size_chart():
    """示例8: 常用尺码对照表"""
    print_separator("常用鞋码对照表")
    
    print("\n📋 部分常用尺码对照:")
    print(f"   {'EU':<6} {'US Men':<10} {'US Women':<12} {'UK':<6} {'CM':<6} {'CN':<6}")
    print(f"   {'-'*46}")
    
    for entry in COMMON_SIZE_CHART:
        print(f"   {entry['EU']:<6} {entry['US_MEN']:<10} {entry['US_WOMEN']:<12} {entry['UK']:<6} {entry['CM']:<6} {entry['CN']:<6}")


def example_detailed_info():
    """示例9: 详细信息"""
    print_separator("鞋码详细信息")
    
    info = ShoeSizeConverter.get_size_info(42, SizeSystem.EU)
    
    print(f"\n📌 EU 42 详细信息:")
    print(f"\n   原始码: {info['原始码']}")
    print(f"   脚长: {info['脚长']}")
    print(f"   类型: {info['类型']}")
    
    print(f"\n   所有码对照:")
    for name, value in info['所有码'].items():
        print(f"      {name}: {value}")
    
    print(f"\n   购鞋建议:")
    for shoe_type, advice in info['购鞋建议'].items():
        print(f"      {shoe_type}: {advice}")


def example_shoe_size_object():
    """示例10: 鞋码对象"""
    print_separator("鞋码数据结构")
    
    # 创建鞋码对象
    size1 = ShoeSize(42, SizeSystem.EU)
    size2 = ShoeSize(8.5, SizeSystem.US_MEN, Gender.MEN)
    
    print(f"\n📦 鞋码对象:")
    print(f"   {size1}")
    print(f"   {size2}")
    
    print(f"\n   详细属性:")
    print(f"   size1.size = {size1.size}")
    print(f"   size1.system = {size1.system}")
    print(f"   size1.gender = {size1.gender}")
    
    print(f"\n   size2.size = {size2.size}")
    print(f"   size2.system = {size2.system}")
    print(f"   size2.gender = {size2.gender}")


def main():
    """运行所有示例"""
    example_basic_conversion()
    example_all_sizes()
    example_foot_length()
    example_shoe_recommendation()
    example_size_validation()
    example_size_comparison()
    example_find_closest()
    example_size_chart()
    example_detailed_info()
    example_shoe_size_object()
    
    print_separator()
    print("\n✅ 所有示例运行完成!\n")


if __name__ == "__main__":
    main()