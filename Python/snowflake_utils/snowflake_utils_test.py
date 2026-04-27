"""
Snowflake ID Generator 单元测试
"""

import sys
import os
import unittest
import time
import threading
from datetime import datetime, timezone, timedelta
from typing import List


# Add module directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mod import (
    SnowflakeGenerator,
    SnowflakeConfig,
    DiscordSnowflake,
    TwitterSnowflake,
    generate_id,
    generate_batch,
    decompose_id,
    extract_timestamp,
    extract_datetime,
    create_generator,
    get_default_generator
)


class TestSnowflakeConfig(unittest.TestCase):
    """测试SnowflakeConfig配置"""
    
    def test_config_values(self):
        """测试配置常量值"""
        self.assertEqual(SnowflakeConfig.TIMESTAMP_BITS, 41)
        self.assertEqual(SnowflakeConfig.DATACENTER_BITS, 5)
        self.assertEqual(SnowflakeConfig.WORKER_BITS, 5)
        self.assertEqual(SnowflakeConfig.SEQUENCE_BITS, 12)
        
        self.assertEqual(SnowflakeConfig.MAX_DATACENTER_ID, 31)
        self.assertEqual(SnowflakeConfig.MAX_WORKER_ID, 31)
        self.assertEqual(SnowflakeConfig.MAX_SEQUENCE, 4095)
        
        self.assertEqual(SnowflakeConfig.WORKER_ID_SHIFT, 12)
        self.assertEqual(SnowflakeConfig.DATACENTER_ID_SHIFT, 17)
        self.assertEqual(SnowflakeConfig.TIMESTAMP_SHIFT, 22)
    
    def test_default_epoch(self):
        """测试默认epoch时间"""
        # 默认epoch应该是2024-01-01 00:00:00 UTC
        expected_epoch = datetime(2024, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
        actual_epoch = datetime.fromtimestamp(
            SnowflakeConfig.DEFAULT_EPOCH / 1000.0, 
            tz=timezone.utc
        )
        self.assertEqual(actual_epoch, expected_epoch)


class TestSnowflakeGenerator(unittest.TestCase):
    """测试SnowflakeGenerator"""
    
    def test_create_generator(self):
        """测试创建生成器"""
        gen = SnowflakeGenerator(datacenter_id=1, worker_id=2)
        self.assertEqual(gen.datacenter_id, 1)
        self.assertEqual(gen.worker_id, 2)
    
    def test_invalid_datacenter_id(self):
        """测试无效的数据中心ID"""
        with self.assertRaises(ValueError):
            SnowflakeGenerator(datacenter_id=-1)
        with self.assertRaises(ValueError):
            SnowflakeGenerator(datacenter_id=32)
    
    def test_invalid_worker_id(self):
        """测试无效的工作节点ID"""
        with self.assertRaises(ValueError):
            SnowflakeGenerator(worker_id=-1)
        with self.assertRaises(ValueError):
            SnowflakeGenerator(worker_id=32)
    
    def test_generate_single_id(self):
        """测试生成单个ID"""
        gen = SnowflakeGenerator(datacenter_id=1, worker_id=1)
        sid = gen.generate()
        self.assertIsInstance(sid, int)
        self.assertGreater(sid, 0)
    
    def test_generate_unique_ids(self):
        """测试生成的ID唯一性"""
        gen = SnowflakeGenerator(datacenter_id=1, worker_id=1)
        ids = set()
        for _ in range(1000):
            sid = gen.generate()
            self.assertNotIn(sid, ids, "生成的ID重复")
            ids.add(sid)
        self.assertEqual(len(ids), 1000)
    
    def test_generate_ordered_ids(self):
        """测试ID按时间递增"""
        gen = SnowflakeGenerator(datacenter_id=1, worker_id=1)
        ids = [gen.generate() for _ in range(100)]
        for i in range(len(ids) - 1):
            self.assertLess(ids[i], ids[i + 1], "ID应该按时间递增")
    
    def test_generate_batch(self):
        """测试批量生成"""
        gen = SnowflakeGenerator(datacenter_id=1, worker_id=1)
        batch = gen.generate_batch(100)
        self.assertEqual(len(batch), 100)
        self.assertEqual(len(set(batch)), 100, "批量生成的ID应该唯一")
    
    def test_decompose(self):
        """测试ID解析"""
        gen = SnowflakeGenerator(datacenter_id=3, worker_id=5)
        sid = gen.generate()
        info = gen.decompose(sid)
        
        self.assertEqual(info['id'], sid)
        self.assertEqual(info['datacenter_id'], 3)
        self.assertEqual(info['worker_id'], 5)
        self.assertGreaterEqual(info['timestamp'], gen.epoch)
        self.assertIsInstance(info['datetime'], datetime)
    
    def test_extract_timestamp(self):
        """测试提取时间戳"""
        gen = SnowflakeGenerator()
        sid = gen.generate()
        timestamp = gen.extract_timestamp(sid)
        
        # 时间戳应该在当前时间附近（1秒内）
        current_time = int(time.time() * 1000)
        self.assertLess(abs(timestamp - current_time), 1000)
    
    def test_extract_datetime(self):
        """测试提取datetime"""
        gen = SnowflakeGenerator()
        sid = gen.generate()
        dt = gen.extract_datetime(sid)
        
        self.assertIsInstance(dt, datetime)
        # 时间应该在当前时间附近
        now = datetime.now(timezone.utc)
        diff = abs((dt - now).total_seconds())
        self.assertLess(diff, 1)
    
    def test_extract_datacenter_and_worker(self):
        """测试提取数据中心和工作节点ID"""
        gen = SnowflakeGenerator(datacenter_id=7, worker_id=11)
        sid = gen.generate()
        
        self.assertEqual(gen.extract_datacenter_id(sid), 7)
        self.assertEqual(gen.extract_worker_id(sid), 11)
    
    def test_extract_sequence(self):
        """测试提取序列号"""
        gen = SnowflakeGenerator()
        sid = gen.generate()
        sequence = gen.extract_sequence(sid)
        
        self.assertGreaterEqual(sequence, 0)
        self.assertLessEqual(sequence, SnowflakeConfig.MAX_SEQUENCE)
    
    def test_compare_ids(self):
        """测试ID比较"""
        gen = SnowflakeGenerator()
        id1 = gen.generate()
        id2 = gen.generate()
        
        self.assertEqual(gen.compare_ids(id1, id1), 0)
        self.assertEqual(gen.compare_ids(id1, id2), -1)
        self.assertEqual(gen.compare_ids(id2, id1), 1)
    
    def test_ids_in_range(self):
        """测试时间范围内的ID边界"""
        gen = SnowflakeGenerator()
        
        now = datetime.now(timezone.utc)
        start = now - timedelta(hours=1)
        end = now + timedelta(hours=1)
        
        start_id, end_id = gen.ids_in_range(start, end)
        
        # 生成一个当前ID，应该在范围内
        current_id = gen.generate()
        self.assertGreaterEqual(current_id, start_id)
        self.assertLessEqual(current_id, end_id)
    
    def test_custom_epoch(self):
        """测试自定义epoch"""
        custom_epoch = int(datetime(2020, 1, 1, tzinfo=timezone.utc).timestamp() * 1000)
        gen = SnowflakeGenerator(epoch=custom_epoch)
        
        self.assertEqual(gen.epoch, custom_epoch)
        
        sid = gen.generate()
        info = gen.decompose(sid)
        self.assertEqual(info['epoch'], custom_epoch)
    
    def test_epoch_datetime(self):
        """测试epoch_datetime属性"""
        gen = SnowflakeGenerator()
        epoch_dt = gen.epoch_datetime
        
        self.assertIsInstance(epoch_dt, datetime)
        expected = datetime.fromtimestamp(
            SnowflakeConfig.DEFAULT_EPOCH / 1000.0,
            tz=timezone.utc
        )
        self.assertEqual(epoch_dt, expected)
    
    def test_repr(self):
        """测试字符串表示"""
        gen = SnowflakeGenerator(datacenter_id=1, worker_id=2)
        repr_str = repr(gen)
        
        self.assertIn("SnowflakeGenerator", repr_str)
        self.assertIn("datacenter_id=1", repr_str)
        self.assertIn("worker_id=2", repr_str)


class TestSnowflakeGeneratorThreadSafety(unittest.TestCase):
    """测试线程安全性"""
    
    def test_concurrent_generation(self):
        """测试并发生成ID"""
        gen = SnowflakeGenerator(datacenter_id=1, worker_id=1)
        ids: List[int] = []
        lock = threading.Lock()
        
        def generate_ids():
            for _ in range(100):
                sid = gen.generate()
                with lock:
                    ids.append(sid)
        
        threads = [threading.Thread(target=generate_ids) for _ in range(10)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        
        # 所有ID应该唯一
        self.assertEqual(len(ids), 1000)
        self.assertEqual(len(set(ids)), 1000)
    
    def test_concurrent_order(self):
        """测试并发生成的ID仍然有序"""
        gen = SnowflakeGenerator(datacenter_id=1, worker_id=1)
        ids: List[int] = []
        lock = threading.Lock()
        
        def generate_ids():
            for _ in range(50):
                sid = gen.generate()
                with lock:
                    ids.append(sid)
        
        threads = [threading.Thread(target=generate_ids) for _ in range(2)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        
        # 按生成顺序排序后应该是有序的
        sorted_ids = sorted(ids)
        for i in range(len(sorted_ids) - 1):
            self.assertLess(sorted_ids[i], sorted_ids[i + 1])


class TestDiscordSnowflake(unittest.TestCase):
    """测试Discord Snowflake"""
    
    def test_discord_epoch(self):
        """测试Discord epoch"""
        self.assertEqual(DiscordSnowflake.DISCORD_EPOCH, 1420070400000)
        
        # 验证epoch时间是2015-01-01 00:00:00 UTC
        expected = datetime(2015, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
        actual = datetime.fromtimestamp(
            DiscordSnowflake.DISCORD_EPOCH / 1000.0,
            tz=timezone.utc
        )
        self.assertEqual(actual, expected)
    
    def test_discord_generator(self):
        """测试Discord生成器"""
        gen = DiscordSnowflake(worker_id=1)
        sid = gen.generate()
        
        self.assertIsInstance(sid, int)
        self.assertGreater(sid, 0)
    
    def test_discord_generate_str(self):
        """测试生成字符串形式"""
        gen = DiscordSnowflake(worker_id=1)
        sid_str = gen.generate_str()
        
        self.assertIsInstance(sid_str, str)
        # 应该能转换为整数
        int(sid_str)
    
    def test_discord_get_creation_time(self):
        """测试从Discord ID获取创建时间"""
        gen = DiscordSnowflake(worker_id=1)
        sid = gen.generate()
        
        creation_time = DiscordSnowflake.get_creation_time(sid)
        
        self.assertIsInstance(creation_time, datetime)
        # 创建时间应该在当前时间附近
        now = datetime.now(timezone.utc)
        diff = abs((creation_time - now).total_seconds())
        self.assertLess(diff, 1)
    
    def test_discord_get_creation_time_from_string(self):
        """测试从字符串Discord ID获取创建时间"""
        gen = DiscordSnowflake(worker_id=1)
        sid = gen.generate()
        
        creation_time = DiscordSnowflake.get_creation_time(str(sid))
        
        self.assertIsInstance(creation_time, datetime)


class TestTwitterSnowflake(unittest.TestCase):
    """测试Twitter Snowflake"""
    
    def test_twitter_epoch(self):
        """测试Twitter epoch"""
        self.assertEqual(TwitterSnowflake.TWITTER_EPOCH, 1288834974657)
    
    def test_twitter_generator(self):
        """测试Twitter生成器"""
        gen = TwitterSnowflake(datacenter_id=1, worker_id=1)
        sid = gen.generate()
        
        self.assertIsInstance(sid, int)
        self.assertGreater(sid, 0)
    
    def test_twitter_get_creation_time(self):
        """测试从Twitter ID获取创建时间"""
        gen = TwitterSnowflake(datacenter_id=1, worker_id=1)
        sid = gen.generate()
        
        creation_time = TwitterSnowflake.get_creation_time(sid)
        
        self.assertIsInstance(creation_time, datetime)


class TestConvenienceFunctions(unittest.TestCase):
    """测试便捷函数"""
    
    def test_generate_id(self):
        """测试generate_id函数"""
        sid = generate_id()
        self.assertIsInstance(sid, int)
        self.assertGreater(sid, 0)
    
    def test_generate_batch(self):
        """测试generate_batch函数"""
        ids = generate_batch(10)
        self.assertEqual(len(ids), 10)
        self.assertEqual(len(set(ids)), 10)
    
    def test_decompose_id(self):
        """测试decompose_id函数"""
        sid = generate_id()
        info = decompose_id(sid)
        
        self.assertEqual(info['id'], sid)
        self.assertIn('timestamp', info)
        self.assertIn('datetime', info)
        self.assertIn('datacenter_id', info)
        self.assertIn('worker_id', info)
        self.assertIn('sequence', info)
    
    def test_extract_timestamp(self):
        """测试extract_timestamp函数"""
        sid = generate_id()
        timestamp = extract_timestamp(sid)
        
        self.assertIsInstance(timestamp, int)
        current = int(time.time() * 1000)
        self.assertLess(abs(timestamp - current), 1000)
    
    def test_extract_datetime(self):
        """测试extract_datetime函数"""
        sid = generate_id()
        dt = extract_datetime(sid)
        
        self.assertIsInstance(dt, datetime)
    
    def test_create_generator(self):
        """测试create_generator函数"""
        gen = create_generator(datacenter_id=5, worker_id=10)
        
        self.assertIsInstance(gen, SnowflakeGenerator)
        self.assertEqual(gen.datacenter_id, 5)
        self.assertEqual(gen.worker_id, 10)
    
    def test_get_default_generator(self):
        """测试get_default_generator函数"""
        gen1 = get_default_generator()
        gen2 = get_default_generator()
        
        self.assertIs(gen1, gen2)


class TestPerformance(unittest.TestCase):
    """性能测试"""
    
    def test_generation_speed(self):
        """测试生成速度"""
        gen = SnowflakeGenerator(datacenter_id=1, worker_id=1)
        
        start = time.time()
        count = 10000
        for _ in range(count):
            gen.generate()
        elapsed = time.time() - start
        
        # 应该每秒至少生成10万个ID
        ids_per_second = count / elapsed
        self.assertGreater(ids_per_second, 100000, 
            f"生成速度太慢: {ids_per_second:.0f} IDs/秒")
        
        print(f"\n生成速度: {ids_per_second:.0f} IDs/秒")


class TestEdgeCases(unittest.TestCase):
    """边界条件测试"""
    
    def test_max_datacenter_id(self):
        """测试最大数据中心ID"""
        gen = SnowflakeGenerator(datacenter_id=31)
        sid = gen.generate()
        info = gen.decompose(sid)
        self.assertEqual(info['datacenter_id'], 31)
    
    def test_max_worker_id(self):
        """测试最大工作节点ID"""
        gen = SnowflakeGenerator(worker_id=31)
        sid = gen.generate()
        info = gen.decompose(sid)
        self.assertEqual(info['worker_id'], 31)
    
    def test_both_max_ids(self):
        """测试数据中心和工作节点都取最大值"""
        gen = SnowflakeGenerator(datacenter_id=31, worker_id=31)
        ids = [gen.generate() for _ in range(100)]
        
        for sid in ids:
            info = gen.decompose(sid)
            self.assertEqual(info['datacenter_id'], 31)
            self.assertEqual(info['worker_id'], 31)
    
    def test_sequence_overflow(self):
        """测试序列号溢出处理"""
        gen = SnowflakeGenerator()
        
        # 快速生成超过序列号上限的ID
        # 序列号上限是4095，我们生成更多
        ids = [gen.generate() for _ in range(5000)]
        
        # 所有ID应该唯一
        self.assertEqual(len(set(ids)), 5000)
    
    def test_multiple_generators_different_datacenter(self):
        """测试不同数据中心的生成器"""
        gen1 = SnowflakeGenerator(datacenter_id=1, worker_id=1)
        gen2 = SnowflakeGenerator(datacenter_id=2, worker_id=1)
        
        sid1 = gen1.generate()
        sid2 = gen2.generate()
        
        # ID应该不同
        self.assertNotEqual(sid1, sid2)
        
        # 数据中心ID应该正确
        self.assertEqual(gen1.extract_datacenter_id(sid1), 1)
        self.assertEqual(gen2.extract_datacenter_id(sid2), 2)
    
    def test_multiple_generators_different_worker(self):
        """测试不同工作节点的生成器"""
        gen1 = SnowflakeGenerator(datacenter_id=1, worker_id=1)
        gen2 = SnowflakeGenerator(datacenter_id=1, worker_id=2)
        
        sid1 = gen1.generate()
        sid2 = gen2.generate()
        
        # ID应该不同
        self.assertNotEqual(sid1, sid2)
        
        # 工作节点ID应该正确
        self.assertEqual(gen1.extract_worker_id(sid1), 1)
        self.assertEqual(gen2.extract_worker_id(sid2), 2)


if __name__ == "__main__":
    unittest.main(verbosity=2)