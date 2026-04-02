#!/usr/bin/env python3
"""基于现有内容重新生成规范的大纲"""

import re
import csv
import sys
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass, field


@dataclass
class Chapter:
    """章节数据类"""
    num: int
    title: str = ''
    time: str = ''
    location: str = ''
    scene: str = ''
    emotion: str = ''
    events: List[str] = field(default_factory=list)
    props: str = ''
    foreshadowing: str = ''
    climax: str = ''
    hook: str = ''
    key_info: str = ''

    def to_csv_row(self) -> List[str]:
        """转换为CSV行数据"""
        return [
            str(self.num),
            self.time,
            self.location,
            self.scene,
            self.emotion,
            ' '.join(self.events),
            self.props,
            self.foreshadowing,
            self.climax,
            '',  # 前章钩子
            self.hook,
            '',  # 后章预告
            self.key_info
        ]


# 字段映射配置
FIELD_MAPPING: Dict[str, str] = {
    '时间': 'time',
    '地点': 'location',
    '场景': 'scene',
    '情绪': 'emotion',
    '关键道具': 'props',
    '伏笔': 'foreshadowing',
    '爽点': 'climax',
    '钩子': 'hook',
    '关键信息标记': 'key_info',
}


def parse_chapter_title(line: str) -> Optional[tuple[int, str]]:
    """解析章节标题，返回(章节号, 标题)"""
    if not (line.startswith('**第') and '章：' in line and line.endswith('**')):
        return None

    match = re.search(r'\*\*第(\d+)章：(.+?)\*\*', line)
    if match:
        return int(match.group(1)), match.group(2)
    return None


def parse_field_line(line: str) -> Optional[tuple[str, str]]:
    """解析字段行，返回(字段名, 值)"""
    match = re.match(r'- \*\*(.+?)\*\*：(.+)', line)
    if match:
        return match.group(1), match.group(2).strip()
    return None


def is_event_line(line: str) -> bool:
    """判断是否为事件列表行（1. 2. 3. 开头）"""
    return bool(re.match(r'^\d+\.', line.strip()))


def extract_chapters(content: str) -> Dict[int, Chapter]:
    """从内容中提取所有章节信息"""
    lines = content.split('\n')
    chapters: Dict[int, Chapter] = {}
    current: Optional[Chapter] = None

    i = 0
    while i < len(lines):
        line = lines[i].strip()

        # 匹配章节标题
        chapter_info = parse_chapter_title(line)
        if chapter_info:
            ch_num, ch_title = chapter_info
            if ch_num not in chapters:  # 只保留第一次出现的
                chapters[ch_num] = Chapter(num=ch_num, title=ch_title)
                current = chapters[ch_num]
            i += 1
            continue

        if current is None:
            i += 1
            continue

        # 匹配字段
        field_info = parse_field_line(line)
        if field_info:
            field_name, field_value = field_info

            if field_name == '核心事件':
                # 收集后续的事件列表行
                i += 1
                while i < len(lines) and is_event_line(lines[i]):
                    current.events.append(lines[i].strip())
                    i += 1
                continue

            # 映射到其他字段
            if field_name in FIELD_MAPPING:
                setattr(current, FIELD_MAPPING[field_name], field_value)

        i += 1

    return chapters


def generate_csv(chapters: Dict[int, Chapter], output_path: Path) -> None:
    """生成CSV文件"""
    headers = [
        '章节', '时间', '地点', '场景描述', '情绪基调', '核心事件',
        '关键道具', '伏笔操作', '爽点', '前章钩子', '本章钩子',
        '后章预告', '关键信息标记'
    ]

    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(headers)

        for i in range(1, 101):
            if i in chapters:
                writer.writerow(chapters[i].to_csv_row())


def generate_climax_md(chapters: Dict[int, Chapter], output_path: Path) -> None:
    """生成爽点节奏表"""
    lines = [
        "# 《下班后别找我》爽点节奏表\n",
        "| 章节 | 爽点类型 | 内容 | 压抑铺垫 |",
        "|------|---------|------|---------|"
    ]

    for i in range(1, 101):
        if i in chapters and chapters[i].climax:
            ch = chapters[i]
            content = ch.climax[:50] + '...' if len(ch.climax) > 50 else ch.climax
            lines.append(f"| {i} | - | {content} | - |")

    output_path.write_text('\n'.join(lines), encoding='utf-8')


def main() -> int:
    """主函数"""
    base_path = Path('/home/admin/.openclaw/workspace/novel-ideas/下班后别找我_2026-03-08')
    input_path = base_path / '大纲.md.bak'
    csv_path = base_path / '章节规划表.csv'
    md_path = base_path / '爽点节奏表.md'

    if not input_path.exists():
        print(f"错误：输入文件不存在 {input_path}", file=sys.stderr)
        return 1

    try:
        content = input_path.read_text(encoding='utf-8')
        chapters = extract_chapters(content)
        print(f"提取到 {len(chapters)} 个唯一章节")

        generate_csv(chapters, csv_path)
        print(f"章节规划表.csv 生成完成：{csv_path}")

        generate_climax_md(chapters, md_path)
        print(f"爽点节奏表.md 生成完成：{md_path}")

        print("\n完成！")
        return 0

    except Exception as e:
        print(f"错误：{e}", file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
