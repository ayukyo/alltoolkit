"""
word_ladder_utils - Word Ladder Puzzle Utilities

A lightweight utility for word ladder puzzles (also known as "Doublets" or "Word Golf").
Transform one word into another by changing one letter at a time.

Features:
- Find shortest word ladder path between two words
- Generate word ladder puzzles
- Validate word ladder solutions
- Find all possible one-letter transformations
- Built-in word dictionary for common word lengths
- Support for custom word lists

Zero external dependencies - uses only Python standard library.

Author: AllToolkit Auto-Generator
Date: 2026-05-20
"""

from typing import List, Dict, Set, Optional, Tuple
from collections import deque


# Built-in English word dictionary (common words, 3-6 letters)
# These are curated common English words for word ladder puzzles
BUILTIN_WORDS: Dict[int, Set[str]] = {
    3: {
        "ace", "act", "add", "age", "ago", "aid", "aim", "air", "all", "and",
        "ant", "any", "ape", "arc", "are", "ark", "arm", "art", "ask", "ate",
        "bad", "bag", "ban", "bar", "bat", "bay", "bed", "bee", "beg", "bet",
        "bid", "big", "bin", "bit", "bow", "box", "boy", "bud", "bug", "bus",
        "but", "buy", "cab", "can", "cap", "car", "cat", "cob", "cod", "cog",
        "cop", "cot", "cow", "cry", "cub", "cup", "cut", "dad", "dam", "day",
        "den", "dew", "did", "die", "dig", "dim", "dip", "dog", "dot", "dry",
        "dub", "dud", "due", "dug", "dye", "ear", "eat", "eel", "egg", "elf",
        "elk", "elm", "end", "era", "eve", "eye", "fan", "far", "fat", "fax",
        "fed", "fee", "few", "fig", "fin", "fir", "fit", "fix", "fly", "foe",
        "fog", "for", "fox", "fry", "fun", "fur", "gag", "gap", "gas", "gay",
        "gel", "gem", "get", "gig", "gin", "god", "got", "gum", "gun", "gut",
        "guy", "gym", "had", "ham", "has", "hat", "hay", "hem", "hen", "her",
        "hid", "him", "hip", "his", "hit", "hog", "hop", "hot", "how", "hub",
        "hug", "hum", "hut", "ice", "icy", "ill", "imp", "ink", "inn", "ion",
        "its", "ivy", "jab", "jam", "jar", "jaw", "jay", "jet", "jig", "job",
        "jog", "joy", "jug", "key", "kid", "kin", "kit", "lab", "lad", "lag",
        "lap", "law", "lay", "led", "leg", "let", "lid", "lie", "lip", "lit",
        "log", "lot", "low", "mad", "man", "map", "mar", "mat", "may", "men",
        "met", "mid", "mix", "mob", "mod", "mom", "mop", "mud", "mug", "nag",
        "nap", "net", "new", "nil", "nip", "nod", "nor", "not", "now", "nut",
        "oak", "oar", "oat", "odd", "off", "oil", "old", "one", "opt", "orb",
        "ore", "our", "out", "owe", "owl", "own", "pad", "pal", "pan", "pat",
        "paw", "pay", "pea", "peg", "pen", "per", "pet", "pie", "pig", "pin",
        "pit", "ply", "pod", "pop", "pot", "pro", "pub", "pun", "pup", "put",
        "rag", "ram", "ran", "rap", "rat", "raw", "ray", "red", "ref", "rib",
        "rid", "rig", "rim", "rip", "rob", "rod", "rot", "row", "rub", "rug",
        "run", "rut", "sad", "sag", "sat", "saw", "say", "sea", "set", "sew",
        "she", "shy", "sin", "sip", "sir", "sit", "six", "ski", "sky", "sly",
        "sob", "sod", "son", "sow", "soy", "spa", "spy", "sub", "sue", "sum",
        "sun", "tab", "tag", "tan", "tap", "tar", "tax", "tea", "ten", "the",
        "thy", "tie", "tin", "tip", "toe", "ton", "too", "top", "tow", "toy",
        "try", "tub", "tug", "two", "urn", "use", "van", "vat", "vet", "via",
        "vow", "wad", "wag", "war", "was", "wax", "way", "web", "wed", "wet",
        "who", "why", "wig", "win", "wit", "woe", "wok", "won", "woo", "wow",
        "yak", "yam", "yap", "yaw", "yea", "yes", "yet", "yew", "you", "zap",
        "zed", "zen", "zip", "zoo"
    },
    4: {
        "able", "ache", "acid", "aged", "aide", "ally", "also", "amid", "arch",
        "area", "army", "aunt", "auto", "away", "baby", "back", "bait", "bake",
        "bald", "ball", "band", "bank", "bare", "bark", "barn", "base", "bath",
        "bead", "beak", "beam", "bean", "bear", "beat", "been", "beer", "bell",
        "belt", "bend", "bent", "best", "bike", "bill", "bind", "bird", "bite",
        "blow", "blue", "boat", "body", "boil", "bold", "bolt", "bomb", "bond",
        "bone", "book", "boom", "boot", "bore", "born", "boss", "both", "bowl",
        "brag", "bran", "bred", "brew", "buck", "bulk", "bull", "bump", "burn",
        "bury", "bush", "busy", "cafe", "cage", "cake", "calf", "call", "calm",
        "came", "camp", "card", "care", "carp", "cart", "case", "cash", "cast",
        "cave", "cell", "chat", "chef", "chin", "chip", "chop", "city", "clam",
        "clap", "clay", "clip", "club", "clue", "coal", "coat", "code", "coin",
        "cold", "colt", "comb", "come", "cook", "cool", "cope", "copy", "cord",
        "core", "corn", "cost", "cozy", "crab", "crew", "crop", "crow", "cure",
        "cute", "dame", "damp", "dare", "dark", "dart", "dash", "data", "date",
        "dawn", "dead", "deal", "dean", "dear", "debt", "deck", "deed", "deem",
        "deep", "deer", "demo", "deny", "desk", "dial", "dice", "died", "diet",
        "dime", "dine", "dirt", "disc", "dish", "disk", "dive", "dock", "does",
        "doll", "dome", "done", "doom", "door", "dose", "down", "drag", "draw",
        "drew", "drip", "drop", "drum", "dual", "duck", "dude", "duke", "dull",
        "dump", "dune", "dunk", "dust", "duty", "each", "earn", "ease", "east",
        "easy", "eats", "echo", "edge", "edit", "else", "emit", "envy", "epic",
        "euro", "even", "ever", "evil", "exam", "exit", "face", "fact", "fade",
        "fail", "fair", "fake", "fall", "fame", "fare", "farm", "fast", "fate",
        "fear", "feat", "feed", "feel", "fell", "felt", "file", "fill", "film",
        "find", "fine", "fire", "firm", "fish", "fist", "five", "flag", "flame",
        "flap", "flat", "flaw", "fled", "flee", "flew", "flip", "flow", "foam",
        "fold", "folk", "food", "fool", "foot", "ford", "fore", "fork", "form",
        "fort", "foul", "four", "free", "from", "fuel", "full", "fund", "gain",
        "gale", "game", "gang", "gate", "gave", "gaze", "gear", "gene", "gift",
        "girl", "give", "glad", "glow", "glue", "goal", "goat", "goes", "gold",
        "golf", "gone", "good", "gown", "grab", "gram", "gray", "grew", "grey",
        "grid", "grim", "grin", "grip", "grow", "gulf", "gust", "guts", "hack",
        "hail", "hair", "half", "hall", "halt", "hand", "hang", "hard", "hare",
        "harm", "hate", "haul", "have", "hawk", "haze", "hazy", "head", "heal",
        "heap", "hear", "heat", "heel", "held", "hell", "help", "herb", "herd",
        "here", "hero", "hide", "high", "hike", "hill", "hint", "hire", "hold",
        "hole", "holy", "home", "hook", "hope", "horn", "hose", "host", "hour",
        "huge", "hull", "hung", "hunt", "hurt", "hype", "idea", "inch", "into",
        "iron", "isle", "item", "jack", "jade", "jail", "jazz", "jean", "jeans",
        "jerk", "jest", "jobs", "join", "joke", "jolt", "josh", "jump", "june",
        "junk", "jury", "just", "keen", "keep", "kept", "kick", "kill", "kind",
        "king", "kiss", "kite", "knee", "knew", "knit", "knob", "knot", "know",
        "lace", "lack", "lady", "laid", "lake", "lamb", "lame", "lamp", "land",
        "lane", "lard", "last", "late", "lawn", "lead", "leaf", "leak", "lean",
        "leap", "left", "lend", "lens", "less", "liar", "lice", "lick", "life",
        "lift", "like", "limb", "lime", "limp", "line", "link", "lion", "list",
        "live", "load", "loaf", "loan", "lock", "loft", "logo", "lone", "long",
        "look", "loop", "lord", "lose", "loss", "lost", "loud", "love", "luck",
        "lump", "lung", "lure", "lurk", "made", "mail", "main", "make", "male",
        "mall", "malt", "many", "mark", "mars", "mart", "mask", "mass", "mate",
        "math", "maze", "meal", "mean", "meat", "meet", "melt", "memo", "mend",
        "menu", "mere", "mesh", "mess", "mice", "mild", "mile", "milk", "mill",
        "mind", "mine", "mint", "miss", "mist", "mode", "mold", "mole", "molt",
        "monk", "mood", "moon", "moor", "more", "morn", "moss", "most", "moth",
        "move", "much", "mule", "must", "mute", "myth", "nail", "name", "navy",
        "near", "neat", "neck", "need", "nest", "news", "next", "nice", "nine",
        "node", "none", "noon", "norm", "nose", "note", "noun", "nude", "nut",
        "odds", "okay", "once", "ones", "only", "onto", "open", "oral", "oven",
        "over", "owed", "pace", "pack", "page", "paid", "pain", "pair", "pale",
        "palm", "pane", "pant", "park", "part", "pass", "past", "path", "pave",
        "peak", "pear", "peas", "peel", "peer", "pest", "pick", "pier", "pike",
        "pile", "pill", "pine", "pink", "pipe", "pity", "plan", "play", "plea",
        "plot", "plow", "plug", "plum", "plus", "poem", "poet", "pole", "poll",
        "pond", "pool", "poor", "pope", "pork", "port", "pose", "post", "pour",
        "pray", "prep", "prey", "prop", "puff", "pull", "pump", "pure", "push",
        "quit", "race", "rack", "rage", "raid", "rail", "rain", "rank", "rare",
        "rate", "rave", "read", "real", "reap", "rear", "reed", "reef", "reel",
        "rely", "rent", "rest", "rice", "rich", "ride", "ring", "riot", "rise",
        "risk", "road", "roam", "roar", "robe", "rock", "rode", "role", "roll",
        "roof", "room", "root", "rope", "rose", "rosy", "ruin", "rule", "rung",
        "runt", "rush", "rust", "sack", "safe", "sage", "said", "sail", "sake",
        "sale", "salt", "same", "sand", "sane", "sang", "sank", "save", "scan",
        "seal", "seam", "sear", "seat", "seed", "seek", "seem", "seen", "self",
        "sell", "send", "sent", "shed", "ship", "shop", "shot", "show", "shut",
        "sick", "side", "sigh", "sign", "silk", "sing", "sink", "site", "size",
        "skin", "skip", "slam", "slap", "slat", "slay", "sled", "slew", "slid",
        "slim", "slip", "slit", "slot", "slow", "snap", "snow", "soak", "soap",
        "soar", "sock", "soda", "sofa", "soft", "soil", "sold", "sole", "some",
        "song", "soon", "sore", "sort", "soul", "soup", "sour", "span", "spar",
        "spec", "spin", "spit", "spot", "stab", "star", "stay", "stem", "step",
        "stew", "stir", "stop", "such", "suck", "suit", "sung", "sunk", "sure",
        "surf", "swap", "swim", "tail", "take", "tale", "talk", "tall", "tank",
        "tape", "task", "team", "tear", "teas", "tech", "teen", "tell", "temp",
        "tend", "tent", "term", "test", "text", "than", "that", "them", "then",
        "they", "thin", "this", "thou", "tide", "tidy", "tied", "tier", "tile",
        "till", "tilt", "time", "tiny", "tire", "toad", "toes", "told", "toll",
        "tomb", "tone", "took", "tool", "tops", "tore", "torn", "toss", "tour",
        "town", "trap", "tray", "tree", "trim", "trio", "trip", "trot", "true",
        "tube", "tuck", "tune", "turn", "twin", "type", "ugly", "unit", "upon",
        "urge", "used", "user", "vain", "vase", "vast", "verb", "very", "vest",
        "vice", "view", "vine", "visa", "void", "volt", "vote", "wade", "wage",
        "wail", "wait", "wake", "walk", "wall", "want", "ward", "warm", "warn",
        "warp", "wary", "wash", "wasp", "wave", "wavy", "waxy", "weak", "wear",
        "weed", "week", "weep", "well", "went", "were", "west", "what", "when",
        "whip", "whom", "wide", "wife", "wild", "will", "wind", "wine", "wing",
        "wink", "wipe", "wire", "wise", "wish", "with", "woke", "wolf", "womb",
        "wood", "wool", "word", "wore", "work", "worm", "worn", "wrap", "yard",
        "yarn", "yeah", "year", "yell", "yoga", "your", "zero", "zone", "zoom"
    },
    5: {
        "about", "above", "abuse", "actor", "acute", "admit", "adopt", "adult",
        "after", "again", "agent", "agree", "ahead", "alarm", "album", "alert",
        "alien", "align", "alike", "alive", "alley", "allow", "alone", "along",
        "alter", "amuse", "angel", "anger", "angle", "angry", "apart", "apple",
        "apply", "arena", "argue", "arise", "armor", "array", "arrow", "aside",
        "asset", "avoid", "award", "aware", "awful", "bacon", "badge", "badly",
        "baker", "basic", "basin", "basis", "batch", "beach", "beard", "beast",
        "begin", "being", "belly", "below", "bench", "berry", "birth", "black",
        "blade", "blame", "blank", "blast", "blaze", "bleed", "blend", "bless",
        "blind", "block", "blood", "bloom", "blown", "board", "boast", "bonus",
        "boost", "booth", "bound", "brain", "brake", "brand", "brass", "brave",
        "bread", "break", "breed", "brick", "bride", "brief", "bring", "broad",
        "broke", "brook", "brown", "brush", "build", "built", "bunch", "burst",
        "buyer", "cabin", "cable", "camel", "candy", "cargo", "carry", "catch",
        "cause", "cease", "chain", "chair", "chaos", "charm", "chart", "chase",
        "cheap", "cheat", "check", "cheek", "cheer", "chess", "chest", "chief",
        "child", "chill", "china", "choir", "chord", "chunk", "cigar", "civil",
        "claim", "clash", "class", "clean", "clear", "clerk", "click", "cliff",
        "climb", "cling", "clock", "close", "cloth", "cloud", "coach", "coast",
        "colon", "color", "couch", "cough", "could", "count", "court", "cover",
        "crack", "craft", "crash", "crawl", "crazy", "cream", "creek", "creep",
        "crisp", "cross", "crowd", "crown", "crude", "cruel", "crush", "curve",
        "cycle", "daily", "dairy", "dance", "death", "debut", "decay", "decor",
        "delay", "delta", "dense", "depth", "derby", "deter", "devil", "diary",
        "digit", "dirty", "disco", "ditch", "dodge", "donor", "doubt", "dough",
        "dozen", "draft", "drain", "drake", "drama", "drank", "drawn", "dread",
        "dream", "dress", "dried", "drift", "drill", "drink", "drive", "drown",
        "drunk", "dying", "eager", "eagle", "early", "earth", "eight", "elder",
        "elect", "elite", "empty", "enemy", "enjoy", "enter", "entry", "equal",
        "equip", "error", "essay", "event", "every", "exact", "exist", "extra",
        "faint", "fairy", "faith", "false", "fancy", "fatal", "fault", "favor",
        "feast", "fence", "ferry", "fetch", "fever", "fewer", "fiber", "field",
        "fifth", "fifty", "fight", "final", "first", "fixed", "flame", "flash",
        "flask", "flesh", "float", "flock", "flood", "floor", "flour", "fluid",
        "flush", "focal", "focus", "force", "forge", "forth", "forty", "forum",
        "fossil", "found", "frame", "frank", "fraud", "freak", "fresh", "front",
        "frost", "fruit", "fudge", "fully", "funny", "fuzzy", "giant", "given",
        "glass", "globe", "glory", "glove", "goose", "grace", "grade", "grain",
        "grand", "grant", "grape", "graph", "grasp", "grass", "grave", "great",
        "greed", "green", "greet", "grief", "grill", "grind", "groan", "groom",
        "gross", "group", "grove", "grown", "guard", "guess", "guest", "guide",
        "guild", "guilt", "guise", "habit", "happy", "hardy", "harsh", "haste",
        "hasty", "hatch", "haven", "heard", "heart", "heath", "heavy", "hedge",
        "heist", "hello", "hence", "hinge", "hobby", "hoist", "honey", "honor",
        "horse", "hotel", "hound", "house", "human", "humid", "humor", "hurry",
        "ideal", "image", "imply", "index", "inner", "input", "irony", "issue",
        "ivory", "jeans", "jewel", "joint", "joker", "jolly", "judge", "juice",
        "jumbo", "jumpy", "junky", "karma", "kayak", "khaki", "kiosk", "knife",
        "knock", "known", "label", "labor", "lance", "large", "laser", "latch",
        "later", "laugh", "layer", "learn", "lease", "least", "leave", "legal",
        "lemon", "level", "lever", "light", "limit", "linen", "liner", "liver",
        "lobby", "local", "lodge", "lofty", "logic", "loose", "lorry", "loser",
        "lotus", "loved", "lover", "lower", "loyal", "lucky", "lunar", "lunch",
        "lying", "magic", "major", "maker", "manor", "maple", "march", "marsh",
        "match", "mayor", "medal", "media", "melon", "mercy", "merge", "merit",
        "merry", "metal", "meter", "might", "milky", "mimic", "mince", "minor",
        "minus", "mirth", "misty", "mixed", "mixer", "model", "modem", "money",
        "month", "moose", "moral", "motor", "motto", "mount", "mouse", "mouth",
        "moved", "mover", "movie", "music", "naked", "nasty", "naval", "nerve",
        "never", "newly", "night", "ninth", "noble", "noise", "north", "notch",
        "noted", "novel", "nurse", "nylon", "occur", "ocean", "offer", "often",
        "olive", "onion", "opera", "orbit", "order", "organ", "other", "ought",
        "ounce", "outer", "outdo", "outgo", "owned", "owner", "oxide", "ozone",
        "paint", "panda", "panel", "panic", "paper", "party", "pasta", "paste",
        "patch", "pause", "peace", "peach", "pearl", "pedal", "penny", "perch",
        "peril", "petty", "phase", "phone", "photo", "piano", "piece", "pilot",
        "pinch", "pitch", "pizza", "place", "plain", "plane", "plant", "plate",
        "plaza", "plead", "pleat", "pluck", "plumb", "plump", "plunge", "poach",
        "point", "polar", "polio", "polka", "polyp", "porch", "poser", "pound",
        "power", "prank", "press", "price", "pride", "prime", "print", "prior",
        "prize", "probe", "prone", "proof", "proud", "prove", "prowl", "prune",
        "pulse", "punch", "pupil", "puppy", "purse", "pushy", "qualm", "quart",
        "quasi", "queen", "query", "quest", "quick", "quiet", "quilt", "quirk",
        "quota", "quote", "rabbi", "radar", "radio", "rainy", "raise", "rally",
        "ranch", "range", "rapid", "ratio", "razor", "reach", "react", "ready",
        "realm", "rebel", "refer", "reign", "relax", "relay", "remit", "remix",
        "renew", "repay", "reply", "reset", "resin", "retro", "rider", "ridge",
        "rifle", "right", "rigid", "rinse", "ripen", "risen", "risky", "rival",
        "river", "roast", "robin", "robot", "rocky", "roman", "roomy", "roots",
        "rough", "round", "route", "rover", "royal", "rugby", "ruler", "rumor",
        "rural", "rusty", "sadly", "saint", "salad", "salon", "sandy", "sauce",
        "sauna", "scale", "scare", "scene", "scent", "scope", "score", "scout",
        "scrap", "seize", "sense", "serum", "serve", "setup", "seven", "shade",
        "shaft", "shake", "shall", "shame", "shape", "share", "shark", "sharp",
        "sheep", "sheer", "sheet", "shelf", "shell", "shift", "shine", "shirt",
        "shock", "shoot", "shore", "short", "shout", "shove", "shown", "shrub",
        "siege", "sight", "sigma", "silky", "silly", "since", "sixth", "sixty",
        "skate", "skill", "skull", "slate", "slave", "sleek", "sleep", "slice",
        "slide", "slope", "sloth", "small", "smart", "smell", "smile", "smoke",
        "smoky", "snake", "sneak", "sniff", "sober", "solar", "solid", "solve",
        "sonic", "sorry", "sound", "south", "space", "spare", "spark", "speak",
        "spear", "speed", "spell", "spend", "spice", "spill", "spine", "spite",
        "split", "spoke", "spoon", "sport", "spray", "squad", "stack", "staff",
        "stage", "stain", "stair", "stake", "stale", "stamp", "stand", "stare",
        "stark", "start", "state", "steak", "steal", "steam", "steel", "steep",
        "steer", "stern", "stick", "stiff", "still", "sting", "stock", "stomp",
        "stone", "stood", "stool", "store", "storm", "story", "stout", "stove",
        "strap", "straw", "stray", "strip", "stuck", "study", "stuff", "style",
        "sugar", "suite", "sunny", "super", "surge", "swamp", "swear", "sweat",
        "sweep", "sweet", "swift", "swing", "sword", "swore", "sworn", "table",
        "taboo", "taken", "tally", "talon", "tango", "tangy", "tapir", "tardy",
        "taste", "tasty", "taunt", "teach", "teens", "tempo", "tense", "tenth",
        "tepid", "terms", "thank", "theft", "their", "theme", "there", "these",
        "thick", "thief", "thigh", "thing", "think", "third", "thorn", "those",
        "three", "threw", "throw", "thumb", "tiger", "tight", "title", "toast",
        "today", "token", "tonal", "topic", "torch", "total", "touch", "tough",
        "towel", "tower", "toxic", "trace", "track", "trade", "trail", "train",
        "trait", "tramp", "trash", "trawl", "tread", "treat", "trend", "trial",
        "tribe", "trick", "tried", "trout", "truce", "truck", "truly", "trump",
        "trunk", "trust", "truth", "tumor", "tuner", "tunic", "turbo", "tutor",
        "twang", "tweak", "tweed", "tweet", "twice", "twine", "twirl", "twist",
        "ulcer", "ultra", "uncle", "under", "undid", "unfit", "union", "unite",
        "unity", "until", "upper", "upset", "urban", "urged", "usher", "usual",
        "utter", "vague", "valid", "value", "valve", "vault", "vegas", "venom",
        "venue", "verge", "verse", "video", "vigor", "vinyl", "viola", "viper",
        "viral", "virus", "visor", "vista", "vital", "vivid", "vocal", "vodka",
        "vogue", "voice", "voter", "vouch", "vowel", "wafer", "wager", "wagon",
        "waist", "waltz", "waste", "watch", "water", "weary", "weave", "wedge",
        "weigh", "weird", "wheat", "wheel", "where", "which", "while", "whine",
        "white", "whole", "whose", "widen", "wider", "widow", "width", "wired",
        "witch", "witty", "woken", "woman", "women", "woods", "woody", "world",
        "worry", "worse", "worst", "worth", "would", "wound", "woven", "wrath",
        "wreck", "wrist", "write", "wrong", "wrote", "yacht", "yearn", "yeast",
        "yield", "young", "youth", "zebra", "zesty", "zonal"
    },
    6: {
        "abroad", "accept", "access", "accord", "across", "action", "active",
        "actual", "advice", "advise", "affair", "affect", "afford", "afraid",
        "agency", "agenda", "almost", "always", "amount", "animal", "annual",
        "answer", "anyone", "anyway", "appeal", "appear", "around", "arrive",
        "artist", "aspect", "assert", "assess", "assign", "assist", "assume",
        "attack", "attend", "autumn", "avenue", "backed", "backup", "banana",
        "banker", "barely", "barrel", "basket", "battle", "beauty", "became",
        "become", "before", "behalf", "behind", "belief", "belong", "better",
        "beyond", "bishop", "bitter", "blanket", "bottle", "bottom", "bought",
        "bounce", "branch", "breach", "breath", "bridge", "bright", "broken",
        "broker", "bronze", "bubble", "bucket", "budget", "buffer", "bullet",
        "bundle", "burden", "butter", "button", "camera", "campus", "cancer",
        "cannot", "canvas", "carbon", "career", "castle", "casual", "cattle",
        "caught", "center", "centre", "chance", "change", "charge", "choice",
        "choose", "church", "circle", "circus", "client", "closed", "closer",
        "closet", "coffee", "column", "combat", "comedy", "coming", "commit",
        "common", "comply", "copper", "corner", "costly", "cotton", "county",
        "couple", "course", "cousin", "create", "credit", "crisis", "custom",
        "damage", "danger", "dealer", "debate", "decade", "decent", "decide",
        "defeat", "defend", "define", "degree", "demand", "dental", "depend",
        "deploy", "deputy", "derive", "desert", "design", "desire", "detail",
        "detect", "device", "devote", "dialog", "diesel", "differ", "dinner",
        "direct", "doctor", "dollar", "domain", "donate", "double", "dozens",
        "drawer", "driven", "driver", "during", "easily", "eating", "editor",
        "effect", "effort", "either", "eleven", "emerge", "empire", "employ",
        "enable", "ending", "energy", "engage", "engine", "enough", "ensure",
        "entire", "entity", "equity", "escape", "estate", "ethnic", "evolve",
        "exceed", "except", "excuse", "expand", "expect", "expert", "export",
        "extend", "extent", "fabric", "factor", "fairly", "fallen", "family",
        "famous", "farmer", "father", "favour", "fellow", "female", "figure",
        "filing", "filter", "finder", "finger", "finish", "fiscal", "flight",
        "flower", "folder", "follow", "forced", "forest", "forget", "format",
        "former", "fossil", "foster", "fought", "fourth", "freely", "freeze",
        "french", "friend", "frozen", "future", "garden", "gather", "gender",
        "gentle", "german", "global", "golden", "gotten", "govern", "gravel",
        "greedy", "groove", "ground", "growth", "guilty", "guitar", "handle",
        "happen", "harbor", "hardly", "headed", "header", "health", "height",
        "helper", "hidden", "highly", "holder", "honest", "horror", "humour",
        "hunter", "ignore", "impact", "import", "impose", "income", "indeed",
        "infant", "inform", "injury", "insect", "inside", "insist", "intact",
        "intend", "intent", "invest", "island", "jacket", "jersey", "jingle",
        "junior", "keeper", "kernel", "killer", "knight", "launch", "lawyer",
        "layout", "leader", "league", "length", "lesson", "letter", "lights",
        "likely", "linear", "linked", "liquid", "listen", "litter", "little",
        "living", "locate", "locked", "lodge", "lonely", "longer", "looked",
        "luxury", "mainly", "manage", "manner", "manual", "marble", "margin",
        "marine", "market", "master", "matter", "mature", "medium", "member",
        "memory", "mental", "mentor", "merely", "merger", "method", "middle",
        "miller", "minded", "mining", "minute", "mirror", "mobile", "modern",
        "modest", "modify", "moment", "monkey", "mother", "motion", "motors",
        "mount", "museum", "mutual", "myself", "namely", "narrow", "nation",
        "native", "nature", "nearby", "nearly", "neatly", "needed", "nephew",
        "nested", "nights", "nobody", "normal", "notice", "notion", "number",
        "object", "obtain", "occupy", "officer", "office", "online", "opener",
        "oppose", "option", "orange", "origin", "output", "oxygen", "packed",
        "palace", "parent", "partly", "passed", "patent", "patron", "paused",
        "paying", "people", "period", "permit", "person", "phrase", "picked",
        "picnic", "pillow", "planet", "player", "please", "pledge", "plenty",
        "pocket", "poetry", "police", "policy", "polish", "portal", "postal",
        "poster", "potato", "potter", "powder", "prefer", "prince", "prison",
        "profit", "proper", "proven", "public", "purple", "pursue", "puzzle",
        "python", "rabbit", "racing", "random", "rarely", "rather", "rating",
        "reader", "really", "reason", "recall", "recent", "record", "reduce",
        "reform", "refuse", "regard", "region", "regret", "reject", "relate",
        "relief", "remain", "remark", "remedy", "remind", "remote", "remove",
        "render", "rental", "repair", "repeat", "report", "rescue", "resign",
        "resist", "resort", "result", "retail", "retain", "retire", "return",
        "reveal", "review", "reward", "ribbon", "riding", "rising", "ritual",
        "rocket", "roller", "rubber", "runner", "sacred", "safely", "safety",
        "sailor", "salary", "salmon", "sample", "saving", "scared", "scheme",
        "school", "screen", "script", "search", "season", "second", "secret",
        "sector", "secure", "seeing", "seemed", "senior", "serial", "series",
        "server", "settle", "severe", "shadow", "shaken", "shaped", "shared",
        "shield", "should", "shower", "signal", "signed", "silent", "silver",
        "simple", "simply", "single", "sister", "sketch", "slight", "smooth",
        "social", "sodium", "solely", "solved", "source", "sought", "speech",
        "sphere", "spider", "spirit", "splash", "spoken", "spread", "spring",
        "square", "stable", "stacks", "staged", "stairs", "stamps", "stance",
        "static", "status", "steady", "stereo", "sticky", "stolen", "stones",
        "stored", "strain", "strand", "stream", "street", "stress", "strict",
        "strike", "string", "stripe", "stroke", "studio", "stupid", "submit",
        "subtle", "suburb", "sudden", "suffer", "summer", "summit", "sunday",
        "sunset", "supper", "supply", "surely", "survey", "switch", "symbol",
        "syntax", "system", "tablet", "tackle", "tactic", "taking", "talent",
        "target", "temple", "tenant", "tender", "tennis", "terror", "thanks",
        "theory", "thirty", "thread", "threat", "thrill", "throne", "thrown",
        "ticket", "timber", "timing", "tissue", "toilet", "tongue", "topped",
        "toward", "towers", "travel", "treaty", "trendy", "trials", "tribal",
        "tribes", "troops", "tunnel", "turkey", "turned", "twelve", "twenty",
        "unable", "unfair", "unique", "unless", "unlike", "update", "upward",
        "urgent", "useful", "valley", "valued", "varied", "velvet", "vendor",
        "verbal", "verses", "vessel", "victim", "vision", "visual", "volume",
        "voting", "waited", "walker", "wanted", "wealth", "weapon", "weekly",
        "weight", "widely", "window", "winner", "winter", "wisdom", "within",
        "wonder", "wooden", "worker", "worthy", "writer", "yellow", "zombie"
    }
}


class WordLadderSolver:
    """
    Word Ladder Puzzle Solver using BFS (Breadth-First Search).
    
    This class provides efficient methods for finding the shortest
    transformation path between two words.
    
    Attributes:
        words: Dictionary mapping word length to set of valid words
        case_sensitive: Whether to treat words as case-sensitive
    """
    
    def __init__(
        self, 
        custom_words: Optional[Dict[int, Set[str]]] = None,
        case_sensitive: bool = False
    ):
        """
        Initialize the word ladder solver.
        
        Args:
            custom_words: Optional custom word dictionary (overrides built-in)
            case_sensitive: Whether to treat words as case-sensitive
        """
        self.words = custom_words if custom_words is not None else BUILTIN_WORDS
        self.case_sensitive = case_sensitive
        # Normalize words to lowercase if not case-sensitive
        if not case_sensitive:
            self.words = {
                length: {w.lower() for w in word_set}
                for length, word_set in self.words.items()
            }
    
    def get_neighbors(self, word: str) -> List[str]:
        """
        Get all words that differ by exactly one letter.
        
        Args:
            word: The word to find neighbors for
            
        Returns:
            List of words that differ by exactly one letter
            
        Examples:
            >>> solver = WordLadderSolver()
            >>> neighbors = solver.get_neighbors("cat")
            >>> "cot" in neighbors or "bat" in neighbors
            True
        """
        if not self.case_sensitive:
            word = word.lower()
        
        length = len(word)
        if length not in self.words:
            return []
        
        word_set = self.words[length]
        neighbors = []
        
        # Generate all possible one-letter changes
        for i in range(length):
            for c in 'abcdefghijklmnopqrstuvwxyz':
                if c != word[i]:
                    new_word = word[:i] + c + word[i + 1:]
                    if new_word in word_set:
                        neighbors.append(new_word)
        
        return neighbors
    
    def find_shortest_path(
        self, 
        start: str, 
        end: str, 
        max_depth: int = 100
    ) -> Optional[List[str]]:
        """
        Find the shortest word ladder from start to end.
        
        Uses BFS to guarantee finding the shortest path.
        
        Args:
            start: Starting word
            end: Target word
            max_depth: Maximum path length to search
            
        Returns:
            List of words forming the shortest path, or None if no path exists
            
        Examples:
            >>> solver = WordLadderSolver()
            >>> path = solver.find_shortest_path("cat", "dog")
            >>> path[0] == "cat" and path[-1] == "dog"
            True
        """
        if not self.case_sensitive:
            start = start.lower()
            end = end.lower()
        
        # Validate inputs
        if len(start) != len(end):
            return None
        
        if start == end:
            return [start]
        
        length = len(start)
        if length not in self.words:
            return None
        
        word_set = self.words[length]
        
        if start not in word_set or end not in word_set:
            return None
        
        # BFS
        queue = deque([(start, [start])])
        visited = {start}
        
        while queue:
            current, path = queue.popleft()
            
            if len(path) > max_depth:
                continue
            
            for neighbor in self.get_neighbors(current):
                if neighbor == end:
                    return path + [neighbor]
                
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))
        
        return None
    
    def find_all_paths(
        self, 
        start: str, 
        end: str, 
        max_paths: int = 10,
        max_depth: int = 100
    ) -> List[List[str]]:
        """
        Find all word ladders from start to end (up to max_paths).
        
        Args:
            start: Starting word
            end: Target word
            max_paths: Maximum number of paths to return
            max_depth: Maximum path length to search
            
        Returns:
            List of paths (each path is a list of words)
            
        Examples:
            >>> solver = WordLadderSolver()
            >>> paths = solver.find_all_paths("cat", "dog", max_paths=3)
            >>> len(paths) > 0
            True
        """
        if not self.case_sensitive:
            start = start.lower()
            end = end.lower()
        
        if len(start) != len(end):
            return []
        
        if start == end:
            return [[start]]
        
        length = len(start)
        if length not in self.words:
            return []
        
        word_set = self.words[length]
        
        if start not in word_set or end not in word_set:
            return []
        
        # Find shortest path length first
        shortest = self.find_shortest_path(start, end, max_depth)
        if not shortest:
            return []
        
        target_length = len(shortest)
        
        # DFS to find all paths of target length
        paths = []
        
        def dfs(current: str, path: List[str], visited: Set[str]):
            if len(paths) >= max_paths:
                return
            
            if current == end:
                if len(path) == target_length:
                    paths.append(path[:])
                return
            
            if len(path) >= target_length:
                return
            
            for neighbor in self.get_neighbors(current):
                if neighbor not in visited:
                    visited.add(neighbor)
                    path.append(neighbor)
                    dfs(neighbor, path, visited)
                    path.pop()
                    visited.remove(neighbor)
        
        dfs(start, [start], {start})
        return paths
    
    def is_valid_word(self, word: str) -> bool:
        """
        Check if a word is in the dictionary.
        
        Args:
            word: Word to check
            
        Returns:
            True if word is valid, False otherwise
        """
        if not self.case_sensitive:
            word = word.lower()
        
        length = len(word)
        return length in self.words and word in self.words[length]
    
    def is_valid_transformation(self, word1: str, word2: str) -> bool:
        """
        Check if two words differ by exactly one letter.
        
        Args:
            word1: First word
            word2: Second word
            
        Returns:
            True if words differ by exactly one letter
            
        Examples:
            >>> solver = WordLadderSolver()
            >>> solver.is_valid_transformation("cat", "cot")
            True
            >>> solver.is_valid_transformation("cat", "dog")
            False
        """
        if not self.case_sensitive:
            word1 = word1.lower()
            word2 = word2.lower()
        
        if len(word1) != len(word2):
            return False
        
        differences = sum(1 for c1, c2 in zip(word1, word2) if c1 != c2)
        return differences == 1
    
    def validate_ladder(self, ladder: List[str]) -> Tuple[bool, str]:
        """
        Validate a word ladder sequence.
        
        Args:
            ladder: List of words forming the ladder
            
        Returns:
            Tuple of (is_valid, error_message)
            
        Examples:
            >>> solver = WordLadderSolver()
            >>> valid, msg = solver.validate_ladder(["cat", "cot", "dot", "dog"])
            >>> valid
            True
        """
        if not ladder:
            return False, "Empty ladder"
        
        if len(ladder) < 2:
            return False, "Ladder must have at least 2 words"
        
        # Check all words are valid
        for i, word in enumerate(ladder):
            if not self.is_valid_word(word):
                return False, f"Invalid word at position {i}: '{word}'"
        
        # Check all transformations are valid
        for i in range(len(ladder) - 1):
            if not self.is_valid_transformation(ladder[i], ladder[i + 1]):
                return False, f"Invalid transformation from '{ladder[i]}' to '{ladder[i + 1]}'"
        
        return True, "Valid ladder"
    
    def get_words_of_length(self, length: int) -> Set[str]:
        """
        Get all words of a specific length.
        
        Args:
            length: Word length
            
        Returns:
            Set of words with the specified length
        """
        return self.words.get(length, set()).copy()
    
    def generate_puzzle(
        self, 
        length: int = 4, 
        min_path_length: int = 3,
        max_attempts: int = 100
    ) -> Optional[Tuple[str, str, int]]:
        """
        Generate a word ladder puzzle.
        
        Args:
            length: Word length
            min_path_length: Minimum path length for the puzzle
            max_attempts: Maximum number of attempts
            
        Returns:
            Tuple of (start_word, end_word, solution_length) or None
        """
        import random
        
        words = list(self.get_words_of_length(length))
        if len(words) < 2:
            return None
        
        for _ in range(max_attempts):
            start = random.choice(words)
            end = random.choice(words)
            
            if start == end:
                continue
            
            path = self.find_shortest_path(start, end)
            if path and len(path) >= min_path_length:
                return (start, end, len(path))
        
        return None
    
    def add_words(self, words: List[str]) -> None:
        """
        Add words to the dictionary.
        
        Args:
            words: List of words to add
        """
        for word in words:
            if not self.case_sensitive:
                word = word.lower()
            
            length = len(word)
            if length not in self.words:
                self.words[length] = set()
            self.words[length].add(word)
    
    def get_ladder_difficulty(
        self, 
        start: str, 
        end: str
    ) -> Dict[str, any]:
        """
        Calculate the difficulty of a word ladder puzzle.
        
        Args:
            start: Starting word
            end: Target word
            
        Returns:
            Dictionary with difficulty metrics
        """
        if not self.case_sensitive:
            start = start.lower()
            end = end.lower()
        
        path = self.find_shortest_path(start, end)
        
        if not path:
            return {
                "solvable": False,
                "difficulty": None,
                "path_length": None,
                "branching_factor": None
            }
        
        path_length = len(path)
        
        # Calculate average branching factor
        total_neighbors = 0
        for word in path:
            total_neighbors += len(self.get_neighbors(word))
        avg_branching = total_neighbors / path_length if path_length > 0 else 0
        
        # Calculate difficulty score (1-10)
        # Longer paths and lower branching = harder
        length_score = min(path_length - 1, 10)  # 1-10
        branch_score = max(1, 10 - avg_branching / 3)  # Lower branching = harder
        
        difficulty = round((length_score + branch_score) / 2, 1)
        
        return {
            "solvable": True,
            "difficulty": difficulty,
            "path_length": path_length,
            "branching_factor": round(avg_branching, 2),
            "start_word": start,
            "end_word": end
        }


# Convenience functions using default solver
_default_solver = WordLadderSolver()


def find_shortest_path(start: str, end: str, max_depth: int = 100) -> Optional[List[str]]:
    """
    Find the shortest word ladder path (using default solver).
    
    Args:
        start: Starting word
        end: Target word
        max_depth: Maximum path length to search
        
    Returns:
        List of words forming the shortest path, or None
    """
    return _default_solver.find_shortest_path(start, end, max_depth)


def find_all_paths(
    start: str, 
    end: str, 
    max_paths: int = 10,
    max_depth: int = 100
) -> List[List[str]]:
    """
    Find all word ladder paths (using default solver).
    
    Args:
        start: Starting word
        end: Target word
        max_paths: Maximum number of paths to return
        max_depth: Maximum path length to search
        
    Returns:
        List of paths
    """
    return _default_solver.find_all_paths(start, end, max_paths, max_depth)


def get_neighbors(word: str) -> List[str]:
    """
    Get all one-letter transformations of a word (using default solver).
    
    Args:
        word: Word to find neighbors for
        
    Returns:
        List of neighbor words
    """
    return _default_solver.get_neighbors(word)


def is_valid_word(word: str) -> bool:
    """
    Check if a word is in the dictionary (using default solver).
    
    Args:
        word: Word to check
        
    Returns:
        True if valid word
    """
    return _default_solver.is_valid_word(word)


def is_valid_transformation(word1: str, word2: str) -> bool:
    """
    Check if two words differ by exactly one letter (using default solver).
    
    Args:
        word1: First word
        word2: Second word
        
    Returns:
        True if valid transformation
    """
    return _default_solver.is_valid_transformation(word1, word2)


def validate_ladder(ladder: List[str]) -> Tuple[bool, str]:
    """
    Validate a word ladder sequence (using default solver).
    
    Args:
        ladder: List of words
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    return _default_solver.validate_ladder(ladder)


def generate_puzzle(
    length: int = 4, 
    min_path_length: int = 3,
    max_attempts: int = 100
) -> Optional[Tuple[str, str, int]]:
    """
    Generate a word ladder puzzle (using default solver).
    
    Args:
        length: Word length
        min_path_length: Minimum path length
        max_attempts: Maximum attempts
        
    Returns:
        Tuple of (start_word, end_word, solution_length) or None
    """
    return _default_solver.generate_puzzle(length, min_path_length, max_attempts)


def get_ladder_difficulty(start: str, end: str) -> Dict[str, any]:
    """
    Calculate the difficulty of a word ladder puzzle (using default solver).
    
    Args:
        start: Starting word
        end: Target word
        
    Returns:
        Dictionary with difficulty metrics
    """
    return _default_solver.get_ladder_difficulty(start, end)


def get_words_of_length(length: int) -> Set[str]:
    """
    Get all words of a specific length (using default solver).
    
    Args:
        length: Word length
        
    Returns:
        Set of words
    """
    return _default_solver.get_words_of_length(length)


def add_words(words: List[str]) -> None:
    """
    Add words to the dictionary (using default solver).
    
    Args:
        words: List of words to add
    """
    _default_solver.add_words(words)


def create_solver(
    custom_words: Optional[Dict[int, Set[str]]] = None,
    case_sensitive: bool = False
) -> WordLadderSolver:
    """
    Create a new WordLadderSolver instance.
    
    Args:
        custom_words: Optional custom word dictionary
        case_sensitive: Whether to treat words as case-sensitive
        
    Returns:
        WordLadderSolver instance
    """
    return WordLadderSolver(custom_words, case_sensitive)


if __name__ == "__main__":
    # Demo
    print("=" * 60)
    print("Word Ladder Puzzle Demo")
    print("=" * 60)
    
    # Example 1: Classic cat -> dog
    print("\n1. Classic: cat -> dog")
    path = find_shortest_path("cat", "dog")
    if path:
        print(f"   Shortest path ({len(path)} steps): {' -> '.join(path)}")
    
    # Example 2: Longer ladder
    print("\n2. Longer: cold -> warm")
    path = find_shortest_path("cold", "warm")
    if path:
        print(f"   Shortest path ({len(path)} steps): {' -> '.join(path)}")
    
    # Example 3: Generate a puzzle
    print("\n3. Generated puzzle (4-letter words):")
    puzzle = generate_puzzle(length=4, min_path_length=4)
    if puzzle:
        start, end, solution_len = puzzle
        print(f"   Start: '{start}', End: '{end}'")
        print(f"   Solution length: {solution_len} steps")
    
    # Example 4: Get neighbors
    print("\n4. Neighbors of 'love':")
    neighbors = get_neighbors("love")
    print(f"   {len(neighbors)} neighbors: {neighbors[:10]}...")
    
    # Example 5: Validate a ladder
    print("\n5. Validate ladder:")
    test_ladder = ["cat", "cot", "dot", "dog"]
    valid, msg = validate_ladder(test_ladder)
    print(f"   {test_ladder}")
    print(f"   Valid: {valid}, Message: {msg}")
    
    # Example 6: Difficulty rating
    print("\n6. Difficulty rating:")
    difficulty = get_ladder_difficulty("love", "hate")
    print(f"   love -> hate: {difficulty}")