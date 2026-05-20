"""
摩尔斯电码工具使用示例

演示如何使用 morse_utils 模块进行:
- 文本编码为摩尔斯电码
- 摩尔斯电码解码为文本
- 音频生成与保存
- 统计信息获取
- 可视化输出
- 练习功能
"""

import sys
import os

# 添加父目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from morse_utils.mod import (
    MorseUtils, MorseEncoder, MorseDecoder, MorseAudioGenerator,
    MorseConfig, encode, decode, get_morse_table, get_abbreviations
)


def example_basic_encoding():
    """基本编码示例"""
    print("\n" + "="*60)
    print("示例 1: 基本编码")
    print("="*60)
    
    # 使用便捷函数
    text = "HELLO WORLD"
    morse = encode(text)
    print(f"原文: {text}")
    print(f"电码: {morse}")
    
    # 使用类
    encoder = MorseEncoder()
    texts = ["SOS", "MORSE CODE", "ABC123"]
    for t in texts:
        print(f"{t} -> {encoder.encode(t)}")


def example_basic_decoding():
    """基本解码示例"""
    print("\n" + "="*60)
    print("示例 2: 基本解码")
    print("="*60)
    
    # 使用便捷函数
    morse = "... --- ..."
    text = decode(morse)
    print(f"电码: {morse}")
    print(f"原文: {text}")
    
    # 使用类
    decoder = MorseDecoder()
    morse_codes = [
        "... --- ...",           # SOS
        ".- -... -.-.",          # ABC
        ".---- ..--- ...--",     # 123
        ".... . .-.. .-.. --- / .-- --- .-. .-.. -..",  # HELLO WORLD
    ]
    for m in morse_codes:
        print(f"{m} -> {decoder.decode(m)}")


def example_round_trip():
    """编码解码往返示例"""
    print("\n" + "="*60)
    print("示例 3: 编码解码往返")
    print("="*60)
    
    utils = MorseUtils()
    
    messages = [
        "HELLO",
        "SOS",
        "MORSE CODE",
        "12345",
        "HELP ME",
    ]
    
    for msg in messages:
        morse = utils.encode(msg)
        decoded = utils.decode(morse)
        print(f"原文: {msg}")
        print(f"电码: {morse}")
        print(f"解码: {decoded}")
        print(f"一致: {msg.upper() == decoded}")
        print()


def example_custom_config():
    """自定义配置示例"""
    print("\n" + "="*60)
    print("示例 4: 自定义配置")
    print("="*60)
    
    # 自定义符号
    config1 = MorseConfig(dot_symbol='*', dash_symbol='_')
    encoder1 = MorseEncoder(config1)
    print("使用 * 和 _ 作为符号:")
    print(f"SOS -> {encoder1.encode('SOS')}")
    
    # 自定义分隔符
    config2 = MorseConfig(letter_separator=' | ', word_separator=' // ')
    encoder2 = MorseEncoder(config2)
    print("\n使用自定义分隔符:")
    print(f"HELLO WORLD -> {encoder2.encode('HELLO WORLD')}")
    
    # 自定义音频参数
    config3 = MorseConfig(
        frequency=500,        # 500 Hz
        dot_duration=0.08,    # 80ms 点
    )
    utils = MorseUtils(config3)
    duration = utils.calculate_duration('SOS')
    print(f"\n使用 500Hz/80ms 配置:")
    print(f"SOS 播放时长: {duration:.2f} 秒")


def example_audio_generation():
    """音频生成示例"""
    print("\n" + "="*60)
    print("示例 5: 音频生成")
    print("="*60)
    
    generator = MorseAudioGenerator()
    
    # 生成音频数据
    text = "SOS"
    audio_data = generator.generate_audio(text)
    print(f"为 '{text}' 生成的音频大小: {len(audio_data)} 字节")
    
    # 保存到临时文件
    import tempfile
    with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as f:
        filepath = f.name
    
    generator.save_audio(text, filepath)
    print(f"音频已保存到: {filepath}")
    
    # 检查文件
    file_size = os.path.getsize(filepath)
    print(f"文件大小: {file_size} 字节")
    
    # 清理
    os.unlink(filepath)
    print("临时文件已删除")


def example_statistics():
    """统计信息示例"""
    print("\n" + "="*60)
    print("示例 6: 统计信息")
    print("="*60)
    
    utils = MorseUtils()
    
    texts = ["SOS", "HELLO WORLD", "THE QUICK BROWN FOX"]
    
    for text in texts:
        stats = utils.get_statistics(text)
        print(f"\n文本: {text}")
        print(f"  电码: {stats['morse_code']}")
        print(f"  点数: {stats['dot_count']}")
        print(f"  划数: {stats['dash_count']}")
        print(f"  总符号: {stats['total_symbols']}")
        print(f"  时长: {stats['duration_seconds']:.3f} 秒")
        print(f"  字符数: {stats['character_count']}")
        print(f"  单词数: {stats['word_count']}")


def example_visualization():
    """可视化示例"""
    print("\n" + "="*60)
    print("示例 7: 可视化")
    print("="*60)
    
    utils = MorseUtils()
    
    text = "SOS"
    
    # 标准格式
    print(f"标准格式: {utils.visualize(text, 'standard')}")
    
    # 圆点格式
    print(f"圆点格式: {utils.visualize(text, 'dots')}")
    
    # 竖线格式
    print(f"竖线格式: {utils.visualize(text, 'bars')}")
    
    # 音效拟声
    print(f"音效拟声: {utils.visualize(text, 'sound')}")
    
    # 更多示例
    print("\n完整句子可视化:")
    sentence = "HELLO WORLD"
    print(f"音效: {utils.visualize(sentence, 'sound')}")


def example_morse_table():
    """摩尔斯电码表示例"""
    print("\n" + "="*60)
    print("示例 8: 摩尔斯电码表")
    print("="*60)
    
    table = get_morse_table()
    
    # 显示字母
    print("字母电码表:")
    for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        print(f"  {letter}: {table[letter]}")
    
    # 显示数字
    print("\n数字电码表:")
    for digit in "0123456789":
        print(f"  {digit}: {table[digit]}")
    
    # 显示部分标点
    print("\n常用标点:")
    for punc in ". , ? ! /":
        print(f"  {punc}: {table[punc]}")


def example_abbreviations():
    """常用缩写示例"""
    print("\n" + "="*60)
    print("示例 9: 常用缩写")
    print("="*60)
    
    abbreviations = get_abbreviations()
    
    print("无线电通讯常用缩写:")
    for name, morse in abbreviations.items():
        print(f"  {name}: {morse}")
    
    # 解码缩写
    decoder = MorseDecoder()
    print("\n解码 SOS:")
    print(f"  电码: {abbreviations['SOS']}")
    print(f"  解码: {decoder.decode(abbreviations['SOS'])}")


def example_practice():
    """练习功能示例"""
    print("\n" + "="*60)
    print("示例 10: 练习功能")
    print("="*60)
    
    utils = MorseUtils()
    
    # 指定字符练习
    practice = utils.practice('A')
    print(f"字符: {practice['character']}")
    print(f"电码: {practice['morse_code']}")
    print(f"描述: {practice['description']}")
    print(f"口诀: {practice['mnemonic']}")
    
    # 随机练习
    print("\n随机练习示例:")
    for i in range(5):
        p = utils.practice()
        print(f"  {p['character']}: {p['morse_code']}")


def example_duration_calculation():
    """持续时间计算示例"""
    print("\n" + "="*60)
    print("示例 11: 持续时间计算")
    print("="*60)
    
    utils = MorseUtils()
    
    # 不同文本的播放时长
    texts = ["E", "T", "SOS", "HELLO", "HELLO WORLD"]
    
    for text in texts:
        duration = utils.calculate_duration(text)
        morse = utils.encode(text)
        print(f"'{text}' ({morse}): {duration:.3f} 秒")
    
    # 使用更快的速度
    print("\n使用更快的速度 (40ms 点):")
    config = MorseConfig(dot_duration=0.04)
    fast_utils = MorseUtils(config)
    for text in texts:
        duration = fast_utils.calculate_duration(text)
        print(f"'{text}': {duration:.3f} 秒")


def example_full_workflow():
    """完整工作流示例"""
    print("\n" + "="*60)
    print("示例 12: 完整工作流")
    print("="*60)
    
    # 1. 创建工具实例
    utils = MorseUtils()
    
    # 2. 输入消息
    message = "HELP"
    print(f"原始消息: {message}")
    
    # 3. 编码
    morse = utils.encode(message)
    print(f"摩尔斯电码: {morse}")
    
    # 4. 获取统计
    stats = utils.get_statistics(message)
    print(f"播放时长: {stats['duration_seconds']:.2f} 秒")
    
    # 5. 可视化
    print(f"音效表示: {utils.visualize(message, 'sound')}")
    
    # 6. 生成音频 (演示，不保存文件)
    audio = utils.generate_audio(message)
    print(f"音频大小: {len(audio)} 字节")
    
    # 7. 解码验证
    decoded = utils.decode(morse)
    print(f"解码验证: {decoded}")
    
    # 8. 验证一致性
    if decoded == message.upper():
        print("✓ 编码解码一致")


def example_unknown_characters():
    """未知字符处理示例"""
    print("\n" + "="*60)
    print("示例 13: 未知字符处理")
    print("="*60)
    
    # 默认配置 - 替换未知字符
    encoder = MorseEncoder()
    text = "HELLO世界"
    print(f"原文: {text}")
    print(f"默认处理: {encoder.encode(text)}")
    
    # 忽略未知字符
    config = MorseConfig(ignore_unknown=True)
    encoder2 = MorseEncoder(config)
    print(f"忽略处理: {encoder2.encode(text)}")


def example_validation():
    """验证功能示例"""
    print("\n" + "="*60)
    print("示例 14: 电码验证")
    print("="*60)
    
    decoder = MorseDecoder()
    
    valid_codes = ["... --- ...", ".- -... -.-.", ".----"]
    invalid_codes = ["abc", "...xyz...", "123"]
    
    print("有效电码:")
    for code in valid_codes:
        print(f"  '{code}': {decoder.is_valid_morse(code)}")
    
    print("\n无效电码:")
    for code in invalid_codes:
        print(f"  '{code}': {decoder.is_valid_morse(code)}")


def example_punctuation():
    """标点符号示例"""
    print("\n" + "="*60)
    print("示例 15: 标点符号")
    print("="*60)
    
    encoder = MorseEncoder()
    decoder = MorseDecoder()
    
    # 常用标点
    punctuations = [
        ("句号", "."),
        ("逗号", ","),
        ("问号", "?"),
        ("感叹号", "!"),
        ("斜杠", "/"),
        ("冒号", ":"),
        ("等号", "="),
        ("加号", "+"),
        ("减号", "-"),
    ]
    
    for name, char in punctuations:
        morse = encoder.encode(char)
        decoded = decoder.decode(morse)
        print(f"{name} ({char}): {morse} -> {decoded}")


def run_all_examples():
    """运行所有示例"""
    print("\n" + "="*60)
    print("摩尔斯电码工具使用示例")
    print("="*60)
    
    example_basic_encoding()
    example_basic_decoding()
    example_round_trip()
    example_custom_config()
    example_audio_generation()
    example_statistics()
    example_visualization()
    example_morse_table()
    example_abbreviations()
    example_practice()
    example_duration_calculation()
    example_full_workflow()
    example_unknown_characters()
    example_validation()
    example_punctuation()
    
    print("\n" + "="*60)
    print("所有示例运行完成!")
    print("="*60)


if __name__ == '__main__':
    run_all_examples()