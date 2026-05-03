#!/usr/bin/env python3
"""
json_flatten_utils 使用示例
===========================

展示各种实际使用场景。
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    flatten_dict,
    unflatten_dict,
    flatten_list,
    deep_merge,
    get_nested_value,
    set_nested_value,
    delete_nested_value,
    has_nested_key,
    diff_dicts,
    dict_paths,
    dict_depth,
    pick_keys,
    omit_keys,
)


def example_basic_flatten():
    """基本扁平化示例"""
    print("\n" + "="*50)
    print("示例: 基本字典扁平化")
    print("="*50)
    
    # 用户数据
    user_data = {
        "user": {
            "name": "Alice",
            "age": 30,
            "address": {
                "city": "Beijing",
                "country": "China",
                "zip": "100000"
            }
        },
        "status": "active"
    }
    
    print("\n原始数据:")
    print(f"  {user_data}")
    
    # 扁平化
    flat = flatten_dict(user_data)
    print("\n扁平化后:")
    for key, value in flat.items():
        print(f"  {key}: {value}")
    
    # 反扁平化
    restored = unflatten_dict(flat)
    print("\n反扁平化后:")
    print(f"  {restored}")
    
    # 验证一致性
    assert restored["user"]["name"] == user_data["user"]["name"]
    print("\n✓ 数据一致性验证通过")


def example_custom_separator():
    """自定义分隔符示例"""
    print("\n" + "="*50)
    print("示例: 自定义分隔符")
    print("="*50)
    
    data = {"api": {"v1": {"users": {"endpoint": "/users"}}}}
    
    # 点号分隔符（默认）
    print("\n点号分隔符:")
    print(f"  {flatten_dict(data)}")
    
    # 下划线分隔符
    print("\n下划线分隔符:")
    print(f"  {flatten_dict(data, separator='_')}")
    
    # 斜杠分隔符（适合URL）
    print("\n斜杠分隔符:")
    print(f"  {flatten_dict(data, separator='/')}")


def example_list_flattening():
    """列表扁平化示例"""
    print("\n" + "="*50)
    print("示例: 列表扁平化")
    print("="*50)
    
    # 包含列表的数据
    order_data = {
        "order": {
            "id": "ORD-001",
            "items": [
                {"name": "Product A", "price": 100, "qty": 2},
                {"name": "Product B", "price": 200, "qty": 1}
            ],
            "total": 400
        }
    }
    
    print("\n原始订单数据:")
    print(f"  id: {order_data['order']['id']}")
    print(f"  items: [{len(order_data['order']['items'])} items]")
    print(f"  total: {order_data['order']['total']}")
    
    # 扁平化列表中的字典
    flat = flatten_dict(order_data, flatten_lists=True)
    print("\n扁平化后（包含列表项）:")
    for key, value in flat.items():
        print(f"  {key}: {value}")
    
    # 自定义列表索引格式
    flat_custom = flatten_dict(order_data, flatten_lists=True, list_index_format="_{}")
    print("\n自定义索引格式（_{}）:")
    for key, value in flat_custom.items():
        if "item" in key:
            print(f"  {key}: {value}")


def example_depth_control():
    """深度控制示例"""
    print("\n" + "="*50)
    print("示例: 深度控制")
    print("="*50)
    
    deep_data = {
        "level1": {
            "level2": {
                "level3": {
                    "level4": {
                        "value": "deep_value"
                    }
                }
            }
        }
    }
    
    print(f"\n嵌套深度: {dict_depth(deep_data)}")
    
    # 无限制
    print("\n无深度限制:")
    flat = flatten_dict(deep_data)
    print(f"  键: {list(flat.keys())}")
    
    # 深度限制为2
    print("\n深度限制=2:")
    flat = flatten_dict(deep_data, max_depth=2)
    print(f"  键: {list(flat.keys())}")
    print(f"  值: {flat['level1.level2']}")


def example_deep_merge():
    """深度合并示例"""
    print("\n" + "="*50)
    print("示例: 深度合并")
    print("="*50)
    
    # 默认配置
    default_config = {
        "server": {
            "host": "localhost",
            "port": 8080,
            "timeout": 30
        },
        "logging": {
            "level": "INFO",
            "format": "simple"
        }
    }
    
    # 用户配置
    user_config = {
        "server": {
            "port": 3000,
            "ssl": True
        },
        "logging": {
            "level": "DEBUG"
        }
    }
    
    print("\n默认配置:")
    print(f"  server.port: {default_config['server']['port']}")
    print(f"  logging.level: {default_config['logging']['level']}")
    
    print("\n用户配置:")
    print(f"  server.port: {user_config['server']['port']}")
    print(f"  logging.level: {user_config['logging']['level']}")
    
    # 合并
    merged = deep_merge(default_config, user_config)
    print("\n合并结果:")
    print(f"  server.host: {merged['server']['host']} (来自默认)")
    print(f"  server.port: {merged['server']['port']} (来自用户)")
    print(f"  server.ssl: {merged['server']['ssl']} (来自用户)")
    print(f"  server.timeout: {merged['server']['timeout']} (来自默认)")
    print(f"  logging.level: {merged['logging']['level']} (来自用户)")
    
    # 不覆盖模式
    merged_no_overwrite = deep_merge(default_config, user_config, overwrite=False)
    print("\n不覆盖模式:")
    print(f"  server.port: {merged_no_overwrite['server']['port']} (保持默认)")
    
    # 列表合并
    list_data1 = {"tags": ["python", "code"]}
    list_data2 = {"tags": ["js", "web"]}
    merged_lists = deep_merge(list_data1, list_data2, merge_lists=True)
    print("\n列表合并:")
    print(f"  tags: {merged_lists['tags']}")


def example_nested_operations():
    """嵌套值操作示例"""
    print("\n" + "="*50)
    print("示例: 嵌套值操作")
    print("="*50)
    
    data = {"user": {"profile": {"name": "Alice", "email": "alice@example.com"}}}
    
    print("\n原始数据:")
    print(f"  {data}")
    
    # 获取值
    name = get_nested_value(data, "user.profile.name")
    print(f"\n获取 user.profile.name: {name}")
    
    # 获取不存在的值（带默认值）
    phone = get_nested_value(data, "user.profile.phone", default="N/A")
    print(f"获取 user.profile.phone (默认): {phone}")
    
    # 设置值
    data = set_nested_value(data, "user.profile.phone", "123-456-7890")
    print(f"\n设置 user.profile.phone 后:")
    print(f"  phone: {data['user']['profile']['phone']}")
    
    # 创建新路径
    data = set_nested_value(data, "user.settings.theme", "dark")
    print(f"\n创建 user.settings.theme:")
    print(f"  theme: {data['user']['settings']['theme']}")
    
    # 检查键是否存在
    print(f"\n检查键存在:")
    print(f"  user.profile.name 存在: {has_nested_key(data, 'user.profile.name')}")
    print(f"  user.profile.avatar 存在: {has_nested_key(data, 'user.profile.avatar')}")
    
    # 删除值
    data = delete_nested_value(data, "user.profile.phone")
    print(f"\n删除 user.profile.phone 后:")
    print(f"  phone 存在: {has_nested_key(data, 'user.profile.phone')}")


def example_diff_comparison():
    """差异比较示例"""
    print("\n" + "="*50)
    print("示例: 字典差异比较")
    print("="*50)
    
    # 版本1数据
    v1_data = {
        "user": {"name": "Alice", "role": "admin"},
        "settings": {"theme": "light", "lang": "en"},
        "features": {"beta": False}
    }
    
    # 版本2数据
    v2_data = {
        "user": {"name": "Alice", "role": "user", "email": "alice@new.com"},
        "settings": {"theme": "dark", "lang": "en"},
        "features": {"beta": True, "new_feature": True}
    }
    
    print("\n版本1:")
    print(f"  user.role: admin")
    print(f"  settings.theme: light")
    print(f"  features.beta: False")
    
    print("\n版本2:")
    print(f"  user.role: user")
    print(f"  user.email: alice@new.com (新增)")
    print(f"  settings.theme: dark")
    print(f"  features.beta: True")
    print(f"  features.new_feature: True (新增)")
    
    # 比较差异
    diff = diff_dicts(v1_data, v2_data)
    
    print("\n差异结果:")
    print("\n新增的键:")
    for key, value in diff["added"].items():
        print(f"  + {key}: {value}")
    
    print("\n移除的键:")
    for key, value in diff["removed"].items():
        print(f"  - {key}: {value}")
    
    print("\n变化的键:")
    for key, change in diff["changed"].items():
        print(f"  ~ {key}: {change['old']} -> {change['new']}")
    
    print("\n不变的键:")
    for key, value in diff["unchanged"].items():
        print(f"  = {key}: {value}")


def example_pick_omit():
    """选取和排除示例"""
    print("\n" + "="*50)
    print("示例: 键选取和排除")
    print("="*50)
    
    profile_data = {
        "user": {
            "id": 123,
            "name": "Alice",
            "email": "alice@example.com",
            "password": "secret123",  # 敏感字段
            "ssn": "123-45-6789"       # 敏感字段
        },
        "public": {
            "bio": "Developer",
            "website": "alice.dev"
        }
    }
    
    print("\n原始数据（包含敏感信息）:")
    print(f"  user.password: [HIDDEN]")
    print(f"  user.ssn: [HIDDEN]")
    
    # 选取公开字段
    public_fields = ["user.id", "user.name", "public.bio", "public.website"]
    public_data = pick_keys(profile_data, public_fields)
    print("\n选取公开字段:")
    for key in dict_paths(public_data):
        print(f"  {key}")
    
    # 排除敏感字段
    safe_data = omit_keys(profile_data, ["user.password", "user.ssn"])
    print("\n排除敏感字段:")
    flat_safe = flatten_dict(safe_data)
    for key in flat_safe:
        print(f"  {key}")
    
    # 验证敏感字段已移除
    assert not has_nested_key(safe_data, "user.password")
    assert not has_nested_key(safe_data, "user.ssn")
    print("\n✓ 敏感字段已安全移除")


def example_flatten_list():
    """列表扁平化示例"""
    print("\n" + "="*50)
    print("示例: 列表扁平化")
    print("="*50)
    
    nested_list = [1, [2, [3, [4, [5]]]], 6, [7, 8]]
    
    print("\n原始嵌套列表:")
    print(f"  {nested_list}")
    
    # 完全扁平化
    flat = flatten_list(nested_list)
    print("\n完全扁平化:")
    print(f"  {flat}")
    
    # 深度限制
    flat_depth2 = flatten_list(nested_list, max_depth=2)
    print("\n深度限制=2:")
    print(f"  {flat_depth2}")
    
    # 混合类型
    mixed = [1, (2, 3), [4, [5, 6]], {7, 8}]
    flat_mixed = flatten_list(mixed, preserve_types=True)
    print("\n混合类型扁平化（保留元组/集合）:")
    print(f"  {flat_mixed}")


def example_api_response():
    """API响应处理示例"""
    print("\n" + "="*50)
    print("示例: API响应处理")
    print("="*50)
    
    # 模拟API响应
    api_response = {
        "status": "success",
        "data": {
            "users": [
                {
                    "id": 1,
                    "profile": {"name": "Alice", "role": "admin"},
                    "stats": {"posts": 100, "followers": 500}
                },
                {
                    "id": 2,
                    "profile": {"name": "Bob", "role": "user"},
                    "stats": {"posts": 50, "followers": 200}
                }
            ],
            "meta": {"total": 2, "page": 1}
        }
    }
    
    print("\nAPI响应结构:")
    print(f"  状态: {api_response['status']}")
    print(f"  用户数: {api_response['data']['meta']['total']}")
    
    # 扁平化
    flat = flatten_dict(api_response, flatten_lists=True)
    print("\n扁平化后的键:")
    for key in sorted(flat.keys()):
        if "profile" in key or "stats" in key:
            print(f"  {key}: {flat[key]}")
    
    # 提取用户数据
    print("\n提取第一个用户数据:")
    user1_name = get_nested_value(flat, "data.users[0].profile.name")
    user1_posts = get_nested_value(flat, "data.users[0].stats.posts")
    print(f"  名称: {user1_name}")
    print(f"  帖子数: {user1_posts}")


def example_config_migration():
    """配置迁移示例"""
    print("\n" + "="*50)
    print("示例: 配置迁移")
    print("="*50)
    
    old_config = {
        "database": {
            "host": "localhost",
            "port": 3306,
            "credentials": {
                "user": "root",
                "password": "old_pass"
            }
        },
        "features": {
            "cache": True,
            "logging": False
        }
    }
    
    new_config_template = {
        "database": {
            "host": "db.example.com",
            "port": 5432,
            "credentials": {
                "user": "admin",
                "password": "new_pass"
            },
            "ssl": True  # 新增
        },
        "features": {
            "cache": True,
            "logging": True,
            "monitoring": True  # 新增
        }
    }
    
    print("\n旧配置:")
    print(f"  database.host: {old_config['database']['host']}")
    print(f"  database.port: {old_config['database']['port']}")
    
    print("\n新配置模板:")
    print(f"  database.host: {new_config_template['database']['host']}")
    print(f"  database.ssl: {new_config_template['database']['ssl']} (新增)")
    
    # 比较差异
    diff = diff_dicts(old_config, new_config_template)
    
    print("\n迁移需要处理的变化:")
    
    if diff["added"]:
        print("\n新增配置项:")
        for key in diff["added"]:
            print(f"  + {key}")
    
    if diff["changed"]:
        print("\n变更配置项:")
        for key, change in diff["changed"].items():
            print(f"  ~ {key}: {change['old']} -> {change['new']}")
    
    if diff["removed"]:
        print("\n废弃配置项:")
        for key in diff["removed"]:
            print(f"  - {key}")


def run_all_examples():
    """运行所有示例"""
    print("\n" + "="*60)
    print("json_flatten_utils 使用示例集")
    print("="*60)
    
    examples = [
        example_basic_flatten,
        example_custom_separator,
        example_list_flattening,
        example_depth_control,
        example_deep_merge,
        example_nested_operations,
        example_diff_comparison,
        example_pick_omit,
        example_flatten_list,
        example_api_response,
        example_config_migration,
    ]
    
    for example in examples:
        try:
            example()
        except Exception as e:
            print(f"\n✗ 示例 {example.__name__} 失败: {e}")
    
    print("\n" + "="*60)
    print("所有示例运行完成")
    print("="*60 + "\n")


if __name__ == "__main__":
    run_all_examples()