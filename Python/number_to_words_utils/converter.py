"""
Number to Words Converter

Core implementation for converting numbers to word representations.
Supports English, Chinese (Simplified), Japanese, Korean, Spanish, French, and German.
"""

from typing import Union, Optional, Tuple
from decimal import Decimal, InvalidOperation


# Language definitions
ENGLISH = {
    "ones": ["", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine",
             "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen",
             "seventeen", "eighteen", "nineteen"],
    "tens": ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"],
    "scales": ["", "thousand", "million", "billion", "trillion", "quadrillion", "quintillion",
               "sextillion", "septillion", "octillion", "nonillion", "decillion"],
    "hundred": "hundred",
    "negative": "negative",
    "and": "and",
    "point": "point",
    "zero": "zero",
    "currency": {
        "major": ("dollar", "dollars"),
        "minor": ("cent", "cents"),
        "major_symbol": "$",
    },
    "ordinal": {
        "ones": ["", "first", "second", "third", "fourth", "fifth", "sixth", "seventh",
                 "eighth", "ninth", "tenth", "eleventh", "twelfth", "thirteenth", "fourteenth",
                 "fifteenth", "sixteenth", "seventeenth", "eighteenth", "nineteenth"],
        "tens": ["", "", "twentieth", "thirtieth", "fortieth", "fiftieth", "sixtieth",
                 "seventieth", "eightieth", "ninetieth"],
        "hundredth": "hundredth",
        "thousandth": "thousandth",
        "millionth": "millionth",
        "billionth": "billionth",
    }
}

CHINESE = {
    "digits": ["零", "一", "二", "三", "四", "五", "六", "七", "八", "九"],
    "units": ["", "十", "百", "千"],
    "scales": ["", "万", "亿", "兆", "京", "垓"],
    "negative": "负",
    "point": "点",
    "zero": "零",
    "ten_special": True,  # 一十 vs 十 for numbers 10-19
    "currency": {
        "major": ("元", "元"),
        "minor": ("角", "分"),
        "major_symbol": "￥",
        "digits": ["零", "壹", "贰", "叁", "肆", "伍", "陆", "柒", "捌", "玖"],
        "units": ["", "拾", "佰", "仟"],
    },
    "ordinal_prefix": "第",
}

JAPANESE = {
    "digits": ["零", "一", "二", "三", "四", "五", "六", "七", "八", "九"],
    "units": ["", "十", "百", "千"],
    "scales": ["", "万", "億", "兆", "京"],
    "negative": "マイナス",
    "point": "点",
    "zero": "零",
    "ten_special": True,
    "currency": {
        "major": ("円", "円"),
        "minor": None,
        "major_symbol": "￥",
    },
    "ordinal_prefix": "第",
}

KOREAN = {
    "digits_native": ["", "하나", "둘", "셋", "넷", "다섯", "여섯", "일곱", "여덟", "아홉", "열"],
    "digits_sino": ["", "일", "이", "삼", "사", "오", "육", "칠", "팔", "구"],
    "units_native": ["", "열", "스물", "서른", "마흔", "쉰", "예순", "일흔", "여든", "아흔"],
    "units_sino": ["", "십", "백", "천"],
    "scales": ["", "만", "억", "조", "경"],
    "negative": "마이너스",
    "point": "점",
    "zero": "영",
    "use_sino": True,  # Use Sino-Korean for large numbers
    "currency": {
        "major": ("원", "원"),
        "minor": None,
        "major_symbol": "￦",
    },
    "ordinal_suffix": "번째",
}

SPANISH = {
    "ones": ["", "uno", "dos", "tres", "cuatro", "cinco", "seis", "siete", "ocho", "nueve",
             "diez", "once", "doce", "trece", "catorce", "quince", "dieciséis", "diecisiete",
             "dieciocho", "diecinueve"],
    "tens": ["", "", "veinte", "treinta", "cuarenta", "cincuenta", "sesenta", "setenta",
             "ochenta", "noventa"],
    "hundreds": ["", "ciento", "doscientos", "trescientos", "cuatrocientos", "quinientos",
                 "seiscientos", "setecientos", "ochocientos", "novecientos"],
    "scales": ["", "mil", "millón", "mil millones", "billón", "mil billones", "trillón"],
    "scales_plural": ["", "mil", "millones", "mil millones", "billones", "mil billones", "trillones"],
    "hundred": "cien",
    "negative": "menos",
    "and": "y",
    "point": "punto",
    "zero": "cero",
    "twenty_special": True,  # veintiuno, veintidós, etc.
    "twenty_ones": ["", "veintiuno", "veintidós", "veintitrés", "veinticuatro", "veinticinco",
                    "veintiséis", "veintisiete", "veintiocho", "veintinueve"],
    "currency": {
        "major": ("euro", "euros"),
        "minor": ("céntimo", "céntimos"),
        "major_symbol": "€",
    },
    "ordinal": {
        "ones": ["", "primero", "segundo", "tercero", "cuarto", "quinto", "sexto", "séptimo",
                 "octavo", "noveno", "décimo"],
    }
}

FRENCH = {
    "ones": ["", "un", "deux", "trois", "quatre", "cinq", "six", "sept", "huit", "neuf",
             "dix", "onze", "douze", "treize", "quatorze", "quinze", "seize", "dix-sept",
             "dix-huit", "dix-neuf"],
    "tens": ["", "", "vingt", "trente", "quarante", "cinquante", "soixante", "soixante",
             "quatre-vingt", "quatre-vingt"],
    "scales": ["", "mille", "million", "milliard", "billion"],
    "scales_plural": ["", "mille", "millions", "milliards", "billions"],
    "hundred": "cent",
    "hundreds": "cents",
    "negative": "moins",
    "and": "et",
    "point": "virgule",
    "zero": "zéro",
    "seventy_special": True,  # soixante-dix, etc.
    "eighty_special": True,   # quatre-vingts
    "ninety_special": True,   # quatre-vingt-dix
    "currency": {
        "major": ("euro", "euros"),
        "minor": ("centime", "centimes"),
        "major_symbol": "€",
    },
    "ordinal": {
        "ones": ["", "premier", "deuxième", "troisième", "quatrième", "cinquième",
                 "sixième", "septième", "huitième", "neuvième", "dixième"],
    }
}

GERMAN = {
    "ones": ["", "eins", "zwei", "drei", "vier", "fünf", "sechs", "sieben", "acht", "neun",
             "zehn", "elf", "zwölf", "dreizehn", "vierzehn", "fünfzehn", "sechzehn",
             "siebzehn", "achtzehn", "neunzehn"],
    "tens": ["", "", "zwanzig", "dreißig", "vierzig", "fünfzig", "sechzig", "siebzig",
             "achtzig", "neunzig"],
    "scales": ["", "tausend", "Million", "Milliarde", "Billion"],
    "scales_plural": ["", "tausend", "Millionen", "Milliarden", "Billionen"],
    "hundred": "hundert",
    "negative": "minus",
    "and": "und",
    "point": "Komma",
    "zero": "null",
    "currency": {
        "major": ("Euro", "Euro"),
        "minor": ("Cent", "Cent"),
        "major_symbol": "€",
    },
    "ordinal": {
        "ones": ["", "erste", "zweite", "dritte", "vierte", "fünfte", "sechste", "siebte",
                 "achte", "neunte", "zehnte"],
        "tens": ["", "", "zwanzigste", "dreißigste", "vierzigste", "fünfzigste", "sechzigste",
                 "siebzigste", "achtzigste", "neunzigste"],
        "hundredth": "hundertste",
        "thousandth": "tausendste",
    }
}

LANGUAGES = {
    "en": ENGLISH,
    "english": ENGLISH,
    "zh": CHINESE,
    "chinese": CHINESE,
    "ja": JAPANESE,
    "japanese": JAPANESE,
    "ko": KOREAN,
    "korean": KOREAN,
    "es": SPANISH,
    "spanish": SPANISH,
    "fr": FRENCH,
    "french": FRENCH,
    "de": GERMAN,
    "german": GERMAN,
}


def get_supported_languages() -> list:
    """Return list of supported language codes."""
    return list(set(LANGUAGES.keys()))


def _parse_number(num: Union[int, float, str, Decimal]) -> Tuple[int, Optional[str]]:
    """Parse input to integer and optional decimal part."""
    if isinstance(num, str):
        num = num.strip()
        if num.startswith('+'):
            num = num[1:]
    
    try:
        dec = Decimal(str(num))
    except (InvalidOperation, ValueError):
        raise ValueError(f"Invalid number: {num}")
    
    if dec.is_infinite() or dec.is_nan():
        raise ValueError(f"Cannot convert {num} to words")
    
    # Check range (limit to 10^36 for most languages)
    if abs(dec) >= Decimal('1e36'):
        raise ValueError(f"Number too large: {num}")
    
    sign = -1 if dec < 0 else 1
    dec = abs(dec)
    
    int_part = int(dec)
    dec_str = str(dec)
    
    if '.' in dec_str:
        decimal_part = dec_str.split('.')[1].rstrip('0')
    else:
        decimal_part = None
    
    return sign * int_part, decimal_part


def _convert_english(num: int, lang: dict) -> str:
    """Convert integer to English words."""
    if num == 0:
        return lang["zero"]
    
    parts = []
    
    if num < 0:
        parts.append(lang["negative"])
        num = abs(num)
    
    # Group by thousands
    groups = []
    while num > 0:
        groups.append(num % 1000)
        num //= 1000
    
    for i, group in enumerate(reversed(groups)):
        if group == 0:
            continue
        
        scale_idx = len(groups) - 1 - i
        scale = lang["scales"][scale_idx] if scale_idx < len(lang["scales"]) else ""
        
        group_words = _convert_group_english(group, lang)
        
        if scale:
            group_words = f"{group_words} {scale}"
        
        parts.append(group_words.strip())
    
    result = " ".join(parts)
    return result


def _convert_group_english(num: int, lang: dict) -> str:
    """Convert a group of 3 digits to English words."""
    hundreds = num // 100
    remainder = num % 100
    
    parts = []
    
    if hundreds > 0:
        parts.append(f"{lang['ones'][hundreds]} {lang['hundred']}")
    
    if remainder > 0:
        if remainder < 20:
            parts.append(lang["ones"][remainder])
        else:
            tens = remainder // 10
            ones = remainder % 10
            if ones > 0:
                parts.append(f"{lang['tens'][tens]}-{lang['ones'][ones]}")
            else:
                parts.append(lang["tens"][tens])
    
    return " and ".join(parts) if " and " not in " ".join(parts) else " ".join(parts)


def _convert_chinese(num: int, lang: dict, financial: bool = False) -> str:
    """Convert integer to Chinese words."""
    if num == 0:
        return lang["zero"]
    
    digits = lang["digits"]
    units = lang["units"]
    scales = lang["scales"]
    
    if financial and "currency" in lang and "digits" in lang["currency"]:
        digits = lang["currency"]["digits"]
        units = lang["currency"]["units"]
    
    parts = []
    
    if num < 0:
        parts.append(lang["negative"])
        num = abs(num)
    
    # Handle special case for numbers 10-19
    if num < 20 and num >= 10 and lang.get("ten_special") and not financial:
        if num == 10:
            return (lang["negative"] + " " if parts else "") + "十"
        else:
            return (lang["negative"] + " " if parts else "") + "十" + digits[num - 10]
    
    # Group by scales (万, 亿, etc.)
    scale_groups = []
    scale_unit = 10000  # Chinese uses 10000 as the major grouping
    
    while num > 0:
        scale_groups.append(num % scale_unit)
        num //= scale_unit
    
    need_zero = False
    
    for i, group in enumerate(reversed(scale_groups)):
        if group == 0:
            if i < len(scale_groups) - 1:  # Not the last group
                need_zero = True
            continue
        
        scale_idx = len(scale_groups) - 1 - i
        
        # Add zero if needed
        if need_zero:
            parts.append(digits[0])
            need_zero = False
        
        group_str = _convert_group_chinese(group, digits, units, lang.get("ten_special", False))
        parts.append(group_str)
        
        if scale_idx > 0 and scale_idx < len(scales):
            parts.append(scales[scale_idx])
    
    return "".join(parts)


def _convert_group_chinese(num: int, digits: list, units: list, ten_special: bool) -> str:
    """Convert a group of up to 4 digits to Chinese words."""
    if num == 0:
        return ""
    
    result = []
    
    # Thousands
    if num >= 1000:
        qian = num // 1000
        result.append(digits[qian] + units[3])
        num %= 1000
    elif result:  # Need zero placeholder
        result.append(digits[0])
    
    # Hundreds
    if num >= 100:
        bai = num // 100
        result.append(digits[bai] + units[2])
        num %= 100
    elif result and num > 0:
        result.append(digits[0])
    
    # Tens
    if num >= 10:
        shi = num // 10
        if ten_special and shi == 1 and not result:
            result.append(units[1])
        else:
            result.append(digits[shi] + units[1])
        num %= 10
    elif result and num > 0:
        result.append(digits[0])
    
    # Ones
    if num > 0:
        result.append(digits[num])
    
    return "".join(result)


def _convert_decimal_english(decimal_part: str, lang: dict) -> str:
    """Convert decimal digits to English words."""
    return " ".join([lang["point"]] + [lang["ones"][int(d)] for d in decimal_part])


def _convert_decimal_chinese(decimal_part: str, lang: dict) -> str:
    """Convert decimal digits to Chinese words."""
    return lang["point"] + "".join([lang["digits"][int(d)] for d in decimal_part])


def _convert_ordinal_english(num: int, lang: dict) -> str:
    """Convert integer to English ordinal words."""
    if num < 0:
        return f"{lang['negative']} {_convert_ordinal_english(-num, lang)}"
    
    if num <= 19:
        return lang["ordinal"]["ones"][num]
    
    if num < 100:
        tens = num // 10
        ones = num % 10
        if ones == 0:
            return lang["ordinal"]["tens"][tens]
        return f"{lang['tens'][tens]}-{lang['ordinal']['ones'][ones]}"
    
    if num < 1000:
        hundreds = num // 100
        remainder = num % 100
        if remainder == 0:
            return f"{lang['ones'][hundreds]} {lang['ordinal']['hundredth']}"
        return f"{lang['ones'][hundreds]} {lang['hundred']} {_convert_ordinal_english(remainder, lang)}"
    
    # For larger numbers, use the cardinal form + "th"
    cardinal = _convert_english(num, lang)
    
    # Simple heuristic: append "th" (not linguistically perfect but functional)
    if cardinal.endswith('y'):
        return cardinal[:-1] + "ieth"
    elif cardinal.endswith(('one', 'three', 'five', 'eight', 'nine')):
        return cardinal + "th"
    elif cardinal.endswith('two'):
        return cardinal[:-1] + "second"
    elif cardinal.endswith('four'):
        return cardinal + "th"
    elif cardinal.endswith('six'):
        return cardinal + "th"
    elif cardinal.endswith('seven'):
        return cardinal + "th"
    else:
        return cardinal + "th"


def _convert_ordinal_chinese(num: int, lang: dict) -> str:
    """Convert integer to Chinese ordinal words."""
    if num < 0:
        return f"{lang['negative']}{lang['ordinal_prefix']}{_convert_chinese(-num, lang)}"
    
    return lang["ordinal_prefix"] + _convert_chinese(num, lang)


def _convert_currency_english(num: Union[int, float, str, Decimal], lang: dict) -> str:
    """Convert number to English currency words."""
    dec = Decimal(str(num))
    
    if dec < 0:
        prefix = f"{lang['negative']} "
        dec = abs(dec)
    else:
        prefix = ""
    
    int_part = int(dec)
    decimal_part = dec - int_part
    cents = int(decimal_part * 100 + Decimal('0.0001'))  # Handle rounding
    
    major_name = lang["currency"]["major"]
    minor_name = lang["currency"]["minor"]
    
    parts = []
    
    if int_part > 0:
        major = major_name[1] if int_part != 1 else major_name[0]
        parts.append(f"{_convert_english(int_part, lang)} {major}")
    
    if cents > 0:
        minor = minor_name[1] if cents != 1 else minor_name[0]
        parts.append(f"{_convert_english(cents, lang)} {minor}")
    elif int_part == 0:
        parts.append(f"{lang['zero']} {minor_name[0]}")
    
    if not parts:
        parts.append(f"{lang['zero']} {major_name[0]}")
    
    return prefix + " and ".join(parts)


def _convert_currency_chinese(num: Union[int, float, str, Decimal], lang: dict) -> str:
    """Convert number to Chinese currency words (人民币大写)."""
    dec = Decimal(str(num))
    
    if dec < 0:
        prefix = lang["negative"]
        dec = abs(dec)
    else:
        prefix = ""
    
    int_part = int(dec)
    decimal_part = dec - int_part
    
    # Get financial digits and units
    fin_digits = lang["currency"]["digits"]
    fin_units = lang["currency"]["units"]
    
    parts = []
    
    if int_part > 0:
        # Convert integer part
        int_str = str(int_part)
        for i, digit in enumerate(int_str):
            pos = len(int_str) - i - 1
            d = int(digit)
            
            if d == 0:
                # Handle zero
                if i < len(int_str) - 1 and int(int_str[i+1]) != 0:
                    parts.append(fin_digits[0])
            else:
                unit_idx = pos % 4
                if unit_idx < len(fin_units):
                    parts.append(fin_digits[d] + fin_units[unit_idx])
                else:
                    parts.append(fin_digits[d])
        
        # Add scale markers (万, 亿)
        num_copy = int_part
        scale_parts = []
        scale_idx = 0
        scales_fin = ["", "万", "亿", "兆"]
        
        while num_copy > 0:
            group = num_copy % 10000
            if scale_idx > 0 and group > 0:
                scale_parts.append(scales_fin[scale_idx])
            num_copy //= 10000
            scale_idx += 1
        
        parts = parts[:len(parts)-len(scale_parts)] + scale_parts[::-1] + parts[len(parts)-len(scale_parts):]
        
        result = "".join(parts)
        parts = [result + lang["currency"]["major"][0]]
    else:
        parts = [fin_digits[0] + lang["currency"]["major"][0]]
    
    # Handle decimal part (角, 分)
    jiao = int(decimal_part * 10)
    fen = int((decimal_part * 100) % 10)
    
    if jiao > 0 or fen > 0:
        if jiao > 0:
            parts.append(fin_digits[jiao] + lang["currency"]["minor"][0])
        if fen > 0:
            parts.append(fin_digits[fen] + lang["currency"]["minor"][1])
    else:
        parts.append("整")
    
    return prefix + "".join(parts)


def _convert_spanish(num: int, lang: dict) -> str:
    """Convert integer to Spanish words."""
    if num == 0:
        return lang["zero"]
    
    parts = []
    
    if num < 0:
        parts.append(lang["negative"])
        num = abs(num)
    
    # Handle special cases
    if num == 100:
        return " ".join(parts + [lang["hundred"]]) if parts else lang["hundred"]
    
    # Handle millions
    if num >= 1000000:
        millions = num // 1000000
        rest = num % 1000000
        
        if millions == 1:
            parts.append("un millón")
        else:
            parts.append(f"{_convert_spanish(millions, lang)} millones")
        
        if rest > 0:
            parts.append(_convert_spanish(rest, lang))
        
        return " ".join(parts)
    
    # Handle thousands (mil is used for any thousand multiplier)
    if num >= 1000:
        thousands = num // 1000
        rest = num % 1000
        
        if thousands == 1:
            parts.append("mil")
        else:
            parts.append(f"{_convert_spanish(thousands, lang)} mil")
        
        if rest > 0:
            parts.append(_convert_spanish(rest, lang))
        
        return " ".join(parts)
    
    # Handle hundreds (only for numbers < 1000)
    if num >= 100:
        hundreds = num // 100
        if hundreds == 1:
            parts.append(lang["hundreds"][1])  # ciento
        else:
            parts.append(lang["hundreds"][hundreds])
        num %= 100
    
    # Handle remaining number
    if num > 0:
        if num < 20:
            parts.append(lang["ones"][num])
        elif num < 30:
            if num == 20:
                parts.append(lang["tens"][2])
            else:
                parts.append(lang["twenty_ones"][num - 20])
        else:
            tens = num // 10
            ones = num % 10
            if ones == 0:
                parts.append(lang["tens"][tens])
            else:
                parts.append(f"{lang['tens'][tens]} y {lang['ones'][ones]}")
    
    return " ".join(parts)


def _convert_french(num: int, lang: dict) -> str:
    """Convert integer to French words."""
    if num == 0:
        return lang["zero"]
    
    parts = []
    
    if num < 0:
        parts.append(lang["negative"])
        num = abs(num)
    
    # Handle large scales
    if num >= 1000000:
        millions = num // 1000000
        rest = num % 1000000
        
        if millions == 1:
            parts.append("un million")
        else:
            parts.append(f"{_convert_french(millions, lang)} millions")
        
        if rest > 0:
            parts.append(_convert_french(rest, lang))
        
        return " ".join(parts)
    
    if num >= 1000:
        thousands = num // 1000
        rest = num % 1000
        
        if thousands == 1:
            parts.append("mille")
        else:
            parts.append(f"{_convert_french(thousands, lang)} mille")
        
        if rest > 0:
            parts.append(_convert_french(rest, lang))
        
        return " ".join(parts)
    
    # Handle hundreds
    if num >= 100:
        hundreds = num // 100
        rest = num % 100
        
        if hundreds == 1:
            if rest == 0:
                parts.append("cent")
            else:
                parts.append("cent")
        else:
            if rest == 0:
                parts.append(f"{_convert_french(hundreds, lang)} cents")
            else:
                parts.append(f"{_convert_french(hundreds, lang)} cent")
        
        num = rest
    
    # Handle tens and ones
    if num > 0:
        if num < 17:
            parts.append(lang["ones"][num])
        elif num < 20:
            parts.append(lang["ones"][num])
        elif num < 70:
            tens = num // 10
            ones = num % 10
            if ones == 0:
                parts.append(lang["tens"][tens])
            elif ones == 1:
                parts.append(f"{lang['tens'][tens]} et un")
            else:
                parts.append(f"{lang['tens'][tens]}-{lang['ones'][ones]}")
        elif num < 80:
            # soixante-dix, soixante-et-onze, etc.
            rest = num - 60
            if rest == 10:
                parts.append("soixante-dix")
            elif rest == 11:
                parts.append("soixante et onze")
            else:
                parts.append(f"soixante-{lang['ones'][rest]}")
        elif num == 80:
            parts.append("quatre-vingts")
        elif num < 100:
            rest = num - 80
            if rest == 0:
                parts.append("quatre-vingts")
            else:
                parts.append(f"quatre-vingt-{lang['ones'][rest]}")
    
    return " ".join(parts)


def _convert_german(num: int, lang: dict) -> str:
    """Convert integer to German words."""
    if num == 0:
        return lang["zero"]
    
    parts = []
    
    if num < 0:
        parts.append(lang["negative"])
        num = abs(num)
    
    # Handle large scales
    if num >= 1000000:
        millions = num // 1000000
        rest = num % 1000000
        
        if millions == 1:
            parts.append("eine Million")
        else:
            parts.append(f"{_convert_german(millions, lang)} Millionen")
        
        if rest > 0:
            parts.append(_convert_german(rest, lang))
        
        return " ".join(parts)
    
    if num >= 1000:
        thousands = num // 1000
        rest = num % 1000
        
        if thousands == 1:
            parts.append("eintausend")
        else:
            parts.append(f"{_convert_german(thousands, lang)}tausend")
        
        if rest > 0:
            parts.append(_convert_german(rest, lang))
        
        return "".join(parts)  # German writes compound words
    
    # Handle hundreds
    if num >= 100:
        hundreds = num // 100
        rest = num % 100
        
        if hundreds == 1:
            parts.append("einhundert")
        else:
            parts.append(f"{lang['ones'][hundreds]}hundert")
        
        num = rest
    
    # Handle tens and ones (German writes ones before tens, e.g., "dreiundzwanzig")
    if num > 0:
        if num < 20:
            parts.append(lang["ones"][num])
        else:
            tens = num // 10
            ones = num % 10
            
            if ones > 0:
                # Special: "ein" not "eins" in compound numbers
                one_word = "ein" if ones == 1 else lang['ones'][ones]
                parts.append(f"{one_word}und{lang['tens'][tens]}")
            else:
                parts.append(lang["tens"][tens])
    
    return "".join(parts)


def _convert_japanese(num: int, lang: dict) -> str:
    """Convert integer to Japanese words."""
    if num == 0:
        return lang["zero"]
    
    digits = lang["digits"]
    units = lang["units"]
    scales = lang["scales"]
    
    parts = []
    
    if num < 0:
        parts.append(lang["negative"])
        num = abs(num)
    
    # Special cases for standalone units (百, 千 without 一)
    if num == 100:
        return "百"
    if num == 1000:
        return "千"
    
    # Group by scales (万, 億, etc.)
    scale_groups = []
    scale_unit = 10000
    
    while num > 0:
        scale_groups.append(num % scale_unit)
        num //= scale_unit
    
    for i, group in enumerate(reversed(scale_groups)):
        if group == 0:
            continue
        
        scale_idx = len(scale_groups) - 1 - i
        
        group_str = _convert_group_japanese(group, digits, units)
        parts.append(group_str)
        
        if scale_idx > 0 and scale_idx < len(scales):
            parts.append(scales[scale_idx])
    
    return (lang["negative"] + " " if parts and parts[0] == lang["negative"] else "") + "".join(parts)


def _convert_group_japanese(num: int, digits: list, units: list) -> str:
    """Convert a group of up to 4 digits to Japanese words (with special 一 omission)."""
    if num == 0:
        return ""
    
    result = []
    
    # Thousands - omit 一 for 千
    if num >= 1000:
        sen = num // 1000
        if sen > 1:
            result.append(digits[sen])
        result.append(units[3])
        num %= 1000
    
    # Hundreds - omit 一 for 百
    if num >= 100:
        hyaku = num // 100
        if hyaku > 1:
            result.append(digits[hyaku])
        result.append(units[2])
        num %= 100
    
    # Tens - omit 一 for 十 (Japanese style)
    if num >= 10:
        ju = num // 10
        if ju > 1:
            result.append(digits[ju])
        result.append(units[1])
        num %= 10
    
    # Ones
    if num > 0:
        result.append(digits[num])
    
    return "".join(result)


def _convert_korean(num: int, lang: dict) -> str:
    """Convert integer to Korean words."""
    if num == 0:
        return lang["zero"]
    
    parts = []
    
    if num < 0:
        parts.append(lang["negative"])
        num = abs(num)
    
    # Use Sino-Korean for large numbers
    if lang.get("use_sino", True) or num >= 100:
        return _convert_korean_sino(num, lang)
    
    # Use native Korean for small numbers
    return _convert_korean_native(num, lang)


def _convert_korean_sino(num: int, lang: dict) -> str:
    """Convert integer to Sino-Korean words."""
    digits = lang["digits_sino"]
    units = lang["units_sino"]
    scales = lang["scales"]
    
    if num == 0:
        return lang["zero"]
    
    parts = []
    
    if num < 0:
        parts.append(lang["negative"])
        num = abs(num)
    
    # Group by scales
    scale_groups = []
    scale_unit = 10000
    
    while num > 0:
        scale_groups.append(num % scale_unit)
        num //= scale_unit
    
    for i, group in enumerate(reversed(scale_groups)):
        if group == 0:
            continue
        
        scale_idx = len(scale_groups) - 1 - i
        
        group_str = _convert_group_korean_sino(group, digits, units)
        parts.append(group_str)
        
        if scale_idx > 0 and scale_idx < len(scales):
            parts.append(scales[scale_idx])
    
    result = "".join(parts)
    return (lang["negative"] + " " if parts and parts[0] == lang["negative"] else "") + result


def _convert_group_korean_sino(num: int, digits: list, units: list) -> str:
    """Convert a group of up to 4 digits to Sino-Korean words."""
    if num == 0:
        return ""
    
    result = []
    
    # Thousands
    if num >= 1000:
        cheon = num // 1000
        if cheon > 1:
            result.append(digits[cheon])
        result.append(units[3])
        num %= 1000
    
    # Hundreds
    if num >= 100:
        baek = num // 100
        if baek > 1:
            result.append(digits[baek])
        result.append(units[2])
        num %= 100
    
    # Tens
    if num >= 10:
        ship = num // 10
        if ship > 1:
            result.append(digits[ship])
        result.append(units[1])
        num %= 10
    
    # Ones
    if num > 0:
        result.append(digits[num])
    
    return "".join(result)


def _convert_korean_native(num: int, lang: dict) -> str:
    """Convert integer to native Korean words (for small numbers)."""
    if num == 0:
        return lang["zero"]
    
    if num <= 10:
        return lang["digits_native"][num]
    
    if num < 100:
        tens = num // 10
        ones = num % 10
        
        result = lang["units_native"][tens]
        if ones > 0:
            result += " " + lang["digits_native"][ones]
        return result
    
    # Fall back to Sino-Korean for larger numbers
    return _convert_korean_sino(num, lang)


def number_to_words(
    num: Union[int, float, str, Decimal],
    lang: str = "en",
    ordinal: bool = False
) -> str:
    """
    Convert a number to its word representation.
    
    Args:
        num: The number to convert (int, float, str, or Decimal)
        lang: Language code ('en', 'zh', 'ja', 'ko', 'es', 'fr', 'de')
        ordinal: If True, return ordinal form (first, second, etc.)
    
    Returns:
        The number in words
    
    Raises:
        ValueError: If the number is invalid or too large
    
    Examples:
        >>> number_to_words(42)
        'forty-two'
        >>> number_to_words(1234, lang='zh')
        '一千二百三十四'
        >>> number_to_words(3, ordinal=True)
        'third'
    """
    if lang.lower() not in LANGUAGES:
        raise ValueError(f"Unsupported language: {lang}. Supported: {get_supported_languages()}")
    
    lang_data = LANGUAGES[lang.lower()]
    int_part, decimal_part = _parse_number(num)
    
    # Handle ordinal
    if ordinal:
        if decimal_part:
            raise ValueError("Ordinal form not supported for decimal numbers")
        
        if lang.lower() in ("en", "english"):
            return _convert_ordinal_english(int_part, lang_data)
        elif lang.lower() in ("zh", "chinese"):
            return _convert_ordinal_chinese(int_part, lang_data)
        else:
            # For other languages, just add a prefix/suffix or return cardinal
            if "ordinal_prefix" in lang_data:
                prefix = lang_data.get("ordinal_prefix", "")
                result = number_to_words(abs(int_part), lang, ordinal=False)
                if int_part < 0:
                    return f"{lang_data['negative']}{prefix}{result}"
                return f"{prefix}{result}"
            elif "ordinal_suffix" in lang_data:
                suffix = lang_data.get("ordinal_suffix", "")
                result = number_to_words(abs(int_part), lang, ordinal=False)
                if int_part < 0:
                    return f"{lang_data['negative']} {result}{suffix}"
                return f"{result}{suffix}"
            else:
                return number_to_words(int_part, lang, ordinal=False)
    
    # Convert based on language
    result_parts = []
    
    if lang.lower() in ("en", "english"):
        result_parts.append(_convert_english(int_part, lang_data))
        if decimal_part:
            result_parts.append(_convert_decimal_english(decimal_part, lang_data))
    elif lang.lower() in ("zh", "chinese"):
        int_result = _convert_chinese(int_part, lang_data)
        if decimal_part:
            int_result += _convert_decimal_chinese(decimal_part, lang_data)
        return int_result
    elif lang.lower() in ("ja", "japanese"):
        result_parts.append(_convert_japanese(int_part, lang_data))
        if decimal_part:
            result_parts.append(lang_data["point"] + "".join([lang_data["digits"][int(d)] for d in decimal_part]))
    elif lang.lower() in ("ko", "korean"):
        result_parts.append(_convert_korean(int_part, lang_data))
        if decimal_part:
            result_parts.append(lang_data["point"] + "".join([lang_data["digits_sino"][int(d)] for d in decimal_part]))
    elif lang.lower() in ("es", "spanish"):
        result_parts.append(_convert_spanish(int_part, lang_data))
        if decimal_part:
            result_parts.append(lang_data["point"] + " ".join([lang_data["ones"][int(d)] for d in decimal_part]))
    elif lang.lower() in ("fr", "french"):
        result_parts.append(_convert_french(int_part, lang_data))
        if decimal_part:
            result_parts.append(lang_data["point"] + " ".join([lang_data["ones"][int(d)] for d in decimal_part]))
    elif lang.lower() in ("de", "german"):
        result_parts.append(_convert_german(int_part, lang_data))
        if decimal_part:
            result_parts.append(lang_data["point"] + " ".join([lang_data["ones"][int(d)] for d in decimal_part]))
    
    return " ".join(result_parts)


def number_to_currency_words(
    num: Union[int, float, str, Decimal],
    lang: str = "en",
    currency: Optional[str] = None
) -> str:
    """
    Convert a number to currency words.
    
    Args:
        num: The amount to convert
        lang: Language code ('en' or 'zh' have full currency support)
        currency: Optional currency code (future expansion)
    
    Returns:
        The amount in currency words
    
    Examples:
        >>> number_to_currency_words(42.50)
        'forty-two dollars and fifty cents'
        >>> number_to_currency_words(100.01, lang='zh')
        '壹佰元壹分'
    """
    if lang.lower() not in ("en", "english", "zh", "chinese"):
        # Fall back to basic conversion for unsupported languages
        return number_to_words(num, lang)
    
    lang_data = LANGUAGES[lang.lower()]
    
    if lang.lower() in ("en", "english"):
        return _convert_currency_english(num, lang_data)
    elif lang.lower() in ("zh", "chinese"):
        return _convert_currency_chinese(num, lang_data)


def number_to_ordinal_words(
    num: Union[int, float, str, Decimal],
    lang: str = "en"
) -> str:
    """
    Convert a number to ordinal words (first, second, third, etc.).
    
    Args:
        num: The number to convert (must be an integer)
        lang: Language code
    
    Returns:
        The ordinal in words
    
    Examples:
        >>> number_to_ordinal_words(1)
        'first'
        >>> number_to_ordinal_words(21)
        'twenty-first'
        >>> number_to_ordinal_words(5, lang='zh')
        '第五'
    """
    return number_to_words(num, lang, ordinal=True)