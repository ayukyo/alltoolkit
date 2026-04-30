"""
Pagination Utilities 测试

全面测试所有分页类型和功能。
"""

import unittest
from typing import List, Dict, Any
import sys
import os

# 添加模块路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pagination_utils.mod import (
    PaginationType,
    PageMetadata,
    CursorMetadata,
    PaginatedResult,
    OffsetPaginator,
    CursorPaginator,
    KeysetPaginator,
    InfiniteScrollPaginator,
    Pagination,
    paginate_offset,
    paginate_cursor,
    paginate_infinite,
    page_range,
)


class TestPageMetadata(unittest.TestCase):
    """测试分页元数据"""
    
    def test_page_metadata_creation(self):
        """测试元数据创建"""
        metadata = PageMetadata(
            current_page=3,
            total_pages=10,
            total_items=100,
            items_per_page=10,
            has_previous=True,
            has_next=True,
            previous_page=2,
            next_page=4,
            first_page=1,
            last_page=10,
            start_index=21,
            end_index=30,
        )
        
        self.assertEqual(metadata.current_page, 3)
        self.assertEqual(metadata.total_pages, 10)
        self.assertTrue(metadata.has_previous)
        self.assertTrue(metadata.has_next)
    
    def test_page_metadata_to_dict(self):
        """测试元数据字典转换"""
        metadata = PageMetadata(
            current_page=1,
            total_pages=5,
            total_items=50,
            items_per_page=10,
            has_previous=False,
            has_next=True,
            previous_page=None,
            next_page=2,
        )
        
        result = metadata.to_dict()
        self.assertIsInstance(result, dict)
        self.assertEqual(result['current_page'], 1)
        self.assertEqual(result['total_pages'], 5)
        self.assertFalse(result['has_previous'])


class TestOffsetPaginator(unittest.TestCase):
    """测试偏移量分页器"""
    
    def setUp(self):
        """设置测试数据"""
        self.paginator = OffsetPaginator(items_per_page=10)
        self.items = [f"Item-{i}" for i in range(1, 101)]  # 100 条数据
    
    def test_first_page(self):
        """测试第一页"""
        result = self.paginator.paginate(self.items, page=1)
        
        self.assertEqual(len(result.items), 10)
        self.assertEqual(result.items[0], "Item-1")
        self.assertEqual(result.items[-1], "Item-10")
        self.assertFalse(result.metadata.has_previous)
        self.assertTrue(result.metadata.has_next)
    
    def test_middle_page(self):
        """测试中间页"""
        result = self.paginator.paginate(self.items, page=5)
        
        self.assertEqual(len(result.items), 10)
        self.assertEqual(result.items[0], "Item-41")
        self.assertEqual(result.items[-1], "Item-50")
        self.assertTrue(result.metadata.has_previous)
        self.assertTrue(result.metadata.has_next)
    
    def test_last_page(self):
        """测试最后一页"""
        result = self.paginator.paginate(self.items, page=10)
        
        self.assertEqual(len(result.items), 10)
        self.assertEqual(result.items[0], "Item-91")
        self.assertEqual(result.items[-1], "Item-100")
        self.assertTrue(result.metadata.has_previous)
        self.assertFalse(result.metadata.has_next)
    
    def test_page_overflow(self):
        """测试页码溢出"""
        result = self.paginator.paginate(self.items, page=20)
        
        # 应返回最后一页
        self.assertEqual(result.metadata.current_page, 10)
        self.assertFalse(result.metadata.has_next)
    
    def test_page_underflow(self):
        """测试页码不足"""
        result = self.paginator.paginate(self.items, page=0)
        
        # 应返回第一页
        self.assertEqual(result.metadata.current_page, 1)
        self.assertFalse(result.metadata.has_previous)
    
    def test_custom_per_page(self):
        """测试自定义每页数量"""
        result = self.paginator.paginate(self.items, page=1, per_page=20)
        
        self.assertEqual(len(result.items), 20)
        self.assertEqual(result.metadata.items_per_page, 20)
        self.assertEqual(result.metadata.total_pages, 5)
    
    def test_per_page_max_limit(self):
        """测试每页最大限制"""
        result = self.paginator.paginate(self.items, page=1, per_page=200)
        
        # 应限制到最大值
        self.assertLessEqual(result.metadata.items_per_page, self.paginator.max_items_per_page)
    
    def test_empty_items(self):
        """测试空列表"""
        result = self.paginator.paginate([], page=1)
        
        self.assertEqual(len(result.items), 0)
        self.assertEqual(result.metadata.total_items, 0)
        self.assertEqual(result.metadata.total_pages, 1)
    
    def test_get_offset_limit(self):
        """测试 OFFSET/LIMIT 计算"""
        offset, limit = self.paginator.get_offset_limit(page=5)
        
        self.assertEqual(offset, 40)
        self.assertEqual(limit, 10)
    
    def test_calculate_pages(self):
        """测试页数计算"""
        total_pages = self.paginator.calculate_pages(100)
        self.assertEqual(total_pages, 10)
        
        total_pages = self.paginator.calculate_pages(95)
        self.assertEqual(total_pages, 10)  # ceil
    
    def test_start_end_index(self):
        """测试起始结束索引"""
        result = self.paginator.paginate(self.items, page=5)
        
        self.assertEqual(result.metadata.start_index, 41)
        self.assertEqual(result.metadata.end_index, 50)


class TestCursorPaginator(unittest.TestCase):
    """测试游标分页器"""
    
    def setUp(self):
        """设置测试数据"""
        self.paginator = CursorPaginator(limit=10)
        self.items = [f"Item-{i}" for i in range(1, 101)]
    
    def test_first_page(self):
        """测试第一页"""
        result = self.paginator.paginate(self.items)
        
        self.assertEqual(len(result.items), 10)
        self.assertEqual(result.items[0], "Item-1")
        self.assertTrue(result.metadata.has_more)
        self.assertIsNotNone(result.metadata.next_cursor)
    
    def test_cursor_navigation(self):
        """测试游标导航"""
        # 第一页
        result1 = self.paginator.paginate(self.items)
        
        # 第二页
        cursor = result1.metadata.next_cursor
        result2 = self.paginator.paginate(self.items, cursor=cursor)
        
        self.assertEqual(result2.items[0], "Item-11")
        self.assertEqual(result2.items[-1], "Item-20")
    
    def test_cursor_encoding_decoding(self):
        """测试游标编解码"""
        cursor = self.paginator.encode_cursor(50, 'next')
        decoded = self.paginator.decode_cursor(cursor)
        
        self.assertEqual(decoded['index'], 50)
        self.assertEqual(decoded['direction'], 'next')
    
    def test_backward_navigation(self):
        """测试向后导航"""
        # 先跳到后面
        cursor = self.paginator.encode_cursor(30, 'previous')
        result = self.paginator.paginate(self.items, cursor=cursor, direction='previous')
        
        self.assertEqual(result.items[0], "Item-21")
    
    def test_custom_limit(self):
        """测试自定义限制"""
        result = self.paginator.paginate(self.items, limit=20)
        
        self.assertEqual(len(result.items), 20)
        self.assertEqual(result.metadata.limit, 20)
    
    def test_last_batch(self):
        """测试最后一批"""
        # 跳到接近末尾
        cursor = self.paginator.encode_cursor(95, 'next')
        result = self.paginator.paginate(self.items, cursor=cursor, limit=10)
        
        self.assertEqual(len(result.items), 5)  # 只剩 5 条
        self.assertFalse(result.metadata.has_more)
        self.assertIsNone(result.metadata.next_cursor)
    
    def test_empty_items(self):
        """测试空列表"""
        result = self.paginator.paginate([])
        
        self.assertEqual(len(result.items), 0)
        self.assertFalse(result.metadata.has_more)
    
    def test_get_first_page(self):
        """测试获取第一页"""
        result = self.paginator.get_first_page(self.items)
        
        self.assertEqual(result.items[0], "Item-1")


class TestKeysetPaginator(unittest.TestCase):
    """测试键集分页器"""
    
    def setUp(self):
        """设置测试数据"""
        self.paginator = KeysetPaginator(limit=10, key_field='id')
        # 模拟数据库记录
        self.items = [
            {'id': i, 'name': f'Name-{i}', 'value': i * 10}
            for i in range(1, 101)
        ]
    
    def test_first_page(self):
        """测试第一页"""
        result = self.paginator.paginate(self.items)
        
        self.assertEqual(len(result.items), 10)
        self.assertEqual(result.items[0]['id'], 1)
        self.assertTrue(result.metadata.has_more)
    
    def test_keyset_navigation(self):
        """测试键集导航"""
        # 第一页
        result1 = self.paginator.paginate(self.items)
        
        # 第二页 - 使用最后一条的键作为游标
        cursor = result1.metadata.next_cursor
        result2 = self.paginator.paginate(self.items, cursor=cursor)
        
        self.assertEqual(result2.items[0]['id'], 11)
    
    def test_custom_key_field(self):
        """测试自定义键字段"""
        paginator = KeysetPaginator(limit=10, key_field='value')
        result = paginator.paginate(self.items)
        
        self.assertEqual(result.items[0]['value'], 10)
    
    def test_key_extractor(self):
        """测试键提取器"""
        def extract_id(item):
            return item['id'] * 2
        
        paginator = KeysetPaginator(limit=10, key_extractor=extract_id)
        result = paginator.paginate(self.items)
        
        # 键提取器应该正常工作
        self.assertEqual(len(result.items), 10)
    
    def test_cursor_encode_decode(self):
        """测试游标编解码"""
        cursor = self.paginator.encode_cursor(50)
        key = self.paginator.decode_cursor(cursor)
        
        self.assertEqual(key, 50)
    
    def test_descending_order(self):
        """测试降序"""
        reversed_items = list(reversed(self.items))
        result = self.paginator.paginate(reversed_items, descending=True)
        
        self.assertEqual(result.items[0]['id'], 100)
    
    def test_object_with_attribute(self):
        """测试有属性的对象"""
        class Item:
            def __init__(self, id, name):
                self.id = id
                self.name = name
        
        items = [Item(i, f'Name-{i}') for i in range(1, 21)]
        result = self.paginator.paginate(items)
        
        self.assertEqual(len(result.items), 10)
        self.assertEqual(result.items[0].id, 1)


class TestInfiniteScrollPaginator(unittest.TestCase):
    """测试无限滚动分页器"""
    
    def setUp(self):
        """设置测试数据"""
        self.paginator = InfiniteScrollPaginator(batch_size=10)
        self.items = [f"Item-{i}" for i in range(1, 101)]
    
    def test_initial_load(self):
        """测试初始加载"""
        result = self.paginator.paginate(self.items)
        
        self.assertEqual(len(result.items), 10)
        self.assertEqual(result.items[0], "Item-1")
        self.assertTrue(result.metadata.has_more)
    
    def test_next_batch(self):
        """测试下一批"""
        result = self.paginator.paginate(self.items, loaded_count=10)
        
        self.assertEqual(result.items[0], "Item-11")
        self.assertEqual(len(result.items), 10)
    
    def test_custom_batch_size(self):
        """测试自定义批次大小"""
        result = self.paginator.paginate(self.items, batch_size=20)
        
        self.assertEqual(len(result.items), 20)
    
    def test_get_load_state(self):
        """测试加载状态"""
        state = self.paginator.get_load_state(100, 30)
        
        self.assertEqual(state['total'], 100)
        self.assertEqual(state['loaded'], 30)
        self.assertEqual(state['remaining'], 70)
        self.assertEqual(state['progress'], 0.3)
        self.assertFalse(state['is_complete'])
    
    def test_preload_threshold(self):
        """测试预加载阈值"""
        paginator = InfiniteScrollPaginator(batch_size=10, preload_threshold=5)
        state = paginator.get_load_state(100, 95)
        
        # 剩余 5 条，应该触发预加载
        self.assertTrue(state['should_preload'])
    
    def test_complete_state(self):
        """测试完成状态"""
        state = self.paginator.get_load_state(100, 100)
        
        self.assertEqual(state['remaining'], 0)
        self.assertTrue(state['is_complete'])
    
    def test_last_batch(self):
        """测试最后一批"""
        result = self.paginator.paginate(self.items, loaded_count=95)
        
        self.assertEqual(len(result.items), 5)
        self.assertFalse(result.metadata.has_more)


class TestPaginationClass(unittest.TestCase):
    """测试 Pagination 高级接口"""
    
    def setUp(self):
        """设置测试数据"""
        self.items = [f"Item-{i}" for i in range(1, 101)]
    
    def test_offset_static(self):
        """测试静态偏移量分页"""
        result = Pagination.offset(self.items, page=5, per_page=10)
        
        self.assertEqual(result.pagination_type, PaginationType.OFFSET)
        self.assertEqual(result.metadata.current_page, 5)
    
    def test_cursor_static(self):
        """测试静态游标分页"""
        result = Pagination.cursor(self.items, limit=10)
        
        self.assertEqual(result.pagination_type, PaginationType.CURSOR)
        self.assertIsNotNone(result.metadata.next_cursor)
    
    def test_keyset_static(self):
        """测试静态键集分页"""
        dict_items = [{'id': i, 'name': f'Name-{i}'} for i in range(1, 21)]
        result = Pagination.keyset(dict_items, limit=10, key_field='id')
        
        self.assertEqual(result.pagination_type, PaginationType.KEYSET)
    
    def test_infinite_static(self):
        """测试静态无限滚动"""
        result = Pagination.infinite(self.items, loaded_count=0, batch_size=10)
        
        self.assertEqual(result.pagination_type, PaginationType.INFINITE)
    
    def test_calculate_page_range(self):
        """测试页码范围计算"""
        # 中间页 - max_display=7 显示 7 页，当前页居中
        pages = Pagination.calculate_page_range(5, 20, 7)
        self.assertEqual(pages, [2, 3, 4, 5, 6, 7, 8])
        
        # 首页附近
        pages = Pagination.calculate_page_range(1, 20, 7)
        self.assertEqual(pages, [1, 2, 3, 4, 5, 6, 7])
        
        # 末页附近
        pages = Pagination.calculate_page_range(20, 20, 7)
        self.assertEqual(pages, [14, 15, 16, 17, 18, 19, 20])
        
        # 总页数小于显示数
        pages = Pagination.calculate_page_range(3, 5, 7)
        self.assertEqual(pages, [1, 2, 3, 4, 5])
    
    def test_generate_links(self):
        """测试链接生成"""
        links = Pagination.generate_links('/api/items', 5, 10)
        
        self.assertEqual(links['first'], '/api/items?page=1')
        self.assertEqual(links['last'], '/api/items?page=10')
        self.assertEqual(links['prev'], '/api/items?page=4')
        self.assertEqual(links['next'], '/api/items?page=6')
        self.assertEqual(links['self'], '/api/items?page=5')
    
    def test_generate_header_links(self):
        """测试 HTTP Link Header 生成"""
        header = Pagination.generate_header_links('/api/items', 5, 10)
        
        self.assertIn('rel="first"', header)
        self.assertIn('rel="last"', header)
        self.assertIn('rel="prev"', header)
        self.assertIn('rel="next"', header)
        self.assertIn('rel="self"', header)
    
    def test_first_page_links(self):
        """测试第一页链接"""
        links = Pagination.generate_links('/api/items', 1, 10)
        
        self.assertIsNone(links.get('prev'))
        self.assertIn('next', links)
    
    def test_last_page_links(self):
        """测试最后一页链接"""
        links = Pagination.generate_links('/api/items', 10, 10)
        
        self.assertIsNone(links.get('next'))
        self.assertIn('prev', links)


class TestPaginatedResult(unittest.TestCase):
    """测试分页结果"""
    
    def test_to_dict_with_list_items(self):
        """测试列表项转字典"""
        items = [1, 2, 3]
        result = PaginatedResult(
            items=items,
            metadata=PageMetadata(
                current_page=1,
                total_pages=1,
                total_items=3,
                items_per_page=3,
                has_previous=False,
                has_next=False,
            ),
            pagination_type=PaginationType.OFFSET,
        )
        
        dict_result = result.to_dict()
        self.assertEqual(dict_result['items'], [1, 2, 3])
        self.assertEqual(dict_result['type'], 'offset')
    
    def test_to_dict_with_serializer(self):
        """测试带序列化器"""
        items = [{'id': 1, 'name': 'A'}, {'id': 2, 'name': 'B'}]
        
        def serializer(item):
            return {'id': item['id'], 'label': item['name']}
        
        result = PaginatedResult(
            items=items,
            metadata=PageMetadata(
                current_page=1,
                total_pages=1,
                total_items=2,
                items_per_page=2,
                has_previous=False,
                has_next=False,
            ),
            pagination_type=PaginationType.OFFSET,
        )
        
        dict_result = result.to_dict(item_serializer=serializer)
        self.assertEqual(dict_result['items'][0]['label'], 'A')


class TestConvenienceFunctions(unittest.TestCase):
    """测试便捷函数"""
    
    def test_paginate_offset_function(self):
        """测试偏移量分页函数"""
        items = [i for i in range(100)]
        result = paginate_offset(items, page=2, per_page=20)
        
        self.assertEqual(len(result.items), 20)
        self.assertEqual(result.metadata.current_page, 2)
    
    def test_paginate_cursor_function(self):
        """测试游标分页函数"""
        items = [i for i in range(100)]
        result = paginate_cursor(items, limit=10)
        
        self.assertEqual(len(result.items), 10)
        self.assertTrue(result.metadata.has_more)
    
    def test_paginate_infinite_function(self):
        """测试无限滚动函数"""
        items = [i for i in range(100)]
        result = paginate_infinite(items, loaded=0, batch=15)
        
        self.assertEqual(len(result.items), 15)
    
    def test_page_range_function(self):
        """测试页码范围函数"""
        pages = page_range(10, 50, 9)
        
        self.assertEqual(len(pages), 9)
        self.assertIn(10, pages)


class TestEdgeCases(unittest.TestCase):
    """测试边界情况"""
    
    def test_single_item(self):
        """测试单个条目"""
        items = ['only-one']
        result = Pagination.offset(items, page=1, per_page=10)
        
        self.assertEqual(len(result.items), 1)
        self.assertEqual(result.metadata.total_pages, 1)
        self.assertFalse(result.metadata.has_next)
    
    def test_items_less_than_per_page(self):
        """测试条目数少于每页数"""
        items = [1, 2, 3]
        result = Pagination.offset(items, page=1, per_page=10)
        
        self.assertEqual(len(result.items), 3)
        self.assertEqual(result.metadata.total_pages, 1)
    
    def test_large_page_number(self):
        """测试超大页码"""
        items = [i for i in range(10)]
        result = Pagination.offset(items, page=1000, per_page=5)
        
        # 应返回最后一页
        self.assertEqual(result.metadata.current_page, 2)
    
    def test_negative_page(self):
        """测试负页码"""
        items = [i for i in range(10)]
        result = Pagination.offset(items, page=-1, per_page=5)
        
        # 应返回第一页
        self.assertEqual(result.metadata.current_page, 1)
    
    def test_zero_limit(self):
        """测试零限制"""
        items = [i for i in range(10)]
        
        # 零限制应该被调整为最小值
        paginator = OffsetPaginator(items_per_page=10, min_items_per_page=1)
        result = paginator.paginate(items, per_page=0)
        
        self.assertGreaterEqual(result.metadata.items_per_page, 1)


class TestPaginationTypes(unittest.TestCase):
    """测试分页类型"""
    
    def test_offset_type(self):
        """测试偏移量类型"""
        result = Pagination.offset([1, 2, 3])
        self.assertEqual(result.pagination_type, PaginationType.OFFSET)
    
    def test_cursor_type(self):
        """测试游标类型"""
        result = Pagination.cursor([1, 2, 3])
        self.assertEqual(result.pagination_type, PaginationType.CURSOR)
    
    def test_keyset_type(self):
        """测试键集类型"""
        items = [{'id': i} for i in range(5)]
        result = Pagination.keyset(items)
        self.assertEqual(result.pagination_type, PaginationType.KEYSET)
    
    def test_infinite_type(self):
        """测试无限滚动类型"""
        result = Pagination.infinite([1, 2, 3])
        self.assertEqual(result.pagination_type, PaginationType.INFINITE)


if __name__ == '__main__':
    unittest.main(verbosity=2)