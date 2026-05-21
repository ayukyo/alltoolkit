#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Homoglyph Utils - Unicode 同形字检测工具模块
============================================
提供 Unicode 同形字（视觉相似字符）检测、转换和分析功能。
零外部依赖，仅使用 Python 标准库。

主要功能:
- 同形字检测（西里尔、希腊、全角等混淆字符）
- 字符正规化（统一到标准形式）
- 同形字攻击风险评估
- 字符串相似度分析（视觉相似性）
- 同形字映射查询
- 批量文本扫描
- 域名安全检查

应用场景:
- IDN 同形字攻击检测
- 钓鱼域名识别
- 用户名安全验证
- 文本欺诈检测
- 密码强度分析

作者: AllToolkit
日期: 2026-05-21
"""

from typing import Dict, List, Tuple, Set, Optional
from dataclasses import dataclass
from enum import Enum
import unicodedata


class HomoglyphCategory(Enum):
    """同形字类别"""
    LATIN_CYRILLIC = "latin_cyrillic"      # 拉丁-西里尔混淆
    LATIN_GREEK = "latin_greek"            # 拉丁-希腊混淆
    FULLWIDTH = "fullwidth"                # 全角-半角混淆
    LOOKALIKE = "lookalike"                # 视觉相似字符
    INVISIBLE = "invisible"                # 不可见字符
    CONFUSABLE = "confusable"              # 通用混淆字符


@dataclass
class HomoglyphMatch:
    """同形字匹配结果"""
    position: int                # 字符位置
    original_char: str           # 原字符
    original_codepoint: int      # 原字符码点
    canonical_char: str          # 规范字符（建议替换为）
    canonical_codepoint: int     # 规范字符码点
    category: HomoglyphCategory  # 类别
    description: str             # 描述
    risk_level: int              # 风险等级 (1-5)
    
    def __str__(self) -> str:
        return (f"位置 {self.position}: '{self.original_char}' (U+{self.original_codepoint:04X}) "
                f"→ '{self.canonical_char}' (U+{self.canonical_codepoint:04X}) [{self.category.value}]")


@dataclass
class HomoglyphScanResult:
    """同形字扫描结果"""
    text: str                              # 原始文本
    normalized: str                        # 规范化文本
    matches: List[HomoglyphMatch]          # 匹配结果
    risk_score: int                        # 总风险分数 (0-100)
    risk_level: str                        # 风险等级描述
    
    @property
    def has_homoglyphs(self) -> bool:
        """是否包含同形字"""
        return len(self.matches) > 0
    
    @property
    def match_count(self) -> int:
        """匹配数量"""
        return len(self.matches)
    
    def get_by_category(self, category: HomoglyphCategory) -> List[HomoglyphMatch]:
        """按类别筛选"""
        return [m for m in self.matches if m.category == category]
    
    def get_high_risk(self, min_level: int = 4) -> List[HomoglyphMatch]:
        """获取高风险匹配"""
        return [m for m in self.matches if m.risk_level >= min_level]


# ==================== 同形字映射表 ====================

# 西里尔字母同形字 (最常见的安全威胁)
CYRILLIC_HOMOGLYPHS: Dict[str, str] = {
    # 西里尔 -> 拉丁
    '\u0430': 'a',   # CYRILLIC SMALL LETTER A -> LATIN SMALL LETTER A
    '\u0410': 'A',   # CYRILLIC CAPITAL LETTER A -> LATIN CAPITAL LETTER A
    '\u0435': 'e',   # CYRILLIC SMALL LETTER IE -> LATIN SMALL LETTER E
    '\u0415': 'E',   # CYRILLIC CAPITAL LETTER IE -> LATIN CAPITAL LETTER E
    '\u043E': 'o',   # CYRILLIC SMALL LETTER O -> LATIN SMALL LETTER O
    '\u041E': 'O',   # CYRILLIC CAPITAL LETTER O -> LATIN CAPITAL LETTER O
    '\u0440': 'p',   # CYRILLIC SMALL LETTER ER -> LATIN SMALL LETTER P
    '\u0420': 'P',   # CYRILLIC CAPITAL LETTER ER -> LATIN CAPITAL LETTER P
    '\u0441': 'c',   # CYRILLIC SMALL LETTER ES -> LATIN SMALL LETTER C
    '\u0421': 'C',   # CYRILLIC CAPITAL LETTER ES -> LATIN CAPITAL LETTER C
    '\u0443': 'y',   # CYRILLIC SMALL LETTER U -> LATIN SMALL LETTER Y
    '\u0423': 'Y',   # CYRILLIC CAPITAL LETTER U -> LATIN CAPITAL LETTER Y (similar)
    '\u0445': 'x',   # CYRILLIC SMALL LETTER HA -> LATIN SMALL LETTER X
    '\u0425': 'X',   # CYRILLIC CAPITAL LETTER HA -> LATIN CAPITAL LETTER X
    '\u0456': 'i',   # CYRILLIC SMALL LETTER BYELORUSSIAN-UKRAINIAN I -> LATIN SMALL LETTER I
    '\u0406': 'I',   # CYRILLIC CAPITAL LETTER BYELORUSSIAN-UKRAINIAN I -> LATIN CAPITAL LETTER I
    '\u0457': 'ï',   # CYRILLIC SMALL LETTER YI
    '\u0407': 'Ï',   # CYRILLIC CAPITAL LETTER YI
    '\u0458': 'j',   # CYRILLIC SMALL LETTER JE -> LATIN SMALL LETTER J
    '\u0408': 'J',   # CYRILLIC CAPITAL LETTER JE -> LATIN CAPITAL LETTER J
    '\u04BB': 'h',   # CYRILLIC SMALL LETTER SHHA -> LATIN SMALL LETTER H
    '\u04BA': 'H',   # CYRILLIC CAPITAL LETTER SHHA -> LATIN CAPITAL LETTER H
    '\u0432': 'B',   # CYRILLIC SMALL LETTER VE -> LATIN CAPITAL LETTER B (similar)
    '\u0412': 'B',   # CYRILLIC CAPITAL LETTER VE -> LATIN CAPITAL LETTER B
    '\u043C': 'M',   # CYRILLIC SMALL LETTER EM -> similar to small m but looks like M
    '\u041C': 'M',   # CYRILLIC CAPITAL LETTER EM -> LATIN CAPITAL LETTER M
    '\u043D': 'H',   # CYRILLIC SMALL LETTER EN -> similar to H
    '\u041D': 'H',   # CYRILLIC CAPITAL LETTER EN -> LATIN CAPITAL LETTER H
    '\u043A': 'K',   # CYRILLIC SMALL LETTER KA -> LATIN SMALL LETTER K (similar)
    '\u041A': 'K',   # CYRILLIC CAPITAL LETTER KA -> LATIN CAPITAL LETTER K
    '\u0442': 'T',   # CYRILLIC SMALL LETTER TE -> LATIN CAPITAL LETTER T
    '\u0422': 'T',   # CYRILLIC CAPITAL LETTER TE -> LATIN CAPITAL LETTER T
}

# 希腊字母同形字
GREEK_HOMOGLYPHS: Dict[str, str] = {
    # 希腊 -> 拉丁
    '\u03B1': 'a',   # GREEK SMALL LETTER ALPHA -> LATIN SMALL LETTER A
    '\u0391': 'A',   # GREEK CAPITAL LETTER ALPHA -> LATIN CAPITAL LETTER A
    '\u03B5': 'e',   # GREEK SMALL LETTER EPSILON -> LATIN SMALL LETTER E
    '\u0395': 'E',   # GREEK CAPITAL LETTER EPSILON -> LATIN CAPITAL LETTER E
    '\u03BF': 'o',   # GREEK SMALL LETTER OMICRON -> LATIN SMALL LETTER O
    '\u039F': 'O',   # GREEK CAPITAL LETTER OMICRON -> LATIN CAPITAL LETTER O
    '\u03C1': 'p',   # GREEK SMALL LETTER RHO -> LATIN SMALL LETTER P
    '\u03A1': 'P',   # GREEK CAPITAL LETTER RHO -> LATIN CAPITAL LETTER P
    '\u03C4': 't',   # GREEK SMALL LETTER TAU -> LATIN SMALL LETTER T
    '\u03A4': 'T',   # GREEK CAPITAL LETTER TAU -> LATIN CAPITAL LETTER T
    '\u03B9': 'i',   # GREEK SMALL LETTER IOTA -> LATIN SMALL LETTER I
    '\u0399': 'I',   # GREEK CAPITAL LETTER IOTA -> LATIN CAPITAL LETTER I
    '\u03BA': 'K',   # GREEK SMALL LETTER KAPPA -> LATIN SMALL LETTER K (similar)
    '\u039A': 'K',   # GREEK CAPITAL LETTER KAPPA -> LATIN CAPITAL LETTER K
    '\u03BD': 'v',   # GREEK SMALL LETTER NU -> LATIN SMALL LETTER V
    '\u039D': 'N',   # GREEK CAPITAL LETTER NU -> LATIN CAPITAL LETTER N
    '\u03C5': 'u',   # GREEK SMALL LETTER UPSILON -> LATIN SMALL LETTER U
    '\u03A5': 'Y',   # GREEK CAPITAL LETTER UPSILON -> LATIN CAPITAL LETTER Y
    '\u03C7': 'x',   # GREEK SMALL LETTER CHI -> LATIN SMALL LETTER X
    '\u03A7': 'X',   # GREEK CAPITAL LETTER CHI -> LATIN CAPITAL LETTER X
}

# 全角字符
FULLWIDTH_HOMOGLYPHS: Dict[str, str] = {
    # 全角 -> 半角
    '\uFF01': '!',   # ！ -> !
    '\uFF02': '"',   # ＂ -> "
    '\uFF03': '#',   # ＃ -> #
    '\uFF04': '$',   # ＄ -> $
    '\uFF05': '%',   # ％ -> %
    '\uFF06': '&',   # ＆ -> &
    '\uFF07': "'",   # ＇ -> '
    '\uFF08': '(',   # （ -> (
    '\uFF09': ')',   # ） -> )
    '\uFF0A': '*',   # ＊ -> *
    '\uFF0B': '+',   # ＋ -> +
    '\uFF0C': ',',   # ， -> ,
    '\uFF0D': '-',   # － -> -
    '\uFF0E': '.',   # ． -> .
    '\uFF0F': '/',   # ／ -> /
    '\uFF10': '0',   # ０ -> 0
    '\uFF11': '1',   # １ -> 1
    '\uFF12': '2',   # ２ -> 2
    '\uFF13': '3',   # ３ -> 3
    '\uFF14': '4',   # ４ -> 4
    '\uFF15': '5',   # ５ -> 5
    '\uFF16': '6',   # ６ -> 6
    '\uFF17': '7',   # ７ -> 7
    '\uFF18': '8',   # ８ -> 8
    '\uFF19': '9',   # ９ -> 9
    '\uFF1A': ':',   # ： -> :
    '\uFF1B': ';',   # ； -> ;
    '\uFF1C': '<',   # ＜ -> <
    '\uFF1D': '=',   # ＝ -> =
    '\uFF1E': '>',   # ＞ -> >
    '\uFF1F': '?',   # ？ -> ?
    '\uFF20': '@',   # ＠ -> @
    '\uFF21': 'A',   # Ａ -> A
    '\uFF22': 'B',   # Ｂ -> B
    '\uFF23': 'C',   # Ｃ -> C
    '\uFF24': 'D',   # Ｄ -> D
    '\uFF25': 'E',   # Ｅ -> E
    '\uFF26': 'F',   # Ｆ -> F
    '\uFF27': 'G',   # Ｇ -> G
    '\uFF28': 'H',   # Ｈ -> H
    '\uFF29': 'I',   # Ｉ -> I
    '\uFF2A': 'J',   # Ｊ -> J
    '\uFF2B': 'K',   # Ｋ -> K
    '\uFF2C': 'L',   # Ｌ -> L
    '\uFF2D': 'M',   # Ｍ -> M
    '\uFF2E': 'N',   # Ｎ -> N
    '\uFF2F': 'O',   # Ｏ -> O
    '\uFF30': 'P',   # Ｐ -> P
    '\uFF31': 'Q',   # Ｑ -> Q
    '\uFF32': 'R',   # Ｒ -> R
    '\uFF33': 'S',   # Ｓ -> S
    '\uFF34': 'T',   # Ｔ -> T
    '\uFF35': 'U',   # Ｕ -> U
    '\uFF36': 'V',   # Ｖ -> V
    '\uFF37': 'W',   # Ｗ -> W
    '\uFF38': 'X',   # Ｘ -> X
    '\uFF39': 'Y',   # Ｙ -> Y
    '\uFF3A': 'Z',   # Ｚ -> Z
    '\uFF3B': '[',   # ［ -> [
    '\uFF3C': '\\',  # ＼ -> \
    '\uFF3D': ']',   # ］ -> ]
    '\uFF3E': '^',   # ＾ -> ^
    '\uFF3F': '_',   # ＿ -> _
    '\uFF40': '`',   # ｀ -> `
    '\uFF41': 'a',   # ａ -> a
    '\uFF42': 'b',   # ｂ -> b
    '\uFF43': 'c',   # ｃ -> c
    '\uFF44': 'd',   # ｄ -> d
    '\uFF45': 'e',   # ｅ -> e
    '\uFF46': 'f',   # ｆ -> f
    '\uFF47': 'g',   # ｇ -> g
    '\uFF48': 'h',   # ｈ -> h
    '\uFF49': 'i',   # ｉ -> i
    '\uFF4A': 'j',   # ｊ -> j
    '\uFF4B': 'k',   # ｋ -> k
    '\uFF4C': 'l',   # ｌ -> l
    '\uFF4D': 'm',   # ｍ -> m
    '\uFF4E': 'n',   # ｎ -> n
    '\uFF4F': 'o',   # ｏ -> o
    '\uFF50': 'p',   # ｐ -> p
    '\uFF51': 'q',   # ｑ -> q
    '\uFF52': 'r',   # ｒ -> r
    '\uFF53': 's',   # ｓ -> s
    '\uFF54': 't',   # ｔ -> t
    '\uFF55': 'u',   # ｕ -> u
    '\uFF56': 'v',   # ｖ -> v
    '\uFF57': 'w',   # ｗ -> w
    '\uFF58': 'x',   # ｘ -> x
    '\uFF59': 'y',   # ｙ -> y
    '\uFF5A': 'z',   # ｚ -> z
}

# 其他视觉相似字符
LOOKALIKE_HOMOGLYPHS: Dict[str, str] = {
    '\u0131': 'i',   # LATIN SMALL LETTER DOTLESS I -> i
    '\u0307': '',    # COMBINING DOT ABOVE (单独使用)
    '\u006C\u0307': 'i',  # l + 组合点 -> i
    '\u0127': 'h',   # LATIN SMALL LETTER H WITH STROKE -> h
    '\u0126': 'H',   # LATIN CAPITAL LETTER H WITH STROKE -> H
    '\u0269': 'i',   # LATIN SMALL LETTER IOTA -> i
    '\u0196': 'I',   # LATIN CAPITAL LETTER IOTA -> I
    '\u051D': 'w',   # CYRILLIC SMALL LETTER WE -> w
    '\u051C': 'W',   # CYRILLIC CAPITAL LETTER WE -> W
    '\u0AB0': 'r',   # GUJARATI LETTER RA -> r (similar)
    '\u2010': '-',   # HYPHEN -> -
    '\u2011': '-',   # NON-BREAKING HYPHEN -> -
    '\u2012': '-',   # FIGURE DASH -> -
    '\u2013': '-',   # EN DASH -> -
    '\u2014': '-',   # EM DASH -> -
    '\u2212': '-',   # MINUS SIGN -> -
    '\uFF0D': '-',   # FULLWIDTH HYPHEN-MINUS -> -
    '\u00A0': ' ',   # NO-BREAK SPACE -> space
    '\u2000': ' ',   # EN QUAD -> space
    '\u2001': ' ',   # EM QUAD -> space
    '\u2002': ' ',   # EN SPACE -> space
    '\u2003': ' ',   # EM SPACE -> space
    '\u2004': ' ',   # THREE-PER-EM SPACE -> space
    '\u2005': ' ',   # FOUR-PER-EM SPACE -> space
    '\u2006': ' ',   # SIX-PER-EM SPACE -> space
    '\u2007': ' ',   # FIGURE SPACE -> space
    '\u2008': ' ',   # PUNCTUATION SPACE -> space
    '\u2009': ' ',   # THIN SPACE -> space
    '\u200A': ' ',   # HAIR SPACE -> space
    '\u202F': ' ',   # NARROW NO-BREAK SPACE -> space
    '\u205F': ' ',   # MEDIUM MATHEMATICAL SPACE -> space
    '\u3000': ' ',   # IDEOGRAPHIC SPACE -> space
    '\u200B': '',    # ZERO WIDTH SPACE (移除)
    '\u200C': '',    # ZERO WIDTH NON-JOINER (移除)
    '\u200D': '',    # ZERO WIDTH JOINER (移除)
    '\uFEFF': '',    # ZERO WIDTH NO-BREAK SPACE (移除)
    '\u00AD': '',    # SOFT HYPHEN (移除)
    '\u034F': '',    # COMBINING GRAPHEME JOINER (移除)
    '\u180E': '',    # MONGOLIAN VOWEL SEPARATOR (移除)
    '\u2060': '',    # WORD JOINER (移除)
    '\u2061': '',    # FUNCTION APPLICATION (移除)
    '\u2062': '',    # INVISIBLE TIMES (移除)
    '\u2063': '',    # INVISIBLE SEPARATOR (移除)
    '\u2064': '',    # INVISIBLE PLUS (移除)
    '\u206A': '',    # INHIBIT SYMMETRIC SWAPPING (移除)
    '\u206B': '',    # ACTIVATE SYMMETRIC SWAPPING (移除)
    '\u206C': '',    # INHIBIT ARABIC FORM SHAPING (移除)
    '\u206D': '',    # ACTIVATE ARABIC FORM SHAPING (移除)
    '\u206E': '',    # NATIONAL DIGIT SHAPES (移除)
    '\u206F': '',    # NOMINAL DIGIT SHAPES (移除)
}

# 零和 O 混淆
ZERO_O_HOMOGLYPHS: Dict[str, str] = {
    '\u0030': '0',   # DIGIT ZERO (标准)
    '\u004F': 'O',   # LATIN CAPITAL LETTER O (标准)
    '\u006F': 'o',   # LATIN SMALL LETTER O (标准)
    '\u041E': 'O',   # CYRILLIC CAPITAL LETTER O
    '\u043E': 'o',   # CYRILLIC SMALL LETTER O
    '\u039F': 'O',   # GREEK CAPITAL LETTER OMICRON
    '\u03BF': 'o',   # GREEK SMALL LETTER OMICRON
    '\uFF10': '0',   # FULLWIDTH DIGIT ZERO
    '\uFF2F': 'O',   # FULLWIDTH LATIN CAPITAL LETTER O
    '\uFF4F': 'o',   # FULLWIDTH LATIN SMALL LETTER O
    '\u01A0': 'O',   # LATIN CAPITAL LETTER O WITH HORN
    '\u01A1': 'o',   # LATIN SMALL LETTER O WITH HORN
    '\u0222': 'O',   # LATIN CAPITAL LETTER O WITH DOUBLE ACUTE
    '\u0223': 'o',   # LATIN SMALL LETTER O WITH DOUBLE ACUTE
    '\u1ECC': 'O',   # LATIN CAPITAL LETTER O WITH DOT BELOW
    '\u1ECD': 'o',   # LATIN SMALL LETTER O WITH DOT BELOW
    '\u1ECE': 'O',   # LATIN CAPITAL LETTER O WITH HOOK ABOVE
    '\u1ECF': 'o',   # LATIN SMALL LETTER O WITH HOOK ABOVE
    '\u1ED0': 'O',   # LATIN CAPITAL LETTER O WITH CIRCUMFLEX AND ACUTE
    '\u1ED1': 'o',   # LATIN SMALL LETTER O WITH CIRCUMFLEX AND ACUTE
    '\u1ED2': 'O',   # LATIN CAPITAL LETTER O WITH CIRCUMFLEX AND GRAVE
    '\u1ED3': 'o',   # LATIN SMALL LETTER O WITH CIRCUMFLEX AND GRAVE
    '\u1ED4': 'O',   # LATIN CAPITAL LETTER O WITH CIRCUMFLEX AND HOOK ABOVE
    '\u1ED5': 'o',   # LATIN SMALL LETTER O WITH CIRCUMFLEX AND HOOK ABOVE
    '\u1ED6': 'O',   # LATIN CAPITAL LETTER O WITH CIRCUMFLEX AND TILDE
    '\u1ED7': 'o',   # LATIN SMALL LETTER O WITH CIRCUMFLEX AND TILDE
    '\u1ED8': 'O',   # LATIN CAPITAL LETTER O WITH CIRCUMFLEX AND DOT BELOW
    '\u1ED9': 'o',   # LATIN SMALL LETTER O WITH CIRCUMFLEX AND DOT BELOW
    '\u1EDA': 'O',   # LATIN CAPITAL LETTER O WITH HORN AND ACUTE
    '\u1EDB': 'o',   # LATIN SMALL LETTER O WITH HORN AND ACUTE
    '\u1EDC': 'O',   # LATIN CAPITAL LETTER O WITH HORN AND GRAVE
    '\u1EDD': 'o',   # LATIN SMALL LETTER O WITH HORN AND GRAVE
    '\u1EDE': 'O',   # LATIN CAPITAL LETTER O WITH HORN AND HOOK ABOVE
    '\u1EDF': 'o',   # LATIN SMALL LETTER O WITH HORN AND HOOK ABOVE
    '\u1EE0': 'O',   # LATIN CAPITAL LETTER O WITH HORN AND TILDE
    '\u1EE1': 'o',   # LATIN SMALL LETTER O WITH HORN AND TILDE
    '\u1EE2': 'O',   # LATIN CAPITAL LETTER O WITH HORN AND DOT BELOW
    '\u1EE3': 'o',   # LATIN SMALL LETTER O WITH HORN AND DOT BELOW
}

# l 和 1 混淆
L_ONE_HOMOGLYPHS: Dict[str, str] = {
    '\u006C': 'l',   # LATIN SMALL LETTER L (标准)
    '\u0049': 'I',   # LATIN CAPITAL LETTER I (标准)
    '\u0069': 'i',   # LATIN SMALL LETTER I (标准)
    '\u0031': '1',   # DIGIT ONE (标准)
    '\u007C': '|',   # VERTICAL LINE
    '\u0131': 'i',   # LATIN SMALL LETTER DOTLESS I
    '\u012B': 'i',   # LATIN SMALL LETTER I WITH MACRON
    '\u012A': 'I',   # LATIN CAPITAL LETTER I WITH MACRON
    '\u012D': 'i',   # LATIN SMALL LETTER I WITH BREVE
    '\u012C': 'I',   # LATIN CAPITAL LETTER I WITH BREVE
    '\u012F': 'i',   # LATIN SMALL LETTER I WITH OGONEK
    '\u012E': 'I',   # LATIN CAPITAL LETTER I WITH OGONEK
    '\u0269': 'i',   # LATIN SMALL LETTER IOTA
    '\u0196': 'I',   # LATIN CAPITAL LETTER IOTA
    '\u04BB': 'h',   # CYRILLIC SMALL LETTER SHHA (看起来像 H)
    '\u0456': 'i',   # CYRILLIC SMALL LETTER BYELORUSSIAN-UKRAINIAN I
    '\u0406': 'I',   # CYRILLIC CAPITAL LETTER BYELORUSSIAN-UKRAINIAN I
    '\u0399': 'I',   # GREEK CAPITAL LETTER IOTA
    '\u03B9': 'i',   # GREEK SMALL LETTER IOTA
    '\u03AF': 'i',   # GREEK SMALL LETTER IOTA WITH TONOS
    '\u038A': 'I',   # GREEK CAPITAL LETTER IOTA WITH TONOS
    '\u03AA': 'I',   # GREEK CAPITAL LETTER IOTA WITH DIALYTIKA
    '\u03CA': 'i',   # GREEK SMALL LETTER IOTA WITH DIALYTIKA
    '\u03CB': 'i',   # GREEK SMALL LETTER IOTA WITH DIALYTIKA AND TONOS
    '\u217C': 'l',   # SMALL ROMAN NUMERAL FIFTY
    '\u216C': 'L',   # ROMAN NUMERAL FIFTY
    '\uFF11': '1',   # FULLWIDTH DIGIT ONE
    '\uFF29': 'I',   # FULLWIDTH LATIN CAPITAL LETTER I
    '\uFF49': 'i',   # FULLWIDTH LATIN SMALL LETTER I
    '\uFF4C': 'l',   # FULLWIDTH LATIN SMALL LETTER L
    '\uFF31': 'I',   # FULLWIDTH LATIN CAPITAL LETTER I (sic)
}


def _get_all_homoglyphs() -> Dict[str, Tuple[str, HomoglyphCategory]]:
    """获取所有同形字映射"""
    result = {}
    for char, canonical in CYRILLIC_HOMOGLYPHS.items():
        result[char] = (canonical, HomoglyphCategory.LATIN_CYRILLIC)
    for char, canonical in GREEK_HOMOGLYPHS.items():
        result[char] = (canonical, HomoglyphCategory.LATIN_GREEK)
    for char, canonical in FULLWIDTH_HOMOGLYPHS.items():
        result[char] = (canonical, HomoglyphCategory.FULLWIDTH)
    for char, canonical in LOOKALIKE_HOMOGLYPHS.items():
        result[char] = (canonical, HomoglyphCategory.LOOKALIKE)
    return result


def _get_char_description(char: str, canonical: str, category: HomoglyphCategory) -> str:
    """获取字符描述"""
    codepoint = ord(char)
    try:
        name = unicodedata.name(char, 'UNKNOWN')
    except ValueError:
        name = 'UNKNOWN'
    
    if category == HomoglyphCategory.LATIN_CYRILLIC:
        return f"西里尔字母 '{char}' (U+{codepoint:04X}, {name}) 混淆拉丁字母 '{canonical}'"
    elif category == HomoglyphCategory.LATIN_GREEK:
        return f"希腊字母 '{char}' (U+{codepoint:04X}, {name}) 混淆拉丁字母 '{canonical}'"
    elif category == HomoglyphCategory.FULLWIDTH:
        return f"全角字符 '{char}' (U+{codepoint:04X}, {name}) 混淆半角字符 '{canonical}'"
    elif category == HomoglyphCategory.LOOKALIKE:
        if canonical == '':
            return f"不可见字符 (U+{codepoint:04X}, {name})"
        return f"视觉相似字符 '{char}' (U+{codepoint:04X}, {name}) 混淆 '{canonical}'"
    else:
        return f"混淆字符 '{char}' (U+{codepoint:04X}, {name})"


def _get_risk_level(char: str, category: HomoglyphCategory) -> int:
    """获取风险等级 (1-5)"""
    # 西里尔字母同形字是最危险的，常用于 IDN 欺骗
    if category == HomoglyphCategory.LATIN_CYRILLIC:
        # 某些西里尔字母比其他更危险
        high_risk_chars = {'а', 'е', 'о', 'р', 'с', 'х', 'у'}  # a, e, o, p, c, x, y
        if char.lower() in high_risk_chars:
            return 5
        return 4
    elif category == HomoglyphCategory.LATIN_GREEK:
        return 4
    elif category == HomoglyphCategory.FULLWIDTH:
        return 2
    elif category == HomoglyphCategory.LOOKALIKE:
        codepoint = ord(char)
        # 零宽字符
        if codepoint in (0x200B, 0x200C, 0x200D, 0xFEFF, 0x00AD, 0x034F):
            return 5
        # 特殊空格
        if codepoint in (0x00A0, 0x2000, 0x2001, 0x2002, 0x2003, 0x2004, 0x2005, 
                         0x2006, 0x2007, 0x2008, 0x2009, 0x200A, 0x202F, 0x205F, 0x3000):
            return 3
        return 3
    else:
        return 2


# ==================== 核心检测函数 ====================

def detect_homoglyphs(text: str, 
                      categories: Optional[List[HomoglyphCategory]] = None,
                      include_invisible: bool = True) -> List[HomoglyphMatch]:
    """
    检测文本中的同形字
    
    Args:
        text: 要检测的文本
        categories: 要检测的类别列表，None 表示所有类别
        include_invisible: 是否包含不可见字符
    
    Returns:
        同形字匹配列表
    
    Examples:
        >>> matches = detect_homoglyphs("pаypal.com")  # 使用西里尔字母 'а'
        >>> len(matches)
        1
        >>> matches[0].original_char
        'а'
        >>> matches[0].canonical_char
        'a'
    """
    if categories is None:
        categories = list(HomoglyphCategory)
    
    all_homoglyphs = _get_all_homoglyphs()
    matches = []
    
    for i, char in enumerate(text):
        if char in all_homoglyphs:
            canonical, category = all_homoglyphs[char]
            
            if category not in categories:
                continue
            
            # 处理不可见字符
            if canonical == '' and not include_invisible:
                continue
            
            description = _get_char_description(char, canonical, category)
            risk_level = _get_risk_level(char, category)
            
            matches.append(HomoglyphMatch(
                position=i,
                original_char=char,
                original_codepoint=ord(char),
                canonical_char=canonical,
                canonical_codepoint=ord(canonical) if canonical else 0,
                category=category,
                description=description,
                risk_level=risk_level
            ))
    
    return matches


def normalize_homoglyphs(text: str, 
                         categories: Optional[List[HomoglyphCategory]] = None) -> str:
    """
    将同形字转换为规范形式
    
    Args:
        text: 要规范化的文本
        categories: 要处理的类别列表，None 表示所有类别
    
    Returns:
        规范化后的文本
    
    Examples:
        >>> normalize_homoglyphs("pаypal.com")  # 西里尔字母 'а' -> 拉丁 'a'
        'paypal.com'
        >>> normalize_homoglyphs("Ｈｅｌｌｏ")  # 全角 -> 半角
        'Hello'
    """
    if categories is None:
        categories = list(HomoglyphCategory)
    
    all_homoglyphs = _get_all_homoglyphs()
    result = []
    
    for char in text:
        if char in all_homoglyphs:
            canonical, category = all_homoglyphs[char]
            if category in categories:
                result.append(canonical)
            else:
                result.append(char)
        else:
            result.append(char)
    
    return ''.join(result)


def scan_text(text: str, 
              categories: Optional[List[HomoglyphCategory]] = None,
              include_invisible: bool = True) -> HomoglyphScanResult:
    """
    扫描文本并返回详细结果
    
    Args:
        text: 要扫描的文本
        categories: 要检测的类别列表
        include_invisible: 是否包含不可见字符
    
    Returns:
        扫描结果对象
    
    Examples:
        >>> result = scan_text("pаypal.com")
        >>> result.has_homoglyphs
        True
        >>> result.risk_level
        '高风险'
    """
    matches = detect_homoglyphs(text, categories, include_invisible)
    normalized = normalize_homoglyphs(text, categories)
    
    # 计算风险分数 (0-100)
    if not matches:
        risk_score = 0
    else:
        # 基于匹配数量和风险等级计算
        max_score = len(text) * 5  # 最高每字符5分
        actual_score = sum(m.risk_level for m in matches)
        risk_score = min(100, int(actual_score * 100 / max(max_score, 1)))
    
    # 风险等级描述
    if risk_score == 0:
        risk_level = "无风险"
    elif risk_score < 20:
        risk_level = "低风险"
    elif risk_score < 40:
        risk_level = "中低风险"
    elif risk_score < 60:
        risk_level = "中风险"
    elif risk_score < 80:
        risk_level = "中高风险"
    else:
        risk_level = "高风险"
    
    return HomoglyphScanResult(
        text=text,
        normalized=normalized,
        matches=matches,
        risk_score=risk_score,
        risk_level=risk_level
    )


# ==================== 专项检测函数 ====================

def check_domain_safety(domain: str) -> HomoglyphScanResult:
    """
    检查域名安全性（IDN 同形字攻击检测）
    
    Args:
        domain: 要检查的域名
    
    Returns:
        扫描结果
    
    Examples:
        >>> result = check_domain_safety("pаypal.com")  # 西里尔字母 'а'
        >>> result.has_homoglyphs
        True
        >>> result.matches[0].category == HomoglyphCategory.LATIN_CYRILLIC
        True
    """
    # 域名检测重点关注西里尔和希腊字母
    return scan_text(domain, [
        HomoglyphCategory.LATIN_CYRILLIC,
        HomoglyphCategory.LATIN_GREEK,
        HomoglyphCategory.FULLWIDTH,
        HomoglyphCategory.LOOKALIKE
    ])


def check_username_safety(username: str) -> HomoglyphScanResult:
    """
    检查用户名安全性
    
    Args:
        username: 要检查的用户名
    
    Returns:
        扫描结果
    """
    return scan_text(username, [
        HomoglyphCategory.LATIN_CYRILLIC,
        HomoglyphCategory.LATIN_GREEK,
        HomoglyphCategory.FULLWIDTH,
        HomoglyphCategory.LOOKALIKE
    ])


def check_password_homoglyphs(password: str) -> HomoglyphScanResult:
    """
    检查密码中的同形字（可能导致输入问题）
    
    Args:
        password: 要检查的密码
    
    Returns:
        扫描结果
    """
    return scan_text(password)


def check_zero_o_confusion(text: str) -> List[HomoglyphMatch]:
    """
    专门检测 0/O 混淆
    
    Args:
        text: 要检测的文本
    
    Returns:
        匹配列表
    
    Examples:
        >>> matches = check_zero_o_confusion("ABC０１２OОО")
        >>> len(matches) > 0
        True
    """
    matches = []
    for i, char in enumerate(text):
        if char in ZERO_O_HOMOGLYPHS:
            canonical = ZERO_O_HOMOGLYPHS[char]
            matches.append(HomoglyphMatch(
                position=i,
                original_char=char,
                original_codepoint=ord(char),
                canonical_char=canonical,
                canonical_codepoint=ord(canonical),
                category=HomoglyphCategory.LOOKALIKE,
                description=f"数字0/字母O混淆字符 '{char}' (U+{ord(char):04X})",
                risk_level=4
            ))
    return matches


def check_l_one_confusion(text: str) -> List[HomoglyphMatch]:
    """
    专门检测 l/1/I 混淆
    
    Args:
        text: 要检测的文本
    
    Returns:
        匹配列表
    """
    matches = []
    for i, char in enumerate(text):
        if char in L_ONE_HOMOGLYPHS:
            canonical = L_ONE_HOMOGLYPHS[char]
            matches.append(HomoglyphMatch(
                position=i,
                original_char=char,
                original_codepoint=ord(char),
                canonical_char=canonical,
                canonical_codepoint=ord(canonical) if canonical else 0,
                category=HomoglyphCategory.LOOKALIKE,
                description=f"字母l/数字1/字母I混淆字符 '{char}' (U+{ord(char):04X})",
                risk_level=4
            ))
    return matches


def detect_invisible_chars(text: str) -> List[HomoglyphMatch]:
    """
    检测不可见字符
    
    Args:
        text: 要检测的文本
    
    Returns:
        不可见字符列表
    
    Examples:
        >>> text = "hello\u200bworld"  # 包含零宽空格
        >>> matches = detect_invisible_chars(text)
        >>> len(matches)
        1
    """
    return detect_homoglyphs(text, [HomoglyphCategory.LOOKALIKE], include_invisible=True)


def remove_invisible_chars(text: str) -> str:
    """
    移除不可见字符
    
    Args:
        text: 要处理的文本
    
    Returns:
        清理后的文本
    
    Examples:
        >>> remove_invisible_chars("hello\u200bworld")
        'helloworld'
    """
    invisible_codepoints = {
        0x200B,  # ZERO WIDTH SPACE
        0x200C,  # ZERO WIDTH NON-JOINER
        0x200D,  # ZERO WIDTH JOINER
        0xFEFF,  # ZERO WIDTH NO-BREAK SPACE (BOM)
        0x00AD,  # SOFT HYPHEN
        0x034F,  # COMBINING GRAPHEME JOINER
        0x180E,  # MONGOLIAN VOWEL SEPARATOR
        0x2060,  # WORD JOINER
        0x2061,  # FUNCTION APPLICATION
        0x2062,  # INVISIBLE TIMES
        0x2063,  # INVISIBLE SEPARATOR
        0x2064,  # INVISIBLE PLUS
        0x206A,  # INHIBIT SYMMETRIC SWAPPING
        0x206B,  # ACTIVATE SYMMETRIC SWAPPING
        0x206C,  # INHIBIT ARABIC FORM SHAPING
        0x206D,  # ACTIVATE ARABIC FORM SHAPING
        0x206E,  # NATIONAL DIGIT SHAPES
        0x206F,  # NOMINAL DIGIT SHAPES
    }
    return ''.join(c for c in text if ord(c) not in invisible_codepoints)


def normalize_spaces(text: str) -> str:
    """
    规范化各种空格字符
    
    Args:
        text: 要处理的文本
    
    Returns:
        规范化后的文本
    
    Examples:
        >>> normalize_spaces("hello\u00A0world")  # 不换行空格
        'hello world'
    """
    space_codepoints = {
        0x00A0,  # NO-BREAK SPACE
        0x2000,  # EN QUAD
        0x2001,  # EM QUAD
        0x2002,  # EN SPACE
        0x2003,  # EM SPACE
        0x2004,  # THREE-PER-EM SPACE
        0x2005,  # FOUR-PER-EM SPACE
        0x2006,  # SIX-PER-EM SPACE
        0x2007,  # FIGURE SPACE
        0x2008,  # PUNCTUATION SPACE
        0x2009,  # THIN SPACE
        0x200A,  # HAIR SPACE
        0x202F,  # NARROW NO-BREAK SPACE
        0x205F,  # MEDIUM MATHEMATICAL SPACE
        0x3000,  # IDEOGRAPHIC SPACE
    }
    return ''.join(' ' if ord(c) in space_codepoints else c for c in text)


# ==================== 批量处理 ====================

def batch_scan(texts: List[str], 
               categories: Optional[List[HomoglyphCategory]] = None) -> List[HomoglyphScanResult]:
    """
    批量扫描多个文本
    
    Args:
        texts: 文本列表
        categories: 要检测的类别列表
    
    Returns:
        扫描结果列表
    """
    return [scan_text(text, categories) for text in texts]


def find_homoglyph_pairs(text: str) -> Dict[str, List[int]]:
    """
    找出文本中所有同形字对（原字符位置按规范字符分组）
    
    Args:
        text: 要分析的文本
    
    Returns:
        字典：{规范字符: [位置列表]}
    
    Examples:
        >>> find_homoglyph_pairs("pаypаl")  # 两个西里尔 'а'
        {'a': [1, 4]}
    """
    all_homoglyphs = _get_all_homoglyphs()
    pairs: Dict[str, List[int]] = {}
    
    for i, char in enumerate(text):
        if char in all_homoglyphs:
            canonical, _ = all_homoglyphs[char]
            if canonical:
                if canonical not in pairs:
                    pairs[canonical] = []
                pairs[canonical].append(i)
    
    return pairs


def get_confusable_stats(text: str) -> Dict[str, int]:
    """
    获取文本中混淆字符的统计信息
    
    Args:
        text: 要分析的文本
    
    Returns:
        统计字典：{类别名: 数量}
    """
    matches = detect_homoglyphs(text)
    stats: Dict[str, int] = {}
    
    for match in matches:
        cat_name = match.category.value
        stats[cat_name] = stats.get(cat_name, 0) + 1
    
    return stats


# ==================== 工具函数 ====================

def get_char_info(char: str) -> Dict[str, any]:
    """
    获取字符的详细信息
    
    Args:
        char: 单个字符
    
    Returns:
        字符信息字典
    """
    codepoint = ord(char)
    try:
        name = unicodedata.name(char, 'UNKNOWN')
    except ValueError:
        name = 'UNKNOWN'
    
    category = unicodedata.category(char)
    combining = unicodedata.combining(char)
    bidirectional = unicodedata.bidirectional(char)
    mirrored = unicodedata.mirrored(char)
    normalized = unicodedata.normalize('NFC', char)
    
    all_homoglyphs = _get_all_homoglyphs()
    is_homoglyph = char in all_homoglyphs
    canonical = all_homoglyphs.get(char, (None, None))[0] if is_homoglyph else None
    
    return {
        'char': char,
        'codepoint': codepoint,
        'codepoint_hex': f'U+{codepoint:04X}',
        'name': name,
        'category': category,
        'combining': combining,
        'bidirectional': bidirectional,
        'mirrored': bool(mirrored),
        'nfc_normalized': normalized,
        'is_homoglyph': is_homoglyph,
        'canonical_char': canonical,
    }


def is_mixed_script(text: str, 
                    scripts: Optional[List[str]] = None) -> bool:
    """
    检测文本是否混合了多种书写系统（可能表示同形字攻击）
    
    Args:
        text: 要检测的文本
        scripts: 要检测的脚本列表（'Latin', 'Cyrillic', 'Greek'等）
                None 表示检测 Latin 与 Cyrillic/Greek 的混合
    
    Returns:
        是否混合脚本
    
    Examples:
        >>> is_mixed_script("pаypal")  # Latin + Cyrillic
        True
        >>> is_mixed_script("paypal")
        False
    """
    if scripts is None:
        scripts = ['Latin', 'Cyrillic', 'Greek']
    
    found_scripts: Set[str] = set()
    
    for char in text:
        # 跳过非字母字符
        if not char.isalpha():
            continue
        
        codepoint = ord(char)
        
        # 拉丁字母
        if (0x0041 <= codepoint <= 0x007A or  # Basic Latin
            0x00C0 <= codepoint <= 0x024F or  # Latin Extended
            0x1E00 <= codepoint <= 0x1EFF):   # Latin Extended Additional
            found_scripts.add('Latin')
        
        # 西里尔字母
        elif (0x0400 <= codepoint <= 0x04FF or   # Cyrillic
              0x0500 <= codepoint <= 0x052F or   # Cyrillic Supplement
              0x2DE0 <= codepoint <= 0x2DFF or   # Cyrillic Extended-A
              0xA640 <= codepoint <= 0xA69F):   # Cyrillic Extended-B
            found_scripts.add('Cyrillic')
        
        # 希腊字母
        elif (0x0370 <= codepoint <= 0x03FF or   # Greek and Coptic
              0x1F00 <= codepoint <= 0x1FFF):   # Greek Extended
            found_scripts.add('Greek')
    
    # 如果找到了多个指定的脚本，则返回 True
    relevant_scripts = found_scripts.intersection(scripts)
    return len(relevant_scripts) > 1


def suggest_replacement(text: str) -> List[Tuple[int, str, str]]:
    """
    建议字符替换方案
    
    Args:
        text: 要分析的文本
    
    Returns:
        替换建议列表：[(位置, 原字符, 建议字符), ...]
    
    Examples:
        >>> suggest_replacement("pаypal")
        [(1, 'а', 'a')]
    """
    all_homoglyphs = _get_all_homoglyphs()
    suggestions = []
    
    for i, char in enumerate(text):
        if char in all_homoglyphs:
            canonical, _ = all_homoglyphs[char]
            if canonical:  # 跳过不可见字符
                suggestions.append((i, char, canonical))
    
    return suggestions


# ==================== 主函数 ====================

def main():
    """演示函数"""
    print("=" * 60)
    print("Homoglyph Utils - Unicode 同形字检测工具演示")
    print("=" * 60)
    
    # 示例 1: 检测 IDN 同形字攻击
    print("\n[示例 1] IDN 同形字攻击检测")
    print("-" * 40)
    fake_domain = "pаypal.com"  # 使用西里尔字母 'а'
    result = check_domain_safety(fake_domain)
    print(f"域名: {fake_domain}")
    print(f"规范化: {result.normalized}")
    print(f"风险等级: {result.risk_level} (分数: {result.risk_score})")
    for match in result.matches:
        print(f"  - {match}")
    
    # 示例 2: 检测全角字符
    print("\n[示例 2] 全角字符检测")
    print("-" * 40)
    fullwidth_text = "Ｈｅｌｌｏ　Ｗｏｒｌｄ！"
    result = scan_text(fullwidth_text)
    print(f"原文: {fullwidth_text}")
    print(f"规范化: {result.normalized}")
    print(f"匹配数量: {result.match_count}")
    
    # 示例 3: 检测不可见字符
    print("\n[示例 3] 不可见字符检测")
    print("-" * 40)
    invisible_text = "hello\u200bworld\u200c\u200d"  # 零宽字符
    matches = detect_invisible_chars(invisible_text)
    print(f"文本长度: {len(invisible_text)} (可见: {len(remove_invisible_chars(invisible_text))})")
    print(f"不可见字符数量: {len(matches)}")
    for match in matches:
        print(f"  - 位置 {match.position}: U+{match.original_codepoint:04X}")
    
    # 示例 4: 混合脚本检测
    print("\n[示例 4] 混合脚本检测")
    print("-" * 40)
    mixed_texts = [
        "paypal",           # 纯拉丁
        "pаypal",           # Latin + Cyrillic 'а'
        "hεllo",            # Latin + Greek 'ε'
        "mіcrosoft",        # Latin + Cyrillic 'і'
    ]
    for text in mixed_texts:
        is_mixed = is_mixed_script(text)
        print(f"'{text}' -> 混合脚本: {is_mixed}")
    
    # 示例 5: 0/O 混淆检测
    print("\n[示例 5] 数字0/字母O 混淆检测")
    print("-" * 40)
    confusing_text = "PASS０123OООO"
    matches = check_zero_o_confusion(confusing_text)
    print(f"文本: {confusing_text}")
    print(f"混淆字符数量: {len(matches)}")
    for match in matches:
        print(f"  - {match.description}")
    
    # 示例 6: 批量扫描
    print("\n[示例 6] 批量域名扫描")
    print("-" * 40)
    domains = [
        "google.com",
        "gоogle.com",     # Cyrillic 'о'
        "amazоn.com",     # Cyrillic 'о'
        "аpple.com",      # Cyrillic 'а'
        "microsoft.com",
    ]
    for domain in domains:
        result = check_domain_safety(domain)
        status = "⚠️ 可疑" if result.has_homoglyphs else "✓ 安全"
        print(f"  {status}: {domain}")
        if result.has_homoglyphs:
            print(f"         -> {result.normalized}")
    
    print("\n" + "=" * 60)
    print("演示完成")


if __name__ == "__main__":
    main()