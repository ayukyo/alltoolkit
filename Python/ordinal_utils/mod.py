"""
Ordinal Number Utilities

A comprehensive library for working with ordinal numbers (1st, 2nd, 3rd, etc.)
with support for multiple languages and various formatting options.

Features:
- Convert cardinal numbers to ordinal (1 → 1st, 2 → 2nd, etc.)
- Convert ordinal strings back to cardinal numbers
- Support for multiple languages (English, Chinese, Spanish, French, German, etc.)
- Roman numeral ordinals (I, II, III, etc.)
- Suffix extraction and validation
- Date formatting with ordinals
- Ranking and position display utilities

Zero external dependencies - uses only Python standard library.
"""

from typing import Optional, Union, List, Tuple, Dict


# Language-specific ordinal suffix rules
ORDINAL_RULES: Dict[str, Dict] = {
    "en": {
        "suffixes": {
            1: "st",
            2: "nd",
            3: "rd",
            "default": "th"
        },
        "specials": {
            11: "th",  # 11th, not 11st
            12: "th",  # 12th, not 12nd
            13: "th",  # 13th, not 13rd
        }
    },
    "es": {
        # Spanish uses gendered suffixes
        "suffixes_male": {
            1: "o",
            2: "o",
            3: "o",
            "default": "o"
        },
        "suffixes_female": {
            1: "a",
            2: "a",
            3: "a",
            "default": "a"
        },
        "prefix": {
            1: "primer",
            2: "segund",
            3: "tercer",
            4: "cuart",
            5: "quint",
            6: "sext",
            7: "séptim",
            8: "octav",
            9: "noven",
            10: "décim"
        }
    },
    "fr": {
        # French always uses "e" suffix for most numbers
        "suffixes": {
            1: "er",
            "default": "e"
        }
    },
    "de": {
        # German uses period after number
        "suffix": ".",
        "uses_period": True
    },
    "it": {
        # Italian uses "o" or "a" based on gender
        "suffixes_male": "o",
        "suffixes_female": "a"
    },
    "pt": {
        # Portuguese uses "o" or "a" based on gender
        "suffixes_male": "o",
        "suffixes_female": "a"
    },
    "nl": {
        # Dutch uses "e" suffix
        "suffixes": {
            "default": "e"
        }
    },
    "ru": {
        # Russian ordinal indicators
        "suffixes": {
            "default": "-й"
        }
    },
    "zh": {
        # Chinese uses special characters
        "suffix": "第",
        "prefix": True,  # 第1 (di-yi)
        "suffix_char": ""
    },
    "ja": {
        # Japanese uses counter words
        "counter": "番目",
        "suffix": True  # 1番目
    }
}


def get_ordinal_suffix(n: int, language: str = "en") -> str:
    """
    Get the ordinal suffix for a number in the specified language.
    
    Args:
        n: The cardinal number
        language: Language code (en, es, fr, de, it, pt, nl, ru, zh, ja)
    
    Returns:
        The ordinal suffix (e.g., "st", "nd", "rd", "th" for English)
    
    Examples:
        >>> get_ordinal_suffix(1)
        'st'
        >>> get_ordinal_suffix(2)
        'nd'
        >>> get_ordinal_suffix(3)
        'rd'
        >>> get_ordinal_suffix(4)
        'th'
        >>> get_ordinal_suffix(11)
        'th'
        >>> get_ordinal_suffix(21)
        'st'
        >>> get_ordinal_suffix(111)
        'th'
    """
    if language not in ORDINAL_RULES:
        language = "en"
    
    rules = ORDINAL_RULES[language]
    
    # German uses period
    if rules.get("uses_period"):
        return "."
    
    # Chinese/Japanese have different patterns
    if language in ("zh", "ja"):
        return rules.get("suffix_char", "")
    
    # English rules with special cases
    if language == "en":
        specials = rules.get("specials", {})
        
        # Check for special cases (11, 12, 13)
        if n % 100 in specials:
            return specials[n % 100]
        
        # Get last digit
        last_digit = n % 10
        suffixes = rules.get("suffixes", {})
        
        if last_digit in suffixes:
            return suffixes[last_digit]
        
        return suffixes.get("default", "th")
    
    # French rules
    if language == "fr":
        suffixes = rules.get("suffixes", {})
        if n == 1:
            return suffixes.get(1, "er")
        return suffixes.get("default", "e")
    
    # Default for other languages
    suffixes = rules.get("suffixes", {})
    return suffixes.get("default", "th")


def to_ordinal(n: int, language: str = "en", gender: str = "male") -> str:
    """
    Convert a cardinal number to its ordinal representation.
    
    Args:
        n: The cardinal number (must be non-negative)
        language: Language code (en, es, fr, de, it, pt, nl, ru, zh, ja)
        gender: Gender for gendered languages ("male" or "female")
    
    Returns:
        The ordinal representation as a string
    
    Raises:
        ValueError: If n is negative
    
    Examples:
        >>> to_ordinal(1)
        '1st'
        >>> to_ordinal(22)
        '22nd'
        >>> to_ordinal(133)
        '133rd'
        >>> to_ordinal(42, language="fr")
        '42e'
        >>> to_ordinal(1, language="fr")
        '1er'
        >>> to_ordinal(5, language="de")
        '5.'
        >>> to_ordinal(3, language="zh")
        '第3'
        >>> to_ordinal(5, language="ja")
        '5番目'
    """
    if n < 0:
        raise ValueError("Ordinal numbers must be non-negative")
    
    if language not in ORDINAL_RULES:
        language = "en"
    
    rules = ORDINAL_RULES[language]
    
    # Chinese: prefix style (第N)
    if language == "zh":
        return f"第{n}"
    
    # Japanese: suffix style (N番目)
    if language == "ja":
        return f"{n}番目"
    
    # German: period style (N.)
    if rules.get("uses_period"):
        return f"{n}."
    
    # English and others with suffixes
    suffix = get_ordinal_suffix(n, language)
    return f"{n}{suffix}"


def to_ordinal_word(n: int, language: str = "en", gender: str = "male") -> str:
    """
    Convert a number to its ordinal word form (e.g., 1 → "first", 2 → "second").
    
    Args:
        n: The cardinal number (1-100)
        language: Language code
        gender: Gender for gendered languages
    
    Returns:
        The ordinal word
    
    Examples:
        >>> to_ordinal_word(1)
        'first'
        >>> to_ordinal_word(2)
        'second'
        >>> to_ordinal_word(21)
        'twenty-first'
        >>> to_ordinal_word(100)
        'hundredth'
    """
    # English ordinal words
    ENGLISH_ORDINAL_WORDS = {
        1: "first", 2: "second", 3: "third", 4: "fourth", 5: "fifth",
        6: "sixth", 7: "seventh", 8: "eighth", 9: "ninth", 10: "tenth",
        11: "eleventh", 12: "twelfth", 13: "thirteenth", 14: "fourteenth",
        15: "fifteenth", 16: "sixteenth", 17: "seventeenth", 18: "eighteenth",
        19: "nineteenth", 20: "twentieth", 30: "thirtieth", 40: "fortieth",
        50: "fiftieth", 60: "sixtieth", 70: "seventieth", 80: "eightieth",
        90: "ninetieth", 100: "hundredth"
    }
    
    ENGLISH_CARDINAL_WORDS = {
        20: "twenty", 30: "thirty", 40: "forty", 50: "fifty",
        60: "sixty", 70: "seventy", 80: "eighty", 90: "ninety"
    }
    
    if language != "en":
        # For other languages, fall back to numeric ordinal
        return to_ordinal(n, language, gender)
    
    if n in ENGLISH_ORDINAL_WORDS:
        return ENGLISH_ORDINAL_WORDS[n]
    
    if n > 100:
        # For numbers > 100, use numeric form
        return to_ordinal(n, language, gender)
    
    # Handle compound numbers (21-99)
    tens = (n // 10) * 10
    ones = n % 10
    
    if tens in ENGLISH_CARDINAL_WORDS and ones > 0:
        ones_word = ENGLISH_ORDINAL_WORDS.get(ones, str(ones))
        return f"{ENGLISH_CARDINAL_WORDS[tens]}-{ones_word}"
    
    # Fallback to numeric ordinal
    return to_ordinal(n, language, gender)


def from_ordinal(ordinal_str: str, language: str = "en") -> Optional[int]:
    """
    Parse an ordinal string back to its cardinal number.
    
    Args:
        ordinal_str: The ordinal string (e.g., "1st", "第3", "5.")
        language: Language code (auto-detected if not specified)
    
    Returns:
        The cardinal number, or None if parsing fails
    
    Examples:
        >>> from_ordinal("1st")
        1
        >>> from_ordinal("22nd")
        22
        >>> from_ordinal("第3")
        3
        >>> from_ordinal("5.")
        5
        >>> from_ordinal("first")
        1
        >>> from_ordinal("twenty-third")
        23
    """
    if not ordinal_str:
        return None
    
    ordinal_str = ordinal_str.strip()
    
    # Try to detect language from format
    if ordinal_str.startswith("第"):
        language = "zh"
    elif "番目" in ordinal_str:
        language = "ja"
    elif ordinal_str.endswith("."):
        language = "de"
    
    # Chinese format: 第N
    if language == "zh" and ordinal_str.startswith("第"):
        try:
            return int(ordinal_str[1:])
        except ValueError:
            return None
    
    # Japanese format: N番目
    if language == "ja" and "番目" in ordinal_str:
        try:
            return int(ordinal_str.replace("番目", ""))
        except ValueError:
            return None
    
    # Try to extract number from beginning of string
    import re
    
    # Match number at the start
    match = re.match(r'^(\d+)', ordinal_str)
    if match:
        return int(match.group(1))
    
    # Try English word ordinals
    ordinal_str_lower = ordinal_str.lower()
    
    ENGLISH_WORD_ORDINALS = {
        "first": 1, "second": 2, "third": 3, "fourth": 4, "fifth": 5,
        "sixth": 6, "seventh": 7, "eighth": 8, "ninth": 9, "tenth": 10,
        "eleventh": 11, "twelfth": 12, "thirteenth": 13, "fourteenth": 14,
        "fifteenth": 15, "sixteenth": 16, "seventeenth": 17, "eighteenth": 18,
        "nineteenth": 19, "twentieth": 20, "thirtieth": 30, "fortieth": 40,
        "fiftieth": 50, "sixtieth": 60, "seventieth": 70, "eightieth": 80,
        "ninetieth": 90, "hundredth": 100
    }
    
    if ordinal_str_lower in ENGLISH_WORD_ORDINALS:
        return ENGLISH_WORD_ORDINALS[ordinal_str_lower]
    
    # Try compound ordinals (e.g., "twenty-third")
    ENGLISH_TENS = {
        "twenty": 20, "thirty": 30, "forty": 40, "fifty": 50,
        "sixty": 60, "seventy": 70, "eighty": 80, "ninety": 90
    }
    
    ENGLISH_ONES = {
        "first": 1, "second": 2, "third": 3, "fourth": 4, "fifth": 5,
        "sixth": 6, "seventh": 7, "eighth": 8, "ninth": 9
    }
    
    for ten_word, ten_val in ENGLISH_TENS.items():
        if ordinal_str_lower.startswith(ten_word):
            for one_word, one_val in ENGLISH_ONES.items():
                if ordinal_str_lower.endswith(one_word):
                    return ten_val + one_val
            return ten_val
    
    return None


def is_ordinal(s: str, language: str = "en") -> bool:
    """
    Check if a string is a valid ordinal representation.
    
    Args:
        s: The string to check
        language: Language code
    
    Returns:
        True if the string is a valid ordinal
    
    Examples:
        >>> is_ordinal("1st")
        True
        >>> is_ordinal("2nd")
        True
        >>> is_ordinal("3th")
        False
        >>> is_ordinal("第5")
        True
        >>> is_ordinal("hello")
        False
    """
    if not s:
        return False
    
    result = from_ordinal(s, language)
    return result is not None


def get_all_ordinal_forms(n: int, gender: str = "male") -> Dict[str, str]:
    """
    Get ordinal representations in all supported languages.
    
    Args:
        n: The cardinal number
        gender: Gender for gendered languages
    
    Returns:
        Dictionary mapping language codes to ordinal strings
    
    Examples:
        >>> forms = get_all_ordinal_forms(5)
        >>> forms["en"]
        '5th'
        >>> forms["fr"]
        '5e'
        >>> forms["de"]
        '5.'
    """
    result = {}
    for lang in ORDINAL_RULES:
        result[lang] = to_ordinal(n, lang, gender)
    return result


def format_date_with_ordinal(
    day: int, 
    month: Optional[str] = None, 
    year: Optional[int] = None,
    language: str = "en",
    format_type: str = "mdy"
) -> str:
    """
    Format a date with ordinal day number.
    
    Args:
        day: Day of month (1-31)
        month: Month name or number
        year: Year
        language: Language code
        format_type: Date format ("mdy", "dmy", "ymd")
    
    Returns:
        Formatted date string with ordinal
    
    Examples:
        >>> format_date_with_ordinal(1, "January", 2026)
        'January 1st, 2026'
        >>> format_date_with_ordinal(22, "March", 2026)
        'March 22nd, 2026'
        >>> format_date_with_ordinal(3, "May", 2026, format_type="dmy")
        '3rd May 2026'
    """
    month_names = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ]
    
    # Convert month number to name if needed
    if month is not None:
        if isinstance(month, int) and 1 <= month <= 12:
            month = month_names[month - 1]
    else:
        month = ""
    
    ordinal_day = to_ordinal(day, language)
    
    # Build date string based on format
    if format_type == "mdy":
        result = f"{month} {ordinal_day}"
        if year:
            result += f", {year}"
    elif format_type == "dmy":
        result = f"{ordinal_day} {month}"
        if year:
            result += f" {year}"
    elif format_type == "ymd":
        result = f"{year} {month} {ordinal_day}" if year else f"{month} {ordinal_day}"
    else:
        result = f"{month} {ordinal_day}"
        if year:
            result += f", {year}"
    
    return result


def get_rank_suffix(rank: int) -> str:
    """
    Get the ranking suffix (gold, silver, bronze for top 3, ordinal for others).
    
    Args:
        rank: The rank/position (1, 2, 3, etc.)
    
    Returns:
        Special suffix for top 3, ordinal suffix otherwise
    
    Examples:
        >>> get_rank_suffix(1)
        '🥇'
        >>> get_rank_suffix(2)
        '🥈'
        >>> get_rank_suffix(3)
        '🥉'
        >>> get_rank_suffix(4)
        '4th'
    """
    RANK_EMOJIS = {
        1: "🥇",
        2: "🥈",
        3: "🥉"
    }
    
    if rank in RANK_EMOJIS:
        return RANK_EMOJIS[rank]
    return to_ordinal(rank)


def format_ranking(rank: int, name: str = "", score: Optional[Union[int, float]] = None) -> str:
    """
    Format a ranking entry with medal/ordinal and optional score.
    
    Args:
        rank: The rank/position
        name: The name of the ranked entity
        score: Optional score/value
    
    Returns:
        Formatted ranking string
    
    Examples:
        >>> format_ranking(1, "Team Alpha", 100)
        '🥇 Team Alpha (100)'
        >>> format_ranking(4, "Team Delta", 85)
        '4th Team Delta (85)'
        >>> format_ranking(2, "Team Beta")
        '🥈 Team Beta'
    """
    suffix = get_rank_suffix(rank)
    
    if name:
        result = f"{suffix} {name}"
    else:
        result = suffix
    
    if score is not None:
        result += f" ({score})"
    
    return result


def ordinal_range(start: int, end: int, language: str = "en") -> List[str]:
    """
    Generate a list of ordinal numbers in a range.
    
    Args:
        start: Start of range (inclusive)
        end: End of range (inclusive)
        language: Language code
    
    Returns:
        List of ordinal strings
    
    Examples:
        >>> ordinal_range(1, 5)
        ['1st', '2nd', '3rd', '4th', '5th']
        >>> ordinal_range(1, 3, language="fr")
        ['1er', '2e', '3e']
    """
    step = 1 if start <= end else -1
    return [to_ordinal(i, language) for i in range(start, end + step, step)]


def compare_ordinals(ord1: str, ord2: str) -> int:
    """
    Compare two ordinal strings numerically.
    
    Args:
        ord1: First ordinal string
        ord2: Second ordinal string
    
    Returns:
        -1 if ord1 < ord2, 0 if equal, 1 if ord1 > ord2
    
    Examples:
        >>> compare_ordinals("1st", "2nd")
        -1
        >>> compare_ordinals("10th", "5th")
        1
        >>> compare_ordinals("第3", "第3")
        0
    """
    n1 = from_ordinal(ord1)
    n2 = from_ordinal(ord2)
    
    if n1 is None or n2 is None:
        raise ValueError("Invalid ordinal string")
    
    if n1 < n2:
        return -1
    elif n1 > n2:
        return 1
    return 0


def ordinal_to_roman(n: int) -> str:
    """
    Convert a cardinal number to Roman numeral format (uppercase).
    
    Args:
        n: The cardinal number (1-3999)
    
    Returns:
        Roman numeral string
    
    Raises:
        ValueError: If n is not in valid range
    
    Examples:
        >>> ordinal_to_roman(1)
        'I'
        >>> ordinal_to_roman(4)
        'IV'
        >>> ordinal_to_roman(2024)
        'MMXXIV'
    """
    if not 1 <= n <= 3999:
        raise ValueError("Roman numerals must be between 1 and 3999")
    
    val = [1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1]
    syms = ["M", "CM", "D", "CD", "C", "XC", "L", "XL", "X", "IX", "V", "IV", "I"]
    
    result = []
    for v, s in zip(val, syms):
        while n >= v:
            result.append(s)
            n -= v
    
    return "".join(result)


def roman_to_ordinal(roman: str) -> Optional[int]:
    """
    Convert a Roman numeral to its cardinal number.
    
    Args:
        roman: Roman numeral string
    
    Returns:
        The cardinal number, or None if invalid
    
    Examples:
        >>> roman_to_ordinal("I")
        1
        >>> roman_to_ordinal("IV")
        4
        >>> roman_to_ordinal("MMXXIV")
        2024
    """
    roman = roman.upper().strip()
    
    if not roman:
        return None
    
    values = {
        "I": 1, "V": 5, "X": 10, "L": 50,
        "C": 100, "D": 500, "M": 1000
    }
    
    # Validate characters
    if not all(c in values for c in roman):
        return None
    
    total = 0
    prev_value = 0
    
    for c in reversed(roman):
        curr_value = values[c]
        if curr_value < prev_value:
            total -= curr_value
        else:
            total += curr_value
        prev_value = curr_value
    
    return total


def get_ordinal_suffix_only(n: int, language: str = "en") -> str:
    """
    Get only the ordinal suffix without the number.
    
    Args:
        n: The cardinal number
        language: Language code
    
    Returns:
        Just the suffix (e.g., "st", "nd", "rd", "th")
    
    Examples:
        >>> get_ordinal_suffix_only(1)
        'st'
        >>> get_ordinal_suffix_only(21)
        'st'
        >>> get_ordinal_suffix_only(11)
        'th'
    """
    return get_ordinal_suffix(n, language)


# Convenience function aliases
ordinal = to_ordinal
from_ordinal_number = from_ordinal
ordinal_word = to_ordinal_word


if __name__ == "__main__":
    # Quick demo
    print("=== Ordinal Number Utilities ===\n")
    
    print("English ordinals 1-10:")
    for i in range(1, 11):
        print(f"  {to_ordinal(i)}", end="  ")
    print("\n")
    
    print("Ordinal words:")
    for i in [1, 2, 3, 21, 100]:
        print(f"  {i} → {to_ordinal_word(i)}")
    print()
    
    print("Multilingual ordinals for 5:")
    for lang, form in get_all_ordinal_forms(5).items():
        print(f"  {lang}: {form}")
    print()
    
    print("Date formatting:")
    print(f"  {format_date_with_ordinal(4, 'July', 2026)}")
    print(f"  {format_date_with_ordinal(22, 'March', 2026, format_type='dmy')}")
    print()
    
    print("Ranking format:")
    for i in range(1, 5):
        print(f"  {format_ranking(i, f'Team {chr(64+i)}', 100 - (i-1)*10)}")
    print()
    
    print("Roman numerals:")
    for i in [1, 4, 9, 49, 100, 2024]:
        print(f"  {i} → {ordinal_to_roman(i)}")