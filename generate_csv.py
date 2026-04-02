#!/usr/bin/env python3
"""从大纲.md提取章节信息生成CSV"""

import re
import csv
import sys
from pathlib import Path
from typing import Dict, List, Optional


def parse_chapter_line(line: str) -> Optional[Dict[str, str]]:
    """解析章节标题行，提取章节号和标题"""
    match = re.search(r'\*\*第(\d+)章：(.+?)\*\*', line)
    if match:
        return {'章节': match.group(1), '标题': match.group(2)}
    return None


def parse_field_line(line: str, field_name: str) -> Optional[str]:
    """解析字段行，如 '- **时间**：xxx'"""
    prefix = f'- **{field_name}**：'
    if line.startswith(prefix):
        return line[len(prefix):].strip()
    return None


def parse_events(lines: List[str], start_idx: int) -> List[str]:
    """解析核心事件列表（1. 2. 3. 4. 开头的行）"""
    events = []
    for j in range(start_idx, len(lines)):
        stripped = lines[j].strip()
        if re.match(r'^\d+\.', stripped):
            events.append(stripped)
        else:
            break
    return events


def extract_chapters(content: str) -> List[Dict[str, str]]:
    """从大纲内容中提取所有章节信息"""
    lines = content.split('\n')
    chapters: List[Dict[str, str]] = []
    current: Dict[str, str] = {}

    field_mapping = {
        '时间': '时间',
        '地点': '地点',
        '场景': '场景描述',
        '情绪': '情绪基调',
        '关键道具': '关键道具',
        '伏笔': '伏笔操作',
        '爽点': '爽点',
        '钩子': '本章钩子',
        '关键信息标记': '关键信息标记',
    }

    i = 0
    while i < len(lines):
        line = lines[i].strip()

        # 匹配章节标题
        if line.startswith('**第') and '章：' in line:
            if current and '章节' in current:
                chapters.append(current)
            parsed = parse_chapter_line(line)
            if parsed:
                current = parsed
            else:
                current = {}
            i += 1
            continue

        # 匹配核心事件（需要向前看）
        if line.startswith('- **核心事件**：') and current:
            events = parse_events(lines, i + 1)
            current['核心事件'] = ' '.join(events)
            i += len(events) + 1
            continue

        # 匹配其他字段
        for src_field, dst_field in field_mapping.items():
            value = parse_field_line(line, src_field)
            if value is not None and current:
                current[dst_field] = value
                break

        i += 1

    # 添加最后一章
    if current and '章节' in current:
        chapters.append(current)

    return chapters


def write_csv(chapters: List[Dict[str, str]], output_path: Path) -> None:
    """将章节信息写入CSV文件"""
    headers = [
        '章节', '时间', '地点', '场景描述', '情绪基调', '核心事件',
        '关键道具', '伏笔操作', '爽点', '前章钩子', '本章钩子',
        '后章预告', '关键信息标记'
    ]

    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(headers)

        for ch in chapters:
            writer.writerow([
                ch.get('章节', ''),
                ch.get('时间', ''),
                ch.get('地点', ''),
                ch.get('场景描述', ''),
                ch.get('情绪基调', ''),
                ch.get('核心事件', ''),
                ch.get('关键道具', ''),
                ch.get('伏笔操作', ''),
                ch.get('爽点', ''),
                '',  # 前章钩子
                ch.get('本章钩子', ''),
                '',  # 后章预告
                ch.get('关键信息标记', '')
            ])


def main() -> int:
    """主函数"""
    base_path = Path('/home/admin/.openclaw/workspace/novel-ideas/下班后别找我_2026-03-08')
    input_path = base_path / '大纲.md'
    output_path = base_path / '章节规划表.csv'

    if not input_path.exists():
        print(f"错误：输入文件不存在 {input_path}", file=sys.stderr)
        return 1

    try:
        content = input_path.read_text(encoding='utf-8')
        chapters = extract_chapters(content)
        print(f"提取到 {len(chapters)} 章")

        write_csv(chapters, output_path)
        print(f"CSV生成完成：{output_path}")
        return 0

    except Exception as e:
        print(f"错误：{e}", file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
