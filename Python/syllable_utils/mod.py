"""
音节计数工具 (Syllable Counter Utils)

提供英文单词和句子的音节计数功能，支持：
- 单词音节计数
- 句子音节计数
- 音节模式分析
- 诗歌韵律分析
- 语音合成预处理

零外部依赖，仅使用 Python 标准库。
"""

import re
from typing import List, Tuple, Dict, Optional
from collections import Counter


# 常见单词音节数字典（用于提高准确性）
SYLLABLE_DICT: Dict[str, int] = {
    # 单音节词
    "the": 1, "a": 1, "an": 1, "is": 1, "are": 1, "was": 1, "were": 1,
    "be": 1, "been": 1, "being": 2, "have": 1, "has": 1, "had": 1,
    "do": 1, "does": 1, "did": 1, "will": 1, "would": 1, "could": 1,
    "should": 1, "may": 1, "might": 1, "must": 1, "shall": 1, "can": 1,
    "i": 1, "you": 1, "he": 1, "she": 1, "it": 1, "we": 1, "they": 1,
    "me": 1, "him": 1, "her": 1, "us": 1, "them": 1,
    "my": 1, "your": 1, "his": 1, "its": 1, "our": 1, "their": 1,
    "this": 1, "that": 1, "these": 1, "those": 1,
    "here": 1, "there": 1, "where": 1, "when": 1, "why": 1, "how": 1,
    "what": 1, "who": 1, "which": 1, "whom": 1, "whose": 1,
    "not": 1, "no": 1, "yes": 1, "but": 1, "and": 1, "or": 1, "nor": 1,
    "for": 1, "to": 1, "of": 1, "in": 1, "on": 1, "at": 1, "by": 1,
    "with": 1, "from": 1, "into": 2, "onto": 2, "upon": 2,
    "about": 2, "above": 2, "across": 2, "after": 2, "against": 2,
    "along": 2, "among": 2, "around": 2, "before": 2, "behind": 2,
    "below": 2, "beneath": 2, "beside": 2, "between": 2, "beyond": 2,
    "during": 2, "except": 2, "inside": 2, "outside": 2, "since": 1,
    "through": 1, "throughout": 2, "toward": 2, "under": 2, "until": 2,
    "within": 2, "without": 2,
    # 双音节词
    "happy": 2, "baby": 2, "city": 2, "party": 2, "story": 2,
    "water": 2, "money": 2, "power": 2, "people": 2, "little": 2,
    "very": 2, "many": 2, "only": 2, "also": 2, "even": 2,
    "first": 1, "second": 2, "third": 1, "other": 2, "another": 3,
    "some": 1, "something": 2, "someone": 2, "sometime": 2,
    "any": 2, "anyone": 3, "anything": 3, "anywhere": 3,
    "every": 2, "everyone": 3, "everything": 3, "everywhere": 3,
    "make": 1, "made": 1, "making": 2, "take": 1, "taken": 2, "taking": 2,
    "give": 1, "given": 2, "giving": 2, "live": 1, "living": 2,
    "love": 1, "loving": 2, "come": 1, "coming": 2, "came": 1,
    "go": 1, "going": 2, "went": 1, "gone": 1,
    "see": 1, "seeing": 2, "seen": 1, "saw": 1,
    "know": 1, "knowing": 2, "known": 1, "knew": 1,
    "think": 1, "thinking": 2, "thought": 1,
    "say": 1, "saying": 2, "said": 1,
    "tell": 1, "telling": 2, "told": 1,
    "find": 1, "finding": 2, "found": 1,
    "give": 1, "giving": 2, "given": 2,
    "work": 1, "working": 2, "worked": 1,
    "call": 1, "calling": 2, "called": 1,
    "try": 1, "trying": 2, "tried": 1,
    "ask": 1, "asking": 2, "asked": 1,
    "need": 1, "needing": 2, "needed": 2,
    "feel": 1, "feeling": 2, "felt": 1,
    "become": 2, "became": 2, "becoming": 3,
    "leave": 1, "leaving": 2, "left": 1,
    "bring": 1, "bringing": 2, "brought": 1,
    "begin": 2, "began": 2, "begun": 2, "beginning": 3,
    "keep": 1, "keeping": 2, "kept": 1,
    "hold": 1, "holding": 2, "held": 1,
    "write": 1, "writing": 2, "written": 2, "wrote": 1,
    "stand": 1, "standing": 2, "stood": 1,
    "hear": 1, "hearing": 2, "heard": 1,
    "let": 1, "letting": 2, "let": 1,
    "mean": 1, "meaning": 2, "meant": 1,
    "set": 1, "setting": 2, "set": 1,
    "meet": 1, "meeting": 2, "met": 1,
    "run": 1, "running": 2, "ran": 1,
    "pay": 1, "paying": 2, "paid": 1,
    "sit": 1, "sitting": 2, "sat": 1,
    "speak": 1, "speaking": 2, "spoken": 2, "spoke": 1,
    "lie": 1, "lying": 2, "lay": 1, "lain": 1,
    "lead": 1, "leading": 2, "led": 1,
    "read": 1, "reading": 2, "read": 1,
    "grow": 1, "growing": 2, "grew": 1, "grown": 1,
    "lose": 1, "losing": 2, "lost": 1,
    "fall": 1, "falling": 2, "fell": 1, "fallen": 2,
    "send": 1, "sending": 2, "sent": 1,
    "build": 1, "building": 2, "built": 1,
    "understand": 3, "understanding": 4, "understood": 3,
    "draw": 1, "drawing": 2, "drew": 1, "drawn": 1,
    "break": 1, "breaking": 2, "broke": 1, "broken": 2,
    "spend": 1, "spending": 2, "spent": 1,
    "cut": 1, "cutting": 2, "cut": 1,
    "hit": 1, "hitting": 2, "hit": 1,
    "put": 1, "putting": 2, "put": 1,
    "hurt": 1, "hurting": 2, "hurt": 1,
    # 三音节词
    "beautiful": 3, "wonderful": 3, "important": 3, "different": 3,
    "interesting": 4, "necessary": 3, "remember": 3, "understand": 3,
    "family": 3, "company": 3, "country": 3, "problem": 2,
    "example": 3, "question": 2, "business": 2, "government": 3,
    "development": 4, "information": 4, "education": 4, "experience": 4,
    "environment": 4, "opportunity": 5, "community": 4, "communication": 5,
    # 特殊词
    "hour": 1, "fire": 2, "tire": 2, "wire": 2,
    "are": 1, "our": 1, "their": 1,
    "eye": 1, "eyes": 1, "ear": 1, "ears": 1,
    "idea": 3, "ideal": 2, "poem": 2, "poet": 2, "poetry": 3,
    "science": 2, "scientist": 3, "scientific": 4,
    "society": 4, "social": 2, "variety": 4, "various": 3,
    "quiet": 2, "quite": 1, "quit": 1,
    "flower": 2, "flour": 1, "shower": 2, "power": 2,
    "every": 2, "ever": 2, "never": 2, "forever": 3,
    "really": 2, "actually": 4, "finally": 3, "usually": 4,
    "probably": 3, "possibly": 3, "especially": 4, "generally": 4,
    "absolutely": 4, "definitely": 4, "certainly": 3, "obviously": 4,
}

# 常见后缀及其音节数调整
SUFFIX_ADJUSTMENTS: Dict[str, int] = {
    "es": -1,  # -es 结尾通常不增加音节（如: goes, does）
    "ed": -1,  # -ed 结尾通常不增加音节（如: worked, played）
    "e": 0,    # 静默 e 不计入音节
    "le": 1,   # -le 结尾通常增加音节（如: little, able）
    "tion": 1, # -tion 通常是一个音节
    "sion": 1, # -sion 通常是一个音节
    "ious": 2, # -ious 是两个音节
    "eous": 2, # -eous 是两个音节
    "ual": 2,  # -ual 是两个音节
    "ier": 2,  # -ier 是两个音节
    "ies": 2,  # -ies 是两个音节（如: stories）
    "ied": 2,  # -ied 是两个音节（如: studied）
}

# 不发音字母组合
SILENT_PATTERNS = [
    (r"e$", "e"),          # 词尾静默 e
    (r"[aeiou]ble$", ""),  # -able, -ible 结尾
    (r"[aeiou]re$", ""),   # -are, -ere, -ire, -ore, -ure 结尾
]


def count_syllables(word: str) -> int:
    """
    计算单个英文单词的音节数
    
    使用混合策略：
    1. 先查字典（最准确）
    2. 再用规则启发式计算
    
    Args:
        word: 英文单词
        
    Returns:
        音节数（最小为1）
        
    Examples:
        >>> count_syllables("hello")
        2
        >>> count_syllables("beautiful")
        3
        >>> count_syllables("the")
        1
    """
    if not word:
        return 0
    
    # 清理并转小写
    word = word.strip().lower()
    word = re.sub(r"[^a-z]", "", word)
    
    if not word:
        return 0
    
    # 查字典
    if word in SYLLABLE_DICT:
        return SYLLABLE_DICT[word]
    
    # 处理复数和过去式
    base_word = word
    if word.endswith("es") and len(word) > 3:
        # 检查是否是 -es 结尾的动词形式
        potential_base = word[:-2]
        if potential_base in SYLLABLE_DICT:
            return SYLLABLE_DICT[potential_base]
        if word.endswith("ies") and len(word) > 4:
            potential_base = word[:-3] + "y"
            if potential_base in SYLLABLE_DICT:
                return SYLLABLE_DICT[potential_base]
    
    if word.endswith("ed") and len(word) > 3:
        potential_base = word[:-2]
        if potential_base in SYLLABLE_DICT:
            base_count = SYLLABLE_DICT[potential_base]
            # -ed 是否发音
            if word.endswith("ted") or word.endswith("ded"):
                return base_count + 1
            return base_count
        if word.endswith("ied") and len(word) > 4:
            potential_base = word[:-3] + "y"
            if potential_base in SYLLABLE_DICT:
                return SYLLABLE_DICT[potential_base]
    
    if word.endswith("ing") and len(word) > 4:
        potential_base = word[:-3]
        if potential_base in SYLLABLE_DICT:
            return SYLLABLE_DICT[potential_base] + 1
        if word.endswith("ying") and len(word) > 5:
            potential_base = word[:-4] + "ie"
            if potential_base in SYLLABLE_DICT:
                return SYLLABLE_DICT[potential_base] + 1
        if word.endswith("ing") and len(word) > 4:
            potential_base = word[:-3] + "e"
            if potential_base in SYLLABLE_DICT:
                return SYLLABLE_DICT[potential_base]
    
    # 启发式计算
    return _count_syllables_heuristic(word)


def _count_syllables_heuristic(word: str) -> int:
    """
    使用启发式规则计算音节数
    
    Args:
        word: 清理后的英文单词
        
    Returns:
        估计的音节数
    """
    if not word:
        return 0
    
    # 特殊情况：单个字母
    if len(word) == 1:
        return 1 if word in "aeiou" else 1
    
    # 计数元音组（连续元音算作一个音节）
    vowel_groups = re.findall(r"[aeiouy]+", word)
    count = len(vowel_groups)
    
    # 特殊处理 -le 结尾
    if word.endswith("le") and len(word) > 2 and word[-3] not in "aeiouy":
        count += 1
    
    # 处理词尾静默 e
    if word.endswith("e"):
        count -= 1
    
    # 处理 -es 结尾（复数或动词第三人称）
    if word.endswith("es") and len(word) > 3:
        if word.endswith("ches") or word.endswith("shes") or word.endswith("xes") or word.endswith("ses") or word.endswith("zes"):
            # -es 发音为一个音节
            pass
        else:
            count -= 1
    
    # 处理 -ed 结尾
    if word.endswith("ed") and len(word) > 3:
        if word.endswith("ted") or word.endswith("ded"):
            # -ed 发音
            pass
        else:
            count -= 1
    
    # 处理 y 作为元音
    if 'y' in word and not word.startswith('y'):
        # y 在词中通常作为元音
        pass
    
    # 处理特殊后缀
    for suffix, adj in SUFFIX_ADJUSTMENTS.items():
        if word.endswith(suffix) and len(word) > len(suffix):
            count += adj
            break
    
    # 确保至少有一个音节
    return max(1, count)


def count_sentence_syllables(sentence: str) -> int:
    """
    计算句子的总音节数
    
    Args:
        sentence: 英文句子
        
    Returns:
        总音节数
        
    Examples:
        >>> count_sentence_syllables("Hello world")
        3
        >>> count_sentence_syllables("I love programming")
        6
    """
    if not sentence:
        return 0
    
    # 提取单词
    words = re.findall(r"[a-zA-Z]+", sentence)
    
    total = 0
    for word in words:
        total += count_syllables(word)
    
    return total


def get_syllable_pattern(sentence: str) -> List[int]:
    """
    获取句子中每个单词的音节数模式
    
    Args:
        sentence: 英文句子
        
    Returns:
        每个单词的音节数列表
        
    Examples:
        >>> get_syllable_pattern("I love Python")
        [1, 1, 2]
    """
    if not sentence:
        return []
    
    words = re.findall(r"[a-zA-Z]+", sentence)
    return [count_syllables(word) for word in words]


def get_syllable_breakdown(word: str) -> Dict[str, any]:
    """
    获取单词的音节详细分析
    
    Args:
        word: 英文单词
        
    Returns:
        包含详细分析的字典
        
    Examples:
        >>> get_syllable_breakdown("beautiful")
        {'word': 'beautiful', 'syllables': 3, 'pattern': [1, 1, 1], 'method': 'dict'}
    """
    if not word:
        return {"word": "", "syllables": 0, "pattern": [], "method": "empty"}
    
    clean_word = word.strip().lower()
    clean_word = re.sub(r"[^a-z]", "", clean_word)
    
    if clean_word in SYLLABLE_DICT:
        syllables = SYLLABLE_DICT[clean_word]
        method = "dict"
    else:
        syllables = _count_syllables_heuristic(clean_word)
        method = "heuristic"
    
    return {
        "word": word,
        "syllables": syllables,
        "pattern": [1] * syllables,  # 简化模式
        "method": method
    }


def analyze_rhyme_scheme(text: str) -> Dict[str, any]:
    """
    分析文本的韵律结构（用于诗歌分析）
    
    Args:
        text: 多行英文文本
        
    Returns:
        包含韵律分析的字典
        
    Examples:
        >>> text = "The stars shine bright\\nIn the quiet night\\nDreams take their flight\\nWith all their might"
        >>> result = analyze_rhyme_scheme(text)
    """
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    
    analysis = {
        "line_count": len(lines),
        "lines": [],
        "rhyme_scheme": "",
        "syllable_counts": [],
        "meter": []
    }
    
    # 分析每行
    for line in lines:
        words = re.findall(r"[a-zA-Z]+", line)
        syllables = sum(count_syllables(w) for w in words)
        last_word = words[-1] if words else ""
        
        analysis["lines"].append({
            "text": line,
            "syllables": syllables,
            "word_count": len(words),
            "last_word": last_word
        })
        analysis["syllable_counts"].append(syllables)
    
    # 推断韵脚模式（基于最后一个单词的结尾音）
    rhyme_pattern = []
    rhyme_groups: Dict[str, str] = {}
    current_label = 'A'
    
    for line_info in analysis["lines"]:
        last_word = line_info["last_word"].lower()
        
        # 获取结尾音（最后2-3个字母）
        if len(last_word) >= 2:
            ending = last_word[-2:] if len(last_word) >= 3 else last_word[-1:]
        else:
            ending = last_word
        
        # 检查是否已有相同的韵脚
        found = False
        for existing_ending, label in rhyme_groups.items():
            if _sounds_similar(ending, existing_ending):
                rhyme_pattern.append(label)
                found = True
                break
        
        if not found:
            rhyme_groups[ending] = current_label
            rhyme_pattern.append(current_label)
            current_label = chr(ord(current_label) + 1)
    
    analysis["rhyme_scheme"] = "".join(rhyme_pattern)
    
    # 分析格律
    avg_syllables = sum(analysis["syllable_counts"]) / len(analysis["syllable_counts"]) if analysis["syllable_counts"] else 0
    if avg_syllables > 0:
        if all(s == analysis["syllable_counts"][0] for s in analysis["syllable_counts"]):
            analysis["meter"] = f"Regular ({analysis['syllable_counts'][0]} syllables per line)"
        else:
            analysis["meter"] = f"Irregular (avg: {avg_syllables:.1f} syllables)"
    
    return analysis


def _sounds_similar(ending1: str, ending2: str) -> bool:
    """
    判断两个结尾音是否相似（用于押韵判断）
    """
    if ending1 == ending2:
        return True
    
    # 元音替换
    vowel_map = {
        'a': ['a', 'e', 'i'],
        'e': ['e', 'a', 'i'],
        'i': ['i', 'e', 'y'],
        'o': ['o', 'u'],
        'u': ['u', 'o'],
        'y': ['y', 'i', 'e']
    }
    
    if ending1[-1] in vowel_map:
        if ending2[-1] in vowel_map.get(ending1[-1], []):
            return True
    
    return False


def get_stress_pattern(word: str) -> List[int]:
    """
    估计单词的重音模式（简化版）
    
    Args:
        word: 英文单词
        
    Returns:
        重音模式列表（1=重音, 0=非重音）
        
    Examples:
        >>> get_stress_pattern("beautiful")
        [1, 0, 0]
    """
    syllables = count_syllables(word)
    if syllables <= 1:
        return [1] if syllables == 1 else []
    
    # 简化规则：第一个音节通常重音
    pattern = [0] * syllables
    pattern[0] = 1
    
    # 某些后缀会影响重音
    word_lower = word.lower()
    if word_lower.endswith("tion") or word_lower.endswith("sion"):
        # -tion/-sion 前面的音节重音
        pattern = [0] * syllables
        if syllables > 1:
            pattern[-2] = 1
    elif word_lower.endswith("ic"):
        # -ic 结尾通常倒数第二音节重音
        pattern = [0] * syllables
        if syllables > 1:
            pattern[-2] = 1
    elif word_lower.endswith("ity"):
        # -ity 结尾通常倒数第三音节重音
        pattern = [0] * syllables
        if syllables > 2:
            pattern[-3] = 1
    
    return pattern


def suggest_haiku_lines(text: str) -> List[Dict[str, any]]:
    """
    从文本中提取可能的俳句结构（5-7-5音节模式）
    
    Args:
        text: 英文文本
        
    Returns:
        可能的俳句结构列表
        
    Examples:
        >>> suggest_haiku_lines("The gentle rain falls soft upon the ground below my feet")
        >>> # 返回符合5-7-5模式的行组合
    """
    words = re.findall(r"[a-zA-Z]+", text)
    if not words:
        return []
    
    # 计算每个单词的音节
    word_syllables = [(w, count_syllables(w)) for w in words]
    
    haikus = []
    
    # 寻找 5-7-5 模式
    for i in range(len(words)):
        total = 0
        first_line_end = -1
        
        # 第一行：5个音节
        for j in range(i, len(words)):
            total += word_syllables[j][1]
            if total == 5:
                first_line_end = j
                break
            elif total > 5:
                break
        
        if first_line_end == -1:
            continue
        
        # 第二行：7个音节
        total = 0
        second_line_end = -1
        for j in range(first_line_end + 1, len(words)):
            total += word_syllables[j][1]
            if total == 7:
                second_line_end = j
                break
            elif total > 7:
                break
        
        if second_line_end == -1:
            continue
        
        # 第三行：5个音节
        total = 0
        third_line_end = -1
        for j in range(second_line_end + 1, len(words)):
            total += word_syllables[j][1]
            if total == 5:
                third_line_end = j
                break
            elif total > 5:
                break
        
        if third_line_end != -1:
            first_line = " ".join(words[i:first_line_end + 1])
            second_line = " ".join(words[first_line_end + 1:second_line_end + 1])
            third_line = " ".join(words[second_line_end + 1:third_line_end + 1])
            
            haikus.append({
                "first_line": first_line,
                "second_line": second_line,
                "third_line": third_line,
                "start_word": i,
                "end_word": third_line_end
            })
    
    return haikus


def readability_score(text: str) -> Dict[str, float]:
    """
    计算文本的可读性分数（基于音节数）
    
    简化版的 Flesch-Kincaid 可读性计算
    
    Args:
        text: 英文文本
        
    Returns:
        包含可读性指标的字典
        
    Examples:
        >>> readability_score("The cat sat on the mat")
        {'syllables': 6, 'words': 6, 'sentences': 1, 'avg_syllables': 1.0, 'difficulty': 'easy'}
    """
    if not text:
        return {"syllables": 0, "words": 0, "sentences": 0, "avg_syllables": 0, "difficulty": "unknown"}
    
    # 提取单词和句子
    words = re.findall(r"[a-zA-Z]+", text)
    sentences = re.split(r"[.!?]+", text)
    sentences = [s.strip() for s in sentences if s.strip()]
    
    if not words:
        return {"syllables": 0, "words": 0, "sentences": 0, "avg_syllables": 0, "difficulty": "unknown"}
    
    # 计算总音节数
    total_syllables = sum(count_syllables(w) for w in words)
    
    # 计算指标
    word_count = len(words)
    sentence_count = len(sentences) if sentences else 1
    avg_syllables = total_syllables / word_count if word_count > 0 else 0
    
    # 判断难度
    if avg_syllables < 1.3:
        difficulty = "easy"
    elif avg_syllables < 1.6:
        difficulty = "medium"
    else:
        difficulty = "hard"
    
    return {
        "syllables": total_syllables,
        "words": word_count,
        "sentences": sentence_count,
        "avg_syllables": round(avg_syllables, 2),
        "avg_word_length": round(sum(len(w) for w in words) / word_count, 2),
        "difficulty": difficulty
    }


def count_complex_words(text: str, threshold: int = 3) -> Dict[str, any]:
    """
    统计文本中的复杂词（多音节词）
    
    Args:
        text: 英文文本
        threshold: 复杂词的音节阈值（默认3）
        
    Returns:
        复杂词统计信息
        
    Examples:
        >>> count_complex_words("I love programming and beautiful sunsets")
        {'complex_words': ['programming', 'beautiful'], 'count': 2, 'percentage': 28.57}
    """
    words = re.findall(r"[a-zA-Z]+", text)
    if not words:
        return {"complex_words": [], "count": 0, "percentage": 0}
    
    complex_words = []
    for word in words:
        if count_syllables(word) >= threshold:
            complex_words.append(word)
    
    percentage = (len(complex_words) / len(words)) * 100 if words else 0
    
    return {
        "complex_words": complex_words,
        "count": len(complex_words),
        "total_words": len(words),
        "percentage": round(percentage, 2)
    }


def split_into_syllables(word: str) -> List[str]:
    """
    将单词拆分为音节（简化版本）
    
    注意：这是一个简化实现，不处理所有边缘情况
    
    Args:
        word: 英文单词
        
    Returns:
        音节列表
        
    Examples:
        >>> split_into_syllables("beautiful")
        ['beau', 'ti', 'ful']
    """
    if not word:
        return []
    
    word = word.lower().strip()
    word = re.sub(r"[^a-z]", "", word)
    
    if len(word) <= 2:
        return [word] if word else []
    
    syllables = count_syllables(word)
    if syllables == 1:
        return [word]
    
    # 简化拆分：按元音组拆分
    result = []
    current = ""
    vowels = "aeiouy"
    in_vowel_group = False
    vowel_count = 0
    
    for i, char in enumerate(word):
        current += char
        is_vowel = char in vowels
        
        if is_vowel and not in_vowel_group:
            vowel_count += 1
            in_vowel_group = True
        elif not is_vowel:
            in_vowel_group = False
        
        # 尝试在音节边界拆分
        if vowel_count >= 1 and not is_vowel and i < len(word) - 1:
            next_is_vowel = word[i + 1] in vowels if i + 1 < len(word) else False
            if next_is_vowel:
                result.append(current)
                current = ""
                vowel_count = 0
    
    if current:
        result.append(current)
    
    # 确保结果数量匹配预期音节数
    if len(result) != syllables:
        # 回退到等分
        if syllables > 0:
            chunk_size = len(word) // syllables
            result = [word[i:i + chunk_size] for i in range(0, len(word), chunk_size)]
            # 处理剩余
            if len(result) > syllables:
                result = result[:syllables]
    
    return result


def generate_syllable_word_list(syllable_count: int, word_list: Optional[List[str]] = None) -> List[str]:
    """
    生成指定音节数的单词列表
    
    Args:
        syllable_count: 目标音节数
        word_list: 可选的单词列表（默认使用内置字典）
        
    Returns:
        符合音节数要求的单词列表
        
    Examples:
        >>> words = generate_syllable_word_list(1)
        >>> len(words) > 0
        True
    """
    if word_list is None:
        # 使用内置字典中符合音节数的单词
        return [word for word, count in SYLLABLE_DICT.items() if count == syllable_count]
    
    return [word for word in word_list if count_syllables(word) == syllable_count]


def get_word_rhythm(word: str) -> str:
    """
    获取单词的节奏模式（用符号表示）
    
    Args:
        word: 英文单词
        
    Returns:
        节奏模式字符串（/ = 重音, x = 非重音）
        
    Examples:
        >>> get_word_rhythm("beautiful")
        '/ x x'
    """
    stress = get_stress_pattern(word)
    if not stress:
        return ""
    
    return " ".join("/" if s == 1 else "x" for s in stress)


def batch_count_syllables(words: List[str]) -> Dict[str, int]:
    """
    批量计算多个单词的音节数
    
    Args:
        words: 单词列表
        
    Returns:
        单词到音节数的映射
        
    Examples:
        >>> batch_count_syllables(["hello", "world", "beautiful"])
        {'hello': 2, 'world': 1, 'beautiful': 3}
    """
    return {word: count_syllables(word) for word in words}


def get_syllable_stats(text: str) -> Dict[str, any]:
    """
    获取文本的音节统计信息
    
    Args:
        text: 英文文本
        
    Returns:
        统计信息字典
        
    Examples:
        >>> get_syllable_stats("Hello beautiful world")
        {'total_syllables': 6, 'word_count': 3, 'avg_per_word': 2.0, 'distribution': {1: 1, 2: 1, 3: 1}}
    """
    words = re.findall(r"[a-zA-Z]+", text)
    if not words:
        return {"total_syllables": 0, "word_count": 0, "avg_per_word": 0, "distribution": {}}
    
    syllable_counts = [count_syllables(w) for w in words]
    distribution = Counter(syllable_counts)
    
    return {
        "total_syllables": sum(syllable_counts),
        "word_count": len(words),
        "avg_per_word": round(sum(syllable_counts) / len(words), 2),
        "min_syllables": min(syllable_counts),
        "max_syllables": max(syllable_counts),
        "distribution": dict(sorted(distribution.items()))
    }


# 便捷函数别名
count = count_syllables
count_word = count_syllables
count_text = count_sentence_syllables
pattern = get_syllable_pattern
breakdown = get_syllable_breakdown
rhythm = get_word_rhythm