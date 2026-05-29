"""
Passphrase Utilities - Secure Password and Passphrase Generator

A comprehensive toolkit for generating secure passwords and memorable passphrases.
Zero external dependencies - uses only Python standard library.

Features:
- Generate random passwords with configurable complexity
- Generate memorable passphrases (e.g., "correct-horse-battery-staple")
- Calculate password strength and entropy
- Support multiple word lists and languages
- Pronounceable password generation
- PIN and token generation

Security considerations:
- Uses secrets module for cryptographically secure random generation
- Configurable entropy requirements
- Avoids ambiguous characters by default
- Supports various character sets and word lists
"""

import secrets
import math
import re
from typing import Optional, List, Dict, Tuple, Set
from dataclasses import dataclass
from enum import Enum


class PasswordStyle(Enum):
    """Password generation styles."""
    RANDOM = "random"  # Random characters
    PASSPHRASE = "passphrase"  # Word-based passphrase
    PRONOUNCEABLE = "pronounceable"  # Pronounceable syllables
    PIN = "pin"  # Numeric PIN
    TOKEN = "token"  # URL-safe token


@dataclass
class PasswordStrength:
    """Password strength analysis result."""
    score: int  # 0-100
    entropy: float  # Bits of entropy
    crack_time: str  # Estimated time to crack
    rating: str  # "weak", "fair", "good", "strong", "excellent"
    issues: List[str]  # Potential issues
    suggestions: List[str]  # Improvement suggestions


# Default character sets
LOWERCASE = "abcdefghijklmnopqrstuvwxyz"
UPPERCASE = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
DIGITS = "0123456789"
SYMBOLS = "!@#$%^&*()_+-=[]{}|;:,.<>?"
AMBIGUOUS = "0O1lI"  # Characters often confused

# Default word list (EffDiceRoll style - 7776 words for Diceware)
# Using a curated list of common, memorable words
DEFAULT_WORD_LIST = [
    "abandon", "ability", "able", "about", "above", "absent", "absorb", "abstract",
    "absurd", "abuse", "access", "accident", "account", "accuse", "achieve", "acid",
    "acoustic", "acquire", "across", "act", "action", "actor", "actress", "actual",
    "adapt", "add", "addict", "address", "adjust", "admit", "adult", "advance",
    "advice", "aerobic", "affair", "afford", "afraid", "again", "age", "agent",
    "agree", "ahead", "aim", "air", "airport", "aisle", "alarm", "album",
    "alcohol", "alert", "alien", "all", "alley", "allow", "almost", "alone",
    "alpha", "already", "also", "alter", "always", "amateur", "amazing", "among",
    "amount", "amused", "anchor", "analysis", "angel", "anger", "angle", "angry",
    "ankle", "announce", "annual", "another", "answer", "antenna", "antique", "anxiety",
    "any", "apart", "apology", "appear", "apple", "approve", "april", "arch",
    "arctic", "area", "arena", "argue", "arm", "armed", "armor", "army",
    "around", "arrange", "arrest", "arrive", "arrow", "art", "artefact", "artist",
    "artwork", "ask", "aspect", "assault", "asset", "assist", "assume", "asthma",
    "athlete", "atom", "attack", "attend", "attitude", "attract", "auction", "audit",
    "august", "aunt", "author", "auto", "autumn", "average", "avocado", "avoid",
    "awake", "aware", "away", "awesome", "awful", "awkward", "axis", "baby",
    "bachelor", "bacon", "badge", "bag", "balance", "balcony", "ball", "bamboo",
    "banana", "banner", "bar", "barely", "bargain", "barrel", "base", "basic",
    "basket", "battle", "beach", "bean", "beauty", "become", "beef", "before",
    "begin", "behave", "behind", "believe", "below", "belt", "bench", "benefit",
    "best", "betray", "better", "between", "beyond", "bicycle", "bid", "bike",
    "bind", "biology", "bird", "birth", "bitter", "black", "blade", "blame",
    "blanket", "blast", "bleak", "bless", "blind", "blood", "blossom", "blouse",
    "blue", "blur", "blush", "board", "boat", "body", "boil", "bomb",
    "bone", "bonus", "book", "boost", "border", "boring", "borrow", "boss",
    "bottom", "bounce", "box", "boy", "bracket", "brain", "brand", "brass",
    "brave", "bread", "breeze", "brick", "bridge", "brief", "bright", "bring",
    "brisk", "broken", "bronze", "broom", "brother", "brown", "brush", "bubble",
    "buddy", "budget", "buffalo", "build", "bulb", "bulk", "bullet", "bundle",
    "bunker", "burden", "burger", "burst", "bus", "business", "busy", "butter",
    "buyer", "buzz", "cabbage", "cabin", "cable", "cactus", "cage", "cake",
    "call", "calm", "camera", "camp", "can", "canal", "cancel", "candy",
    "cannon", "canoe", "canvas", "canyon", "capable", "capital", "captain", "car",
    "carbon", "card", "cargo", "carpet", "carry", "cart", "case", "cash",
    "casino", "castle", "casual", "cat", "catalog", "catch", "category", "cattle",
    "caught", "cause", "caution", "cave", "ceiling", "cement", "census", "center",
    "century", "cereal", "certain", "chair", "chalk", "champion", "change", "chaos",
    "chapter", "charge", "chase", "chat", "cheap", "check", "cheese", "chef",
    "cherry", "chest", "chicken", "chief", "child", "chimney", "choice", "choose",
    "chronic", "chuckle", "chunk", "churn", "cigar", "cinnamon", "circle", "citizen",
    "city", "civil", "claim", "clap", "clarify", "claw", "clay", "clean",
    "clerk", "clever", "click", "client", "cliff", "climb", "clinic", "clip",
    "clock", "clog", "close", "cloth", "cloud", "clover", "club", "clump",
    "cluster", "clutch", "coach", "coast", "coconut", "code", "coffee", "coil",
    "coin", "collect", "color", "column", "combine", "come", "comfort", "comic",
    "common", "company", "concert", "conduct", "confirm", "congress", "connect", "consider",
    "consume", "contact", "contain", "content", "context", "control", "cook", "cool",
    "copper", "copy", "coral", "core", "corn", "correct", "cost", "cotton",
    "couch", "country", "couple", "course", "cousin", "cover", "coyote", "crack",
    "cradle", "craft", "crane", "crash", "craw", "crazy", "cream", "credit",
    "cricket", "creek", "crew", "cricket", "crime", "crisp", "critic", "crop",
    "cross", "crowd", "crown", "crucial", "cruel", "cruise", "crush", "cry",
    "crystal", "cube", "culture", "cup", "cupboard", "curious", "current", "curtain",
    "curve", "cushion", "custom", "cute", "cycle", "dad", "damage", "damp",
    "dance", "danger", "dare", "darkness", "daughter", "dawn", "day", "deal",
    "debate", "debris", "decade", "december", "decide", "decline", "decorate", "decrease",
    "deer", "defense", "define", "defy", "degree", "delay", "deliver", "demand",
    "demise", "denial", "dentist", "deny", "depart", "depend", "deposit", "depth",
    "deputy", "derive", "describe", "desert", "design", "desk", "despair", "destroy",
    "detect", "develop", "device", "devote", "diagram", "dial", "diamond", "diary",
    "dice", "diesel", "diet", "differ", "digital", "dignity", "dilemma", "dinner",
    "dinosaur", "direct", "dirt", "disagree", "discover", "disease", "dish", "dismiss",
    "disorder", "display", "distance", "divert", "divide", "divorce", "dizzy", "doctor",
    "document", "dog", "doll", "dolphin", "domain", "donate", "donkey", "donor",
    "door", "dose", "double", "dove", "draft", "dragon", "drama", "drastic",
    "draw", "dream", "dress", "drift", "drill", "drink", "drip", "drive",
    "drop", "drum", "dry", "duck", "dumb", "dune", "during", "dust",
    "dutch", "dwarf", "dynamics", "eager", "eagle", "early", "earn", "earth",
    "easily", "east", "easy", "echo", "ecology", "economy", "edge", "edit",
    "educate", "effort", "egg", "eight", "either", "elbow", "elder", "electric",
    "elegant", "element", "elephant", "elevator", "elite", "else", "embark", "embody",
    "embrace", "emerge", "emotion", "employ", "empower", "empty", "enable", "enact",
    "end", "endless", "endorse", "enemy", "energy", "enforce", "engage", "engine",
    "enhance", "enjoy", "enlist", "enough", "enrich", "enroll", "ensure", "enter",
    "entire", "entrance", "envelope", "episode", "equal", "equip", "era", "erase",
    "erode", "erosion", "error", "erupt", "escape", "essay", "essence", "estate",
    "eternal", "ethics", "evidence", "evil", "evoke", "evolve", "exact", "example",
    "excess", "exchange", "excite", "exclude", "excuse", "execute", "exercise", "exhaust",
    "exhibit", "exile", "exist", "exit", "exotic", "expand", "expect", "expire",
    "explain", "expose", "express", "extend", "extra", "eye", "eyebrow", "fabric",
    "face", "faculty", "fade", "faint", "faith", "fall", "false", "fame",
    "family", "famous", "fan", "fancy", "fantasy", "farm", "fashion", "fat",
    "fatal", "father", "fatigue", "fault", "favorite", "feature", "february", "federal",
    "fee", "feed", "feel", "female", "fence", "festival", "fever", "few",
    "fiber", "fiction", "field", "figure", "file", "film", "filter", "final",
    "find", "fine", "finger", "finish", "fire", "firm", "first", "fiscal",
    "fish", "fit", "fitness", "fix", "flag", "flame", "flash", "flat",
    "flavor", "flee", "flesh", "flight", "flip", "float", "flock", "flood",
    "floor", "flower", "fluid", "flush", "fly", "foam", "focus", "fog",
    "foil", "fold", "follow", "food", "foot", "force", "forest", "forget",
    "fork", "form", "formal", "format", "fortune", "forum", "forward", "fossil",
    "foster", "found", "fox", "fragile", "frame", "frequent", "fresh", "friend",
    "fringe", "frog", "front", "frost", "frown", "frozen", "fruit", "fuel",
    "fun", "functional", "funny", "fur", "furniture", "fury", "future", "gadget",
    "gain", "galaxy", "gallery", "game", "gap", "garage", "garbage", "garden",
    "garlic", "garment", "gas", "gasp", "gate", "gather", "gauge", "gaze",
    "general", "genius", "genre", "gentle", "genuine", "gesture", "ghost", "giant",
    "gift", "giggle", "ginger", "giraffe", "girl", "give", "glad", "glance",
    "glare", "glass", "glide", "glimpse", "globe", "gloom", "glory", "glove",
    "glow", "glue", "goat", "goddess", "gold", "good", "goose", "gorilla",
    "gospel", "gossip", "govern", "gown", "grab", "grace", "grain", "grant",
    "grape", "graph", "grasp", "grass", "gravity", "great", "green", "grid",
    "grief", "grit", "grocery", "group", "grow", "grunt", "guard", "guess",
    "guide", "guilt", "guitar", "gun", "gym", "habit", "hair", "half",
    "hammer", "hamster", "hand", "happy", "harbor", "hard", "harsh", "harvest",
    "hat", "have", "hawk", "hazard", "head", "health", "heart", "heavy",
    "hedgehog", "height", "hello", "helmet", "help", "hen", "hero", "hidden",
    "high", "hill", "hint", "hip", "hire", "history", "hobby", "hockey",
    "hold", "hole", "holiday", "hollow", "home", "honey", "hood", "hope",
    "horn", "horror", "horse", "hospital", "host", "hotel", "hour", "hover",
    "hub", "huge", "human", "humble", "humor", "hundred", "hungry", "hunt",
    "hurdle", "hurry", "hurt", "husband", "hybrid", "ice", "icon", "idea",
    "identify", "idle", "ignore", "ill", "illegal", "illness", "image", "imitate",
    "immense", "immune", "impact", "impose", "improve", "impulse", "inch", "include",
    "income", "increase", "index", "indicate", "indoor", "industry", "infant", "inflict",
    "inform", "inhale", "inherit", "initial", "inject", "injury", "inmate", "inner",
    "innocent", "input", "inquiry", "insane", "insect", "inside", "inspire", "install",
    "intact", "interest", "into", "invest", "invite", "involve", "iron", "island",
    "isolate", "issue", "item", "ivory", "jacket", "jaguar", "jar", "jazz",
    "jealous", "jeans", "jelly", "jerk", "jewel", "job", "join", "joke",
    "journey", "joy", "judge", "juice", "jump", "jungle", "junior", "junk",
    "just", "kangaroo", "keen", "keep", "ketchup", "key", "kick", "kid",
    "kidney", "kind", "kingdom", "kiss", "kit", "kitchen", "kite", "kitten",
    "kiwi", "knee", "knife", "knock", "know", "lab", "label", "labor",
    "ladder", "lady", "lake", "lamp", "language", "laptop", "large", "later",
    "latin", "laugh", "laundry", "lava", "law", "lawn", "lawsuit", "layer",
    "lazy", "leader", "leaf", "learn", "leave", "lecture", "left", "leg",
    "legal", "legend", "leisure", "lemon", "lend", "length", "lens", "leopard",
    "lesson", "letter", "level", "liar", "liberty", "library", "license", "life",
    "lift", "light", "like", "limb", "limit", "link", "lion", "liquid",
    "list", "little", "live", "lizard", "load", "loan", "lobster", "local",
    "lock", "logic", "lonely", "long", "loop", "lottery", "loud", "lounge",
    "love", "loyal", "lucky", "luggage", "lumber", "lunar", "lunch", "luxury",
    "lyrics", "machine", "mad", "magic", "magnet", "maid", "mail", "main",
    "major", "make", "mammal", "man", "manage", "mandate", "mango", "mansion",
    "manual", "maple", "marble", "march", "margin", "marine", "market", "marriage",
    "mask", "mass", "master", "match", "material", "math", "matrix", "matter",
    "maximum", "maze", "meadow", "mean", "measure", "meat", "mechanic", "medal",
    "media", "melody", "melt", "member", "memory", "mention", "menu", "mercy",
    "merge", "merit", "merry", "mesh", "message", "metal", "method", "middle",
    "midnight", "milk", "million", "mimic", "mind", "minimum", "minor", "minute",
    "miracle", "mirror", "misery", "miss", "mistake", "mix", "mixed", "mixture",
    "mobile", "model", "modify", "mom", "moment", "monitor", "monkey", "monster",
    "month", "moon", "moral", "more", "morning", "mosquito", "mother", "motion",
    "motor", "mountain", "mouse", "move", "movie", "much", "muffin", "mule",
    "muscle", "museum", "mushroom", "music", "must", "mutual", "myself", "mystery",
    "myth", "naive", "name", "napkin", "narrow", "nasty", "nation", "nature",
    "near", "neck", "need", "negative", "neglect", "neither", "nephew", "nerve",
    "nest", "net", "network", "neutral", "never", "news", "next", "nice",
    "night", "noble", "noise", "nominee", "noodle", "normal", "north", "nose",
    "notable", "note", "nothing", "notice", "novel", "now", "nuclear", "number",
    "nurse", "nut", "oak", "obey", "object", "oblige", "obscure", "observe",
    "obtain", "obvious", "occur", "ocean", "october", "odor", "off", "offer",
    "often", "oil", "okay", "old", "olive", "olympic", "omit", "once",
    "one", "onion", "online", "only", "open", "opera", "opinion", "oppose",
    "option", "orange", "orbit", "orchard", "order", "ordinary", "organ", "orient",
    "original", "orphan", "ostrich", "other", "outdoor", "outer", "output", "outside",
    "oval", "oven", "over", "own", "owner", "oxygen", "oyster", "ozone",
    "pact", "paddle", "page", "pair", "palace", "palm", "panda", "panel",
    "panic", "panther", "paper", "parade", "parent", "park", "parrot", "party",
    "pass", "patch", "path", "patient", "patrol", "pattern", "pause", "pave",
    "payment", "peace", "peanut", "pear", "peasant", "pelican", "pen", "penalty",
    "pencil", "people", "pepper", "perfect", "permit", "person", "pet", "phone",
    "photo", "phrase", "physical", "piano", "picnic", "picture", "piece", "pig",
    "pigeon", "pill", "pilot", "pink", "pioneer", "pipe", "pistol", "pitch",
    "pizza", "place", "planet", "plastic", "plate", "play", "please", "pledge",
    "pluck", "plug", "plunge", "poem", "poet", "point", "polar", "pole",
    "police", "pond", "pony", "pool", "popular", "portion", "position", "possible",
    "post", "potato", "pottery", "poverty", "powder", "power", "practice", "praise",
    "predict", "prefer", "prepare", "present", "pretty", "prevent", "price", "pride",
    "primary", "print", "priority", "prison", "private", "prize", "problem", "process",
    "produce", "profit", "program", "project", "promote", "proof", "property", "prosper",
    "protect", "proud", "provide", "public", "pudding", "pull", "pulp", "pulse",
    "pumpkin", "punch", "pupil", "puppy", "purchase", "purity", "purpose", "purse",
    "push", "put", "puzzle", "pyramid", "quality", "quantum", "quarter", "question",
    "quick", "quit", "quiz", "quote", "rabbit", "raccoon", "race", "rack",
    "radar", "radio", "rail", "rain", "rally", "ramp", "ranch", "random",
    "range", "rapid", "rare", "rate", "rather", "raven", "raw", "razor",
    "ready", "real", "reason", "rebel", "rebuild", "recall", "receive", "recipe",
    "record", "recycle", "reduce", "reflect", "reform", "refuse", "region", "regret",
    "regular", "reject", "relax", "release", "relief", "rely", "remain", "remember",
    "remind", "remove", "render", "renew", "rent", "reopen", "repair", "repeat",
    "replace", "report", "require", "rescue", "resemble", "resist", "resource", "response",
    "result", "retire", "retreat", "return", "reunion", "reveal", "review", "reward",
    "rhythm", "rib", "ribbon", "rice", "rich", "ride", "ridge", "rifle",
    "right", "rigid", "ring", "riot", "ripple", "risk", "ritual", "rival",
    "river", "road", "roast", "robot", "robust", "rocket", "romance", "roof",
    "rookie", "room", "rose", "rotate", "rough", "round", "route", "royal",
    "rubber", "rude", "rug", "rule", "run", "runway", "rural", "sad",
    "saddle", "sadness", "safe", "sail", "salad", "salmon", "salon", "salt",
    "salute", "same", "sample", "sand", "satisfy", "satoshi", "sauce", "sausage",
    "save", "say", "scale", "scan", "scare", "scatter", "scene", "scheme",
    "school", "science", "scissors", "scorpion", "scout", "scrap", "screen", "script",
    "scrub", "sea", "search", "season", "seat", "second", "secret", "section",
    "security", "seed", "seek", "segment", "select", "sell", "seminar", "senior",
    "sense", "sentence", "series", "service", "session", "settle", "setup", "seven",
    "shadow", "shaft", "shallow", "share", "shed", "shell", "sheriff", "shield",
    "shift", "shine", "ship", "shiver", "shock", "shoe", "shoot", "shop",
    "short", "shoulder", "shove", "shrimp", "shrug", "shuffle", "shut", "shy",
    "sibling", "sick", "side", "siege", "sight", "sign", "silent", "silk",
    "silly", "silver", "similar", "simple", "since", "sing", "siren", "sister",
    "situate", "six", "size", "skate", "sketch", "ski", "skill", "skin",
    "skull", "slab", "slam", "sleep", "slender", "slice", "slide", "slight",
    "slim", "slogan", "slot", "slow", "slush", "small", "smart", "smile",
    "smoke", "smooth", "snack", "snake", "snap", "sniff", "snow", "soap",
    "soccer", "social", "sock", "soda", "soft", "solar", "soldier", "solid",
    "solution", "solve", "someone", "song", "soon", "sorry", "sort", "soul",
    "sound", "soup", "source", "south", "space", "spare", "spatial", "spawn",
    "speak", "special", "speed", "spell", "spend", "sphere", "spice", "spider",
    "spike", "spin", "spirit", "split", "spoil", "sponsor", "spoon", "sport",
    "spot", "spray", "spread", "spring", "spy", "square", "squeeze", "squirrel",
    "stable", "stadium", "staff", "stage", "stairs", "stamp", "stand", "start",
    "state", "stay", "steak", "steel", "stem", "step", "stereo", "stick",
    "still", "sting", "stock", "stomach", "stone", "stool", "story", "stove",
    "strategy", "street", "strike", "strong", "struggle", "student", "stuff", "stumble",
    "style", "subject", "submit", "subway", "success", "such", "sudden", "suffer",
    "sugar", "suggest", "suit", "summer", "sun", "sunny", "sunset", "super",
    "supply", "supreme", "sure", "surface", "surge", "surprise", "surround", "survey",
    "suspect", "sustain", "swallow", "swamp", "swap", "swarm", "swear", "sweet",
    "swift", "swim", "swing", "switch", "sword", "symbol", "symptom", "syrup",
    "system", "table", "tackle", "tag", "tail", "talent", "talk", "tank",
    "tape", "target", "task", "taste", "tattoo", "taxi", "teach", "team",
    "tell", "ten", "tenant", "tennis", "tent", "term", "test", "text",
    "thank", "that", "theme", "then", "theory", "there", "they", "thing",
    "this", "thought", "three", "thrive", "throw", "thumb", "thunder", "ticket",
    "tide", "tiger", "tilt", "timber", "time", "tiny", "tip", "tired",
    "tissue", "title", "toast", "tobacco", "today", "toddler", "toe", "together",
    "toilet", "token", "tomato", "tomorrow", "tone", "tongue", "tonight", "tool",
    "tooth", "top", "topic", "topple", "torch", "tornado", "tortoise", "toss",
    "total", "tourist", "toward", "tower", "town", "toy", "track", "trade",
    "traffic", "tragic", "train", "transfer", "trap", "trash", "travel", "tray",
    "treat", "tree", "trend", "trial", "tribe", "trick", "trigger", "trim",
    "trip", "trophy", "trouble", "truck", "true", "truly", "trumpet", "trust",
    "truth", "try", "tube", "tuition", "tumble", "tuna", "tunnel", "turkey",
    "turn", "turtle", "twelve", "twenty", "two", "type", "typical", "ugly",
    "umbrella", "unable", "unaware", "uncle", "uncover", "under", "undo", "unfair",
    "unfold", "unhappy", "uniform", "unique", "unit", "universe", "unknown", "unlock",
    "until", "unusual", "unveil", "update", "upgrade", "uphold", "upon", "upper",
    "upset", "urban", "urge", "usage", "use", "used", "useful", "useless",
    "usual", "utility", "vacant", "vacuum", "vague", "valid", "valley", "valve",
    "van", "vanish", "vapor", "various", "vast", "vault", "vehicle", "velvet",
    "vendor", "venture", "venue", "verb", "verify", "version", "very", "vessel",
    "veteran", "viable", "vibrant", "vicious", "victory", "video", "view", "village",
    "vintage", "violin", "virtual", "virus", "visa", "visit", "visual", "vital",
    "vivid", "vocal", "voice", "void", "volcano", "volume", "vote", "voyage",
    "wage", "wagon", "wait", "walk", "wall", "walnut", "want", "warfare",
    "warm", "warrior", "wash", "wasp", "waste", "watch", "water", "wave",
    "way", "wealth", "weapon", "wear", "weasel", "weather", "web", "wedding",
    "weekend", "weird", "welcome", "west", "wet", "whale", "what", "wheat",
    "wheel", "when", "where", "whip", "whisper", "wide", "width", "wife",
    "wild", "will", "win", "window", "wine", "wing", "wink", "winner",
    "winter", "wire", "wisdom", "wise", "wish", "witness", "wolf", "woman",
    "wonder", "wood", "wool", "word", "work", "world", "worry", "worth",
    "wrap", "wreck", "wrestle", "wrist", "write", "wrong", "yard", "year",
    "yellow", "you", "young", "youth", "zebra", "zero", "zone", "zoo",
]


def generate_password(
    length: int = 16,
    lowercase: bool = True,
    uppercase: bool = True,
    digits: bool = True,
    symbols: bool = True,
    exclude_ambiguous: bool = True,
    custom_chars: Optional[str] = None,
    min_lowercase: int = 0,
    min_uppercase: int = 0,
    min_digits: int = 0,
    min_symbols: int = 0,
) -> str:
    """
    Generate a secure random password.

    Args:
        length: Password length (default: 16)
        lowercase: Include lowercase letters (default: True)
        uppercase: Include uppercase letters (default: True)
        digits: Include digits (default: True)
        symbols: Include symbols (default: True)
        exclude_ambiguous: Exclude ambiguous characters like 0O1lI (default: True)
        custom_chars: Custom character set to use (overrides other options)
        min_lowercase: Minimum lowercase letters required
        min_uppercase: Minimum uppercase letters required
        min_digits: Minimum digits required
        min_symbols: Minimum symbols required

    Returns:
        Generated password string

    Raises:
        ValueError: If invalid parameters provided

    Example:
        >>> password = generate_password(12)
        >>> len(password)
        12
        >>> password = generate_password(20, symbols=False)
        >>> '!' not in password or '@' not in password  # May not have symbols
        True
    """
    # 边界处理：长度验证
    if length < 1:
        raise ValueError("Password length must be at least 1")

    # 如果提供了自定义字符集，直接使用
    if custom_chars:
        if not custom_chars.strip():
            raise ValueError("Custom characters cannot be empty")
        return ''.join(secrets.choice(custom_chars) for _ in range(length))

    # 构建字符集
    char_sets = []
    required_chars = []

    if lowercase:
        chars = LOWERCASE
        if exclude_ambiguous:
            chars = ''.join(c for c in chars if c not in AMBIGUOUS)
        char_sets.append(chars)
        if min_lowercase > 0:
            required_chars.extend(secrets.choice(chars) for _ in range(min_lowercase))

    if uppercase:
        chars = UPPERCASE
        if exclude_ambiguous:
            chars = ''.join(c for c in chars if c not in AMBIGUOUS)
        char_sets.append(chars)
        if min_uppercase > 0:
            required_chars.extend(secrets.choice(chars) for _ in range(min_uppercase))

    if digits:
        chars = DIGITS
        if exclude_ambiguous:
            chars = ''.join(c for c in chars if c not in AMBIGUOUS)
        char_sets.append(chars)
        if min_digits > 0:
            required_chars.extend(secrets.choice(chars) for _ in range(min_digits))

    if symbols:
        char_sets.append(SYMBOLS)
        if min_symbols > 0:
            required_chars.extend(secrets.choice(SYMBOLS) for _ in range(min_symbols))

    # 验证至少有一个字符集
    if not char_sets:
        raise ValueError("At least one character type must be enabled")

    # 合并所有字符集
    all_chars = ''.join(char_sets)

    # 计算剩余需要生成的字符数
    remaining_length = length - len(required_chars)

    # 边界处理：确保长度足够满足最小要求
    if remaining_length < 0:
        raise ValueError(
            f"Password length {length} is too short for minimum requirements "
            f"(need at least {len(required_chars)} characters)"
        )

    # 生成剩余字符
    password_chars = list(required_chars)
    password_chars.extend(secrets.choice(all_chars) for _ in range(remaining_length))

    # 打乱顺序
    secrets.SystemRandom().shuffle(password_chars)

    return ''.join(password_chars)


def generate_passphrase(
    word_count: int = 4,
    separator: str = "-",
    capitalize: bool = False,
    include_number: bool = False,
    word_list: Optional[List[str]] = None,
    min_word_length: int = 3,
    max_word_length: int = 12,
) -> str:
    """
    Generate a memorable passphrase from random words.

    Args:
        word_count: Number of words (default: 4)
        separator: Word separator (default: "-")
        capitalize: Capitalize first letter of each word (default: False)
        include_number: Append a random number (default: False)
        word_list: Custom word list (default: built-in list)
        min_word_length: Minimum word length (default: 3)
        max_word_length: Maximum word length (default: 12)

    Returns:
        Generated passphrase string

    Example:
        >>> phrase = generate_passphrase()
        >>> len(phrase.split('-'))
        4
        >>> phrase = generate_passphrase(6, separator=' ', capitalize=True)
        >>> phrase.count(' ')  # 5 spaces between 6 words
        5
    """
    # 边界处理：验证参数
    if word_count < 1:
        raise ValueError("Word count must be at least 1")

    # 使用提供的词表或默认词表
    words = word_list if word_list is not None else DEFAULT_WORD_LIST

    # 边界处理：空词表
    if not words:
        raise ValueError("Word list cannot be empty")

    # 过滤词表
    filtered_words = [
        w for w in words
        if min_word_length <= len(w) <= max_word_length
    ]

    # 如果过滤后为空，使用原始词表
    if not filtered_words:
        filtered_words = words

    # 选择随机词
    selected_words = [secrets.choice(filtered_words) for _ in range(word_count)]

    # 可选：首字母大写
    if capitalize:
        selected_words = [w.capitalize() for w in selected_words]

    # 构建密码短语
    passphrase = separator.join(selected_words)

    # 可选：添加数字
    if include_number:
        passphrase += str(secrets.randbelow(100))

    return passphrase


def generate_pronounceable(
    length: int = 12,
    include_digits: bool = False,
    include_symbols: bool = False,
) -> str:
    """
    Generate a pronounceable password using syllable patterns.

    Args:
        length: Approximate password length (default: 12)
        include_digits: Include some digits (default: False)
        include_symbols: Include some symbols (default: False)

    Returns:
        Pronounceable password string

    Example:
        >>> password = generate_pronounceable(10)
        >>> len(password) >= 8
        True
        >>> password.isalpha() or any(c.isalpha() for c in password)
        True
    """
    # 边界处理：长度验证
    if length < 4:
        length = 4

    # 音节模式: CVC (辅音-元音-辅音) 或 VCV 等
    consonants = "bcdfghjklmnpqrstvwxyz"
    vowels = "aeiou"

    # 随机选择起始模式
    patterns = ["CV", "VC", "CVC", "VCV", "CVCV"]

    result = []
    while len(''.join(result)) < length - 2:
        pattern = secrets.choice(patterns)
        for char_type in pattern:
            if char_type == 'C':
                result.append(secrets.choice(consonants))
            else:
                result.append(secrets.choice(vowels))

    # 可选：添加数字
    if include_digits:
        pos = secrets.randbelow(len(result))
        result.insert(pos, str(secrets.randbelow(10)))

    # 可选：添加符号
    if include_symbols:
        pos = secrets.randbelow(len(result))
        result.insert(pos, secrets.choice("!@#$%"))

    password = ''.join(result)

    # 截断或填充到目标长度
    if len(password) > length:
        password = password[:length]

    return password


def generate_pin(length: int = 6) -> str:
    """
    Generate a numeric PIN code.

    Args:
        length: PIN length (default: 6)

    Returns:
        Numeric PIN string

    Example:
        >>> pin = generate_pin(4)
        >>> len(pin)
        4
        >>> pin.isdigit()
        True
    """
    # 边界处理
    if length < 1:
        length = 1
    if length > 32:
        length = 32

    return ''.join(secrets.choice(DIGITS) for _ in range(length))


def generate_token(length: int = 32) -> str:
    """
    Generate a URL-safe random token.

    Args:
        length: Token length (default: 32)

    Returns:
        URL-safe token string

    Example:
        >>> token = generate_token(16)
        >>> len(token)
        16
        >>> all(c.isalnum() or c in '-_' for c in token)
        True
    """
    # 边界处理
    if length < 1:
        length = 1

    # URL-safe Base64 字符集
    chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_"

    return ''.join(secrets.choice(chars) for _ in range(length))


def generate_hex_token(length: int = 32) -> str:
    """
    Generate a hexadecimal token.

    Args:
        length: Number of hex characters (default: 32)

    Returns:
        Hexadecimal string

    Example:
        >>> token = generate_hex_token(16)
        >>> len(token)
        16
        >>> all(c in '0123456789abcdef' for c in token)
        True
    """
    # 边界处理
    if length < 1:
        length = 1

    return secrets.token_hex(length // 2 + 1)[:length]


def analyze_password(password: str) -> PasswordStrength:
    """
    Analyze password strength and security.

    Args:
        password: Password to analyze

    Returns:
        PasswordStrength object with analysis results

    Example:
        >>> result = analyze_password("MyP@ssw0rd!")
        >>> result.rating in ['weak', 'fair', 'good', 'strong', 'excellent']
        True
        >>> result.entropy > 0
        True
    """
    issues = []
    suggestions = []

    # 边界处理：空密码
    if not password:
        return PasswordStrength(
            score=0,
            entropy=0,
            crack_time="instant",
            rating="weak",
            issues=["Password is empty"],
            suggestions=["Create a password with at least 8 characters"],
        )

    length = len(password)

    # 检查字符类型
    has_lowercase = bool(re.search(r'[a-z]', password))
    has_uppercase = bool(re.search(r'[A-Z]', password))
    has_digits = bool(re.search(r'\d', password))
    has_symbols = bool(re.search(r'[!@#$%^&*()_+\-=\[\]{}|;:,.<>?]', password))

    # 计算字符集大小
    charset_size = 0
    if has_lowercase:
        charset_size += 26
    if has_uppercase:
        charset_size += 26
    if has_digits:
        charset_size += 10
    if has_symbols:
        charset_size += 32

    # 计算熵
    if charset_size > 0:
        entropy = length * math.log2(charset_size)
    else:
        entropy = 0

    # 检查常见问题
    if length < 8:
        issues.append("Password is too short (less than 8 characters)")
        suggestions.append("Use at least 8 characters, preferably 12 or more")

    if length < 12:
        suggestions.append("Consider using 12 or more characters for better security")

    if not has_lowercase:
        issues.append("Missing lowercase letters")
        suggestions.append("Add lowercase letters (a-z)")

    if not has_uppercase:
        issues.append("Missing uppercase letters")
        suggestions.append("Add uppercase letters (A-Z)")

    if not has_digits:
        issues.append("Missing digits")
        suggestions.append("Add digits (0-9)")

    if not has_symbols:
        suggestions.append("Consider adding symbols for extra security")

    # 检查常见模式
    common_patterns = [
        (r'(.)\1{2,}', "Repeated characters detected"),
        (r'(012|123|234|345|456|567|678|789|890)', "Sequential digits detected"),
        (r'(abc|bcd|cde|def|efg|fgh|ghi|hij|ijk|jkl|klm|lmn|mno|nop|opq|pqr|qrs|rst|stu|tuv|uvw|vwx|wxy|xyz)', "Sequential letters detected"),
        (r'(qwerty|asdfgh|zxcvbn)', "Keyboard pattern detected"),
    ]

    for pattern, message in common_patterns:
        if re.search(pattern, password.lower()):
            issues.append(message)
            suggestions.append("Avoid common patterns and sequences")
            break

    # 检查常见密码（简化版）
    common_passwords = {
        "password", "123456", "12345678", "qwerty", "abc123",
        "monkey", "master", "dragon", "111111", "baseball",
        "iloveyou", "trustno1", "sunshine", "princess", "welcome",
    }

    if password.lower() in common_passwords:
        issues.append("Password is too common")
        suggestions.append("Choose a unique password not found in common password lists")

    # 计算分数 (0-100)
    score = 0

    # 长度分数
    score += min(length * 4, 32)  # 最多 32 分

    # 字符类型分数
    if has_lowercase:
        score += 8
    if has_uppercase:
        score += 8
    if has_digits:
        score += 8
    if has_symbols:
        score += 12

    # 额外长度奖励
    if length >= 12:
        score += 10
    if length >= 16:
        score += 10

    # 模式惩罚
    score -= len(issues) * 8

    # 限制范围
    score = max(0, min(100, score))

    # 估算破解时间（基于 100亿/秒 的假设破解速度）
    if entropy > 0:
        combinations = 2 ** entropy
        seconds = combinations / 10_000_000_000  # 100亿次/秒

        crack_time = _format_crack_time(seconds)
    else:
        crack_time = "instant"

    # 评级
    if score >= 80:
        rating = "excellent"
    elif score >= 60:
        rating = "strong"
    elif score >= 40:
        rating = "good"
    elif score >= 20:
        rating = "fair"
    else:
        rating = "weak"

    return PasswordStrength(
        score=score,
        entropy=round(entropy, 2),
        crack_time=crack_time,
        rating=rating,
        issues=issues,
        suggestions=suggestions,
    )


def _format_crack_time(seconds: float) -> str:
    """格式化破解时间为人类可读格式。"""
    if seconds < 1:
        return "less than a second"
    elif seconds < 60:
        return f"{int(seconds)} seconds"
    elif seconds < 3600:
        minutes = int(seconds / 60)
        return f"{minutes} minute{'s' if minutes != 1 else ''}"
    elif seconds < 86400:
        hours = int(seconds / 3600)
        return f"{hours} hour{'s' if hours != 1 else ''}"
    elif seconds < 2592000:  # 30 days
        days = int(seconds / 86400)
        return f"{days} day{'s' if days != 1 else ''}"
    elif seconds < 31536000:  # 365 days
        months = int(seconds / 2592000)
        return f"{months} month{'s' if months != 1 else ''}"
    elif seconds < 31536000 * 100:  # 100 years
        years = int(seconds / 31536000)
        return f"{years} year{'s' if years != 1 else ''}"
    elif seconds < 31536000 * 1000:  # 1000 years
        centuries = int(seconds / (31536000 * 100))
        return f"{centuries} centur{'ies' if centuries != 1 else 'y'}"
    elif seconds < 31536000 * 1000000:  # 1 million years
        millennia = int(seconds / (31536000 * 1000))
        return f"{millennia} millennium{'a' if millennia != 1 else ''}"
    else:
        millions = int(seconds / (31536000 * 1000000))
        return f"{millions}+ million years"


def check_password_pwned(password: str) -> bool:
    """
    Check if a password has been exposed in known data breaches.
    Note: This is a simulation for demonstration. In production, use Have I Been Pwned API.

    Args:
        password: Password to check

    Returns:
        True if password appears in breach database (simulated)

    Example:
        >>> check_password_pwned("password")  # Common password
        True
        >>> check_password_pwned("xK9#mP2$vL5")  # Uncommon password
        False
    """
    # 常见密码黑名单（模拟）
    common_breached = {
        "password", "123456", "12345678", "qwerty", "abc123",
        "monkey", "master", "dragon", "111111", "baseball",
        "iloveyou", "trustno1", "sunshine", "princess", "welcome",
        "admin", "login", "passw0rd", "password1", "password123",
    }

    return password.lower() in common_breached


def calculate_entropy(password: str) -> float:
    """
    Calculate the entropy (bits) of a password.

    Args:
        password: Password to analyze

    Returns:
        Entropy in bits

    Example:
        >>> entropy = calculate_entropy("password")
        >>> entropy > 0
        True
    """
    if not password:
        return 0.0

    # 计算字符集大小
    has_lower = bool(re.search(r'[a-z]', password))
    has_upper = bool(re.search(r'[A-Z]', password))
    has_digit = bool(re.search(r'\d', password))
    has_symbol = bool(re.search(r'[!@#$%^&*()_+\-=\[\]{}|;:,.<>?]', password))
    has_space = ' ' in password

    charset_size = 0
    if has_lower:
        charset_size += 26
    if has_upper:
        charset_size += 26
    if has_digit:
        charset_size += 10
    if has_symbol:
        charset_size += 32
    if has_space:
        charset_size += 1

    # 如果没有识别的字符集，使用实际使用的唯一字符数
    if charset_size == 0:
        charset_size = len(set(password))

    return round(len(password) * math.log2(charset_size), 2)


def generate_diceware(
    word_count: int = 5,
    word_list: Optional[List[str]] = None,
    separator: str = " ",
) -> str:
    """
    Generate a passphrase using Diceware method.
    Uses 5 dice rolls per word for true randomness.

    Args:
        word_count: Number of words (default: 5)
        word_list: Custom word list (should have 7776 words for true Diceware)
        separator: Word separator (default: space)

    Returns:
        Diceware-style passphrase

    Example:
        >>> phrase = generate_diceware(5)
        >>> len(phrase.split(' '))
        5
    """
    words = word_list if word_list is not None else DEFAULT_WORD_LIST

    selected = [secrets.choice(words) for _ in range(word_count)]

    return separator.join(selected)


def suggest_improvements(password: str) -> List[str]:
    """
    Suggest improvements for a password.

    Args:
        password: Password to analyze

    Returns:
        List of improvement suggestions

    Example:
        >>> suggestions = suggest_improvements("password")
        >>> len(suggestions) > 0
        True
    """
    strength = analyze_password(password)
    return strength.suggestions


def is_strong_password(
    password: str,
    min_length: int = 12,
    require_uppercase: bool = True,
    require_lowercase: bool = True,
    require_digits: bool = True,
    require_symbols: bool = False,
) -> Tuple[bool, List[str]]:
    """
    Check if a password meets strength requirements.

    Args:
        password: Password to check
        min_length: Minimum length requirement
        require_uppercase: Require uppercase letters
        require_lowercase: Require lowercase letters
        require_digits: Require digits
        require_symbols: Require symbols

    Returns:
        Tuple of (is_strong, list_of_issues)

    Example:
        >>> is_strong, issues = is_strong_password("MyP@ssw0rd")
        >>> isinstance(is_strong, bool)
        True
    """
    issues = []

    if len(password) < min_length:
        issues.append(f"Password must be at least {min_length} characters")

    if require_uppercase and not re.search(r'[A-Z]', password):
        issues.append("Password must contain uppercase letters")

    if require_lowercase and not re.search(r'[a-z]', password):
        issues.append("Password must contain lowercase letters")

    if require_digits and not re.search(r'\d', password):
        issues.append("Password must contain digits")

    if require_symbols and not re.search(r'[!@#$%^&*()_+\-=\[\]{}|;:,.<>?]', password):
        issues.append("Password must contain symbols")

    return len(issues) == 0, issues


def generate_password_variants(
    base_word: str,
    count: int = 5,
    style: str = "mixed",
) -> List[str]:
    """
    Generate multiple password variants based on a base word.

    Args:
        base_word: Base word to build passwords from
        count: Number of variants to generate
        style: Style of variations ("mixed", "numbers", "symbols", "leet")

    Returns:
        List of password variants

    Example:
        >>> variants = generate_password_variants("secure", count=3)
        >>> len(variants)
        3
    """
    if not base_word:
        return []

    variants = []

    for i in range(count):
        if style == "leet" or (style == "mixed" and i % 4 == 0):
            # Leet speak转换
            leet_map = {'a': '@', 'e': '3', 'i': '1', 'o': '0', 's': '$', 't': '7'}
            variant = ''.join(leet_map.get(c.lower(), c) for c in base_word)
        elif style == "numbers" or (style == "mixed" and i % 4 == 1):
            # 添加数字
            variant = base_word + str(secrets.randbelow(1000))
        elif style == "symbols" or (style == "mixed" and i % 4 == 2):
            # 添加符号
            variant = base_word.capitalize() + secrets.choice("!@#$%^&*")
        else:
            # 随机混合
            suffix = ''.join(secrets.choice(DIGITS) for _ in range(3))
            symbol = secrets.choice("!@#$%^&*")
            variant = base_word.capitalize() + suffix + symbol

        variants.append(variant)

    return variants


def estimate_crack_time(
    password: str,
    guesses_per_second: int = 10_000_000_000,
) -> str:
    """
    Estimate time to crack a password.

    Args:
        password: Password to analyze
        guesses_per_second: Assumed cracking speed (default: 10 billion/sec)

    Returns:
        Human-readable time estimate

    Example:
        >>> time = estimate_crack_time("MyVeryLongP@ssw0rd123!")
        >>> "year" in time.lower() or "centur" in time.lower() or "millennium" in time.lower()
        True
    """
    entropy = calculate_entropy(password)

    if entropy <= 0:
        return "instant"

    combinations = 2 ** entropy
    seconds = combinations / guesses_per_second

    return _format_crack_time(seconds)


def create_memorable_password(
    include_pattern: bool = True,
    separator: str = "-",
) -> str:
    """
    Create a memorable yet secure password using a pattern.
    Format: [Word][Number][Symbol][Word]

    Args:
        include_pattern: Include pattern elements
        separator: Separator between words

    Returns:
        Memorable password string

    Example:
        >>> password = create_memorable_password()
        >>> len(password) > 8
        True
    """
    # 选择两个随机词
    word1 = secrets.choice(DEFAULT_WORD_LIST)
    word2 = secrets.choice(DEFAULT_WORD_LIST)

    if include_pattern:
        # 添加数字和符号
        number = str(secrets.randbelow(100))
        symbol = secrets.choice("!@#$%^&*")

        # 组合: Word-Number-Symbol-Word
        return f"{word1.capitalize()}{separator}{number}{separator}{symbol}{separator}{word2.capitalize()}"
    else:
        return f"{word1.capitalize()}{separator}{word2.capitalize()}"


def batch_generate(
    count: int = 10,
    style: PasswordStyle = PasswordStyle.RANDOM,
    **kwargs,
) -> List[str]:
    """
    Generate multiple passwords at once.

    Args:
        count: Number of passwords to generate
        style: Password generation style
        **kwargs: Additional arguments passed to the generator

    Returns:
        List of generated passwords

    Example:
        >>> passwords = batch_generate(5, PasswordStyle.PASSPHRASE, word_count=3)
        >>> len(passwords)
        5
    """
    if count < 1:
        return []

    passwords = []

    for _ in range(count):
        if style == PasswordStyle.RANDOM:
            passwords.append(generate_password(**kwargs))
        elif style == PasswordStyle.PASSPHRASE:
            passwords.append(generate_passphrase(**kwargs))
        elif style == PasswordStyle.PRONOUNCEABLE:
            passwords.append(generate_pronounceable(**kwargs))
        elif style == PasswordStyle.PIN:
            passwords.append(generate_pin(**kwargs))
        elif style == PasswordStyle.TOKEN:
            passwords.append(generate_token(**kwargs))

    return passwords


def get_word_list_stats(word_list: Optional[List[str]] = None) -> Dict[str, any]:
    """
    Get statistics about a word list.

    Args:
        word_list: Word list to analyze (default: built-in list)

    Returns:
        Dictionary with word list statistics

    Example:
        >>> stats = get_word_list_stats()
        >>> stats['word_count'] > 1000
        True
    """
    words = word_list if word_list is not None else DEFAULT_WORD_LIST

    if not words:
        return {
            'word_count': 0,
            'min_length': 0,
            'max_length': 0,
            'avg_length': 0,
            'unique_words': 0,
        }

    lengths = [len(w) for w in words]

    return {
        'word_count': len(words),
        'min_length': min(lengths),
        'max_length': max(lengths),
        'avg_length': round(sum(lengths) / len(lengths), 2),
        'unique_words': len(set(words)),
    }