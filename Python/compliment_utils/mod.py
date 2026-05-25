"""
Compliment Utils - 称赞/赞美语生成工具库

功能：
- 随机称赞生成
- 分类称赞（工作、外貌、性格、能力等）
- 多语言支持（中文、英文）
- 可定制称赞模板
- 称赞强度分级（轻度、中度、强力）
- 个性化称赞（带名字）
- 零外部依赖，纯 Python 标准库实现

Author: AllToolkit
Version: 1.0.0
Date: 2026-05-25
"""

from typing import Optional, List, Dict, Tuple, Any
from enum import Enum
import random


class ComplimentCategory(Enum):
    """称赞类别"""
    WORK = "工作"
    APPEARANCE = "外貌"
    PERSONALITY = "性格"
    SKILL = "能力"
    EFFORT = "努力"
    ATTITUDE = "态度"
    ACHIEVEMENT = "成就"
    CREATIVITY = "创造力"
    KINDNESS = "善良"
    INTELLIGENCE = "智慧"
    HUMOR = "幽默"
    FRIENDSHIP = "友谊"
    GENERAL = "通用"


class ComplimentStrength(Enum):
    """称赞强度"""
    LIGHT = "轻度"      # 轻微赞美，日常用语
    MEDIUM = "中度"     # 标准赞美
    STRONG = "强力"     # 强烈赞美，印象深刻


class Language(Enum):
    """语言"""
    CHINESE = "zh"
    ENGLISH = "en"


# 中文称赞数据库
_CHINESE_COMPLIMENTS: Dict[ComplimentCategory, Dict[ComplimentStrength, List[str]]] = {
    ComplimentCategory.WORK: {
        ComplimentStrength.LIGHT: [
            "你工作做得不错",
            "你的工作效率挺高的",
            "这工作处理得很好",
            "你的工作态度很认真",
        ],
        ComplimentStrength.MEDIUM: [
            "你的工作能力真的很出色",
            "你在工作中表现得非常专业",
            "你对工作的投入让人敬佩",
            "你的工作成果令人印象深刻",
        ],
        ComplimentStrength.STRONG: [
            "你的工作能力简直是行业标杆",
            "你在工作中的表现堪称完美",
            "你是我见过最专业的工作者",
            "你的工作成果已经超越了所有人的期待",
        ],
    },
    ComplimentCategory.APPEARANCE: {
        ComplimentStrength.LIGHT: [
            "你今天看起来很不错",
            "你的穿着很有品味",
            "你的笑容很温暖",
            "你的发型很合适",
        ],
        ComplimentStrength.MEDIUM: [
            "你今天的样子特别迷人",
            "你的气质真的很出众",
            "你的打扮总是恰到好处",
            "你的眼睛很有神采",
        ],
        ComplimentStrength.STRONG: [
            "你今天的造型简直惊艳全场",
            "你的气质独一无二，令人难忘",
            "你是我见过的最有魅力的人",
            "你的美丽让整个房间都亮了起来",
        ],
    },
    ComplimentCategory.PERSONALITY: {
        ComplimentStrength.LIGHT: [
            "你人挺好的",
            "你的性格很随和",
            "你很容易相处",
            "你很友善",
        ],
        ComplimentStrength.MEDIUM: [
            "你的性格真的很迷人",
            "你待人真诚，让人感动",
            "你的个性既独特又可爱",
            "你的人格魅力让人印象深刻",
        ],
        ComplimentStrength.STRONG: [
            "你的性格是我最欣赏的类型",
            "你的人格魅力简直是无可替代",
            "你的真诚和善良触动了我",
            "你是我遇到过的最美好的人",
        ],
    },
    ComplimentCategory.SKILL: {
        ComplimentStrength.LIGHT: [
            "你的技能很不错",
            "你在这方面做得挺好",
            "你很有天赋",
            "你学得很快",
        ],
        ComplimentStrength.MEDIUM: [
            "你的技能水平让人赞叹",
            "你在这方面的能力非常突出",
            "你的天赋真是让人羡慕",
            "你的学习速度令人惊讶",
        ],
        ComplimentStrength.STRONG: [
            "你在这一领域的技能已经达到了大师级别",
            "你的天赋简直是上天恩赐",
            "你的能力已经超越了绝大多数人",
            "你在这方面的造诣无人能及",
        ],
    },
    ComplimentCategory.EFFORT: {
        ComplimentStrength.LIGHT: [
            "你很努力",
            "你的付出值得肯定",
            "你一直在进步",
            "你的坚持很棒",
        ],
        ComplimentStrength.MEDIUM: [
            "你的努力真的很让人佩服",
            "你的付出一定会得到回报",
            "你不断进步的精神令人感动",
            "你的毅力值得学习",
        ],
        ComplimentStrength.STRONG: [
            "你的努力程度令人震撼",
            "你的付出已经超越了所有人的想象",
            "你是我见过的最努力的人",
            "你的坚持精神将激励无数人",
        ],
    },
    ComplimentCategory.ATTITUDE: {
        ComplimentStrength.LIGHT: [
            "你的态度很好",
            "你很积极",
            "你的心态不错",
            "你很乐观",
        ],
        ComplimentStrength.MEDIUM: [
            "你的积极态度感染了周围的人",
            "你的乐观心态让人感到温暖",
            "你面对困难的态度令人敬佩",
            "你的正能量让人受益",
        ],
        ComplimentStrength.STRONG: [
            "你的态度是我学习的榜样",
            "你的乐观精神拯救了许多人",
            "你面对一切的积极态度简直完美",
            "你的正能量影响了整个团队",
        ],
    },
    ComplimentCategory.ACHIEVEMENT: {
        ComplimentStrength.LIGHT: [
            "你做得很好",
            "这是个不错的成绩",
            "你进步很明显",
            "这个成果很棒",
        ],
        ComplimentStrength.MEDIUM: [
            "你的成就值得庆祝",
            "这个成绩真的很出色",
            "你的进步令人刮目相看",
            "这个成果超越了预期",
        ],
        ComplimentStrength.STRONG: [
            "你的成就将载入史册",
            "这个成绩创造了新的纪录",
            "你的进步简直是奇迹般的",
            "这个成果震惊了所有人",
        ],
    },
    ComplimentCategory.CREATIVITY: {
        ComplimentStrength.LIGHT: [
            "你的想法很有创意",
            "你的思路很新颖",
            "你很有想象力",
            "你的点子很独特",
        ],
        ComplimentStrength.MEDIUM: [
            "你的创意让人眼前一亮",
            "你的想象力非常丰富",
            "你的思维总是与众不同",
            "你的创新精神值得赞赏",
        ],
        ComplimentStrength.STRONG: [
            "你的创意简直是天才级别",
            "你的想象力无人能比",
            "你的思维方式开创了新的领域",
            "你的创新将改变这个行业",
        ],
    },
    ComplimentCategory.KINDNESS: {
        ComplimentStrength.LIGHT: [
            "你很善良",
            "你心地很好",
            "你很体贴",
            "你很关心他人",
        ],
        ComplimentStrength.MEDIUM: [
            "你的善良让人感动",
            "你的心地真是纯净",
            "你的体贴温暖了许多人",
            "你对他人的关心令人敬佩",
        ],
        ComplimentStrength.STRONG: [
            "你的善良是世界上最珍贵的品质",
            "你的心地善良照亮了周围",
            "你的体贴挽救了无数人的心灵",
            "你是我遇到的最善良的人",
        ],
    },
    ComplimentCategory.INTELLIGENCE: {
        ComplimentStrength.LIGHT: [
            "你很聪明",
            "你的想法很明智",
            "你反应很快",
            "你的见解很独到",
        ],
        ComplimentStrength.MEDIUM: [
            "你的智慧让人印象深刻",
            "你的见解总是深刻而有价值",
            "你的思维敏捷令人赞叹",
            "你的聪明才智是大家的财富",
        ],
        ComplimentStrength.STRONG: [
            "你的智慧简直是天才级别",
            "你的见解开创了新的视角",
            "你的思维速度无人能及",
            "你的聪明才智将改变世界",
        ],
    },
    ComplimentCategory.HUMOR: {
        ComplimentStrength.LIGHT: [
            "你很有趣",
            "你的笑话很好笑",
            "你总是能逗人开心",
            "你很幽默",
        ],
        ComplimentStrength.MEDIUM: [
            "你的幽默感让人快乐",
            "你总能带来欢笑",
            "你的风趣感染了大家",
            "你的幽默是一种天赋",
        ],
        ComplimentStrength.STRONG: [
            "你的幽默感简直是天生的喜剧演员",
            "你总能把最严肃的场合变得欢乐",
            "你的风趣让人笑得合不拢嘴",
            "你的幽默是我最欣赏的特质",
        ],
    },
    ComplimentCategory.FRIENDSHIP: {
        ComplimentStrength.LIGHT: [
            "你是个好朋友",
            "你很可靠",
            "你很支持朋友",
            "你很值得信任",
        ],
        ComplimentStrength.MEDIUM: [
            "你的友谊很珍贵",
            "你是朋友们的支柱",
            "你对朋友的支持让人感动",
            "你的可靠让人安心",
        ],
        ComplimentStrength.STRONG: [
            "你是我生命中最珍贵的朋友",
            "你总是能在关键时刻支持朋友",
            "你的友谊是无价的宝藏",
            "你是最值得信赖的人",
        ],
    },
    ComplimentCategory.GENERAL: {
        ComplimentStrength.LIGHT: [
            "你很棒",
            "你很不错",
            "你做得挺好",
            "你很优秀",
        ],
        ComplimentStrength.MEDIUM: [
            "你真的很出色",
            "你让人印象深刻",
            "你是个很特别的人",
            "你值得被赞赏",
        ],
        ComplimentStrength.STRONG: [
            "你简直是完美无缺",
            "你是我见过最优秀的人",
            "你的存在让世界更美好",
            "你值得所有的赞美",
        ],
    },
}

# 英文称赞数据库
_ENGLISH_COMPLIMENTS: Dict[ComplimentCategory, Dict[ComplimentStrength, List[str]]] = {
    ComplimentCategory.WORK: {
        ComplimentStrength.LIGHT: [
            "You did a good job",
            "Your work efficiency is impressive",
            "You handled that task well",
            "You have a professional approach to work",
        ],
        ComplimentStrength.MEDIUM: [
            "Your work capabilities are outstanding",
            "You demonstrate true professionalism",
            "Your dedication to work is admirable",
            "Your work results are impressive",
        ],
        ComplimentStrength.STRONG: [
            "Your work abilities set the industry standard",
            "Your performance at work is flawless",
            "You are the most professional worker I've ever met",
            "Your results exceed all expectations",
        ],
    },
    ComplimentCategory.APPEARANCE: {
        ComplimentStrength.LIGHT: [
            "You look nice today",
            "Your outfit has great style",
            "Your smile is warm",
            "Your hairstyle suits you well",
        ],
        ComplimentStrength.MEDIUM: [
            "You look particularly charming today",
            "You have a truly outstanding aura",
            "Your style is always perfect",
            "Your eyes sparkle with life",
        ],
        ComplimentStrength.STRONG: [
            "Your appearance today is absolutely stunning",
            "Your presence lights up the entire room",
            "You are the most charming person I've ever seen",
            "Your beauty is truly unforgettable",
        ],
    },
    ComplimentCategory.PERSONALITY: {
        ComplimentStrength.LIGHT: [
            "You're a nice person",
            "You have a pleasant personality",
            "You're easy to get along with",
            "You're very friendly",
        ],
        ComplimentStrength.MEDIUM: [
            "Your personality is truly captivating",
            "Your sincerity touches hearts",
            "You have a unique and lovely character",
            "Your personal charm is memorable",
        ],
        ComplimentStrength.STRONG: [
            "Your personality is exactly the type I admire most",
            "Your personal charm is irreplaceable",
            "Your sincerity and kindness deeply moved me",
            "You are the finest person I've ever encountered",
        ],
    },
    ComplimentCategory.SKILL: {
        ComplimentStrength.LIGHT: [
            "You have good skills",
            "You're doing well in this area",
            "You have natural talent",
            "You learn quickly",
        ],
        ComplimentStrength.MEDIUM: [
            "Your skill level is admirable",
            "Your ability in this area is exceptional",
            "Your talent is enviable",
            "Your learning speed is astonishing",
        ],
        ComplimentStrength.STRONG: [
            "Your skills in this field have reached master level",
            "Your talent is truly a gift from heaven",
            "Your abilities surpass almost everyone",
            "Your expertise in this area is unmatched",
        ],
    },
    ComplimentCategory.EFFORT: {
        ComplimentStrength.LIGHT: [
            "You work hard",
            "Your effort deserves recognition",
            "You're constantly improving",
            "Your persistence is admirable",
        ],
        ComplimentStrength.MEDIUM: [
            "Your effort is truly admirable",
            "Your dedication will surely pay off",
            "Your constant progress inspires others",
            "Your perseverance is worth learning from",
        ],
        ComplimentStrength.STRONG: [
            "The intensity of your effort is staggering",
            "Your dedication exceeds everyone's imagination",
            "You are the most hardworking person I've met",
            "Your persistence will inspire countless people",
        ],
    },
    ComplimentCategory.ATTITUDE: {
        ComplimentStrength.LIGHT: [
            "You have a great attitude",
            "You're very positive",
            "You have a good mindset",
            "You're optimistic",
        ],
        ComplimentStrength.MEDIUM: [
            "Your positive attitude spreads to others",
            "Your optimism warms hearts",
            "Your attitude toward challenges is admirable",
            "Your positive energy benefits everyone",
        ],
        ComplimentStrength.STRONG: [
            "Your attitude is my role model",
            "Your optimism has saved many people",
            "Your positive approach to everything is perfect",
            "Your positive energy has transformed the team",
        ],
    },
    ComplimentCategory.ACHIEVEMENT: {
        ComplimentStrength.LIGHT: [
            "You did great",
            "That's a good achievement",
            "Your progress is evident",
            "That result is excellent",
        ],
        ComplimentStrength.MEDIUM: [
            "Your achievement deserves celebration",
            "This result is truly outstanding",
            "Your progress makes everyone take notice",
            "This result exceeded expectations",
        ],
        ComplimentStrength.STRONG: [
            "Your achievement will be remembered forever",
            "This result has set a new record",
            "Your progress is nothing short of miraculous",
            "This result shocked everyone",
        ],
    },
    ComplimentCategory.CREATIVITY: {
        ComplimentStrength.LIGHT: [
            "Your idea is creative",
            "Your approach is novel",
            "You have great imagination",
            "Your concept is unique",
        ],
        ComplimentStrength.MEDIUM: [
            "Your creativity catches everyone's eye",
            "Your imagination is rich and vibrant",
            "Your thinking is always distinctive",
            "Your innovation spirit is commendable",
        ],
        ComplimentStrength.STRONG: [
            "Your creativity is at genius level",
            "Your imagination is unparalleled",
            "Your thinking has opened a new field",
            "Your innovation will transform this industry",
        ],
    },
    ComplimentCategory.KINDNESS: {
        ComplimentStrength.LIGHT: [
            "You are kind",
            "You have a good heart",
            "You're considerate",
            "You care about others",
        ],
        ComplimentStrength.MEDIUM: [
            "Your kindness moves people",
            "Your heart is truly pure",
            "Your consideration warms many hearts",
            "Your care for others is admirable",
        ],
        ComplimentStrength.STRONG: [
            "Your kindness is the world's most precious quality",
            "Your pure heart illuminates everything around you",
            "Your consideration has saved countless hearts",
            "You are the kindest person I've ever met",
        ],
    },
    ComplimentCategory.INTELLIGENCE: {
        ComplimentStrength.LIGHT: [
            "You're smart",
            "Your ideas are wise",
            "You're quick to respond",
            "Your insights are unique",
        ],
        ComplimentStrength.MEDIUM: [
            "Your wisdom makes a deep impression",
            "Your insights are always profound and valuable",
            "Your quick thinking is admirable",
            "Your intelligence is a treasure for everyone",
        ],
        ComplimentStrength.STRONG: [
            "Your wisdom is at genius level",
            "Your insights have created new perspectives",
            "Your thinking speed is unmatched",
            "Your intelligence will change the world",
        ],
    },
    ComplimentCategory.HUMOR: {
        ComplimentStrength.LIGHT: [
            "You're fun",
            "Your jokes are funny",
            "You always make people laugh",
            "You're humorous",
        ],
        ComplimentStrength.MEDIUM: [
            "Your humor brings joy",
            "You always bring laughter",
            "Your wit spreads to everyone",
            "Your humor is a natural gift",
        ],
        ComplimentStrength.STRONG: [
            "Your humor is like a natural comedian",
            "You turn even serious moments into joy",
            "Your wit makes people laugh uncontrollably",
            "Your humor is my most appreciated trait",
        ],
    },
    ComplimentCategory.FRIENDSHIP: {
        ComplimentStrength.LIGHT: [
            "You're a good friend",
            "You're reliable",
            "You support your friends",
            "You're trustworthy",
        ],
        ComplimentStrength.MEDIUM: [
            "Your friendship is precious",
            "You're a pillar for your friends",
            "Your support for friends is touching",
            "Your reliability brings peace of mind",
        ],
        ComplimentStrength.STRONG: [
            "You are the most precious friend in my life",
            "You always support friends at critical moments",
            "Your friendship is an invaluable treasure",
            "You are the most trustworthy person",
        ],
    },
    ComplimentCategory.GENERAL: {
        ComplimentStrength.LIGHT: [
            "You're great",
            "You're nice",
            "You did well",
            "You're excellent",
        ],
        ComplimentStrength.MEDIUM: [
            "You're truly outstanding",
            "You make a deep impression",
            "You're a special person",
            "You deserve appreciation",
        ],
        ComplimentStrength.STRONG: [
            "You are simply flawless",
            "You are the most excellent person I've ever met",
            "Your existence makes the world better",
            "You deserve all the praise",
        ],
    },
}

# 称赞前缀（用于个性化称赞）
_PREFIXES: Dict[Language, Dict[ComplimentStrength, List[str]]] = {
    Language.CHINESE: {
        ComplimentStrength.LIGHT: ["嘿，", "哇，", "看，", "你知道吗，"],
        ComplimentStrength.MEDIUM: ["说实话，", "真的，", "不得不承认，", "真诚地，"],
        ComplimentStrength.STRONG: ["必须说，", "毫无疑问，", "千真万确，", "我坚信，"],
    },
    Language.ENGLISH: {
        ComplimentStrength.LIGHT: ["Hey, ", "Wow, ", "Look, ", "You know, "],
        ComplimentStrength.MEDIUM: ["Honestly, ", "Really, ", "Have to admit, ", "Sincerely, "],
        ComplimentStrength.STRONG: ["Must say, ", "Without doubt, ", "Absolutely, ", "I firmly believe, "],
    },
}

# 称赞后缀（用于增强效果）
_SUFFIXES: Dict[Language, Dict[ComplimentStrength, List[str]]] = {
    Language.CHINESE: {
        ComplimentStrength.LIGHT: ["！", "～", "。", "呢！"],
        ComplimentStrength.MEDIUM: ["！", "真的！", "太棒了！", "为你点赞！"],
        ComplimentStrength.STRONG: ["！！！", "太了不起了！", "为你骄傲！", "世界因你更美好！"],
    },
    Language.ENGLISH: {
        ComplimentStrength.LIGHT: ["!", "~", ".", " you know!"],
        ComplimentStrength.MEDIUM: ["!", " really!", " awesome!", " thumbs up!"],
        ComplimentStrength.STRONG: ["!!!", " incredible!", " proud of you!", " you make the world better!"],
    },
}


class ComplimentUtils:
    """称赞生成工具类"""

    @staticmethod
    def get_compliment(
        category: Optional[ComplimentCategory] = None,
        strength: Optional[ComplimentStrength] = None,
        language: Optional[Language] = None,
        include_prefix: bool = False,
        include_suffix: bool = False,
    ) -> str:
        """
        获取称赞语
        
        Args:
            category: 称赞类别，默认随机
            strength: 称赞强度，默认随机
            language: 语言，默认中文
            include_prefix: 是否包含前缀
            include_suffix: 是否包含后缀
            
        Returns:
            称赞语字符串
        """
        if language is None:
            language = Language.CHINESE
        
        if category is None:
            category = random.choice(list(ComplimentCategory))
        
        if strength is None:
            strength = random.choice(list(ComplimentStrength))
        
        # 获取对应语言的数据库
        db = _CHINESE_COMPLIMENTS if language == Language.CHINESE else _ENGLISH_COMPLIMENTS
        
        # 获取称赞内容
        compliments = db.get(category, {}).get(strength, [])
        if not compliments:
            # 降级到通用类别
            compliments = db.get(ComplimentCategory.GENERAL, {}).get(strength, [])
        
        if not compliments:
            return ""
        
        result = random.choice(compliments)
        
        # 添加前缀
        if include_prefix:
            prefixes = _PREFIXES.get(language, {}).get(strength, [])
            if prefixes:
                result = random.choice(prefixes) + result
        
        # 添加后缀
        if include_suffix:
            suffixes = _SUFFIXES.get(language, {}).get(strength, [])
            if suffixes:
                result = result + random.choice(suffixes)
        
        return result

    @staticmethod
    def get_personalized_compliment(
        name: str,
        category: Optional[ComplimentCategory] = None,
        strength: Optional[ComplimentStrength] = None,
        language: Optional[Language] = None,
    ) -> str:
        """
        获取个性化称赞（带名字）
        
        Args:
            name: 被称赞者的名字
            category: 称赞类别
            strength: 称赞强度
            language: 语言
            
        Returns:
            个性化称赞语
        """
        if language is None:
            language = Language.CHINESE
        
        compliment = ComplimentUtils.get_compliment(
            category=category,
            strength=strength,
            language=language,
            include_prefix=True,
        )
        
        # 插入名字
        if language == Language.CHINESE:
            templates = [
                f"{name}，{compliment}",
                f"{compliment}，{name}",
                f"亲爱的{name}，{compliment}",
            ]
        else:
            templates = [
                f"{name}, {compliment}",
                f"{compliment}, {name}",
                f"Dear {name}, {compliment}",
            ]
        
        return random.choice(templates)

    @staticmethod
    def get_batch_compliments(
        count: int = 5,
        category: Optional[ComplimentCategory] = None,
        strength: Optional[ComplimentStrength] = None,
        language: Optional[Language] = None,
        unique: bool = True,
    ) -> List[str]:
        """
        获取批量称赞语
        
        Args:
            count: 数量
            category: 称赞类别
            strength: 称赞强度
            language: 语言
            unique: 是否唯一（不重复）
            
        Returns:
            称赞语列表
        """
        results = []
        seen = set()
        
        db = _CHINESE_COMPLIMENTS if (language or Language.CHINESE) == Language.CHINESE else _ENGLISH_COMPLIMENTS
        
        # 确定可用的称赞
        if category:
            available = db.get(category, {}).get(strength or ComplimentStrength.MEDIUM, [])
        else:
            available = []
            for cat_data in db.values():
                for str_data in cat_data.values():
                    available.extend(str_data)
        
        if not available:
            return []
        
        for _ in range(min(count, len(available) if unique else count * 10)):
            compliment = ComplimentUtils.get_compliment(category, strength, language)
            if unique:
                if compliment in seen:
                    continue
                seen.add(compliment)
            results.append(compliment)
            if len(results) >= count:
                break
        
        return results

    @staticmethod
    def get_compliment_for_context(
        context: str,
        language: Optional[Language] = None,
    ) -> str:
        """
        根据上下文获取称赞语
        
        Args:
            context: 上下文描述（如 "完成了项目"、"帮助了同事"）
            language: 语言
            
        Returns:
            适合的称赞语
        """
        if language is None:
            language = Language.CHINESE
        
        # 根据关键词判断类别
        context_lower = context.lower()
        
        # 关键词映射
        keyword_map: Dict[ComplimentCategory, List[str]] = {
            ComplimentCategory.WORK: ["工作", "任务", "项目", "完成", "work", "task", "project", "finished", "done"],
            ComplimentCategory.APPEARANCE: ["漂亮", "好看", "衣服", "发型", "beautiful", "pretty", "nice", "outfit", "hair"],
            ComplimentCategory.EFFORT: ["努力", "坚持", "付出", "尝试", "effort", "hard", "try", "persist"],
            ComplimentCategory.ACHIEVEMENT: ["成就", "成功", "获奖", "赢", "achievement", "success", "win", "award"],
            ComplimentCategory.CREATIVITY: ["创意", "想法", "创新", "设计", "creative", "idea", "innovation", "design"],
            ComplimentCategory.KINDNESS: ["帮助", "善良", "体贴", "关心", "kind", "help", "care", "nice"],
            ComplimentCategory.FRIENDSHIP: ["朋友", "友谊", "陪伴", "支持", "friend", "support", "together"],
        }
        
        matched_category = ComplimentCategory.GENERAL
        for category, keywords in keyword_map.items():
            for keyword in keywords:
                if keyword in context_lower:
                    matched_category = category
                    break
        
        return ComplimentUtils.get_compliment(category=matched_category, language=language)

    @staticmethod
    def get_categories(language: Optional[Language] = None) -> List[str]:
        """
        获取所有称赞类别
        
        Args:
            language: 语言
            
        Returns:
            类别列表
        """
        if language == Language.ENGLISH:
            return [cat.name for cat in ComplimentCategory]
        return [cat.value for cat in ComplimentCategory]

    @staticmethod
    def get_strengths(language: Optional[Language] = None) -> List[str]:
        """
        获取所有称赞强度
        
        Args:
            language: 语言
            
        Returns:
            强度列表
        """
        if language == Language.ENGLISH:
            return [str.name for str in ComplimentStrength]
        return [str.value for str in ComplimentStrength]

    @staticmethod
    def get_compliment_count(category: Optional[ComplimentCategory] = None, language: Optional[Language] = None) -> int:
        """
        获取称赞语数量
        
        Args:
            category: 类别（可选，统计总数）
            language: 语言
            
        Returns:
            数量
        """
        db = _CHINESE_COMPLIMENTS if (language or Language.CHINESE) == Language.CHINESE else _ENGLISH_COMPLIMENTS
        
        if category:
            return sum(len(compliments) for compliments in db.get(category, {}).values())
        
        return sum(
            sum(len(compliments) for compliments in cat_data.values())
            for cat_data in db.values()
        )

    @staticmethod
    def get_daily_compliment(language: Optional[Language] = None) -> str:
        """
        获取每日称赞（适合用于定时提醒）
        
        Args:
            language: 语言
            
        Returns:
            每日称赞语
        """
        import datetime
        
        if language is None:
            language = Language.CHINESE
        
        # 根据日期生成不同的称赞
        today = datetime.date.today()
        day_offset = today.day % len(list(ComplimentCategory))
        categories = list(ComplimentCategory)
        selected_category = categories[day_offset]
        
        strength = ComplimentStrength.MEDIUM
        
        compliment = ComplimentUtils.get_compliment(
            category=selected_category,
            strength=strength,
            language=language,
            include_prefix=True,
            include_suffix=True,
        )
        
        # 添加日期前缀
        if language == Language.CHINESE:
            return f"【{today.strftime('%Y年%m月%d日')} 每日称赞】\n{compliment}"
        else:
            return f"[{today.strftime('%Y-%m-%d')} Daily Compliment]\n{compliment}"

    @staticmethod
    def get_motivational_compliment(language: Optional[Language] = None) -> str:
        """
        获取激励性称赞
        
        Args:
            language: 语言
            
        Returns:
            激励性称赞语
        """
        if language is None:
            language = Language.CHINESE
        
        # 选择激励相关的类别
        motivational_categories = [
            ComplimentCategory.EFFORT,
            ComplimentCategory.ACHIEVEMENT,
            ComplimentCategory.ATTITUDE,
            ComplimentCategory.SKILL,
        ]
        
        category = random.choice(motivational_categories)
        strength = random.choice([ComplimentStrength.MEDIUM, ComplimentStrength.STRONG])
        
        return ComplimentUtils.get_compliment(
            category=category,
            strength=strength,
            language=language,
            include_prefix=True,
            include_suffix=True,
        )


# 便捷函数
def get_compliment(
    category: Optional[str] = None,
    strength: Optional[str] = None,
    language: str = "zh",
) -> str:
    """
    获取称赞语（便捷函数）
    
    Args:
        category: 类别名称（中文或英文）
        strength: 强度名称（轻度/中度/强力 或 LIGHT/MEDIUM/STRONG）
        language: 语言代码（zh 或 en）
        
    Returns:
        称赞语
    """
    cat_enum = None
    if category:
        for cat in ComplimentCategory:
            if cat.value == category or cat.name == category.upper():
                cat_enum = cat
                break
    
    str_enum = None
    if strength:
        for str_val in ComplimentStrength:
            if str_val.value == strength or str_val.name == strength.upper():
                str_enum = str_val
                break
    
    lang_enum = Language.CHINESE if language == "zh" else Language.ENGLISH
    
    return ComplimentUtils.get_compliment(category=cat_enum, strength=str_enum, language=lang_enum)


def get_personalized_compliment(name: str, language: str = "zh") -> str:
    """获取个性化称赞"""
    lang_enum = Language.CHINESE if language == "zh" else Language.ENGLISH
    return ComplimentUtils.get_personalized_compliment(name=name, language=lang_enum)


def get_daily_compliment(language: str = "zh") -> str:
    """获取每日称赞"""
    lang_enum = Language.CHINESE if language == "zh" else Language.ENGLISH
    return ComplimentUtils.get_daily_compliment(language=lang_enum)


def get_motivational_compliment(language: str = "zh") -> str:
    """获取激励性称赞"""
    lang_enum = Language.CHINESE if language == "zh" else Language.ENGLISH
    return ComplimentUtils.get_motivational_compliment(language=lang_enum)


def get_batch_compliments(count: int = 5, language: str = "zh") -> List[str]:
    """获取批量称赞"""
    lang_enum = Language.CHINESE if language == "zh" else Language.ENGLISH
    return ComplimentUtils.get_batch_compliments(count=count, language=lang_enum)


def random_compliment() -> str:
    """随机称赞"""
    return ComplimentUtils.get_compliment()