"""
File Utils 使用示例

演示 file_utils.py 中各函数的使用方法
直接运行: python example_file_utils.py
"""

from file_utils import (
    safe_read_text,
    safe_write_text,
    get_file_hash,
    get_file_size,
    ensure_dir,
    list_files,
    copy_file,
    move_file,
    delete_file,
    get_unique_filename
)
import tempfile
import os


def demo_safe_write_and_read():
    """演示安全读写功能"""
    print("=" * 50)
    print("演示: safe_write_text / safe_read_text")
    print("=" * 50)
    
    # 创建临时目录
    temp_dir = tempfile.mkdtemp()
    test_file = os.path.join(temp_dir, "test.txt")
    
    # 写入文件
    content = "Hello, AllToolkit!\n这是测试内容。"
    success = safe_write_text(test_file, content)
    print(f"写入文件: {success}")
    
    # 读取文件
    read_content = safe_read_text(test_file, default="读取失败")
    print(f"读取内容: {read_content}")
    
    # 自动创建目录
    nested_file = os.path.join(temp_dir, "sub", "dir", "nested.txt")
    safe_write_text(nested_file, "自动创建目录结构")
    print(f"嵌套文件已创建: {os.path.exists(nested_file)}")
    
    # 清理
    import shutil
    shutil.rmtree(temp_dir)
    print(f"临时目录已清理")
    print()


def demo_file_hash():
    """演示文件哈希功能"""
    print("=" * 50)
    print("演示: get_file_hash")
    print("=" * 50)
    
    temp_dir = tempfile.mkdtemp()
    test_file = os.path.join(temp_dir, "hash_test.txt")
    
    # 写入测试内容
    safe_write_text(test_file, "Test content for hashing")
    
    # 计算不同算法的哈希
    md5_hash = get_file_hash(test_file, algorithm='md5')
    sha256_hash = get_file_hash(test_file, algorithm='sha256')
    
    print(f"MD5:    {md5_hash}")
    print(f"SHA256: {sha256_hash}")
    
    # 清理
    import shutil
    shutil.rmtree(temp_dir)
    print()


def demo_file_size():
    """演示文件大小功能"""
    print("=" * 50)
    print("演示: get_file_size")
    print("=" * 50)
    
    temp_dir = tempfile.mkdtemp()
    test_file = os.path.join(temp_dir, "size_test.txt")
    
    # 写入 2048 字节内容
    safe_write_text(test_file, "X" * 2048)
    
    size_bytes = get_file_size(test_file)
    size_human = get_file_size(test_file, human_readable=True)
    
    print(f"文件大小: {size_bytes} bytes")
    print(f"人类可读: {size_human}")
    
    # 清理
    import shutil
    shutil.rmtree(temp_dir)
    print()


def demo_ensure_dir():
    """演示目录创建功能"""
    print("=" * 50)
    print("演示: ensure_dir")
    print("=" * 50)
    
    temp_dir = tempfile.mkdtemp()
    new_dir = os.path.join(temp_dir, "level1", "level2", "level3")
    
    result = ensure_dir(new_dir)
    print(f"创建目录: {result}")
    print(f"目录存在: {os.path.isdir(new_dir)}")
    
    # 清理
    import shutil
    shutil.rmtree(temp_dir)
    print()


def demo_list_files():
    """演示文件列表功能"""
    print("=" * 50)
    print("演示: list_files")
    print("=" * 50)
    
    temp_dir = tempfile.mkdtemp()
    
    # 创建测试文件
    safe_write_text(os.path.join(temp_dir, "file1.txt"), "content1")
    safe_write_text(os.path.join(temp_dir, "file2.py"), "content2")
    safe_write_text(os.path.join(temp_dir, "file3.txt"), "content3")
    ensure_dir(os.path.join(temp_dir, "subdir"))
    safe_write_text(os.path.join(temp_dir, "subdir", "nested.py"), "nested")
    
    # 列出所有文件
    all_files = list_files(temp_dir)
    print(f"所有文件: {[f.name for f in all_files]}")
    
    # 列出 .txt 文件
    txt_files = list_files(temp_dir, pattern="*.txt")
    print(f"TXT 文件: {[f.name for f in txt_files]}")
    
    # 递归列出
    recursive_files = list_files(temp_dir, recursive=True)
    print(f"递归文件: {[f.name for f in recursive_files]}")
    
    # 清理
    import shutil
    shutil.rmtree(temp_dir)
    print()


def demo_file_operations():
    """演示文件操作功能"""
    print("=" * 50)
    print("演示: copy_file / move_file / delete_file")
    print("=" * 50)
    
    temp_dir = tempfile.mkdtemp()
    src_file = os.path.join(temp_dir, "source.txt")
    copy_dest = os.path.join(temp_dir, "backup", "source_copy.txt")
    move_dest = os.path.join(temp_dir, "moved.txt")
    
    # 创建源文件
    safe_write_text(src_file, "Original content")
    
    # 复制文件
    copy_result = copy_file(src_file, copy_dest)
    print(f"复制结果: {copy_result}")
    print(f"复制文件存在: {os.path.exists(copy_dest)}")
    
    # 移动文件
    move_result = move_file(src_file, move_dest)
    print(f"移动结果: {move_result}")
    print(f"源文件存在: {os.path.exists(src_file)}")
    print(f"目标文件存在: {os.path.exists(move_dest)}")
    
    # 删除文件
    delete_result = delete_file(move_dest)
    print(f"删除结果: {delete_result}")
    print(f"文件存在: {os.path.exists(move_dest)}")
    
    # 清理
    import shutil
    shutil.rmtree(temp_dir)
    print()


def demo_unique_filename():
    """演示唯一文件名功能"""
    print("=" * 50)
    print("演示: get_unique_filename")
    print("=" * 50)
    
    temp_dir = tempfile.mkdtemp()
    base_file = os.path.join(temp_dir, "report.pdf")
    
    # 创建原始文件
    safe_write_text(base_file, "original")
    
    # 获取唯一文件名
    unique1 = get_unique_filename(base_file)
    unique2 = get_unique_filename(base_file)
    unique3 = get_unique_filename(base_file, suffix_format="({})")
    
    print(f"原始文件: {base_file}")
    print(f"唯一名 1: {unique1.name}")
    print(f"唯一名 2: {unique2.name}")
    print(f"唯一名 3: {unique3.name}")
    
    # 清理
    import shutil
    shutil.rmtree(temp_dir)
    print()


if __name__ == "__main__":
    print("\n" + "=" * 50)
    print("AllToolkit - Python File Utils 示例")
    print("=" * 50 + "\n")
    
    demo_safe_write_and_read()
    demo_file_hash()
    demo_file_size()
    demo_ensure_dir()
    demo_list_files()
    demo_file_operations()
    demo_unique_filename()
    
    print("=" * 50)
    print("所有示例运行完成！")
    print("=" * 50)
