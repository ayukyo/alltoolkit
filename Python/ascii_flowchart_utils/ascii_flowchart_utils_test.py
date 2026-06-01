# ASCII Flowchart Utils — Tests
# Pure Python, zero external dependencies.

import sys
sys.path.insert(0, __file__.replace("ascii_flowchart_utils_test.py", "ascii_flowchart_utils"))

from mod import Flowchart, flowchart, STYLE_GLYPHS, ARROW_RIGHT, ARROW_DOWN

# ─── Fixtures ─────────────────────────────────────────────────────────────────

def base():
    return Flowchart(style="box", indent=2, min_col_width=14)

# ─── Tests ─────────────────────────────────────────────────────────────────────

def test_empty():
    out = Flowchart().render()
    assert out == ""

def test_start_end():
    fc = Flowchart(style="box")
    fc.start("开始").end("结束")
    out = fc.render()
    assert "开始" in out
    assert "结束" in out
    assert "开始" in out
    assert "结束" in out
    # Arrows and non-space chars present
    assert "→" in out or "↓" in out or any(c in out for c in "[]()")

def test_process():
    fc = Flowchart(style="box")
    fc.process("执行任务")
    out = fc.render()
    assert "执行任务" in out

def test_decision():
    fc = Flowchart(style="box")
    fc.decision("条件判断?")
    out = fc.render()
    assert "条件判断" in out

def test_data_node():
    fc = Flowchart(style="box")
    fc.data("输入数据")
    out = fc.render()
    assert "输入数据" in out

def test_sub_preparation():
    fc = Flowchart(style="box")
    fc.sub("初始化")
    out = fc.render()
    assert "初始化" in out

def test_manual_input():
    fc = Flowchart(style="box")
    fc.input("用户输入")
    out = fc.render()
    assert "用户输入" in out

def test_connector_node():
    fc = Flowchart(style="box")
    fc.connector("连接点")
    out = fc.render()
    assert "连接点" in out

def test_off_page():
    fc = Flowchart(style="box")
    fc.off_page("下一页")
    out = fc.render()
    assert "下一页" in out

def test_multi_style():
    for style in STYLE_GLYPHS:
        fc = Flowchart(style=style)
        fc.start("A").process("B").end("C")
        out = fc.render()
        assert "A" in out
        assert "B" in out
        assert "C" in out

def test_invalid_style():
    try:
        Flowchart(style="nonexistent")
        assert False, "Should raise"
    except ValueError as e:
        assert "Unknown style" in str(e)

def test_quick_helper():
    out = flowchart("开始", "处理", "结束")
    assert "开始" in out
    assert "处理" in out
    assert "结束" in out

def test_long_text_wrap():
    fc = Flowchart(style="box", min_col_width=8)
    fc.process("这是一段很长的文本需要自动换行处理")
    out = fc.render()
    assert "这" in out  # at least something rendered

def test_min_col_width_override():
    fc = Flowchart(style="box", min_col_width=20)
    fc.process("短")
    out = fc.render()
    assert "短" in out

def test_fluent_api():
    fc = Flowchart()
    result = (
        fc.start("开始")
         .process("步骤1")
         .process("步骤2")
         .decision("判断?")
         .end("结束")
    )
    assert result is fc
    out = fc.render()
    assert "开始" in out
    assert "步骤1" in out
    assert "步骤2" in out
    assert "判断" in out
    assert "结束" in out

def test_arrow_different():
    fc = Flowchart(style="box", arrow=ARROW_DOWN)
    fc.start().process("A").end()
    out = fc.render()
    assert "开始" in out
    assert "A" in out
    assert "结束" in out

# ─── Run ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import traceback
    tests = [
        test_empty, test_start_end, test_process, test_decision,
        test_data_node, test_sub_preparation, test_manual_input,
        test_connector_node, test_off_page, test_multi_style,
        test_invalid_style, test_quick_helper, test_long_text_wrap,
        test_min_col_width_override, test_fluent_api, test_arrow_different,
    ]
    passed = 0
    failed = 0
    for t in tests:
        try:
            t()
            print(f"  PASS  {t.__name__}")
            passed += 1
        except Exception as e:
            traceback.print_exc()
            print(f"  FAIL  {t.__name__}: {e}")
            failed += 1
    print(f"\n{passed}/{passed+failed} passed")
    if failed:
        sys.exit(1)