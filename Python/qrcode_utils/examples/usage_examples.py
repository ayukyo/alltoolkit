"""
QR Code Generator 使用示例

展示如何使用 qrcode_utils 生成各种类型的 QR 码：
- 基本文本 QR 码
- WiFi 配置 QR 码
- 名片 (vCard) QR 码
- URL QR 码
- 邮件 QR 码
- 短信 QR 码
- 地理位置 QR 码
- SVG 输出
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    QRCode,
    ErrorCorrection,
    generate_qr,
    encode_wifi,
    encode_vcard,
    encode_url,
    encode_email,
    encode_sms,
    encode_geo
)


def example_basic_text():
    """示例 1: 基本文本 QR 码"""
    print("\n" + "=" * 60)
    print("示例 1: 基本文本 QR 码")
    print("=" * 60)
    
    text = "Hello, QR Code!"
    print(f"编码文本: {text}")
    
    # 生成 QR 码
    qr = generate_qr(text)
    
    # 获取信息
    info = qr.get_info()
    print(f"版本: {info['version']}")
    print(f"尺寸: {info['size']}x{info['size']} 模块")
    print(f"纠错级别: {info['error_correction']}")
    print(f"编码模式: {info['mode']}")
    
    # 打印 ASCII QR 码
    print("\nQR 码:")
    qr.print_ascii()
    
    print("\n提示: 使用手机扫码应用扫描上面的 QR 码")


def example_error_correction():
    """示例 2: 不同纠错级别"""
    print("\n" + "=" * 60)
    print("示例 2: 不同纠错级别")
    print("=" * 60)
    
    text = "Error Correction Test"
    
    print(f"编码文本: {text}\n")
    
    for ec_name in ['L', 'M', 'Q', 'H']:
        ec = getattr(ErrorCorrection, ec_name)
        qr = QRCode(text, error_correction=ec)
        info = qr.get_info()
        
        print(f"纠错级别 {ec_name}:")
        print(f"  - 版本: {info['version']}")
        print(f"  - 尺寸: {info['size']}x{info['size']}")
        print(f"  - 容量: {info['capacity']} 字符")
        print(f"  - 纠错能力: ", end="")
        if ec_name == 'L':
            print("7% (可容忍少量污损)")
        elif ec_name == 'M':
            print("15% (推荐，平衡容量和纠错)")
        elif ec_name == 'Q':
            print("25% (适合可能受损的场景)")
        else:
            print("30% (最大纠错，容量最小)")
        print()


def example_wifi():
    """示例 3: WiFi 配置 QR 码"""
    print("\n" + "=" * 60)
    print("示例 3: WiFi 配置 QR 码")
    print("=" * 60)
    
    # 基本配置
    ssid = "MyHomeWiFi"
    password = "SecurePassword123"
    
    print(f"WiFi 名称: {ssid}")
    print(f"密码: {password}")
    
    # 生成 WiFi 字符串
    wifi_str = encode_wifi(ssid, password, security="WPA")
    print(f"\n编码字符串: {wifi_str}")
    
    # 生成 QR 码
    qr = generate_qr(wifi_str)
    print(f"\nQR 码 (版本 {qr.version}):")
    qr.print_ascii()
    
    # 隐藏网络示例
    print("\n隐藏网络示例:")
    wifi_hidden = encode_wifi("HiddenNetwork", "SecretPass", hidden=True)
    print(f"编码字符串: {wifi_hidden}")


def example_vcard():
    """示例 4: 名片 QR 码"""
    print("\n" + "=" * 60)
    print("示例 4: 名片 (vCard) QR 码")
    print("=" * 60)
    
    # 完整名片
    vcard = encode_vcard(
        name="张三",
        phone="138-0013-8000",
        email="zhangsan@example.com",
        organization="创新科技有限公司",
        url="https://example.com",
        address="北京市朝阳区xxx路xxx号"
    )
    
    print("名片信息:")
    print("-" * 40)
    for line in vcard.split('\n'):
        print(f"  {line}")
    print("-" * 40)
    
    # 生成 QR 码
    qr = generate_qr(vcard, error_correction='M')
    print(f"\nQR 码 (版本 {qr.version}):")
    qr.print_ascii()
    
    print("\n提示: 扫描后可直接添加到通讯录")


def example_url():
    """示例 5: URL QR 码"""
    print("\n" + "=" * 60)
    print("示例 5: URL QR 码")
    print("=" * 60)
    
    urls = [
        "example.com",
        "https://github.com",
        "http://localhost:8080"
    ]
    
    for url in urls:
        encoded = encode_url(url)
        print(f"原始: {url}")
        print(f"编码: {encoded}")
        
        qr = generate_qr(encoded)
        print(f"版本: {qr.version}")
        print()


def example_email():
    """示例 6: 邮件 QR 码"""
    print("\n" + "=" * 60)
    print("示例 6: 邮件 QR 码")
    print("=" * 60)
    
    # 简单邮件地址
    email_simple = encode_email("contact@example.com")
    print(f"简单邮件: {email_simple}")
    qr = generate_qr(email_simple)
    print(f"QR 码版本: {qr.version}\n")
    
    # 完整邮件
    email_full = encode_email(
        "support@example.com",
        subject="技术支持请求",
        body="您好，我需要技术支持。请回复此邮件。"
    )
    print(f"完整邮件: {email_full[:60]}...")
    qr = generate_qr(email_full)
    print(f"QR 码版本: {qr.version}")
    
    print("\n提示: 扫描后会打开邮件客户端并自动填写")


def example_sms():
    """示例 7: 短信 QR 码"""
    print("\n" + "=" * 60)
    print("示例 7: 短信 QR 码")
    print("=" * 60)
    
    # 简单电话号码
    sms_simple = encode_sms("13800138000")
    print(f"简单号码: {sms_simple}")
    qr = generate_qr(sms_simple)
    print(f"QR 码版本: {qr.version}\n")
    
    # 带内容的短信
    sms_full = encode_sms("10086", message="CX YE")  # 查询余额
    print(f"带内容短信: {sms_full}")
    qr = generate_qr(sms_full)
    print(f"QR 码版本: {qr.version}")


def example_geo():
    """示例 8: 地理位置 QR 码"""
    print("\n" + "=" * 60)
    print("示例 8: 地理位置 QR 码")
    print("=" * 60)
    
    locations = [
        ("北京天安门", 39.9042, 116.4074),
        ("上海东方明珠", 31.2397, 121.4998),
        ("广州塔", 23.1067, 113.3245),
    ]
    
    for name, lat, lng in locations:
        geo = encode_geo(lat, lng)
        print(f"{name}: {geo}")
        
        qr = generate_qr(geo)
        print(f"  QR 码版本: {qr.version}\n")


def example_svg_output():
    """示例 9: SVG 输出"""
    print("\n" + "=" * 60)
    print("示例 9: SVG 输出")
    print("=" * 60)
    
    # 生成 QR 码
    qr = generate_qr("https://example.com")
    
    # 生成 SVG
    svg_content = qr.to_svg(size=300)
    print(f"SVG 内容长度: {len(svg_content)} 字符")
    print(f"SVG 预览 (前 200 字符):")
    print(svg_content[:200] + "...")
    
    # 自定义颜色
    svg_colored = qr.to_svg(
        size=300,
        dark_color='#2196F3',  # 蓝色
        light_color='#FFFFFF'   # 白色背景
    )
    print(f"\n自定义颜色 SVG 长度: {len(svg_colored)} 字符")
    
    # 保存到文件
    output_file = "/tmp/qrcode_example.svg"
    qr.save_svg(output_file, size=400)
    print(f"\nSVG 已保存到: {output_file}")


def example_ascii_styles():
    """示例 10: ASCII 风格"""
    print("\n" + "=" * 60)
    print("示例 10: ASCII 风格")
    print("=" * 60)
    
    text = "Style"
    qr = generate_qr(text)
    
    # 默认样式
    print("默认样式 (██和空格):")
    qr.print_ascii()
    
    # 方块样式
    print("\n方块样式 (▓░):")
    print(qr.get_ascii(dark='▓', light='░'))
    
    # 点阵样式
    print("\n点阵样式 (●○):")
    print(qr.get_ascii(dark='●', light='○'))
    
    # 反转样式
    qr_inverted = generate_qr(text, invert=True)
    print("\n反转样式:")
    qr_inverted.print_ascii()


def example_chinese():
    """示例 11: 中文 QR 码"""
    print("\n" + "=" * 60)
    print("示例 11: 中文 QR 码")
    print("=" * 60)
    
    chinese_texts = [
        "你好，世界！",
        "微信公众号：测试账号",
        "支付金额：¥99.99",
        "这是一段中文测试文本，用于验证 QR 码对中文字符的编码支持。",
    ]
    
    for text in chinese_texts:
        print(f"\n文本: {text}")
        qr = generate_qr(text)
        info = qr.get_info()
        print(f"版本: {info['version']}, 模式: {info['mode']}")
        qr.print_ascii()


def example_large_data():
    """示例 12: 大数据量"""
    print("\n" + "=" * 60)
    print("示例 12: 大数据量 QR 码")
    print("=" * 60)
    
    # 数字数据
    numeric_data = "1234567890" * 10
    print(f"数字数据 (100 位):")
    qr = generate_qr(numeric_data)
    print(f"  版本: {qr.version}, 模式: {qr.get_info()['mode']}")
    
    # 字母数字数据
    alpha_data = "ABC123" * 15
    print(f"\n字母数字数据 (90 字符):")
    qr = generate_qr(alpha_data)
    print(f"  版本: {qr.version}, 模式: {qr.get_info()['mode']}")
    
    # 字节/中文数据
    byte_data = "测试" * 30
    print(f"\n中文数据 (60 字符):")
    qr = generate_qr(byte_data)
    print(f"  版本: {qr.version}, 模式: {qr.get_info()['mode']}")


def example_real_world():
    """示例 13: 实际应用场景"""
    print("\n" + "=" * 60)
    print("示例 13: 实际应用场景")
    print("=" * 60)
    
    # 场景 1: 支付码
    print("场景 1: 支付码 (模拟)")
    payment_code = "wxp://f2f0xxxxxxxxxxxx"
    qr = generate_qr(payment_code)
    print(f"  支付码内容: {payment_code}")
    print(f"  QR 版本: {qr.version}\n")
    
    # 场景 2: 活动门票
    print("场景 2: 活动门票")
    ticket = "EVENT2024-001234-A1B2C3"
    qr = generate_qr(ticket, error_correction='H')  # 高纠错
    print(f"  票号: {ticket}")
    print(f"  QR 版本: {qr.version} (高纠错以确保可扫描)\n")
    
    # 场景 3: 产品追溯
    print("场景 3: 产品追溯")
    trace_url = encode_url("https://trace.example.com/product/12345")
    qr = generate_qr(trace_url)
    print(f"  追溯链接: {trace_url}")
    print(f"  QR 版本: {qr.version}")


def main():
    """运行所有示例"""
    print("=" * 60)
    print("QR Code Generator 使用示例")
    print("=" * 60)
    
    examples = [
        ("基本文本 QR 码", example_basic_text),
        ("不同纠错级别", example_error_correction),
        ("WiFi 配置 QR 码", example_wifi),
        ("名片 QR 码", example_vcard),
        ("URL QR 码", example_url),
        ("邮件 QR 码", example_email),
        ("短信 QR 码", example_sms),
        ("地理位置 QR 码", example_geo),
        ("SVG 输出", example_svg_output),
        ("ASCII 风格", example_ascii_styles),
        ("中文 QR 码", example_chinese),
        ("大数据量", example_large_data),
        ("实际应用场景", example_real_world),
    ]
    
    print("\n可用示例:")
    for i, (name, _) in enumerate(examples, 1):
        print(f"  {i}. {name}")
    
    print("\n运行所有示例...\n")
    
    for name, example_func in examples:
        try:
            example_func()
        except Exception as e:
            print(f"\n示例 '{name}' 出错: {e}")
    
    print("\n" + "=" * 60)
    print("示例演示完成!")
    print("=" * 60)


if __name__ == '__main__':
    main()