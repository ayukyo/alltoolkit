#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Hash Utils - File Integrity Check Example

演示如何使用哈希校验文件完整性。
"""

import sys
import os
import tempfile
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import hash_file, verify_file_hash, hash_directory


def main():
    print("="*60)
    print("Hash Utils - File Integrity Check Example")
    print("="*60)
    print()
    
    # 创建临时目录和文件用于演示
    temp_dir = tempfile.mkdtemp()
    print(f"临时目录：{temp_dir}")
    print()
    
    try:
        # 1. 创建示例文件
        print("1. 创建示例文件")
        print("-"*60)
        files = {
            "document.txt": "This is an important document.",
            "config.json": '{"name": "test", "version": "1.0"}',
            "data.csv": "id,name,value\n1,Alice,100\n2,Bob,200",
        }
        
        for filename, content in files.items():
            filepath = Path(temp_dir) / filename
            filepath.write_text(content)
            print(f"  ✓ 创建：{filename} ({len(content)} 字节)")
        print()
        
        # 2. 计算文件哈希
        print("2. 计算文件哈希值")
        print("-"*60)
        hashes = {}
        for filename in files.keys():
            filepath = Path(temp_dir) / filename
            file_hash = hash_file(filepath)
            hashes[filename] = file_hash
            print(f"  {filename}:")
            print(f"    SHA256: {file_hash}")
        print()
        
        # 3. 验证文件完整性
        print("3. 验证文件完整性")
        print("-"*60)
        for filename, expected_hash in hashes.items():
            filepath = Path(temp_dir) / filename
            is_valid = verify_file_hash(filepath, expected_hash)
            status = "✓ 完整" if is_valid else "✗ 损坏"
            print(f"  {filename}: {status}")
        print()
        
        # 4. 模拟文件篡改
        print("4. 模拟文件篡改检测")
        print("-"*60)
        tampered_file = Path(temp_dir) / "document.txt"
        original_content = tampered_file.read_text()
        tampered_file.write_text(original_content + "\n[TAMPERED]")
        
        is_valid = verify_file_hash(tampered_file, hashes["document.txt"])
        status = "✓ 完整" if is_valid else "✗ 检测到篡改！"
        print(f"  document.txt: {status}")
        
        # 恢复文件
        tampered_file.write_text(original_content)
        print()
        
        # 5. 目录批量哈希
        print("5. 目录批量哈希")
        print("-"*60)
        dir_hashes = hash_directory(temp_dir)
        print(f"  目录：{temp_dir}")
        print(f"  文件数量：{len(dir_hashes)}")
        print()
        for rel_path, file_hash in sorted(dir_hashes.items()):
            print(f"  {rel_path}:")
            print(f"    {file_hash[:48]}...")
        print()
        
        # 6. 使用不同算法
        print("6. 使用不同哈希算法")
        print("-"*60)
        test_file = Path(temp_dir) / "document.txt"
        algorithms = ['md5', 'sha1', 'sha256', 'sha512']
        
        for algo in algorithms:
            h = hash_file(test_file, algorithm=algo)
            print(f"  {algo.upper():8}: {h[:48]}...")
        print()
        
        # 7. 哈希对比
        print("7. 文件哈希对比")
        print("-"*60)
        hash1 = hash_file(Path(temp_dir) / "document.txt")
        hash2 = hash_file(Path(temp_dir) / "config.json")
        
        print(f"  document.txt: {hash1[:32]}...")
        print(f"  config.json:  {hash2[:32]}...")
        print(f"  哈希不同：{hash1 != hash2}")
        print()
        
    finally:
        # 清理临时文件
        import shutil
        shutil.rmtree(temp_dir)
        print("="*60)
        print("示例完成！临时文件已清理。")
        print("="*60)


if __name__ == "__main__":
    main()
