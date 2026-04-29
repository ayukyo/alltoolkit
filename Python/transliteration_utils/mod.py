"""
Transliteration Utils - 文字系统音译转换工具

支持多种文字系统之间的音译转换：
- 西里尔字母 (俄语等) → 拉丁字母
- 希腊字母 → 拉丁字母
- 阿拉伯字母 → 拉丁字母
- 日语假名 → 罗马音
- 韩语谚文 → 罗马音 (基础)
- 泰语 → 拉丁字母
- 希伯来语 → 拉丁字母
- 拉丁字母 → 西里尔字母

零外部依赖，纯Python实现。
"""

from typing import Dict, List, Tuple, Optional
import re


class TransliterationUtils:
    """文字系统音译转换工具类"""
    
    # 西里尔字母 (俄语) → 拉丁字母映射表 (ISO 9 / GOST 7.79-2000)
    CYRILLIC_TO_LATIN: Dict[str, str] = {
        # 大写字母
        'А': 'A', 'Б': 'B', 'В': 'V', 'Г': 'G', 'Д': 'D', 'Е': 'E',
        'Ё': 'Yo', 'Ж': 'Zh', 'З': 'Z', 'И': 'I', 'Й': 'Y', 'К': 'K',
        'Л': 'L', 'М': 'M', 'Н': 'N', 'О': 'O', 'П': 'P', 'Р': 'R',
        'С': 'S', 'Т': 'T', 'У': 'U', 'Ф': 'F', 'Х': 'Kh', 'Ц': 'Ts',
        'Ч': 'Ch', 'Ш': 'Sh', 'Щ': 'Shch', 'Ъ': '', 'Ы': 'Y', 'Ь': '',
        'Э': 'E', 'Ю': 'Yu', 'Я': 'Ya',
        # 小写字母
        'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e',
        'ё': 'yo', 'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'y', 'к': 'k',
        'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r',
        'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', 'х': 'kh', 'ц': 'ts',
        'ч': 'ch', 'ш': 'sh', 'щ': 'shch', 'ъ': '', 'ы': 'y', 'ь': '',
        'э': 'e', 'ю': 'yu', 'я': 'ya',
    }
    
    # 拉丁字母 → 西里尔字母映射表 (俄语)
    LATIN_TO_CYRILLIC: Dict[str, str] = {
        # 大写
        'A': 'А', 'B': 'Б', 'V': 'В', 'G': 'Г', 'D': 'Д', 'E': 'Е',
        'Zh': 'Ж', 'Z': 'З', 'I': 'И', 'Y': 'Й', 'K': 'К', 'L': 'Л',
        'M': 'М', 'N': 'Н', 'O': 'О', 'P': 'П', 'R': 'Р', 'S': 'С',
        'T': 'Т', 'U': 'У', 'F': 'Ф', 'Kh': 'Х', 'Ts': 'Ц', 'Ch': 'Ч',
        'Sh': 'Ш', 'Shch': 'Щ', 'Yu': 'Ю', 'Ya': 'Я', 'Yo': 'Ё',
        # 小写
        'a': 'а', 'b': 'б', 'v': 'в', 'g': 'г', 'd': 'д', 'e': 'е',
        'zh': 'ж', 'z': 'з', 'i': 'и', 'y': 'й', 'k': 'к', 'l': 'л',
        'm': 'м', 'n': 'н', 'o': 'о', 'p': 'п', 'r': 'р', 's': 'с',
        't': 'т', 'u': 'у', 'f': 'ф', 'kh': 'х', 'ts': 'ц', 'ch': 'ч',
        'sh': 'ш', 'shch': 'щ', 'yu': 'ю', 'ya': 'я', 'yo': 'ё',
    }
    
    # 希腊字母 → 拉丁字母映射表
    GREEK_TO_LATIN: Dict[str, str] = {
        # 大写字母
        'Α': 'A', 'Β': 'V', 'Γ': 'G', 'Δ': 'D', 'Ε': 'E', 'Ζ': 'Z',
        'Η': 'I', 'Θ': 'Th', 'Ι': 'I', 'Κ': 'K', 'Λ': 'L', 'Μ': 'M',
        'Ν': 'N', 'Ξ': 'X', 'Ο': 'O', 'Π': 'P', 'Ρ': 'R', 'Σ': 'S',
        'Τ': 'T', 'Υ': 'Y', 'Φ': 'F', 'Χ': 'Ch', 'Ψ': 'Ps', 'Ω': 'O',
        # 小写字母
        'α': 'a', 'β': 'v', 'γ': 'g', 'δ': 'd', 'ε': 'e', 'ζ': 'z',
        'η': 'i', 'θ': 'th', 'ι': 'i', 'κ': 'k', 'λ': 'l', 'μ': 'm',
        'ν': 'n', 'ξ': 'x', 'ο': 'o', 'π': 'p', 'ρ': 'r', 'σ': 's',
        'ς': 's', 'τ': 't', 'υ': 'y', 'φ': 'f', 'χ': 'ch', 'ψ': 'ps',
        'ω': 'o',
        # 双字母组合
        'αι': 'ai', 'ει': 'ei', 'οι': 'oi', 'ου': 'ou', 'αυ': 'av',
        'ευ': 'ev', 'ηυ': 'iv',
    }
    
    # 平假名 → 罗马音映射表 (Hepburn罗马音)
    HIRAGANA_TO_ROMAJI: Dict[str, str] = {
        # 基本音节
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
        # 浊音
        'が': 'ga', 'ぎ': 'gi', 'ぐ': 'gu', 'げ': 'ge', 'ご': 'go',
        'ざ': 'za', 'じ': 'ji', 'ず': 'zu', 'ぜ': 'ze', 'ぞ': 'zo',
        'だ': 'da', 'ぢ': 'ji', 'づ': 'zu', 'で': 'de', 'ど': 'do',
        'ば': 'ba', 'び': 'bi', 'ぶ': 'bu', 'べ': 'be', 'ぼ': 'bo',
        # 半浊音
        'ぱ': 'pa', 'ぴ': 'pi', 'ぷ': 'pu', 'ぺ': 'pe', 'ぽ': 'po',
        # 拗音
        'きゃ': 'kya', 'きゅ': 'kyu', 'きょ': 'kyo',
        'しゃ': 'sha', 'しゅ': 'shu', 'しょ': 'sho',
        'ちゃ': 'cha', 'ちゅ': 'chu', 'ちょ': 'cho',
        'にゃ': 'nya', 'にゅ': 'nyu', 'にょ': 'nyo',
        'ひゃ': 'hya', 'ひゅ': 'hyu', 'ひょ': 'hyo',
        'みゃ': 'mya', 'みゅ': 'myu', 'みょ': 'myo',
        'りゃ': 'rya', 'りゅ': 'ryu', 'りょ': 'ryo',
        'ぎゃ': 'gya', 'ぎゅ': 'gyu', 'ぎょ': 'gyo',
        'じゃ': 'ja', 'じゅ': 'ju', 'じょ': 'jo',
        'びゃ': 'bya', 'びゅ': 'byu', 'びょ': 'byo',
        'ぴゃ': 'pya', 'ぴゅ': 'pyu', 'ぴょ': 'pyo',
        # 小假名
        'ぁ': 'a', 'ぃ': 'i', 'ぅ': 'u', 'ぇ': 'e', 'ぉ': 'o',
        'ゃ': 'ya', 'ゅ': 'yu', 'ょ': 'yo', 'ゎ': 'wa',
        'っ': '',  # 促音符号，需要特殊处理
    }
    
    # 片假名 → 罗马音映射表
    KATAKANA_TO_ROMAJI: Dict[str, str] = {
        # 基本音节
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
        # 浊音
        'ガ': 'ga', 'ギ': 'gi', 'グ': 'gu', 'ゲ': 'ge', 'ゴ': 'go',
        'ザ': 'za', 'ジ': 'ji', 'ズ': 'zu', 'ゼ': 'ze', 'ゾ': 'zo',
        'ダ': 'da', 'ヂ': 'ji', 'ヅ': 'zu', 'デ': 'de', 'ド': 'do',
        'バ': 'ba', 'ビ': 'bi', 'ブ': 'bu', 'ベ': 'be', 'ボ': 'bo',
        # 半浊音
        'パ': 'pa', 'ピ': 'pi', 'プ': 'pu', 'ペ': 'pe', 'ポ': 'po',
        # 拗音
        'キャ': 'kya', 'キュ': 'kyu', 'キョ': 'kyo',
        'シャ': 'sha', 'シュ': 'shu', 'ショ': 'sho',
        'チャ': 'cha', 'チュ': 'chu', 'チョ': 'cho',
        'ニャ': 'nya', 'ニュ': 'nyu', 'ニョ': 'nyo',
        'ヒャ': 'hya', 'ヒュ': 'hyu', 'ヒョ': 'hyo',
        'ミャ': 'mya', 'ミュ': 'myu', 'ミョ': 'myo',
        'リャ': 'rya', 'リュ': 'ryu', 'リョ': 'ryo',
        'ギャ': 'gya', 'ギュ': 'gyu', 'ギョ': 'gyo',
        'ジャ': 'ja', 'ジュ': 'ju', 'ジョ': 'jo',
        'ビャ': 'bya', 'ビュ': 'byu', 'ビョ': 'byo',
        'ピャ': 'pya', 'ピュ': 'pyu', 'ピョ': 'pyo',
        # 小假名
        'ァ': 'a', 'ィ': 'i', 'ゥ': 'u', 'ェ': 'e', 'ォ': 'o',
        'ャ': 'ya', 'ュ': 'yu', 'ョ': 'yo', 'ヮ': 'wa',
        'ッ': '',  # 促音符号
        # 外来音
        'ヴ': 'vu', 'ヴァ': 'va', 'ヴィ': 'vi', 'ヴェ': 've', 'ヴォ': 'vo',
        'ファ': 'fa', 'フィ': 'fi', 'フェ': 'fe', 'フォ': 'fo',
        'ティ': 'ti', 'ディ': 'di', 'トゥ': 'tu', 'ドゥ': 'du',
        'ウィ': 'wi', 'ウェ': 'we', 'ウォ': 'wo',
    }
    
    # 韩语谚文 (基础辅音+元音组合)
    HANGUL_CONSONANTS: Dict[str, str] = {
        'ㄱ': 'g', 'ㄲ': 'kk', 'ㄴ': 'n', 'ㄷ': 'd', 'ㄸ': 'tt',
        'ㄹ': 'r', 'ㅁ': 'm', 'ㅂ': 'b', 'ㅃ': 'pp', 'ㅅ': 's',
        'ㅆ': 'ss', 'ㅇ': '', 'ㅈ': 'j', 'ㅉ': 'jj', 'ㅊ': 'ch',
        'ㅋ': 'k', 'ㅌ': 't', 'ㅍ': 'p', 'ㅎ': 'h',
    }
    
    HANGUL_VOWELS: Dict[str, str] = {
        'ㅏ': 'a', 'ㅐ': 'ae', 'ㅑ': 'ya', 'ㅒ': 'yae', 'ㅓ': 'eo',
        'ㅔ': 'e', 'ㅕ': 'yeo', 'ㅖ': 'ye', 'ㅗ': 'o', 'ㅘ': 'wa',
        'ㅙ': 'wae', 'ㅚ': 'oe', 'ㅛ': 'yo', 'ㅜ': 'u', 'ㅝ': 'wo',
        'ㅞ': 'we', 'ㅟ': 'wi', 'ㅠ': 'yu', 'ㅡ': 'eu', 'ㅢ': 'ui',
        'ㅣ': 'i',
    }
    
    HANGUL_FINALS: Dict[str, str] = {
        '': '', 'ㄱ': 'k', 'ㄲ': 'k', 'ㄳ': 'k', 'ㄴ': 'n', 'ㄵ': 'n',
        'ㄶ': 'n', 'ㄷ': 't', 'ㄹ': 'l', 'ㄺ': 'k', 'ㄻ': 'm', 'ㄼ': 'l',
        'ㄽ': 'l', 'ㄾ': 'l', 'ㄿ': 'p', 'ㅀ': 'l', 'ㅁ': 'm', 'ㅂ': 'p',
        'ㅄ': 'p', 'ㅅ': 't', 'ㅆ': 't', 'ㅇ': 'ng', 'ㅈ': 't', 'ㅊ': 't',
        'ㅋ': 'k', 'ㅌ': 't', 'ㅍ': 'p', 'ㅎ': 't',
    }
    
    # 阿拉伯字母 → 拉丁字母映射表
    ARABIC_TO_LATIN: Dict[str, str] = {
        # 基本字母
        'ا': 'a', 'ب': 'b', 'ت': 't', 'ث': 'th', 'ج': 'j',
        'ح': 'h', 'خ': 'kh', 'د': 'd', 'ذ': 'dh', 'ر': 'r',
        'ز': 'z', 'س': 's', 'ش': 'sh', 'ص': 's', 'ض': 'd',
        'ط': 't', 'ظ': 'z', 'ع': '', 'غ': 'gh', 'ف': 'f',
        'ق': 'q', 'ك': 'k', 'ل': 'l', 'م': 'm', 'ن': 'n',
        'ه': 'h', 'و': 'w', 'ي': 'y', 'ى': 'a',
        # 变体
        'أ': 'a', 'إ': 'i', 'آ': 'a', 'ؤ': '', 'ئ': '',
        'ة': 'h',
    }
    
    # 泰语 → 拉丁字母映射表
    THAI_TO_LATIN: Dict[str, str] = {
        # 辅音
        'ก': 'k', 'ข': 'kh', 'ฃ': 'kh', 'ค': 'kh', 'ฅ': 'kh',
        'ฆ': 'kh', 'ง': 'ng', 'จ': 'ch', 'ฉ': 'ch', 'ช': 'ch',
        'ซ': 's', 'ฌ': 'ch', 'ญ': 'y', 'ฎ': 'd', 'ฏ': 't',
        'ฐ': 'th', 'ฑ': 'th', 'ฒ': 'th', 'ณ': 'n', 'ด': 'd',
        'ต': 't', 'ถ': 'th', 'ท': 'th', 'ธ': 'th', 'น': 'n',
        'บ': 'b', 'ป': 'p', 'ผ': 'ph', 'ฝ': 'f', 'พ': 'ph',
        'ฟ': 'f', 'ภ': 'ph', 'ม': 'm', 'ย': 'y', 'ร': 'r',
        'ล': 'l', 'ว': 'w', 'ศ': 's', 'ษ': 's', 'ส': 's',
        'ห': 'h', 'ฬ': 'l', 'ฮ': 'h',
        # 元音
        'ะ': 'a', 'า': 'a', 'ำ': 'am', 'ิ': 'i', 'ี': 'i',
        'ึ': 'ue', 'ื': 'ue', 'ุ': 'u', 'ู': 'u', 'เ': 'e',
        'แ': 'ae', 'โ': 'o', 'ใ': 'ai', 'ไ': 'ai', 'ๆ': '',
        'ฯ': '',
    }
    
    # 希伯来语 → 拉丁字母映射表
    HEBREW_TO_LATIN: Dict[str, str] = {
        'א': '', 'ב': 'b', 'ג': 'g', 'ד': 'd', 'ה': 'h',
        'ו': 'v', 'ז': 'z', 'ח': 'ch', 'ט': 't', 'י': 'y',
        'ך': 'ch', 'כ': 'k', 'ל': 'l', 'ם': 'm', 'מ': 'm',
        'ן': 'n', 'נ': 'n', 'ס': 's', 'ע': '', 'ף': 'f',
        'פ': 'p', 'ץ': 'ts', 'צ': 'ts', 'ק': 'k', 'ר': 'r',
        'ש': 'sh', 'ת': 't',
    }
    
    def __init__(self):
        """初始化音译工具"""
        pass
    
    @staticmethod
    def cyrillic_to_latin(text: str) -> str:
        """
        将西里尔字母 (俄语) 转换为拉丁字母
        
        Args:
            text: 西里尔字母文本
            
        Returns:
            拉丁字母文本
            
        Example:
            >>> TransliterationUtils.cyrillic_to_latin("Привет мир")
            'Privet mir'
        """
        result = []
        i = 0
        while i < len(text):
            char = text[i]
            if char in TransliterationUtils.CYRILLIC_TO_LATIN:
                result.append(TransliterationUtils.CYRILLIC_TO_LATIN[char])
            else:
                result.append(char)
            i += 1
        return ''.join(result)
    
    @staticmethod
    def latin_to_cyrillic(text: str) -> str:
        """
        将拉丁字母转换为西里尔字母 (俄语)
        
        使用优先匹配长音节的原则
        
        Args:
            text: 拉丁字母文本
            
        Returns:
            西里尔字母文本
            
        Example:
            >>> TransliterationUtils.latin_to_cyrillic("Privet mir")
            'Привет мир'
        """
        result = []
        i = 0
        while i < len(text):
            matched = False
            # 尝试匹配最长组合 (3字符)
            for length in [4, 3, 2, 1]:
                if i + length <= len(text):
                    substr = text[i:i+length]
                    if substr in TransliterationUtils.LATIN_TO_CYRILLIC:
                        result.append(TransliterationUtils.LATIN_TO_CYRILLIC[substr])
                        i += length
                        matched = True
                        break
            if not matched:
                result.append(text[i])
                i += 1
        return ''.join(result)
    
    @staticmethod
    def greek_to_latin(text: str) -> str:
        """
        将希腊字母转换为拉丁字母
        
        Args:
            text: 希腊字母文本
            
        Returns:
            拉丁字母文本
            
        Example:
            >>> TransliterationUtils.greek_to_latin("Γειά σου")
            'Geia sou'
        """
        result = []
        i = 0
        while i < len(text):
            char = text[i]
            # 先尝试匹配双字母组合
            if i + 1 < len(text):
                two_chars = text[i:i+2]
                if two_chars in TransliterationUtils.GREEK_TO_LATIN:
                    result.append(TransliterationUtils.GREEK_TO_LATIN[two_chars])
                    i += 2
                    continue
            if char in TransliterationUtils.GREEK_TO_LATIN:
                result.append(TransliterationUtils.GREEK_TO_LATIN[char])
            else:
                result.append(char)
            i += 1
        return ''.join(result)
    
    @staticmethod
    def hiragana_to_romaji(text: str) -> str:
        """
        将日语平假名转换为罗马音 (Hepburn罗马音)
        
        Args:
            text: 平假名文本
            
        Returns:
            罗马音文本
            
        Example:
            >>> TransliterationUtils.hiragana_to_romaji("こんにちは")
            'konnichiha'
        """
        result = []
        i = 0
        while i < len(text):
            char = text[i]
            # 处理促音 (っ + 辅音)
            if char == 'っ' and i + 1 < len(text):
                next_char = text[i + 1]
                # 找到下一个假名对应的罗马音首字母
                if next_char in TransliterationUtils.HIRAGANA_TO_ROMAJI:
                    romaji = TransliterationUtils.HIRAGANA_TO_ROMAJI[next_char]
                    if romaji and romaji[0]:
                        result.append(romaji[0])  # 重复辅音
                i += 1
                continue
            
            # 先尝试匹配拗音 (两字符组合)
            if i + 1 < len(text):
                two_chars = text[i:i+2]
                if two_chars in TransliterationUtils.HIRAGANA_TO_ROMAJI:
                    result.append(TransliterationUtils.HIRAGANA_TO_ROMAJI[two_chars])
                    i += 2
                    continue
            
            if char in TransliterationUtils.HIRAGANA_TO_ROMAJI:
                result.append(TransliterationUtils.HIRAGANA_TO_ROMAJI[char])
            else:
                result.append(char)
            i += 1
        return ''.join(result)
    
    @staticmethod
    def katakana_to_romaji(text: str) -> str:
        """
        将日语片假名转换为罗马音 (Hepburn罗马音)
        
        Args:
            text: 片假名文本
            
        Returns:
            罗马音文本
            
        Example:
            >>> TransliterationUtils.katakana_to_romaji("コンニチハ")
            'konnichiha'
        """
        result = []
        i = 0
        while i < len(text):
            char = text[i]
            # 处理促音 (ッ + 辅音)
            if char == 'ッ' and i + 1 < len(text):
                next_char = text[i + 1]
                if next_char in TransliterationUtils.KATAKANA_TO_ROMAJI:
                    romaji = TransliterationUtils.KATAKANA_TO_ROMAJI[next_char]
                    if romaji and romaji[0]:
                        result.append(romaji[0])
                i += 1
                continue
            
            # 先尝试匹配拗音 (两字符组合)
            if i + 1 < len(text):
                two_chars = text[i:i+2]
                if two_chars in TransliterationUtils.KATAKANA_TO_ROMAJI:
                    result.append(TransliterationUtils.KATAKANA_TO_ROMAJI[two_chars])
                    i += 2
                    continue
            
            if char in TransliterationUtils.KATAKANA_TO_ROMAJI:
                result.append(TransliterationUtils.KATAKANA_TO_ROMAJI[char])
            else:
                result.append(char)
            i += 1
        return ''.join(result)
    
    @staticmethod
    def japanese_to_romaji(text: str) -> str:
        """
        将日语 (平假名+片假名) 转换为罗马音
        
        Args:
            text: 日语文本 (混合假名)
            
        Returns:
            罗马音文本
            
        Example:
            >>> TransliterationUtils.japanese_to_romaji("こんにちは世界")
            'konnichiha世界'
        """
        result = []
        i = 0
        while i < len(text):
            char = text[i]
            
            # 检查是否是平假名
            if char in TransliterationUtils.HIRAGANA_TO_ROMAJI or char == 'っ':
                # 促音处理
                if char == 'っ' and i + 1 < len(text):
                    next_char = text[i + 1]
                    if next_char in TransliterationUtils.HIRAGANA_TO_ROMAJI:
                        romaji = TransliterationUtils.HIRAGANA_TO_ROMAJI[next_char]
                        if romaji and romaji[0]:
                            result.append(romaji[0])
                        i += 2
                        continue
                    result.append('')
                    i += 1
                    continue
                
                # 拗音匹配
                if i + 1 < len(text):
                    two_chars = text[i:i+2]
                    if two_chars in TransliterationUtils.HIRAGANA_TO_ROMAJI:
                        result.append(TransliterationUtils.HIRAGANA_TO_ROMAJI[two_chars])
                        i += 2
                        continue
                
                result.append(TransliterationUtils.HIRAGANA_TO_ROMAJI.get(char, char))
            
            # 检查是否是片假名
            elif char in TransliterationUtils.KATAKANA_TO_ROMAJI or char == 'ッ':
                # 促音处理
                if char == 'ッ' and i + 1 < len(text):
                    next_char = text[i + 1]
                    if next_char in TransliterationUtils.KATAKANA_TO_ROMAJI:
                        romaji = TransliterationUtils.KATAKANA_TO_ROMAJI[next_char]
                        if romaji and romaji[0]:
                            result.append(romaji[0])
                        i += 2
                        continue
                    result.append('')
                    i += 1
                    continue
                
                # 拗音匹配
                if i + 1 < len(text):
                    two_chars = text[i:i+2]
                    if two_chars in TransliterationUtils.KATAKANA_TO_ROMAJI:
                        result.append(TransliterationUtils.KATAKANA_TO_ROMAJI[two_chars])
                        i += 2
                        continue
                
                result.append(TransliterationUtils.KATAKANA_TO_ROMAJI.get(char, char))
            
            else:
                result.append(char)
            
            i += 1
        
        return ''.join(result)
    
    @staticmethod
    def hangul_to_romaji(text: str) -> str:
        """
        将韩语谚文转换为罗马音 (Revised Romanization)
        
        Args:
            text: 韩语谚文文本
            
        Returns:
            罗马音文本
            
        Example:
            >>> TransliterationUtils.hangul_to_romaji("안녕하세요")
            'annyeonghaseyo'
        """
        result = []
        
        for char in text:
            # 检查是否是韩文字符 (AC00-D7AF 范围)
            code = ord(char)
            if 0xAC00 <= code <= 0xD7AF:
                # 计算分解
                index = code - 0xAC00
                initial_index = index // (21 * 28)
                vowel_index = (index // 28) % 21
                final_index = index % 28
                
                # 获取初声、中声、终声
                initials = list("ㄱㄲㄴㄷㄸㄹㅁㅂㅃㅅㅆㅇㅈㅉㅊㅋㅌㅍㅎ")
                vowels = list("ㅏㅐㅑㅒㅓㅔㅕㅖㅗㅘㅙㅚㅛㅜㅝㅞㅟㅠㅡㅢㅣ")
                finals = list(" ㄱㄲㄳㄴㄵㄶㄷㄹㄺㄻㄼㄽㄾㄿㅀㅁㅂㅄㅅㅆㅇㅈㅊㅋㅌㅍㅎ")
                
                initial = initials[initial_index] if initial_index < len(initials) else ''
                vowel = vowels[vowel_index] if vowel_index < len(vowels) else ''
                final = finals[final_index] if final_index < len(finals) else ''
                
                # 转换
                c = TransliterationUtils.HANGUL_CONSONANTS.get(initial, '')
                v = TransliterationUtils.HANGUL_VOWELS.get(vowel, '')
                f = TransliterationUtils.HANGUL_FINALS.get(final, '')
                
                result.append(c + v + f)
            else:
                result.append(char)
        
        return ''.join(result)
    
    @staticmethod
    def arabic_to_latin(text: str) -> str:
        """
        将阿拉伯字母转换为拉丁字母
        
        Args:
            text: 阿拉伯字母文本
            
        Returns:
            拉丁字母文本
            
        Example:
            >>> TransliterationUtils.arabic_to_latin("مرحبا")
            'mrhba'
        """
        result = []
        for char in text:
            if char in TransliterationUtils.ARABIC_TO_LATIN:
                result.append(TransliterationUtils.ARABIC_TO_LATIN[char])
            else:
                result.append(char)
        return ''.join(result)
    
    @staticmethod
    def thai_to_latin(text: str) -> str:
        """
        将泰语转换为拉丁字母 (基础转换)
        
        Args:
            text: 泰语文本
            
        Returns:
            拉丁字母文本
            
        Example:
            >>> TransliterationUtils.thai_to_latin("สวัสดี")
            'swatsdi'
        """
        result = []
        for char in text:
            if char in TransliterationUtils.THAI_TO_LATIN:
                result.append(TransliterationUtils.THAI_TO_LATIN[char])
            else:
                result.append(char)
        return ''.join(result)
    
    @staticmethod
    def hebrew_to_latin(text: str) -> str:
        """
        将希伯来字母转换为拉丁字母
        
        Args:
            text: 希伯来字母文本
            
        Returns:
            拉丁字母文本
            
        Example:
            >>> TransliterationUtils.hebrew_to_latin("שלום")
            'shlom'
        """
        result = []
        for char in text:
            if char in TransliterationUtils.HEBREW_TO_LATIN:
                result.append(TransliterationUtils.HEBREW_TO_LATIN[char])
            else:
                result.append(char)
        return ''.join(result)
    
    @staticmethod
    def detect_script(text: str) -> str:
        """
        检测文本使用的文字系统
        
        Args:
            text: 输入文本
            
        Returns:
            文字系统名称: 'cyrillic', 'greek', 'hiragana', 'katakana', 
                         'hangul', 'arabic', 'thai', 'hebrew', 'latin', 'mixed', 'unknown'
            
        Example:
            >>> TransliterationUtils.detect_script("Привет")
            'cyrillic'
        """
        scripts = {
            'cyrillic': 0,
            'greek': 0,
            'hiragana': 0,
            'katakana': 0,
            'hangul': 0,
            'arabic': 0,
            'thai': 0,
            'hebrew': 0,
            'latin': 0,
        }
        
        for char in text:
            code = ord(char)
            
            # 西里尔字母 (俄语等)
            if 0x0400 <= code <= 0x04FF or 0x0500 <= code <= 0x052F:
                scripts['cyrillic'] += 1
            # 希腊字母
            elif 0x0370 <= code <= 0x03FF:
                scripts['greek'] += 1
            # 平假名
            elif 0x3040 <= code <= 0x309F:
                scripts['hiragana'] += 1
            # 片假名
            elif 0x30A0 <= code <= 0x30FF:
                scripts['katakana'] += 1
            # 韩文
            elif 0xAC00 <= code <= 0xD7AF or 0x1100 <= code <= 0x11FF:
                scripts['hangul'] += 1
            # 阿拉伯字母
            elif 0x0600 <= code <= 0x06FF or 0x0750 <= code <= 0x077F:
                scripts['arabic'] += 1
            # 泰语
            elif 0x0E00 <= code <= 0x0E7F:
                scripts['thai'] += 1
            # 希伯来语
            elif 0x0590 <= code <= 0x05FF:
                scripts['hebrew'] += 1
            # 拉丁字母
            elif (0x0041 <= code <= 0x005A) or (0x0061 <= code <= 0x007A):
                scripts['latin'] += 1
        
        # 找出主要文字系统
        max_count = max(scripts.values())
        if max_count == 0:
            return 'unknown'
        
        main_scripts = [s for s, c in scripts.items() if c == max_count]
        if len(main_scripts) > 1:
            return 'mixed'
        
        return main_scripts[0]
    
    @staticmethod
    def auto_transliterate(text: str) -> Tuple[str, str]:
        """
        自动检测文字系统并转换为拉丁字母
        
        Args:
            text: 输入文本
            
        Returns:
            (转换后的文本, 检测到的文字系统)
            
        Example:
            >>> TransliterationUtils.auto_transliterate("Привет мир")
            ('Privet mir', 'cyrillic')
        """
        script = TransliterationUtils.detect_script(text)
        
        converters = {
            'cyrillic': TransliterationUtils.cyrillic_to_latin,
            'greek': TransliterationUtils.greek_to_latin,
            'hiragana': TransliterationUtils.hiragana_to_romaji,
            'katakana': TransliterationUtils.katakana_to_romaji,
            'hangul': TransliterationUtils.hangul_to_romaji,
            'arabic': TransliterationUtils.arabic_to_latin,
            'thai': TransliterationUtils.thai_to_latin,
            'hebrew': TransliterationUtils.hebrew_to_latin,
        }
        
        if script in converters:
            return converters[script](text), script
        
        return text, script
    
    @staticmethod
    def transliterate(text: str, from_script: str, to_script: str = 'latin') -> str:
        """
        指定源文字系统和目标文字系统进行转换
        
        Args:
            text: 输入文本
            from_script: 源文字系统 ('cyrillic', 'greek', 'hiragana', 'katakana',
                                   'hangul', 'arabic', 'thai', 'hebrew', 'japanese')
            to_script: 目标文字系统 (目前只支持 'latin')
            
        Returns:
            转换后的文本
            
        Example:
            >>> TransliterationUtils.transliterate("Привет", "cyrillic", "latin")
            'Privet'
        """
        if to_script != 'latin':
            raise ValueError(f"目前只支持转换为拉丁字母，不支持: {to_script}")
        
        converters = {
            'cyrillic': TransliterationUtils.cyrillic_to_latin,
            'greek': TransliterationUtils.greek_to_latin,
            'hiragana': TransliterationUtils.hiragana_to_romaji,
            'katakana': TransliterationUtils.katakana_to_romaji,
            'hangul': TransliterationUtils.hangul_to_romaji,
            'arabic': TransliterationUtils.arabic_to_latin,
            'thai': TransliterationUtils.thai_to_latin,
            'hebrew': TransliterationUtils.hebrew_to_latin,
            'japanese': TransliterationUtils.japanese_to_romaji,
        }
        
        if from_script not in converters:
            raise ValueError(f"不支持的源文字系统: {from_script}")
        
        return converters[from_script](text)
    
    @staticmethod
    def get_supported_scripts() -> List[str]:
        """
        获取支持的文字系统列表
        
        Returns:
            支持的文字系统名称列表
        """
        return [
            'cyrillic',      # 西里尔字母 (俄语等)
            'greek',         # 希腊字母
            'hiragana',      # 日语平假名
            'katakana',      # 日语片假名
            'japanese',      # 日语 (混合)
            'hangul',        # 韩语谚文
            'arabic',        # 阿拉伯字母
            'thai',          # 泰语
            'hebrew',        # 希伯来语
        ]


# 便捷函数
def cyrillic_to_latin(text: str) -> str:
    """将西里尔字母转换为拉丁字母"""
    return TransliterationUtils.cyrillic_to_latin(text)


def latin_to_cyrillic(text: str) -> str:
    """将拉丁字母转换为西里尔字母"""
    return TransliterationUtils.latin_to_cyrillic(text)


def greek_to_latin(text: str) -> str:
    """将希腊字母转换为拉丁字母"""
    return TransliterationUtils.greek_to_latin(text)


def hiragana_to_romaji(text: str) -> str:
    """将日语平假名转换为罗马音"""
    return TransliterationUtils.hiragana_to_romaji(text)


def katakana_to_romaji(text: str) -> str:
    """将日语片假名转换为罗马音"""
    return TransliterationUtils.katakana_to_romaji(text)


def japanese_to_romaji(text: str) -> str:
    """将日语转换为罗马音"""
    return TransliterationUtils.japanese_to_romaji(text)


def hangul_to_romaji(text: str) -> str:
    """将韩语谚文转换为罗马音"""
    return TransliterationUtils.hangul_to_romaji(text)


def arabic_to_latin(text: str) -> str:
    """将阿拉伯字母转换为拉丁字母"""
    return TransliterationUtils.arabic_to_latin(text)


def thai_to_latin(text: str) -> str:
    """将泰语转换为拉丁字母"""
    return TransliterationUtils.thai_to_latin(text)


def hebrew_to_latin(text: str) -> str:
    """将希伯来字母转换为拉丁字母"""
    return TransliterationUtils.hebrew_to_latin(text)


def detect_script(text: str) -> str:
    """检测文本使用的文字系统"""
    return TransliterationUtils.detect_script(text)


def auto_transliterate(text: str) -> Tuple[str, str]:
    """自动检测并转换文字系统"""
    return TransliterationUtils.auto_transliterate(text)


def transliterate(text: str, from_script: str, to_script: str = 'latin') -> str:
    """指定文字系统进行转换"""
    return TransliterationUtils.transliterate(text, from_script, to_script)


if __name__ == "__main__":
    # 简单演示
    print("=== Transliteration Utils Demo ===\n")
    
    # 俄语
    russian = "Привет мир! Как дела?"
    print(f"Russian: {russian}")
    print(f"Latin:   {cyrillic_to_latin(russian)}")
    print()
    
    # 希腊语
    greek = "Γειά σου κόσμε"
    print(f"Greek: {greek}")
    print(f"Latin: {greek_to_latin(greek)}")
    print()
    
    # 日语
    japanese = "こんにちは世界"
    print(f"Japanese: {japanese}")
    print(f"Romaji:   {japanese_to_romaji(japanese)}")
    print()
    
    # 韩语
    korean = "안녕하세요"
    print(f"Korean:  {korean}")
    print(f"Romaji:  {hangul_to_romaji(korean)}")
    print()
    
    # 自动检测
    texts = ["Привет", "Γειά", "こんにちは", "안녕하세요", "مرحبا"]
    print("Auto detection:")
    for t in texts:
        result, script = auto_transliterate(t)
        print(f"  {t} ({script}) -> {result}")