#!/usr/bin/env python3
"""
AllToolkit - YAML Utilities 使用示例

本文件展示了 yaml_utils 模块的各种使用场景。

运行方式:
    python basic_usage.py

依赖:
    pip install PyYAML  # 推荐，获得完整功能
    # 或无需安装（使用 JSON 降级模式）
"""

import os
import sys
import tempfile
from pathlib import Path

# 添加父目录到路径以导入 mod
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 导入 yaml_utils 模块
from mod import (
    # 版本信息
    get_version,
    is_pyyaml_available,
    get_module_info,
    
    # 读取功能
    load_yaml,
    load_yaml_string,
    load_yaml_file,
    safe_load_yaml,
    
    # 写入功能
    dump_yaml,
    dump_yaml_file,
    dump_yaml_string,
    
    # 验证功能
    validate_yaml,
    is_valid_yaml,
    
    # 转换功能
    yaml_to_json,
    json_to_yaml,
    
    # 合并功能
    merge_yaml,
    
    # 差分功能
    diff_yaml,
    
    # 便捷功能
    get_yaml_value,
    set_yaml_value,
    delete_yaml_key,
    
    # 安全功能
    contains_unsafe_tags,
    
    # 工具功能
    get_yaml_info,
)


def print_section(title):
    """打印章节标题。"""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def example_01_basic_info():
    """示例 1: 基本信息"""
    print_section("示例 1: 基本信息")
    
    print(f"模块版本：{get_version()}")
    print(f"PyYAML 可用：{is_pyyaml_available()}")
    
    info = get_module_info()
    print(f"模块信息：{info}")


def example_02_load_yaml():
    """示例 2: 加载 YAML"""
    print_section("示例 2: 加载 YAML")
    
    # 从字符串加载
    yaml_str = """
name: 示例配置
version: 1.0
database:
  host: localhost
  port: 5432
  name: mydb
features:
  - 用户管理
  - 数据导出
  - 报表生成
enabled: true
"""
    
    data = load_yaml_string(yaml_str)
    print(f"加载的数据：{data}")
    print(f"名称：{data['name']}")
    print(f"数据库主机：{data['database']['host']}")
    print(f"功能列表：{data['features']}")


def example_03_save_yaml():
    """示例 3: 保存 YAML"""
    print_section("示例 3: 保存 YAML")
    
    # 创建测试数据
    config = {
        'application': {
            'name': 'MyApp',
            'version': '2.0.0',
            'environment': 'production'
        },
        'server': {
            'host': '0.0.0.0',
            'port': 8080,
            'workers': 4
        },
        'logging': {
            'level': 'INFO',
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        },
        'features': ['auth', 'api', 'cache', 'metrics']
    }
    
    # 转储为字符串
    yaml_str = dump_yaml_string(config)
    print("YAML 字符串输出:")
    print(yaml_str)
    
    # 保存到文件
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
        temp_file = f.name
    
    dump_yaml_file(config, temp_file)
    print(f"\n已保存到文件：{temp_file}")
    
    # 验证保存的内容
    loaded = load_yaml_file(temp_file)
    print(f"验证加载：{loaded['application']['name']} v{loaded['application']['version']}")
    
    # 清理
    os.unlink(temp_file)


def example_04_validation():
    """示例 4: YAML 验证"""
    print_section("示例 4: YAML 验证")
    
    # 创建测试文件
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
        f.write("""
name: 测试应用
version: 1.0
port: 8080
debug: false
""")
        temp_file = f.name
    
    # 基本验证
    valid = is_valid_yaml(temp_file)
    print(f"YAML 是否有效：{valid}")
    
    # 带模式验证
    schema = {
        'name': str,
        'version': float,
        'port': int,
        'debug': bool,
        'optional_field': None  # None 表示可选
    }
    
    is_valid, errors = validate_yaml(temp_file, schema)
    print(f"模式验证：{'通过' if is_valid else '失败'}")
    if errors:
        print(f"错误：{errors}")
    
    # 清理
    os.unlink(temp_file)


def example_05_conversion():
    """示例 5: 格式转换"""
    print_section("示例 5: 格式转换")
    
    # 创建 YAML 文件
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
        f.write("""
application:
  name: Converter
  version: 1.0
settings:
  timeout: 30
  retry: 3
""")
        yaml_file = f.name
    
    # YAML 转 JSON
    json_str = yaml_to_json(yaml_file)
    print("YAML 转 JSON:")
    print(json_str)
    
    # JSON 转 YAML
    json_str = '{"service": "API", "port": 3000, "enabled": true}'
    yaml_result = json_to_yaml(json_str)
    print("\nJSON 转 YAML:")
    print(yaml_result)
    
    # 清理
    os.unlink(yaml_file)


def example_06_merge():
    """示例 6: 合并 YAML"""
    print_section("示例 6: 合并 YAML")
    
    # 创建基础配置
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
        f.write("""
database:
  host: localhost
  port: 5432
  name: dev_db
logging:
  level: DEBUG
cache:
  enabled: true
""")
        base_file = f.name
    
    # 创建生产覆盖配置
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
        f.write("""
database:
  host: prod-db.example.com
  name: prod_db
  password: secret123
logging:
  level: WARNING
metrics:
  enabled: true
""")
        override_file = f.name
    
    # 深度合并
    merged = merge_yaml([base_file, override_file], deep=True)
    
    print("合并后的配置:")
    print(dump_yaml_string(merged))
    
    print("\n说明:")
    print(f"- database.host 被覆盖：{merged['database']['host']}")
    print(f"- database.port 保留：{merged['database']['port']}")
    print(f"- database.password 新增：{merged['database'].get('password', 'N/A')}")
    print(f"- cache 保留：{merged.get('cache', 'N/A')}")
    print(f"- metrics 新增：{merged.get('metrics', 'N/A')}")
    
    # 清理
    os.unlink(base_file)
    os.unlink(override_file)


def example_07_diff():
    """示例 7: 差分比较"""
    print_section("示例 7: 差分比较")
    
    # 创建原始配置
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
        f.write("""
version: 1.0
name: MyApp
port: 8080
debug: true
features:
  - auth
  - api
""")
        original_file = f.name
    
    # 创建修改后配置
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
        f.write("""
version: 2.0
name: MyApp Pro
port: 8080
debug: false
features:
  - auth
  - api
  - metrics
""")
        modified_file = f.name
    
    # 比较差异
    diff = diff_yaml(original_file, modified_file)
    
    print("配置变更分析:")
    
    if diff['added']:
        print(f"\n➕ 新增字段:")
        for key, value in diff['added'].items():
            print(f"   {key}: {value}")
    
    if diff['removed']:
        print(f"\n➖ 移除字段:")
        for key, value in diff['removed'].items():
            print(f"   {key}: {value}")
    
    if diff['modified']:
        print(f"\n🔄 修改字段:")
        for key, change in diff['modified'].items():
            print(f"   {key}: {change['old']} → {change['new']}")
    
    # 清理
    os.unlink(original_file)
    os.unlink(modified_file)


def example_08_convenience():
    """示例 8: 便捷功能"""
    print_section("示例 8: 便捷功能")
    
    # 创建配置文件
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
        f.write("""
database:
  connection:
    host: db.example.com
    port: 5432
    credentials:
      username: admin
      password: secret
  pool:
    min_size: 5
    max_size: 20
app:
  name: ConfigApp
  version: 1.0
""")
        config_file = f.name
    
    # 获取嵌套值
    host = get_yaml_value(config_file, 'database.connection.host')
    print(f"数据库主机：{host}")
    
    username = get_yaml_value(config_file, 'database.connection.credentials.username')
    print(f"数据库用户：{username}")
    
    # 获取不存在的值（带默认值）
    timeout = get_yaml_value(config_file, 'database.timeout', 30)
    print(f"超时设置（默认）: {timeout}")
    
    # 设置值
    set_yaml_value(config_file, 'app.version', '2.0')
    new_version = get_yaml_value(config_file, 'app.version')
    print(f"\n更新后版本：{new_version}")
    
    # 删除敏感值
    delete_yaml_key(config_file, 'database.connection.credentials.password')
    password = get_yaml_value(config_file, 'database.connection.credentials.password', '已删除')
    print(f"密码状态：{password}")
    
    # 清理
    os.unlink(config_file)


def example_09_security():
    """示例 9: 安全功能"""
    print_section("示例 9: 安全功能")
    
    # 安全 YAML
    safe_yaml = """
config:
  name: 安全配置
  value: 123
"""
    
    # 不安全 YAML（包含 Python 标签）
    unsafe_yaml = """
!!python/object/apply:os.system
args: ['rm -rf /']
"""
    
    print(f"安全 YAML 检测：{contains_unsafe_tags(safe_yaml)}")
    print(f"不安全 YAML 检测：{contains_unsafe_tags(unsafe_yaml)}")
    
    # 使用安全加载
    print("\n使用 safe_load_yaml 加载（防止代码执行）:")
    try:
        data = safe_load_yaml(safe_yaml)
        print(f"安全加载成功：{data}")
    except Exception as e:
        print(f"加载失败：{e}")


def example_10_file_info():
    """示例 10: 文件信息"""
    print_section("示例 10: 文件信息")
    
    # 创建测试文件
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
        f.write("""
project:
  name: InfoTest
  version: 1.0
  team:
    - Alice
    - Bob
    - Charlie
""")
        test_file = f.name
    
    # 获取文件信息
    info = get_yaml_info(test_file)
    
    print("YAML 文件信息:")
    print(f"  路径：{info['path']}")
    print(f"  存在：{info['exists']}")
    print(f"  大小：{info['size']} 字节")
    print(f"  有效：{info['valid']}")
    print(f"  类型：{info['type']}")
    print(f"  顶层键：{info['keys']}")
    
    # 清理
    os.unlink(test_file)


def example_11_real_world():
    """示例 11: 实际应用场景"""
    print_section("示例 11: 实际应用场景 - 配置文件管理")
    
    # 场景：管理应用的开发/测试/生产配置
    
    # 基础配置
    base_config = {
        'app': {
            'name': 'MyApplication',
            'version': '1.0.0'
        },
        'database': {
            'driver': 'postgresql',
            'pool_size': 10
        },
        'logging': {
            'format': '%(asctime)s - %(levelname)s - %(message)s'
        }
    }
    
    # 环境特定配置
    dev_config = {
        'database': {
            'host': 'localhost',
            'port': 5432,
            'name': 'dev_db'
        },
        'logging': {
            'level': 'DEBUG'
        },
        'debug': True
    }
    
    prod_config = {
        'database': {
            'host': 'prod-db.example.com',
            'port': 5432,
            'name': 'prod_db',
            'ssl': True
        },
        'logging': {
            'level': 'WARNING'
        },
        'debug': False,
        'cache': {
            'enabled': True,
            'ttl': 3600
        }
    }
    
    # 创建临时文件
    with tempfile.TemporaryDirectory() as tmpdir:
        base_file = os.path.join(tmpdir, 'base.yaml')
        dev_file = os.path.join(tmpdir, 'dev.yaml')
        prod_file = os.path.join(tmpdir, 'prod.yaml')
        
        dump_yaml_file(base_config, base_file)
        dump_yaml_file(dev_config, dev_file)
        dump_yaml_file(prod_config, prod_file)
        
        # 生成开发环境配置
        dev_merged = merge_yaml([base_file, dev_file])
        print("开发环境配置:")
        print(dump_yaml_string(dev_merged))
        
        # 生成生产环境配置
        prod_merged = merge_yaml([base_file, prod_file])
        print("\n生产环境配置:")
        print(dump_yaml_string(prod_merged))
        
        # 比较环境差异
        print("\n环境差异分析:")
        diff = diff_yaml(dev_file, prod_file)
        
        if diff['modified']:
            print(f"修改的配置项：{list(diff['modified'].keys())}")
        if diff['added']:
            print(f"生产环境独有：{list(diff['added'].keys())}")


def main():
    """运行所有示例。"""
    print("\n" + "🎉" * 30)
    print("  AllToolkit YAML Utilities - 使用示例")
    print("🎉" * 30)
    
    # 运行所有示例
    example_01_basic_info()
    example_02_load_yaml()
    example_03_save_yaml()
    example_04_validation()
    example_05_conversion()
    example_06_merge()
    example_07_diff()
    example_08_convenience()
    example_09_security()
    example_10_file_info()
    example_11_real_world()
    
    print("\n" + "=" * 60)
    print("  ✅ 所有示例运行完成！")
    print("=" * 60 + "\n")


if __name__ == '__main__':
    main()
