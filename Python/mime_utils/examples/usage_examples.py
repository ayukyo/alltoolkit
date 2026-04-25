"""
MIME 类型工具模块使用示例
=======================

本示例展示 mime_utils 模块的主要功能：
1. 根据扩展名获取 MIME 类型
2. 根据 MIME 类型获取扩展名
3. 通过魔数检测文件类型
4. 类型判断函数
5. Content-Disposition 生成
"""

import sys
import os

# 添加父目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from mime_utils.mod import (
    get_mime_type,
    get_extensions,
    get_primary_extension,
    detect_mime_from_content,
    detect_mime_from_file,
    is_image,
    is_video,
    is_audio,
    is_document,
    is_text,
    is_archive,
    is_code,
    get_category,
    get_mime_info,
    parse_mime_type,
    build_mime_type,
    content_disposition,
    guess_type,
    MimeTypeDetector,
)


def print_header(title):
    """打印标题"""
    print(f"\n{'=' * 60}")
    print(f"  {title}")
    print('=' * 60)


def example_basic_lookup():
    """基本查询示例"""
    print_header("1. 基本 MIME 类型查询")
    
    # 根据扩展名获取 MIME 类型
    print("\n根据扩展名获取 MIME 类型:")
    extensions = ['.jpg', '.png', '.mp4', '.pdf', '.zip', '.py']
    for ext in extensions:
        mime = get_mime_type(ext)
        print(f"  {ext:10} -> {mime}")
    
    # 不带点的扩展名也可以
    print("\n不带点的扩展名:")
    print(f"  'jpg'      -> {get_mime_type('jpg')}")
    print(f"  'html'     -> {get_mime_type('html')}")
    
    # 大小写不敏感
    print("\n大小写不敏感:")
    print(f"  '.JPG'     -> {get_mime_type('.JPG')}")
    print(f"  '.PNG'     -> {get_mime_type('.PNG')}")
    
    # 未知类型返回默认值
    print("\n未知类型返回默认值:")
    print(f"  '.xyz'     -> {get_mime_type('.xyz')}")
    print(f"  '.xyz' (自定义默认) -> {get_mime_type('.xyz', 'text/plain')}")


def example_reverse_lookup():
    """反向查询示例"""
    print_header("2. MIME 类型 -> 扩展名查询")
    
    # 获取所有扩展名
    print("\n获取所有扩展名:")
    mimes = ['image/jpeg', 'video/mp4', 'application/json', 'application/octet-stream']
    for mime in mimes:
        exts = get_extensions(mime)
        print(f"  {mime:30} -> {exts}")
    
    # 获取首选扩展名
    print("\n获取首选扩展名:")
    print(f"  'image/jpeg' -> {get_primary_extension('image/jpeg')}")
    print(f"  'image/png'  -> {get_primary_extension('image/png')}")
    print(f"  'unknown'    -> {get_primary_extension('unknown/type', '.bin')}")


def example_magic_detection():
    """魔数检测示例"""
    print_header("3. 魔数检测文件类型")
    
    # JPEG 魔数
    print("\n检测 JPEG (魔数: FF D8 FF):")
    jpeg_data = b'\xff\xd8\xff\xe0\x00\x10JFIF\x00'
    print(f"  数据: {jpeg_data[:10].hex()}")
    print(f"  类型: {detect_mime_from_content(jpeg_data)}")
    
    # PNG 魔数
    print("\n检测 PNG (魔数: 89 50 4E 47...):")
    png_data = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR'
    print(f"  数据: {png_data[:10].hex()}")
    print(f"  类型: {detect_mime_from_content(png_data)}")
    
    # PDF 魔数
    print("\n检测 PDF:")
    pdf_data = b'%PDF-1.4\n%'
    print(f"  数据: {pdf_data.decode('ascii', errors='replace')[:10]}")
    print(f"  类型: {detect_mime_from_content(pdf_data)}")
    
    # ZIP 魔数
    print("\n检测 ZIP:")
    zip_data = b'PK\x03\x04\x14\x00\x00\x00\x08\x00'
    print(f"  数据: {zip_data[:10].hex()}")
    print(f"  类型: {detect_mime_from_content(zip_data)}")
    
    # MP3 (带 ID3 标签)
    print("\n检测 MP3 (ID3 标签):")
    mp3_data = b'ID3\x03\x00\x00\x00\x00\x00\x00'
    print(f"  数据: {mp3_data[:10].hex()}")
    print(f"  类型: {detect_mime_from_content(mp3_data)}")
    
    # WAV (RIFF 格式)
    print("\n检测 WAV:")
    wav_data = b'RIFF\x24\x00\x00\x00WAVEfmt '
    print(f"  数据: {wav_data[:12]}")
    print(f"  类型: {detect_mime_from_content(wav_data)}")


def example_type_checks():
    """类型判断示例"""
    print_header("4. 类型判断函数")
    
    test_types = [
        'image/jpeg',
        'image/png',
        'video/mp4',
        'video/webm',
        'audio/mpeg',
        'audio/wav',
        'application/pdf',
        'application/zip',
        'text/plain',
        'text/x-python',
    ]
    
    print("\n类型分类:")
    print(f"  {'MIME 类型':<35} {'类别':<12} {'图片':<6} {'视频':<6} {'音频':<6} {'文档':<6} {'文本':<6} {'压缩':<6}")
    print(f"  {'-' * 35} {'-' * 12} {'-' * 6} {'-' * 6} {'-' * 6} {'-' * 6} {'-' * 6} {'-' * 6}")
    
    for mime in test_types:
        category = get_category(mime) or '-'
        print(f"  {mime:<35} {category:<12} "
              f"{'✓' if is_image(mime) else '':<6} "
              f"{'✓' if is_video(mime) else '':<6} "
              f"{'✓' if is_audio(mime) else '':<6} "
              f"{'✓' if is_document(mime) else '':<6} "
              f"{'✓' if is_text(mime) else '':<6} "
              f"{'✓' if is_archive(mime) else '':<6}")


def example_mime_info():
    """MIME 类型信息示例"""
    print_header("5. 获取 MIME 类型详细信息")
    
    mimes = ['image/jpeg', 'video/mp4', 'text/html']
    
    for mime in mimes:
        info = get_mime_info(mime)
        print(f"\n{mime}:")
        print(f"  扩展名: {info['extensions']}")
        print(f"  首选扩展名: {info['primary_extension']}")
        print(f"  类别: {info['category']}")
        print(f"  是图片: {info['is_image']}")
        print(f"  是视频: {info['is_video']}")
        print(f"  是音频: {info['is_audio']}")


def example_parse_build():
    """解析和构建示例"""
    print_header("6. 解析和构建 MIME 类型")
    
    # 解析 MIME 类型
    print("\n解析 MIME 类型:")
    test_strings = [
        'text/html',
        'text/html; charset=utf-8',
        'application/json; charset=utf-8; indent=2',
    ]
    
    for s in test_strings:
        mime, params = parse_mime_type(s)
        print(f"  '{s}'")
        print(f"    -> MIME: {mime}, 参数: {params}")
    
    # 构建 MIME 类型
    print("\n构建 MIME 类型:")
    print(f"  build_mime_type('text/html'): {build_mime_type('text/html')}")
    print(f"  build_mime_type('text/html', {{'charset': 'utf-8'}}): {build_mime_type('text/html', {'charset': 'utf-8'})}")


def example_content_disposition():
    """Content-Disposition 示例"""
    print_header("7. Content-Disposition 生成")
    
    filenames = [
        'report.pdf',
        'image.png',
        '中文文件.txt',
        'file with spaces.doc',
        'file"with"quotes.csv',
    ]
    
    print("\n附件模式:")
    for filename in filenames:
        cd = content_disposition(filename)
        print(f"  {filename:<25} -> {cd}")
    
    print("\n内联模式:")
    for filename in ['image.png', 'document.pdf']:
        cd = content_disposition(filename, inline=True)
        print(f"  {filename:<25} -> {cd}")


def example_guess_type():
    """guess_type 示例"""
    print_header("8. guess_type (兼容 mimetypes)")
    
    filenames = [
        'document.pdf',
        '/path/to/image.jpg',
        'C:\\Users\\test\\video.mp4',
        'archive.tar.gz',
        'unknown.xyz',
    ]
    
    for filename in filenames:
        mime = guess_type(filename)
        print(f"  {filename:<35} -> {mime}")


def example_detector_class():
    """MimeTypeDetector 类示例"""
    print_header("9. MimeTypeDetector 类")
    
    detector = MimeTypeDetector()
    
    # 使用内容检测
    print("\n内容检测:")
    jpeg_data = b'\xff\xd8\xff\xe0\x00\x10JFIF'
    print(f"  JPEG 数据: {detector.detect(jpeg_data)}")
    
    unknown_data = b'some unknown data'
    print(f"  未知数据 (无扩展名): {detector.detect(unknown_data)}")
    print(f"  未知数据 (带扩展名 .txt): {detector.detect(unknown_data, extension='.txt')}")


def example_web_server():
    """Web 服务器使用示例"""
    print_header("10. Web 服务器场景示例")
    
    def simulate_http_response(filename, content=None):
        """模拟 HTTP 响应生成"""
        # 获取 MIME 类型
        content_type = get_mime_type(os.path.splitext(filename)[1])
        
        # 生成 Content-Disposition
        if is_image(content_type) or is_text(content_type):
            cd = content_disposition(filename, inline=True)
        else:
            cd = content_disposition(filename, inline=False)
        
        # 检测内容类型（如果有内容）
        detected = None
        if content:
            detected = detect_mime_from_content(content)
        
        print(f"\n  文件: {filename}")
        print(f"  Content-Type: {content_type}")
        print(f"  Content-Disposition: {cd}")
        print(f"  类别: {get_category(content_type)}")
        if detected and detected != content_type:
            print(f"  ⚠️ 内容检测与扩展名不符: {detected}")
    
    simulate_http_response('image.jpg')
    simulate_http_response('document.pdf')
    simulate_http_response('video.mp4')
    simulate_http_response('data.json')
    
    # 模拟文件上传验证
    print("\n\n文件上传验证示例:")
    
    def validate_upload(filename, content):
        """验证上传文件"""
        ext_mime = get_mime_type(os.path.splitext(filename)[1])
        content_mime = detect_mime_from_content(content)
        
        print(f"\n  上传文件: {filename}")
        print(f"  扩展名类型: {ext_mime}")
        print(f"  内容类型: {content_mime}")
        
        if ext_mime != content_mime:
            print(f"  ⚠️ 警告: 扩展名与内容不匹配!")
        else:
            print(f"  ✓ 验证通过")
        
        return ext_mime == content_mime
    
    # 正常文件
    validate_upload('image.jpg', b'\xff\xd8\xff\xe0\x00\x10JFIF')
    
    # 伪装文件
    validate_upload('image.jpg', b'%PDF-1.4')


def example_file_filter():
    """文件过滤示例"""
    print_header("11. 文件过滤场景")
    
    files = [
        'photo.jpg', 'video.mp4', 'song.mp3', 'report.pdf',
        'data.json', 'archive.zip', 'script.py', 'index.html',
        'styles.css', 'config.yaml'
    ]
    
    print("\n按类别过滤文件:")
    
    print("\n  图片文件:")
    for f in files:
        if is_image(get_mime_type(os.path.splitext(f)[1])):
            print(f"    - {f}")
    
    print("\n  媒体文件 (视频+音频):")
    for f in files:
        mime = get_mime_type(os.path.splitext(f)[1])
        if is_video(mime) or is_audio(mime):
            print(f"    - {f}")
    
    print("\n  代码文件:")
    for f in files:
        if is_code(get_mime_type(os.path.splitext(f)[1])):
            print(f"    - {f}")
    
    print("\n  文档文件:")
    for f in files:
        if is_document(get_mime_type(os.path.splitext(f)[1])):
            print(f"    - {f}")


def main():
    """运行所有示例"""
    example_basic_lookup()
    example_reverse_lookup()
    example_magic_detection()
    example_type_checks()
    example_mime_info()
    example_parse_build()
    example_content_disposition()
    example_guess_type()
    example_detector_class()
    example_web_server()
    example_file_filter()
    
    print("\n" + "=" * 60)
    print("  所有示例运行完成!")
    print("=" * 60 + "\n")


if __name__ == '__main__':
    main()