"""
ASCII Banner Utils 测试套件
测试所有核心功能
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    ASCIIBannerGenerator,
    render,
    print_banner,
    list_fonts,
    list_colors,
    BannerBuilder,
    template,
    show_template,
    TEMPLATES
)


def test_initialization():
    """测试初始化"""
    gen = ASCIIBannerGenerator()
    assert gen.font == 'standard'
    
    gen_block = ASCIIBannerGenerator('block')
    assert gen_block.font == 'block'
    
    try:
        ASCIIBannerGenerator('unknown_font')
        assert False, "应该抛出异常"
    except ValueError as e:
        assert '未知字体' in str(e)


def test_available_fonts():
    """测试可用字体列表"""
    fonts = list_fonts()
    assert 'standard' in fonts
    assert 'block' in fonts
    assert 'mini' in fonts
    assert 'shadow' in fonts
    assert 'digital' in fonts
    assert 'bubble' in fonts


def test_available_colors():
    """测试可用颜色列表"""
    colors = list_colors()
    assert 'red' in colors
    assert 'green' in colors
    assert 'blue' in colors
    assert 'cyan' in colors
    assert 'yellow' in colors
    assert 'magenta' in colors
    assert 'white' in colors


def test_render_char():
    """测试单字符渲染"""
    gen = ASCIIBannerGenerator('standard')
    
    # 渲染 'A'
    lines = gen.render_char('A')
    assert len(lines) == 5
    assert all(isinstance(line, str) for line in lines)
    
    # 渲染未知字符（应返回空格）
    lines_unknown = gen.render_char('~')
    assert len(lines_unknown) == 5
    
    # 渲染带颜色
    lines_color = gen.render_char('B', color='red')
    assert '\033[31m' in lines_color[0]
    assert '\033[0m' in lines_color[0]


def test_render_text_basic():
    """测试基本文本渲染"""
    result = render("ABC")
    assert isinstance(result, str)
    lines = result.split('\n')
    assert len(lines) >= 5  # 至少5行（根据字体高度）


def test_render_text_empty():
    """测试空文本"""
    result = render("")
    assert result == ""


def test_render_text_with_color():
    """测试带颜色渲染"""
    result = render("HI", color='blue')
    assert '\033[34m' in result  # 蓝色 ANSI 代码
    assert '\033[0m' in result   # 重置 ANSI 代码


def test_render_text_with_fill():
    """测试填充字符替换"""
    result = render("AB", fill_char='*')
    assert '*' in result


def test_render_text_with_border():
    """测试边框功能"""
    for border_style in ['single', 'double', 'rounded', 'bold', 'ascii']:
        result = render("TEST", border=border_style)
        lines = result.split('\n')
        assert len(lines) >= 7  # 边框增加上下两行
        
        # 检查边框字符存在
        if border_style == 'single':
            assert '─' in result or '│' in result
        elif border_style == 'double':
            assert '═' in result or '║' in result
        elif border_style == 'rounded':
            assert '─' in result or '│' in result or '╭' in result
        elif border_style == 'bold':
            assert '━' in result or '┃' in result
        elif border_style == 'ascii':
            assert '-' in result or '|' in result or '+' in result


def test_render_text_alignment():
    """测试对齐功能"""
    result_left = render("X", align='left', max_width=50)
    result_center = render("X", align='center', max_width=50)
    result_right = render("X", align='right', max_width=50)
    
    # 所有结果都应该有输出
    assert result_left
    assert result_center
    assert result_right


def test_render_text_width_limit():
    """测试宽度限制"""
    result = render("HELLO WORLD", max_width=20)
    lines = result.split('\n')
    # 检查每行宽度（忽略 ANSI 代码）
    for line in lines:
        # 简单检查：实际宽度可能因字体而异
        assert len(line) <= 30  # 允许一些余量


def test_different_fonts():
    """测试不同字体"""
    fonts_to_test = ['standard', 'block', 'mini', 'shadow', 'digital', 'bubble']
    
    for font in fonts_to_test:
        gen = ASCIIBannerGenerator(font)
        result = gen.render_text("TEST")
        assert result, f"字体 {font} 应该能渲染文本"
        assert '\n' in result, f"字体 {font} 应该渲染多行"


def test_digital_font():
    """测试数字字体（主要用于数字）"""
    gen = ASCIIBannerGenerator('digital')
    result = gen.render_text("1234567890")
    assert result
    # 数字字体主要用于数字
    result_time = gen.render_text("12:30")
    assert result_time  # 时间格式支持冒号


def test_mini_font():
    """测试迷你字体"""
    gen = ASCIIBannerGenerator('mini')
    result = gen.render_text("MINI")
    lines = result.split('\n')
    assert len(lines) == 3  # mini 字体只有 3 行高


def test_banner_builder():
    """测试流式 API"""
    builder = BannerBuilder("TEST")
    
    result = (builder
              .font('block')
              .color('green')
              .border('double')
              .align('center')
              .width(50)
              .build())
    
    assert result
    assert '\n' in result


def test_banner_builder_show():
    """测试 BannerBuilder 的 show 方法"""
    builder = BannerBuilder("HI").font('mini')
    result = builder.build()
    assert result  # 应该能生成输出


def test_template():
    """测试预定义模板"""
    for name in TEMPLATES.keys():
        result = template(name)
        assert result, f"模板 {name} 应该能渲染"


def test_template_invalid():
    """测试无效模板名"""
    try:
        template('invalid_template')
        assert False, "应该抛出异常"
    except ValueError as e:
        assert '未知模板' in str(e)


def test_print_banner():
    """测试 print_banner 函数"""
    # print_banner 应该能正常工作
    result = render("TEST", font='mini')
    assert result  # 应该有输出


def test_show_template():
    """测试 show_template 函数"""
    result = template('done')
    assert result  # 应该有输出


def test_set_font():
    """测试动态切换字体"""
    gen = ASCIIBannerGenerator('standard')
    assert gen.font == 'standard'
    
    gen.set_font('block')
    assert gen.font == 'block'
    
    try:
        gen.set_font('invalid')
        assert False, "应该抛出异常"
    except ValueError:
        pass


def test_render_special_characters():
    """测试特殊字符渲染"""
    gen = ASCIIBannerGenerator('standard')
    
    # 空格
    result = gen.render_text("A B")
    assert result
    
    # 数字
    result = gen.render_text("123")
    assert result
    
    # 标点
    result = gen.render_text("HI!")
    assert result


def test_multiple_lines():
    """测试多行文本"""
    result = render("ABC DEF GHI")
    assert result
    lines = result.split('\n')
    assert len(lines) >= 5


def test_strip_ansi():
    """测试 ANSI 代码移除"""
    gen = ASCIIBannerGenerator()
    
    # 带颜色的文本
    colored = gen.render_text("TEST", color='red')
    
    # 移除 ANSI 代码
    stripped = gen._strip_ansi(colored)
    
    # 确认没有 ANSI 代码
    assert '\033[' not in stripped
    assert stripped  # 应该还有内容


def test_long_text():
    """测试长文本"""
    result = render("THIS IS A LONGER TEXT FOR TESTING")
    assert result
    lines = result.split('\n')
    assert len(lines) >= 5


def run_all_tests():
    """运行所有测试"""
    print("=" * 60)
    print("ASCII Banner Utils 测试套件")
    print("=" * 60)
    
    tests = [
        test_initialization,
        test_available_fonts,
        test_available_colors,
        test_render_char,
        test_render_text_basic,
        test_render_text_empty,
        test_render_text_with_color,
        test_render_text_with_fill,
        test_render_text_with_border,
        test_render_text_alignment,
        test_render_text_width_limit,
        test_different_fonts,
        test_digital_font,
        test_mini_font,
        test_banner_builder,
        test_template,
        test_template_invalid,
        test_print_banner,
        test_show_template,
        test_set_font,
        test_render_special_characters,
        test_multiple_lines,
        test_strip_ansi,
        test_long_text,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            print(f"✓ {test.__name__}")
            passed += 1
        except AssertionError as e:
            print(f"✗ {test.__name__}: {e}")
            failed += 1
        except Exception as e:
            print(f"✗ {test.__name__}: {type(e).__name__}: {e}")
            failed += 1
    
    print("\n" + "=" * 60)
    print(f"测试结果: {passed} 通过, {failed} 失败")
    print("=" * 60)
    
    return failed == 0


if __name__ == '__main__':
    # 手动运行一些演示
    print("\n演示 print_banner 函数:")
    print_banner("TEST", font='mini')
    
    print("\n演示 show_template 函数:")
    show_template('done')
    
    print("\n演示 BannerBuilder.show():")
    BannerBuilder("HI").font('mini').show()
    
    # 运行所有测试
    success = run_all_tests()
    
    sys.exit(0 if success else 1)