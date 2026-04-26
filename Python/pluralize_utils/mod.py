"""
pluralize_utils - 英文单词单复数转换工具

提供英文单词的单数/复数形式转换功能，支持规则变化和不规则变化。
零外部依赖，纯 Python 实现。

功能:
- 单数转复数 (singular_to_plural)
- 复数转单数 (plural_to_singular)
- 判断是否为复数 (is_plural)
- 获取单词的单复数形式 (get_plural_form)
- 批量转换 (batch_pluralize, batch_singularize)
"""

import re
from typing import Dict, List, Tuple, Optional, Set


# 不规则变化单词映射
IRREGULAR_PLURALS: Dict[str, str] = {
    # 人称代词
    'i': 'we',
    'me': 'us',
    'my': 'our',
    'mine': 'ours',
    'you': 'you',
    'your': 'your',
    'yours': 'yours',
    'he': 'they',
    'him': 'them',
    'his': 'their',
    'she': 'they',
    'her': 'them',
    'hers': 'theirs',
    'it': 'they',
    'its': 'their',
    'this': 'these',
    'that': 'those',
    
    # 常见不规则名词
    'man': 'men',
    'woman': 'women',
    'child': 'children',
    'person': 'people',
    'foot': 'feet',
    'tooth': 'teeth',
    'goose': 'geese',
    'mouse': 'mice',
    'louse': 'lice',
    'ox': 'oxen',
    'brother': 'brothers',  # 可以是 brethren (古语)
    'die': 'dice',
    'penny': 'pence',
    
    # -f/-fe 结尾变 -ves
    'leaf': 'leaves',
    'loaf': 'loaves',
    'knife': 'knives',
    'wife': 'wives',
    'life': 'lives',
    'wolf': 'wolves',
    'calf': 'calves',
    'half': 'halves',
    'self': 'selves',
    'shelf': 'shelves',
    'thief': 'thieves',
    
    # 拉丁/希腊源词
    'analysis': 'analyses',
    'basis': 'bases',
    'crisis': 'crises',
    'diagnosis': 'diagnoses',
    'hypothesis': 'hypotheses',
    'oasis': 'oases',
    'parenthesis': 'parentheses',
    'thesis': 'theses',
    'phenomenon': 'phenomena',
    'criterion': 'criteria',
    'datum': 'data',
    'medium': 'media',
    'bacterium': 'bacteria',
    'curriculum': 'curricula',
    'appendix': 'appendices',
    'index': 'indices',
    'matrix': 'matrices',
    'vertex': 'vertices',
    'axis': 'axes',
    'appendix': 'appendices',
    'focus': 'foci',
    'fungus': 'fungi',
    'nucleus': 'nuclei',
    'radius': 'radii',
    'stimulus': 'stimuli',
    'syllabus': 'syllabi',
    'alumnus': 'alumni',
    'corpus': 'corpora',
    'genus': 'genera',
    'opus': 'opera',
    
    # 法语源词
    'beau': 'beaux',
    'bureau': 'bureaux',
    'tableau': 'tableaux',
    'chateau': 'chateaux',
    'trousseau': 'trousseaux',
    
    # 单复数同形
    'sheep': 'sheep',
    'deer': 'deer',
    'fish': 'fish',
    'species': 'species',
    'series': 'series',
    'moose': 'moose',
    'swine': 'swine',
    'aircraft': 'aircraft',
    'spacecraft': 'spacecraft',
    'hovercraft': 'hovercraft',
    'salmon': 'salmon',
    'trout': 'trout',
    'bison': 'bison',
    'shrimp': 'shrimp',
    'means': 'means',
    'offspring': 'offspring',
    'headquarters': 'headquarters',
    
    # 无复数形式或复数特殊
    'information': 'information',
    'knowledge': 'knowledge',
    'advice': 'advice',
    'furniture': 'furniture',
    'equipment': 'equipment',
    'luggage': 'luggage',
    'traffic': 'traffic',
    'homework': 'homework',
    'news': 'news',
    'mathematics': 'mathematics',
    'physics': 'physics',
    'economics': 'economics',
    'politics': 'politics',
    'athletics': 'athletics',
    'measles': 'measles',
    'mumps': 'mumps',
    'billiards': 'billiards',
    'darts': 'darts',
    'tactics': 'tactics',
}

# 反向映射：复数 -> 单数
IRREGULAR_SINGULARS: Dict[str, str] = {v: k for k, v in IRREGULAR_PLURALS.items()}

# 单复数同形的单词
UNCOUNTABLE_WORDS: Set[str] = {
    'sheep', 'deer', 'fish', 'species', 'series', 'moose', 'swine',
    'aircraft', 'spacecraft', 'hovercraft', 'salmon', 'trout', 'bison',
    'shrimp', 'means', 'offspring', 'headquarters', 'information',
    'knowledge', 'advice', 'furniture', 'equipment', 'luggage', 'traffic',
    'homework', 'news', 'mathematics', 'physics', 'economics', 'politics',
    'athletics', 'measles', 'mumps', 'billiards', 'darts', 'tactics',
    'rice', 'wheat', 'corn', 'sugar', 'salt', 'pepper', 'water', 'tea',
    'coffee', 'milk', 'juice', 'butter', 'cheese', 'bread', 'hair',
    'grass', 'dust', 'sand', 'air', 'love', 'hate', 'peace', 'war',
    'music', 'art', 'happiness', 'sadness', 'anger', 'courage', 'luck',
}

# 以 -s 结尾但为单数的单词
SINGULAR_S_WORDS: Set[str] = {
    'news', 'politics', 'mathematics', 'physics', 'economics',
    'athletics', 'measles', 'mumps', 'billiards', 'darts', 'tactics',
    'acoustics', 'aerobics', 'linguistics', 'classics', 'gymnastics',
    'electronics', 'mechanics', 'thermodynamics', 'optics', 'ethics',
    'aesthetics', 'metaphysics', 'ceramics', 'diabetes', 'rabies',
    'rickets', 'shingles', 'syphilis', 'series', 'species', 'means',
    'lens', 'bus', 'gas', 'chaos', 'boss', 'glass', 'class', 'pass',
    'mass', 'kiss', 'cross', 'loss', 'boss', 'miss', 'fuss', 'plus',
    'status', 'census', 'virus', 'genius', 'radius', 'stimulus',
    'hippopotamus', 'octopus', 'platypus', 'syllabus', 'nucleus',
    'focus', 'fungus', 'cactus', 'lotus', 'bonus', 'corpus', 'thrombus',
    'atlas', 'alias', 'venus', 'campus', 'chorus', 'circus', 'citrus',
    'plus', 'sinus', 'termite', 'antelope',
}


def singular_to_plural(word: str, count: Optional[int] = None) -> str:
    """
    将英文单词从单数转换为复数形式。
    
    参数:
        word: 要转换的单词（单数形式）
        count: 可选的数量，如果为1则返回原词
        
    返回:
        复数形式的单词
        
    示例:
        >>> singular_to_plural('cat')
        'cats'
        >>> singular_to_plural('box')
        'boxes'
        >>> singular_to_plural('child')
        'children'
        >>> singular_to_plural('cat', count=1)
        'cat'
    """
    if not word:
        return word
    
    # 如果提供了 count 且为 1，返回原词
    if count is not None and count == 1:
        return word
    
    original_word = word
    word_lower = word.lower()
    
    # 检查不可数名词
    if word_lower in UNCOUNTABLE_WORDS:
        return word
    
    # 检查不规则变化
    if word_lower in IRREGULAR_PLURALS:
        plural = IRREGULAR_PLURALS[word_lower]
        return _preserve_case(original_word, plural)
    
    # 处理缩写和数字
    # 缩写：包含数字的词（如 MP3）或已知缩写词（如 PDF, UFO）
    abbreviations = {'pdf', 'ufo', 'nato', 'unesco', 'jpeg', 'mpeg', 'gif', 'html', 'css', 'js', 'api', 'url', 'http', 'https', 'sql', 'cpu', 'gpu', 'ram', 'rom', 'usb', 'wifi', 'bluetooth'}
    if re.match(r'.*\d+$', word) or word_lower in abbreviations:
        return word + 's'
    
    # 处理连字符复合词（如 brother-in-law -> brothers-in-law）
    if '-' in word:
        parts = word.split('-')
        # 只将主要词变为复数（通常是第一个词）
        if len(parts) >= 2:
            # 主要词通常是第一个词（brother-in-law -> brothers-in-law）
            # 特殊情况：passer-by -> passers-by（倒数第二个）
            first_lower = parts[0].lower()
            if first_lower in ('passer', 'runner', 'looker', 'hanger'):
                main_index = 0
            else:
                # 默认：第一个词是主要词
                main_index = 0
            plural_main = singular_to_plural(parts[main_index])
            parts[main_index] = plural_main
            return '-'.join(parts)
    
    # 应用规则变化
    
    # -is -> -es (axis -> axes, analysis -> analyses) - 已在不规则变化中处理
    
    # -on -> -a (phenomenon -> phenomena, criterion -> criteria) - 已在不规则变化中处理
    
    # -um -> -a (datum -> data, medium -> media, curriculum -> curricula)
    if word_lower.endswith('um') and word_lower not in ('sum', 'gum', 'drum', 'hum', 'mum'):
        plural = word_lower[:-2] + 'a'
        return _preserve_case(original_word, plural)
    
    # -a -> -ae (formula -> formulae, antenna -> antennae, alga -> algae)
    if word_lower.endswith('a') and word_lower not in ('area', 'era', 'idea', 'tea', 'sea'):
        # 检查是否是已知的拉丁词
        if word_lower in ('formula', 'antenna', 'alga', 'nebula', 'vertebra', 'uvula', 'scapula', 'fibula', 'tibia', 'clavicle'):
            plural = word_lower + 'e'
            return _preserve_case(original_word, plural)
    
    # -us -> -i (alumnus -> alumni, focus -> foci) - 大部分在不规则变化中
    
    # -ex/-ix -> -ices (index -> indices, appendix -> appendices, matrix -> matrices)
    if word_lower.endswith('ex') or word_lower.endswith('ix'):
        plural = word_lower[:-2] + 'ices'
        return _preserve_case(original_word, plural)
    
    # -y 规则
    if word_lower.endswith('y'):
        # 辅音 + y -> -ies
        if len(word) > 1 and word[-2] not in 'aeiouAEIOU':
            plural = word_lower[:-1] + 'ies'
            return _preserve_case(original_word, plural)
        # 元音 + y -> -ys
        else:
            plural = word_lower + 's'
            return _preserve_case(original_word, plural)
    
    # -o 规则
    if word_lower.endswith('o'):
        # 常见 -oes 结尾的词
        oes_words = {'potato', 'tomato', 'hero', 'torpedo', 'veto', 'echo', 'embargo', 'mosquito', 'tornado', 'volcano', 'buffalo'}
        if word_lower in oes_words:
            plural = word_lower + 'es'
            return _preserve_case(original_word, plural)
        # 缩写或专有名词
        if len(word) <= 2 or word.isupper():
            plural = word_lower + 's'
            return _preserve_case(original_word, plural)
        # 其他 -o 结尾通常加 -s
        plural = word_lower + 's'
        return _preserve_case(original_word, plural)
    
    # -f/-fe -> -ves 规则 - 大部分在不规则变化中，这里处理其他情况
    if word_lower.endswith('fe') and word_lower not in ('safe', 'cafe', 'wife', 'knife', 'life'):
        # 大多数 -fe 结尾只加 s
        plural = word_lower + 's'
        return _preserve_case(original_word, plural)
    if word_lower.endswith('f') and word_lower not in ('chef', 'chief', 'roof', 'belief', 'brief', 'grief', 'proof', 'calf', 'half', 'knife', 'life', 'leaf', 'loaf', 'self', 'shelf', 'thief', 'wolf'):
        plural = word_lower + 's'
        return _preserve_case(original_word, plural)
    
    # -s, -x, -z, -ch, -sh -> -es
    if word_lower.endswith(('s', 'x', 'z', 'ch', 'sh', 'ss')):
        # -z -> -zes 或 -zzes
        if word_lower.endswith('z'):
            if word_lower.endswith('zz'):
                plural = word_lower + 'es'
            else:
                plural = word_lower + 'zes'
            return _preserve_case(original_word, plural)
        plural = word_lower + 'es'
        return _preserve_case(original_word, plural)
    
    # 默认情况：加 -s
    plural = word_lower + 's'
    return _preserve_case(original_word, plural)


def plural_to_singular(word: str) -> str:
    """
    将英文单词从复数转换为单数形式。
    
    参数:
        word: 要转换的单词（复数形式）
        
    返回:
        单数形式的单词
        
    示例:
        >>> plural_to_singular('cats')
        'cat'
        >>> plural_to_singular('boxes')
        'box'
        >>> plural_to_singular('children')
        'child'
    """
    if not word:
        return word
    
    original_word = word
    word_lower = word.lower()
    
    # 检查不可数名词
    if word_lower in UNCOUNTABLE_WORDS:
        return word
    
    # 检查不规则变化（反向映射）
    if word_lower in IRREGULAR_SINGULARS:
        singular = IRREGULAR_SINGULARS[word_lower]
        return _preserve_case(original_word, singular)
    
    # 单复数同形的词
    if word_lower in IRREGULAR_PLURALS and IRREGULAR_PLURALS[word_lower] == word_lower:
        return word
    
    # 处理连字符复合词
    if '-' in word:
        parts = word.split('-')
        if len(parts) >= 2:
            # 主要词通常是第一个词（brothers-in-law -> brother-in-law）
            first_lower = parts[0].lower()
            if first_lower in ('passers', 'runners', 'lookers', 'hangers'):
                main_index = 0
            else:
                # 默认：第一个词是主要词
                main_index = 0
            singular_main = plural_to_singular(parts[main_index])
            parts[main_index] = singular_main
            return '-'.join(parts)
    
    # 应用逆向规则变化
    
    # -ices -> -ex/-ix (indices -> index, appendices -> appendix, matrices -> matrix)
    if word_lower.endswith('ices'):
        base = word[:-4]
        # 根据语境判断，默认 -ex
        return base + 'ex'
    
    # -ae -> -a (formulae -> formula, antennae -> antenna)
    if word_lower.endswith('ae'):
        return word[:-1]
    
    # -a -> -um (data -> datum, media -> medium, curricula -> curriculum)
    if word_lower.endswith('a') and len(word) > 2:
        # 检查常见拉丁词
        latin_a_words = {
            'data': 'datum',
            'media': 'medium',
            'curricula': 'curriculum',
            'bacteria': 'bacterium',
            'criteria': 'criterion',
            'phenomena': 'phenomenon',
        }
        if word_lower in latin_a_words:
            return _preserve_case(original_word, latin_a_words[word_lower])
    
    # -i -> -us (alumni -> alumnus, foci -> focus)
    if word_lower.endswith('i'):
        latin_i_words = {
            'alumni': 'alumnus',
            'foci': 'focus',
            'fungi': 'fungus',
            'nuclei': 'nucleus',
            'radii': 'radius',
            'stimuli': 'stimulus',
            'syllabi': 'syllabus',
        }
        if word_lower in latin_i_words:
            return _preserve_case(original_word, latin_i_words[word_lower])
        return word[:-1] + 'us'
    
    # -esces -> -esc (某些特殊情况)
    
    # -ves -> -f/-fe (wives -> wife, leaves -> leaf)
    if word_lower.endswith('ves'):
        f_words = {
            'wives': 'wife',
            'lives': 'life',
            'knives': 'knife',
            'leaves': 'leaf',
            'loaves': 'loaf',
            'wolves': 'wolf',
            'calves': 'calf',
            'halves': 'half',
            'selves': 'self',
            'shelves': 'shelf',
            'thieves': 'thief',
        }
        if word_lower in f_words:
            return _preserve_case(original_word, f_words[word_lower])
        # 默认情况
        return word[:-3] + 'f'
    
    # -ies -> -y (cities -> city, stories -> story)
    if word_lower.endswith('ies'):
        return word[:-3] + 'y'
    
    # -oes -> -o (potatoes -> potato, tomatoes -> tomato)
    if word_lower.endswith('oes'):
        oes_sing = {
            'potatoes': 'potato',
            'tomatoes': 'tomato',
            'heroes': 'hero',
            'torpedoes': 'torpedo',
            'vetoes': 'veto',
            'echoes': 'echo',
            'embargoes': 'embargo',
            'mosquitoes': 'mosquito',
            'tornadoes': 'tornado',
            'volcanoes': 'volcano',
            'buffaloes': 'buffalo',
        }
        if word_lower in oes_sing:
            return _preserve_case(original_word, oes_sing[word_lower])
    
    # -es -> 原词 (boxes -> box, churches -> church)
    if word_lower.endswith('es'):
        # 检查 -sses -> -ss (classes -> class)
        if word_lower.endswith('sses'):
            return word[:-2]
        # -ses -> -s (buses -> bus, gases -> gas)
        if word_lower.endswith('ses') and not word_lower.endswith('sses'):
            # 特殊处理：去掉 es
            return word[:-2]
        # -xes -> -x
        if word_lower.endswith('xes'):
            return word[:-2]
        # -ches -> -ch
        if word_lower.endswith('ches'):
            return word[:-2]
        # -shes -> -sh
        if word_lower.endswith('shes'):
            return word[:-2]
        # -zes -> -z / -zz
        if word_lower.endswith('zzes'):
            return word[:-3] + 'z'
        if word_lower.endswith('zes'):
            return word[:-2]
        # -oes 已在上面处理
        # 其他 -es 结尾，去掉 -es
        # 但要小心不要误处理只是 -s 结尾的词
    
    # -s -> 去掉 (cats -> cat, dogs -> dog)
    if word_lower.endswith('s') and not word_lower.endswith('ss'):
        return word[:-1]
    
    # 已经是单数或无法确定
    return word


def is_plural(word: str) -> bool:
    """
    判断单词是否为复数形式。
    
    参数:
        word: 要判断的单词
        
    返回:
        True 如果是复数，False 如果是单数
        
    示例:
        >>> is_plural('cats')
        True
        >>> is_plural('cat')
        False
        >>> is_plural('sheep')  # 单复数同形
        False
    """
    if not word:
        return False
    
    word_lower = word.lower()
    
    # 不可数名词不被视为复数
    if word_lower in UNCOUNTABLE_WORDS:
        return False
    
    # 单复数同形的词
    if word_lower in ('sheep', 'deer', 'fish', 'species', 'series', 'moose', 'swine', 'aircraft', 'salmon', 'trout', 'bison', 'shrimp', 'means', 'offspring'):
        return False
    
    # 检查是否在不规则复数列表中（作为复数形式）
    if word_lower in IRREGULAR_SINGULARS:
        return True
    
    # 检查是否在不规则单数列表中（作为单数形式）
    if word_lower in IRREGULAR_PLURALS:
        return False
    
    # 以 -s 结尾但为单数的词
    if word_lower in SINGULAR_S_WORDS:
        return False
    
    # 常见复数后缀
    plural_endings = ('s', 'es', 'ies', 'ves', 'ae', 'i', 'a')
    
    # -a 结尾可能是拉丁复数
    if word_lower.endswith('a') and word_lower not in ('area', 'era', 'idea', 'tea', 'sea'):
        latin_plural_a = ('data', 'media', 'curricula', 'bacteria', 'criteria', 'phenomena', 'antennae', 'formulae', 'nebulae', 'algae', 'vertebrae')
        if word_lower in latin_plural_a:
            return True
    
    # -i 结尾可能是拉丁复数
    if word_lower.endswith('i'):
        latin_plural_i = ('alumni', 'foci', 'fungi', 'nuclei', 'radii', 'stimuli', 'syllabi', 'cacti', 'nucleoli')
        if word_lower in latin_plural_i:
            return True
    
    # -ae 结尾
    if word_lower.endswith('ae'):
        return True
    
    # -ies 结尾（city -> cities）
    if word_lower.endswith('ies'):
        return True
    
    # -ves 结尾（wife -> wives）
    if word_lower.endswith('ves'):
        ves_words = ('wives', 'lives', 'knives', 'leaves', 'loaves', 'wolves', 'calves', 'halves', 'selves', 'shelves', 'thieves')
        if word_lower in ves_words:
            return True
    
    # 简单规则：以 -s 结尾
    if word_lower.endswith('s'):
        return True
    
    return False


def get_plural_form(word: str, count: int = 2) -> str:
    """
    根据数量返回单词的正确形式。
    
    参数:
        word: 单词（单数或复数形式）
        count: 数量
        
    返回:
        根据数量返回单数或复数形式
        
    示例:
        >>> get_plural_form('cat', 1)
        'cat'
        >>> get_plural_form('cat', 2)
        'cats'
        >>> get_plural_form('cats', 1)
        'cat'
    """
    if count == 1:
        # 需要单数形式
        if is_plural(word):
            return plural_to_singular(word)
        return word
    else:
        # 需要复数形式
        if is_plural(word):
            return word
        return singular_to_plural(word)


def batch_pluralize(words: List[str]) -> List[str]:
    """
    批量将单词转换为复数形式。
    
    参数:
        words: 单词列表
        
    返回:
        复数形式的单词列表
        
    示例:
        >>> batch_pluralize(['cat', 'dog', 'box'])
        ['cats', 'dogs', 'boxes']
    """
    return [singular_to_plural(word) for word in words]


def batch_singularize(words: List[str]) -> List[str]:
    """
    批量将单词转换为单数形式。
    
    参数:
        words: 单词列表
        
    返回:
        单数形式的单词列表
        
    示例:
        >>> batch_singularize(['cats', 'dogs', 'boxes'])
        ['cat', 'dog', 'box']
    """
    return [plural_to_singular(word) for word in words]


def _preserve_case(original: str, result: str) -> str:
    """
    保持原始单词的大小写格式。
    
    参数:
        original: 原始单词
        result: 转换结果（小写或已处理）
        
    返回:
        保持原格式的结果
    """
    if not original or not result:
        return result
    
    # 全大写
    if original.isupper():
        return result.upper()
    
    # 首字母大写（其他小写）
    if original[0].isupper() and (len(original) == 1 or original[1:].islower()):
        return result[0].upper() + result[1:] if len(result) > 0 else result
    
    # 标题格式（每个单词首字母大写）
    if original.istitle():
        return result.title()
    
    # 其他情况保持原样（保持result的当前格式）
    return result


def pluralize_word(word: str, count: Optional[int] = None) -> str:
    """
    智能判断并转换单词形式（singular_to_plural 的别名）。
    
    参数:
        word: 要转换的单词
        count: 可选的数量
        
    返回:
        复数形式的单词
    """
    return singular_to_plural(word, count)


def singularize_word(word: str) -> str:
    """
    智能判断并转换单词形式（plural_to_singular 的别名）。
    
    参数:
        word: 要转换的单词
        
    返回:
        单数形式的单词
    """
    return plural_to_singular(word)


def get_article(word: str, count: int = 1) -> str:
    """
    获取适合单词的冠词。
    
    参数:
        word: 单词
        count: 数量
        
    返回:
        冠词 ('a', 'an', 或 '')
        
    示例:
        >>> get_article('cat', 1)
        'a'
        >>> get_article('apple', 1)
        'an'
        >>> get_article('cat', 2)
        ''
    """
    if count != 1:
        return ''
    
    word_lower = word.lower()
    if word_lower[0] in 'aeiou':
        return 'an'
    return 'a'


def format_count(word: str, count: int, include_article: bool = True) -> str:
    """
    格式化数量和单词的组合。
    
    参数:
        word: 单词
        count: 数量
        include_article: 是否在数量为1时包含冠词
        
    返回:
        格式化的字符串
        
    示例:
        >>> format_count('cat', 1)
        'a cat'
        >>> format_count('cat', 2)
        '2 cats'
        >>> format_count('apple', 1)
        'an apple'
    """
    if count == 1:
        if include_article:
            article = get_article(word, count)
            return f"{article} {word}" if article else word
        return word
    
    plural = singular_to_plural(word) if not is_plural(word) else word
    return f"{count} {plural}"


# 导出公共接口
__all__ = [
    'singular_to_plural',
    'plural_to_singular',
    'is_plural',
    'get_plural_form',
    'batch_pluralize',
    'batch_singularize',
    'pluralize_word',
    'singularize_word',
    'get_article',
    'format_count',
    'IRREGULAR_PLURALS',
    'IRREGULAR_SINGULARS',
    'UNCOUNTABLE_WORDS',
    'SINGULAR_S_WORDS',
]