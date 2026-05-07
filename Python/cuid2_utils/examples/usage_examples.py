"""
CUID2 Utils 使用示例

展示如何使用 CUID2 生成唯一 ID：
- 基本 ID 生成
- 批量生成
- 安全变体
- 带前缀 ID
- ID 验证
"""

import sys
import os

# 添加父目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from cuid2_utils.mod import (
    Cuid2,
    SecureCuid2,
    PrefixedCuid2,
    create_id,
    create_id_batch,
    create_prefixed_id,
    is_cuid2
)


def basic_usage():
    """基本使用示例"""
    print("\n=== 基本使用 ===")
    
    # 创建 CUID2 生成器
    cuid = Cuid2()
    
    # 生成单个 ID（默认 24 字符）
    id1 = cuid.generate()
    print(f"默认长度 ID: {id1}")
    print(f"ID 长度: {len(id1)}")
    
    # 生成自定义长度 ID
    id_short = cuid.generate(length=8)
    id_long = cuid.generate(length=32)
    print(f"短 ID (8): {id_short}")
    print(f"长 ID (32): {id_long}")


def quick_functions():
    """快捷函数示例"""
    print("\n=== 快捷函数 ===")
    
    # 使用快捷函数生成 ID
    id1 = create_id()
    print(f"快捷生成: {id1}")
    
    # 自定义长度
    id2 = create_id(length=16)
    print(f"自定义长度: {id2}")
    
    # 批量生成
    ids = create_id_batch(5)
    print(f"批量生成 ({len(ids)} 个):")
    for i, id_val in enumerate(ids, 1):
        print(f"  {i}. {id_val}")


def validation_example():
    """ID 验证示例"""
    print("\n=== ID 验证 ===")
    
    cuid = Cuid2()
    
    # 验证有效 ID
    valid_id = cuid.generate()
    print(f"ID: {valid_id}")
    print(f"是否有效: {cuid.is_valid(valid_id)}")
    
    # 使用快捷验证函数
    print(f"is_cuid2(): {is_cuid2(valid_id)}")
    
    # 验证无效 ID
    invalid_ids = ["", "a", "abc!@#", "x" * 33]
    for id_val in invalid_ids:
        print(f"'{id_val[:20]}...' 有效: {is_cuid2(id_val)}")


def secure_cuid2_example():
    """安全 CUID2 示例"""
    print("\n=== 安全 CUID2 ===")
    
    # 创建安全生成器（默认 32 字符）
    secure = SecureCuid2()
    
    id1 = secure.generate()
    print(f"安全 ID: {id1}")
    print(f"长度: {len(id1)}")
    
    # 批量生成
    secure_ids = secure.generate_batch(5)
    print(f"批量安全 ID:")
    for i, id_val in enumerate(secure_ids, 1):
        print(f"  {i}. {id_val}")


def prefixed_cuid2_example():
    """带前缀 CUID2 示例"""
    print("\n=== 带前缀 CUID2 ===")
    
    # 创建不同前缀的生成器
    user_gen = PrefixedCuid2(prefix="user")
    order_gen = PrefixedCuid2(prefix="order")
    product_gen = PrefixedCuid2(prefix="prod")
    
    # 生成带前缀 ID
    user_id = user_gen.generate()
    order_id = order_gen.generate()
    product_id = product_gen.generate()
    
    print(f"用户 ID: {user_id}")
    print(f"订单 ID: {order_id}")
    print(f"产品 ID: {product_id}")
    
    # 使用快捷函数
    session_id = create_prefixed_id("session")
    print(f"会话 ID: {session_id}")
    
    # 验证和提取
    print(f"\n提取前缀: {user_gen.extract_prefix(user_id)}")
    print(f"提取 CUID: {user_gen.extract_cuid(user_id)}")
    print(f"验证: {user_gen.is_valid(user_id)}")


def id_info_example():
    """ID 信息获取示例"""
    print("\n=== ID 信息 ===")
    
    cuid = Cuid2()
    id1 = cuid.generate()
    
    info = cuid.get_info(id1)
    print(f"ID: {info['id']}")
    print(f"长度: {info['length']}")
    print(f"有效: {info['valid']}")
    print(f"格式: {info['format']}")
    print(f"编码: {info['encoding']}")


def fingerprint_example():
    """自定义指纹示例"""
    print("\n=== 自定义指纹 ===")
    
    # 使用自定义指纹（用于多实例环境）
    cuid1 = Cuid2(fingerprint="server_instance_1")
    cuid2 = Cuid2(fingerprint="server_instance_2")
    
    id1 = cuid1.generate()
    id2 = cuid2.generate()
    
    print(f"实例 1 ID: {id1}")
    print(f"实例 2 ID: {id2}")
    
    # 查看指纹
    print(f"实例 1 指纹: {cuid1.fingerprint}")
    print(f"实例 2 指纹: {cuid2.fingerprint}")


def database_example():
    """数据库应用示例"""
    print("\n=== 数据库应用示例 ===")
    
    # 模拟数据库记录
    user_gen = PrefixedCuid2(prefix="user")
    post_gen = PrefixedCuid2(prefix="post")
    comment_gen = PrefixedCuid2(prefix="comment")
    
    # 创建用户
    user = {
        "id": user_gen.generate(),
        "name": "张三",
        "email": "zhangsan@example.com"
    }
    print(f"用户: {user}")
    
    # 创建帖子
    post = {
        "id": post_gen.generate(),
        "user_id": user["id"],
        "title": "我的第一篇帖子",
        "content": "这是内容..."
    }
    print(f"帖子: {post}")
    
    # 创建评论
    comment = {
        "id": comment_gen.generate(),
        "post_id": post["id"],
        "user_id": user["id"],
        "content": "很棒的帖子！"
    }
    print(f"评论: {comment}")


def performance_example():
    """性能测试示例"""
    print("\n=== 性能测试 ===")
    
    import time
    
    cuid = Cuid2()
    
    # 测试单次生成速度
    start = time.time()
    for _ in range(10000):
        cuid.generate()
    single_time = time.time() - start
    
    # 测试批量生成速度
    start = time.time()
    cuid.generate_batch(10000)
    batch_time = time.time() - start
    
    print(f"单次生成 10000 个: {single_time:.3f}s ({10000/single_time:.0f} ID/s)")
    print(f"批量生成 10000 个: {batch_time:.3f}s ({10000/batch_time:.0f} ID/s)")


def uniqueness_demo():
    """唯一性演示"""
    print("\n=== 唯一性演示 ===")
    
    cuid = Cuid2()
    
    # 生成大量 ID
    print("生成 10000 个 ID...")
    ids = cuid.generate_batch(10000)
    
    # 检查唯一性
    unique_count = len(set(ids))
    print(f"总 ID 数: {len(ids)}")
    print(f"唯一 ID 数: {unique_count}")
    print(f"重复数: {len(ids) - unique_count}")
    
    # 显示部分 ID
    print("\n前 5 个 ID:")
    for i, id_val in enumerate(ids[:5], 1):
        print(f"  {i}. {id_val}")


def main():
    """运行所有示例"""
    print("=" * 60)
    print("CUID2 Utils 使用示例")
    print("=" * 60)
    
    basic_usage()
    quick_functions()
    validation_example()
    secure_cuid2_example()
    prefixed_cuid2_example()
    id_info_example()
    fingerprint_example()
    database_example()
    performance_example()
    uniqueness_demo()
    
    print("\n" + "=" * 60)
    print("示例完成！")
    print("=" * 60)


if __name__ == "__main__":
    main()