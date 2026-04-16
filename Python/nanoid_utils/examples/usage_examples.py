"""
nanoid_utils 使用示例

展示 NanoID 工具库的各种使用场景：
1. 基础生成
2. 自定义字符集
3. 批量生成
4. 验证与唯一性
5. 实际应用场景
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    generate,
    generate_custom,
    generate_number,
    generate_lowercase,
    generate_alphabet,
    generate_no_lookalikes,
    batch,
    validate,
    is_unique,
    generate_unique,
    estimate_collision_probability,
    nanoid,
)


def print_section(title: str):
    """打印章节标题"""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print('='*60)


def example_basic_generation():
    """基础生成示例"""
    print_section("1. 基础生成")
    
    # 默认长度21
    print(f"默认NanoID (21字符): {generate()}")
    
    # 自定义长度
    print(f"10字符ID: {generate(10)}")
    print(f"8字符ID: {generate(8)}")
    print(f"32字符ID: {generate(32)}")
    
    # 使用别名
    print(f"使用nanoid别名: {nanoid()}")


def example_predefined_alphabets():
    """预定义字符集示例"""
    print_section("2. 预定义字符集")
    
    # 纯数字
    print(f"纯数字ID (16位): {generate_number()}")
    print(f"纯数字ID (8位): {generate_number(8)}")
    
    # 小写字母+数字
    print(f"小写字母+数字: {generate_lowercase()}")
    
    # 纯字母
    print(f"纯字母ID: {generate_alphabet()}")
    
    # 无易混淆字符
    print(f"无易混淆字符: {generate_no_lookalikes()}")


def example_custom_alphabet():
    """自定义字符集示例"""
    print_section("3. 自定义字符集")
    
    # 十六进制ID
    hex_alphabet = '0123456789abcdef'
    hex_id = generate_custom(32, hex_alphabet)
    print(f"十六进制ID (32位): {hex_id}")
    
    # Base36 (小写字母+数字)
    base36 = '0123456789abcdefghijklmnopqrstuvwxyz'
    base36_id = generate_custom(25, base36)
    print(f"Base36 ID (25位): {base36_id}")
    
    # 自定义表情符号字符集
    emoji = '😀😁😂🤣😃😄😅😆😉😊'
    emoji_id = generate_custom(5, emoji)
    print(f"表情符号ID (5位): {emoji_id}")
    
    # 二进制
    binary_id = generate_custom(32, '01')
    print(f"二进制ID (32位): {binary_id}")


def example_batch_generation():
    """批量生成示例"""
    print_section("4. 批量生成")
    
    # 生成10个ID
    ids = batch(10)
    print("批量生成10个ID:")
    for i, id_ in enumerate(ids, 1):
        print(f"  {i:2d}. {id_}")
    
    # 生成指定长度的批量ID
    short_ids = batch(5, 8)
    print(f"\n批量生成5个8字符ID: {short_ids}")


def example_validation():
    """验证示例"""
    print_section("5. 验证功能")
    
    # 验证标准ID
    valid_id = generate()
    print(f"ID: {valid_id}")
    print(f"  验证结果: {validate(valid_id)}")
    
    # 验证长度
    print(f"  长度为21: {validate(valid_id, size=21)}")
    print(f"  长度为10: {validate(valid_id, size=10)}")
    
    # 验证无效ID
    invalid_id = "invalid@id!"
    print(f"\n无效ID: {invalid_id}")
    print(f"  验证结果: {validate(invalid_id)}")
    
    # 使用自定义字符集验证
    hex_id = generate_custom(16, '0123456789abcdef')
    print(f"\n十六进制ID: {hex_id}")
    print(f"  在十六进制字符集中: {validate(hex_id, alphabet='0123456789abcdef')}")
    print(f"  在默认字符集中: {validate(hex_id, alphabet='0123456789abcdefABCDEF')}")


def example_uniqueness():
    """唯一性检查示例"""
    print_section("6. 唯一性保证")
    
    # 现有ID集合
    existing_ids = {"user_abc123", "order_xyz789", "product_qwe456"}
    
    # 检查唯一性
    new_id = "user_new001"
    print(f"检查 '{new_id}' 是否唯一: {is_unique(new_id, existing_ids)}")
    
    duplicate_id = "user_abc123"
    print(f"检查 '{duplicate_id}' 是否唯一: {is_unique(duplicate_id, existing_ids)}")
    
    # 生成确保唯一的ID
    guaranteed_unique = generate_unique(existing_ids=existing_ids)
    print(f"\n生成保证唯一的ID: {guaranteed_unique}")
    print(f"  确实唯一: {is_unique(guaranteed_unique, existing_ids)}")


def example_collision_probability():
    """碰撞概率估算示例"""
    print_section("7. 碰撞概率估算")
    
    scenarios = [
        ("标准21字符", 21, 64, 1000000),
        ("短ID (8字符)", 8, 64, 10000),
        ("纯数字 (16位)", 16, 10, 100000),
        ("更短 (6字符)", 6, 64, 10000),
    ]
    
    print("不同场景的碰撞概率估算:")
    for name, size, alphabet_len, count in scenarios:
        prob = estimate_collision_probability(size, alphabet_len, count)
        percentage = prob * 100
        print(f"  {name}: 生成 {count:,} 个ID, 碰撞概率 = {percentage:.6f}%")


def example_practical_use_cases():
    """实际应用场景示例"""
    print_section("8. 实际应用场景")
    
    print("用户ID:")
    for i in range(3):
        print(f"  用户{i+1}: usr_{generate(12)}")
    
    print("\n订单号:")
    for i in range(3):
        print(f"  订单{i+1}: ORD-{generate_number(10)}")
    
    print("\n短链接码:")
    for i in range(3):
        print(f"  链接{i+1}: https://short.url/{generate(6)}")
    
    print("\n会话令牌:")
    print(f"  Session: sess_{generate(32)}")
    
    print("\nAPI密钥:")
    print(f"  API Key: sk_live_{generate(32)}")
    
    print("\n文件名 (避免冲突):")
    filename = generate(8)
    print(f"  原文件: image.png")
    print(f"  存储为: {filename}.png")
    
    print("\n数据库主键替代:")
    print(f"  用户表: {generate(16)}")
    print(f"  评论表: {generate(16)}")


def example_database_simulation():
    """模拟数据库使用场景"""
    print_section("9. 模拟数据库场景")
    
    # 模拟用户表
    users = {}
    
    # 添加用户
    for name in ["Alice", "Bob", "Charlie"]:
        user_id = generate_unique(existing_ids=set(users.keys()))
        users[user_id] = {
            "id": user_id,
            "name": name,
            "created_at": "2024-01-01"
        }
    
    print("模拟用户表:")
    for user_id, user in users.items():
        print(f"  {user_id}: {user['name']}")
    
    # 模拟订单
    print("\n模拟订单表:")
    orders = {}
    for user_id, user in users.items():
        order_id = f"ORD-{generate_number(10)}"
        orders[order_id] = {
            "order_id": order_id,
            "user_id": user_id,
            "user_name": user["name"],
            "amount": 100.00
        }
        print(f"  {order_id}: 用户 {user['name']} 订单")


def example_performance():
    """性能测试示例"""
    print_section("10. 性能测试")
    
    import time
    
    # 测试生成速度
    count = 100000
    
    start = time.time()
    ids = batch(count)
    elapsed = time.time() - start
    
    print(f"生成 {count:,} 个ID:")
    print(f"  耗时: {elapsed:.3f} 秒")
    print(f"  速度: {count/elapsed:,.0f} ID/秒")
    
    # 检查唯一性
    unique_count = len(set(ids))
    print(f"  唯一ID: {unique_count:,}/{count:,}")
    
    # 平均长度
    avg_len = sum(len(id_) for id_ in ids[:1000]) / 1000
    print(f"  平均长度: {avg_len:.1f} 字符")


if __name__ == '__main__':
    print("\n" + "="*60)
    print("  NanoID Utils - 使用示例")
    print("="*60)
    
    example_basic_generation()
    example_predefined_alphabets()
    example_custom_alphabet()
    example_batch_generation()
    example_validation()
    example_uniqueness()
    example_collision_probability()
    example_practical_use_cases()
    example_database_simulation()
    example_performance()
    
    print("\n" + "="*60)
    print("  示例演示完成!")
    print("="*60 + "\n")