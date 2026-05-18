"""
Kaomoji Utils - 日式颜文字工具集

提供丰富的日式颜文字表情（Kaomoji），支持按情绪分类、随机获取、关键词搜索等功能。
零外部依赖，纯 Python 实现。

使用示例:
    >>> from kaomoji_utils import get_random, get_by_emotion, search
    >>> get_random()
    '(◕‿◕)'
    >>> get_by_emotion('happy')
    ['(◕‿◕)', '(｡♥‿♥｡)', '(✿◠‿◠)']
    >>> search('love')
    ['(｡♥‿♥｡)', '(♥ω♥*)', '(´,,•ω•,,)♥']
"""

from typing import List, Dict, Optional
import random
from dataclasses import dataclass


@dataclass
class KaomojiEntry:
    """颜文字条目"""
    kaomoji: str
    emotion: str
    keywords: List[str]
    description: str


# 颜文字数据库 - 按情绪分类
KAOMOJI_DATABASE: Dict[str, List[KaomojiEntry]] = {
    "happy": [
        KaomojiEntry("(◕‿◕)", "happy", ["happy", "joy", "smile"], "开心微笑"),
        KaomojiEntry("(｡♥‿♥｡)", "happy", ["happy", "love", "joy"], "幸福开心"),
        KaomojiEntry("(✿◠‿◠)", "happy", ["happy", "cute", "smile"], "可爱微笑"),
        KaomojiEntry("(≧◡≦)", "happy", ["happy", "excited", "joy"], "兴奋开心"),
        KaomojiEntry("ヽ(>∀<☆)ノ", "happy", ["happy", "excited", "celebrate"], "欢庆"),
        KaomojiEntry("(ﾉ◕ヮ◕)ﾉ*:・ﾟ✧", "happy", ["happy", "sparkle", "magic"], "闪烁开心"),
        KaomojiEntry("(｡◕‿◕｡)", "happy", ["happy", "cute", "smile"], "可爱开心"),
        KaomojiEntry("(*≧ω≦*)", "happy", ["happy", "cute", "excited"], "激动开心"),
        KaomojiEntry("(◠‿◠)", "happy", ["happy", "smile", "peaceful"], "平和微笑"),
        KaomojiEntry("(ﾉ´▽`)ﾉ♪", "happy", ["happy", "sing", "music"], "唱歌开心"),
        KaomojiEntry("٩(◕‿◕｡)۶", "happy", ["happy", "celebrate", "yay"], "庆祝"),
        KaomojiEntry("(✧ω✧)", "happy", ["happy", "shiny", "sparkle"], "闪耀"),
        KaomojiEntry("(*´▽`*)", "happy", ["happy", "content", "pleased"], "满足"),
        KaomojiEntry("(´▽`ʃ♡ƪ)", "happy", ["happy", "love", "pleased"], "愉悦"),
        KaomojiEntry("(∩˃o˂∩)♡", "happy", ["happy", "love", "cute"], "幸福"),
    ],
    "love": [
        KaomojiEntry("(♥ω♥*)", "love", ["love", "heart", "romance"], "爱心"),
        KaomojiEntry("(´,,•ω•,,)♥", "love", ["love", "shy", "heart"], "害羞爱意"),
        KaomojiEntry("(⁄ ⁄•⁄ω⁄•⁄ ⁄)", "love", ["love", "shy", "blush"], "害羞"),
        KaomojiEntry("(人´∀`)☆", "love", ["love", "thank", "grateful"], "感谢"),
        KaomojiEntry("♡(◡‿◡)", "love", ["love", "heart", "cute"], "爱心可爱"),
        KaomojiEntry("(´∀｀)♡", "love", ["love", "heart", "warm"], "温暖爱意"),
        KaomojiEntry("(￣３￣)❤", "love", ["love", "kiss", "heart"], "亲吻"),
        KaomojiEntry("(灬º‿º灬)♡", "love", ["love", "blush", "heart"], "脸红爱意"),
        KaomojiEntry("(人´▽`)♥", "love", ["love", "thank", "heart"], "感谢爱意"),
        KaomojiEntry("♡＾▽＾♡", "love", ["love", "happy", "heart"], "甜蜜"),
        KaomojiEntry("(๑♡⌓♡๑)", "love", ["love", "heart", "excited"], "心动"),
        KaomojiEntry("(人 ◕‿◕)", "love", ["love", "hug", "cute"], "拥抱"),
        KaomojiEntry("(*^^*)♡", "love", ["love", "shy", "blush"], "害羞爱"),
        KaomojiEntry("(◕‿◕)♡", "love", ["love", "heart", "smile"], "微笑爱心"),
        KaomojiEntry("(´,,•ω•,,)", "love", ["love", "shy", "cute"], "害羞"),
    ],
    "sad": [
        KaomojiEntry("(╥_╥)", "sad", ["sad", "cry", "tears"], "哭泣"),
        KaomojiEntry("(´;ω;`)", "sad", ["sad", "cry", "tears"], "伤心哭泣"),
        KaomojiEntry("(╯︵╰,)", "sad", ["sad", "down", "disappointed"], "失望"),
        KaomojiEntry("(ノД`)・゜・。", "sad", ["sad", "cry", "sob"], "抽泣"),
        KaomojiEntry("(◞‸◟)", "sad", ["sad", "down", "gloomy"], "忧郁"),
        KaomojiEntry("(´°̥̥̥̥̥̥̥̥ω°̥̥̥̥̥̥̥̥`)", "sad", ["sad", "cry", "sobbing"], "痛哭"),
        KaomojiEntry("(｡•́︿•̀｡)", "sad", ["sad", "upset", "hurt"], "受伤"),
        KaomojiEntry("(◞‸◟;)", "sad", ["sad", "awkward", "sweat"], "尴尬悲伤"),
        KaomojiEntry("(´°̥̥̥̥̥̥̥̥ѡ°̥̥̥̥̥̥̥̥`)", "sad", ["sad", "cry", "bawling"], "大哭"),
        KaomojiEntry("(╯_╰)", "sad", ["sad", "down", "depressed"], "沮丧"),
        KaomojiEntry("(´•ω•̥`)", "sad", ["sad", "tears", "upset"], "委屈"),
        KaomojiEntry("(・_・;)", "sad", ["sad", "upset", "disappointed"], "难过"),
        KaomojiEntry("(ノ_<。)", "sad", ["sad", "cry", "tears"], "流泪"),
        KaomojiEntry("(´-ω-`)", "sad", ["sad", "lonely", "empty"], "空虚"),
    ],
    "angry": [
        KaomojiEntry("(╬ Ò﹏Ó)", "angry", ["angry", "mad", "furious"], "愤怒"),
        KaomojiEntry("(ノಠ益ಠ)ノ彡┻━┻", "angry", ["angry", "flip", "table"], "掀桌"),
        KaomojiEntry("(╯°□°)╯︵ ┻━┻", "angry", ["angry", "flip", "table"], "掀桌愤怒"),
        KaomojiEntry("(≧Д≦)", "angry", ["angry", "mad", "frustrated"], "沮丧愤怒"),
        KaomojiEntry("(｀Д´)", "angry", ["angry", "mad", "yell"], "大喊"),
        KaomojiEntry("(╬▔皿▔)╯", "angry", ["angry", "mad", "furious"], "暴怒"),
        KaomojiEntry("(ノ°Д°)ノ︵┻━┻", "angry", ["angry", "table", "flip"], "愤怒掀桌"),
        KaomojiEntry("(≧ヘ≦)", "angry", ["angry", "mad", "annoyed"], "恼火"),
        KaomojiEntry("(｀ε´)", "angry", ["angry", "mad", "pout"], "撇嘴生气"),
        KaomojiEntry("(╬￣皿￣)=○", "angry", ["angry", "punch", "mad"], "出拳"),
        KaomojiEntry("( ` ω ´ )", "angry", ["angry", "mad", "annoyed"], "不爽"),
        KaomojiEntry("凸(￣ヘ￣)", "angry", ["angry", "finger", "mad"], "竖中指"),
        KaomojiEntry("ヽ(`Д´)ノ", "angry", ["angry", "yell", "mad"], "咆哮"),
        KaomojiEntry("(￣皿￣)", "angry", ["angry", "annoyed", "irritated"], "烦躁"),
    ],
    "surprised": [
        KaomojiEntry("(°o°)", "surprised", ["surprised", "shock", "wow"], "惊讶"),
        KaomojiEntry("(⊙_⊙)", "surprised", ["surprised", "shock", "stare"], "瞪大眼"),
        KaomojiEntry("(°△°|||)", "surprised", ["surprised", "shock", "sweat"], "震惊出汗"),
        KaomojiEntry("(゜ロ゜)", "surprised", ["surprised", "shock", "wow"], "惊讶张嘴"),
        KaomojiEntry("(ﾟДﾟ)", "surprised", ["surprised", "shock", "what"], "震惊"),
        KaomojiEntry("(O_O)", "surprised", ["surprised", "shock", "stare"], "惊讶凝视"),
        KaomojiEntry("(◎_◎;)", "surprised", ["surprised", "shock", "sweat"], "惊讶出汗"),
        KaomojiEntry("(°o°;)", "surprised", ["surprised", "shock", "nervous"], "紧张惊讶"),
        KaomojiEntry("(゜Д゜)", "surprised", ["surprised", "shock", "what"], "惊讶什么"),
        KaomojiEntry("(⊙°⊙)", "surprised", ["surprised", "shock", "wow"], "圆眼惊讶"),
        KaomojiEntry("(°∀°)ﾉ", "surprised", ["surprised", "wave", "wow"], "惊讶挥手"),
        KaomojiEntry("(ﾟДﾟ;)", "surprised", ["surprised", "shock", "sweat"], "震惊出汗"),
        KaomojiEntry("(゜∀゜)", "surprised", ["surprised", "shock", "amazed"], "惊奇"),
        KaomojiEntry("(°Δ°)", "surprised", ["surprised", "shock", "wow"], "惊讶张嘴"),
        KaomojiEntry("(ʘ言ʘ)", "surprised", ["surprised", "shock", "speechless"], "无言惊讶"),
    ],
    "cute": [
        KaomojiEntry("(◕ᴗ◕✿)", "cute", ["cute", "flower", "sweet"], "花朵可爱"),
        KaomojiEntry("(｡◕‿◕｡)", "cute", ["cute", "happy", "sweet"], "甜蜜可爱"),
        KaomojiEntry("(*≧ω≦)", "cute", ["cute", "happy", "excited"], "激动可爱"),
        KaomojiEntry("(◕‿◕)♡", "cute", ["cute", "love", "heart"], "爱心可爱"),
        KaomojiEntry("(◠‿◠)", "cute", ["cute", "happy", "smile"], "微笑可爱"),
        KaomojiEntry("(´・ω・`)", "cute", ["cute", "shy", "soft"], "害羞可爱"),
        KaomojiEntry("(◕‿◕✿)", "cute", ["cute", "flower", "sweet"], "花朵甜蜜"),
        KaomojiEntry("(*^‿^*)", "cute", ["cute", "happy", "smile"], "开心可爱"),
        KaomojiEntry("(◠ω◠)", "cute", ["cute", "cat", "mouth"], "猫咪嘴"),
        KaomojiEntry("(*´∀`*)", "cute", ["cute", "happy", "pleased"], "开心满足"),
        KaomojiEntry("(◕‿-)", "cute", ["cute", "wink", "flirty"], "眨眼可爱"),
        KaomojiEntry("(◠ᴗ◠✿)", "cute", ["cute", "flower", "sweet"], "甜美花朵"),
        KaomojiEntry("(*´ω`*)", "cute", ["cute", "soft", "happy"], "柔软可爱"),
        KaomojiEntry("(◕ω◕✿)", "cute", ["cute", "flower", "cat"], "花朵猫咪"),
    ],
    "shy": [
        KaomojiEntry("(⁄ ⁄•⁄ω⁄•⁄ ⁄)", "shy", ["shy", "blush", "love"], "害羞脸红"),
        KaomojiEntry("(´,,•ω•,,)", "shy", ["shy", "blush", "cute"], "害羞可爱"),
        KaomojiEntry("(*^^*)", "shy", ["shy", "blush", "embarrassed"], "尴尬脸红"),
        KaomojiEntry("(⁄ ⁄>⁄ ▽ ⁄<⁄ ⁄)", "shy", ["shy", "blush", "embarrassed"], "害羞"),
        KaomojiEntry("( ´ ▽ ` )ﾉ", "shy", ["shy", "wave", "greeting"], "害羞问候"),
        KaomojiEntry("(*´▽`*)", "shy", ["shy", "blush", "happy"], "害羞开心"),
        KaomojiEntry("(灬º‿º灬)", "shy", ["shy", "blush", "love"], "脸红害羞"),
        KaomojiEntry("(⁄●⁄﹏⁄●⁄)", "shy", ["shy", "blush", "embarrassed"], "尴尬"),
        KaomojiEntry("(´ω｀)", "shy", ["shy", "soft", "quiet"], "害羞安静"),
        KaomojiEntry("(*´﹃｀*)", "shy", ["shy", "blush", "dreamy"], "害羞梦幻"),
        KaomojiEntry("(⁄✿⁄•⁄ω⁄•⁄✿⁄)", "shy", ["shy", "blush", "flower"], "花朵害羞"),
        KaomojiEntry("(´,,•ω•,,)♡", "shy", ["shy", "love", "blush"], "害羞爱意"),
        KaomojiEntry("(*´∀`*)", "shy", ["shy", "happy", "blush"], "开心害羞"),
        KaomojiEntry("(⁄ ⁄≧⁄▽⁄≦⁄ ⁄)", "shy", ["shy", "excited", "blush"], "激动害羞"),
        KaomojiEntry("(´-ω-`)", "shy", ["shy", "soft", "quiet"], "害羞安静"),
    ],
    "wink": [
        KaomojiEntry("(◕‿-)", "wink", ["wink", "flirty", "cute"], "眨眼"),
        KaomojiEntry("(^_−)☆", "wink", ["wink", "star", "cute"], "眨眼星星"),
        KaomojiEntry("(;-;)", "wink", ["wink", "sweat", "nervous"], "紧张眨眼"),
        KaomojiEntry("( ◕‿-)", "wink", ["wink", "flirty", "smile"], "调皮眨眼"),
        KaomojiEntry("( ◕ ᴗ ◕ )", "wink", ["wink", "cute", "happy"], "可爱眨眼"),
        KaomojiEntry("(*^‿^*)", "wink", ["wink", "happy", "smile"], "开心眨眼"),
        KaomojiEntry("( ◕‿◕ )", "wink", ["wink", "happy", "cute"], "快乐眨眼"),
        KaomojiEntry("(╹ڡ╹ )", "wink", ["wink", "cute", "blush"], "脸红眨眼"),
    ],
    "table_flip": [
        KaomojiEntry("(╯°□°)╯︵ ┻━┻", "table_flip", ["table", "flip", "angry"], "掀桌"),
        KaomojiEntry("(ノಠ益ಠ)ノ彡┻━┻", "table_flip", ["table", "flip", "angry"], "愤怒掀桌"),
        KaomojiEntry("(╯°Д°)╯︵ /(.□ . \\)", "table_flip", ["table", "flip", "person"], "掀人"),
        KaomojiEntry("(ノ°Д°)ノ︵┻━┻", "table_flip", ["table", "flip", "mad"], "疯狂掀桌"),
        KaomojiEntry("(╯ಠ益ಠ)╯彡┻━┻", "table_flip", ["table", "flip", "rage"], "暴怒掀桌"),
        KaomojiEntry("(ノಥ,_｣ಥ)ノ︵┻━┻", "table_flip", ["table", "flip", "cry"], "哭泣掀桌"),
        KaomojiEntry("(╯‵□′)╯︵┻━┻", "table_flip", ["table", "flip", "angry"], "愤怒掀桌"),
        KaomojiEntry("(ノ｀Д)ノ︵┻━┻", "table_flip", ["table", "flip", "mad"], "生气掀桌"),
        KaomojiEntry("(╯°□°）╯︵ ┻━┻", "table_flip", ["table", "flip", "angry"], "经典掀桌"),
    ],
    "greeting": [
        KaomojiEntry("(｡◕‿◕｡)ノ", "greeting", ["hello", "hi", "wave"], "你好"),
        KaomojiEntry("(◕‿◕)ノ", "greeting", ["hello", "hi", "wave"], "打招呼"),
        KaomojiEntry("ヽ(>∀<☆)ノ", "greeting", ["hello", "hi", "welcome"], "欢迎"),
        KaomojiEntry("( ^▽^ )ノ", "greeting", ["hello", "hi", "bye"], "问候"),
        KaomojiEntry("(´▽`ʃ♡ƪ)", "greeting", ["thank", "thanks", "love"], "感谢"),
        KaomojiEntry("(◠‿◠)ノ", "greeting", ["hello", "hi", "wave"], "挥手问好"),
        KaomojiEntry("(人´∀`)☆", "greeting", ["thank", "thanks", "grateful"], "感谢"),
        KaomojiEntry("(*´▽`*)ノ", "greeting", ["hello", "hi", "bye"], "开心问候"),
        KaomojiEntry("(✿◠‿◠)ノ", "greeting", ["hello", "hi", "welcome"], "花朵欢迎"),
        KaomojiEntry("( ◕‿◕)ノ", "greeting", ["hello", "hi", "wave"], "可爱问候"),
    ],
    "sorry": [
        KaomojiEntry("(´・ω・`)", "sorry", ["sorry", "apologize", "sad"], "道歉"),
        KaomojiEntry("(；′⌒`)", "sorry", ["sorry", "apologize", "cry"], "哭泣道歉"),
        KaomojiEntry("(人 •͈ᴗ•͈)", "sorry", ["sorry", "apologize", "bow"], "鞠躬道歉"),
        KaomojiEntry("(´；ω；`)", "sorry", ["sorry", "apologize", "cry"], "伤心道歉"),
        KaomojiEntry("(>人<)", "sorry", ["sorry", "apologize", "bow"], "深深鞠躬"),
        KaomojiEntry("(´°̥̥̥̥̥̥̥̥ω°̥̥̥̥̥̥̥̥`)", "sorry", ["sorry", "apologize", "cry"], "痛哭道歉"),
        KaomojiEntry("(人´Д`)", "sorry", ["sorry", "apologize", "bow"], "诚恳道歉"),
        KaomojiEntry("(；ω；)", "sorry", ["sorry", "apologize", "tears"], "流泪道歉"),
    ],
    "confused": [
        KaomojiEntry("(・_・;)", "confused", ["confused", "sweat", "awkward"], "困惑出汗"),
        KaomojiEntry("(・_・)", "confused", ["confused", "what", "puzzled"], "困惑"),
        KaomojiEntry("(°△°)", "confused", ["confused", "what", "puzzled"], "疑惑"),
        KaomojiEntry("(・_・ヾ", "confused", ["confused", "what", "sweat"], "困惑"),
        KaomojiEntry("(・∀・)", "confused", ["confused", "what", "huh"], "疑惑不解"),
        KaomojiEntry("(´・ω・`)?", "confused", ["confused", "question", "what"], "困惑问号"),
        KaomojiEntry("(・_・;)?", "confused", ["confused", "question", "sweat"], "困惑问号"),
        KaomojiEntry("(°_°)", "confused", ["confused", "blank", "stare"], "茫然"),
        KaomojiEntry("(・・;)", "confused", ["confused", "sweat", "awkward"], "尴尬困惑"),
        KaomojiEntry("(・・?)", "confused", ["confused", "question", "puzzled"], "疑惑问号"),
    ],
    "sleepy": [
        KaomojiEntry("(´-ω-`)zzZ", "sleepy", ["sleepy", "tired", "sleep"], "困倦"),
        KaomojiEntry("(๑ᵕ⌓ᵕ̤)", "sleepy", ["sleepy", "tired", "yawn"], "打哈欠"),
        KaomojiEntry("(´-ω-`)", "sleepy", ["sleepy", "tired", "relaxed"], "放松困倦"),
        KaomojiEntry("(￣o￣)", "sleepy", ["sleepy", "tired", "yawn"], "打哈欠"),
        KaomojiEntry("(－ω－) zzZ", "sleepy", ["sleepy", "sleep", "tired"], "睡觉"),
        KaomojiEntry("(￣ー￣)", "sleepy", ["sleepy", "tired", "relaxed"], "放松"),
        KaomojiEntry("(´〜｀)", "sleepy", ["sleepy", "tired", "relaxed"], "困倦放松"),
        KaomojiEntry("(๑•̀ㅂ•́)و✧", "sleepy", ["sleepy", "tired", "exhausted"], "疲惫"),
        KaomojiEntry("(－ω－)", "sleepy", ["sleepy", "tired", "sleep"], "困了"),
        KaomojiEntry("(￣ω￣)", "sleepy", ["sleepy", "tired", "relaxed"], "困倦放松"),
    ],
    "excited": [
        KaomojiEntry("٩(◕‿◕｡)۶", "excited", ["excited", "yay", "celebrate"], "庆祝"),
        KaomojiEntry("ヽ(>∀<☆)ノ", "excited", ["excited", "yay", "happy"], "兴奋"),
        KaomojiEntry("(*≧▽≦)", "excited", ["excited", "happy", "yay"], "激动开心"),
        KaomojiEntry("ヽ(゜▽゜;)ノ", "excited", ["excited", "happy", "celebrate"], "欢庆"),
        KaomojiEntry("(≧◡≦)", "excited", ["excited", "happy", "yay"], "开心兴奋"),
        KaomojiEntry("(*≧ω≦*)", "excited", ["excited", "happy", "cute"], "激动可爱"),
        KaomojiEntry("ヽ(✿ﾟ▽ﾟ)ノ", "excited", ["excited", "happy", "celebrate"], "庆祝兴奋"),
        KaomojiEntry("(ﾉ◕ヮ◕)ﾉ*:・ﾟ✧", "excited", ["excited", "magic", "sparkle"], "魔法闪烁"),
        KaomojiEntry("٩(๑>◡<๑)۶", "excited", ["excited", "happy", "yay"], "欢呼"),
        KaomojiEntry("ヽ(´▽`)/", "excited", ["excited", "happy", "celebrate"], "庆祝开心"),
    ],
    "cat": [
        KaomojiEntry("(=^･ω･^=)", "cat", ["cat", "kitten", "cute"], "猫咪"),
        KaomojiEntry("(=①ω①=)", "cat", ["cat", "kitten", "cute"], "可爱猫咪"),
        KaomojiEntry("(=^.ω.^=)", "cat", ["cat", "kitten", "cute"], "小猫"),
        KaomojiEntry("(=｀ω´=)", "cat", ["cat", "kitten", "cute"], "猫咪表情"),
        KaomojiEntry("(=^･ｪ･^=)", "cat", ["cat", "kitten", "cute"], "可爱小猫"),
        KaomojiEntry("ฅ^•ﻌ•^ฅ", "cat", ["cat", "kitten", "cute"], "小猫咪"),
        KaomojiEntry("ฅ(• ɪ •)ฅ", "cat", ["cat", "kitten", "cute"], "可爱猫咪"),
        KaomojiEntry("( =ω= )", "cat", ["cat", "kitten", "cute"], "猫咪"),
        KaomojiEntry("ฅ(• ω •)ฅ", "cat", ["cat", "kitten", "cute"], "小猫"),
        KaomojiEntry("( =①ω①=)", "cat", ["cat", "kitten", "cute"], "猫咪表情"),
    ],
    "bear": [
        KaomojiEntry("( ˘ᴥ˘ )", "bear", ["bear", "cute", "animal"], "熊"),
        KaomojiEntry("ʕ•ᴥ•ʔ", "bear", ["bear", "cute", "animal"], "可爱熊"),
        KaomojiEntry("ʕ•ᴥ•ʔﾉ♡", "bear", ["bear", "love", "cute"], "爱心熊"),
        KaomojiEntry("( ´(00)` )", "bear", ["bear", "cute", "animal"], "小熊"),
        KaomojiEntry("ʕᵔᴥᵔʔ", "bear", ["bear", "cute", "animal"], "可爱熊"),
        KaomojiEntry("ʕ·ᴥ·ʔ", "bear", ["bear", "cute", "animal"], "熊熊"),
        KaomojiEntry("( ◔ ursos ◔ )", "bear", ["bear", "cute", "animal"], "小熊"),
        KaomojiEntry("ʕ≧ᴥ≦ʔ", "bear", ["bear", "cute", "happy"], "开心熊"),
        KaomojiEntry("ʕ•̫͡•ʔ", "bear", ["bear", "cute", "animal"], "可爱熊"),
        KaomojiEntry("( ˘ᴥ˘ )っ♡", "bear", ["bear", "love", "cute"], "爱心小熊"),
    ],
    "flower": [
        KaomojiEntry("(◕‿◕✿)", "flower", ["flower", "cute", "spring"], "花朵"),
        KaomojiEntry("(✿◠‿◠)", "flower", ["flower", "cute", "spring"], "可爱花朵"),
        KaomojiEntry("✿◕ ‿ ◕✿", "flower", ["flower", "cute", "spring"], "小花"),
        KaomojiEntry("(◕ᴗ◕✿)", "flower", ["flower", "cute", "spring"], "可爱小花"),
        KaomojiEntry("❀◕ ‿ ◕❀", "flower", ["flower", "cute", "spring"], "花朵"),
        KaomojiEntry("(✿╹◡╹)", "flower", ["flower", "cute", "spring"], "小花"),
        KaomojiEntry("✿◠‿◠✿", "flower", ["flower", "cute", "spring"], "可爱花朵"),
        KaomojiEntry("(◠ᴗ◠✿)", "flower", ["flower", "cute", "spring"], "花朵可爱"),
        KaomojiEntry("(◕ω◕✿)", "flower", ["flower", "cute", "spring"], "小花可爱"),
        KaomojiEntry("❀◕ᴗ◕❀", "flower", ["flower", "cute", "spring"], "可爱花朵"),
    ],
    "food": [
        KaomojiEntry("( ˘▽˘)っ♨", "food", ["food", "eat", "hungry"], "吃饭"),
        KaomojiEntry("(っ˘ڡ˘ς)", "food", ["food", "eat", "yummy"], "好吃"),
        KaomojiEntry("( ^▽^)っψ🍜", "food", ["food", "noodle", "eat"], "吃面"),
        KaomojiEntry("( ˘ω˘ )っ☕", "food", ["food", "coffee", "drink"], "喝咖啡"),
        KaomojiEntry("( ^▽^)っ🍕", "food", ["food", "pizza", "eat"], "吃披萨"),
        KaomojiEntry("(っ˘ڡ˘ς)🍩", "food", ["food", "donut", "eat"], "吃甜甜圈"),
        KaomojiEntry("( ˘ω˘ )っ🍵", "food", ["food", "tea", "drink"], "喝茶"),
        KaomojiEntry("( ^▽^)っ🍰", "food", ["food", "cake", "eat"], "吃蛋糕"),
        KaomojiEntry("(っ˘ڡ˘ς)🍔", "food", ["food", "burger", "eat"], "吃汉堡"),
        KaomojiEntry("( ˘ω˘ )っ🍱", "food", ["food", "bento", "eat"], "吃便当"),
    ],
    "music": [
        KaomojiEntry("(ﾉ´▽`)ﾉ♪", "music", ["music", "sing", "song"], "唱歌"),
        KaomojiEntry("ヽ(・∀・)ﾉ♬", "music", ["music", "sing", "song"], "欢唱"),
        KaomojiEntry("(´▽`ʃ♪)", "music", ["music", "sing", "song"], "歌唱"),
        KaomojiEntry("♪┏(・o･)┛♪", "music", ["music", "dance", "song"], "跳舞唱歌"),
        KaomojiEntry("( ^▽^)っ♪", "music", ["music", "sing", "song"], "唱歌"),
        KaomojiEntry("♬♩♪♩ ♪♩♬", "music", ["music", "note", "song"], "音符"),
        KaomojiEntry("ヽ(♪ ∇_∇)ﾉ", "music", ["music", "sing", "song"], "欢唱"),
        KaomojiEntry("(≧◡≦) ♡♪♡", "music", ["music", "love", "song"], "爱音乐"),
        KaomojiEntry("♫꒰･◡･꒱", "music", ["music", "sing", "song"], "唱歌"),
        KaomojiEntry("(￣▽￣)ﾉ♪", "music", ["music", "sing", "song"], "歌唱"),
    ],
    "fight": [
        KaomojiEntry("(ง •̀_•́)ง", "fight", ["fight", "battle", "ready"], "准备战斗"),
        KaomojiEntry("ง(•̀_•́)ง", "fight", ["fight", "battle", "ready"], "战斗姿态"),
        KaomojiEntry("(ง •̀ω•́)ง", "fight", ["fight", "battle", "ready"], "战斗准备"),
        KaomojiEntry("(ง •̀o•́)ง", "fight", ["fight", "battle", "ready"], "斗志昂扬"),
        KaomojiEntry("(ง •̀Θ•́)ง", "fight", ["fight", "battle", "ready"], "战斗"),
        KaomojiEntry("٩(╬ʘ益ʘ╬)۶", "fight", ["fight", "battle", "angry"], "愤怒战斗"),
        KaomojiEntry("(ง `ω´ )ง", "fight", ["fight", "battle", "ready"], "战斗模式"),
        KaomojiEntry("ง( ` ω ´ )ง", "fight", ["fight", "battle", "ready"], "战斗准备"),
        KaomojiEntry("(ง •̀∀•́)ง", "fight", ["fight", "battle", "ready"], "战斗姿态"),
        KaomojiEntry("٩(•̀ᴗ•́)و", "fight", ["fight", "battle", "victory"], "胜利姿态"),
    ],
    "magic": [
        KaomojiEntry("(ﾉ◕ヮ◕)ﾉ*:・ﾟ✧", "magic", ["magic", "sparkle", "wand"], "魔法"),
        KaomojiEntry("✧･ﾟ: *✧･ﾟ:*  *:･ﾟ✧*:･ﾟ✧", "magic", ["magic", "sparkle", "star"], "闪烁星星"),
        KaomojiEntry("(✧ω✧)", "magic", ["magic", "sparkle", "shiny"], "闪耀"),
        KaomojiEntry("ヽ(✿ﾟ▽ﾟ)ノ", "magic", ["magic", "sparkle", "cute"], "魔法可爱"),
        KaomojiEntry("✧◝(⁰▿⁰)◜✧", "magic", ["magic", "sparkle", "happy"], "魔法开心"),
        KaomojiEntry("(☆ω☆)", "magic", ["magic", "star", "shiny"], "星星"),
        KaomojiEntry("(✧∀✧)", "magic", ["magic", "sparkle", "happy"], "闪耀开心"),
        KaomojiEntry("ヽ(★ω★)ノ", "magic", ["magic", "star", "sparkle"], "星星闪烁"),
        KaomojiEntry("✧⁺⸜(●'▾'●)⸝⁺✧", "magic", ["magic", "sparkle", "cute"], "可爱魔法"),
        KaomojiEntry("(✧≖‿≖)", "magic", ["magic", "sparkle", "mystery"], "神秘魔法"),
    ],
    "run": [
        KaomojiEntry("ε=ε=ε=┌( >_<)┘", "run", ["run", "fast", "escape"], "快跑"),
        KaomojiEntry("ε=ε=┌( >_<)┘", "run", ["run", "fast", "escape"], "逃跑"),
        KaomojiEntry("ε=ε=ε=ε=┌(; >_<)┘", "run", ["run", "fast", "panic"], "恐慌逃跑"),
        KaomojiEntry("C= C= C= C=┌( `ー´)┘", "run", ["run", "fast", "escape"], "奔跑"),
        KaomojiEntry("ε=ε=ε=ε=ε=┌( >_<)┘", "run", ["run", "fast", "escape"], "快速逃跑"),
        KaomojiEntry("┌( >_<)┘", "run", ["run", "fast", "escape"], "奔跑"),
        KaomojiEntry("C= C=┌( `ー´)┘", "run", ["run", "fast", "escape"], "奔跑"),
    ],
    "hide": [
        KaomojiEntry("｜−・;）", "hide", ["hide", "peek", "spy"], "躲藏偷看"),
        KaomojiEntry("｜゜゜）", "hide", ["hide", "peek", "spy"], "偷看"),
        KaomojiEntry("｜。・）", "hide", ["hide", "peek", "spy"], "躲藏"),
        KaomojiEntry("｜－・）", "hide", ["hide", "peek", "spy"], "偷窥"),
        KaomojiEntry("┏(・o･)┛", "hide", ["hide", "peek", "spy"], "躲藏"),
        KaomojiEntry("｜。｜", "hide", ["hide", "peek", "spy"], "躲起来"),
        KaomojiEntry("｜x・）", "hide", ["hide", "peek", "spy"], "偷看"),
        KaomojiEntry("｜_・）", "hide", ["hide", "peek", "spy"], "躲藏偷窥"),
        KaomojiEntry("｜°・）", "hide", ["hide", "peek", "spy"], "躲藏"),
        KaomojiEntry("｜＞＜）", "hide", ["hide", "peek", "spy"], "躲藏偷看"),
    ],
    "peace": [
        KaomojiEntry("(◕‿◕)✌", "peace", ["peace", "victory", "cute"], "剪刀手"),
        KaomojiEntry("✌(◕‿◕)", "peace", ["peace", "victory", "cute"], "胜利"),
        KaomojiEntry("( ^_^)∠※", "peace", ["peace", "victory", "cute"], "和平"),
        KaomojiEntry("(✿◠‿◠)✌", "peace", ["peace", "victory", "cute"], "可爱剪刀手"),
        KaomojiEntry("✌(◠‿◠)", "peace", ["peace", "victory", "cute"], "胜利剪刀手"),
        KaomojiEntry("(◕ᴗ◕)✌", "peace", ["peace", "victory", "cute"], "和平胜利"),
        KaomojiEntry("✌(◕ᴗ◕)", "peace", ["peace", "victory", "cute"], "胜利可爱"),
        KaomojiEntry("(´▽`ʃ✌", "peace", ["peace", "victory", "cute"], "和平可爱"),
        KaomojiEntry("✌(´▽`)", "peace", ["peace", "victory", "cute"], "胜利可爱"),
        KaomojiEntry("(◕ω◕)✌", "peace", ["peace", "victory", "cute"], "剪刀手可爱"),
    ],
}


def get_all_emotions() -> List[str]:
    """获取所有情绪类别
    
    Returns:
        所有情绪类别的列表
    """
    return list(KAOMOJI_DATABASE.keys())


def get_by_emotion(emotion: str) -> List[str]:
    """获取指定情绪的所有颜文字
    
    Args:
        emotion: 情绪类别名称（如 'happy', 'sad', 'love' 等）
    
    Returns:
        该情绪类别的所有颜文字列表
    
    Raises:
        ValueError: 如果情绪类别不存在
    """
    emotion = emotion.lower()
    if emotion not in KAOMOJI_DATABASE:
        available = ", ".join(get_all_emotions())
        raise ValueError(f"未知的情绪类别: '{emotion}'。可用类别: {available}")
    return [entry.kaomoji for entry in KAOMOJI_DATABASE[emotion]]


def get_random(emotion: Optional[str] = None) -> str:
    """获取随机颜文字
    
    Args:
        emotion: 可选，指定情绪类别。如果为 None，则从所有类别中随机选择
    
    Returns:
        随机颜文字字符串
    """
    if emotion is None:
        all_entries = []
        for entries in KAOMOJI_DATABASE.values():
            all_entries.extend(entries)
        return random.choice(all_entries).kaomoji
    
    emotion = emotion.lower()
    if emotion not in KAOMOJI_DATABASE:
        available = ", ".join(get_all_emotions())
        raise ValueError(f"未知的情绪类别: '{emotion}'。可用类别: {available}")
    
    entries = KAOMOJI_DATABASE[emotion]
    return random.choice(entries).kaomoji


def search(keyword: str) -> List[str]:
    """根据关键词搜索颜文字
    
    在颜文字的关键词和描述中搜索匹配项
    
    Args:
        keyword: 搜索关键词
    
    Returns:
        匹配的颜文字列表
    """
    keyword = keyword.lower()
    results = []
    
    for entries in KAOMOJI_DATABASE.values():
        for entry in entries:
            # 在关键词中搜索
            if keyword in [kw.lower() for kw in entry.keywords]:
                results.append(entry.kaomoji)
            # 在描述中搜索
            elif keyword in entry.description.lower():
                results.append(entry.kaomoji)
            # 直接搜索颜文字本身
            elif keyword in entry.kaomoji:
                results.append(entry.kaomoji)
    
    # 去重并保持顺序
    seen = set()
    unique_results = []
    for r in results:
        if r not in seen:
            seen.add(r)
            unique_results.append(r)
    
    return unique_results


def get_details(kaomoji: str) -> Optional[KaomojiEntry]:
    """获取颜文字的详细信息
    
    Args:
        kaomoji: 颜文字字符串
    
    Returns:
        KaomojiEntry 对象，如果未找到则返回 None
    """
    for entries in KAOMOJI_DATABASE.values():
        for entry in entries:
            if entry.kaomoji == kaomoji:
                return entry
    return None


def get_random_entry(emotion: Optional[str] = None) -> KaomojiEntry:
    """获取随机颜文字条目（包含详细信息）
    
    Args:
        emotion: 可选，指定情绪类别
    
    Returns:
        KaomojiEntry 对象
    """
    if emotion is None:
        all_entries = []
        for entries in KAOMOJI_DATABASE.values():
            all_entries.extend(entries)
        return random.choice(all_entries)
    
    emotion = emotion.lower()
    if emotion not in KAOMOJI_DATABASE:
        available = ", ".join(get_all_emotions())
        raise ValueError(f"未知的情绪类别: '{emotion}'。可用类别: {available}")
    
    entries = KAOMOJI_DATABASE[emotion]
    return random.choice(entries)


def count() -> Dict[str, int]:
    """统计各类别颜文字数量
    
    Returns:
        字典，键为情绪类别，值为数量
    """
    return {emotion: len(entries) for emotion, entries in KAOMOJI_DATABASE.items()}


def count_total() -> int:
    """获取颜文字总数
    
    Returns:
        颜文字总数
    """
    return sum(len(entries) for entries in KAOMOJI_DATABASE.values())


# 预定义的常用颜文字快捷访问
HAPPY = "(◕‿◕)"
SAD = "(╥_╥)"
LOVE = "(♥ω♥*)"
ANGRY = "(╬ Ò﹏Ó)"
SURPRISED = "(°o°)"
CUTE = "(◕ᴗ◕✿)"
SHY = "(⁄ ⁄•⁄ω⁄•⁄ ⁄)"
WINK = "(◕‿-)"
TABLE_FLIP = "(╯°□°)╯︵ ┻━┻"
CAT = "(=^･ω･^=)"
BEAR = "ʕ•ᴥ•ʔ"
FLOWER = "(◕‿◕✿)"
FIGHT = "(ง •̀_•́)ง"
MAGIC = "(ﾉ◕ヮ◕)ﾉ*:・ﾟ✧"
RUN = "ε=ε=ε=┌( >_<)┘"


# 便捷函数
def happy() -> str:
    """获取随机开心颜文字"""
    return get_random("happy")


def sad() -> str:
    """获取随机伤心颜文字"""
    return get_random("sad")


def love() -> str:
    """获取随机爱意颜文字"""
    return get_random("love")


def angry() -> str:
    """获取随机生气颜文字"""
    return get_random("angry")


def surprised() -> str:
    """获取随机惊讶颜文字"""
    return get_random("surprised")


def cute() -> str:
    """获取随机可爱颜文字"""
    return get_random("cute")


def shy() -> str:
    """获取随机害羞颜文字"""
    return get_random("shy")


def cat() -> str:
    """获取随机猫咪颜文字"""
    return get_random("cat")


def bear() -> str:
    """获取随机熊颜文字"""
    return get_random("bear")


def flower() -> str:
    """获取随机花朵颜文字"""
    return get_random("flower")


if __name__ == "__main__":
    # 演示用法
    print("=" * 50)
    print("Kaomoji Utils - 日式颜文字工具集")
    print("=" * 50)
    
    print(f"\n📊 颜文字总数: {count_total()}")
    print(f"\n📋 各类别数量:")
    for emotion, cnt in count().items():
        print(f"  {emotion}: {cnt}")
    
    print(f"\n🎲 随机颜文字:")
    for _ in range(5):
        print(f"  {get_random()}")
    
    print(f"\n😊 开心颜文字 (随机5个):")
    happy_list = get_by_emotion("happy")
    for k in random.sample(happy_list, min(5, len(happy_list))):
        print(f"  {k}")
    
    print(f"\n💔 伤心颜文字 (随机5个):")
    sad_list = get_by_emotion("sad")
    for k in random.sample(sad_list, min(5, len(sad_list))):
        print(f"  {k}")
    
    print(f"\n❤️ 爱意颜文字 (随机5个):")
    love_list = get_by_emotion("love")
    for k in random.sample(love_list, min(5, len(love_list))):
        print(f"  {k}")
    
    print(f"\n🔍 搜索关键词 'love':")
    results = search("love")
    for k in results[:5]:
        print(f"  {k}")
    
    print(f"\n🔍 搜索关键词 'cute':")
    results = search("cute")
    for k in results[:5]:
        print(f"  {k}")
    
    print(f"\n🔍 搜索关键词 '猫':")
    results = search("猫")
    for k in results[:5]:
        print(f"  {k}")
    
    print(f"\n📝 颜文字详情:")
    entry = get_details(HAPPY)
    if entry:
        print(f"  颜文字: {entry.kaomoji}")
        print(f"  情绪: {entry.emotion}")
        print(f"  关键词: {entry.keywords}")
        print(f"  描述: {entry.description}")
    
    print(f"\n🎯 快捷函数:")
    print(f"  happy(): {happy()}")
    print(f"  sad(): {sad()}")
    print(f"  love(): {love()}")
    print(f"  cute(): {cute()}")
    print(f"  cat(): {cat()}")
    print(f"  bear(): {bear()}")