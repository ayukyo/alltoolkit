#!/usr/bin/env python3
"""
JSON Utilities 使用示例

演示 json_utils 模块的主要功能。
"""

import sys
sys.path.insert(0, '..')

from mod import (
    # 格式化
    format_json, prettify_json, minify_json,
    # 验证
    validate_json, validate_json_schema,
    # 路径操作
    get_value, set_value, has_path, delete_value,
    # 展平和嵌套
    flatten_json, unflatten_json,
    # 搜索
    find_all, find_first, grep_json,
    # 过滤和映射
    filter_json, map_json,
    # 差异比较
    diff_json, diff_summary,
    # 合并
    merge_json,
    # 统计
    json_stats,
    # 选择和排除
    select_keys, omit_keys,
    # 遍历
    walk_json, get_all_paths,
    # 克隆和比较
    deep_clone, deep_equals,
    # 安全操作
    safe_get, safe_string,
    # 类和便捷函数
    JsonUtils, loads, dumps,
)


def print_section(title):
    """打印分节标题"""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print('='*60)


def example_formatting():
    """格式化示例"""
    print_section("JSON 格式化")
    
    data = {"name": "张三", "age": 25, "city": "北京"}
    
    # 美化输出
    print("美化输出:")
    print(format_json(data, indent=2))
    
    # 压缩输出
    print("\n压缩输出:")
    print(format_json(data, compact=True))
    
    # 从字符串美化
    json_str = '{"name":"test","items":[1,2,3]}'
    print("\n从字符串美化:")
    print(prettify_json(json_str))


def example_validation():
    """验证示例"""
    print_section("JSON 验证")
    
    # 验证 JSON 字符串
    valid_json = '{"name": "test", "value": 123}'
    invalid_json = '{"name": "test"'
    
    print(f"验证有效 JSON: {validate_json(valid_json).valid}")
    print(f"验证无效 JSON: {validate_json(invalid_json).valid}")
    
    if not validate_json(invalid_json).valid:
        result = validate_json(invalid_json)
        print(f"  错误: {result.error}")
        print(f"  位置: 行 {result.line}, 列 {result.column}")
    
    # Schema 验证
    print("\nSchema 验证:")
    data = {"name": "John", "age": 25}
    schema = {
        "type": "object",
        "required": ["name", "age"],
        "properties": {
            "name": {"type": "string"},
            "age": {"type": "integer", "minimum": 0, "maximum": 150}
        }
    }
    
    valid, errors = validate_json_schema(data, schema)
    print(f"数据: {data}")
    print(f"验证结果: {'通过' if valid else '失败'}")
    if errors:
        print(f"错误: {errors}")


def example_path_operations():
    """路径操作示例"""
    print_section("路径操作")
    
    data = {
        "name": "测试项目",
        "user": {
            "id": 1,
            "profile": {
                "email": "test@example.com",
                "level": "gold"
            }
        },
        "items": [
            {"id": 1, "name": "商品A", "price": 100},
            {"id": 2, "name": "商品B", "price": 200}
        ]
    }
    
    print("原始数据:")
    print(format_json(data))
    
    # 获取值
    print("\n获取值:")
    print(f"  name: {get_value(data, 'name')}")
    print(f"  user.id: {get_value(data, 'user.id')}")
    print(f"  user.profile.email: {get_value(data, 'user.profile.email')}")
    print(f"  items[0].name: {get_value(data, 'items[0].name')}")
    print(f"  items[1].price: {get_value(data, 'items[1].price')}")
    
    # 设置值
    print("\n设置值:")
    set_value(data, "user.profile.level", "platinum")
    print(f"  user.profile.level: {get_value(data, 'user.profile.level')}")
    
    # 检查路径
    print("\n检查路径存在:")
    print(f"  user.id 存在: {has_path(data, 'user.id')}")
    print(f"  user.missing 存在: {has_path(data, 'user.missing')}")


def example_flatten_unflatten():
    """展平和嵌套示例"""
    print_section("展平和嵌套")
    
    data = {
        "user": {
            "name": "张三",
            "profile": {
                "email": "zhangsan@example.com",
                "age": 30
            }
        },
        "items": [
            {"id": 1, "name": "商品A"},
            {"id": 2, "name": "商品B"}
        ]
    }
    
    print("原始数据:")
    print(format_json(data))
    
    # 展平
    print("\n展平后:")
    flat = flatten_json(data)
    for key, value in flat.items():
        print(f"  {key}: {value}")
    
    # 还原
    print("\n还原后:")
    restored = unflatten_json(flat)
    print(format_json(restored))


def example_search():
    """搜索示例"""
    print_section("JSON 搜索")
    
    data = {
        "name": "主项目",
        "manager": {
            "name": "李四",
            "email": "lisi@example.com"
        },
        "members": [
            {"name": "张三", "role": "developer"},
            {"name": "王五", "role": "designer"}
        ]
    }
    
    print("原始数据:")
    print(format_json(data))
    
    # 按键名搜索
    print("\n搜索键 'name':")
    results = find_all(data, key="name")
    for r in results:
        print(f"  {r.path}: {r.value}")
    
    # 按值搜索
    print("\n搜索值 '张三':")
    results = find_all(data, value="张三")
    for r in results:
        print(f"  {r.path}: {r.value}")
    
    # 正则搜索
    print("\n正则搜索邮箱:")
    results = grep_json(data, r'\w+@example\.com')
    for r in results:
        print(f"  {r.path}: {r.value}")


def example_filter_map():
    """过滤和映射示例"""
    print_section("过滤和映射")
    
    data = {
        "name": "项目A",
        "public_info": "可见",
        "secret": "密码123",
        "user": {
            "name": "张三",
            "secret": "另一个密码"
        }
    }
    
    print("原始数据:")
    print(format_json(data))
    
    # 过滤
    print("\n过滤掉包含 'secret' 的字段:")
    filtered = filter_json(data, lambda path, value: "secret" not in path)
    print(format_json(filtered))
    
    # 映射
    print("\n数值翻倍:")
    numbers = {"a": 1, "b": 2, "c": 3, "nested": {"x": 10, "y": 20}}
    doubled = map_json(numbers, lambda path, value: value * 2 if isinstance(value, (int, float)) else value)
    print(format_json(doubled))


def example_diff():
    """差异比较示例"""
    print_section("差异比较")
    
    old_data = {
        "name": "项目A",
        "version": "1.0",
        "users": [
            {"id": 1, "name": "张三"},
            {"id": 2, "name": "李四"}
        ],
        "config": {
            "debug": True,
            "timeout": 30
        }
    }
    
    new_data = {
        "name": "项目A（新）",
        "version": "2.0",
        "users": [
            {"id": 1, "name": "张三"},
            {"id": 2, "name": "王五"}  # 名字变了
        ],
        "config": {
            "debug": False,  # 值变了
            "timeout": 30
        }
    }
    
    print("旧数据:")
    print(format_json(old_data))
    print("\n新数据:")
    print(format_json(new_data))
    
    # 比较
    print("\n差异:")
    diffs = diff_json(old_data, new_data)
    for diff in diffs:
        print(f"  [{diff.change_type}] {diff.path}")
        print(f"    旧值: {diff.old_value}")
        print(f"    新值: {diff.new_value}")
    
    # 摘要
    print("\n摘要:")
    print(format_json(diff_summary(diffs)))


def example_merge():
    """合并示例"""
    print_section("JSON 合并")
    
    base = {
        "name": "项目",
        "version": "1.0",
        "config": {
            "debug": True,
            "timeout": 30
        }
    }
    
    overlay1 = {
        "version": "2.0",
        "config": {
            "timeout": 60
        }
    }
    
    overlay2 = {
        "author": "张三",
        "config": {
            "logLevel": "info"
        }
    }
    
    print("基础数据:")
    print(format_json(base))
    print("\n覆盖数据1:")
    print(format_json(overlay1))
    print("\n覆盖数据2:")
    print(format_json(overlay2))
    
    # 深度合并
    print("\n合并结果:")
    result = merge_json(base, overlay1, overlay2, deep=True)
    print(format_json(result))


def example_stats():
    """统计示例"""
    print_section("JSON 统计")
    
    data = {
        "name": "大型项目",
        "version": "1.0.0",
        "contributors": [
            {"name": "张三", "commits": 100},
            {"name": "李四", "commits": 50},
            {"name": "王五", "commits": 25}
        ],
        "config": {
            "debug": True,
            "features": {
                "auth": True,
                "api": True
            }
        }
    }
    
    print("数据:")
    print(format_json(data))
    
    print("\n统计信息:")
    stats = json_stats(data)
    print(f"  总键数: {stats['total_keys']}")
    print(f"  总值数: {stats['total_values']}")
    print(f"  最大深度: {stats['max_depth']}")
    print(f"  字节数: {stats['size_bytes']}")
    print(f"  类型分布: {stats['types']}")


def example_select_omit():
    """选择和排除示例"""
    print_section("选择和排除键")
    
    data = {
        "id": 1,
        "name": "张三",
        "email": "zhangsan@example.com",
        "password": "secret123",
        "created_at": "2024-01-01"
    }
    
    print("原始数据:")
    print(format_json(data))
    
    # 选择特定键
    print("\n选择 id, name, email:")
    selected = select_keys(data, ["id", "name", "email"])
    print(format_json(selected))
    
    # 排除特定键
    print("\n排除 password:")
    omitted = omit_keys(data, ["password"])
    print(format_json(omitted))


def example_walk():
    """遍历示例"""
    print_section("JSON 遍历")
    
    data = {
        "a": 1,
        "b": {"x": 2, "y": 3},
        "c": [4, 5, 6]
    }
    
    print("数据:")
    print(format_json(data))
    
    print("\n遍历所有路径和值:")
    for path, value in walk_json(data):
        print(f"  {path}: {value}")
    
    print("\n所有路径:")
    print(f"  {get_all_paths(data)}")


def example_json_utils_class():
    """JsonUtils 类示例"""
    print_section("JsonUtils 类")
    
    # 创建实例
    jutil = JsonUtils({
        "name": "测试",
        "user": {
            "id": 1,
            "tags": ["a", "b", "c"]
        }
    })
    
    print("初始数据:")
    print(jutil.to_string())
    
    # 路径操作
    print("\n路径操作:")
    print(f"  get('name'): {jutil.get('name')}")
    print(f"  get('user.id'): {jutil.get('user.id')}")
    print(f"  has('user.tags'): {jutil.has('user.tags')}")
    
    # 设置值
    print("\n设置值:")
    jutil.set("user.email", "test@example.com")
    print(f"  set('user.email', 'test@example.com')")
    print(f"  get('user.email'): {jutil.get('user.email')}")
    
    # 查找
    print("\n查找:")
    results = jutil.find(key="id")
    for r in results:
        print(f"  找到 id: {r.path} = {r.value}")
    
    # 统计
    print("\n统计:")
    stats = jutil.stats()
    print(f"  最大深度: {stats['max_depth']}")
    print(f"  总键数: {stats['total_keys']}")


def example_safe_operations():
    """安全操作示例"""
    print_section("安全操作")
    
    data = {
        "user": {
            "profile": {
                "name": "张三"
            }
        }
    }
    
    print("数据:")
    print(format_json(data))
    
    # 安全获取
    print("\n安全获取:")
    print(f"  safe_get(data, 'user', 'profile', 'name'): {safe_get(data, 'user', 'profile', 'name')}")
    print(f"  safe_get(data, 'user', 'missing', 'field', default='默认'): {safe_get(data, 'user', 'missing', 'field', default='默认')}")
    
    # 安全解析
    print("\n安全解析:")
    success, result = safe_string('{"valid": true}')
    print(f"  解析有效 JSON: 成功={success}, 结果={result}")
    
    success, result = safe_string('{"invalid": }')
    print(f"  解析无效 JSON: 成功={success}, 错误={result}")


def example_clone_equals():
    """克隆和比较示例"""
    print_section("克隆和比较")
    
    data = {
        "name": "项目",
        "items": [1, 2, {"x": 10}]
    }
    
    # 深度克隆
    print("深度克隆:")
    cloned = deep_clone(data)
    cloned["items"][2]["x"] = 100
    print(f"  原始数据 items[2].x: {data['items'][2]['x']}")
    print(f"  克隆数据 items[2].x: {cloned['items'][2]['x']}")
    
    # 深度比较
    print("\n深度比较:")
    a = {"x": [1, 2, {"y": 3}]}
    b = {"x": [1, 2, {"y": 3}]}
    c = {"x": [1, 2, {"y": 4}]}
    print(f"  a == b: {deep_equals(a, b)}")
    print(f"  a == c: {deep_equals(a, c)}")


def main():
    """运行所有示例"""
    example_formatting()
    example_validation()
    example_path_operations()
    example_flatten_unflatten()
    example_search()
    example_filter_map()
    example_diff()
    example_merge()
    example_stats()
    example_select_omit()
    example_walk()
    example_json_utils_class()
    example_safe_operations()
    example_clone_equals()
    
    print("\n" + "="*60)
    print("  所有示例运行完成!")
    print("="*60 + "\n")


if __name__ == '__main__':
    main()