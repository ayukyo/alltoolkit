"""
json_diff_utils 使用示例

演示 JSON 差异比较、JSON Patch 生成与应用等功能。
"""

import json
from mod import (
    JsonDiffer,
    JsonPatcher,
    JsonMergePatch,
    JsonDiffVisualizer,
    diff,
    diff_strings,
    generate_patch,
    apply_patch,
    generate_merge_patch,
    apply_merge_patch
)


def example_basic_diff():
    """基本差异比较示例"""
    print("=" * 60)
    print("示例 1: 基本 JSON 差异比较")
    print("=" * 60)
    
    old_user = {
        "id": 1,
        "name": "Alice",
        "age": 30,
        "email": "alice@example.com",
        "hobbies": ["reading", "gaming"]
    }
    
    new_user = {
        "id": 1,
        "name": "Alice",
        "age": 31,
        "email": "alice.new@example.com",
        "hobbies": ["reading", "traveling", "coding"],
        "phone": "123-456-7890"
    }
    
    result = diff(old_user, new_user)
    
    print("\n旧数据:")
    print(json.dumps(old_user, indent=2, ensure_ascii=False))
    
    print("\n新数据:")
    print(json.dumps(new_user, indent=2, ensure_ascii=False))
    
    print("\n差异结果:")
    print(result)
    
    print("\n统计信息:")
    print(f"  新增: {result.stats['added']}")
    print(f"  删除: {result.stats['removed']}")
    print(f"  修改: {result.stats['modified']}")


def example_nested_diff():
    """嵌套对象差异示例"""
    print("\n" + "=" * 60)
    print("示例 2: 嵌套对象差异比较")
    print("=" * 60)
    
    old_config = {
        "app": {
            "name": "MyApp",
            "version": "1.0.0",
            "settings": {
                "debug": False,
                "database": {
                    "host": "localhost",
                    "port": 5432
                }
            }
        }
    }
    
    new_config = {
        "app": {
            "name": "MyApp",
            "version": "2.0.0",
            "settings": {
                "debug": True,
                "database": {
                    "host": "db.example.com",
                    "port": 5432,
                    "ssl": True
                },
                "cache": {
                    "enabled": True
                }
            }
        }
    }
    
    result = diff(old_config, new_config)
    
    print("\n差异:")
    for d in result.diffs:
        if d.change_type.value == "added":
            print(f"  + {d.path}: {d.new_value}")
        elif d.change_type.value == "removed":
            print(f"  - {d.path}: {d.old_value}")
        else:
            print(f"  ~ {d.path}: {d.old_value} -> {d.new_value}")


def example_ignore_keys():
    """忽略特定键示例"""
    print("\n" + "=" * 60)
    print("示例 3: 忽略特定键（如时间戳）")
    print("=" * 60)
    
    old_data = {
        "name": "Alice",
        "updated_at": "2024-01-01T00:00:00Z",
        "version": 1
    }
    
    new_data = {
        "name": "Alice",
        "updated_at": "2024-01-02T00:00:00Z",
        "version": 2
    }
    
    # 不忽略任何键
    result_all = diff(old_data, new_data)
    print(f"\n比较所有键: {result_all.stats['modified']} 个变化")
    
    # 忽略 updated_at
    result_ignore = diff(old_data, new_data, ignore_keys=["updated_at"])
    print(f"忽略 updated_at: {result_ignore.stats['modified']} 个变化")


def example_json_patch():
    """JSON Patch 示例"""
    print("\n" + "=" * 60)
    print("示例 4: JSON Patch (RFC 6902)")
    print("=" * 60)
    
    original = {
        "name": "Alice",
        "age": 30
    }
    
    target = {
        "name": "Alice",
        "age": 31,
        "email": "alice@example.com"
    }
    
    # 生成补丁
    patches = generate_patch(original, target)
    
    print("\n原始数据:")
    print(json.dumps(original, indent=2))
    
    print("\n目标数据:")
    print(json.dumps(target, indent=2))
    
    print("\n生成的 JSON Patch:")
    for p in patches:
        print(f"  {p}")
    
    # 应用补丁
    result = apply_patch(original, patches)
    print("\n应用补丁后:")
    print(json.dumps(result, indent=2))
    
    print(f"\n补丁应用成功: {result == target}")


def test_json_patch_operations():
    """JSON Patch 各种操作示例"""
    print("\n" + "=" * 60)
    print("示例 5: JSON Patch 各种操作")
    print("=" * 60)
    
    data = {"users": ["Alice", "Bob"]}
    
    print("\n初始数据:")
    print(json.dumps(data, indent=2))
    
    # 添加操作
    patches = [
        {"op": "add", "path": "/users/2", "value": "Charlie"},
        {"op": "add", "path": "/count", "value": 3}
    ]
    result = apply_patch(data, patches)
    print("\n添加 Charlie 和 count:")
    print(json.dumps(result, indent=2))
    
    # 替换操作
    patches = [{"op": "replace", "path": "/users/0", "value": "Alice2"}]
    result = apply_patch(result, patches)
    print("\n替换第一个用户:")
    print(json.dumps(result, indent=2))
    
    # 移动操作
    patches = [{"op": "move", "from": "/users/2", "path": "/users/0"}]
    result = apply_patch(result, patches)
    print("\n移动 Charlie 到开头:")
    print(json.dumps(result, indent=2))
    
    # 复制操作
    patches = [{"op": "copy", "from": "/users/0", "path": "/users/-"}]  # - 表示数组末尾
    # 注意：简化版本可能不支持 - 符号，这里用具体索引
    patches = [{"op": "copy", "from": "/users/0", "path": "/users/3"}]
    result = apply_patch(result, patches)
    print("\n复制第一个用户到末尾:")
    print(json.dumps(result, indent=2))
    
    # 删除操作
    patches = [{"op": "remove", "path": "/count"}]
    result = apply_patch(result, patches)
    print("\n删除 count:")
    print(json.dumps(result, indent=2))


def example_json_merge_patch():
    """JSON Merge Patch 示例"""
    print("\n" + "=" * 60)
    print("示例 6: JSON Merge Patch (RFC 7396)")
    print("=" * 60)
    
    original = {
        "name": "Alice",
        "age": 30,
        "email": "alice@example.com"
    }
    
    patch = {
        "age": 31,
        "email": None  # null 表示删除
    }
    
    print("\n原始数据:")
    print(json.dumps(original, indent=2))
    
    print("\nMerge Patch:")
    print(json.dumps(patch, indent=2))
    
    result = apply_merge_patch(original, patch)
    
    print("\n应用后:")
    print(json.dumps(result, indent=2))
    
    # 生成 Merge Patch
    old = {"a": 1, "b": 2, "c": 3}
    new = {"a": 1, "b": 3}
    
    generated_patch = generate_merge_patch(old, new)
    print("\n从差异生成 Merge Patch:")
    print(f"  旧: {old}")
    print(f"  新: {new}")
    print(f"  补丁: {generated_patch}")


def example_visualization():
    """可视化示例"""
    print("\n" + "=" * 60)
    print("示例 7: 差异可视化")
    print("=" * 60)
    
    old_data = {
        "name": "Alice",
        "age": 30,
        "hobbies": ["reading"],
        "address": {
            "city": "Beijing"
        }
    }
    
    new_data = {
        "name": "Alice",
        "age": 31,
        "hobbies": ["reading", "coding"],
        "address": {
            "city": "Shanghai",
            "zip": "200000"
        },
        "email": "alice@example.com"
    }
    
    result = diff(old_data, new_data)
    
    print("\n彩色终端输出:")
    print(JsonDiffVisualizer.to_colored_text(result))
    
    print("\nMarkdown 输出:")
    print(JsonDiffVisualizer.to_markdown(result))
    
    print("\nHTML 输出:")
    print(JsonDiffVisualizer.to_html(result))


def example_array_id_matching():
    """基于 ID 的数组匹配示例"""
    print("\n" + "=" * 60)
    print("示例 8: 基于 ID 的数组匹配")
    print("=" * 60)
    
    old_users = {
        "users": [
            {"id": 1, "name": "Alice", "role": "admin"},
            {"id": 2, "name": "Bob", "role": "user"},
            {"id": 3, "name": "Charlie", "role": "user"}
        ]
    }
    
    new_users = {
        "users": [
            {"id": 1, "name": "Alice", "role": "super_admin"},  # 角色变更
            {"id": 2, "name": "Bob", "role": "user"},
            # Charlie 被删除
            {"id": 4, "name": "David", "role": "user"}  # 新增
        ]
    }
    
    # 使用 ID 字段匹配数组元素
    differ = JsonDiffer(array_id_field="id")
    result = differ.diff(old_users, new_users)
    
    print("\n旧用户列表:")
    for u in old_users["users"]:
        print(f"  - {u['id']}: {u['name']} ({u['role']})")
    
    print("\n新用户列表:")
    for u in new_users["users"]:
        print(f"  - {u['id']}: {u['name']} ({u['role']})")
    
    print("\n差异:")
    for d in result.diffs:
        if d.change_type.value == "modified":
            print(f"  ~ {d.path}: {d.old_value} -> {d.new_value}")
        elif d.change_type.value == "added":
            print(f"  + {d.path}: {d.new_value}")
        elif d.change_type.value == "removed":
            print(f"  - {d.path}: {d.old_value}")


def example_diff_strings():
    """JSON 字符串比较示例"""
    print("\n" + "=" * 60)
    print("示例 9: JSON 字符串比较")
    print("=" * 60)
    
    old_json = '''
    {
        "name": "Alice",
        "scores": [85, 90, 78]
    }
    '''
    
    new_json = '''
    {
        "name": "Alice",
        "scores": [85, 92, 78]
    }
    '''
    
    result = diff_strings(old_json, new_json)
    
    print("JSON 字符串差异:")
    for d in result.diffs:
        print(f"  {d}")


def example_real_world_config():
    """实际应用：配置文件差异"""
    print("\n" + "=" * 60)
    print("示例 10: 实际应用 - 配置文件变更追踪")
    print("=" * 60)
    
    old_config = {
        "database": {
            "host": "localhost",
            "port": 5432,
            "pool_size": 10
        },
        "cache": {
            "enabled": False,
            "ttl": 300
        },
        "logging": {
            "level": "INFO",
            "file": "/var/log/app.log"
        }
    }
    
    new_config = {
        "database": {
            "host": "db.production.com",
            "port": 5432,
            "pool_size": 20,
            "ssl": True
        },
        "cache": {
            "enabled": True,
            "ttl": 600,
            "type": "redis"
        },
        "logging": {
            "level": "WARNING",
            "file": "/var/log/app.log"
        }
    }
    
    result = diff(old_config, new_config)
    
    print("\n配置变更报告:")
    print(f"总变更数: {result.stats['total']}")
    print(f"新增: {result.stats['added']}")
    print(f"删除: {result.stats['removed']}")
    print(f"修改: {result.stats['modified']}")
    
    # 按模块分组显示
    db_changes = result.filter_by_path(r"database\.")
    cache_changes = result.filter_by_path(r"cache\.")
    log_changes = result.filter_by_path(r"logging\.")
    
    if db_changes:
        print(f"\n数据库配置 ({len(db_changes)} 个变更):")
        for c in db_changes:
            print(f"  {c}")
    
    if cache_changes:
        print(f"\n缓存配置 ({len(cache_changes)} 个变更):")
        for c in cache_changes:
            print(f"  {c}")
    
    if log_changes:
        print(f"\n日志配置 ({len(log_changes)} 个变更):")
        for c in log_changes:
            print(f"  {c}")


if __name__ == "__main__":
    example_basic_diff()
    example_nested_diff()
    example_ignore_keys()
    example_json_patch()
    test_json_patch_operations()
    example_json_merge_patch()
    example_visualization()
    example_array_id_matching()
    example_diff_strings()
    example_real_world_config()
    
    print("\n" + "=" * 60)
    print("所有示例完成!")
    print("=" * 60)