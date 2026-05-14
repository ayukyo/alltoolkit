"""
ASCII Banner Utils 使用示例
演示各种功能和用法
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

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


def example_basic():
    """基本用法示例"""
    print("\n" + "=" * 60)
    print("1. 基本用法")
    print("=" * 60)
    
    # 使用快捷函数
    print("\n使用 render() 函数:")
    print(render("HELLO"))
    
    print("\n使用 print_banner() 函数:")
    print_banner("WORLD")
    
    # 使用类实例
    print("\n使用 ASCIIBannerGenerator 类:")
    gen = ASCIIBannerGenerator('standard')
    print(gen.render_text("PYTHON"))


def example_fonts():
    """不同字体示例"""
    print("\n" + "=" * 60)
    print("2. 不同字体")
    print("=" * 60)
    
    fonts = list_fonts()
    print(f"\n可用字体: {', '.join(fonts)}")
    
    text = "ABC"
    
    for font in fonts:
        print(f"\n【{font} 字体】")
        print_banner(text, font=font)


def example_colors():
    """颜色示例"""
    print("\n" + "=" * 60)
    print("3. 颜色支持")
    print("=" * 60)
    
    colors = list_colors()
    print(f"\n可用颜色: {', '.join(colors)}")
    
    print("\n彩色横幅:")
    print_banner("RED", color='red')
    print_banner("GREEN", color='green')
    print_banner("BLUE", color='blue')
    print_banner("YELLOW", color='yellow')
    print_banner("CYAN", color='cyan')
    print_banner("MAGENTA", color='magenta')


def example_borders():
    """边框示例"""
    print("\n" + "=" * 60)
    print("4. 边框样式")
    print("=" * 60)
    
    text = "FRAME"
    styles = ['single', 'double', 'rounded', 'bold', 'ascii']
    
    for style in styles:
        print(f"\n【{style} 边框】")
        print_banner(text, font='block', border=style)


def example_fill_chars():
    """填充字符示例"""
    print("\n" + "=" * 60)
    print("5. 自定义填充字符")
    print("=" * 60)
    
    text = "STAR"
    
    print("\n默认填充:")
    print_banner(text, font='block')
    
    print("\n使用 * 填充:")
    print_banner(text, font='block', fill_char='*')
    
    print("\n使用 # 填充:")
    print_banner(text, font='block', fill_char='#')
    
    print("\n使用 @ 填充:")
    print_banner(text, font='block', fill_char='@')


def example_builder():
    """流式 API 示例"""
    print("\n" + "=" * 60)
    print("6. 流式 API (BannerBuilder)")
    print("=" * 60)
    
    print("\n构建简单横幅:")
    BannerBuilder("HELLO").show()
    
    print("\n构建带边框的横幅:")
    BannerBuilder("WELCOME").font('block').border('double').show()
    
    print("\n构建彩色横幅:")
    BannerBuilder("SUCCESS").font('shadow').color('green').show()
    
    print("\n完整配置:")
    (BannerBuilder("BANNER")
     .font('block')
     .color('cyan')
     .border('rounded')
     .align('center')
     .width(50)
     .show())


def example_templates():
    """预定义模板示例"""
    print("\n" + "=" * 60)
    print("7. 预定义模板")
    print("=" * 60)
    
    print(f"\n可用模板: {', '.join(TEMPLATES.keys())}")
    
    for name in TEMPLATES.keys():
        print(f"\n【{name} 模板】")
        show_template(name)


def example_alignment():
    """对齐示例"""
    print("\n" + "=" * 60)
    print("8. 文本对齐")
    print("=" * 60)
    
    text = "ALIGN"
    
    print("\n左对齐:")
    print_banner(text, font='mini', align='left', max_width=40)
    
    print("\n居中对齐:")
    print_banner(text, font='mini', align='center', max_width=40)
    
    print("\n右对齐:")
    print_banner(text, font='mini', align='right', max_width=40)


def example_digital_clock():
    """数字时钟示例"""
    print("\n" + "=" * 60)
    print("9. 数字时钟风格")
    print("=" * 60)
    
    print("\n当前时间展示:")
    print_banner("12:30", font='digital', color='cyan')
    print_banner("09:45", font='digital', color='green')
    print_banner("23:59", font='digital', color='yellow')


def example_numbers():
    """数字示例"""
    print("\n" + "=" * 60)
    print("10. 数字和数学")
    print("=" * 60)
    
    print("\n数学运算:")
    print_banner("1 + 2 = 3", font='standard')
    
    print("\n百分比:")
    print_banner("100%", font='block', color='green')
    
    print("\n版本号:")
    print_banner("V2.0", font='mini', color='cyan')


def example_special_chars():
    """特殊字符示例"""
    print("\n" + "=" * 60)
    print("11. 特殊字符")
    print("=" * 60)
    
    print("\n感叹号:")
    print_banner("HI!", font='standard')
    
    print("\n问号:")
    print_banner("WHAT?", font='standard')
    
    print("\n带括号:")
    print_banner("(TEST)", font='mini')


def example_console_app():
    """控制台应用示例"""
    print("\n" + "=" * 60)
    print("12. 控制台应用标题")
    print("=" * 60)
    
    print("\n启动界面:")
    print_banner("CLI TOOL", font='block', color='cyan', border='double')
    
    print("\n欢迎信息:")
    print_banner("WELCOME USER", font='mini', color='green')
    
    print("\n成功提示:")
    print_banner("DONE!", font='mini', color='bright_green')
    
    print("\n错误提示:")
    print_banner("ERROR!", font='standard', color='red', border='bold')


def example_mini_banner():
    """迷你横幅示例"""
    print("\n" + "=" * 60)
    print("13. 紧凑迷你横幅")
    print("=" * 60)
    
    # Mini 字体适合空间有限的场景
    print("\n状态指示:")
    print_banner("OK", font='mini', color='green')
    print_banner("WARN", font='mini', color='yellow')
    print_banner("FAIL", font='mini', color='red')
    
    print("\n简短标签:")
    print_banner("API", font='mini')
    print_banner("CLI", font='mini')
    print_banner("GUI", font='mini')


def example_multi_line():
    """多行组合示例"""
    print("\n" + "=" * 60)
    print("14. 多行组合")
    print("=" * 60)
    
    print("\n双行标题:")
    print_banner("PROJECT", font='block', color='cyan')
    print_banner("NAME", font='block', color='cyan')
    
    print("\n组合信息:")
    print_banner("HELLO", font='standard', color='green')
    print_banner("WORLD", font='standard', color='blue')


def example_custom_width():
    """自定义宽度示例"""
    print("\n" + "=" * 60)
    print("15. 宽度控制")
    print("=" * 60)
    
    print("\n限制宽度为 30:")
    print_banner("LONG TEXT HERE", font='mini', max_width=30)
    
    print("\n限制宽度为 50:")
    print_banner("THIS IS A BANNER", font='standard', max_width=50)


def run_all_examples():
    """运行所有示例"""
    example_basic()
    example_fonts()
    example_colors()
    example_borders()
    example_fill_chars()
    example_builder()
    example_templates()
    example_alignment()
    example_digital_clock()
    example_numbers()
    example_special_chars()
    example_console_app()
    example_mini_banner()
    example_multi_line()
    example_custom_width()
    
    print("\n" + "=" * 60)
    print("所有示例完成!")
    print("=" * 60)


if __name__ == '__main__':
    run_all_examples()