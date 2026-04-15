"""
Morse Utils - 使用示例

展示摩尔斯电码工具的各种用法：
1. 基本编码解码
2. 音频生成
3. 练习模式
4. 文件操作
5. 高级功能
"""

import sys
import os

# 添加模块路径（直接导入 mod）
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    encode,
    decode,
    MorseConfig,
    MorseCode,
    generate_morse_audio,
    calculate_duration,
    get_morse_stats,
    get_supported_characters,
    get_morse_for_char,
    get_char_for_morse,
    is_valid_morse,
    is_valid_text_for_encoding,
    translate_abbreviation,
    translate_q_code,
    list_abbreviations,
    list_q_codes,
    practice_mode,
    reverse_encode,
    compare_morse,
    text_to_morse,
    morse_to_text,
    text_to_audio,
)


def print_section(title):
    """打印章节标题"""
    print("\n" + "=" * 50)
    print(f"  {title}")
    print("=" * 50)


def example_basic_encoding():
    """基本编码示例"""
    print_section("1. 基本编码")
    
    # 编码单个字符
    print("\n编码单个字符:")
    print(f"  A -> {encode('A')}")
    print(f"  B -> {encode('B')}")
    print(f"  E -> {encode('E')}")
    print(f"  T -> {encode('T')}")
    
    # 编码单词
    print("\n编码单词:")
    print(f"  HELLO -> {encode('HELLO')}")
    print(f"  WORLD -> {encode('WORLD')}")
    print(f"  SOS -> {encode('SOS')}")
    
    # 编码句子
    print("\n编码句子:")
    print(f"  'HELLO WORLD' -> {encode('HELLO WORLD')}")
    print(f"  'I LOVE YOU' -> {encode('I LOVE YOU')}")
    
    # 编码数字和符号
    print("\n编码数字和符号:")
    print(f"  123 -> {encode('123')}")
    print(f"  S.O.S -> {encode('S.O.S')}")
    print(f"  TEST@EMAIL.COM -> {encode('TEST@EMAIL.COM')}")


def example_basic_decoding():
    """基本解码示例"""
    print_section("2. 基本解码")
    
    # 解码单个字符
    print("\n解码单个字符:")
    print(f"  .- -> {decode('.-')}")
    print(f"  -... -> {decode('-...')}")
    print(f"  . -> {decode('.')}")
    print(f"  - -> {decode('-')}")
    
    # 解码单词
    print("\n解码单词:")
    print(f"  '.... . .-.. .-.. ---' -> {decode('.... . .-.. .-.. ---')}")
    print(f"  '... --- ...' -> {decode('... --- ...')}")
    
    # 解码句子
    print("\n解码句子:")
    morse = '.... . .-.. .-.. --- / .-- --- .-. .-.. -..'
    print(f"  '{morse}' -> {decode(morse)}")


def example_custom_separator():
    """自定义分隔符示例"""
    print_section("3. 自定义分隔符")
    
    # 默认分隔符
    text = "HELLO WORLD"
    print(f"\n文本: {text}")
    print(f"默认分隔符: {encode(text)}")
    
    # 自定义字母分隔符
    print(f"字母分隔符 '/': {encode(text, letter_separator='/')}")
    
    # 自定义单词分隔符
    print(f"单词分隔符 ' | ': {encode(text, word_separator=' | ')}")
    
    # 解码时使用相同分隔符
    # 先用自定义分隔符编码，再解码
    morse_custom = encode("HI", letter_separator='|')
    print(f"\n用 '|' 作为字母分隔符编码 'HI': {morse_custom}")
    decoded = decode(morse_custom, letter_separator='|')
    print(f"解码结果: {decoded}")


def example_audio_generation():
    """音频生成示例"""
    print_section("4. 音频生成")
    
    # 默认配置
    print("\n默认配置:")
    print(f"  点时长: 0.1 秒")
    print(f"  划时长: 0.3 秒 (点的 3 倍)")
    print(f"  频率: 600 Hz")
    
    # 生成音频
    text = "SOS"
    audio = generate_morse_audio(text)
    print(f"\n生成 '{text}' 的音频:")
    print(f"  音频大小: {len(audio)} 字节")
    print(f"  WAV 格式: RIFF 头 = {audio[:4]}")
    
    # 计算播放时长
    morse = encode(text)
    duration = calculate_duration(morse)
    print(f"  预计时长: {duration:.2f} 秒")
    
    # 自定义配置
    print("\n自定义配置:")
    config = MorseConfig(
        dot_duration=0.08,    # 更快的点
        frequency=800,        # 更高的频率
    )
    mc = MorseCode(config)
    audio = mc.to_audio("HELLO")
    duration = mc.duration(encode("HELLO"))
    print(f"  频率: {config.frequency} Hz")
    print(f"  点时长: {config.dot_duration} 秒")
    print(f"  'HELLO' 预计时长: {duration:.2f} 秒")


def example_statistics():
    """统计功能示例"""
    print_section("5. 统计功能")
    
    morse = encode("HELLO WORLD")
    stats = get_morse_stats(morse)
    
    print(f"\n摩尔斯码: {morse}")
    print(f"统计信息:")
    print(f"  点数: {stats['dots']}")
    print(f"  划数: {stats['dashes']}")
    print(f"  字母数: {stats['letters']}")
    print(f"  单词数: {stats['words']}")
    print(f"  总符号数: {stats['total_symbols']}")
    
    # 反转摩尔斯码
    print(f"\n反转摩尔斯码:")
    original = "..."
    reversed_morse = reverse_encode(original)
    print(f"  原始: {original}")
    print(f"  反转: {reversed_morse}")


def example_validation():
    """验证功能示例"""
    print_section("6. 验证功能")
    
    # 验证摩尔斯码
    print("\n验证摩尔斯码:")
    valid_morse = "... --- ..."
    invalid_morse = "... abc ..."
    print(f"  '{valid_morse}' 有效: {is_valid_morse(valid_morse)}")
    print(f"  '{invalid_morse}' 有效: {is_valid_morse(invalid_morse)}")
    
    # 验证文本
    print("\n验证文本编码:")
    valid, invalid = is_valid_text_for_encoding("HELLO")
    print(f"  'HELLO' 可编码: {valid}, 无效字符: {invalid}")
    
    valid, invalid = is_valid_text_for_encoding("你好")
    print(f"  '你好' 可编码: {valid}, 无效字符: {invalid}")


def example_abbreviations():
    """缩写和 Q 代码示例"""
    print_section("7. 缩写和 Q 代码")
    
    # 常见缩写
    print("\n常见摩尔斯缩写:")
    abbreviations = ['SOS', 'CQ', 'K', 'SK']
    for abbr in abbreviations:
        morse = translate_abbreviation(abbr)
        print(f"  {abbr}: {morse}")
    
    # Q 代码
    print("\n常用 Q 代码:")
    q_codes = ['QTH', 'QRZ', 'QRM', 'QRN', 'QSL']
    for code in q_codes:
        meaning = translate_q_code(code)
        print(f"  {code}: {meaning}")


def example_practice_mode():
    """练习模式示例"""
    print_section("8. 练习模式")
    
    # 编码练习
    print("\n编码练习:")
    practice = practice_mode(text='HELLO', show_answer=False)
    print(f"  类型: {practice['type']}")
    print(f"  文本: {practice['text']}")
    print(f"  提示: {practice['hint']}")
    print(f"  (隐藏答案)")
    
    practice = practice_mode(text='HELLO', show_answer=True)
    print(f"\n  显示答案:")
    print(f"  摩尔斯码: {practice['morse']}")
    
    # 解码练习
    print("\n解码练习:")
    practice = practice_mode(morse='... --- ...', show_answer=False)
    print(f"  类型: {practice['type']}")
    print(f"  摩尔斯码: {practice['morse']}")
    print(f"  提示: {practice['hint']}")
    print(f"  (隐藏答案)")
    
    practice = practice_mode(morse='... --- ...', show_answer=True)
    print(f"\n  显示答案:")
    print(f"  文本: {practice['text']}")


def example_class_api():
    """面向对象 API 示例"""
    print_section("9. 面向对象 API")
    
    # 创建 MorseCode 对象
    mc = MorseCode()
    print(f"\n创建 MorseCode 对象: {mc}")
    
    # 编码
    text = "HELLO"
    morse = mc.encode(text)
    print(f"\n编码 '{text}': {morse}")
    
    # 解码
    decoded = mc.decode(morse)
    print(f"解码 '{morse}': {decoded}")
    
    # 计算时长
    duration = mc.duration(morse)
    print(f"播放时长: {duration:.2f} 秒")
    
    # 生成音频
    audio = mc.to_audio(text)
    print(f"音频大小: {len(audio)} 字节")
    
    # 自定义配置
    config = MorseConfig(
        dot_duration=0.05,
        frequency=700
    )
    mc_fast = MorseCode(config)
    print(f"\n快速配置: {mc_fast}")
    duration_fast = mc_fast.duration(morse)
    print(f"快速播放时长: {duration_fast:.2f} 秒")


def example_convenience_functions():
    """便捷函数示例"""
    print_section("10. 便捷函数")
    
    # text_to_morse
    text = "SOS"
    morse = text_to_morse(text)
    print(f"\ntext_to_morse('{text}'): {morse}")
    
    # morse_to_text
    decoded = morse_to_text(morse)
    print(f"morse_to_text('{morse}'): {decoded}")
    
    # text_to_audio
    audio = text_to_audio("SOS")
    print(f"text_to_audio('SOS'): {len(audio)} 字节")


def example_character_lookup():
    """字符查询示例"""
    print_section("11. 字符查询")
    
    # 获取支持的字符
    chars = get_supported_characters()
    print(f"\n支持的字符数: {len(chars)}")
    print(f"字母: {[c for c in chars if c.isalpha() and len(c) == 1][:10]}...")
    print(f"数字: {[c for c in chars if c.isdigit()]}")
    
    # 查询字符对应的摩尔斯码
    print("\n字符摩尔斯码查询:")
    for char in ['A', 'B', 'S', 'O', '1', '0']:
        morse = get_morse_for_char(char)
        print(f"  {char} -> {morse}")
    
    # 查询摩尔斯码对应的字符
    print("\n摩尔斯码字符查询:")
    for morse in ['.-', '-...', '...', '---']:
        char = get_char_for_morse(morse)
        print(f"  {morse} -> {char}")


def example_compare():
    """比较功能示例"""
    print_section("12. 比较功能")
    
    # 比较相同的摩尔斯码
    morse1 = "... --- ..."
    morse2 = "... --- ..."
    equal, diff = compare_morse(morse1, morse2)
    print(f"\n比较 '{morse1}' 和 '{morse2}':")
    print(f"  相等: {equal}")
    print(f"  匹配: {diff['matches']}, 不匹配: {diff['mismatches']}")
    
    # 比较不同的摩尔斯码
    morse1 = "... --- ..."
    morse2 = "... ... ..."
    equal, diff = compare_morse(morse1, morse2)
    print(f"\n比较 '{morse1}' 和 '{morse2}':")
    print(f"  相等: {equal}")
    print(f"  匹配: {diff['matches']}, 不匹配: {diff['mismatches']}")


def example_complete():
    """完整示例"""
    print_section("13. 完整示例")
    
    # 模拟电报发送
    message = "HELLO WORLD"
    
    print(f"\n发送消息: '{message}'")
    
    # 1. 编码
    morse = encode(message)
    print(f"\n1. 编码为摩尔斯电码:")
    print(f"   {morse}")
    
    # 2. 统计
    stats = get_morse_stats(morse)
    print(f"\n2. 统计信息:")
    print(f"   点: {stats['dots']}, 划: {stats['dashes']}")
    print(f"   字母: {stats['letters']}, 单词: {stats['words']}")
    
    # 3. 计算时长
    duration = calculate_duration(morse)
    print(f"\n3. 播放时长: {duration:.2f} 秒")
    
    # 4. 生成音频
    audio = generate_morse_audio(message)
    print(f"\n4. 生成音频: {len(audio)} 字节")
    
    # 5. 解码
    decoded = decode(morse)
    print(f"\n5. 解码还原: '{decoded}'")
    
    print(f"\n✅ 消息发送完成!")


def main():
    """运行所有示例"""
    print("\n" + "=" * 60)
    print("  Morse Utils 使用示例")
    print("=" * 60)
    
    example_basic_encoding()
    example_basic_decoding()
    example_custom_separator()
    example_audio_generation()
    example_statistics()
    example_validation()
    example_abbreviations()
    example_practice_mode()
    example_class_api()
    example_convenience_functions()
    example_character_lookup()
    example_compare()
    example_complete()
    
    print("\n" + "=" * 60)
    print("  示例演示完成!")
    print("=" * 60 + "\n")


if __name__ == '__main__':
    main()