"""
Markdown Table Utils 使用示例
============================

本示例展示 markdown_table_utils 的各种用法。
"""

import sys
sys.path.insert(0, '..')

from mod import (
    MarkdownTable, Align, TableConfig,
    generate_table, parse_table, from_dict_list, from_csv,
    find_tables, compare_tables, table, dict_table, csv_table
)


def example_1_basic_table():
    """示例1: 基本表格生成"""
    print("=" * 60)
    print("示例1: 基本表格生成")
    print("=" * 60)
    
    headers = ["产品", "数量", "单价", "总价"]
    rows = [
        ["苹果", 10, 5.50, 55.00],
        ["香蕉", 20, 3.20, 64.00],
        ["橙子", 15, 4.80, 72.00]
    ]
    
    result = generate_table(headers, rows)
    print(result)


def example_2_aligned_table():
    """示例2: 带对齐方式的表格"""
    print("\n" + "=" * 60)
    print("示例2: 带对齐方式的表格")
    print("=" * 60)
    
    headers = ["ID", "产品名称", "单价", "状态"]
    rows = [
        [1, "笔记本电脑", 5999.00, "在售"],
        [2, "无线鼠标", 99.00, "在售"],
        [3, "机械键盘", 399.00, "缺货"]
    ]
    aligns = [Align.RIGHT, Align.LEFT, Align.RIGHT, Align.CENTER]
    
    result = generate_table(headers, rows, aligns)
    print(result)


def example_3_table_class():
    """示例3: 使用MarkdownTable类"""
    print("\n" + "=" * 60)
    print("示例3: 使用MarkdownTable类")
    print("=" * 60)
    
    # 创建表格
    table = MarkdownTable(
        headers=["员工", "部门", "薪资"],
        rows=[
            ["张三", "技术部", 15000],
            ["李四", "销售部", 12000],
            ["王五", "市场部", 13000]
        ],
        aligns=[Align.LEFT, Align.CENTER, Align.RIGHT]
    )
    
    print("原始表格:")
    print(table)
    
    # 添加行
    table.add_row(["赵六", "人事部", 11000])
    print("\n添加行后:")
    print(table)
    
    # 排序
    table.sort_by("薪资", reverse=True)
    print("\n按薪资降序排序:")
    print(table)


def example_4_dict_to_table():
    """示例4: 从字典列表创建表格"""
    print("\n" + "=" * 60)
    print("示例4: 从字典列表创建表格")
    print("=" * 60)
    
    products = [
        {"id": 1, "name": "iPhone 15", "price": 6999, "stock": 100},
        {"id": 2, "name": "Samsung S24", "price": 5999, "stock": 80},
        {"id": 3, "name": "Pixel 8", "price": 4999, "stock": 50}
    ]
    
    # 选择特定列
    table = from_dict_list(
        products, 
        columns=["name", "price", "stock"],
        aligns=[Align.LEFT, Align.RIGHT, Align.CENTER]
    )
    
    print(table)


def example_5_csv_to_table():
    """示例5: 从CSV创建表格"""
    print("\n" + "=" * 60)
    print("示例5: 从CSV创建表格")
    print("=" * 60)
    
    csv_data = """日期,销售额,利润
2024-01,100000,20000
2024-02,120000,25000
2024-03,150000,30000
2024-04,130000,26000"""
    
    table = from_csv(csv_data)
    print(table)


def example_6_parse_markdown():
    """示例6: 解析Markdown表格"""
    print("\n" + "=" * 60)
    print("示例6: 解析Markdown表格")
    print("=" * 60)
    
    markdown = """
| 项目 | 进度 | 负责人 |
|------|------|--------|
| 前端开发 | 80% | 张三 |
| 后端开发 | 60% | 李四 |
| 测试 | 40% | 王五 |
"""
    
    table = parse_table(markdown)
    print(f"表头: {table.headers}")
    print(f"数据行: {table.rows}")
    print(f"对齐: {[a.value for a in table.aligns]}")
    
    # 转换为字典列表
    dict_list = table.to_dict_list()
    print(f"\n字典列表: {dict_list}")


def example_7_filter_sort():
    """示例7: 表格筛选和排序"""
    print("\n" + "=" * 60)
    print("示例7: 表格筛选和排序")
    print("=" * 60)
    
    table = MarkdownTable(
        headers=["产品", "类别", "价格", "库存"],
        rows=[
            ["iPhone", "手机", 6999, 100],
            ["iPad", "平板", 4999, 50],
            ["MacBook", "电脑", 9999, 30],
            ["Galaxy", "手机", 5999, 80],
            ["Surface", "电脑", 7999, 40]
        ]
    )
    
    print("原始表格:")
    print(table)
    
    # 筛选手机
    phones = table.filter("类别", "手机")
    print("\n筛选'手机'类别:")
    print(phones)
    
    # 按价格排序
    sorted_table = MarkdownTable(table.headers, [r[:] for r in table.rows], table.aligns)
    sorted_table.sort_by("价格", reverse=True)
    print("\n按价格降序排序:")
    print(sorted_table)


def example_8_transpose():
    """示例8: 表格转置"""
    print("\n" + "=" * 60)
    print("示例8: 表格转置")
    print("=" * 60)
    
    # 季度报表
    table = MarkdownTable(
        headers=["指标", "Q1", "Q2", "Q3", "Q4"],
        rows=[
            ["营收", 100, 120, 150, 180],
            ["成本", 60, 70, 85, 100],
            ["利润", 40, 50, 65, 80]
        ],
        aligns=[Align.LEFT, Align.RIGHT, Align.RIGHT, Align.RIGHT, Align.RIGHT]
    )
    
    print("原始表格 (行=指标):")
    print(table)
    
    transposed = table.transpose("季度")
    print("\n转置后 (行=季度):")
    print(transposed)


def example_9_merge_tables():
    """示例9: 表格合并"""
    print("\n" + "=" * 60)
    print("示例9: 表格合并")
    print("=" * 60)
    
    # 垂直合并
    table1 = MarkdownTable(
        headers=["部门", "人数"],
        rows=[["技术部", 50], ["销售部", 30]]
    )
    
    table2 = MarkdownTable(
        headers=["部门", "人数"],
        rows=[["市场部", 20], ["人事部", 10]]
    )
    
    print("表格1:")
    print(table1)
    print("\n表格2:")
    print(table2)
    
    merged = table1.merge(table2, "vertical")
    print("\n垂直合并:")
    print(merged)
    
    # 水平合并
    table3 = MarkdownTable(
        headers=["预算", "支出"],
        rows=[[1000, 800], [600, 500]]
    )
    
    print("\n表格3 (水平合并):")
    print(table3)
    
    merged_h = table1.merge(table3, "horizontal")
    print("\n水平合并:")
    print(merged_h)


def example_10_find_tables():
    """示例10: 从文档中提取表格"""
    print("\n" + "=" * 60)
    print("示例10: 从文档中提取表格")
    print("=" * 60)
    
    document = """
# 销售报告

## 第一季度

| 产品 | 销量 |
|------|------|
| 手机 | 1000 |
| 电脑 | 500 |

## 第二季度

| 产品 | 销量 |
|------|------|
| 手机 | 1200 |
| 电脑 | 600 |

## 总结

以上是各季度的销售数据。
"""
    
    tables = find_tables(document)
    print(f"找到 {len(tables)} 个表格")
    
    for i, t in enumerate(tables, 1):
        print(f"\n表格 {i}:")
        print(t)


def example_11_html_export():
    """示例11: 导出HTML表格"""
    print("\n" + "=" * 60)
    print("示例11: 导出HTML表格")
    print("=" * 60)
    
    table = MarkdownTable(
        headers=["姓名", "年龄", "城市"],
        rows=[
            ["张三", 25, "北京"],
            ["李四", 30, "上海"]
        ]
    )
    
    html = table.to_html()
    print(html)


def example_12_stats():
    """示例12: 表格统计"""
    print("\n" + "=" * 60)
    print("示例12: 表格统计")
    print("=" * 60)
    
    table = MarkdownTable(
        headers=["A", "B", "C"],
        rows=[
            [1, 2, 3],
            [4, None, 6],
            [7, 8, 9]
        ]
    )
    
    stats = table.get_stats()
    print("表格统计信息:")
    for key, value in stats.items():
        print(f"  {key}: {value}")


def example_13_config():
    """示例13: 表格配置"""
    print("\n" + "=" * 60)
    print("示例13: 表格配置")
    print("=" * 60)
    
    # 自定义配置
    config = TableConfig(
        min_col_width=8,  # 最小列宽
        padding=2,        # 单元格内边距
    )
    
    result = generate_table(
        headers=["A", "B"],
        rows=[[1, 2]],
        config=config
    )
    print(result)


def example_14_compare():
    """示例14: 表格比较"""
    print("\n" + "=" * 60)
    print("示例14: 表格比较")
    print("=" * 60)
    
    table1 = MarkdownTable(
        headers=["ID", "名称"],
        rows=[[1, "A"], [2, "B"]]
    )
    
    table2 = MarkdownTable(
        headers=["ID", "名称"],
        rows=[[1, "A"], [2, "B"], [3, "C"]]
    )
    
    result = compare_tables(table1, table2)
    print("比较结果:")
    for key, value in result.items():
        print(f"  {key}: {value}")


def example_15_convenience():
    """示例15: 便捷函数"""
    print("\n" + "=" * 60)
    print("示例15: 便捷函数")
    print("=" * 60)
    
    # 快速创建表格
    print("table() 函数:")
    print(table(["X", "Y"], [[1, 2], [3, 4]]))
    
    # 从字典快速创建
    print("\ndict_table() 函数:")
    print(dict_table([
        {"name": "Alice", "age": 30},
        {"name": "Bob", "age": 25}
    ]))
    
    # 从CSV快速创建
    print("\ncsv_table() 函数:")
    print(csv_table("a,b\n1,2\n3,4"))


def run_all_examples():
    """运行所有示例"""
    examples = [
        example_1_basic_table,
        example_2_aligned_table,
        example_3_table_class,
        example_4_dict_to_table,
        example_5_csv_to_table,
        example_6_parse_markdown,
        example_7_filter_sort,
        example_8_transpose,
        example_9_merge_tables,
        example_10_find_tables,
        example_11_html_export,
        example_12_stats,
        example_13_config,
        example_14_compare,
        example_15_convenience
    ]
    
    for example in examples:
        example()
    
    print("\n" + "=" * 60)
    print("所有示例运行完成！")
    print("=" * 60)


if __name__ == "__main__":
    run_all_examples()