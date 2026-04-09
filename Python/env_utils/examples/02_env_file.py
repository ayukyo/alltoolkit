#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit Environment Utilities - .env 文件操作示例

演示 .env 文件的解析、加载、保存和合并。
"""

import sys
import os
import tempfile

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from mod import *


def main():
    print("="*60)
    print("  AllToolkit Environment Utilities - .env 文件操作示例")
    print("="*60)
    
    # 创建示例 .env 文件
    with tempfile.NamedTemporaryFile(mode='w', suffix='.env', delete=False) as f:
        f.write("# 数据库配置\n")
        f.write("DATABASE_URL=postgres://localhost:5432/mydb\n")
        f.write("DATABASE_USER=admin\n")
        f.write('DATABASE_PASSWORD="super-secret-password"\n')
        f.write("\n")
        f.write("# 应用配置\n")
        f.write("APP_NAME=MyApplication\n")
        f.write("APP_VERSION=1.0.0\n")
        f.write("DEBUG=true\n")
        f.write("PORT=8080\n")
        f.write("\n")
        f.write("# API 配置\n")
        f.write("API_KEY=sk-abc123xyz789\n")
        f.write("API_SECRET=very-secret-key\n")
        base_env_file = f.name
    
    try:
        # 1. 解析 .env 文件
        print("\n1️⃣  解析 .env 文件")
        print("-"*40)
        
        env_vars = parse_env_file(base_env_file)
        print(f"   解析到 {len(env_vars)} 个变量：")
        for key, value in env_vars.items():
            print(f"     {key}={value}")
        
        # 2. 加载 .env 文件到环境变量
        print("\n2️⃣  加载 .env 文件到环境变量")
        print("-"*40)
        
        # 先清理可能存在的变量
        for key in env_vars.keys():
            delete_env(key)
        
        loaded = load_env_file(base_env_file)
        print(f"   加载了 {len(loaded)} 个变量")
        print(f"   DATABASE_URL = {get_env('DATABASE_URL')}")
        print(f"   APP_NAME = {get_env('APP_NAME')}")
        
        # 3. 保存环境变量到新文件
        print("\n3️⃣  保存环境变量到新文件")
        print("-"*40)
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.env', delete=False) as f:
            output_file = f.name
        
        # 只保存应用相关变量
        app_vars = {
            'APP_NAME': get_env('APP_NAME'),
            'APP_VERSION': get_env('APP_VERSION'),
            'DEBUG': get_env('DEBUG'),
            'PORT': get_env('PORT')
        }
        
        count = save_env_file(output_file, app_vars)
        print(f"   保存了 {count} 个变量到 {output_file}")
        
        # 读取并显示保存的内容
        print("\n   保存的文件内容：")
        with open(output_file, 'r') as f:
            for line in f:
                print(f"   {line.rstrip()}")
        
        # 4. 创建第二个 .env 文件用于合并
        print("\n4️⃣  合并多个 .env 文件")
        print("-"*40)
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.env', delete=False) as f:
            f.write("# 本地覆盖配置\n")
            f.write("DEBUG=false\n")  # 覆盖
            f.write("LOCAL_MODE=true\n")  # 新增
            f.write("CACHE_ENABLED=true\n")  # 新增
            local_env_file = f.name
        
        # 合并文件（后者覆盖前者）
        merged = merge_env_files([base_env_file, local_env_file])
        print(f"   合并后共有 {len(merged)} 个变量")
        print(f"   DEBUG = {merged.get('DEBUG')} (被覆盖)")
        print(f"   LOCAL_MODE = {merged.get('LOCAL_MODE')} (新增)")
        print(f"   DATABASE_URL = {merged.get('DATABASE_URL')} (保留)")
        
        # 5. 保存合并结果
        with tempfile.NamedTemporaryFile(mode='w', suffix='.env', delete=False) as f:
            merged_file = f.name
        
        save_env_file(merged_file, merged)
        print(f"\n   合并结果已保存到：{merged_file}")
        
        # 6. 演示带引号和特殊字符的值
        print("\n5️⃣  处理特殊字符")
        print("-"*40)
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.env', delete=False) as f:
            f.write('SIMPLE=value\n')
            f.write('WITH_SPACES=hello world\n')
            f.write('WITH_QUOTES="quoted value"\n')
            f.write("WITH_SINGLE_QUOTES='single quoted'\n")
            f.write('WITH_EQUALS=key=value=more\n')
            special_env_file = f.name
        
        special_vars = parse_env_file(special_env_file)
        print("   解析结果：")
        for key, value in special_vars.items():
            print(f"     {key} = '{value}'")
        
        # 清理
        os.unlink(base_env_file)
        os.unlink(output_file)
        os.unlink(local_env_file)
        os.unlink(merged_file)
        os.unlink(special_env_file)
        
        for key in list(env_vars.keys()) + ['LOCAL_MODE', 'CACHE_ENABLED']:
            delete_env(key)
        
        print("\n" + "="*60)
        print("  示例执行完成！")
        print("="*60)
    
    except Exception as e:
        print(f"\n   ❌ 错误：{e}")
        os.unlink(base_env_file)
        raise


if __name__ == '__main__':
    main()
