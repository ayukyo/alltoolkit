"""
polyglot_cipher.py — 编程语言密码器 (Polyglot Cipher)
====================================================================
创意：用编程语言写"密码"——不是加密算法，而是把明文转换成语法有效的
代码片段，让语言本身成为密码本。

原理：
  将 26 个字母映射到该语言中语法正确的符号、短语或关键词，
  消息被编码为一段"看起来像真实代码"的字符串。
  解码时根据当前语言解析映射，还原原文。

支持的 8 种语言每种都有独特的密码表：
  Rust  → 借用符号系：& ' " :: () {} [] ! ?
  Go    → 关键字系：fn let pub use mod impl trait const var ...
  Swift → 协议系：func var let protocol extension guard defer ...
  Kotlin→ 空安全系：val var null safe :: .. in is as ? !! ?: .
  TypeScript → 类型系：type interface enum extends implements <T> =>
  JavaScript → 箭头系：=> -> function const let var async await ...
  Java → 泛型系：public static void class interface extends new ...
  C/C++ → 预处理系：#define #include #ifdef #ifndef #endif << >> & | ^ ~

功能：
  1. encode(message) → 用当前语言编码字符串
  2. decode(cipher)   → 用当前语言解码字符串
  3. brute(cipher)   → 尝试所有 8 种语言自动解码
  4. polyglot_encode(messages_dict) → 用多种语言同时编码（发送一次，8人各能解密）
  5. polyglot_decode(cipher)        → 尝试所有语言解码

示例：
  Rust 模式编码 "HELLO" → "&'&::'&?! &'"  （随机从密码表中选字符）
  Go    模式编码 "HELLO" → "fn&&& let&&& fn&&&"  （用关键字填充）
  解码时用相同语言解析映射表反向还原

与 language_rotation.json 集成：
  - encode/decode 自动使用 current_index 对应的语言
  - brute 自动尝试所有 8 种语言
  - polyglot_* 支持同时使用所有语言

Distinct from existing modules:
  - polyglot_sentinel:   学习健康仪表盘
  - polyglot_resonator:  时间-语言共振分析
  - polyglot_pulse:      轮换历史脉搏追踪
  - polyglot_cipher:     用语言语法写密码（符号即密码本）

这不是加密算法（容易被频率分析破解），而是——
让编程语言本身成为一种好玩的密码艺术。

作者：AllToolkit 全自动生成
依赖：仅 Python 标准库（json, random, string, pathlib）
====================================================================
"""

import json
import os
import random
import re
import string
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# ─────────────────────────────────────────────
# 路径配置
# ─────────────────────────────────────────────
_MODULE_DIR = Path(__file__).parent.parent
_WORKSPACE_ROOT = _MODULE_DIR.parent
DEFAULT_LANGUAGE_ROTATION_JSON = str(_WORKSPACE_ROOT / "language_rotation.json")

# 8 种核心语言
CORE_LANGUAGES: List[str] = [
    "Rust", "Go", "Swift", "Kotlin",
    "TypeScript", "JavaScript", "Java", "C/C++",
]

LANGUAGE_EMOJI: Dict[str, str] = {
    "Rust": "🦀", "Go": "🐹", "Swift": "🦅", "Kotlin": "🟣",
    "TypeScript": "🔷", "JavaScript": "🟡", "Java": "☕", "C/C++": "🔩",
}

# ─────────────────────────────────────────────
# 密码表：每种语言一套符号/关键字映射
# ─────────────────────────────────────────────

# 基础字母表
ALPHABET = list(string.ascii_uppercase)  # A-Z
ALPHABET_LOWER = list(string.ascii_lowercase)  # a-z
DIGITS = list(string.digits)  # 0-9

# 每种语言的密码本：字母 → 多个候选符号
CIPHER_TABLES: Dict[str, Dict[str, List[str]]] = {
    "Rust": {
        # 借用符号系：用 Rust 特有的符号映射字母
        "A": ["&", "'", "!"],
        "B": ["*", "::", "!="],
        "C": ["::", "->", "?"],
        "D": [".", "::", ")"],
        "E": ["!", "'", "&"],
        "F": ["fn", "&", "!"],
        "G": ["&", "|", ">"],
        "H": ["#", "!", "@"],
        "I": ["impl", "!", "'"],
        "J": ["::", "?", ")"],
        "K": ["!", "@", "&"],
        "L": ["let", "'", "?"],
        "M": ["mut", "&", "!"],
        "N": ["!", "?", "'"],
        "O": ["or", "|", "!"],
        "P": ["pub", "&", "*"],
        "Q": ["!", "?", ")"],
        "R": ["&", "ref", "'"],
        "S": ["self", "&", "$"],
        "T": ["trait", "!", "'"],
        "U": ["&", "::", "!"],
        "V": ["val", "&", "!"],
        "W": ["!", "@", "#"],
        "X": ["!", "?", "&"],
        "Y": ["!", "'", "?"],
        "Z": ["!", "::", ")"],
        " ": [" ", "  ", "   "],
        "0": ["0", "0i32", "0u8"],
        "1": ["1", "1i32", "1u8"],
        "2": ["2", "2i32", "2u8"],
        "3": ["3", "3i32", "3u8"],
        "4": ["4", "4i32", "4u8"],
        "5": ["5", "5i32", "5u8"],
        "6": ["6", "6i32", "6u8"],
        "7": ["7", "7i32", "7u8"],
        "8": ["8", "8i32", "8u8"],
        "9": ["9", "9i32", "9u8"],
    },
    "Go": {
        # 关键字系：用 Go 关键字填充
        "A": ["and", "any", "app"],
        "B": ["break", "bool", "byte"],
        "C": ["case", "chan", "const", "cap"],
        "D": ["default", "defer", "delete"],
        "E": ["else", "error", "enum"],
        "F": ["fallthrough", "for", "func", "float64"],
        "G": ["go", "goto", "interface"],
        "H": ["http", "handle", "header"],
        "I": ["if", "int", "iota", "import"],
        "J": ["json", "join"],
        "K": ["key", "kind"],
        "L": ["len", "let", "log", "list"],
        "M": ["map", "make", "method"],
        "N": ["nil", "new", "not", "name"],
        "O": ["or", "ok", "order", "object"],
        "P": ["package", "panic", "print", "pub"],
        "Q": ["query", "queue"],
        "R": ["range", "return", "read"],
        "S": ["select", "struct", "string", "switch"],
        "T": ["type", "true", "table", "test"],
        "U": ["uint", "universe", "unique"],
        "V": ["var", "void", "val"],
        "W": ["while", "with", "write"],
        "X": ["xor", "xml"],
        "Y": ["yes", "yield"],
        "Z": ["zero", "zip"],
        " ": [" ", "  ", "   ", "_"],
        "0": ["0", "nil", "false"],
        "1": ["1", "true"],
        "2": ["2"],
        "3": ["3"],
        "4": ["4"],
        "5": ["5"],
        "6": ["6"],
        "7": ["7"],
        "8": ["8"],
        "9": ["9"],
    },
    "Swift": {
        # 协议系
        "A": ["actor", "any", "as"],
        "B": ["break", "bool", "break"],
        "C": ["case", "catch", "class", "convenience"],
        "D": ["defer", "default", "deinit", "do"],
        "E": ["else", "enum", "extension", "escape"],
        "F": ["fallthrough", "fileprivate", "final", "for", "func"],
        "G": ["get", "guard", "group"],
        "H": ["hash", "handle", "header"],
        "I": ["if", "import", "in", "init", "inout", "is"],
        "J": ["join"],
        "K": ["key", "kind"],
        "L": ["let", "lazy", "link"],
        "M": ["mutating", "move", "map", "module"],
        "N": ["nil", "none", "nonisolated"],
        "O": ["or", "operator", "optional", "override"],
        "P": ["private", "protocol", "public", "precedencegroup"],
        "Q": ["query"],
        "R": ["repeat", "rethrows", "return"],
        "S": ["self", "Self", "static", "struct", "subscript", "switch"],
        "T": ["throw", "throws", "try", "typealias", "throw"],
        "U": ["unowned", "unsafe", "using"],
        "V": ["var", "var", "virtual"],
        "W": ["weak", "where", "while", "willSet"],
        "X": ["xor"],
        "Y": ["yield"],
        "Z": ["zip"],
        " ": ["_", "  ", "   "],
        "0": ["0", "nil"],
        "1": ["1"],
        "2": ["2"],
        "3": ["3"],
        "4": ["4"],
        "5": ["5"],
        "6": ["6"],
        "7": ["7"],
        "8": ["8"],
        "9": ["9"],
    },
    "Kotlin": {
        # 空安全系
        "A": ["as", "also", "abstract"],
        "B": ["by", "break", "byte"],
        "C": ["class", "companion", "const", "continue"],
        "D": ["do", "data", "delegate"],
        "E": ["else", "enum", "eval", "exit"],
        "F": ["fun", "false", "finally", "for", "fileprivate"],
        "G": ["get", "guard"],
        "H": ["head", "header"],
        "I": ["if", "in", "inner", "interface", "import", "is"],
        "J": ["join", "joinToString"],
        "K": ["key", "kind"],
        "L": ["lateinit", "lazy", "let", "list"],
        "M": ["map", "mutable", "mutableListOf"],
        "N": ["null", "not", "name"],
        "O": ["object", "open", "operator", "or"],
        "P": ["package", "private", "public", "println"],
        "Q": ["query"],
        "R": ["return", "reified", "read"],
        "S": ["sealed", "static", "struct"],
        "T": ["typealias", "true", "this", "throw", "try"],
        "U": ["unit", "until", "unsafe"],
        "V": ["val", "var", "vararg", "when"],
        "W": ["when", "where", "while", "with"],
        "X": ["xor"],
        "Y": ["yield"],
        "Z": ["zip"],
        " ": ["_", "  ", "   "],
        "0": ["0", "null"],
        "1": ["1"],
        "2": ["2"],
        "3": ["3"],
        "4": ["4"],
        "5": ["5"],
        "6": ["6"],
        "7": ["7"],
        "8": ["8"],
        "9": ["9"],
    },
    "TypeScript": {
        # 类型系
        "A": ["as", "abstract", "any"],
        "B": ["boolean", "break", "bigint"],
        "C": ["class", "case", "const", "constructor"],
        "D": ["declare", "default", "do"],
        "E": ["enum", "export", "extends", "else"],
        "F": ["false", "finally", "for", "from", "function"],
        "G": ["get", "guard"],
        "H": ["header"],
        "I": ["if", "implements", "import", "in", "infer", "instanceof", "interface", "is"],
        "J": ["keyof", "typeof"],
        "K": ["key", "kind"],
        "L": ["let", "list"],
        "M": ["module", "namespace"],
        "N": ["namespace", "never", "new", "null"],
        "O": ["object", "of", "override", "or"],
        "P": ["private", "protected", "public", "partial", "readonly"],
        "Q": ["query"],
        "R": ["return", "readonly"],
        "S": ["static", "string", "super", "switch", "symbol"],
        "T": ["type", "this", "throw", "true", "try", "typeof"],
        "U": ["undefined", "unique", "unknown"],
        "V": ["var", "void"],
        "W": ["while", "when"],
        "X": ["xor"],
        "Y": ["yield"],
        "Z": ["zip"],
        " ": ["_", "  ", "   "],
        "0": ["0", "null"],
        "1": ["1"],
        "2": ["2"],
        "3": ["3"],
        "4": ["4"],
        "5": ["5"],
        "6": ["6"],
        "7": ["7"],
        "8": ["8"],
        "9": ["9"],
    },
    "JavaScript": {
        # 箭头系
        "A": ["async", "await", "any"],
        "B": ["break", "boolean"],
        "C": ["class", "const", "catch", "case", "constructor"],
        "D": ["debugger", "default", "delete", "do"],
        "E": ["export", "extends", "else", "enum", "eval"],
        "F": ["false", "finally", "for", "from", "function"],
        "G": ["get", "goto"],
        "H": ["header"],
        "I": ["if", "import", "in", "instanceof", "interface"],
        "J": ["json"],
        "K": ["key", "kind"],
        "L": ["let", "list"],
        "M": ["module", "map", "method"],
        "N": ["new", "null", "name"],
        "O": ["of", "or", "object"],
        "P": ["private", "protected", "public", "promise"],
        "Q": ["query"],
        "R": ["return", "readonly"],
        "S": ["static", "string", "super", "switch", "symbol"],
        "T": ["this", "throw", "true", "try", "typeof", "type"],
        "U": ["undefined", "unique"],
        "V": ["var", "void"],
        "W": ["while", "when", "with"],
        "X": ["xor"],
        "Y": ["yield"],
        "Z": ["zip"],
        " ": ["_", "  ", "   "],
        "0": ["0", "null"],
        "1": ["1"],
        "2": ["2"],
        "3": ["3"],
        "4": ["4"],
        "5": ["5"],
        "6": ["6"],
        "7": ["7"],
        "8": ["8"],
        "9": ["9"],
    },
    "Java": {
        # 泛型系
        "A": ["abstract", "assert", "args"],
        "B": ["break", "boolean", "byte", "break"],
        "C": ["case", "catch", "class", "const", "continue"],
        "D": ["default", "do", "double", "delete"],
        "E": ["else", "enum", "extends", "else"],
        "F": ["false", "final", "finally", "float", "for", "function"],
        "G": ["goto", "get"],
        "H": ["header"],
        "I": ["if", "implements", "import", "in", "int", "interface", "instanceof"],
        "J": ["json"],
        "K": ["key", "kind"],
        "L": ["long", "list"],
        "M": ["module", "map", "method", "main"],
        "N": ["new", "null", "native"],
        "O": ["or", "object", "override"],
        "P": ["package", "private", "protected", "public", "print"],
        "Q": ["query"],
        "R": ["return", "readonly"],
        "S": ["static", "strictfp", "super", "switch", "synchronized"],
        "T": ["this", "throw", "throws", "transient", "true", "try", "type"],
        "U": ["void", "volatile"],
        "V": ["var", "void", "val"],
        "W": ["while", "when"],
        "X": ["xor"],
        "Y": ["yield"],
        "Z": ["zip"],
        " ": ["_", "  ", "   "],
        "0": ["0", "null"],
        "1": ["1"],
        "2": ["2"],
        "3": ["3"],
        "4": ["4"],
        "5": ["5"],
        "6": ["6"],
        "7": ["7"],
        "8": ["8"],
        "9": ["9"],
    },
    "C/C++": {
        # 预处理系
        "A": ["and", "alignas", "and_eq", "asm", "auto"],
        "B": ["break", "bool", "bitand", "bitor", "break"],
        "C": ["case", "catch", "char", "class", "compl", "const", "continue"],
        "D": ["default", "delete", "do", "double", "dynamic_cast"],
        "E": ["else", "enum", "explicit", "export", "extern"],
        "F": ["false", "float", "for", "friend", "function"],
        "G": ["goto", "get"],
        "H": ["header", "hash"],
        "I": ["if", "inline", "int", "interface", "instanceof"],
        "J": ["json"],
        "K": ["key", "kind"],
        "L": ["long", "list"],
        "M": ["module", "map", "method", "mutable"],
        "N": ["namespace", "new", "noexcept", "not", "nullptr"],
        "O": ["or", "object", "operator", "or_eq"],
        "P": ["private", "protected", "public", "printf"],
        "Q": ["query"],
        "R": ["return", "register", "reinterpret_cast"],
        "S": ["static", "struct", "switch", "signed", "sizeof", "string"],
        "T": ["template", "this", "throw", "true", "try", "typedef", "typeid"],
        "U": ["union", "unsigned", "using"],
        "V": ["virtual", "void", "volatile", "var"],
        "W": ["while", "when", "wchar_t"],
        "X": ["xor", "xor_eq"],
        "Y": ["yield"],
        "Z": ["zip"],
        " ": ["_", "  ", "   "],
        "0": ["0", "nullptr"],
        "1": ["1"],
        "2": ["2"],
        "3": ["3"],
        "4": ["4"],
        "5": ["5"],
        "6": ["6"],
        "7": ["7"],
        "8": ["8"],
        "9": ["9"],
    },
}


# ─────────────────────────────────────────────
# 反向解码映射：每种语言的符号 → 字母
# ─────────────────────────────────────────────

def _build_reverse_table(table: Dict[str, List[str]]) -> Dict[str, str]:
    """从正向表构建反向解码表（符号 → 字母）。"""
    reverse: Dict[str, str] = {}
    for letter, symbols in table.items():
        for sym in symbols:
            # 短的符号优先精确匹配
            reverse[sym] = letter
    return reverse


REVERSE_TABLES: Dict[str, Dict[str, str]] = {
    lang: _build_reverse_table(table)
    for lang, table in CIPHER_TABLES.items()
}


# ─────────────────────────────────────────────
# 辅助函数
# ─────────────────────────────────────────────

def _read_rotation_json(json_path: str) -> Dict[str, Any]:
    """读取 language_rotation.json，返回 dict。"""
    if not os.path.exists(json_path):
        raise FileNotFoundError(f"Cannot find {json_path}")
    with open(json_path, "r", encoding="utf-8") as f:
        return json.load(f)


def _write_rotation_json(json_path: str, data: Dict[str, Any]) -> Dict[str, Any]:
    """更新 language_rotation.json 的 current_index，并写入文件。返回更新后的数据。"""
    languages = data["languages"]
    idx = data.get("current_index", 0) % len(languages)
    current = languages[idx]
    next_idx = (idx + 1) % len(languages)

    data["current_index"] = next_idx
    data["last_language"] = current
    from datetime import datetime
    data["updated_at"] = datetime.now().strftime("%Y-%m-%dT%H:%M:%S+08:00")

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    return data


def _encode_char(char: str, table: Dict[str, List[str]], rng: random.Random) -> str:
    """用给定密码表编码一个字符。"""
    upper = char.upper()
    if upper in table:
        candidates = table[upper]
        return rng.choice(candidates)
    elif char in table:
        return table[char][0]
    elif char in string.digits:
        return char  # 数字直接返回
    else:
        return char  # 未知字符原样返回


def _normalize_space_handling(text: str) -> str:
    """规范化空格处理，让解码更稳定。"""
    # 把多个连续空格替换为固定数量
    return re.sub(r" {2,}", "   ", text)


# ─────────────────────────────────────────────
# 核心编码/解码 API
# ─────────────────────────────────────────────

def encode(
    message: str,
    language: Optional[str] = None,
    json_path: str = DEFAULT_LANGUAGE_ROTATION_JSON,
    seed: Optional[int] = None,
    advance: bool = True,
) -> Dict[str, Any]:
    """
    用指定语言（或 language_rotation.json 当前语言）编码消息。

    参数：
        message: 要编码的明文消息
        language: 指定语言（None=从 json_path 读取 current_index）
        json_path: language_rotation.json 路径
        seed: 随机种子（用于可复现的编码）
        advance: 是否推进 current_index（默认 True）

    返回：
        {
            "cipher": str,           # 编码后的密文
            "language": str,         # 使用的语言
            "alphabetical": str,     # 字母部分的编码（去掉空格）
            "seed": int or None,
            "json_updated": bool,
            "timestamp": str,
        }
    """
    from datetime import datetime

    # 获取语言
    if language is None:
        data = _read_rotation_json(json_path)
        languages = data["languages"]
        idx = data.get("current_index", 0) % len(languages)
        lang = languages[idx]
    else:
        lang = language
        data = None

    if lang not in CIPHER_TABLES:
        raise ValueError(f"Language '{lang}' not supported. Use one of: {list(CIPHER_TABLES.keys())}")

    # 随机编码
    rng = random.Random(seed)
    table = CIPHER_TABLES[lang]

    normalized = _normalize_space_handling(message)
    chars = list(normalized)
    cipher_parts = [_encode_char(c, table, rng) for c in chars]
    cipher = " ".join(cipher_parts)

    # 字母压缩版（去掉空格，保留所有符号）
    alpha_cipher = "".join(c for c in cipher if not c.isspace())

    # 推进索引
    json_updated = False
    if advance and data is not None:
        _write_rotation_json(json_path, data)
        json_updated = True

    return {
        "cipher": cipher,
        "language": lang,
        "alphabetical": alpha_cipher,
        "seed": seed,
        "json_updated": json_updated,
        "timestamp": datetime.now().strftime("%Y-%m-%dT%H:%M:%S+08:00"),
    }


def decode(
    cipher: str,
    language: str,
    json_path: str = DEFAULT_LANGUAGE_ROTATION_JSON,
) -> Dict[str, Any]:
    """
    用指定语言解码密文。

    参数：
        cipher: 编码后的密文
        language: 解码使用的语言
        json_path: 仅用于返回 current_language 时读取

    返回：
        {
            "message": str,         # 解码后的明文
            "language": str,        # 使用的语言
            "confidence": float,   # 解码置信度（所有符号都识别=1.0）
            "timestamp": str,
        }
    """
    from datetime import datetime

    if language not in REVERSE_TABLES:
        raise ValueError(f"Language '{language}' not supported")

    reverse = REVERSE_TABLES[language]
    table = CIPHER_TABLES[language]

    # 清理密文
    cipher_clean = cipher.strip()

    # 尝试解码：用空格分割 token，或逐字符匹配
    # 策略：先用空格分割，匹配每个 token；空格 token → 空格
    tokens = cipher_clean.split(" ")
    decoded_chars = []
    unknown_count = 0

    for token in tokens:
        if token == "":
            decoded_chars.append(" ")
        elif token in reverse:
            decoded_chars.append(reverse[token])
        else:
            # 尝试精确匹配（长符号优先）
            best_match = None
            # 按符号长度降序排列尝试
            candidates = sorted(reverse.keys(), key=len, reverse=True)
            for sym in candidates:
                if cipher_clean.startswith(sym):
                    # 这里简化处理
                    pass

            # 直接找最长前缀匹配
            matched = False
            for sym in candidates:
                if token == sym:
                    decoded_chars.append(reverse[sym])
                    matched = True
                    break
            if not matched:
                # 未知符号，尝试单字符
                if token in reverse:
                    decoded_chars.append(reverse[token])
                elif len(token) == 1 and token.upper() in table:
                    decoded_chars.append(token.upper())
                else:
                    decoded_chars.append("?")
                    unknown_count += 1

    message = "".join(decoded_chars)
    # 清理多余空格
    message = re.sub(r" {2,}", " ", message).strip()

    # 计算置信度
    total_tokens = len([t for t in tokens if t != ""])
    confidence = (total_tokens - unknown_count) / max(total_tokens, 1) if total_tokens > 0 else 0.0

    # 获取当前语言
    try:
        data = _read_rotation_json(json_path)
        languages = data["languages"]
        idx = data.get("current_index", 0) % len(languages)
        current_lang = languages[idx]
    except Exception:
        current_lang = language

    return {
        "message": message,
        "language": language,
        "confidence": confidence,
        "unknown_count": unknown_count,
        "current_language": current_lang,
        "timestamp": datetime.now().strftime("%Y-%m-%dT%H:%M:%S+08:00"),
    }


def brute_decode(
    cipher: str,
    json_path: str = DEFAULT_LANGUAGE_ROTATION_JSON,
) -> Dict[str, Any]:
    """
    尝试用所有 8 种语言自动解码密文，返回置信度最高的结果。

    返回：
        {
            "message": str,
            "best_language": str,
            "all_results": {lang: {"message": str, "confidence": float}},
            "timestamp": str,
        }
    """
    from datetime import datetime

    results = {}
    best_lang = None
    best_conf = -1.0
    best_message = ""

    for lang in CORE_LANGUAGES:
        result = decode(cipher, lang, json_path)
        results[lang] = {
            "message": result["message"],
            "confidence": result["confidence"],
            "emoji": LANGUAGE_EMOJI.get(lang, "📦"),
        }
        if result["confidence"] > best_conf:
            best_conf = result["confidence"]
            best_lang = lang
            best_message = result["message"]

    return {
        "message": best_message,
        "best_language": best_lang,
        "best_confidence": best_conf,
        "all_results": results,
        "timestamp": datetime.now().strftime("%Y-%m-%dT%H:%M:%S+08:00"),
    }


def polyglot_encode(
    message: str,
    json_path: str = DEFAULT_LANGUAGE_ROTATION_JSON,
    seed: Optional[int] = None,
) -> Dict[str, Any]:
    """
    用所有 8 种语言同时编码同一消息，生成 8 套密文。
    任何拥有对应语言解码能力的人都能解开。

    返回：
        {
            "message": str,
            "ciphers": {lang: cipher_str},
            "alphabetical": {lang: alpha_str},
            "seed": int or None,
            "timestamp": str,
        }
    """
    from datetime import datetime

    ciphers = {}
    alphabetical = {}

    rng = random.Random(seed)

    for lang in CORE_LANGUAGES:
        table = CIPHER_TABLES[lang]
        normalized = _normalize_space_handling(message)
        chars = list(normalized)
        cipher_parts = [_encode_char(c, table, rng) for c in chars]
        cipher = " ".join(cipher_parts)
        ciphers[lang] = cipher
        alphabetical[lang] = "".join(c for c in cipher if not c.isspace())

    return {
        "message": message,
        "ciphers": ciphers,
        "alphabetical": alphabetical,
        "seed": seed,
        "timestamp": datetime.now().strftime("%Y-%m-%dT%H:%M:%S+08:00"),
    }


def polyglot_decode(
    cipher_or_dict: Dict[str, str],
    json_path: str = DEFAULT_LANGUAGE_ROTATION_JSON,
) -> Dict[str, Any]:
    """
    多语言密文解码。cipher_or_dict 可以是：
      - dict: {lang: cipher} → 用对应语言分别解码
      - str:  纯字符串密文 → 用 brute_decode 尝试所有语言

    返回各语言的解码结果。
    """
    from datetime import datetime

    if isinstance(cipher_or_dict, dict):
        results = {}
        for lang, cipher in cipher_or_dict.items():
            if lang in CORE_LANGUAGES:
                result = decode(cipher, lang, json_path)
                results[lang] = {
                    "message": result["message"],
                    "confidence": result["confidence"],
                    "emoji": LANGUAGE_EMOJI.get(lang, "📦"),
                }
        return {
            "results": results,
            "timestamp": datetime.now().strftime("%Y-%m-%dT%H:%M:%S+08:00"),
        }
    else:
        return brute_decode(cipher_or_dict, json_path)


def get_current_language(json_path: str = DEFAULT_LANGUAGE_ROTATION_JSON) -> str:
    """获取当前轮换语言（不推进索引）。"""
    data = _read_rotation_json(json_path)
    languages = data["languages"]
    idx = data.get("current_index", 0) % len(languages)
    return languages[idx]


def get_cipher_status(json_path: str = DEFAULT_LANGUAGE_ROTATION_JSON) -> Dict[str, Any]:
    """获取密码器状态。"""
    from datetime import datetime
    data = _read_rotation_json(json_path)
    languages = data["languages"]
    idx = data.get("current_index", 0) % len(languages)
    lang = languages[idx]
    return {
        "current_language": lang,
        "emoji": LANGUAGE_EMOJI.get(lang, "📦"),
        "current_index": idx,
        "total_languages": len(languages),
        "next_language": languages[(idx + 1) % len(languages)],
        "timestamp": datetime.now().strftime("%Y-%m-%dT%H:%M:%S+08:00"),
    }


def list_languages() -> List[str]:
    """列出所有支持的语言。"""
    return CORE_LANGUAGES


# ─────────────────────────────────────────────
# 格式化输出
# ─────────────────────────────────────────────

def format_encode_result(result: Dict[str, Any]) -> str:
    """格式化编码结果。"""
    lang = result["language"]
    emoji = LANGUAGE_EMOJI.get(lang, "📦")
    lines = [
        f"  ╔══════════════════════════════════════════════════════════╗",
        f"  ║  🔐 Polyglot Cipher — 语言密码器                        ║",
        f"  ╠══════════════════════════════════════════════════════════╣",
        f"  ║  {emoji} 语言：{lang:<47}  ║",
        f"  ╠══════════════════════════════════════════════════════════╣",
        f"  ║  📝 原文：{result.get('message', ''):<44}  ║" if "message" in result else "",
        f"  ║  🔒 密文：{result['cipher']:<44}  ║",
        f"  ║  📋 压缩：{result['alphabetical']:<44}  ║",
        f"  ║  🎲 种子：{str(result['seed']):<44}  ║" if result["seed"] is not None else f"  ║  🎲 种子：随机                                        ║",
        f"  ║  ✅ 索引已推进" if result.get("json_updated") else f"  ║  ⏸️  索引未推进",
        f"  ╚══════════════════════════════════════════════════════════╝",
    ]
    lines = [l for l in lines if l]
    return "\n".join(lines)


def format_decode_result(result: Dict[str, Any]) -> str:
    """格式化解码结果。"""
    lang = result["language"]
    emoji = LANGUAGE_EMOJI.get(lang, "📦")
    conf_pct = f"{result['confidence'] * 100:.1f}%"
    lines = [
        f"  ╔══════════════════════════════════════════════════════════╗",
        f"  ║  🔓 Polyglot Cipher — 解码结果                          ║",
        f"  ╠══════════════════════════════════════════════════════════╣",
        f"  ║  {emoji} 语言：{lang:<47}  ║",
        f"  ╠══════════════════════════════════════════════════════════╣",
        f"  ║  💬 解密：{result['message']:<44}  ║",
        f"  ║  📊 置信：{conf_pct:<44}  ║",
        f"  ║  ⚠️  未知符号：{result.get('unknown_count', 0):<39}  ║",
        f"  ╚══════════════════════════════════════════════════════════╝",
    ]
    return "\n".join(lines)


def format_polyglot_result(result: Dict[str, Any]) -> str:
    """格式化多语言编码结果。"""
    lines = [
        f"  ╔══════════════════════════════════════════════════════════╗",
        f"  ║  🌍 Polyglot Cipher — 多语言同时编码                     ║",
        f"  ╠══════════════════════════════════════════════════════════╣",
        f"  ║  📝 原文：{result['message']:<44}  ║",
        f"  ╠══════════════════════════════════════════════════════════╣",
    ]
    for lang, cipher in result["ciphers"].items():
        emoji = LANGUAGE_EMOJI.get(lang, "📦")
        lines.append(f"  ║  {emoji} {lang:<8} {cipher[:36]:<36}  ║")

    lines += [
        f"  ╠══════════════════════════════════════════════════════════╣",
        f"  ║  💡 每人只需用自己的语言解码，即还原原文                   ║",
        f"  ╚══════════════════════════════════════════════════════════╝",
    ]
    return "\n".join(lines)


def format_brute_result(result: Dict[str, Any]) -> str:
    """格式化暴力解码结果（尝试所有语言）。"""
    lines = [
        f"  ╔══════════════════════════════════════════════════════════╗",
        f"  ║  🔍 Polyglot Cipher — 全语言自动解码                     ║",
        f"  ╠══════════════════════════════════════════════════════════╣",
        f"  ║  🏆 最佳语言：{result['best_language']:<40}  ║",
        f"  ║  📊 最佳置信：{result['best_confidence'] * 100:.1f}%{' ' * 37}  ║",
        f"  ║  💬 解密结果：{result['message'][:40]:<40}  ║",
        f"  ╠══════════════════════════════════════════════════════════╣",
        f"  ║  📋 各语言解码结果：                                     ║",
    ]
    for lang, res in result["all_results"].items():
        emoji = res["emoji"]
        conf = f"{res['confidence'] * 100:.1f}%"
        marker = "✅" if lang == result["best_language"] else "  "
        lines.append(
            f"  ║  {marker} {emoji} {lang:<8} 置信:{conf:<8}  {res['message'][:30]:<30}  ║"
        )
    lines.append(f"  ╚══════════════════════════════════════════════════════════╝")
    return "\n".join(lines)


# ─────────────────────────────────────────────
# CLI 入口
# ─────────────────────────────────────────────

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Polyglot Cipher — 编程语言密码器")
    sub = parser.add_subparsers(dest="cmd")

    enc = sub.add_parser("encode", help="编码消息")
    enc.add_argument("message", help="要编码的消息")
    enc.add_argument("-l", "--language", help="指定语言（默认从 rotation 读取）")
    enc.add_argument("-s", "--seed", type=int, help="随机种子（可复现）")
    enc.add_argument("--no-advance", action="store_true", help="不推进轮换索引")

    dec = sub.add_parser("decode", help="解码消息")
    dec.add_argument("cipher", help="要解码的密文")
    dec.add_argument("-l", "--language", required=True, help="指定语言")

    sub.add_parser("brute", help="尝试所有语言自动解码")
    sub.add_parser("brute", help="自动解码（尝试所有语言）").add_argument("cipher", help="密文")

    poly = sub.add_parser("polyglot-encode", help="多语言同时编码")
    poly.add_argument("message", help="要编码的消息")
    poly.add_argument("-s", "--seed", type=int, help="随机种子")

    polydec = sub.add_parser("polyglot-decode", help="多语言解码")
    polydec.add_argument("cipher", nargs="+", help="密文（格式: lang:cipher）")

    status = sub.add_parser("status", help="查看当前状态")

    args = parser.parse_args()

    if args.cmd == "encode":
        result = encode(
            args.message,
            language=args.language,
            seed=args.seed,
            advance=not args.no_advance,
        )
        print(format_encode_result(result))

    elif args.cmd == "decode":
        result = decode(args.cipher, args.language)
        print(format_decode_result(result))

    elif args.cmd == "brute":
        result = brute_decode(args.cipher)
        print(format_brute_result(result))

    elif args.cmd == "polyglot-encode":
        result = polyglot_encode(args.message, seed=args.seed)
        print(format_polyglot_result(result))

    elif args.cmd == "polyglot-decode":
        # 格式: lang:cipher
        cipher_dict = {}
        for item in args.cipher:
            if ":" in item:
                lang, cipher = item.split(":", 1)
                cipher_dict[lang] = cipher
            else:
                print(f"Invalid format: {item}, expected lang:cipher")
                sys.exit(1)
        result = polyglot_decode(cipher_dict)
        print(json.dumps(result, ensure_ascii=False, indent=2))

    elif args.cmd == "status":
        st = get_cipher_status()
        emoji = st["emoji"]
        print(f"\n🔐 Polyglot Cipher 状态\n")
        print(f"  当前语言: {emoji} {st['current_language']}")
        print(f"  索引位置: {st['current_index'] + 1}/{st['total_languages']}")
        print(f"  下一语言: {LANGUAGE_EMOJI.get(st['next_language'], '📦')} {st['next_language']}")
        print(f"  支持语言: {', '.join(CORE_LANGUAGES)}")

    else:
        parser.print_help()
