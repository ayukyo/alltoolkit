#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - INI Config Utilities Example
INI配置文件工具模块使用示例

本示例展示如何使用ini_config_utils模块进行INI配置文件的
读取、写入、修改和验证等操作。
"""

import sys
import os

# 添加模块路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'ini_config_utils'))

from mod import (
    IniConfig, IniSection, IniConfigError,
    SectionNotFoundError, KeyNotFoundError,
    read_ini, write_ini, parse_ini, create_ini
)


def example_1_basic_usage():
    """示例1: 基本用法 - 创建和读取配置"""
    print("=" * 60)
    print("示例1: 基本用法 - 创建和读取配置")
    print("=" * 60)
    
    config = IniConfig()
    
    # 设置配置值
    config.set('database', 'host', 'localhost')
    config.set('database', 'port', 3306)
    config.set('database', 'username', 'admin')
    config.set('database', 'password', 'secret123')
    
    config.set('app', 'name', 'MyApplication')
    config.set('app', 'version', '1.0.0')
    config.set('app', 'debug', True)
    
    # 读取配置值
    print(f"数据库主机: {config.get('database', 'host')}")
    print(f"数据库端口: {config.get_int('database', 'port')}")
    print(f"应用名称: {config.get('app', 'name')}")
    print(f"调试模式: {config.get_bool('app', 'debug')}")
    
    print("\n生成的INI内容:")
    print("-" * 40)
    print(config.write_string())
    print()


def example_2_type_conversion():
    """示例2: 类型转换"""
    print("=" * 60)
    print("示例2: 类型转换")
    print("=" * 60)
    
    config = IniConfig()
    
    config.set('settings', 'timeout', 30)
    config.set('settings', 'pi', 3.14159)
    config.set('settings', 'enabled', True)
    config.set('settings', 'features', ['auth', 'cache', 'logging'])
    
    timeout = config.get_int('settings', 'timeout')
    pi = config.get_float('settings', 'pi')
    enabled = config.get_bool('settings', 'enabled')
    features = config.get_list('settings', 'features')
    
    print(f"超时时间 (int): {timeout}")
    print(f"圆周率 (float): {pi}")
    print(f"启用状态 (bool): {enabled}")
    print(f"功能列表 (list): {features}")
    print()


def example_3_parsing_and_writing():
    """示例3: 解析和写入文件"""
    print("=" * 60)
    print("示例3: 解析和写入文件")
    print("=" * 60)
    
    ini_content = """# 应用程序配置
[database]
host = localhost
port = 5432
name = mydb
ssl = true

[cache]
enabled = yes
ttl = 3600
servers = 192.168.1.1, 192.168.1.2

[logging]
level = info
file = /var/log/app.log
"""
    
    config = parse_ini(ini_content)
    
    print("解析后的配置:")
    print(f"数据库主机: {config.get('database', 'host')}")
    print(f"数据库端口: {config.get_int('database', 'port')}")
    print(f"数据库SSL: {config.get_bool('database', 'ssl')}")
    print(f"缓存服务器: {config.get_list('cache', 'servers')}")
    print()


def example_4_section_operations():
    """示例4: 节操作"""
    print("=" * 60)
    print("示例4: 节操作")
    print("=" * 60)
    
    config = IniConfig()
    
    db_section = config.add_section('database', '数据库配置')
    db_section.set('host', 'localhost')
    db_section.set('port', 3306)
    
    section = config.section('database')
    print(f"节 '{section.name}' 包含 {len(section)} 个键")
    print(f"'database' 节存在: {config.has_section('database')}")
    print(f"所有节: {config.sections()}")
    print()


def example_5_comments():
    """示例5: 注释"""
    print("=" * 60)
    print("示例5: 注释")
    print("=" * 60)
    
    config = IniConfig()
    config._global_comments = ['应用程序配置文件', '请勿手动修改']
    
    config.add_section('server', '服务器配置')
    config.set('server', 'host', '0.0.0.0', '监听地址')
    config.set('server', 'port', 8080, '监听端口')
    
    print("带注释的INI内容:")
    print("-" * 40)
    print(config.write_string())
    print()


def example_6_validation():
    """示例6: 配置验证"""
    print("=" * 60)
    print("示例6: 配置验证")
    print("=" * 60)
    
    config = IniConfig()
    config.set('database', 'host', 'localhost')
    config.set('database', 'port', 3306)
    config.set('app', 'name', 'MyApp')
    
    schema = {
        'database': ['host', 'port', 'username', 'password'],
        'app': ['name', 'debug'],
    }
    
    errors = config.validate(schema)
    
    if errors:
        print("配置验证失败:")
        for error in errors:
            print(f"  - {error}")
    else:
        print("配置验证通过!")
    print()


def example_7_merge():
    """示例7: 合并配置"""
    print("=" * 60)
    print("示例7: 合并配置")
    print("=" * 60)
    
    base_config = IniConfig()
    base_config.set('app', 'name', 'MyApp')
    base_config.set('app', 'debug', False)
    
    env_config = IniConfig()
    env_config.set('app', 'debug', True)
    env_config.set('cache', 'enabled', True)
    
    print("基础配置:")
    print(base_config.write_string())
    
    base_config.merge(env_config)
    print("合并后:")
    print(base_config.write_string())
    print()


def example_8_dict():
    """示例8: 字典转换"""
    print("=" * 60)
    print("示例8: 字典转换")
    print("=" * 60)
    
    data = {
        'database': {'host': 'localhost', 'port': '3306'},
        'cache': {'enabled': 'true', 'ttl': '3600'},
    }
    
    config = create_ini(data)
    print("从字典创建的配置:")
    print(config.write_string())
    
    dict_data = config.to_dict()
    print(f"转换回字典: {dict_data}")
    print()


def main():
    """运行所有示例"""
    examples = [
        example_1_basic_usage,
        example_2_type_conversion,
        example_3_parsing_and_writing,
        example_4_section_operations,
        example_5_comments,
        example_6_validation,
        example_7_merge,
        example_8_dict,
    ]
    
    for example in examples:
        try:
            example()
        except Exception as e:
            print(f"示例 {example.__name__} 出错: {e}")
            import traceback
            traceback.print_exc()
    
    print("=" * 60)
    print("所有示例运行完成!")
    print("=" * 60)


if __name__ == '__main__':
    main()
