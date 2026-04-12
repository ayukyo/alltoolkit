"""
QR Code Utilities Test Suite
二维码工具函数测试套件

覆盖场景:
- QR 码矩阵生成
- ASCII/Emoji 渲染
- PNG 图片生成
- 数据编码（URL/vCard/WiFi/Email/SMS）
- 数据验证
- 批量处理
- 边界情况和异常处理

Author: AllToolkit
Version: 1.0.0
"""

import os
import sys
import tempfile
import shutil
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from qr_utils import (
    QRCodeError,
    QRCodeDataError,
    QRCodeRenderError,
    QRMatrixGenerator,
    ERROR_CORRECTION_L,
    ERROR_CORRECTION_M,
    ERROR_CORRECTION_Q,
    ERROR_CORRECTION_H,
    generate_qr_matrix,
    render_qr_ascii,
    render_qr_emoji,
    save_qr_image,
    generate_qr_data_url,
    encode_url,
    encode_vcard,
    encode_wifi,
    encode_text,
    encode_email,
    encode_sms,
    get_qr_info,
    validate_qr_data,
    get_matrix_stats,
    generate_qr_batch,
    get_version,
    get_capabilities,
)


# ============================================================================
# 测试辅助函数
# ============================================================================

def print_test_header(test_name: str):
    """打印测试标题"""
    print(f"\n{'='*60}")
    print(f"测试：{test_name}")
    print('='*60)


def print_result(passed: bool, message: str = ''):
    """打印测试结果"""
    status = "✅ 通过" if passed else "❌ 失败"
    if message:
        print(f"  {status}: {message}")
    else:
        print(f"  {status}")
    return passed


# ============================================================================
# 测试用例
# ============================================================================

def test_version_and_capabilities():
    """测试版本和功能列表"""
    print_test_header("版本和功能列表")
    
    version = get_version()
    passed = print_result(version == "1.0.0", f"版本号：{version}")
    
    caps = get_capabilities()
    passed = passed and print_result(len(caps) > 0, f"功能数量：{len(caps)}")
    passed = passed and print_result("generate_qr_matrix" in caps, "包含核心功能")
    
    return passed


def test_qr_matrix_generator_init():
    """测试 QR 码生成器初始化"""
    print_test_header("QR 码生成器初始化")
    
    # 正常初始化
    try:
        gen = QRMatrixGenerator(version=1, error_correction=ERROR_CORRECTION_M)
        passed = print_result(True, "版本 1 初始化成功")
    except Exception as e:
        passed = print_result(False, f"初始化失败：{e}")
    
    # 测试不同版本
    for version in [1, 5, 10]:
        try:
            gen = QRMatrixGenerator(version=version)
            expected_size = version * 4 + 17
            passed = passed and print_result(gen.size == expected_size, 
                                            f"版本 {version} 矩阵大小：{gen.size}")
        except Exception as e:
            passed = passed and print_result(False, f"版本 {version} 失败：{e}")
    
    # 测试无效版本
    try:
        gen = QRMatrixGenerator(version=0)
        passed = print_result(False, "版本 0 应该抛出异常")
    except QRCodeDataError:
        passed = passed and print_result(True, "版本 0 正确抛出异常")
    
    try:
        gen = QRMatrixGenerator(version=11)
        passed = print_result(False, "版本 11 应该抛出异常")
    except QRCodeDataError:
        passed = passed and print_result(True, "版本 11 正确抛出异常")
    
    # 测试无效纠错级别
    try:
        gen = QRMatrixGenerator(error_correction='X')
        passed = print_result(False, "无效纠错级别应该抛出异常")
    except QRCodeDataError:
        passed = passed and print_result(True, "无效纠错级别正确抛出异常")
    
    return passed


def test_generate_qr_matrix_basic():
    """测试基本 QR 码矩阵生成"""
    print_test_header("基本 QR 码矩阵生成")
    
    test_cases = [
        ("Hello", 1),
        ("Hello, World!", 1),
        ("https://example.com", 2),
        ("这是一段中文测试数据", 2),
        ("A" * 100, 5),
    ]
    
    all_passed = True
    for data, expected_min_version in test_cases:
        try:
            matrix = generate_qr_matrix(data)
            
            # 检查矩阵大小
            size = len(matrix)
            expected_size = expected_min_version * 4 + 17
            
            is_square = all(len(row) == size for row in matrix)
            passed = print_result(is_square, f"'{data[:20]}...' 矩阵：{size}x{size} (方形：{is_square})")
            all_passed = all_passed and passed
            
        except Exception as e:
            all_passed = print_result(False, f"'{data[:20]}...' 生成失败：{e}")
    
    return all_passed


def test_generate_qr_matrix_error_correction():
    """测试不同纠错级别"""
    print_test_header("纠错级别测试")
    
    data = "Test data for error correction"
    all_passed = True
    
    for ec_level in [ERROR_CORRECTION_L, ERROR_CORRECTION_M, 
                     ERROR_CORRECTION_Q, ERROR_CORRECTION_H]:
        try:
            matrix = generate_qr_matrix(data, error_correction=ec_level)
            passed = print_result(len(matrix) > 0, f"纠错级别 {ec_level}: 矩阵大小 {len(matrix)}x{len(matrix)}")
            all_passed = all_passed and passed
        except Exception as e:
            all_passed = print_result(False, f"纠错级别 {ec_level} 失败：{e}")
    
    return all_passed


def test_generate_qr_matrix_empty():
    """测试空数据"""
    print_test_header("空数据处理")
    
    try:
        matrix = generate_qr_matrix("")
        passed = print_result(False, "空数据应该抛出异常")
    except QRCodeDataError:
        passed = print_result(True, "空数据正确抛出异常")
    except Exception as e:
        passed = print_result(False, f"抛出了错误类型的异常：{e}")
    
    return passed


def test_render_qr_ascii():
    """测试 ASCII 渲染"""
    print_test_header("ASCII 渲染")
    
    data = "Test"
    matrix = generate_qr_matrix(data)
    
    ascii_art = render_qr_ascii(matrix)
    
    # 检查基本属性
    lines = ascii_art.split('\n')
    passed = print_result(len(lines) == len(matrix), f"行数匹配：{len(lines)} == {len(matrix)}")
    passed = passed and print_result(all(len(line) == len(matrix) for line in lines), 
                                     "每行长度匹配矩阵大小")
    passed = passed and print_result('█' in ascii_art, "包含深色字符")
    passed = passed and print_result(' ' in ascii_art, "包含浅色字符")
    
    # 打印预览
    print("\nASCII 预览:")
    print(ascii_art[:500] + ("..." if len(ascii_art) > 500 else ""))
    
    return passed


def test_render_qr_emoji():
    """测试 Emoji 渲染"""
    print_test_header("Emoji 渲染")
    
    data = "Test"
    matrix = generate_qr_matrix(data)
    
    emoji_art = render_qr_emoji(matrix)
    
    lines = emoji_art.split('\n')
    passed = print_result(len(lines) == len(matrix), f"行数匹配：{len(lines)} == {len(matrix)}")
    passed = passed and print_result('🟥' in emoji_art, "包含红色方块")
    passed = passed and print_result('⬜' in emoji_art, "包含白色方块")
    
    # 打印预览（前几行）
    print("\nEmoji 预览 (前 5 行):")
    preview = '\n'.join(lines[:5])
    print(preview)
    
    return passed


def test_save_qr_image():
    """测试 PNG 图片保存"""
    print_test_header("PNG 图片保存")
    
    temp_dir = tempfile.mkdtemp()
    all_passed = True
    
    try:
        # 基本保存
        data = "https://example.com"
        matrix = generate_qr_matrix(data)
        filepath = os.path.join(temp_dir, "test_qr.png")
        
        result_path = save_qr_image(matrix, filepath)
        passed = print_result(os.path.exists(filepath), f"文件创建：{filepath}")
        all_passed = all_passed and passed
        
        # 检查文件大小
        file_size = os.path.getsize(filepath)
        passed = print_result(file_size > 100, f"文件大小：{file_size} 字节")
        all_passed = all_passed and passed
        
        # 检查 PNG 签名
        with open(filepath, 'rb') as f:
            signature = f.read(8)
        is_png = signature == b'\x89PNG\r\n\x1a\n'
        passed = print_result(is_png, "PNG 签名正确")
        all_passed = all_passed and passed
        
        # 测试不同颜色
        for fill_color in ['black', 'red', 'blue', '#FF0000']:
            color_path = os.path.join(temp_dir, f"test_{fill_color.replace('#', '')}.png")
            save_qr_image(matrix, color_path, fill_color=fill_color)
            passed = print_result(os.path.exists(color_path), f"颜色 {fill_color}: 文件创建成功")
            all_passed = all_passed and passed
        
        # 测试不同尺寸
        for box_size in [5, 10, 20]:
            size_path = os.path.join(temp_dir, f"test_box{box_size}.png")
            save_qr_image(matrix, size_path, box_size=box_size)
            passed = print_result(os.path.exists(size_path), f"尺寸 {box_size}: 文件创建成功")
            all_passed = all_passed and passed
        
    finally:
        shutil.rmtree(temp_dir)
    
    return all_passed


def test_generate_qr_data_url():
    """测试 Data URL 生成"""
    print_test_header("Data URL 生成")
    
    data = "https://example.com"
    
    try:
        data_url = generate_qr_data_url(data)
        
        passed = print_result(data_url.startswith("data:image/png;base64,"), 
                             "Data URL 格式正确")
        passed = passed and print_result(len(data_url) > 100, 
                                        f"Data URL 长度：{len(data_url)}")
        
        # 验证可以解码
        import base64
        base64_data = data_url.split(',')[1]
        decoded = base64.b64decode(base64_data)
        passed = passed and print_result(decoded[:8] == b'\x89PNG\r\n\x1a\n', 
                                        "Base64 解码后是有效 PNG")
        
    except Exception as e:
        passed = print_result(False, f"生成失败：{e}")
    
    return passed


def test_encode_url():
    """测试 URL 编码"""
    print_test_header("URL 编码")
    
    test_cases = [
        ("https://example.com", "https://example.com"),
        ("example.com", "https://example.com"),
        ("http://test.org", "http://test.org"),
        ("www.site.net", "https://www.site.net"),
    ]
    
    all_passed = True
    for input_url, expected in test_cases:
        result = encode_url(input_url)
        passed = print_result(result == expected, 
                             f"'{input_url}' -> '{result}'")
        all_passed = all_passed and passed
    
    return all_passed


def test_encode_vcard():
    """测试 vCard 编码"""
    print_test_header("vCard 编码")
    
    vcard = encode_vcard(
        name="张三",
        phone="13800138000",
        email="zhangsan@example.com",
        org="测试公司",
        title="工程师"
    )
    
    passed = print_result(vcard.startswith("BEGIN:VCARD"), "以 BEGIN:VCARD 开头")
    passed = passed and print_result(vcard.endswith("END:VCARD"), "以 END:VCARD 结尾")
    passed = passed and print_result("N:张三" in vcard, "包含姓名")
    passed = passed and print_result("TEL:13800138000" in vcard, "包含电话")
    passed = passed and print_result("EMAIL:zhangsan@example.com" in vcard, "包含邮箱")
    passed = passed and print_result("ORG:测试公司" in vcard, "包含组织")
    passed = passed and print_result("TITLE:工程师" in vcard, "包含职位")
    
    # 打印预览
    print("\nvCard 预览:")
    print(vcard)
    
    return passed


def test_encode_wifi():
    """测试 WiFi 编码"""
    print_test_header("WiFi 编码")
    
    wifi = encode_wifi(
        ssid="MyWiFi",
        password="secret123",
        encryption="WPA",
        hidden=False
    )
    
    passed = print_result(wifi.startswith("WIFI:"), "以 WIFI: 开头")
    passed = passed and print_result("T:WPA" in wifi, "包含加密类型")
    passed = passed and print_result("S:MyWiFi" in wifi, "包含 SSID")
    passed = passed and print_result("P:secret123" in wifi, "包含密码")
    passed = passed and print_result("H:false" in wifi, "包含隐藏标志")
    
    # 测试隐藏网络
    wifi_hidden = encode_wifi("HiddenWiFi", "pass", hidden=True)
    passed = passed and print_result("H:true" in wifi_hidden, "隐藏网络标志正确")
    
    print("\nWiFi 编码预览:")
    print(wifi)
    
    return passed


def test_encode_email():
    """测试 Email 编码"""
    print_test_header("Email 编码")
    
    # 简单邮件
    email1 = encode_email("user@example.com")
    passed = print_result(email1 == "mailto:user@example.com", 
                         f"简单邮件：{email1}")
    
    # 带主题和正文
    email2 = encode_email("user@example.com", "Hello", "Body text")
    passed = passed and print_result(email2.startswith("mailto:user@example.com?"), 
                                    f"完整邮件：{email2[:50]}...")
    passed = passed and print_result("subject=" in email2, "包含主题参数")
    passed = passed and print_result("body=" in email2, "包含正文参数")
    
    return passed


def test_encode_sms():
    """测试 SMS 编码"""
    print_test_header("SMS 编码")
    
    # 简单短信
    sms1 = encode_sms("13800138000")
    passed = print_result(sms1 == "sms:13800138000", f"简单短信：{sms1}")
    
    # 带内容
    sms2 = encode_sms("13800138000", "Hello!")
    passed = passed and print_result(sms2.startswith("sms:13800138000?"), 
                                    f"完整短信：{sms2[:40]}...")
    passed = passed and print_result("body=" in sms2, "包含内容参数")
    
    return passed


def test_encode_text():
    """测试文本编码"""
    print_test_header("文本编码")
    
    test_texts = [
        "Hello, World!",
        "这是一段中文",
        "Special chars: @#$%^&*()",
        "Mixed: 中文 + English + 123",
    ]
    
    all_passed = True
    for text in test_texts:
        result = encode_text(text)
        passed = print_result(result == text, f"'{text[:20]}...' 编码正确")
        all_passed = all_passed and passed
    
    return all_passed


def test_get_qr_info():
    """测试 QR 码信息获取"""
    print_test_header("QR 码信息获取")
    
    data = "https://example.com/page?id=123"
    info = get_qr_info(data)
    
    passed = print_result('data_length' in info, "包含数据长度")
    passed = passed and print_result('recommended_version' in info, "包含推荐版本")
    passed = passed and print_result('matrix_size' in info, "包含矩阵大小")
    passed = passed and print_result('capacity_remaining' in info, "包含剩余容量")
    passed = passed and print_result(info['data_length'] > 0, f"数据长度：{info['data_length']}")
    passed = passed and print_result(info['recommended_version'] >= 1, 
                                    f"推荐版本：{info['recommended_version']}")
    
    print("\nQR 码信息:")
    for key, value in info.items():
        print(f"  {key}: {value}")
    
    return passed


def test_validate_qr_data():
    """测试数据验证"""
    print_test_header("数据验证")
    
    # URL 验证
    passed = print_result(validate_qr_data("https://example.com", "url") == True, 
                         "有效 URL 验证通过")
    passed = passed and print_result(validate_qr_data("not-a-url", "url") == False, 
                                    "无效 URL 验证失败")
    
    # vCard 验证
    vcard = encode_vcard("Test", "123")
    passed = passed and print_result(validate_qr_data(vcard, "vcard") == True, 
                                    "有效 vCard 验证通过")
    passed = passed and print_result(validate_qr_data("not-vcard", "vcard") == False, 
                                    "无效 vCard 验证失败")
    
    # WiFi 验证
    wifi = encode_wifi("SSID", "pass")
    passed = passed and print_result(validate_qr_data(wifi, "wifi") == True, 
                                    "有效 WiFi 验证通过")
    
    # Email 验证
    email = encode_email("test@example.com")
    passed = passed and print_result(validate_qr_data(email, "email") == True, 
                                    "有效 Email 验证通过")
    
    # SMS 验证
    sms = encode_sms("123456")
    passed = passed and print_result(validate_qr_data(sms, "sms") == True, 
                                    "有效 SMS 验证通过")
    
    # 自动模式
    passed = passed and print_result(validate_qr_data("any text", "auto") == True, 
                                    "自动模式接受任意文本")
    
    # 空数据
    passed = passed and print_result(validate_qr_data("", "text") == False, 
                                    "空数据验证失败")
    
    return passed


def test_get_matrix_stats():
    """测试矩阵统计"""
    print_test_header("矩阵统计")
    
    data = "Test data for statistics"
    matrix = generate_qr_matrix(data)
    stats = get_matrix_stats(matrix)
    
    passed = print_result('size' in stats, "包含尺寸")
    passed = passed and print_result('total_modules' in stats, "包含总模块数")
    passed = passed and print_result('dark_modules' in stats, "包含深色模块数")
    passed = passed and print_result('light_modules' in stats, "包含浅色模块数")
    passed = passed and print_result('dark_ratio' in stats, "包含深色比例")
    
    # 验证计算
    expected_total = len(matrix) * len(matrix[0])
    passed = passed and print_result(stats['total_modules'] == expected_total, 
                                    f"总模块数：{stats['total_modules']}")
    passed = passed and print_result(0 <= stats['dark_ratio'] <= 1, 
                                    f"深色比例：{stats['dark_ratio']:.2%}")
    
    print("\n矩阵统计:")
    for key, value in stats.items():
        if isinstance(value, float):
            print(f"  {key}: {value:.4f}")
        else:
            print(f"  {key}: {value}")
    
    return passed


def test_generate_qr_batch():
    """测试批量生成"""
    print_test_header("批量生成")
    
    temp_dir = tempfile.mkdtemp()
    
    try:
        data_list = [
            "https://site1.com",
            "https://site2.com",
            "https://site3.com",
        ]
        
        files = generate_qr_batch(data_list, temp_dir, prefix="batch")
        
        passed = print_result(len(files) == 3, f"生成文件数：{len(files)}")
        
        for i, filepath in enumerate(files):
            exists = os.path.exists(filepath)
            expected_name = f"batch_{i:04d}.png"
            passed = passed and print_result(exists, 
                                            f"文件 {i}: {expected_name} 存在")
        
        # 测试自定义前缀
        files2 = generate_qr_batch(data_list, temp_dir, prefix="custom")
        passed = passed and print_result(len(files2) == 3, "自定义前缀生成成功")
        passed = passed and print_result("custom_0000.png" in files2[0], 
                                        "自定义前缀正确")
        
    finally:
        shutil.rmtree(temp_dir)
    
    return passed


def test_matrix_generator_methods():
    """测试矩阵生成器内部方法"""
    print_test_header("矩阵生成器内部方法")
    
    gen = QRMatrixGenerator(version=3)
    
    # 测试 generate 返回矩阵
    matrix = gen.generate("Test")
    passed = print_result(isinstance(matrix, list), "返回类型为列表")
    passed = passed and print_result(len(matrix) == 29, f"版本 3 矩阵大小：{len(matrix)}")
    passed = passed and print_result(all(isinstance(row, list) for row in matrix), 
                                    "每行都是列表")
    
    return passed


def test_edge_cases():
    """测试边界情况"""
    print_test_header("边界情况")
    
    all_passed = True
    
    # 超长数据
    try:
        long_data = "A" * 500
        matrix = generate_qr_matrix(long_data)
        passed = print_result(len(matrix) > 0, "超长数据处理成功")
    except Exception as e:
        passed = print_result(False, f"超长数据处理失败：{e}")
    all_passed = all_passed and passed
    
    # 特殊字符
    special_chars = "!@#$%^&*()_+-=[]{}|;':\",./<>?"
    try:
        matrix = generate_qr_matrix(special_chars)
        passed = print_result(len(matrix) > 0, "特殊字符处理成功")
    except Exception as e:
        passed = print_result(False, f"特殊字符处理失败：{e}")
    all_passed = all_passed and passed
    
    # Unicode/Emoji
    emoji_data = "Hello 🌍 世界 🚀"
    try:
        matrix = generate_qr_matrix(emoji_data)
        passed = print_result(len(matrix) > 0, "Unicode/Emoji 处理成功")
    except Exception as e:
        passed = print_result(False, f"Unicode/Emoji 处理失败：{e}")
    all_passed = all_passed and passed
    
    # 换行符
    multiline = "Line 1\nLine 2\nLine 3"
    try:
        matrix = generate_qr_matrix(multiline)
        passed = print_result(len(matrix) > 0, "多行文本处理成功")
    except Exception as e:
        passed = print_result(False, f"多行文本处理失败：{e}")
    all_passed = all_passed and passed
    
    return all_passed


# ============================================================================
# 主测试运行器
# ============================================================================

def run_all_tests():
    """运行所有测试"""
    print("\n" + "="*60)
    print("QR Code Utilities - 完整测试套件")
    print("="*60)
    
    tests = [
        ("版本和功能列表", test_version_and_capabilities),
        ("QR 码生成器初始化", test_qr_matrix_generator_init),
        ("基本 QR 码矩阵生成", test_generate_qr_matrix_basic),
        ("纠错级别测试", test_generate_qr_matrix_error_correction),
        ("空数据处理", test_generate_qr_matrix_empty),
        ("ASCII 渲染", test_render_qr_ascii),
        ("Emoji 渲染", test_render_qr_emoji),
        ("PNG 图片保存", test_save_qr_image),
        ("Data URL 生成", test_generate_qr_data_url),
        ("URL 编码", test_encode_url),
        ("vCard 编码", test_encode_vcard),
        ("WiFi 编码", test_encode_wifi),
        ("Email 编码", test_encode_email),
        ("SMS 编码", test_encode_sms),
        ("文本编码", test_encode_text),
        ("QR 码信息获取", test_get_qr_info),
        ("数据验证", test_validate_qr_data),
        ("矩阵统计", test_get_matrix_stats),
        ("批量生成", test_generate_qr_batch),
        ("矩阵生成器方法", test_matrix_generator_methods),
        ("边界情况", test_edge_cases),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n❌ 测试 '{name}' 异常：{e}")
            import traceback
            traceback.print_exc()
            results.append((name, False))
    
    # 打印总结
    print("\n" + "="*60)
    print("测试总结")
    print("="*60)
    
    passed_count = sum(1 for _, result in results if result)
    total_count = len(results)
    
    for name, result in results:
        status = "✅" if result else "❌"
        print(f"  {status} {name}")
    
    print(f"\n总计：{passed_count}/{total_count} 通过")
    print(f"通过率：{passed_count/total_count*100:.1f}%")
    
    return passed_count == total_count


if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)
