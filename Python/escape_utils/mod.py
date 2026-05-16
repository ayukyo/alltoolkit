"""
转义工具 (Escape Utils) 模块

提供多种格式字符串的转义和反转义功能，包括：
- HTML 转义/反转义
- XML 转义/反转义
- URL 编码/解码
- JSON 字符串转义/反转义
- Shell 命令转义
- 正则表达式转义
- Glob 模式转义
- C 语言字符串转义
- SQL 字符串转义
- Base64 编码/解码（标准变体）

零外部依赖，纯 Python 实现。

使用场景：
- 安全处理用户输入
- 生成安全的 HTML/XML 内容
- 构建 URL 查询参数
- 创建安全的 shell 命令
- 处理特殊字符
- 数据传输编码
"""

import re
from typing import Dict, List, Optional, Tuple, Union


# ============================================================================
# HTML 转义
# ============================================================================

HTML_ESCAPE_CHARS: Dict[str, str] = {
    '&': '&amp;',
    '<': '&lt;',
    '>': '&gt;',
    '"': '&quot;',
    "'": '&apos;',
}

HTML_UNESCAPE_CHARS: Dict[str, str] = {
    '&amp;': '&',
    '&lt;': '<',
    '&gt;': '>',
    '&quot;': '"',
    '&apos;': "'",
    '&#39;': "'",
}

# 扩展 HTML 实体（常见字符）
HTML_EXTENDED_ENTITIES: Dict[str, str] = {
    '&nbsp;': ' ',
    '&copy;': '©',
    '&reg;': '®',
    '&trade;': '™',
    '&euro;': '€',
    '&pound;': '£',
    '&yen;': '¥',
    '&cent;': '¢',
    '&deg;': '°',
    '&plusmn;': '±',
    '&times;': '×',
    '&divide;': '÷',
    '&frac12;': '½',
    '&frac14;': '¼',
    '&frac34;': '¾',
    '&para;': '¶',
    '&sect;': '§',
    '&bull;': '•',
    '&middot;': '·',
    '&hellip;': '…',
    '&ndash;': '–',
    '&mdash;': '—',
    '&laquo;': '«',
    '&raquo;': '»',
    '&lsquo;': ''',
    '&rsquo;': ''',
    '&ldquo;': '"',
    '&rdquo;': '"',
    '&sbquo;': '‚',
    '&bdquo;': '„',
    '& dagger;': '†',
    '&Dagger;': '‡',
    '&larr;': '←',
    '&rarr;': '→',
    '&uarr;': '↑',
    '&darr;': '↓',
    '&harr;': '↔',
    '&crarr;': '↵',
    '&lceil;': '⌈',
    '&rceil;': '⌉',
    '&lfloor;': '⌊',
    '&rfloor;': '⌋',
    '&loz;': '◊',
    '&spades;': '♠',
    '&clubs;': '♣',
    '&hearts;': '♥',
    '&diams;': '♦',
    '&alpha;': 'α',
    '&beta;': 'β',
    '&gamma;': 'γ',
    '&delta;': 'δ',
    '&epsilon;': 'ε',
    '&zeta;': 'ζ',
    '&eta;': 'η',
    '&theta;': 'θ',
    '&iota;': 'ι',
    '&kappa;': 'κ',
    '&lambda;': 'λ',
    '&mu;': 'μ',
    '&nu;': 'ν',
    '&xi;': 'ξ',
    '&omicron;': 'ο',
    '&pi;': 'π',
    '&rho;': 'ρ',
    '&sigma;': 'σ',
    '&tau;': 'τ',
    '&upsilon;': 'υ',
    '&phi;': 'φ',
    '&chi;': 'χ',
    '&psi;': 'ψ',
    '&omega;': 'ω',
    '&Alpha;': 'Α',
    '&Beta;': 'Β',
    '&Gamma;': 'Γ',
    '&Delta;': 'Δ',
    '&Epsilon;': 'Ε',
    '&Zeta;': 'Ζ',
    '&Eta;': 'Η',
    '&Theta;': 'Θ',
    '&Iota;': 'Ι',
    '&Kappa;': 'Κ',
    '&Lambda;': 'Λ',
    '&Mu;': 'Μ',
    '&Nu;': 'Ν',
    '&Xi;': 'Ξ',
    '&Omicron;': 'Ο',
    '&Pi;': 'Π',
    '&Rho;': 'Ρ',
    '&Sigma;': 'Σ',
    '&Tau;': 'Τ',
    '&Upsilon;': 'Υ',
    '&Phi;': 'Φ',
    '&Chi;': 'Χ',
    '&Psi;': 'Ψ',
    '&Omega;': 'Ω',
}


def escape_html(text: str, extended: bool = False) -> str:
    """
    转义 HTML 特殊字符
    
    Args:
        text: 要转义的字符串
        extended: 是否转义扩展实体（如 ©, € 等）
        
    Returns:
        转义后的字符串
        
    Example:
        >>> escape_html('<script>alert("XSS")</script>')
        '&lt;script&gt;alert(&quot;XSS&quot;)&lt;/script&gt;'
    """
    result = text
    for char, entity in HTML_ESCAPE_CHARS.items():
        result = result.replace(char, entity)
    
    if extended:
        # 转义扩展字符
        for char, entity in HTML_EXTENDED_ENTITIES.items():
            # 反向查找
            actual_char = HTML_EXTENDED_ENTITIES.get(entity, entity)
            if actual_char in result and entity != actual_char:
                result = result.replace(actual_char, entity)
    
    return result


def unescape_html(text: str, extended: bool = True) -> str:
    """
    反转义 HTML 实体
    
    Args:
        text: 包含 HTML 实体的字符串
        extended: 是否反转义扩展实体
        
    Returns:
        反转义后的字符串
        
    Example:
        >>> unescape_html('&lt;div&gt;Hello&lt;/div&gt;')
        '<div>Hello</div>'
    """
    result = text
    
    # 先处理基本实体
    for entity, char in HTML_UNESCAPE_CHARS.items():
        result = result.replace(entity, char)
    
    # 处理扩展实体
    if extended:
        for entity, char in HTML_EXTENDED_ENTITIES.items():
            result = result.replace(entity, char)
    
    # 处理数字实体（十进制）
    decimal_pattern = re.compile(r'&#(\d+);')
    def replace_decimal(match):
        try:
            return chr(int(match.group(1)))
        except (ValueError, OverflowError):
            return match.group(0)
    result = decimal_pattern.sub(replace_decimal, result)
    
    # 处理数字实体（十六进制）- 支持 x 和 X
    hex_pattern = re.compile(r'&#[xX]([0-9a-fA-F]+);')
    def replace_hex(match):
        try:
            return chr(int(match.group(1), 16))
        except (ValueError, OverflowError):
            return match.group(0)
    result = hex_pattern.sub(replace_hex, result)
    
    return result


# ============================================================================
# XML 转义
# ============================================================================

XML_ESCAPE_CHARS: Dict[str, str] = {
    '&': '&amp;',
    '<': '&lt;',
    '>': '&gt;',
    '"': '&quot;',
    "'": '&apos;',
}

XML_ATTR_ESCAPE_CHARS: Dict[str, str] = {
    '&': '&amp;',
    '<': '&lt;',
    '>': '&gt;',
    '"': '&quot;',
    "'": '&apos;',
    '\t': '&#9;',
    '\n': '&#10;',
    '\r': '&#13;',
}


def escape_xml(text: str, is_attribute: bool = False) -> str:
    """
    转义 XML 特殊字符
    
    Args:
        text: 要转义的字符串
        is_attribute: 是否为属性值（转义更多字符）
        
    Returns:
        转义后的字符串
        
    Example:
        >>> escape_xml('<note>Test</note>')
        '&lt;note&gt;Test&lt;/note&gt;'
    """
    chars = XML_ATTR_ESCAPE_CHARS if is_attribute else XML_ESCAPE_CHARS
    result = text
    for char, entity in chars.items():
        result = result.replace(char, entity)
    return result


def unescape_xml(text: str) -> str:
    """
    反转义 XML 实体
    
    Args:
        text: 包含 XML 实体的字符串
        
    Returns:
        反转义后的字符串
    """
    result = text
    for entity, char in {'&amp;': '&', '&lt;': '<', '&gt;': '>', 
                         '&quot;': '"', '&apos;': "'",
                         '&#9;': '\t', '&#10;': '\n', '&#13;': '\r'}.items():
        result = result.replace(entity, char)
    
    # 处理数字实体
    decimal_pattern = re.compile(r'&#(\d+);')
    def replace_decimal(match):
        try:
            return chr(int(match.group(1)))
        except (ValueError, OverflowError):
            return match.group(0)
    result = decimal_pattern.sub(replace_decimal, result)
    
    hex_pattern = re.compile(r'&#[xX]([0-9a-fA-F]+);')
    def replace_hex(match):
        try:
            return chr(int(match.group(1), 16))
        except (ValueError, OverflowError):
            return match.group(0)
    result = hex_pattern.sub(replace_hex, result)
    
    return result


# ============================================================================
# URL 编码
# ============================================================================

# URL 安全字符（RFC 3986）
URL_SAFE_CHARS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-._~"
URL_QUERY_SAFE_CHARS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-._~!$'()*,;"


def escape_url(text: str, encoding: str = 'utf-8', 
               safe: str = '', plus_space: bool = True) -> str:
    """
    URL 编码
    
    Args:
        text: 要编码的字符串
        encoding: 字符编码
        safe: 不需要编码的额外字符
        plus_space: 是否将空格编码为 '+'（查询字符串风格）
        
    Returns:
        URL 编码后的字符串
        
    Example:
        >>> escape_url('hello world')
        'hello+world'
        >>> escape_url('hello world', plus_space=False)
        'hello%20world'
    """
    result = []
    
    # 合并安全字符
    all_safe = URL_SAFE_CHARS + safe
    
    for char in text:
        if char in all_safe:
            result.append(char)
        elif char == ' ' and plus_space:
            result.append('+')
        else:
            # 编码字符
            encoded = char.encode(encoding)
            for byte in encoded:
                result.append(f'%{byte:02X}')
    
    return ''.join(result)


def unescape_url(text: str, encoding: str = 'utf-8', plus_space: bool = True) -> str:
    """
    URL 解码
    
    Args:
        text: URL 编码的字符串
        encoding: 字符编码
        plus_space: 是否将 '+' 解码为空格
        
    Returns:
        URL 解码后的字符串
        
    Example:
        >>> unescape_url('hello%20world')
        'hello world'
    """
    result = []
    i = 0
    
    while i < len(text):
        if text[i] == '%' and i + 2 < len(text):
            # 解码百分号编码
            try:
                byte_val = int(text[i+1:i+3], 16)
                result.append(byte_val)
                i += 3
            except ValueError:
                result.append(ord(text[i]))
                i += 1
        elif text[i] == '+' and plus_space:
            result.append(ord(' '))
            i += 1
        else:
            result.append(ord(text[i]))
            i += 1
    
    # 解码字节序列
    try:
        return bytes(result).decode(encoding)
    except UnicodeDecodeError:
        return ''.join(chr(b) if b < 128 else f'%{b:02X}' for b in result)


def escape_url_query(params: Dict[str, Union[str, List[str]]], 
                     encoding: str = 'utf-8') -> str:
    """
    将字典转换为 URL 查询字符串
    
    Args:
        params: 参数字典
        encoding: 字符编码
        
    Returns:
        URL 查询字符串
        
    Example:
        >>> escape_url_query({'name': '张三', 'age': '25'})
        'name=%E5%BC%A0%E4%B8%89&age=25'
    """
    parts = []
    
    for key, value in params.items():
        encoded_key = escape_url(str(key), encoding, plus_space=True)
        
        if isinstance(value, list):
            for item in value:
                encoded_value = escape_url(str(item), encoding, plus_space=True)
                parts.append(f'{encoded_key}={encoded_value}')
        else:
            encoded_value = escape_url(str(value), encoding, plus_space=True)
            parts.append(f'{encoded_key}={encoded_value}')
    
    return '&'.join(parts)


def unescape_url_query(query: str, encoding: str = 'utf-8',
                       plus_space: bool = True) -> Dict[str, Union[str, List[str]]]:
    """
    解析 URL 查询字符串为字典
    
    Args:
        query: URL 查询字符串
        encoding: 字符编码
        plus_space: 是否将 '+' 解码为空格
        
    Returns:
        参数字典（重复参数会合并为列表）
        
    Example:
        >>> unescape_url_query('name=%E5%BC%A0%E4%B8%89&age=25')
        {'name': '张三', 'age': '25'}
    """
    params: Dict[str, Union[str, List[str]]] = {}
    
    if not query:
        return params
    
    # 去除前导 '?'
    if query.startswith('?'):
        query = query[1:]
    
    for part in query.split('&'):
        if not part:
            continue
        
        if '=' in part:
            key, value = part.split('=', 1)
            key = unescape_url(key, encoding, plus_space)
            value = unescape_url(value, encoding, plus_space)
        else:
            key = unescape_url(part, encoding, plus_space)
            value = ''
        
        if key in params:
            existing = params[key]
            if isinstance(existing, list):
                existing.append(value)
            else:
                params[key] = [existing, value]
        else:
            params[key] = value
    
    return params


# ============================================================================
# JSON 字符串转义
# ============================================================================

JSON_ESCAPE_CHARS: Dict[str, str] = {
    '"': '\\"',
    '\\': '\\\\',
    '\b': '\\b',
    '\f': '\\f',
    '\n': '\\n',
    '\r': '\\r',
    '\t': '\\t',
}

# JSON 控制字符（需要转义）
JSON_CONTROL_CHARS = set(chr(i) for i in range(32))


def escape_json_string(text: str, ensure_ascii: bool = True) -> str:
    """
    转义 JSON 字符串
    
    Args:
        text: 要转义的字符串
        ensure_ascii: 是否确保输出为 ASCII（非 ASCII 转为 \\uXXXX）
        
    Returns:
        转义后的 JSON 字符串（不含引号）
        
    Example:
        >>> escape_json_string('Hello\\nWorld')
        'Hello\\\\nWorld'
    """
    result = []
    
    for char in text:
        if char in JSON_ESCAPE_CHARS:
            result.append(JSON_ESCAPE_CHARS[char])
        elif char in JSON_CONTROL_CHARS and char not in JSON_ESCAPE_CHARS:
            # 其他控制字符
            result.append(f'\\u{ord(char):04x}')
        elif ensure_ascii and ord(char) > 127:
            # 非 ASCII 字符
            result.append(f'\\u{ord(char):04x}')
        else:
            result.append(char)
    
    return ''.join(result)


def unescape_json_string(text: str) -> str:
    """
    反转义 JSON 字符串
    
    Args:
        text: JSON 转义的字符串
        
    Returns:
        反转义后的字符串
        
    Example:
        >>> unescape_json_string('Hello\\\\nWorld')
        'Hello\\nWorld'
    """
    result = []
    i = 0
    
    while i < len(text):
        if text[i] == '\\' and i + 1 < len(text):
            next_char = text[i + 1]
            
            if next_char in {'"', '\\', '/'}:
                result.append(next_char)
                i += 2
            elif next_char == 'b':
                result.append('\b')
                i += 2
            elif next_char == 'f':
                result.append('\f')
                i += 2
            elif next_char == 'n':
                result.append('\n')
                i += 2
            elif next_char == 'r':
                result.append('\r')
                i += 2
            elif next_char == 't':
                result.append('\t')
                i += 2
            elif next_char == 'u' and i + 5 < len(text):
                # Unicode 转义
                try:
                    code = int(text[i+2:i+6], 16)
                    result.append(chr(code))
                    i += 6
                except ValueError:
                    result.append(text[i])
                    i += 1
            else:
                result.append(next_char)
                i += 2
        else:
            result.append(text[i])
            i += 1
    
    return ''.join(result)


# ============================================================================
# Shell 命令转义
# ============================================================================

# Shell 特殊字符（需要转义）
SHELL_SPECIAL_CHARS = set('\\`$!&|;<>{}[]()\'"*?~# \t\n\r')


def escape_shell(text: str, style: str = 'posix') -> str:
    """
    转义 Shell 命令字符串
    
    Args:
        text: 要转义的字符串
        style: 转义风格 ('posix', 'windows', 'bash')
        
    Returns:
        转义后的字符串
        
    Example:
        >>> escape_shell('hello world')
        "'hello world'"
    """
    if not text:
        return "''"
    
    if style == 'windows':
        # Windows CMD 转义
        # 检查是否需要引号
        if not any(c in text for c in ' \t&|<>^'):
            return text
        
        # 双引号，内部特殊字符用 ^ 转义（CMD）
        result = '"'
        for char in text:
            if char in '"^':
                result += '^' + char
            else:
                result += char
        result += '"'
        return result
    
    # POSIX/Bash 风格
    # 如果字符串安全（不含特殊字符），直接返回
    if not any(c in text for c in SHELL_SPECIAL_CHARS):
        return text
    
    # 检查是否可以安全使用单引号
    if "'" not in text:
        return "'" + text + "'"
    
    # 使用双引号，转义必要字符
    result = '"'
    for char in text:
        if char in '"\\$`':
            result += '\\' + char
        else:
            result += char
    result += '"'
    return result


def escape_shell_args(args: List[str], style: str = 'posix') -> str:
    """
    转义 Shell 命令参数列表
    
    Args:
        args: 参数列表
        style: 转义风格
        
    Returns:
        转义后的命令字符串
        
    Example:
        >>> escape_shell_args(['echo', 'hello world'])
        "echo 'hello world'"
    """
    return ' '.join(escape_shell(arg, style) for arg in args)


# ============================================================================
# 正则表达式转义
# ============================================================================

# 正则表达式元字符
REGEX_SPECIAL_CHARS = set('\\.^$*+?{}[]|()')


def escape_regex(text: str) -> str:
    """
    转义正则表达式特殊字符
    
    Args:
        text: 要转义的字符串
        
    Returns:
        可安全用于正则表达式的字符串
        
    Example:
        >>> escape_regex('a.b*c')
        'a\\.b\\*c'
    """
    result = []
    for char in text:
        if char in REGEX_SPECIAL_CHARS:
            result.append('\\' + char)
        else:
            result.append(char)
    return ''.join(result)


# ============================================================================
# Glob 模式转义
# ============================================================================

# Glob 特殊字符
GLOB_SPECIAL_CHARS = set('*?[]{}')


def escape_glob(text: str) -> str:
    """
    转义 Glob 模式特殊字符
    
    Args:
        text: 要转义的字符串
        
    Returns:
        可安全用于 Glob 模式的字符串
        
    Example:
        >>> escape_glob('file*.txt')
        'file\\*.txt'
    """
    result = []
    for char in text:
        if char in GLOB_SPECIAL_CHARS:
            result.append('\\' + char)
        else:
            result.append(char)
    return ''.join(result)


# ============================================================================
# C 语言字符串转义
# ============================================================================

C_ESCAPE_CHARS: Dict[str, str] = {
    '\a': '\\a',
    '\b': '\\b',
    '\f': '\\f',
    '\n': '\\n',
    '\r': '\\r',
    '\t': '\\t',
    '\v': '\\v',
    '\\': '\\\\',
    '"': '\\"',
    "'": "\\'",
}


def escape_c_string(text: str) -> str:
    """
    转义 C 语言字符串
    
    Args:
        text: 要转义的字符串
        
    Returns:
        转义后的 C 字符串
        
    Example:
        >>> escape_c_string('Hello\\nWorld')
        'Hello\\\\nWorld'
    """
    result = []
    for char in text:
        if char in C_ESCAPE_CHARS:
            result.append(C_ESCAPE_CHARS[char])
        elif ord(char) < 32 or ord(char) > 127:
            # 使用八进制或十六进制表示
            result.append(f'\\x{ord(char):02x}')
        else:
            result.append(char)
    return ''.join(result)


def unescape_c_string(text: str) -> str:
    """
    反转义 C 语言字符串
    
    Args:
        text: C 转义的字符串
        
    Returns:
        反转义后的字符串
    """
    result = []
    i = 0
    
    while i < len(text):
        if text[i] == '\\' and i + 1 < len(text):
            next_char = text[i + 1]
            
            if next_char == 'a':
                result.append('\a')
                i += 2
            elif next_char == 'b':
                result.append('\b')
                i += 2
            elif next_char == 'f':
                result.append('\f')
                i += 2
            elif next_char == 'n':
                result.append('\n')
                i += 2
            elif next_char == 'r':
                result.append('\r')
                i += 2
            elif next_char == 't':
                result.append('\t')
                i += 2
            elif next_char == 'v':
                result.append('\v')
                i += 2
            elif next_char in {'\\', '"', "'"}:
                result.append(next_char)
                i += 2
            elif next_char == 'x' and i + 3 < len(text):
                # 十六进制
                try:
                    code = int(text[i+2:i+4], 16)
                    result.append(chr(code))
                    i += 4
                except ValueError:
                    result.append('\\x')
                    i += 2
            elif next_char in '01234567':
                # 八进制（最多 3 位）
                octal = next_char
                j = i + 2
                while j < len(text) and j < i + 4 and text[j] in '01234567':
                    octal += text[j]
                    j += 1
                try:
                    code = int(octal, 8)
                    result.append(chr(code))
                    i = j
                except ValueError:
                    result.append('\\')
                    i += 1
            else:
                result.append(next_char)
                i += 2
        else:
            result.append(text[i])
            i += 1
    
    return ''.join(result)


# ============================================================================
# SQL 字符串转义（基础版）
# ============================================================================

SQL_ESCAPE_CHARS: Dict[str, str] = {
    "'": "''",
    '\\': '\\\\',
    '\0': '\\0',
    '\n': '\\n',
    '\r': '\\r',
    '\x1a': '\\Z',  # Ctrl+Z
}


def escape_sql_string(text: str, style: str = 'standard') -> str:
    """
    转义 SQL 字符串（基础实现，仅供参考）
    
    注意：生产环境应使用数据库驱动的参数化查询，
    此函数仅供简单场景或教学使用。
    
    Args:
        text: 要转义的字符串
        style: 转义风格 ('standard', 'mysql', 'postgres')
        
    Returns:
        转义后的 SQL 字符串
        
    Example:
        >>> escape_sql_string("O'Brien")
        "O''Brien"
    """
    if style == 'mysql':
        # MySQL 风格：转义单引号为 \' 或 ''
        result = []
        for char in text:
            if char == "'":
                result.append("\\'")
            elif char in {'\\', '\0', '\n', '\r', '\x1a'}:
                result.append('\\' + char)
            else:
                result.append(char)
        return ''.join(result)
    
    elif style == 'postgres':
        # PostgreSQL 风格：单引号双写
        return text.replace("'", "''")
    
    # 标准 SQL 风格：单引号双写
    return text.replace("'", "''")


# ============================================================================
# 综合转义函数
# ============================================================================

ESCAPE_FUNCTIONS = {
    'html': escape_html,
    'xml': escape_xml,
    'url': escape_url,
    'json': escape_json_string,
    'shell': escape_shell,
    'regex': escape_regex,
    'glob': escape_glob,
    'c': escape_c_string,
    'sql': escape_sql_string,
}

UNESCAPE_FUNCTIONS = {
    'html': unescape_html,
    'xml': unescape_xml,
    'url': unescape_url,
    'json': unescape_json_string,
    'c': unescape_c_string,
}


def escape(text: str, format: str, **kwargs) -> str:
    """
    综合转义函数
    
    Args:
        text: 要转义的字符串
        format: 转义格式 ('html', 'xml', 'url', 'json', 'shell', 'regex', 'glob', 'c', 'sql')
        **kwargs: 格式特定参数
        
    Returns:
        转义后的字符串
        
    Example:
        >>> escape('<script>', 'html')
        '&lt;script&gt;'
    """
    if format not in ESCAPE_FUNCTIONS:
        raise ValueError(f"未知的转义格式: {format}")
    
    return ESCAPE_FUNCTIONS[format](text, **kwargs)


def unescape(text: str, format: str, **kwargs) -> str:
    """
    综合反转义函数
    
    Args:
        text: 要反转义的字符串
        format: 反转义格式
        **kwargs: 格式特定参数
        
    Returns:
        反转义后的字符串
        
    Example:
        >>> unescape('&lt;script&gt;', 'html')
        '<script>'
    """
    if format not in UNESCAPE_FUNCTIONS:
        raise ValueError(f"未知的反转义格式: {format}")
    
    return UNESCAPE_FUNCTIONS[format](text, **kwargs)


# ============================================================================
# 批量转义
# ============================================================================

def batch_escape(texts: List[str], format: str, **kwargs) -> List[str]:
    """
    批量转义字符串列表
    
    Args:
        texts: 字符串列表
        format: 转义格式
        **kwargs: 格式特定参数
        
    Returns:
        转义后的字符串列表
    """
    return [escape(text, format, **kwargs) for text in texts]


def batch_unescape(texts: List[str], format: str, **kwargs) -> List[str]:
    """
    批量反转义字符串列表
    
    Args:
        texts: 字符串列表
        format: 反转义格式
        **kwargs: 格式特定参数
        
    Returns:
        反转义后的字符串列表
    """
    return [unescape(text, format, **kwargs) for text in texts]


# ============================================================================
# 检测函数
# ============================================================================

def needs_escape(text: str, format: str) -> bool:
    """
    检测字符串是否需要转义
    
    Args:
        text: 要检测的字符串
        format: 格式
        
    Returns:
        是否需要转义
    """
    if format == 'html':
        return any(c in text for c in HTML_ESCAPE_CHARS)
    elif format == 'xml':
        return any(c in text for c in XML_ESCAPE_CHARS)
    elif format == 'url':
        return any(c not in URL_SAFE_CHARS for c in text)
    elif format == 'json':
        return any(c in JSON_ESCAPE_CHARS or ord(c) < 32 for c in text)
    elif format == 'shell':
        return any(c in SHELL_SPECIAL_CHARS for c in text)
    elif format == 'regex':
        return any(c in REGEX_SPECIAL_CHARS for c in text)
    elif format == 'glob':
        return any(c in GLOB_SPECIAL_CHARS for c in text)
    elif format == 'c':
        return any(c in C_ESCAPE_CHARS or ord(c) < 32 or ord(c) > 127 for c in text)
    elif format == 'sql':
        return "'" in text
    
    return False


def detect_escapes(text: str) -> List[str]:
    """
    检测字符串中使用的转义格式
    
    Args:
        text: 包含可能的转义字符的字符串
        
    Returns:
        检测到的转义格式列表
    """
    detected = []
    
    # HTML 实体
    if re.search(r'&(?:amp|lt|gt|quot|apos|nbsp|#\d+|#x[0-9a-fA-F]+);', text):
        detected.append('html')
    
    # URL 编码
    if re.search(r'%[0-9A-Fa-f]{2}', text) or '+' in text:
        detected.append('url')
    
    # JSON 转义
    if re.search(r'\\(?:["\\/bfnrt]|u[0-9a-fA-F]{4})', text):
        detected.append('json')
    
    # C 转义
    if re.search(r'\\(?:[abfnrtv\\"\'x]|x[0-9a-fA-F]{2}|[0-7]{1,3})', text):
        detected.append('c')
    
    return detected


# ============================================================================
# 常用字符集转义
# ============================================================================

def escape_for_attribute(text: str, attr_type: str = 'html') -> str:
    """
    转义 HTML/XML 属性值
    
    Args:
        text: 属性值
        attr_type: 属性类型 ('html', 'xml')
        
    Returns:
        转义后的属性值
    """
    if attr_type == 'xml':
        return escape_xml(text, is_attribute=True)
    return escape_html(text)


def escape_for_css(text: str) -> str:
    """
    转义 CSS 字符串
    
    Args:
        text: CSS 内容
        
    Returns:
        转义后的 CSS 字符串
    """
    result = []
    for char in text:
        if char in {'<', '>', '&', "'", '"', '\\'}:
            result.append('\\' + char)
        else:
            result.append(char)
    return ''.join(result)


def escape_for_javascript(text: str) -> str:
    """
    转义 JavaScript 字符串
    
    Args:
        text: JavaScript 内容
        
    Returns:
        转义后的 JavaScript 字符串
    """
    result = []
    for char in text:
        if char in {'\\', "'", '"', '\n', '\r', '\t'}:
            if char == '\n':
                result.append('\\n')
            elif char == '\r':
                result.append('\\r')
            elif char == '\t':
                result.append('\\t')
            else:
                result.append('\\' + char)
        elif ord(char) < 32:
            result.append(f'\\x{ord(char):02x}')
        else:
            result.append(char)
    return ''.join(result)


if __name__ == "__main__":
    # 演示用法
    print("=== 转义工具演示 ===\n")
    
    # HTML 转义
    html_input = '<script>alert("XSS")</script>'
    print(f"HTML 转义:")
    print(f"  输入: {html_input}")
    print(f"  输出: {escape_html(html_input)}")
    print(f"  反转义: {unescape_html(escape_html(html_input))}")
    print()
    
    # URL 编码
    url_input = '你好世界/测试?key=value'
    print(f"URL 编码:")
    print(f"  输入: {url_input}")
    print(f"  输出: {escape_url(url_input, plus_space=False)}")
    print(f"  反转义: {unescape_url(escape_url(url_input, plus_space=False), plus_space=False)}")
    print()
    
    # URL 查询字符串
    params = {'name': '张三', 'age': '25', 'tags': ['开发', '测试']}
    print(f"URL 查询字符串:")
    print(f"  参数: {params}")
    print(f"  输出: {escape_url_query(params)}")
    print(f"  解析: {unescape_url_query(escape_url_query(params))}")
    print()
    
    # JSON 转义
    json_input = 'Hello\nWorld\t"测试"'
    print(f"JSON 转义:")
    print(f"  输入: {repr(json_input)}")
    print(f"  输出: {escape_json_string(json_input)}")
    print(f"  反转义: {repr(unescape_json_string(escape_json_string(json_input)))}")
    print()
    
    # Shell 转义
    shell_input = 'hello world $HOME'
    print(f"Shell 转义:")
    print(f"  输入: {shell_input}")
    print(f"  输出: {escape_shell(shell_input)}")
    print()
    
    # 正则表达式转义
    regex_input = 'a.b*c[d]e'
    print(f"正则表达式转义:")
    print(f"  输入: {regex_input}")
    print(f"  输出: {escape_regex(regex_input)}")
    print()
    
    # 检测转义格式
    test_text = '&lt;div&gt;Hello%20World&#64;'
    print(f"检测转义格式:")
    print(f"  文本: {test_text}")
    print(f"  检测结果: {detect_escapes(test_text)}")
    print()
    
    # 综合转义
    print("综合转义演示:")
    for format in ['html', 'url', 'json', 'regex', 'shell']:
        test = '<test>&"special"'
        print(f"  {format}: {escape(test, format)}")