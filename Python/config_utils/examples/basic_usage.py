#!/usr/bin/env python3
"""
AllToolkit - Configuration Utilities Basic Usage Examples

演示 config_utils 模块的基本用法。
"""

import sys
import os

# 添加模块路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import Config, create_schema, load_config, parse_config, ConfigFormat


def example_basic_config():
    """基本配置操作示例。"""
    print("=" * 60)
    print("示例 1: 基本配置操作")
    print("=" * 60)
    
    # 创建配置
    config = Config({
        'host': 'localhost',
        'port': 8080,
        'debug': True,
        'name': 'MyApplication',
    })
    
    # 获取值
    print(f"host: {config.get('host')}")
    print(f"port: {config.get('port')}")
    print(f"debug: {config.get('debug')}")
    print(f"name: {config.get('name')}")
    
    # 获取不存在的键（带默认值）
    print(f"missing (default): {config.get('missing', 'default_value')}")
    
    # 使用便捷访问
    print(f"config['host']: {config['host']}")
    print(f"'host' in config: {'host' in config}")
    print(f"len(config): {len(config)}")
    
    print()


def example_nested_config():
    """嵌套配置示例。"""
    print("=" * 60)
    print("示例 2: 嵌套配置")
    print("=" * 60)
    
    config = Config({
        'server': {
            'host': '0.0.0.0',
            'port': 8080,
        },
        'database': {
            'host': 'localhost',
            'port': 5432,
            'name': 'mydb',
            'credentials': {
                'user': 'admin',
                'password': 'secret',
            }
        },
        'features': ['auth', 'logging', 'cache'],
    })
    
    # 点号访问嵌套值
    print(f"server.host: {config.get('server.host')}")
    print(f"server.port: {config.get('server.port')}")
    print(f"database.host: {config.get('database.host')}")
    print(f"database.credentials.user: {config.get('database.credentials.user')}")
    print(f"features: {config.get('features')}")
    
    # 设置嵌套值
    config.set('database.credentials.password', 'new_secret')
    print(f"新密码：{config.get('database.credentials.password')}")
    
    print()


def example_typed_getters():
    """类型化获取器示例。"""
    print("=" * 60)
    print("示例 3: 类型化获取器")
    print("=" * 60)
    
    # 配置值都是字符串（常见于从文件加载）
    config = Config({
        'count': '42',
        'ratio': '3.14159',
        'enabled': 'true',
        'disabled': 'false',
        'tags': 'python,web,api,fast',
        'metadata': '{"version": "1.0", "author": "test"}',
    })
    
    # 自动类型转换
    print(f"count (int): {config.get_int('count')} (type: {type(config.get_int('count')).__name__})")
    print(f"ratio (float): {config.get_float('ratio')} (type: {type(config.get_float('ratio')).__name__})")
    print(f"enabled (bool): {config.get_bool('enabled')} (type: {type(config.get_bool('enabled')).__name__})")
    print(f"disabled (bool): {config.get_bool('disabled')}")
    print(f"tags (list): {config.get_list('tags')}")
    print(f"metadata (dict): {config.get_dict('metadata')}")
    
    print()


def example_env_substitution():
    """环境变量替换示例。"""
    print("=" * 60)
    print("示例 4: 环境变量替换")
    print("=" * 60)
    
    # 设置测试环境变量
    os.environ['APP_HOST'] = 'api.example.com'
    os.environ['APP_PORT'] = '3000'
    os.environ['DB_PASSWORD'] = 'super_secret'
    
    config = Config({
        # 基本替换
        'host': '${APP_HOST}',
        'port': '$APP_PORT',
        
        # 带默认值
        'timeout': '${TIMEOUT:-30}',
        'missing': '${NONEXISTENT:-fallback_value}',
        
        # 组合使用
        'api_url': 'https://${APP_HOST}:${APP_PORT}/api',
        'db_password': '${DB_PASSWORD}',
    }, env_substitute=True)
    
    print(f"host: {config.get('host')}")
    print(f"port: {config.get('port')}")
    print(f"timeout: {config.get('timeout')}")
    print(f"missing: {config.get('missing')}")
    print(f"api_url: {config.get('api_url')}")
    print(f"db_password: {'*' * len(config.get('db_password'))}")
    
    # 清理环境变量
    del os.environ['APP_HOST']
    del os.environ['APP_PORT']
    del os.environ['DB_PASSWORD']
    
    print()


def example_schema_validation():
    """Schema 验证示例。"""
    print("=" * 60)
    print("示例 5: Schema 验证")
    print("=" * 60)
    
    # 定义 Schema
    schema = create_schema(
        host=dict(type=str, required=True, description="服务器地址"),
        port=dict(type=int, required=True, min=1, max=65535, description="端口号"),
        debug=dict(type=bool, default=False, description="调试模式"),
        log_level=dict(
            type=str, 
            choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
            default='INFO',
            description="日志级别"
        ),
        email=dict(
            type=str,
            pattern=r'^[\w.-]+@[\w.-]+\.\w+$',
            description="联系邮箱"
        ),
    )
    
    # 有效配置
    print("验证有效配置...")
    valid_config = Config({
        'host': 'localhost',
        'port': 8080,
        'debug': True,
        'log_level': 'DEBUG',
        'email': 'test@example.com',
    }, schema)
    
    is_valid, errors = valid_config.validate()
    print(f"  有效：{is_valid}")
    if errors:
        for error in errors:
            print(f"  错误：{error}")
    
    # 无效配置 - 缺少必填字段
    print("\n验证无效配置（缺少必填字段）...")
    invalid_config = Config({
        'host': 'localhost',
        # 缺少 port
    }, schema)
    
    is_valid, errors = invalid_config.validate()
    print(f"  有效：{is_valid}")
    for error in errors:
        print(f"  错误：{error}")
    
    # 无效配置 - 超出范围
    print("\n验证无效配置（端口超出范围）...")
    invalid_config2 = Config({
        'host': 'localhost',
        'port': 100000,  # 超出 65535
    }, schema)
    
    is_valid, errors = invalid_config2.validate()
    print(f"  有效：{is_valid}")
    for error in errors:
        print(f"  错误：{error}")
    
    # 无效配置 - 不在选项中
    print("\n验证无效配置（日志级别无效）...")
    invalid_config3 = Config({
        'host': 'localhost',
        'port': 8080,
        'log_level': 'INVALID',
    }, schema)
    
    is_valid, errors = invalid_config3.validate()
    print(f"  有效：{is_valid}")
    for error in errors:
        print(f"  错误：{error}")
    
    print()


def example_parse_formats():
    """解析不同格式示例。"""
    print("=" * 60)
    print("示例 6: 解析不同格式")
    print("=" * 60)
    
    from mod import ConfigParser, ConfigFormat
    
    parser = ConfigParser()
    
    # Key-Value 格式
    kv_content = """
    # 配置文件
    host=localhost
    port=8080
    debug=true
    name="My Application"
    """
    kv_config = parser.parse_key_value(kv_content)
    print("Key-Value 格式:")
    print(f"  {kv_config}")
    
    # JSON 格式
    json_content = """
    {
        "host": "localhost",
        "port": 8080,
        "debug": true,
        "features": ["auth", "logging"]
    }
    """
    json_config = parser.parse_json(json_content)
    print("\nJSON 格式:")
    print(f"  {json_config}")
    
    # INI 格式
    ini_content = """
    [server]
    host=0.0.0.0
    port=8080
    
    [database]
    host=localhost
    port=5432
    name=mydb
    """
    ini_config = parser.parse_ini(ini_content)
    print("\nINI 格式:")
    for section, values in ini_config.items():
        print(f"  [{section}]")
        for key, value in values.items():
            print(f"    {key}={value}")
    
    print()


def example_immutable_config():
    """不可变配置示例。"""
    print("=" * 60)
    print("示例 7: 不可变配置")
    print("=" * 60)
    
    from mod import ConfigError
    
    # 创建可配置
    config = Config({'host': 'localhost', 'port': 8080})
    print(f"初始配置：{config.to_dict()}")
    
    # 修改配置
    config.set('debug', True)
    print(f"修改后：{config.to_dict()}")
    
    # 设为不可变
    config.freeze()
    print("配置已冻结")
    
    # 尝试修改（会抛出异常）
    try:
        config.set('port', 9090)
    except ConfigError as e:
        print(f"修改失败：{e}")
    
    print()


def example_prebuilt_schemas():
    """预定义 Schema 示例。"""
    print("=" * 60)
    print("示例 8: 预定义 Schema")
    print("=" * 60)
    
    from mod import DATABASE_SCHEMA, SERVER_SCHEMA, LOGGING_SCHEMA
    
    # 数据库配置
    print("数据库配置 Schema:")
    db_config = Config({
        'host': 'localhost',
        'port': 5432,
        'name': 'mydb',
        'user': 'admin',
        'password': 'secret',
        'ssl': True,
    }, DATABASE_SCHEMA)
    is_valid, errors = db_config.validate()
    print(f"  验证：{'通过' if is_valid else '失败'}")
    
    # 服务器配置
    print("\n服务器配置 Schema:")
    server_config = Config({
        'host': '0.0.0.0',
        'port': 8080,
        'debug': False,
        'workers': 4,
    }, SERVER_SCHEMA)
    is_valid, errors = server_config.validate()
    print(f"  验证：{'通过' if is_valid else '失败'}")
    
    # 日志配置
    print("\n日志配置 Schema:")
    log_config = Config({
        'level': 'INFO',
        'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        'max_size': 10485760,
        'backup_count': 5,
    }, LOGGING_SCHEMA)
    is_valid, errors = log_config.validate()
    print(f"  验证：{'通过' if is_valid else '失败'}")
    
    print()


def main():
    """运行所有示例。"""
    print("\n" + "=" * 60)
    print("AllToolkit Configuration Utilities - 使用示例")
    print("=" * 60 + "\n")
    
    example_basic_config()
    example_nested_config()
    example_typed_getters()
    example_env_substitution()
    example_schema_validation()
    example_parse_formats()
    example_immutable_config()
    example_prebuilt_schemas()
    
    print("=" * 60)
    print("所有示例运行完成！")
    print("=" * 60)


if __name__ == '__main__':
    main()
