"""
密码短语生成工具 (Passphrase Utils)
生成安全且易于记忆的密码短语
零外部依赖，纯 Python 标准库实现

功能列表:
1. PassphraseGenerator - 密码短语生成器
2. 计算密码短语熵值
3. 支持多种分隔符和格式
4. 内置单词列表（英语常用词）
5. 支持自定义单词列表
6. Diceware 模式支持
"""

import secrets
import math
from typing import List, Optional, Callable
from dataclasses import dataclass
from enum import Enum


class Separator(Enum):
    """分隔符类型"""
    SPACE = " "
    HYPHEN = "-"
    UNDERSCORE = "_"
    DOT = "."
    NONE = ""
    RANDOM = "random"


class WordCase(Enum):
    """单词大小写"""
    LOWER = "lower"
    UPPER = "upper"
    CAPITALIZE = "capitalize"
    RANDOM = "random"
    ALTERNATE = "alternate"


# 内置的常用英语单词列表（约 7776 个 Diceware 标准单词的一部分）
# 这些单词易于记忆和拼写
BUILTIN_WORDLIST = [
    # A
    "able", "acid", "aged", "also", "area", "army", "away", "baby", "back", "ball",
    "band", "bank", "base", "bath", "bear", "beat", "been", "beer", "bell", "belt",
    "best", "bill", "bird", "blow", "blue", "boat", "body", "bomb", "bond", "bone",
    "book", "boom", "born", "boss", "both", "bowl", "bulk", "burn", "bush", "busy",
    # B
    "call", "calm", "came", "camp", "card", "care", "case", "cash", "cast", "cell",
    "chat", "chip", "city", "club", "coal", "coat", "code", "cold", "come", "cook",
    "cool", "cope", "copy", "core", "cost", "crew", "crop", "dark", "data", "date",
    "dawn", "days", "dead", "deal", "dean", "dear", "debt", "deep", "desk", "diet",
    # C
    "dirt", "dish", "disk", "does", "done", "door", "dose", "down", "draw", "drew",
    "drop", "drug", "dual", "duke", "dust", "duty", "each", "earn", "ease", "east",
    "easy", "edge", "else", "even", "ever", "evil", "exit", "face", "fact", "fail",
    "fair", "fall", "fame", "farm", "fast", "fate", "fear", "feed", "feel", "feet",
    # D
    "fell", "felt", "file", "fill", "film", "find", "fine", "fire", "firm", "fish",
    "five", "flat", "flow", "folk", "food", "foot", "ford", "form", "fort", "four",
    "free", "from", "fuel", "full", "fund", "gain", "game", "gang", "gave", "gear",
    "gene", "gift", "girl", "give", "glad", "goal", "goes", "gold", "golf", "gone",
    # E
    "good", "grab", "gray", "grew", "grey", "grow", "gulf", "guys", "hair", "half",
    "hall", "hand", "hang", "hard", "harm", "hate", "have", "head", "heat", "held",
    "hell", "help", "here", "hero", "high", "hill", "hire", "hold", "hole", "holy",
    "home", "hope", "host", "hour", "huge", "hung", "hunt", "hurt", "idea", "inch",
    # F
    "iron", "item", "jack", "jail", "jane", "jean", "jobs", "john", "join", "joke",
    "josh", "judy", "jump", "june", "jury", "just", "keen", "keep", "kent", "kept",
    "kick", "kill", "kind", "king", "knee", "knew", "know", "lack", "lady", "laid",
    "lake", "land", "lane", "last", "late", "lead", "left", "less", "life", "lift",
    # G
    "like", "line", "link", "list", "live", "load", "loan", "lock", "logo", "long",
    "look", "lord", "lose", "loss", "lost", "love", "luck", "made", "mail", "main",
    "make", "male", "mall", "many", "mark", "mars", "mask", "mass", "matt", "meal",
    "mean", "meat", "meet", "menu", "mere", "mild", "mile", "milk", "mill", "mind",
    # H
    "mine", "miss", "mode", "mood", "moon", "more", "most", "move", "much", "must",
    "myth", "nail", "name", "navy", "near", "neat", "neck", "need", "news", "next",
    "nice", "nick", "nine", "none", "nose", "note", "nova", "nuts", "okay", "once",
    "only", "onto", "open", "oral", "over", "pace", "pack", "page", "paid", "pain",
    # I
    "pair", "palm", "park", "part", "pass", "past", "path", "peak", "pick", "pine",
    "pink", "pipe", "plan", "play", "plot", "plus", "poem", "poet", "poll", "pool",
    "poor", "port", "pose", "post", "pour", "pray", "pull", "pure", "push", "race",
    "rain", "rank", "rare", "rate", "read", "real", "rear", "rely", "rent", "rest",
    # J
    "rice", "rich", "ride", "ring", "rise", "risk", "road", "rock", "rode", "role",
    "roll", "roof", "room", "root", "rose", "rule", "rush", "ruth", "safe", "said",
    "sake", "sale", "salt", "same", "sand", "save", "seal", "seat", "seed", "seek",
    "seem", "seen", "self", "sell", "send", "sent", "ship", "shop", "shot", "show",
    # K
    "shut", "sick", "side", "sign", "silk", "size", "skin", "slip", "slow", "snow",
    "soft", "soil", "sold", "sole", "some", "song", "soon", "sort", "soul", "spot",
    "star", "stay", "stem", "step", "stop", "such", "suit", "sure", "take", "tale",
    "talk", "tall", "tank", "tape", "task", "team", "tell", "tend", "term", "test",
    # L
    "text", "than", "that", "them", "then", "they", "thin", "this", "thus", "till",
    "time", "tiny", "told", "toll", "tone", "took", "tool", "tour", "town", "tree",
    "trip", "true", "tube", "tune", "turn", "twin", "type", "unit", "upon", "used",
    "user", "vary", "vast", "verb", "very", "vice", "view", "vote", "wage", "wait",
    # M
    "wake", "walk", "wall", "want", "warm", "warn", "wash", "wave", "ways", "weak",
    "wear", "week", "well", "went", "were", "west", "what", "when", "whom", "wide",
    "wife", "wild", "will", "wind", "wine", "wing", "wire", "wise", "wish", "with",
    "wood", "word", "wore", "work", "wrap", "yard", "yeah", "year", "yoga", "your",
    "zero", "zone", "zoom",
    # N
    # 额外常用词
    "apple", "baker", "beach", "brain", "bread", "brick", "bring", "brown", "brush",
    "carry", "catch", "chair", "chart", "cheap", "check", "chest", "claim", "class",
    "clean", "clear", "climb", "clock", "close", "cloth", "cloud", "coach", "count",
    "court", "cover", "crack", "craft", "crash", "cream", "crime", "cross", "crowd",
    # O
    "crown", "cycle", "daily", "dance", "debug", "delta", "doubt", "draft", "drain",
    "drama", "dream", "dress", "drink", "drive", "drown", "drunk", "earth", "eight",
    "email", "empty", "enemy", "enjoy", "enter", "entry", "equal", "error", "essay",
    "event", "every", "exact", "exist", "extra", "faith", "false", "fault", "field",
    # P
    "fifth", "fifty", "fight", "final", "first", "fixed", "flash", "fleet", "floor",
    "fluid", "focus", "force", "forth", "forty", "forum", "frame", "frank", "fresh",
    "front", "fruit", "glass", "glory", "grace", "grade", "grain", "grand", "grant",
    "grape", "grasp", "grass", "grave", "great", "green", "greet", "gross", "group",
    # Q
    "guard", "guess", "guest", "guide", "guilt", "happy", "harsh", "haven", "heavy",
    "hello", "hence", "hobby", "horse", "hotel", "house", "human", "humor", "ideal",
    "image", "imply", "index", "inner", "input", "issue", "japan", "jimmy", "joint",
    "jones", "judge", "juice", "knife", "knock", "known", "label", "labor", "large",
    # R
    "laugh", "layer", "learn", "lease", "leave", "legal", "lemon", "level", "light",
    "limit", "logic", "loose", "lorry", "lucky", "lunch", "lunar", "magic", "major",
    "maker", "march", "maria", "match", "maybe", "mayor", "medal", "media", "metal",
    "meter", "might", "minor", "mixed", "model", "money", "month", "motor", "mount",
    # S
    "mouse", "mouth", "movie", "music", "naked", "nerve", "never", "night", "ninth",
    "noise", "north", "novel", "nurse", "ocean", "offer", "often", "olive", "order",
    "other", "outer", "owner", "paint", "panel", "paper", "party", "peace", "peter",
    "phase", "phone", "photo", "piano", "piece", "pilot", "pitch", "pizza", "place",
    # T
    "plain", "plane", "plant", "plate", "plaza", "point", "polar", "pound", "power",
    "press", "price", "pride", "prime", "print", "prior", "prize", "proof", "proud",
    "prove", "pulse", "pupil", "queen", "query", "quest", "quick", "quiet", "quite",
    "radar", "radio", "raise", "rally", "ranch", "range", "rapid", "ratio", "reach",
    # U
    "react", "ready", "refer", "relax", "reply", "right", "rigid", "rival", "river",
    "robot", "rocky", "roman", "rough", "round", "route", "royal", "rugby", "ruler",
    "rural", "sadly", "saint", "salad", "salon", "sandy", "santa", "sauce", "scale",
    "scene", "scoop", "scope", "score", "scout", "sharp", "sheet", "shelf", "shell",
    # V
    "shift", "shirt", "shock", "shoot", "shore", "short", "shout", "sight", "sigma",
    "silly", "simon", "since", "sixth", "skill", "skirt", "slave", "sleep", "slice",
    "slide", "slope", "small", "smart", "smell", "smile", "smoke", "snake", "solid",
    "solve", "sorry", "sound", "south", "space", "spare", "spark", "speak", "speed",
    # W
    "spend", "spite", "split", "spoke", "spoon", "sport", "spray", "squad", "stack",
    "staff", "stage", "stair", "stake", "stall", "stamp", "stand", "stark", "start",
    "state", "steak", "steal", "steam", "steel", "steep", "steer", "stick", "still",
    "stock", "stone", "store", "storm", "story", "stove", "strap", "straw", "strip",
    # X
    "stuck", "study", "stuff", "style", "sugar", "suite", "super", "sunny", "susan",
    "sweet", "swing", "sword", "table", "taken", "taste", "taxes", "teach", "teeth",
    "tempo", "tense", "terms", "thank", "theft", "theme", "there", "these", "thick",
    "thief", "thing", "think", "third", "those", "three", "threw", "throw", "thumb",
    # Y
    "tight", "timber", "today", "token", "tommy", "trace", "track", "trade", "trail",
    "train", "trash", "treat", "trend", "trial", "tribe", "trick", "tried", "truck",
    "truly", "trump", "trunk", "trust", "truth", "twice", "uncle", "under", "union",
    "unity", "until", "upper", "upset", "urban", "usage", "usual", "valid", "value",
    # Z
    "video", "virus", "visit", "vital", "vocal", "voice", "voter", "wagon", "waste",
    "watch", "water", "wheel", "where", "which", "while", "white", "whole", "whose",
    "witch", "woman", "worth", "would", "wound", "write", "wrong", "wrote", "yield",
    "young", "youth", "alpha", "bravo", "delta", "gamma", "omega", "sigma", "theta",
]

# Diceware 标准单词列表（简化版，约 7776 个单词的代表性子集）
DICETIME_WORDLIST = [
    "abandon", "ability", "able", "about", "above", "absent", "absorb", "abstract",
    "absurd", "abuse", "access", "accident", "account", "accuse", "achieve", "acid",
    "acoustic", "acquire", "across", "act", "action", "actor", "actress", "actual",
    "adapt", "add", "addict", "address", "adjust", "admit", "adult", "advance",
    "advice", "aerobic", "affair", "afford", "afraid", "again", "age", "agent",
    "agree", "ahead", "aim", "air", "airport", "aisle", "alarm", "album", "alcohol",
    "alert", "alien", "all", "alley", "allow", "almost", "alone", "alpha", "already",
    "also", "alter", "always", "amateur", "amazing", "among", "amount", "amused",
    "analyst", "anchor", "ancient", "anger", "angle", "angry", "animal", "ankle",
    "announce", "annual", "another", "answer", "antenna", "antique", "anxiety", "any",
    "apart", "apology", "appear", "apple", "approve", "april", "arch", "arctic", "area",
    "arena", "argue", "arm", "armed", "armor", "army", "around", "arrange", "arrest",
    "arrive", "arrow", "art", "article", "artist", "ask", "aspect", "assault", "asset",
    "assist", "assume", "asthma", "athlete", "atom", "attack", "attend", "attitude",
    "attract", "auction", "audit", "august", "aunt", "author", "auto", "autumn", "avail",
    "average", "avocado", "avoid", "awake", "aware", "away", "awesome", "awful", "awkward",
    "axis", "baby", "bachelor", "bacon", "badge", "bag", "balance", "balcony", "ball",
    "bamboo", "banana", "banner", "bar", "barely", "bargain", "barrel", "base", "basic",
    "basket", "battle", "beach", "bean", "beauty", "become", "beef", "before", "begin",
    "behave", "behind", "believe", "below", "belt", "bench", "benefit", "best", "betray",
    "better", "between", "beyond", "bicycle", "bid", "bike", "bind", "biology", "bird",
    "birth", "bitter", "black", "blade", "blame", "blanket", "blast", "bleak", "bless",
    "blind", "blood", "blossom", "blouse", "blue", "blur", "blush", "board", "boat",
    "body", "boil", "bomb", "bone", "bonus", "book", "boost", "border", "boring", "borrow",
    "boss", "bottom", "bounce", "box", "boy", "bracket", "brain", "brand", "brass", "brave",
    "bread", "breeze", "brick", "bridge", "brief", "bright", "bring", "brisk", "broken",
    "bronze", "broom", "brother", "brown", "brush", "bubble", "buddy", "budget", "buffalo",
    "build", "bulb", "bulk", "bullet", "bundle", "bunker", "burden", "burger", "burst",
    "bus", "business", "busy", "butter", "buyer", "buzz", "cabbage", "cabin", "cable",
    "cactus", "cage", "cake", "call", "calm", "camera", "camp", "can", "canal", "cancel",
    "candy", "cannon", "canoe", "canvas", "canyon", "capable", "capital", "captain", "car",
    "carbon", "card", "cargo", "carpet", "carry", "cart", "case", "cash", "casino", "castle",
    "casual", "cat", "catalog", "catch", "category", "cattle", "caught", "cause", "caution",
    "cave", "ceiling", "cement", "census", "cereal", "certain", "chain", "chair", "chalk",
    "champion", "change", "chaos", "chapter", "charge", "chase", "chat", "cheap", "check",
    "cheese", "chef", "cherry", "chest", "chicken", "chief", "child", "chimney", "choice",
    "choose", "chronic", "chuckle", "chunk", "churn", "cigar", "cinema", "circle", "citizen",
    "city", "civil", "claim", "clap", "clarify", "clarity", "clash", "clasp", "class",
    "classic", "classroom", "clean", "clear", "clerk", "clever", "click", "client", "cliff",
    "climb", "clinic", "clip", "clock", "clog", "close", "cloth", "cloud", "clover", "club",
    "clutch", "clue", "clump", "coach", "coal", "coast", "coat", "code", "coffee", "coil",
    "coin", "collect", "color", "column", "comb", "combat", "comedy", "comfort", "comic",
    "common", "company", "concert", "conduct", "confirm", "connect", "consist", "contact",
    "context", "contract", "contrast", "control", "convert", "cookie", "cool", "cope",
    "copy", "core", "corn", "corner", "corridor", "cost", "couch", "cough", "could", "count",
    "counter", "country", "couple", "course", "court", "cousin", "cover", "crack", "craft",
    "crash", "crawl", "crazy", "cream", "credit", "creek", "crew", "cricket", "crime", "crisp",
    "critic", "crop", "cross", "crouch", "crowd", "crown", "crucial", "cruel", "cruise",
    "crush", "cry", "crystal", "cube", "culture", "cup", "curious", "current", "curtain",
    "curve", "cushion", "custom", "cute", "cycle", "dad", "damage", "damp", "dance", "danger",
    "dare", "dark", "data", "daughter", "day", "dead", "deal", "debate", "debris", "decade",
    "decide", "decay", "decorate", "decrease", "deer", "defense", "define", "defy", "degree",
    "delay", "deliver", "demand", "demise", "denial", "dentist", "deny", "depart", "depend",
    "deposit", "depth", "deputy", "derive", "describe", "desert", "design", "desk", "despair",
    "detail", "detect", "develop", "device", "devote", "diagram", "dial", "diamond", "diary",
    "dice", "diet", "differ", "digital", "dignity", "dilemma", "dinner", "dinosaur", "direct",
    "dirt", "disagree", "discover", "disease", "dish", "dismiss", "disorder", "display",
    "distance", "divert", "divide", "divorce", "dizzy", "doctor", "document", "dog", "doll",
    "dolphin", "domain", "donate", "donkey", "donor", "door", "dose", "double", "dove", "draft",
    "dragon", "drama", "drastic", "draw", "dream", "dress", "drift", "drill", "drink", "drip",
    "drive", "drop", "drum", "dry", "duck", "dumb", "dune", "during", "dust", "dutch", "duty",
    "dwarf", "dynamic", "eager", "eagle", "early", "earn", "earth", "easily", "east", "easy",
    "echo", "ecology", "economy", "edge", "edit", "educate", "effort", "egg", "eight", "either",
    "elbow", "elder", "electric", "elegant", "element", "elephant", "elevator", "elite", "else",
    "embark", "embody", "embrace", "emerge", "emotion", "employ", "empower", "empty", "enable",
    "enact", "end", "endless", "endorse", "enemy", "energy", "enforce", "engage", "engine",
    "enhance", "enjoy", "enlist", "enough", "enrich", "enroll", "ensure", "enter", "entire",
    "entrance", "entry", "envelope", "episode", "equal", "equip", "era", "erode", "erosion",
    "error", "erupt", "escape", "essay", "essence", "estate", "eternal", "ethics", "evidence",
    "evil", "evoke", "evolve", "exact", "example", "excess", "exchange", "excite", "exclude",
    "excuse", "execute", "exercise", "exhaust", "exhibit", "exile", "exist", "exit", "exotic",
    "expand", "expect", "expire", "explain", "expose", "express", "extend", "extra", "eye",
    "eyebrow", "fabric", "face", "faculty", "fade", "faint", "faith", "fall", "false", "fame",
    "family", "famous", "fan", "fancy", "fantasy", "farm", "fashion", "fat", "fatal", "father",
    "fatigue", "fault", "favorite", "feature", "february", "federal", "ferry", "fetch", "fever",
    "fiber", "fiction", "field", "figure", "file", "filter", "final", "find", "fine", "finger",
    "finish", "fire", "firm", "first", "fiscal", "fish", "fit", "fitness", "fix", "flag", "flame",
    "flash", "flat", "flavor", "flee", "flesh", "flight", "flip", "float", "flock", "flood",
    "floor", "flower", "fluid", "flush", "fly", "foam", "focus", "fog", "foil", "fold", "follow",
    "food", "foot", "force", "forest", "forget", "fork", "fortune", "forum", "forward", "fossil",
    "foster", "found", "fox", "fragile", "frame", "frequent", "fresh", "friend", "fringe", "frog",
    "front", "frost", "frown", "frozen", "fruit", "fuel", "fun", "funny", "furnace", "fury",
    "future", "gadget", "gain", "galaxy", "gallery", "game", "gap", "garage", "garbage", "garden",
    "garlic", "garment", "gas", "gasp", "gate", "gather", "gauge", "gaze", "general", "genius",
    "genre", "gentle", "genuine", "gesture", "ghost", "giant", "gift", "ginger", "giraffe", "girl",
    "give", "glad", "glance", "glare", "glass", "glide", "glimpse", "globe", "gloom", "glory",
    "glove", "glow", "glue", "goal", "goddess", "gold", "good", "goose", "gorilla", "gospel",
    "gossip", "govern", "gown", "grab", "grace", "grain", "grant", "grape", "grass", "gravity",
    "great", "green", "grid", "grief", "grill", "grimace", "grin", "grind", "grip", "grocery",
    "group", "grow", "grunt", "guard", "guess", "guest", "guide", "guilt", "guitar", "gun", "gym",
    "habit", "hair", "half", "hammer", "hamster", "hand", "hang", "happen", "happy", "harbor",
    "hard", "harsh", "harvest", "hat", "have", "hawk", "hazard", "head", "health", "heart", "heavy",
    "hedgehog", "height", "hello", "helmet", "help", "hen", "hero", "hidden", "high", "hill", "hint",
    "hip", "hire", "history", "hobby", "hockey", "hold", "hole", "holiday", "hollow", "home", "honey",
    "hood", "hook", "hope", "horn", "horror", "horse", "hospital", "host", "hotel", "hour", "hover",
    "hub", "huge", "human", "humble", "humor", "hundred", "hungry", "hunt", "hurdle", "hurry", "hurt",
    "husband", "hybrid", "ice", "icon", "idea", "identify", "idle", "ignore", "ill", "illness",
    "image", "imitate", "immense", "immune", "impact", "impose", "improve", "impulse", "inch",
    "include", "income", "increase", "index", "indicate", "indoor", "infant", "inflict", "inform",
    "inherit", "initial", "inject", "injury", "inmate", "inner", "innocent", "input", "inquiry",
    "insane", "insect", "inside", "inspire", "install", "intact", "interest", "into", "invest",
    "invite", "involve", "iron", "island", "isolate", "issue", "item", "ivory", "jacket", "jaguar",
    "jar", "jazz", "jealous", "jeans", "jelly", "jewel", "job", "join", "joke", "journey", "joy",
    "judge", "juice", "jump", "jungle", "junior", "junk", "just", "kangaroo", "keen", "keep", "ketchup",
    "key", "kick", "kid", "kidney", "kind", "kingdom", "kiss", "kit", "kitchen", "kite", "kitten",
    "kiwi", "knee", "knife", "knock", "know", "lab", "label", "labor", "ladder", "lady", "lake", "lamp",
    "language", "laptop", "large", "later", "latin", "laugh", "laundry", "lava", "law", "lawn", "lawsuit",
    "layer", "lazy", "leader", "leaf", "learn", "leave", "lecture", "left", "leg", "legal", "legend",
    "leisure", "lemon", "lend", "length", "lens", "leopard", "lesson", "letter", "level", "liar", "liberty",
    "library", "license", "life", "lift", "light", "like", "limb", "limit", "link", "lion", "liquid",
    "list", "little", "live", "lizard", "load", "loan", "lobster", "local", "lock", "logic", "lonely",
    "long", "loop", "lottery", "loud", "lounge", "love", "luck", "luggage", "lumber", "lunar", "lunch",
    "luxury", "lyrics", "machine", "mad", "magic", "magnet", "maid", "mail", "main", "major", "make",
    "mammal", "man", "manage", "mandate", "mango", "mansion", "manual", "maple", "marble", "march",
    "margin", "marine", "market", "marriage", "mask", "mass", "master", "match", "material", "math",
    "matrix", "matter", "maximum", "maze", "meadow", "mean", "measure", "meat", "mechanic", "medal",
    "media", "melody", "melt", "member", "memory", "mention", "menu", "mercy", "merge", "merit", "merry",
    "mesh", "message", "metal", "method", "middle", "midnight", "milk", "million", "mimic", "mind", "minimum",
    "minor", "minute", "miracle", "mirror", "misery", "miss", "mistake", "mix", "mixed", "mixture", "mobile",
    "model", "modify", "mom", "moment", "monitor", "monkey", "monster", "month", "moon", "moral", "more",
    "morning", "mosquito", "mother", "motion", "motor", "mountain", "mouse", "move", "movie", "much", "muffin",
    "mule", "multiply", "muscle", "museum", "mushroom", "music", "must", "mutual", "myself", "mystery", "myth",
    "naive", "name", "napkin", "narrow", "nasty", "nation", "nature", "near", "neck", "need", "negative",
    "neglect", "neither", "nephew", "nerve", "nest", "net", "network", "neutral", "never", "news", "next",
    "nice", "night", "noble", "noise", "nominee", "noodle", "normal", "north", "nose", "notable", "note",
    "nothing", "notice", "novel", "now", "nuclear", "number", "nurse", "nut", "oak", "obey", "object", "oblige",
    "obscure", "observe", "obtain", "obvious", "occur", "ocean", "october", "odor", "off", "offer", "office",
    "often", "oil", "okay", "old", "olive", "olympic", "omit", "once", "one", "onion", "online", "only", "open",
    "opera", "opinion", "oppose", "option", "orange", "orbit", "orchard", "order", "ordinary", "organ", "orient",
    "original", "orphan", "ostrich", "other", "outdoor", "outer", "output", "outside", "oval", "oven", "over",
    "own", "owner", "oxygen", "oyster", "ozone", "pact", "paddle", "page", "pair", "palace", "palm", "panda",
    "panel", "panic", "panther", "paper", "parade", "parent", "park", "parrot", "party", "pass", "patch", "path",
    "patient", "patrol", "pattern", "pause", "pave", "payment", "peace", "peanut", "pear", "peasant", "pelican",
    "pen", "penalty", "pencil", "people", "pepper", "perfect", "permit", "person", "pet", "phone", "photo",
    "phrase", "physical", "piano", "picnic", "picture", "piece", "pig", "pigeon", "pill", "pilot", "pink",
    "pioneer", "pipe", "pistol", "pitch", "pizza", "place", "planet", "plastic", "plate", "play", "please",
    "pledge", "pluck", "plug", "plunge", "poem", "poet", "point", "polar", "pole", "police", "pond", "pony",
    "pool", "popular", "portion", "position", "possible", "post", "potato", "pottery", "poverty", "powder",
    "power", "practice", "praise", "predict", "prefer", "prepare", "present", "pretty", "prevent", "price",
    "pride", "primary", "print", "priority", "prison", "private", "prize", "problem", "process", "produce",
    "profit", "program", "project", "promote", "proof", "property", "promote", "protect", "proud", "provide",
    "public", "pudding", "pull", "pulp", "pulse", "pumpkin", "punch", "pupil", "puppy", "purchase", "purity",
    "purpose", "purse", "push", "put", "puzzle", "pyramid", "quality", "quantum", "quarter", "question",
    "quick", "quit", "quiz", "quote", "rabbit", "raccoon", "race", "rack", "radar", "radio", "rail", "rain",
    "raise", "rally", "ramp", "ranch", "random", "range", "rapid", "rare", "rate", "rather", "raven", "raw",
    "razor", "ready", "real", "reason", "rebel", "rebuild", "recall", "receive", "recipe", "record", "recycle",
    "reduce", "reflect", "reform", "refuse", "region", "regret", "regular", "reject", "relax", "release",
    "relief", "rely", "remain", "remember", "remind", "remove", "render", "renew", "rent", "reopen", "repair",
    "repeat", "replace", "report", "require", "rescue", "resemble", "resist", "resource", "response", "result",
    "retire", "retreat", "return", "reunion", "reveal", "review", "reward", "rhythm", "rib", "ribbon", "rice",
    "rich", "ride", "ridge", "rifle", "right", "rigid", "ring", "riot", "ripple", "risk", "ritual", "rival",
    "river", "road", "roast", "robot", "robust", "rocket", "romance", "roof", "rookie", "room", "rose", "rotate",
    "rough", "round", "route", "royal", "rubber", "rude", "rug", "rule", "run", "runway", "rural", "sad", "saddle",
    "sadness", "safe", "sail", "salad", "salmon", "salon", "salt", "salute", "same", "sample", "sand", "satisfy",
    "satoshi", "sauce", "sausage", "save", "say", "scale", "scan", "scare", "scatter", "scene", "scheme", "school",
    "science", "scissors", "scorpion", "scout", "scrap", "screen", "script", "scrub", "sea", "search", "season",
    "seat", "second", "secret", "section", "security", "seed", "seek", "segment", "select", "sell", "seminar",
    "senior", "sense", "sentence", "series", "service", "session", "settle", "setup", "seven", "shadow", "shaft",
    "shallow", "share", "shed", "shell", "sheriff", "shield", "shift", "shine", "ship", "shiver", "shock", "shoe",
    "shoot", "shop", "short", "shoulder", "shove", "shrimp", "shrug", "shuffle", "shut", "shy", "sibling", "sick",
    "side", "siege", "sight", "sign", "silent", "silk", "silly", "silver", "similar", "simple", "since", "sing",
    "siren", "sister", "situate", "six", "size", "skate", "sketch", "ski", "skill", "skull", "slab", "slam",
    "sleep", "slender", "slice", "slide", "slight", "slim", "slogan", "slot", "slow", "slush", "small", "smart",
    "smile", "smoke", "smooth", "snack", "snake", "snap", "sniff", "snow", "soap", "soccer", "social", "sock",
    "soda", "soft", "solar", "soldier", "solid", "solution", "solve", "someone", "song", "soon", "sorry", "sort",
    "soul", "sound", "soup", "source", "south", "space", "spare", "spatial", "spawn", "speak", "special", "speed",
    "spell", "spend", "sphere", "spice", "spider", "spike", "spin", "spirit", "split", "spoil", "sponsor", "spoon",
    "sport", "spot", "spray", "spread", "spring", "spy", "square", "squeeze", "squirrel", "stable", "stadium",
    "staff", "stage", "stairs", "stamp", "stand", "start", "state", "stay", "steak", "steel", "stem", "step",
    "stereo", "stick", "still", "sting", "stock", "stomach", "stone", "stool", "story", "stove", "strategy",
    "street", "strike", "strong", "struggle", "student", "stuff", "stumble", "style", "subject", "submit",
    "subway", "success", "such", "sudden", "suffer", "sugar", "suggest", "suit", "summer", "sun", "sunny", "sunset",
    "super", "supply", "supreme", "sure", "surface", "surge", "surprise", "surround", "survey", "suspect", "sustain",
    "swallow", "swamp", "swap", "swarm", "swear", "sweet", "swift", "swim", "swing", "switch", "sword", "symbol",
    "symptom", "syrup", "system", "table", "tackle", "tag", "tail", "talent", "talk", "tank", "tape", "target",
    "task", "taste", "tattoo", "taxi", "teach", "team", "tell", "ten", "tenant", "tennis", "tent", "term", "test",
    "text", "thank", "that", "theme", "then", "theory", "there", "they", "thing", "this", "thought", "three",
    "thrive", "throw", "thumb", "thunder", "ticket", "tide", "tiger", "tilt", "timber", "time", "tiny", "tip", "tired",
    "tissue", "title", "toast", "tobacco", "today", "toddler", "toe", "together", "toilet", "token", "tomato",
    "tomorrow", "tone", "tongue", "tonight", "tool", "tooth", "top", "topic", "topple", "torch", "tornado", "tortoise",
    "toss", "total", "tourist", "toward", "tower", "town", "toy", "track", "trade", "traffic", "tragic", "train",
    "transfer", "trap", "trash", "travel", "tray", "treat", "tree", "trend", "trial", "tribe", "trick", "trigger",
    "trim", "trip", "trophy", "trouble", "truck", "true", "truly", "trumpet", "trust", "truth", "try", "tube", "tuition",
    "tumble", "tuna", "tunnel", "turkey", "turn", "turtle", "twelve", "twenty", "twice", "twin", "twist", "two", "type",
    "typical", "ugly", "umbrella", "unable", "unaware", "uncle", "under", "unfair", "undo", "unhappy", "uniform",
    "unique", "unit", "universe", "unknown", "unlock", "until", "unusual", "unveil", "update", "upgrade", "uphold",
    "upon", "upper", "upset", "urban", "urge", "usage", "use", "used", "useful", "useless", "usual", "utility",
    "vacant", "vacuum", "vague", "valid", "valley", "valve", "van", "vanish", "vapor", "various", "vast", "vault",
    "vehicle", "velvet", "vendor", "venture", "venue", "verb", "verify", "version", "very", "vessel", "veteran",
    "viable", "vibrant", "vicious", "victory", "video", "view", "village", "vintage", "violin", "virtual", "virus",
    "visa", "visit", "visual", "vital", "vivid", "vocal", "voice", "void", "volcano", "volume", "vote", "voyage",
    "wage", "wagon", "wait", "walk", "wall", "walnut", "want", "warfare", "warm", "warrior", "wash", "wasp", "waste",
    "water", "wave", "way", "wealth", "weapon", "wear", "weasel", "weather", "web", "wedding", "weekend", "weird",
    "welcome", "west", "wet", "whale", "what", "wheat", "wheel", "when", "where", "whip", "whisper", "wide", "width",
    "wife", "wild", "will", "win", "window", "wine", "wing", "wink", "winner", "winter", "wire", "wisdom", "wise",
    "wish", "witness", "wolf", "woman", "wonder", "wood", "wool", "word", "work", "world", "worry", "worth", "wrap",
    "wreck", "wrestle", "wrist", "write", "wrong", "yard", "year", "yellow", "you", "young", "youth", "zebra", "zero",
    "zone", "zoo",
]


@dataclass
class PassphraseResult:
    """密码短语结果"""
    passphrase: str
    words: List[str]
    entropy_bits: float
    separator: str
    word_count: int
    wordlist_name: str


class PassphraseGenerator:
    """
    密码短语生成器
    
    生成安全且易于记忆的密码短语，支持多种配置选项。
    
    示例:
        >>> gen = PassphraseGenerator()
        >>> result = gen.generate(4)
        >>> print(result.passphrase)
        'correct-horse-battery-staple'
    """
    
    def __init__(
        self,
        wordlist: Optional[List[str]] = None,
        wordlist_name: str = "builtin"
    ):
        """
        初始化生成器
        
        Args:
            wordlist: 自定义单词列表，如果为 None 则使用内置列表
            wordlist_name: 单词列表名称，用于标识
        """
        self.wordlist = wordlist if wordlist is not None else BUILTIN_WORDLIST
        self.wordlist_name = wordlist_name if wordlist is not None else "builtin"
        self._validate_wordlist()
    
    def _validate_wordlist(self) -> None:
        """验证单词列表"""
        if not self.wordlist:
            raise ValueError("单词列表不能为空")
        if len(self.wordlist) < 10:
            raise ValueError(f"单词列表太少（{len(self.wordlist)}），建议至少 10 个单词")
        if len(self.wordlist) < 100:
            import warnings
            warnings.warn(f"单词列表较少（{len(self.wordlist)}），建议至少 100 个单词以确保足够的安全性")
    
    def _get_separator(self, separator: Separator) -> str:
        """获取分隔符"""
        if separator == Separator.RANDOM:
            separators = [" ", "-", "_", ".", ""]
            return secrets.choice(separators)
        return separator.value
    
    def _transform_word(
        self,
        word: str,
        word_case: WordCase,
        index: int
    ) -> str:
        """转换单词大小写"""
        if word_case == WordCase.LOWER:
            return word.lower()
        elif word_case == WordCase.UPPER:
            return word.upper()
        elif word_case == WordCase.CAPITALIZE:
            return word.capitalize()
        elif word_case == WordCase.RANDOM:
            if secrets.randbelow(2) == 0:
                return word.capitalize()
            return word.lower()
        elif word_case == WordCase.ALTERNATE:
            if index % 2 == 0:
                return word.capitalize()
            return word.lower()
        return word
    
    def generate(
        self,
        word_count: int = 4,
        separator: Separator = Separator.HYPHEN,
        word_case: WordCase = WordCase.LOWER,
        min_word_length: int = 3,
        max_word_length: int = 10,
        include_numbers: bool = False,
        include_special: bool = False,
        special_chars: str = "!@#$%^&*"
    ) -> PassphraseResult:
        """
        生成密码短语
        
        Args:
            word_count: 单词数量（建议 4-7 个）
            separator: 分隔符类型
            word_case: 单词大小写
            min_word_length: 最小单词长度
            max_word_length: 最大单词长度
            include_numbers: 是否在末尾添加随机数字
            include_special: 是否在末尾添加特殊字符
            special_chars: 可选的特殊字符
            
        Returns:
            PassphraseResult: 包含密码短语及元数据的结果对象
        """
        if word_count < 1:
            raise ValueError("单词数量必须至少为 1")
        if word_count > 20:
            raise ValueError("单词数量不能超过 20")
        
        # 过滤符合长度要求的单词
        valid_words = [
            w for w in self.wordlist
            if min_word_length <= len(w) <= max_word_length
        ]
        
        if len(valid_words) < word_count:
            valid_words = self.wordlist
        
        # 随机选择单词（使用 secrets 模块确保安全性）
        selected_words = []
        for i in range(word_count):
            word = secrets.choice(valid_words)
            word = self._transform_word(word, word_case, i)
            selected_words.append(word)
        
        # 获取分隔符
        sep = self._get_separator(separator)
        
        # 组合密码短语
        passphrase = sep.join(selected_words)
        
        # 添加数字
        if include_numbers:
            number = secrets.randbelow(10000)
            passphrase = f"{passphrase}{number}"
        
        # 添加特殊字符
        if include_special:
            special = secrets.choice(special_chars)
            passphrase = f"{passphrase}{special}"
        
        # 计算熵值
        entropy = self.calculate_entropy(word_count, len(valid_words))
        
        return PassphraseResult(
            passphrase=passphrase,
            words=selected_words,
            entropy_bits=entropy,
            separator=sep,
            word_count=word_count,
            wordlist_name=self.wordlist_name
        )
    
    def calculate_entropy(
        self,
        word_count: int,
        wordlist_size: Optional[int] = None
    ) -> float:
        """
        计算密码短语的熵值（比特）
        
        熵值表示密码的不确定性，值越大越安全。
        一般建议熵值不低于 50 比特，高安全性场景建议 70+ 比特。
        
        Args:
            word_count: 单词数量
            wordlist_size: 单词列表大小，默认使用当前列表
            
        Returns:
            float: 熵值（比特）
        """
        if wordlist_size is None:
            wordlist_size = len(self.wordlist)
        
        # 熵值 = word_count * log2(wordlist_size)
        entropy = word_count * math.log2(wordlist_size)
        return round(entropy, 2)
    
    def generate_multiple(
        self,
        count: int = 5,
        **kwargs
    ) -> List[PassphraseResult]:
        """
        生成多个密码短语
        
        Args:
            count: 生成数量
            **kwargs: 传递给 generate() 的参数
            
        Returns:
            List[PassphraseResult]: 密码短语列表
        """
        if count < 1 or count > 100:
            raise ValueError("生成数量必须在 1-100 之间")
        
        return [self.generate(**kwargs) for _ in range(count)]
    
    def estimate_crack_time(
        self,
        entropy_bits: float,
        guesses_per_second: float = 1e12
    ) -> str:
        """
        估算破解所需时间
        
        Args:
            entropy_bits: 密码熵值
            guesses_per_second: 每秒猜测次数（默认 1 万亿次）
            
        Returns:
            str: 可读的时间估计
        """
        # 总猜测次数 = 2^entropy
        total_guesses = 2 ** entropy_bits
        
        # 平均猜测次数（假设均匀分布）
        avg_guesses = total_guesses / 2
        
        # 所需秒数
        seconds = avg_guesses / guesses_per_second
        
        # 转换为可读格式
        if seconds < 1:
            return "瞬间"
        elif seconds < 60:
            return f"{seconds:.1f} 秒"
        elif seconds < 3600:
            return f"{seconds / 60:.1f} 分钟"
        elif seconds < 86400:
            return f"{seconds / 3600:.1f} 小时"
        elif seconds < 31536000:
            return f"{seconds / 86400:.1f} 天"
        elif seconds < 31536000 * 100:
            return f"{seconds / 31536000:.1f} 年"
        elif seconds < 31536000 * 1000000:
            return f"{seconds / 31536000:.0f} 年"
        else:
            return "数十亿年以上"
    
    def analyze_passphrase(self, passphrase: str) -> dict:
        """
        分析密码短语的强度
        
        Args:
            passphrase: 要分析的密码短语
            
        Returns:
            dict: 分析结果
        """
        # 尝试识别分隔符
        possible_seps = [' ', '-', '_', '.', '']
        words = []
        detected_sep = None
        
        for sep in possible_seps:
            parts = passphrase.split(sep) if sep else list(passphrase)
            # 检查是否在单词列表中
            matches = sum(1 for p in parts if p.lower() in [w.lower() for w in self.wordlist])
            if matches > len(parts) / 2:
                words = parts
                detected_sep = sep
                break
        
        word_count = len(words)
        
        # 计算熵值估计
        if word_count > 1:
            entropy = self.calculate_entropy(word_count)
        else:
            # 单个词或未知格式，使用字符熵估计
            entropy = len(passphrase) * math.log2(62)  # 假设字母数字
        
        # 检查是否包含数字
        has_number = any(c.isdigit() for c in passphrase)
        
        # 检查是否包含特殊字符
        has_special = any(not c.isalnum() for c in passphrase)
        
        # 评估强度
        if entropy < 28:
            strength = "非常弱"
        elif entropy < 36:
            strength = "弱"
        elif entropy < 60:
            strength = "中等"
        elif entropy < 80:
            strength = "强"
        else:
            strength = "非常强"
        
        return {
            "passphrase": passphrase,
            "word_count": word_count,
            "words": words if words else [passphrase],
            "separator": detected_sep,
            "entropy_bits": round(entropy, 2),
            "has_number": has_number,
            "has_special": has_special,
            "strength": strength,
            "estimated_crack_time": self.estimate_crack_time(entropy)
        }


def generate_passphrase(
    word_count: int = 4,
    separator: str = "-",
    wordlist: Optional[List[str]] = None
) -> str:
    """
    快捷函数：生成密码短语
    
    Args:
        word_count: 单词数量
        separator: 分隔符字符串
        wordlist: 自定义单词列表
        
    Returns:
        str: 生成的密码短语
    """
    sep_map = {
        " ": Separator.SPACE,
        "-": Separator.HYPHEN,
        "_": Separator.UNDERSCORE,
        ".": Separator.DOT,
        "": Separator.NONE
    }
    sep = sep_map.get(separator, Separator.HYPHEN)
    
    gen = PassphraseGenerator(wordlist=wordlist)
    result = gen.generate(word_count=word_count, separator=sep)
    return result.passphrase


def generate_diceware(
    word_count: int = 5,
    separator: str = " "
) -> str:
    """
    使用 Diceware 方法生成密码短语
    
    Diceware 是一种使用骰子生成密码短语的方法，每个单词由 5 次骰子投掷决定。
    这提供了高质量的随机性和安全性。
    
    Args:
        word_count: 单词数量（建议 5-7 个）
        separator: 分隔符
        
    Returns:
        str: Diceware 密码短语
    """
    sep_map = {
        " ": Separator.SPACE,
        "-": Separator.HYPHEN,
        "_": Separator.UNDERSCORE,
        ".": Separator.DOT,
        "": Separator.NONE
    }
    sep = sep_map.get(separator, Separator.SPACE)
    
    gen = PassphraseGenerator(wordlist=DICETIME_WORDLIST, wordlist_name="diceware")
    result = gen.generate(word_count=word_count, separator=sep)
    return result.passphrase


def passphrase_strength(passphrase: str) -> dict:
    """
    快捷函数：分析密码短语强度
    
    Args:
        passphrase: 要分析的密码短语
        
    Returns:
        dict: 强度分析结果
    """
    gen = PassphraseGenerator()
    return gen.analyze_passphrase(passphrase)


if __name__ == "__main__":
    # 演示用法
    print("=== 密码短语生成器演示 ===\n")
    
    gen = PassphraseGenerator()
    
    # 生成标准密码短语
    print("1. 标准密码短语（4 个单词）：")
    result = gen.generate(4)
    print(f"   {result.passphrase}")
    print(f"   熵值: {result.entropy_bits} 比特")
    print(f"   单词: {result.words}\n")
    
    # 生成带增强的密码短语
    print("2. 增强密码短语（带数字和特殊字符）：")
    result = gen.generate(
        word_count=4,
        separator=Separator.HYPHEN,
        include_numbers=True,
        include_special=True
    )
    print(f"   {result.passphrase}")
    print(f"   熵值: {result.entropy_bits} 比特\n")
    
    # Diceware 风格
    print("3. Diceware 风格（5 个单词，空格分隔）：")
    result = gen.generate(5, Separator.SPACE)
    print(f"   {result.passphrase}")
    print(f"   预估破解时间: {gen.estimate_crack_time(result.entropy_bits)}\n")
    
    # 多个密码短语
    print("4. 生成 5 个候选：")
    results = gen.generate_multiple(5)
    for i, r in enumerate(results, 1):
        print(f"   {i}. {r.passphrase} ({r.entropy_bits} bits)")
    
    print("\n=== 熵值参考 ===")
    print("   < 28 bits: 非常弱，瞬间可破")
    print("   28-35 bits: 弱，几分钟到几小时")
    print("   36-59 bits: 中等，数天到数年")
    print("   60-79 bits: 强，数年到数百年")
    print("   >= 80 bits: 非常强，实际上不可破")