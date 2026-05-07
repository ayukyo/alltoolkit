"""
Wordle 游戏辅助工具
支持单词过滤、最优猜测计算、字母频率分析等功能
零外部依赖，纯 Python 实现
"""

import math
from typing import List, Dict, Set, Tuple, Optional
from collections import Counter
from functools import lru_cache

# 常见5字母英语单词列表（约500个）
DEFAULT_WORDS: List[str] = [
    # 常见动词
    "about", "above", "abuse", "actor", "acute", "admit", "adopt", "adult", "after", "again",
    "agent", "agree", "ahead", "alarm", "album", "alert", "alike", "alive", "allow", "alone",
    "along", "alter", "among", "anger", "angle", "angry", "apart", "apple", "apply", "arena",
    "argue", "arise", "array", "aside", "asset", "avoid", "award", "aware", "awful",
    # 常见名词
    "bacon", "badge", "badly", "baker", "bases", "basic", "basin", "basis", "batch", "beach",
    "beard", "beast", "began", "begin", "being", "belly", "below", "bench", "berry", "birth",
    "black", "blade", "blame", "blank", "blast", "blaze", "bleed", "blend", "bless", "blind",
    "block", "blood", "bloom", "board", "boast", "bonus", "boost", "booth", "bound", "brain",
    "brand", "brass", "brave", "bread", "break", "breed", "brick", "bride", "brief", "bring",
    "broad", "broke", "brook", "brown", "brush", "build", "built", "bunch", "burst", "buyer",
    "cabin", "cable", "camel", "candy", "cargo", "carry", "carve", "catch", "cause", "cease",
    "chain", "chair", "chalk", "champ", "chaos", "charm", "chart", "chase", "cheap", "check",
    "cheek", "cheer", "chess", "chest", "chief", "child", "chill", "china", "chord", "chunk",
    "claim", "class", "clean", "clear", "clerk", "click", "cliff", "climb", "cling", "clock",
    "close", "cloth", "cloud", "coach", "coast", "color", "comet", "comic", "coral", "couch",
    "count", "court", "cover", "crack", "craft", "crane", "crash", "crawl", "crazy", "cream", "creek",
    "creep", "crest", "crime", "crisp", "cross", "crowd", "crown", "crude", "cruel", "crush",
    "curve", "cycle",
    # D开头单词
    "daily", "dairy", "daisy", "dance", "dates", "dealt", "death", "debut", "decay", "decor",
    "delay", "delta", "dense", "depth", "derby", "deter", "digit", "dirty", "disco", "ditch",
    "diver", "dizzy", "dodge", "doing", "doubt", "dough", "dozen", "draft", "drain", "drake",
    "drama", "drank", "drape", "drawn", "dread", "dream", "dress", "dried", "drift", "drill",
    "drink", "drive", "droit", "drown", "drown", "drunk", "dwell",
    # E开头单词
    "eager", "eagle", "early", "earth", "eased", "eaten", "eater", "edge", "eight", "elbow",
    "elder", "elect", "elite", "email", "empty", "enemy", "enjoy", "enter", "entry", "equal",
    "equip", "erase", "error", "essay", "ethic", "evade", "event", "every", "exact", "exams",
    "exist", "extra",
    # F开头单词
    "fable", "faced", "facet", "faith", "false", "fancy", "fatal", "fatty", "fault", "favor",
    "feast", "fence", "ferry", "fetch", "fever", "fiber", "field", "fiery", "fifth", "fifty",
    "fight", "final", "first", "fixed", "flair", "flame", "flank", "flash", "flask", "fleet",
    "flesh", "flick", "fling", "float", "flock", "flood", "floor", "flora", "flour", "flown",
    "fluid", "flush", "focal", "focus", "foggy", "force", "forge", "forth", "forty", "forum",
    "found", "frame", "frank", "fraud", "freak", "fresh", "friar", "fried", "frill", "frisk",
    "front", "frost", "fruit", "fully", "fungi", "funny", "fuzzy",
    # G开头单词
    "gable", "gains", "games", "gamma", "gangs", "gaudy", "gauge", "gaunt", "gauze", "gavel",
    "gears", "genes", "genre", "ghost", "giant", "given", "giver", "glade", "gland", "glare",
    "glass", "glaze", "gleam", "glean", "glide", "glint", "globe", "gloom", "glory", "gloss",
    "glove", "glyph", "goats", "going", "golden", "golem", "goner", "goods", "goose", "gorge",
    "gourd", "grace", "grade", "grain", "grand", "grant", "grape", "graph", "grasp", "grass",
    "grave", "gravy", "graze", "great", "greed", "greek", "green", "greet", "grief", "grill",
    "grind", "gripe", "groan", "groom", "grope", "gross", "group", "grove", "growl", "grown",
    "guard", "guess", "guest", "guide", "guild", "guilt", "guise", "gulch", "gummy", "gypsy",
    # H开头单词
    "habit", "hairy", "handy", "happy", "harsh", "haste", "hasty", "hatch", "haunt", "haven",
    "haven", "heart", "heavy", "hedge", "heist", "hello", "hence", "hinge", "hobby", "honey",
    "honor", "horse", "hotel", "hound", "house", "hover", "human", "humid", "humor", "hurry",
    # I开头单词
    "ideal", "idiom", "idiot", "image", "imply", "index", "indie", "inner", "input", "inter",
    "intro", "irony", "issue", "ivory",
    # J开头单词
    "jelly", "jerky", "jewel", "jiffy", "joint", "joker", "jolly", "joust", "judge", "juice",
    "juicy", "jumbo", "jumpy", "juror",
    # K开头单词
    "karma", "kayak", "khaki", "kinky", "kiosk", "kitty", "knack", "knead", "kneel", "knife",
    "knock", "known",
    # L开头单词
    "label", "labor", "lance", "large", "laser", "latch", "later", "latex", "laugh", "layer",
    "leafy", "learn", "lease", "least", "leave", "ledge", "legal", "lemon", "level", "lever",
    "light", "limbo", "limit", "linen", "liner", "lingo", "liver", "lobby", "local", "lofty",
    "logic", "login", "loose", "lorry", "loser", "lotus", "lousy", "lover", "lower", "loyal",
    "lucky", "lunar", "lunch", "lurch", "lying", "lyric",
    # M开头单词
    "macho", "macro", "magic", "major", "maker", "manor", "maple", "march", "marry", "marsh",
    "match", "maybe", "mayor", "medal", "media", "melon", "mercy", "merge", "merit", "merry",
    "messy", "metal", "meter", "micro", "midst", "might", "mimic", "mince", "minor", "minus",
    "mirth", "miser", "misty", "mixed", "mixer", "model", "modem", "moist", "money", "month",
    "moose", "moral", "motor", "motto", "mould", "mound", "mount", "mourn", "mouse", "mouth",
    "movie", "muddy", "mummy", "mural", "murky", "music", "musty", "mutch",
    # N开头单词
    "naive", "naked", "nasty", "naval", "nerve", "never", "newer", "newly", "night", "ninth",
    "noble", "noise", "noisy", "north", "notch", "noted", "novel", "nudge", "nurse", "nutty",
    # O开头单词
    "occur", "ocean", "oddly", "offer", "often", "olive", "omega", "onion", "onset", "opera",
    "optic", "orbit", "order", "organ", "other", "ought", "ounce", "outer", "outgo", "outwit",
    "owner", "oxide", "ozone",
    # P开头单词
    "paddy", "pagan", "paint", "panel", "panic", "paper", "party", "pasta", "paste", "pasty",
    "patch", "pause", "peace", "peach", "pearl", "pedal", "penny", "perch", "peril", "perky",
    "petal", "petty", "phase", "phone", "photo", "piano", "piece", "pilot", "pinch", "pitch",
    "pixel", "pizza", "place", "plain", "plane", "plant", "plate", "plaza", "plead", "pleat",
    "plier", "pluck", "plumb", "plump", "plunge", "plus", "poach", "point", "poise", "poker",
    "polar", "polka", "polyp", "porch", "poser", "posit", "pouch", "pound", "power", "press",
    "price", "pride", "prime", "print", "prior", "prism", "prize", "probe", "proof", "prose",
    "proud", "prove", "prowl", "proxy", "prune", "psalm", "pulse", "punch", "pupil", "puppy",
    "purge", "purse", "pushy", "putty",
    # Q开头单词
    "quake", "qualm", "quart", "quasi", "queen", "query", "quest", "queue", "quick", "quiet",
    "quilt", "quirk", "quota", "quote",
    # R开头单词
    "radar", "radio", "rainy", "raise", "rally", "ranch", "range", "rapid", "ratio", "razor",
    "reach", "react", "ready", "realm", "rebel", "refer", "reign", "relax", "relay", "relic",
    "remit", "renew", "repay", "reply", "reset", "resin", "retro", "rhino", "rider", "ridge",
    "rifle", "right", "rigid", "rigor", "rinse", "ripen", "risen", "risky", "rival", "river",
    "rivet", "roach", "roast", "robot", "rocky", "roger", "rogue", "roman", "roost", "rough",
    "round", "route", "rover", "rowdy", "royal", "rugby", "ruler", "rumor", "rural", "rusty",
    # S开头单词
    "sadly", "saint", "salad", "salty", "sandy", "sassy", "sauce", "savor", "scale", "scalp",
    "scant", "scare", "scarf", "scary", "scene", "scent", "scope", "score", "scout", "scrap",
    "screw", "seize", "sense", "serum", "serve", "setup", "seven", "shade", "shady", "shaft",
    "shake", "shaky", "shall", "shame", "shape", "share", "shark", "sharp", "shave", "shawl",
    "shear", "sheen", "sheep", "sheer", "sheet", "shelf", "shell", "shift", "shine", "shiny",
    "shire", "shirt", "shock", "shoot", "shore", "short", "shout", "shove", "shown", "showy",
    "shrub", "shrug", "sight", "sigma", "silly", "since", "sixth", "sixty", "sized", "skate",
    "skill", "skimp", "skirt", "skull", "slack", "slain", "slang", "slant", "slash", "slate",
    "slave", "sleek", "sleep", "sleet", "slept", "slice", "slide", "slime", "slimy", "sling",
    "slink", "slope", "sloth", "slump", "small", "smart", "smash", "smell", "smile", "smoke",
    "smoky", "snack", "snail", "snake", "snare", "snarl", "sneak", "sniff", "snore", "snort",
    "snout", "snowy", "sober", "solar", "solid", "solve", "sonar", "sonic", "sorry", "sound",
    "south", "space", "spade", "spare", "spark", "spawn", "speak", "spear", "speed", "spell",
    "spend", "spent", "spice", "spicy", "spill", "spine", "spiny", "splat", "split", "spoke",
    "spoon", "sport", "spout", "spray", "spree", "squad", "squat", "squid", "stack", "staff",
    "stage", "stain", "stair", "stake", "stale", "stalk", "stall", "stamp", "stand", "stare",
    "stark", "start", "state", "stave", "stead", "steak", "steal", "steam", "steel", "steep",
    "steer", "stern", "stick", "stiff", "still", "sting", "stink", "stock", "stomp", "stone",
    "stony", "stood", "stool", "stoop", "store", "stork", "storm", "story", "stout", "stove",
    "strap", "straw", "stray", "strip", "strut", "stuck", "study", "stuff", "stump", "stung",
    "stunk", "stunt", "style", "suave", "sugar", "suite", "sunny", "super", "surge", "sushi",
    "swamp", "swarm", "swear", "sweat", "sweep", "sweet", "swell", "swept", "swift", "swing",
    "swipe", "swirl", "swiss", "sword", "swore", "sworn", "swung",
    # T开头单词
    "table", "taboo", "tacit", "tacky", "taint", "taken", "tally", "talon", "tango", "tangy",
    "taper", "tapir", "tardy", "taste", "tasty", "tatty", "taunt", "tawny", "teach", "teary",
    "tease", "teddy", "teeth", "tempo", "tenet", "tenor", "tense", "tenth", "tepid", "terra",
    "terse", "thank", "theft", "their", "theme", "there", "these", "thick", "thief", "thigh",
    "thing", "think", "third", "thorn", "those", "three", "threw", "throw", "thumb", "thump",
    "tiger", "tight", "tilde", "timer", "timid", "tipsy", "tired", "titan", "title", "toast",
    "today", "token", "tonal", "topic", "torch", "total", "touch", "tough", "towel", "tower",
    "toxic", "trace", "track", "tract", "trade", "trail", "train", "trait", "tramp", "trash",
    "trawl", "tread", "treat", "trend", "trial", "tribe", "trick", "tried", "trill", "tripe",
    "trite", "troll", "troop", "trout", "truce", "truck", "truly", "trump", "trunk", "trust",
    "truth", "tuber", "tulip", "tumor", "tuner", "tunic", "turbo", "tutor", "twang", "tweak",
    "tweed", "tweet", "twice", "twine", "twirl", "twist", "tying",
    # U开头单词
    "udder", "ulcer", "ultra", "umbra", "uncle", "under", "undid", "undue", "unfed", "unfit",
    "unify", "union", "unite", "unity", "unlit", "unmet", "unset", "untie", "until", "upper",
    "upset", "urban", "urine", "usage", "usher", "using", "usual", "utter",
    # V开头单词
    "vague", "valid", "valor", "value", "valve", "vapor", "vault", "vaunt", "vegan", "venom",
    "venue", "verge", "verse", "verso", "vexed", "vicar", "video", "vigor", "vinyl", "viola",
    "viper", "viral", "virus", "visit", "visor", "vista", "vital", "vivid", "vocal", "vodka",
    "vogue", "voice", "voter", "vouch", "vowel",
    # W开头单词
    "wacky", "wafer", "wager", "wagon", "waist", "waltz", "warty", "waste", "watch", "water",
    "waver", "weary", "weave", "wedge", "weedy", "weigh", "weird", "whale", "wharf", "wheat",
    "wheel", "where", "which", "while", "whine", "whirl", "white", "whole", "whose", "widen",
    "wider", "widow", "width", "wield", "wight", "willy", "wimpy", "wince", "winch", "windy",
    "wiper", "witch", "witty", "woken", "woman", "women", "woods", "woody", "world", "worry",
    "worse", "worst", "worth", "would", "wound", "woven", "wrack", "wrath", "wreak", "wreck",
    "wrest", "wring", "wrist", "write", "wrong", "wrote", "wrung",
    # X开头单词
    "xenon",
    # Y开头单词
    "yacht", "yearn", "yeast", "yield", "young", "youth", "yummy",
    # Z开头单词
    "zebra", "zesty", "zippy", "zonal", "zooms"
]


class WordleHelper:
    """
    Wordle 游戏辅助类
    
    功能：
    - 单词过滤（根据已知条件）
    - 最优猜测计算
    - 字母频率分析
    """
    
    def __init__(self, words: Optional[List[str]] = None):
        """
        初始化 Wordle 辅助器
        
        Args:
            words: 可选的单词列表，默认使用内置词库
        """
        # 明确区分 None 和空列表的情况
        if words is None:
            words = DEFAULT_WORDS
        self.words = [w.lower() for w in words if len(w) == 5]
        self._letter_freq: Optional[Dict[str, float]] = None
        self._position_freq: Optional[List[Dict[str, float]]] = None
    
    @property
    def letter_frequency(self) -> Dict[str, float]:
        """计算字母频率"""
        if self._letter_freq is None:
            self._calculate_frequencies()
        return self._letter_freq or {}
    
    @property
    def position_frequency(self) -> List[Dict[str, float]]:
        """计算每个位置的字母频率"""
        if self._position_freq is None:
            self._calculate_frequencies()
        return self._position_freq or [{} for _ in range(5)]
    
    def _calculate_frequencies(self) -> None:
        """计算字母频率和位置频率"""
        if not self.words:
            self._letter_freq = {}
            self._position_freq = [{} for _ in range(5)]
            return
        
        # 字母频率
        letter_counts: Counter = Counter()
        for word in self.words:
            letter_counts.update(set(word))  # 每个字母只计一次
        
        total = len(self.words)
        self._letter_freq = {
            letter: count / total 
            for letter, count in letter_counts.items()
        }
        
        # 位置频率
        self._position_freq = []
        for pos in range(5):
            pos_counts: Counter = Counter()
            for word in self.words:
                pos_counts[word[pos]] += 1
            self._position_freq.append({
                letter: count / total 
                for letter, count in pos_counts.items()
            })
    
    def filter_words(
        self,
        correct: Optional[str] = None,
        present: Optional[str] = None,
        absent: Optional[str] = None,
        pattern: Optional[str] = None,
        contains: Optional[str] = None,
        not_contains: Optional[str] = None,
        starts_with: Optional[str] = None,
        ends_with: Optional[str] = None,
        regex: Optional[str] = None
    ) -> List[str]:
        """
        根据多种条件过滤单词
        
        Args:
            correct: 正确位置的字母，用字母表示正确位置，其他位置用'.'或'_'表示
                     例如："..a.." 表示第3个字母是'a'
            present: 存在但位置不对的字母（字符串）
            absent: 不存在的字母（字符串）
            pattern: 正确位置的字母，格式同correct
            contains: 必须包含的字母
            not_contains: 不能包含的字母
            starts_with: 开头字母
            ends_with: 结尾字母
            regex: 正则表达式模式
        
        Returns:
            符合条件的单词列表
        """
        result = self.words.copy()
        
        # 处理正确位置
        correct_pattern = correct or pattern
        if correct_pattern:
            correct_pattern = correct_pattern.lower()
            for i, char in enumerate(correct_pattern):
                if char not in '._?*' and char.isalpha():
                    result = [w for w in result if w[i] == char]
        
        # 处理存在的字母（位置不对）
        if present:
            present = present.lower()
            for char in present:
                if char.isalpha():
                    result = [w for w in result if char in w]
        
        # 处理不存在的字母
        absent_letters = absent or not_contains
        if absent_letters:
            absent_letters = absent_letters.lower()
            result = [w for w in result if not any(c in absent_letters for c in w)]
        
        # 处理必须包含
        if contains:
            contains = contains.lower()
            for char in contains:
                if char.isalpha():
                    result = [w for w in result if char in w]
        
        # 处理开头字母
        if starts_with:
            starts_with = starts_with.lower()
            result = [w for w in result if w.startswith(starts_with)]
        
        # 处理结尾字母
        if ends_with:
            ends_with = ends_with.lower()
            result = [w for w in result if w.endswith(ends_with)]
        
        # 处理正则表达式
        if regex:
            import re
            try:
                pattern_re = re.compile(regex, re.IGNORECASE)
                result = [w for w in result if pattern_re.match(w)]
            except re.error:
                pass  # 无效正则，忽略
        
        return result
    
    def get_best_guess(
        self,
        candidates: Optional[List[str]] = None,
        method: str = "frequency"
    ) -> Tuple[str, float]:
        """
        获取最优猜测词
        
        Args:
            candidates: 候选词列表，默认使用所有词
            method: 计算方法
                - "frequency": 基于字母频率
                - "position": 基于位置频率
                - "entropy": 基于信息熵
                - "combined": 综合方法
        
        Returns:
            (最优词, 得分) 元组
        """
        # 如果 candidates 是空列表（非 None），返回空
        if candidates is not None and len(candidates) == 0:
            return ("", 0.0)
        
        words = candidates if candidates is not None else self.words
        if not words:
            return ("", 0.0)
        
        if len(words) == 1:
            return (words[0], 1.0)
        
        if method == "frequency":
            return self._best_by_frequency(words)
        elif method == "position":
            return self._best_by_position(words)
        elif method == "entropy":
            return self._best_by_entropy(words)
        else:  # combined
            return self._best_combined(words)
    
    def _best_by_frequency(self, words: List[str]) -> Tuple[str, float]:
        """基于字母频率选择最优猜测"""
        freq = self.letter_frequency
        best_word = ""
        best_score = -1.0
        
        for word in words:
            # 使用唯一字母的频率之和
            unique_letters = set(word)
            score = sum(freq.get(c, 0) for c in unique_letters)
            if score > best_score:
                best_score = score
                best_word = word
        
        return (best_word, best_score)
    
    def _best_by_position(self, words: List[str]) -> Tuple[str, float]:
        """基于位置频率选择最优猜测"""
        pos_freq = self.position_frequency
        best_word = ""
        best_score = -1.0
        
        for word in words:
            score = sum(
                pos_freq[i].get(word[i], 0) 
                for i in range(5)
            )
            if score > best_score:
                best_score = score
                best_word = word
        
        return (best_word, best_score)
    
    def _best_by_entropy(self, words: List[str]) -> Tuple[str, float]:
        """基于信息熵选择最优猜测"""
        best_word = ""
        best_entropy = -1.0
        
        for word in words:
            # 计算该词可能产生的反馈模式的信息熵
            pattern_counts: Counter = Counter()
            
            for answer in words:
                pattern = self._get_pattern(word, answer)
                pattern_counts[pattern] += 1
            
            # 计算熵
            total = len(words)
            entropy = 0.0
            for count in pattern_counts.values():
                p = count / total
                if p > 0:
                    entropy -= p * math.log2(p)
            
            if entropy > best_entropy:
                best_entropy = entropy
                best_word = word
        
        return (best_word, best_entropy)
    
    def _get_pattern(self, guess: str, answer: str) -> str:
        """
        获取猜测相对于答案的反馈模式
        2 = 正确位置（绿色）
        1 = 存在但位置错误（黄色）
        0 = 不存在（灰色）
        """
        pattern = ['0'] * 5
        answer_chars = list(answer)
        
        # 第一遍：标记正确位置
        for i in range(5):
            if guess[i] == answer[i]:
                pattern[i] = '2'
                answer_chars[i] = '#'  # 标记已使用
        
        # 第二遍：标记存在但位置错误
        for i in range(5):
            if pattern[i] == '0':
                if guess[i] in answer_chars:
                    pattern[i] = '1'
                    # 移除一个匹配
                    idx = answer_chars.index(guess[i])
                    answer_chars[idx] = '#'
        
        return ''.join(pattern)
    
    def _best_combined(self, words: List[str]) -> Tuple[str, float]:
        """综合方法选择最优猜测"""
        freq = self.letter_frequency
        pos_freq = self.position_frequency
        best_word = ""
        best_score = -1.0
        
        for word in words:
            # 频率得分
            unique_letters = set(word)
            freq_score = sum(freq.get(c, 0) for c in unique_letters)
            
            # 位置得分
            pos_score = sum(
                pos_freq[i].get(word[i], 0) 
                for i in range(5)
            )
            
            # 字母多样性得分（更多不同字母更好）
            diversity = len(unique_letters) / 5
            
            # 综合得分
            score = freq_score * 0.4 + pos_score * 0.4 + diversity * 0.2
            
            if score > best_score:
                best_score = score
                best_word = word
        
        return (best_word, best_score)
    
    def analyze_feedback(self, guess: str, feedback: str) -> Dict:
        """
        分析反馈并返回过滤条件
        
        Args:
            guess: 猜测的词
            feedback: 反馈字符串
                'g' 或 '2' 或 '=' 表示绿色（正确位置）
                'y' 或 '1' 或 '?' 表示黄色（存在但位置错误）
                'b' 或 '0' 或 'x' 或 '_' 表示灰色（不存在）
        
        Returns:
            包含过滤条件的字典
        """
        feedback = feedback.lower()
        correct = ['_'] * 5
        present = set()
        absent = set()
        yellow_positions: Dict[str, Set[int]] = {}  # 字母 -> 不能在的位置
        
        for i, (char, fb) in enumerate(zip(guess, feedback)):
            if fb in 'g2=':
                correct[i] = char
            elif fb in 'y1?':
                present.add(char)
                if char not in yellow_positions:
                    yellow_positions[char] = set()
                yellow_positions[char].add(i)
            elif fb in 'b0x_':
                # 只有当这个字母没有在其他位置出现时才算absent
                if char not in present and char not in correct:
                    absent.add(char)
        
        # 构建pattern
        pattern = ''.join(correct)
        
        return {
            'correct': pattern if '_' not in pattern else None,
            'pattern': pattern,
            'present': ''.join(present) if present else None,
            'absent': ''.join(absent) if absent else None,
            'yellow_positions': yellow_positions
        }
    
    def suggest_next_guess(
        self, 
        history: List[Tuple[str, str]]
    ) -> Tuple[str, List[str], int]:
        """
        根据历史猜测建议下一个最优猜测
        
        Args:
            history: 历史 (猜测, 反馈) 元组列表
                     反馈格式：'g'绿色 'y'黄色 'b'灰色
        
        Returns:
            (建议词, 剩余候选词, 候选词数量) 元组
        """
        candidates = self.words.copy()
        
        for guess, feedback in history:
            conditions = self.analyze_feedback(guess, feedback)
            
            # 应用正确位置过滤
            if conditions['pattern']:
                pattern = conditions['pattern']
                for i, char in enumerate(pattern):
                    if char != '_':
                        candidates = [w for w in candidates if w[i] == char]
            
            # 应用存在字母过滤
            if conditions['present']:
                for char in conditions['present']:
                    candidates = [w for w in candidates if char in w]
            
            # 应用不存在字母过滤
            if conditions['absent']:
                absent = conditions['absent']
                candidates = [w for w in candidates if not any(c in absent for c in w)]
            
            # 应用黄色位置约束
            for char, positions in conditions['yellow_positions'].items():
                for pos in positions:
                    candidates = [w for w in candidates if w[pos] != char]
        
        if not candidates:
            return ("", [], 0)
        
        best, _ = self.get_best_guess(candidates)
        return (best, candidates[:20], len(candidates))  # 返回前20个候选


class WordleSolver:
    """
    Wordle 自动求解器
    自动玩 Wordle 游戏
    """
    
    def __init__(self, words: Optional[List[str]] = None):
        """
        初始化求解器
        
        Args:
            words: 可选的单词列表
        """
        self.helper = WordleHelper(words)
        self.history: List[Tuple[str, str]] = []
        self.candidates = self.helper.words.copy()
    
    def reset(self) -> None:
        """重置求解器"""
        self.history = []
        self.candidates = self.helper.words.copy()
    
    def get_first_guess(self, method: str = "combined") -> str:
        """获取第一个猜测词"""
        guess, _ = self.helper.get_best_guess(method=method)
        return guess
    
    def submit_feedback(self, guess: str, feedback: str) -> None:
        """
        提交反馈
        
        Args:
            guess: 猜测的词
            feedback: 反馈字符串
        """
        self.history.append((guess, feedback))
        
        # 更新候选词
        conditions = self.helper.analyze_feedback(guess, feedback)
        
        if conditions['pattern']:
            pattern = conditions['pattern']
            for i, char in enumerate(pattern):
                if char != '_':
                    self.candidates = [w for w in self.candidates if w[i] == char]
        
        if conditions['present']:
            for char in conditions['present']:
                self.candidates = [w for w in self.candidates if char in w]
        
        if conditions['absent']:
            absent = conditions['absent']
            self.candidates = [w for w in self.candidates if not any(c in absent for c in w)]
        
        for char, positions in conditions['yellow_positions'].items():
            for pos in positions:
                self.candidates = [w for w in self.candidates if w[pos] != char]
    
    def get_next_guess(self, method: str = "combined") -> str:
        """获取下一个猜测词"""
        if not self.candidates:
            return ""
        if len(self.candidates) == 1:
            return self.candidates[0]
        
        guess, _ = self.helper.get_best_guess(self.candidates, method=method)
        return guess
    
    def auto_solve(
        self, 
        answer: str, 
        max_attempts: int = 6,
        first_guess: Optional[str] = None,
        method: str = "combined",
        verbose: bool = True
    ) -> Tuple[bool, int, List[Tuple[str, str]]]:
        """
        自动求解指定答案
        
        Args:
            answer: 目标答案
            max_attempts: 最大尝试次数
            first_guess: 第一个猜测词（可选）
            method: 计算方法
            verbose: 是否打印过程
        
        Returns:
            (是否成功, 尝试次数, 历史记录) 元组
        """
        self.reset()
        answer = answer.lower()
        
        if answer not in self.helper.words:
            if verbose:
                print(f"警告: '{answer}' 不在词库中")
            return (False, 0, [])
        
        if first_guess:
            guess = first_guess.lower()
        else:
            guess = self.get_first_guess(method)
        
        for attempt in range(1, max_attempts + 1):
            if verbose:
                print(f"第 {attempt} 次猜测: {guess}")
            
            feedback = self.helper._get_pattern(guess, answer)
            feedback_display = feedback.replace('2', '🟩').replace('1', '🟨').replace('0', '⬜')
            
            if verbose:
                print(f"反馈: {feedback_display}")
            
            self.submit_feedback(guess, feedback)
            
            if guess == answer:
                if verbose:
                    print(f"🎉 成功！用了 {attempt} 次猜中！")
                return (True, attempt, self.history)
            
            guess = self.get_next_guess(method)
            if not guess:
                if verbose:
                    print("无法找到候选词")
                return (False, attempt, self.history)
        
        if verbose:
            print(f"失败！用了 {max_attempts} 次未猜中。答案是: {answer}")
        return (False, max_attempts, self.history)


# 便捷函数
def filter_words(
    words: Optional[List[str]] = None,
    **kwargs
) -> List[str]:
    """
    过滤单词的便捷函数
    
    Args:
        words: 单词列表（可选）
        **kwargs: 过滤条件
    
    Returns:
        过滤后的单词列表
    """
    helper = WordleHelper(words)
    return helper.filter_words(**kwargs)


def get_best_guess(
    words: Optional[List[str]] = None,
    method: str = "combined"
) -> Tuple[str, float]:
    """
    获取最优猜测的便捷函数
    
    Args:
        words: 单词列表（可选）
        method: 计算方法
    
    Returns:
        (最优词, 得分) 元组
    """
    helper = WordleHelper(words)
    return helper.get_best_guess(method=method)


def calculate_letter_frequency(words: Optional[List[str]] = None) -> Dict[str, float]:
    """
    计算字母频率的便捷函数
    
    Args:
        words: 单词列表（可选）
    
    Returns:
        字母频率字典
    """
    helper = WordleHelper(words)
    return helper.letter_frequency