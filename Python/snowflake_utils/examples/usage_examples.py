"""
Snowflake ID Generator 使用示例

本示例展示如何使用Snowflake ID生成器：
1. 基本用法
2. 分布式场景
3. Discord/Twitter风格ID
4. ID解析和分析
5. 时间范围查询
"""

import time
from datetime import datetime, timezone, timedelta

from snowflake_utils import (
    SnowflakeGenerator,
    DiscordSnowflake,
    TwitterSnowflake,
    generate_id,
    generate_batch,
    decompose_id,
    extract_timestamp,
    extract_datetime,
    create_generator
)


def example_basic_usage():
    """基本用法示例"""
    print("=" * 60)
    print("1. 基本用法")
    print("=" * 60)
    
    # 创建生成器
    gen = SnowflakeGenerator(datacenter_id=1, worker_id=1)
    
    # 生成单个ID
    snowflake_id = gen.generate()
    print(f"生成的Snowflake ID: {snowflake_id}")
    
    # 解析ID
    info = gen.decompose(snowflake_id)
    print(f"\nID解析结果:")
    print(f"  ID值: {info['id']}")
    print(f"  时间戳: {info['timestamp']}")
    print(f"  日期时间: {info['datetime']}")
    print(f"  数据中心ID: {info['datacenter_id']}")
    print(f"  工作节点ID: {info['worker_id']}")
    print(f"  序列号: {info['sequence']}")
    
    # 批量生成
    print(f"\n批量生成10个ID:")
    batch = gen.generate_batch(10)
    for i, sid in enumerate(batch[:5], 1):
        print(f"  {i}. {sid}")
    print(f"  ... 共{len(batch)}个")


def example_convenience_functions():
    """便捷函数示例"""
    print("\n" + "=" * 60)
    print("2. 便捷函数")
    print("=" * 60)
    
    # 使用便捷函数快速生成ID
    sid = generate_id()
    print(f"快速生成的ID: {sid}")
    
    # 解析ID
    info = decompose_id(sid)
    print(f"创建时间: {info['datetime']}")
    
    # 批量生成
    ids = generate_batch(5)
    print(f"\n批量生成的5个ID:")
    for i, id in enumerate(ids, 1):
        print(f"  {i}. {id}")


def example_distributed_scenario():
    """分布式场景示例"""
    print("\n" + "=" * 60)
    print("3. 分布式场景 - 多节点同时生成")
    print("=" * 60)
    
    # 模拟3个不同节点
    node1 = SnowflakeGenerator(datacenter_id=0, worker_id=1)
    node2 = SnowflakeGenerator(datacenter_id=0, worker_id=2)
    node3 = SnowflakeGenerator(datacenter_id=1, worker_id=1)
    
    # 各节点生成ID
    id1 = node1.generate()
    id2 = node2.generate()
    id3 = node3.generate()
    
    print(f"节点(数据中心=0, 工作节点=1)生成的ID: {id1}")
    print(f"节点(数据中心=0, 工作节点=2)生成的ID: {id2}")
    print(f"节点(数据中心=1, 工作节点=1)生成的ID: {id3}")
    
    # 解析来源
    print(f"\n解析ID来源:")
    for sid, name in [(id1, "节点1"), (id2, "节点2"), (id3, "节点3")]:
        dc = (sid >> 17) & 31
        wk = (sid >> 12) & 31
        print(f"  {name}的ID {sid}: 数据中心={dc}, 工作节点={wk}")
    
    # 验证所有ID唯一
    all_ids = [id1, id2, id3]
    print(f"\n所有ID唯一: {len(all_ids) == len(set(all_ids))}")


def example_discord_snowflake():
    """Discord风格Snowflake示例"""
    print("\n" + "=" * 60)
    print("4. Discord Snowflake ID")
    print("=" * 60)
    
    # 创建Discord风格生成器
    discord_gen = DiscordSnowflake(worker_id=1)
    
    # 生成ID
    discord_id = discord_gen.generate()
    print(f"Discord ID: {discord_id}")
    
    # 字符串形式（Discord常用）
    discord_id_str = discord_gen.generate_str()
    print(f"Discord ID (字符串): {discord_id_str}")
    
    # 获取创建时间
    creation_time = DiscordSnowflake.get_creation_time(discord_id)
    print(f"创建时间: {creation_time}")
    
    # 解析一个真实的Discord ID
    # 示例：Discord官方公告频道的一个消息ID
    print("\n解析Discord时间:")
    # 可以用任意Discord ID测试
    test_id = 1234567890123456789
    try:
        creation = DiscordSnowflake.get_creation_time(test_id)
        print(f"  ID {test_id} 的创建时间: {creation}")
    except:
        print(f"  无法解析测试ID")


def example_twitter_snowflake():
    """Twitter风格Snowflake示例"""
    print("\n" + "=" * 60)
    print("5. Twitter Snowflake ID")
    print("=" * 60)
    
    # 创建Twitter风格生成器
    twitter_gen = TwitterSnowflake(datacenter_id=1, worker_id=1)
    
    # 生成ID
    tweet_id = twitter_gen.generate()
    print(f"Twitter Tweet ID: {tweet_id}")
    
    # 获取创建时间
    creation_time = TwitterSnowflake.get_creation_time(tweet_id)
    print(f"创建时间: {creation_time}")


def example_time_range_query():
    """时间范围查询示例"""
    print("\n" + "=" * 60)
    print("6. 时间范围查询")
    print("=" * 60)
    
    gen = SnowflakeGenerator(datacenter_id=1, worker_id=1)
    
    # 定义时间范围
    now = datetime.now(timezone.utc)
    start_time = now - timedelta(hours=1)
    end_time = now + timedelta(hours=1)
    
    # 计算ID范围
    start_id, end_id = gen.ids_in_range(start_time, end_time)
    
    print(f"时间范围: {start_time} 到 {end_time}")
    print(f"对应的ID范围:")
    print(f"  起始ID: {start_id}")
    print(f"  结束ID: {end_id}")
    
    # 生成一个ID并验证是否在范围内
    current_id = gen.generate()
    print(f"\n当前生成的ID: {current_id}")
    print(f"ID在范围内: {start_id <= current_id <= end_id}")


def example_id_analysis():
    """ID分析示例"""
    print("\n" + "=" * 60)
    print("7. ID分析")
    print("=" * 60)
    
    gen = SnowflakeGenerator(datacenter_id=3, worker_id=7)
    
    # 生成ID
    sid = gen.generate()
    
    print(f"分析ID: {sid}")
    print(f"\n二进制表示: {bin(sid)}")
    
    # 手动提取各部分
    print(f"\n手动解析:")
    timestamp_part = sid >> 22
    datacenter_part = (sid >> 17) & 31
    worker_part = (sid >> 12) & 4095
    sequence_part = sid & 4095
    
    print(f"  时间戳部分: {timestamp_part}")
    print(f"  数据中心+工作节点部分: {datacenter_part}")
    print(f"  工作节点部分: {worker_part}")
    print(f"  序列号部分: {sequence_part}")
    
    # 使用生成器方法
    print(f"\n使用生成器方法:")
    print(f"  时间戳: {gen.extract_timestamp(sid)}")
    print(f"  日期时间: {gen.extract_datetime(sid)}")
    print(f"  数据中心ID: {gen.extract_datacenter_id(sid)}")
    print(f"  工作节点ID: {gen.extract_worker_id(sid)}")
    print(f"  序列号: {gen.extract_sequence(sid)}")


def example_performance():
    """性能测试示例"""
    print("\n" + "=" * 60)
    print("8. 性能测试")
    print("=" * 60)
    
    gen = SnowflakeGenerator(datacenter_id=1, worker_id=1)
    
    # 测试生成速度
    count = 100000
    start = time.time()
    for _ in range(count):
        gen.generate()
    elapsed = time.time() - start
    
    ids_per_second = count / elapsed
    print(f"生成 {count} 个ID耗时: {elapsed:.3f}秒")
    print(f"生成速度: {ids_per_second:,.0f} IDs/秒")
    
    # 测试批量生成
    start = time.time()
    batch = gen.generate_batch(10000)
    elapsed = time.time() - start
    
    print(f"\n批量生成10000个ID耗时: {elapsed:.3f}秒")
    print(f"平均每个ID: {elapsed/10000*1000000:.2f}微秒")


def example_custom_epoch():
    """自定义epoch示例"""
    print("\n" + "=" * 60)
    print("9. 自定义Epoch")
    print("=" * 60)
    
    # 使用自定义epoch（如项目启动时间）
    project_start = datetime(2024, 6, 1, tzinfo=timezone.utc)
    custom_epoch = int(project_start.timestamp() * 1000)
    
    gen = SnowflakeGenerator(
        datacenter_id=1,
        worker_id=1,
        epoch=custom_epoch
    )
    
    print(f"自定义Epoch: {project_start}")
    print(f"Epoch时间戳: {custom_epoch}")
    
    sid = gen.generate()
    print(f"生成的ID: {sid}")
    
    info = gen.decompose(sid)
    print(f"解析后的时间: {info['datetime']}")


def example_high_throughput():
    """高吞吐量场景示例"""
    print("\n" + "=" * 60)
    print("10. 高吞吐量场景")
    print("=" * 60)
    
    gen = SnowflakeGenerator(datacenter_id=1, worker_id=1)
    
    # 单毫秒内最多可生成4096个ID
    print("单毫秒内生成1000个ID...")
    ids = [gen.generate() for _ in range(1000)]
    
    # 检查唯一性
    unique_count = len(set(ids))
    print(f"生成1000个ID，唯一ID数: {unique_count}")
    
    # 检查有序性
    is_sorted = all(ids[i] < ids[i+1] for i in range(len(ids)-1))
    print(f"ID严格递增: {is_sorted}")
    
    # 显示序列号分布
    sequences = [gen.extract_sequence(sid) for sid in ids[:20]]
    print(f"\n前20个ID的序列号: {sequences}")


if __name__ == "__main__":
    example_basic_usage()
    example_convenience_functions()
    example_distributed_scenario()
    example_discord_snowflake()
    example_twitter_snowflake()
    example_time_range_query()
    example_id_analysis()
    example_performance()
    example_custom_epoch()
    example_high_throughput()
    
    print("\n" + "=" * 60)
    print("示例完成！")
    print("=" * 60)