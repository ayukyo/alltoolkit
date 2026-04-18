"""
AllToolkit - JSONPath Utilities Usage Examples

This file demonstrates various JSONPath query capabilities.
"""

import json
import sys
sys.path.insert(0, '..')
from mod import JSONPath, find, find_one, compile, validate


# =============================================================================
# Sample Data
# =============================================================================

SAMPLE_DATA = {
    "store": {
        "book": [
            {
                "category": "reference",
                "author": "Nigel Rees",
                "title": "Sayings of the Century",
                "price": 8.95
            },
            {
                "category": "fiction",
                "author": "Evelyn Waugh",
                "title": "Sword of Honour",
                "price": 12.99
            },
            {
                "category": "fiction",
                "author": "Herman Melville",
                "title": "Moby Dick",
                "isbn": "0-553-21311-3",
                "price": 8.99
            },
            {
                "category": "fiction",
                "author": "J. R. R. Tolkien",
                "title": "The Lord of the Rings",
                "isbn": "0-395-19395-8",
                "price": 22.99
            }
        ],
        "bicycle": {
            "color": "red",
            "price": 19.95
        }
    },
    "expensive": 10
}


def print_result(expression: str, result: list, label: str = ""):
    """Helper to print query results."""
    print(f"\n{'='*60}")
    print(f"表达式: {expression}")
    if label:
        print(f"说明: {label}")
    print(f"结果数量: {len(result)}")
    print(f"结果:")
    print(json.dumps(result, indent=2, ensure_ascii=False))


# =============================================================================
# Basic Queries
# =============================================================================

def example_basic_queries():
    """演示基本查询功能"""
    print("\n" + "="*60)
    print("基本查询示例")
    print("="*60)
    
    # 1. Root - 返回整个文档
    result = find('$', SAMPLE_DATA)
    print_result('$', result, "返回根对象")
    
    # 2. Child accessor - 使用点号访问子属性
    result = find('$.store', SAMPLE_DATA)
    print_result('$.store', result, "访问 store 属性")
    
    # 3. Nested child - 链式访问嵌套属性
    result = find('$.store.bicycle', SAMPLE_DATA)
    print_result('$.store.bicycle', result, "访问嵌套的 bicycle 属性")
    
    # 4. Bracket notation - 使用括号访问
    result = find('$["store"]["bicycle"]["color"]', SAMPLE_DATA)
    print_result('$["store"]["bicycle"]["color"]', result, "使用括号语法访问")
    
    # 5. Mixed access - 混合使用点和括号
    result = find('$.store["bicycle"].color', SAMPLE_DATA)
    print_result('$.store["bicycle"].color', result, "混合语法")


# =============================================================================
# Array Queries
# =============================================================================

def example_array_queries():
    """演示数组查询功能"""
    print("\n" + "="*60)
    print("数组查询示例")
    print("="*60)
    
    # 1. Array index - 数组索引
    result = find('$.store.book[0]', SAMPLE_DATA)
    print_result('$.store.book[0]', result, "获取第一本书")
    
    # 2. Negative index - 负索引
    result = find('$.store.book[-1]', SAMPLE_DATA)
    print_result('$.store.book[-1]', result, "获取最后一本书")
    
    # 3. Array slice - 数组切片
    result = find('$.store.book[0:2]', SAMPLE_DATA)
    print_result('$.store.book[0:2]', result, "获取前两本书")
    
    # 4. Slice with step - 带步长的切片
    result = find('$.store.book[::2]', SAMPLE_DATA)
    print_result('$.store.book[::2]', result, "每隔一本书取一本")
    
    # 5. Union - 多索引选择
    result = find('$.store.book[0,2]', SAMPLE_DATA)
    print_result('$.store.book[0,2]', result, "选择第1和第3本书")


# =============================================================================
# Wildcard Queries
# =============================================================================

def example_wildcard_queries():
    """演示通配符查询"""
    print("\n" + "="*60)
    print("通配符查询示例")
    print("="*60)
    
    # 1. Wildcard on object - 对象通配符
    result = find('$.store.*', SAMPLE_DATA)
    print_result('$.store.*', result, "获取 store 下所有属性值")
    
    # 2. Wildcard on array - 数组通配符
    result = find('$.store.book[*]', SAMPLE_DATA)
    print_result('$.store.book[*]', result, "获取所有书籍")
    
    # 3. Wildcard nested - 嵌套通配符
    result = find('$.store.book[*].author', SAMPLE_DATA)
    print_result('$.store.book[*].author', result, "获取所有书籍作者")


# =============================================================================
# Recursive Descent Queries
# =============================================================================

def example_recursive_queries():
    """演示递归下降查询"""
    print("\n" + "="*60)
    print("递归下降查询示例")
    print("="*60)
    
    # 1. Find all prices - 查找所有价格
    result = find('$..price', SAMPLE_DATA)
    print_result('$..price', result, "查找所有 price 属性（包括书籍和自行车）")
    
    # 2. Find all authors - 查找所有作者
    result = find('$..author', SAMPLE_DATA)
    print_result('$..author', result, "查找所有 author 属性")
    
    # 3. Recursive wildcard - 递归通配符
    result = find('$..*', SAMPLE_DATA)
    print_result('$..*', result[:10], "查找所有值（截取前10个）")


# =============================================================================
# Filter Queries
# =============================================================================

def example_filter_queries():
    """演示过滤器查询"""
    print("\n" + "="*60)
    print("过滤器查询示例")
    print("="*60)
    
    # 1. Filter by price - 按价格过滤
    result = find('$.store.book[?(@.price < 10)]', SAMPLE_DATA)
    print_result('$.store.book[?(@.price < 10)]', result, "价格小于10的书")
    
    # 2. Filter by category - 按类别过滤
    result = find('$.store.book[?(@.category == "fiction")]', SAMPLE_DATA)
    print_result('$.store.book[?(@.category == "fiction")]', result, "小说类书籍")
    
    # 3. Filter with AND - AND 条件
    result = find('$.store.book[?(@.category == "fiction" && @.price < 10)]', SAMPLE_DATA)
    print_result('$.store.book[?(@.category == "fiction" && @.price < 10)]', 
                 result, "小说类且价格小于10的书")
    
    # 4. Filter with OR - OR 条件
    result = find('$.store.book[?(@.price < 10 || @.price > 20)]', SAMPLE_DATA)
    print_result('$.store.book[?(@.price < 10 || @.price > 20)]', 
                 result, "价格小于10或大于20的书")
    
    # 5. Filter by existence - 检查属性存在
    result = find('$.store.book[?(@.isbn)]', SAMPLE_DATA)
    print_result('$.store.book[?(@.isbn)]', result, "有 ISBN 的书")
    
    # 6. Filter by comparison with root - 与根对象比较
    result = find('$.store.book[?(@.price < $.expensive)]', SAMPLE_DATA)
    print_result('$.store.book[?(@.price < $.expensive)]', 
                 result, "价格小于 expensive 值的书")


# =============================================================================
# Convenience Functions
# =============================================================================

def example_convenience_functions():
    """演示便捷函数"""
    print("\n" + "="*60)
    print("便捷函数示例")
    print("="*60)
    
    # 1. find() - 快速查询
    print("\n使用 find() 快速查询:")
    result = find('$.store.book[*].title', SAMPLE_DATA)
    print(f"书籍标题: {result}")
    
    # 2. find_one() - 获取单个结果
    print("\n使用 find_one() 获取单个结果:")
    result = find_one('$.store.bicycle.color', SAMPLE_DATA)
    print(f"自行车颜色: {result}")
    
    # 3. compile() - 编译表达式用于复用
    print("\n使用 compile() 编译表达式:")
    path = compile('$.store.book[*].author')
    # 可以多次使用同一个编译后的路径
    result1 = path.query(SAMPLE_DATA)
    result2 = path.query(SAMPLE_DATA)
    print(f"作者列表（第一次）: {result1}")
    print(f"作者列表（第二次）: {result2}")
    
    # 4. validate() - 验证表达式
    print("\n使用 validate() 验证表达式:")
    print(f"'$.store.book[*]' 是否有效: {validate('$.store.book[*]')}")
    print(f"'invalid' 是否有效: {validate('invalid')}")


# =============================================================================
# Real-world Scenarios
# =============================================================================

def example_real_world():
    """真实应用场景示例"""
    print("\n" + "="*60)
    print("真实应用场景示例")
    print("="*60)
    
    # 1. API 响应处理
    api_response = {
        "status": "success",
        "data": {
            "users": [
                {"id": 1, "name": "Alice", "email": "alice@example.com"},
                {"id": 2, "name": "Bob", "email": "bob@example.com"},
                {"id": 3, "name": "Charlie", "email": "charlie@example.com"}
            ],
            "total": 3
        }
    }
    
    print("\n场景1: API 响应处理")
    print("- 获取所有用户名:", find('$.data.users[*].name', api_response))
    print("- 获取用户总数:", find_one('$.data.total', api_response))
    
    # 2. 配置文件解析
    config = {
        "app": {
            "name": "MyApp",
            "version": "1.0.0",
            "settings": {
                "debug": True,
                "log_level": "info",
                "features": ["feature1", "feature2"]
            }
        },
        "database": {
            "host": "localhost",
            "port": 5432,
            "name": "myapp_db"
        }
    }
    
    print("\n场景2: 配置文件解析")
    print("- 获取应用名:", find_one('$.app.name', config))
    print("- 获取调试模式:", find_one('$.app.settings.debug', config))
    print("- 获取数据库配置:", find('$.database.*', config))
    
    # 3. 日志分析
    logs = {
        "entries": [
            {"level": "ERROR", "message": "Connection failed", "timestamp": "2024-01-15T10:00:00"},
            {"level": "INFO", "message": "Server started", "timestamp": "2024-01-15T10:01:00"},
            {"level": "ERROR", "message": "Database timeout", "timestamp": "2024-01-15T10:02:00"},
            {"level": "WARN", "message": "High memory usage", "timestamp": "2024-01-15T10:03:00"}
        ]
    }
    
    print("\n场景3: 日志分析")
    print("- 所有错误日志:", find('$.entries[?(@.level == "ERROR")]', logs))
    print("- 错误日志消息:", find('$.entries[?(@.level == "ERROR")].message', logs))
    
    # 4. 商品数据过滤
    products = {
        "items": [
            {"id": 1, "name": "Laptop", "price": 999, "category": "electronics", "stock": 5},
            {"id": 2, "name": "Mouse", "price": 25, "category": "electronics", "stock": 100},
            {"id": 3, "name": "Book", "price": 15, "category": "books", "stock": 50},
            {"id": 4, "name": "Keyboard", "price": 75, "category": "electronics", "stock": 0}
        ]
    }
    
    print("\n场景4: 商品数据过滤")
    print("- 有库存的商品:", find('$.items[?(@.stock > 0)].name', products))
    print("- 价格低于100的电子产品:", 
          find('$.items[?(@.category == "electronics" && @.price < 100)].name', products))
    print("- 所有商品价格:", find('$..price', products))


# =============================================================================
# Performance Tips
# =============================================================================

def example_performance():
    """性能优化示例"""
    print("\n" + "="*60)
    print("性能优化示例")
    print("="*60)
    
    print("\n建议:")
    print("1. 对于重复查询，使用 compile() 预编译表达式")
    print("2. 避免过度使用 $..，它会遍历整个文档")
    print("3. 尽量使用精确路径而不是通配符")
    print("4. 对于大型数据，考虑使用 slice 限制结果数量")
    
    # 编译后的路径可复用
    print("\n预编译示例:")
    path = compile('$.store.book[*].title')
    
    large_data = {
        "store": {
            "book": [{"title": f"Book {i}"} for i in range(1000)]
        }
    }
    
    # 多次使用同一个编译路径
    result1 = path.query(large_data)
    result2 = path.query(large_data)
    print(f"查询结果数量: {len(result1)}")


# =============================================================================
# Main
# =============================================================================

def main():
    """运行所有示例"""
    print("="*60)
    print("AllToolkit JSONPath Utilities - 使用示例")
    print("="*60)
    
    example_basic_queries()
    example_array_queries()
    example_wildcard_queries()
    example_recursive_queries()
    example_filter_queries()
    example_convenience_functions()
    example_real_world()
    example_performance()
    
    print("\n" + "="*60)
    print("示例完成!")
    print("="*60)


if __name__ == '__main__':
    main()