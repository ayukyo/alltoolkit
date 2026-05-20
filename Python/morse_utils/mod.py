"""
摩尔斯电码工具模块 (Morse Code Utilities)

提供摩尔斯电码的编码、解码、音频生成等功能。
零依赖，纯 Python 标准库实现。

功能:
- 文本转摩尔斯电码
- 摩尔斯电码转文本
- 音频信号生成 (WAV 格式)
- 国际摩尔斯电码标准
- 支持字母、数字、标点符号
- 可配置的音频参数
"""

import math
import struct
import wave
from dataclasses import dataclass
from enum import Enum
from typing import Optional, Union, List, Tuple, BinaryIO


class MorseUnit(Enum):
    """摩尔斯电码时间单位"""
    DOT = 1       # 点 (基本单位)
    DASH = 3      # 划 (3个点)
    SYMBOL_GAP = 1  # 符号内间隔 (1个点)
    LETTER_GAP = 3  # 字母间隔 (3个点)
    WORD_GAP = 7    # 单词间隔 (7个点)


# 国际摩尔斯电码表
MORSE_CODE = {
    # 字母
    'A': '.-',      'B': '-...',    'C': '-.-.',
    'D': '-..',     'E': '.',       'F': '..-.',
    'G': '--.',     'H': '....',    'I': '..',
    'J': '.---',    'K': '-.-',     'L': '.-..',
    'M': '--',      'N': '-.',      'O': '---',
    'P': '.--.',    'Q': '--.-',    'R': '.-.',
    'S': '...',     'T': '-',       'U': '..-',
    'V': '...-',    'W': '.--',     'X': '-..-',
    'Y': '-.--',    'Z': '--..',
    # 数字
    '0': '-----',   '1': '.----',   '2': '..---',
    '3': '...--',    '4': '....-',   '5': '.....',
    '6': '-....',    '7': '--...',   '8': '---..',
    '9': '----.',
    # 标点符号
    '.': '.-.-.-',   ',': '--..--',  '?': '..--..',
    "'": '.----.',   '!': '-.-.--',  '/': '-..-.',
    '(': '-.--.',    ')': '-.--.-',  '&': '.-...',
    ':': '---...',   ';': '-.-.-.',  '=': '-...-',
    '+': '.-.-.',    '-': '-....-',  '_': '..--.-',
    '"': '.-..-.',   '$': '...-..-', '@': '.--.-.',
    # 特殊字符
    'Á': '.--.-',    'À': '.--.-',   'Ä': '.-.-',
    'É': '..-..',    'Ñ': '--.--',   'Ö': '---.',
    'Ü': '..--',     'ß': '...--..',
}

# 反向映射表 (摩尔斯电码 -> 字符)
# 注意: 对于有重复电码的情况，只保留第一个
MORSE_DECODE = {}
for k, v in MORSE_CODE.items():
    if v not in MORSE_DECODE:
        MORSE_DECODE[v] = k

# 常用缩写
MORSE_ABBREVIATIONS = {
    'SOS': '... --- ...',      # 求救信号
    'CQ': '-.-. --.-',          # 呼叫所有台站
    'DE': '-.. .',              # 来自
    'K': '-.-',                 # 邀请回复
    'R': '.-.',                 # 收到/确认
    '73': '--... ...--',       # 致意
    '88': '---.. ---..',       # 爱与吻
    'QTH': '--.- - ....',      # 位置
    'QRZ': '--.- .-. --..',    # 谁在呼叫?
    'QRM': '--.- .-. --',      # 干扰
    'QRN': '--.- .-. -.',      # 天电干扰
    'QSL': '--.- ... .-..',    # 确认收到
    'QSO': '--.- ... ---',     # 通讯
    'RST': '.-. ... -',        # 信号报告
    'HAM': '.... .- --',       # 业余无线电爱好者
}


@dataclass
class MorseConfig:
    """摩尔斯电码配置"""
    dot_symbol: str = '.'           # 点符号
    dash_symbol: str = '-'          # 划符号
    symbol_separator: str = ' '     # 符号间隔
    letter_separator: str = ' '     # 字母间隔
    word_separator: str = ' / '     # 单词间隔
    
    # 音频参数
    frequency: int = 700            # 音频频率 (Hz)
    sample_rate: int = 44100        # 采样率
    dot_duration: float = 0.06      # 点持续时间 (秒)
    
    # 字符处理
    unknown_char: str = '?'         # 未知字符替换
    ignore_unknown: bool = False    # 是否忽略未知字符
    
    def __post_init__(self):
        """验证配置参数"""
        if self.frequency <= 0:
            raise ValueError(f"频率必须为正数: {self.frequency}")
        if self.sample_rate <= 0:
            raise ValueError(f"采样率必须为正数: {self.sample_rate}")
        if self.dot_duration <= 0:
            raise ValueError(f"点持续时间必须为正数: {self.dot_duration}")


class MorseEncoder:
    """摩尔斯电码编码器"""
    
    def __init__(self, config: Optional[MorseConfig] = None):
        self.config = config or MorseConfig()
    
    def encode(self, text: str) -> str:
        """
        将文本编码为摩尔斯电码
        
        Args:
            text: 要编码的文本
        
        Returns:
            摩尔斯电码字符串
        
        Example:
            >>> encoder = MorseEncoder()
            >>> encoder.encode('SOS')
            '... --- ...'
            >>> encoder.encode('Hello World')
            '.... . .-.. .-.. --- / .-- --- .-. .-.. -..'
        """
        if not text:
            return ''
        
        words = text.upper().split()
        encoded_words = []
        
        for word in words:
            encoded_letters = []
            for char in word:
                if char in MORSE_CODE:
                    # 使用自定义符号替换默认符号
                    morse = MORSE_CODE[char]
                    morse = morse.replace('.', self.config.dot_symbol).replace('-', self.config.dash_symbol)
                    encoded_letters.append(morse)
                elif char in MORSE_ABBREVIATIONS:
                    morse = MORSE_ABBREVIATIONS[char]
                    morse = morse.replace('.', self.config.dot_symbol).replace('-', self.config.dash_symbol)
                    encoded_letters.append(morse)
                else:
                    if not self.config.ignore_unknown:
                        encoded_letters.append(self.config.unknown_char)
            
            if encoded_letters:
                encoded_words.append(self.config.letter_separator.join(encoded_letters))
        
        return self.config.word_separator.join(encoded_words)
    
    def encode_letter(self, char: str) -> Optional[str]:
        """
        编码单个字符
        
        Args:
            char: 要编码的字符
        
        Returns:
            摩尔斯电码字符串，如果字符不支持则返回 None
        """
        if len(char) != 1:
            raise ValueError("只能编码单个字符")
        
        char = char.upper()
        return MORSE_CODE.get(char)
    
    def encode_with_timing(self, text: str) -> List[Tuple[str, int]]:
        """
        编码文本并返回带时间单位的结果
        
        Args:
            text: 要编码的文本
        
        Returns:
            列表，每项为 (符号, 时间单位) 元组
            符号为 'dot', 'dash', 'gap' 或 'word_gap'
        
        Example:
            >>> encoder = MorseEncoder()
            >>> encoder.encode_with_timing('A')
            [('dot', 1), ('gap', 1), ('dash', 3)]
        """
        result = []
        morse = self.encode(text)
        
        prev_symbol = None
        for char in morse:
            if char == self.config.dot_symbol:
                result.append(('dot', 1))
                prev_symbol = 'dot'
            elif char == self.config.dash_symbol:
                result.append(('dash', 3))
                prev_symbol = 'dash'
            elif char == ' ' and prev_symbol in ('dot', 'dash'):
                # 符号间隔已在 MORSE_CODE 中包含
                prev_symbol = 'gap'
            elif char == '/' or (char == ' ' and prev_symbol == 'gap'):
                result.append(('word_gap', 7))
                prev_symbol = 'word_gap'
        
        return result


class MorseDecoder:
    """摩尔斯电码解码器"""
    
    def __init__(self, config: Optional[MorseConfig] = None):
        self.config = config or MorseConfig()
    
    def decode(self, morse: str) -> str:
        """
        将摩尔斯电码解码为文本
        
        Args:
            morse: 摩尔斯电码字符串
        
        Returns:
            解码后的文本
        
        Example:
            >>> decoder = MorseDecoder()
            >>> decoder.decode('... --- ...')
            'SOS'
            >>> decoder.decode('.... . .-.. .-.. --- / .-- --- .-. .-.. -..')
            'HELLO WORLD'
        """
        if not morse:
            return ''
        
        # 标准化分隔符
        morse = morse.replace('/', self.config.word_separator)
        
        # 分割单词
        words = morse.split(self.config.word_separator.strip())
        decoded_words = []
        
        for word in words:
            word = word.strip()
            if not word:
                continue
            
            # 分割字母
            letters = word.split(self.config.letter_separator)
            decoded_letters = []
            
            for letter in letters:
                letter = letter.strip()
                if not letter:
                    continue
                
                # 标准化符号
                letter = letter.replace('•', '.').replace('—', '-').replace('–', '-')
                letter = letter.replace('＊', '.').replace('━', '-')
                
                if letter in MORSE_DECODE:
                    decoded_letters.append(MORSE_DECODE[letter])
                else:
                    if not self.config.ignore_unknown:
                        decoded_letters.append(self.config.unknown_char)
            
            if decoded_letters:
                decoded_words.append(''.join(decoded_letters))
        
        return ' '.join(decoded_words)
    
    def decode_letter(self, morse: str) -> Optional[str]:
        """
        解码单个摩尔斯电码为字符
        
        Args:
            morse: 摩尔斯电码字符串
        
        Returns:
            解码后的字符，如果电码无效则返回 None
        """
        morse = morse.strip()
        morse = morse.replace('•', '.').replace('—', '-').replace('–', '-')
        return MORSE_DECODE.get(morse)
    
    def is_valid_morse(self, morse: str) -> bool:
        """
        检查摩尔斯电码是否有效
        
        Args:
            morse: 摩尔斯电码字符串
        
        Returns:
            是否有效
        """
        morse = morse.strip()
        if not morse:
            return False
        
        # 只包含有效字符
        valid_chars = set('.- /•—–')
        return all(c in valid_chars for c in morse)


class MorseAudioGenerator:
    """摩尔斯电码音频生成器"""
    
    def __init__(self, config: Optional[MorseConfig] = None):
        self.config = config or MorseConfig()
    
    def _generate_tone(self, frequency: int, duration: float, 
                       sample_rate: int) -> bytes:
        """
        生成正弦波音频数据
        
        Args:
            frequency: 频率 (Hz)
            duration: 持续时间 (秒)
            sample_rate: 采样率
        
        Returns:
            音频数据 (16位 PCM)
        """
        samples = int(duration * sample_rate)
        data = []
        
        for i in range(samples):
            t = i / sample_rate
            # 使用正弦波生成音频
            value = math.sin(2 * math.pi * frequency * t)
            # 转换为 16 位有符号整数
            sample = int(value * 32767)
            # 应用平滑包络，避免爆音
            envelope = 1.0
            attack_samples = int(0.005 * sample_rate)  # 5ms 起音
            release_samples = int(0.005 * sample_rate)  # 5ms 释放
            
            if i < attack_samples:
                envelope = i / attack_samples
            elif i > samples - release_samples:
                envelope = (samples - i) / release_samples
            
            sample = int(sample * envelope)
            data.append(struct.pack('<h', sample))
        
        return b''.join(data)
    
    def _generate_silence(self, duration: float, sample_rate: int) -> bytes:
        """
        生成静音数据
        
        Args:
            duration: 持续时间 (秒)
            sample_rate: 采样率
        
        Returns:
            静音数据 (16位 PCM)
        """
        samples = int(duration * sample_rate)
        return b'\x00\x00' * samples
    
    def generate_audio(self, text: str) -> bytes:
        """
        为文本生成摩尔斯电码音频
        
        Args:
            text: 要转换的文本
        
        Returns:
            WAV 音频数据 (bytes)
        
        Example:
            >>> generator = MorseAudioGenerator()
            >>> audio = generator.generate_audio('SOS')
            >>> # 保存到文件
            >>> with open('morse.wav', 'wb') as f:
            ...     f.write(audio)
        """
        config = self.config
        encoder = MorseEncoder(config)
        morse = encoder.encode(text)
        
        if not morse:
            return self._create_wav(b'')
        
        dot_time = config.dot_duration
        dash_time = dot_time * 3
        symbol_gap = dot_time
        letter_gap = dot_time * 3
        word_gap = dot_time * 7
        
        audio_data = []
        
        for char in morse:
            if char == config.dot_symbol:
                # 点
                audio_data.append(self._generate_tone(
                    config.frequency, dot_time, config.sample_rate
                ))
                audio_data.append(self._generate_silence(symbol_gap, config.sample_rate))
            elif char == config.dash_symbol:
                # 划
                audio_data.append(self._generate_tone(
                    config.frequency, dash_time, config.sample_rate
                ))
                audio_data.append(self._generate_silence(symbol_gap, config.sample_rate))
            elif char == config.letter_separator:
                # 字母间隔 (减去已添加的符号间隔)
                audio_data.append(self._generate_silence(
                    letter_gap - symbol_gap, config.sample_rate
                ))
            elif char == '/':
                # 单词间隔
                audio_data.append(self._generate_silence(word_gap, config.sample_rate))
        
        # 移除末尾多余的静音
        combined = b''.join(audio_data)
        if combined.endswith(self._generate_silence(symbol_gap, config.sample_rate)):
            combined = combined[:-len(self._generate_silence(symbol_gap, config.sample_rate))]
        
        return self._create_wav(combined)
    
    def _create_wav(self, audio_data: bytes) -> bytes:
        """
        创建 WAV 文件数据
        
        Args:
            audio_data: 音频数据 (16位 PCM)
        
        Returns:
            完整的 WAV 文件数据
        """
        import io
        buffer = io.BytesIO()
        
        with wave.open(buffer, 'wb') as wav:
            wav.setnchannels(1)  # 单声道
            wav.setsampwidth(2)  # 16位
            wav.setframerate(self.config.sample_rate)
            wav.writeframes(audio_data)
        
        return buffer.getvalue()
    
    def save_audio(self, text: str, filepath: str) -> int:
        """
        将摩尔斯电码音频保存到文件
        
        Args:
            text: 要转换的文本
            filepath: 文件路径
        
        Returns:
            写入的字节数
        
        Example:
            >>> generator = MorseAudioGenerator()
            >>> generator.save_audio('SOS', 'sos.wav')
            44100
        """
        audio_data = self.generate_audio(text)
        with open(filepath, 'wb') as f:
            f.write(audio_data)
        return len(audio_data)


class MorseUtils:
    """摩尔斯电码工具类"""
    
    def __init__(self, config: Optional[MorseConfig] = None):
        self.config = config or MorseConfig()
        self.encoder = MorseEncoder(config)
        self.decoder = MorseDecoder(config)
        self.audio_generator = MorseAudioGenerator(config)
    
    def encode(self, text: str) -> str:
        """编码文本为摩尔斯电码"""
        return self.encoder.encode(text)
    
    def decode(self, morse: str) -> str:
        """解码摩尔斯电码为文本"""
        return self.decoder.decode(morse)
    
    def generate_audio(self, text: str) -> bytes:
        """生成音频数据"""
        return self.audio_generator.generate_audio(text)
    
    def save_audio(self, text: str, filepath: str) -> int:
        """保存音频到文件"""
        return self.audio_generator.save_audio(text, filepath)
    
    @staticmethod
    def get_morse_table() -> dict:
        """获取完整的摩尔斯电码表"""
        return MORSE_CODE.copy()
    
    @staticmethod
    def get_abbreviations() -> dict:
        """获取常用缩写表"""
        return MORSE_ABBREVIATIONS.copy()
    
    def is_valid_morse(self, morse: str) -> bool:
        """检查摩尔斯电码是否有效"""
        return self.decoder.is_valid_morse(morse)
    
    def calculate_duration(self, text: str) -> float:
        """
        计算播放摩尔斯电码所需时间
        
        Args:
            text: 文本
        
        Returns:
            时长 (秒)
        """
        morse = self.encode(text)
        dot_time = self.config.dot_duration
        
        total_units = 0
        for char in morse:
            if char == self.config.dot_symbol:
                total_units += 1  # 点 = 1 单位
            elif char == self.config.dash_symbol:
                total_units += 3  # 划 = 3 单位
            elif char == self.config.letter_separator:
                total_units += 2  # 字母间隔 = 3 - 1 (减去已加的符号间隔)
            elif char == '/':
                total_units += 6  # 单词间隔 = 7 - 1
        
        # 加上最后一个符号后的静音
        return total_units * dot_time
    
    def get_statistics(self, text: str) -> dict:
        """
        获取摩尔斯电码统计信息
        
        Args:
            text: 文本
        
        Returns:
            统计信息字典
        """
        morse = self.encode(text)
        
        dots = morse.count(self.config.dot_symbol)
        dashes = morse.count(self.config.dash_symbol)
        
        return {
            'original_text': text,
            'morse_code': morse,
            'dot_count': dots,
            'dash_count': dashes,
            'total_symbols': dots + dashes,
            'duration_seconds': self.calculate_duration(text),
            'character_count': len(text.replace(' ', '')),
            'word_count': len(text.split()),
        }
    
    def visualize(self, text: str, style: str = 'standard') -> str:
        """
        可视化摩尔斯电码
        
        Args:
            text: 文本
            style: 样式 ('standard', 'dots', 'bars', 'sound')
        
        Returns:
            可视化字符串
        
        Example:
            >>> utils = MorseUtils()
            >>> utils.visualize('SOS', style='sound')
            'di-di-dit da-da-dah di-di-dit'
        """
        morse = self.encode(text)
        
        if style == 'standard':
            return morse
        elif style == 'dots':
            # 使用圆点表示
            return morse.replace('.', '•').replace('-', '—')
        elif style == 'bars':
            # 使用竖线表示
            return morse.replace('.', '|').replace('-', '|||')
        elif style == 'sound':
            # 音效拟声表示
            result = []
            current_word = []
            
            for char in morse:
                if char == '.':
                    current_word.append('di')
                elif char == '-':
                    current_word.append('da')
                elif char == ' ' and current_word:
                    # 字母结束
                    if current_word and current_word[-1] == 'di':
                        current_word[-1] = 'dit'
                    result.append('-'.join(current_word))
                    current_word = []
                elif char == '/':
                    # 单词结束
                    result.append(' ')
            
            if current_word:
                if current_word[-1] == 'di':
                    current_word[-1] = 'dit'
                result.append('-'.join(current_word))
            
            return ' '.join(result)
        else:
            return morse
    
    def practice(self, char: Optional[str] = None) -> dict:
        """
        生成练习材料
        
        Args:
            char: 指定练习的字符，None 则随机
        
        Returns:
            练习信息字典
        """
        import random
        
        if char:
            char = char.upper()
        else:
            char = random.choice(list(MORSE_CODE.keys()))
        
        morse = MORSE_CODE.get(char, '')
        
        return {
            'character': char,
            'morse_code': morse,
            'description': self._get_char_description(char),
            'mnemonic': self._get_mnemonic(char),
        }
    
    def _get_char_description(self, char: str) -> str:
        """获取字符描述"""
        descriptions = {
            'A': "Alpha - 点划",
            'B': "Bravo - 划点点点",
            'C': "Charlie - 划点划点",
            'D': "Delta - 划点点",
            'E': "Echo - 点",
            'F': "Foxtrot - 点点划点",
            'G': "Golf - 划划点",
            'H': "Hotel - 点点点点",
            'I': "India - 点点",
            'J': "Juliet - 点划划划",
            'K': "Kilo - 划点划",
            'L': "Lima - 点划点点",
            'M': "Mike - 划划",
            'N': "November - 划点",
            'O': "Oscar - 划划划",
            'P': "Papa - 点划划点",
            'Q': "Quebec - 划划点划",
            'R': "Romeo - 点划点",
            'S': "Sierra - 点点点",
            'T': "Tango - 划",
            'U': "Uniform - 点点划",
            'V': "Victor - 点点点划",
            'W': "Whiskey - 点划划",
            'X': "X-ray - 划点点划",
            'Y': "Yankee - 划点划划",
            'Z': "Zulu - 划划点点",
        }
        return descriptions.get(char, f"字符 {char}")
    
    def _get_mnemonic(self, char: str) -> str:
        """获取记忆口诀"""
        mnemonics = {
            'A': "A (点划): a-PART (划比点长)",
            'B': "B (划点点点): B-BB-B (划长后三个短)",
            'C': "C (划点划点): CO-CO (划点交替)",
            'D': "D (划点点): DOG-DO (划后两个点)",
            'E': "E (点): E (最短)",
            'S': "S (点点点): SSS (三个点)",
            'O': "O (划划划): OOO (三个划)",
            'T': "T (划): T (最长)",
        }
        return mnemonics.get(char, "")


# 便捷函数
def encode(text: str, config: Optional[MorseConfig] = None) -> str:
    """编码文本为摩尔斯电码"""
    return MorseEncoder(config).encode(text)


def decode(morse: str, config: Optional[MorseConfig] = None) -> str:
    """解码摩尔斯电码为文本"""
    return MorseDecoder(config).decode(morse)


def generate_audio(text: str, config: Optional[MorseConfig] = None) -> bytes:
    """生成摩尔斯电码音频"""
    return MorseAudioGenerator(config).generate_audio(text)


def save_audio(text: str, filepath: str, config: Optional[MorseConfig] = None) -> int:
    """保存摩尔斯电码音频到文件"""
    return MorseAudioGenerator(config).save_audio(text, filepath)


def get_morse_table() -> dict:
    """获取摩尔斯电码表"""
    return MORSE_CODE.copy()


def get_abbreviations() -> dict:
    """获取常用缩写表"""
    return MORSE_ABBREVIATIONS.copy()