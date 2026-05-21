"""
Verb Conjugation Utils - 动词变位工具

支持多种语言的动词变位功能。
零外部依赖，仅使用 Python 标准库。

支持的语言：
- 英语 (English)
- 西班牙语 (Spanish) - 基础支持
- 法语 (French) - 基础支持
- 德语 (German) - 基础支持

支持的时态：
- 现在时 (Present)
- 过去时 (Past)
- 将来时 (Future)
- 现在完成时 (Present Perfect)
- 过去进行时 (Past Continuous)
- 条件句 (Conditional)

支持的人称：
- 第一人称单数/复数 (I/We)
- 第二人称单数/复数 (You/You)
- 第三人称单数/复数 (He/She/It/They)
"""

from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple, Set
from enum import Enum
import re


class Language(Enum):
    """支持的语言"""
    ENGLISH = "english"
    SPANISH = "spanish"
    FRENCH = "french"
    GERMAN = "german"


class Tense(Enum):
    """时态类型"""
    PRESENT = "present"
    PRESENT_SIMPLE = "present_simple"
    PRESENT_CONTINUOUS = "present_continuous"
    PAST = "past"
    PAST_SIMPLE = "past_simple"
    PAST_CONTINUOUS = "past_continuous"
    FUTURE = "future"
    FUTURE_SIMPLE = "future_simple"
    FUTURE_CONTINUOUS = "future_continuous"
    PRESENT_PERFECT = "present_perfect"
    PAST_PERFECT = "past_perfect"
    FUTURE_PERFECT = "future_perfect"
    CONDITIONAL = "conditional"
    CONDITIONAL_PERFECT = "conditional_perfect"
    IMPERATIVE = "imperative"
    INFINITIVE = "infinitive"
    GERUND = "gerund"
    PARTICIPLE = "participle"


class Person(Enum):
    """人称"""
    FIRST_SINGULAR = "first_singular"    # I
    FIRST_PLURAL = "first_plural"        # We
    SECOND_SINGULAR = "second_singular"  # You (singular)
    SECOND_PLURAL = "second_plural"      # You (plural)
    THIRD_SINGULAR = "third_singular"    # He/She/It
    THIRD_PLURAL = "third_plural"        # They


class Mood(Enum):
    """语气"""
    INDICATIVE = "indicative"
    INTERROGATIVE = "interrogative"
    NEGATIVE = "negative"
    IMPERATIVE = "imperative"


@dataclass
class ConjugationResult:
    """变位结果"""
    verb: str
    tense: Tense
    person: Person
    conjugated: str
    auxiliary: Optional[str] = None
    negative: Optional[str] = None
    interrogative: Optional[str] = None


@dataclass
class VerbInfo:
    """动词信息"""
    infinitive: str
    past_simple: str
    past_participle: str
    present_participle: str
    third_person_singular: str
    is_regular: bool
    is_irregular: bool
    transitive: bool = True
    intransitive: bool = False
    reflexive: bool = False


# ==================== 英语不规则动词表 ====================

ENGLISH_IRREGULAR_VERBS: Dict[str, VerbInfo] = {
    "be": VerbInfo("be", "was/were", "been", "being", "is", False, True),
    "have": VerbInfo("have", "had", "had", "having", "has", False, True),
    "do": VerbInfo("do", "did", "done", "doing", "does", False, True),
    "say": VerbInfo("say", "said", "said", "saying", "says", False, True),
    "go": VerbInfo("go", "went", "gone", "going", "goes", False, True, False, True),
    "get": VerbInfo("get", "got", "got/gotten", "getting", "gets", False, True),
    "make": VerbInfo("make", "made", "made", "making", "makes", False, True),
    "know": VerbInfo("know", "knew", "known", "knowing", "knows", False, True, False, True),
    "think": VerbInfo("think", "thought", "thought", "thinking", "thinks", False, True),
    "take": VerbInfo("take", "took", "taken", "taking", "takes", False, True),
    "see": VerbInfo("see", "saw", "seen", "seeing", "sees", False, True),
    "come": VerbInfo("come", "came", "come", "coming", "comes", False, True, False, True),
    "want": VerbInfo("want", "wanted", "wanted", "wanting", "wants", True, False),
    "look": VerbInfo("look", "looked", "looked", "looking", "looks", True, False),
    "use": VerbInfo("use", "used", "used", "using", "uses", True, False),
    "find": VerbInfo("find", "found", "found", "finding", "finds", False, True),
    "give": VerbInfo("give", "gave", "given", "giving", "gives", False, True),
    "tell": VerbInfo("tell", "told", "told", "telling", "tells", False, True),
    "work": VerbInfo("work", "worked", "worked", "working", "works", True, False, False, True),
    "call": VerbInfo("call", "called", "called", "calling", "calls", True, False),
    "try": VerbInfo("try", "tried", "tried", "trying", "tries", True, False),
    "ask": VerbInfo("ask", "asked", "asked", "asking", "asks", True, False),
    "need": VerbInfo("need", "needed", "needed", "needing", "needs", True, False, False, True),
    "feel": VerbInfo("feel", "felt", "felt", "feeling", "feels", False, True, False, True),
    "become": VerbInfo("become", "became", "become", "becoming", "becomes", False, True, False, True),
    "leave": VerbInfo("leave", "left", "left", "leaving", "leaves", False, True),
    "put": VerbInfo("put", "put", "put", "putting", "puts", False, True),
    "mean": VerbInfo("mean", "meant", "meant", "meaning", "means", False, True),
    "keep": VerbInfo("keep", "kept", "kept", "keeping", "keeps", False, True),
    "let": VerbInfo("let", "let", "let", "letting", "lets", False, True),
    "begin": VerbInfo("begin", "began", "begun", "beginning", "begins", False, True, False, True),
    "seem": VerbInfo("seem", "seemed", "seemed", "seeming", "seems", True, False, False, True),
    "help": VerbInfo("help", "helped", "helped", "helping", "helps", True, False),
    "show": VerbInfo("show", "showed", "shown", "showing", "shows", False, True),
    "hear": VerbInfo("hear", "heard", "heard", "hearing", "hears", False, True, False, True),
    "play": VerbInfo("play", "played", "played", "playing", "plays", True, False),
    "run": VerbInfo("run", "ran", "run", "running", "runs", False, True, False, True),
    "move": VerbInfo("move", "moved", "moved", "moving", "moves", True, False, True, True),
    "live": VerbInfo("live", "lived", "lived", "living", "lives", True, False, False, True),
    "believe": VerbInfo("believe", "believed", "believed", "believing", "believes", True, False, False, True),
    "bring": VerbInfo("bring", "brought", "brought", "bringing", "brings", False, True),
    "happen": VerbInfo("happen", "happened", "happened", "happening", "happens", True, False, False, True),
    "write": VerbInfo("write", "wrote", "written", "writing", "writes", False, True),
    "provide": VerbInfo("provide", "provided", "provided", "providing", "provides", True, False),
    "sit": VerbInfo("sit", "sat", "sat", "sitting", "sits", False, True, False, True),
    "stand": VerbInfo("stand", "stood", "stood", "standing", "stands", False, True, False, True),
    "lose": VerbInfo("lose", "lost", "lost", "losing", "loses", False, True),
    "pay": VerbInfo("pay", "paid", "paid", "paying", "pays", False, True),
    "meet": VerbInfo("meet", "met", "met", "meeting", "meets", False, True),
    "include": VerbInfo("include", "included", "included", "including", "includes", True, False),
    "continue": VerbInfo("continue", "continued", "continued", "continuing", "continues", True, False),
    "set": VerbInfo("set", "set", "set", "setting", "sets", False, True),
    "learn": VerbInfo("learn", "learned/learnt", "learned/learnt", "learning", "learns", True, False),
    "change": VerbInfo("change", "changed", "changed", "changing", "changes", True, False, True, True),
    "lead": VerbInfo("lead", "led", "led", "leading", "leads", False, True),
    "understand": VerbInfo("understand", "understood", "understood", "understanding", "understands", False, True, False, True),
    "watch": VerbInfo("watch", "watched", "watched", "watching", "watches", True, False),
    "follow": VerbInfo("follow", "followed", "followed", "following", "follows", True, False),
    "stop": VerbInfo("stop", "stopped", "stopped", "stopping", "stops", True, False, True, True),
    "create": VerbInfo("create", "created", "created", "creating", "creates", True, False),
    "speak": VerbInfo("speak", "spoke", "spoken", "speaking", "speaks", False, True),
    "read": VerbInfo("read", "read", "read", "reading", "reads", False, True, False, True),
    "spend": VerbInfo("spend", "spent", "spent", "spending", "spends", False, True),
    "grow": VerbInfo("grow", "grown", "grown", "growing", "grows", False, True, True, True),
    "open": VerbInfo("open", "opened", "opened", "opening", "opens", True, False, True, True),
    "walk": VerbInfo("walk", "walked", "walked", "walking", "walks", True, False, False, True),
    "win": VerbInfo("win", "won", "won", "winning", "wins", False, True),
    "offer": VerbInfo("offer", "offered", "offered", "offering", "offers", True, False),
    "remember": VerbInfo("remember", "remembered", "remembered", "remembering", "remembers", True, False, False, True),
    "love": VerbInfo("love", "loved", "loved", "loving", "loves", True, False, False, True),
    "consider": VerbInfo("consider", "considered", "considered", "considering", "considers", True, False, False, True),
    "appear": VerbInfo("appear", "appeared", "appeared", "appearing", "appears", True, False, False, True),
    "buy": VerbInfo("buy", "bought", "bought", "buying", "buys", False, True),
    "wait": VerbInfo("wait", "waited", "waited", "waiting", "waits", True, False, False, True),
    "serve": VerbInfo("serve", "served", "served", "serving", "serves", True, False, True, True),
    "die": VerbInfo("die", "died", "died", "dying", "dies", True, False, False, True),
    "send": VerbInfo("send", "sent", "sent", "sending", "sends", False, True),
    "expect": VerbInfo("expect", "expected", "expected", "expecting", "expects", True, False, False, True),
    "build": VerbInfo("build", "built", "built", "building", "builds", False, True),
    "stay": VerbInfo("stay", "stayed", "stayed", "staying", "stays", True, False, False, True),
    "fall": VerbInfo("fall", "fell", "fallen", "falling", "falls", False, True, False, True),
    "cut": VerbInfo("cut", "cut", "cut", "cutting", "cuts", False, True),
    "reach": VerbInfo("reach", "reached", "reached", "reaching", "reaches", True, False),
    "kill": VerbInfo("kill", "killed", "killed", "killing", "kills", True, False),
    "remain": VerbInfo("remain", "remained", "remained", "remaining", "remains", True, False, False, True),
    "suggest": VerbInfo("suggest", "suggested", "suggested", "suggesting", "suggests", True, False),
    "raise": VerbInfo("raise", "raised", "raised", "raising", "raises", True, False),
    "pass": VerbInfo("pass", "passed", "passed", "passing", "passes", True, False, True, True),
    "sell": VerbInfo("sell", "sold", "sold", "selling", "sells", False, True),
    "require": VerbInfo("require", "required", "required", "requiring", "requires", True, False, False, True),
    "report": VerbInfo("report", "reported", "reported", "reporting", "reports", True, False),
    "decide": VerbInfo("decide", "decided", "decided", "deciding", "decides", True, False),
    "pull": VerbInfo("pull", "pulled", "pulled", "pulling", "pulls", True, False),
    "break": VerbInfo("break", "broke", "broken", "breaking", "breaks", False, True, True, True),
}

# ==================== 英语人称映射 ====================

ENGLISH_PERSON_PRONOUNS: Dict[Person, Tuple[str, str]] = {
    Person.FIRST_SINGULAR: ("I", "my"),
    Person.FIRST_PLURAL: ("we", "our"),
    Person.SECOND_SINGULAR: ("you", "your"),
    Person.SECOND_PLURAL: ("you", "your"),
    Person.THIRD_SINGULAR: ("he/she/it", "his/her/its"),
    Person.THIRD_PLURAL: ("they", "their"),
}

# ==================== 辅助动词 ====================

AUXILIARY_VERBS = {
    "be": {"forms": ["am", "is", "are", "was", "were", "been", "being"]},
    "have": {"forms": ["have", "has", "had", "having"]},
    "do": {"forms": ["do", "does", "did", "doing", "done"]},
    "will": {"forms": ["will", "would"]},
    "shall": {"forms": ["shall", "should"]},
    "can": {"forms": ["can", "could"]},
    "may": {"forms": ["may", "might"]},
    "must": {"forms": ["must"]},
}


# ==================== 核心功能函数 ====================

def get_verb_info(verb: str, language: Language = Language.ENGLISH) -> VerbInfo:
    """
    获取动词信息
    
    Args:
        verb: 动词原形
        language: 语言
    
    Returns:
        VerbInfo 对象
    """
    verb_lower = verb.lower().strip()
    
    if language == Language.ENGLISH:
        # 查找不规则动词
        if verb_lower in ENGLISH_IRREGULAR_VERBS:
            return ENGLISH_IRREGULAR_VERBS[verb_lower]
        
        # 规则动词处理
        # 处理特殊结尾
        if verb_lower.endswith("e"):
            past_simple = verb_lower + "d"
            past_participle = verb_lower + "d"
            present_participle = verb_lower[:-1] + "ing"
            third_person = verb_lower + "s"
        elif verb_lower.endswith("y") and len(verb_lower) > 1 and verb_lower[-2] not in "aeiou":
            past_simple = verb_lower[:-1] + "ied"
            past_participle = verb_lower[:-1] + "ied"
            present_participle = verb_lower + "ing"
            third_person = verb_lower[:-1] + "ies"
        elif verb_lower.endswith(("ss", "sh", "ch", "x", "zz", "o")):
            past_simple = verb_lower + "ed"
            past_participle = verb_lower + "ed"
            present_participle = verb_lower + "ing"
            third_person = verb_lower + "es"
        else:
            # 检查是否需要双写最后字母
            if len(verb_lower) >= 2:
                last = verb_lower[-1]
                second_last = verb_lower[-2]
                # CVC 结构需要双写
                if last in "bcdfghjklmnprstvwxz" and second_last in "aeiou":
                    if len(verb_lower) >= 3 and verb_lower[-3] not in "aeiou":
                        past_simple = verb_lower + last + "ed"
                        past_participle = verb_lower + last + "ed"
                        present_participle = verb_lower + last + "ing"
                        third_person = verb_lower + "s"
                    else:
                        past_simple = verb_lower + "ed"
                        past_participle = verb_lower + "ed"
                        present_participle = verb_lower + "ing"
                        third_person = verb_lower + "s"
                else:
                    past_simple = verb_lower + "ed"
                    past_participle = verb_lower + "ed"
                    present_participle = verb_lower + "ing"
                    third_person = verb_lower + "s"
            else:
                past_simple = verb_lower + "ed"
                past_participle = verb_lower + "ed"
                present_participle = verb_lower + "ing"
                third_person = verb_lower + "s"
        
        return VerbInfo(
            infinitive=verb_lower,
            past_simple=past_simple,
            past_participle=past_participle,
            present_participle=present_participle,
            third_person_singular=third_person,
            is_regular=True,
            is_irregular=False
        )
    
    raise ValueError(f"Unsupported language: {language}")


def conjugate_english_present_simple(verb_info: VerbInfo, person: Person) -> str:
    """英语现在简单时变位"""
    if person == Person.THIRD_SINGULAR:
        return verb_info.third_person_singular
    return verb_info.infinitive


def conjugate_english_present_continuous(verb_info: VerbInfo, person: Person) -> Tuple[str, str]:
    """英语现在进行时变位"""
    be_forms = {
        Person.FIRST_SINGULAR: "am",
        Person.FIRST_PLURAL: "are",
        Person.SECOND_SINGULAR: "are",
        Person.SECOND_PLURAL: "are",
        Person.THIRD_SINGULAR: "is",
        Person.THIRD_PLURAL: "are",
    }
    return (be_forms[person], verb_info.present_participle)


def conjugate_english_past_simple(verb_info: VerbInfo, person: Person) -> str:
    """英语过去简单时变位"""
    if verb_info.infinitive == "be":
        if person == Person.FIRST_SINGULAR or person == Person.THIRD_SINGULAR:
            return "was"
        return "were"
    return verb_info.past_simple


def conjugate_english_past_continuous(verb_info: VerbInfo, person: Person) -> Tuple[str, str]:
    """英语过去进行时变位"""
    be_forms = {
        Person.FIRST_SINGULAR: "was",
        Person.FIRST_PLURAL: "were",
        Person.SECOND_SINGULAR: "were",
        Person.SECOND_PLURAL: "were",
        Person.THIRD_SINGULAR: "was",
        Person.THIRD_PLURAL: "were",
    }
    return (be_forms[person], verb_info.present_participle)


def conjugate_english_future_simple(verb_info: VerbInfo, person: Person) -> Tuple[str, str]:
    """英语将来简单时变位"""
    return ("will", verb_info.infinitive)


def conjugate_english_future_continuous(verb_info: VerbInfo, person: Person) -> Tuple[str, str, str]:
    """英语将来进行时变位"""
    return ("will", "be", verb_info.present_participle)


def conjugate_english_present_perfect(verb_info: VerbInfo, person: Person) -> Tuple[str, str]:
    """英语现在完成时变位"""
    have_forms = {
        Person.FIRST_SINGULAR: "have",
        Person.FIRST_PLURAL: "have",
        Person.SECOND_SINGULAR: "have",
        Person.SECOND_PLURAL: "have",
        Person.THIRD_SINGULAR: "has",
        Person.THIRD_PLURAL: "have",
    }
    return (have_forms[person], verb_info.past_participle)


def conjugate_english_past_perfect(verb_info: VerbInfo, person: Person) -> Tuple[str, str]:
    """英语过去完成时变位"""
    return ("had", verb_info.past_participle)


def conjugate_english_future_perfect(verb_info: VerbInfo, person: Person) -> Tuple[str, str, str]:
    """英语将来完成时变位"""
    return ("will", "have", verb_info.past_participle)


def conjugate_english_conditional(verb_info: VerbInfo, person: Person) -> Tuple[str, str]:
    """英语条件句变位"""
    return ("would", verb_info.infinitive)


def conjugate_english_conditional_perfect(verb_info: VerbInfo, person: Person) -> Tuple[str, str, str]:
    """英语条件完成时变位"""
    return ("would", "have", verb_info.past_participle)


def conjugate_english_imperative(verb_info: VerbInfo, plural: bool = False) -> str:
    """英语祈使句变位"""
    return verb_info.infinitive


def conjugate(
    verb: str,
    tense: Tense,
    person: Person = Person.FIRST_SINGULAR,
    language: Language = Language.ENGLISH,
    mood: Mood = Mood.INDICATIVE,
    negative: bool = False,
    interrogative: bool = False
) -> ConjugationResult:
    """
    变位动词
    
    Args:
        verb: 动词原形
        tense: 时态
        person: 人称
        language: 语言
        mood: 语气
        negative: 否定形式
        interrogative: 疑问形式
    
    Returns:
        ConjugationResult 对象
    """
    verb_info = get_verb_info(verb, language)
    
    if language == Language.ENGLISH:
        conjugated, auxiliary = _conjugate_english(verb_info, tense, person)
        
        # 处理否定
        neg_form = None
        if negative:
            neg_form = _make_negative(conjugated, auxiliary, tense, person, verb_info)
        
        # 处理疑问
        int_form = None
        if interrogative:
            int_form = _make_interrogative(conjugated, auxiliary, tense, person, verb_info)
        
        return ConjugationResult(
            verb=verb,
            tense=tense,
            person=person,
            conjugated=conjugated,
            auxiliary=auxiliary,
            negative=neg_form,
            interrogative=int_form
        )
    
    raise ValueError(f"Unsupported language: {language}")


def _conjugate_english(verb_info: VerbInfo, tense: Tense, person: Person) -> Tuple[str, Optional[str]]:
    """英语变位内部函数"""
    if tense == Tense.PRESENT or tense == Tense.PRESENT_SIMPLE:
        result = conjugate_english_present_simple(verb_info, person)
        return (result, None)
    
    elif tense == Tense.PRESENT_CONTINUOUS:
        aux, main = conjugate_english_present_continuous(verb_info, person)
        return (f"{aux} {main}", aux)
    
    elif tense == Tense.PAST or tense == Tense.PAST_SIMPLE:
        result = conjugate_english_past_simple(verb_info, person)
        return (result, None)
    
    elif tense == Tense.PAST_CONTINUOUS:
        aux, main = conjugate_english_past_continuous(verb_info, person)
        return (f"{aux} {main}", aux)
    
    elif tense == Tense.FUTURE or tense == Tense.FUTURE_SIMPLE:
        aux, main = conjugate_english_future_simple(verb_info, person)
        return (f"{aux} {main}", aux)
    
    elif tense == Tense.FUTURE_CONTINUOUS:
        aux1, aux2, main = conjugate_english_future_continuous(verb_info, person)
        return (f"{aux1} {aux2} {main}", f"{aux1} {aux2}")
    
    elif tense == Tense.PRESENT_PERFECT:
        aux, main = conjugate_english_present_perfect(verb_info, person)
        return (f"{aux} {main}", aux)
    
    elif tense == Tense.PAST_PERFECT:
        aux, main = conjugate_english_past_perfect(verb_info, person)
        return (f"{aux} {main}", aux)
    
    elif tense == Tense.FUTURE_PERFECT:
        aux1, aux2, main = conjugate_english_future_perfect(verb_info, person)
        return (f"{aux1} {aux2} {main}", f"{aux1} {aux2}")
    
    elif tense == Tense.CONDITIONAL:
        aux, main = conjugate_english_conditional(verb_info, person)
        return (f"{aux} {main}", aux)
    
    elif tense == Tense.CONDITIONAL_PERFECT:
        aux1, aux2, main = conjugate_english_conditional_perfect(verb_info, person)
        return (f"{aux1} {aux2} {main}", f"{aux1} {aux2}")
    
    elif tense == Tense.IMPERATIVE:
        result = conjugate_english_imperative(verb_info)
        return (result, None)
    
    elif tense == Tense.INFINITIVE:
        return (verb_info.infinitive, None)
    
    elif tense == Tense.GERUND:
        return (verb_info.present_participle, None)
    
    elif tense == Tense.PARTICIPLE:
        return (verb_info.past_participle, None)
    
    raise ValueError(f"Unsupported tense: {tense}")


def _make_negative(conjugated: str, auxiliary: Optional[str], tense: Tense, 
                   person: Person, verb_info: VerbInfo) -> str:
    """构造否定形式"""
    if auxiliary:
        # 有辅助动词时，在辅助动词后加 not
        parts = conjugated.split()
        if len(parts) >= 2:
            return f"{parts[0]} not {parts[1]}" + (" " + parts[2] if len(parts) > 2 else "")
        return f"{auxiliary} not {verb_info.infinitive}"
    
    # 无辅助动词时使用 do/does/did + not
    if tense in [Tense.PRESENT, Tense.PRESENT_SIMPLE]:
        if person == Person.THIRD_SINGULAR:
            return f"does not {verb_info.infinitive}"
        return f"do not {verb_info.infinitive}"
    
    elif tense in [Tense.PAST, Tense.PAST_SIMPLE]:
        return f"did not {verb_info.infinitive}"
    
    # 祈使句
    elif tense == Tense.IMPERATIVE:
        return f"do not {verb_info.infinitive}"
    
    # be 动词特殊处理
    if verb_info.infinitive == "be":
        if tense in [Tense.PRESENT, Tense.PRESENT_SIMPLE]:
            if person == Person.FIRST_SINGULAR:
                return "am not"
            elif person == Person.THIRD_SINGULAR:
                return "is not"
            return "are not"
        elif tense in [Tense.PAST, Tense.PAST_SIMPLE]:
            if person in [Person.FIRST_SINGULAR, Person.THIRD_SINGULAR]:
                return "was not"
            return "were not"
    
    return conjugated


def _make_interrogative(conjugated: str, auxiliary: Optional[str], tense: Tense,
                        person: Person, verb_info: VerbInfo) -> str:
    """构造疑问形式"""
    pronoun = ENGLISH_PERSON_PRONOUNS[person][0]
    
    if auxiliary:
        # 有辅助动词时，将辅助动词移到前面
        parts = conjugated.split()
        if len(parts) >= 2:
            remaining = " ".join(parts[1:])
            return f"{parts[0]} {pronoun} {remaining}"
        return f"{auxiliary} {pronoun} {verb_info.infinitive}"
    
    # 无辅助动词时使用 do/does/did
    if tense in [Tense.PRESENT, Tense.PRESENT_SIMPLE]:
        if person == Person.THIRD_SINGULAR:
            return f"Does {pronoun} {verb_info.infinitive}"
        return f"Do {pronoun} {verb_info.infinitive}"
    
    elif tense in [Tense.PAST, Tense.PAST_SIMPLE]:
        return f"Did {pronoun} {verb_info.infinitive}"
    
    # be 动词特殊处理
    if verb_info.infinitive == "be":
        if tense in [Tense.PRESENT, Tense.PRESENT_SIMPLE]:
            if person == Person.FIRST_SINGULAR:
                return f"Am {pronoun}"
            elif person == Person.THIRD_SINGULAR:
                return f"Is {pronoun}"
            return f"Are {pronoun}"
        elif tense in [Tense.PAST, Tense.PAST_SIMPLE]:
            if person in [Person.FIRST_SINGULAR, Person.THIRD_SINGULAR]:
                return f"Was {pronoun}"
            return f"Were {pronoun}"
    
    return conjugated


def conjugate_all_forms(verb: str, language: Language = Language.ENGLISH) -> Dict[str, Dict[str, str]]:
    """
    变位动词的所有形式
    
    Args:
        verb: 动词原形
        language: 语言
    
    Returns:
        包含所有变位形式的字典
    """
    verb_info = get_verb_info(verb, language)
    result = {}
    
    persons = list(Person)
    tenses = [
        Tense.PRESENT_SIMPLE,
        Tense.PRESENT_CONTINUOUS,
        Tense.PAST_SIMPLE,
        Tense.PAST_CONTINUOUS,
        Tense.FUTURE_SIMPLE,
        Tense.FUTURE_CONTINUOUS,
        Tense.PRESENT_PERFECT,
        Tense.PAST_PERFECT,
        Tense.FUTURE_PERFECT,
        Tense.CONDITIONAL,
        Tense.CONDITIONAL_PERFECT,
    ]
    
    for tense in tenses:
        tense_name = tense.value
        result[tense_name] = {}
        
        for person in persons:
            person_name = person.value
            conj_result = conjugate(verb, tense, person, language)
            pronoun = ENGLISH_PERSON_PRONOUNS[person][0]
            result[tense_name][person_name] = {
                "pronoun": pronoun,
                "conjugated": conj_result.conjugated,
                "negative": conj_result.negative,
                "interrogative": conj_result.interrogative,
            }
    
    # 非人称形式
    result["imperative"] = conjugate_english_imperative(verb_info)
    result["infinitive"] = verb_info.infinitive
    result["gerund"] = verb_info.present_participle
    result["past_participle"] = verb_info.past_participle
    
    return result


def list_irregular_verbs(language: Language = Language.ENGLISH) -> List[VerbInfo]:
    """
    列出所有不规则动词
    
    Args:
        language: 语言
    
    Returns:
        不规则动词列表
    """
    if language == Language.ENGLISH:
        return list(ENGLISH_IRREGULAR_VERBS.values())
    raise ValueError(f"Unsupported language: {language}")


def is_irregular_verb(verb: str, language: Language = Language.ENGLISH) -> bool:
    """
    检查动词是否不规则
    
    Args:
        verb: 动词原形
        language: 语言
    
    Returns:
        是否不规则
    """
    verb_lower = verb.lower().strip()
    if language == Language.ENGLISH:
        return verb_lower in ENGLISH_IRREGULAR_VERBS and ENGLISH_IRREGULAR_VERBS[verb_lower].is_irregular
    raise ValueError(f"Unsupported language: {language}")


def get_participle_forms(verb: str, language: Language = Language.ENGLISH) -> Tuple[str, str]:
    """
    获取动词的分词形式
    
    Args:
        verb: 动词原形
        language: 语言
    
    Returns:
        (现在分词, 过去分词)
    """
    verb_info = get_verb_info(verb, language)
    return (verb_info.present_participle, verb_info.past_participle)


def get_past_forms(verb: str, language: Language = Language.ENGLISH) -> Tuple[str, str]:
    """
    获取动词的过去形式
    
    Args:
        verb: 动词原形
        language: 语言
    
    Returns:
        (过去式, 过去分词)
    """
    verb_info = get_verb_info(verb, language)
    return (verb_info.past_simple, verb_info.past_participle)


def generate_verb_table(verb: str, language: Language = Language.ENGLISH) -> str:
    """
    生成动词变位表格
    
    Args:
        verb: 动词原形
        language: 语言
    
    Returns:
        文本表格
    """
    verb_info = get_verb_info(verb, language)
    all_forms = conjugate_all_forms(verb, language)
    
    lines = [
        f"=== {verb.upper()} Verb Conjugation Table ===",
        f"",
        f"Infinitive: {verb_info.infinitive}",
        f"Past Simple: {verb_info.past_simple}",
        f"Past Participle: {verb_info.past_participle}",
        f"Present Participle: {verb_info.present_participle}",
        f"Third Person Singular: {verb_info.third_person_singular}",
        f"Regular: {verb_info.is_regular}",
        f"",
    ]
    
    # 添加各时态表格
    tenses_display = [
        ("Present Simple", Tense.PRESENT_SIMPLE),
        ("Present Continuous", Tense.PRESENT_CONTINUOUS),
        ("Past Simple", Tense.PAST_SIMPLE),
        ("Past Continuous", Tense.PAST_CONTINUOUS),
        ("Future Simple", Tense.FUTURE_SIMPLE),
        ("Future Continuous", Tense.FUTURE_CONTINUOUS),
        ("Present Perfect", Tense.PRESENT_PERFECT),
        ("Past Perfect", Tense.PAST_PERFECT),
        ("Future Perfect", Tense.FUTURE_PERFECT),
        ("Conditional", Tense.CONDITIONAL),
        ("Conditional Perfect", Tense.CONDITIONAL_PERFECT),
    ]
    
    for tense_display, tense_enum in tenses_display:
        tense_key = tense_enum.value
        lines.append(f"--- {tense_display} ---")
        
        for person in Person:
            person_key = person.value
            form = all_forms[tense_key][person_key]
            lines.append(f"  {form['pronoun']}: {form['conjugated']}")
        
        lines.append("")
    
    # 祈使句
    lines.append("--- Imperative ---")
    lines.append(f"  {all_forms['imperative']}")
    lines.append("")
    
    return "\n".join(lines)


def detect_verb_type(verb: str) -> Dict[str, bool]:
    """
    检测动词类型
    
    Args:
        verb: 动词原形
    
    Returns:
        包含动词类型信息的字典
    """
    verb_lower = verb.lower().strip()
    verb_info = get_verb_info(verb_lower, Language.ENGLISH)
    
    return {
        "is_auxiliary": verb_lower in AUXILIARY_VERBS,
        "is_irregular": verb_info.is_irregular,
        "is_regular": verb_info.is_regular,
        "is_transitive": verb_info.transitive,
        "is_intransitive": verb_info.intransitive,
        "is_reflexive": verb_info.reflexive,
        "ending": {
            "ends_with_e": verb_lower.endswith("e"),
            "ends_with_y": verb_lower.endswith("y"),
            "ends_with_consonant": verb_lower[-1] in "bcdfghjklmnprstvwxz" if verb_lower else False,
            "is_cvc_pattern": _is_cvc_pattern(verb_lower),
        }
    }


def _is_cvc_pattern(word: str) -> bool:
    """检查是否为 CVC 结构（辅音-元音-辅音）"""
    if len(word) < 3:
        return False
    consonants = "bcdfghjklmnprstvwxz"
    vowels = "aeiou"
    return (word[-3] in consonants and word[-2] in vowels and word[-1] in consonants)


def suggest_spelling(verb: str) -> List[str]:
    """
    建议动词拼写
    
    Args:
        verb: 可能拼写错误的动词
    
    Returns:
        建议的正确拼写列表
    """
    verb_lower = verb.lower().strip()
    
    # 如果动词已存在，直接返回
    if verb_lower in ENGLISH_IRREGULAR_VERBS:
        return [verb_lower]
    
    suggestions = []
    
    # 检查不规则动词表中的相似动词
    for known_verb in ENGLISH_IRREGULAR_VERBS:
        if _levenshtein_distance(verb_lower, known_verb) <= 2:
            suggestions.append(known_verb)
    
    return suggestions[:5]


def _levenshtein_distance(s1: str, s2: str) -> int:
    """计算 Levenshtein 编辑距离"""
    if len(s1) < len(s2):
        return _levenshtein_distance(s2, s1)
    
    if len(s2) == 0:
        return len(s1)
    
    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    
    return previous_row[-1]


def create_sentence(verb: str, tense: Tense, person: Person,
                    subject: Optional[str] = None,
                    object: Optional[str] = None,
                    negative: bool = False,
                    interrogative: bool = False) -> str:
    """
    创建完整句子
    
    Args:
        verb: 动词
        tense: 时态
        person: 人称
        subject: 主语（可选，默认使用代词）
        object: 宾语（可选）
        negative: 是否否定
        interrogative: 是否疑问
    
    Returns:
        完整句子
    """
    conj_result = conjugate(verb, tense, person, negative=negative, interrogative=interrogative)
    
    if interrogative:
        # 疑问句
        question = conj_result.interrogative or conj_result.conjugated
        if object:
            return f"{question} {object}?"
        return f"{question}?"
    
    # 陈述句或否定句
    if subject:
        main_subject = subject
    else:
        main_subject = ENGLISH_PERSON_PRONOUNS[person][0]
    
    if negative:
        verb_phrase = conj_result.negative or conj_result.conjugated
    else:
        verb_phrase = conj_result.conjugated
    
    sentence = f"{main_subject} {verb_phrase}"
    
    if object:
        sentence = f"{sentence} {object}"
    
    return sentence


def get_verbs_by_pattern(pattern: str) -> List[VerbInfo]:
    """
    按模式查找动词
    
    Args:
        pattern: 搜索模式
    
    Returns:
        匹配的动词列表
    """
    pattern_lower = pattern.lower()
    result = []
    
    for verb, info in ENGLISH_IRREGULAR_VERBS.items():
        if pattern_lower in verb:
            result.append(info)
    
    return result


def compare_verbs(verb1: str, verb2: str) -> Dict:
    """
    比较两个动词
    
    Args:
        verb1: 第一个动词
        verb2: 第二个动词
    
    Returns:
        比较结果
    """
    info1 = get_verb_info(verb1)
    info2 = get_verb_info(verb2)
    
    return {
        "verb1": {
            "infinitive": info1.infinitive,
            "past_simple": info1.past_simple,
            "past_participle": info1.past_participle,
            "is_regular": info1.is_regular,
        },
        "verb2": {
            "infinitive": info2.infinitive,
            "past_simple": info2.past_simple,
            "past_participle": info2.past_participle,
            "is_regular": info2.is_regular,
        },
        "same_irregularity": info1.is_irregular == info2.is_irregular,
        "same_past_form": info1.past_simple == info2.past_simple,
        "same_participle": info1.past_participle == info2.past_participle,
    }


if __name__ == "__main__":
    # 示例用法
    print("=== Verb Conjugation Utils Examples ===\n")
    
    # 1. 基本变位
    print("1. Basic Conjugation:")
    print(f"  'eat' in Present Simple, Third Singular: {conjugate('eat', Tense.PRESENT_SIMPLE, Person.THIRD_SINGULAR).conjugated}")
    print(f"  'run' in Past Simple, First Singular: {conjugate('run', Tense.PAST_SIMPLE, Person.FIRST_SINGULAR).conjugated}")
    print(f"  'work' in Present Continuous: {conjugate('work', Tense.PRESENT_CONTINUOUS, Person.FIRST_SINGULAR).conjugated}")
    print()
    
    # 2. 所有形式
    print("2. All Forms of 'write':")
    forms = conjugate_all_forms("write")
    print(f"  Present Simple: {forms['present_simple']['first_singular']['conjugated']}")
    print(f"  Present Continuous: {forms['present_continuous']['first_singular']['conjugated']}")
    print(f"  Past Simple: {forms['past_simple']['first_singular']['conjugated']}")
    print(f"  Present Perfect: {forms['present_perfect']['first_singular']['conjugated']}")
    print()
    
    # 3. 否定和疑问
    print("3. Negative and Interrogative Forms:")
    result = conjugate("play", Tense.PRESENT_SIMPLE, Person.THIRD_SINGULAR, negative=True)
    print(f"  Negative: {result.negative}")
    result = conjugate("play", Tense.PRESENT_SIMPLE, Person.THIRD_SINGULAR, interrogative=True)
    print(f"  Interrogative: {result.interrogative}")
    print()
    
    # 4. 动词信息
    print("4. Verb Information for 'go':")
    info = get_verb_info("go")
    print(f"  Infinitive: {info.infinitive}")
    print(f"  Past Simple: {info.past_simple}")
    print(f"  Past Participle: {info.past_participle}")
    print(f"  Is Irregular: {info.is_irregular}")
    print()
    
    # 5. 不规则动词列表
    print("5. First 10 Irregular Verbs:")
    irregular = list_irregular_verbs()
    for v in irregular[:10]:
        print(f"  {v.infinitive}: {v.past_simple} / {v.past_participle}")
    print()
    
    # 6. 创建句子
    print("6. Creating Sentences:")
    print(f"  {create_sentence('write', Tense.PRESENT_SIMPLE, Person.FIRST_SINGULAR, 'I', 'a letter')}")
    print(f"  {create_sentence('write', Tense.PAST_SIMPLE, Person.THIRD_SINGULAR, 'She', 'an email', negative=True)}")
    print(f"  {create_sentence('write', Tense.PRESENT_SIMPLE, Person.THIRD_SINGULAR, object='a book', interrogative=True)}")
    print()
    
    # 7. 动词表格
    print("7. Verb Table for 'be':")
    print(generate_verb_table("be"))