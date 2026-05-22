"""
中文文本对齐工具 (Chinese Text Alignment Utils)

提供中文文本的对齐显示功能，支持：
- 全角/半角字符混合对齐
- 中英文混合文本对齐
- 表格格式化输出
- 文本宽度计算（考虑中英文字符宽度差异）

零外部依赖，纯 Python 实现。
"""

from typing import List, Tuple, Optional, Union


def get_display_width(char: str) -> int:
    """
    计算单个字符的显示宽度
    
    中文字符、全角字符宽度为2，ASCII字符宽度为1
    
    Args:
        char: 单个字符
        
    Returns:
        显示宽度（1或2）
    """
    if not char:
        return 0
    
    code = ord(char)
    
    # ASCII 控制字符（宽度0）
    if code < 32 or 127 <= code < 160:
        return 0
    
    # ASCII 字符和半角字符（宽度1）
    if code < 127:
        return 1
    
    # 中文标点符号（宽度2）
    # 中文标点范围：\u3000-\u303F, \uFF00-\uFFEF
    if 0x3000 <= code <= 0x303F:
        return 2
    
    # 全角字符（宽度2）
    if 0xFF00 <= code <= 0xFFEF:
        # 全角 ASCII 字符
        if 0xFF01 <= code <= 0xFF5E:
            return 2
        # 全角空格
        if code == 0x3000:
            return 2
        return 2
    
    # CJK 统一汉字（宽度2）
    if 0x4E00 <= code <= 0x9FFF:
        return 2
    
    # CJK 扩展A区
    if 0x3400 <= code <= 0x4DBF:
        return 2
    
    # CJK 扩展B-I区
    if 0x20000 <= code <= 0x323AF:
        return 2
    
    # 其他字符默认宽度1
    return 1


def text_width(text: str) -> int:
    """
    计算字符串的显示宽度
    
    Args:
        text: 输入字符串
        
    Returns:
        总显示宽度
    """
    return sum(get_display_width(char) for char in text)


def pad_left(text: str, width: int, fillchar: str = ' ') -> str:
    """
    左填充使文本达到指定显示宽度
    
    Args:
        text: 原文本
        width: 目标宽度
        fillchar: 填充字符
        
    Returns:
        填充后的文本
    """
    current_width = text_width(text)
    if current_width >= width:
        return text
    
    fill_width = get_display_width(fillchar)
    if fill_width == 0:
        return text
    
    padding_count = (width - current_width) // fill_width
    return fillchar * padding_count + text


def pad_right(text: str, width: int, fillchar: str = ' ') -> str:
    """
    右填充使文本达到指定显示宽度
    
    Args:
        text: 原文本
        width: 目标宽度
        fillchar: 填充字符
        
    Returns:
        填充后的文本
    """
    current_width = text_width(text)
    if current_width >= width:
        return text
    
    fill_width = get_display_width(fillchar)
    if fill_width == 0:
        return text
    
    padding_count = (width - current_width) // fill_width
    return text + fillchar * padding_count


def pad_center(text: str, width: int, fillchar: str = ' ') -> str:
    """
    居中填充使文本达到指定显示宽度
    
    Args:
        text: 原文本
        width: 目标宽度
        fillchar: 填充字符
        
    Returns:
        填充后的文本
    """
    current_width = text_width(text)
    if current_width >= width:
        return text
    
    fill_width = get_display_width(fillchar)
    if fill_width == 0:
        return text
    
    total_padding = width - current_width
    # 左侧填充稍微多一点（奇数时）
    left_count = (total_padding + 1) // 2 // fill_width
    right_count = (total_padding // 2) // fill_width
    
    return fillchar * left_count + text + fillchar * right_count


def truncate(text: str, max_width: int, suffix: str = '...') -> str:
    """
    截断文本以适应指定显示宽度
    
    Args:
        text: 原文本
        max_width: 最大显示宽度
        suffix: 截断后缀
        
    Returns:
        截断后的文本
    """
    if text_width(text) <= max_width:
        return text
    
    suffix_width = text_width(suffix)
    if suffix_width >= max_width:
        return suffix[:max_width]
    
    target_width = max_width - suffix_width
    result = []
    current_width = 0
    
    for char in text:
        char_width = get_display_width(char)
        if current_width + char_width > target_width:
            break
        result.append(char)
        current_width += char_width
    
    return ''.join(result) + suffix


def align_columns(
    rows: List[List[str]],
    widths: Optional[List[int]] = None,
    align: Union[str, List[str]] = 'left',
    sep: str = ' | ',
    header_sep: str = '-',
    show_header_line: bool = True
) -> str:
    """
    对齐多列文本并格式化为表格
    
    Args:
        rows: 数据行列表，每行是一个字符串列表
        widths: 各列宽度，None 则自动计算
        align: 对齐方式 ('left', 'right', 'center') 或各列对齐方式列表
        sep: 列分隔符
        header_sep: 表头分隔线字符
        show_header_line: 是否显示表头分隔线
        
    Returns:
        格式化后的表格字符串
    """
    if not rows:
        return ''
    
    num_cols = max(len(row) for row in rows)
    
    # 补齐列数
    padded_rows = []
    for row in rows:
        padded_row = list(row) + [''] * (num_cols - len(row))
        padded_rows.append(padded_row)
    
    # 计算各列宽度
    if widths is None:
        col_widths = []
        for col_idx in range(num_cols):
            max_width = max(text_width(row[col_idx]) for row in padded_rows)
            col_widths.append(max_width)
    else:
        col_widths = list(widths) + [10] * (num_cols - len(widths))
    
    # 处理对齐方式
    if isinstance(align, str):
        aligns = [align] * num_cols
    else:
        aligns = list(align) + ['left'] * (num_cols - len(align))
    
    def format_cell(text: str, width: int, align_mode: str) -> str:
        if align_mode == 'right':
            return pad_left(text, width)
        elif align_mode == 'center':
            return pad_center(text, width)
        else:
            return pad_right(text, width)
    
    # 格式化各行
    result_lines = []
    for row_idx, row in enumerate(padded_rows):
        formatted_cells = [
            format_cell(cell, col_widths[i], aligns[i])
            for i, cell in enumerate(row)
        ]
        result_lines.append(sep.join(formatted_cells))
        
        # 在第一行后添加分隔线
        if show_header_line and row_idx == 0:
            separator_parts = []
            for i, width in enumerate(col_widths):
                # 根据填充字符计算分隔线
                sep_char = header_sep
                if get_display_width(sep_char) == 1:
                    separator_parts.append(sep_char * width)
                else:
                    # 如果是全角字符，需要减半
                    separator_parts.append(sep_char * (width // 2 + width % 2))
            result_lines.append(sep.join(separator_parts))
    
    return '\n'.join(result_lines)


def align_bilingual(
    chinese: str,
    english: str,
    mode: str = 'parallel',
    width: int = 80,
    gap: int = 4
) -> str:
    """
    对齐中英文双语文本
    
    Args:
        chinese: 中文文本
        english: 英文文本
        mode: 对齐模式
            - 'parallel': 并排显示
            - 'interleaved': 交错显示
            - 'block': 块状显示
        width: 总宽度
        gap: 中英文间隔
        
    Returns:
        对齐后的文本
    """
    cn_lines = chinese.strip().split('\n')
    en_lines = english.strip().split('\n')
    
    if mode == 'parallel':
        # 并排显示
        cn_width = (width - gap) // 2
        en_width = width - gap - cn_width
        
        max_lines = max(len(cn_lines), len(en_lines))
        result = []
        
        for i in range(max_lines):
            cn_line = cn_lines[i] if i < len(cn_lines) else ''
            en_line = en_lines[i] if i < len(en_lines) else ''
            
            cn_truncated = truncate(cn_line, cn_width)
            en_truncated = truncate(en_line, en_width)
            
            result.append(
                pad_right(cn_truncated, cn_width) + ' ' * gap + pad_right(en_truncated, en_width)
            )
        
        return '\n'.join(result)
    
    elif mode == 'interleaved':
        # 交错显示
        result = []
        max_lines = max(len(cn_lines), len(en_lines))
        
        for i in range(max_lines):
            if i < len(cn_lines):
                result.append(cn_lines[i])
            if i < len(en_lines):
                result.append(en_lines[i])
            if i < max_lines - 1:
                result.append('')  # 添加空行分隔
        
        return '\n'.join(result)
    
    else:  # block
        # 块状显示
        return f"【中文】\n{chinese}\n\n【English】\n{english}"


def create_progress_bar(
    current: int,
    total: int,
    width: int = 40,
    fill: str = '█',
    empty: str = '░',
    show_percent: bool = True
) -> str:
    """
    创建支持中文显示的进度条
    
    Args:
        current: 当前进度
        total: 总量
        width: 进度条宽度（字符数）
        fill: 填充字符
        empty: 空白字符
        show_percent: 是否显示百分比
        
    Returns:
        进度条字符串
    """
    if total == 0:
        percent = 100
    else:
        percent = min(100, int(current * 100 / total))
    
    fill_width = percent * width // 100
    empty_width = width - fill_width
    
    bar = fill * fill_width + empty * empty_width
    
    if show_percent:
        return f"[{bar}] {percent:3d}%"
    return f"[{bar}]"


def wrap_text(text: str, width: int = 80, indent: str = '') -> str:
    """
    按显示宽度换行文本（支持中英文混合）
    
    Args:
        text: 输入文本
        width: 最大显示宽度
        indent: 缩进字符串
        
    Returns:
        换行后的文本
    """
    if not text:
        return text
    
    indent_width = text_width(indent)
    available_width = width - indent_width
    
    if available_width <= 0:
        return text
    
    # 判断是否是纯英文文本（按空格分词） - Python 3.6兼容方式
    def is_ascii_or_space(c):
        return ord(c) < 128 or c.isspace()
    
    is_english_text = all(is_ascii_or_space(c) for c in text)
    
    lines = []
    current_line = []
    current_width = 0
    
    # 英文按空格分词，中文按字符分
    words = text.split() if is_english_text else list(text)
    
    for word in words:
        if not word:  # 空词跳过
            continue
            
        word_width = text_width(word)
        
        # 如果单个词/字符就超过宽度，需要逐字符处理
        if word_width > available_width:
            # 先提交当前行
            if current_line:
                lines.append(indent + ''.join(current_line))
                current_line = []
                current_width = 0
            
            # 逐字符处理超长词
            for char in word:
                char_width = get_display_width(char)
                if current_width + char_width > available_width:
                    lines.append(indent + ''.join(current_line))
                    current_line = [char]
                    current_width = char_width
                else:
                    current_line.append(char)
                    current_width += char_width
        
        # 检查是否需要换行（英文需要考虑空格）
        elif current_width + word_width + (1 if current_line and is_english_text else 0) > available_width:
            lines.append(indent + ''.join(current_line))
            current_line = [word]
            current_width = word_width
        
        # 添加到当前行
        else:
            if current_line and is_english_text:
                current_line.append(' ')
                current_width += 1
            current_line.append(word)
            current_width += word_width
    
    # 提交最后一行
    if current_line:
        lines.append(indent + ''.join(current_line))
    
    return '\n'.join(lines)


def split_by_width(text: str, width: int) -> List[str]:
    """
    按显示宽度分割文本
    
    Args:
        text: 输入文本
        width: 每段的最大宽度
        
    Returns:
        分割后的文本列表
    """
    if width <= 0:
        return [text]
    
    segments = []
    current_segment = []
    current_width = 0
    
    for char in text:
        char_width = get_display_width(char)
        if current_width + char_width > width:
            if current_segment:
                segments.append(''.join(current_segment))
            current_segment = [char]
            current_width = char_width
        else:
            current_segment.append(char)
            current_width += char_width
    
    if current_segment:
        segments.append(''.join(current_segment))
    
    return segments


class ChineseTextAligner:
    """
    中文文本对齐器类
    
    提供链式调用接口进行文本对齐操作
    """
    
    def __init__(self, text: str = ''):
        self._text = text
        self._width = 80
        self._indent = ''
    
    def width(self, width: int) -> 'ChineseTextAligner':
        """设置宽度"""
        self._width = width
        return self
    
    def indent(self, indent: str) -> 'ChineseTextAligner':
        """设置缩进"""
        self._indent = indent
        return self
    
    def pad_left(self, fillchar: str = ' ') -> str:
        """左填充"""
        return pad_left(self._text, self._width, fillchar)
    
    def pad_right(self, fillchar: str = ' ') -> str:
        """右填充"""
        return pad_right(self._text, self._width, fillchar)
    
    def pad_center(self, fillchar: str = ' ') -> str:
        """居中填充"""
        return pad_center(self._text, self._width, fillchar)
    
    def truncate(self, suffix: str = '...') -> str:
        """截断"""
        return truncate(self._text, self._width, suffix)
    
    def wrap(self) -> str:
        """换行"""
        return wrap_text(self._text, self._width, self._indent)


def format_table(
    headers: List[str],
    rows: List[List[str]],
    title: Optional[str] = None,
    border: bool = True,
    padding: int = 1
) -> str:
    """
    格式化表格（支持中英文混合）
    
    Args:
        headers: 表头
        rows: 数据行
        title: 表格标题
        border: 是否显示边框
        padding: 单元格内边距
        
    Returns:
        格式化后的表格字符串
    """
    if not headers and not rows:
        return ''
    
    # 合并表头和数据
    all_rows = [headers] + rows if headers else rows
    
    # 计算列数和列宽
    num_cols = max(len(row) for row in all_rows)
    col_widths = [0] * num_cols
    
    for row in all_rows:
        for i, cell in enumerate(row):
            col_widths[i] = max(col_widths[i], text_width(str(cell)))
    
    # 添加内边距
    cell_padding = ' ' * padding
    content_widths = [w + padding * 2 for w in col_widths]
    
    # 构建边框字符
    if border:
        # 根据内容宽度调整边框字符
        h_border = '─'
        v_border = '│'
        tl_corner = '┌'
        tr_corner = '┐'
        bl_corner = '└'
        br_corner = '┘'
        cross_t = '┬'
        cross_b = '┴'
        cross_l = '├'
        cross_r = '┤'
        cross_center = '┼'
    else:
        h_border = v_border = tl_corner = tr_corner = ''
        bl_corner = br_corner = cross_t = cross_b = ''
        cross_l = cross_r = cross_center = ''
    
    result = []
    
    # 标题
    if title:
        title_width = sum(content_widths) + (num_cols - 1) * 3
        if border:
            result.append('┌' + '─' * (title_width + 2) + '┐')
            result.append('│' + pad_center(title, title_width + 2) + '│')
        else:
            result.append(pad_center(title, sum(content_widths)))
    
    # 顶部边框
    if border:
        top = tl_corner + cross_t.join(h_border * w for w in content_widths) + tr_corner
        result.append(top)
    
    # 数据行
    for row_idx, row in enumerate(all_rows):
        # 补齐列数
        padded_row = list(row) + [''] * (num_cols - len(row))
        
        # 格式化单元格
        cells = []
        for i, cell in enumerate(padded_row):
            cell_str = str(cell)
            cells.append(cell_padding + pad_right(cell_str, col_widths[i]) + cell_padding)
        
        if border:
            result.append(v_border + v_border.join(cells) + v_border)
        else:
            result.append(' '.join(cells))
        
        # 表头分隔线
        if row_idx == 0 and border and headers:
            sep = cross_l + cross_center.join(h_border * w for w in content_widths) + cross_r
            result.append(sep)
    
    # 底部边框
    if border:
        bottom = bl_corner + cross_b.join(h_border * w for w in content_widths) + br_corner
        result.append(bottom)
    
    return '\n'.join(result)


# 便捷函数
def ljust(text: str, width: int, fillchar: str = ' ') -> str:
    """左对齐（等同于 pad_right）"""
    return pad_right(text, width, fillchar)


def rjust(text: str, width: int, fillchar: str = ' ') -> str:
    """右对齐（等同于 pad_left）"""
    return pad_left(text, width, fillchar)


def center(text: str, width: int, fillchar: str = ' ') -> str:
    """居中对齐（等同于 pad_center）"""
    return pad_center(text, width, fillchar)