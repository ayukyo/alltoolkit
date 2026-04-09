#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CSV Utils 高级使用示例

演示复杂的数据处理场景
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from mod import (
    read_csv, write_csv,
    read_csv_stream, process_csv_stream,
    group_by, join_tables, merge_rows,
    to_dict_by_key,
    merge_csv_files, split_csv_file,
    csv_to_json, json_to_csv,
    transform_column, add_column, filter_rows,
)
import json


def example_data_transformation():
    """数据转换示例"""
    print("=" * 50)
    print("示例 1: 复杂数据转换")
    print("=" * 50)
    
    # 创建原始数据
    raw_data = [
        {'id': '1', 'name': 'alice smith', 'salary': '75000', 'start_date': '2020-01-15'},
        {'id': '2', 'name': 'bob johnson', 'salary': '85000', 'start_date': '2019-06-01'},
        {'id': '3', 'name': 'charlie brown', 'salary': '95000', 'start_date': '2018-03-20'},
    ]
    
    write_csv('raw_employees.csv', raw_data)
    
    # 多步转换
    data = read_csv('raw_employees.csv')
    
    # 1. 格式化名字（首字母大写）
    data = transform_column(data, 'name', lambda x: x.title())
    
    # 2. 添加格式化后的薪资
    data = add_column(data, 'formatted_salary', 
                     lambda x: f"${int(x['salary']):,}")
    
    # 3. 添加工龄（简化版）
    data = add_column(data, 'years', 
                     lambda x: str(2026 - int(x['start_date'][:4])))
    
    write_csv('transformed_employees.csv', data)
    
    print("转换完成:")
    for emp in data:
        print(f"  {emp['name']}: {emp['formatted_salary']}, 工龄：{emp['years']} 年")
    print()


def example_grouping_and_aggregation():
    """分组聚合示例"""
    print("=" * 50)
    print("示例 2: 分组和聚合")
    print("=" * 50)
    
    # 创建销售数据
    sales_data = [
        {'region': 'North', 'product': 'A', 'amount': '1000'},
        {'region': 'North', 'product': 'B', 'amount': '1500'},
        {'region': 'South', 'product': 'A', 'amount': '2000'},
        {'region': 'South', 'product': 'B', 'amount': '2500'},
        {'region': 'North', 'product': 'A', 'amount': '1200'},
        {'region': 'East', 'product': 'B', 'amount': '1800'},
    ]
    
    write_csv('sales.csv', sales_data)
    data = read_csv('sales.csv')
    
    # 按地区分组
    by_region = group_by(data, 'region')
    
    print("按地区分组统计:")
    for region, rows in by_region.items():
        total = sum(int(r['amount']) for r in rows)
        count = len(rows)
        avg = total / count
        print(f"  {region}: {count} 笔交易，总额 ${total:,}，平均 ${avg:,.2f}")
    
    # 按产品分组
    by_product = group_by(data, 'product')
    print("\n按产品分组统计:")
    for product, rows in by_product.items():
        total = sum(int(r['amount']) for r in rows)
        print(f"  产品 {product}: ${total:,}")
    print()


def example_table_join():
    """表连接示例"""
    print("=" * 50)
    print("示例 3: 表连接 (JOIN)")
    print("=" * 50)
    
    # 员工表
    employees = [
        {'emp_id': '1', 'name': 'Alice', 'dept_id': 'D1'},
        {'emp_id': '2', 'name': 'Bob', 'dept_id': 'D2'},
        {'emp_id': '3', 'name': 'Charlie', 'dept_id': 'D1'},
        {'emp_id': '4', 'name': 'Diana', 'dept_id': 'D3'},
    ]
    
    # 部门表
    departments = [
        {'dept_id': 'D1', 'dept_name': 'Engineering', 'budget': '500000'},
        {'dept_id': 'D2', 'dept_name': 'Marketing', 'budget': '300000'},
        {'dept_id': 'D3', 'dept_name': 'Sales', 'budget': '400000'},
    ]
    
    write_csv('employees.csv', employees)
    write_csv('departments.csv', departments)
    
    # 内连接
    joined = join_tables(employees, departments, 'dept_id', 'dept_id', 'inner')
    
    print("员工 - 部门连接结果:")
    for row in joined:
        print(f"  {row['name']} → {row['right_dept_name']} (预算：${row['right_budget']})")
    
    # 写入连接结果
    write_csv('employees_with_dept.csv', joined)
    print("\n✓ 已保存至 employees_with_dept.csv")
    print()


def example_large_file_processing():
    """大文件处理示例"""
    print("=" * 50)
    print("示例 4: 大文件流式处理")
    print("=" * 50)
    
    # 创建模拟大文件
    print("创建模拟数据文件 (1000 行)...")
    large_data = [
        {'id': str(i), 'value': str(i * 10), 'category': f'cat{i % 5}'}
        for i in range(1000)
    ]
    write_csv('large_input.csv', large_data)
    
    # 流式处理：计算总和并添加新列
    print("流式处理中...")
    
    running_total = [0]  # 使用列表以便在闭包中修改
    
    def process_row(row):
        running_total[0] += int(row['value'])
        return {
            'id': row['id'],
            'original_value': row['value'],
            'doubled_value': str(int(row['value']) * 2),
            'running_total': str(running_total[0])
        }
    
    process_csv_stream('large_input.csv', process_row, 'large_output.csv')
    
    # 验证结果
    output_data = read_csv('large_output.csv')
    print(f"处理完成：{len(output_data)} 行")
    print(f"最终累计值：{output_data[-1]['running_total']}")
    print(f"前 3 行示例:")
    for row in output_data[:3]:
        print(f"  ID {row['id']}: {row['original_value']} → {row['doubled_value']}")
    print()


def example_file_merge_split():
    """文件合并和分割示例"""
    print("=" * 50)
    print("示例 5: 文件合并和分割")
    print("=" * 50)
    
    import tempfile
    import os
    
    # 创建多个小文件
    print("创建 3 个测试文件...")
    files = []
    for i in range(3):
        filename = f'part_{i}.csv'
        data = [
            {'source': f'file_{i}', 'index': str(j), 'value': str(i * 100 + j)}
            for j in range(5)
        ]
        write_csv(filename, data)
        files.append(filename)
        print(f"  ✓ {filename} (5 行)")
    
    # 合并文件
    print("\n合并文件...")
    total = merge_csv_files(files, 'merged.csv')
    print(f"✓ 合并完成：共 {total} 行")
    
    # 分割文件
    print("\n分割文件 (每块 4 行)...")
    from pathlib import Path
    chunks = split_csv_file('merged.csv', 4, 'chunks/', prefix='chunk')
    print(f"✓ 分割为 {len(chunks)} 个文件:")
    for chunk in chunks:
        chunk_data = read_csv(chunk)
        print(f"  {chunk.name}: {len(chunk_data)} 行")
    print()


def example_format_conversion():
    """格式转换示例"""
    print("=" * 50)
    print("示例 6: CSV ↔ JSON 格式转换")
    print("=" * 50)
    
    # 创建 CSV
    data = [
        {'name': 'Product A', 'price': '29.99', 'stock': '100'},
        {'name': 'Product B', 'price': '49.99', 'stock': '50'},
        {'name': 'Product C', 'price': '19.99', 'stock': '200'},
    ]
    write_csv('products.csv', data)
    
    # CSV 转 JSON
    json_str = csv_to_json('products.csv')
    print("CSV → JSON:")
    parsed_json = json.loads(json_str)
    print(json.dumps(parsed_json, indent=2, ensure_ascii=False)[:200] + "...")
    
    # JSON 转 CSV
    new_json = '''[
        {"item": "Apple", "qty": "10", "price": "1.50"},
        {"item": "Orange", "qty": "15", "price": "2.00"},
        {"item": "Banana", "qty": "20", "price": "0.80"}
    ]'''
    json_to_csv(new_json, 'fruits.csv')
    
    fruits = read_csv('fruits.csv')
    print(f"\nJSON → CSV:")
    for fruit in fruits:
        print(f"  {fruit['item']}: {fruit['qty']} @ ${fruit['price']}")
    print()


def example_complex_pipeline():
    """复杂数据处理流水线示例"""
    print("=" * 50)
    print("示例 7: 完整数据处理流水线")
    print("=" * 50)
    
    # 模拟原始订单数据
    orders = [
        {'order_id': '1001', 'customer': 'Alice', 'product': 'Laptop', 'amount': '1200', 'status': 'completed'},
        {'order_id': '1002', 'customer': 'Bob', 'product': 'Mouse', 'amount': '50', 'status': 'pending'},
        {'order_id': '1003', 'customer': 'Charlie', 'product': 'Keyboard', 'amount': '150', 'status': 'completed'},
        {'order_id': '1004', 'customer': 'Alice', 'product': 'Monitor', 'amount': '400', 'status': 'completed'},
        {'order_id': '1005', 'customer': 'Diana', 'product': 'Laptop', 'amount': '1200', 'status': 'cancelled'},
        {'order_id': '1006', 'customer': 'Bob', 'product': 'Keyboard', 'amount': '150', 'status': 'completed'},
    ]
    
    write_csv('orders_raw.csv', orders)
    print("1. 读取原始订单数据")
    
    # 步骤 1: 只保留已完成的订单
    data = read_csv('orders_raw.csv')
    completed = filter_rows(data, lambda x: x['status'] == 'completed')
    print(f"2. 过滤完成订单：{len(completed)} 个")
    
    # 步骤 2: 按客户分组
    by_customer = group_by(completed, 'customer')
    print(f"3. 按客户分组：{len(by_customer)} 个客户")
    
    # 步骤 3: 计算每个客户的总消费
    customer_summary = []
    for customer, orders in by_customer.items():
        total = sum(int(o['amount']) for o in orders)
        order_count = len(orders)
        customer_summary.append({
            'customer': customer,
            'total_spent': str(total),
            'order_count': str(order_count),
            'avg_order': str(total // order_count)
        })
    
    # 步骤 4: 按总消费排序
    customer_summary.sort(key=lambda x: int(x['total_spent']), reverse=True)
    
    # 步骤 5: 添加排名
    for i, row in enumerate(customer_summary, 1):
        row['rank'] = str(i)
    
    write_csv('customer_summary.csv', customer_summary)
    print("4. 生成客户消费报告")
    
    print("\n客户消费排行榜:")
    for row in customer_summary:
        print(f"  #{row['rank']} {row['customer']}: ${row['total_spent']} ({row['order_count']} 单)")
    print()


def main():
    """运行所有高级示例"""
    print("\n" + "🔧" * 25)
    print("CSV Utils 高级示例")
    print("🔧" * 25 + "\n")
    
    example_data_transformation()
    example_grouping_and_aggregation()
    example_table_join()
    example_large_file_processing()
    example_file_merge_split()
    example_format_conversion()
    example_complex_pipeline()
    
    print("=" * 50)
    print("✅ 所有高级示例运行完成!")
    print("=" * 50)
    
    # 清理提示
    print("\n生成的文件列表:")
    generated_files = [
        'raw_employees.csv', 'transformed_employees.csv',
        'sales.csv', 'employees.csv', 'departments.csv', 'employees_with_dept.csv',
        'large_input.csv', 'large_output.csv',
        'part_0.csv', 'part_1.csv', 'part_2.csv', 'merged.csv',
        'products.csv', 'fruits.csv',
        'orders_raw.csv', 'customer_summary.csv',
    ]
    for f in generated_files:
        print(f"  - {f}")
    print("\n提示：可手动删除这些示例文件")


if __name__ == '__main__':
    main()
