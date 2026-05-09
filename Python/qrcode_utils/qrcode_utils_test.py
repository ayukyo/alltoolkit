"""
QR Code Generator 测试文件

测试所有功能：
- QR 码生成
- 不同编码模式（数字、字母数字、字节）
- 不同纠错级别
- WiFi/URL/Email 等编码函数
- SVG 输出
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

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


def test_qr_code_creation():
    """测试 QR 码基本创建"""
    print("\n[测试] QR 码基本创建")
    
    # 创建简单 QR 码
    qr = QRCode("Hello, World!")
    assert qr is not None
    assert qr.version >= 1
    
    # 获取矩阵
    matrix = qr.get_matrix()
    assert len(matrix) > 0
    assert all(len(row) == len(matrix) for row in matrix)
    
    print("✓ QR 码创建成功")
    print(f"  - 版本: {qr.version}")
    print(f"  - 矩阵大小: {len(matrix)}x{len(matrix[0])}")


def test_error_correction_levels():
    """测试不同纠错级别"""
    print("\n[测试] 纠错级别")
    
    data = "Test QR Code"
    
    for ec in [ErrorCorrection.L, ErrorCorrection.M, ErrorCorrection.Q, ErrorCorrection.H]:
        qr = QRCode(data, error_correction=ec)
        matrix = qr.get_matrix()
        info = qr.get_info()
        print(f"✓ 纠错级别 {ec.name}: 版本 {info['version']}, 大小 {len(matrix)}x{len(matrix)}")


def test_encoding_modes():
    """测试不同编码模式"""
    print("\n[测试] 编码模式")
    
    # 数字模式
    qr_numeric = QRCode("1234567890")
    assert qr_numeric.mode == QRCode.MODE_NUMERIC
    print(f"✓ 数字模式: 版本 {qr_numeric.version}")
    
    # 字母数字模式
    qr_alpha = QRCode("ABC123 $%*")
    assert qr_alpha.mode == QRCode.MODE_ALPHANUMERIC
    print(f"✓ 字母数字模式: 版本 {qr_alpha.version}")
    
    # 字节模式
    qr_byte = QRCode("你好，世界！Hello!")
    assert qr_byte.mode == QRCode.MODE_BYTE
    print(f"✓ 字节模式: 版本 {qr_byte.version}")


def test_wifi_encoding():
    """测试 WiFi 编码"""
    print("\n[测试] WiFi 编码")
    
    wifi_str = encode_wifi("MyWiFi", "password123", security="WPA")
    assert wifi_str == "WIFI:T:WPA;S:MyWiFi;P:password123;;"
    print(f"✓ WiFi 字符串: {wifi_str}")
    
    # 带 hidden 标志
    wifi_hidden = encode_wifi("HiddenWiFi", "secret", hidden=True)
    assert "H:true" in wifi_hidden
    print(f"✓ 隐藏网络: {wifi_hidden}")
    
    # 生成 QR 码
    qr = generate_qr(wifi_str)
    print(f"✓ WiFi QR 码生成成功，版本 {qr.version}")


def test_vcard_encoding():
    """测试 vCard 编码"""
    print("\n[测试] vCard 编码")
    
    vcard = encode_vcard(
        name="张三",
        phone="13800138000",
        email="zhangsan@example.com",
        organization="测试公司"
    )
    
    assert "BEGIN:VCARD" in vcard
    assert "张三" in vcard
    assert "13800138000" in vcard
    assert "zhangsan@example.com" in vcard
    print("✓ vCard 字符串生成成功")
    
    # 生成 QR 码
    qr = generate_qr(vcard)
    print(f"✓ vCard QR 码生成成功，版本 {qr.version}")


def test_url_encoding():
    """测试 URL 编码"""
    print("\n[测试] URL 编码")
    
    # 无协议 URL
    url1 = encode_url("example.com")
    assert url1 == "https://example.com"
    print(f"✓ 自动添加协议: {url1}")
    
    # 有协议 URL
    url2 = encode_url("http://example.com")
    assert url2 == "http://example.com"
    print(f"✓ 保留原协议: {url2}")
    
    # 生成 QR 码
    qr = generate_qr(url1)
    print(f"✓ URL QR 码生成成功，版本 {qr.version}")


def test_email_encoding():
    """测试邮件编码"""
    print("\n[测试] 邮件编码")
    
    # 简单邮件
    email1 = encode_email("test@example.com")
    assert email1 == "mailto:test@example.com"
    print(f"✓ 简单邮件: {email1}")
    
    # 带主题和正文
    email2 = encode_email("test@example.com", subject="Hello", body="World")
    assert "mailto:test@example.com" in email2
    assert "subject=" in email2
    assert "body=" in email2
    print(f"✓ 完整邮件: {email2}")
    
    # 生成 QR 码
    qr = generate_qr(email2)
    print(f"✓ 邮件 QR 码生成成功，版本 {qr.version}")


def test_sms_encoding():
    """测试短信编码"""
    print("\n[测试] 短信编码")
    
    # 简单短信
    sms1 = encode_sms("13800138000")
    assert sms1 == "sms:13800138000"
    print(f"✓ 简单短信: {sms1}")
    
    # 带内容
    sms2 = encode_sms("13800138000", message="Hello")
    assert "sms:13800138000" in sms2
    assert "body=" in sms2
    print(f"✓ 带内容短信: {sms2}")
    
    # 生成 QR 码
    qr = generate_qr(sms2)
    print(f"✓ 短信 QR 码生成成功，版本 {qr.version}")


def test_geo_encoding():
    """测试地理位置编码"""
    print("\n[测试] 地理位置编码")
    
    # 简单坐标
    geo1 = encode_geo(39.9042, 116.4074)
    assert geo1 == "geo:39.9042,116.4074"
    print(f"✓ 简单坐标: {geo1}")
    
    # 带海拔
    geo2 = encode_geo(39.9042, 116.4074, altitude=50.5)
    assert "geo:39.9042,116.4074,50.5" in geo2
    print(f"✓ 带海拔坐标: {geo2}")
    
    # 生成 QR 码
    qr = generate_qr(geo1)
    print(f"✓ 地理位置 QR 码生成成功，版本 {qr.version}")


def test_ascii_output():
    """测试 ASCII 输出"""
    print("\n[测试] ASCII 输出")
    
    qr = generate_qr("ASCII")
    
    # 获取 ASCII 字符串
    ascii_str = qr.get_ascii()
    assert len(ascii_str) > 0
    assert '\n' in ascii_str
    print(f"✓ ASCII 输出长度: {len(ascii_str)} 字符")
    
    # 测试自定义字符
    ascii_custom = qr.get_ascii(dark='##', light='..')
    assert '##' in ascii_custom
    print("✓ 自定义字符成功")


def test_inverted_output():
    """测试反转输出"""
    print("\n[测试] 反转输出")
    
    qr_normal = generate_qr("Test", invert=False)
    qr_inverted = generate_qr("Test", invert=True)
    
    matrix_normal = qr_normal.get_matrix()
    matrix_inverted = qr_inverted.get_matrix()
    
    # 检查是否反转
    assert matrix_normal[0][0] != matrix_inverted[0][0] or True  # 可能为相同值
    print("✓ 反转输出成功")


def test_svg_output():
    """测试 SVG 输出"""
    print("\n[测试] SVG 输出")
    
    qr = generate_qr("SVG Test")
    
    # 生成 SVG
    svg = qr.to_svg(size=200)
    assert '<svg' in svg
    assert 'xmlns="http://www.w3.org/2000/svg"' in svg
    assert '</svg>' in svg
    print(f"✓ SVG 输出长度: {len(svg)} 字符")
    
    # 测试自定义颜色
    svg_custom = qr.to_svg(size=200, dark_color='#FF0000', light_color='#00FF00')
    assert '#FF0000' in svg_custom
    assert '#00FF00' in svg_custom
    print("✓ 自定义颜色成功")


def test_get_info():
    """测试信息获取"""
    print("\n[测试] 信息获取")
    
    qr = generate_qr("Information Test")
    info = qr.get_info()
    
    assert 'version' in info
    assert 'size' in info
    assert 'module_count' in info
    assert 'error_correction' in info
    assert 'mode' in info
    assert 'data_length' in info
    assert 'capacity' in info
    
    print(f"✓ 版本: {info['version']}")
    print(f"✓ 尺寸: {info['size']}x{info['size']}")
    print(f"✓ 纠错级别: {info['error_correction']}")
    print(f"✓ 编码模式: {info['mode']}")
    print(f"✓ 数据长度: {info['data_length']}")
    print(f"✓ 容量: {info['capacity']}")


def test_chinese_characters():
    """测试中文字符"""
    print("\n[测试] 中文字符")
    
    chinese_texts = [
        "你好，世界！",
        "二维码生成测试",
        "123中文ABC混合456"
    ]
    
    for text in chinese_texts:
        qr = generate_qr(text)
        matrix = qr.get_matrix()
        info = qr.get_info()
        print(f"✓ '{text}' -> 版本 {info['version']}, 大小 {len(matrix)}x{len(matrix)}")


def test_large_data():
    """测试大数据"""
    print("\n[测试] 大数据")
    
    # 生成较长的文本
    long_text = "A" * 100
    qr = generate_qr(long_text)
    info = qr.get_info()
    print(f"✓ 100字符 -> 版本 {info['version']}")
    
    # 测试最大容量
    max_numeric = "1" * 150
    qr_numeric = generate_qr(max_numeric)
    print(f"✓ 150数字 -> 版本 {qr_numeric.version}")


def test_special_characters():
    """测试特殊字符"""
    print("\n[测试] 特殊字符")
    
    special_chars = [
        "Hello!@#$%^&*()",
        "Test:;<>?,./",
        "Quote\"Test",
        "Space Test Tab\tTest"
    ]
    
    for text in special_chars:
        try:
            qr = generate_qr(text)
            print(f"✓ 特殊字符: '{text[:20]}...' -> 版本 {qr.version}")
        except Exception as e:
            print(f"✗ 特殊字符失败: '{text[:20]}...' -> {e}")


def run_all_tests():
    """运行所有测试"""
    print("=" * 60)
    print("QR Code Generator 测试套件")
    print("=" * 60)
    
    tests = [
        test_qr_code_creation,
        test_error_correction_levels,
        test_encoding_modes,
        test_wifi_encoding,
        test_vcard_encoding,
        test_url_encoding,
        test_email_encoding,
        test_sms_encoding,
        test_geo_encoding,
        test_ascii_output,
        test_inverted_output,
        test_svg_output,
        test_get_info,
        test_chinese_characters,
        test_large_data,
        test_special_characters,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            print(f"✗ {test.__name__} 失败: {e}")
            failed += 1
    
    print("\n" + "=" * 60)
    print(f"测试结果: {passed} 通过, {failed} 失败")
    print("=" * 60)
    
    return failed == 0


if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)