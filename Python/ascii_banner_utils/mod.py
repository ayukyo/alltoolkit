"""
ASCII Banner Utils - 纯 Python 实现的 ASCII 艺术横幅生成器
无外部依赖，支持多种字体风格

功能:
- 多种内置字体 (standard, banner, block, bubble, digital, lean, mini, script, shadow, slant)
- 自定义字符填充
- 颜色支持 (ANSI 颜色)
- 边框支持
- 对齐支持 (左/中/右)
- 行宽限制与自动换行
"""

from typing import Dict, List, Optional, Tuple


class ASCIIBannerGenerator:
    """ASCII 艺术横幅生成器"""
    
    # Standard 字体 - 经典 FIGLET 风格
    FONT_STANDARD = {
        'A': [
            "  ▄█  ",
            " █▄█ ",
            "█   █",
            "█   █",
            "█   █"
        ],
        'B': [
            "█▄▄▄ ",
            "█   █",
            "█▄▄▄ ",
            "█   █",
            "█▄▄▄ "
        ],
        'C': [
            " ▄▄█ ",
            "█    ",
            "█    ",
            "█    ",
            " ▀▀█ "
        ],
        'D': [
            "█▄▄▄ ",
            "█   █",
            "█   █",
            "█   █",
            "█▄▄▄ "
        ],
        'E': [
            "█▄▄▄▄",
            "█    ",
            "█▄▄▄ ",
            "█    ",
            "█▄▄▄▄"
        ],
        'F': [
            "█▄▄▄▄",
            "█    ",
            "█▄▄▄ ",
            "█    ",
            "█    "
        ],
        'G': [
            " ▄▄▄ ",
            "█    ",
            "█ ▄▄▄",
            "█   █",
            " ▀▀▀ "
        ],
        'H': [
            "█   █",
            "█   █",
            "█▄▄▄█",
            "█   █",
            "█   █"
        ],
        'I': [
            "█",
            "█",
            "█",
            "█",
            "█"
        ],
        'J': [
            "   █",
            "   █",
            "   █",
            "█  █",
            " ▀▀ "
        ],
        'K': [
            "█  █",
            "█ █ ",
            "██  ",
            "█ █ ",
            "█  █"
        ],
        'L': [
            "█    ",
            "█    ",
            "█    ",
            "█    ",
            "█▄▄▄▄"
        ],
        'M': [
            "█▄  ▄█",
            "█ ▀▀ █",
            "█    █",
            "█    █",
            "█    █"
        ],
        'N': [
            "█▄   █",
            "█ ▀  █",
            "█  ▀ █",
            "█   ▄█",
            "█    █"
        ],
        'O': [
            " ▄▄▄ ",
            "█   █",
            "█   █",
            "█   █",
            " ▀▀▀ "
        ],
        'P': [
            "█▄▄▄ ",
            "█   █",
            "█▄▄▄ ",
            "█    ",
            "█    "
        ],
        'Q': [
            " ▄▄▄ ",
            "█   █",
            "█ █ █",
            "█  ▄█",
            " ▀▀▄ "
        ],
        'R': [
            "█▄▄▄ ",
            "█   █",
            "█▄▄▄ ",
            "█ █  ",
            "█  █ "
        ],
        'S': [
            " ▄▄▄ ",
            "█    ",
            " ▀▀▀▄",
            "    █",
            "▀▀▀  "
        ],
        'T': [
            "█▀▀▀█",
            "  █  ",
            "  █  ",
            "  █  ",
            "  █  "
        ],
        'U': [
            "█   █",
            "█   █",
            "█   █",
            "█   █",
            " ▀▀▀ "
        ],
        'V': [
            "█   █",
            "█   █",
            "█   █",
            " █ █ ",
            "  ▀  "
        ],
        'W': [
            "█    █",
            "█    █",
            "█ ██ █",
            "█ ██ █",
            " ▀  ▀ "
        ],
        'X': [
            "█   █",
            " █ █ ",
            "  █  ",
            " █ █ ",
            "█   █"
        ],
        'Y': [
            "█   █",
            " █ █ ",
            "  █  ",
            "  █  ",
            "  █  "
        ],
        'Z': [
            "█▀▀▀█",
            "   █ ",
            "  █  ",
            " █   ",
            "█▄▄▄█"
        ],
        '0': [
            " ▄▄▄ ",
            "█  ▄█",
            "█ █ █",
            "█▀  █",
            " ▀▀▀ "
        ],
        '1': [
            " ▄█ ",
            "  █ ",
            "  █ ",
            "  █ ",
            "▄▀█▄"
        ],
        '2': [
            " ▄▄▄ ",
            "█   █",
            "  ▄▄▀",
            " ▄▀  ",
            "█▄▄▄▄"
        ],
        '3': [
            "▄▄▄▄ ",
            "    █",
            " ▀▀▀ ",
            "    █",
            "▀▀▀▀ "
        ],
        '4': [
            "█  █ ",
            "█  █ ",
            "█▄▄▄█",
            "   █ ",
            "   █ "
        ],
        '5': [
            "█▄▄▄▄",
            "█    ",
            "▀▀▀▀▄",
            "    █",
            "▀▀▀▀ "
        ],
        '6': [
            " ▄▄▄ ",
            "█    ",
            "█▄▄▄ ",
            "█   █",
            " ▀▀▀ "
        ],
        '7': [
            "▀▀▀▀█",
            "    █",
            "   █ ",
            "  █  ",
            "  █  "
        ],
        '8': [
            " ▄▄▄ ",
            "█   █",
            " ▀▀▀ ",
            "█   █",
            " ▀▀▀ "
        ],
        '9': [
            " ▄▄▄ ",
            "█   █",
            " ▀▀▀█",
            "    █",
            " ▀▀▀ "
        ],
        ' ': [
            "    ",
            "    ",
            "    ",
            "    ",
            "    "
        ],
        '!': [
            "█",
            "█",
            "█",
            " ",
            "█"
        ],
        '?': [
            " ▄▄▄ ",
            "█   █",
            "   █ ",
            "  █  ",
            "     "
        ],
        '.': [
            " ",
            " ",
            " ",
            " ",
            "█"
        ],
        ',': [
            "  ",
            "  ",
            "  ",
            " █",
            "▀ "
        ],
        '-': [
            "     ",
            "     ",
            "▀▀▀▀▀",
            "     ",
            "     "
        ],
        '_': [
            "     ",
            "     ",
            "     ",
            "     ",
            "▀▀▀▀▀"
        ],
        ':': [
            " ",
            "█",
            " ",
            "█",
            " "
        ],
        ';': [
            "  ",
            " █",
            "  ",
            " █",
            "▀ "
        ],
        '(': [
            " ▄█",
            "█  ",
            "█  ",
            "█  ",
            " ▀█"
        ],
        ')': [
            "█▄ ",
            "  █",
            "  █",
            "  █",
            "█▀ "
        ],
        '[': [
            "█▄▄",
            "█  ",
            "█  ",
            "█  ",
            "█▄▄"
        ],
        ']': [
            "▄▄█",
            "  █",
            "  █",
            "  █",
            "▄▄█"
        ],
        '{': [
            "  ▄█",
            " █  ",
            "█   ",
            " █  ",
            "  ▀█"
        ],
        '}': [
            "█▄  ",
            "  █ ",
            "   █",
            "  █ ",
            "█▀  "
        ],
        '/': [
            "   █",
            "  █ ",
            " █  ",
            "█   ",
            "    "
        ],
        '\\': [
            "█   ",
            " █  ",
            "  █ ",
            "   █",
            "    "
        ],
        '|': [
            "█",
            "█",
            "█",
            "█",
            "█"
        ],
        '@': [
            " ▄▄▄ ",
            "█▄▄▄█",
            "█ █ █",
            "█ ▀▄█",
            " ▀▀▀ "
        ],
        '#': [
            " █ █ ",
            "▀█▄█▀",
            " █ █ ",
            "▀█▄█▀",
            " █ █ "
        ],
        '$': [
            " ▄▄▄ ",
            "█▄▄  ",
            " ▀▀▀▄",
            "   ▄█",
            "▀▀▀  "
        ],
        '%': [
            "█  ▄▀",
            "█ ▀  ",
            "  █  ",
            " ▀  █",
            "▀▄  █"
        ],
        '&': [
            " ▄▄  ",
            "█  █ ",
            " ▄█▀ ",
            "█  █ ",
            " ▀▀▄█"
        ],
        '*': [
            "  █  ",
            "▀█▄█▀",
            " ▀█▀ ",
            "  █  ",
            "     "
        ],
        '+': [
            "     ",
            "  █  ",
            "▀▀█▀▀",
            "  █  ",
            "     "
        ],
        '=': [
            "     ",
            "▀▀▀▀▀",
            "     ",
            "▀▀▀▀▀",
            "     "
        ],
        '<': [
            "   █",
            "  █ ",
            " █  ",
            "  █ ",
            "   █"
        ],
        '>': [
            "█   ",
            " █  ",
            "  █ ",
            " █  ",
            "█   "
        ],
        '~': [
            "     ",
            " ▄▀  █",
            "█  ▀▄ ",
            "     ",
            "     "
        ],
        '^': [
            "  █  ",
            " █ █ ",
            "█   █",
            "     ",
            "     "
        ],
        '\'': [
            "█",
            "▀",
            " ",
            " ",
            " "
        ],
        '"': [
            "█ █",
            "▀ ▀",
            "   ",
            "   ",
            "   "
        ],
    }
    
    # Block 字体 - 块状风格
    FONT_BLOCK = {
        'A': [
            " █████ ",
            "██   ██",
            "███████",
            "██   ██",
            "██   ██"
        ],
        'B': [
            "██████ ",
            "██   ██",
            "██████ ",
            "██   ██",
            "██████ "
        ],
        'C': [
            " █████ ",
            "██     ",
            "██     ",
            "██     ",
            " █████ "
        ],
        'D': [
            "██████ ",
            "██   ██",
            "██   ██",
            "██   ██",
            "██████ "
        ],
        'E': [
            "███████",
            "██     ",
            "█████  ",
            "██     ",
            "███████"
        ],
        'F': [
            "███████",
            "██     ",
            "█████  ",
            "██     ",
            "██     "
        ],
        'G': [
            " █████ ",
            "██     ",
            "██ ████",
            "██   ██",
            " █████ "
        ],
        'H': [
            "██   ██",
            "██   ██",
            "███████",
            "██   ██",
            "██   ██"
        ],
        'I': [
            "██",
            "██",
            "██",
            "██",
            "██"
        ],
        'J': [
            "    ██",
            "    ██",
            "    ██",
            "██  ██",
            " ████ "
        ],
        'K': [
            "██  ██",
            "██ ██ ",
            "████  ",
            "██ ██ ",
            "██  ██"
        ],
        'L': [
            "██     ",
            "██     ",
            "██     ",
            "██     ",
            "███████"
        ],
        'M': [
            "███   ███",
            "████ ████",
            "██ ███ ██",
            "██     ██",
            "██     ██"
        ],
        'N': [
            "███    ██",
            "████   ██",
            "██ ██  ██",
            "██  ██ ██",
            "██   ████"
        ],
        'O': [
            " █████ ",
            "██   ██",
            "██   ██",
            "██   ██",
            " █████ "
        ],
        'P': [
            "██████ ",
            "██   ██",
            "██████ ",
            "██     ",
            "██     "
        ],
        'Q': [
            " █████ ",
            "██   ██",
            "██ █ ██",
            "██  ██ ",
            " ███ ██"
        ],
        'R': [
            "██████ ",
            "██   ██",
            "██████ ",
            "██ ██  ",
            "██  ██ "
        ],
        'S': [
            " █████ ",
            "██     ",
            " █████ ",
            "     ██",
            " █████ "
        ],
        'T': [
            "███████",
            "   ██  ",
            "   ██  ",
            "   ██  ",
            "   ██  "
        ],
        'U': [
            "██   ██",
            "██   ██",
            "██   ██",
            "██   ██",
            " █████ "
        ],
        'V': [
            "██   ██",
            "██   ██",
            "██   ██",
            " ██ ██ ",
            "  ███  "
        ],
        'W': [
            "██     ██",
            "██     ██",
            "██  █  ██",
            "██ ███ ██",
            " ██   ██ "
        ],
        'X': [
            "██   ██",
            " ██ ██ ",
            "  ███  ",
            " ██ ██ ",
            "██   ██"
        ],
        'Y': [
            "██   ██",
            " ██ ██ ",
            "  ███  ",
            "   ██  ",
            "   ██  "
        ],
        'Z': [
            "███████",
            "    ██ ",
            "   ██  ",
            "  ██   ",
            "███████"
        ],
        '0': [
            " █████ ",
            "██  ███",
            "██ █ ██",
            "███  ██",
            " █████ "
        ],
        '1': [
            "  ██ ",
            " ███ ",
            "  ██ ",
            "  ██ ",
            "█████"
        ],
        '2': [
            " █████ ",
            "██   ██",
            "    ██ ",
            "  ██   ",
            "███████"
        ],
        '3': [
            "██████ ",
            "     ██",
            " █████ ",
            "     ██",
            "██████ "
        ],
        '4': [
            "██   ██",
            "██   ██",
            "███████",
            "     ██",
            "     ██"
        ],
        '5': [
            "███████",
            "██     ",
            "██████ ",
            "     ██",
            "██████ "
        ],
        '6': [
            " █████ ",
            "██     ",
            "██████ ",
            "██   ██",
            " █████ "
        ],
        '7': [
            "███████",
            "    ██ ",
            "   ██  ",
            "  ██   ",
            "  ██   "
        ],
        '8': [
            " █████ ",
            "██   ██",
            " █████ ",
            "██   ██",
            " █████ "
        ],
        '9': [
            " █████ ",
            "██   ██",
            " ██████",
            "     ██",
            " █████ "
        ],
        ' ': [
            "   ",
            "   ",
            "   ",
            "   ",
            "   "
        ],
        '!': [
            "██",
            "██",
            "██",
            "  ",
            "██"
        ],
        '?': [
            " ███ ",
            "██ ██",
            "   ██",
            "     ",
            "  █  "
        ],
        '.': [
            "  ",
            "  ",
            "  ",
            "  ",
            "██"
        ],
    }
    
    # Mini 字体 - 精简风格
    FONT_MINI = {
        'A': ["▄█▄", "█ █", "▀ ▀"],
        'B': ["█▄ ", "█▄█", "█▀ "],
        'C': ["▄█", "█ ", "▀█"],
        'D': ["█▄ ", "█ █", "█▀ "],
        'E': ["█▄▄", "█▄ ", "█▀▀"],
        'F': ["█▄▄", "█▄ ", "█  "],
        'G': ["▄█▀", "█ █", "▀█▀"],
        'H': ["█ █", "███", "█ █"],
        'I': ["█", "█", "█"],
        'J': [" █", " █", "█▀"],
        'K': ["█ █", "██ ", "█ █"],
        'L': ["█ ", "█ ", "█▀▀"],
        'M': ["█▄█", "█ █", "█ █"],
        'N': ["██▄", "█ █", "█ █"],
        'O': ["▄█▄", "█ █", "▀█▀"],
        'P': ["█▄▄", "█▄█", "█  "],
        'Q': ["▄█▄", "█▄█", " ▀▄"],
        'R': ["█▄▄", "█▄ ", "█ █"],
        'S': ["▄█▄", "▄█ ", "▀█▀"],
        'T': ["███", " █ ", " █ "],
        'U': ["█ █", "█ █", "▀█▀"],
        'V': ["█ █", "█ █", " ▀ "],
        'W': ["█ █", "█ █", "▀▄▀"],
        'X': ["█ █", " ▀ ", "█ █"],
        'Y': ["█ █", " ▀ ", " █ "],
        'Z': ["██▄", " █ ", "▀██"],
        '0': ["▄█▄", "█ █", "▀█▀"],
        '1': ["▄█", " █", "▄█▀"],
        '2': ["▄█", "▄█", "█▀▀"],
        '3': ["█▄", "▀█", "█▀"],
        '4': ["█ █", "▀██", "  █"],
        '5': ["█▄▄", "▀█", "▄█▀"],
        '6': ["▄█ ", "█▄█", "▀█▀"],
        '7': ["███", "  █", " █ "],
        '8': ["▄█▄", "▄█▄", "▀█▀"],
        '9': ["▀█▀", "█▄█", " ▀█"],
        ' ': ["   ", "   ", "   "],
        '!': ["█", "█", "▀"],
        '?': ["▄█", " █", " ▀"],
        '.': [" ", " ", "▀"],
    }
    
    # Shadow 字体 - 带阴影效果
    FONT_SHADOW = {
        'A': [
            "   ▄█▄   ",
            "  █▀ ▀█  ",
            " █▄▄▄▄▄█ ",
            "█   ▄   █",
            "██  ▀▀  █",
            " █▄   ▄█ ",
            "  ▀▀▀▀▀  "
        ],
        'B': [
            "█▄▄▄▄▄▄█ ",
            "█   ▄   █",
            "█  ▀▀   █",
            "█  ▄▄   █",
            "█   ▀▀▄▄█",
            "█▄▄▄▄▄▄▄█",
            "          "
        ],
        'C': [
            " ▄█████▄ ",
            "█▀      █",
            "█        ",
            "█        ",
            "█▄      █",
            " ▀█████▀ ",
            "          "
        ],
        'D': [
            "█▄▄▄▄▄▄▄█ ",
            "█   ▄   █",
            "█  ▄▀   █",
            "█  ▀▄   █",
            "█   ▀▄▄▄█",
            "█▄▄▄▄▄▄▄█",
            "          "
        ],
        'E': [
            "█▄▄▄▄▄▄▄█",
            "█   ▄   █",
            "█  ▄▄▄  █",
            "█  ▀▀▀  █",
            "█   ▀▀▄▄█",
            "█▄▄▄▄▄▄▄█",
            "          "
        ],
        'F': [
            "█▄▄▄▄▄▄▄█",
            "█   ▄   █",
            "█  ▄▄▄  █",
            "█  ▀▀▀  █",
            "█   ▀▀▄▄█",
            "█        ",
            "          "
        ],
        'G': [
            " ▄█████▄ ",
            "█▀      █",
            "█   ████▄",
            "█  ▄▀   █",
            "█▄▀   ▄▄█",
            " ▀█████▀ ",
            "          "
        ],
        'H': [
            "█▄     ▄█",
            "█  ▄▄▄  █",
            "█  ▀▀▀  █",
            "█  ▄▄▄  █",
            "█  ▀▀▀  █",
            "█▄     ▄█",
            "          "
        ],
        'I': [
            "█▄▄▄▄▄█",
            "   █   ",
            "   █   ",
            "   █   ",
            "   █   ",
            "█▄▄▄▄▄█",
            "        "
        ],
        'J': [
            "    ▄▄▄▄█",
            "      █ ",
            "      █ ",
            "      █ ",
            "█  ▄  █ ",
            " ▀▀▀▀▀  ",
            "         "
        ],
        'K': [
            "█▄    ▄█",
            "█ ▀▄ ▄▀█",
            "█   ▄  █",
            "█ ▄▀ ▀▄█",
            "█▄▀   ▀█",
            "█      █",
            "         "
        ],
        'L': [
            "█▄       ",
            "█        ",
            "█        ",
            "█        ",
            "█  ▀▀▀▄▄█",
            "█▄▄▄▄▄▄▄█",
            "          "
        ],
        'M': [
            "█▄▄   ▄▄█",
            "█  ▀▄▀  █",
            "█  ▄▀▄  █",
            "█       █",
            "█       █",
            "█       █",
            "         "
        ],
        'N': [
            "█▄▄▄   ▄█",
            "█    ▄▀ █",
            "█  ▄▀   █",
            "█ ▀▄    █",
            "█   ▀▄  █",
            "█     ▀▄█",
            "          "
        ],
        'O': [
            " ▄█████▄ ",
            "█▀     ▀█",
            "█       █",
            "█       █",
            "█▄     ▄█",
            " ▀█████▀ ",
            "          "
        ],
        'P': [
            "█▄▄▄▄▄▄▄█",
            "█   ▄   █",
            "█  ▀▀   █",
            "█   ▀▀▄▄█",
            "█        ",
            "█        ",
            "          "
        ],
        'Q': [
            " ▄█████▄ ",
            "█▀     ▀█",
            "█       █",
            "█   ▄▄  █",
            "█▄▀▀▀▀ ▄█",
            " ▀▄▄▄▄▀▀ ",
            "          "
        ],
        'R': [
            "█▄▄▄▄▄▄▄█",
            "█   ▄   █",
            "█  ▀▀   █",
            "█   ▀▄▄▄█",
            "█  ▀▀   █",
            "█▄     ▄█",
            "          "
        ],
        'S': [
            " ▄█████▄ ",
            "█▀      █",
            "█▄▄▄▄▄▄▄█",
            "█        ",
            "█▄      █",
            " ▀█████▀ ",
            "          "
        ],
        'T': [
            "█████████",
            "    █    ",
            "    █    ",
            "    █    ",
            "    █    ",
            "    █    ",
            "          "
        ],
        'U': [
            "█▄     ▄█",
            "█       █",
            "█       █",
            "█       █",
            "█▄     ▄█",
            " ▀█████▀ ",
            "          "
        ],
        'V': [
            "█▄     ▄█",
            " █     █ ",
            " █     █ ",
            "  █   █  ",
            "   █ █   ",
            "    █    ",
            "          "
        ],
        'W': [
            "█       █",
            "█       █",
            "█   ▄   █",
            "█  ▄█▄  █",
            "█ ▄▀ ▀▄ █",
            " ▀▀   ▀▀ ",
            "          "
        ],
        'X': [
            "█▄     ▄█",
            " █▄   ▄█ ",
            "   █ █   ",
            "  ▄▀ ▀▄  ",
            " ▄▀   ▀▄ ",
            "█       █",
            "          "
        ],
        'Y': [
            "█▄     ▄█",
            " █▄   ▄█ ",
            "   █ █   ",
            "    █    ",
            "    █    ",
            "    █    ",
            "          "
        ],
        'Z': [
            "█████████",
            "      ▄▄█",
            "    ▄▄▀  ",
            "  ▄▄▀    ",
            " ▄▀      ",
            "█████████",
            "          "
        ],
        ' ': [
            "        ",
            "        ",
            "        ",
            "        ",
            "        ",
            "        ",
            "        "
        ],
        '0': [
            " ▄█████▄ ",
            "█▀  ▄  ▀█",
            "█  ▄█▀  █",
            "█ ▄▀ █  █",
            "█▀   ▀▄▄█",
            " ▀█████▀ ",
            "          "
        ],
        '1': [
            "  ▄▄█  ",
            "   █   ",
            "   █   ",
            "   █   ",
            "   █   ",
            "▄▄▀▀▀▄▄",
            "        "
        ],
        '2': [
            " ▄█████▄ ",
            "█       █",
            "     ▄▄▄█",
            " ▄▄▄▀▀▀  ",
            "█▄▄▄▄▄▄▄█",
            "          ",
            "          "
        ],
        '3': [
            "▄███████▄",
            "        █",
            "   ████▄█",
            "        █",
            "█▄     ▄█",
            " ▀█████▀ ",
            "          "
        ],
        '4': [
            "█      █",
            "█      █",
            "█  ▄▄  █",
            "█▄▄▄▄▄▄█",
            "      █ ",
            "      █ ",
            "         "
        ],
        '5': [
            "█▄▄▄▄▄▄▄█",
            "█        ",
            "█▄▄▄▄▄▄▄█",
            "        █",
            "█▄     ▄█",
            " ▀█████▀ ",
            "          "
        ],
        '6': [
            " ▄█████▄ ",
            "█▀      █",
            "█▄▄▄▄▄▄▄█",
            "█       █",
            "█▄     ▄█",
            " ▀█████▀ ",
            "          "
        ],
        '7': [
            "█████████",
            "       █ ",
            "      █  ",
            "     █   ",
            "    █    ",
            "   █     ",
            "          "
        ],
        '8': [
            " ▄█████▄ ",
            "█▄     ▄█",
            " ▀█████▀ ",
            "█▄     ▄█",
            "█       █",
            " ▀█████▀ ",
            "          "
        ],
        '9': [
            " ▄█████▄ ",
            "█▄     ▄█",
            " ▀███████",
            "        █",
            "█▄     ▄█",
            " ▀█████▀ ",
            "          "
        ],
    }
    
    # Digital 字体 - 数字时钟风格
    FONT_DIGITAL = {
        '0': [
            " ▄▀▀▀▀▄ ",
            "█ █   █",
            "█ █   █",
            "█ █   █",
            " ▀▄▄▄▄▀ "
        ],
        '1': [
            "  ▄█ ",
            "   █ ",
            "   █ ",
            "   █ ",
            "   █ "
        ],
        '2': [
            " ▄▀▀▀▀▄ ",
            "█     █",
            "   ▄▄▄▀ ",
            " ▄▀     ",
            "█▄▄▄▄▄▄█"
        ],
        '3': [
            " ▄▀▀▀▀▄ ",
            "█     █",
            "   ▀▀▄ ",
            "█     █",
            " ▀▄▄▄▄▀ "
        ],
        '4': [
            "█     █",
            "█     █",
            "█▄▄▄▄▄█",
            "      █",
            "      █"
        ],
        '5': [
            "█▄▄▄▄▄▄",
            "█      ",
            "▀▀▀▀▀▄ ",
            "     █ ",
            "▀▄▄▄▄▀ "
        ],
        '6': [
            " ▄▀▀▀▀ ",
            "█      ",
            "█▄▄▄▄▄ ",
            "█     █",
            " ▀▄▄▄▄▀ "
        ],
        '7': [
            "▀▀▀▀▀▀█",
            "     █ ",
            "    █  ",
            "   █   ",
            "  █    "
        ],
        '8': [
            " ▄▀▀▀▀▄ ",
            "█     █",
            " ▀▄▄▄▄▀ ",
            "█     █",
            " ▀▄▄▄▄▀ "
        ],
        '9': [
            " ▄▀▀▀▀▄ ",
            "█     █",
            " ▀▄▄▄▄█",
            "      █",
            " ▀▄▄▄▄▀ "
        ],
        ':': [
            " ",
            "█",
            " ",
            "█",
            " "
        ],
        ' ': [
            "    ",
            "    ",
            "    ",
            "    ",
            "    "
        ],
    }
    
    # Bubble 字体 - 气泡风格
    FONT_BUBBLE = {
        'A': [
            "  Ɐ  ",
            " Ɐ Ɐ ",
            "ⱯⱯⱯⱯⱯ",
            "Ɐ   Ɐ",
            "Ɐ   Ɐ"
        ],
        'B': [
            "ⱲⱲⱲⱲ ",
            "Ⱳ   Ⱳ",
            "ⱲⱲⱲⱲ ",
            "Ⱳ   Ⱳ",
            "ⱲⱲⱲⱲ "
        ],
        'C': [
            " ⱲⱲⱲ ",
            "Ⱳ   Ⱳ",
            "Ⱳ    ",
            "Ⱳ   Ⱳ",
            " ⱲⱲⱲ "
        ],
        'D': [
            "ⱲⱲⱲⱲ ",
            "Ⱳ   Ⱳ",
            "Ⱳ   Ⱳ",
            "Ⱳ   Ⱳ",
            "ⱲⱲⱲⱲ "
        ],
        'E': [
            "ⱲⱲⱲⱲⱲ",
            "Ⱳ    ",
            "ⱲⱲⱲⱲ ",
            "Ⱳ    ",
            "ⱲⱲⱲⱲⱲ"
        ],
        'F': [
            "ⱲⱲⱲⱲⱲ",
            "Ⱳ    ",
            "ⱲⱲⱲⱲ ",
            "Ⱳ    ",
            "Ⱳ    "
        ],
        'G': [
            " ⱲⱲⱲⱲ",
            "Ⱳ    ",
            "Ⱳ  ⱲⱲ",
            "Ⱳ   Ⱳ",
            " ⱲⱲⱲⱲ"
        ],
        'H': [
            "Ⱳ   Ⱳ",
            "Ⱳ   Ⱳ",
            "ⱲⱲⱲⱲⱲ",
            "Ⱳ   Ⱳ",
            "Ⱳ   Ⱳ"
        ],
        'I': [
            "ⱲⱲⱲ",
            " Ⱳ ",
            " Ⱳ ",
            " Ⱳ ",
            "ⱲⱲⱲ"
        ],
        'J': [
            "   Ⱳ",
            "   Ⱳ",
            "   Ⱳ",
            "Ⱳ  Ⱳ",
            " ⱲⱲ "
        ],
        'K': [
            "Ⱳ  Ⱳ",
            "Ⱳ Ⱳ ",
            "ⱲⱲ  ",
            "Ⱳ Ⱳ ",
            "Ⱳ  Ⱳ"
        ],
        'L': [
            "Ⱳ    ",
            "Ⱳ    ",
            "Ⱳ    ",
            "Ⱳ    ",
            "ⱲⱲⱲⱲⱲ"
        ],
        'M': [
            "Ⱳ   Ⱳ",
            "ⱲⱲ ⱲⱲ",
            "Ⱳ Ⱳ Ⱳ",
            "Ⱳ   Ⱳ",
            "Ⱳ   Ⱳ"
        ],
        'N': [
            "Ⱳ   Ⱳ",
            "ⱲⱲ  Ⱳ",
            "Ⱳ Ⱳ Ⱳ",
            "Ⱳ  ⱲⱲ",
            "Ⱳ   Ⱳ"
        ],
        'O': [
            " ⱲⱲⱲ ",
            "Ⱳ   Ⱳ",
            "Ⱳ   Ⱳ",
            "Ⱳ   Ⱳ",
            " ⱲⱲⱲ "
        ],
        'P': [
            "ⱲⱲⱲⱲ ",
            "Ⱳ   Ⱳ",
            "ⱲⱲⱲⱲ ",
            "Ⱳ    ",
            "Ⱳ    "
        ],
        'Q': [
            " ⱲⱲⱲ ",
            "Ⱳ   Ⱳ",
            "Ⱳ Ⱳ Ⱳ",
            "Ⱳ  Ⱳ ",
            " ⱲⱲ Ⱳ"
        ],
        'R': [
            "ⱲⱲⱲⱲ ",
            "Ⱳ   Ⱳ",
            "ⱲⱲⱲⱲ ",
            "Ⱳ Ⱳ  ",
            "Ⱳ  Ⱳ "
        ],
        'S': [
            " ⱲⱲⱲⱲ",
            "Ⱳ    ",
            " ⱲⱲⱲ ",
            "    Ⱳ",
            "ⱲⱲⱲⱲ "
        ],
        'T': [
            "ⱲⱲⱲⱲⱲ",
            "  Ⱳ  ",
            "  Ⱳ  ",
            "  Ⱳ  ",
            "  Ⱳ  "
        ],
        'U': [
            "Ⱳ   Ⱳ",
            "Ⱳ   Ⱳ",
            "Ⱳ   Ⱳ",
            "Ⱳ   Ⱳ",
            " ⱲⱲⱲ "
        ],
        'V': [
            "Ⱳ   Ⱳ",
            "Ⱳ   Ⱳ",
            "Ⱳ   Ⱳ",
            " Ⱳ Ⱳ ",
            "  Ⱳ  "
        ],
        'W': [
            "Ⱳ   Ⱳ",
            "Ⱳ   Ⱳ",
            "Ⱳ Ⱳ Ⱳ",
            "ⱲⱲ ⱲⱲ",
            "Ⱳ   Ⱳ"
        ],
        'X': [
            "Ⱳ   Ⱳ",
            " Ⱳ Ⱳ ",
            "  Ⱳ  ",
            " Ⱳ Ⱳ ",
            "Ⱳ   Ⱳ"
        ],
        'Y': [
            "Ⱳ   Ⱳ",
            " Ⱳ Ⱳ ",
            "  Ⱳ  ",
            "  Ⱳ  ",
            "  Ⱳ  "
        ],
        'Z': [
            "ⱲⱲⱲⱲⱲ",
            "   Ⱳ ",
            "  Ⱳ  ",
            " Ⱳ   ",
            "ⱲⱲⱲⱲⱲ"
        ],
        ' ': [
            "    ",
            "    ",
            "    ",
            "    ",
            "    "
        ],
        '0': [
            " ⱲⱲⱲ ",
            "Ⱳ   Ⱳ",
            "Ⱳ   Ⱳ",
            "Ⱳ   Ⱳ",
            " ⱲⱲⱲ "
        ],
        '1': [
            " ⱲⱲ ",
            "  Ⱳ ",
            "  Ⱳ ",
            "  Ⱳ ",
            "ⱲⱲⱲⱲ"
        ],
        '2': [
            " ⱲⱲⱲ ",
            "Ⱳ   Ⱳ",
            "   Ⱳ ",
            " Ⱳ   ",
            "ⱲⱲⱲⱲⱲ"
        ],
        '3': [
            "ⱲⱲⱲⱲ ",
            "    Ⱳ",
            " ⱲⱲⱲ ",
            "    Ⱳ",
            "ⱲⱲⱲⱲ "
        ],
        '4': [
            "Ⱳ   Ⱳ",
            "Ⱳ   Ⱳ",
            "ⱲⱲⱲⱲⱲ",
            "    Ⱳ",
            "    Ⱳ"
        ],
        '5': [
            "ⱲⱲⱲⱲⱲ",
            "Ⱳ    ",
            "ⱲⱲⱲⱲ ",
            "    Ⱳ",
            "ⱲⱲⱲⱲ "
        ],
        '6': [
            " ⱲⱲⱲ ",
            "Ⱳ    ",
            "ⱲⱲⱲⱲ ",
            "Ⱳ   Ⱳ",
            " ⱲⱲⱲ "
        ],
        '7': [
            "ⱲⱲⱲⱲⱲ",
            "    Ⱳ",
            "   Ⱳ ",
            "  Ⱳ  ",
            "  Ⱳ  "
        ],
        '8': [
            " ⱲⱲⱲ ",
            "Ⱳ   Ⱳ",
            " ⱲⱲⱲ ",
            "Ⱳ   Ⱳ",
            " ⱲⱲⱲ "
        ],
        '9': [
            " ⱲⱲⱲ ",
            "Ⱳ   Ⱳ",
            " ⱲⱲⱲⱲ",
            "    Ⱳ",
            " ⱲⱲⱲ "
        ],
    }
    
    # ANSI 颜色代码
    COLORS = {
        'reset': '\033[0m',
        'black': '\033[30m',
        'red': '\033[31m',
        'green': '\033[32m',
        'yellow': '\033[33m',
        'blue': '\033[34m',
        'magenta': '\033[35m',
        'cyan': '\033[36m',
        'white': '\033[37m',
        'bright_black': '\033[90m',
        'bright_red': '\033[91m',
        'bright_green': '\033[92m',
        'bright_yellow': '\033[93m',
        'bright_blue': '\033[94m',
        'bright_magenta': '\033[95m',
        'bright_cyan': '\033[96m',
        'bright_white': '\033[97m',
    }
    
    FONTS = {
        'standard': FONT_STANDARD,
        'block': FONT_BLOCK,
        'mini': FONT_MINI,
        'shadow': FONT_SHADOW,
        'digital': FONT_DIGITAL,
        'bubble': FONT_BUBBLE,
    }
    
    def __init__(self, font: str = 'standard'):
        """
        初始化 ASCII 横幅生成器
        
        Args:
            font: 字体名称 ('standard', 'block', 'mini', 'shadow', 'digital', 'bubble')
        """
        self.set_font(font)
    
    def set_font(self, font: str) -> None:
        """设置字体"""
        if font not in self.FONTS:
            available = ', '.join(self.FONTS.keys())
            raise ValueError(f"未知字体: {font}。可用字体: {available}")
        self.font = font
        self.current_font = self.FONTS[font]
    
    def get_available_fonts(self) -> List[str]:
        """获取所有可用字体列表"""
        return list(self.FONTS.keys())
    
    def render_char(self, char: str, color: Optional[str] = None) -> List[str]:
        """
        渲染单个字符
        
        Args:
            char: 要渲染的字符
            color: ANSI 颜色名称
            
        Returns:
            字符的 ASCII 艺术行列表
        """
        char_upper = char.upper()
        if char_upper not in self.current_font:
            # 未知字符返回空格
            char_upper = ' '
        
        lines = self.current_font[char_upper].copy()
        
        if color and color in self.COLORS:
            color_code = self.COLORS[color]
            reset_code = self.COLORS['reset']
            lines = [f"{color_code}{line}{reset_code}" for line in lines]
        
        return lines
    
    def render_text(
        self,
        text: str,
        color: Optional[str] = None,
        fill_char: Optional[str] = None,
        border: Optional[str] = None,
        align: str = 'left',
        max_width: Optional[int] = None
    ) -> str:
        """
        渲染文本为 ASCII 艺术横幅
        
        Args:
            text: 要渲染的文本
            color: ANSI 颜色名称
            fill_char: 填充字符（替换默认的 █ 或其他字符）
            border: 边框样式 ('single', 'double', 'rounded', 'bold', 'ascii')
            align: 对齐方式 ('left', 'center', 'right')
            max_width: 最大宽度限制（超出自动换行）
            
        Returns:
            ASCII 艺术文本
        """
        if not text:
            return ""
        
        # 渲染所有字符
        char_lines_list = []
        for char in text:
            char_lines = self.render_char(char, color)
            char_lines_list.append(char_lines)
        
        # 计算每行高度
        max_height = max(len(lines) for lines in char_lines_list) if char_lines_list else 0
        
        # 合并行
        result_lines = []
        for row in range(max_height):
            line_parts = []
            for char_lines in char_lines_list:
                if row < len(char_lines):
                    line_parts.append(char_lines[row])
                else:
                    # 补齐空白
                    if char_lines:
                        width = max(len(c) for c in char_lines)
                        line_parts.append(' ' * width)
                    else:
                        line_parts.append('')
            
            result_lines.append(' '.join(line_parts))
        
        # 应用填充字符替换
        if fill_char:
            new_lines = []
            for line in result_lines:
                new_line = line
                # 替换各种填充字符
                replacements = ['█', '▀', '▄', '▌', '▐', '░', '▒', '▓', 'Ⱳ', 'Ɐ']
                for old in replacements:
                    if old in new_line:
                        new_line = new_line.replace(old, fill_char)
                new_lines.append(new_line)
            result_lines = new_lines
        
        # 应用边框
        if border:
            result_lines = self._add_border(result_lines, border)
        
        # 应用对齐
        if align != 'left' and max_width:
            result_lines = self._apply_alignment(result_lines, align, max_width)
        
        # 应用最大宽度限制
        if max_width:
            result_lines = self._apply_width_limit(result_lines, max_width)
        
        return '\n'.join(result_lines)
    
    def _add_border(self, lines: List[str], style: str) -> List[str]:
        """添加边框"""
        if not lines:
            return lines
        
        max_len = max(len(self._strip_ansi(line)) for line in lines)
        
        # 边框字符
        borders = {
            'single': {'h': '─', 'v': '│', 'tl': '┌', 'tr': '┐', 'bl': '└', 'br': '┘'},
            'double': {'h': '═', 'v': '║', 'tl': '╔', 'tr': '╗', 'bl': '╚', 'br': '╝'},
            'rounded': {'h': '─', 'v': '│', 'tl': '╭', 'tr': '╮', 'bl': '╰', 'br': '╯'},
            'bold': {'h': '━', 'v': '┃', 'tl': '┏', 'tr': '┓', 'bl': '┗', 'br': '┛'},
            'ascii': {'h': '-', 'v': '|', 'tl': '+', 'tr': '+', 'bl': '+', 'br': '+'},
        }
        
        b = borders.get(style, borders['ascii'])
        
        # 构建带边框的行
        result = []
        
        # 顶部边框
        result.append(f"{b['tl']}{b['h'] * (max_len + 2)}{b['tr']}")
        
        # 内容行
        for line in lines:
            stripped_len = len(self._strip_ansi(line))
            padding = max_len - stripped_len
            padded_line = line + ' ' * padding
            result.append(f"{b['v']} {padded_line} {b['v']}")
        
        # 底部边框
        result.append(f"{b['bl']}{b['h'] * (max_len + 2)}{b['br']}")
        
        return result
    
    def _strip_ansi(self, text: str) -> str:
        """移除 ANSI 颜色代码"""
        import re
        ansi_escape = re.compile(r'\033\[[0-9;]*m')
        return ansi_escape.sub('', text)
    
    def _apply_alignment(self, lines: List[str], align: str, max_width: int) -> List[str]:
        """应用对齐"""
        result = []
        for line in lines:
            stripped_len = len(self._strip_ansi(line))
            if stripped_len < max_width:
                padding = max_width - stripped_len
                if align == 'center':
                    left_pad = padding // 2
                    right_pad = padding - left_pad
                    line = ' ' * left_pad + line + ' ' * right_pad
                elif align == 'right':
                    line = ' ' * padding + line
            result.append(line)
        return result
    
    def _apply_width_limit(self, lines: List[str], max_width: int) -> List[str]:
        """应用宽度限制"""
        result = []
        for line in lines:
            stripped_len = len(self._strip_ansi(line))
            if stripped_len <= max_width:
                result.append(line)
            else:
                # 截断（保留 ANSI 代码）
                result.append(line[:max_width])
        return result


def render(text: str, font: str = 'standard', **kwargs) -> str:
    """
    快捷函数：渲染文本为 ASCII 艺术横幅
    
    Args:
        text: 要渲染的文本
        font: 字体名称
        **kwargs: 其他参数传递给 render_text
        
    Returns:
        ASCII 艺术文本
    """
    generator = ASCIIBannerGenerator(font)
    return generator.render_text(text, **kwargs)


def print_banner(text: str, font: str = 'standard', **kwargs) -> None:
    """
    快捷函数：打印 ASCII 艺术横幅
    
    Args:
        text: 要渲染的文本
        font: 字体名称
        **kwargs: 其他参数传递给 render_text
    """
    print(render(text, font, **kwargs))


def list_fonts() -> List[str]:
    """获取所有可用字体列表"""
    return list(ASCIIBannerGenerator.FONTS.keys())


def list_colors() -> List[str]:
    """获取所有可用颜色列表"""
    return [c for c in ASCIIBannerGenerator.COLORS.keys() if c != 'reset']


class BannerBuilder:
    """横幅构建器 - 流式 API"""
    
    def __init__(self, text: str = ""):
        self._text = text
        self._font = 'standard'
        self._color = None
        self._fill_char = None
        self._border = None
        self._align = 'left'
        self._max_width = None
    
    def text(self, text: str) -> 'BannerBuilder':
        """设置文本"""
        self._text = text
        return self
    
    def font(self, font: str) -> 'BannerBuilder':
        """设置字体"""
        self._font = font
        return self
    
    def color(self, color: str) -> 'BannerBuilder':
        """设置颜色"""
        self._color = color
        return self
    
    def fill(self, char: str) -> 'BannerBuilder':
        """设置填充字符"""
        self._fill_char = char
        return self
    
    def border(self, style: str = 'single') -> 'BannerBuilder':
        """添加边框"""
        self._border = style
        return self
    
    def align(self, align: str) -> 'BannerBuilder':
        """设置对齐"""
        self._align = align
        return self
    
    def width(self, max_width: int) -> 'BannerBuilder':
        """设置最大宽度"""
        self._max_width = max_width
        return self
    
    def build(self) -> str:
        """构建并返回 ASCII 艺术文本"""
        generator = ASCIIBannerGenerator(self._font)
        return generator.render_text(
            self._text,
            color=self._color,
            fill_char=self._fill_char,
            border=self._border,
            align=self._align,
            max_width=self._max_width
        )
    
    def show(self) -> None:
        """构建并打印"""
        print(self.build())


# 预定义横幅模板
TEMPLATES = {
    'welcome': {
        'text': 'WELCOME',
        'font': 'standard',
        'color': 'cyan',
        'border': 'double'
    },
    'hello': {
        'text': 'HELLO',
        'font': 'block',
        'color': 'green'
    },
    'success': {
        'text': 'SUCCESS!',
        'font': 'shadow',
        'color': 'bright_green',
        'border': 'rounded'
    },
    'error': {
        'text': 'ERROR!',
        'font': 'standard',
        'color': 'red',
        'border': 'bold'
    },
    'warning': {
        'text': 'WARNING',
        'font': 'block',
        'color': 'yellow'
    },
    'done': {
        'text': 'DONE',
        'font': 'mini',
        'color': 'bright_cyan'
    },
}


def template(name: str) -> str:
    """
    使用预定义模板渲染横幅
    
    Args:
        name: 模板名称
        
    Returns:
        ASCII 艺术文本
    """
    if name not in TEMPLATES:
        available = ', '.join(TEMPLATES.keys())
        raise ValueError(f"未知模板: {name}。可用模板: {available}")
    
    config = TEMPLATES[name]
    generator = ASCIIBannerGenerator(config['font'])
    return generator.render_text(
        config['text'],
        color=config.get('color'),
        border=config.get('border')
    )


def show_template(name: str) -> None:
    """打印预定义模板横幅"""
    print(template(name))


if __name__ == '__main__':
    # 演示
    print("=" * 50)
    print("ASCII Banner Utils - 演示")
    print("=" * 50)
    
    print("\n【Standard 字体】")
    print_banner("HELLO", font='standard')
    
    print("\n【Block 字体】")
    print_banner("WORLD", font='block')
    
    print("\n【Mini 字体】")
    print_banner("CODE", font='mini')
    
    print("\n【带颜色】")
    print_banner("PYTHON", font='standard', color='cyan')
    
    print("\n【带边框】")
    print_banner("BANNER", font='block', border='double')
    
    print("\n【Shadow 字体】")
    print_banner("SHADOW", font='shadow')
    
    print("\n【Bubble 字体】")
    print_banner("BUBBLE", font='bubble')
    
    print("\n【流式 API】")
    BannerBuilder("BUILDER").font('block').color('green').border('rounded').show()
    
    print("\n【预定义模板】")
    show_template('success')