"""
Morse Utils - 摩尔斯电码工具

零依赖的摩尔斯电码库，支持：
- 文本转摩尔斯电码编码
- 摩尔斯电码转文本解码
- 音频信号生成（正弦波）
- 支持多语言字符（A-Z、数字、常见符号）
- 自定义分隔符和时间参数
- 摩尔斯电码验证
- 常见缩写和Q代码支持

Author: AllToolkit
License: MIT
"""

from typing import Union, List, Tuple, Optional, Dict
import math
import struct


# 国际摩尔斯电码表
MORSE_CODE = {
    # 字母
    'A': '.-',
    'B': '-...',
    'C': '-.-.',
    'D': '-..',
    'E': '.',
    'F': '..-.',
    'G': '--.',
    'H': '....',
    'I': '..',
    'J': '.---',
    'K': '-.-',
    'L': '.-..',
    'M': '--',
    'N': '-.',
    'O': '---',
    'P': '.--.',
    'Q': '--.-',
    'R': '.-.',
    'S': '...',
    'T': '-',
    'U': '..-',
    'V': '...-',
    'W': '.--',
    'X': '-..-',
    'Y': '-.--',
    'Z': '--..',
    # 数字
    '0': '-----',
    '1': '.----',
    '2': '..---',
    '3': '...--',
    '4': '....-',
    '5': '.....',
    '6': '-....',
    '7': '--...',
    '8': '---..',
    '9': '----.',
    # 标点符号
    '.': '.-.-.-',
    ',': '--..--',
    '?': '..--..',
    "'": '.----.',
    '!': '-.-.--',
    '/': '-..-.',
    '(': '-.--.',
    ')': '-.--.-',
    '&': '.-...',
    ':': '---...',
    ';': '-.-.-.',
    '=': '-...-',
    '+': '.-.-.',
    '-': '-....-',
    '_': '..--.-',
    '"': '.-..-.',
    '$': '...-..-',
    '@': '.--.-.',
    # 非英语字符
    'À': '.--.-',
    'Å': '.--.-',
    'Ä': '.-.-',
    'Æ': '.-.-',
    'É': '..-..',
    'Ñ': '--.--',
    'Ö': '---.',
    'Ø': '---.',
    'Ü': '..--',
    'Ş': '...-.',  # S with cedilla
    'Ğ': '--.-.',  # G with breve
    'Ç': '-.-..',  # C with cedilla
}

# 反向映射表（摩尔斯电码转字符）
MORSE_DECODE = {v: k for k, v in MORSE_CODE.items()}

# 常见摩尔斯缩写
MORSE_ABBREVIATIONS = {
    'SOS': '...---...',  # 求救信号
    'CQ': '-.-.--.-',    # 呼叫所有电台
    'K': '-.-',          # 邀请发送
    'KN': '-.---',       # 邀请特定电台发送
    'SK': '...-.-',      # 结束通信
    'BK': '-...-.-',     # 打断
    'AR': '.-.-.',       # 消息结束
    'BT': '-...-',       # 分隔符
    'AA': '.-.-',        # 行结束
    'AS': '.-...',       # 等待
    'CL': '-.-..-..',    # 关闭
    'GA': '--.-.',       # 开始
    'HI': '......',      # 笑声
    'HM': '....--',      # 思考
    'NR': '-.-..-.',     # 编号
    'NW': '-.---',       # 现在
    'OK': '---.-',       # 好的
    'OM': '---..',       # 老朋友
    'R': '.-.',          # 收到
    'SN': '...-.',       # 明白
    'TU': '-..-',        # 谢谢
    'UR': '..-.',        # 你的
    'WX': '.--..-',      # 天气
}

# Q代码（常用）
Q_CODE = {
    'QTH': 'What is your position?',      # 询问位置
    'QRL': 'Is this frequency busy?',     # 询问频率
    'QRZ': 'Who is calling me?',           # 谁在呼叫
    'QRM': 'Are you being interfered?',   # 干扰
    'QRN': 'Are you receiving static?',   # 静电噪声
    'QRO': 'Shall I increase power?',     # 增加功率
    'QRP': 'Shall I decrease power?',     # 减少功率
    'QRQ': 'Shall I send faster?',        # 发送更快
    'QRS': 'Shall I send slower?',         # 发送更慢
    'QRT': 'Shall I stop sending?',       # 停止发送
    'QRU': 'Have you anything for me?',   # 有什么给我吗
    'QRV': 'Are you ready?',              # 准备好了吗
    'QRX': 'When will you call again?',   # 何时再呼叫
    'QSA': 'What is my signal strength?', # 信号强度
    'QSB': 'Is my signal fading?',        # 信号衰落
    'QSL': 'Can you acknowledge?',        # 确认收到
    'QSO': 'Can you communicate with...?', # 通信
    'QSY': 'Shall I change frequency?',   # 更换频率
}


class MorseError(Exception):
    """摩尔斯电码错误基类"""
    pass


class InvalidCharacterError(MorseError):
    """无效字符错误"""
    pass


class InvalidMorseError(MorseError):
    """无效摩尔斯电码错误"""
    pass


class MorseConfig:
    """摩尔斯电码配置"""
    
    def __init__(
        self,
        dot_duration: float = 0.1,      # 点持续时间（秒）
        dash_duration: float = None,    # 划持续时间（默认为点的3倍）
        symbol_gap: float = None,        # 符号间间隔（默认为点的1倍）
        letter_gap: float = None,        # 字母间间隔（默认为点的3倍）
        word_gap: float = None,          # 单词间间隔（默认为点的7倍）
        sample_rate: int = 44100,        # 音频采样率
        frequency: float = 600.0,        # 音频频率（Hz）
    ):
        self.dot_duration = dot_duration
        self.dash_duration = dash_duration if dash_duration else dot_duration * 3
        self.symbol_gap = symbol_gap if symbol_gap else dot_duration
        self.letter_gap = letter_gap if letter_gap else dot_duration * 3
        self.word_gap = word_gap if word_gap else dot_duration * 7
        self.sample_rate = sample_rate
        self.frequency = frequency
    
    @property
    def unit(self) -> float:
        """获取基本时间单位"""
        return self.dot_duration


# 默认配置
DEFAULT_CONFIG = MorseConfig()


def encode(
    text: str,
    letter_separator: str = ' ',
    word_separator: str = ' / ',
    config: MorseConfig = None,
    ignore_unknown: bool = False
) -> str:
    """
    将文本编码为摩尔斯电码
    
    Args:
        text: 要编码的文本
        letter_separator: 字母分隔符
        word_separator: 单词分隔符
        config: 配置对象（未使用，保留用于扩展）
        ignore_unknown: 是否忽略未知字符
    
    Returns:
        摩尔斯电码字符串
    
    Raises:
        InvalidCharacterError: 包含无法编码的字符
    
    Example:
        >>> encode('HELLO')
        '.... . .-.. .-.. ---'
        >>> encode('SOS')
        '... --- ...'
    """
    if not text:
        return ''
    
    text = text.upper()
    words = text.split()
    encoded_words = []
    
    for word in words:
        encoded_letters = []
        for char in word:
            if char in MORSE_CODE:
                encoded_letters.append(MORSE_CODE[char])
            elif ignore_unknown:
                continue
            else:
                raise InvalidCharacterError(f"无法编码字符: {char!r}")
        
        if encoded_letters:
            encoded_words.append(letter_separator.join(encoded_letters))
    
    return word_separator.join(encoded_words)


def decode(
    morse: str,
    letter_separator: str = ' ',
    word_separator: str = '/',
    config: MorseConfig = None,
    ignore_unknown: bool = False
) -> str:
    """
    将摩尔斯电码解码为文本
    
    Args:
        morse: 摩尔斯电码字符串
        letter_separator: 字母分隔符
        word_separator: 单词分隔符
        config: 配置对象（未使用，保留用于扩展）
        ignore_unknown: 是否忽略未知的摩尔斯码
    
    Returns:
        解码后的文本
    
    Raises:
        InvalidMorseError: 包含无效的摩尔斯电码
    
    Example:
        >>> decode('.... . .-.. .-.. ---')
        'HELLO'
        >>> decode('... --- ...')
        'SOS'
    """
    if not morse:
        return ''
    
    # 标准化分隔符
    morse = morse.strip()
    
    # 按单词分隔
    words = morse.split(word_separator)
    decoded_words = []
    
    for word in words:
        word = word.strip()
        if not word:
            decoded_words.append('')
            continue
        
        # 按字母分隔
        letters = word.split(letter_separator)
        decoded_letters = []
        
        for letter in letters:
            letter = letter.strip()
            if not letter:
                continue
            
            # 标准化摩尔斯码（移除多余空格）
            letter = ''.join(c for c in letter if c in '.-')
            
            if letter in MORSE_DECODE:
                decoded_letters.append(MORSE_DECODE[letter])
            elif ignore_unknown:
                decoded_letters.append('?')
            else:
                raise InvalidMorseError(f"无法解码摩尔斯码: {letter!r}")
        
        decoded_words.append(''.join(decoded_letters))
    
    return ' '.join(decoded_words)


def encode_file(
    input_path: str,
    output_path: str,
    letter_separator: str = ' ',
    word_separator: str = ' / ',
    ignore_unknown: bool = False
) -> int:
    """
    编码文件内容
    
    Args:
        input_path: 输入文件路径
        output_path: 输出文件路径
        letter_separator: 字母分隔符
        word_separator: 单词分隔符
        ignore_unknown: 是否忽略未知字符
    
    Returns:
        编码的字符数
    """
    with open(input_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    encoded = encode(content, letter_separator, word_separator, None, ignore_unknown)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(encoded)
    
    return len(content)


def decode_file(
    input_path: str,
    output_path: str,
    letter_separator: str = ' ',
    word_separator: str = '/',
    ignore_unknown: bool = False
) -> int:
    """
    解码文件内容
    
    Args:
        input_path: 输入文件路径
        output_path: 输出文件路径
        letter_separator: 字母分隔符
        word_separator: 单词分隔符
        ignore_unknown: 是否忽略未知摩尔斯码
    
    Returns:
        解码的摩尔斯码元素数
    """
    with open(input_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    decoded = decode(content, letter_separator, word_separator, None, ignore_unknown)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(decoded)
    
    return len(content.split())


def is_valid_morse(morse: str) -> bool:
    """
    检查字符串是否为有效的摩尔斯电码
    
    Args:
        morse: 要检查的字符串
    
    Returns:
        是否为有效的摩尔斯电码
    
    Example:
        >>> is_valid_morse('... --- ...')
        True
        >>> is_valid_morse('abc')
        False
    """
    if not morse:
        return True
    
    # 只能包含点、划和分隔符
    valid_chars = set('.- /')
    return all(c in valid_chars for c in morse)


def is_valid_text_for_encoding(text: str) -> Tuple[bool, List[str]]:
    """
    检查文本是否可以完全编码
    
    Args:
        text: 要检查的文本
    
    Returns:
        (是否可编码, 无法编码的字符列表)
    
    Example:
        >>> is_valid_text_for_encoding('HELLO')
        (True, [])
        >>> is_valid_text_for_encoding('你好')
        (False, ['你', '好'])
    """
    if not text:
        return True, []
    
    invalid = []
    for char in text.upper():
        if char != ' ' and char not in MORSE_CODE:
            invalid.append(char)
    
    return len(invalid) == 0, invalid


def get_supported_characters() -> List[str]:
    """
    获取所有支持的字符
    
    Returns:
        支持的字符列表
    """
    return sorted(MORSE_CODE.keys())


def get_morse_for_char(char: str) -> Optional[str]:
    """
    获取字符对应的摩尔斯电码
    
    Args:
        char: 字符
    
    Returns:
        摩尔斯电码，如果字符不支持则返回None
    
    Example:
        >>> get_morse_for_char('A')
        '.-'
        >>> get_morse_for_char('你')
        None
    """
    return MORSE_CODE.get(char.upper())


def get_char_for_morse(morse: str) -> Optional[str]:
    """
    获取摩尔斯电码对应的字符
    
    Args:
        morse: 摩尔斯电码
    
    Returns:
        字符，如果摩尔斯码无效则返回None
    
    Example:
        >>> get_char_for_morse('.-')
        'A'
        >>> get_char_for_morse('...')
        'S'
    """
    return MORSE_DECODE.get(morse)


def normalize_morse(morse: str) -> str:
    """
    标准化摩尔斯电码字符串
    
    将各种划表示统一，移除空格和无效字符，只保留点和划
    
    Args:
        morse: 摩尔斯电码字符串
    
    Returns:
        标准化后的摩尔斯电码（只包含点和划）
    
    Example:
        >>> normalize_morse('. - .')
        '.-.'
        >>> normalize_morse('.—.')
        '..-.'
    """
    # 将各种划表示统一
    result = morse.replace('—', '-').replace('–', '-')
    # 移除空格和无效字符，只保留点和划
    result = ''.join(c for c in result if c in '.-')
    return result


def calculate_duration(
    morse: str,
    config: MorseConfig = None
) -> float:
    """
    计算摩尔斯电码播放时长（秒）
    
    Args:
        morse: 摩尔斯电码
        config: 配置对象
    
    Returns:
        预计播放时长（秒）
    
    Example:
        >>> calculate_duration('... --- ...', MorseConfig(dot_duration=0.1))
        2.2
    """
    if config is None:
        config = DEFAULT_CONFIG
    
    duration = 0.0
    
    for i, char in enumerate(morse):
        if char == '.':
            duration += config.dot_duration + config.symbol_gap
        elif char == '-':
            duration += config.dash_duration + config.symbol_gap
        elif char == ' ':
            # 空格表示字母间隔
            duration += config.letter_gap - config.symbol_gap
        elif char == '/':
            # 斜杠表示单词间隔
            duration += config.word_gap - config.letter_gap
    
    return duration


def generate_tone(
    frequency: float,
    duration: float,
    sample_rate: int = 44100,
    amplitude: float = 0.5
) -> bytes:
    """
    生成正弦波音频数据
    
    Args:
        frequency: 频率（Hz）
        duration: 持续时间（秒）
        sample_rate: 采样率
        amplitude: 振幅（0.0-1.0）
    
    Returns:
        WAV格式的音频数据（bytes）
    
    Example:
        >>> data = generate_tone(600, 0.1)
        >>> len(data) > 0
        True
    """
    num_samples = int(sample_rate * duration)
    
    # 生成正弦波
    samples = []
    for i in range(num_samples):
        t = i / sample_rate
        value = amplitude * math.sin(2 * math.pi * frequency * t)
        # 转换为16位PCM
        sample = int(value * 32767)
        samples.append(sample)
    
    # 创建WAV文件头
    wav_data = struct.pack('<' + 'h' * len(samples), *samples)
    
    # WAV文件头
    header = struct.pack(
        '<4sI4s4sIHHIIHH4sI',
        b'RIFF',
        36 + len(wav_data),  # 文件大小 - 8
        b'WAVE',
        b'fmt ',
        16,          # fmt块大小
        1,           # PCM格式
        1,           # 单声道
        sample_rate, # 采样率
        sample_rate * 2,  # 字节率
        2,           # 块对齐
        16,          # 位深度
        b'data',
        len(wav_data)
    )
    
    return header + wav_data


def generate_silence(
    duration: float,
    sample_rate: int = 44100
) -> bytes:
    """
    生成静音数据
    
    Args:
        duration: 持续时间（秒）
        sample_rate: 采样率
    
    Returns:
        WAV格式的静音数据（bytes）
    """
    num_samples = int(sample_rate * duration)
    samples = [0] * num_samples
    
    wav_data = struct.pack('<' + 'h' * len(samples), *samples)
    
    header = struct.pack(
        '<4sI4s4sIHHIIHH4sI',
        b'RIFF',
        36 + len(wav_data),
        b'WAVE',
        b'fmt ',
        16,
        1,
        1,
        sample_rate,
        sample_rate * 2,
        2,
        16,
        b'data',
        len(wav_data)
    )
    
    return header + wav_data


def generate_morse_audio(
    text: str,
    config: MorseConfig = None,
    output_path: str = None,
    ignore_unknown: bool = False
) -> bytes:
    """
    将文本转换为摩尔斯电码音频
    
    Args:
        text: 要转换的文本
        config: 配置对象
        output_path: 输出文件路径（可选）
        ignore_unknown: 是否忽略未知字符
    
    Returns:
        WAV格式的音频数据
    
    Example:
        >>> audio = generate_morse_audio('SOS')
        >>> len(audio) > 0
        True
    """
    if config is None:
        config = DEFAULT_CONFIG
    
    # 编码为摩尔斯电码
    morse = encode(text, ' ', '/', config, ignore_unknown)
    
    audio_parts = []
    
    for char in morse:
        if char == '.':
            # 点
            tone = generate_tone(
                config.frequency,
                config.dot_duration,
                config.sample_rate
            )
            audio_parts.append(tone)
            # 符号间间隔
            silence = generate_silence(config.symbol_gap, config.sample_rate)
            audio_parts.append(silence)
        
        elif char == '-':
            # 划
            tone = generate_tone(
                config.frequency,
                config.dash_duration,
                config.sample_rate
            )
            audio_parts.append(tone)
            # 符号间间隔
            silence = generate_silence(config.symbol_gap, config.sample_rate)
            audio_parts.append(silence)
        
        elif char == ' ':
            # 字母间隔（减去已有的符号间隔）
            silence = generate_silence(
                config.letter_gap - config.symbol_gap,
                config.sample_rate
            )
            audio_parts.append(silence)
        
        elif char == '/':
            # 单词间隔（减去已有的字母间隔）
            silence = generate_silence(
                config.word_gap - config.letter_gap,
                config.sample_rate
            )
            audio_parts.append(silence)
    
    # 合并音频数据
    # 注意：由于每个部分都是完整的WAV文件，我们需要合并原始PCM数据
    raw_audio = b''
    for part in audio_parts:
        # 跳过WAV头（44字节），只取PCM数据
        if len(part) > 44:
            raw_audio += part[44:]
    
    # 创建最终的WAV文件
    header = struct.pack(
        '<4sI4s4sIHHIIHH4sI',
        b'RIFF',
        36 + len(raw_audio),
        b'WAVE',
        b'fmt ',
        16,
        1,
        1,
        config.sample_rate,
        config.sample_rate * 2,
        2,
        16,
        b'data',
        len(raw_audio)
    )
    
    audio_data = header + raw_audio
    
    # 如果指定了输出路径，保存文件
    if output_path:
        with open(output_path, 'wb') as f:
            f.write(audio_data)
    
    return audio_data


def translate_abbreviation(abbr: str) -> Optional[str]:
    """
    获取摩尔斯缩写的含义
    
    Args:
        abbr: 缩写
    
    Returns:
        含义，如果不存在则返回None
    
    Example:
        >>> translate_abbreviation('SOS')
        '...---...'
    """
    return MORSE_ABBREVIATIONS.get(abbr.upper())


def translate_q_code(code: str) -> Optional[str]:
    """
    获取Q代码的含义
    
    Args:
        code: Q代码
    
    Returns:
        含义，如果不存在则返回None
    
    Example:
        >>> translate_q_code('QTH')
        'What is your position?'
    """
    return Q_CODE.get(code.upper())


def list_abbreviations() -> Dict[str, str]:
    """
    获取所有摩尔斯缩写
    
    Returns:
        缩写字典
    """
    return dict(MORSE_ABBREVIATIONS)


def list_q_codes() -> Dict[str, str]:
    """
    获取所有Q代码
    
    Returns:
        Q代码字典
    """
    return dict(Q_CODE)


def get_morse_stats(morse: str) -> Dict[str, int]:
    """
    获取摩尔斯电码统计信息
    
    Args:
        morse: 摩尔斯电码字符串
    
    Returns:
        统计信息字典
    
    Example:
        >>> get_morse_stats('... --- ...')
        {'dots': 6, 'dashes': 3, 'letters': 3, 'words': 1}
    """
    dots = morse.count('.')
    dashes = morse.count('-')
    
    # 计算字母数（非空摩尔斯码元素）
    letters = len([m for m in morse.split() if m.strip('/')])
    
    # 计算单词数
    words = morse.count('/') + 1 if morse.strip() else 0
    
    return {
        'dots': dots,
        'dashes': dashes,
        'letters': letters,
        'words': words,
        'total_symbols': dots + dashes,
    }


def reverse_encode(morse: str) -> str:
    """
    反转摩尔斯电码（点变划，划变点）
    
    Args:
        morse: 摩尔斯电码
    
    Returns:
        反转后的摩尔斯电码
    
    Example:
        >>> reverse_encode('...')
        '---'
        >>> reverse_encode('.-')
        '-.'
    """
    return morse.replace('.', 'X').replace('-', '.').replace('X', '-')


def compare_morse(morse1: str, morse2: str) -> Tuple[bool, Dict[str, int]]:
    """
    比较两个摩尔斯电码
    
    Args:
        morse1: 第一个摩尔斯电码
        morse2: 第二个摩尔斯电码
    
    Returns:
        (是否相等, 差异统计)
    
    Example:
        >>> compare_morse('...', '...')
        (True, {'matches': 3, 'mismatches': 0})
    """
    # 标准化
    m1 = normalize_morse(morse1).replace(' ', '').replace('/', '')
    m2 = normalize_morse(morse2).replace(' ', '').replace('/', '')
    
    matches = 0
    mismatches = 0
    
    max_len = max(len(m1), len(m2))
    
    for i in range(max_len):
        c1 = m1[i] if i < len(m1) else None
        c2 = m2[i] if i < len(m2) else None
        
        if c1 == c2 and c1 is not None:
            matches += 1
        else:
            mismatches += 1
    
    return matches > 0 and mismatches == 0, {
        'matches': matches,
        'mismatches': mismatches,
    }


def practice_mode(
    text: str = None,
    morse: str = None,
    show_answer: bool = True
) -> Dict[str, str]:
    """
    摩尔斯电码练习模式
    
    Args:
        text: 文本（用于编码练习）
        morse: 摩尔斯电码（用于解码练习）
        show_answer: 是否显示答案
    
    Returns:
        练习数据字典
    
    Example:
        >>> practice_mode(text='HELLO')
        {'text': 'HELLO', 'morse': '.... . .-.. .-.. ---', 'type': 'encode'}
    """
    if text and not morse:
        # 编码练习
        encoded = encode(text)
        return {
            'type': 'encode',
            'text': text,
            'morse': encoded if show_answer else None,
            'hint': '将文本编码为摩尔斯电码',
        }
    elif morse and not text:
        # 解码练习
        decoded = decode(morse)
        return {
            'type': 'decode',
            'morse': morse,
            'text': decoded if show_answer else None,
            'hint': '将摩尔斯电码解码为文本',
        }
    else:
        return {
            'type': 'unknown',
            'error': '请提供text或morse参数（二选一）',
        }


class MorseCode:
    """
    摩尔斯电码类，提供面向对象的API
    """
    
    def __init__(self, config: MorseConfig = None):
        """
        初始化摩尔斯电码对象
        
        Args:
            config: 配置对象
        """
        self.config = config or DEFAULT_CONFIG
    
    def encode(self, text: str, **kwargs) -> str:
        """编码文本"""
        return encode(text, config=self.config, **kwargs)
    
    def decode(self, morse: str, **kwargs) -> str:
        """解码摩尔斯电码"""
        return decode(morse, config=self.config, **kwargs)
    
    def to_audio(self, text: str, **kwargs) -> bytes:
        """转换为音频"""
        return generate_morse_audio(text, config=self.config, **kwargs)
    
    def duration(self, morse: str) -> float:
        """计算播放时长"""
        return calculate_duration(morse, self.config)
    
    def __repr__(self):
        return f'MorseCode(dot={self.config.dot_duration}s, freq={self.config.frequency}Hz)'


# 便捷函数
def text_to_morse(text: str, **kwargs) -> str:
    """文本转摩尔斯电码（encode的别名）"""
    return encode(text, **kwargs)


def morse_to_text(morse: str, **kwargs) -> str:
    """摩尔斯电码转文本（decode的别名）"""
    return decode(morse, **kwargs)


def text_to_audio(text: str, **kwargs) -> bytes:
    """文本转音频（generate_morse_audio的别名）"""
    return generate_morse_audio(text, **kwargs)


if __name__ == '__main__':
    # 演示
    print("=== 摩尔斯电码工具演示 ===\n")
    
    # 编码
    text = "HELLO WORLD"
    morse = encode(text)
    print(f"编码: {text} -> {morse}")
    
    # 解码
    decoded = decode(morse)
    print(f"解码: {morse} -> {decoded}")
    
    # 计算时长
    duration = calculate_duration(morse)
    print(f"播放时长: {duration:.2f}秒")
    
    # 统计
    stats = get_morse_stats(morse)
    print(f"统计: {stats}")
    
    # 常见缩写
    print(f"\nSOS摩尔斯码: {translate_abbreviation('SOS')}")
    print(f"QTH含义: {translate_q_code('QTH')}")
    
    # 支持的字符
    print(f"\n支持的字符: {get_supported_characters()}")
    
    print("\n=== 演示完成 ===")