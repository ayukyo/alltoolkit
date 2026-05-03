"""
文件签名/魔数检测工具使用示例

演示如何使用 file_signature_utils 检测文件真实类型。
"""

import os
import sys
import tempfile

# 添加父目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from file_signature_utils.mod import (
    detect_file_type,
    detect_extension,
    detect_mime_type,
    verify_extension,
    batch_detect,
    is_type,
    is_image,
    is_video,
    is_audio,
    is_document,
    is_archive,
    is_executable,
    get_supported_types,
    get_extension_mime_map,
    analyze_file,
)


def example_basic_detection():
    """基本文件类型检测示例"""
    print("=" * 60)
    print("基本文件类型检测")
    print("=" * 60)
    
    # 检测各种文件格式的字节流
    test_data = [
        (b'\xff\xd8\xff\xe0\x00\x10JFIF', "JPEG 图片"),
        (b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR', "PNG 图片"),
        (b'GIF89a\x00\x00\x00', "GIF 图片"),
        (b'%PDF-1.4\n%', "PDF 文档"),
        (b'PK\x03\x04\x00\x00', "ZIP 压缩包"),
        (b'Rar!\x1a\x07\x00', "RAR 压缩包"),
        (b'\x1f\x8b\x08\x00', "GZIP 压缩包"),
        (b'ID3\x03\x00\x00', "MP3 音频"),
        (b'fLaC\x00\x00\x00', "FLAC 音频"),
        (b'\x00\x00\x00\x20ftypisom', "MP4 视频"),
        (b'\x7fELF\x02\x01', "Linux 可执行文件"),
        (b'SQLite format 3\x00', "SQLite 数据库"),
    ]
    
    for data, description in test_data:
        ft = detect_file_type(data)
        if ft:
            print(f"\n{description}:")
            print(f"  扩展名: {ft.extension}")
            print(f"  MIME类型: {ft.mime_type}")
            print(f"  描述: {ft.description}")
            print(f"  置信度: {ft.confidence}")
        else:
            print(f"\n{description}: 无法识别")


def example_extension_mime_detection():
    """扩展名和 MIME 类型检测示例"""
    print("\n" + "=" * 60)
    print("扩展名和 MIME 类型检测")
    print("=" * 60)
    
    # 只获取扩展名
    png_data = b'\x89PNG\r\n\x1a\n'
    ext = detect_extension(png_data)
    print(f"\nPNG 数据扩展名: {ext}")
    
    # 只获取 MIME 类型
    jpg_data = b'\xff\xd8\xff\xe0'
    mime = detect_mime_type(jpg_data)
    print(f"JPEG 数据 MIME 类型: {mime}")
    
    # PDF 文档
    pdf_data = b'%PDF-1.4\n%'
    ext = detect_extension(pdf_data)
    mime = detect_mime_type(pdf_data)
    print(f"PDF 扩展名: {ext}, MIME: {mime}")


def example_verify_extension():
    """验证文件扩展名示例"""
    print("\n" + "=" * 60)
    print("验证文件扩展名")
    print("=" * 60)
    
    # 创建临时文件进行测试
    with tempfile.TemporaryDirectory() as tmpdir:
        # 创建一个真正的 PNG 文件
        real_png = os.path.join(tmpdir, 'real.png')
        with open(real_png, 'wb') as f:
            f.write(b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR')
        
        match, declared, actual = verify_extension(real_png)
        print(f"\n真正的 PNG 文件 (real.png):")
        print(f"  声明扩展名: {declared}")
        print(f"  实际类型: {actual}")
        print(f"  匹配: {match}")
        
        # 创建一个伪装的文件（实际是 PNG，但声明是 TXT）
        fake_txt = os.path.join(tmpdir, 'fake.txt')
        with open(fake_txt, 'wb') as f:
            f.write(b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR')
        
        match, declared, actual = verify_extension(fake_txt)
        print(f"\n伪装的文件 (fake.txt - 实际是 PNG):")
        print(f"  声明扩展名: {declared}")
        print(f"  实际类型: {actual}")
        print(f"  匹配: {match}")
        print("  ⚠️ 警告: 扩展名与实际类型不匹配！")


def example_type_checking():
    """类型检查函数示例"""
    print("\n" + "=" * 60)
    print("类型检查函数")
    print("=" * 60)
    
    # 检查是否为特定类型
    png_data = b'\x89PNG\r\n\x1a\n'
    print(f"\nPNG 数据:")
    print(f"  is_type(png, 'png'): {is_type(png_data, 'png')}")
    print(f"  is_type(png, 'jpg'): {is_type(png_data, 'jpg')}")
    print(f"  is_image(png): {is_image(png_data)}")
    print(f"  is_video(png): {is_video(png_data)}")
    
    # 检查视频
    mp4_data = b'\x00\x00\x00\x20ftypisom'
    print(f"\nMP4 数据:")
    print(f"  is_video(mp4): {is_video(mp4_data)}")
    print(f"  is_audio(mp4): {is_audio(mp4_data)}")
    
    # 检查音频
    mp3_data = b'ID3\x03\x00\x00'
    print(f"\nMP3 数据:")
    print(f"  is_audio(mp3): {is_audio(mp3_data)}")
    print(f"  is_image(mp3): {is_image(mp3_data)}")
    
    # 检查压缩包
    zip_data = b'PK\x03\x04\x00\x00'
    rar_data = b'Rar!\x1a\x07\x00'
    print(f"\n压缩包数据:")
    print(f"  is_archive(zip): {is_archive(zip_data)}")
    print(f"  is_archive(rar): {is_archive(rar_data)}")
    
    # 检查可执行文件
    elf_data = b'\x7fELF\x02\x01'
    print(f"\nELF 可执行文件:")
    print(f"  is_executable(elf): {is_executable(elf_data)}")


def example_batch_detection():
    """批量检测示例"""
    print("\n" + "=" * 60)
    print("批量文件检测")
    print("=" * 60)
    
    with tempfile.TemporaryDirectory() as tmpdir:
        # 创建多个临时文件
        files = []
        
        # 图片文件
        img_file = os.path.join(tmpdir, 'image.png')
        with open(img_file, 'wb') as f:
            f.write(b'\x89PNG\r\n\x1a\n')
        files.append(img_file)
        
        # 音频文件
        audio_file = os.path.join(tmpdir, 'audio.mp3')
        with open(audio_file, 'wb') as f:
            f.write(b'ID3\x03\x00\x00')
        files.append(audio_file)
        
        # 文档文件
        doc_file = os.path.join(tmpdir, 'document.pdf')
        with open(doc_file, 'wb') as f:
            f.write(b'%PDF-1.4\n%')
        files.append(doc_file)
        
        # 未知文件
        unknown_file = os.path.join(tmpdir, 'unknown.dat')
        with open(unknown_file, 'wb') as f:
            f.write(b'\x00\x01\x02\x03\x04\x05')
        files.append(unknown_file)
        
        # 批量检测
        results = batch_detect(files)
        
        for file_path, ft in results.items():
            filename = os.path.basename(file_path)
            if ft:
                print(f"\n{filename}:")
                print(f"  类型: {ft.description}")
                print(f"  扩展名: {ft.extension}")
            else:
                print(f"\n{filename}: 无法识别")


def example_analyze_file():
    """全面文件分析示例"""
    print("\n" + "=" * 60)
    print("全面文件分析")
    print("=" * 60)
    
    with tempfile.TemporaryDirectory() as tmpdir:
        # 创建一个图片文件
        img_file = os.path.join(tmpdir, 'test.png')
        with open(img_file, 'wb') as f:
            f.write(b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR')
        
        # 全面分析
        result = analyze_file(img_file)
        
        print(f"\n文件: test.png")
        print(f"  文件类型: {result['file_type']}")
        print(f"  文件大小: {result['size']} 字节")
        print(f"  声明扩展名: {result['declared_extension']}")
        print(f"  实际扩展名: {result['actual_extension']}")
        print(f"  扩展名匹配: {result['extension_match']}")
        print(f"  是图片: {result['is_image']}")
        print(f"  是视频: {result['is_video']}")
        print(f"  是音频: {result['is_audio']}")
        print(f"  是文档: {result['is_document']}")
        print(f"  是压缩包: {result['is_archive']}")
        print(f"  是可执行文件: {result['is_executable']}")


def example_supported_types():
    """支持的文件类型示例"""
    print("\n" + "=" * 60)
    print("支持的文件类型")
    print("=" * 60)
    
    types = get_supported_types()
    
    for category, extensions in types.items():
        print(f"\n{category}:")
        print(f"  {', '.join(extensions)}")
    
    # MIME 类型映射
    print("\n" + "=" * 60)
    print("扩展名到 MIME 类型映射")
    print("=" * 60)
    
    mime_map = get_extension_mime_map()
    common_extensions = ['jpg', 'png', 'gif', 'mp4', 'mp3', 'pdf', 'zip', 'json', 'xml']
    
    for ext in common_extensions:
        mime = mime_map.get(ext)
        print(f"  {ext}: {mime}")


def example_security_check():
    """安全检查示例"""
    print("\n" + "=" * 60)
    print("安全检查场景")
    print("=" * 60)
    
    print("\n场景: 检查上传的文件是否伪装")
    
    with tempfile.TemporaryDirectory() as tmpdir:
        # 用户上传了一个声称是图片的文件
        uploaded_file = os.path.join(tmpdir, 'safe_image.jpg')
        with open(uploaded_file, 'wb') as f:
            f.write(b'\xff\xd8\xff\xe0\x00\x10JFIF')  # 真正的 JPEG
        
        match, declared, actual = verify_extension(uploaded_file)
        
        if match:
            print(f"✅ 文件验证通过: {declared} == {actual}")
        else:
            print(f"❌ 文件验证失败: 声明是 {declared}, 实际是 {actual}")
        
        # 检查是否真的是图片
        if is_image(uploaded_file):
            print("✅ 文件确实是图片类型")
        else:
            print("❌ 文件不是图片类型")
        
        # 检查另一个伪装的可执行文件
        malware_file = os.path.join(tmpdir, 'cute_cat.jpg')
        with open(malware_file, 'wb') as f:
            f.write(b'\x7fELF\x02\x01\x01\x00')  # ELF 可执行文件
        
        match, declared, actual = verify_extension(malware_file)
        
        print(f"\n伪装的可执行文件:")
        if not match:
            print(f"❌ 文件伪装检测: 声明是 {declared}, 实际是 {actual}")
        
        if is_executable(malware_file):
            print("⚠️ 警告: 文件实际是可执行程序，可能是恶意软件！")


def example_file_object_input():
    """文件对象输入示例"""
    print("\n" + "=" * 60)
    print("使用文件对象检测")
    print("=" * 60)
    
    with tempfile.TemporaryDirectory() as tmpdir:
        test_file = os.path.join(tmpdir, 'test.pdf')
        with open(test_file, 'wb') as f:
            f.write(b'%PDF-1.4\n%')
        
        # 使用文件对象而不是路径
        with open(test_file, 'rb') as f:
            # 文件对象可以作为输入
            ft = detect_file_type(f)
            print(f"\n从文件对象检测:")
            print(f"  类型: {ft.description}")
            print(f"  扩展名: {ft.extension}")
            print(f"  MIME: {ft.mime_type}")
            
            # 文件位置保持不变，可以继续读取
            content = f.read(100)
            print(f"  读取内容长度: {len(content)}")


def main():
    """运行所有示例"""
    print("\n" + "#" * 60)
    print("# 文件签名/魔数检测工具使用示例")
    print("#" * 60)
    
    example_basic_detection()
    example_extension_mime_detection()
    example_verify_extension()
    example_type_checking()
    example_batch_detection()
    example_analyze_file()
    example_supported_types()
    example_security_check()
    example_file_object_input()
    
    print("\n" + "=" * 60)
    print("示例完成")
    print("=" * 60)


if __name__ == '__main__':
    main()