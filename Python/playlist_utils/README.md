# Playlist Utils - 播放列表处理工具

播放列表工具模块，支持 M3U/M3U8、PLS、XSPF 等常见播放列表格式的解析、生成和转换。

## 功能特性

- **多格式支持**: M3U/M3U8、PLS、XSPF (XML Shareable Playlist Format)
- **格式转换**: 不同格式之间的相互转换
- **自动检测**: 自动识别播放列表格式
- **丰富元数据**: 支持标题、艺术家、专辑、时长、音轨号等信息
- **播放列表操作**: 去重、排序、筛选、合并、随机排列
- **统计信息**: 曲目数、总时长、艺术家/专辑统计
- **JSON 支持**: 导出导入 JSON 格式
- **Unicode 支持**: 完善的中文、日文等多语言支持
- **零外部依赖**: 仅使用 Python 标准库

## 快速开始

### 创建播放列表

```python
from playlist_utils.mod import Playlist, Track

# 创建播放列表
playlist = Playlist(title="我的音乐", creator="测试用户")

# 添加曲目
playlist.add_track(Track(
    location="/music/song.mp3",
    title="歌曲名称",
    artist="艺术家",
    album="专辑",
    duration=180,  # 秒
    track_number=1,
    genre="流行",
    year=2024
))

print(f"曲目数: {len(playlist)}")
print(f"总时长: {playlist.format_total_duration()}")
```

### M3U/M3U8 格式

```python
from playlist_utils.mod import parse_m3u, generate_m3u

# 生成 M3U8
m3u8_content = generate_m3u(playlist, extended=True)

# 解析 M3U8
parsed = parse_m3u(m3u8_content)
for track in parsed:
    print(f"{track.title} - {track.artist}")
```

### PLS 格式

```python
from playlist_utils.mod import parse_pls, generate_pls

# 生成 PLS
pls_content = generate_pls(playlist)

# 解析 PLS
parsed = parse_pls(pls_content)
```

### XSPF 格式

```python
from playlist_utils.mod import parse_xspf, generate_xspf

# 生成 XSPF
xspf_content = generate_xspf(playlist)

# 解析 XSPF
parsed = parse_xspf(xspf_content)
```

### 格式转换

```python
from playlist_utils.mod import convert

# M3U 转 PLS
pls_content = convert(m3u_content, "m3u", "pls")

# M3U 转 XSPF
xspf_content = convert(m3u_content, "m3u", "xspf")
```

### 自动检测格式

```python
from playlist_utils.mod import parse, detect_format

# 自动检测并解析
playlist = parse(content)

# 仅检测格式
format_name = detect_format(content)  # 返回 'm3u', 'pls', 'xspf', 'unknown'
```

## 播放列表操作

### 去重

```python
# 按位置去重
deduped = playlist.deduplicate(by_location=True)

# 按标题去重
deduped = playlist.deduplicate(by_title=True)

# 同时按位置和标题去重
deduped = playlist.deduplicate(by_location=True, by_title=True)
```

### 排序

```python
# 按标题排序
sorted_playlist = playlist.sort_by_title()

# 按艺术家排序
sorted_playlist = playlist.sort_by_artist()

# 按时长排序（降序）
sorted_playlist = playlist.sort_by_duration(reverse=True)

# 随机排序
shuffled = playlist.shuffle()
```

### 篮选

```python
# 按艺术家筛选
filtered = playlist.filter_by_artist("艺术家名称")

# 按专辑筛选
filtered = playlist.filter_by_album("专辑名称")

# 按时长筛选
filtered = playlist.filter_by_duration(min_seconds=180, max_seconds=300)
```

### 合并

```python
from playlist_utils.mod import merge_playlists

# 合并多个播放列表
merged = merge_playlists([playlist1, playlist2], title="合并播放列表")
```

## 统计信息

```python
from playlist_utils.mod import get_statistics

stats = get_statistics(playlist)
print(f"曲目数: {stats['track_count']}")
print(f"总时长: {stats['total_duration_formatted']}")
print(f"独立艺术家: {stats['unique_artists']}")
print(f"独立专辑: {stats['unique_albums']}")
print(f"平均时长: {stats['average_duration']} 秒")
print(f"最短时长: {stats['min_duration']} 秒")
print(f"最长时长: {stats['max_duration']} 秒")
```

## JSON 支持

```python
from playlist_utils.mod import export_to_json, import_from_json

# 导出为 JSON
json_str = export_to_json(playlist)

# 从 JSON 导入
imported = import_from_json(json_str)
```

## 查找重复

```python
from playlist_utils.mod import find_duplicates

# 查找位置重复
duplicates = find_duplicates(playlist, by_location=True)
for idx, track in duplicates:
    print(f"索引 {idx}: {track.location}")
```

## 文件操作

```python
from playlist_utils.mod import load_file, save_file

# 加载文件
playlist = load_file("playlist.m3u")

# 保存文件
save_file(playlist, "output.xspf", format="xspf")
```

## 路径处理

```python
from playlist_utils.mod import make_relative_paths, make_absolute_paths

# 转换为相对路径
relative = make_relative_paths(playlist, "/music/base")

# 转换为绝对路径
absolute = make_absolute_paths(playlist, "/music/base")
```

## 数据结构

### Track

```python
@dataclass
class Track:
    location: str              # 文件路径或URL（必需）
    title: Optional[str]       # 标题
    duration: Optional[int]    # 时长（秒）
    artist: Optional[str]      # 艺术家
    album: Optional[str]       # 专辑
    track_number: Optional[int] # 音轨号
    info: Optional[str]        # 信息链接
    image: Optional[str]       # 封面图片
    album_artist: Optional[str] # 专辑艺术家
    composer: Optional[str]    # 作曲家
    genre: Optional[str]       # 流派
    year: Optional[int]        # 年份
```

### Playlist

```python
@dataclass
class Playlist:
    tracks: List[Track]        # 曲目列表
    title: Optional[str]       # 播放列表标题
    creator: Optional[str]     # 创建者
    annotation: Optional[str]  # 注释
    info: Optional[str]        # 信息链接
    location: Optional[str]    # 播放列表位置
    identifier: Optional[str]  # 唯一标识符
    image: Optional[str]       # 播放列表封面
    date: Optional[str]        # 创建日期
    license_url: Optional[str] # 许可证链接
```

## 支持的格式

| 格式 | 说明 | 特性 |
|------|------|------|
| M3U | 基本播放列表格式 | 简单文件列表 |
| M3U8 | 扩展 M3U 格式 | EXTINF 标签、时长、标题、艺术家 |
| PLS | INI 格式播放列表 | File/Title/Length 键值对 |
| XSPF | XML 播放列表格式 | 丰富的元数据、标准 XML 格式 |

## 格式详解

### M3U/M3U8

```
#EXTM3U
#PLAYLIST:播放列表标题
#EXTINF:180,歌曲标题
#EXTART:艺术家
#EXTALBUM:专辑
song.mp3
```

### PLS

```
[playlist]
File1=song.mp3
Title1=歌曲标题
Length1=180
NumberOfEntries=1
Version=2
```

### XSPF

```xml
<?xml version="1.0" encoding="UTF-8"?>
<playlist xmlns="http://xspf.org/ns/0/" version="1">
  <title>播放列表标题</title>
  <trackList>
    <track>
      <location>song.mp3</location>
      <title>歌曲标题</title>
      <creator>艺术家</creator>
      <album>专辑</album>
      <duration>180000</duration>
    </track>
  </trackList>
</playlist>
```

## 测试

运行测试：

```bash
python Python/playlist_utils/playlist_utils_test.py
```

运行示例：

```bash
python Python/playlist_utils/examples/usage_examples.py
```

## 许可证

MIT License

## 更新日志

- 2026-05-08: 初始版本，支持 M3U/M3U8、PLS、XSPF 格式