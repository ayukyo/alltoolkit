"""
JSON 工具集使用示例
JSON Utilities Usage Examples

本文件展示了 json_utils 模块的所有主要功能
"""

import sys
import os

# Add module directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from mod import (
    json_validate, json_prettify, json_minify,
    safe_json_loads, safe_json_dumps,
    json_flatten, json_unflatten,
    json_merge, json_diff, json_patch,
    json_get, json_set, json_delete, json_has,
    json_query, json_schema_validate,
    json_to_xml, xml_to_json,
    json_to_csv, csv_to_json,
    json_transform, json_filter, json_map,
    json_deepclone, json_pick, json_omit,
    json_stats, json_size,
)


def example_basic_operations():
    """基础操作示例"""
    print("=" * 60)
    print("基础操作示例")
    print("=" * 60)
    
    # 1. JSON 验证
    print("\n1. JSON 验证:")
    valid_json = '{"name": "Alice", "age": 30}'
    invalid_json = '{invalid json}'
    
    valid, error = json_validate(valid_json)
    print(f"   有效 JSON: {valid}, 错误: {error}")
    
    valid, error = json_validate(invalid_json)
    print(f"   无效 JSON: {valid}, 错误: {error[:50]}...")
    
    # 2. JSON 美化
    print("\n2. JSON 美化:")
    compact_json = '{"name":"Alice","age":30,"address":{"city":"北京","zip":"100000"}}'
    pretty = json_prettify(compact_json, indent=2)
    print(f"   原始: {compact_json}")
    print(f"   美化后:")
    print("   " + pretty.replace("\n", "\n   "))
    
    # 3. JSON 压缩
    print("\n3. JSON 压缩:")
    spaces_json = '{ "name" : "Alice" , "age" : 30 }'
    minified = json_minify(spaces_json)
    print(f"   原始: {spaces_json}")
    print(f"   压缩后: {minified}")
    
    # 4. 安全解析
    print("\n4. 安全解析:")
    result = safe_json_loads('{"a": 1}', {})
    print(f"   有效 JSON: {result}")
    
    result = safe_json_loads('invalid', {"default": "value"})
    print(f"   无效 JSON (返回默认值): {result}")


def example_flatten_unflatten():
    """扁平化/反扁平化示例"""
    print("\n" + "=" * 60)
    print("扁平化/反扁平化示例")
    print("=" * 60)
    
    # 1. 扁平化
    print("\n1. JSON 扁平化:")
    nested = {
        "user": {
            "name": "Alice",
            "profile": {
                "age": 30,
                "city": "北京"
            }
        },
        "tags": ["developer", "python"]
    }
    
    flat = json_flatten(nested)
    print(f"   原始 JSON: {nested}")
    print(f"   扁平化后:")
    for key, value in flat.items():
        print(f"      {key}: {value}")
    
    # 2. 反扁平化
    print("\n2. JSON 反扁平化:")
    flat_data = {"user.name": "Alice", "user.profile.age": 30, "items.0": 1, "items.1": 2}
    unflat = json_unflatten(flat_data)
    print(f"   扁平数据: {flat_data}")
    print(f"   反扁平化后: {unflat}")


def example_merge():
    """合并示例"""
    print("\n" + "=" * 60)
    print("JSON 合并示例")
    print("=" * 60)
    
    # 1. 深度合并
    print("\n1. 深度合并:")
    obj1 = {"user": {"name": "Alice", "age": 30}, "settings": {"theme": "dark"}}
    obj2 = {"user": {"email": "alice@example.com"}, "settings": {"lang": "zh"}}
    
    merged = json_merge(obj1, obj2)
    print(f"   对象 1: {obj1}")
    print(f"   对象 2: {obj2}")
    print(f"   合并结果: {merged}")
    
    # 2. 数组合并策略
    print("\n2. 数组合并策略:")
    arr1 = {"items": [1, 2, 3]}
    arr2 = {"items": [4, 5]}
    
    # concat 策略
    concat_result = json_merge(arr1, arr2, array_strategy="concat")
    print(f"   concat 策略: {concat_result}")
    
    # replace 策略
    replace_result = json_merge(arr1, arr2, array_strategy="replace")
    print(f"   replace 策略: {replace_result}")


def example_diff_patch():
    """差异比较和补丁示例"""
    print("\n" + "=" * 60)
    print("JSON 差异比较和补丁示例")
    print("=" * 60)
    
    # 1. 差异比较
    print("\n1. JSON 差异比较:")
    old = {"name": "Alice", "age": 30, "city": "北京"}
    new = {"name": "Alice", "age": 31, "email": "alice@example.com"}
    
    diffs = json_diff(old, new)
    print(f"   旧对象: {old}")
    print(f"   新对象: {new}")
    print(f"   差异:")
    for diff in diffs:
        print(f"      {diff}")
    
    # 2. JSON Patch
    print("\n2. JSON Patch 应用:")
    target = {"name": "Alice", "age": 30}
    patches = [
        {"op": "add", "path": "/email", "value": "alice@example.com"},
        {"op": "replace", "path": "/age", "value": 31}
    ]
    
    result = json_patch(target, patches)
    print(f"   原对象: {target}")
    print(f"   补丁: {patches}")
    print(f"   结果: {result}")


def example_path_operations():
    """路径操作示例"""
    print("\n" + "=" * 60)
    print("JSON 路径操作示例")
    print("=" * 60)
    
    data = {
        "user": {
            "name": "Alice",
            "profile": {
                "age": 30,
                "skills": ["Python", "JavaScript", "Go"]
            }
        },
        "config": {
            "debug": True
        }
    }
    
    # 1. 获取值
    print("\n1. 获取指定路径值:")
    print(f"   $.user.name: {json_get(data, 'user.name')}")
    print(f"   $.user.profile.age: {json_get(data, 'user.profile.age')}")
    print(f"   $.user.profile.skills.0: {json_get(data, 'user.profile.skills.0')}")
    print(f"   $.user.profile.skills[1]: {json_get(data, 'user.profile.skills[1]}')")  # 方括号语法
    print(f"   $.missing (默认值): {json_get(data, 'missing', 'N/A')}")
    
    # 2. 设置值
    print("\n2. 设置指定路径值:")
    new_data = json_set(data, "user.profile.city", "上海")
    print(f"   设置 user.profile.city = '上海'")
    print(f"   新数据: {new_data}")
    
    # 3. 删除值
    print("\n3. 删除指定路径值:")
    deleted_data = json_delete(data, "config.debug")
    print(f"   删除 config.debug")
    print(f"   新数据: {deleted_data}")
    
    # 4. 检查路径存在
    print("\n4. 检查路径是否存在:")
    print(f"   user.name 存在: {json_has(data, 'user.name')}")
    print(f"   user.phone 存在: {json_has(data, 'user.phone')}")


def example_jsonpath_query():
    """JSONPath 查询示例"""
    print("\n" + "=" * 60)
    print("JSONPath 查询示例")
    print("=" * 60)
    
    data = {
        "store": {
            "book": [
                {"category": "fiction", "title": "小说1", "price": 10},
                {"category": "tech", "title": "技术书", "price": 20},
                {"category": "fiction", "title": "小说2", "price": 15}
            ],
            "bicycle": {"color": "red", "price": 100}
        }
    }
    
    print("\n1. 查询所有书籍价格:")
    prices = json_query(data, "$.store.book[*].price")
    print(f"   查询: $.store.book[*].price")
    print(f"   结果: {prices}")
    
    print("\n2. 查询自行车颜色:")
    color = json_query(data, "$.store.bicycle.color")
    print(f"   查询: $.store.bicycle.color")
    print(f"   结果: {color}")
    
    print("\n3. 查询第一本书:")
    first_book = json_query(data, "$.store.book[0]")
    print(f"   查询: $.store.book[0]")
    print(f"   结果: {first_book}")


def example_schema_validation():
    """JSON Schema 验证示例"""
    print("\n" + "=" * 60)
    print("JSON Schema 验证示例")
    print("=" * 60)
    
    schema = {
        "type": "object",
        "required": ["name", "email"],
        "properties": {
            "name": {"type": "string", "minLength": 2},
            "email": {"type": "string", "pattern": "^[\\w.-]+@[\\w.-]+\\.[\\w]+$"},
            "age": {"type": "integer", "minimum": 0, "maximum": 150},
            "tags": {"type": "array", "items": {"type": "string"}, "minItems": 1}
        }
    }
    
    print(f"\n   Schema:")
    print(f"   - 类型: object")
    print(f"   - 必填: name, email")
    print(f"   - name: 字符串，最小长度 2")
    print(f"   - email: 字符串，需匹配邮箱格式")
    print(f"   - age: 整数，范围 0-150")
    print(f"   - tags: 字符串数组，至少 1 个元素")
    
    # 有效数据
    valid_data = {
        "name": "Alice",
        "email": "alice@example.com",
        "age": 30,
        "tags": ["developer"]
    }
    
    valid, errors = json_schema_validate(valid_data, schema)
    print(f"\n   有效数据: {valid_data}")
    print(f"   验证结果: {valid}, 错误: {errors}")
    
    # 无效数据
    invalid_data = {
        "name": "A",  # 长度太短
        "email": "invalid-email",  # 格式错误
        "age": -1,  # 超出范围
    }
    
    valid, errors = json_schema_validate(invalid_data, schema)
    print(f"\n   无效数据: {invalid_data}")
    print(f"   验证结果: {valid}")
    print(f"   错误列表:")
    for error in errors:
        print(f"      - {error}")


def example_conversions():
    """转换示例"""
    print("\n" + "=" * 60)
    print("JSON 转换示例")
    print("=" * 60)
    
    # 1. JSON 转 XML
    print("\n1. JSON 转 XML:")
    json_data = {"person": {"name": "Alice", "age": 30, "skills": ["Python", "Go"]}}
    xml = json_to_xml(json_data)
    print(f"   JSON: {json_data}")
    print(f"   XML: {xml}")
    
    # 2. XML 转 JSON
    print("\n2. XML 转 JSON:")
    xml_str = '<root><person><name>Alice</name><age>30</age></person></root>'
    json_result = xml_to_json(xml_str)
    print(f"   XML: {xml_str}")
    print(f"   JSON: {json_result}")
    
    # 3. JSON 转 CSV
    print("\n3. JSON 转 CSV:")
    json_list = [
        {"name": "Alice", "age": 30, "city": "北京"},
        {"name": "Bob", "age": 25, "city": "上海"},
        {"name": "Charlie", "age": 35, "city": "广州"}
    ]
    csv = json_to_csv(json_list)
    print(f"   JSON 列表:")
    for item in json_list:
        print(f"      {item}")
    print(f"   CSV:")
    print("   " + csv.replace("\n", "\n   "))
    
    # 4. CSV 转 JSON
    print("\n4. CSV 转 JSON:")
    csv_str = "name,age,city\nAlice,30,北京\nBob,25,上海"
    json_result = csv_to_json(csv_str)
    print(f"   CSV:")
    print("   " + csv_str.replace("\n", "\n   "))
    print(f"   JSON: {json_result}")


def example_transformations():
    """变换示例"""
    print("\n" + "=" * 60)
    print("JSON 变换示例")
    print("=" * 60)
    
    # 1. 键名变换
    print("\n1. 键名变换（驼峰转下划线）:")
    data = {"firstName": "Alice", "lastName": "Smith", "userProfile": {"userId": 123}}
    
    def camel_to_snake(key):
        return ''.join(['_' + c.lower() if c.isupper() else c for c in key]).lstrip('_')
    
    result = json_transform(data, key_transform=camel_to_snake)
    print(f"   原始: {data}")
    print(f"   变换后: {result}")
    
    # 2. 值变换
    print("\n2. 值变换（字符串数字转整数）:")
    data = {"age": "30", "score": "95", "name": "Alice"}
    
    def to_int_if_possible(value):
        if isinstance(value, str) and value.isdigit():
            return int(value)
        return value
    
    result = json_transform(data, value_transform=to_int_if_possible)
    print(f"   原始: {data}")
    print(f"   变换后: {result}")
    
    # 3. 过滤
    print("\n3. JSON 过滤:")
    data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    result = json_filter(data, lambda x: x % 2 == 0)
    print(f"   原始: {data}")
    print(f"   过滤偶数: {result}")
    
    # 4. 映射
    print("\n4. JSON 映射:")
    data = [1, 2, 3, 4, 5]
    result = json_map(data, lambda x: x ** 2)
    print(f"   原始: {data}")
    print(f"   平方映射: {result}")


def example_pick_omit():
    """选取/排除示例"""
    print("\n" + "=" * 60)
    print("JSON 选取/排除示例")
    print("=" * 60)
    
    user = {
        "id": 123,
        "name": "Alice",
        "email": "alice@example.com",
        "password": "secret123",
        "internal_token": "abc123",
        "created_at": "2024-01-01"
    }
    
    # 选取公开字段
    print("\n1. 选取公开字段:")
    public_fields = ["id", "name", "email", "created_at"]
    public_user = json_pick(user, public_fields)
    print(f"   原始: {user}")
    print(f"   选取字段: {public_fields}")
    print(f"   结果: {public_user}")
    
    # 排除敏感字段
    print("\n2. 排除敏感字段:")
    sensitive_fields = ["password", "internal_token"]
    safe_user = json_omit(user, sensitive_fields)
    print(f"   原始: {user}")
    print(f"   排除字段: {sensitive_fields}")
    print(f"   结果: {safe_user}")


def example_deepclone():
    """深度克隆示例"""
    print("\n" + "=" * 60)
    print("JSON 深度克隆示例")
    print("=" * 60)
    
    original = {
        "user": {"name": "Alice", "profile": {"tags": ["python", "go"]}},
        "settings": {"theme": "dark"}
    }
    
    cloned = json_deepclone(original)
    
    # 修改克隆不影响原始
    cloned["user"]["profile"]["tags"].append("rust")
    cloned["settings"]["theme"] = "light"
    
    print(f"   原始数据: {original}")
    print(f"   克隆并修改后: {cloned}")
    print(f"   原始数据 (未受影响): {original}")


def example_stats():
    """统计示例"""
    print("\n" + "=" * 60)
    print("JSON 统计示例")
    print("=" * 60)
    
    data = {
        "users": [
            {"name": "Alice", "age": 30, "active": True},
            {"name": "Bob", "age": 25, "active": False},
            {"name": None, "age": None, "active": True}
        ],
        "config": {
            "debug": True,
            "version": "1.0.0"
        }
    }
    
    stats = json_stats(data)
    print(f"   数据: {data}")
    print(f"   统计:")
    print(f"      - 深度: {stats['depth']}")
    print(f"      - 键数量: {stats['keys']}")
    print(f"      - 数组数量: {stats['arrays']}")
    print(f"      - 对象数量: {stats['objects']}")
    print(f"      - 基本类型数量: {stats['primitives']}")
    print(f"      - null 数量: {stats['nulls']}")
    print(f"      - 布尔值数量: {stats['booleans']}")
    print(f"      - 数字数量: {stats['numbers']}")
    print(f"      - 字符串数量: {stats['strings']}")
    
    # 大小
    size = json_size(data)
    print(f"      - 字节大小: {size}")


def main():
    """运行所有示例"""
    print("\n" + "#" * 60)
    print("# JSON 工具集使用示例")
    print("# JSON Utilities Usage Examples")
    print("#" * 60)
    
    example_basic_operations()
    example_flatten_unflatten()
    example_merge()
    example_diff_patch()
    example_path_operations()
    example_jsonpath_query()
    example_schema_validation()
    example_conversions()
    example_transformations()
    example_pick_omit()
    example_deepclone()
    example_stats()
    
    print("\n" + "#" * 60)
    print("# 示例演示完成!")
    print("#" * 60)


if __name__ == '__main__':
    main()