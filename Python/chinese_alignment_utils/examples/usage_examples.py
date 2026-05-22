"""
中文文本对齐工具使用示例

演示各种功能的使用方法
"""

import sys
import os

# 正确添加模块路径
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from mod import (
    get_display_width,
    text_width,
    pad_left,
    pad_right,
    pad_center,
    truncate,
    align_columns,
    align_bilingual,
    create_progress_bar,
    wrap_text,
    split_by_width,
    ChineseTextAligner,
    format_table,
    ljust,
    rjust,
    center,
)


def demo_display_width():
    """演示字符宽度计算"""
    print("=" * 50)
    print("【字符宽度计算示例】")
    print("=" * 50)
    
    chars = [
        ('A', 'ASCII字母'),
        ('中', '汉字'),
        ('。', '中文标点'),
        ('Ａ', '全角字母'),
        ('★', '特殊符号'),
        ('\t', '制表符'),
    ]
    
    for char, desc in chars:
        width = get_display_width(char)
        print(f"  '{char}' ({desc}): 宽度 = {width}")
    
    print("\n文本总宽度计算：")
    texts = [
        "hello",
        "你好",
        "hello世界",
        "这是一个测试！",
    ]
    for text in texts:
        print(f"  '{text}' -> 宽度 = {text_width(text)}")


def demo_padding():
    """演示文本填充"""
    print("\n" + "=" * 50)
    print("【文本填充示例】")
    print("=" * 50)
    
    text = "测试"
    width = 20
    
    print(f"原文本: '{text}' (宽度: {text_width(text)})")
    print(f"目标宽度: {width}")
    print()
    print(f"左填充: |{pad_left(text, width)}|")
    print(f"右填充: |{pad_right(text, width)}|")
    print(f"居中: |{pad_center(text, width)}|")
    
    print("\n使用自定义填充字符：")
    print(f"左填充(*): |{pad_left(text, width, '*')}|")
    print(f"右填充(中): |{pad_right(text, width, '中')}|")


def demo_truncate():
    """演示文本截断"""
    print("\n" + "=" * 50)
    print("【文本截断示例】")
    print("=" * 50)
    
    texts = [
        "这是一段很长的中文文本用于测试截断功能",
        "This is a very long English text for testing truncation",
        "混合Mixed文本Text测试Test",
    ]
    
    widths = [20, 15, 25]
    
    for text, width in zip(texts, widths):
        result = truncate(text, width)
        print(f"原文本: {text}")
        print(f"截断到 {width} 宽度: {result}")
        print(f"实际宽度: {text_width(result)}")
        print()


def demo_table_alignment():
    """演示表格对齐"""
    print("\n" + "=" * 50)
    print("【表格对齐示例】")
    print("=" * 50)
    
    # 中文表格
    print("1. 基本表格:")
    rows = [
        ['姓名', '年龄', '城市'],
        ['张三', '25', '北京'],
        ['李四', '30', '上海'],
        ['王五', '28', '广州'],
    ]
    print(align_columns(rows))
    
    print("\n2. 中英文混合表格:")
    rows = [
        ['Name', '年龄', 'Score'],
        ['Alice', '25', '95.5'],
        ['张三', '30', '88.0'],
        ['Bob', '28', '92.3'],
    ]
    print(align_columns(rows))
    
    print("\n3. 右对齐数字列:")
    rows = [
        ['产品', '价格', '数量'],
        ['商品A', '￥99.00', '100'],
        ['商品B', '￥199.00', '50'],
    ]
    print(align_columns(rows, align=['left', 'right', 'right']))


def demo_bilingual_alignment():
    """演示双语对齐"""
    print("\n" + "=" * 50)
    print("【双语对齐示例】")
    print("=" * 50)
    
    chinese = "你好世界\n这是测试文本"
    english = "Hello World\nThis is a test text"
    
    print("1. 并排显示 (parallel):")
    print(align_bilingual(chinese, english, mode='parallel', width=40))
    
    print("\n2. 交错显示 (interleaved):")
    print(align_bilingual(chinese, english, mode='interleaved'))
    
    print("\n3. 块状显示 (block):")
    print(align_bilingual(chinese, english, mode='block'))


def demo_progress_bar():
    """演示进度条"""
    print("\n" + "=" * 50)
    print("【进度条示例】")
    print("=" * 50)
    
    print("不同进度状态：")
    for progress in [0, 25, 50, 75, 100]:
        bar = create_progress_bar(progress, 100, width=30)
        print(f"  {progress:3d}%: {bar}")
    
    print("\n自定义样式：")
    print(f"  方块: {create_progress_bar(60, 100, fill='■', empty='□')}")
    print(f"  圆点: {create_progress_bar(40, 100, fill='●', empty='○')}")
    print(f"  星号: {create_progress_bar(80, 100, fill='*', empty='-')}")


def demo_text_wrap():
    """演示文本换行"""
    print("\n" + "=" * 50)
    print("【文本换行示例】")
    print("=" * 50)
    
    english = "This is a long English sentence that needs to be wrapped into multiple lines for better readability."
    chinese = "这是一段很长的中文文本，需要进行换行处理以便于在终端中显示，提高可读性。"
    mixed = "这是Chinese和English混合mixed的text文本，测试test换行功能。"
    
    print("1. 英文换行 (宽度30):")
    print(wrap_text(english, width=30))
    
    print("\n2. 中文换行 (宽度30):")
    print(wrap_text(chinese, width=30))
    
    print("\n3. 中英文混合换行 (宽度30):")
    print(wrap_text(mixed, width=30))
    
    print("\n4. 带缩进换行 (宽度40, 缩进2空格):")
    print(wrap_text(english, width=40, indent='  '))


def demo_split_by_width():
    """演示按宽度分割"""
    print("\n" + "=" * 50)
    print("【按宽度分割示例】")
    print("=" * 50)
    
    text = "HelloWorld你好世界Test测试"
    
    print(f"原文本: {text}")
    print(f"总宽度: {text_width(text)}")
    print()
    
    for width in [5, 10, 15]:
        segments = split_by_width(text, width)
        print(f"按宽度 {width} 分割: {segments}")


def demo_format_table():
    """演示表格格式化"""
    print("\n" + "=" * 50)
    print("【高级表格格式化示例】")
    print("=" * 50)
    
    print("1. 带标题的表格:")
    headers = ['项目', '进度', '状态']
    rows = [
        ['项目A', '80%', '进行中'],
        ['项目B', '100%', '已完成'],
        ['项目C', '45%', '待审核'],
    ]
    print(format_table(headers, rows, title='项目状态表'))
    
    print("\n2. 无边框表格:")
    print(format_table(headers, rows, border=False))
    
    print("\n3. 数据报表:")
    headers = ['月份', '销售额', '增长率']
    rows = [
        ['一月', '￥125,000', '+12%'],
        ['二月', '￥138,500', '+10.8%'],
        ['三月', '￥152,300', '+9.9%'],
    ]
    print(format_table(headers, rows, title='季度销售报表'))


def demo_text_aligner_class():
    """演示文本对齐器类"""
    print("\n" + "=" * 50)
    print("【ChineseTextAligner 类示例】")
    print("=" * 50)
    
    print("链式调用:")
    
    # 右填充
    result = ChineseTextAligner('Hello').width(20).pad_right()
    print(f"右填充: |{result}|")
    
    # 左填充
    result = ChineseTextAligner('世界').width(20).pad_left('-')
    print(f"左填充: |{result}|")
    
    # 居中
    result = ChineseTextAligner('测试').width(20).pad_center('=')
    print(f"居中: |{result}|")
    
    # 截断
    result = ChineseTextAligner('这是一个很长的测试文本').width(10).truncate()
    print(f"截断: {result}")


def demo_convenience_functions():
    """演示便捷函数"""
    print("\n" + "=" * 50)
    print("【便捷函数示例】")
    print("=" * 50)
    
    text = "测试"
    width = 15
    
    print(f"原文本: '{text}'")
    print(f"ljust({width}): |{ljust(text, width)}|")
    print(f"rjust({width}): |{rjust(text, width)}|")
    print(f"center({width}): |{center(text, width)}|")


def demo_real_world_scenario():
    """演示实际应用场景"""
    print("\n" + "=" * 50)
    print("【实际应用场景】")
    print("=" * 50)
    
    # 场景：格式化输出命令行结果
    print("1. 命令行输出格式化:")
    
    commands = [
        ['命令', '描述', '状态'],
        ['git status', '查看仓库状态', '✓'],
        ['npm install', '安装依赖包', '✓'],
        ['python test', '运行测试', '✗'],
    ]
    print(align_columns(commands, align=['left', 'left', 'center']))
    
    # 场景：进度显示
    print("\n2. 任务进度显示:")
    tasks = ['下载文件', '解压缩', '安装依赖', '配置环境', '完成']
    for i, task in enumerate(tasks):
        progress = (i + 1) * 20
        bar = create_progress_bar(progress, 100, width=20)
        print(f"  {task}: {bar}")
    
    # 场景：中英文对照文档
    print("\n3. 中英文对照文档:")
    cn = "欢迎使用本系统\n请按照提示操作"
    en = "Welcome to this system\nPlease follow the instructions"
    print(align_bilingual(cn, en, mode='interleaved'))


def main():
    """运行所有示例"""
    demo_display_width()
    demo_padding()
    demo_truncate()
    demo_table_alignment()
    demo_bilingual_alignment()
    demo_progress_bar()
    demo_text_wrap()
    demo_split_by_width()
    demo_format_table()
    demo_text_aligner_class()
    demo_convenience_functions()
    demo_real_world_scenario()
    
    print("\n" + "=" * 50)
    print("所有示例运行完成！")
    print("=" * 50)


if __name__ == '__main__':
    main()