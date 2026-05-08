"""
Playlist Utils 使用示例

演示播放列表工具的各种功能。
"""

import sys
import os

# 添加父目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from playlist_utils.mod import (
    Track, Playlist,
    parse_m3u, generate_m3u,
    parse_pls, generate_pls,
    parse_xspf, generate_xspf,
    detect_format, parse, convert,
    merge_playlists,
    get_statistics, find_duplicates,
    export_to_json, import_from_json
)


def example_create_playlist():
    """示例：创建播放列表"""
    print("\n=== 创建播放列表 ===")
    
    # 创建播放列表
    playlist = Playlist(title="我的音乐", creator="测试用户")
    
    # 添加曲目
    playlist.add_track(Track(
        location="/music/song1.mp3",
        title="第一首歌",
        duration=180,
        artist="艺术家A",
        album="专辑X",
        track_number=1,
        genre="流行",
        year=2024
    ))
    
    playlist.add_track(Track(
        location="/music/song2.mp3",
        title="第二首歌",
        duration=240,
        artist="艺术家B",
        album="专辑Y"
    ))
    
    playlist.add_track(Track(
        location="/music/song3.mp3",
        title="第三首歌",
        duration=300,
        artist="艺术家A",
        album="专辑X"
    ))
    
    print(f"播放列表: {playlist.title}")
    print(f"曲目数: {len(playlist)}")
    print(f"总时长: {playlist.format_total_duration()}")
    
    # 打印每首曲目
    for i, track in enumerate(playlist, 1):
        print(f"{i}. {track.title} - {track.artist} ({track.format_duration()})")


def example_m3u_format():
    """示例：M3U 格式"""
    print("\n=== M3U/M3U8 格式 ===")
    
    # 创建播放列表
    playlist = Playlist(title="M3U 示例")
    playlist.add_track(Track(location="song1.mp3", title="歌曲 1", duration=180, artist="艺术家"))
    playlist.add_track(Track(location="song2.mp3", title="歌曲 2", duration=240))
    playlist.add_track(Track(location="http://example.com/stream.mp3", title="网络流", duration=-1))
    
    # 生成 M3U8 (扩展格式)
    print("\n生成 M3U8:")
    m3u8_content = generate_m3u(playlist, extended=True)
    print(m3u8_content)
    
    # 解析 M3U8
    print("\n解析 M3U8:")
    parsed = parse_m3u(m3u8_content)
    for track in parsed:
        print(f"- {track.title}: {track.location}")


def example_pls_format():
    """示例：PLS 格式"""
    print("\n=== PLS 格式 ===")
    
    # 创建播放列表
    playlist = Playlist()
    playlist.add_track(Track(location="song1.mp3", title="歌曲 1", duration=180))
    playlist.add_track(Track(location="song2.mp3", title="歌曲 2", duration=240))
    
    # 生成 PLS
    print("\n生成 PLS:")
    pls_content = generate_pls(playlist)
    print(pls_content)
    
    # 解析 PLS
    print("\n解析 PLS:")
    parsed = parse_pls(pls_content)
    for track in parsed:
        print(f"- {track.title}: {track.location} ({track.format_duration()})")


def example_xspf_format():
    """示例：XSPF 格式"""
    print("\n=== XSPF 格式 ===")
    
    # 创建播放列表
    playlist = Playlist(
        title="XSPF 示例",
        creator="测试用户",
        annotation="这是一个示例播放列表",
        info="http://example.com/info"
    )
    playlist.add_track(Track(
        location="/music/song1.mp3",
        title="歌曲 1",
        artist="艺术家",
        album="专辑",
        duration=180,
        track_number=1,
        genre="流行",
        year=2024
    ))
    playlist.add_track(Track(
        location="/music/song2.mp3",
        title="歌曲 2",
        duration=240
    ))
    
    # 生成 XSPF
    print("\n生成 XSPF:")
    xspf_content = generate_xspf(playlist)
    print(xspf_content)
    
    # 解析 XSPF
    print("\n解析 XSPF:")
    parsed = parse_xspf(xspf_content)
    print(f"标题: {parsed.title}")
    print(f"创建者: {parsed.creator}")
    for track in parsed:
        print(f"- {track.title}: {track.location}")


def example_format_conversion():
    """示例：格式转换"""
    print("\n=== 格式转换 ===")
    
    # M3U 内容
    m3u_content = """#EXTM3U
#PLAYLIST:我的歌曲
#EXTINF:180,歌曲 1
song1.mp3
#EXTINF:240,歌曲 2
song2.mp3
"""
    
    print("原始 M3U:")
    print(m3u_content)
    
    # 转换为 PLS
    print("\n转换为 PLS:")
    pls_content = convert(m3u_content, "m3u", "pls")
    print(pls_content)
    
    # 转换为 XSPF
    print("\n转换为 XSPF:")
    xspf_content = convert(m3u_content, "m3u", "xspf", playlist_title="我的歌曲")
    print(xspf_content)


def example_auto_detect():
    """示例：自动检测格式"""
    print("\n=== 自动检测格式 ===")
    
    # 不同格式的内容
    samples = {
        "M3U": "#EXTM3U\n#EXTINF:180,歌曲\nsong.mp3",
        "PLS": "[playlist]\nFile1=song.mp3\nNumberOfEntries=1",
        "XSPF": '<?xml version="1.0"?><playlist xmlns="http://xspf.org/ns/0/" version="1"></playlist>',
        "简单列表": "song1.mp3\nsong2.mp3"
    }
    
    for name, content in samples.items():
        format_name = detect_format(content)
        print(f"{name}: 检测为 '{format_name}' 格式")


def example_playlist_operations():
    """示例：播放列表操作"""
    print("\n=== 播放列表操作 ===")
    
    # 创建播放列表
    playlist = Playlist(title="操作示例")
    
    # 添加曲目（包括重复）
    playlist.add_track(Track(location="song1.mp3", title="歌曲 A", artist="艺术家 1", duration=180))
    playlist.add_track(Track(location="song2.mp3", title="歌曲 B", artist="艺术家 2", duration=240))
    playlist.add_track(Track(location="song1.mp3", title="歌曲 C", artist="艺术家 1", duration=300))  # 重复位置
    playlist.add_track(Track(location="song3.mp3", title="歌曲 D", artist="艺术家 2", duration=200))
    
    print(f"原始曲目数: {len(playlist)}")
    
    # 去重
    deduped = playlist.deduplicate(by_location=True)
    print(f"去重后曲目数: {len(deduped)}")
    
    # 排序
    sorted_by_title = playlist.sort_by_title()
    print("\n按标题排序:")
    for track in sorted_by_title:
        print(f"- {track.title}")
    
    sorted_by_duration = playlist.sort_by_duration(reverse=True)
    print("\n按时长排序（降序）:")
    for track in sorted_by_duration:
        print(f"- {track.title} ({track.format_duration()})")
    
    # 篛选
    filtered = playlist.filter_by_artist("艺术家 1")
    print(f"\n筛选艺术家 1: {len(filtered)} 首")
    
    filtered_duration = playlist.filter_by_duration(min_seconds=200, max_seconds=250)
    print(f"筛选时长 200-250秒: {len(filtered_duration)} 首")


def example_statistics():
    """示例：统计信息"""
    print("\n=== 统计信息 ===")
    
    playlist = Playlist(title="统计示例")
    playlist.add_track(Track(location="a.mp3", title="A", artist="艺术家 1", album="专辑 1", duration=120, genre="流行"))
    playlist.add_track(Track(location="b.mp3", title="B", artist="艺术家 1", album="专辑 1", duration=180, genre="流行"))
    playlist.add_track(Track(location="c.mp3", title="C", artist="艺术家 2", album="专辑 2", duration=240, genre="摇滚"))
    playlist.add_track(Track(location="d.mp3", title="D", artist="艺术家 3", album="专辑 3", duration=300, genre="摇滚"))
    playlist.add_track(Track(location="e.mp3", title="E", artist="艺术家 2", duration=None))
    
    stats = get_statistics(playlist)
    
    print(f"曲目数: {stats['track_count']}")
    print(f"总时长: {stats['total_duration_formatted']}")
    print(f"独立艺术家: {stats['unique_artists']}")
    print(f"独立专辑: {stats['unique_albums']}")
    print(f"独立流派: {stats['unique_genres']}")
    print(f"有时长曲目: {stats['tracks_with_duration']}")
    print(f"无时长曲目: {stats['tracks_without_duration']}")
    print(f"最短时长: {stats['min_duration']} 秒")
    print(f"最长时长: {stats['max_duration']} 秒")
    print(f"平均时长: {stats['average_duration']} 秒")


def example_merge_playlists():
    """示例：合并播放列表"""
    print("\n=== 合并播放列表 ===")
    
    # 创建两个播放列表
    p1 = Playlist(title="列表 1")
    p1.add_track(Track(location="song1.mp3", title="歌曲 1"))
    p1.add_track(Track(location="song2.mp3", title="歌曲 2"))
    
    p2 = Playlist(title="列表 2")
    p2.add_track(Track(location="song3.mp3", title="歌曲 3"))
    p2.add_track(Track(location="song4.mp3", title="歌曲 4"))
    
    print(f"列表 1: {len(p1)} 首")
    print(f"列表 2: {len(p2)} 首")
    
    # 合并
    merged = merge_playlists([p1, p2], title="合并列表")
    print(f"合并后: {len(merged)} 首")
    
    for track in merged:
        print(f"- {track.title}")


def example_json_export():
    """示例：JSON 导出导入"""
    print("\n=== JSON 导出导入 ===")
    
    playlist = Playlist(title="JSON 示例", creator="测试用户")
    playlist.add_track(Track(
        location="/music/song.mp3",
        title="歌曲",
        artist="艺术家",
        album="专辑",
        duration=180
    ))
    
    # 导出为 JSON
    json_str = export_to_json(playlist)
    print("导出的 JSON:")
    print(json_str)
    
    # 从 JSON 导入
    imported = import_from_json(json_str)
    print(f"\n导入的播放列表: {imported.title}")
    print(f"曲目数: {len(imported)}")


def example_find_duplicates():
    """示例：查找重复"""
    print("\n=== 查找重复 ===")
    
    playlist = Playlist()
    playlist.add_track(Track(location="song1.mp3", title="歌曲 A"))
    playlist.add_track(Track(location="song2.mp3", title="歌曲 B"))
    playlist.add_track(Track(location="song1.mp3", title="歌曲 C"))  # 重复位置
    playlist.add_track(Track(location="song3.mp3", title="歌曲 A"))  # 重复标题
    
    # 查找位置重复
    duplicates = find_duplicates(playlist, by_location=True)
    print(f"位置重复数: {len(duplicates)}")
    for idx, track in duplicates:
        print(f"- 索引 {idx}: {track.location}")
    
    # 查找标题重复
    duplicates = find_duplicates(playlist, by_title=True)
    print(f"\n标题重复数: {len(duplicates)}")


def example_network_playlist():
    """示例：网络播放列表"""
    print("\n=== 网络播放列表 ===")
    
    # 创建包含网络流的播放列表
    playlist = Playlist(title="网络电台")
    playlist.add_track(Track(
        location="http://stream.example.com:8000/live.mp3",
        title="直播流 1",
        duration=-1
    ))
    playlist.add_track(Track(
        location="https://server.example.com/radio.ogg",
        title="直播流 2",
        duration=-1,
        image="http://example.com/logo.png"
    ))
    
    # M3U8 支持网络属性
    m3u8 = generate_m3u(playlist, extended=True)
    print("网络播放列表 M3U8:")
    print(m3u8)


def example_complete_workflow():
    """示例：完整工作流程"""
    print("\n=== 完整工作流程 ===")
    
    # 1. 创建播放列表
    playlist = Playlist(title="我的收藏", creator="音乐爱好者")
    
    songs = [
        ("流行歌曲", "流行歌手", "流行专辑", 180),
        ("摇滚歌曲", "摇滚乐队", "摇滚专辑", 240),
        ("古典曲目", "古典乐团", "古典专辑", 300),
        ("爵士乐曲", "爵士大师", "爵士专辑", 210),
    ]
    
    for i, (title, artist, album, duration) in enumerate(songs, 1):
        playlist.add_track(Track(
            location=f"/music/{title}.mp3",
            title=title,
            artist=artist,
            album=album,
            duration=duration,
            track_number=i
        ))
    
    print(f"创建了播放列表: {playlist.title}")
    print(f"曲目数: {len(playlist)}")
    print(f"总时长: {playlist.format_total_duration()}")
    
    # 2. 生成不同格式
    print("\n生成 M3U8 格式...")
    m3u8 = generate_m3u(playlist)
    
    print("生成 PLS 格式...")
    pls = generate_pls(playlist)
    
    print("生成 XSPF 格式...")
    xspf = generate_xspf(playlist)
    
    # 3. 统计信息
    stats = get_statistics(playlist)
    print(f"\n统计信息:")
    print(f"  - 平均时长: {stats['average_duration']} 秒")
    print(f"  - 独立艺术家: {stats['unique_artists']}")
    
    # 4. JSON 导出
    json_data = export_to_json(playlist)
    print(f"\nJSON 导出长度: {len(json_data)} 字符")


def run_all_examples():
    """运行所有示例"""
    print("="*60)
    print("Playlist Utils 使用示例")
    print("="*60)
    
    example_create_playlist()
    example_m3u_format()
    example_pls_format()
    example_xspf_format()
    example_format_conversion()
    example_auto_detect()
    example_playlist_operations()
    example_statistics()
    example_merge_playlists()
    example_json_export()
    example_find_duplicates()
    example_network_playlist()
    example_complete_workflow()
    
    print("\n"+"="*60)
    print("示例演示完成")
    print("="*60)


if __name__ == "__main__":
    run_all_examples()