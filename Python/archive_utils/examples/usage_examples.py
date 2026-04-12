"""
AllToolkit - Archive Utils Usage Examples

演示 archive_utils 模块的各种使用场景。
"""

import os
import sys
import tempfile
import shutil

# 添加模块路径
script_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(script_dir)
sys.path.insert(0, parent_dir)

from mod import (
    ArchiveUtils,
    ArchiveFormat,
    CompressionLevel,
    ArchiveInfo,
    create_archive,
    extract_archive,
    list_archive,
    get_archive_info,
    verify_archive,
    calculate_checksum,
)


def example_basic_usage():
    """基础使用示例"""
    print("\n" + "=" * 60)
    print("示例 1: 基础使用")
    print("=" * 60)
    
    utils = ArchiveUtils()
    
    with tempfile.TemporaryDirectory() as tmpdir:
        # 创建测试文件
        test_file = os.path.join(tmpdir, "test.txt")
        with open(test_file, 'w') as f:
            f.write("Hello, Archive Utils!")
        
        # 创建 ZIP
        zip_path = os.path.join(tmpdir, "example.zip")
        result = utils.create_archive(zip_path, [test_file])
        print(f"✓ 创建归档：{result.success}")
        print(f"  处理文件：{result.files_processed}")
        
        # 列出内容
        members = utils.list_archive(zip_path)
        print(f"✓ 归档内容：{len(members)} 个成员")
        for m in members:
            print(f"  - {m.name} ({m.size} bytes)")
        
        # 获取信息
        info = utils.get_archive_info(zip_path)
        print(f"✓ 归档信息:")
        print(f"  格式：{info.format.value}")
        print(f"  压缩率：{info.compression_ratio:.2%}")
        
        # 解压
        extract_dir = os.path.join(tmpdir, "extracted")
        result = utils.extract_archive(zip_path, extract_dir)
        print(f"✓ 解压完成：{result.files_processed} 个文件")


def example_compression_levels():
    """压缩级别对比示例"""
    print("\n" + "=" * 60)
    print("示例 2: 压缩级别对比")
    print("=" * 60)
    
    utils = ArchiveUtils()
    
    with tempfile.TemporaryDirectory() as tmpdir:
        # 创建可压缩的测试数据
        test_file = os.path.join(tmpdir, "data.txt")
        with open(test_file, 'w') as f:
            # 重复内容更容易压缩
            f.write("Hello World! " * 1000)
        
        print("\n不同压缩级别对比:")
        print("-" * 40)
        
        for level in [CompressionLevel.FASTEST, CompressionLevel.DEFAULT, CompressionLevel.BEST]:
            zip_path = os.path.join(tmpdir, f"test_{level.name}.zip")
            utils.create_archive(zip_path, [test_file], compression=level)
            
            info = utils.get_archive_info(zip_path)
            print(f"\n{level.name}:")
            print(f"  归档大小：{info.size} bytes")
            print(f"  压缩率：{info.compression_ratio:.2%}")


def example_multiple_formats():
    """多格式支持示例"""
    print("\n" + "=" * 60)
    print("示例 3: 多格式支持")
    print("=" * 60)
    
    utils = ArchiveUtils()
    
    with tempfile.TemporaryDirectory() as tmpdir:
        test_file = os.path.join(tmpdir, "data.txt")
        with open(test_file, 'w') as f:
            f.write("Test content for multiple formats")
        
        formats = [
            ("test.zip", ArchiveFormat.ZIP),
            ("test.tar", ArchiveFormat.TAR),
            ("test.tar.gz", ArchiveFormat.TAR_GZ),
            ("test.tar.bz2", ArchiveFormat.TAR_BZ2),
            ("test.tar.xz", ArchiveFormat.TAR_XZ),
        ]
        
        print("\n创建不同格式的归档:")
        print("-" * 40)
        
        for filename, expected_fmt in formats:
            path = os.path.join(tmpdir, filename)
            result = utils.create_archive(path, [test_file])
            
            # 验证格式检测
            detected = utils.detect_format(path)
            status = "✓" if detected == expected_fmt else "✗"
            
            print(f"{status} {filename}:")
            print(f"    预期：{expected_fmt.value}, 检测：{detected.value if detected else 'None'}")
            print(f"    大小：{os.path.getsize(path)} bytes")


def example_verification():
    """验证与校验示例"""
    print("\n" + "=" * 60)
    print("示例 4: 验证与校验")
    print("=" * 60)
    
    utils = ArchiveUtils()
    
    with tempfile.TemporaryDirectory() as tmpdir:
        test_file = os.path.join(tmpdir, "important.txt")
        with open(test_file, 'w') as f:
            f.write("Important data that needs verification")
        
        zip_path = os.path.join(tmpdir, "verified.zip")
        utils.create_archive(zip_path, [test_file])
        
        # 完整性验证
        verify_result = utils.verify_archive(zip_path)
        print(f"\n完整性验证：{'✓ 通过' if verify_result.success else '✗ 失败'}")
        if not verify_result.success:
            print(f"  错误：{verify_result.errors}")
        
        # 多种校验和
        print("\n校验和:")
        print("-" * 40)
        for algo in ['md5', 'sha1', 'sha256']:
            checksum = utils.calculate_checksum(zip_path, algo)
            print(f"  {algo.upper()}: {checksum}")


def example_selective_extraction():
    """选择性解压示例"""
    print("\n" + "=" * 60)
    print("示例 5: 选择性解压")
    print("=" * 60)
    
    utils = ArchiveUtils()
    
    with tempfile.TemporaryDirectory() as tmpdir:
        # 创建多个文件
        files = []
        for i in range(5):
            fpath = os.path.join(tmpdir, f"file{i}.txt")
            with open(fpath, 'w') as f:
                f.write(f"Content of file {i}")
            files.append(fpath)
        
        # 创建归档
        zip_path = os.path.join(tmpdir, "multi.zip")
        utils.create_archive(zip_path, files)
        
        # 列出所有成员
        print("\n归档中的所有成员:")
        members = utils.list_archive(zip_path)
        for m in members:
            print(f"  - {m.name}")
        
        # 只解压特定文件
        extract_dir = os.path.join(tmpdir, "selective")
        result = utils.extract_archive(
            zip_path,
            extract_dir,
            members=["file0.txt", "file2.txt", "file4.txt"]
        )
        
        print(f"\n选择性解压结果:")
        print(f"  解压文件数：{result.files_processed}")
        
        # 验证
        extracted = os.listdir(extract_dir)
        print(f"  实际文件：{extracted}")


def example_archive_management():
    """归档管理示例（添加/删除）"""
    print("\n" + "=" * 60)
    print("示例 6: 归档管理")
    print("=" * 60)
    
    utils = ArchiveUtils()
    
    with tempfile.TemporaryDirectory() as tmpdir:
        # 创建初始归档
        file1 = os.path.join(tmpdir, "initial.txt")
        with open(file1, 'w') as f:
            f.write("Initial content")
        
        zip_path = os.path.join(tmpdir, "managed.zip")
        utils.create_archive(zip_path, [file1])
        
        print("\n初始状态:")
        members = utils.list_archive(zip_path)
        print(f"  成员：{[m.name for m in members]}")
        
        # 添加文件
        file2 = os.path.join(tmpdir, "added.txt")
        with open(file2, 'w') as f:
            f.write("Added content")
        
        add_result = utils.add_to_archive(zip_path, [file2])
        print(f"\n添加文件后:")
        print(f"  添加成功：{add_result.success}")
        members = utils.list_archive(zip_path)
        print(f"  成员：{[m.name for m in members]}")
        
        # 删除文件
        remove_result = utils.remove_from_archive(zip_path, ["initial.txt"])
        print(f"\n删除文件后:")
        print(f"  删除成功：{remove_result.success}")
        members = utils.list_archive(zip_path)
        print(f"  成员：{[m.name for m in members]}")


def example_backup_workflow():
    """完整备份工作流示例"""
    print("\n" + "=" * 60)
    print("示例 7: 完整备份工作流")
    print("=" * 60)
    
    utils = ArchiveUtils()
    
    with tempfile.TemporaryDirectory() as tmpdir:
        # 模拟项目目录
        project_dir = os.path.join(tmpdir, "myproject")
        os.makedirs(project_dir)
        
        # 创建项目文件
        files = {
            "src/main.py": "print('Hello')",
            "src/utils.py": "def helper(): pass",
            "README.md": "# My Project",
            "config.json": '{"version": "1.0"}',
            "tests/test_main.py": "def test(): assert True",
        }
        
        for path, content in files.items():
            full_path = os.path.join(project_dir, path)
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            with open(full_path, 'w') as f:
                f.write(content)
        
        # 创建备份
        backup_path = os.path.join(tmpdir, "backup.zip")
        print("\n创建项目备份...")
        result = utils.create_archive(
            backup_path,
            [project_dir],
            compression=CompressionLevel.BEST,
            base_dir=tmpdir
        )
        print(f"✓ 备份完成：{result.files_processed} 个文件")
        
        # 生成备份报告
        info = utils.get_archive_info(backup_path)
        print(f"\n备份报告:")
        print("-" * 40)
        print(f"  归档文件：{backup_path}")
        print(f"  归档格式：{info.format.value}")
        print(f"  文件数量：{info.file_count}")
        print(f"  原始大小：{info.uncompressed_size / 1024:.1f} KB")
        print(f"  压缩大小：{info.compressed_size / 1024:.1f} KB")
        print(f"  压缩率：{info.compression_ratio:.1%}")
        print(f"  创建时间：{info.modified}")
        
        # 验证备份
        verify_result = utils.verify_archive(backup_path)
        print(f"\n  完整性：{'✓ 验证通过' if verify_result.success else '✗ 验证失败'}")
        
        # 计算校验和用于后续验证
        checksum = utils.calculate_checksum(backup_path)
        print(f"  SHA256: {checksum[:32]}...")
        
        # 列出备份内容
        print(f"\n备份内容:")
        members = utils.list_archive(backup_path)
        for m in members:
            icon = "📁" if m.is_dir else "📄"
            print(f"  {icon} {m.name} ({m.size} bytes)")


def example_format_detection():
    """格式检测示例"""
    print("\n" + "=" * 60)
    print("示例 8: 格式检测")
    print("=" * 60)
    
    utils = ArchiveUtils()
    
    test_cases = [
        "archive.zip",
        "backup.tar.gz",
        "data.tgz",
        "files.tar.bz2",
        "logs.tar.xz",
        "document.txt.gz",
        "data.bz2",
        "archive.xz",
        "unknown.xyz",
        "ARCHIVE.ZIP",  # 测试大小写
    ]
    
    print("\n格式检测结果:")
    print("-" * 40)
    
    for filename in test_cases:
        fmt = utils.detect_format(filename)
        fmt_str = fmt.value if fmt else "未知"
        print(f"  {filename:25} → {fmt_str}")


def run_all_examples():
    """运行所有示例"""
    print("\n" + "=" * 60)
    print("AllToolkit Archive Utils - 使用示例")
    print("=" * 60)
    
    examples = [
        example_basic_usage,
        example_compression_levels,
        example_multiple_formats,
        example_verification,
        example_selective_extraction,
        example_archive_management,
        example_backup_workflow,
        example_format_detection,
    ]
    
    for example in examples:
        try:
            example()
        except Exception as e:
            print(f"\n✗ 示例执行失败：{e}")
    
    print("\n" + "=" * 60)
    print("所有示例执行完成！")
    print("=" * 60)


if __name__ == '__main__':
    run_all_examples()
