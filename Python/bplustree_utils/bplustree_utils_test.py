"""
B+树工具模块测试
B+ Tree Utilities Test Suite
"""

import unittest
import random
import pickle
import json
from mod import (
    BPlusTree, LeafNode, InternalNode,
    bulk_load, merge_trees, get_tree_stats
)


class TestBPlusTreeBasic(unittest.TestCase):
    """基础功能测试"""
    
    def test_create_tree(self):
        """测试创建B+树"""
        tree = BPlusTree(order=4)
        self.assertEqual(tree.size, 0)
        self.assertTrue(tree.is_empty)
        self.assertEqual(tree.height, 0)
    
    def test_create_tree_invalid_order(self):
        """测试无效阶数"""
        with self.assertRaises(ValueError):
            BPlusTree(order=2)
        with self.assertRaises(ValueError):
            BPlusTree(order=1)
    
    def test_insert_single(self):
        """测试插入单个键值对"""
        tree = BPlusTree(order=4)
        tree.insert(10, "value10")
        
        self.assertEqual(tree.size, 1)
        self.assertEqual(tree.get(10), "value10")
        self.assertTrue(tree.contains(10))
    
    def test_insert_multiple(self):
        """测试插入多个键值对"""
        tree = BPlusTree(order=4)
        items = [(i, f"value{i}") for i in range(10)]
        
        for key, value in items:
            tree.insert(key, value)
        
        self.assertEqual(tree.size, 10)
        
        for key, value in items:
            self.assertEqual(tree.get(key), value)
    
    def test_insert_update(self):
        """测试更新已存在的键"""
        tree = BPlusTree(order=4)
        tree.insert(1, "old")
        tree.insert(1, "new")
        
        self.assertEqual(tree.size, 1)
        self.assertEqual(tree.get(1), "new")
    
    def test_insert_random(self):
        """测试随机插入"""
        tree = BPlusTree(order=5)
        items = list(range(100))
        random.shuffle(items)
        
        for i in items:
            tree.insert(i, f"value{i}")
        
        self.assertEqual(tree.size, 100)
        
        # 验证所有键值对
        for i in range(100):
            self.assertEqual(tree.get(i), f"value{i}")
    
    def test_bracket_operator(self):
        """测试 [] 操作符"""
        tree = BPlusTree(order=4)
        tree[1] = "one"
        
        self.assertEqual(tree[1], "one")
        self.assertIn(1, tree)
    
    def test_key_error(self):
        """测试不存在的键抛出KeyError"""
        tree = BPlusTree(order=4)
        
        with self.assertRaises(KeyError):
            _ = tree[100]
    
    def test_string_keys(self):
        """测试字符串键"""
        tree = BPlusTree(order=4)
        tree.insert("apple", 1)
        tree.insert("banana", 2)
        tree.insert("cherry", 3)
        
        self.assertEqual(tree.get("apple"), 1)
        self.assertEqual(tree.get("banana"), 2)
        self.assertEqual(tree.get("cherry"), 3)


class TestBPlusTreeSplit(unittest.TestCase):
    """节点分裂测试"""
    
    def test_leaf_split(self):
        """测试叶节点分裂"""
        tree = BPlusTree(order=4)  # 最多3个键
        
        # 插入足够多的键触发分裂
        for i in range(10):
            tree.insert(i, f"value{i}")
        
        self.assertEqual(tree.size, 10)
        
        # 验证树结构有效
        for i in range(10):
            self.assertEqual(tree.get(i), f"value{i}")
    
    def test_internal_split(self):
        """测试内部节点分裂"""
        tree = BPlusTree(order=3)  # 小阶数更容易触发多层分裂
        
        # 插入大量数据
        for i in range(50):
            tree.insert(i, f"value{i}")
        
        self.assertEqual(tree.size, 50)
        self.assertGreater(tree.height, 1)
        
        # 验证所有数据
        for i in range(50):
            self.assertEqual(tree.get(i), f"value{i}")
    
    def test_descending_insert(self):
        """测试降序插入（触发不同的分裂模式）"""
        tree = BPlusTree(order=4)
        
        for i in range(20, 0, -1):
            tree.insert(i, f"value{i}")
        
        self.assertEqual(tree.size, 20)
        
        for i in range(1, 21):
            self.assertEqual(tree.get(i), f"value{i}")


class TestBPlusTreeDelete(unittest.TestCase):
    """删除操作测试"""
    
    def test_delete_single(self):
        """测试删除单个键"""
        tree = BPlusTree(order=4)
        tree.insert(1, "one")
        
        self.assertTrue(tree.delete(1))
        self.assertEqual(tree.size, 0)
        self.assertIsNone(tree.get(1))
    
    def test_delete_nonexistent(self):
        """测试删除不存在的键"""
        tree = BPlusTree(order=4)
        tree.insert(1, "one")
        
        self.assertFalse(tree.delete(100))
        self.assertEqual(tree.size, 1)
    
    def test_delete_multiple(self):
        """测试删除多个键"""
        tree = BPlusTree(order=4)
        
        for i in range(20):
            tree.insert(i, f"value{i}")
        
        # 删除一半的键
        for i in range(0, 20, 2):
            self.assertTrue(tree.delete(i))
        
        self.assertEqual(tree.size, 10)
        
        # 验证删除的键不存在
        for i in range(0, 20, 2):
            self.assertIsNone(tree.get(i))
        
        # 验证其他键仍然存在
        for i in range(1, 20, 2):
            self.assertEqual(tree.get(i), f"value{i}")
    
    def test_del_operator(self):
        """测试 del 操作符"""
        tree = BPlusTree(order=4)
        tree[1] = "one"
        
        del tree[1]
        
        self.assertEqual(tree.size, 0)
        self.assertIsNone(tree.get(1))
    
    def test_clear(self):
        """测试清空树"""
        tree = BPlusTree(order=4)
        
        for i in range(100):
            tree.insert(i, f"value{i}")
        
        tree.clear()
        
        self.assertEqual(tree.size, 0)
        self.assertTrue(tree.is_empty)


class TestBPlusTreeRangeQuery(unittest.TestCase):
    """范围查询测试"""
    
    def test_range_query_basic(self):
        """测试基本范围查询"""
        tree = BPlusTree(order=4)
        
        for i in range(100):
            tree.insert(i, f"value{i}")
        
        results = tree.range_query(10, 20)
        self.assertEqual(len(results), 11)
        
        for i in range(10, 21):
            self.assertIn((i, f"value{i}"), results)
    
    def test_range_query_exclusive(self):
        """测试排除边界的范围查询"""
        tree = BPlusTree(order=4)
        
        for i in range(100):
            tree.insert(i, f"value{i}")
        
        # 排除起始
        results = tree.range_query(10, 20, include_start=False)
        self.assertNotIn((10, "value10"), results)
        self.assertIn((11, "value11"), results)
        
        # 排除结束
        results = tree.range_query(10, 20, include_end=False)
        self.assertIn((10, "value10"), results)
        self.assertNotIn((20, "value20"), results)
        
        # 排除两边
        results = tree.range_query(10, 20, include_start=False, include_end=False)
        self.assertNotIn((10, "value10"), results)
        self.assertNotIn((20, "value20"), results)
    
    def test_range_query_empty(self):
        """测试空范围查询"""
        tree = BPlusTree(order=4)
        
        for i in range(10):
            tree.insert(i, f"value{i}")
        
        results = tree.range_query(100, 200)
        self.assertEqual(len(results), 0)
    
    def test_range_query_single(self):
        """测试单点范围查询"""
        tree = BPlusTree(order=4)
        
        for i in range(100):
            tree.insert(i, f"value{i}")
        
        results = tree.range_query(50, 50)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0], (50, "value50"))


class TestBPlusTreeNavigation(unittest.TestCase):
    """遍历和导航测试"""
    
    def test_get_all(self):
        """测试获取所有键值对"""
        tree = BPlusTree(order=4)
        items = [(3, "c"), (1, "a"), (2, "b")]
        
        for key, value in items:
            tree.insert(key, value)
        
        results = tree.get_all()
        self.assertEqual(len(results), 3)
        
        # 验证按键排序
        self.assertEqual(results[0], (1, "a"))
        self.assertEqual(results[1], (2, "b"))
        self.assertEqual(results[2], (3, "c"))
    
    def test_get_keys_values(self):
        """测试获取键和值"""
        tree = BPlusTree(order=4)
        
        for i in range(10):
            tree.insert(i, f"value{i}")
        
        keys = tree.get_keys()
        values = tree.get_values()
        
        self.assertEqual(keys, list(range(10)))
        self.assertEqual(values, [f"value{i}" for i in range(10)])
    
    def test_get_min_max(self):
        """测试获取最小最大键"""
        tree = BPlusTree(order=4)
        
        items = [(5, "e"), (1, "a"), (9, "i"), (3, "c")]
        for key, value in items:
            tree.insert(key, value)
        
        self.assertEqual(tree.get_min(), (1, "a"))
        self.assertEqual(tree.get_max(), (9, "i"))
    
    def test_get_min_max_empty(self):
        """测试空树的最小最大键"""
        tree = BPlusTree(order=4)
        
        self.assertIsNone(tree.get_min())
        self.assertIsNone(tree.get_max())
    
    def test_iteration(self):
        """测试迭代"""
        tree = BPlusTree(order=4)
        
        for i in range(10):
            tree.insert(i, f"value{i}")
        
        results = list(tree)
        self.assertEqual(len(results), 10)
        
        # 验证排序
        for i, (key, value) in enumerate(results):
            self.assertEqual(key, i)
            self.assertEqual(value, f"value{i}")
    
    def test_iterate_keys_values(self):
        """测试键和值的迭代器"""
        tree = BPlusTree(order=4)
        
        for i in range(5):
            tree.insert(i, f"value{i}")
        
        keys = list(tree.iterate_keys())
        values = list(tree.iterate_values())
        
        self.assertEqual(keys, [0, 1, 2, 3, 4])
        self.assertEqual(values, [f"value{i}" for i in range(5)])


class TestBPlusTreeSerialization(unittest.TestCase):
    """序列化测试"""
    
    def test_to_dict(self):
        """测试转换为字典"""
        tree = BPlusTree(order=4)
        
        for i in range(10):
            tree.insert(i, f"value{i}")
        
        data = tree.to_dict()
        
        self.assertEqual(data['order'], 4)
        self.assertEqual(data['size'], 10)
        self.assertEqual(len(data['items']), 10)
    
    def test_from_dict(self):
        """测试从字典创建"""
        original = BPlusTree(order=4)
        
        for i in range(10):
            original.insert(i, f"value{i}")
        
        data = original.to_dict()
        tree = BPlusTree.from_dict(data)
        
        self.assertEqual(tree.size, 10)
        self.assertEqual(tree.order, 4)
        
        for i in range(10):
            self.assertEqual(tree.get(i), f"value{i}")
    
    def test_json_serialization(self):
        """测试JSON序列化"""
        tree = BPlusTree(order=4)
        
        for i in range(5):
            tree.insert(i, f"value{i}")
        
        json_str = tree.to_json()
        restored = BPlusTree.from_json(json_str)
        
        self.assertEqual(restored.size, 5)
        
        for i in range(5):
            self.assertEqual(restored.get(i), f"value{i}")
    
    def test_pickle_serialization(self):
        """测试pickle序列化"""
        tree = BPlusTree(order=4)
        
        for i in range(10):
            tree.insert(i, f"value{i}")
        
        data = tree.to_pickle()
        restored = BPlusTree.from_pickle(data)
        
        self.assertEqual(restored.size, 10)
        
        for i in range(10):
            self.assertEqual(restored.get(i), f"value{i}")


class TestBPlusTreeValidation(unittest.TestCase):
    """验证测试"""
    
    def test_validate_empty(self):
        """测试空树验证"""
        tree = BPlusTree(order=4)
        self.assertTrue(tree.validate())
    
    def test_validate_single(self):
        """测试单元素树验证"""
        tree = BPlusTree(order=4)
        tree.insert(1, "one")
        self.assertTrue(tree.validate())
    
    def test_validate_multiple(self):
        """测试多元素树验证"""
        tree = BPlusTree(order=4)
        
        for i in range(100):
            tree.insert(i, f"value{i}")
        
        self.assertTrue(tree.validate())
    
    def test_validate_random(self):
        """测试随机插入后的验证"""
        tree = BPlusTree(order=5)
        items = list(range(100))
        random.shuffle(items)
        
        for i in items:
            tree.insert(i, f"value{i}")
        
        self.assertTrue(tree.validate())


class TestBulkOperations(unittest.TestCase):
    """批量操作测试"""
    
    def test_bulk_load(self):
        """测试批量加载"""
        items = [(i, f"value{i}") for i in range(1000)]
        tree = bulk_load(items)
        
        self.assertEqual(tree.size, 1000)
        
        for i in range(1000):
            self.assertEqual(tree.get(i), f"value{i}")
    
    def test_merge_trees(self):
        """测试合并树"""
        tree1 = BPlusTree(order=4)
        tree2 = BPlusTree(order=4)
        
        for i in range(10):
            tree1.insert(i, f"tree1_{i}")
        
        for i in range(5, 15):
            tree2.insert(i, f"tree2_{i}")
        
        merged = merge_trees(tree1, tree2)
        
        self.assertEqual(merged.size, 15)
        
        # tree2 的值覆盖 tree1 的重叠键
        self.assertEqual(merged.get(5), "tree2_5")
        self.assertEqual(merged.get(14), "tree2_14")
        self.assertEqual(merged.get(0), "tree1_0")


class TestTreeStats(unittest.TestCase):
    """统计信息测试"""
    
    def test_stats_empty(self):
        """测试空树统计"""
        tree = BPlusTree(order=4)
        stats = get_tree_stats(tree)
        
        self.assertEqual(stats['size'], 0)
        self.assertEqual(stats['height'], 0)
        self.assertEqual(stats['leaf_count'], 0)
    
    def test_stats_single(self):
        """测试单元素树统计"""
        tree = BPlusTree(order=4)
        tree.insert(1, "one")
        stats = get_tree_stats(tree)
        
        self.assertEqual(stats['size'], 1)
        self.assertEqual(stats['height'], 1)
        self.assertEqual(stats['leaf_count'], 1)
    
    def test_stats_large(self):
        """测试大树统计"""
        tree = BPlusTree(order=4)
        
        for i in range(100):
            tree.insert(i, f"value{i}")
        
        stats = get_tree_stats(tree)
        
        self.assertEqual(stats['size'], 100)
        self.assertGreater(stats['height'], 0)
        self.assertGreater(stats['leaf_count'], 0)


class TestBPlusTreeEdgeCases(unittest.TestCase):
    """边界情况测试"""
    
    def test_negative_keys(self):
        """测试负数键"""
        tree = BPlusTree(order=4)
        
        for i in range(-10, 10):
            tree.insert(i, f"value{i}")
        
        self.assertEqual(tree.size, 20)
        
        for i in range(-10, 10):
            self.assertEqual(tree.get(i), f"value{i}")
    
    def test_float_keys(self):
        """测试浮点数键"""
        tree = BPlusTree(order=4)
        
        for i in range(10):
            tree.insert(i * 0.5, f"value{i}")
        
        self.assertEqual(tree.size, 10)
        self.assertEqual(tree.get(0.0), "value0")
        self.assertEqual(tree.get(2.0), "value4")
    
    def test_tuple_keys(self):
        """测试元组键"""
        tree = BPlusTree(order=4)
        
        tree.insert((1, "a"), "first")
        tree.insert((1, "b"), "second")
        tree.insert((2, "a"), "third")
        
        self.assertEqual(tree.get((1, "a")), "first")
        self.assertEqual(tree.get((1, "b")), "second")
        self.assertEqual(tree.get((2, "a")), "third")
    
    def test_large_values(self):
        """测试大值"""
        tree = BPlusTree(order=4)
        
        large_value = "x" * 10000
        tree.insert(1, large_value)
        
        self.assertEqual(tree.get(1), large_value)
    
    def test_none_values(self):
        """测试None值"""
        tree = BPlusTree(order=4)
        
        tree.insert(1, None)
        tree.insert(2, "two")
        
        self.assertIsNone(tree.get(1))
        self.assertEqual(tree.get(2), "two")
    
    def test_duplicate_insert(self):
        """测试重复插入"""
        tree = BPlusTree(order=4)
        
        tree.insert(1, "first")
        tree.insert(1, "second")
        tree.insert(1, "third")
        
        self.assertEqual(tree.size, 1)
        self.assertEqual(tree.get(1), "third")


class TestBPlusTreeStress(unittest.TestCase):
    """压力测试"""
    
    def test_large_scale_insert(self):
        """测试大规模插入"""
        tree = BPlusTree(order=64)
        
        for i in range(10000):
            tree.insert(i, f"value{i}")
        
        self.assertEqual(tree.size, 10000)
        self.assertTrue(tree.validate())
    
    def test_large_scale_mixed(self):
        """测试大规模混合操作"""
        tree = BPlusTree(order=32)
        items = {}
        
        # 插入
        for i in range(1000):
            key = random.randint(0, 2000)
            value = f"value{key}_{random.randint(0, 100)}"
            tree.insert(key, value)
            items[key] = value
        
        # 删除一半
        keys_to_delete = random.sample(list(items.keys()), len(items) // 2)
        for key in keys_to_delete:
            tree.delete(key)
            del items[key]
        
        # 验证
        for key, value in items.items():
            self.assertEqual(tree.get(key), value)
        
        self.assertEqual(tree.size, len(items))
    
    def test_sequential_access(self):
        """测试顺序访问"""
        tree = BPlusTree(order=16)
        
        for i in range(1000):
            tree.insert(i, f"value{i}")
        
        # 顺序读取
        for i in range(1000):
            self.assertEqual(tree.get(i), f"value{i}")
        
        # 范围查询
        results = tree.range_query(100, 200)
        self.assertEqual(len(results), 101)


if __name__ == "__main__":
    unittest.main(verbosity=2)