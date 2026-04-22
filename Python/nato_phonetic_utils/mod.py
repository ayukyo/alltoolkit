"""
NATO Phonetic Alphabet Utils - 北约音标字母工具

零依赖的北约音标字母库，支持：
- 文本转北约音标字母编码
- 北约音标字母转文本解码
- 音标拼写输出（带分隔符）
- 数字和特殊字符转换
- 多种输出格式（纯文本、空格分隔、编号列表）
- 语音播报文本生成
- 国际无线电通话字母表标准

NATO Phonetic Alphabet (国际无线电通话字母表):
- 字母: Alpha, Bravo, Charlie, Delta, Echo, Foxtrot, Golf, Hotel, 
       India, Juliet, Kilo, Lima, Mike, November, Oscar, Papa, 
       Quebec, Romeo, Sierra, Tango, Uniform, Victor, Whiskey, 
       X-ray, Yankee, Zulu
- 数字: Zero, One, Two, Three, Four, Five, Six, Seven, Eight, Nine

Author: AllToolkit
License: MIT
"""

from typing import Union, List, Tuple, Optional, Dict


# NATO 音标字母表（字母）
NATO_ALPHABET = {
    'A': 'Alpha',
    'B': 'Bravo',
    'C': 'Charlie',
    'D': 'Delta',
    'E': 'Echo',
    'F': 'Foxtrot',
    'G': 'Golf',
    'H': 'Hotel',
    'I': 'India',
    'J': 'Juliet',
    'K': 'Kilo',
    'L': 'Lima',
    'M': 'Mike',
    'N': 'November',
    'O': 'Oscar',
    'P': 'Papa',
    'Q': 'Quebec',
    'R': 'Romeo',
    'S': 'Sierra',
    'T': 'Tango',
    'U': 'Uniform',
    'V': 'Victor',
    'W': 'Whiskey',
    'X': 'X-ray',
    'Y': 'Yankee',
    'Z': 'Zulu',
}

# NATO 音标数字表
NATO_NUMBERS = {
    '0': 'Zero',
    '1': 'One',
    '2': 'Two',
    '3': 'Three',
    '4': 'Four',
    '5': 'Five',
    '6': 'Six',
    '7': 'Seven',
    '8': 'Eight',
    '9': 'Nine',
}

# NATO 音标特殊符号
NATO_SPECIAL = {
    '.': 'Decimal',      # 小数点
    '-': 'Dash',         # 连字符
    '/': 'Slash',        # 斜杠
    ' ': 'Space',        # 空格
    '+': 'Plus',         # 加号
    '*': 'Star',         # 星号
    '=': 'Equals',       # 等号
    '@': 'At',           # at 符号
    '#': 'Hash',         # 井号
    '$': 'Dollar',       # 美元符号
    '%': 'Percent',      # 百分号
    '&': 'Ampersand',    # 和号
    '(': 'Left Paren',   # 左括号
    ')': 'Right Paren',  # 右括号
    '[': 'Left Bracket', # 左方括号
    ']': 'Right Bracket',# 右方括号
    '{': 'Left Brace',   # 左花括号
    '}': 'Right Brace',  # 右花括号
    '<': 'Less Than',    # 小于号
    '>': 'Greater Than',# 大于号
    '_': 'Underscore',   # 下划线
    '|': 'Pipe',         # 管道符
    '\\': 'Backslash',   # 反斜杠
    '^': 'Caret',        # 脱字符
    '~': 'Tilde',        # 波浪号
    '`': 'Grave',        # 反引号
    "'": 'Apostrophe',   # 单引号
    '"': 'Quote',        # 双引号
    ':': 'Colon',        # 冒号
    ';': 'Semicolon',    # 分号
    ',': 'Comma',        # 逗号
    '?': 'Question',     # 问号
    '!': 'Exclamation',  # 感叹号
}

# 反向映射表（音标词转字符）
# 处理带连字符的音标词（如 X-ray）
NATO_DECODE_ALPHABET = {}
for k, v in NATO_ALPHABET.items():
    NATO_DECODE_ALPHABET[v.upper()] = k
    # 也添加不带连字符的版本
    NATO_DECODE_ALPHABET[v.upper().replace('-', '')] = k
    # 也添加带空格的版本（X ray）
    NATO_DECODE_ALPHABET[v.upper().replace('-', ' ')] = k

NATO_DECODE_NUMBERS = {v.upper(): k for k, v in NATO_NUMBERS.items()}
NATO_DECODE_SPECIAL = {v.upper(): k for k, v in NATO_SPECIAL.items()}

# 合并所有解码表
NATO_DECODE_ALL = {}
NATO_DECODE_ALL.update(NATO_DECODE_ALPHABET)
NATO_DECODE_ALL.update(NATO_DECODE_NUMBERS)
NATO_DECODE_ALL.update(NATO_DECODE_SPECIAL)

# 音标词的常见变体（解码时使用）
NATO_VARIANTS = {
    # 常见拼写变体
    'ALFA': 'A',        # 某些地区使用 Alfa 而非 Alpha
    'JULIETT': 'J',     # 某些地区使用 Juliett
    # 数字变体
    'NADAZERO': '0',    # ICAO 数字发音
    'UNAONE': '1',
    'BISOTWO': '2',
    'SERRATHREE': '3',
    'KARTEFour': '4',
    'PANTAFIVE': '5',
    'SOXISIX': '6',
    'SETTESEVEN': '7',
    'OKTOEIGHT': '8',
    'NOVENINE': '9',
    # 小数点变体
    'DECIMAL': '.',
    'POINT': '.',
    'DASH': '-',
    'MINUS': '-',
    'HYPHEN': '-',
}


def encode(
    text: str,
    separator: str = ' ',
    include_original: bool = False,
    skip_unknown: bool = False,
    unknown_placeholder: str = '?'
) -> str:
    """
    将文本编码为北约音标字母
    
    Args:
        text: 要编码的文本
        separator: 字符之间的分隔符，默认为空格
        include_original: 是否在输出中包含原始字符，如 "A-Alpha"
        skip_unknown: 是否跳过无法识别的字符
        unknown_placeholder: 未知字符的占位符
    
    Returns:
        北约音标编码字符串
    
    Examples:
        >>> encode('SOS')
        'Sierra Oscar Sierra'
        >>> encode('123', separator='-')
        'One-Two-Three'
        >>> encode('AB', include_original=True)
        'A-Alpha B-Bravo'
    """
    if not text:
        return ''
    
    result = []
    
    for char in text.upper():
        encoded = None
        
        # 查找字符对应的音标词
        if char in NATO_ALPHABET:
            encoded = NATO_ALPHABET[char]
        elif char in NATO_NUMBERS:
            encoded = NATO_NUMBERS[char]
        elif char in NATO_SPECIAL:
            encoded = NATO_SPECIAL[char]
        
        if encoded:
            if include_original:
                result.append(f"{char}-{encoded}")
            else:
                result.append(encoded)
        elif not skip_unknown:
            if include_original:
                result.append(f"{char}-{unknown_placeholder}")
            else:
                result.append(unknown_placeholder)
    
    return separator.join(result)


def decode(
    nato_text: str,
    separator: str = None,
    case_sensitive: bool = False
) -> str:
    """
    将北约音标字母解码为文本
    
    Args:
        nato_text: 北约音标文本（如 "Alpha Bravo Charlie"）
        separator: 输入的分隔符，默认自动检测（空格、逗号、换行等）
        case_sensitive: 是否区分大小写
    
    Returns:
        解码后的文本
    
    Examples:
        >>> decode('Sierra Oscar Sierra')
        'SOS'
        >>> decode('One-Two-Three', separator='-')
        '123'
        >>> decode('alpha BRAVO charlie')
        'ABC'
    """
    if not nato_text:
        return ''
    
    # 处理输入
    if not case_sensitive:
        nato_text_upper = nato_text.upper()
    else:
        nato_text_upper = nato_text
    
    # 先检查整个输入是否是一个有效的音标词（如 "X-ray"）
    if nato_text_upper in NATO_DECODE_ALL:
        return NATO_DECODE_ALL[nato_text_upper]
    if nato_text_upper in NATO_VARIANTS:
        return NATO_VARIANTS[nato_text_upper]
    
    # 自动检测分隔符
    if separator is None:
        # 尝试常见分隔符，优先使用空格
        separators_to_try = [' ', ',', '\n', '\t']
        for sep in separators_to_try:
            if sep in nato_text_upper:
                separator = sep
                break
        if separator is None:
            # 如果没有找到常见分隔符，检查是否包含连字符
            # 但要排除音标词内部的连字符（如 X-ray）
            if '-' in nato_text_upper:
                # 检查是否是多个音标词用连字符分隔
                parts = nato_text_upper.split('-')
                # 如果分割后的部分都是有效音标词，则使用连字符作为分隔符
                valid_parts = [p for p in parts if p in NATO_DECODE_ALL or p in NATO_VARIANTS]
                if len(valid_parts) == len(parts) and len(parts) > 1:
                    separator = '-'
                else:
                    # 否则不分割，保持原样
                    separator = ' '
            else:
                separator = ' '
    
    # 分割并解码
    words = [w.strip() for w in nato_text_upper.split(separator) if w.strip()]
    result = []
    
    for word in words:
        # 查找解码
        if word in NATO_DECODE_ALL:
            result.append(NATO_DECODE_ALL[word])
        elif word in NATO_VARIANTS:
            result.append(NATO_VARIANTS[word])
        else:
            # 尝试部分匹配（处理可能的拼写错误）
            found = False
            for key, value in NATO_DECODE_ALL.items():
                if key.startswith(word) or word.startswith(key):
                    result.append(value)
                    found = True
                    break
            if not found:
                result.append('?')  # 未知字符
    
    return ''.join(result)


def encode_word(word: str, separator: str = ' - ') -> str:
    """
    将单词编码为带分隔符的音标拼写
    
    Args:
        word: 要编码的单词
        separator: 字母之间的分隔符
    
    Returns:
        音标拼写字符串
    
    Examples:
        >>> encode_word('HELLO')
        'Hotel - Echo - Lima - Lima - Oscar'
    """
    return encode(word, separator)


def spell(text: str, format_type: str = 'default') -> str:
    """
    以指定格式拼写文本
    
    Args:
        text: 要拼写的文本
        format_type: 输出格式
            - 'default': 默认格式，如 "Alpha Bravo Charlie"
            - 'numbered': 编号格式，如 "1. Alpha 2. Bravo 3. Charlie"
            - 'table': 表格格式，如 "A = Alpha"
            - 'phonetic': 音标格式，如 "A as in Alpha"
    
    Returns:
        格式化的拼写输出
    
    Examples:
        >>> spell('ABC', format_type='numbered')
        '1. Alpha\\n2. Bravo\\n3. Charlie'
        >>> spell('ABC', format_type='table')
        'A = Alpha\\nB = Bravo\\nC = Charlie'
    """
    if not text:
        return ''
    
    result = []
    
    for i, char in enumerate(text.upper(), 1):
        encoded = None
        if char in NATO_ALPHABET:
            encoded = NATO_ALPHABET[char]
        elif char in NATO_NUMBERS:
            encoded = NATO_NUMBERS[char]
        elif char in NATO_SPECIAL:
            encoded = NATO_SPECIAL[char]
        
        if not encoded:
            continue
        
        if format_type == 'default':
            result.append(encoded)
        elif format_type == 'numbered':
            result.append(f"{i}. {encoded}")
        elif format_type == 'table':
            result.append(f"{char} = {encoded}")
        elif format_type == 'phonetic':
            result.append(f"{char} as in {encoded}")
        else:
            result.append(encoded)
    
    if format_type == 'default':
        return ' '.join(result)
    else:
        return '\n'.join(result)


def get_nato_word(char: str) -> Optional[str]:
    """
    获取单个字符对应的北约音标词
    
    Args:
        char: 单个字符
    
    Returns:
        对应的北约音标词，如果字符不支持则返回 None
    
    Examples:
        >>> get_nato_word('A')
        'Alpha'
        >>> get_nato_word('5')
        'Five'
        >>> get_nato_word('@')
        'At'
    """
    if not char or len(char) != 1:
        return None
    
    char = char.upper()
    
    if char in NATO_ALPHABET:
        return NATO_ALPHABET[char]
    elif char in NATO_NUMBERS:
        return NATO_NUMBERS[char]
    elif char in NATO_SPECIAL:
        return NATO_SPECIAL[char]
    
    return None


def get_char_from_nato(nato_word: str) -> Optional[str]:
    """
    从北约音标词获取对应的字符
    
    Args:
        nato_word: 北约音标词
    
    Returns:
        对应的字符，如果词不存在则返回 None
    
    Examples:
        >>> get_char_from_nato('Alpha')
        'A'
        >>> get_char_from_nato('Five')
        '5'
        >>> get_char_from_nato('ALPHA')  # 不区分大小写
        'A'
    """
    if not nato_word:
        return None
    
    nato_upper = nato_word.upper()
    
    if nato_upper in NATO_DECODE_ALL:
        return NATO_DECODE_ALL[nato_upper]
    elif nato_upper in NATO_VARIANTS:
        return NATO_VARIANTS[nato_upper]
    
    return None


def is_nato_word(word: str) -> bool:
    """
    检查单词是否为有效的北约音标词
    
    Args:
        word: 要检查的单词
    
    Returns:
        是否为有效的北约音标词
    
    Examples:
        >>> is_nato_word('Alpha')
        True
        >>> is_nato_word('Hello')
        False
    """
    if not word:
        return False
    
    return word.upper() in NATO_DECODE_ALL or word.upper() in NATO_VARIANTS


def get_all_letters() -> Dict[str, str]:
    """
    获取完整的北约字母表
    
    Returns:
        字母到音标词的映射字典
    
    Examples:
        >>> letters = get_all_letters()
        >>> letters['A']
        'Alpha'
    """
    return NATO_ALPHABET.copy()


def get_all_numbers() -> Dict[str, str]:
    """
    获取完整的北约数字表
    
    Returns:
        数字到音标词的映射字典
    
    Examples:
        >>> numbers = get_all_numbers()
        >>> numbers['1']
        'One'
    """
    return NATO_NUMBERS.copy()


def get_all_special() -> Dict[str, str]:
    """
    获取完整的北约特殊符号表
    
    Returns:
        特殊符号到音标词的映射字典
    """
    return NATO_SPECIAL.copy()


def text_to_radio_speech(text: str, include_spelling: bool = False) -> str:
    """
    将文本转换为无线电通话格式
    
    Args:
        text: 要转换的文本
        include_spelling: 是否在每个音标词后添加"as in..."
    
    Returns:
        无线电通话格式的字符串
    
    Examples:
        >>> text_to_radio_speech('ABC')
        'Alpha Bravo Charlie'
        >>> text_to_radio_speech('ABC', include_spelling=True)
        'A as in Alpha, B as in Bravo, C as in Charlie'
    """
    if not text:
        return ''
    
    result = []
    
    for char in text.upper():
        nato = get_nato_word(char)
        if nato:
            if include_spelling:
                result.append(f"{char} as in {nato}")
            else:
                result.append(nato)
        else:
            result.append(char)
    
    if include_spelling:
        return ', '.join(result)
    else:
        return ' '.join(result)


def pronounce_number(number: Union[int, float, str]) -> str:
    """
    将数字转换为北约音标发音
    
    Args:
        number: 要发音的数字
    
    Returns:
        北约音标格式的数字发音
    
    Examples:
        >>> pronounce_number(123)
        'One Two Three'
        >>> pronounce_number(3.14)
        'Three Decimal One Four'
    """
    if isinstance(number, (int, float)):
        number_str = str(number)
    else:
        number_str = number
    
    result = []
    
    for char in number_str:
        if char in NATO_NUMBERS:
            result.append(NATO_NUMBERS[char])
        elif char == '.':
            result.append('Decimal')
        elif char == '-':
            result.append('Minus')
        elif char == '+':
            result.append('Plus')
        else:
            result.append(char)
    
    return ' '.join(result)


def pronounce_phone_number(phone: str, include_country_code: bool = True) -> str:
    """
    将电话号码转换为北约音标发音格式
    
    Args:
        phone: 电话号码字符串
        include_country_code: 是否单独处理国家代码
    
    Returns:
        北约音标格式的电话号码发音
    
    Examples:
        >>> pronounce_phone_number('911')
        'Nine One One'
        >>> pronounce_phone_number('+1-555-123-4567')
        'Plus One Dash Five Five Five Dash One Two Three Dash Four Five Six Seven'
    """
    # 移除空格
    phone = phone.replace(' ', '')
    
    result = []
    
    for char in phone:
        if char in NATO_NUMBERS:
            result.append(NATO_NUMBERS[char])
        elif char == '+':
            result.append('Plus')
        elif char == '-':
            result.append('Dash')
        elif char == '(':
            result.append('Left Paren')
        elif char == ')':
            result.append('Right Paren')
        else:
            result.append(char)
    
    return ' '.join(result)


def pronounce_callsign(callsign: str, use_numbers_as_digits: bool = True) -> str:
    """
    将呼号转换为北约音标发音格式
    
    Args:
        callsign: 呼号字符串
        use_numbers_as_digits: 数字是否逐位发音
    
    Returns:
        北约音标格式的呼号发音
    
    Examples:
        >>> pronounce_callsign('KLM123')
        'Kilo Lima Mike One Two Three'
    """
    result = []
    
    for char in callsign.upper():
        if char in NATO_ALPHABET:
            result.append(NATO_ALPHABET[char])
        elif char in NATO_NUMBERS:
            result.append(NATO_NUMBERS[char])
        elif char in NATO_SPECIAL:
            result.append(NATO_SPECIAL[char])
        else:
            result.append(char)
    
    return ' '.join(result)


def verify_callsign(callsign: str) -> Tuple[bool, List[str]]:
    """
    验证呼号并返回音标拼写
    
    Args:
        callsign: 要验证的呼号
    
    Returns:
        (是否有效, 音标拼写列表)
    
    Examples:
        >>> verify_callsign('ABC123')
        (True, ['Alpha', 'Bravo', 'Charlie', 'One', 'Two', 'Three'])
        >>> verify_callsign('ABC@123')
        (False, ['Alpha', 'Bravo', 'Charlie', '?', 'One', 'Two', 'Three'])
    """
    result = []
    all_valid = True
    
    for char in callsign.upper():
        nato = get_nato_word(char)
        if nato:
            result.append(nato)
        else:
            result.append('?')
            all_valid = False
    
    return (all_valid, result)


def compare_nato_words(word1: str, word2: str) -> Tuple[bool, str, str]:
    """
    比较两个单词的北约音标拼写
    
    Args:
        word1: 第一个单词
        word2: 第二个单词
    
    Returns:
        (是否相同, 第一个单词的音标, 第二个单词的音标)
    
    Examples:
        >>> compare_nato_words('ABC', 'abc')
        (True, 'Alpha Bravo Charlie', 'Alpha Bravo Charlie')
    """
    nato1 = encode(word1)
    nato2 = encode(word2)
    
    return (nato1.upper() == nato2.upper(), nato1, nato2)


def generate_spelling_alphabet(language: str = 'nato') -> Dict[str, str]:
    """
    生成指定语言的拼写字母表
    
    Args:
        language: 字母表类型
            - 'nato': NATO 音标字母表（默认）
            - 'icao': ICAO 音标字母表（与 NATO 相同）
            - 'itu': ITU 音标字母表（与 NATO 相同）
            - 'ansi': ANSI 音标字母表（与 NATO 相同）
    
    Returns:
        字母到音标词的映射字典
    """
    # NATO, ICAO, ITU, ANSI 都使用相同的字母表
    return NATO_ALPHABET.copy()


class NATOConverter:
    """
    NATO 音标字母转换器类
    
    提供面向对象的接口进行编码和解码操作
    
    Examples:
        >>> converter = NATOConverter()
        >>> converter.encode('Hello')
        'Hotel Echo Lima Lima Oscar'
        >>> converter.decode('Alpha Bravo')
        'AB'
        >>> converter.spell('SOS')
        'Sierra Oscar Sierra'
    """
    
    def __init__(self, separator: str = ' '):
        """
        初始化转换器
        
        Args:
            separator: 默认分隔符
        """
        self.separator = separator
    
    def encode(self, text: str, separator: str = None) -> str:
        """编码文本为北约音标"""
        return encode(text, separator or self.separator)
    
    def decode(self, nato_text: str, separator: str = None) -> str:
        """解码北约音标为文本"""
        return decode(nato_text, separator)
    
    def spell(self, text: str, format_type: str = 'default') -> str:
        """拼写文本"""
        return spell(text, format_type)
    
    def get_word(self, char: str) -> Optional[str]:
        """获取字符对应的音标词"""
        return get_nato_word(char)
    
    def get_char(self, nato_word: str) -> Optional[str]:
        """从音标词获取字符"""
        return get_char_from_nato(nato_word)
    
    def is_valid_word(self, word: str) -> bool:
        """检查是否为有效音标词"""
        return is_nato_word(word)
    
    def pronounce(self, text: str) -> str:
        """生成发音文本"""
        return text_to_radio_speech(text)
    
    def __repr__(self) -> str:
        return "NATOConverter(separator='{}')".format(self.separator)
    
    def __str__(self) -> str:
        return "NATO Phonetic Alphabet Converter"


# 便捷函数别名
nato_encode = encode
nato_decode = decode
nato_spell = spell
nato_word = get_nato_word
nato_char = get_char_from_nato


if __name__ == '__main__':
    # 演示用法
    print("=" * 60)
    print("NATO Phonetic Alphabet Utils - 北约音标字母工具")
    print("=" * 60)
    
    # 基本编码
    print("\n基本编码:")
    print(f"  'SOS' -> {encode('SOS')}")
    print(f"  'ABC123' -> {encode('ABC123')}")
    
    # 不同分隔符
    print("\n不同分隔符:")
    print(f"  'ABC' (空格) -> {encode('ABC', ' ')}")
    print(f"  'ABC' (短横) -> {encode('ABC', '-')}")
    print(f"  'ABC' (斜杠) -> {encode('ABC', '/')}")
    
    # 包含原始字符
    print("\n包含原始字符:")
    print(f"  'AB' -> {encode('AB', include_original=True)}")
    
    # 解码
    print("\n解码:")
    print(f"  'Alpha Bravo' -> '{decode('Alpha Bravo')}'")
    print(f"  'One Two Three' -> '{decode('One Two Three')}'")
    print(f"  'Sierra-Oscar-Sierra' -> '{decode('Sierra-Oscar-Sierra', separator='-')}'")
    
    # 不同格式拼写
    print("\n不同格式拼写:")
    print(f"  默认格式:\n{spell('ABC', 'default')}")
    print(f"\n  编号格式:\n{spell('ABC', 'numbered')}")
    print(f"\n  表格格式:\n{spell('ABC', 'table')}")
    print(f"\n  音标格式:\n{spell('ABC', 'phonetic')}")
    
    # 数字发音
    print("\n数字发音:")
    print(f"  123 -> {pronounce_number(123)}")
    print(f"  3.14 -> {pronounce_number(3.14)}")
    
    # 电话号码
    print("\n电话号码发音:")
    print(f"  911 -> {pronounce_phone_number('911')}")
    print(f"  +1-555-123-4567 -> {pronounce_phone_number('+1-555-123-4567')}")
    
    # 呼号
    print("\n呼号发音:")
    print(f"  KLM123 -> {pronounce_callsign('KLM123')}")
    
    # 使用类
    print("\n使用 NATOConverter 类:")
    converter = NATOConverter()
    print(f"  编码 'HELLO' -> {converter.encode('HELLO')}")
    print(f"  解码 'Alpha Bravo' -> {converter.decode('Alpha Bravo')}")
    print(f"  验证呼号 'ABC123': {verify_callsign('ABC123')}")
    
    print("\n" + "=" * 60)
    print("完整字母表:")
    print("=" * 60)
    for char, word in NATO_ALPHABET.items():
        print(f"  {char} = {word}")
    
    print("\n" + "=" * 60)
    print("数字表:")
    print("=" * 60)
    for char, word in NATO_NUMBERS.items():
        print(f"  {char} = {word}")