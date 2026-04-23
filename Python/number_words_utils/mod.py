#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - Number Words Utilities Module
===========================================
A comprehensive number-to-words and words-to-number conversion utility module 
with zero external dependencies.

Features:
    - Convert numbers to words (123 → "one hundred twenty-three")
    - Convert words to numbers ("one hundred twenty-three" → 123)
    - Multi-language support (English, Chinese)
    - Ordinal number support (1 → "first", "first" → 1)
    - Currency format support ($123.45 → "one hundred twenty-three dollars and forty-five cents")
    - Fraction and decimal support
    - Negative number handling
    - Large number support (up to quintillions)

Author: AllToolkit Contributors
License: MIT
"""

from typing import Union, Tuple, Optional, Dict, List
from enum import Enum


# ============================================================================
# Type Aliases
# ============================================================================

Number = Union[int, float]


# ============================================================================
# English Number Words
# ============================================================================

ENGLISH_ONES = [
    "", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine",
    "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen",
    "seventeen", "eighteen", "nineteen"
]

ENGLISH_TENS = [
    "", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"
]

ENGLISH_ORDINAL_ONES = [
    "", "first", "second", "third", "fourth", "fifth", "sixth", "seventh", "eighth", "ninth",
    "tenth", "eleventh", "twelfth", "thirteenth", "fourteenth", "fifteenth", "sixteenth",
    "seventeenth", "eighteenth", "nineteenth"
]

ENGLISH_ORDINAL_TENS = [
    "", "", "twentieth", "thirtieth", "fortieth", "fiftieth", "sixtieth", "seventieth", "eightieth", "ninetieth"
]

ENGLISH_SCALES = [
    "", "thousand", "million", "billion", "trillion", "quadrillion", "quintillion"
]

ENGLISH_ORDINAL_SCALES = [
    "", "thousandth", "millionth", "billionth", "trillionth", "quadrillionth", "quintillionth"
]

# Mapping from words to numbers for English
ENGLISH_WORD_TO_NUM: Dict[str, int] = {}
for i, word in enumerate(ENGLISH_ONES):
    if word:
        ENGLISH_WORD_TO_NUM[word] = i
for i, word in enumerate(ENGLISH_TENS):
    if word:
        ENGLISH_WORD_TO_NUM[word] = i * 10
ENGLISH_WORD_TO_NUM["hundred"] = 100
for i, word in enumerate(ENGLISH_SCALES):
    if word:
        ENGLISH_WORD_TO_NUM[word] = 10 ** (i * 3)

# Ordinal word to number mapping
ENGLISH_ORDINAL_TO_NUM: Dict[str, int] = {}
for i, word in enumerate(ENGLISH_ORDINAL_ONES):
    if word:
        ENGLISH_ORDINAL_TO_NUM[word] = i
for i, word in enumerate(ENGLISH_ORDINAL_TENS):
    if word:
        ENGLISH_ORDINAL_TO_NUM[word] = i * 10


# ============================================================================
# Chinese Number Words
# ============================================================================

CHINESE_DIGITS = ["零", "一", "二", "三", "四", "五", "六", "七", "八", "九"]
CHINESE_UNITS = ["", "十", "百", "千"]
CHINESE_SCALES = ["", "万", "亿", "兆"]
CHINESE_ORDINAL_PREFIX = "第"

# Chinese word to number mapping
CHINESE_WORD_TO_NUM: Dict[str, int] = {}
for i, word in enumerate(CHINESE_DIGITS):
    CHINESE_WORD_TO_NUM[word] = i
CHINESE_WORD_TO_NUM["两"] = 2  # Alternative for two
CHINESE_WORD_TO_NUM["十"] = 10
CHINESE_WORD_TO_NUM["百"] = 100
CHINESE_WORD_TO_NUM["千"] = 1000
CHINESE_WORD_TO_NUM["万"] = 10000
CHINESE_WORD_TO_NUM["亿"] = 100000000
CHINESE_WORD_TO_NUM["兆"] = 1000000000000


# ============================================================================
# Decimal/Fraction Words
# ============================================================================

ENGLISH_DECIMAL_WORDS = [
    "", "tenths", "hundredths", "thousandths", "ten-thousandths",
    "hundred-thousandths", "millionths"
]

CHINESE_DECIMAL_WORDS = ["", "分", "厘", "毫", "丝", "忽", "微"]


# ============================================================================
# Currency Words
# ============================================================================

ENGLISH_CURRENCY = {
    "USD": ("dollar", "dollars", "cent", "cents"),
    "EUR": ("euro", "euros", "cent", "cents"),
    "GBP": ("pound", "pounds", "pence", "pence"),
    "CNY": ("yuan", "yuan", "fen", "fen"),
    "JPY": ("yen", "yen", "sen", "sen"),
}

CHINESE_CURRENCY = {
    "USD": ("美元", "美元", "美分", "美分"),
    "EUR": ("欧元", "欧元", "欧分", "欧分"),
    "GBP": ("英镑", "英镑", "便士", "便士"),
    "CNY": ("元", "元", "分", "分"),
    "JPY": ("日元", "日元", "钱", "钱"),
}


# ============================================================================
# Language Enum
# ============================================================================

class Language(Enum):
    """Supported languages for number-word conversion."""
    ENGLISH = "en"
    CHINESE = "zh"


class NumberWordsError(Exception):
    """Base exception for number-words operations."""
    pass


class UnsupportedLanguageError(NumberWordsError):
    """Raised when an unsupported language is specified."""
    pass


class InvalidNumberError(NumberWordsError):
    """Raised when an invalid number is provided."""
    pass


class InvalidWordError(NumberWordsError):
    """Raised when invalid word format is provided."""
    pass


# ============================================================================
# Number to Words Conversion
# ============================================================================

def _english_number_to_words_under_100(n: int) -> str:
    """Convert a number less than 100 to English words."""
    if n < 20:
        return ENGLISH_ONES[n]
    tens, ones = divmod(n, 10)
    if ones == 0:
        return ENGLISH_TENS[tens]
    return f"{ENGLISH_TENS[tens]}-{ENGLISH_ONES[ones]}"


def _english_number_to_words_under_1000(n: int) -> str:
    """Convert a number less than 1000 to English words."""
    hundreds, remainder = divmod(n, 100)
    if remainder == 0:
        return f"{ENGLISH_ONES[hundreds]} hundred" if hundreds > 0 else ""
    if hundreds == 0:
        return _english_number_to_words_under_100(remainder)
    return f"{ENGLISH_ONES[hundreds]} hundred {_english_number_to_words_under_100(remainder)}"


def number_to_words(
    number: Number,
    language: Union[Language, str] = Language.ENGLISH,
    ordinal: bool = False
) -> str:
    """
    Convert a number to its word representation.
    
    Args:
        number: The number to convert (int or float)
        language: Target language (Language.ENGLISH or Language.CHINESE)
        ordinal: If True, return ordinal form (1 → "first" instead of "one")
        
    Returns:
        The word representation of the number
        
    Raises:
        InvalidNumberError: If the number is out of supported range
        UnsupportedLanguageError: If the language is not supported
        
    Examples:
        >>> number_to_words(123)
        'one hundred twenty-three'
        >>> number_to_words(123, Language.CHINESE)
        '一百二十三'
        >>> number_to_words(1, ordinal=True)
        'first'
        >>> number_to_words(123.45)
        'one hundred twenty-three point four five'
    """
    if isinstance(language, str):
        language = Language(language.lower())
    
    if language == Language.ENGLISH:
        return _english_number_to_words(number, ordinal)
    elif language == Language.CHINESE:
        return _chinese_number_to_words(number, ordinal)
    else:
        raise UnsupportedLanguageError(f"Unsupported language: {language}")


def _english_number_to_words(n: Number, ordinal: bool = False) -> str:
    """Convert a number to English words."""
    # Handle negative numbers
    negative = False
    if n < 0:
        negative = True
        n = abs(n)
    
    # Handle zero
    if n == 0:
        return "zeroth" if ordinal else "zero"
    
    # Handle floats
    if isinstance(n, float) and not n.is_integer():
        integer_part = int(n)
        decimal_part = n - integer_part
        # Use format to avoid floating point precision issues (limit to 10 decimal places)
        decimal_str = f"{decimal_part:.10f}".rstrip('0').rstrip('.')[2:]
        if not decimal_str:
            decimal_str = "0"
        
        words = []
        if integer_part > 0:
            words.append(_english_number_to_words(integer_part))
        else:
            words.append("zero")  # Add "zero" for 0.x
        words.append("point")
        for digit in decimal_str:
            # Use "zero" for digit 0 in decimals (ENGLISH_ONES[0] is empty)
            if digit == '0':
                words.append("zero")
            else:
                words.append(ENGLISH_ONES[int(digit)])
        
        result = " ".join(words)
        return f"minus {result}" if negative else result
    
    n = int(n)
    
    # Handle ordinal for simple numbers (1-19)
    if ordinal and n < 20:
        result = ENGLISH_ORDINAL_ONES[n]
        return f"minus {result}" if negative else result
    
    # Handle ordinal for exact tens (20, 30, ..., 90)
    if ordinal and n <= 90 and n % 10 == 0:
        tens_index = n // 10
        if tens_index < len(ENGLISH_ORDINAL_TENS):
            result = ENGLISH_ORDINAL_TENS[tens_index]
            return f"minus {result}" if negative else result
    
    # Split into groups of three digits
    groups: List[Tuple[int, str]] = []
    scale_index = 0
    
    while n > 0:
        group = n % 1000
        if group > 0:
            scale_word = ENGLISH_SCALES[scale_index]
            groups.append((group, scale_word))
        n //= 1000
        scale_index += 1
    
    groups.reverse()
    
    # Convert each group
    result_parts = []
    for group, scale in groups:
        group_words = _english_number_to_words_under_1000(group)
        if scale:
            group_words = f"{group_words} {scale}"
        result_parts.append(group_words)
    
    result = " ".join(result_parts)
    
    # Apply ordinal suffix if needed
    if ordinal:
        result = _make_ordinal_english(result, groups[-1][0] if groups else 0)
    
    return f"minus {result}" if negative else result


def _make_ordinal_english(words: str, last_group: int) -> str:
    """Convert the last part of words to ordinal form."""
    # Handle scale numbers (thousand, million, etc.)
    for scale in ENGLISH_SCALES[1:]:
        if words.endswith(f" {scale}"):
            ordinal_scale = ENGLISH_ORDINAL_SCALES[ENGLISH_SCALES.index(scale)]
            return words[:-len(scale)-1] + f" {ordinal_scale}"
    
    # Handle tens and ones
    if last_group < 20:
        # Already handled above
        return words
    
    # Replace last word with ordinal
    last_hundred = last_group % 100
    if last_hundred < 20:
        # Replace the ones word with ordinal
        parts = words.rsplit(" ", 1)
        if len(parts) == 2:
            for i, word in enumerate(ENGLISH_ONES[1:20], 1):
                if parts[1] == word:
                    return parts[0] + " " + ENGLISH_ORDINAL_ONES[i]
        return words
    
    # Handle tens
    tens, ones = divmod(last_hundred, 10)
    
    if ones == 0:
        # Replace tens word with ordinal tens
        parts = words.rsplit(" ", 1)
        if len(parts) == 2:
            for i, word in enumerate(ENGLISH_TENS[2:], 2):
                if parts[1] == word:
                    return parts[0] + " " + ENGLISH_ORDINAL_TENS[i]
        return words
    
    # Replace ones word with ordinal
    parts = words.rsplit("-", 1)
    if len(parts) == 2:
        for i, word in enumerate(ENGLISH_ONES[1:], 1):
            if parts[1] == word:
                return parts[0] + "-" + ENGLISH_ORDINAL_ONES[i]
    
    return words


def _chinese_number_to_words(n: Number, ordinal: bool = False) -> str:
    """Convert a number to Chinese words."""
    # Handle negative numbers
    negative = False
    if n < 0:
        negative = True
        n = abs(n)
    
    # Handle zero
    if n == 0:
        result = "零"
        return f"负{result}" if negative else result
    
    # Handle floats
    if isinstance(n, float) and not n.is_integer():
        integer_part = int(n)
        decimal_part = n - integer_part
        # Use format to avoid floating point precision issues (limit to 10 decimal places)
        decimal_str = f"{decimal_part:.10f}".rstrip('0').rstrip('.')[2:]
        if not decimal_str:
            decimal_str = "0"
        
        words = []
        if integer_part > 0:
            words.append(_chinese_number_to_words(integer_part))
        words.append("点")
        for digit in decimal_str:
            words.append(CHINESE_DIGITS[int(digit)])
        
        result = "".join(words)
        return f"负{result}" if negative else result
    
    n = int(n)
    
    result = _chinese_int_to_words(n)
    
    if ordinal:
        result = f"第{result}"
    
    return f"负{result}" if negative else result


def _chinese_int_to_words(n: int) -> str:
    """Convert an integer to Chinese words."""
    if n == 0:
        return "零"
    
    result = []
    
    # Process each scale group (亿, 万, etc.)
    scales = [(100000000, "亿"), (10000, "万")]
    
    for scale_value, scale_word in scales:
        if n >= scale_value:
            scale_part = n // scale_value
            result.append(_chinese_int_to_words_under_scale(scale_part))
            result.append(scale_word)
            n %= scale_value
    
    # Process the remaining part (under 万)
    if n > 0:
        result.append(_chinese_int_to_words_under_10000(n))
    elif not result:
        return "零"
    
    return "".join(result)


def _chinese_int_to_words_under_scale(n: int) -> str:
    """Convert a number under 10000 for scale groups."""
    if n == 0:
        return ""
    return _chinese_int_to_words_under_10000(n)


def _chinese_int_to_words_under_10000(n: int, is_scale_group: bool = False) -> str:
    """Convert a number under 10000 to Chinese words.
    
    Args:
        n: The number to convert
        is_scale_group: If True, this is part of a scale group (万, 亿, etc.)
                        In this case, 10 is written as "十" not "一十"
    """
    if n == 0:
        return ""
    
    result = []
    
    # Thousands
    if n >= 1000:
        qian = n // 1000
        result.append(CHINESE_DIGITS[qian])
        result.append("千")
        n %= 1000
        if n < 100 and n > 0:
            result.append("零")
    
    # Hundreds
    if n >= 100:
        bai = n // 100
        result.append(CHINESE_DIGITS[bai])
        result.append("百")
        n %= 100
        if n < 10 and n > 0:
            result.append("零")
    
    # Tens
    if n >= 10:
        shi = n // 10
        # Only add "一" before "十" if:
        # 1. shi > 1 (e.g., 二十, 三十)
        # 2. There's something before it (e.g., 一百一十)
        # For standalone 10-19 or scale groups like 10万, use just "十"
        if shi > 1:
            result.append(CHINESE_DIGITS[shi])
        elif len(result) > 0:
            # Has hundreds or thousands before, need to add "一"
            result.append(CHINESE_DIGITS[shi])
        result.append("十")
        n %= 10
    
    # Ones
    if n > 0:
        result.append(CHINESE_DIGITS[n])
    
    return "".join(result)


# ============================================================================
# Words to Number Conversion
# ============================================================================

def words_to_number(
    words: str,
    language: Union[Language, str] = Language.ENGLISH
) -> Union[int, float]:
    """
    Convert word representation to a number.
    
    Args:
        words: The word representation of the number
        language: Source language (Language.ENGLISH or Language.CHINESE)
        
    Returns:
        The numeric value
        
    Raises:
        InvalidWordError: If the word format is invalid
        
    Examples:
        >>> words_to_number("one hundred twenty-three")
        123
        >>> words_to_number("一百二十三", Language.CHINESE)
        123
        >>> words_to_number("first")
        1
        >>> words_to_number("one hundred twenty-three point four five")
        123.45
    """
    if isinstance(language, str):
        language = Language(language.lower())
    
    if language == Language.ENGLISH:
        return _english_words_to_number(words)
    elif language == Language.CHINESE:
        return _chinese_words_to_number(words)
    else:
        raise UnsupportedLanguageError(f"Unsupported language: {language}")


def _english_words_to_number(words: str) -> Union[int, float]:
    """Convert English words to a number."""
    words = words.strip().lower()
    
    # Handle "minus" or "negative"
    negative = False
    if words.startswith("minus ") or words.startswith("negative "):
        negative = True
        words = words.split(" ", 1)[1]
    
    # Handle "point" for decimals
    if " point " in words:
        parts = words.split(" point ")
        integer_part = _english_words_to_number(parts[0]) if parts[0] else 0
        decimal_str = parts[1]
        decimal_value = 0.0
        for i, digit_word in enumerate(decimal_str.split()):
            digit = ENGLISH_WORD_TO_NUM.get(digit_word, 0)
            decimal_value += digit * (10 ** -(i + 1))
        result = integer_part + decimal_value
        return -result if negative else result
    
    # Check for ordinal
    words_lower = words.lower()
    if words_lower in ENGLISH_ORDINAL_TO_NUM:
        result = ENGLISH_ORDINAL_TO_NUM[words_lower]
        return -result if negative else result
    
    # Split into words and handle hyphenated numbers
    word_list = []
    for part in words.split():
        if "-" in part:
            word_list.extend(part.split("-"))
        else:
            word_list.append(part)
    
    if not word_list:
        raise InvalidWordError("Empty word string")
    
    # Handle special case: "zero"
    if len(word_list) == 1 and word_list[0] == "zero":
        return 0
    
    # Check for ordinals in compound
    if word_list[-1] in ENGLISH_ORDINAL_TO_NUM:
        # Handle ordinal at end
        ordinal_val = ENGLISH_ORDINAL_TO_NUM[word_list[-1]]
        if len(word_list) == 1:
            return -ordinal_val if negative else ordinal_val
        # Need to handle compound ordinal like "twenty-first"
        # For now, just return the ordinal value
    
    result = 0
    current = 0
    
    for word in word_list:
        if word == "hundred":
            if current == 0:
                current = 100
            else:
                current *= 100
        elif word in ENGLISH_SCALES:
            scale = 10 ** (ENGLISH_SCALES.index(word) * 3)
            if current == 0:
                current = 1
            current *= scale
            result += current
            current = 0
        elif word in ENGLISH_WORD_TO_NUM:
            current += ENGLISH_WORD_TO_NUM[word]
        elif word in ENGLISH_ORDINAL_TO_NUM:
            current += ENGLISH_ORDINAL_TO_NUM[word]
        elif word not in ["and", "a"]:
            raise InvalidWordError(f"Unknown word: {word}")
    
    result += current
    
    return -result if negative else result


def _chinese_words_to_number(words: str) -> Union[int, float]:
    """Convert Chinese words to a number."""
    words = words.strip()
    
    # Handle "负" (negative)
    negative = False
    if words.startswith("负"):
        negative = True
        words = words[1:]
    
    # Handle ordinal "第"
    if words.startswith("第"):
        words = words[1:]
        if words.endswith("个"):
            words = words[:-1]
    
    # Handle "点" (decimal point)
    if "点" in words:
        parts = words.split("点")
        integer_part = _chinese_words_to_number(parts[0]) if parts[0] else 0
        decimal_str = parts[1] if len(parts) > 1 else ""
        decimal_value = 0.0
        for i, char in enumerate(decimal_str):
            if char in CHINESE_DIGITS:
                decimal_value += CHINESE_WORD_TO_NUM[char] * (10 ** -(i + 1))
        result = integer_part + decimal_value
        return -result if negative else result
    
    # Handle zero
    if words == "零":
        return 0
    
    # Parse the number
    result = 0
    
    # Process scales from largest to smallest
    # Check for 兆 (trillion)
    if "兆" in words:
        parts = words.split("兆", 1)
        result += _chinese_words_to_number(parts[0]) * 1000000000000
        words = parts[1] if len(parts) > 1 else ""
    
    # Check for 亿 (hundred million)
    if "亿" in words:
        parts = words.split("亿", 1)
        result += _chinese_words_to_number(parts[0]) * 100000000
        words = parts[1] if len(parts) > 1 else ""
    
    # Check for 万 (ten thousand)
    if "万" in words:
        parts = words.split("万", 1)
        result += _chinese_words_to_number(parts[0]) * 10000
        words = parts[1] if len(parts) > 1 else ""
    
    # Process remaining (under 万)
    if words:
        result += _chinese_parse_under_10000(words)
    
    return -result if negative else result


def _chinese_parse_under_10000(words: str) -> int:
    """Parse Chinese words under 10000."""
    result = 0
    
    # Handle 千 (thousand)
    if "千" in words:
        idx = words.index("千")
        if idx > 0:
            digit = CHINESE_WORD_TO_NUM.get(words[idx-1], 1)
            result += digit * 1000
        else:
            result += 1000
        words = words[idx+1:]
    
    # Handle 百 (hundred)
    if "百" in words:
        idx = words.index("百")
        if idx > 0:
            digit = CHINESE_WORD_TO_NUM.get(words[idx-1], 1)
            result += digit * 100
        else:
            result += 100
        words = words[idx+1:]
    
    # Handle 十 (ten)
    if "十" in words:
        idx = words.index("十")
        if idx > 0:
            digit = CHINESE_WORD_TO_NUM.get(words[idx-1], 1)
            result += digit * 10
        else:
            result += 10  # "十" by itself means 10
        words = words[idx+1:]
    
    # Handle remaining ones
    for char in words:
        if char in CHINESE_WORD_TO_NUM and char not in ["零", "十", "百", "千", "万", "亿", "兆"]:
            result += CHINESE_WORD_TO_NUM[char]
            break  # Only add the last digit
    
    return result


# ============================================================================
# Currency Conversion
# ============================================================================

def number_to_currency_words(
    amount: Union[int, float],
    currency: str = "USD",
    language: Union[Language, str] = Language.ENGLISH
) -> str:
    """
    Convert a currency amount to words.
    
    Args:
        amount: The currency amount
        currency: Currency code (USD, EUR, GBP, CNY, JPY)
        language: Target language
        
    Returns:
        The currency amount in words
        
    Examples:
        >>> number_to_currency_words(123.45)
        'one hundred twenty-three dollars and forty-five cents'
        >>> number_to_currency_words(123.45, "CNY", Language.CHINESE)
        '一百二十三元四十五分'
    """
    if isinstance(language, str):
        language = Language(language.lower())
    
    if currency not in ENGLISH_CURRENCY:
        raise ValueError(f"Unsupported currency: {currency}")
    
    # Split into integer and decimal parts
    if isinstance(amount, float):
        integer_part = int(amount)
        decimal_part = int(round((amount - integer_part) * 100))
    else:
        integer_part = amount
        decimal_part = 0
    
    if language == Language.ENGLISH:
        singular, plural, cent_singular, cent_plural = ENGLISH_CURRENCY[currency]
        
        # Build integer part
        if integer_part == 0:
            result = "zero"
        else:
            result = number_to_words(integer_part, language)
        
        # Add currency word
        if integer_part == 1:
            result += f" {singular}"
        else:
            result += f" {plural}"
        
        # Add cents if present
        if decimal_part > 0:
            cent_word = cent_singular if decimal_part == 1 else cent_plural
            result += f" and {number_to_words(decimal_part, language)} {cent_word}"
        
        return result
    
    elif language == Language.CHINESE:
        _, _, fen_word, _ = CHINESE_CURRENCY[currency]
        yuan_word = CHINESE_CURRENCY[currency][0]
        
        result = number_to_words(integer_part, language)
        result += yuan_word
        
        if decimal_part > 0:
            result += number_to_words(decimal_part, language)
            result += fen_word
        
        return result
    
    else:
        raise UnsupportedLanguageError(f"Unsupported language: {language}")


# ============================================================================
# Utility Functions
# ============================================================================

def is_valid_number_word(word: str, language: Union[Language, str] = Language.ENGLISH) -> bool:
    """
    Check if a word represents a valid number word.
    
    Args:
        word: The word to check
        language: The language to check against
        
    Returns:
        True if the word is a valid number word
    """
    if isinstance(language, str):
        language = Language(language.lower())
    
    word_lower = word.lower()
    
    if language == Language.ENGLISH:
        return (
            word_lower in ENGLISH_WORD_TO_NUM or
            word_lower in ENGLISH_ORDINAL_TO_NUM or
            word_lower in ["and", "point", "minus", "negative", "zero"]
        )
    elif language == Language.CHINESE:
        return word in CHINESE_WORD_TO_NUM or word in ["点", "负", "第"]
    
    return False


def get_number_words_list(language: Union[Language, str] = Language.ENGLISH) -> List[str]:
    """
    Get a list of all valid number words for a language.
    
    Args:
        language: The language to get words for
        
    Returns:
        List of valid number words
    """
    if isinstance(language, str):
        language = Language(language.lower())
    
    if language == Language.ENGLISH:
        words = list(ENGLISH_WORD_TO_NUM.keys()) + list(ENGLISH_ORDINAL_TO_NUM.keys())
        words.extend(["and", "point", "minus", "negative", "zero"])
        return sorted(set(words))
    elif language == Language.CHINESE:
        words = list(CHINESE_WORD_TO_NUM.keys())
        words.extend(["点", "负", "第"])
        return sorted(set(words))
    
    return []


# ============================================================================
# Convenience Aliases
# ============================================================================

def to_words(number: Number, language: str = "en", ordinal: bool = False) -> str:
    """Convenience alias for number_to_words."""
    lang = Language.CHINESE if language.lower() in ["zh", "chinese"] else Language.ENGLISH
    return number_to_words(number, lang, ordinal)


def from_words(words: str, language: str = "en") -> Union[int, float]:
    """Convenience alias for words_to_number."""
    lang = Language.CHINESE if language.lower() in ["zh", "chinese"] else Language.ENGLISH
    return words_to_number(words, lang)


# ============================================================================
# Main Entry Point
# ============================================================================

if __name__ == "__main__":
    # Demo
    print("=== Number to Words Examples ===")
    print(f"123 → {number_to_words(123)}")
    print(f"1234567 → {number_to_words(1234567)}")
    print(f"123.45 → {number_to_words(123.45)}")
    print(f"-42 → {number_to_words(-42)}")
    print(f"21st → {number_to_words(21, ordinal=True)}")
    
    print("\n=== Chinese Examples ===")
    print(f"123 → {number_to_words(123, Language.CHINESE)}")
    print(f"12345 → {number_to_words(12345, Language.CHINESE)}")
    print(f"第123 → {number_to_words(123, Language.CHINESE, ordinal=True)}")
    
    print("\n=== Words to Number Examples ===")
    print(f"'one hundred twenty-three' → {words_to_number('one hundred twenty-three')}")
    print(f"'two million three hundred thousand' → {words_to_number('two million three hundred thousand')}")
    print(f"'一百二十三' → {words_to_number('一百二十三', Language.CHINESE)}")
    
    print("\n=== Currency Examples ===")
    print(f"$123.45 → {number_to_currency_words(123.45, 'USD')}")
    print(f"¥123.45 → {number_to_currency_words(123.45, 'CNY', Language.CHINESE)}")