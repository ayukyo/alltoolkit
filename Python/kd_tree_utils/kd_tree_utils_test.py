"""
KD树工具模块测试
"""

import unittest
import math
import random
from mod import (
    KDTree, KDNode, create_kd_tree, nearest_neighbor_search,
    KDTreeBuilder
)


class TestKDNode(unittest.TestCase):
    """KDNode测试"""
    
    def test_create_node(self):
        """测试创建节点"""
        node = KDNode(point=[1, 2, 3], data="test", axis=0)
        self.assertEqual(node.point, [1, 2, 3])
        self.assertEqual(node.data, "test")
        self.assertEqual(node.axis, 0)
        self.assertIsNone(node.left)
        self.assertIsNone(node.right)
    
    def test_node_repr(self):
        """测试节点字符串表示"""
        node = KDNode(point=[1, 2], data="data")
        self.assertIn("point=[1, 2]", repr(node))
        self.assertIn("data=data", repr(node))


class TestKDTree(unittest.TestCase):
    """KDTree测试"""
    
    def test_create_tree(self):
        """测试创建树"""
        tree = KDTree(dimension=2)
        self.assertEqual(tree.dimension, 2)
        self.assertEqual(tree.size(), 0)
        self.assertTrue(tree.is_empty())
    
    def test_create_tree_invalid_dimension(self):
        """测试无效维度"""
        with self.assertRaises(ValueError):
            KDTree(dimension=0)
        with self.assertRaises(ValueError):
            KDTree(dimension=-1)
    
    def test_insert_single_point(self):
        """测试插入单个点"""
        tree = KDTree(dimension=2)
        tree.insert([1, 2], data="test")
        self.assertEqual(tree.size(), 1)
        self.assertFalse(tree.is_empty())
    
    def test_insert_multiple_points(self):
        """测试插入多个点"""
        tree = KDTree(dimension=2)
        points = [[1, 2], [3, 4], [5, 6], [7, 8]]
        for p in points:
            tree.insert(p)
        self.assertEqual(tree.size(), 4)
    
    def test_insert_invalid_dimension(self):
        """测试插入维度错误的点"""
        tree = KDTree(dimension=2)
        with self.assertRaises(ValueError):
            tree.insert([1, 2, 3])  # 3维点插入2维树
    
    def test_build_balanced_tree(self):
        """测试构建平衡树"""
        tree = KDTree(dimension=2)
        points = [([i, i], f"point_{i}") for i in range(10)]
        tree.build(points)
        self.assertEqual(tree.size(), 10)
    
    def test_nearest_neighbor_empty_tree(self):
        """测试空树的最近邻"""
        tree = KDTree(dimension=2)
        result = tree.nearest_neighbor([1, 1])
        self.assertIsNone(result)
    
    def test_nearest_neighbor_single_point(self):
        """测试单点的最近邻"""
        tree = KDTree(dimension=2)
        tree.insert([1, 1], "A")
        result = tree.nearest_neighbor([2, 2])
        self.assertIsNotNone(result)
        self.assertEqual(result[0], [1, 1])
        self.assertEqual(result[1], "A")
        self.assertAlmostEqual(result[2], math.sqrt(2), places=5)
    
    def test_nearest_neighbor_multiple_points(self):
        """测试多点的最近邻"""
        tree = KDTree(dimension=2)
        tree.insert([0, 0], "A")
        tree.insert([10, 10], "B")
        tree.insert([5, 5], "C")
        
        result = tree.nearest_neighbor([4, 4])
        self.assertIsNotNone(result)
        self.assertEqual(result[0], [5, 5])
    
    def test_nearest_neighbor_exact_match(self):
        """测试查询点存在于树中"""
        tree = KDTree(dimension=2)
        tree.insert([3, 3], "target")
        tree.insert([1, 1], "other")
        
        result = tree.nearest_neighbor([3, 3])
        self.assertIsNotNone(result)
        self.assertEqual(result[0], [3, 3])
        self.assertEqual(result[1], "target")
        self.assertAlmostEqual(result[2], 0, places=5)
    
    def test_k_nearest_neighbors(self):
        """测试k近邻查询"""
        tree = KDTree(dimension=2)
        points = [[0, 0], [1, 1], [2, 2], [3, 3], [10, 10]]
        for p in points:
            tree.insert(p)
        
        neighbors = tree.k_nearest_neighbors([2, 2], 3)
        self.assertEqual(len(neighbors), 3)
        # 最近的是[2, 2]自己
        self.assertEqual(neighbors[0][0], [2, 2])
        self.assertAlmostEqual(neighbors[0][2], 0, places=5)
    
    def test_k_nearest_neighbors_k_larger_than_size(self):
        """测试k大于树大小时"""
        tree = KDTree(dimension=2)
        tree.insert([1, 1])
        tree.insert([2, 2])
        
        neighbors = tree.k_nearest_neighbors([0, 0], 10)
        self.assertEqual(len(neighbors), 2)
    
    def test_k_nearest_neighbors_empty_tree(self):
        """测试空树的k近邻"""
        tree = KDTree(dimension=2)
        neighbors = tree.k_nearest_neighbors([1, 1], 3)
        self.assertEqual(len(neighbors), 0)
    
    def test_range_query(self):
        """测试范围查询"""
        tree = KDTree(dimension=2)
        tree.insert([1, 1], "A")
        tree.insert([2, 2], "B")
        tree.insert([5, 5], "C")
        tree.insert([6, 6], "D")
        
        result = tree.range_query([(0, 3), (0, 3)])
        self.assertEqual(len(result), 2)
        points = [r[0] for r in result]
        self.assertIn([1, 1], points)
        self.assertIn([2, 2], points)
    
    def test_range_query_no_results(self):
        """测试范围查询无结果"""
        tree = KDTree(dimension=2)
        tree.insert([10, 10])
        
        result = tree.range_query([(0, 5), (0, 5)])
        self.assertEqual(len(result), 0)
    
    def test_range_query_invalid_dimension(self):
        """测试范围查询维度错误"""
        tree = KDTree(dimension=2)
        with self.assertRaises(ValueError):
            tree.range_query([(0, 5)])  # 应该是2个维度
    
    def test_radius_query(self):
        """测试圆形范围查询"""
        tree = KDTree(dimension=2)
        tree.insert([0, 0], "A")
        tree.insert([1, 1], "B")  # 距离[0,0]约1.414
        tree.insert([3, 3], "C")  # 距离[0,0]约4.24
        tree.insert([5, 5], "D")
        
        result = tree.radius_query([0, 0], 2)
        self.assertEqual(len(result), 2)  # A和B
    
    def test_radius_query_empty_tree(self):
        """测试空树圆形查询"""
        tree = KDTree(dimension=2)
        result = tree.radius_query([0, 0], 10)
        self.assertEqual(len(result), 0)
    
    def test_find_existing_point(self):
        """测试查找存在的点"""
        tree = KDTree(dimension=2)
        tree.insert([1, 2], "test")
        
        node = tree.find([1, 2])
        self.assertIsNotNone(node)
        self.assertEqual(node.point, [1, 2])
        self.assertEqual(node.data, "test")
    
    def test_find_non_existing_point(self):
        """测试查找不存在的点"""
        tree = KDTree(dimension=2)
        tree.insert([1, 2])
        
        node = tree.find([3, 4])
        self.assertIsNone(node)
    
    def test_contains(self):
        """测试contains方法"""
        tree = KDTree(dimension=2)
        tree.insert([1, 2])
        
        self.assertTrue(tree.contains([1, 2]))
        self.assertFalse(tree.contains([3, 4]))
    
    def test_delete_leaf(self):
        """测试删除叶子节点"""
        tree = KDTree(dimension=2)
        tree.insert([1, 1], "A")
        tree.insert([3, 3], "B")
        
        self.assertTrue(tree.delete([3, 3]))
        self.assertEqual(tree.size(), 1)
        self.assertFalse(tree.contains([3, 3]))
    
    def test_delete_non_existing(self):
        """测试删除不存在的点"""
        tree = KDTree(dimension=2)
        tree.insert([1, 1])
        
        self.assertFalse(tree.delete([2, 2]))
        self.assertEqual(tree.size(), 1)
    
    def test_delete_from_empty_tree(self):
        """测试从空树删除"""
        tree = KDTree(dimension=2)
        self.assertFalse(tree.delete([1, 1]))
    
    def test_height(self):
        """测试树高度"""
        tree = KDTree(dimension=2)
        self.assertEqual(tree.height(), 0)
        
        tree.insert([1, 1])
        self.assertEqual(tree.height(), 1)
        
        tree.insert([2, 2])
        self.assertGreaterEqual(tree.height(), 2)
    
    def test_is_balanced(self):
        """测试平衡检查"""
        tree = KDTree(dimension=2)
        points = [([i, i], None) for i in range(100)]
        tree.build(points)  # 使用build创建平衡树
        self.assertTrue(tree.is_balanced())
    
    def test_all_points(self):
        """测试获取所有点"""
        tree = KDTree(dimension=2)
        tree.insert([1, 1], "A")
        tree.insert([2, 2], "B")
        tree.insert([3, 3], "C")
        
        all_points = tree.all_points()
        self.assertEqual(len(all_points), 3)
        
        points = [p[0] for p in all_points]
        self.assertIn([1, 1], points)
        self.assertIn([2, 2], points)
        self.assertIn([3, 3], points)
    
    def test_to_dict(self):
        """测试转换为字典"""
        tree = KDTree(dimension=2)
        tree.insert([1, 1], "A")
        
        d = tree.to_dict()
        self.assertEqual(d['dimension'], 2)
        self.assertEqual(d['size'], 1)
        self.assertEqual(d['height'], 1)
        self.assertIsNotNone(d['root'])
    
    def test_len(self):
        """测试__len__"""
        tree = KDTree(dimension=2)
        self.assertEqual(len(tree), 0)
        
        tree.insert([1, 1])
        self.assertEqual(len(tree), 1)
    
    def test_repr(self):
        """测试__repr__"""
        tree = KDTree(dimension=3)
        self.assertIn("dimension=3", repr(tree))
        self.assertIn("size=0", repr(tree))


class TestDistanceMetrics(unittest.TestCase):
    """距离度量测试"""
    
    def test_euclidean_distance(self):
        """测试欧几里得距离"""
        tree = KDTree(dimension=2, distance_metric='euclidean')
        tree.insert([0, 0])
        
        result = tree.nearest_neighbor([3, 4])
        self.assertIsNotNone(result)
        self.assertAlmostEqual(result[2], 5, places=5)
    
    def test_manhattan_distance(self):
        """测试曼哈顿距离"""
        tree = KDTree(dimension=2, distance_metric='manhattan')
        tree.insert([0, 0])
        
        result = tree.nearest_neighbor([3, 4])
        self.assertIsNotNone(result)
        self.assertAlmostEqual(result[2], 7, places=5)  # |3-0| + |4-0| = 7
    
    def test_chebyshev_distance(self):
        """测试切比雪夫距离"""
        tree = KDTree(dimension=2, distance_metric='chebyshev')
        tree.insert([0, 0])
        
        result = tree.nearest_neighbor([3, 4])
        self.assertIsNotNone(result)
        self.assertAlmostEqual(result[2], 4, places=5)  # max(|3-0|, |4-0|) = 4
    
    def test_invalid_distance_metric(self):
        """测试无效距离度量"""
        tree = KDTree(dimension=2, distance_metric='invalid')
        tree.insert([1, 1])
        
        with self.assertRaises(ValueError):
            tree.nearest_neighbor([0, 0])


class TestCreateKDTree(unittest.TestCase):
    """create_kd_tree函数测试"""
    
    def test_create_from_points(self):
        """测试从点列表创建"""
        points = [([1, 1], "A"), ([2, 2], "B"), ([3, 3], "C")]
        tree = create_kd_tree(points)
        
        self.assertEqual(tree.size(), 3)
        self.assertTrue(tree.contains([1, 1]))
        self.assertTrue(tree.contains([2, 2]))
        self.assertTrue(tree.contains([3, 3]))
    
    def test_create_with_dimension(self):
        """测试指定维度创建"""
        points = [([1, 1, 1], "A"), ([2, 2, 2], "B")]
        tree = create_kd_tree(points, dimension=3)
        self.assertEqual(tree.dimension, 3)
    
    def test_create_empty(self):
        """测试空列表"""
        with self.assertRaises(ValueError):
            create_kd_tree([])
    
    def test_create_with_distance_metric(self):
        """测试指定距离度量"""
        points = [([1, 1], None)]
        tree = create_kd_tree(points, distance_metric='manhattan')
        self.assertEqual(tree.distance_metric, 'manhattan')


class TestNearestNeighborSearch(unittest.TestCase):
    """nearest_neighbor_search函数测试"""
    
    def test_basic_search(self):
        """测试基本搜索"""
        points = [[0, 0], [1, 1], [2, 2], [5, 5]]
        result = nearest_neighbor_search(points, [1.5, 1.5], k=2)
        
        self.assertEqual(len(result), 2)
        # [1, 1] 和 [2, 2] 应该是最近的两个
        found_points = [r[0] for r in result]
        self.assertIn([1, 1], found_points)
        self.assertIn([2, 2], found_points)
    
    def test_empty_points(self):
        """测试空点集"""
        result = nearest_neighbor_search([], [0, 0])
        self.assertEqual(len(result), 0)
    
    def test_k_larger_than_points(self):
        """测试k大于点数"""
        points = [[1, 1], [2, 2]]
        result = nearest_neighbor_search(points, [0, 0], k=10)
        self.assertEqual(len(result), 2)


class TestKDTreeBuilder(unittest.TestCase):
    """KDTreeBuilder测试"""
    
    def test_builder_basic(self):
        """测试基本构建"""
        tree = (KDTreeBuilder(2)
            .add([1, 1], "A")
            .add([2, 2], "B")
            .build())
        
        self.assertEqual(tree.size(), 2)
    
    def test_builder_add_many(self):
        """测试批量添加"""
        points = [([3, 3], "C"), ([4, 4], "D")]
        tree = (KDTreeBuilder(2)
            .add([1, 1], "A")
            .add_many(points)
            .build())
        
        self.assertEqual(tree.size(), 3)
    
    def test_builder_clear(self):
        """测试清空"""
        builder = KDTreeBuilder(2).add([1, 1]).add([2, 2])
        builder.clear()
        
        tree = builder.build()
        self.assertEqual(tree.size(), 0)
    
    def test_builder_with_distance_metric(self):
        """测试指定距离度量"""
        tree = (KDTreeBuilder(2, 'manhattan')
            .add([1, 1])
            .build())
        
        self.assertEqual(tree.distance_metric, 'manhattan')


class Test3DTree(unittest.TestCase):
    """3D KD树测试"""
    
    def test_3d_operations(self):
        """测试3D操作"""
        tree = KDTree(dimension=3)
        
        points = [
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9],
            [2, 3, 4],
            [5, 6, 7]
        ]
        
        for p in points:
            tree.insert(p)
        
        self.assertEqual(tree.size(), 5)
        
        # 最近邻 - [2,3,4] 和 [4,5,6] 到 [3,4,5] 距离相同
        result = tree.nearest_neighbor([3, 4, 5])
        self.assertIsNotNone(result)
        # 检查返回的是其中一个最近点
        self.assertIn(result[0], [[2, 3, 4], [4, 5, 6]])
        # 距离应该是 sqrt(3)
        self.assertAlmostEqual(result[2], math.sqrt(3), places=5)
        
        # 范围查询
        range_result = tree.range_query([(1, 5), (2, 6), (3, 7)])
        self.assertGreater(len(range_result), 0)


class TestLargeDataset(unittest.TestCase):
    """大数据集测试"""
    
    def test_large_random_dataset(self):
        """测试大型随机数据集"""
        random.seed(42)
        
        tree = KDTree(dimension=2)
        points = [(random.random() * 100, random.random() * 100) for _ in range(1000)]
        
        for x, y in points:
            tree.insert([x, y])
        
        self.assertEqual(tree.size(), 1000)
        
        # 验证最近邻搜索
        query = [50, 50]
        result = tree.nearest_neighbor(query)
        self.assertIsNotNone(result)
        
        # 验证k近邻
        k_nearest = tree.k_nearest_neighbors(query, 10)
        self.assertEqual(len(k_nearest), 10)
        
        # 验证结果按距离排序
        distances = [n[2] for n in k_nearest]
        self.assertEqual(distances, sorted(distances))
    
    def test_performance_knn(self):
        """测试k近邻性能"""
        random.seed(123)
        
        tree = KDTree(dimension=3)
        points = [[random.random() * 100 for _ in range(3)] for _ in range(500)]
        
        for p in points:
            tree.insert(p)
        
        # 执行多次查询
        for _ in range(50):
            query = [random.random() * 100 for _ in range(3)]
            result = tree.k_nearest_neighbors(query, 5)
            self.assertEqual(len(result), 5)


class TestEdgeCases(unittest.TestCase):
    """边缘情况测试"""
    
    def test_single_dimension(self):
        """测试1维KD树"""
        tree = KDTree(dimension=1)
        tree.insert([1])
        tree.insert([5])
        tree.insert([3])
        
        result = tree.nearest_neighbor([2])
        self.assertIsNotNone(result)
        self.assertEqual(result[0], [1])
    
    def test_high_dimension(self):
        """测试高维KD树"""
        tree = KDTree(dimension=10)
        point1 = [i for i in range(10)]
        point2 = [i + 100 for i in range(10)]
        
        tree.insert(point1)
        tree.insert(point2)
        
        result = tree.nearest_neighbor([5, 5, 5, 5, 5, 5, 5, 5, 5, 5])
        self.assertIsNotNone(result)
        self.assertEqual(result[0], point1)
    
    def test_duplicate_points(self):
        """测试重复点"""
        tree = KDTree(dimension=2)
        tree.insert([1, 1], "first")
        tree.insert([1, 1], "second")
        
        # 应该都能找到
        self.assertEqual(tree.size(), 2)
    
    def test_negative_coordinates(self):
        """测试负坐标"""
        tree = KDTree(dimension=2)
        tree.insert([-5, -5])
        tree.insert([-1, -1])
        tree.insert([5, 5])
        
        result = tree.nearest_neighbor([0, 0])
        self.assertIsNotNone(result)
        self.assertEqual(result[0], [-1, -1])
    
    def test_zero_radius_query(self):
        """测试零半径查询"""
        tree = KDTree(dimension=2)
        tree.insert([1, 1])
        tree.insert([2, 2])
        
        result = tree.radius_query([1, 1], 0)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0][0], [1, 1])
        self.assertAlmostEqual(result[0][2], 0, places=5)


if __name__ == "__main__":
    unittest.main(verbosity=2)