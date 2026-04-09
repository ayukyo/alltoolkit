#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CSV Utils 测试套件

测试所有核心功能和边界情况
"""

import os
import sys
import tempfile
import shutil
from pathlib import Path

# 导入被测试模块
from mod import (
    CSVHandler,
    read_csv, read_csv_rows, parse_csv_string, parse_csv_string_rows,
    write_csv, write_csv_rows, to_csv_string,
    filter_rows, filter_by_value, filter_by_contains, sort_rows,
    select_columns, add_column, transform_column, remove_column, rename_column,
    get_column, get_unique_values,
    count_rows, count_by_value, get_numeric_stats,
    to_dict_by_key, group_by, merge_rows, join_tables,
    merge_csv_files, split_csv_file, csv_to_json, json_to_csv,
    read_csv_stream, process_csv_stream,
)


class TestResult:
    """测试结果记录"""
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.errors = []
    
    def ok(self, name: str):
        self.passed += 1
        print(f"  ✓ {name}")
    
    def fail(self, name: str, expected, actual):
        self.failed += 1
        self.errors.append((name, expected, actual))
        print(f"  ✗ {name}")
        print(f"    期望：{expected}")
        print(f"    实际：{actual}")
    
    def error(self, name: str, message: str):
        self.failed += 1
        self.errors.append((name, None, message))
        print(f"  ✗ {name}: {message}")
    
    def summary(self):
        total = self.passed + self.failed
        print(f"\n{'='*60}")
        print(f"测试结果：{self.passed}/{total} 通过")
        if self.failed > 0:
            print(f"\n失败的测试：")
            for name, expected, actual in self.errors:
                print(f"  - {name}")
        return self.failed == 0


# 创建测试用的临时目录
TEST_DIR = tempfile.mkdtemp(prefix='csv_utils_test_')


def setup_module():
    """测试前准备"""
    print(f"测试目录：{TEST_DIR}")


def teardown_module():
    """测试后清理"""
    shutil.rmtree(TEST_DIR, ignore_errors=True)
    print(f"已清理测试目录")


def test_csv_handler_basic(result: TestResult):
    """测试 CSVHandler 基本功能"""
    print("\n[测试] CSVHandler 基本功能")
    
    handler = CSVHandler()
    test_file = Path(TEST_DIR) / 'test_basic.csv'
    
    # 测试写入
    data = [
        {'name': 'Alice', 'age': '25', 'city': 'New York'},
        {'name': 'Bob', 'age': '30', 'city': 'London'},
        {'name': 'Charlie', 'age': '35', 'city': 'Tokyo'},
    ]
    
    try:
        handler.write(test_file, data)
        result.ok("写入 CSV 文件")
    except Exception as e:
        result.error("写入 CSV 文件", str(e))
        return
    
    # 测试读取
    try:
        read_data = handler.read(test_file)
        if len(read_data) == 3 and read_data[0]['name'] == 'Alice':
            result.ok("读取 CSV 文件")
        else:
            result.fail("读取 CSV 文件", 3, len(read_data))
    except Exception as e:
        result.error("读取 CSV 文件", str(e))
    
    # 测试追加
    try:
        handler.append(test_file, [{'name': 'David', 'age': '40', 'city': 'Paris'}])
        read_data = handler.read(test_file)
        if len(read_data) == 4:
            result.ok("追加数据到 CSV")
        else:
            result.fail("追加数据到 CSV", 4, len(read_data))
    except Exception as e:
        result.error("追加数据到 CSV", str(e))
    
    # 测试二维列表读写
    test_file2 = Path(TEST_DIR) / 'test_rows.csv'
    rows_data = [['A', 'B', 'C'], [1, 2, 3], [4, 5, 6]]
    try:
        handler.write_rows(test_file2, rows_data[1:], header=rows_data[0])
        read_rows = handler.read_rows(test_file2)
        if len(read_rows) == 3:
            result.ok("二维列表读写")
        else:
            result.fail("二维列表读写", 3, len(read_rows))
    except Exception as e:
        result.error("二维列表读写", str(e))


def test_read_functions(result: TestResult):
    """测试读取函数"""
    print("\n[测试] 读取函数")
    
    # 创建测试文件
    test_file = Path(TEST_DIR) / 'test_read.csv'
    write_csv(test_file, [
        {'id': '1', 'name': 'Alice', 'score': '90'},
        {'id': '2', 'name': 'Bob', 'score': '85'},
    ])
    
    # 测试 read_csv
    try:
        data = read_csv(test_file)
        if len(data) == 2 and data[0]['id'] == '1':
            result.ok("read_csv")
        else:
            result.fail("read_csv", 2, len(data))
    except Exception as e:
        result.error("read_csv", str(e))
    
    # 测试 read_csv_rows
    try:
        rows = read_csv_rows(test_file)
        if len(rows) == 3:  # 包含表头
            result.ok("read_csv_rows")
        else:
            result.fail("read_csv_rows", 3, len(rows))
    except Exception as e:
        result.error("read_csv_rows", str(e))
    
    # 测试 parse_csv_string
    csv_str = "name,age\nAlice,25\nBob,30"
    try:
        data = parse_csv_string(csv_str)
        if len(data) == 2 and data[0]['name'] == 'Alice':
            result.ok("parse_csv_string")
        else:
            result.fail("parse_csv_string", 2, len(data))
    except Exception as e:
        result.error("parse_csv_string", str(e))
    
    # 测试 parse_csv_string_rows
    try:
        rows = parse_csv_string_rows(csv_str)
        if len(rows) == 3:
            result.ok("parse_csv_string_rows")
        else:
            result.fail("parse_csv_string_rows", 3, len(rows))
    except Exception as e:
        result.error("parse_csv_string_rows", str(e))


def test_write_functions(result: TestResult):
    """测试写入函数"""
    print("\n[测试] 写入函数")
    
    # 测试 write_csv
    test_file = Path(TEST_DIR) / 'test_write.csv'
    data = [{'a': '1', 'b': '2'}, {'a': '3', 'b': '4'}]
    try:
        write_csv(test_file, data)
        read_data = read_csv(test_file)
        if len(read_data) == 2:
            result.ok("write_csv")
        else:
            result.fail("write_csv", 2, len(read_data))
    except Exception as e:
        result.error("write_csv", str(e))
    
    # 测试 write_csv_rows
    test_file2 = Path(TEST_DIR) / 'test_write_rows.csv'
    try:
        write_csv_rows(test_file2, [[1, 2], [3, 4]], header=['x', 'y'])
        rows = read_csv_rows(test_file2)
        if len(rows) == 3:
            result.ok("write_csv_rows")
        else:
            result.fail("write_csv_rows", 3, len(rows))
    except Exception as e:
        result.error("write_csv_rows", str(e))
    
    # 测试 to_csv_string
    try:
        csv_str = to_csv_string(data)
        if 'a,b' in csv_str and '1,2' in csv_str:
            result.ok("to_csv_string")
        else:
            result.fail("to_csv_string", "包含表头和数据", csv_str)
    except Exception as e:
        result.error("to_csv_string", str(e))
    
    # 测试空数据
    test_file3 = Path(TEST_DIR) / 'test_empty.csv'
    try:
        write_csv(test_file3, [])
        if test_file3.exists():
            result.ok("写入空数据")
        else:
            result.fail("写入空数据", "文件存在", "文件不存在")
    except Exception as e:
        result.error("写入空数据", str(e))


def test_filter_functions(result: TestResult):
    """测试过滤函数"""
    print("\n[测试] 过滤函数")
    
    data = [
        {'name': 'Alice', 'age': '25', 'city': 'NYC'},
        {'name': 'Bob', 'age': '30', 'city': 'LA'},
        {'name': 'Charlie', 'age': '35', 'city': 'NYC'},
        {'name': 'David', 'age': '40', 'city': 'SF'},
    ]
    
    # 测试 filter_rows
    try:
        filtered = filter_rows(data, lambda x: int(x['age']) > 30)
        if len(filtered) == 2:
            result.ok("filter_rows")
        else:
            result.fail("filter_rows", 2, len(filtered))
    except Exception as e:
        result.error("filter_rows", str(e))
    
    # 测试 filter_by_value
    try:
        filtered = filter_by_value(data, 'city', 'NYC')
        if len(filtered) == 2:
            result.ok("filter_by_value")
        else:
            result.fail("filter_by_value", 2, len(filtered))
    except Exception as e:
        result.error("filter_by_value", str(e))
    
    # 测试 filter_by_contains
    try:
        filtered = filter_by_contains(data, 'name', 'li')
        if len(filtered) == 2:  # Alice, Charlie
            result.ok("filter_by_contains")
        else:
            result.fail("filter_by_contains", 2, len(filtered))
    except Exception as e:
        result.error("filter_by_contains", str(e))


def test_sort_functions(result: TestResult):
    """测试排序函数"""
    print("\n[测试] 排序函数")
    
    data = [
        {'name': 'Charlie', 'age': '35'},
        {'name': 'Alice', 'age': '25'},
        {'name': 'Bob', 'age': '30'},
    ]
    
    # 测试升序排序
    try:
        sorted_data = sort_rows(data, 'age')
        if sorted_data[0]['name'] == 'Alice' and sorted_data[2]['name'] == 'Charlie':
            result.ok("sort_rows 升序")
        else:
            result.fail("sort_rows 升序", "Alice 第一", sorted_data[0]['name'])
    except Exception as e:
        result.error("sort_rows 升序", str(e))
    
    # 测试降序排序
    try:
        sorted_data = sort_rows(data, 'age', reverse=True)
        if sorted_data[0]['name'] == 'Charlie':
            result.ok("sort_rows 降序")
        else:
            result.fail("sort_rows 降序", "Charlie 第一", sorted_data[0]['name'])
    except Exception as e:
        result.error("sort_rows 降序", str(e))


def test_column_operations(result: TestResult):
    """测试列操作"""
    print("\n[测试] 列操作")
    
    data = [
        {'name': 'Alice', 'age': '25', 'city': 'NYC'},
        {'name': 'Bob', 'age': '30', 'city': 'LA'},
    ]
    
    # 测试 select_columns
    try:
        selected = select_columns(data, ['name', 'age'])
        if 'city' not in selected[0] and len(selected[0]) == 2:
            result.ok("select_columns")
        else:
            result.fail("select_columns", "只包含 name 和 age", list(selected[0].keys()))
    except Exception as e:
        result.error("select_columns", str(e))
    
    # 测试 add_column
    try:
        added = add_column(data, 'country', lambda x: 'USA')
        if 'country' in added[0] and added[0]['country'] == 'USA':
            result.ok("add_column")
        else:
            result.fail("add_column", "包含 country 列", list(added[0].keys()))
    except Exception as e:
        result.error("add_column", str(e))
    
    # 测试 transform_column
    try:
        transformed = transform_column(data, 'age', lambda x: int(x) * 2)
        if transformed[0]['age'] == 50:
            result.ok("transform_column")
        else:
            result.fail("transform_column", 50, transformed[0]['age'])
    except Exception as e:
        result.error("transform_column", str(e))
    
    # 测试 remove_column
    try:
        removed = remove_column(data, 'city')
        if 'city' not in removed[0]:
            result.ok("remove_column")
        else:
            result.fail("remove_column", "不包含 city", list(removed[0].keys()))
    except Exception as e:
        result.error("remove_column", str(e))
    
    # 测试 rename_column
    try:
        renamed = rename_column(data, 'name', 'full_name')
        if 'full_name' in renamed[0] and 'name' not in renamed[0]:
            result.ok("rename_column")
        else:
            result.fail("rename_column", "name 改为 full_name", list(renamed[0].keys()))
    except Exception as e:
        result.error("rename_column", str(e))
    
    # 测试 get_column
    try:
        names = get_column(data, 'name')
        if names == ['Alice', 'Bob']:
            result.ok("get_column")
        else:
            result.fail("get_column", "['Alice', 'Bob']", names)
    except Exception as e:
        result.error("get_column", str(e))
    
    # 测试 get_unique_values
    try:
        data_with_dupes = [
            {'city': 'NYC'}, {'city': 'LA'}, {'city': 'NYC'}, {'city': 'SF'}
        ]
        unique = get_unique_values(data_with_dupes, 'city')
        if len(unique) == 3 and 'NYC' in unique:
            result.ok("get_unique_values")
        else:
            result.fail("get_unique_values", 3, len(unique))
    except Exception as e:
        result.error("get_unique_values", str(e))


def test_statistics(result: TestResult):
    """测试统计函数"""
    print("\n[测试] 统计函数")
    
    data = [
        {'name': 'A', 'score': '90'},
        {'name': 'B', 'score': '80'},
        {'name': 'C', 'score': '70'},
        {'name': 'D', 'score': '90'},
    ]
    
    # 测试 count_rows
    try:
        count = count_rows(data)
        if count == 4:
            result.ok("count_rows")
        else:
            result.fail("count_rows", 4, count)
    except Exception as e:
        result.error("count_rows", str(e))
    
    # 测试 count_by_value
    try:
        counts = count_by_value(data, 'score')
        if counts['90'] == 2 and counts['80'] == 1:
            result.ok("count_by_value")
        else:
            result.fail("count_by_value", "{'90': 2, ...}", counts)
    except Exception as e:
        result.error("count_by_value", str(e))
    
    # 测试 get_numeric_stats
    try:
        stats = get_numeric_stats(data, 'score')
        if stats['count'] == 4 and stats['avg'] == 82.5:
            result.ok("get_numeric_stats")
        else:
            result.fail("get_numeric_stats", "avg=82.5", stats)
    except Exception as e:
        result.error("get_numeric_stats", str(e))


def test_transformations(result: TestResult):
    """测试转换函数"""
    print("\n[测试] 转换函数")
    
    data = [
        {'id': '1', 'name': 'Alice', 'dept': 'HR'},
        {'id': '2', 'name': 'Bob', 'dept': 'IT'},
        {'id': '3', 'name': 'Charlie', 'dept': 'HR'},
    ]
    
    # 测试 to_dict_by_key
    try:
        dict_data = to_dict_by_key(data, 'id')
        if '1' in dict_data and dict_data['1']['name'] == 'Alice':
            result.ok("to_dict_by_key")
        else:
            result.fail("to_dict_by_key", "键为 id 的字典", type(dict_data))
    except Exception as e:
        result.error("to_dict_by_key", str(e))
    
    # 测试 group_by
    try:
        grouped = group_by(data, 'dept')
        if len(grouped['HR']) == 2 and len(grouped['IT']) == 1:
            result.ok("group_by")
        else:
            result.fail("group_by", "HR=2, IT=1", {k: len(v) for k, v in grouped.items()})
    except Exception as e:
        result.error("group_by", str(e))
    
    # 测试 join_tables
    try:
        left = [{'id': '1', 'name': 'Alice'}, {'id': '2', 'name': 'Bob'}]
        right = [{'emp_id': '1', 'salary': '5000'}, {'emp_id': '2', 'salary': '6000'}]
        joined = join_tables(left, right, 'id', 'emp_id', 'inner')
        if len(joined) == 2 and 'right_salary' in joined[0]:
            result.ok("join_tables")
        else:
            result.fail("join_tables", 2, len(joined))
    except Exception as e:
        result.error("join_tables", str(e))


def test_file_operations(result: TestResult):
    """测试文件操作"""
    print("\n[测试] 文件操作")
    
    # 创建测试文件
    file1 = Path(TEST_DIR) / 'merge1.csv'
    file2 = Path(TEST_DIR) / 'merge2.csv'
    output_file = Path(TEST_DIR) / 'merged.csv'
    
    write_csv(file1, [{'name': 'A', 'val': '1'}, {'name': 'B', 'val': '2'}])
    write_csv(file2, [{'name': 'C', 'val': '3'}, {'name': 'D', 'val': '4'}])
    
    # 测试 merge_csv_files
    try:
        total = merge_csv_files([file1, file2], output_file)
        if total == 4:
            result.ok("merge_csv_files")
        else:
            result.fail("merge_csv_files", 4, total)
    except Exception as e:
        result.error("merge_csv_files", str(e))
    
    # 测试 split_csv_file
    try:
        split_dir = Path(TEST_DIR) / 'split_output'
        chunks = split_csv_file(output_file, 2, split_dir, prefix='part')
        if len(chunks) == 2:
            result.ok("split_csv_file")
        else:
            result.fail("split_csv_file", 2, len(chunks))
    except Exception as e:
        result.error("split_csv_file", str(e))
    
    # 测试 csv_to_json
    try:
        json_str = csv_to_json(file1)
        if '"name"' in json_str and '"val"' in json_str:
            result.ok("csv_to_json")
        else:
            result.fail("csv_to_json", "包含 JSON 格式", json_str[:50])
    except Exception as e:
        result.error("csv_to_json", str(e))
    
    # 测试 json_to_csv
    try:
        json_str = '[{"x": "1", "y": "2"}, {"x": "3", "y": "4"}]'
        csv_output = Path(TEST_DIR) / 'from_json.csv'
        json_to_csv(json_str, csv_output)
        data = read_csv(csv_output)
        if len(data) == 2:
            result.ok("json_to_csv")
        else:
            result.fail("json_to_csv", 2, len(data))
    except Exception as e:
        result.error("json_to_csv", str(e))


def test_stream_processing(result: TestResult):
    """测试流式处理"""
    print("\n[测试] 流式处理")
    
    # 创建测试文件
    test_file = Path(TEST_DIR) / 'stream_test.csv'
    write_csv(test_file, [
        {'id': str(i), 'value': str(i * 10)}
        for i in range(100)
    ])
    
    # 测试 read_csv_stream
    try:
        count = 0
        for row in read_csv_stream(test_file):
            count += 1
        if count == 100:
            result.ok("read_csv_stream")
        else:
            result.fail("read_csv_stream", 100, count)
    except Exception as e:
        result.error("read_csv_stream", str(e))
    
    # 测试 process_csv_stream
    try:
        output_file = Path(TEST_DIR) / 'stream_output.csv'
        process_csv_stream(
            test_file,
            lambda row: {'id': row['id'], 'doubled': str(int(row['value']) * 2)},
            output_file
        )
        result_data = read_csv(output_file)
        if len(result_data) == 100 and result_data[0]['doubled'] == '0':
            result.ok("process_csv_stream")
        else:
            result.fail("process_csv_stream", "100 行且 doubled=0", len(result_data))
    except Exception as e:
        result.error("process_csv_stream", str(e))


def test_edge_cases(result: TestResult):
    """测试边界情况"""
    print("\n[测试] 边界情况")
    
    # 测试空字符串
    try:
        result_data = parse_csv_string("")
        if result_data == []:
            result.ok("空字符串解析")
        else:
            result.fail("空字符串解析", "[]", result_data)
    except Exception as e:
        result.error("空字符串解析", str(e))
    
    # 测试包含特殊字符
    try:
        csv_str = 'name,desc\n"Alice","Hello, World"\n"Bob","Say ""Hi"""'
        data = parse_csv_string(csv_str)
        if len(data) == 2:
            result.ok("特殊字符处理")
        else:
            result.fail("特殊字符处理", 2, len(data))
    except Exception as e:
        result.error("特殊字符处理", str(e))
    
    # 测试 Unicode 字符
    try:
        data = [{'name': '张三', 'city': '北京'}, {'name': '李四', 'city': '上海'}]
        test_file = Path(TEST_DIR) / 'unicode_test.csv'
        write_csv(test_file, data)
        read_data = read_csv(test_file)
        if read_data[0]['name'] == '张三':
            result.ok("Unicode 支持")
        else:
            result.fail("Unicode 支持", "张三", read_data[0]['name'])
    except Exception as e:
        result.error("Unicode 支持", str(e))
    
    # 测试文件不存在
    try:
        read_csv(Path(TEST_DIR) / 'nonexistent.csv')
        result.fail("文件不存在处理", "抛出异常", "未抛出异常")
    except FileNotFoundError:
        result.ok("文件不存在处理")
    except Exception as e:
        result.error("文件不存在处理", str(e))


def main():
    """运行所有测试"""
    print("="*60)
    print("CSV Utils 测试套件")
    print("="*60)
    
    setup_module()
    
    result = TestResult()
    
    # 运行所有测试
    test_csv_handler_basic(result)
    test_read_functions(result)
    test_write_functions(result)
    test_filter_functions(result)
    test_sort_functions(result)
    test_column_operations(result)
    test_statistics(result)
    test_transformations(result)
    test_file_operations(result)
    test_stream_processing(result)
    test_edge_cases(result)
    
    teardown_module()
    
    # 输出结果
    success = result.summary()
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
