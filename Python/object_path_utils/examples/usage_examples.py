"""
Object Path Utils - 使用示例

演示对象路径操作工具的各种用法。
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    get, set, delete, has, paths, flatten, unflatten,
    pick, omit, merge, ObjectPath
)


def example_basic_get():
    """基本获取操作"""
    print("=== 基本获取操作 ===\n")
    
    # 简单字典
    user = {
        "name": "Alice",
        "age": 30,
        "email": "alice@example.com"
    }
    
    print(f"用户名: {get(user, 'name')}")
    print(f"年龄: {get(user, 'age')}")
    print(f"不存在的字段: {get(user, 'phone', '未设置')}")
    print()


def example_nested_access():
    """嵌套对象访问"""
    print("=== 嵌套对象访问 ===\n")
    
    # 复杂嵌套结构
    data = {
        "user": {
            "profile": {
                "name": "Alice",
                "settings": {
                    "theme": "dark",
                    "language": "zh-CN"
                }
            },
            "stats": {
                "login_count": 42,
                "last_login": "2024-01-15"
            }
        },
        "app": {
            "version": "2.0.0",
            "config": {
                "debug": False,
                "log_level": "INFO"
            }
        }
    }
    
    print(f"用户名: {get(data, 'user.profile.name')}")
    print(f"主题: {get(data, 'user.profile.settings.theme')}")
    print(f"登录次数: {get(data, 'user.stats.login_count')}")
    print(f"应用版本: {get(data, 'app.version')}")
    print(f"不存在的深层路径: {get(data, 'user.profile.avatar.url', '默认头像')}")
    print()


def example_array_access():
    """数组访问"""
    print("=== 数组访问 ===\n")
    
    data = {
        "users": [
            {"id": 1, "name": "Alice"},
            {"id": 2, "name": "Bob"},
            {"id": 3, "name": "Charlie"}
        ],
        "matrix": [
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9]
        ],
        "tags": ["python", "javascript", "rust"]
    }
    
    print(f"第一个用户: {get(data, 'users[0]')}")
    print(f"第二个用户名: {get(data, 'users[1].name')}")
    print(f"矩阵中心元素: {get(data, 'matrix[1][1]')}")
    print(f"第三个标签: {get(data, 'tags[2]')}")
    print(f"越界访问: {get(data, 'tags[10]', '不存在')}")
    print()


def example_set_operations():
    """设置操作"""
    print("=== 设置操作 ===\n")
    
    # 创建嵌套结构
    config = {}
    set(config, "database.host", "localhost")
    set(config, "database.port", 5432)
    set(config, "database.credentials.username", "admin")
    set(config, "database.credentials.password", "secret")
    
    print("创建的配置:")
    print(config)
    print()
    
    # 修改现有值
    set(config, "database.port", 5433)
    print(f"修改后的端口: {get(config, 'database.port')}")
    print()
    
    # 创建数组
    data = {}
    set(data, "items[0]", "first")
    set(data, "items[2]", "third")  # 自动扩展数组
    
    print(f"自动扩展的数组: {get(data, 'items')}")
    print()


def example_delete_operations():
    """删除操作"""
    print("=== 删除操作 ===\n")
    
    user = {
        "name": "Alice",
        "age": 30,
        "email": "alice@example.com",
        "temp": "should be removed"
    }
    
    print(f"删除前: {user}")
    
    result = delete(user, "temp")
    print(f"删除 'temp': {result}")
    print(f"删除后: {user}")
    
    # 删除嵌套字段
    data = {
        "user": {
            "name": "Alice",
            "password": "secret123"
        }
    }
    
    delete(data, "user.password")
    print(f"删除密码后: {data}")
    print()


def example_has_operations():
    """检查存在性"""
    print("=== 检查存在性 ===\n")
    
    config = {
        "database": {
            "host": "localhost",
            "port": 5432
        },
        "cache": None
    }
    
    print(f"数据库主机存在: {has(config, 'database.host')}")
    print(f"数据库密码存在: {has(config, 'database.password')}")
    print(f"缓存存在（值为 None）: {has(config, 'cache')}")
    print()


def example_paths_list():
    """列出所有路径"""
    print("=== 列出所有路径 ===\n")
    
    data = {
        "user": {
            "name": "Alice",
            "roles": ["admin", "user"]
        },
        "settings": {
            "theme": "dark"
        }
    }
    
    all_paths = paths(data)
    print("所有路径:")
    for p in all_paths:
        print(f"  - {p}")
    print()


def example_flatten():
    """扁平化操作"""
    print("=== 扁平化操作 ===\n")
    
    config = {
        "database": {
            "host": "localhost",
            "port": 5432,
            "credentials": {
                "username": "admin",
                "password": "secret"
            }
        },
        "cache": {
            "enabled": True,
            "ttl": 3600
        }
    }
    
    flat = flatten(config)
    print("扁平化后:")
    for key, value in flat.items():
        print(f"  {key}: {value}")
    print()
    
    # 自定义分隔符
    flat_underscore = flatten(config, separator="_")
    print("使用下划线分隔符:")
    for key, value in flat_underscore.items():
        print(f"  {key}: {value}")
    print()


def example_unflatten():
    """反扁平化操作"""
    print("=== 反扁平化操作 ===\n")
    
    # 环境变量风格的配置
    env_config = {
        "APP_NAME": "MyApp",
        "APP_VERSION": "1.0.0",
        "DB_HOST": "localhost",
        "DB_PORT": "5432",
        "DB_USER": "admin"
    }
    
    # 转换为小写并用点分隔
    normalized = {k.lower().replace("_", "."): v for k, v in env_config.items()}
    config = unflatten(normalized)
    
    print("环境变量转换后的配置:")
    print(config)
    print()


def example_pick_omit():
    """选取和排除"""
    print("=== 选取和排除 ===\n")
    
    user = {
        "id": 1,
        "name": "Alice",
        "email": "alice@example.com",
        "password_hash": "xxx",
        "created_at": "2024-01-01",
        "updated_at": "2024-01-15"
    }
    
    # 只选取需要的字段
    public_data = pick(user, "id", "name", "email")
    print("公开数据:")
    print(public_data)
    print()
    
    # 排除敏感字段
    safe_data = omit(user, "password_hash")
    print("安全数据（排除密码）:")
    print(safe_data)
    print()


def example_merge():
    """合并对象"""
    print("=== 合并对象 ===\n")
    
    # 默认配置
    default_config = {
        "database": {
            "host": "localhost",
            "port": 5432,
            "pool_size": 10
        },
        "cache": {
            "enabled": True,
            "ttl": 3600
        }
    }
    
    # 用户配置
    user_config = {
        "database": {
            "host": "production-db.example.com",
            "username": "admin"
        },
        "cache": {
            "ttl": 7200
        }
    }
    
    # 深度合并
    merged = merge(default_config, user_config)
    print("合并后的配置:")
    print(merged)
    print()


def example_object_path_class():
    """ObjectPath 类使用"""
    print("=== ObjectPath 类 ===\n")
    
    # 创建 ObjectPath 实例
    op = ObjectPath({})
    
    # 链式设置
    op.set("user.name", "Alice") \
      .set("user.age", 30) \
      .set("user.tags", ["admin", "user"])
    
    print("设置后的对象:")
    print(op.obj)
    print()
    
    # 链式操作
    print(f"用户名: {op.get('user.name')}")
    print(f"第一个标签: {op.get('user.tags[0]')}")
    print(f"路径存在 'user.email': {op.has('user.email')}")
    print()
    
    # 获取所有路径
    print("所有路径:")
    for p in op.paths():
        print(f"  - {p}")
    print()


def example_real_world():
    """实际应用场景"""
    print("=== 实际应用场景 ===\n")
    
    # 场景 1: API 响应处理
    print("场景 1: API 响应处理")
    api_response = {
        "code": 200,
        "data": {
            "user": {
                "id": 123,
                "profile": {
                    "nickname": "Alice",
                    "avatar": "https://example.com/avatar.jpg"
                }
            },
            "meta": {
                "total": 1,
                "page": 1
            }
        }
    }
    
    # 安全地提取嵌套数据
    user_id = get(api_response, "data.user.id", 0)
    nickname = get(api_response, "data.user.profile.nickname", "未知用户")
    
    print(f"用户ID: {user_id}")
    print(f"昵称: {nickname}")
    print()
    
    # 场景 2: 配置文件处理
    print("场景 2: 配置文件处理")
    
    # 从扁平配置创建嵌套配置
    flat_config = {
        "server.host": "0.0.0.0",
        "server.port": "8080",
        "server.ssl.enabled": "true",
        "server.ssl.cert": "/path/to/cert.pem",
        "database.url": "postgresql://localhost/mydb",
        "database.pool.min": "5",
        "database.pool.max": "20"
    }
    
    # 转换为嵌套结构
    nested_config = unflatten(flat_config)
    print("嵌套配置:")
    import json
    print(json.dumps(nested_config, indent=2, ensure_ascii=False))
    print()
    
    # 场景 3: 表单数据提取
    print("场景 3: 表单数据提取")
    form_data = {
        "user.name": "Alice",
        "user.email": "alice@example.com",
        "user.phone": "123-456-7890",
        "preferences.theme": "dark",
        "preferences.language": "zh-CN"
    }
    
    # 只提取用户信息
    user_info = {k: v for k, v in form_data.items() if k.startswith("user.")}
    print("用户信息:")
    print(user_info)
    print()
    
    # 场景 4: JSON Patch 操作
    print("场景 4: JSON Patch 风格操作")
    document = {
        "users": [
            {"id": 1, "name": "Alice", "active": True},
            {"id": 2, "name": "Bob", "active": False}
        ]
    }
    
    # 使用路径修改特定元素
    set(document, "users[0].active", False)
    set(document, "users[1].active", True)
    
    print("修改后的文档:")
    print(document)
    print()


def main():
    """运行所有示例"""
    example_basic_get()
    example_nested_access()
    example_array_access()
    example_set_operations()
    example_delete_operations()
    example_has_operations()
    example_paths_list()
    example_flatten()
    example_unflatten()
    example_pick_omit()
    example_merge()
    example_object_path_class()
    example_real_world()
    
    print("=" * 50)
    print("所有示例演示完成！")
    print("=" * 50)


if __name__ == "__main__":
    main()