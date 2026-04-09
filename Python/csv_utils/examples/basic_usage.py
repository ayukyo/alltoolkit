#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CSV Utils 基础使用示例

演示最常用的功能
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from mod import (
    read_csv, write_csv,
    filter_by_value, filter_by_contains, filter_rows,
    sort_rows,
    select_columns, add_column,
    count_rows, count_by_value, get_numeric_stats,
    to_csv_string, parse_csv_string,
)


def example_basic_read_write():
    """基础读写示例"""
    print("=" * 50)
    print("示例 1: 基础读写")
    print("=" * 50)
    
    # 创建示例数据
    data = [
        {'name': 'Alice', 'age': '25', 'city': 'New York', 'salary': '75000'},
        {'name': 'Bob', 'age': '30', 'city': 'Los Angeles', 'salary': '85000'},
        {'name': 'Charlie', 'age': '35', 'city': 'Chicago', 'salary': '95000'},
        {'name': 'Diana', 'age': '28', 'city': 'New York', 'salary': '80000'},
        {'name': 'Eve', 'age': '32', 'city': 'Los Angeles', 'salary': '90000'},
    ]
    
    # 写入 CSV
    write_csv('employees.csv', data)
    print("✓ 已写入 employees.csv")
    
    # 读取 CSV
    data = read_csv('employees.csv')
    print(f"✓ 已读取 {len(data)} 行数据")
    print(f"第一行：{data[0]}")
    print()


def example_filtering():
    """过滤示例"""
    print("=" * 50)
    print("示例 2: 数据过滤")
    print("=" * 50)
    
    data = read_csv('employees.csv')
    
    # 精确匹配过滤
    ny_employees = filter_by_value(data, 'city', 'New York')
    print(f"纽约员工 ({len(ny_employees)} 人):")
    for emp in ny_employees:
        print(f"  - {emp['name']}")
    
    # 子字符串匹配
    contains_e = filter_by_contains(data, 'name', 'e')
    print(f"\n名字包含 'e' 的员工 ({len(contains_e)} 人):")
    for emp in contains_e:
        print(f"  - {emp['name']}")
    
    # 自定义条件过滤
    high_earners = filter_rows(data, lambda x: int(x['salary']) > 85000)
    print(f"\n高薪员工 (>85k, {len(high_earners)} 人):")
    for emp in high_earners:
        print(f"  - {emp['name']}: ${emp['salary']}")
    print()


def example_sorting():
    """排序示例"""
    print("=" * 50)
    print("示例 3: 数据排序")
    print("=" * 50)
    
    data = read_csv('employees.csv')
    
    # 按年龄升序
    sorted_by_age = sort_rows(data, 'age')
    print("按年龄升序:")
    for emp in sorted_by_age[:3]:
        print(f"  {emp['name']}: {emp['age']} 岁")
    
    # 按薪资降序
    sorted_by_salary = sort_rows(data, 'salary', reverse=True)
    print("\n按薪资降序:")
    for emp in sorted_by_salary[:3]:
        print(f"  {emp['name']}: ${emp['salary']}")
    print()


def example_column_operations():
    """列操作示例"""
    print("=" * 50)
    print("示例 4: 列操作")
    print("=" * 50)
    
    data = read_csv('employees.csv')
    
    # 选择列
    selected = select_columns(data, ['name', 'city'])
    print("只保留 name 和 city 列:")
    print(f"  列：{list(selected[0].keys())}")
    
    # 添加列
    with_country = add_column(data, 'country', lambda x: 'USA')
    print(f"\n添加 country 列:")
    print(f"  列：{list(with_country[0].keys())}")
    
    # 转换列
    with_doubled_salary = add_column(data, 'double_salary', lambda x: str(int(x['salary']) * 2))
    print(f"\n添加 double_salary 列:")
    print(f"  {with_doubled_salary[0]['name']}: ${with_doubled_salary[0]['salary']} → ${with_doubled_salary[0]['double_salary']}")
    print()


def example_statistics():
    """统计示例"""
    print("=" * 50)
    print("示例 5: 数据统计")
    print("=" * 50)
    
    data = read_csv('employees.csv')
    
    # 行数统计
    total = count_rows(data)
    print(f"总员工数：{total}")
    
    # 按城市分组计数
    city_counts = count_by_value(data, 'city')
    print("\n各城市员工数:")
    for city, count in city_counts.items():
        print(f"  {city}: {count} 人")
    
    # 数值统计
    salary_stats = get_numeric_stats(data, 'salary')
    print(f"\n薪资统计:")
    print(f"  最低：${salary_stats['min']:,.0f}")
    print(f"  最高：${salary_stats['max']:,.0f}")
    print(f"  平均：${salary_stats['avg']:,.2f}")
    print(f"  总和：${salary_stats['sum']:,.0f}")
    print()


def example_string_conversion():
    """字符串转换示例"""
    print("=" * 50)
    print("示例 6: CSV 字符串转换")
    print("=" * 50)
    
    data = [
        {'product': 'Apple', 'price': '1.50', 'stock': '100'},
        {'product': 'Banana', 'price': '0.80', 'stock': '200'},
    ]
    
    # 字典列表转 CSV 字符串
    csv_str = to_csv_string(data)
    print("转换为 CSV 字符串:")
    print(csv_str)
    
    # CSV 字符串转字典列表
    parsed = parse_csv_string(csv_str)
    print(f"\n解析回字典列表:")
    print(f"  产品：{parsed[0]['product']}, 价格：${parsed[0]['price']}")
    print()


def example_real_world():
    """实际应用场景示例"""
    print("=" * 50)
    print("示例 7: 实际应用场景 - 员工报告")
    print("=" * 50)
    
    data = read_csv('employees.csv')
    
    # 1. 过滤纽约员工
    ny_employees = filter_by_value(data, 'city', 'New York')
    
    # 2. 按薪资降序
    sorted_ny = sort_rows(ny_employees, 'salary', reverse=True)
    
    # 3. 选择需要的列
    report_data = select_columns(sorted_ny, ['name', 'salary', 'age'])
    
    # 4. 添加排名列
    ranked_data = []
    for i, row in enumerate(report_data, 1):
        new_row = row.copy()
        new_row['rank'] = str(i)
        ranked_data.append(new_row)
    
    # 5. 写入报告
    write_csv('ny_employee_report.csv', ranked_data)
    
    print("纽约员工报告已生成：ny_employee_report.csv")
    print("\n报告内容:")
    for emp in ranked_data:
        print(f"  #{emp['rank']} {emp['name']}: ${emp['salary']} (年龄：{emp['age']})")
    print()


def main():
    """运行所有示例"""
    print("\n" + "📊" * 25)
    print("CSV Utils 使用示例")
    print("📊" * 25 + "\n")
    
    example_basic_read_write()
    example_filtering()
    example_sorting()
    example_column_operations()
    example_statistics()
    example_string_conversion()
    example_real_world()
    
    print("=" * 50)
    print("✅ 所有示例运行完成!")
    print("=" * 50)
    print("\n生成的文件:")
    print("  - employees.csv")
    print("  - ny_employee_report.csv")


if __name__ == '__main__':
    main()
