#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit Environment Utilities - 验证与快照示例

演示环境变量验证和快照功能。
"""

import sys
import os
import json

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from mod import *


def main():
    print("="*60)
    print("  AllToolkit Environment Utilities - 验证与快照示例")
    print("="*60)
    
    # 1. 环境变量验证
    print("\n1️⃣  环境变量验证")
    print("-"*40)
    
    # 设置测试变量
    os.environ['APP_PORT'] = '8080'
    os.environ['APP_ENV'] = 'production'
    os.environ['APP_NAME'] = 'MyApp'
    os.environ['ADMIN_EMAIL'] = 'admin@example.com'
    
    # 验证端口范围
    print("   验证端口范围 (1024-65535):")
    result = validate_env('APP_PORT', [
        {'rule': 'required'},
        {'rule': 'min_value', 'value': 1024},
        {'rule': 'max_value', 'value': 65535}
    ])
    print(f"   端口 8080: {'✓ 有效' if result.valid else '✗ 无效'}")
    
    os.environ['APP_PORT'] = '80'
    result = validate_env('APP_PORT', [
        {'rule': 'min_value', 'value': 1024}
    ])
    print(f"   端口 80: {'✓ 有效' if result.valid else '✗ 无效'}")
    if not result.valid:
        print(f"   错误：{result.errors[0]}")
    
    # 验证邮箱格式
    print("\n   验证邮箱格式:")
    result = validate_env('ADMIN_EMAIL', [
        {'rule': 'pattern', 'value': r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'}
    ])
    print(f"   admin@example.com: {'✓ 有效' if result.valid else '✗ 无效'}")
    
    # 验证选项
    print("\n   验证环境选项:")
    result = validate_env('APP_ENV', [
        {'rule': 'choices', 'value': ['development', 'staging', 'production']}
    ])
    print(f"   production: {'✓ 有效' if result.valid else '✗ 无效'}")
    
    os.environ['APP_ENV'] = 'invalid'
    result = validate_env('APP_ENV', [
        {'rule': 'choices', 'value': ['development', 'staging', 'production']}
    ])
    print(f"   invalid: {'✓ 有效' if result.valid else '✗ 无效'}")
    
    # Schema 验证
    print("\n   Schema 验证（多个变量）:")
    os.environ['APP_PORT'] = '8080'
    os.environ['APP_ENV'] = 'production'
    
    schema = {
        'APP_NAME': {
            'rules': [
                {'rule': 'required'},
                {'rule': 'min_length', 'value': 3},
                {'rule': 'max_length', 'value': 50}
            ]
        },
        'APP_PORT': {
            'rules': [
                {'rule': 'required'},
                {'rule': 'min_value', 'value': 1024},
                {'rule': 'max_value', 'value': 65535}
            ]
        },
        'APP_ENV': {
            'rules': [
                {'rule': 'required'},
                {'rule': 'choices', 'value': ['development', 'staging', 'production']}
            ]
        },
        'ADMIN_EMAIL': {
            'rules': [
                {'rule': 'pattern', 'value': r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'}
            ]
        }
    }
    
    result = validate_env_schema(schema)
    if result.valid:
        print("   ✓ 所有变量验证通过！")
    else:
        print(f"   ✗ 验证失败：{result.errors}")
    
    # 2. 快照功能
    print("\n2️⃣  快照功能")
    print("-"*40)
    
    # 捕获初始快照
    print("   捕获初始快照...")
    before = capture_snapshot('初始状态')
    print(f"   快照时间：{before.timestamp}")
    print(f"   变量数量：{before.variable_count}")
    
    # 修改环境变量
    print("\n   修改环境变量...")
    set_env('SNAPSHOT_VAR1', 'value1')
    set_env('SNAPSHOT_VAR2', 'value2')
    set_env('SNAPSHOT_VAR3', 'original')
    
    # 捕获修改后快照
    after_add = capture_snapshot('添加变量后')
    print(f"   新增变量数：{after_add.variable_count - before.variable_count}")
    
    # 修改一个变量
    os.environ['SNAPSHOT_VAR3'] = 'modified'
    after_modify = capture_snapshot('修改变量后')
    
    # 比较快照
    print("\n   比较快照差异...")
    diff = diff_snapshots(after_add, after_modify)
    print(f"   新增：{diff['summary']['added_count']}")
    print(f"   删除：{diff['summary']['removed_count']}")
    print(f"   修改：{diff['summary']['changed_count']}")
    
    if diff['changed']:
        for key, change in diff['changed'].items():
            print(f"     {key}: {change['old']} → {change['new']}")
    
    # 保存快照到文件
    print("\n   保存快照到文件...")
    snapshot_file = '/tmp/env_snapshot_demo.json'
    saved = save_snapshot(before, snapshot_file)
    print(f"   保存结果：{'✓ 成功' if saved else '✗ 失败'}")
    
    # 加载快照
    print("\n   从文件加载快照...")
    loaded = load_snapshot(snapshot_file)
    if loaded:
        print(f"   加载成功！")
        print(f"   快照描述：{loaded.description}")
        print(f"   变量数量：{loaded.variable_count}")
    
    # 恢复快照
    print("\n   恢复快照...")
    os.environ['SNAPSHOT_VAR3'] = 'changed_again'
    print(f"   恢复前 SNAPSHOT_VAR3 = {os.environ.get('SNAPSHOT_VAR3')}")
    
    # 创建只包含测试变量的快照用于恢复
    test_snapshot = EnvSnapshot(
        timestamp=datetime.now().isoformat(),
        variables={
            'SNAPSHOT_VAR1': 'restored1',
            'SNAPSHOT_VAR2': 'restored2',
            'SNAPSHOT_VAR3': 'restored3'
        },
        source='test',
        description='恢复测试'
    )
    restore_snapshot(test_snapshot)
    print(f"   恢复后 SNAPSHOT_VAR3 = {os.environ.get('SNAPSHOT_VAR3')}")
    
    # 3. 敏感信息处理
    print("\n3️⃣  敏感信息处理")
    print("-"*40)
    
    test_vars = {
        'DATABASE_PASSWORD': 'super-secret-123',
        'API_KEY': 'sk-abcdefghij123456',
        'AWS_SECRET_KEY': 'wJalrXUtnFEMI/K7MDENG/bPxRfiCY',
        'APP_NAME': 'MyApplication',
        'DEBUG': 'true',
        'SHORT_PWD': 'abc'
    }
    
    print("   原始变量：")
    for key, value in test_vars.items():
        print(f"     {key}={value}")
    
    masked = mask_sensitive_vars(test_vars)
    print("\n   脱敏后：")
    for key, value in masked.items():
        print(f"     {key}={value}")
    
    # 4. require_envs 便捷函数
    print("\n4️⃣  便捷函数演示")
    print("-"*40)
    
    os.environ['DB_HOST'] = 'localhost'
    os.environ['DB_PORT'] = '5432'
    os.environ['DB_NAME'] = 'mydb'
    
    try:
        db_config = require_envs('DB_HOST', 'DB_PORT', 'DB_NAME')
        print("   ✓ 成功获取所有必需变量：")
        for key, value in db_config.items():
            print(f"     {key}={value}")
    except EnvironmentError as e:
        print(f"   ✗ 错误：{e}")
    
    # 尝试获取不存在的变量
    try:
        require_envs('DB_HOST', 'NONEXISTENT_VAR')
    except EnvironmentError as e:
        print(f"\n   捕获异常：{e}")
    
    # 清理
    cleanup_vars = [
        'APP_PORT', 'APP_ENV', 'APP_NAME', 'ADMIN_EMAIL',
        'SNAPSHOT_VAR1', 'SNAPSHOT_VAR2', 'SNAPSHOT_VAR3',
        'DB_HOST', 'DB_PORT', 'DB_NAME'
    ]
    for var in cleanup_vars:
        delete_env(var)
    
    try:
        os.unlink(snapshot_file)
    except:
        pass
    
    print("\n" + "="*60)
    print("  示例执行完成！")
    print("="*60)


if __name__ == '__main__':
    main()
