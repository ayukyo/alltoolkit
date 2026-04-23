"""
slug_utils - URL友好slug生成工具
===================================

零依赖的slug生成工具库，支持多语言、自定义分隔符、大小写转换等功能。

功能特性：
- slugify: 将字符串转换为URL友好的slug
- 自定义分隔符（默认连字符）
- 大小写转换选项
- 去除特殊字符
- 数字保留选项
- 最大长度限制
- 自定义替换规则
- 多语言支持（ASCII音译）
- 重复分隔符合并

使用示例：
    >>> from slug_utils import slugify
    >>> slugify("Hello World!")
    'hello-world'
    >>> slugify("你好世界", separator="_")
    'ni-hao-shi-jie'
"""

import re
import unicodedata
from typing import Optional, Dict, List, Union, Callable


# 默认保留字符（字母、数字、连字符）
DEFAULT_PATTERN = r'[^a-zA-Z0-9\-]+'

# 中文拼音映射表（常用字，去除重复键）
PINYIN_MAP = {
    '你': 'ni', '好': 'hao', '世': 'shi', '界': 'jie',
    '中': 'zhong', '国': 'guo', '人': 'ren', '大': 'da',
    '小': 'xiao', '天': 'tian', '地': 'di', '日': 'ri',
    '月': 'yue', '年': 'nian', '新': 'xin', '闻': 'wen',
    '学': 'xue', '习': 'xi', '工': 'gong', '作': 'zuo',
    '生': 'sheng', '活': 'huo', '家': 'jia', '庭': 'ting',
    '朋': 'peng', '友': 'you', '爱': 'ai', '情': 'qing',
    '心': 'xin', '思': 'si', '想': 'xiang', '念': 'nian',
    '时': 'shi', '间': 'jian', '今': 'jin', '明': 'ming',
    '昨': 'zuo', '前': 'qian', '后': 'hou',
    '上': 'shang', '下': 'xia', '左': 'zuo', '右': 'you',
    '东': 'dong', '西': 'xi', '南': 'nan', '北': 'bei',
    '春': 'chun', '夏': 'xia', '秋': 'qiu', '冬': 'dong',
    '风': 'feng', '雨': 'yu', '雪': 'xue', '云': 'yun',
    '山': 'shan', '水': 'shui', '火': 'huo', '木': 'mu',
    '金': 'jin', '土': 'tu', '花': 'hua', '草': 'cao',
    '树': 'shu', '林': 'lin', '森': 'sen', '海': 'hai',
    '河': 'he', '湖': 'hu', '江': 'jiang', '鱼': 'yu',
    '鸟': 'niao', '马': 'ma', '牛': 'niu', '羊': 'yang',
    '猪': 'zhu', '狗': 'gou', '猫': 'mao', '兔': 'tu',
    '龙': 'long', '虎': 'hu', '蛇': 'she', '鼠': 'shu',
    '鸡': 'ji', '蛋': 'dan', '肉': 'rou', '菜': 'cai',
    '果': 'guo', '茶': 'cha', '酒': 'jiu', '饭': 'fan',
    '书': 'shu', '笔': 'bi', '纸': 'zhi', '画': 'hua',
    '音': 'yin', '乐': 'le', '歌': 'ge', '舞': 'wu',
    '电': 'dian', '脑': 'nao', '手': 'shou', '机': 'ji',
    '网': 'wang', '络': 'luo', '信': 'xin', '息': 'xi',
    '科': 'ke', '技': 'ji', '发': 'fa', '展': 'zhan',
    '经': 'jing', '济': 'ji', '商': 'shang', '业': 'ye',
    '公': 'gong', '司': 'si', '企': 'qi', '事': 'shi',
    '单': 'dan', '位': 'wei', '部': 'bu',
    '门': 'men', '组': 'zu', '织': 'zhi', '团': 'tuan',
    '队': 'dui', '员': 'yuan', '长': 'zhang', '老': 'lao',
    '师': 'shi', '先': 'xian',
    '女': 'nv', '男': 'nan', '孩': 'hai', '童': 'tong',
    '子': 'zi', '父': 'fu', '母': 'mu', '兄': 'xiong',
    '弟': 'di', '姐': 'jie', '妹': 'mei', '爷': 'ye',
    '奶': 'nai', '叔': 'shu', '姨': 'yi', '姑': 'gu',
    '舅': 'jiu', '表': 'biao', '堂': 'tang', '亲': 'qin',
    '戚': 'qi', '邻': 'lin', '居': 'ju', '客': 'ke',
    '主': 'zhu', '仆': 'pu', '王': 'wang', '皇': 'huang',
    '帝': 'di', '将': 'jiang', '军': 'jun', '兵': 'bing',
    '士': 'shi', '官': 'guan', '民': 'min',
    '众': 'zhong', '群': 'qun', '族': 'zu',
    '城': 'cheng', '市': 'shi', '镇': 'zhen', '村': 'cun',
    '乡': 'xiang', '街': 'jie', '道': 'dao', '路': 'lu',
    '桥': 'qiao', '楼': 'lou', '房': 'fang', '屋': 'wu',
    '窗': 'chuang', '墙': 'qiang', '壁': 'bi',
    '板': 'ban', '顶': 'ding', '底': 'di',
    '智': 'zhi', '能': 'neng',
}

# 日文假名转罗马音映射
HIRAGANA_MAP = {
    'あ': 'a', 'い': 'i', 'う': 'u', 'え': 'e', 'お': 'o',
    'か': 'ka', 'き': 'ki', 'く': 'ku', 'け': 'ke', 'こ': 'ko',
    'さ': 'sa', 'し': 'shi', 'す': 'su', 'せ': 'se', 'そ': 'so',
    'た': 'ta', 'ち': 'chi', 'つ': 'tsu', 'て': 'te', 'と': 'to',
    'な': 'na', 'に': 'ni', 'ぬ': 'nu', 'ね': 'ne', 'の': 'no',
    'は': 'ha', 'ひ': 'hi', 'ふ': 'fu', 'へ': 'he', 'ほ': 'ho',
    'ま': 'ma', 'み': 'mi', 'む': 'mu', 'め': 'me', 'も': 'mo',
    'や': 'ya', 'ゆ': 'yu', 'よ': 'yo',
    'ら': 'ra', 'り': 'ri', 'る': 'ru', 'れ': 're', 'ろ': 'ro',
    'わ': 'wa', 'を': 'wo', 'ん': 'n',
    'が': 'ga', 'ぎ': 'gi', 'ぐ': 'gu', 'げ': 'ge', 'ご': 'go',
    'ざ': 'za', 'じ': 'ji', 'ず': 'zu', 'ぜ': 'ze', 'ぞ': 'zo',
    'だ': 'da', 'ぢ': 'ji', 'づ': 'zu', 'で': 'de', 'ど': 'do',
    'ば': 'ba', 'び': 'bi', 'ぶ': 'bu', 'べ': 'be', 'ぼ': 'bo',
    'ぱ': 'pa', 'ぴ': 'pi', 'ぷ': 'pu', 'ぺ': 'pe', 'ぽ': 'po',
}

KATAKANA_MAP = {
    'ア': 'a', 'イ': 'i', 'ウ': 'u', 'エ': 'e', 'オ': 'o',
    'カ': 'ka', 'キ': 'ki', 'ク': 'ku', 'ケ': 'ke', 'コ': 'ko',
    'サ': 'sa', 'シ': 'shi', 'ス': 'su', 'セ': 'se', 'ソ': 'so',
    'タ': 'ta', 'チ': 'chi', 'ツ': 'tsu', 'テ': 'te', 'ト': 'to',
    'ナ': 'na', 'ニ': 'ni', 'ヌ': 'nu', 'ネ': 'ne', 'ノ': 'no',
    'ハ': 'ha', 'ヒ': 'hi', 'フ': 'fu', 'ヘ': 'he', 'ホ': 'ho',
    'マ': 'ma', 'ミ': 'mi', 'ム': 'mu', 'メ': 'me', 'モ': 'mo',
    'ヤ': 'ya', 'ユ': 'yu', 'ヨ': 'yo',
    'ラ': 'ra', 'リ': 'ri', 'ル': 'ru', 'レ': 're', 'ロ': 'ro',
    'ワ': 'wa', 'ヲ': 'wo', 'ン': 'n',
    'ガ': 'ga', 'ギ': 'gi', 'グ': 'gu', 'ゲ': 'ge', 'ゴ': 'go',
    'ザ': 'za', 'ジ': 'ji', 'ズ': 'zu', 'ゼ': 'ze', 'ゾ': 'zo',
    'ダ': 'da', 'ヂ': 'ji', 'ヅ': 'zu', 'デ': 'de', 'ド': 'do',
    'バ': 'ba', 'ビ': 'bi', 'ブ': 'bu', 'ベ': 'be', 'ボ': 'bo',
    'パ': 'pa', 'ピ': 'pi', 'プ': 'pu', 'ペ': 'pe', 'ポ': 'po',
}

# 韩文元音和辅音映射（简化版）
KOREAN_MAP = {
    '가': 'ga', '나': 'na', '다': 'da', '라': 'ra', '마': 'ma',
    '바': 'ba', '사': 'sa', '아': 'a', '자': 'ja', '차': 'cha',
    '카': 'ka', '타': 'ta', '파': 'pa', '하': 'ha',
    '한': 'han', '국': 'guk', '안': 'an', '녕': 'nyeong',
}


def _transliterate_char(char: str) -> str:
    """
    将单个字符转换为ASCII字符。
    
    Args:
        char: 要转换的字符
        
    Returns:
        转换后的ASCII字符串
    """
    # 优先使用自定义映射
    if char in PINYIN_MAP:
        return PINYIN_MAP[char]
    if char in HIRAGANA_MAP:
        return HIRAGANA_MAP[char]
    if char in KATAKANA_MAP:
        return KATAKANA_MAP[char]
    if char in KOREAN_MAP:
        return KOREAN_MAP[char]
    
    # 尝试NFKD分解
    try:
        decomposed = unicodedata.normalize('NFKD', char)
        # 过滤掉组合字符（音标等）
        result = ''.join(
            c for c in decomposed 
            if not unicodedata.combining(c) and ord(c) < 128
        )
        if result:
            return result
    except (ValueError, TypeError):
        pass
    
    # 无法转换则返回空
    return ''


def _transliterate(text: str, keep_untranslated: bool = False, separator: str = '-') -> str:
    """
    将Unicode文本音译为ASCII字符。
    
    Args:
        text: 要转换的文本
        keep_untranslated: 是否保留无法音译的字符
        separator: 音译字符之间使用的分隔符
        
    Returns:
        音译后的字符串
    """
    result = []
    last_was_multi_char_translit = False  # 上一个是否是多字符音译
    
    for char in text:
        if ord(char) < 128:
            # ASCII字符：如果之前是多字符音译，添加分隔符
            if last_was_multi_char_translit and result and result[-1] != separator:
                result.append(separator)
            result.append(char)
            last_was_multi_char_translit = False
        else:
            transliterated = _transliterate_char(char)
            if transliterated:
                # 判断是否是多字符音译（如拼音）
                is_multi_char = len(transliterated) > 1
                
                if is_multi_char:
                    # 多字符音译：如果之前不是分隔符，添加分隔符
                    if result and result[-1] != separator and result[-1] not in ' \t\n\r-_.':
                        result.append(separator)
                    result.append(transliterated)
                    last_was_multi_char_translit = True
                else:
                    # 单字符音译（如重音字符）：直接添加，不加分隔符
                    result.append(transliterated)
                    last_was_multi_char_translit = False
            elif keep_untranslated:
                result.append(char)
                last_was_multi_char_translit = True
    
    return ''.join(result)


def slugify(
    text: str,
    separator: str = '-',
    lowercase: bool = True,
    keep_numbers: bool = True,
    max_length: Optional[int] = None,
    replacements: Optional[Dict[str, str]] = None,
    keep_untranslated: bool = False,
    word_boundary: bool = False,
    custom_pattern: Optional[str] = None,
    trim_separator: bool = True,
    merge_separators: bool = True,
) -> str:
    """
    将字符串转换为URL友好的slug。
    
    Args:
        text: 要转换的字符串
        separator: 分隔符，默认为连字符
        lowercase: 是否转换为小写，默认为True
        keep_numbers: 是否保留数字，默认为True
        max_length: 最大长度限制，None表示无限制
        replacements: 自定义替换规则，例如 {'&': 'and', '@': 'at'}
        keep_untranslated: 是否保留无法音译的非ASCII字符
        word_boundary: 是否在单词边界处添加分隔符
        custom_pattern: 自定义保留字符的正则表达式模式
        trim_separator: 是否去除首尾的分隔符
        merge_separators: 是否合并连续的分隔符
        
    Returns:
        URL友好的slug字符串
        
    Examples:
        >>> slugify("Hello World!")
        'hello-world'
        >>> slugify("你好世界")
        'ni-hao-shi-jie'
        >>> slugify("Hello   World", separator="_")
        'hello_world'
        >>> slugify("Product #123", keep_numbers=True)
        'product-123'
        >>> slugify("Café & Restaurant", replacements={'&': 'and'})
        'cafe-and-restaurant'
    """
    if not text:
        return ''
    
    # 应用自定义替换
    if replacements:
        for old, new in replacements.items():
            text = text.replace(old, f' {new} ')
    
    # 音译非ASCII字符
    text = _transliterate(text, keep_untranslated, separator)
    
    # 大小写转换
    if lowercase:
        text = text.lower()
    
    # 构建保留字符模式
    if custom_pattern:
        pattern = custom_pattern
    elif keep_numbers:
        pattern = r'[^a-z0-9]' if lowercase else r'[^a-zA-Z0-9]'
    else:
        pattern = r'[^a-z]' if lowercase else r'[^a-zA-Z]'
    
    # 替换非保留字符为分隔符
    slug = re.sub(pattern, separator, text)
    
    # 合并连续的分隔符
    if merge_separators and separator:
        escaped_sep = re.escape(separator)
        slug = re.sub(f'{escaped_sep}+', separator, slug)
    
    # 去除首尾分隔符
    if trim_separator and separator:
        slug = slug.strip(separator)
    
    # 限制最大长度
    if max_length is not None:
        if max_length <= 0:
            return ''
        # 尝试在分隔符处截断，避免截断单词
        if len(slug) > max_length:
            # 找到最后一个分隔符的位置
            truncated = slug[:max_length]
            last_sep = truncated.rfind(separator)
            if separator and last_sep > max_length // 2:
                slug = truncated[:last_sep]
            else:
                slug = truncated.rstrip(separator) if separator else truncated
    
    return slug


def slugify_unique(
    text: str,
    existing: Optional[List[str]] = None,
    separator: str = '-',
    max_attempts: int = 100,
    **kwargs
) -> str:
    """
    生成唯一的slug，自动添加数字后缀避免冲突。
    
    Args:
        text: 要转换的字符串
        existing: 已存在的slug列表
        separator: 分隔符
        max_attempts: 最大尝试次数
        **kwargs: 传递给slugify的其他参数
        
    Returns:
        唯一的slug字符串
        
    Examples:
        >>> slugify_unique("Hello World", existing=["hello-world"])
        'hello-world-2'
        >>> slugify_unique("Hello World", existing=["hello-world", "hello-world-2"])
        'hello-world-3'
    """
    existing = existing or []
    existing_set = set(existing)
    
    base_slug = slugify(text, separator=separator, **kwargs)
    
    if base_slug not in existing_set:
        return base_slug
    
    # 尝试添加数字后缀
    for i in range(2, max_attempts + 2):
        candidate = f"{base_slug}{separator}{i}"
        if candidate not in existing_set:
            return candidate
    
    # 如果所有尝试都失败，使用时间戳
    import time
    return f"{base_slug}{separator}{int(time.time())}"


def generate_slug(
    text: str,
    prefix: str = '',
    suffix: str = '',
    **kwargs
) -> str:
    """
    生成带有前缀和后缀的slug。
    
    Args:
        text: 要转换的字符串
        prefix: 前缀
        suffix: 后缀
        **kwargs: 传递给slugify的其他参数
        
    Returns:
        带前缀和后缀的slug
        
    Examples:
        >>> generate_slug("Hello World", prefix="blog", suffix="2024")
        'blog-hello-world-2024'
    """
    slug = slugify(text, **kwargs)
    separator = kwargs.get('separator', '-')
    
    parts = []
    if prefix:
        parts.append(slugify(prefix, **kwargs))
    parts.append(slug)
    if suffix:
        parts.append(slugify(suffix, **kwargs))
    
    return separator.join(parts)


def is_valid_slug(
    slug: str,
    allow_uppercase: bool = False,
    allow_numbers: bool = True,
    separator: str = '-',
    min_length: int = 1,
    max_length: int = 2083,  # URL最大长度限制
) -> bool:
    """
    验证字符串是否为有效的slug。
    
    Args:
        slug: 要验证的字符串
        allow_uppercase: 是否允许大写字母
        allow_numbers: 是否允许数字
        separator: 允许的分隔符
        min_length: 最小长度
        max_length: 最大长度
        
    Returns:
        是否为有效的slug
        
    Examples:
        >>> is_valid_slug("hello-world")
        True
        >>> is_valid_slug("hello_world", separator="_")
        True
        >>> is_valid_slug("Hello World")
        False
    """
    if not slug:
        return False
    
    if len(slug) < min_length or len(slug) > max_length:
        return False
    
    # 检查是否以分隔符开头或结尾
    if slug.startswith(separator) or slug.endswith(separator):
        return False
    
    # 构建验证模式
    if allow_uppercase:
        char_class = 'a-zA-Z'
    else:
        char_class = 'a-z'
    
    if allow_numbers:
        char_class += '0-9'
    
    escaped_sep = re.escape(separator)
    pattern = f'^[{char_class}{escaped_sep}]+$'
    
    return bool(re.match(pattern, slug))


def unslugify(
    slug: str,
    separator: str = '-',
    title_case: bool = False,
    space_replacement: str = ' ',
) -> str:
    """
    将slug转换回可读的字符串。
    
    Args:
        slug: slug字符串
        separator: 分隔符
        title_case: 是否转换为标题格式（首字母大写）
        space_replacement: 用于替换分隔符的字符
        
    Returns:
        可读的字符串
        
    Examples:
        >>> unslugify("hello-world")
        'hello world'
        >>> unslugify("hello-world", title_case=True)
        'Hello World'
        >>> unslugify("hello_world", separator="_")
        'hello world'
    """
    if not slug:
        return ''
    
    text = slug.replace(separator, space_replacement)
    
    if title_case:
        text = text.title()
    
    return text


def slug_range(
    text: str,
    start: int,
    end: int,
    separator: str = '-',
    **kwargs
) -> List[str]:
    """
    生成一系列带数字后缀的slug。
    
    Args:
        text: 基础字符串
        start: 起始数字
        end: 结束数字（包含）
        separator: 分隔符
        **kwargs: 传递给slugify的其他参数
        
    Returns:
        slug列表
        
    Examples:
        >>> slug_range("Chapter", 1, 3)
        ['chapter-1', 'chapter-2', 'chapter-3']
    """
    base = slugify(text, separator=separator, **kwargs)
    return [f"{base}{separator}{i}" for i in range(start, end + 1)]


def smart_slugify(
    text: str,
    **kwargs
) -> str:
    """
    智能slug生成，自动处理特殊场景。
    
    自动处理：
    - HTML实体解码
    - 多种引号类型
    - 常见符号替换
    - 表情符号移除
    
    Args:
        text: 要转换的字符串
        **kwargs: 传递给slugify的其他参数
        
    Returns:
        智能生成的slug
        
    Examples:
        >>> smart_slugify("What's Up?!")
        'whats-up'
        >>> smart_slugify("Hello™ World®")
        'hello-tm-world-r'
    """
    if not text:
        return ''
    
    # 预处理：移除撇号和引号
    for char in ["'", "'", '"', '"', '`']:
        text = text.replace(char, '')
    
    # 常见符号替换
    smart_replacements = {
        '&': 'and',
        '@': 'at',
        '+': 'plus',
        '=': 'equals',
        '%': 'percent',
        '#': 'number',
        '$': 'dollar',
        '€': 'euro',
        '£': 'pound',
        '¥': 'yen',
        '©': 'c',
        '®': 'r',
        '™': 'tm',
        '°': 'deg',
        '×': 'x',
        '÷': 'div',
        '±': 'plus-minus',
        '≈': 'approx',
        '≠': 'not-equal',
        '≤': 'le',
        '≥': 'ge',
        '√': 'sqrt',
        '∞': 'infinity',
        'π': 'pi',
        'α': 'alpha',
        'β': 'beta',
        'γ': 'gamma',
        'δ': 'delta',
        'ε': 'epsilon',
    }
    
    # 合并用户自定义替换
    user_replacements = kwargs.pop('replacements', None) or {}
    replacements = {**smart_replacements, **user_replacements}
    
    return slugify(text, replacements=replacements, **kwargs)


def count_slug_words(slug: str, separator: str = '-') -> int:
    """
    统计slug中的单词数量。
    
    Args:
        slug: slug字符串
        separator: 分隔符
        
    Returns:
        单词数量
        
    Examples:
        >>> count_slug_words("hello-world-foo")
        3
        >>> count_slug_words("single")
        1
    """
    if not slug:
        return 0
    
    # 去除首尾分隔符后分割
    clean_slug = slug.strip(separator)
    if not clean_slug:
        return 0
    
    return len(clean_slug.split(separator))


def truncate_slug(
    slug: str,
    max_length: int,
    separator: str = '-',
    preserve_words: bool = True,
) -> str:
    """
    截断slug到指定长度。
    
    Args:
        slug: 原始slug
        max_length: 最大长度
        separator: 分隔符
        preserve_words: 是否尽量保留完整单词
        
    Returns:
        截断后的slug
        
    Examples:
        >>> truncate_slug("hello-world-from-python", 15)
        'hello-world-from'
        >>> truncate_slug("hello-world-from-python", 10, preserve_words=False)
        'hello-worl'
    """
    if not slug or len(slug) <= max_length:
        return slug
    
    if not preserve_words:
        return slug[:max_length].rstrip(separator)
    
    # 在最后一个分隔符处截断
    truncated = slug[:max_length]
    last_sep = truncated.rfind(separator)
    
    if last_sep > 0:
        return truncated[:last_sep]
    
    return truncated.rstrip(separator)


def compare_slugs(
    slug1: str,
    slug2: str,
    separator: str = '-',
) -> Dict[str, any]:
    """
    比较两个slug的相似度。
    
    Args:
        slug1: 第一个slug
        slug2: 第二个slug
        separator: 分隔符
        
    Returns:
        包含比较结果的字典：
        - exact_match: 是否完全匹配
        - word_overlap: 重叠单词数
        - similarity: 相似度（0-1）
        - common_words: 共同单词列表
        - unique_to_first: 只在第一个中的单词
        - unique_to_second: 只在第二个中的单词
        
    Examples:
        >>> compare_slugs("hello-world", "hello-python")
        {'exact_match': False, 'word_overlap': 1, 'similarity': 0.5, ...}
    """
    words1 = set(slug1.split(separator)) if slug1 else set()
    words2 = set(slug2.split(separator)) if slug2 else set()
    
    common = words1 & words2
    unique1 = words1 - words2
    unique2 = words2 - words1
    
    total_words = len(words1 | words2)
    similarity = len(common) / total_words if total_words > 0 else 1.0
    
    return {
        'exact_match': slug1 == slug2,
        'word_overlap': len(common),
        'similarity': round(similarity, 4),
        'common_words': sorted(list(common)),
        'unique_to_first': sorted(list(unique1)),
        'unique_to_second': sorted(list(unique2)),
    }


def batch_slugify(
    texts: List[str],
    unique: bool = False,
    separator: str = '-',
    **kwargs
) -> List[str]:
    """
    批量生成slug。
    
    Args:
        texts: 字符串列表
        unique: 是否保证slug唯一
        separator: 分隔符
        **kwargs: 传递给slugify的其他参数
        
    Returns:
        slug列表
        
    Examples:
        >>> batch_slugify(["Hello World", "Hello World", "Foo Bar"])
        ['hello-world', 'hello-world', 'foo-bar']
        >>> batch_slugify(["Hello World", "Hello World", "Foo Bar"], unique=True)
        ['hello-world', 'hello-world-2', 'foo-bar']
    """
    if not unique:
        return [slugify(text, separator=separator, **kwargs) for text in texts]
    
    result = []
    existing = []
    for text in texts:
        slug = slugify_unique(text, existing=existing, separator=separator, **kwargs)
        result.append(slug)
        existing.append(slug)
    
    return result


# 版本信息
__version__ = '1.0.0'
__author__ = 'AllToolkit'
__all__ = [
    'slugify',
    'slugify_unique',
    'generate_slug',
    'is_valid_slug',
    'unslugify',
    'slug_range',
    'smart_slugify',
    'count_slug_words',
    'truncate_slug',
    'compare_slugs',
    'batch_slugify',
]