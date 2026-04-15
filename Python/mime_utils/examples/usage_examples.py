"""
MIME 工具模块使用示例

演示如何使用 mime_utils 处理 MIME 类型相关任务。
"""

import sys
import os

# 添加父目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    get_mime_type, get_extension, get_extensions,
    is_category, get_category,
    is_image, is_video, is_audio, is_document, is_text,
    is_archive, is_code,
    parse_content_type, build_content_type,
    build_content_disposition,
    guess_type_from_content,
    get_mime_info,
    MimeTypeRegistry,
)


def example_basic_usage():
    """基本用法示例"""
    print("=" * 60)
    print("基本用法")
    print("=" * 60)
    
    # 根据文件名获取 MIME 类型
    print("\n1. 根据文件名获取 MIME 类型:")
    files = ['image.png', 'document.pdf', 'video.mp4', 'data.json', 'script.js']
    for f in files:
        mime = get_mime_type(f)
        print(f"   {f:20} -> {mime}")
    
    # 根据扩展名获取 MIME 类型
    print("\n2. 根据扩展名获取 MIME 类型:")
    exts = ['.png', 'jpg', 'md', 'docx', 'woff2']
    for ext in exts:
        mime = get_mime_type(ext)
        print(f"   {ext:10} -> {mime}")
    
    # 根据 MIME 类型获取扩展名
    print("\n3. 根据 MIME 类型获取扩展名:")
    mimes = ['image/png', 'application/json', 'text/markdown', 'video/webm']
    for mime in mimes:
        ext = get_extension(mime)
        print(f"   {mime:30} -> {ext}")


def example_category_detection():
    """类别检测示例"""
    print("\n" + "=" * 60)
    print("类别检测")
    print("=" * 60)
    
    # 检测文件类别
    print("\n1. 检测文件类别:")
    test_files = [
        ('photo.jpg', 'image/jpeg'),
        ('movie.mp4', 'video/mp4'),
        ('song.mp3', 'audio/mpeg'),
        ('report.pdf', 'application/pdf'),
        ('data.json', 'application/json'),
        ('archive.zip', 'application/zip'),
        ('script.js', 'application/javascript'),
    ]
    
    for filename, expected_mime in test_files:
        mime = get_mime_type(filename)
        category = get_category(mime)
        print(f"   {filename:15} -> {mime:45} [{category or 'unknown'}]")
    
    # 使用便捷函数
    print("\n2. 使用便捷函数判断类别:")
    test_mimes = [
        'image/png',
        'video/mp4',
        'audio/mpeg',
        'application/pdf',
        'text/plain',
        'application/zip',
        'application/javascript',
    ]
    
    for mime in test_mimes:
        checks = []
        if is_image(mime): checks.append('图片')
        if is_video(mime): checks.append('视频')
        if is_audio(mime): checks.append('音频')
        if is_document(mime): checks.append('文档')
        if is_text(mime): checks.append('文本')
        if is_archive(mime): checks.append('压缩包')
        if is_code(mime): checks.append('代码')
        
        categories = ' | '.join(checks) if checks else '未知'
        print(f"   {mime:35} -> {categories}")


def example_content_type_handling():
    """Content-Type 处理示例"""
    print("\n" + "=" * 60)
    print("Content-Type 处理")
    print("=" * 60)
    
    # 解析 Content-Type
    print("\n1. 解析 Content-Type 头:")
    headers = [
        'text/html',
        'text/html; charset=utf-8',
        'application/json; charset=utf-8',
        'multipart/form-data; boundary=----WebKitFormBoundary',
        'text/plain; charset=utf-8; format=flowed',
    ]
    
    for header in headers:
        mime, params = parse_content_type(header)
        params_str = ', '.join(f'{k}={v}' for k, v in params.items())
        print(f"   {header}")
        print(f"      MIME: {mime}, 参数: {params_str or '无'}")
    
    # 构建 Content-Type
    print("\n2. 构建 Content-Type 头:")
    
    # 简单
    ct = build_content_type('text/html')
    print(f"   简单: {ct}")
    
    # 带 charset
    ct = build_content_type('text/html', charset='utf-8')
    print(f"   带 charset: {ct}")
    
    # multipart
    ct = build_content_type('multipart/form-data', boundary='----WebKitFormBoundary')
    print(f"   multipart: {ct}")
    
    # 自定义参数
    ct = build_content_type('application/json', charset='utf-8', version='1.0')
    print(f"   自定义参数: {ct}")


def example_content_disposition():
    """Content-Disposition 处理示例"""
    print("\n" + "=" * 60)
    print("Content-Disposition 处理")
    print("=" * 60)
    
    # 构建下载头
    print("\n1. 构建下载头:")
    filenames = ['report.pdf', 'image.png', 'data.json', '报告.pdf', '文件.docx']
    
    for filename in filenames:
        cd = build_content_disposition(filename, disposition='attachment')
        print(f"   {filename:15} -> {cd}")
    
    # 构建内联显示头
    print("\n2. 构建内联显示头:")
    for filename in ['image.png', 'preview.pdf']:
        cd = build_content_disposition(filename, disposition='inline')
        print(f"   {filename:15} -> {cd}")


def example_content_detection():
    """内容检测示例"""
    print("\n" + "=" * 60)
    print("根据内容检测 MIME 类型（魔数检测）")
    print("=" * 60)
    
    # 模拟文件内容
    print("\n1. 根据文件头检测类型:")
    
    test_contents = [
        (b'\x89PNG\r\n\x1a\n', 'PNG 图片'),
        (b'\xff\xd8\xff\xe0\x00\x10JFIF', 'JPEG 图片'),
        (b'GIF89a', 'GIF 图片'),
        (b'%PDF-1.4', 'PDF 文档'),
        (b'PK\x03\x04', 'ZIP 压缩包'),
        (b'\x1f\x8b\x08', 'GZIP 压缩包'),
        (b'ID3', 'MP3 音频（带 ID3）'),
        (b'\x1aE\xdf\xa3', 'WebM 视频'),
    ]
    
    for content, desc in test_contents:
        mime = guess_type_from_content(content)
        print(f"   {desc:20} -> {mime}")
    
    # 检测文本
    print("\n2. 检测文本内容:")
    text_content = b'Hello, World! This is plain text.'
    mime = guess_type_from_content(text_content)
    print(f"   纯文本 -> {mime}")


def example_mime_info():
    """MIME 类型信息示例"""
    print("\n" + "=" * 60)
    print("获取 MIME 类型详细信息")
    print("=" * 60)
    
    test_mimes = [
        'image/png',
        'video/mp4',
        'application/pdf',
        'text/markdown',
        'application/json',
    ]
    
    for mime in test_mimes:
        info = get_mime_info(mime)
        print(f"\n   {mime}")
        print(f"   ─────────────────────")
        print(f"   类别: {info['category'] or '未知'}")
        print(f"   扩展名: {', '.join(info['extensions'])}")
        print(f"   可内联显示: {'是' if info['inline_displayable'] else '否'}")
        print(f"   文本可读: {'是' if info['text_readable'] else '否'}")


def example_custom_registry():
    """自定义 MIME 注册表示例"""
    print("\n" + "=" * 60)
    print("自定义 MIME 类型注册表")
    print("=" * 60)
    
    # 创建自定义注册表
    registry = MimeTypeRegistry()
    
    # 注册自定义类型
    print("\n1. 注册自定义 MIME 类型:")
    registry.register('.xyz', 'application/x-xyz-file')
    registry.register('.abc', 'application/x-abc-file')
    print("   已注册: .xyz -> application/x-xyz-file")
    print("   已注册: .abc -> application/x-abc-file")
    
    # 使用注册表
    print("\n2. 使用注册表查询:")
    print(f"   get_mime_type('file.xyz') -> {registry.get_mime_type('file.xyz')}")
    print(f"   get_extension('application/x-xyz-file') -> {registry.get_extension('application/x-xyz-file')}")
    
    # 回退到全局
    print("\n3. 回退到全局映射（未注册的类型）:")
    print(f"   get_mime_type('image.png') -> {registry.get_mime_type('image.png')}")
    
    # 列出所有注册
    print("\n4. 列出所有已注册映射:")
    for ext, mime in registry.list_all().items():
        print(f"   {ext} -> {mime}")


def example_practical_use_cases():
    """实际应用场景示例"""
    print("\n" + "=" * 60)
    print("实际应用场景")
    print("=" * 60)
    
    # 场景1：文件上传处理
    print("\n1. 文件上传处理:")
    uploaded_file = 'user_avatar.png'
    mime = get_mime_type(uploaded_file)
    
    if is_image(mime):
        print(f"   ✓ {uploaded_file} 是有效的图片文件 ({mime})")
    else:
        print(f"   ✗ {uploaded_file} 不是有效的图片文件")
    
    # 场景2：HTTP 响应头设置
    print("\n2. 设置 HTTP 响应头:")
    filename = '下载报告.pdf'
    mime = get_mime_type(filename)
    charset = 'utf-8' if is_text(mime) else None
    
    content_type = build_content_type(mime, charset=charset)
    content_disposition = build_content_disposition(filename)
    
    print(f"   Content-Type: {content_type}")
    print(f"   Content-Disposition: {content_disposition}")
    
    # 场景3：文件类型过滤
    print("\n3. 文件类型过滤:")
    all_files = ['photo.jpg', 'document.pdf', 'video.mp4', 'music.mp3', 'archive.zip', 'data.json']
    
    allowed_types = ['image', 'document']
    filtered = [f for f in all_files if is_category(get_mime_type(f), allowed_types[0]) 
                or is_category(get_mime_type(f), allowed_types[1])]
    
    print(f"   所有文件: {all_files}")
    print(f"   允许类型: {allowed_types}")
    print(f"   过滤结果: {filtered}")
    
    # 场景4：安全检查
    print("\n4. 文件安全检查:")
    def check_file_safety(filename: str) -> tuple[bool, str]:
        mime = get_mime_type(filename)
        category = get_category(mime)
        
        # 禁止可执行文件
        dangerous_extensions = ['.exe', '.bat', '.cmd', '.sh', '.ps1']
        ext = '.' + filename.rsplit('.', 1)[-1].lower() if '.' in filename else ''
        
        if ext in dangerous_extensions:
            return False, f"禁止上传可执行文件 ({ext})"
        
        if is_binary(mime) and not is_image(mime):
            return False, f"禁止上传未知二进制文件 ({mime})"
        
        return True, f"文件类型: {mime} ({category or '未知'})"
    
    test_files = ['image.png', 'program.exe', 'document.pdf', 'unknown.bin']
    for f in test_files:
        safe, msg = check_file_safety(f)
        status = "✓" if safe else "✗"
        print(f"   {status} {f:20} -> {msg}")


def main():
    """运行所有示例"""
    example_basic_usage()
    example_category_detection()
    example_content_type_handling()
    example_content_disposition()
    example_content_detection()
    example_mime_info()
    example_custom_registry()
    example_practical_use_cases()
    
    print("\n" + "=" * 60)
    print("示例完成！")
    print("=" * 60)


if __name__ == '__main__':
    main()