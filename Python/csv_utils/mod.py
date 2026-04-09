#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CSV Utils - CSV 文件处理工具库

零依赖，仅使用 Python 标准库
功能：读取、写入、解析、生成、过滤、排序、转换 CSV 文件

Author: AllToolkit
License: MIT
"""

import csv
import io
from typing import List, Dict, Any, Optional, Callable, Union, Iterator
from pathlib import Path


# ============================================================================
# 核心类
# ============================================================================

class CSVHandler:
    """CSV 文件处理器"""
    
    def __init__(self, delimiter: str = ',', quotechar: str = '"', 
                 encoding: str = 'utf-8', newline: str = ''):
        """
        初始化 CSV 处理器
        
        Args:
            delimiter: 字段分隔符，默认逗号
            quotechar: 引用字符，默认双引号
            encoding: 文件编码，默认 UTF-8
            newline: 换行符控制，默认空字符串（通用换行）
        """
        self.delimiter = delimiter
        self.quotechar = quotechar
        self.encoding = encoding
        self.newline = newline
    
    def read(self, filepath: Union[str, Path]) -> List[Dict[str, str]]:
        """
        读取 CSV 文件为字典列表
        
        Args:
            filepath: CSV 文件路径
            
        Returns:
            字典列表，每个字典代表一行数据
        """
        filepath = Path(filepath)
        if not filepath.exists():
            raise FileNotFoundError(f"CSV 文件不存在：{filepath}")
        
        with open(filepath, 'r', encoding=self.encoding, newline=self.newline) as f:
            reader = csv.DictReader(f, delimiter=self.delimiter, quotechar=self.quotechar)
            return list(reader)
    
    def read_rows(self, filepath: Union[str, Path]) -> List[List[str]]:
        """
        读取 CSV 文件为二维列表（不包含表头）
        
        Args:
            filepath: CSV 文件路径
            
        Returns:
            二维列表，每行是一个字符串列表
        """
        filepath = Path(filepath)
        if not filepath.exists():
            raise FileNotFoundError(f"CSV 文件不存在：{filepath}")
        
        with open(filepath, 'r', encoding=self.encoding, newline=self.newline) as f:
            reader = csv.reader(f, delimiter=self.delimiter, quotechar=self.quotechar)
            return list(reader)
    
    def write(self, filepath: Union[str, Path], data: List[Dict[str, Any]], 
              fieldnames: Optional[List[str]] = None) -> None:
        """
        将字典列表写入 CSV 文件
        
        Args:
            filepath: 输出文件路径
            data: 字典列表数据
            fieldnames: 字段名列表（可选，默认使用第一个字典的键）
        """
        filepath = Path(filepath)
        filepath.parent.mkdir(parents=True, exist_ok=True)
        
        if not data:
            # 空数据，创建空文件
            filepath.touch()
            return
        
        if fieldnames is None:
            fieldnames = list(data[0].keys())
        
        with open(filepath, 'w', encoding=self.encoding, newline=self.newline) as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=self.delimiter, 
                                   quotechar=self.quotechar)
            writer.writeheader()
            writer.writerows(data)
    
    def write_rows(self, filepath: Union[str, Path], data: List[List[Any]], 
                   header: Optional[List[str]] = None) -> None:
        """
        将二维列表写入 CSV 文件
        
        Args:
            filepath: 输出文件路径
            data: 二维列表数据
            header: 表头（可选）
        """
        filepath = Path(filepath)
        filepath.parent.mkdir(parents=True, exist_ok=True)
        
        with open(filepath, 'w', encoding=self.encoding, newline=self.newline) as f:
            writer = csv.writer(f, delimiter=self.delimiter, quotechar=self.quotechar)
            if header:
                writer.writerow(header)
            writer.writerows(data)
    
    def append(self, filepath: Union[str, Path], data: List[Dict[str, Any]]) -> None:
        """
        追加数据到 CSV 文件末尾
        
        Args:
            filepath: CSV 文件路径
            data: 字典列表数据
        """
        filepath = Path(filepath)
        
        if not filepath.exists():
            # 文件不存在，直接写入
            self.write(filepath, data)
            return
        
        # 读取现有字段名
        with open(filepath, 'r', encoding=self.encoding, newline=self.newline) as f:
            reader = csv.DictReader(f, delimiter=self.delimiter, quotechar=self.quotechar)
            fieldnames = reader.fieldnames
        
        if not fieldnames:
            raise ValueError("无法从现有文件获取字段名")
        
        # 追加数据
        with open(filepath, 'a', encoding=self.encoding, newline=self.newline) as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=self.delimiter,
                                   quotechar=self.quotechar)
            writer.writerows(data)


# ============================================================================
# 便捷函数 - 读取
# ============================================================================

def read_csv(filepath: Union[str, Path], encoding: str = 'utf-8') -> List[Dict[str, str]]:
    """
    读取 CSV 文件为字典列表
    
    Args:
        filepath: CSV 文件路径
        encoding: 文件编码
        
    Returns:
        字典列表
    """
    handler = CSVHandler(encoding=encoding)
    return handler.read(filepath)


def read_csv_rows(filepath: Union[str, Path], encoding: str = 'utf-8') -> List[List[str]]:
    """
    读取 CSV 文件为二维列表
    
    Args:
        filepath: CSV 文件路径
        encoding: 文件编码
        
    Returns:
        二维列表
    """
    handler = CSVHandler(encoding=encoding)
    return handler.read_rows(filepath)


def parse_csv_string(csv_string: str, delimiter: str = ',') -> List[Dict[str, str]]:
    """
    解析 CSV 格式的字符串
    
    Args:
        csv_string: CSV 格式的字符串
        delimiter: 字段分隔符
        
    Returns:
        字典列表
    """
    f = io.StringIO(csv_string)
    reader = csv.DictReader(f, delimiter=delimiter)
    return list(reader)


def parse_csv_string_rows(csv_string: str, delimiter: str = ',') -> List[List[str]]:
    """
    解析 CSV 格式的字符串为二维列表
    
    Args:
        csv_string: CSV 格式的字符串
        delimiter: 字段分隔符
        
    Returns:
        二维列表
    """
    f = io.StringIO(csv_string)
    reader = csv.reader(f, delimiter=delimiter)
    return list(reader)


# ============================================================================
# 便捷函数 - 写入
# ============================================================================

def write_csv(filepath: Union[str, Path], data: List[Dict[str, Any]], 
              encoding: str = 'utf-8') -> None:
    """
    将字典列表写入 CSV 文件
    
    Args:
        filepath: 输出文件路径
        data: 字典列表数据
        encoding: 文件编码
    """
    handler = CSVHandler(encoding=encoding)
    handler.write(filepath, data)


def write_csv_rows(filepath: Union[str, Path], data: List[List[Any]], 
                   header: Optional[List[str]] = None, encoding: str = 'utf-8') -> None:
    """
    将二维列表写入 CSV 文件
    
    Args:
        filepath: 输出文件路径
        data: 二维列表数据
        header: 表头
        encoding: 文件编码
    """
    handler = CSVHandler(encoding=encoding)
    handler.write_rows(filepath, data, header)


def to_csv_string(data: List[Dict[str, Any]], delimiter: str = ',') -> str:
    """
    将字典列表转换为 CSV 格式字符串
    
    Args:
        data: 字典列表数据
        delimiter: 字段分隔符
        
    Returns:
        CSV 格式字符串
    """
    if not data:
        return ''
    
    output = io.StringIO()
    fieldnames = list(data[0].keys())
    writer = csv.DictWriter(output, fieldnames=fieldnames, delimiter=delimiter)
    writer.writeheader()
    writer.writerows(data)
    return output.getvalue()


# ============================================================================
# 数据处理函数
# ============================================================================

def filter_rows(data: List[Dict[str, Any]], 
                condition: Callable[[Dict[str, Any]], bool]) -> List[Dict[str, Any]]:
    """
    根据条件过滤行
    
    Args:
        data: 字典列表数据
        condition: 过滤条件函数，接收一行数据返回布尔值
        
    Returns:
        过滤后的数据
    """
    return [row for row in data if condition(row)]


def filter_by_value(data: List[Dict[str, Any]], column: str, 
                    value: Any) -> List[Dict[str, Any]]:
    """
    根据列值过滤行（精确匹配）
    
    Args:
        data: 字典列表数据
        column: 列名
        value: 匹配值
        
    Returns:
        过滤后的数据
    """
    return [row for row in data if row.get(column) == value]


def filter_by_contains(data: List[Dict[str, Any]], column: str, 
                       substring: str) -> List[Dict[str, Any]]:
    """
    根据列值包含的子字符串过滤行
    
    Args:
        data: 字典列表数据
        column: 列名
        substring: 要搜索的子字符串
        
    Returns:
        过滤后的数据
    """
    return [row for row in data if substring in str(row.get(column, ''))]


def sort_rows(data: List[Dict[str, Any]], column: str, 
              reverse: bool = False, key_func: Optional[Callable] = None) -> List[Dict[str, Any]]:
    """
    根据列值排序
    
    Args:
        data: 字典列表数据
        column: 排序列名
        reverse: 是否降序
        key_func: 自定义排序键函数（可选）
        
    Returns:
        排序后的数据
    """
    if key_func:
        return sorted(data, key=lambda x: key_func(x.get(column)), reverse=reverse)
    
    # 尝试数值排序
    def try_numeric(val):
        try:
            return float(val)
        except (TypeError, ValueError):
            return str(val) if val is not None else ''
    
    return sorted(data, key=lambda x: try_numeric(x.get(column)), reverse=reverse)


def select_columns(data: List[Dict[str, Any]], 
                   columns: List[str]) -> List[Dict[str, Any]]:
    """
    选择指定的列
    
    Args:
        data: 字典列表数据
        columns: 要保留的列名列表
        
    Returns:
        只包含指定列的数据
    """
    return [{col: row.get(col) for col in columns} for row in data]


def add_column(data: List[Dict[str, Any]], column: str, 
               value_func: Callable[[Dict[str, Any]], Any]) -> List[Dict[str, Any]]:
    """
    添加新列
    
    Args:
        data: 字典列表数据
        column: 新列名
        value_func: 计算列值的函数，接收一行数据返回新值
        
    Returns:
        添加新列后的数据（新列表）
    """
    result = []
    for row in data:
        new_row = row.copy()
        new_row[column] = value_func(row)
        result.append(new_row)
    return result


def transform_column(data: List[Dict[str, Any]], column: str,
                     transform_func: Callable[[Any], Any]) -> List[Dict[str, Any]]:
    """
    转换列的值
    
    Args:
        data: 字典列表数据
        column: 要转换的列名
        transform_func: 转换函数
        
    Returns:
        转换后的数据（新列表）
    """
    result = []
    for row in data:
        new_row = row.copy()
        if column in new_row:
            new_row[column] = transform_func(new_row[column])
        result.append(new_row)
    return result


def remove_column(data: List[Dict[str, Any]], column: str) -> List[Dict[str, Any]]:
    """
    删除列
    
    Args:
        data: 字典列表数据
        column: 要删除的列名
        
    Returns:
        删除列后的数据（新列表）
    """
    result = []
    for row in data:
        new_row = {k: v for k, v in row.items() if k != column}
        result.append(new_row)
    return result


def rename_column(data: List[Dict[str, Any]], old_name: str, 
                  new_name: str) -> List[Dict[str, Any]]:
    """
    重命名列
    
    Args:
        data: 字典列表数据
        old_name: 原列名
        new_name: 新列名
        
    Returns:
        重命名列后的数据（新列表）
    """
    result = []
    for row in data:
        new_row = {}
        for k, v in row.items():
            if k == old_name:
                new_row[new_name] = v
            else:
                new_row[k] = v
        result.append(new_row)
    return result


def get_column(data: List[Dict[str, Any]], column: str) -> List[Any]:
    """
    获取单列的所有值
    
    Args:
        data: 字典列表数据
        column: 列名
        
    Returns:
        列值列表
    """
    return [row.get(column) for row in data]


def get_unique_values(data: List[Dict[str, Any]], column: str) -> List[Any]:
    """
    获取列的唯一值列表
    
    Args:
        data: 字典列表数据
        column: 列名
        
    Returns:
        唯一值列表（保持原有顺序）
    """
    seen = set()
    unique = []
    for row in data:
        val = row.get(column)
        if val not in seen:
            seen.add(val)
            unique.append(val)
    return unique


# ============================================================================
# 统计函数
# ============================================================================

def count_rows(data: List[Dict[str, Any]]) -> int:
    """
    统计行数
    
    Args:
        data: 字典列表数据
        
    Returns:
        行数
    """
    return len(data)


def count_by_value(data: List[Dict[str, Any]], column: str) -> Dict[Any, int]:
    """
    按列值分组计数
    
    Args:
        data: 字典列表数据
        column: 列名
        
    Returns:
        值到计数的映射
    """
    counts = {}
    for row in data:
        val = row.get(column)
        counts[val] = counts.get(val, 0) + 1
    return counts


def get_numeric_stats(data: List[Dict[str, Any]], column: str) -> Dict[str, float]:
    """
    获取数值列的统计信息
    
    Args:
        data: 字典列表数据
        column: 列名
        
    Returns:
        包含 count, sum, min, max, avg 的字典
    """
    values = []
    for row in data:
        val = row.get(column)
        try:
            values.append(float(val))
        except (TypeError, ValueError):
            continue
    
    if not values:
        return {'count': 0, 'sum': 0, 'min': 0, 'max': 0, 'avg': 0}
    
    return {
        'count': len(values),
        'sum': sum(values),
        'min': min(values),
        'max': max(values),
        'avg': sum(values) / len(values)
    }


# ============================================================================
# 转换函数
# ============================================================================

def to_dict_by_key(data: List[Dict[str, Any]], key_column: str) -> Dict[Any, Dict[str, Any]]:
    """
    将字典列表转换为以某列为键的字典
    
    Args:
        data: 字典列表数据
        key_column: 作为键的列名
        
    Returns:
        键值对字典
    """
    result = {}
    for row in data:
        key = row.get(key_column)
        if key is not None:
            result[key] = row
    return result


def group_by(data: List[Dict[str, Any]], column: str) -> Dict[Any, List[Dict[str, Any]]]:
    """
    按列值分组
    
    Args:
        data: 字典列表数据
        column: 分组列名
        
    Returns:
        分组后的字典，键为列值，值为该组的行列表
    """
    groups = {}
    for row in data:
        key = row.get(column)
        if key not in groups:
            groups[key] = []
        groups[key].append(row)
    return groups


def merge_rows(data: List[Dict[str, Any]], key_column: str, 
               merge_func: Callable[[Dict[str, Any], Dict[str, Any]], Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    合并具有相同键值的行
    
    Args:
        data: 字典列表数据
        key_column: 合并键列名
        merge_func: 合并函数，接收两行数据返回合并结果
        
    Returns:
        合并后的数据
    """
    groups = group_by(data, key_column)
    result = []
    for key, rows in groups.items():
        merged = rows[0]
        for row in rows[1:]:
            merged = merge_func(merged, row)
        result.append(merged)
    return result


def join_tables(left: List[Dict[str, Any]], right: List[Dict[str, Any]],
                left_key: str, right_key: str, 
                join_type: str = 'inner') -> List[Dict[str, Any]]:
    """
    连接两个表（类似 SQL JOIN）
    
    Args:
        left: 左表数据
        right: 右表数据
        left_key: 左表连接键列名
        right_key: 右表连接键列名
        join_type: 连接类型 ('inner', 'left', 'right', 'outer')
        
    Returns:
        连接后的数据
    """
    result = []
    right_dict = to_dict_by_key(right, right_key)
    left_keys_seen = set()
    
    # 处理左表
    for left_row in left:
        left_key_val = left_row.get(left_key)
        left_keys_seen.add(left_key_val)
        
        if left_key_val in right_dict:
            # 匹配成功
            merged = {**left_row}
            # 添加右表字段（添加前缀避免冲突）
            for k, v in right_dict[left_key_val].items():
                if k != right_key:
                    merged[f'right_{k}'] = v
            result.append(merged)
        elif join_type in ('left', 'outer'):
            # 左连接或外连接，保留左表数据
            merged = {**left_row}
            result.append(merged)
    
    # 处理右表（右连接和外连接）
    if join_type in ('right', 'outer'):
        for right_row in right:
            right_key_val = right_row.get(right_key)
            if right_key_val not in left_keys_seen:
                merged = {}
                # 添加右表字段
                for k, v in right_row.items():
                    if k != right_key:
                        merged[f'right_{k}'] = v
                result.append(merged)
    
    return result


# ============================================================================
# 文件操作
# ============================================================================

def merge_csv_files(filepaths: List[Union[str, Path]], output_path: Union[str, Path],
                    encoding: str = 'utf-8') -> int:
    """
    合并多个 CSV 文件
    
    Args:
        filepaths: 输入文件路径列表
        output_path: 输出文件路径
        encoding: 文件编码
        
    Returns:
        合并后的总行数
    """
    handler = CSVHandler(encoding=encoding)
    all_data = []
    
    for fp in filepaths:
        data = handler.read(fp)
        all_data.extend(data)
    
    handler.write(output_path, all_data)
    return len(all_data)


def split_csv_file(filepath: Union[str, Path], chunk_size: int, 
                   output_dir: Union[str, Path], encoding: str = 'utf-8',
                   prefix: str = 'chunk') -> List[Path]:
    """
    将 CSV 文件分割成多个小文件
    
    Args:
        filepath: 输入文件路径
        chunk_size: 每个文件的行数
        output_dir: 输出目录
        encoding: 文件编码
        prefix: 输出文件前缀
        
    Returns:
        生成的文件路径列表
    """
    handler = CSVHandler(encoding=encoding)
    data = handler.read(filepath)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    output_files = []
    for i in range(0, len(data), chunk_size):
        chunk = data[i:i + chunk_size]
        output_path = output_dir / f'{prefix}_{i // chunk_size}.csv'
        handler.write(output_path, chunk)
        output_files.append(output_path)
    
    return output_files


def csv_to_json(filepath: Union[str, Path], encoding: str = 'utf-8') -> str:
    """
    将 CSV 文件转换为 JSON 字符串
    
    Args:
        filepath: CSV 文件路径
        encoding: 文件编码
        
    Returns:
        JSON 格式字符串
    """
    import json
    handler = CSVHandler(encoding=encoding)
    data = handler.read(filepath)
    return json.dumps(data, ensure_ascii=False, indent=2)


def json_to_csv(json_string: str, output_path: Union[str, Path], 
                encoding: str = 'utf-8') -> None:
    """
    将 JSON 字符串转换为 CSV 文件
    
    Args:
        json_string: JSON 格式字符串
        output_path: 输出 CSV 文件路径
        encoding: 文件编码
    """
    import json
    data = json.loads(json_string)
    handler = CSVHandler(encoding=encoding)
    handler.write(output_path, data)


# ============================================================================
# 流式处理（大文件）
# ============================================================================

def read_csv_stream(filepath: Union[str, Path], encoding: str = 'utf-8') -> Iterator[Dict[str, str]]:
    """
    流式读取 CSV 文件（适合大文件）
    
    Args:
        filepath: CSV 文件路径
        encoding: 文件编码
        
    Yields:
        每行数据的字典
    """
    filepath = Path(filepath)
    if not filepath.exists():
        raise FileNotFoundError(f"CSV 文件不存在：{filepath}")
    
    with open(filepath, 'r', encoding=encoding, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            yield row


def process_csv_stream(filepath: Union[str, Path], 
                       process_func: Callable[[Dict[str, str]], Dict[str, Any]],
                       output_path: Optional[Union[str, Path]] = None,
                       encoding: str = 'utf-8') -> Optional[List[Dict[str, Any]]]:
    """
    流式处理 CSV 文件
        
    Args:
        filepath: 输入 CSV 文件路径
        process_func: 处理函数，接收一行数据返回处理结果
        output_path: 输出文件路径（可选，不提供则返回结果列表）
        encoding: 文件编码
        
    Returns:
        如果未指定输出路径，返回处理后的数据列表；否则返回 None
    """
    handler = CSVHandler(encoding=encoding)
    results = []
    
    with open(filepath, 'r', encoding=encoding, newline='') as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        
        for row in reader:
            result = process_func(row)
            results.append(result)
    
    if output_path:
        handler.write(output_path, results)
        return None
    
    return results


# ============================================================================
# 模块导出
# ============================================================================

__all__ = [
    # 核心类
    'CSVHandler',
    
    # 读取函数
    'read_csv',
    'read_csv_rows',
    'parse_csv_string',
    'parse_csv_string_rows',
    
    # 写入函数
    'write_csv',
    'write_csv_rows',
    'to_csv_string',
    
    # 数据处理
    'filter_rows',
    'filter_by_value',
    'filter_by_contains',
    'sort_rows',
    'select_columns',
    'add_column',
    'transform_column',
    'remove_column',
    'rename_column',
    'get_column',
    'get_unique_values',
    
    # 统计函数
    'count_rows',
    'count_by_value',
    'get_numeric_stats',
    
    # 转换函数
    'to_dict_by_key',
    'group_by',
    'merge_rows',
    'join_tables',
    
    # 文件操作
    'merge_csv_files',
    'split_csv_file',
    'csv_to_json',
    'json_to_csv',
    
    # 流式处理
    'read_csv_stream',
    'process_csv_stream',
]


# ============================================================================
# 命令行接口
# ============================================================================

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 2:
        print("CSV Utils - 命令行工具")
        print("用法:")
        print("  python mod.py read <file.csv>     - 读取并显示 CSV 文件")
        print("  python mod.py count <file.csv>    - 统计行数")
        print("  python mod.py columns <file.csv>  - 显示列名")
        print("  python mod.py head <file.csv> [n] - 显示前 n 行（默认 10）")
        sys.exit(0)
    
    command = sys.argv[1]
    
    if command == 'read' and len(sys.argv) >= 3:
        data = read_csv(sys.argv[2])
        for row in data[:20]:
            print(row)
        if len(data) > 20:
            print(f"... 共 {len(data)} 行")
    
    elif command == 'count' and len(sys.argv) >= 3:
        data = read_csv(sys.argv[2])
        print(f"行数：{len(data)}")
    
    elif command == 'columns' and len(sys.argv) >= 3:
        data = read_csv(sys.argv[2])
        if data:
            print(f"列名：{', '.join(data[0].keys())}")
    
    elif command == 'head' and len(sys.argv) >= 3:
        n = int(sys.argv[3]) if len(sys.argv) >= 4 else 10
        data = read_csv(sys.argv[2])
        for row in data[:n]:
            print(row)
    
    else:
        print(f"未知命令：{command}")
        sys.exit(1)
