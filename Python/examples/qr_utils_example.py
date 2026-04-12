#!/usr/bin/env python3
"""
QR Code Utilities Examples
二维码工具库使用示例

演示 qr_utils 模块的各种使用场景。

Author: AllToolkit
Version: 1.0.0
"""

import os
import sys
import tempfile

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from qr_utils import (
    generate_qr_matrix,
    render_qr_ascii,
    render_qr_emoji,
    save_qr_image,
    generate_qr_data_url,
    encode_url,
    encode_vcard,
    encode_wifi,
    encode_email,
    encode_sms,
    encode_text,
    get_qr_info,
    validate_qr_data,
    get_matrix_stats,
    generate_qr_batch,
)


def print_section(title: str):
    """打印章节标题"""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def example_basic_usage():
    """示例 1: 基本用法"""
    print_section("示例 1: 基本用法")
    
    # 生成 QR 码
    data = "Hello, AllToolkit!"
    print(f"生成 QR 码：{data}")
    
    matrix = generate_qr_matrix(data)
    print(f"矩阵大小：{len(matrix)}x{len(matrix)}")
    
    # ASCII 预览
    print("\nASCII 预览:")
    print(render_qr_ascii(matrix))


def example_website_qr():
    """示例 2: 网站 QR 码"""
    print_section("示例 2: 网站 QR 码")
    
    url = encode_url("https://github.com")
    print(f"编码 URL: {url}")
    
    matrix = generate_qr_matrix(url)
    
    # 保存为图片
    temp_dir = tempfile.mkdtemp()
    filepath = os.path.join(temp_dir, "github_qr.png")
    save_qr_image(matrix, filepath, box_size=15, border=4)
    print(f"已保存：{filepath} ({os.path.getsize(filepath)} 字节)")
    
    # 获取信息
    info = get_qr_info(url)
    print(f"\nQR 码信息:")
    print(f"  版本：{info['recommended_version']}")
    print(f"  容量剩余：{info['capacity_remaining']} 字节")


def example_wifi_qr():
    """示例 3: WiFi 连接码"""
    print_section("示例 3: WiFi 连接码")
    
    wifi = encode_wifi(
        ssid="Office-Guest",
        password="Welcome2026",
        encryption="WPA",
        hidden=False
    )
    
    print("WiFi 编码:")
    print(wifi)
    
    matrix = generate_qr_matrix(wifi)
    print("\n手机扫描此 QR 码即可自动连接 WiFi:")
    print(render_qr_emoji(matrix))


def example_vcard():
    """示例 4: 电子名片"""
    print_section("示例 4: 电子名片")
    
    vcard = encode_vcard(
        name="李明",
        phone="13800138000",
        email="liming@example.com",
        org="某某科技有限公司",
        title="技术总监"
    )
    
    print("vCard 内容:")
    print(vcard)
    
    matrix = generate_qr_matrix(vcard)
    
    temp_dir = tempfile.mkdtemp()
    filepath = os.path.join(temp_dir, "business_card.png")
    save_qr_image(matrix, filepath, fill_color='#1a1a1a', back_color='#f5f5f5')
    print(f"\n已保存名片 QR 码：{filepath}")


def example_email_sms():
    """示例 5: 邮件和短信"""
    print_section("示例 5: 邮件和短信")
    
    # 邮件
    mail = encode_email(
        to="support@example.com",
        subject="产品咨询",
        body="您好，我想了解..."
    )
    print(f"邮件链接：{mail[:60]}...")
    
    # 短信
    sms = encode_sms("10086", "CXLL")
    print(f"短信链接：{sms}")
    
    # 生成 QR 码
    mail_matrix = generate_qr_matrix(mail)
    sms_matrix = generate_qr_matrix(sms)
    
    print("\n邮件 QR 码 (ASCII):")
    print(render_qr_ascii(mail_matrix)[:500] + "...")


def example_html_embed():
    """示例 6: HTML 嵌入"""
    print_section("示例 6: HTML 嵌入 (Data URL)")
    
    data_url = generate_qr_data_url(
        "https://example.com",
        box_size=8,
        fill_color='#0066cc',
        back_color='white'
    )
    
    html = f'''
<!DOCTYPE html>
<html>
<head><title>QR Code Example</title></head>
<body>
  <h1>扫描二维码访问</h1>
  <img src="{data_url}" alt="QR Code" width="200" height="200">
  <p>或直接访问：https://example.com</p>
</body>
</html>
'''
    print("HTML 代码 (部分):")
    print(html[:400] + "...")


def example_batch_generation():
    """示例 7: 批量生成"""
    print_section("示例 7: 批量生成")
    
    # 示例产品列表
    products = [
        ("产品 A", "https://shop.com/product/A001"),
        ("产品 B", "https://shop.com/product/B002"),
        ("产品 C", "https://shop.com/product/C003"),
    ]
    
    temp_dir = tempfile.mkdtemp()
    
    # 批量生成
    urls = [url for _, url in products]
    files = generate_qr_batch(
        urls,
        temp_dir,
        prefix="product",
        box_size=10
    )
    
    print(f"批量生成 {len(files)} 个 QR 码:")
    for i, (name, url) in enumerate(products):
        print(f"  {i+1}. {name}: {os.path.basename(files[i])}")


def example_validation():
    """示例 8: 数据验证"""
    print_section("示例 8: 数据验证")
    
    test_cases = [
        ("https://example.com", "url", True),
        ("not-a-url", "url", False),
        (encode_vcard("Test", "123"), "vcard", True),
        (encode_wifi("SSID", "pass"), "wifi", True),
        ("", "text", False),
    ]
    
    print("数据验证测试:")
    for data, dtype, expected in test_cases:
        result = validate_qr_data(data, dtype)
        status = "✓" if result == expected else "✗"
        preview = data[:30] + "..." if len(data) > 30 else data
        print(f"  {status} '{preview}' ({dtype}): {result}")


def example_statistics():
    """示例 9: 矩阵统计"""
    print_section("示例 9: 矩阵统计")
    
    test_data = [
        "短文本",
        "中等长度的文本内容用于测试",
        "This is a longer text string to test how the QR code matrix statistics work with different data lengths and character counts.",
    ]
    
    print("不同数据长度的矩阵统计:\n")
    print(f"{'数据':<20} {'版本':>6} {'大小':>8} {'深色比例':>10}")
    print("-" * 50)
    
    for data in test_data:
        matrix = generate_qr_matrix(data)
        stats = get_matrix_stats(matrix)
        info = get_qr_info(data)
        
        preview = data[:17] + "..." if len(data) > 20 else data
        print(f"{preview:<20} {info['recommended_version']:>6} {stats['size']:>7}x{stats['size']} {stats['dark_ratio']:>9.2%}")


def example_custom_colors():
    """示例 10: 自定义颜色"""
    print_section("示例 10: 自定义颜色")
    
    data = "Colorful QR Code"
    matrix = generate_qr_matrix(data)
    
    temp_dir = tempfile.mkdtemp()
    
    colors = [
        ('black', 'white', '经典黑白'),
        ('red', 'white', '红色主题'),
        ('blue', 'yellow', '蓝黄对比'),
        ('#00aa00', '#f0f0f0', '绿色系'),
        ('#663399', '#ffffff', '紫色系'),
    ]
    
    print("生成不同颜色的 QR 码:")
    for fill, back, name in colors:
        filepath = os.path.join(temp_dir, f"qr_{name.replace(' ', '_')}.png")
        save_qr_image(matrix, filepath, fill_color=fill, back_color=back)
        print(f"  ✓ {name}: {filepath}")


def example_error_correction():
    """示例 11: 纠错级别对比"""
    print_section("示例 11: 纠错级别对比")
    
    data = "Error Correction Test"
    
    print(f"数据：{data}\n")
    print(f"{'级别':>6} {'恢复能力':>10} {'矩阵大小':>10}")
    print("-" * 30)
    
    levels = [
        ('L', '7%'),
        ('M', '15%'),
        ('Q', '25%'),
        ('H', '30%'),
    ]
    
    for level, recovery in levels:
        matrix = generate_qr_matrix(data, error_correction=level)
        info = get_qr_info(data)
        print(f"{level:>6} {recovery:>10} {len(matrix):>9}x{len(matrix)}")


def main():
    """运行所有示例"""
    print("\n" + "=" * 60)
    print("  QR Code Utilities - 使用示例")
    print("  AllToolkit Python 工具库")
    print("=" * 60)
    
    examples = [
        example_basic_usage,
        example_website_qr,
        example_wifi_qr,
        example_vcard,
        example_email_sms,
        example_html_embed,
        example_batch_generation,
        example_validation,
        example_statistics,
        example_custom_colors,
        example_error_correction,
    ]
    
    for example in examples:
        try:
            example()
        except Exception as e:
            print(f"\n❌ 示例 '{example.__name__}' 出错：{e}")
            import traceback
            traceback.print_exc()
    
    print("\n" + "=" * 60)
    print("  所有示例运行完成！")
    print("=" * 60 + "\n")


if __name__ == '__main__':
    main()
