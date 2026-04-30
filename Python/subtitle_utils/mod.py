"""
Subtitle Utils - 字幕解析与处理工具

支持格式:
- SRT (SubRip)
- VTT (WebVTT)
- ASS/SSA (Advanced SubStation Alpha)

功能:
- 解析与生成字幕文件
- 时间轴调整 (延迟/提前)
- 字幕合并与分割
- 格式转换
- 字幕过滤

零外部依赖，纯 Python 实现
"""

from dataclasses import dataclass, field
from typing import List, Optional, Tuple, Iterator, Union
from datetime import timedelta
import re
import html


@dataclass
class SubtitleEntry:
    """字幕条目"""
    index: int
    start: timedelta
    end: timedelta
    text: str
    
    @property
    def duration(self) -> timedelta:
        """字幕持续时间"""
        return self.end - self.start
    
    def shift(self, delta: timedelta) -> 'SubtitleEntry':
        """时间轴偏移"""
        return SubtitleEntry(
            index=self.index,
            start=self.start + delta,
            end=self.end + delta,
            text=self.text
        )
    
    def is_valid(self) -> bool:
        """检查字幕有效性"""
        return self.start < self.end and bool(self.text.strip())


class SRTParser:
    """SRT 字幕解析器"""
    
    # SRT 时间格式: 00:00:00,000 --> 00:00:00,000
    TIME_PATTERN = re.compile(
        r'(\d{2}):(\d{2}):(\d{2})[,.](\d{3})'
    )
    
    @classmethod
    def parse_time(cls, time_str: str) -> timedelta:
        """解析 SRT 时间字符串"""
        match = cls.TIME_PATTERN.match(time_str.strip())
        if not match:
            raise ValueError(f"Invalid SRT time format: {time_str}")
        
        hours, minutes, seconds, millis = map(int, match.groups())
        return timedelta(
            hours=hours,
            minutes=minutes,
            seconds=seconds,
            milliseconds=millis
        )
    
    @classmethod
    def format_time(cls, td: timedelta) -> str:
        """格式化为 SRT 时间字符串"""
        total_seconds = int(td.total_seconds())
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        millis = td.microseconds // 1000
        return f"{hours:02d}:{minutes:02d}:{seconds:02d},{millis:03d}"
    
    @classmethod
    def parse(cls, content: str) -> List[SubtitleEntry]:
        """解析 SRT 内容"""
        entries = []
        blocks = re.split(r'\n\s*\n', content.strip())
        
        for block in blocks:
            block = block.strip()
            if not block:
                continue
            
            lines = block.split('\n')
            if len(lines) < 2:
                continue
            
            # 解析序号
            try:
                index = int(lines[0].strip())
            except ValueError:
                continue
            
            # 解析时间轴
            time_line = lines[1].strip()
            if '-->' not in time_line:
                continue
            
            time_parts = time_line.split('-->')
            if len(time_parts) != 2:
                continue
            
            try:
                start = cls.parse_time(time_parts[0])
                end = cls.parse_time(time_parts[1])
            except ValueError:
                continue
            
            # 解析文本 (可能有多行)
            text = '\n'.join(lines[2:]).strip()
            
            entries.append(SubtitleEntry(
                index=index,
                start=start,
                end=end,
                text=text
            ))
        
        return entries
    
    @classmethod
    def generate(cls, entries: List[SubtitleEntry]) -> str:
        """生成 SRT 内容"""
        lines = []
        for entry in entries:
            lines.append(str(entry.index))
            lines.append(f"{cls.format_time(entry.start)} --> {cls.format_time(entry.end)}")
            lines.append(entry.text)
            lines.append('')
        
        return '\n'.join(lines)


class VTTParser:
    """WebVTT 字幕解析器"""
    
    # VTT 时间格式: 00:00:00.000 或 00:00.000
    TIME_PATTERN = re.compile(
        r'(?:(\d{2}):)?(\d{2}):(\d{2})\.(\d{3})'
    )
    
    @classmethod
    def parse_time(cls, time_str: str) -> timedelta:
        """解析 VTT 时间字符串"""
        match = cls.TIME_PATTERN.match(time_str.strip())
        if not match:
            raise ValueError(f"Invalid VTT time format: {time_str}")
        
        hours, minutes, seconds, millis = match.groups()
        hours = int(hours) if hours else 0
        minutes = int(minutes)
        seconds = int(seconds)
        millis = int(millis)
        
        return timedelta(
            hours=hours,
            minutes=minutes,
            seconds=seconds,
            milliseconds=millis
        )
    
    @classmethod
    def format_time(cls, td: timedelta) -> str:
        """格式化为 VTT 时间字符串"""
        total_seconds = int(td.total_seconds())
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        millis = td.microseconds // 1000
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}.{millis:03d}"
    
    @classmethod
    def parse(cls, content: str) -> Tuple[List[SubtitleEntry], dict]:
        """解析 VTT 内容，返回字幕列表和头部元数据"""
        entries = []
        metadata = {}
        
        lines = content.split('\n')
        
        # 检查 WEBVTT 头
        if not lines[0].startswith('WEBVTT'):
            raise ValueError("Invalid VTT file: missing WEBVTT header")
        
        # 解析头部元数据
        i = 1
        while i < len(lines) and lines[i].strip() and '-->' not in lines[i]:
            line = lines[i].strip()
            if ':' in line:
                key, value = line.split(':', 1)
                metadata[key.strip()] = value.strip()
            i += 1
        
        # 解析字幕块
        current_index = 1
        while i < len(lines):
            line = lines[i].strip()
            
            # 跳过空行
            if not line:
                i += 1
                continue
            
            # 检查时间轴
            if '-->' in line:
                time_parts = line.split('-->')
                if len(time_parts) >= 2:
                    try:
                        start = cls.parse_time(time_parts[0])
                        # 处理可能的额外参数 (如 position:50%)
                        end_str = time_parts[1].split()[0]
                        end = cls.parse_time(end_str)
                        
                        # 收集文本
                        i += 1
                        text_lines = []
                        while i < len(lines) and lines[i].strip() and '-->' not in lines[i]:
                            text_lines.append(lines[i].strip())
                            i += 1
                        
                        text = '\n'.join(text_lines)
                        # 移除 VTT 标签
                        text = cls._strip_vtt_tags(text)
                        
                        entries.append(SubtitleEntry(
                            index=current_index,
                            start=start,
                            end=end,
                            text=text
                        ))
                        current_index += 1
                    except ValueError:
                        i += 1
                        continue
            else:
                i += 1
        
        return entries, metadata
    
    @classmethod
    def _strip_vtt_tags(cls, text: str) -> str:
        """移除 VTT 标签 (<b>, <i>, <c>, 等)"""
        # 移除语音标签 <v ...>
        text = re.sub(r'<v[^>]*>', '', text)
        # 移除类标签 <c.classname>
        text = re.sub(r'<c\.?[^>]*>', '', text)
        # 保留基本格式标签的内容，但移除标签本身
        text = re.sub(r'</?[biu]>', '', text)
        return text.strip()
    
    @classmethod
    def generate(cls, entries: List[SubtitleEntry], metadata: Optional[dict] = None) -> str:
        """生成 VTT 内容"""
        lines = ['WEBVTT']
        
        # 添加元数据
        if metadata:
            for key, value in metadata.items():
                lines.append(f"{key}: {value}")
        
        lines.append('')
        
        for entry in entries:
            lines.append(f"{cls.format_time(entry.start)} --> {cls.format_time(entry.end)}")
            lines.append(entry.text)
            lines.append('')
        
        return '\n'.join(lines)


class ASSParser:
    """ASS/SSA 字幕解析器 (基础支持)"""
    
    STYLE_PATTERN = re.compile(r'Style:\s*(.+)')
    DIALOGUE_PATTERN = re.compile(r'Dialogue:\s*(.+)')
    
    @classmethod
    def parse_time(cls, time_str: str) -> timedelta:
        """解析 ASS 时间格式 (H:MM:SS.CS)"""
        parts = time_str.strip().split(':')
        if len(parts) != 3:
            raise ValueError(f"Invalid ASS time format: {time_str}")
        
        hours = int(parts[0])
        minutes = int(parts[1])
        sec_parts = parts[2].split('.')
        seconds = int(sec_parts[0])
        centis = int(sec_parts[1]) if len(sec_parts) > 1 else 0
        
        return timedelta(
            hours=hours,
            minutes=minutes,
            seconds=seconds,
            milliseconds=centis * 10
        )
    
    @classmethod
    def format_time(cls, td: timedelta) -> str:
        """格式化为 ASS 时间格式"""
        total_seconds = int(td.total_seconds())
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        centis = (td.microseconds // 10000) % 100
        return f"{hours}:{minutes:02d}:{seconds:02d}.{centis:02d}"
    
    @classmethod
    def parse(cls, content: str) -> Tuple[List[SubtitleEntry], dict]:
        """解析 ASS/SSA 内容"""
        entries = []
        styles = {}
        info = {}
        
        current_section = None
        index = 1
        
        for line in content.split('\n'):
            line = line.strip()
            
            # 识别段
            if line.startswith('[') and line.endswith(']'):
                current_section = line[1:-1].lower()
                continue
            
            if current_section == 'script info':
                if ':' in line:
                    key, value = line.split(':', 1)
                    info[key.strip()] = value.strip()
            
            elif current_section == 'v4+ styles':
                match = cls.STYLE_PATTERN.match(line)
                if match:
                    style_data = match.group(1).split(',')
                    if len(style_data) >= 1:
                        styles[style_data[0].strip()] = style_data
            
            elif current_section == 'events':
                match = cls.DIALOGUE_PATTERN.match(line)
                if match:
                    parts = match.group(1).split(',', 9)
                    if len(parts) >= 10:
                        try:
                            start = cls.parse_time(parts[1])
                            end = cls.parse_time(parts[2])
                            text = parts[9]
                            # 移除 ASS 标签
                            text = cls._strip_ass_tags(text)
                            
                            if text.strip():
                                entries.append(SubtitleEntry(
                                    index=index,
                                    start=start,
                                    end=end,
                                    text=text
                                ))
                                index += 1
                        except ValueError:
                            continue
        
        metadata = {
            'info': info,
            'styles': styles
        }
        
        return entries, metadata
    
    @classmethod
    def _strip_ass_tags(cls, text: str) -> str:
        """移除 ASS 标签"""
        # 移除花括号标签 {\tag}
        text = re.sub(r'\{[^}]*\}', '', text)
        # 移除 \N 换行符
        text = text.replace('\\N', '\n').replace('\\n', '\n')
        return text.strip()
    
    @classmethod
    def generate(cls, entries: List[SubtitleEntry], 
                 title: str = "Subtitle",
                 styles: Optional[dict] = None,
                 metadata: Optional[dict] = None) -> str:
        """生成 ASS 内容"""
        # 如果 metadata 中有 title，优先使用
        if metadata and 'title' in metadata:
            title = metadata['title']
        
        lines = [
            '[Script Info]',
            f'Title: {title}',
            'ScriptType: v4.00+',
            'Collisions: Normal',
            'PlayDepth: 0',
            '',
            '[V4+ Styles]',
            'Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding',
            'Style: Default,Arial,16,&H00FFFFFF,&H000000FF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,2,0,2,10,10,10,1',
            '',
            '[Events]',
            'Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text'
        ]
        
        for entry in entries:
            text = entry.text.replace('\n', '\\N')
            lines.append(
                f"Dialogue: 0,{cls.format_time(entry.start)},"
                f"{cls.format_time(entry.end)},Default,,0,0,0,,{text}"
            )
        
        return '\n'.join(lines)


class SubtitleUtils:
    """字幕工具集"""
    
    @staticmethod
    def load_file(filepath: str, encoding: str = 'utf-8') -> Tuple[List[SubtitleEntry], str, dict]:
        """
        加载字幕文件，自动识别格式
        
        返回: (字幕列表, 格式类型, 元数据)
        """
        with open(filepath, 'r', encoding=encoding) as f:
            content = f.read()
        
        return SubtitleUtils.parse(content, filepath)
    
    @staticmethod
    def parse(content: str, filename: str = '') -> Tuple[List[SubtitleEntry], str, dict]:
        """
        解析字幕内容，自动识别格式
        
        返回: (字幕列表, 格式类型, 元数据)
        """
        content = content.strip()
        metadata = {}
        
        # 检测格式
        if content.startswith('WEBVTT'):
            entries, metadata = VTTParser.parse(content)
            return entries, 'vtt', metadata
        elif content.startswith('[Script Info]') or '[V4+ Styles]' in content:
            entries, metadata = ASSParser.parse(content)
            return entries, 'ass', metadata
        else:
            # 默认 SRT
            entries = SRTParser.parse(content)
            return entries, 'srt', metadata
    
    @staticmethod
    def save_file(entries: List[SubtitleEntry], filepath: str, 
                  format: str = 'srt', metadata: Optional[dict] = None,
                  encoding: str = 'utf-8') -> None:
        """保存字幕文件"""
        content = SubtitleUtils.generate(entries, format, metadata)
        with open(filepath, 'w', encoding=encoding) as f:
            f.write(content)
    
    @staticmethod
    def generate(entries: List[SubtitleEntry], format: str = 'srt',
                 metadata: Optional[dict] = None) -> str:
        """生成字幕内容"""
        format = format.lower()
        if format == 'srt':
            return SRTParser.generate(entries)
        elif format == 'vtt':
            return VTTParser.generate(entries, metadata)
        elif format in ('ass', 'ssa'):
            return ASSParser.generate(entries, metadata=metadata)
        else:
            raise ValueError(f"Unsupported format: {format}")
    
    @staticmethod
    def shift(entries: List[SubtitleEntry], delta: timedelta) -> List[SubtitleEntry]:
        """调整所有字幕时间轴"""
        return [entry.shift(delta) for entry in entries]
    
    @staticmethod
    def delay(entries: List[SubtitleEntry], seconds: float) -> List[SubtitleEntry]:
        """延迟字幕"""
        return SubtitleUtils.shift(entries, timedelta(seconds=seconds))
    
    @staticmethod
    def advance(entries: List[SubtitleEntry], seconds: float) -> List[SubtitleEntry]:
        """提前字幕"""
        return SubtitleUtils.shift(entries, timedelta(seconds=-seconds))
    
    @staticmethod
    def merge(*sub_lists: List[SubtitleEntry], 
              reindex: bool = True) -> List[SubtitleEntry]:
        """合并多个字幕列表"""
        all_entries = []
        for sub_list in sub_lists:
            all_entries.extend(sub_list)
        
        # 按开始时间排序
        all_entries.sort(key=lambda e: e.start)
        
        if reindex:
            for i, entry in enumerate(all_entries, 1):
                entry.index = i
        
        return all_entries
    
    @staticmethod
    def split(entries: List[SubtitleEntry], 
              at: timedelta) -> Tuple[List[SubtitleEntry], List[SubtitleEntry]]:
        """在指定时间点分割字幕"""
        before = []
        after = []
        
        for entry in entries:
            if entry.end <= at:
                before.append(entry)
            elif entry.start >= at:
                after.append(entry.shift(-at))
            else:
                # 跨越分割点的字幕 - 放入前半部分
                before.append(entry)
        
        return before, after
    
    @staticmethod
    def filter_by_time(entries: List[SubtitleEntry],
                       start: Optional[timedelta] = None,
                       end: Optional[timedelta] = None) -> List[SubtitleEntry]:
        """按时间范围过滤字幕"""
        result = []
        for entry in entries:
            if start is not None and entry.end <= start:
                continue
            if end is not None and entry.start >= end:
                continue
            result.append(entry)
        return result
    
    @staticmethod
    def filter_by_text(entries: List[SubtitleEntry],
                       pattern: str,
                       case_sensitive: bool = False) -> List[SubtitleEntry]:
        """按文本过滤字幕"""
        flags = 0 if case_sensitive else re.IGNORECASE
        regex = re.compile(pattern, flags)
        return [e for e in entries if regex.search(e.text)]
    
    @staticmethod
    def convert(entries: List[SubtitleEntry], 
                from_format: str, to_format: str,
                metadata: Optional[dict] = None) -> str:
        """转换字幕格式"""
        return SubtitleUtils.generate(entries, to_format, metadata)
    
    @staticmethod
    def reindex(entries: List[SubtitleEntry], start: int = 1) -> List[SubtitleEntry]:
        """重新编号"""
        return [
            SubtitleEntry(index=i, start=e.start, end=e.end, text=e.text)
            for i, e in enumerate(entries, start)
        ]
    
    @staticmethod
    def deduplicate(entries: List[SubtitleEntry], 
                    min_gap: timedelta = timedelta(milliseconds=100)) -> List[SubtitleEntry]:
        """去除重复或重叠的字幕"""
        if not entries:
            return []
        
        sorted_entries = sorted(entries, key=lambda e: e.start)
        result = [sorted_entries[0]]
        
        for entry in sorted_entries[1:]:
            last = result[-1]
            # 如果与上一条重叠且文本相同，合并
            if entry.start < last.end + min_gap and entry.text == last.text:
                result[-1] = SubtitleEntry(
                    index=last.index,
                    start=last.start,
                    end=max(last.end, entry.end),
                    text=last.text
                )
            else:
                result.append(entry)
        
        return SubtitleUtils.reindex(result)
    
    @staticmethod
    def get_statistics(entries: List[SubtitleEntry]) -> dict:
        """获取字幕统计信息"""
        if not entries:
            return {
                'count': 0,
                'total_duration': timedelta(),
                'avg_duration': timedelta(),
                'total_chars': 0,
                'avg_chars': 0,
                'longest': None,
                'shortest': None
            }
        
        durations = [e.duration for e in entries]
        chars = [len(e.text) for e in entries]
        
        longest = max(entries, key=lambda e: e.duration)
        shortest = min(entries, key=lambda e: e.duration)
        
        return {
            'count': len(entries),
            'total_duration': sum(durations, timedelta()),
            'avg_duration': sum(durations, timedelta()) / len(durations),
            'total_chars': sum(chars),
            'avg_chars': sum(chars) / len(chars),
            'longest': longest,
            'shortest': shortest
        }
    
    @staticmethod
    def validate(entries: List[SubtitleEntry]) -> List[str]:
        """验证字幕，返回错误列表"""
        errors = []
        seen_times = {}
        
        for i, entry in enumerate(entries):
            # 检查时间顺序
            if entry.start >= entry.end:
                errors.append(f"Entry {entry.index}: start time >= end time")
            
            # 检查空文本
            if not entry.text.strip():
                errors.append(f"Entry {entry.index}: empty text")
            
            # 检查重叠
            for j in range(i):
                prev = entries[j]
                if entry.start < prev.end and entry.end > prev.start:
                    errors.append(
                        f"Entry {entry.index} overlaps with {prev.index}"
                    )
        
        return errors


def parse_srt(content: str) -> List[SubtitleEntry]:
    """快捷方法：解析 SRT"""
    return SRTParser.parse(content)


def parse_vtt(content: str) -> Tuple[List[SubtitleEntry], dict]:
    """快捷方法：解析 VTT"""
    return VTTParser.parse(content)


def parse_ass(content: str) -> Tuple[List[SubtitleEntry], dict]:
    """快捷方法：解析 ASS"""
    return ASSParser.parse(content)


def load(filepath: str, encoding: str = 'utf-8') -> Tuple[List[SubtitleEntry], str, dict]:
    """快捷方法：加载字幕文件"""
    return SubtitleUtils.load_file(filepath, encoding)


def save(entries: List[SubtitleEntry], filepath: str,
         format: str = 'srt', metadata: Optional[dict] = None,
         encoding: str = 'utf-8') -> None:
    """快捷方法：保存字幕文件"""
    SubtitleUtils.save_file(entries, filepath, format, metadata, encoding)


if __name__ == '__main__':
    # 演示用法
    srt_content = """1
00:00:01,000 --> 00:00:04,000
Hello, world!

2
00:00:05,000 --> 00:00:08,000
This is a test subtitle.

3
00:00:09,000 --> 00:00:12,000
Multiple lines
are supported!
"""
    
    entries = parse_srt(srt_content)
    print(f"Parsed {len(entries)} entries")
    
    for entry in entries:
        print(f"  [{entry.index}] {entry.start} --> {entry.end}: {entry.text[:20]}...")
    
    # 测试时间偏移
    shifted = SubtitleUtils.delay(entries, 2.5)
    print(f"\nAfter delaying 2.5s:")
    print(f"  First entry: {shifted[0].start} --> {shifted[0].end}")
    
    # 测试统计
    stats = SubtitleUtils.get_statistics(entries)
    print(f"\nStatistics:")
    print(f"  Total entries: {stats['count']}")
    print(f"  Total chars: {stats['total_chars']}")