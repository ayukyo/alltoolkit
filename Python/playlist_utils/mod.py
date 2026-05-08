"""
Playlist Utils - 播放列表处理工具

支持 M3U/M3U8、PLS、XSPF 等播放列表格式的解析、生成和转换。
零外部依赖，仅使用 Python 标准库。

功能：
- 解析和生成 M3U/M3U8 播放列表
- 解析和生成 PLS 播放列表
- 解析和生成 XSPF 播放列表
- 格式转换
- 播放列表合并、去重、排序
- 元数据提取和修改
"""

from typing import List, Dict, Optional, Union, Tuple, Any
from dataclasses import dataclass, field
from datetime import timedelta
import re
import xml.etree.ElementTree as ET
from xml.dom import minidom
import urllib.parse


@dataclass
class Track:
    """音轨信息"""
    location: str  # 文件路径或URL
    title: Optional[str] = None  # 标题
    duration: Optional[int] = None  # 时长（秒），-1表示未知
    artist: Optional[str] = None  # 艺术家
    album: Optional[str] = None  # 专辑
    track_number: Optional[int] = None  # 音轨号
    info: Optional[str] = None  # 信息链接
    image: Optional[str] = None  # 封面图片
    annotation: Optional[str] = None  # 注释/描述
    album_artist: Optional[str] = None  # 专辑艺术家
    composer: Optional[str] = None  # 作曲家
    genre: Optional[str] = None  # 流派
    year: Optional[int] = None  # 年份
    
    def __post_init__(self):
        """验证和清理数据"""
        if self.location:
            self.location = self.location.strip()
        if self.title:
            self.title = self.title.strip()
        if self.artist:
            self.artist = self.artist.strip()
        if self.album:
            self.album = self.album.strip()
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            'location': self.location,
            'title': self.title,
            'duration': self.duration,
            'artist': self.artist,
            'album': self.album,
            'track_number': self.track_number,
            'info': self.info,
            'image': self.image,
            'annotation': self.annotation,
            'album_artist': self.album_artist,
            'composer': self.composer,
            'genre': self.genre,
            'year': self.year
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Track':
        """从字典创建"""
        return cls(
            location=data.get('location', ''),
            title=data.get('title'),
            duration=data.get('duration'),
            artist=data.get('artist'),
            album=data.get('album'),
            track_number=data.get('track_number'),
            info=data.get('info'),
            image=data.get('image'),
            annotation=data.get('annotation'),
            album_artist=data.get('album_artist'),
            composer=data.get('composer'),
            genre=data.get('genre'),
            year=data.get('year')
        )
    
    def format_duration(self) -> str:
        """格式化时长为 MM:SS 或 HH:MM:SS 格式"""
        if self.duration is None or self.duration < 0:
            return "?:??"
        
        total_seconds = self.duration
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        
        if hours > 0:
            return f"{hours}:{minutes:02d}:{seconds:02d}"
        return f"{minutes}:{seconds:02d}"


@dataclass
class Playlist:
    """播放列表"""
    tracks: List[Track] = field(default_factory=list)
    title: Optional[str] = None  # 播放列表标题
    creator: Optional[str] = None  # 创建者
    annotation: Optional[str] = None  # 注释
    info: Optional[str] = None  # 信息链接
    location: Optional[str] = None  # 播放列表位置
    identifier: Optional[str] = None  # 唯一标识符
    image: Optional[str] = None  # 播放列表封面
    date: Optional[str] = None  # 创建日期
    license_url: Optional[str] = None  # 许可证链接
    
    def add_track(self, track: Track) -> 'Playlist':
        """添加音轨"""
        self.tracks.append(track)
        return self
    
    def remove_track(self, index: int) -> Optional[Track]:
        """移除音轨"""
        if 0 <= index < len(self.tracks):
            return self.tracks.pop(index)
        return None
    
    def clear(self) -> 'Playlist':
        """清空播放列表"""
        self.tracks.clear()
        return self
    
    def get_total_duration(self) -> int:
        """获取总时长（秒）"""
        total = 0
        for track in self.tracks:
            if track.duration and track.duration > 0:
                total += track.duration
        return total
    
    def format_total_duration(self) -> str:
        """格式化总时长"""
        total = self.get_total_duration()
        hours = total // 3600
        minutes = (total % 3600) // 60
        seconds = total % 60
        
        if hours > 0:
            return f"{hours}小时{minutes}分{seconds}秒"
        return f"{minutes}分{seconds}秒"
    
    def deduplicate(self, by_location: bool = True, by_title: bool = False) -> 'Playlist':
        """去重
        
        Args:
            by_location: 按位置去重
            by_title: 按标题去重
        
        Returns:
            去重后的新播放列表
        """
        seen = set()
        unique_tracks = []
        
        for track in self.tracks:
            key_parts = []
            if by_location and track.location:
                key_parts.append(track.location)
            if by_title and track.title:
                key_parts.append(track.title)
            
            key = tuple(key_parts) if key_parts else id(track)
            
            if key not in seen:
                seen.add(key)
                unique_tracks.append(track)
        
        return Playlist(
            tracks=unique_tracks,
            title=self.title,
            creator=self.creator,
            annotation=self.annotation,
            info=self.info,
            location=self.location,
            identifier=self.identifier,
            image=self.image,
            date=self.date,
            license_url=self.license_url
        )
    
    def sort_by_title(self, reverse: bool = False) -> 'Playlist':
        """按标题排序"""
        sorted_tracks = sorted(
            self.tracks,
            key=lambda t: (t.title or '', t.location),
            reverse=reverse
        )
        return Playlist(tracks=sorted_tracks, title=self.title, creator=self.creator)
    
    def sort_by_artist(self, reverse: bool = False) -> 'Playlist':
        """按艺术家排序"""
        sorted_tracks = sorted(
            self.tracks,
            key=lambda t: (t.artist or '', t.album or '', t.track_number or 0),
            reverse=reverse
        )
        return Playlist(tracks=sorted_tracks, title=self.title, creator=self.creator)
    
    def sort_by_duration(self, reverse: bool = False) -> 'Playlist':
        """按时长排序"""
        sorted_tracks = sorted(
            self.tracks,
            key=lambda t: t.duration or -1,
            reverse=reverse
        )
        return Playlist(tracks=sorted_tracks, title=self.title, creator=self.creator)
    
    def shuffle(self) -> 'Playlist':
        """随机排序（使用Fisher-Yates算法）"""
        import random
        tracks = self.tracks.copy()
        for i in range(len(tracks) - 1, 0, -1):
            j = random.randint(0, i)
            tracks[i], tracks[j] = tracks[j], tracks[i]
        return Playlist(tracks=tracks, title=self.title, creator=self.creator)
    
    def filter_by_artist(self, artist: str, exact: bool = False) -> 'Playlist':
        """按艺术家筛选"""
        if exact:
            filtered = [t for t in self.tracks if t.artist == artist]
        else:
            artist_lower = artist.lower()
            filtered = [t for t in self.tracks if t.artist and artist_lower in t.artist.lower()]
        return Playlist(tracks=filtered, title=self.title, creator=self.creator)
    
    def filter_by_album(self, album: str, exact: bool = False) -> 'Playlist':
        """按专辑筛选"""
        if exact:
            filtered = [t for t in self.tracks if t.album == album]
        else:
            album_lower = album.lower()
            filtered = [t for t in self.tracks if t.album and album_lower in t.album.lower()]
        return Playlist(tracks=filtered, title=self.title, creator=self.creator)
    
    def filter_by_duration(self, min_seconds: int = None, max_seconds: int = None) -> 'Playlist':
        """按时长筛选"""
        filtered = []
        for track in self.tracks:
            if track.duration is None or track.duration < 0:
                continue
            if min_seconds is not None and track.duration < min_seconds:
                continue
            if max_seconds is not None and track.duration > max_seconds:
                continue
            filtered.append(track)
        return Playlist(tracks=filtered, title=self.title, creator=self.creator)
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            'title': self.title,
            'creator': self.creator,
            'annotation': self.annotation,
            'info': self.info,
            'location': self.location,
            'identifier': self.identifier,
            'image': self.image,
            'date': self.date,
            'license_url': self.license_url,
            'tracks': [t.to_dict() for t in self.tracks]
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Playlist':
        """从字典创建"""
        tracks = [Track.from_dict(t) for t in data.get('tracks', [])]
        return cls(
            tracks=tracks,
            title=data.get('title'),
            creator=data.get('creator'),
            annotation=data.get('annotation'),
            info=data.get('info'),
            location=data.get('location'),
            identifier=data.get('identifier'),
            image=data.get('image'),
            date=data.get('date'),
            license_url=data.get('license_url')
        )
    
    def __len__(self) -> int:
        return len(self.tracks)
    
    def __iter__(self):
        return iter(self.tracks)
    
    def __getitem__(self, index: int) -> Track:
        return self.tracks[index]


# ============== M3U/M3U8 格式 ==============

def parse_m3u(content: str) -> Playlist:
    """解析 M3U/M3U8 播放列表
    
    M3U 格式支持：
    - 简单文件列表
    - EXTINF 标签（标题、时长）
    - EXTALBUM 标签（专辑）
    - EXTART 标签（艺术家）
    - EXTGENRE 标签（流派）
    
    Args:
        content: M3U 文件内容
    
    Returns:
        Playlist 对象
    """
    lines = content.strip().split('\n')
    playlist = Playlist()
    
    # 检查是否是扩展 M3U 格式
    is_extended = lines[0].strip().startswith('#EXTM3U')
    
    current_track_data = {}
    
    for line in lines:
        line = line.strip()
        
        if not line:
            continue
        
        if line.startswith('#EXTM3U'):
            continue
        
        if line.startswith('#PLAYLIST:'):
            playlist.title = line[10:].strip()
            continue
        
        if line.startswith('#EXTINF:'):
            # 格式: #EXTINF:duration,title
            match = re.match(r'#EXTINF:(-?\d+)(?:\s+(.*))?,(.*)', line)
            if match:
                duration = int(match.group(1))
                # 有些格式使用属性
                attrs = match.group(2)
                title = match.group(3).strip()
                
                current_track_data['duration'] = duration if duration > 0 else None
                current_track_data['title'] = title
                
                # 解析属性
                if attrs:
                    attr_pattern = r'(\w+)=["\']([^"\']*)["\']'
                    for attr_match in re.finditer(attr_pattern, attrs):
                        key = attr_match.group(1).lower()
                        value = attr_match.group(2)
                        if key == 'tvg-name':
                            current_track_data['title'] = value
                        elif key == 'tvg-logo':
                            current_track_data['image'] = value
                        elif key == 'group-title':
                            current_track_data['album'] = value
            continue
        
        if line.startswith('#EXTALBUM:'):
            current_track_data['album'] = line[10:].strip()
            continue
        
        if line.startswith('#EXTART:'):
            current_track_data['artist'] = line[8:].strip()
            continue
        
        if line.startswith('#EXTGENRE:'):
            current_track_data['genre'] = line[10:].strip()
            continue
        
        if line.startswith('#EXTBYT:'):
            # 字节大小（某些播放器使用）
            continue
        
        if line.startswith('#'):
            # 忽略其他注释
            continue
        
        # 这是文件路径/URL
        if line:
            track = Track(
                location=line,
                title=current_track_data.get('title'),
                duration=current_track_data.get('duration'),
                artist=current_track_data.get('artist'),
                album=current_track_data.get('album'),
                genre=current_track_data.get('genre'),
                image=current_track_data.get('image')
            )
            playlist.add_track(track)
            current_track_data = {}
    
    return playlist


def generate_m3u(playlist: Playlist, extended: bool = True, encoding: str = 'utf-8') -> str:
    """生成 M3U/M3U8 播放列表
    
    Args:
        playlist: Playlist 对象
        extended: 是否生成扩展 M3U 格式（M3U8）
        encoding: 编码（仅用于注释）
    
    Returns:
        M3U 文件内容
    """
    lines = []
    
    if extended:
        lines.append('#EXTM3U')
        
        if playlist.title:
            lines.append(f'#PLAYLIST:{playlist.title}')
    
    for track in playlist.tracks:
        if extended:
            # 生成 EXTINF 行
            duration = track.duration if track.duration and track.duration > 0 else -1
            title = track.title or ''
            
            # 添加属性（如果有）
            attrs = []
            if track.image:
                attrs.append(f'tvg-logo="{track.image}"')
            
            if attrs:
                lines.append(f'#EXTINF:{duration} {" ".join(attrs)},{title}')
            else:
                lines.append(f'#EXTINF:{duration},{title}')
            
            # 添加额外信息
            if track.artist:
                lines.append(f'#EXTART:{track.artist}')
            if track.album:
                lines.append(f'#EXTALBUM:{track.album}')
            if track.genre:
                lines.append(f'#EXTGENRE:{track.genre}')
        
        lines.append(track.location)
    
    return '\n'.join(lines)


# ============== PLS 格式 ==============

def parse_pls(content: str) -> Playlist:
    """解析 PLS 播放列表
    
    PLS 格式示例:
    [playlist]
    File1=path/to/file.mp3
    Title1=Song Title
    Length1=180
    NumberOfEntries=1
    
    Args:
        content: PLS 文件内容
    
    Returns:
        Playlist 对象
    """
    playlist = Playlist()
    
    lines = content.strip().split('\n')
    tracks_data = {}
    num_entries = 0
    
    for line in lines:
        line = line.strip()
        
        if not line or line.startswith(';'):
            continue
        
        if line.lower() == '[playlist]':
            continue
        
        if line.lower().startswith('numberofentries'):
            try:
                num_entries = int(line.split('=')[1])
            except (IndexError, ValueError):
                pass
            continue
        
        if line.lower().startswith('version'):
            continue
        
        # 解析 File1, Title1, Length1 等
        match = re.match(r'^(File|Title|Length)(\d+)=(.*)$', line, re.IGNORECASE)
        if match:
            key = match.group(1).lower()
            index = int(match.group(2))
            value = match.group(3).strip()
            
            if index not in tracks_data:
                tracks_data[index] = {}
            
            if key == 'file':
                tracks_data[index]['location'] = value
            elif key == 'title':
                tracks_data[index]['title'] = value
            elif key == 'length':
                try:
                    duration = int(value)
                    tracks_data[index]['duration'] = duration if duration > 0 else None
                except ValueError:
                    pass
    
    # 按 index 排序并创建 Track 对象
    for index in sorted(tracks_data.keys()):
        data = tracks_data[index]
        if 'location' in data:
            track = Track(
                location=data['location'],
                title=data.get('title'),
                duration=data.get('duration')
            )
            playlist.add_track(track)
    
    return playlist


def generate_pls(playlist: Playlist) -> str:
    """生成 PLS 播放列表
    
    Args:
        playlist: Playlist 对象
    
    Returns:
        PLS 文件内容
    """
    lines = ['[playlist]']
    
    for i, track in enumerate(playlist.tracks, 1):
        lines.append(f'File{i}={track.location}')
        
        if track.title:
            lines.append(f'Title{i}={track.title}')
        else:
            # PLS 需要 Title，从文件名生成
            title = track.location.split('/')[-1].split('\\')[-1]
            if '.' in title:
                title = title.rsplit('.', 1)[0]
            lines.append(f'Title{i}={title}')
        
        duration = track.duration if track.duration and track.duration > 0 else -1
        lines.append(f'Length{i}={duration}')
    
    lines.append(f'NumberOfEntries={len(playlist.tracks)}')
    lines.append('Version=2')
    
    return '\n'.join(lines)


# ============== XSPF 格式 ==============

def parse_xspf(content: str) -> Playlist:
    """解析 XSPF (XML Shareable Playlist Format) 播放列表
    
    XSPF 是 XML 格式的播放列表，支持丰富的元数据。
    
    Args:
        content: XSPF 文件内容
    
    Returns:
        Playlist 对象
    """
    playlist = Playlist()
    
    try:
        root = ET.fromstring(content)
    except ET.ParseError:
        return playlist
    
    # XSPF 命名空间
    ns = {'xspf': 'http://xspf.org/ns/0/'}
    
    # 尝试带命名空间和不带命名空间的解析
    def find_text(parent, local_name):
        # 尝试带命名空间
        elem = parent.find(f'xspf:{local_name}', ns)
        if elem is not None:
            return elem.text
        # 尝试不带命名空间
        elem = parent.find(local_name)
        if elem is not None:
            return elem.text
        return None
    
    def find_all(parent, local_name):
        # 尝试带命名空间
        elems = parent.findall(f'xspf:{local_name}', ns)
        if elems:
            return elems
        # 尝试不带命名空间
        return parent.findall(local_name)
    
    # 解析播放列表元数据
    playlist.title = find_text(root, 'title')
    playlist.creator = find_text(root, 'creator')
    playlist.annotation = find_text(root, 'annotation')
    playlist.info = find_text(root, 'info')
    playlist.location = find_text(root, 'location')
    playlist.identifier = find_text(root, 'identifier')
    playlist.image = find_text(root, 'image')
    playlist.date = find_text(root, 'date')
    playlist.license_url = find_text(root, 'license')
    
    # 解析 trackList
    tracklist = None
    for elem in root:
        if elem.tag.endswith('trackList') or elem.tag == 'trackList':
            tracklist = elem
            break
    
    if tracklist is None:
        return playlist
    
    # 解析每个 track
    for track_elem in find_all(tracklist, 'track') or []:
        location = find_text(track_elem, 'location')
        
        if not location:
            continue
        
        track = Track(location=location)
        
        track.title = find_text(track_elem, 'creator')  # XSPF 中 creator 是艺术家
        track.artist = find_text(track_elem, 'creator')
        track.album = find_text(track_elem, 'album')
        track.title = find_text(track_elem, 'title') or track.title
        track.annotation = find_text(track_elem, 'annotation')
        track.info = find_text(track_elem, 'info')
        track.image = find_text(track_elem, 'image')
        track.track_number = None
        
        # 解析 trackNum
        track_num_text = find_text(track_elem, 'trackNum')
        if track_num_text:
            try:
                track.track_number = int(track_num_text)
            except ValueError:
                pass
        
        # 解析 duration（毫秒）
        duration_text = find_text(track_elem, 'duration')
        if duration_text:
            try:
                # XSPF 使用毫秒
                duration_ms = int(duration_text)
                track.duration = duration_ms // 1000
            except ValueError:
                pass
        
        # 解析 meta 元素（自定义元数据）
        for meta in find_all(track_elem, 'meta') or []:
            rel = meta.get('rel') or meta.get('{http://xspf.org/ns/0/}rel')
            if rel and meta.text:
                if rel == 'albumArtist':
                    track.album_artist = meta.text
                elif rel == 'composer':
                    track.composer = meta.text
                elif rel == 'genre':
                    track.genre = meta.text
                elif rel == 'year':
                    try:
                        track.year = int(meta.text)
                    except ValueError:
                        pass
        
        playlist.add_track(track)
    
    return playlist


def generate_xspf(playlist: Playlist, pretty: bool = True) -> str:
    """生成 XSPF 播放列表
    
    Args:
        playlist: Playlist 对象
        pretty: 是否格式化输出
    
    Returns:
        XSPF 文件内容
    """
    # 创建根元素
    root = ET.Element('playlist')
    root.set('xmlns', 'http://xspf.org/ns/0/')
    root.set('version', '1')
    
    # 添加播放列表元数据
    if playlist.title:
        ET.SubElement(root, 'title').text = playlist.title
    if playlist.creator:
        ET.SubElement(root, 'creator').text = playlist.creator
    if playlist.annotation:
        ET.SubElement(root, 'annotation').text = playlist.annotation
    if playlist.info:
        ET.SubElement(root, 'info').text = playlist.info
    if playlist.location:
        ET.SubElement(root, 'location').text = playlist.location
    if playlist.identifier:
        ET.SubElement(root, 'identifier').text = playlist.identifier
    if playlist.image:
        ET.SubElement(root, 'image').text = playlist.image
    if playlist.date:
        ET.SubElement(root, 'date').text = playlist.date
    if playlist.license_url:
        ET.SubElement(root, 'license').text = playlist.license_url
    
    # 创建 trackList
    tracklist = ET.SubElement(root, 'trackList')
    
    for track in playlist.tracks:
        track_elem = ET.SubElement(tracklist, 'track')
        
        # location 是必需的
        ET.SubElement(track_elem, 'location').text = track.location
        
        if track.title:
            ET.SubElement(track_elem, 'title').text = track.title
        
        if track.artist:
            ET.SubElement(track_elem, 'creator').text = track.artist
        
        if track.album:
            ET.SubElement(track_elem, 'album').text = track.album
        
        if track.annotation:
            ET.SubElement(track_elem, 'annotation').text = track.annotation
        
        if track.info:
            ET.SubElement(track_elem, 'info').text = track.info
        
        if track.image:
            ET.SubElement(track_elem, 'image').text = track.image
        
        if track.track_number is not None:
            ET.SubElement(track_elem, 'trackNum').text = str(track.track_number)
        
        if track.duration is not None and track.duration >= 0:
            # XSPF 使用毫秒
            ET.SubElement(track_elem, 'duration').text = str(track.duration * 1000)
        
        # 添加自定义元数据
        if track.album_artist:
            meta = ET.SubElement(track_elem, 'meta')
            meta.set('rel', 'albumArtist')
            meta.text = track.album_artist
        
        if track.composer:
            meta = ET.SubElement(track_elem, 'meta')
            meta.set('rel', 'composer')
            meta.text = track.composer
        
        if track.genre:
            meta = ET.SubElement(track_elem, 'meta')
            meta.set('rel', 'genre')
            meta.text = track.genre
        
        if track.year:
            meta = ET.SubElement(track_elem, 'meta')
            meta.set('rel', 'year')
            meta.text = str(track.year)
    
    # 生成 XML 字符串
    if pretty:
        # 使用 minidom 格式化
        rough_string = ET.tostring(root, encoding='unicode')
        reparsed = minidom.parseString(rough_string)
        return reparsed.toprettyxml(indent='  ')
    else:
        return ET.tostring(root, encoding='unicode')


# ============== 格式检测和转换 ==============

def detect_format(content: str, filename: str = None) -> str:
    """检测播放列表格式
    
    Args:
        content: 文件内容
        filename: 文件名（可选，用于辅助判断）
    
    Returns:
        格式名称: 'm3u', 'pls', 'xspf', 'unknown'
    """
    content = content.strip()
    
    # 检测 XSPF (XML)
    if content.startswith('<?xml') or content.startswith('<playlist'):
        return 'xspf'
    
    # 检测 PLS
    if content.lower().startswith('[playlist]'):
        return 'pls'
    
    # 检测 M3U/M3U8
    if content.startswith('#EXTM3U'):
        return 'm3u'
    
    # 检测简单 M3U（仅文件列表）
    lines = content.split('\n')
    for line in lines[:10]:  # 检查前10行
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        # 如果是非空行且不是明显的 XML 或 INI 格式，可能是 M3U
        if not line.startswith('[') and not line.startswith('<'):
            # 检查是否像文件路径或 URL
            if '/' in line or '\\' in line or '.' in line or line.startswith('http'):
                return 'm3u'
    
    # 根据文件扩展名判断
    if filename:
        ext = filename.lower().split('.')[-1] if '.' in filename else ''
        if ext in ('m3u', 'm3u8'):
            return 'm3u'
        elif ext == 'pls':
            return 'pls'
        elif ext == 'xspf':
            return 'xspf'
    
    return 'unknown'


def parse(content: str, format: str = None, filename: str = None) -> Playlist:
    """自动检测格式并解析播放列表
    
    Args:
        content: 文件内容
        format: 指定格式 ('m3u', 'pls', 'xspf')，如果不指定则自动检测
        filename: 文件名（用于辅助格式检测）
    
    Returns:
        Playlist 对象
    """
    if format is None:
        format = detect_format(content, filename)
    
    format = format.lower()
    
    if format == 'm3u':
        return parse_m3u(content)
    elif format == 'pls':
        return parse_pls(content)
    elif format == 'xspf':
        return parse_xspf(content)
    else:
        # 默认尝试 M3U
        return parse_m3u(content)


def convert(content: str, from_format: str, to_format: str, 
            playlist_title: str = None) -> str:
    """转换播放列表格式
    
    Args:
        content: 源播放列表内容
        from_format: 源格式 ('m3u', 'pls', 'xspf', 'auto')
        to_format: 目标格式 ('m3u', 'pls', 'xspf')
        playlist_title: 播放列表标题
    
    Returns:
        转换后的播放列表内容
    """
    # 解析源播放列表
    if from_format.lower() == 'auto':
        playlist = parse(content)
    else:
        playlist = parse(content, format=from_format)
    
    # 设置标题
    if playlist_title:
        playlist.title = playlist_title
    
    # 生成目标格式
    to_format = to_format.lower()
    
    if to_format == 'm3u':
        return generate_m3u(playlist, extended=True)
    elif to_format == 'pls':
        return generate_pls(playlist)
    elif to_format == 'xspf':
        return generate_xspf(playlist)
    else:
        raise ValueError(f"不支持的目标格式: {to_format}")


def merge_playlists(playlists: List[Playlist], title: str = None) -> Playlist:
    """合并多个播放列表
    
    Args:
        playlists: Playlist 对象列表
        title: 合并后的播放列表标题
    
    Returns:
        合并后的 Playlist 对象
    """
    merged = Playlist(title=title)
    
    for playlist in playlists:
        for track in playlist.tracks:
            merged.add_track(track)
    
    return merged


def load_file(filepath: str, encoding: str = 'utf-8') -> Playlist:
    """从文件加载播放列表
    
    Args:
        filepath: 文件路径
        encoding: 文件编码
    
    Returns:
        Playlist 对象
    """
    with open(filepath, 'r', encoding=encoding) as f:
        content = f.read()
    
    return parse(content, filename=filepath)


def save_file(playlist: Playlist, filepath: str, format: str = 'm3u',
              encoding: str = 'utf-8') -> None:
    """保存播放列表到文件
    
    Args:
        playlist: Playlist 对象
        filepath: 文件路径
        format: 格式 ('m3u', 'pls', 'xspf')
        encoding: 文件编码
    """
    content = convert('', 'm3u', format, playlist.title) if False else None
    
    # 直接生成内容
    format = format.lower()
    if format == 'm3u':
        content = generate_m3u(playlist, extended=True)
    elif format == 'pls':
        content = generate_pls(playlist)
    elif format == 'xspf':
        content = generate_xspf(playlist)
    else:
        raise ValueError(f"不支持的格式: {format}")
    
    with open(filepath, 'w', encoding=encoding) as f:
        f.write(content)


# ============== 实用函数 ==============

def get_statistics(playlist: Playlist) -> Dict[str, Any]:
    """获取播放列表统计信息
    
    Args:
        playlist: Playlist 对象
    
    Returns:
        统计信息字典
    """
    total_duration = playlist.get_total_duration()
    
    artists = set()
    albums = set()
    genres = set()
    known_durations = 0
    unknown_durations = 0
    min_duration = float('inf')
    max_duration = 0
    
    for track in playlist.tracks:
        if track.artist:
            artists.add(track.artist)
        if track.album:
            albums.add(track.album)
        if track.genre:
            genres.add(track.genre)
        
        if track.duration is not None and track.duration >= 0:
            known_durations += 1
            min_duration = min(min_duration, track.duration)
            max_duration = max(max_duration, track.duration)
        else:
            unknown_durations += 1
    
    return {
        'track_count': len(playlist.tracks),
        'total_duration': total_duration,
        'total_duration_formatted': playlist.format_total_duration(),
        'unique_artists': len(artists),
        'unique_albums': len(albums),
        'unique_genres': len(genres),
        'tracks_with_duration': known_durations,
        'tracks_without_duration': unknown_durations,
        'min_duration': min_duration if min_duration != float('inf') else 0,
        'max_duration': max_duration,
        'average_duration': total_duration // known_durations if known_durations > 0 else 0
    }


def find_duplicates(playlist: Playlist, by_location: bool = True, 
                   by_title: bool = False) -> List[Tuple[int, Track]]:
    """查找重复的音轨
    
    Args:
        playlist: Playlist 对象
        by_location: 按位置比较
        by_title: 按标题比较
    
    Returns:
        重复音轨列表 [(索引, Track), ...]
    """
    seen = {}
    duplicates = []
    
    for i, track in enumerate(playlist.tracks):
        key_parts = []
        if by_location and track.location:
            key_parts.append(track.location)
        if by_title and track.title:
            key_parts.append(track.title)
        
        key = tuple(key_parts) if key_parts else id(track)
        
        if key in seen:
            duplicates.append((i, track))
        else:
            seen[key] = i
    
    return duplicates


def export_to_json(playlist: Playlist) -> str:
    """导出为 JSON 格式
    
    Args:
        playlist: Playlist 对象
    
    Returns:
        JSON 字符串
    """
    import json
    return json.dumps(playlist.to_dict(), indent=2, ensure_ascii=False)


def import_from_json(json_content: str) -> Playlist:
    """从 JSON 导入
    
    Args:
        json_content: JSON 字符串
    
    Returns:
        Playlist 对象
    """
    import json
    data = json.loads(json_content)
    return Playlist.from_dict(data)


def make_relative_paths(playlist: Playlist, base_path: str) -> Playlist:
    """将绝对路径转换为相对路径
    
    Args:
        playlist: Playlist 对象
        base_path: 基准路径
    
    Returns:
        新的 Playlist 对象
    """
    import os
    
    new_tracks = []
    for track in playlist.tracks:
        location = track.location
        
        # 只处理本地文件
        if not location.startswith(('http://', 'https://', 'rtsp://', 'mms://')):
            try:
                rel_path = os.path.relpath(location, base_path)
                location = rel_path
            except ValueError:
                # 不同驱动器无法转换相对路径
                pass
        
        new_tracks.append(Track(
            location=location,
            title=track.title,
            duration=track.duration,
            artist=track.artist,
            album=track.album,
            track_number=track.track_number,
            info=track.info,
            image=track.image,
            album_artist=track.album_artist,
            composer=track.composer,
            genre=track.genre,
            year=track.year
        ))
    
    return Playlist(
        tracks=new_tracks,
        title=playlist.title,
        creator=playlist.creator,
        annotation=playlist.annotation,
        info=playlist.info,
        location=playlist.location,
        identifier=playlist.identifier,
        image=playlist.image,
        date=playlist.date,
        license_url=playlist.license_url
    )


def make_absolute_paths(playlist: Playlist, base_path: str) -> Playlist:
    """将相对路径转换为绝对路径
    
    Args:
        playlist: Playlist 对象
        base_path: 基准路径
    
    Returns:
        新的 Playlist 对象
    """
    import os
    
    new_tracks = []
    for track in playlist.tracks:
        location = track.location
        
        # 只处理相对路径
        if not os.path.isabs(location) and not location.startswith(('http://', 'https://', 'rtsp://', 'mms://')):
            location = os.path.normpath(os.path.join(base_path, location))
        
        new_tracks.append(Track(
            location=location,
            title=track.title,
            duration=track.duration,
            artist=track.artist,
            album=track.album,
            track_number=track.track_number,
            info=track.info,
            image=track.image,
            album_artist=track.album_artist,
            composer=track.composer,
            genre=track.genre,
            year=track.year
        ))
    
    return Playlist(
        tracks=new_tracks,
        title=playlist.title,
        creator=playlist.creator,
        annotation=playlist.annotation,
        info=playlist.info,
        location=playlist.location,
        identifier=playlist.identifier,
        image=playlist.image,
        date=playlist.date,
        license_url=playlist.license_url
    )


def validate_locations(playlist: Playlist) -> Dict[str, List[int]]:
    """验证播放列表中的文件位置
    
    Args:
        playlist: Playlist 对象
    
    Returns:
        验证结果 {'valid': [...], 'invalid': [...], 'remote': [...]}
    """
    import os
    
    valid = []
    invalid = []
    remote = []
    
    for i, track in enumerate(playlist.tracks):
        location = track.location
        
        if location.startswith(('http://', 'https://', 'rtsp://', 'mms://', 'ftp://')):
            remote.append(i)
        elif os.path.exists(location):
            valid.append(i)
        else:
            invalid.append(i)
    
    return {
        'valid': valid,
        'invalid': invalid,
        'remote': remote
    }