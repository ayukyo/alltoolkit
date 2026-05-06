"""
Storage Unit Utils - 使用示例

展示存储单位转换工具的各种使用场景
"""

from storage_unit_utils.mod import (
    convert, to_bytes, from_bytes,
    format_size, format_bits, smart_format,
    parse_size, parse_to_bytes,
    ratio, percentage, progress_bar,
    compare, add, subtract,
    human_readable, find_largest_unit, find_smallest_unit,
    total_size, speed_format, bandwidth_format, estimate_time,
    kb, mb, gb, tb, kib, mib, gib, tib,
    StorageUnit
)


def example_basic_conversion():
    """基本转换示例"""
    print("=" * 50)
    print("基本转换示例")
    print("=" * 50)
    
    # 十进制转换（SI 单位，1000 为基数）
    print("\n十进制转换（SI）：")
    print(f"1 KB = {convert(1, 'KB', 'B')} Bytes")
    print(f"1 MB = {convert(1, 'MB', 'KB')} KB")
    print(f"1 GB = {convert(1, 'GB', 'MB')} MB")
    print(f"1024 MB = {convert(1024, 'MB', 'GB')} GB")
    
    # 二进制转换（IEC 单位，1024 为基数）
    print("\n二进制转换（IEC）：")
    print(f"1 KiB = {convert(1, 'KiB', 'B')} Bytes")
    print(f"1 MiB = {convert(1, 'MiB', 'KiB')} KiB")
    print(f"1 GiB = {convert(1, 'GiB', 'MiB')} MiB")
    print(f"1024 MiB = {convert(1024, 'MiB', 'GiB')} GiB")
    
    # 比特与字节转换
    print("\n比特与字节转换：")
    print(f"8 bits = {convert(8, 'bit', 'B')} Bytes")
    print(f"1 Byte = {convert(1, 'B', 'bit')} bits")
    print(f"1 Kbit = {convert(1, 'Kbit', 'bit')} bits")


def example_formatting():
    """格式化示例"""
    print("\n" + "=" * 50)
    print("格式化示例")
    print("=" * 50)
    
    sizes = [
        0,
        100,
        1024,
        1536,
        1_048_576,
        1_500_000,
        1_073_741_824,
        1_500_000_000,
        1_099_511_627_776,
    ]
    
    print("\n数值 -> 十进制格式 -> 二进制格式")
    print("-" * 60)
    for size in sizes:
        decimal = format_size(size, binary=False)
        binary = format_size(size, binary=True)
        print(f"{size:>20} -> {decimal:>15} -> {binary:>15}")
    
    # 比特格式化
    print("\n比特格式化：")
    bits = [100, 1000, 1_000_000, 1_000_000_000]
    for b in bits:
        print(f"{b:>12} bits = {format_bits(b)}")


def example_parsing():
    """解析示例"""
    print("\n" + "=" * 50)
    print("解析示例")
    print("=" * 50)
    
    inputs = [
        "1KB",
        "1 KiB",
        "1.5GB",
        "2.5 TiB",
        "1024",
        "500MB",
        "1,000KB",
    ]
    
    print("\n解析存储大小字符串：")
    for s in inputs:
        try:
            value, unit = parse_size(s)
            bytes_val = parse_to_bytes(s)
            print(f"  '{s}' -> {value} {unit.value[0]} = {bytes_val:,} Bytes")
        except ValueError as e:
            print(f"  '{s}' -> 错误: {e}")


def example_progress():
    """进度条示例"""
    print("\n" + "=" * 50)
    print("进度条示例")
    print("=" * 50)
    
    print("\n存储进度可视化：")
    
    # 不同进度
    for used, total in [(0, 1000), (250, 1000), (500, 1000), (750, 1000), (1000, 1000)]:
        print(progress_bar(used * 1_000_000, total * 1_000_000, width=30))
    
    print("\n二进制单位进度：")
    for used, total in [(256, 1024), (512, 1024), (768, 1024), (1024, 1024)]:
        print(progress_bar(used * 1024 * 1024, total * 1024 * 1024, binary=True, width=20))
    
    print("\n自定义样式：")
    print(progress_bar(65, 100, width=20, filled="▓", empty="░", binary=True))
    print(progress_bar(30, 100, width=20, filled="█", empty=" "))
    print(progress_bar(80, 100, width=20, filled="●", empty="○"))


def example_comparison_calculation():
    """比较和计算示例"""
    print("\n" + "=" * 50)
    print("比较和计算示例")
    print("=" * 50)
    
    # 比较
    print("\n大小比较：")
    pairs = [
        ("1GB", "500MB"),
        ("1024MB", "1GB"),
        ("1GiB", "1GB"),
        ("1TiB", "1TB"),
    ]
    for a, b in pairs:
        result = compare(a, b)
        symbol = ">" if result > 0 else "<" if result < 0 else "="
        print(f"  {a} {symbol} {b}")
    
    # 加法
    print("\n大小相加：")
    print(f"  1GB + 500MB = {format_size(add('1GB', '500MB'))}")
    print(f"  1.5GB + 500MB + 100MB = {format_size(add('1.5GB', '500MB', '100MB'))}")
    print(f"  1KiB + 1KiB = {format_size(add('1KiB', '1KiB'), binary=True)}")
    
    # 减法
    print("\n大小相减：")
    print(f"  2GB - 500MB = {format_size(subtract('2GB', '500MB'))}")
    print(f"  1GiB - 512MiB = {format_size(subtract('1GiB', '512MiB'), binary=True)}")
    
    # 比例和百分比
    print("\n比例和百分比：")
    print(f"  500MB / 1GB = {ratio(500_000_000, 1_000_000_000):.2%}")
    print(f"  768MiB / 1GiB = {percentage(768 * 1024 * 1024, 1024 * 1024 * 1024)}")


def example_finding_extremes():
    """查找极值示例"""
    print("\n" + "=" * 50)
    print("查找极值示例")
    print("=" * 50)
    
    sizes = ["500MB", "1GB", "2TB", "100KB", "50MB"]
    
    largest, l_bytes = find_largest_unit(sizes)
    smallest, s_bytes = find_smallest_unit(sizes)
    
    print(f"\n列表: {sizes}")
    print(f"最大: {largest} ({format_size(l_bytes)})")
    print(f"最小: {smallest} ({format_size(s_bytes)})")


def example_transfer_speed():
    """传输速度示例"""
    print("\n" + "=" * 50)
    print("传输速度示例")
    print("=" * 50)
    
    speeds = [
        1024,  # 1 KB/s
        1024 * 100,  # 100 KB/s
        1024 * 1024,  # 1 MB/s
        1024 * 1024 * 10,  # 10 MB/s
        1024 * 1024 * 100,  # 100 MB/s
    ]
    
    print("\n文件传输速度：")
    for speed in speeds:
        print(f"  {speed:>15,} Bytes/s = {speed_format(speed)}")
    
    # 带宽
    print("\n网络带宽：")
    bandwidths = [
        1_000_000,  # 1 Mbps
        10_000_000,  # 10 Mbps
        100_000_000,  # 100 Mbps
        1_000_000_000,  # 1 Gbps
    ]
    for bw in bandwidths:
        print(f"  {bw:>15,} bps = {bandwidth_format(bw)}")


def example_download_estimator():
    """下载时间估算示例"""
    print("\n" + "=" * 50)
    print("下载时间估算示例")
    print("=" * 50)
    
    # 模拟下载场景
    scenarios = [
        (gb(1), mb(1)),  # 1GB 文件，1MB/s 速度
        (gb(10), mb(5)),  # 10GB 文件，5MB/s 速度
        (gb(50), mb(10)),  # 50GB 文件，10MB/s 速度
        (tb(1), mb(50)),  # 1TB 文件，50MB/s 速度
    ]
    
    print("\n文件大小 | 下载速度 | 预计时间")
    print("-" * 50)
    for size, speed in scenarios:
        time_str = estimate_time(size, speed)
        print(f"{format_size(size):>10} | {speed_format(speed):>10} | {time_str}")


def example_convenience_functions():
    """便捷函数示例"""
    print("\n" + "=" * 50)
    print("便捷函数示例")
    print("=" * 50)
    
    print("\n快速转换为字节：")
    print(f"  kb(1) = {kb(1):,} Bytes")
    print(f"  mb(1) = {mb(1):,} Bytes")
    print(f"  gb(1) = {gb(1):,} Bytes")
    print(f"  tb(1) = {tb(1):,} Bytes")
    
    print("\n二进制单位转字节：")
    print(f"  kib(1) = {kib(1):,} Bytes")
    print(f"  mib(1) = {mib(1):,} Bytes")
    print(f"  gib(1) = {gib(1):,} Bytes")
    print(f"  tib(1) = {tib(1):,} Bytes")
    
    print("\n计算文件总大小：")
    total = gb(2) + mb(500) + kb(100)
    print(f"  2GB + 500MB + 100KB = {total:,} Bytes = {format_size(total)}")


def example_real_world_scenarios():
    """真实场景示例"""
    print("\n" + "=" * 50)
    print("真实场景示例")
    print("=" * 50)
    
    # 场景1：磁盘空间分析
    print("\n场景1：磁盘空间分析")
    total_space = tb(1)
    used_space = gb(650)
    free_space = total_space - used_space
    
    print(f"  总容量: {format_size(total_space)}")
    print(f"  已使用: {format_size(used_space)}")
    print(f"  剩余: {format_size(free_space)}")
    print(f"  使用率: {percentage(used_space, total_space)}")
    print(f"  " + progress_bar(used_space, total_space, width=30))
    
    # 场景2：文件大小对比
    print("\n场景2：文件大小对比")
    files = {
        "文档.pdf": mb(5),
        "照片.jpg": kb(2500),
        "视频.mp4": gb(1.5),
        "压缩包.zip": mb(500),
    }
    
    for name, size in files.items():
        print(f"  {name}: {format_size(size)}")
    
    total = sum(files.values())
    print(f"  总计: {format_size(total)}")
    
    # 场景3：存储升级决策
    print("\n场景3：存储升级决策")
    current = gb(256)
    needed = gb(500)
    
    if compare(needed, current) > 0:
        shortage = subtract(needed, current)
        print(f"  当前: {format_size(current)}")
        print(f"  需要: {format_size(needed)}")
        print(f"  缺口: {format_size(shortage)}")
        print(f"  建议: 升级到至少 {format_size(needed)} 存储")
    else:
        print(f"  存储充足，无需升级")
    
    # 场景4：云存储成本估算
    print("\n场景4：云存储成本估算")
    storage_used = tb(2.5)
    cost_per_gb = 0.023  # AWS S3 标准存储价格
    
    monthly_cost = from_bytes(storage_used, "GB") * cost_per_gb
    yearly_cost = monthly_cost * 12
    
    print(f"  存储数据: {format_size(storage_used)}")
    print(f"  单价: ${cost_per_gb}/GB/月")
    print(f"  月费用: ${monthly_cost:.2f}")
    print(f"  年费用: ${yearly_cost:.2f}")


def example_human_readable():
    """人类可读格式示例"""
    print("\n" + "=" * 50)
    print("人类可读格式示例")
    print("=" * 50)
    
    sizes = [500, 1024, 1536, 1_048_576, 1_500_000_000]
    
    print("\n短格式 vs 长格式：")
    for size in sizes:
        short = human_readable(size, style="short")
        long = human_readable(size, style="long")
        print(f"  {size:>15,} -> {short:>15} | {long}")
    
    print("\n十进制 vs 二进制（长格式）：")
    for size in [1024, 1_048_576, 1_073_741_824]:
        dec = human_readable(size, style="long", binary=False)
        bin = human_readable(size, style="long", binary=True)
        print(f"  {size:>15,} -> {dec:>20} | {bin}")


def main():
    """运行所有示例"""
    example_basic_conversion()
    example_formatting()
    example_parsing()
    example_progress()
    example_comparison_calculation()
    example_finding_extremes()
    example_transfer_speed()
    example_download_estimator()
    example_convenience_functions()
    example_real_world_scenarios()
    example_human_readable()
    
    print("\n" + "=" * 50)
    print("示例完成！")
    print("=" * 50)


if __name__ == "__main__":
    main()