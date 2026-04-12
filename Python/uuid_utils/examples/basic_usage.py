"""
AllToolkit - UUID Utilities 使用示例

本文件展示 uuid_utils 模块的各种使用场景。
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    UUIDUtils,
    generate_v1, generate_v3, generate_v4, generate_v5,
    parse, is_valid, is_valid_fast,
    to_string, to_bytes, from_bytes, to_int, from_int,
    compare, equal, sort,
    get_timestamp, get_node,
    generate_batch, nil, is_nil,
    hash_to_uuid
)
import uuid


def example_basic_generation():
    """示例 1: 基本 UUID 生成"""
    print("=" * 60)
    print("示例 1: 基本 UUID 生成")
    print("=" * 60)
    
    # v1 - 基于时间
    u1 = generate_v1()
    print(f"UUID v1 (时间基): {u1}")
    print(f"  版本：{u1.version}")
    print(f"  创建时间：{get_timestamp(u1)}")
    
    # v3 - 基于 MD5 命名空间
    u3 = generate_v3(UUIDUtils.NAMESPACE_DNS, 'example.com')
    print(f"\nUUID v3 (MD5 命名空间): {u3}")
    print(f"  版本：{u3.version}")
    print(f"  命名空间：DNS")
    print(f"  名称：example.com")
    
    # v4 - 随机
    u4 = generate_v4()
    print(f"\nUUID v4 (随机): {u4}")
    print(f"  版本：{u4.version}")
    
    # v5 - 基于 SHA-1 命名空间
    u5 = generate_v5(UUIDUtils.NAMESPACE_URL, 'https://example.com')
    print(f"\nUUID v5 (SHA-1 命名空间): {u5}")
    print(f"  版本：{u5.version}")
    print(f"  命名空间：URL")
    print(f"  名称：https://example.com")
    
    print()


def example_deterministic():
    """示例 2: 确定性 UUID（相同输入=相同输出）"""
    print("=" * 60)
    print("示例 2: 确定性 UUID")
    print("=" * 60)
    
    # v3 和 v5 是确定性的
    name = 'user_12345'
    
    u3_a = generate_v3(UUIDUtils.NAMESPACE_DNS, name)
    u3_b = generate_v3(UUIDUtils.NAMESPACE_DNS, name)
    
    print(f"输入：{name}")
    print(f"v3 第一次生成：{u3_a}")
    print(f"v3 第二次生成：{u3_b}")
    print(f"是否相同：{u3_a == u3_b}")  # True!
    
    u5_a = generate_v5(UUIDUtils.NAMESPACE_DNS, name)
    u5_b = generate_v5(UUIDUtils.NAMESPACE_DNS, name)
    
    print(f"\nv5 第一次生成：{u5_a}")
    print(f"v5 第二次生成：{u5_b}")
    print(f"是否相同：{u5_a == u5_b}")  # True!
    
    # v4 是随机的，每次不同
    u4_a = generate_v4()
    u4_b = generate_v4()
    print(f"\nv4 第一次生成：{u4_a}")
    print(f"v4 第二次生成：{u4_b}")
    print(f"是否相同：{u4_a == u4_b}")  # False (几乎总是)
    
    print()


def example_validation():
    """示例 3: UUID 验证"""
    print("=" * 60)
    print("示例 3: UUID 验证")
    print("=" * 60)
    
    test_cases = [
        ('550e8400-e29b-41d4-a716-446655440000', '标准格式'),
        ('{550e8400-e29b-41d4-a716-446655440000}', '带括号'),
        ('urn:uuid:550e8400-e29b-41d4-a716-446655440000', 'URN 格式'),
        ('550e8400e29b41d4a716446655440000', '无连字符'),
        ('550E8400-E29B-41D4-A716-446655440000', '大写'),
        ('not-a-uuid', '无效 UUID'),
        ('', '空字符串'),
    ]
    
    for uuid_str, description in test_cases:
        valid = is_valid(uuid_str)
        fast_valid = is_valid_fast(uuid_str)
        print(f"{description:15} : {uuid_str[:50]:50} -> 有效={valid}, 快速验证={fast_valid}")
    
    print()


def example_conversion():
    """示例 4: UUID 格式转换"""
    print("=" * 60)
    print("示例 4: UUID 格式转换")
    print("=" * 60)
    
    u = parse('550e8400-e29b-41d4-a716-446655440000')
    print(f"原始 UUID: {u}")
    
    # 字符串格式
    print(f"\n字符串格式:")
    print(f"  标准：    {to_string(u, 'standard')}")
    print(f"  带括号：  {to_string(u, 'braced')}")
    print(f"  URN:      {to_string(u, 'urn')}")
    print(f"  无连字符：{to_string(u, 'no-hyphen')}")
    print(f"  大写：    {to_string(u, 'upper')}")
    
    # 字节
    b = to_bytes(u)
    print(f"\n字节表示：{b.hex()}")
    print(f"字节长度：{len(b)} bytes")
    
    # 从字节恢复
    u_from_bytes = from_bytes(b)
    print(f"从字节恢复：{u_from_bytes}")
    print(f"是否相等：{u == u_from_bytes}")
    
    # 整数
    i = to_int(u)
    print(f"\n整数表示：{i}")
    
    # 从整数恢复
    u_from_int = from_int(i)
    print(f"从整数恢复：{u_from_int}")
    print(f"是否相等：{u == u_from_int}")
    
    print()


def example_comparison():
    """示例 5: UUID 比较与排序"""
    print("=" * 60)
    print("示例 5: UUID 比较与排序")
    print("=" * 60)
    
    uuids = [
        '00000000-0000-0000-0000-000000000001',
        '00000000-0000-0000-0000-000000000000',
        '00000000-0000-0000-0000-000000000003',
        '00000000-0000-0000-0000-000000000002',
    ]
    
    print("原始列表:")
    for u in uuids:
        print(f"  {u}")
    
    # 排序
    sorted_uuids = sort(uuids)
    print("\n升序排序:")
    for u in sorted_uuids:
        print(f"  {u}")
    
    # 降序
    sorted_reverse = sort(uuids, reverse=True)
    print("\n降序排序:")
    for u in sorted_reverse:
        print(f"  {u}")
    
    # 比较
    u1 = parse('00000000-0000-0000-0000-000000000001')
    u2 = parse('00000000-0000-0000-0000-000000000002')
    
    print(f"\n比较 {u1} 和 {u2}:")
    print(f"  compare 结果：{compare(u1, u2)}")  # -1
    print(f"  equal 结果：{equal(u1, u2)}")  # False
    
    print()


def example_batch_generation():
    """示例 6: 批量生成"""
    print("=" * 60)
    print("示例 6: 批量生成 UUID")
    print("=" * 60)
    
    # 生成 10 个 v4 UUID
    uuids = generate_batch(10, version=4)
    
    print(f"生成了 {len(uuids)} 个 UUID v4:")
    for i, u in enumerate(uuids[:5], 1):  # 只显示前 5 个
        print(f"  {i}. {u}")
    if len(uuids) > 5:
        print(f"  ... 还有 {len(uuids) - 5} 个")
    
    # 检查唯一性
    unique_count = len(set(uuids))
    print(f"\n唯一性检查：{unique_count}/{len(uuids)} 个唯一")
    
    print()


def example_use_cases():
    """示例 7: 实际使用场景"""
    print("=" * 60)
    print("示例 7: 实际使用场景")
    print("=" * 60)
    
    # 场景 1: 数据库主键
    print("\n场景 1: 数据库主键")
    user_id = generate_v4()
    print(f"  新用户 ID: {user_id}")
    
    # 场景 2: 分布式请求追踪
    print("\n场景 2: 分布式请求追踪")
    request_id = generate_v1()
    timestamp = get_timestamp(request_id)
    print(f"  请求 ID: {request_id}")
    print(f"  生成时间：{timestamp}")
    
    # 场景 3: 缓存键生成
    print("\n场景 3: 缓存键生成（确定性）")
    cache_key = generate_v5(UUIDUtils.NAMESPACE_DNS, 'cache:user:12345:profile')
    print(f"  缓存键：{cache_key}")
    
    # 场景 4: URL 短链接
    print("\n场景 4: URL 短链接 ID")
    short_id = to_string(generate_v4(), 'no-hyphen')[:12]
    print(f"  短链接 ID: {short_id}")
    print(f"  完整 URL: https://example.com/s/{short_id}")
    
    # 场景 5: API 令牌
    print("\n场景 5: API 令牌生成")
    api_token = hash_to_uuid('user_12345:secret_key_abc', 'sha256')
    print(f"  API 令牌：{to_string(api_token, 'no-hyphen')}")
    
    # 场景 6: 分片键
    print("\n场景 6: 数据分片")
    user_uuid = hash_to_uuid('user_12345', 'sha256')
    shard_num = to_int(user_uuid) % 16  # 16 个分片
    print(f"  用户 UUID: {user_uuid}")
    print(f"  分片号：{shard_num}")
    
    print()


def example_nil_uuid():
    """示例 8: Nil UUID 处理"""
    print("=" * 60)
    print("示例 8: Nil UUID (全零 UUID)")
    print("=" * 60)
    
    nil_uuid = nil()
    print(f"Nil UUID: {nil_uuid}")
    print(f"整数值：{to_int(nil_uuid)}")
    print(f"是否为 Nil: {is_nil(nil_uuid)}")
    print(f"是否为 Nil (字符串): {is_nil('00000000-0000-0000-0000-000000000000')}")
    
    # 用作默认值或占位符
    default_user_id = nil()
    print(f"\n默认用户 ID (未设置): {default_user_id}")
    
    print()


def example_v1_timestamp():
    """示例 9: v1 UUID 时间戳提取"""
    print("=" * 60)
    print("示例 9: v1 UUID 时间戳提取")
    print("=" * 60)
    
    # 生成几个 v1 UUID，间隔一小段时间
    import time
    
    u1 = generate_v1()
    time.sleep(0.01)  # 等待 10ms
    u2 = generate_v1()
    time.sleep(0.01)
    u3 = generate_v1()
    
    print("生成的 v1 UUID 及其时间戳:")
    for i, u in enumerate([u1, u2, u3], 1):
        ts = get_timestamp(u)
        node = get_node(u)
        print(f"  {i}. {u}")
        print(f"     时间：{ts}")
        print(f"     节点：{node:012x}")
    
    # v1 UUID 可以排序以反映创建顺序
    uuids = [u3, u1, u2]  # 打乱顺序
    sorted_uuids = sort(uuids)
    
    print("\n排序后（按时间顺序）:")
    for i, u in enumerate(sorted_uuids, 1):
        ts = get_timestamp(u)
        print(f"  {i}. {u} - {ts}")
    
    print()


def main():
    """运行所有示例"""
    print()
    print("╔" + "═" * 58 + "╗")
    print("║" + " " * 15 + "AllToolkit UUID Utilities 示例" + " " * 15 + "║")
    print("╚" + "═" * 58 + "╝")
    print()
    
    example_basic_generation()
    example_deterministic()
    example_validation()
    example_conversion()
    example_comparison()
    example_batch_generation()
    example_use_cases()
    example_nil_uuid()
    example_v1_timestamp()
    
    print("=" * 60)
    print("所有示例完成!")
    print("=" * 60)
    print()


if __name__ == '__main__':
    main()
