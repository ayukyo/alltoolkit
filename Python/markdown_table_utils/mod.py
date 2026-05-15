"""
Markdown Table Utils - Markdown表格处理工具集

功能：
- 从列表/字典生成Markdown表格
- 解析Markdown表格为数据结构
- 表格对齐设置（左、中、右）
- 表格格式化和美化
- 表格转置
- 表格合并
- 表格排序
- 表格筛选

零外部依赖，纯Python实现。
"""

from typing import List, Dict, Any, Optional, Union, Tuple
from dataclasses import dataclass
from enum import Enum
import re


class Align(Enum):
    """表格列对齐方式"""
    LEFT = "left"
    CENTER = "center"
    RIGHT = "right"
    DEFAULT = "default"


@dataclass
class TableConfig:
    """表格配置"""
    align: Align = Align.DEFAULT
    min_col_width: int = 3
    padding: int = 1
    include_header: bool = True


class MarkdownTable:
    """Markdown表格类"""
    
    def __init__(self, headers: List[str], rows: List[List[Any]], 
                 aligns: Optional[List[Align]] = None):
        """
        初始化表格
        
        Args:
            headers: 表头列表
            rows: 数据行列表
            aligns: 每列对齐方式列表
        """
        self.headers = headers
        self.rows = rows
        self.aligns = aligns or [Align.DEFAULT] * len(headers)
        
        if len(self.aligns) != len(headers):
            raise ValueError(f"对齐方式数量({len(self.aligns)})必须与列数({len(headers)})一致")
    
    def __repr__(self) -> str:
        return f"MarkdownTable(headers={self.headers}, rows={len(self.rows)})"
    
    def __str__(self) -> str:
        return self.to_markdown()
    
    def to_markdown(self, config: Optional[TableConfig] = None) -> str:
        """转换为Markdown格式"""
        config = config or TableConfig()
        return generate_table(self.headers, self.rows, self.aligns, config)
    
    def to_html(self) -> str:
        """转换为HTML表格"""
        html = "<table>\n"
        html += "  <thead>\n    <tr>\n"
        for header in self.headers:
            html += f"      <th>{header}</th>\n"
        html += "    </tr>\n  </thead>\n"
        html += "  <tbody>\n"
        for row in self.rows:
            html += "    <tr>\n"
            for cell in row:
                html += f"      <td>{cell}</td>\n"
            html += "    </tr>\n"
        html += "  </tbody>\n</table>"
        return html
    
    def to_dict_list(self) -> List[Dict[str, Any]]:
        """转换为字典列表"""
        result = []
        for row in self.rows:
            row_dict = {}
            for i, header in enumerate(self.headers):
                row_dict[header] = row[i] if i < len(row) else None
            result.append(row_dict)
        return result
    
    def get_column(self, index: int) -> List[Any]:
        """获取指定列"""
        return [row[index] if index < len(row) else None for row in self.rows]
    
    def add_row(self, row: List[Any]) -> None:
        """添加一行"""
        self.rows.append(row)
    
    def add_column(self, header: str, values: List[Any], align: Align = Align.DEFAULT) -> None:
        """添加一列"""
        self.headers.append(header)
        self.aligns.append(align)
        for i, row in enumerate(self.rows):
            if i < len(values):
                row.append(values[i])
            else:
                row.append(None)
    
    def sort_by(self, column: Union[int, str], reverse: bool = False) -> None:
        """按指定列排序"""
        if isinstance(column, str):
            col_index = self.headers.index(column)
        else:
            col_index = column
        
        self.rows.sort(key=lambda r: r[col_index] if col_index < len(r) else None, reverse=reverse)
    
    def filter(self, column: Union[int, str], value: Any) -> 'MarkdownTable':
        """筛选表格"""
        if isinstance(column, str):
            col_index = self.headers.index(column)
        else:
            col_index = column
        
        filtered_rows = [row for row in self.rows 
                        if col_index < len(row) and row[col_index] == value]
        return MarkdownTable(self.headers.copy(), filtered_rows, self.aligns.copy())
    
    def transpose(self, new_header: str = "Column") -> 'MarkdownTable':
        """转置表格"""
        new_headers = [new_header] + [str(h) for h in self.headers]
        new_rows = []
        
        for i, old_header in enumerate(self.headers):
            row = [old_header] + [r[i] if i < len(r) else None for r in self.rows]
            new_rows.append(row)
        
        return MarkdownTable(new_headers, new_rows, [Align.LEFT] + self.aligns.copy())
    
    def merge(self, other: 'MarkdownTable', how: str = "vertical") -> 'MarkdownTable':
        """
        合并表格
        
        Args:
            other: 要合并的表格
            how: 合并方式，"vertical"垂直合并，"horizontal"水平合并
        """
        if how == "vertical":
            if self.headers != other.headers:
                raise ValueError("垂直合并需要相同的表头")
            return MarkdownTable(
                self.headers.copy(),
                self.rows + other.rows,
                self.aligns.copy()
            )
        elif how == "horizontal":
            new_headers = self.headers + other.headers
            max_rows = max(len(self.rows), len(other.rows))
            new_rows = []
            for i in range(max_rows):
                row1 = self.rows[i] if i < len(self.rows) else [None] * len(self.headers)
                row2 = other.rows[i] if i < len(other.rows) else [None] * len(other.headers)
                new_rows.append(row1 + row2)
            return MarkdownTable(
                new_headers,
                new_rows,
                self.aligns + other.aligns
            )
        else:
            raise ValueError(f"不支持的合并方式: {how}")
    
    def get_stats(self) -> Dict[str, Any]:
        """获取表格统计信息"""
        return {
            "rows": len(self.rows),
            "columns": len(self.headers),
            "headers": self.headers,
            "aligns": [a.value for a in self.aligns],
            "total_cells": len(self.rows) * len(self.headers),
            "non_empty_cells": sum(
                1 for row in self.rows 
                for i, cell in enumerate(row) 
                if cell is not None and str(cell).strip() and i < len(self.headers)
            )
        }


def generate_table(headers: List[str], rows: List[List[Any]], 
                   aligns: Optional[List[Align]] = None,
                   config: Optional[TableConfig] = None) -> str:
    """
    生成Markdown表格
    
    Args:
        headers: 表头列表
        rows: 数据行列表
        aligns: 每列对齐方式
        config: 表格配置
    
    Returns:
        Markdown格式的表格字符串
    """
    config = config or TableConfig()
    aligns = aligns or [Align.DEFAULT] * len(headers)
    
    # 计算每列最大宽度
    col_widths = _calculate_column_widths(headers, rows, config.min_col_width)
    
    # 生成表头行
    header_row = _generate_row(headers, col_widths, config.padding)
    
    # 生成分隔行
    separator_row = _generate_separator(col_widths, aligns, config.padding)
    
    # 生成数据行
    data_rows = [_generate_row(row, col_widths, config.padding) for row in rows]
    
    # 组合表格
    table_lines = [header_row, separator_row] + data_rows
    return "\n".join(table_lines)


def _calculate_column_widths(headers: List[str], rows: List[List[Any]], 
                             min_width: int) -> List[int]:
    """计算每列最大宽度"""
    widths = [len(str(h)) for h in headers]
    
    for row in rows:
        for i, cell in enumerate(row):
            if i < len(widths):
                widths[i] = max(widths[i], len(str(cell)))
    
    return [max(w, min_width) for w in widths]


def _generate_row(cells: List[Any], widths: List[int], padding: int) -> str:
    """生成一行"""
    padded_cells = []
    for i, cell in enumerate(cells):
        if i < len(widths):
            cell_str = str(cell) if cell is not None else ""
            padded_cells.append(" " * padding + cell_str.ljust(widths[i]) + " " * padding)
    return "|".join([""] + padded_cells + [""])


def _generate_separator(widths: List[int], aligns: List[Align], padding: int) -> str:
    """生成分隔行"""
    separators = []
    for i, width in enumerate(widths):
        align = aligns[i] if i < len(aligns) else Align.DEFAULT
        
        if align == Align.LEFT:
            sep = ":" + "-" * (width - 1 + padding * 2 - 1)
        elif align == Align.RIGHT:
            sep = "-" * (width - 1 + padding * 2 - 1) + ":"
        elif align == Align.CENTER:
            sep = ":" + "-" * (width - 1 + padding * 2 - 2) + ":"
        else:
            sep = "-" * (width + padding * 2)
        
        separators.append(sep)
    
    return "|".join([""] + separators + [""])


def parse_table(markdown: str) -> MarkdownTable:
    """
    解析Markdown表格
    
    Args:
        markdown: Markdown文本
    
    Returns:
        MarkdownTable对象
    """
    lines = markdown.strip().split("\n")
    
    # 过滤非表格行
    table_lines = [line for line in lines if line.strip().startswith("|")]
    
    if len(table_lines) < 2:
        raise ValueError("无效的Markdown表格：至少需要表头行和分隔行")
    
    # 解析表头
    headers = _parse_row(table_lines[0])
    
    # 解析对齐方式
    aligns = _parse_alignment(table_lines[1])
    
    # 解析数据行
    rows = [_parse_row(line) for line in table_lines[2:]]
    
    return MarkdownTable(headers, rows, aligns)


def _parse_row(line: str) -> List[str]:
    """解析表格行"""
    cells = line.split("|")
    # 移除首尾空元素
    cells = [c.strip() for c in cells[1:-1] if c.strip() != "" or cells.index(c) not in [0, len(cells)-1]]
    return [c.strip() for c in line.split("|")[1:-1]]


def _parse_alignment(line: str) -> List[Align]:
    """解析对齐方式"""
    aligns = []
    cells = line.split("|")[1:-1]
    
    for cell in cells:
        cell = cell.strip()
        if cell.startswith(":") and cell.endswith(":"):
            aligns.append(Align.CENTER)
        elif cell.endswith(":"):
            aligns.append(Align.RIGHT)
        elif cell.startswith(":"):
            aligns.append(Align.LEFT)
        else:
            aligns.append(Align.DEFAULT)
    
    return aligns


def from_dict_list(data: List[Dict[str, Any]], 
                   columns: Optional[List[str]] = None,
                   aligns: Optional[List[Align]] = None) -> MarkdownTable:
    """
    从字典列表创建表格
    
    Args:
        data: 字典列表
        columns: 要显示的列（字典键），默认为所有键
        aligns: 对齐方式
    
    Returns:
        MarkdownTable对象
    """
    if not data:
        raise ValueError("数据不能为空")
    
    # 确定列
    if columns is None:
        columns = list(data[0].keys())
    
    # 提取数据
    rows = [[d.get(col) for col in columns] for d in data]
    
    return MarkdownTable(columns, rows, aligns)


def from_csv(csv_content: str, delimiter: str = ",", 
             has_header: bool = True) -> MarkdownTable:
    """
    从CSV内容创建表格
    
    Args:
        csv_content: CSV文本内容
        delimiter: 分隔符
        has_header: 是否包含表头
    
    Returns:
        MarkdownTable对象
    """
    lines = csv_content.strip().split("\n")
    
    if not lines:
        raise ValueError("CSV内容不能为空")
    
    # 解析CSV行
    rows = [_parse_csv_row(line, delimiter) for line in lines]
    
    if has_header:
        headers = rows[0]
        data_rows = rows[1:]
    else:
        headers = [f"Col{i+1}" for i in range(len(rows[0]))]
        data_rows = rows
    
    return MarkdownTable(headers, data_rows)


def _parse_csv_row(line: str, delimiter: str) -> List[str]:
    """解析CSV行"""
    cells = []
    current = ""
    in_quotes = False
    
    for char in line:
        if char == '"':
            in_quotes = not in_quotes
        elif char == delimiter and not in_quotes:
            cells.append(current.strip())
            current = ""
        else:
            current += char
    
    cells.append(current.strip())
    return cells


def find_tables(markdown: str) -> List[MarkdownTable]:
    """
    从Markdown文本中提取所有表格
    
    Args:
        markdown: Markdown文本
    
    Returns:
        MarkdownTable对象列表
    """
    lines = markdown.split("\n")
    tables = []
    current_table_lines = []
    in_table = False
    
    for line in lines:
        if "|" in line and line.strip().startswith("|"):
            current_table_lines.append(line)
            in_table = True
        elif in_table and current_table_lines:
            # 表格结束
            if len(current_table_lines) >= 2:
                try:
                    table = parse_table("\n".join(current_table_lines))
                    tables.append(table)
                except ValueError:
                    pass
            current_table_lines = []
            in_table = False
    
    # 处理最后一个表格
    if current_table_lines and len(current_table_lines) >= 2:
        try:
            table = parse_table("\n".join(current_table_lines))
            tables.append(table)
        except ValueError:
            pass
    
    return tables


def compare_tables(table1: MarkdownTable, table2: MarkdownTable) -> Dict[str, Any]:
    """
    比较两个表格
    
    Args:
        table1: 第一个表格
        table2: 第二个表格
    
    Returns:
        比较结果字典
    """
    return {
        "same_headers": table1.headers == table2.headers,
        "same_dimensions": len(table1.rows) == len(table2.rows) and len(table1.headers) == len(table2.headers),
        "row_count_diff": len(table2.rows) - len(table1.rows),
        "column_count_diff": len(table2.headers) - len(table1.headers),
        "table1_stats": table1.get_stats(),
        "table2_stats": table2.get_stats()
    }


def align_column(align: Align) -> str:
    """获取对齐标记"""
    if align == Align.LEFT:
        return ":---"
    elif align == Align.RIGHT:
        return "---:"
    elif align == Align.CENTER:
        return ":---:"
    else:
        return "---"


# 便捷函数
def table(headers: List[str], rows: List[List[Any]], 
          aligns: Optional[List[Align]] = None) -> str:
    """快速生成Markdown表格"""
    return generate_table(headers, rows, aligns)


def dict_table(data: List[Dict[str, Any]], 
               columns: Optional[List[str]] = None) -> str:
    """从字典列表生成Markdown表格"""
    t = from_dict_list(data, columns)
    return t.to_markdown()


def csv_table(csv_content: str, delimiter: str = ",") -> str:
    """从CSV生成Markdown表格"""
    t = from_csv(csv_content, delimiter)
    return t.to_markdown()