# ASCII Flowchart Utils — Examples

from mod import Flowchart, BranchFlowchart, flowchart

def example_basic():
    """Linear flowchart."""
    fc = Flowchart(style="box", min_col_width=12)
    fc.start("开始").process("读取文件").process("处理数据").end("结束")
    print(fc.render())

def example_decision():
    """Decision with branching."""
    fc = Flowchart(style="box", min_col_width=14)
    fc.start("开始")
    fc.decision("文件存在?")
    fc.process("读取内容")
    fc.process("显示结果")
    fc.end("结束")
    print(fc.render())

def example_branch():
    """Branch helper with yes/no."""
    fc = Flowchart(style="box", min_col_width=14)
    fc.start("开始")
    fc.decision("验证通过?").branch(
        "验证通过?",
        left_label="N",
        right_label="Y",
    )
    fc.process("显示错误")
    fc.process("保存成功")
    fc.end("结束")
    print(fc.render())

def example_all_styles():
    """Show all 4 styles."""
    for style in ["box", "round", "bold", "double"]:
        print(f"\n=== Style: {style} ===")
        fc = Flowchart(style=style, min_col_width=12)
        fc.start("Start").process("Work").decision("OK?").end("End")
        print(fc.render())

def example_quick_helper():
    """One-liner."""
    print(flowchart("开始", "执行", "结束", style="bold"))

if __name__ == "__main__":
    example_basic()
    print("\n" + "="*50 + "\n")
    example_decision()
    print("\n" + "="*50 + "\n")
    example_all_styles()
    print("\n" + "="*50 + "\n")
    example_quick_helper()