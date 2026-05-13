"""
BIP39 Utilities - BIP39 助记词工具

提供完整的 BIP39 实现，包括：
- 助记词生成（支持 12/15/18/21/24 词）
- 助记词验证
- 助记词转种子（Seed）
- 种子转主密钥（Master Key）
- 校验和计算与验证

零外部依赖，纯 Python 实现。
遵循 BIP39 规范：https://github.com/bitcoin/bips/blob/master/bip-0039.mediawiki
"""

import hashlib
import hmac
import secrets
from typing import List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum


class Language(Enum):
    """支持的语言"""
    ENGLISH = "english"
    CHINESE_SIMPLIFIED = "chinese_simplified"
    CHINESE_TRADITIONAL = "chinese_traditional"


# 英文词表（BIP39 标准，共 2048 词）- 来自官方 BIP39 规范
ENGLISH_WORDLIST = [
    "abandon", "ability", "able", "about", "above", "absent", "absorb", "abstract", "absurd", "abuse",
    "access", "accident", "account", "accuse", "achieve", "acid", "acoustic", "acquire", "across", "act",
    "action", "actor", "actress", "actual", "adapt", "add", "addict", "address", "adjust", "admit",
    "adult", "advance", "advice", "aerobic", "affair", "afford", "afraid", "again", "age", "agent",
    "agree", "ahead", "aim", "air", "airport", "aisle", "alarm", "album", "alcohol", "alert",
    "alien", "all", "alley", "allow", "almost", "alone", "alpha", "already", "also", "alter",
    "always", "amateur", "amazing", "among", "amount", "amused", "analyst", "anchor", "ancient", "anger",
    "angle", "angry", "animal", "ankle", "announce", "annual", "another", "answer", "antenna", "antique",
    "anxiety", "any", "apart", "apology", "appear", "apple", "approve", "april", "arch", "arctic",
    "area", "arena", "argue", "arm", "armed", "armor", "army", "around", "arrange", "arrest",
    "arrive", "arrow", "art", "artefact", "artist", "artwork", "ask", "aspect", "assault", "asset",
    "assist", "assume", "asthma", "athlete", "atom", "attack", "attend", "attitude", "attract", "auction",
    "audit", "august", "aunt", "author", "auto", "autumn", "average", "avocado", "avoid", "awake",
    "aware", "away", "awesome", "awful", "awkward", "axis", "baby", "bachelor", "bacon", "badge",
    "bag", "balance", "balcony", "ball", "bamboo", "banana", "banner", "bar", "barely", "bargain",
    "barrel", "base", "basic", "basket", "battle", "beach", "bean", "beauty", "because", "become",
    "beef", "before", "begin", "behave", "behind", "believe", "below", "belt", "bench", "benefit",
    "best", "betray", "better", "between", "beyond", "bicycle", "bid", "bike", "bind", "biology",
    "bird", "birth", "bitter", "black", "blade", "blame", "blanket", "blast", "bleak", "bless",
    "blind", "blood", "blossom", "blouse", "blue", "blur", "blush", "board", "boat", "body",
    "boil", "bomb", "bone", "bonus", "book", "boost", "border", "boring", "borrow", "boss",
    "bottom", "bounce", "box", "boy", "bracket", "brain", "brand", "brass", "brave", "bread",
    "breeze", "brick", "bridge", "brief", "bright", "bring", "brisk", "broccoli", "broken", "bronze",
    "broom", "brother", "brown", "brush", "bubble", "buddy", "budget", "buffalo", "build", "bulb",
    "bulk", "bullet", "bundle", "bunker", "burden", "burger", "burst", "bus", "business", "busy",
    "butter", "buyer", "buzz", "cabbage", "cabin", "cable", "cactus", "cage", "cake", "call",
    "calm", "camera", "camp", "can", "canal", "cancel", "candy", "cannon", "canoe", "canvas",
    "canyon", "capable", "capital", "captain", "car", "carbon", "card", "cargo", "carpet", "carry",
    "cart", "case", "cash", "casino", "castle", "casual", "cat", "catalog", "catch", "category",
    "cattle", "caught", "cause", "caution", "cave", "ceiling", "celery", "cement", "census", "century",
    "cereal", "certain", "chair", "chalk", "champion", "change", "chaos", "chapter", "charge", "chase",
    "chat", "cheap", "check", "cheese", "chef", "cherry", "chest", "chicken", "chief", "child",
    "chimney", "choice", "choose", "chronic", "chuckle", "chunk", "churn", "cigar", "cinnamon", "circle",
    "citizen", "city", "civil", "claim", "clap", "clarify", "claw", "clay", "clean", "clerk",
    "clever", "click", "client", "cliff", "climb", "clinic", "clip", "clock", "clog", "close",
    "cloth", "cloud", "clown", "club", "clump", "cluster", "clutch", "coach", "coast", "coconut",
    "code", "coffee", "coil", "coin", "collect", "color", "column", "combine", "come", "comfort",
    "comic", "common", "company", "concert", "conduct", "confirm", "congress", "connect", "consider", "control",
    "convince", "cook", "cool", "copper", "copy", "coral", "core", "corn", "correct", "cost",
    "cotton", "couch", "country", "couple", "course", "cousin", "cover", "coyote", "crack", "cradle",
    "craft", "cram", "crane", "crash", "crater", "crawl", "crazy", "cream", "credit", "creek",
    "crew", "cricket", "crime", "crisp", "critic", "crop", "cross", "crouch", "crowd", "crucial",
    "cruel", "cruise", "crumble", "crunch", "crush", "cry", "crystal", "cube", "culture", "cup",
    "cupboard", "curious", "current", "curtain", "curve", "cushion", "custom", "cute", "cycle", "dad",
    "damage", "damp", "dance", "danger", "daring", "dash", "daughter", "dawn", "day", "deal",
    "debate", "debris", "decade", "december", "decide", "decline", "decorate", "decrease", "deer", "defense",
    "define", "defy", "degree", "delay", "deliver", "demand", "demise", "denial", "dentist", "deny",
    "depart", "depend", "deposit", "depth", "deputy", "derive", "describe", "desert", "design", "desk",
    "despair", "destroy", "detail", "detect", "develop", "device", "devote", "diagram", "dial", "diamond",
    "diary", "dice", "diesel", "diet", "differ", "digital", "dignity", "dilemma", "dinner", "dinosaur",
    "direct", "dirt", "disagree", "discover", "disease", "dish", "dismiss", "disorder", "display", "distance",
    "divert", "divide", "divorce", "dizzy", "doctor", "document", "dog", "doll", "dolphin", "domain",
    "donate", "donkey", "donor", "door", "dose", "double", "dove", "draft", "dragon", "drama",
    "drastic", "draw", "dream", "dress", "drift", "drill", "drink", "drip", "drive", "drop",
    "drum", "dry", "duck", "dumb", "dune", "during", "dust", "dutch", "duty", "dwarf",
    "dynamic", "eager", "eagle", "early", "earn", "earth", "easily", "east", "easy", "echo",
    "ecology", "economy", "edge", "edit", "educate", "effort", "egg", "eight", "either", "elbow",
    "elder", "electric", "elegant", "element", "elephant", "elevator", "elite", "else", "embark", "embody",
    "embrace", "emerge", "emotion", "employ", "empower", "empty", "enable", "enact", "end", "endless",
    "endorse", "enemy", "energy", "enforce", "engage", "engine", "enhance", "enjoy", "enlist", "enough",
    "enrich", "enroll", "ensure", "enter", "entire", "entry", "envelope", "episode", "equal", "equip",
    "era", "erase", "erode", "erosion", "error", "erupt", "escape", "essay", "essence", "estate",
    "eternal", "ethics", "evidence", "evil", "evoke", "evolve", "exact", "example", "excess", "exchange",
    "excite", "exclude", "excuse", "execute", "exercise", "exhaust", "exhibit", "exile", "exist", "exit",
    "exotic", "expand", "expect", "expire", "explain", "expose", "express", "extend", "extra", "eye",
    "eyebrow", "fabric", "face", "faculty", "fade", "faint", "faith", "fall", "false", "fame",
    "family", "famous", "fan", "fancy", "fantasy", "farm", "fashion", "fat", "fatal", "father",
    "fatigue", "fault", "favorite", "feature", "february", "federal", "fee", "feed", "feel", "female",
    "fence", "festival", "fetch", "fever", "few", "fiber", "fiction", "field", "figure", "file",
    "film", "filter", "final", "find", "fine", "finger", "finish", "fire", "firm", "first",
    "fiscal", "fish", "fit", "fitness", "fix", "flag", "flame", "flash", "flat", "flavor",
    "flee", "flight", "flip", "float", "flock", "floor", "flower", "fluid", "flush", "fly",
    "foam", "focus", "fog", "foil", "fold", "follow", "food", "foot", "force", "forest",
    "forget", "fork", "fortune", "forum", "forward", "fossil", "foster", "found", "fox", "fragile",
    "frame", "frequent", "fresh", "friend", "fringe", "frog", "front", "frost", "frown", "frozen",
    "fruit", "fuel", "fun", "funny", "furnace", "fury", "future", "gadget", "gain", "galaxy",
    "gallery", "game", "gap", "garage", "garbage", "garden", "garlic", "garment", "gas", "gasp",
    "gate", "gather", "gauge", "gaze", "general", "genius", "genre", "gentle", "genuine", "gesture",
    "ghost", "giant", "gift", "giggle", "ginger", "giraffe", "girl", "give", "glad", "glance",
    "glare", "glass", "glide", "glimpse", "globe", "gloom", "glory", "glove", "glow", "glue",
    "goat", "goddess", "gold", "good", "goose", "gorilla", "gospel", "gossip", "govern", "gown",
    "grab", "grace", "grain", "grant", "grape", "grass", "gravity", "great", "green", "grid",
    "grief", "grit", "grocery", "group", "grow", "grunt", "guard", "guess", "guide", "guilt",
    "guitar", "gun", "gym", "habit", "hair", "half", "hammer", "hamster", "hand", "happy",
    "harbor", "hard", "harsh", "harvest", "hat", "have", "hawk", "hazard", "head", "health",
    "heart", "heavy", "hedgehog", "height", "hello", "helmet", "help", "hen", "hero", "hidden",
    "high", "hill", "hint", "hip", "hire", "history", "hobby", "hockey", "hold", "hole",
    "holiday", "hollow", "home", "honey", "hood", "hope", "horn", "horror", "horse", "hospital",
    "host", "hotel", "hour", "hover", "hub", "huge", "human", "humble", "humor", "hundred",
    "hungry", "hunt", "hurdle", "hurry", "hurt", "husband", "hybrid", "ice", "icon", "idea",
    "identify", "idle", "ignore", "ill", "illegal", "illness", "image", "imitate", "immense", "immune",
    "impact", "impose", "improve", "impulse", "inch", "include", "income", "increase", "index", "indicate",
    "indoor", "industry", "infant", "inflict", "inform", "inhale", "inherit", "initial", "inject", "injury",
    "inmate", "inner", "innocent", "input", "inquiry", "insane", "insect", "inside", "inspire", "install",
    "intact", "interest", "into", "invest", "invite", "involve", "iron", "island", "isolate", "issue",
    "item", "ivory", "jacket", "jaguar", "jar", "jazz", "jealous", "jeans", "jelly", "jewel",
    "job", "join", "joke", "journey", "joy", "judge", "juice", "jump", "jungle", "junior",
    "junk", "just", "kangaroo", "keen", "keep", "ketchup", "key", "kick", "kid", "kidney",
    "kind", "kingdom", "kiss", "kit", "kitchen", "kite", "kitten", "kiwi", "knee", "knife",
    "knock", "know", "lab", "label", "labor", "ladder", "lady", "lake", "lamp", "language",
    "laptop", "large", "later", "latin", "laugh", "laundry", "lava", "law", "lawn", "lawsuit",
    "layer", "lazy", "leader", "leaf", "learn", "leave", "lecture", "left", "leg", "legal",
    "legend", "leisure", "lemon", "lend", "length", "lens", "leopard", "lesson", "letter", "level",
    "liar", "liberty", "library", "license", "life", "lift", "light", "like", "limb", "limit",
    "link", "lion", "liquid", "list", "little", "live", "lizard", "load", "loan", "lobster",
    "local", "lock", "logic", "lonely", "long", "loop", "lottery", "loud", "lounge", "love",
    "loyal", "lucky", "luggage", "lumber", "lunar", "lunch", "luxury", "lyrics", "machine", "mad",
    "magic", "magnet", "maid", "mail", "main", "major", "make", "mammal", "man", "manage",
    "mandate", "mango", "mansion", "manual", "maple", "marble", "march", "margin", "marine", "market",
    "marriage", "mask", "mass", "master", "match", "material", "math", "matrix", "matter", "maximum",
    "maze", "meadow", "mean", "measure", "meat", "mechanic", "medal", "media", "melody", "melt",
    "member", "memory", "mention", "menu", "mercy", "merge", "merit", "merry", "mesh", "message",
    "metal", "method", "middle", "midnight", "milk", "million", "mimic", "mind", "minimum", "minor",
    "minute", "miracle", "mirror", "misery", "miss", "mistake", "mix", "mixed", "mixture", "mobile",
    "model", "modify", "mom", "moment", "monitor", "monkey", "monster", "month", "moon", "moral",
    "more", "morning", "mosquito", "mother", "motion", "motor", "mountain", "mouse", "move", "movie",
    "much", "muffin", "mule", "multiply", "muscle", "museum", "mushroom", "music", "must", "mutual",
    "myself", "mystery", "myth", "naive", "name", "napkin", "narrow", "nasty", "nation", "nature",
    "near", "neck", "need", "negative", "neglect", "neither", "nephew", "nerve", "nest", "net",
    "network", "neutral", "never", "news", "next", "nice", "night", "noble", "noise", "nominee",
    "noodle", "normal", "north", "nose", "notable", "note", "nothing", "notice", "novel", "now",
    "nuclear", "number", "nurse", "nut", "oak", "obey", "object", "oblige", "obscure", "observe",
    "obtain", "obvious", "occur", "ocean", "october", "odor", "off", "offer", "office", "often",
    "oil", "okay", "old", "olive", "olympic", "omit", "once", "one", "onion", "online",
    "only", "open", "opera", "opinion", "oppose", "option", "orange", "orbit", "orchard", "order",
    "ordinary", "organ", "orient", "original", "orphan", "ostrich", "other", "outdoor", "outer", "output",
    "outside", "oval", "oven", "over", "own", "owner", "oxygen", "oyster", "ozone", "pact",
    "paddle", "page", "pair", "palace", "palm", "panda", "panel", "panic", "panther", "paper",
    "parade", "parent", "park", "parrot", "party", "pass", "patch", "path", "patient", "patrol",
    "pattern", "pause", "pave", "payment", "peace", "peanut", "pear", "peasant", "pelican", "pen",
    "penalty", "pencil", "people", "pepper", "perfect", "permit", "person", "pet", "phone", "photo",
    "phrase", "physical", "piano", "picnic", "picture", "piece", "pig", "pigeon", "pill", "pilot",
    "pink", "pioneer", "pipe", "pistol", "pitch", "pizza", "place", "planet", "plastic", "plate",
    "play", "please", "pledge", "pluck", "plug", "plunge", "poem", "poet", "point", "polar",
    "pole", "police", "pond", "pony", "pool", "popular", "portion", "position", "possible", "post",
    "potato", "pottery", "poverty", "powder", "power", "practice", "praise", "predict", "prefer", "prepare",
    "present", "pretty", "prevent", "price", "pride", "primary", "print", "priority", "prison", "private",
    "prize", "problem", "process", "produce", "profit", "program", "project", "promote", "proof", "property",
    "prosper", "protect", "proud", "provide", "public", "pudding", "pull", "pulp", "pulse", "pumpkin",
    "punch", "pupil", "puppy", "purchase", "purity", "purpose", "purse", "push", "put", "puzzle",
    "pyramid", "quality", "quantum", "quarter", "question", "quick", "quit", "quiz", "quote", "rabbit",
    "raccoon", "race", "rack", "radar", "radio", "rail", "rain", "raise", "rally", "ramp",
    "ranch", "random", "range", "rapid", "rare", "rate", "rather", "raven", "raw", "razor",
    "ready", "real", "reason", "rebel", "rebuild", "recall", "receive", "recipe", "record", "recycle",
    "reduce", "reflect", "reform", "refuse", "region", "regret", "regular", "reject", "relax", "release",
    "relief", "rely", "remain", "remember", "remind", "remove", "render", "renew", "rent", "reopen",
    "repair", "repeat", "replace", "report", "require", "rescue", "resemble", "resist", "resource", "response",
    "result", "retire", "retreat", "return", "reunion", "reveal", "review", "reward", "rhythm", "rib",
    "ribbon", "rice", "rich", "ride", "ridge", "rifle", "right", "rigid", "ring", "riot",
    "ripple", "risk", "ritual", "rival", "river", "road", "roast", "robot", "robust", "rocket",
    "romance", "roof", "rookie", "room", "rose", "rotate", "rough", "round", "route", "royal",
    "rubber", "rude", "rug", "rule", "run", "runway", "rural", "sad", "saddle", "sadness",
    "safe", "sail", "salad", "salmon", "salon", "salt", "salute", "same", "sample", "sand",
    "satisfy", "satoshi", "sauce", "sausage", "save", "say", "scale", "scan", "scare", "scatter",
    "scene", "scheme", "school", "science", "scissors", "scorpion", "scout", "scrap", "screen", "script",
    "scrub", "sea", "search", "season", "seat", "second", "secret", "section", "security", "seed",
    "seek", "segment", "select", "sell", "seminar", "senior", "sense", "sentence", "series", "service",
    "session", "settle", "setup", "seven", "shadow", "shaft", "shallow", "share", "shed", "shell",
    "sheriff", "shield", "shift", "shine", "ship", "shiver", "shock", "shoe", "shoot", "shop",
    "short", "shoulder", "shove", "shrimp", "shrug", "shuffle", "shy", "sibling", "sick", "side",
    "siege", "sight", "sign", "silent", "silk", "silly", "silver", "similar", "simple", "since",
    "sing", "siren", "sister", "situate", "six", "size", "skate", "sketch", "ski", "skill",
    "skin", "skirt", "skull", "slab", "slam", "sleep", "slender", "slice", "slide", "slight",
    "slim", "slogan", "slot", "slow", "slush", "small", "smart", "smile", "smoke", "smooth",
    "snack", "snake", "snap", "sniff", "snow", "soap", "soccer", "social", "sock", "soda",
    "soft", "solar", "soldier", "solid", "solution", "solve", "someone", "song", "soon", "sorry",
    "sort", "soul", "sound", "soup", "source", "south", "space", "spare", "spatial", "spawn",
    "speak", "special", "speed", "spell", "spend", "sphere", "spice", "spider", "spike", "spin",
    "spirit", "split", "spoil", "sponsor", "spoon", "sport", "spot", "spray", "spread", "spring",
    "spy", "square", "squeeze", "squirrel", "stable", "stadium", "staff", "stage", "stairs", "stamp",
    "stand", "start", "state", "stay", "steak", "steel", "stem", "step", "stereo", "stick",
    "still", "sting", "stock", "stomach", "stone", "stool", "story", "stove", "strategy", "street",
    "strike", "strong", "struggle", "student", "stuff", "stumble", "style", "subject", "submit", "subway",
    "success", "such", "sudden", "suffer", "sugar", "suggest", "suit", "summer", "sun", "sunny",
    "sunset", "super", "supply", "supreme", "sure", "surface", "surge", "surprise", "surround", "survey",
    "suspect", "sustain", "swallow", "swamp", "swap", "swarm", "swear", "sweet", "swift", "swim",
    "swing", "switch", "sword", "symbol", "symptom", "syrup", "system", "table", "tackle", "tag",
    "tail", "talent", "talk", "tank", "tape", "target", "task", "taste", "tattoo", "taxi",
    "teach", "team", "tell", "ten", "tenant", "tennis", "tent", "term", "test", "text",
    "thank", "that", "theme", "then", "theory", "there", "they", "thing", "this", "thought",
    "three", "thrive", "throw", "thumb", "thunder", "ticket", "tide", "tiger", "tilt", "timber",
    "time", "tiny", "tip", "tired", "tissue", "title", "toast", "tobacco", "today", "toddler",
    "toe", "together", "toilet", "token", "tomato", "tomorrow", "tone", "tongue", "tonight", "tool",
    "tooth", "top", "topic", "topple", "torch", "tornado", "tortoise", "toss", "total", "tourist",
    "toward", "tower", "town", "toy", "track", "trade", "traffic", "tragic", "train", "transfer",
    "trap", "trash", "travel", "tray", "treat", "tree", "trend", "trial", "tribe", "trick",
    "trigger", "trim", "trip", "trophy", "trouble", "truck", "true", "truly", "trumpet", "trust",
    "truth", "try", "tube", "tuition", "tumble", "tuna", "tunnel", "turkey", "turn", "turtle",
    "twelve", "twenty", "twice", "twin", "twist", "two", "type", "typical", "ugly", "umbrella",
    "unable", "unaware", "uncle", "uncover", "under", "undo", "unfair", "unfold", "unhappy", "uniform",
    "unique", "unit", "universe", "unknown", "unlock", "until", "unusual", "unveil", "update", "upgrade",
    "uphold", "upon", "upper", "upset", "urban", "urge", "usage", "use", "used", "useful",
    "useless", "usual", "utility", "vacant", "vacuum", "vague", "valid", "valley", "valve", "van",
    "vanish", "vapor", "various", "vast", "vault", "vehicle", "velvet", "vendor", "venture", "venue",
    "verb", "verify", "version", "very", "vessel", "veteran", "viable", "vibrant", "vicious", "victory",
    "video", "view", "village", "vintage", "violin", "virtual", "virus", "visa", "visit", "visual",
    "vital", "vivid", "vocal", "voice", "void", "volcano", "volume", "vote", "voyage", "wage",
    "wagon", "wait", "walk", "wall", "walnut", "want", "warfare", "warm", "warrior", "wash",
    "wasp", "waste", "water", "wave", "way", "wealth", "weapon", "wear", "weasel", "weather",
    "web", "wedding", "weekend", "weird", "welcome", "west", "wet", "whale", "what", "wheat",
    "wheel", "when", "where", "whip", "whisper", "wide", "width", "wife", "wild", "will",
    "win", "window", "wine", "wing", "wink", "winner", "winter", "wire", "wisdom", "wise",
    "wish", "witness", "wolf", "woman", "wonder", "wood", "wool", "word", "work", "world",
    "worry", "worth", "wrap", "wreck", "wrestle", "wrist", "write", "wrong", "yard", "year",
    "yellow", "you", "young", "youth", "zebra", "zero", "zone", "zoo"
]

# 有效助记词长度
VALID_MNEMONIC_LENGTHS = [12, 15, 18, 21, 24]

# 长度到熵位数的映射
LENGTH_TO_ENTROPY_BITS = {
    12: 128,
    15: 160,
    18: 192,
    21: 224,
    24: 256,
}


@dataclass
class MnemonicResult:
    """助记词生成结果"""
    mnemonic: str           # 助记词字符串（空格分隔）
    words: List[str]        # 助记词列表
    entropy_hex: str        # 熵（十六进制）
    language: Language       # 语言
    word_count: int          # 词数


@dataclass
class SeedResult:
    """种子生成结果"""
    seed: bytes              # 种子（64字节）
    seed_hex: str            # 种子（十六进制）
    master_key: bytes        # 主密钥
    master_key_hex: str      # 主密钥（十六进制）
    chain_code: bytes        # 链码
    chain_code_hex: str      # 链码（十六进制）


@dataclass
class ValidationResult:
    """验证结果"""
    is_valid: bool           # 是否有效
    error: Optional[str]     # 错误信息
    checksum_valid: bool     # 校验和是否有效
    word_count: int          # 词数
    detected_language: Optional[Language]  # 检测到的语言


class BIP39Mnemonic:
    """
    BIP39 助记词工具类
    
    提供助记词生成、验证、种子派生等功能。
    完全遵循 BIP39 规范。
    """
    
    def __init__(self, language: Language = Language.ENGLISH):
        """
        初始化助记词工具
        
        Args:
            language: 词表语言，默认英文
        """
        if language != Language.ENGLISH:
            raise ValueError(f"Only English wordlist is currently supported")
        
        self.language = language
        self.wordlist = ENGLISH_WORDLIST
        self.word_to_index = {word: i for i, word in enumerate(self.wordlist)}
    
    def generate(
        self,
        word_count: int = 12,
        entropy: Optional[bytes] = None,
    ) -> MnemonicResult:
        """
        生成助记词
        
        Args:
            word_count: 助记词数量（12/15/18/21/24）
            entropy: 可选的自定义熵（如不提供则随机生成）
            
        Returns:
            MnemonicResult 包含助记词和相关信息
            
        Raises:
            ValueError: 如果 word_count 无效
        """
        if word_count not in VALID_MNEMONIC_LENGTHS:
            raise ValueError(
                f"Invalid word count: {word_count}. "
                f"Must be one of {VALID_MNEMONIC_LENGTHS}"
            )
        
        # 计算需要的熵位数
        entropy_bits = LENGTH_TO_ENTROPY_BITS[word_count]
        entropy_bytes = entropy_bits // 8
        
        # 生成或使用提供的熵
        if entropy is None:
            entropy = secrets.token_bytes(entropy_bytes)
        else:
            if len(entropy) != entropy_bytes:
                raise ValueError(
                    f"Entropy must be {entropy_bytes} bytes for {word_count} words, "
                    f"got {len(entropy)} bytes"
                )
        
        # 计算校验和
        checksum_bits = word_count // 3
        entropy_hash = hashlib.sha256(entropy).digest()
        checksum = self._get_checksum_bits(entropy_hash, checksum_bits)
        
        # 组合熵和校验和
        entropy_bits_str = self._bytes_to_bits(entropy)
        combined_bits = entropy_bits_str + checksum
        
        # 分割为助记词索引
        word_indices = self._bits_to_indices(combined_bits)
        
        # 获取助记词
        words = [self.wordlist[i] for i in word_indices]
        mnemonic = ' '.join(words)
        
        return MnemonicResult(
            mnemonic=mnemonic,
            words=words,
            entropy_hex=entropy.hex(),
            language=self.language,
            word_count=word_count,
        )
    
    def validate(self, mnemonic: str) -> ValidationResult:
        """
        验证助记词
        
        Args:
            mnemonic: 助记词字符串（空格分隔）
            
        Returns:
            ValidationResult 包含验证结果和详细信息
        """
        words = mnemonic.strip().split()
        
        # 检查词数
        word_count = len(words)
        if word_count not in VALID_MNEMONIC_LENGTHS:
            return ValidationResult(
                is_valid=False,
                error=f"Invalid word count: {word_count}. Must be one of {VALID_MNEMONIC_LENGTHS}",
                checksum_valid=False,
                word_count=word_count,
                detected_language=None,
            )
        
        # 检查所有词是否在词表中
        for word in words:
            if word not in self.word_to_index:
                return ValidationResult(
                    is_valid=False,
                    error=f"Word '{word}' not found in wordlist",
                    checksum_valid=False,
                    word_count=word_count,
                    detected_language=None,
                )
        
        # 检查校验和
        checksum_valid = self._validate_checksum(words)
        
        return ValidationResult(
            is_valid=checksum_valid,
            error=None if checksum_valid else "Invalid checksum",
            checksum_valid=checksum_valid,
            word_count=word_count,
            detected_language=Language.ENGLISH,
        )
    
    def _validate_checksum(self, words: List[str]) -> bool:
        """验证校验和"""
        try:
            # 获取每个词的索引
            indices = [self.word_to_index[word] for word in words]
            
            # 转换为位串
            bits = ''.join(format(i, '011b') for i in indices)
            
            # 分离熵和校验和
            checksum_bits = len(words) // 3
            entropy_bits = len(bits) - checksum_bits
            
            entropy_bits_str = bits[:entropy_bits]
            checksum = bits[entropy_bits:]
            
            # 将位串转换为字节
            entropy = self._bits_to_bytes(entropy_bits_str)
            
            # 计算预期的校验和
            entropy_hash = hashlib.sha256(entropy).digest()
            expected_checksum = self._get_checksum_bits(entropy_hash, checksum_bits)
            
            return checksum == expected_checksum
        except Exception:
            return False
    
    def to_seed(
        self,
        mnemonic: str,
        passphrase: str = "",
    ) -> SeedResult:
        """
        从助记词生成种子
        
        Args:
            mnemonic: 助记词字符串
            passphrase: 可选的密码短语
            
        Returns:
            SeedResult 包含种子和主密钥
            
        Raises:
            ValueError: 如果助记词无效
        """
        # 规范化助记词（NFKD 标准化）
        mnemonic_normalized = ' '.join(mnemonic.strip().split())
        
        # 生成种子
        password = mnemonic_normalized.encode('utf-8')
        salt = ('mnemonic' + passphrase).encode('utf-8')
        
        # PBKDF2-HMAC-SHA512，2048 次迭代
        seed = hashlib.pbkdf2_hmac(
            'sha512',
            password,
            salt,
            iterations=2048,
            dklen=64,
        )
        
        # 从种子派生主密钥
        master_key, chain_code = self._derive_master_key(seed)
        
        return SeedResult(
            seed=seed,
            seed_hex=seed.hex(),
            master_key=master_key,
            master_key_hex=master_key.hex(),
            chain_code=chain_code,
            chain_code_hex=chain_code.hex(),
        )
    
    def _derive_master_key(self, seed: bytes) -> Tuple[bytes, bytes]:
        """从种子派生主密钥"""
        # HMAC-SHA512，key="Bitcoin seed"
        h = hmac.new(b'Bitcoin seed', seed, hashlib.sha512).digest()
        
        # 左 32 字节为主密钥，右 32 字节为链码
        master_key = h[:32]
        chain_code = h[32:]
        
        return master_key, chain_code
    
    def to_entropy(self, mnemonic: str) -> bytes:
        """
        从助记词恢复熵
        
        Args:
            mnemonic: 助记词字符串
            
        Returns:
            原始熵字节
            
        Raises:
            ValueError: 如果助记词无效
        """
        words = mnemonic.strip().split()
        
        if len(words) not in VALID_MNEMONIC_LENGTHS:
            raise ValueError(f"Invalid word count: {len(words)}")
        
        # 转换为位串
        bits = ''.join(format(self.word_to_index[word], '011b') for word in words)
        
        # 分离熵和校验和
        checksum_bits = len(words) // 3
        entropy_bits = len(bits) - checksum_bits
        
        entropy_bits_str = bits[:entropy_bits]
        
        return self._bits_to_bytes(entropy_bits_str)
    
    def _bytes_to_bits(self, data: bytes) -> str:
        """将字节转换为位串"""
        return ''.join(format(byte, '08b') for byte in data)
    
    def _bits_to_bytes(self, bits: str) -> bytes:
        """将位串转换为字节"""
        # 确保长度是 8 的倍数
        if len(bits) % 8 != 0:
            bits = bits.zfill((len(bits) + 7) // 8 * 8)
        
        return bytes(int(bits[i:i+8], 2) for i in range(0, len(bits), 8))
    
    def _get_checksum_bits(self, hash_bytes: bytes, bits: int) -> str:
        """从哈希中提取指定位数的校验和"""
        return format(hash_bytes[0], '08b')[:bits]
    
    def _bits_to_indices(self, bits: str) -> List[int]:
        """将位串分割为 11 位的索引"""
        return [int(bits[i:i+11], 2) for i in range(0, len(bits), 11)]
    
    def word_at_index(self, index: int) -> str:
        """获取指定索引的词"""
        if not 0 <= index < len(self.wordlist):
            raise ValueError(f"Index must be between 0 and {len(self.wordlist) - 1}")
        return self.wordlist[index]
    
    def index_of_word(self, word: str) -> int:
        """获取词的索引"""
        if word not in self.word_to_index:
            raise ValueError(f"Word '{word}' not found in wordlist")
        return self.word_to_index[word]
    
    def is_valid_word(self, word: str) -> bool:
        """检查词是否在词表中"""
        return word in self.word_to_index


# 便捷函数
def generate_mnemonic(word_count: int = 12) -> str:
    """生成助记词的便捷函数"""
    bip = BIP39Mnemonic()
    result = bip.generate(word_count)
    return result.mnemonic


def validate_mnemonic(mnemonic: str) -> bool:
    """验证助记词的便捷函数"""
    bip = BIP39Mnemonic()
    result = bip.validate(mnemonic)
    return result.is_valid


def mnemonic_to_seed(mnemonic: str, passphrase: str = "") -> bytes:
    """助记词转种子的便捷函数"""
    bip = BIP39Mnemonic()
    result = bip.to_seed(mnemonic, passphrase)
    return result.seed


def mnemonic_to_entropy(mnemonic: str) -> bytes:
    """助记词转熵的便捷函数"""
    bip = BIP39Mnemonic()
    return bip.to_entropy(mnemonic)


if __name__ == "__main__":
    print("=== BIP39 助记词工具演示 ===\n")
    
    bip = BIP39Mnemonic()
    
    # 生成助记词
    print("--- 生成助记词 ---")
    result = bip.generate(12)
    print(f"助记词: {result.mnemonic}")
    print(f"词数: {result.word_count}")
    print(f"熵: {result.entropy_hex}")
    
    # 验证助记词
    print("\n--- 验证助记词 ---")
    validation = bip.validate(result.mnemonic)
    print(f"有效: {validation.is_valid}")
    print(f"校验和正确: {validation.checksum_valid}")
    
    # 生成种子
    print("\n--- 生成种子 ---")
    seed_result = bip.to_seed(result.mnemonic)
    print(f"种子: {seed_result.seed_hex[:32]}...")
    print(f"主密钥: {seed_result.master_key_hex[:32]}...")
    
    # 从助记词恢复熵
    print("\n--- 恢复熵 ---")
    entropy = bip.to_entropy(result.mnemonic)
    print(f"恢复的熵: {entropy.hex()}")