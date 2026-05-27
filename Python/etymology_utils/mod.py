#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""AllToolkit - Etymology Utilities Module

Word origin and etymology analysis utilities with zero external dependencies.
Provides word origin tracking, root word analysis, word family generation,
etymology tree visualization, and language origin classification.

Author: AllToolkit
License: MIT
"""

from typing import List, Dict, Any, Optional, Tuple, Set, Union
from dataclasses import dataclass, field
from enum import Enum
import re


# =============================================================================
# Enums
# =============================================================================

class LanguageOrigin(Enum):
    """Language family classification."""
    LATIN = "Latin"
    GREEK = "Greek"
    GERMANIC = "Germanic"
    OLD_ENGLISH = "Old English"
    ENGLISH = "English"
    FRENCH = "French"
    NORMAN = "Norman"
    CELTIC = "Celtic"
    ARABIC = "Arabic"
    HEBREW = "Hebrew"
    PERSIAN = "Persian"
    CHINESE = "Chinese"
    JAPANESE = "Japanese"
    SPANISH = "Spanish"
    ITALIAN = "Italian"
    DUTCH = "Dutch"
    NORSE = "Norse"
    SLAVIC = "Slavic"
    HINDI = "Hindi"
    UNKNOWN = "Unknown"


class HistoricalPeriod(Enum):
    """Historical periods for etymology classification."""
    ANCIENT = "Ancient"  # Before 500 CE
    MEDIEVAL = "Medieval"  # 500-1500 CE
    EARLY_MODERN = "Early Modern"  # 1500-1800 CE
    MODERN = "Modern"  # 1800-present
    CONTEMPORARY = "Contemporary"  # 20th-21st century


class WordRelation(Enum):
    """Types of word relationships."""
    DERIVATION = "Derivation"  # Direct derivation
    COMPOUND = "Compound"  # Compound word
    BORROWING = "Borrowing"  # Loan word
    COGNATE = "Cognate"  # Related word in another language
    ROOT = "Root"  # Root/stem word
    INFLECTION = "Inflection"  # Grammatical variation
    ETYMON = "Etymon"  # Original source word


# =============================================================================
# Data Classes
# =============================================================================

@dataclass
class EtymologyEntry:
    """Single etymology entry for a word."""
    word: str
    language_origin: LanguageOrigin
    historical_period: HistoricalPeriod
    original_form: Optional[str] = None
    intermediate_forms: List[str] = field(default_factory=list)
    meaning_evolution: List[str] = field(default_factory=list)
    related_words: List[str] = field(default_factory=list)
    cognates: Dict[str, str] = field(default_factory=dict)  # language -> cognate word
    notes: Optional[str] = None
    confidence: float = 1.0  # 0.0-1.0 confidence level
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "word": self.word,
            "language_origin": self.language_origin.value,
            "historical_period": self.historical_period.value,
            "original_form": self.original_form,
            "intermediate_forms": self.intermediate_forms,
            "meaning_evolution": self.meaning_evolution,
            "related_words": self.related_words,
            "cognates": self.cognates,
            "notes": self.notes,
            "confidence": self.confidence
        }


@dataclass
class EtymologyTree:
    """Tree structure for etymology visualization."""
    word: str
    children: List['EtymologyTree'] = field(default_factory=list)
    origin: Optional[LanguageOrigin] = None
    period: Optional[HistoricalPeriod] = None
    form: Optional[str] = None
    
    def add_child(self, child: 'EtymologyTree') -> None:
        """Add a child node."""
        self.children.append(child)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "word": self.word,
            "origin": self.origin.value if self.origin else None,
            "period": self.period.value if self.period else None,
            "form": self.form,
            "children": [c.to_dict() for c in self.children]
        }
    
    def depth(self) -> int:
        """Calculate tree depth."""
        if not self.children:
            return 1
        return 1 + max(c.depth() for c in self.children)
    
    def size(self) -> int:
        """Calculate total nodes in tree."""
        return 1 + sum(c.size() for c in self.children)


@dataclass
class WordFamily:
    """Word family group with common root."""
    root: str
    members: List[str] = field(default_factory=list)
    derivations: Dict[str, str] = field(default_factory=dict)  # word -> derivation path
    compounds: List[str] = field(default_factory=list)
    
    def add_member(self, word: str, derivation_path: Optional[str] = None) -> None:
        """Add a word family member."""
        if word not in self.members:
            self.members.append(word)
            if derivation_path:
                self.derivations[word] = derivation_path
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "root": self.root,
            "members": self.members,
            "derivations": self.derivations,
            "compounds": self.compounds
        }


# =============================================================================
# Built-in Etymology Database
# =============================================================================

# Sample etymology database for common English words
ETYMOLOGY_DATABASE: Dict[str, EtymologyEntry] = {
    # Latin origins
    "computer": EtymologyEntry(
        word="computer",
        language_origin=LanguageOrigin.LATIN,
        historical_period=HistoricalPeriod.MODERN,
        original_form="computare",
        intermediate_forms=["compute", "computer"],
        meaning_evolution=["to calculate", "one who computes", "electronic computing device"],
        related_words=["compute", "computation", "computational"],
        cognates={"French": "ordinateur", "German": "Computer", "Spanish": "computadora"},
        notes="From Latin 'computare' (to calculate, count together)"
    ),
    "information": EtymologyEntry(
        word="information",
        language_origin=LanguageOrigin.LATIN,
        historical_period=HistoricalPeriod.EARLY_MODERN,
        original_form="informare",
        intermediate_forms=["inform", "information"],
        meaning_evolution=["to shape/form", "to instruct", "knowledge communicated"],
        related_words=["inform", "informative", "informed"],
        cognates={"French": "information", "German": "Information", "Spanish": "información"}
    ),
    "education": EtymologyEntry(
        word="education",
        language_origin=LanguageOrigin.LATIN,
        historical_period=HistoricalPeriod.EARLY_MODERN,
        original_form="educare",
        intermediate_forms=["educate", "education"],
        meaning_evolution=["to lead out", "to train/teach", "systematic instruction"],
        related_words=["educate", "educator", "educational"],
        cognates={"French": "éducation", "German": "Erziehung", "Spanish": "educación"},
        notes="From Latin 'educare' (to bring up, train) and 'educere' (to lead out)"
    ),
    
    # Greek origins
    "telephone": EtymologyEntry(
        word="telephone",
        language_origin=LanguageOrigin.GREEK,
        historical_period=HistoricalPeriod.MODERN,
        original_form="τῆλε + φωνή",
        intermediate_forms=["tele-phone", "telephone"],
        meaning_evolution=["far + voice", "device for distant voice communication"],
        related_words=["telephony", "telephonic", "phone"],
        cognates={"French": "téléphone", "German": "Telefon", "Spanish": "teléfono"},
        notes="Greek 'tele' (far) + 'phone' (voice)"
    ),
    "philosophy": EtymologyEntry(
        word="philosophy",
        language_origin=LanguageOrigin.GREEK,
        historical_period=HistoricalPeriod.ANCIENT,
        original_form="φιλοσοφία",
        intermediate_forms=["philosophia", "philosophy"],
        meaning_evolution=["love of wisdom", "study of fundamental questions"],
        related_words=["philosopher", "philosophical", "philosophize"],
        cognates={"French": "philosophie", "German": "Philosophie", "Spanish": "filosofía"},
        notes="Greek 'philos' (loving) + 'sophia' (wisdom)"
    ),
    "mathematics": EtymologyEntry(
        word="mathematics",
        language_origin=LanguageOrigin.GREEK,
        historical_period=HistoricalPeriod.ANCIENT,
        original_form="μάθημα",
        intermediate_forms=["mathema", "mathematica", "mathematics"],
        meaning_evolution=["learning/knowledge", "science of numbers"],
        related_words=["mathematic", "mathematician", "math"],
        cognates={"French": "mathématiques", "German": "Mathematik", "Spanish": "matemáticas"},
        notes="Greek 'mathema' (lesson, learning)"
    ),
    
    # Germanic/Old English origins
    "king": EtymologyEntry(
        word="king",
        language_origin=LanguageOrigin.OLD_ENGLISH,
        historical_period=HistoricalPeriod.ANCIENT,
        original_form="cyning",
        intermediate_forms=["cining", "king"],
        meaning_evolution=["tribal leader", "monarch"],
        related_words=["kingdom", "kingly", "kingship"],
        cognates={"German": "König", "Dutch": "koning", "Norwegian": "konge"},
        notes="Old English 'cyning', from Proto-Germanic '*kuningaz'"
    ),
    "friend": EtymologyEntry(
        word="friend",
        language_origin=LanguageOrigin.OLD_ENGLISH,
        historical_period=HistoricalPeriod.ANCIENT,
        original_form="freond",
        intermediate_forms=["friend"],
        meaning_evolution=["one who loves", "close companion"],
        related_words=["friendly", "friendship", "befriend"],
        cognates={"German": "Freund", "Dutch": "vriend", "Norwegian": "venn"},
        notes="Old English 'freond' (friend, lover)"
    ),
    "work": EtymologyEntry(
        word="work",
        language_origin=LanguageOrigin.OLD_ENGLISH,
        historical_period=HistoricalPeriod.ANCIENT,
        original_form="weorc",
        intermediate_forms=["werk", "work"],
        meaning_evolution=["labor/effort", "employment", "productive activity"],
        related_words=["worker", "working", "workmanship"],
        cognates={"German": "Werk", "Dutch": "werk", "Norwegian": "verk"},
        notes="Old English 'weorc', from Proto-Germanic '*werkam'"
    ),
    
    # French/Norman origins
    "government": EtymologyEntry(
        word="government",
        language_origin=LanguageOrigin.FRENCH,
        historical_period=HistoricalPeriod.MEDIEVAL,
        original_form="gouverner",
        intermediate_forms=["governement", "government"],
        meaning_evolution=["to steer/rule", "system of ruling", "state administration"],
        related_words=["govern", "governor", "governing"],
        cognates={"French": "gouvernement", "Spanish": "gobierno"},
        notes="From Old French 'governer', ultimately from Greek 'kybernan' (to steer)"
    ),
    "justice": EtymologyEntry(
        word="justice",
        language_origin=LanguageOrigin.FRENCH,
        historical_period=HistoricalPeriod.MEDIEVAL,
        original_form="justitia",
        intermediate_forms=["justice"],
        meaning_evolution=["righteousness", "legal fairness", "system of law"],
        related_words=["just", "justify", "justification"],
        cognates={"French": "justice", "German": "Justiz", "Spanish": "justicia"},
        notes="From Latin 'justitia' via French"
    ),
    "beauty": EtymologyEntry(
        word="beauty",
        language_origin=LanguageOrigin.FRENCH,
        historical_period=HistoricalPeriod.MEDIEVAL,
        original_form="bel",
        intermediate_forms=["beauté", "beauty"],
        meaning_evolution=["beautiful", "quality of being beautiful"],
        related_words=["beautiful", "beautify", "beautician"],
        cognates={"French": "beauté", "Spanish": "belleza"},
        notes="From Old French 'bel' (beautiful)"
    ),
    
    # Arabic origins
    "algebra": EtymologyEntry(
        word="algebra",
        language_origin=LanguageOrigin.ARABIC,
        historical_period=HistoricalPeriod.MEDIEVAL,
        original_form="al-jabr",
        intermediate_forms=["algebra"],
        meaning_evolution=["restoration/reunion", "mathematical study"],
        related_words=["algebraic", "algebraist"],
        cognates={"Spanish": "álgebra", "French": "algèbre"},
        notes="From Arabic 'al-jabr' (the reunion of broken parts)"
    ),
    "coffee": EtymologyEntry(
        word="coffee",
        language_origin=LanguageOrigin.ARABIC,
        historical_period=HistoricalPeriod.EARLY_MODERN,
        original_form="qahwa",
        intermediate_forms=["kahve", "caffe", "coffee"],
        meaning_evolution=["wine-like drink", "caffeinated beverage"],
        related_words=["cafeteria", "caffeine"],
        cognates={"French": "café", "Italian": "caffè", "Turkish": "kahve"},
        notes="From Arabic 'qahwa', via Turkish 'kahve' and Italian 'caffè'"
    ),
    
    # Japanese origins
    "karate": EtymologyEntry(
        word="karate",
        language_origin=LanguageOrigin.JAPANESE,
        historical_period=HistoricalPeriod.MODERN,
        original_form="空手",
        intermediate_forms=["karate"],
        meaning_evolution=["empty hand", "unarmed martial art"],
        related_words=["karateka", "karate-do"],
        cognates={"English": "karate"},
        notes="Japanese 'kara' (empty) + 'te' (hand)"
    ),
    
    # Chinese origins
    "tea": EtymologyEntry(
        word="tea",
        language_origin=LanguageOrigin.CHINESE,
        historical_period=HistoricalPeriod.EARLY_MODERN,
        original_form="茶",
        intermediate_forms=["te", "tay", "tea"],
        meaning_evolution=["tea plant/beverage"],
        related_words=["teahouse", "teacup"],
        cognates={"French": "thé", "German": "Tee", "Spanish": "té"},
        notes="From Chinese 'te' (Amoy dialect) or 'cha' (Mandarin)"
    ),
    
    # Compound words
    "breakfast": EtymologyEntry(
        word="breakfast",
        language_origin=LanguageOrigin.OLD_ENGLISH,
        historical_period=HistoricalPeriod.MEDIEVAL,
        original_form="break + fast",
        intermediate_forms=["brekefast", "breakfast"],
        meaning_evolution=["breaking the fasting period", "morning meal"],
        related_words=["break", "fast"],
        cognates={},
        notes="Compound of 'break' + 'fast' (breaking the overnight fast)"
    ),
    "airport": EtymologyEntry(
        word="airport",
        language_origin=LanguageOrigin.ENGLISH,
        historical_period=HistoricalPeriod.CONTEMPORARY,
        original_form="air + port",
        intermediate_forms=["airport"],
        meaning_evolution=["port for aircraft", "aviation facility"],
        related_words=["airplane", "airline", "airfield"],
        cognates={"French": "aéroport", "German": "Flughafen"},
        notes="Modern compound: 'air' + 'port'"
    ),
}

# Common root words database
ROOT_WORDS_DATABASE: Dict[str, List[str]] = {
    "act": ["action", "active", "actor", "activate", "actual", "activity"],
    "book": ["booklet", "bookmark", "bookshelf", "bookstore", "textbook", "notebook"],
    "break": ["breakfast", "breakthrough", "breakdown", "outbreak", "breakable"],
    "carry": ["carrier", "carry-on", "carrying", "carriage"],
    "check": ["checkout", "checkup", "checkpoint", "checkbox", "checklist"],
    "come": ["comeback", "outcome", "income", "welcome", "overcome", "become"],
    "do": ["doing", "redo", "undo", "overdo", "outdo", "donor"],
    "form": ["format", "formation", "formula", "formal", "inform", "reform"],
    "head": ["headache", "headline", "headquarter", "headless", "header"],
    "hold": ["holder", "holdup", "holdout", "uphold", "household"],
    "know": ["knowledge", "knowing", "unknown", "well-known", "acknowledge"],
    "life": ["lifestyle", "lifetime", "lifelong", "alive", "lifetime"],
    "light": ["lightning", "lightweight", "highlight", "sunlight", "daylight"],
    "make": ["maker", "making", "remake", "man-made", "makeup"],
    "move": ["movement", "moving", "remove", "movie", "mover"],
    "name": ["namely", "nickname", "rename", "surname", "byname"],
    "note": ["notebook", "notable", "notice", "notify", "denote"],
    "play": ["player", "playing", "playground", "display", "playlist"],
    "point": ["pointer", "pointless", "pointed", "checkpoint", "viewpoint"],
    "power": ["powerful", "powerless", "empower", "superpower", "powerpoint"],
    "read": ["reader", "reading", "reread", "readable", "unread"],
    "run": ["runner", "running", "rerun", "runway", " overrun"],
    "speak": ["speaker", "speaking", "speech", "speakable", "spoken"],
    "stand": ["standing", "standard", "standpoint", "understand", "standby"],
    "start": ["starter", "starting", "restart", "start-up", "startle"],
    "stop": ["stopping", "stopper", "stopover", "nonstop", "stopwatch"],
    "take": ["taken", "taking", "undertake", "mistake", "takeover"],
    "think": ["thinking", "thinker", "thought", " rethink", "thinkable"],
    "time": ["timing", "timely", "lifetime", "part-time", "full-time"],
    "turn": ["turning", "turner", "return", " overturn", "turnover"],
    "use": ["using", "user", "usage", "useful", "useless", "reuse"],
    "view": ["viewer", "viewing", "review", "preview", "viewpoint"],
    "walk": ["walking", "walker", "walkway", " sidewalk", "walkout"],
    "watch": ["watcher", "watching", "watchdog", "watchful", " wristwatch"],
    "work": ["worker", "working", "workplace", "network", "homework"],
    "write": ["writer", "writing", "rewrite", "write-up", "writable"],
}

# Common prefixes and suffixes with origins
PREFIXES_DATABASE: Dict[str, Tuple[LanguageOrigin, str]] = {
    "a": (LanguageOrigin.GREEK, "not/without"),
    "ab": (LanguageOrigin.LATIN, "away from"),
    "ad": (LanguageOrigin.LATIN, "to/toward"),
    "anti": (LanguageOrigin.GREEK, "against"),
    "auto": (LanguageOrigin.GREEK, "self"),
    "be": (LanguageOrigin.OLD_ENGLISH, "make/cause"),
    "bi": (LanguageOrigin.LATIN, "two"),
    "co": (LanguageOrigin.LATIN, "with/together"),
    "de": (LanguageOrigin.LATIN, "down/from"),
    "dis": (LanguageOrigin.LATIN, "apart/not"),
    "ex": (LanguageOrigin.LATIN, "out/from"),
    "extra": (LanguageOrigin.LATIN, "beyond"),
    "fore": (LanguageOrigin.OLD_ENGLISH, "before"),
    "hyper": (LanguageOrigin.GREEK, "over/excessive"),
    "in": (LanguageOrigin.LATIN, "in/not"),
    "inter": (LanguageOrigin.LATIN, "between"),
    "macro": (LanguageOrigin.GREEK, "large"),
    "micro": (LanguageOrigin.GREEK, "small"),
    "mis": (LanguageOrigin.OLD_ENGLISH, "wrong/badly"),
    "multi": (LanguageOrigin.LATIN, "many"),
    "non": (LanguageOrigin.LATIN, "not"),
    "over": (LanguageOrigin.OLD_ENGLISH, "above/excessive"),
    "post": (LanguageOrigin.LATIN, "after"),
    "pre": (LanguageOrigin.LATIN, "before"),
    "pro": (LanguageOrigin.LATIN, "for/forward"),
    "re": (LanguageOrigin.LATIN, "again/back"),
    "sub": (LanguageOrigin.LATIN, "under"),
    "super": (LanguageOrigin.LATIN, "above/over"),
    "trans": (LanguageOrigin.LATIN, "across"),
    "tri": (LanguageOrigin.LATIN, "three"),
    "un": (LanguageOrigin.OLD_ENGLISH, "not"),
    "under": (LanguageOrigin.OLD_ENGLISH, "below"),
    "up": (LanguageOrigin.OLD_ENGLISH, "upward"),
}

SUFFIXES_DATABASE: Dict[str, Tuple[LanguageOrigin, str]] = {
    "able": (LanguageOrigin.LATIN, "capable of"),
    "age": (LanguageOrigin.LATIN, "state/collective"),
    "al": (LanguageOrigin.LATIN, "relating to"),
    "ance": (LanguageOrigin.LATIN, "state/quality"),
    "ant": (LanguageOrigin.LATIN, "performing/being"),
    "ation": (LanguageOrigin.LATIN, "action/process"),
    "dom": (LanguageOrigin.OLD_ENGLISH, "state/condition"),
    "ed": (LanguageOrigin.OLD_ENGLISH, "past tense/adjective"),
    "er": (LanguageOrigin.OLD_ENGLISH, "one who"),
    "est": (LanguageOrigin.OLD_ENGLISH, "most"),
    "ful": (LanguageOrigin.OLD_ENGLISH, "full of"),
    "hood": (LanguageOrigin.OLD_ENGLISH, "state/condition"),
    "ing": (LanguageOrigin.OLD_ENGLISH, "present participle"),
    "ion": (LanguageOrigin.LATIN, "action/state"),
    "ism": (LanguageOrigin.GREEK, "belief/system"),
    "ist": (LanguageOrigin.GREEK, "one who believes"),
    "ity": (LanguageOrigin.LATIN, "state/quality"),
    "ive": (LanguageOrigin.LATIN, "having quality"),
    "less": (LanguageOrigin.OLD_ENGLISH, "without"),
    "ly": (LanguageOrigin.OLD_ENGLISH, "in manner of"),
    "ment": (LanguageOrigin.LATIN, "action/result"),
    "ness": (LanguageOrigin.OLD_ENGLISH, "state/quality"),
    "ous": (LanguageOrigin.LATIN, "having quality"),
    "ship": (LanguageOrigin.OLD_ENGLISH, "state/condition"),
    "tion": (LanguageOrigin.LATIN, "action/state"),
    "ward": (LanguageOrigin.OLD_ENGLISH, "direction"),
    "wise": (LanguageOrigin.OLD_ENGLISH, "manner/direction"),
    "y": (LanguageOrigin.OLD_ENGLISH, "characterized by"),
}


# =============================================================================
# Core Functions
# =============================================================================

def get_etymology(word: str) -> Optional[EtymologyEntry]:
    """
    Get etymology entry for a word from the database.
    
    Args:
        word: Word to lookup
        
    Returns:
        EtymologyEntry if found, None otherwise
    """
    word_lower = word.lower().strip()
    return ETYMOLOGY_DATABASE.get(word_lower)


def add_etymology(entry: EtymologyEntry) -> None:
    """
    Add an etymology entry to the database.
    
    Args:
        entry: EtymologyEntry to add
    """
    ETYMOLOGY_DATABASE[entry.word.lower()] = entry


def search_by_origin(origin: LanguageOrigin) -> List[EtymologyEntry]:
    """
    Find all words with a specific language origin.
    
    Args:
        origin: LanguageOrigin to search
        
    Returns:
        List of EtymologyEntry with matching origin
    """
    return [e for e in ETYMOLOGY_DATABASE.values() if e.language_origin == origin]


def search_by_period(period: HistoricalPeriod) -> List[EtymologyEntry]:
    """
    Find all words from a specific historical period.
    
    Args:
        period: HistoricalPeriod to search
        
    Returns:
        List of EtymologyEntry with matching period
    """
    return [e for e in ETYMOLOGY_DATABASE.values() if e.historical_period == period]


def find_cognates(word: str) -> Dict[str, str]:
    """
    Find cognates of a word across languages.
    
    Args:
        word: Word to find cognates for
        
    Returns:
        Dictionary mapping language to cognate word
    """
    entry = get_etymology(word)
    if entry:
        return entry.cognates
    return {}


def get_word_family(root: str) -> Optional[WordFamily]:
    """
    Get word family for a root word.
    
    Args:
        root: Root word
        
    Returns:
        WordFamily if found, None otherwise
    """
    root_lower = root.lower().strip()
    members = ROOT_WORDS_DATABASE.get(root_lower, [])
    if members:
        family = WordFamily(root=root_lower, members=members)
        for member in members:
            family.derivations[member] = f"{root} → {member}"
        return family
    return None


def build_etymology_tree(word: str) -> EtymologyTree:
    """
    Build an etymology tree for a word.
    
    Args:
        word: Word to build tree for
        
    Returns:
        EtymologyTree structure
    """
    entry = get_etymology(word)
    root = EtymologyTree(word=word)
    
    if entry:
        root.origin = entry.language_origin
        root.period = entry.historical_period
        
        # Add original form as child
        if entry.original_form:
            original_child = EtymologyTree(
                word=entry.original_form,
                origin=entry.language_origin,
                period=HistoricalPeriod.ANCIENT if entry.historical_period != HistoricalPeriod.ANCIENT else entry.historical_period
            )
            root.add_child(original_child)
        
        # Add intermediate forms
        for form in entry.intermediate_forms:
            if form != word:
                child = EtymologyTree(
                    word=form,
                    origin=entry.language_origin,
                    period=entry.historical_period
                )
                root.add_child(child)
        
        # Add related words
        for related in entry.related_words[:5]:  # Limit to 5 related words
            child = EtymologyTree(
                word=related,
                origin=entry.language_origin,
                period=HistoricalPeriod.MODERN
            )
            root.add_child(child)
    
    return root


def extract_root(word: str) -> Optional[str]:
    """
    Extract the root word from a derived word.
    
    Args:
        word: Word to extract root from
        
    Returns:
        Root word if found, None otherwise
    """
    word_lower = word.lower().strip()
    
    # Check prefixes
    for prefix in sorted(PREFIXES_DATABASE.keys(), key=len, reverse=True):
        if word_lower.startswith(prefix):
            potential_root = word_lower[len(prefix):]
            if potential_root in ROOT_WORDS_DATABASE or potential_root in ETYMOLOGY_DATABASE:
                return potential_root
    
    # Check suffixes
    for suffix in sorted(SUFFIXES_DATABASE.keys(), key=len, reverse=True):
        if word_lower.endswith(suffix):
            potential_root = word_lower[:-len(suffix)]
            if potential_root in ROOT_WORDS_DATABASE or potential_root in ETYMOLOGY_DATABASE:
                return potential_root
    
    # Check direct match in root database
    for root, members in ROOT_WORDS_DATABASE.items():
        if word_lower in members:
            return root
    
    return None


def analyze_word(word: str) -> Dict[str, Any]:
    """
    Perform comprehensive etymology analysis on a word.
    
    Args:
        word: Word to analyze
        
    Returns:
        Dictionary with analysis results
    """
    result = {
        "word": word,
        "etymology": None,
        "root": None,
        "prefix": None,
        "suffix": None,
        "word_family": None,
        "cognates": {},
        "is_compound": False,
        "compound_parts": []
    }
    
    entry = get_etymology(word)
    if entry:
        result["etymology"] = entry.to_dict()
        result["cognates"] = entry.cognates
    
    root = extract_root(word)
    if root:
        result["root"] = root
        family = get_word_family(root)
        if family:
            result["word_family"] = family.to_dict()
    
    # Check for prefixes
    for prefix in sorted(PREFIXES_DATABASE.keys(), key=len, reverse=True):
        if word.lower().startswith(prefix):
            result["prefix"] = {
                "prefix": prefix,
                "origin": PREFIXES_DATABASE[prefix][0].value,
                "meaning": PREFIXES_DATABASE[prefix][1]
            }
            break
    
    # Check for suffixes
    for suffix in sorted(SUFFIXES_DATABASE.keys(), key=len, reverse=True):
        if word.lower().endswith(suffix):
            result["suffix"] = {
                "suffix": suffix,
                "origin": SUFFIXES_DATABASE[suffix][0].value,
                "meaning": SUFFIXES_DATABASE[suffix][1]
            }
            break
    
    # Check if compound word
    compound_parts = detect_compound(word)
    if compound_parts:
        result["is_compound"] = True
        result["compound_parts"] = compound_parts
    
    return result


def detect_compound(word: str) -> List[str]:
    """
    Detect if a word is a compound and extract its parts.
    
    Args:
        word: Word to check
        
    Returns:
        List of compound parts if compound, empty list otherwise
    """
    word_lower = word.lower()
    
    # Common compound patterns
    compound_patterns = [
        # Two known words joined
        lambda w: [w[:i], w[i:]] if any(
            w[:i] in ETYMOLOGY_DATABASE or w[:i] in ROOT_WORDS_DATABASE
            for i in range(3, len(w)-2)
        ) and any(
            w[i:] in ETYMOLOGY_DATABASE or w[i:] in ROOT_WORDS_DATABASE
            for i in range(3, len(w)-2)
        ) else []
    ]
    
    # Try common compound splits
    for i in range(3, len(word_lower) - 2):
        part1 = word_lower[:i]
        part2 = word_lower[i:]
        
        if part1 in ETYMOLOGY_DATABASE and part2 in ETYMOLOGY_DATABASE:
            return [part1, part2]
        if part1 in ROOT_WORDS_DATABASE and part2 in ROOT_WORDS_DATABASE:
            return [part1, part2]
        if part1 in ETYMOLOGY_DATABASE and part2 in ROOT_WORDS_DATABASE:
            return [part1, part2]
        if part1 in ROOT_WORDS_DATABASE and part2 in ETYMOLOGY_DATABASE:
            return [part1, part2]
    
    return []


def compare_words(word1: str, word2: str) -> Dict[str, Any]:
    """
    Compare etymology of two words.
    
    Args:
        word1: First word
        word2: Second word
        
    Returns:
        Comparison dictionary
    """
    entry1 = get_etymology(word1)
    entry2 = get_etymology(word2)
    
    result = {
        "word1": word1,
        "word2": word2,
        "same_origin": False,
        "same_period": False,
        "common_root": None,
        "related": False,
        "cognate_languages": []
    }
    
    if entry1 and entry2:
        result["same_origin"] = entry1.language_origin == entry2.language_origin
        result["same_period"] = entry1.historical_period == entry2.historical_period
        
        # Check for common cognate languages
        lang1 = set(entry1.cognates.keys())
        lang2 = set(entry2.cognates.keys())
        result["cognate_languages"] = list(lang1 & lang2)
        
        # Check if related
        result["related"] = (
            word1 in entry2.related_words or 
            word2 in entry1.related_words or
            result["same_origin"]
        )
    
    # Check for common root
    root1 = extract_root(word1)
    root2 = extract_root(word2)
    if root1 and root2 and root1 == root2:
        result["common_root"] = root1
        result["related"] = True
    
    return result


def visualize_tree(tree: EtymologyTree, indent: int = 0) -> str:
    """
    Generate ASCII visualization of an etymology tree.
    
    Args:
        tree: EtymologyTree to visualize
        indent: Current indentation level
        
    Returns:
        ASCII string representation
    """
    lines = []
    prefix = "  " * indent
    connector = "└─ " if indent > 0 else ""
    
    # Current node
    origin_str = f" [{tree.origin.value}]" if tree.origin else ""
    period_str = f" ({tree.period.value})" if tree.period else ""
    form_str = f" → {tree.form}" if tree.form else ""
    
    lines.append(f"{prefix}{connector}{tree.word}{origin_str}{period_str}{form_str}")
    
    # Children
    for child in tree.children:
        lines.append(visualize_tree(child, indent + 1))
    
    return "\n".join(lines)


def get_statistics() -> Dict[str, Any]:
    """
    Get statistics about the etymology database.
    
    Returns:
        Statistics dictionary
    """
    entries = list(ETYMOLOGY_DATABASE.values())
    
    # Count by origin
    origin_counts = {}
    for entry in entries:
        origin = entry.language_origin.value
        origin_counts[origin] = origin_counts.get(origin, 0) + 1
    
    # Count by period
    period_counts = {}
    for entry in entries:
        period = entry.historical_period.value
        period_counts[period] = period_counts.get(period, 0) + 1
    
    return {
        "total_words": len(entries),
        "total_roots": len(ROOT_WORDS_DATABASE),
        "total_prefixes": len(PREFIXES_DATABASE),
        "total_suffixes": len(SUFFIXES_DATABASE),
        "by_origin": origin_counts,
        "by_period": period_counts,
        "average_confidence": sum(e.confidence for e in entries) / len(entries) if entries else 0
    }


def search_words(query: str, fuzzy: bool = False) -> List[str]:
    """
    Search for words in the database.
    
    Args:
        query: Search query
        fuzzy: Whether to use fuzzy matching
        
    Returns:
        List of matching words
    """
    query_lower = query.lower()
    matches = []
    
    for word, entry in ETYMOLOGY_DATABASE.items():
        if fuzzy:
            # Fuzzy matching: check if query appears anywhere
            if query_lower in word or query_lower in entry.original_form.lower() if entry.original_form else False:
                matches.append(word)
        else:
            # Exact prefix matching
            if word.startswith(query_lower):
                matches.append(word)
    
    return sorted(matches)


def validate_etymology(entry: EtymologyEntry) -> List[str]:
    """
    Validate an etymology entry.
    
    Args:
        entry: EtymologyEntry to validate
        
    Returns:
        List of validation errors (empty if valid)
    """
    errors = []
    
    if not entry.word or not entry.word.strip():
        errors.append("Word cannot be empty")
    
    if entry.confidence < 0 or entry.confidence > 1:
        errors.append("Confidence must be between 0 and 1")
    
    if not isinstance(entry.language_origin, LanguageOrigin):
        errors.append("Invalid language origin")
    
    if not isinstance(entry.historical_period, HistoricalPeriod):
        errors.append("Invalid historical period")
    
    return errors


def export_to_json(entries: Optional[List[EtymologyEntry]] = None) -> str:
    """
    Export etymology data to JSON string.
    
    Args:
        entries: List of entries to export (None = all)
        
    Returns:
        JSON string
    """
    import json
    
    if entries is None:
        entries = list(ETYMOLOGY_DATABASE.values())
    
    data = {
        "version": "1.0",
        "source": "AllToolkit Etymology Utilities",
        "entries": [e.to_dict() for e in entries],
        "statistics": get_statistics()
    }
    
    return json.dumps(data, indent=2, ensure_ascii=False)


# =============================================================================
# Advanced Analysis Functions
# =============================================================================

def trace_word_evolution(word: str) -> List[Dict[str, Any]]:
    """
    Trace the evolution of a word through history.
    
    Args:
        word: Word to trace
        
    Returns:
        List of evolution stages
    """
    entry = get_etymology(word)
    if not entry:
        return []
    
    stages = []
    
    # Original form
    if entry.original_form:
        stages.append({
            "form": entry.original_form,
            "period": "Ancient/Original",
            "origin": entry.language_origin.value,
            "meaning": entry.meaning_evolution[0] if entry.meaning_evolution else None
        })
    
    # Intermediate forms
    for i, form in enumerate(entry.intermediate_forms):
        meaning_idx = min(i + 1, len(entry.meaning_evolution) - 1)
        stages.append({
            "form": form,
            "period": entry.historical_period.value,
            "origin": entry.language_origin.value,
            "meaning": entry.meaning_evolution[meaning_idx] if entry.meaning_evolution else None
        })
    
    # Current form
    stages.append({
        "form": word,
        "period": "Modern",
        "origin": "English",
        "meaning": entry.meaning_evolution[-1] if entry.meaning_evolution else None
    })
    
    return stages


def find_language_contributions() -> Dict[str, int]:
    """
    Find how many words each language has contributed.
    
    Returns:
        Dictionary mapping language to contribution count
    """
    stats = get_statistics()
    return stats["by_origin"]


def find_period_contributions() -> Dict[str, int]:
    """
    Find how many words each historical period has contributed.
    
    Returns:
        Dictionary mapping period to contribution count
    """
    stats = get_statistics()
    return stats["by_period"]


def generate_word_report(word: str) -> str:
    """
    Generate a comprehensive text report for a word.
    
    Args:
        word: Word to report
        
    Returns:
        Text report string
    """
    analysis = analyze_word(word)
    lines = [
        f"{'='*50}",
        f"ETYMOLOGY REPORT: {word.upper()}",
        f"{'='*50}",
        "",
    ]
    
    if analysis["etymology"]:
        entry = analysis["etymology"]
        lines.extend([
            f"Origin: {entry['language_origin']}",
            f"Period: {entry['historical_period']}",
            f"Original Form: {entry['original_form'] or 'Unknown'}",
            f"Confidence: {entry['confidence']:.1%}",
            "",
            "Evolution:",
        ])
        
        for form in entry['intermediate_forms']:
            lines.append(f"  → {form}")
        
        if entry['meaning_evolution']:
            lines.extend(["", "Meaning Evolution:"])
            for meaning in entry['meaning_evolution']:
                lines.append(f"  • {meaning}")
        
        if entry['notes']:
            lines.extend(["", f"Notes: {entry['notes']}"])
    
    if analysis["root"]:
        lines.extend(["", f"Root Word: {analysis['root']}"])
    
    if analysis["prefix"]:
        lines.extend(["", f"Prefix: {analysis['prefix']['prefix']} ({analysis['prefix']['meaning']})"])
    
    if analysis["suffix"]:
        lines.extend(["", f"Suffix: {analysis['suffix']['suffix']} ({analysis['suffix']['meaning']})"])
    
    if analysis["is_compound"]:
        lines.extend(["", f"Compound Word: {word} = {'+'.join(analysis['compound_parts'])}"])
    
    if analysis["cognates"]:
        lines.extend(["", "Cognates:"])
        for lang, cognate in analysis["cognates"].items():
            lines.append(f"  • {lang}: {cognate}")
    
    if analysis["word_family"]:
        lines.extend(["", f"Word Family (root: {analysis['word_family']['root']}):"])
        for member in analysis['word_family']['members'][:10]:
            lines.append(f"  • {member}")
    
    lines.extend(["", f"{'='*50}"])
    
    return "\n".join(lines)


# =============================================================================
# Convenience Functions
# =============================================================================

def quick_lookup(word: str) -> str:
    """
    Quick etymology lookup returning a brief summary.
    
    Args:
        word: Word to lookup
        
    Returns:
        Brief summary string
    """
    entry = get_etymology(word)
    if entry:
        origin = entry.language_origin.value
        original = entry.original_form or "unknown"
        period = entry.historical_period.value
        return f"'{word}' from {origin} ({original}), {period} period"
    return f"'{word}' - no etymology data available"


def is_loanword(word: str) -> bool:
    """
    Check if a word is a loanword (borrowed from another language).
    
    Args:
        word: Word to check
        
    Returns:
        True if loanword, False otherwise
    """
    entry = get_etymology(word)
    if entry:
        return entry.language_origin not in [LanguageOrigin.OLD_ENGLISH, LanguageOrigin.GERMANIC]
    return False


def get_loanwords() -> List[str]:
    """
    Get all loanwords in the database.
    
    Returns:
        List of loanword strings
    """
    return [
        entry.word for entry in ETYMOLOGY_DATABASE.values()
        if entry.language_origin not in [LanguageOrigin.OLD_ENGLISH, LanguageOrigin.GERMANIC]
    ]


def get_native_words() -> List[str]:
    """
    Get all native English words in the database.
    
    Returns:
        List of native word strings
    """
    return [
        entry.word for entry in ETYMOLOGY_DATABASE.values()
        if entry.language_origin in [LanguageOrigin.OLD_ENGLISH, LanguageOrigin.GERMANIC]
    ]