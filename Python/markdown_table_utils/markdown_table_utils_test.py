"""
Markdown Table Utils 测试文件
"""

import sys
sys.path.insert(0, '.')

from mod import (
    MarkdownTable, Align, TableConfig,
    generate_table, parse_table, from_dict_list, from_csv,
    find_tables, compare_tables, table, dict_table, csv_table
)


def test_basic_table_generation():
    """测试基本表格生成"""
    print("测试1: 基本表格生成")
    
    headers = ["姓名", "年龄", "城市"]
    rows = [
        ["张三", 25, "北京"],
        ["李四", 30, "上海"],
        ["王五", 28, "广州"]
    ]
    
    result = generate_table(headers, rows)
    print(result)
    print()
    
    # 验证格式
    assert "|" in result
    assert "姓名" in result
    assert "张三" in result
    print("✓ 基本表格生成测试通过\n")


def test_table_with_alignment():
    """测试带对齐方式的表格"""
    print("测试2: 带对齐方式的表格")
    
    headers = ["ID", "名称", "价格"]
    rows = [
        [1, "苹果", 5.50],
        [2, "香蕉", 3.20],
        [3, "橙子", 4.80]
    ]
    aligns = [Align.RIGHT, Align.LEFT, Align.RIGHT]
    
    result = generate_table(headers, rows, aligns)
    print(result)
    print()
    
    # 验证对齐标记
    lines = result.split("\n")
    separator = lines[1]
    assert "|---" in separator  # 左对齐
    assert "---:" in separator  # 右对齐
    print("✓ 对齐方式测试通过\n")


def test_markdown_table_class():
    """测试MarkdownTable类"""
    print("测试3: MarkdownTable类")
    
    table = MarkdownTable(
        headers=["产品", "数量", "单价"],
        rows=[
            ["手机", 10, 2999],
            ["电脑", 5, 5999],
            ["平板", 8, 1999]
        ],
        aligns=[Align.LEFT, Align.CENTER, Align.RIGHT]
    )
    
    print("表格字符串表示:")
    print(table)
    print()
    
    # 测试转HTML
    html = table.to_html()
    assert "<table>" in html
    assert "<th>产品</th>" in html
    print("✓ HTML转换测试通过")
    
    # 测试转字典列表
    dict_list = table.to_dict_list()
    assert len(dict_list) == 3
    assert dict_list[0]["产品"] == "手机"
    print("✓ 字典列表转换测试通过")
    
    # 测试获取列
    col = table.get_column(0)
    assert col == ["手机", "电脑", "平板"]
    print("✓ 获取列测试通过")
    
    # 测试添加行
    table.add_row(["键盘", 20, 199])
    assert len(table.rows) == 4
    print("✓ 添加行测试通过")
    
    # 测试添加列
    table.add_column("库存", [100, 50, 80, 200], Align.CENTER)
    assert len(table.headers) == 4
    assert table.rows[0][-1] == 100
    print("✓ 添加列测试通过\n")


def test_parse_table():
    """测试解析Markdown表格"""
    print("测试4: 解析Markdown表格")
    
    markdown = """
| 姓名 | 年龄 | 城市 |
|------|------|------|
| 张三 | 25 | 北京 |
| 李四 | 30 | 上海 |
"""
    
    table = parse_table(markdown)
    assert table.headers == ["姓名", "年龄", "城市"]
    assert len(table.rows) == 2
    assert table.rows[0] == ["张三", "25", "北京"]
    print(f"解析结果: {table}")
    print("✓ 解析表格测试通过\n")


def test_parse_alignment():
    """测试解析对齐方式"""
    print("测试5: 解析对齐方式")
    
    markdown = """
| 左对齐 | 居中 | 右对齐 | 默认 |
|:-------|:-----:|-------:|-------|
| A | B | C | D |
"""
    
    table = parse_table(markdown)
    assert table.aligns[0] == Align.LEFT
    assert table.aligns[1] == Align.CENTER
    assert table.aligns[2] == Align.RIGHT
    assert table.aligns[3] == Align.DEFAULT
    print("✓ 对齐方式解析测试通过\n")


def test_from_dict_list():
    """测试从字典列表创建表格"""
    print("测试6: 从字典列表创建表格")
    
    data = [
        {"name": "Alice", "age": 30, "city": "NYC"},
        {"name": "Bob", "age": 25, "city": "LA"},
        {"name": "Charlie", "age": 35, "city": "Chicago"}
    ]
    
    table = from_dict_list(data, columns=["name", "age", "city"])
    print(table)
    assert table.headers == ["name", "age", "city"]
    assert len(table.rows) == 3
    print("✓ 字典列表创建测试通过\n")


def test_from_csv():
    """测试从CSV创建表格"""
    print("测试7: 从CSV创建表格")
    
    csv_content = """name,age,city
Alice,30,NYC
Bob,25,LA
Charlie,35,Chicago"""
    
    table = from_csv(csv_content)
    print(table)
    assert table.headers == ["name", "age", "city"]
    assert len(table.rows) == 3
    print("✓ CSV创建测试通过\n")


def test_table_sort():
    """测试表格排序"""
    print("测试8: 表格排序")
    
    table = MarkdownTable(
        headers=["姓名", "年龄"],
        rows=[
            ["张三", 25],
            ["李四", 30],
            ["王五", 20]
        ]
    )
    
    # 按年龄升序
    table.sort_by("年龄")
    assert table.rows[0] == ["王五", 20]  # 年龄最小
    assert table.rows[2] == ["李四", 30]  # 年龄最大
    print("升序排序:")
    print(table)
    print()
    
    # 按年龄降序
    table.sort_by("年龄", reverse=True)
    assert table.rows[0] == ["李四", 30]  # 年龄最大
    print("降序排序:")
    print(table)
    print("✓ 排序测试通过\n")


def test_table_filter():
    """测试表格筛选"""
    print("测试9: 表格筛选")
    
    table = MarkdownTable(
        headers=["产品", "类型", "价格"],
        rows=[
            ["iPhone", "手机", 5999],
            ["iPad", "平板", 3999],
            ["MacBook", "电脑", 9999],
            ["Galaxy", "手机", 4999]
        ]
    )
    
    # 筛选手机
    filtered = table.filter("类型", "手机")
    assert len(filtered.rows) == 2
    print("筛选结果:")
    print(filtered)
    print("✓ 筛选测试通过\n")


def test_table_transpose():
    """测试表格转置"""
    print("测试10: 表格转置")
    
    table = MarkdownTable(
        headers=["指标", "Q1", "Q2", "Q3"],
        rows=[
            ["营收", 100, 120, 150],
            ["利润", 20, 25, 30]
        ]
    )
    
    transposed = table.transpose("季度")
    print("原表格:")
    print(table)
    print("\n转置后:")
    print(transposed)
    
    assert transposed.headers == ["季度", "指标", "Q1", "Q2", "Q3"]
    assert len(transposed.rows) == 4
    print("✓ 转置测试通过\n")


def test_table_merge():
    """测试表格合并"""
    print("测试11: 表格合并")
    
    table1 = MarkdownTable(
        headers=["姓名", "年龄"],
        rows=[
            ["张三", 25],
            ["李四", 30]
        ]
    )
    
    table2 = MarkdownTable(
        headers=["姓名", "年龄"],
        rows=[
            ["王五", 28],
            ["赵六", 32]
        ]
    )
    
    # 垂直合并
    merged_v = table1.merge(table2, "vertical")
    assert len(merged_v.rows) == 4
    print("垂直合并:")
    print(merged_v)
    print()
    
    # 水平合并
    table3 = MarkdownTable(
        headers=["城市", "职业"],
        rows=[
            ["北京", "工程师"],
            ["上海", "设计师"]
        ]
    )
    
    merged_h = table1.merge(table3, "horizontal")
    print("水平合并:")
    print(merged_h)
    assert len(merged_h.headers) == 4
    print("✓ 合并测试通过\n")


def test_table_stats():
    """测试表格统计"""
    print("测试12: 表格统计")
    
    table = MarkdownTable(
        headers=["A", "B", "C"],
        rows=[
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9]
        ]
    )
    
    stats = table.get_stats()
    print(f"统计信息: {stats}")
    
    assert stats["rows"] == 3
    assert stats["columns"] == 3
    assert stats["total_cells"] == 9
    assert stats["non_empty_cells"] == 9
    print("✓ 统计测试通过\n")


def test_find_tables():
    """测试从文本中提取表格"""
    print("测试13: 从文本中提取表格")
    
    markdown = """
# 数据报告

以下是销售数据：

| 产品 | 销量 |
|------|------|
| 手机 | 1000 |
| 电脑 | 500 |

以及员工信息：

| 姓名 | 部门 |
|------|------|
| 张三 | 销售 |
| 李四 | 技术 |
"""
    
    tables = find_tables(markdown)
    print(f"找到 {len(tables)} 个表格")
    
    assert len(tables) == 2
    assert tables[0].headers == ["产品", "销量"]
    assert tables[1].headers == ["姓名", "部门"]
    print("✓ 提取表格测试通过\n")


def test_compare_tables():
    """测试表格比较"""
    print("测试14: 表格比较")
    
    table1 = MarkdownTable(
        headers=["A", "B"],
        rows=[[1, 2], [3, 4]]
    )
    
    table2 = MarkdownTable(
        headers=["A", "B"],
        rows=[[1, 2], [3, 4], [5, 6]]
    )
    
    result = compare_tables(table1, table2)
    print(f"比较结果: {result}")
    
    assert result["same_headers"] == True
    assert result["row_count_diff"] == 1
    print("✓ 比较测试通过\n")


def test_convenience_functions():
    """测试便捷函数"""
    print("测试15: 便捷函数")
    
    # table函数
    result = table(["X", "Y"], [[1, 2], [3, 4]])
    print(f"table函数结果:\n{result}\n")
    
    # dict_table函数
    result = dict_table([{"a": 1, "b": 2}, {"a": 3, "b": 4}])
    print(f"dict_table函数结果:\n{result}\n")
    
    # csv_table函数
    result = csv_table("x,y\n1,2\n3,4")
    print(f"csv_table函数结果:\n{result}\n")
    
    print("✓ 便捷函数测试通过\n")


def test_table_config():
    """测试表格配置"""
    print("测试16: 表格配置")
    
    config = TableConfig(
        align=Align.CENTER,
        min_col_width=10,
        padding=2
    )
    
    result = generate_table(
        headers=["A", "B"],
        rows=[[1, 2]],
        config=config
    )
    print(result)
    print("✓ 表格配置测试通过\n")


def test_empty_values():
    """测试空值处理"""
    print("测试17: 空值处理")
    
    table = MarkdownTable(
        headers=["A", "B", "C"],
        rows=[
            [1, None, 3],
            [None, 2, None],
            [4, 5, 6]
        ]
    )
    
    print(table)
    stats = table.get_stats()
    print(f"统计: {stats}")
    print("✓ 空值处理测试通过\n")


def test_unicode_content():
    """测试Unicode内容"""
    print("测试18: Unicode内容")
    
    table = MarkdownTable(
        headers=["中文", "日本語", "한국어"],
        rows=[
            ["你好", "こんにちは", "안녕하세요"],
            ["世界", "世界", "세계"]
        ]
    )
    
    result = table.to_markdown()
    print(result)
    assert "中文" in result
    assert "日本語" in result
    assert "한국어" in result
    print("✓ Unicode内容测试通过\n")


def run_all_tests():
    """运行所有测试"""
    print("=" * 60)
    print("Markdown Table Utils 测试套件")
    print("=" * 60)
    print()
    
    tests = [
        test_basic_table_generation,
        test_table_with_alignment,
        test_markdown_table_class,
        test_parse_table,
        test_parse_alignment,
        test_from_dict_list,
        test_from_csv,
        test_table_sort,
        test_table_filter,
        test_table_transpose,
        test_table_merge,
        test_table_stats,
        test_find_tables,
        test_compare_tables,
        test_convenience_functions,
        test_table_config,
        test_empty_values,
        test_unicode_content
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            print(f"✗ 测试失败: {test.__name__}")
            print(f"  错误: {e}\n")
            failed += 1
    
    print("=" * 60)
    print(f"测试结果: {passed} 通过, {failed} 失败")
    print("=" * 60)
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)