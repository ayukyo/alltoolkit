"""
Pagination Utilities 使用示例

展示各种分页方式的实际应用场景。
"""

import sys
import os
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(parent_dir))

import importlib.util
spec = importlib.util.spec_from_file_location("pagination_utils_mod", os.path.join(parent_dir, "mod.py"))
pagination_utils_mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pagination_utils_mod)

Pagination = pagination_utils_mod.Pagination
OffsetPaginator = pagination_utils_mod.OffsetPaginator
CursorPaginator = pagination_utils_mod.CursorPaginator
KeysetPaginator = pagination_utils_mod.KeysetPaginator
InfiniteScrollPaginator = pagination_utils_mod.InfiniteScrollPaginator
paginate_offset = pagination_utils_mod.paginate_offset
paginate_cursor = pagination_utils_mod.paginate_cursor
page_range = pagination_utils_mod.page_range


def example_offset_pagination():
    """示例：传统偏移量分页"""
    print("\n" + "=" * 60)
    print("示例 1: 偏移量分页 (传统分页)")
    print("=" * 60)
    
    # 模拟数据 - 例如产品列表
    products = [
        {'id': i, 'name': f'Product-{i}', 'price': i * 10}
        for i in range(1, 101)
    ]
    
    # 创建分页器
    paginator = OffsetPaginator(items_per_page=10)
    
    # 获取第 3 页
    result = paginator.paginate(products, page=3)
    
    print(f"\n第 {result.metadata.current_page} 页内容:")
    for item in result.items[:3]:
        print(f"  - {item['name']}: ¥{item['price']}")
    print(f"  ... 共 {len(result.items)} 条")
    
    print(f"\n分页信息:")
    meta = result.metadata
    print(f"  当前页: {meta.current_page}")
    print(f"  总页数: {meta.total_pages}")
    print(f"  总条数: {meta.total_items}")
    print(f"  上一页: {meta.previous_page}")
    print(f"  下一页: {meta.next_page}")
    
    # 显示页码范围
    pages = page_range(meta.current_page, meta.total_pages, 7)
    print(f"\n显示页码: {pages}")
    
    # 生成 API 链接
    links = Pagination.generate_links('/api/products', meta.current_page, meta.total_pages)
    print(f"\nAPI 链接:")
    for rel, url in links.items():
        print(f"  {rel}: {url}")


def example_cursor_pagination():
    """示例：游标分页 (用于 API)"""
    print("\n" + "=" * 60)
    print("示例 2: 游标分页 (适合大数据集)")
    print("=" * 60)
    
    # 模拟数据 - 例如用户列表
    users = [
        {'id': i, 'username': f'user_{i}', 'email': f'user_{i}@example.com'}
        for i in range(1, 51)
    ]
    
    # 创建游标分页器
    paginator = CursorPaginator(limit=10)
    
    # 获取第一页
    print("\n获取第一页:")
    result1 = paginator.paginate(users)
    
    print(f"返回 {len(result1.items)} 条数据:")
    for user in result1.items[:3]:
        print(f"  - {user['username']}")
    
    print(f"\n下一页游标: {result1.metadata.next_cursor}")
    print(f"还有更多: {result1.metadata.has_more}")
    
    # 使用游标获取下一页
    print("\n使用游标获取下一页:")
    result2 = paginator.paginate(users, cursor=result1.metadata.next_cursor)
    
    print(f"返回 {len(result2.items)} 条数据:")
    for user in result2.items[:3]:
        print(f"  - {user['username']}")
    
    print(f"\n下一页游标: {result2.metadata.next_cursor}")
    
    # API 响应示例
    print("\nAPI 响应格式示例:")
    response = result2.to_dict()
    print(f"  items: [...{len(response['items'])} items...]")
    print(f"  pagination: {response['pagination']}")


def example_keyset_pagination():
    """示例：键集分页 (数据库优化)"""
    print("\n" + "=" * 60)
    print("示例 3: 键集分页 (数据库查询优化)")
    print("=" * 60)
    
    # 模拟数据库记录 - 按时间戳排序的文章
    articles = [
        {'id': i, 'title': f'Article-{i}', 'created_at': f'2024-01-{i:02d}'}
        for i in range(1, 31)
    ]
    
    # 创建键集分页器 (按 id 排序)
    paginator = KeysetPaginator(limit=5, key_field='id')
    
    # 获取第一页
    print("\n获取第一页:")
    result1 = paginator.paginate(articles)
    
    for article in result1.items:
        print(f"  - [{article['id']}] {article['title']}")
    
    print(f"\n下一页游标: {result1.metadata.next_cursor}")
    
    # 获取下一页
    print("\n获取下一页:")
    result2 = paginator.paginate(articles, cursor=result1.metadata.next_cursor)
    
    for article in result2.items:
        print(f"  - [{article['id']}] {article['title']}")
    
    print("\n键集分页优势:")
    print("  - 不使用 OFFSET，性能稳定")
    print("  - 适合大数据集")
    print("  - 数据变化时不会重复")


def example_infinite_scroll():
    """示例：无限滚动 (社交媒体)"""
    print("\n" + "=" * 60)
    print("示例 4: 无限滚动分页 (社交媒体风格)")
    print("=" * 60)
    
    # 模拟社交媒体帖子
    posts = [
        {'id': i, 'content': f'Post content #{i}', 'likes': i * 5}
        for i in range(1, 101)
    ]
    
    # 创建无限滚动分页器
    paginator = InfiniteScrollPaginator(batch_size=10, preload_threshold=3)
    
    # 模拟滚动加载
    loaded_count = 0
    page = 1
    
    while True:
        result = paginator.paginate(posts, loaded_count=loaded_count)
        
        print(f"\n加载批次 {page}:")
        print(f"  新加载: {len(result.items)} 条")
        print(f"  总已加载: {loaded_count + len(result.items)} 条")
        
        # 显示加载状态
        state = paginator.get_load_state(len(posts), loaded_count + len(result.items))
        print(f"  进度: {state['progress'] * 100:.0f}%")
        print(f"  剩余: {state['remaining']} 条")
        
        if state['should_preload']:
            print(f"  ⚠️ 剩余少于阈值，建议预加载!")
        
        loaded_count += len(result.items)
        page += 1
        
        if not result.metadata.has_more:
            print("\n✅ 所有数据已加载完成!")
            break
        
        # 模拟用户滚动
        if page > 3:
            print("\n... 用户继续滚动 ...\n")
            break


def example_sql_integration():
    """示例：与 SQL 查询集成"""
    print("\n" + "=" * 60)
    print("示例 5: SQL 查询集成")
    print("=" * 60)
    
    paginator = OffsetPaginator(items_per_page=20)
    
    # 假设总条目数为 1000
    total_items = 1000
    
    # 获取不同页的 SQL 参数
    print("\n生成 SQL OFFSET/LIMIT 参数:")
    
    for page in [1, 5, 10]:
        offset, limit = paginator.get_offset_limit(page)
        sql = f"SELECT * FROM items ORDER BY id LIMIT {limit} OFFSET {offset}"
        print(f"\n  第 {page} 页:")
        print(f"    SQL: {sql}")
        print(f"    获取条目: {offset + 1} - {offset + limit}")
    
    # 计算总页数
    total_pages = paginator.calculate_pages(total_items)
    print(f"\n总条目: {total_items}")
    print(f"总页数: {total_pages}")


def example_api_response():
    """示例：API 响应构建"""
    print("\n" + "=" * 60)
    print("示例 6: 构建 REST API 响应")
    print("=" * 60)
    
    # 模拟商品数据
    items = [
        {'id': i, 'name': f'Item-{i}', 'price': i * 100}
        for i in range(1, 51)
    ]
    
    # 偏移量分页
    result = Pagination.offset(items, page=2, per_page=10)
    
    # 构建响应
    response = result.to_dict()
    
    print("\nJSON API 响应示例:")
    print("```json")
    print("{")
    print("  'items': [")
    print("    {'id': 11, 'name': 'Item-11', 'price': 1100},")
    print("    {'id': 12, 'name': 'Item-12', 'price': 1200},")
    print("    ...")
    print(f"    // 共 {len(response['items'])} 条")
    print("  ],")
    print("  'pagination': {")
    print(f"    'current_page': {response['pagination']['current_page']},")
    print(f"    'total_pages': {response['pagination']['total_pages']},")
    print(f"    'total_items': {response['pagination']['total_items']},")
    print(f"    'has_next': {response['pagination']['has_next']},")
    print(f"    'has_previous': {response['pagination']['has_previous']}")
    print("  },")
    print("  'links': {")
    links = Pagination.generate_links('/api/items', 2, 5)
    print(f"    'next': '{links.get('next')}',")
    print(f"    'prev': '{links.get('prev')}'")
    print("  }")
    print("}")
    print("```")
    
    # HTTP Link Header
    print("\nHTTP Response Header:")
    header = Pagination.generate_header_links('/api/items', 2, 5)
    print(f"Link: {header}")


def example_page_range_display():
    """示例：页码范围显示"""
    print("\n" + "=" * 60)
    print("示例 7: 页码范围计算 (UI 显示)")
    print("=" * 60)
    
    # 不同场景的页码显示
    scenarios = [
        (1, 10, 7),    # 首页
        (5, 10, 7),    # 中间页
        (10, 10, 7),   # 末页
        (3, 5, 7),     # 总页数少于显示数
        (50, 100, 9),  # 大数据集
    ]
    
    for current, total, max_display in scenarios:
        pages = Pagination.calculate_page_range(current, total, max_display)
        
        # 构建显示字符串
        display = ""
        if pages[0] > 1:
            display += "1 ... "
        display += " ".join(map(str, pages))
        if pages[-1] < total:
            display += f" ... {total}"
        
        print(f"\n  第 {current}/{total} 页，显示 {max_display} 页码:")
        print(f"    计算结果: {pages}")
        print(f"    UI 显示: [{display}]")


def example_comparison():
    """示例：分页方式对比"""
    print("\n" + "=" * 60)
    print("示例 8: 分页方式对比")
    print("=" * 60)
    
    print("\n| 分页类型 | 适用场景 | 优点 | 缺点 |")
    print("|----------|----------|------|------|")
    print("| 偏移量 | 小数据集、需要页码跳转 | 简单、可跳转任意页 | 大数据性能差 |")
    print("| 游标 | API、大数据集 | 性能稳定、数据一致 | 无法跳转 |")
    print("| 键集 | 数据库优化 | 最高效 | 只能单向翻页 |")
    print("| 无限滚动 | 社交媒体、瀑布流 | 用户体验好 | 无法定位特定内容 |")
    
    print("\n选择建议:")
    print("  - 用户管理后台 → 偏移量分页")
    print("  - REST API → 游标分页")
    print("  - 百万级数据 → 键集分页")
    print("  - 移动端列表 → 无限滚动")


def run_all_examples():
    """运行所有示例"""
    example_offset_pagination()
    example_cursor_pagination()
    example_keyset_pagination()
    example_infinite_scroll()
    example_sql_integration()
    example_api_response()
    example_page_range_display()
    example_comparison()
    
    print("\n" + "=" * 60)
    print("所有示例完成!")
    print("=" * 60)


if __name__ == '__main__':
    run_all_examples()