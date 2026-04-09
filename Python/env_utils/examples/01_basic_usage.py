#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit Environment Utilities - 基础使用示例

演示环境变量的基本读写操作。
"""

import sys
import os

# 导入模块
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from mod import *


def main():
    print("="*60)
    print("  AllToolkit Environment Utilities - 基础使用示例")
    print("="*60)
    
    # 1. 获取环境变量
    print("\n1️⃣  获取环境变量")
    print("-"*40)
    
    home = get_env('HOME', default='/unknown')
    print(f"   HOME = {home}")
    
    user = get_env('USER', default='anonymous')
    print(f"   USER = {user}")
    
    # 带默认值
    custom_var = get_env('MY_CUSTOM_VAR', default='default_value')
    print(f"   MY_CUSTOM_VAR = {custom_var} (使用默认值)")
    
    # 2. 设置环境变量
    print("\n2️⃣  设置环境变量")
    print("-"*40)
    
    set_env('APP_NAME', 'MyAwesomeApp')
    set_env('APP_VERSION', '1.0.0')
    print(f"   已设置 APP_NAME = {get_env('APP_NAME')}")
    print(f"   已设置 APP_VERSION = {get_env('APP_VERSION')}")
    
    # 3. 检查变量是否存在
    print("\n3️⃣  检查变量是否存在")
    print("-"*40)
    
    if has_env('HOME'):
        print("   ✓ HOME 环境变量存在")
    
    if not has_env('NONEXISTENT_VAR'):
        print("   ✗ NONEXISTENT_VAR 不存在")
    
    # 4. 删除环境变量
    print("\n4️⃣  删除环境变量")
    print("-"*40)
    
    set_env('TEMP_VAR', 'temporary')
    print(f"   设置 TEMP_VAR = {get_env('TEMP_VAR')}")
    
    delete_env('TEMP_VAR')
    print(f"   删除后是否存在：{has_env('TEMP_VAR')}")
    
    # 5. 获取所有环境变量
    print("\n5️⃣  获取所有环境变量")
    print("-"*40)
    
    all_env = get_all_env()
    print(f"   当前共有 {len(all_env)} 个环境变量")
    print(f"   前 5 个：")
    for i, (key, value) in enumerate(sorted(all_env.items())[:5]):
        print(f"     {key}={value[:50]}{'...' if len(value) > 50 else ''}")
    
    # 6. 类型转换
    print("\n6️⃣  类型转换")
    print("-"*40)
    
    os.environ['PORT'] = '8080'
    os.environ['DEBUG'] = 'true'
    os.environ['RATE'] = '3.14159'
    os.environ['TAGS'] = 'web,api,backend'
    os.environ['CONFIG'] = '{"host": "localhost", "port": 5432}'
    
    port = get_env_as('PORT', VarType.INTEGER)
    print(f"   PORT (int): {port} (类型：{type(port).__name__})")
    
    debug = get_env_as('DEBUG', VarType.BOOLEAN)
    print(f"   DEBUG (bool): {debug}")
    
    rate = get_env_as('RATE', VarType.FLOAT)
    print(f"   RATE (float): {rate}")
    
    tags = get_env_as('TAGS', VarType.LIST)
    print(f"   TAGS (list): {tags}")
    
    config = get_env_as('CONFIG', VarType.JSON)
    print(f"   CONFIG (json): {config}")
    
    # 7. 环境检查
    print("\n7️⃣  环境检查")
    print("-"*40)
    
    os.environ['ENV'] = 'production'
    print(f"   当前环境：{get_env('ENV')}")
    print(f"   是生产环境吗？{is_production()}")
    print(f"   是开发环境吗？{is_development()}")
    print(f"   是测试环境吗？{is_testing()}")
    
    # 8. 获取应用信息
    print("\n8️⃣  获取应用信息")
    print("-"*40)
    
    os.environ['APP_NAME'] = 'DemoApp'
    os.environ['APP_VERSION'] = '2.0.0'
    os.environ['PORT'] = '3000'
    
    info = get_app_info()
    for key, value in info.items():
        print(f"   {key}: {value}")
    
    # 清理
    cleanup_vars = ['APP_NAME', 'APP_VERSION', 'PORT', 'DEBUG', 'RATE', 'TAGS', 'CONFIG', 'ENV']
    for var in cleanup_vars:
        delete_env(var)
    
    print("\n" + "="*60)
    print("  示例执行完成！")
    print("="*60)


if __name__ == '__main__':
    main()
