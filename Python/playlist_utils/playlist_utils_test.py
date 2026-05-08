"""
Playlist Utils 测试

测试播放列表工具的所有功能。
"""

import sys
import os
import json

# 添加父目录到路径以便导入
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from playlist_utils.mod import (
    Track, Playlist,
    parse_m3u, generate_m3u,
    parse_pls, generate_pls,
    parse_xspf, generate_xspf,
    detect_format, parse, convert,
    merge_playlists,
    get_statistics, find_duplicates,
    export_to_json, import_from_json,
    make_relative_paths, make_absolute_paths,
    validate_locations
)


class TestResult:
    """测试结果收集器"""
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.errors = []
    
    def assert_equal(self, actual, expected, message=""):
        if actual != expected:
            self.failed += 1
            self.errors.append(f"断言失败: {message}\n  期望: {expected}\n  实际: {actual}")
            return False
        self.passed += 1
        return True
    
    def assert_true(self, condition, message=""):
        if not condition:
            self.failed += 1
            self.errors.append(f"断言失败: {message}\n  期望: True\n  实际: False")
            return False
        self.passed += 1
        return True
    
    def assert_false(self, condition, message=""):
        if condition:
            self.failed += 1
            self.errors.append(f"断言失败: {message}\n  期望: False\n  实际: True")
            return False
        self.passed += 1
        return True
    
    def assert_in(self, item, container, message=""):
        if item not in container:
            self.failed += 1
            self.errors.append(f"断言失败: {message}\n  期望 '{item}' 在 {container} 中")
            return False
        self.passed += 1
        return True
    
    def assert_not_in(self, item, container, message=""):
        if item in container:
            self.failed += 1
            self.errors.append(f"断言失败: {message}\n  期望 '{item}' 不在 {container} 中")
            return False
        self.passed += 1
        return True
    
    def assert_is_none(self, value, message=""):
        if value is not None:
            self.failed += 1
            self.errors.append(f"断言失败: {message}\n  期望: None\n  实际: {value}")
            return False
        self.passed += 1
        return True
    
    def assert_is_not_none(self, value, message=""):
        if value is None:
            self.failed += 1
            self.errors.append(f"断言失败: {message}\n  期望: 非 None\n  实际: None")
            return False
        self.passed += 1
        return True
    
    def assert_greater(self, actual, expected, message=""):
        if not (actual > expected):
            self.failed += 1
            self.errors.append(f"断言失败: {message}\n  期望: {actual} > {expected}")
            return False
        self.passed += 1
        return True
    
    def assert_less(self, actual, expected, message=""):
        if not (actual < expected):
            self.failed += 1
            self.errors.append(f"断言失败: {message}\n  期望: {actual} < {expected}")
            return False
        self.passed += 1
        return True
    
    def assert_greater_equal(self, actual, expected, message=""):
        if not (actual >= expected):
            self.failed += 1
            self.errors.append(f"断言失败: {message}\n  期望: {actual} >= {expected}")
            return False
        self.passed += 1
        return True
    
    def summary(self):
        total = self.passed + self.failed
        print(f"\n{'='*60}")
        print(f"测试结果: {self.passed} 通过, {self.failed} 失败, 共 {total} 个")
        print(f"{'='*60}")
        
        if self.errors:
            print("\n失败的测试:")
            for i, error in enumerate(self.errors, 1):
                print(f"\n{i}. {error}")
        
        return self.failed == 0


# ============== Track 测试 ==============

def test_track_creation(r: TestResult):
    """测试 Track 创建"""
    print("\n--- 测试 Track 创建 ---")
    
    track = Track(
        location="/path/to/song.mp3",
        title="Test Song",
        duration=180,
        artist="Test Artist",
        album="Test Album"
    )
    
    r.assert_equal(track.location, "/path/to/song.mp3", "Track location")
    r.assert_equal(track.title, "Test Song", "Track title")
    r.assert_equal(track.duration, 180, "Track duration")
    r.assert_equal(track.artist, "Test Artist", "Track artist")
    r.assert_equal(track.album, "Test Album", "Track album")


def test_track_format_duration(r: TestResult):
    """测试 Track 时长格式化"""
    print("\n--- 测试 Track 时长格式化 ---")
    
    track1 = Track(location="test.mp3", duration=185)  # 3:05
    r.assert_equal(track1.format_duration(), "3:05", "3分钟5秒")
    
    track2 = Track(location="test.mp3", duration=3661)  # 1:01:01
    r.assert_equal(track2.format_duration(), "1:01:01", "1小时1分1秒")
    
    track3 = Track(location="test.mp3", duration=-1)
    r.assert_equal(track3.format_duration(), "?:??", "未知时长")
    
    track4 = Track(location="test.mp3", duration=None)
    r.assert_equal(track4.format_duration(), "?:??", "None 时长")


def test_track_to_dict(r: TestResult):
    """测试 Track 字典转换"""
    print("\n--- 测试 Track 字典转换 ---")
    
    track = Track(
        location="/path/to/song.mp3",
        title="Test Song",
        duration=180,
        artist="Test Artist",
        album="Test Album",
        track_number=1,
        genre="Rock",
        year=2024
    )
    
    d = track.to_dict()
    r.assert_equal(d['location'], "/path/to/song.mp3", "dict location")
    r.assert_equal(d['title'], "Test Song", "dict title")
    r.assert_equal(d['duration'], 180, "dict duration")
    r.assert_equal(d['artist'], "Test Artist", "dict artist")
    r.assert_equal(d['album'], "Test Album", "dict album")
    r.assert_equal(d['track_number'], 1, "dict track_number")
    r.assert_equal(d['genre'], "Rock", "dict genre")
    r.assert_equal(d['year'], 2024, "dict year")
    
    # 从字典创建
    track2 = Track.from_dict(d)
    r.assert_equal(track2.location, track.location, "from_dict location")
    r.assert_equal(track2.title, track.title, "from_dict title")
    r.assert_equal(track2.duration, track.duration, "from_dict duration")


# ============== Playlist 测试 ==============

def test_playlist_creation(r: TestResult):
    """测试 Playlist 创建"""
    print("\n--- 测试 Playlist 创建 ---")
    
    playlist = Playlist(title="My Playlist", creator="Test User")
    
    r.assert_equal(playlist.title, "My Playlist", "Playlist title")
    r.assert_equal(playlist.creator, "Test User", "Playlist creator")
    r.assert_equal(len(playlist), 0, "Empty playlist")


def test_playlist_add_remove(r: TestResult):
    """测试 Playlist 添加和移除"""
    print("\n--- 测试 Playlist 添加和移除 ---")
    
    playlist = Playlist()
    
    track1 = Track(location="song1.mp3", title="Song 1")
    track2 = Track(location="song2.mp3", title="Song 2")
    
    playlist.add_track(track1)
    playlist.add_track(track2)
    
    r.assert_equal(len(playlist), 2, "添加2首曲目")
    
    removed = playlist.remove_track(0)
    r.assert_is_not_none(removed, "移除成功")
    r.assert_equal(removed.title, "Song 1", "移除正确的曲目")
    r.assert_equal(len(playlist), 1, "剩余1首曲目")
    
    # 移除无效索引
    removed = playlist.remove_track(10)
    r.assert_is_none(removed, "移除无效索引返回 None")


def test_playlist_total_duration(r: TestResult):
    """测试 Playlist 总时长"""
    print("\n--- 测试 Playlist 总时长 ---")
    
    playlist = Playlist()
    playlist.add_track(Track(location="song1.mp3", duration=120))
    playlist.add_track(Track(location="song2.mp3", duration=180))
    playlist.add_track(Track(location="song3.mp3", duration=-1))  # 未知
    playlist.add_track(Track(location="song4.mp3", duration=None))  # None
    
    total = playlist.get_total_duration()
    r.assert_equal(total, 300, "总时长计算")
    
    formatted = playlist.format_total_duration()
    r.assert_in("5", formatted, "格式化时长包含分钟")


def test_playlist_deduplicate(r: TestResult):
    """测试 Playlist 去重"""
    print("\n--- 测试 Playlist 去重 ---")
    
    playlist = Playlist()
    playlist.add_track(Track(location="song.mp3", title="Song A"))
    playlist.add_track(Track(location="song.mp3", title="Song B"))  # 重复位置
    playlist.add_track(Track(location="other.mp3", title="Song A"))  # 重复标题
    playlist.add_track(Track(location="unique.mp3", title="Unique"))
    
    # 按位置去重
    deduped = playlist.deduplicate(by_location=True, by_title=False)
    r.assert_equal(len(deduped), 3, "按位置去重后3首")
    
    # 按标题去重
    deduped = playlist.deduplicate(by_location=False, by_title=True)
    r.assert_equal(len(deduped), 3, "按标题去重后3首")


def test_playlist_sort(r: TestResult):
    """测试 Playlist 排序"""
    print("\n--- 测试 Playlist 排序 ---")
    
    playlist = Playlist()
    playlist.add_track(Track(location="a.mp3", title="C Song", artist="Artist B", duration=300))
    playlist.add_track(Track(location="b.mp3", title="A Song", artist="Artist A", duration=180))
    playlist.add_track(Track(location="c.mp3", title="B Song", artist="Artist C", duration=240))
    
    # 按标题排序
    sorted_playlist = playlist.sort_by_title()
    r.assert_equal(sorted_playlist[0].title, "A Song", "按标题排序第一个")
    r.assert_equal(sorted_playlist[2].title, "C Song", "按标题排序最后一个")
    
    # 按艺术家排序
    sorted_playlist = playlist.sort_by_artist()
    r.assert_equal(sorted_playlist[0].artist, "Artist A", "按艺术家排序第一个")
    r.assert_equal(sorted_playlist[2].artist, "Artist C", "按艺术家排序最后一个")
    
    # 按时长排序
    sorted_playlist = playlist.sort_by_duration()
    r.assert_equal(sorted_playlist[0].duration, 180, "按时长排序最短")
    r.assert_equal(sorted_playlist[2].duration, 300, "按时长排序最长")
    
    # 降序排序
    sorted_playlist = playlist.sort_by_duration(reverse=True)
    r.assert_equal(sorted_playlist[0].duration, 300, "降序排序第一个")


def test_playlist_filter(r: TestResult):
    """测试 Playlist 筛选"""
    print("\n--- 测试 Playlist 筛选 ---")
    
    playlist = Playlist()
    playlist.add_track(Track(location="a.mp3", title="Song A", artist="Artist A", album="Album 1", duration=180))
    playlist.add_track(Track(location="b.mp3", title="Song B", artist="Artist B", album="Album 2", duration=240))
    playlist.add_track(Track(location="c.mp3", title="Song C", artist="Artist A", album="Album 1", duration=300))
    
    # 按艺术家筛选
    filtered = playlist.filter_by_artist("Artist A")
    r.assert_equal(len(filtered), 2, "Artist A 有2首")
    
    # 按专辑筛选
    filtered = playlist.filter_by_album("Album 1")
    r.assert_equal(len(filtered), 2, "Album 1 有2首")
    
    # 按时长筛选
    filtered = playlist.filter_by_duration(min_seconds=200, max_seconds=280)
    r.assert_equal(len(filtered), 1, "时长200-280秒有1首")


# ============== M3U 格式测试 ==============

def test_parse_simple_m3u(r: TestResult):
    """测试解析简单 M3U"""
    print("\n--- 测试解析简单 M3U ---")
    
    content = """song1.mp3
song2.mp3
/songs/song3.mp3
http://example.com/song4.mp3
"""
    
    playlist = parse_m3u(content)
    
    r.assert_equal(len(playlist), 4, "解析4首曲目")
    r.assert_equal(playlist[0].location, "song1.mp3", "第一首位置")
    r.assert_equal(playlist[3].location, "http://example.com/song4.mp3", "URL 位置")


def test_parse_extended_m3u(r: TestResult):
    """测试解析扩展 M3U (M3U8)"""
    print("\n--- 测试解析扩展 M3U ---")
    
    content = """#EXTM3U
#PLAYLIST:My Playlist
#EXTINF:180,Artist - Song Title
song1.mp3
#EXTINF:240,Another Song
#EXTART:Another Artist
song2.mp3
#EXTINF:-1,Unknown Duration
song3.mp3
"""
    
    playlist = parse_m3u(content)
    
    r.assert_equal(playlist.title, "My Playlist", "播放列表标题")
    r.assert_equal(len(playlist), 3, "3首曲目")
    
    r.assert_equal(playlist[0].title, "Artist - Song Title", "第一首标题")
    r.assert_equal(playlist[0].duration, 180, "第一首时长")
    r.assert_equal(playlist[1].artist, "Another Artist", "第二首艺术家")
    r.assert_equal(playlist[1].duration, 240, "第二首时长")
    r.assert_is_none(playlist[2].duration, "未知时长为 None")


def test_generate_m3u(r: TestResult):
    """测试生成 M3U"""
    print("\n--- 测试生成 M3U ---")
    
    playlist = Playlist(title="Test Playlist")
    playlist.add_track(Track(location="song1.mp3", title="Song 1", duration=180, artist="Artist A"))
    playlist.add_track(Track(location="song2.mp3", title="Song 2", duration=240))
    
    # 扩展格式
    content = generate_m3u(playlist, extended=True)
    
    r.assert_in("#EXTM3U", content, "包含 EXTM3U 头")
    r.assert_in("#PLAYLIST:Test Playlist", content, "包含播放列表标题")
    r.assert_in("#EXTINF:180,Song 1", content, "包含 EXTINF")
    r.assert_in("#EXTART:Artist A", content, "包含艺术家")
    r.assert_in("song1.mp3", content, "包含文件路径")
    
    # 简单格式
    content = generate_m3u(playlist, extended=False)
    r.assert_not_in("#EXTM3U", content, "简单格式不包含 EXTM3U")
    r.assert_in("song1.mp3", content, "简单格式包含文件路径")


def test_m3u_roundtrip(r: TestResult):
    """测试 M3U 往返转换"""
    print("\n--- 测试 M3U 往返转换 ---")
    
    original = Playlist(title="Roundtrip Test")
    original.add_track(Track(location="/music/song1.mp3", title="Song 1", duration=180, artist="Artist A", album="Album X"))
    original.add_track(Track(location="/music/song2.mp3", title="Song 2", duration=240))
    
    content = generate_m3u(original, extended=True)
    parsed = parse_m3u(content)
    
    r.assert_equal(parsed.title, original.title, "标题一致")
    r.assert_equal(len(parsed), len(original), "曲目数一致")
    r.assert_equal(parsed[0].title, original[0].title, "第一首标题一致")
    r.assert_equal(parsed[0].duration, original[0].duration, "第一首时长一致")


# ============== PLS 格式测试 ==============

def test_parse_pls(r: TestResult):
    """测试解析 PLS"""
    print("\n--- 测试解析 PLS ---")
    
    content = """[playlist]
File1=/music/song1.mp3
Title1=Song 1
Length1=180
File2=/music/song2.mp3
Title2=Song 2
Length2=240
NumberOfEntries=2
Version=2
"""
    
    playlist = parse_pls(content)
    
    r.assert_equal(len(playlist), 2, "解析2首曲目")
    r.assert_equal(playlist[0].location, "/music/song1.mp3", "第一首位置")
    r.assert_equal(playlist[0].title, "Song 1", "第一首标题")
    r.assert_equal(playlist[0].duration, 180, "第一首时长")
    r.assert_equal(playlist[1].location, "/music/song2.mp3", "第二首位置")


def test_generate_pls(r: TestResult):
    """测试生成 PLS"""
    print("\n--- 测试生成 PLS ---")
    
    playlist = Playlist()
    playlist.add_track(Track(location="song1.mp3", title="Song 1", duration=180))
    playlist.add_track(Track(location="song2.mp3", title="Song 2", duration=240))
    
    content = generate_pls(playlist)
    
    r.assert_in("[playlist]", content, "包含 playlist 头")
    r.assert_in("File1=song1.mp3", content, "包含 File1")
    r.assert_in("Title1=Song 1", content, "包含 Title1")
    r.assert_in("Length1=180", content, "包含 Length1")
    r.assert_in("NumberOfEntries=2", content, "包含 NumberOfEntries")
    r.assert_in("Version=2", content, "包含 Version")


def test_pls_roundtrip(r: TestResult):
    """测试 PLS 往返转换"""
    print("\n--- 测试 PLS 往返转换 ---")
    
    original = Playlist()
    original.add_track(Track(location="/music/song1.mp3", title="Song 1", duration=180))
    original.add_track(Track(location="/music/song2.mp3", title="Song 2", duration=240))
    
    content = generate_pls(original)
    parsed = parse_pls(content)
    
    r.assert_equal(len(parsed), len(original), "曲目数一致")
    r.assert_equal(parsed[0].location, original[0].location, "第一首位置一致")
    r.assert_equal(parsed[0].duration, original[0].duration, "第一首时长一致")


# ============== XSPF 格式测试 ==============

def test_parse_xspf(r: TestResult):
    """测试解析 XSPF"""
    print("\n--- 测试解析 XSPF ---")
    
    content = """<?xml version="1.0" encoding="UTF-8"?>
<playlist xmlns="http://xspf.org/ns/0/" version="1">
  <title>My Playlist</title>
  <creator>Test User</creator>
  <trackList>
    <track>
      <location>/music/song1.mp3</location>
      <title>Song 1</title>
      <creator>Artist A</creator>
      <album>Album X</album>
      <duration>180000</duration>
      <trackNum>1</trackNum>
    </track>
    <track>
      <location>/music/song2.mp3</location>
      <title>Song 2</title>
      <creator>Artist B</creator>
      <duration>240000</duration>
    </track>
  </trackList>
</playlist>
"""
    
    playlist = parse_xspf(content)
    
    r.assert_equal(playlist.title, "My Playlist", "播放列表标题")
    r.assert_equal(playlist.creator, "Test User", "创建者")
    r.assert_equal(len(playlist), 2, "2首曲目")
    
    r.assert_equal(playlist[0].location, "/music/song1.mp3", "第一首位置")
    r.assert_equal(playlist[0].title, "Song 1", "第一首标题")
    r.assert_equal(playlist[0].artist, "Artist A", "第一首艺术家")
    r.assert_equal(playlist[0].album, "Album X", "第一首专辑")
    r.assert_equal(playlist[0].duration, 180, "第一首时长（秒）")
    r.assert_equal(playlist[0].track_number, 1, "第一首音轨号")


def test_generate_xspf(r: TestResult):
    """测试生成 XSPF"""
    print("\n--- 测试生成 XSPF ---")
    
    playlist = Playlist(title="Test Playlist", creator="Test User")
    playlist.add_track(Track(
        location="song1.mp3",
        title="Song 1",
        artist="Artist A",
        album="Album X",
        duration=180,
        track_number=1
    ))
    
    content = generate_xspf(playlist)
    
    r.assert_in('<?xml', content, "包含 XML 声明")
    r.assert_in('<playlist', content, "包含 playlist 元素")
    r.assert_in('<title>Test Playlist</title>', content, "包含标题")
    r.assert_in('<creator>Test User</creator>', content, "包含创建者")
    r.assert_in('<location>song1.mp3</location>', content, "包含位置")
    r.assert_in('<title>Song 1</title>', content, "包含曲目标题")
    r.assert_in('<creator>Artist A</creator>', content, "包含艺术家")
    r.assert_in('<duration>180000</duration>', content, "包含时长（毫秒）")


def test_xspf_roundtrip(r: TestResult):
    """测试 XSPF 往返转换"""
    print("\n--- 测试 XSPF 往返转换 ---")
    
    original = Playlist(title="Roundtrip", creator="Test")
    original.add_track(Track(location="song1.mp3", title="Song 1", artist="Artist A", duration=180))
    original.add_track(Track(location="song2.mp3", title="Song 2", duration=240))
    
    content = generate_xspf(original)
    parsed = parse_xspf(content)
    
    r.assert_equal(parsed.title, original.title, "标题一致")
    r.assert_equal(len(parsed), len(original), "曲目数一致")
    r.assert_equal(parsed[0].title, original[0].title, "第一首标题一致")
    r.assert_equal(parsed[0].duration, original[0].duration, "第一首时长一致")


# ============== 格式检测测试 ==============

def test_detect_format(r: TestResult):
    """测试格式检测"""
    print("\n--- 测试格式检测 ---")
    
    # M3U
    m3u_content = "#EXTM3U\nsong1.mp3"
    r.assert_equal(detect_format(m3u_content), "m3u", "检测 M3U")
    
    # PLS
    pls_content = "[playlist]\nFile1=song.mp3"
    r.assert_equal(detect_format(pls_content), "pls", "检测 PLS")
    
    # XSPF
    xspf_content = '<?xml version="1.0"?><playlist version="1"></playlist>'
    r.assert_equal(detect_format(xspf_content), "xspf", "检测 XSPF")
    
    # 简单文件列表
    simple_content = "song1.mp3\nsong2.mp3"
    r.assert_equal(detect_format(simple_content), "m3u", "检测简单 M3U")


def test_parse_auto(r: TestResult):
    """测试自动解析"""
    print("\n--- 测试自动解析 ---")
    
    m3u_content = "#EXTM3U\n#EXTINF:180,Song\nsong.mp3"
    pls_content = "[playlist]\nFile1=song.mp3\nNumberOfEntries=1"
    xspf_content = '<?xml version="1.0"?><playlist version="1"><trackList></trackList></playlist>'
    
    m3u_playlist = parse(m3u_content)
    r.assert_equal(len(m3u_playlist), 1, "自动解析 M3U")
    
    pls_playlist = parse(pls_content)
    r.assert_equal(len(pls_playlist), 1, "自动解析 PLS")
    
    xspf_playlist = parse(xspf_content)
    r.assert_equal(len(xspf_playlist), 0, "自动解析 XSPF")


# ============== 格式转换测试 ==============

def test_convert_format(r: TestResult):
    """测试格式转换"""
    print("\n--- 测试格式转换 ---")
    
    m3u_content = """#EXTM3U
#PLAYLIST:My Songs
#EXTINF:180,Song 1
song1.mp3
#EXTINF:240,Song 2
song2.mp3
"""
    
    # M3U -> PLS
    pls_content = convert(m3u_content, "m3u", "pls")
    r.assert_in("[playlist]", pls_content, "M3U 转 PLS")
    r.assert_in("File1=song1.mp3", pls_content, "PLS 包含 File1")
    
    # M3U -> XSPF
    xspf_content = convert(m3u_content, "m3u", "xspf")
    r.assert_in("<playlist", xspf_content, "M3U 转 XSPF")
    r.assert_in("<location>song1.mp3</location>", xspf_content, "XSPF 包含位置")
    
    # PLS -> M3U
    pls_to_m3u = convert(pls_content, "pls", "m3u")
    r.assert_in("#EXTM3U", pls_to_m3u, "PLS 转 M3U")


# ============== 实用函数测试 ==============

def test_merge_playlists(r: TestResult):
    """测试合并播放列表"""
    print("\n--- 测试合并播放列表 ---")
    
    p1 = Playlist(title="Playlist 1")
    p1.add_track(Track(location="song1.mp3", title="Song 1"))
    p1.add_track(Track(location="song2.mp3", title="Song 2"))
    
    p2 = Playlist(title="Playlist 2")
    p2.add_track(Track(location="song3.mp3", title="Song 3"))
    p2.add_track(Track(location="song4.mp3", title="Song 4"))
    
    merged = merge_playlists([p1, p2], title="Merged")
    
    r.assert_equal(len(merged), 4, "合并后4首")
    r.assert_equal(merged.title, "Merged", "合并后标题")


def test_statistics(r: TestResult):
    """测试统计信息"""
    print("\n--- 测试统计信息 ---")
    
    playlist = Playlist()
    playlist.add_track(Track(location="a.mp3", title="A", artist="Artist 1", album="Album 1", duration=120))
    playlist.add_track(Track(location="b.mp3", title="B", artist="Artist 1", album="Album 1", duration=180))
    playlist.add_track(Track(location="c.mp3", title="C", artist="Artist 2", album="Album 2", duration=240))
    playlist.add_track(Track(location="d.mp3", title="D", duration=None))  # 无时长
    
    stats = get_statistics(playlist)
    
    r.assert_equal(stats['track_count'], 4, "曲目数")
    r.assert_equal(stats['total_duration'], 540, "总时长")
    r.assert_equal(stats['unique_artists'], 2, "艺术家数")
    r.assert_equal(stats['unique_albums'], 2, "专辑数")
    r.assert_equal(stats['tracks_with_duration'], 3, "有时长曲目")
    r.assert_equal(stats['tracks_without_duration'], 1, "无时长曲目")
    r.assert_equal(stats['min_duration'], 120, "最短时长")
    r.assert_equal(stats['max_duration'], 240, "最长时长")


def test_find_duplicates(r: TestResult):
    """测试查找重复"""
    print("\n--- 测试查找重复 ---")
    
    playlist = Playlist()
    playlist.add_track(Track(location="song1.mp3", title="Song A"))
    playlist.add_track(Track(location="song2.mp3", title="Song B"))
    playlist.add_track(Track(location="song1.mp3", title="Song C"))  # 重复位置
    playlist.add_track(Track(location="song3.mp3", title="Song A"))  # 重复标题
    
    # 按位置查找重复
    duplicates = find_duplicates(playlist, by_location=True, by_title=False)
    r.assert_equal(len(duplicates), 1, "按位置找到1个重复")
    r.assert_equal(duplicates[0][1].location, "song1.mp3", "重复位置正确")
    
    # 按标题查找重复
    duplicates = find_duplicates(playlist, by_location=False, by_title=True)
    r.assert_equal(len(duplicates), 1, "按标题找到1个重复")


def test_json_export_import(r: TestResult):
    """测试 JSON 导出导入"""
    print("\n--- 测试 JSON 导出导入 ---")
    
    playlist = Playlist(title="JSON Test", creator="Test User")
    playlist.add_track(Track(location="song.mp3", title="Song", artist="Artist", duration=180))
    
    # 导出
    json_str = export_to_json(playlist)
    r.assert_in('"title": "JSON Test"', json_str, "JSON 包含标题")
    r.assert_in('"location": "song.mp3"', json_str, "JSON 包含位置")
    
    # 导入
    imported = import_from_json(json_str)
    r.assert_equal(imported.title, playlist.title, "导入标题一致")
    r.assert_equal(len(imported), len(playlist), "导入曲目数一致")
    r.assert_equal(imported[0].location, playlist[0].location, "导入位置一致")


def test_shuffle(r: TestResult):
    """测试随机排序"""
    print("\n--- 测试随机排序 ---")
    
    playlist = Playlist()
    for i in range(20):
        playlist.add_track(Track(location=f"song{i}.mp3", title=f"Song {i}"))
    
    shuffled = playlist.shuffle()
    
    r.assert_equal(len(shuffled), len(playlist), "随机排序后数量一致")
    
    # 检查是否所有元素都存在
    original_locations = set(t.location for t in playlist)
    shuffled_locations = set(t.location for t in shuffled)
    r.assert_equal(original_locations, shuffled_locations, "所有元素都存在")


def test_validate_locations(r: TestResult):
    """测试位置验证"""
    print("\n--- 测试位置验证 ---")
    
    playlist = Playlist()
    # 添加一个存在的文件
    playlist.add_track(Track(location="/tmp", title="Exists"))
    # 添加一个不存在的文件
    playlist.add_track(Track(location="/nonexistent/file.mp3", title="Not Exists"))
    # 添加一个 URL
    playlist.add_track(Track(location="http://example.com/song.mp3", title="Remote"))
    
    result = validate_locations(playlist)
    
    r.assert_greater_equal(len(result['valid']), 1, "至少有1个有效")
    r.assert_greater_equal(len(result['invalid']), 1, "至少有1个无效")
    r.assert_greater_equal(len(result['remote']), 1, "至少有1个远程")


def test_empty_playlist(r: TestResult):
    """测试空播放列表"""
    print("\n--- 测试空播放列表 ---")
    
    playlist = Playlist()
    
    r.assert_equal(len(playlist), 0, "空播放列表长度为0")
    r.assert_equal(playlist.get_total_duration(), 0, "空播放列表总时长为0")
    
    # 生成空播放列表
    m3u = generate_m3u(playlist, extended=True)
    r.assert_in("#EXTM3U", m3u, "空 M3U 有头")
    
    pls = generate_pls(playlist)
    r.assert_in("NumberOfEntries=0", pls, "空 PLS 有 0 条目")
    
    xspf = generate_xspf(playlist)
    r.assert_in("trackList", xspf, "空 XSPF 有 trackList")


def test_special_characters(r: TestResult):
    """测试特殊字符处理"""
    print("\n--- 测试特殊字符处理 ---")
    
    playlist = Playlist(title="特殊字符测试")
    playlist.add_track(Track(
        location="/音乐/歌曲.mp3",
        title="歌曲名称 & <特殊> 字符",
        artist="艺术家 \"名字\"",
        album="专辑 <测试>"
    ))
    
    # M3U
    m3u = generate_m3u(playlist, extended=True)
    r.assert_in("歌曲名称 & <特殊> 字符", m3u, "M3U 包含特殊字符")
    
    # XSPF (XML 需要转义)
    xspf = generate_xspf(playlist)
    r.assert_in("&lt;特殊&gt;", xspf, "XSPF 转义 < 和 >")
    
    # 解析回来
    parsed_xspf = parse_xspf(xspf)
    r.assert_in("特殊", parsed_xspf[0].title, "解析后包含特殊字符")


def test_unicode_support(r: TestResult):
    """测试 Unicode 支持"""
    print("\n--- 测试 Unicode 支持 ---")
    
    playlist = Playlist(title="Unicode 测试 🎵")
    playlist.add_track(Track(
        location="/music/日本語/歌曲.mp3",
        title="日本語タイトル 🎌",
        artist="한국어 아티스트",
        album="Ελληνικά άλμπουμ"
    ))
    
    m3u = generate_m3u(playlist, extended=True)
    parsed = parse_m3u(m3u)
    
    r.assert_equal(parsed[0].title, "日本語タイトル 🎌", "Unicode 标题一致")
    r.assert_equal(parsed[0].artist, "한국어 아티스트", "Unicode 艺术家一致")
    
    xspf = generate_xspf(playlist)
    parsed_xspf = parse_xspf(xspf)
    r.assert_equal(parsed_xspf[0].title, "日本語タイトル 🎌", "XSPF Unicode 标题一致")


# ============== 运行所有测试 ==============

def run_all_tests():
    """运行所有测试"""
    r = TestResult()
    
    print("="*60)
    print("Playlist Utils 测试套件")
    print("="*60)
    
    # Track 测试
    test_track_creation(r)
    test_track_format_duration(r)
    test_track_to_dict(r)
    
    # Playlist 测试
    test_playlist_creation(r)
    test_playlist_add_remove(r)
    test_playlist_total_duration(r)
    test_playlist_deduplicate(r)
    test_playlist_sort(r)
    test_playlist_filter(r)
    
    # M3U 测试
    test_parse_simple_m3u(r)
    test_parse_extended_m3u(r)
    test_generate_m3u(r)
    test_m3u_roundtrip(r)
    
    # PLS 测试
    test_parse_pls(r)
    test_generate_pls(r)
    test_pls_roundtrip(r)
    
    # XSPF 测试
    test_parse_xspf(r)
    test_generate_xspf(r)
    test_xspf_roundtrip(r)
    
    # 格式检测和转换测试
    test_detect_format(r)
    test_parse_auto(r)
    test_convert_format(r)
    
    # 实用函数测试
    test_merge_playlists(r)
    test_statistics(r)
    test_find_duplicates(r)
    test_json_export_import(r)
    test_shuffle(r)
    test_validate_locations(r)
    
    # 边界测试
    test_empty_playlist(r)
    test_special_characters(r)
    test_unicode_support(r)
    
    return r.summary()


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)