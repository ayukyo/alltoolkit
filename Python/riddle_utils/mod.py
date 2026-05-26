"""
Riddle Utilities - 谜语工具库

提供谜语的存储、获取、提示和答案验证功能。
零外部依赖，纯 Python 标准库实现。

主要功能：
- 内置谜语库（中英文，按类别分类）
- 谜语随机获取与筛选
- 渐进式提示系统
- 答案验证（支持模糊匹配）
- 谜语生成器（基于规则）
- 每日谜语

Examples:
    >>> from riddle_utils import RiddleManager
    >>> manager = RiddleManager()
    >>> riddle = manager.get_random()
    >>> print(riddle.question)
    >>> print(manager.check_answer(riddle.id, "答案"))
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Tuple, Set, Callable
from datetime import datetime, date, timedelta
import hashlib
import random
import re
import json


class RiddleCategory(Enum):
    """谜语类别"""
    OBJECT = "object"  # 物品谜
    ANIMAL = "animal"  # 动物谜
    PLANT = "plant"  # 植物谜
    NATURE = "nature"  # 自然现象
    FOOD = "food"  # 食物谜
    BODY = "body"  # 身体部位
    DAILY = "daily"  # 日常用品
    CHARACTER = "character"  # 字谜
    MATH = "math"  # 数学谜
    WORD = "word"  # 词语谜
    LATERAL = "lateral"  # 水平思考
    LOGIC = "logic"  # 逻辑谜
    HUMOR = "humor"  # 幽默谜
    CLASSIC = "classic"  # 经典谜
    SEASONAL = "seasonal"  # 季节谜


class RiddleDifficulty(Enum):
    """谜语难度"""
    EASY = 1
    MEDIUM = 2
    HARD = 3
    EXPERT = 4


class RiddleLanguage(Enum):
    """谜语语言"""
    CHINESE = "zh"
    ENGLISH = "en"
    BOTH = "both"


@dataclass
class Hint:
    """提示"""
    level: int  # 提示级别 1-5
    content: str  # 提示内容
    reveal_type: str  # reveal_type: "category", "first_letter", "length", "description"


@dataclass
class Riddle:
    """谜语"""
    id: str
    question: str  # 谜面
    answer: str  # 谜底
    category: RiddleCategory
    difficulty: RiddleDifficulty
    language: RiddleLanguage
    hints: List[Hint] = field(default_factory=list)
    explanation: str = ""  # 解析
    alternative_answers: List[str] = field(default_factory=list)  # 别名答案
    tags: List[str] = field(default_factory=list)
    author: str = ""
    source: str = ""  # 来源
    created_at: Optional[datetime] = None
    
    def __post_init__(self):
        if not self.created_at:
            self.created_at = datetime.now()


@dataclass
class RiddleSession:
    """谜语会话"""
    riddle_id: str
    hints_used: int = 0
    attempts: int = 0
    solved: bool = False
    started_at: datetime = field(default_factory=datetime.now)
    solved_at: Optional[datetime] = None
    score: int = 0
    
    def calculate_score(self, base_score: int = 100) -> int:
        """计算得分（根据提示使用次数扣分）"""
        # 提示扣分：每次使用扣15分
        hint_penalty = self.hints_used * 15
        # 错误尝试扣分：从第二次尝试开始，每次扣5分
        attempt_penalty = max(0, self.attempts - 1) * 5
        penalty = hint_penalty + attempt_penalty
        self.score = max(0, base_score - penalty)
        return self.score


class RiddleManager:
    """
    谜语管理器
    
    管理谜语库，提供获取、提示、验证等功能
    
    Examples:
        >>> manager = RiddleManager()
        >>> riddle = manager.get_random()
        >>> print(riddle.question)
        >>> hint = manager.get_hint(riddle.id, level=1)
        >>> is_correct = manager.check_answer(riddle.id, "答案")
    """
    
    def __init__(self, seed: Optional[int] = None):
        """
        初始化谜语管理器
        
        Args:
            seed: 随机种子（用于可重复结果）
        """
        self._riddles: Dict[str, Riddle] = {}
        self._sessions: Dict[str, RiddleSession] = {}
        self._seed = seed
        
        if seed is not None:
            random.seed(seed)
        
        self._load_builtin_riddles()
    
    def _load_builtin_riddles(self) -> None:
        """加载内置谜语"""
        riddles = self._get_builtin_riddles()
        for riddle in riddles:
            self._riddles[riddle.id] = riddle
    
    def _get_builtin_riddles(self) -> List[Riddle]:
        """获取内置谜语列表"""
        riddles = []
        
        # ============ 中文物品谜 ============
        riddles.extend([
            Riddle(
                id="zh_obj_001",
                question="身穿绿衣裳，肚里水汪汪，生的子儿多，个个黑脸膛。",
                answer="西瓜",
                category=RiddleCategory.OBJECT,
                difficulty=RiddleDifficulty.EASY,
                language=RiddleLanguage.CHINESE,
                hints=[
                    Hint(1, "这是一种水果", "category"),
                    Hint(2, "第一个字表示颜色", "first_letter"),
                    Hint(3, "夏天最常见", "description"),
                    Hint(4, "两个字", "length"),
                    Hint(5, "切开后有红瓤黑籽", "description"),
                ],
                explanation="西瓜外皮绿色，内部多汁，籽是黑色的。",
                tags=["水果", "夏天", "植物"]
            ),
            Riddle(
                id="zh_obj_002",
                question="有头没有颈，身上冷冰冰，有翅不能飞，无脚也能行。",
                answer="鱼",
                category=RiddleCategory.ANIMAL,
                difficulty=RiddleDifficulty.EASY,
                language=RiddleLanguage.CHINESE,
                hints=[
                    Hint(1, "这是一种动物", "category"),
                    Hint(2, "生活在水里", "description"),
                    Hint(3, "只有一个字", "length"),
                    Hint(4, "常被端上餐桌", "description"),
                    Hint(5, "有鳞片和鳍", "description"),
                ],
                explanation="鱼有头无颈，身体冰冷，鳍如翅膀但不能飞，用身体游动。",
                tags=["动物", "水生", "食物"]
            ),
            Riddle(
                id="zh_obj_003",
                question="红公鸡，绿尾巴，身子钻在泥底下。",
                answer="胡萝卜",
                category=RiddleCategory.PLANT,
                difficulty=RiddleDifficulty.EASY,
                language=RiddleLanguage.CHINESE,
                hints=[
                    Hint(1, "这是一种蔬菜", "category"),
                    Hint(2, "兔子很喜欢吃", "description"),
                    Hint(3, "三个字", "length"),
                    Hint(4, "颜色在名字里", "description"),
                    Hint(5, "根茎类蔬菜", "description"),
                ],
                explanation="胡萝卜红色的根露在上面，绿色的叶子在上面，根埋在土里。",
                tags=["蔬菜", "植物", "食物"]
            ),
            Riddle(
                id="zh_obj_004",
                question="兄弟七八个，围着柱子坐，大家一分手，衣服都扯破。",
                answer="大蒜",
                category=RiddleCategory.PLANT,
                difficulty=RiddleDifficulty.MEDIUM,
                language=RiddleLanguage.CHINESE,
                hints=[
                    Hint(1, "这是一种调味品", "category"),
                    Hint(2, "两个字", "length"),
                    Hint(3, "味道很辣", "description"),
                    Hint(4, "一瓣一瓣的", "description"),
                    Hint(5, "白色外皮", "description"),
                ],
                explanation="大蒜的蒜瓣围着一根芯，剥开时外皮会破。",
                tags=["蔬菜", "调味品", "植物"]
            ),
            Riddle(
                id="zh_obj_005",
                question="千条线，万条线，掉到水里看不见。",
                answer="雨",
                category=RiddleCategory.NATURE,
                difficulty=RiddleDifficulty.EASY,
                language=RiddleLanguage.CHINESE,
                hints=[
                    Hint(1, "这是一种自然现象", "category"),
                    Hint(2, "从天上落下来", "description"),
                    Hint(3, "一个字", "length"),
                    Hint(4, "云带来的", "description"),
                    Hint(5, "需要打伞", "description"),
                ],
                explanation="雨像线一样从天上落下来，落到水里就看不到了。",
                tags=["自然", "天气", "水"]
            ),
            Riddle(
                id="zh_obj_006",
                question="一物生得真奇怪，肚下长个皮口袋，孩子袋里吃和睡，跑得不快跳得快。",
                answer="袋鼠",
                category=RiddleCategory.ANIMAL,
                difficulty=RiddleDifficulty.MEDIUM,
                language=RiddleLanguage.CHINESE,
                hints=[
                    Hint(1, "这是一种动物", "category"),
                    Hint(2, "生活在澳大利亚", "description"),
                    Hint(3, "两个字", "length"),
                    Hint(4, "肚子上有个袋子", "description"),
                    Hint(5, "跳跃行进", "description"),
                ],
                explanation="袋鼠肚子上有个育儿袋，小袋鼠在袋子里成长，袋鼠跳跃行进。",
                tags=["动物", "澳大利亚", "有袋类"]
            ),
            Riddle(
                id="zh_obj_007",
                question="兄弟两个瘦又长，扭在一起下池塘，池塘里面打个滚，变黄变胖又喷香。",
                answer="油条",
                category=RiddleCategory.FOOD,
                difficulty=RiddleDifficulty.MEDIUM,
                language=RiddleLanguage.CHINESE,
                hints=[
                    Hint(1, "这是一种早餐食品", "category"),
                    Hint(2, "两个字", "length"),
                    Hint(3, "配豆浆很好吃", "description"),
                    Hint(4, "是炸出来的", "description"),
                    Hint(5, "两根面团扭在一起", "description"),
                ],
                explanation="油条是两根面团扭在一起，放到油锅里炸，变金黄变胖，香味扑鼻。",
                tags=["食物", "早餐", "油炸"]
            ),
            Riddle(
                id="zh_obj_008",
                question="左边一个洞，右边一个洞，中间隔座山，两个不相通。",
                answer="耳朵",
                category=RiddleCategory.BODY,
                difficulty=RiddleDifficulty.EASY,
                language=RiddleLanguage.CHINESE,
                hints=[
                    Hint(1, "这是身体的一部分", "category"),
                    Hint(2, "两个一样的", "description"),
                    Hint(3, "两个字", "length"),
                    Hint(4, "用来听声音", "description"),
                    Hint(5, "在头的两侧", "description"),
                ],
                explanation="耳朵有两个，分别在头两侧，中间隔着脑袋，互不相通。",
                tags=["身体", "器官", "感觉"]
            ),
            Riddle(
                id="zh_obj_009",
                question="一个老头，不跑不走，请他睡觉，他就摇头。",
                answer="不倒翁",
                category=RiddleCategory.OBJECT,
                difficulty=RiddleDifficulty.EASY,
                language=RiddleLanguage.CHINESE,
                hints=[
                    Hint(1, "这是一种玩具", "category"),
                    Hint(2, "三个字", "length"),
                    Hint(3, "推不倒", "description"),
                    Hint(4, "圆形底部", "description"),
                    Hint(5, "名字说明了特点", "description"),
                ],
                explanation="不倒翁是玩具，推它会摇晃但不会倒，像在摇头。",
                tags=["玩具", "物品", "儿童"]
            ),
            Riddle(
                id="zh_obj_010",
                question="会飞不是鸟，两翅没有毛，白天休息晚活动，捕捉害虫本领高。",
                answer="蝙蝠",
                category=RiddleCategory.ANIMAL,
                difficulty=RiddleDifficulty.MEDIUM,
                language=RiddleLanguage.CHINESE,
                hints=[
                    Hint(1, "这是一种动物", "category"),
                    Hint(2, "两个字", "length"),
                    Hint(3, "晚上出来活动", "description"),
                    Hint(4, "会飞但不是鸟", "description"),
                    Hint(5, "名字和福字同音", "description"),
                ],
                explanation="蝙蝠有翅膀会飞但不是鸟，没有羽毛，晚上活动，吃害虫。",
                tags=["动物", "哺乳动物", "夜行"]
            ),
        ])
        
        # ============ 字谜 ============
        riddles.extend([
            Riddle(
                id="zh_char_001",
                question="一口咬掉牛尾巴。",
                answer="告",
                category=RiddleCategory.CHARACTER,
                difficulty=RiddleDifficulty.MEDIUM,
                language=RiddleLanguage.CHINESE,
                hints=[
                    Hint(1, "这是一个字谜", "category"),
                    Hint(2, "一个字", "length"),
                    Hint(3, "把'牛'字的尾巴去掉", "description"),
                    Hint(4, "下面加个'口'", "description"),
                    Hint(5, "和'报告'有关", "description"),
                ],
                explanation="'牛'字的尾巴去掉是'⺧'，加上'口'就是'告'。",
                tags=["字谜", "汉字", "趣味"]
            ),
            Riddle(
                id="zh_char_002",
                question="一点一横长，一撇到南洋，南洋有个人，只有一寸长。",
                answer="府",
                category=RiddleCategory.CHARACTER,
                difficulty=RiddleDifficulty.HARD,
                language=RiddleLanguage.CHINESE,
                hints=[
                    Hint(1, "这是一个字谜", "category"),
                    Hint(2, "一个字", "length"),
                    Hint(3, "上面是'广'", "description"),
                    Hint(4, "下面有'付'", "description"),
                    Hint(5, "政府的'府'", "description"),
                ],
                explanation="'广'字头是一点一横一撇，下面'付'是单人旁加寸。",
                tags=["字谜", "汉字", "传统"]
            ),
            Riddle(
                id="zh_char_003",
                question="十张口，一颗心。",
                answer="思",
                category=RiddleCategory.CHARACTER,
                difficulty=RiddleDifficulty.MEDIUM,
                language=RiddleLanguage.CHINESE,
                hints=[
                    Hint(1, "这是一个字谜", "category"),
                    Hint(2, "一个字", "length"),
                    Hint(3, "'田'字像四个'口'", "description"),
                    Hint(4, "下面有个'心'", "description"),
                    Hint(5, "和'思考'有关", "description"),
                ],
                explanation="'田'可以看成四个口，加上'十'的另外部分，下面有'心'就是'思'。",
                tags=["字谜", "汉字", "趣味"]
            ),
            Riddle(
                id="zh_char_004",
                question="太阳的儿子。",
                answer="星",
                category=RiddleCategory.CHARACTER,
                difficulty=RiddleDifficulty.EASY,
                language=RiddleLanguage.CHINESE,
                hints=[
                    Hint(1, "这是一个字谜", "category"),
                    Hint(2, "一个字", "length"),
                    Hint(3, "太阳是'日'", "description"),
                    Hint(4, "儿子代表'生'", "description"),
                    Hint(5, "晚上天上的光点", "description"),
                ],
                explanation="太阳是'日'，'日'生'就是'星'。",
                tags=["字谜", "汉字", "自然"]
            ),
            Riddle(
                id="zh_char_005",
                question="一加一不是二。",
                answer="王",
                category=RiddleCategory.CHARACTER,
                difficulty=RiddleDifficulty.EASY,
                language=RiddleLanguage.CHINESE,
                hints=[
                    Hint(1, "这是一个字谜", "category"),
                    Hint(2, "一个字", "length"),
                    Hint(3, "'一'加'一'", "description"),
                    Hint(4, "再加一横", "description"),
                    Hint(5, "象棋里的将帅", "description"),
                ],
                explanation="两个'一'上下排列，中间加一横，就是'王'。",
                tags=["字谜", "汉字", "趣味"]
            ),
        ])
        
        # ============ 英文谜语 ============
        riddles.extend([
            Riddle(
                id="en_obj_001",
                question="I have keys but no locks. I have space but no room. You can enter, but never go outside. What am I?",
                answer="keyboard",
                category=RiddleCategory.OBJECT,
                difficulty=RiddleDifficulty.EASY,
                language=RiddleLanguage.ENGLISH,
                hints=[
                    Hint(1, "It's an object you use daily", "category"),
                    Hint(2, "First letter is 'K'", "first_letter"),
                    Hint(3, "It has buttons with letters", "description"),
                    Hint(4, "You use it with a computer", "description"),
                    Hint(5, "8 letters", "length"),
                ],
                explanation="A keyboard has keys (buttons) but no locks, has a space bar but no physical room.",
                alternative_answers=["computer keyboard", "a keyboard"],
                tags=["technology", "computer", "daily"]
            ),
            Riddle(
                id="en_obj_002",
                question="The more you take, the more you leave behind. What am I?",
                answer="footsteps",
                category=RiddleCategory.OBJECT,
                difficulty=RiddleDifficulty.MEDIUM,
                language=RiddleLanguage.ENGLISH,
                hints=[
                    Hint(1, "It's related to walking", "category"),
                    Hint(2, "First letter is 'F'", "first_letter"),
                    Hint(3, "You create them when you move", "description"),
                    Hint(4, "They show where you've been", "description"),
                    Hint(5, "9 letters", "length"),
                ],
                explanation="When you take footsteps, you leave footprints behind.",
                alternative_answers=["footprints", "steps", "foot prints"],
                tags=["nature", "walking", "classic"]
            ),
            Riddle(
                id="en_obj_003",
                question="I speak without a mouth and hear without ears. I have no body, but I come alive with the wind. What am I?",
                answer="echo",
                category=RiddleCategory.NATURE,
                difficulty=RiddleDifficulty.MEDIUM,
                language=RiddleLanguage.ENGLISH,
                hints=[
                    Hint(1, "It's a natural phenomenon", "category"),
                    Hint(2, "First letter is 'E'", "first_letter"),
                    Hint(3, "You hear it in mountains", "description"),
                    Hint(4, "It repeats what you say", "description"),
                    Hint(5, "4 letters", "length"),
                ],
                explanation="An echo repeats sounds without having a physical form.",
                tags=["nature", "sound", "classic"]
            ),
            Riddle(
                id="en_obj_004",
                question="What has a head and a tail but no body?",
                answer="coin",
                category=RiddleCategory.OBJECT,
                difficulty=RiddleDifficulty.EASY,
                language=RiddleLanguage.ENGLISH,
                hints=[
                    Hint(1, "It's a small metal object", "category"),
                    Hint(2, "First letter is 'C'", "first_letter"),
                    Hint(3, "You use it to buy things", "description"),
                    Hint(4, "It has two sides", "description"),
                    Hint(5, "4 letters", "length"),
                ],
                explanation="A coin has a 'head' (front) and 'tail' (back) but no body.",
                tags=["money", "object", "wordplay"]
            ),
            Riddle(
                id="en_obj_005",
                question="What can travel around the world while staying in a corner?",
                answer="stamp",
                category=RiddleCategory.OBJECT,
                difficulty=RiddleDifficulty.MEDIUM,
                language=RiddleLanguage.ENGLISH,
                hints=[
                    Hint(1, "It's a small paper item", "category"),
                    Hint(2, "First letter is 'S'", "first_letter"),
                    Hint(3, "It goes on envelopes", "description"),
                    Hint(4, "You need it to mail things", "description"),
                    Hint(5, "4 letters", "length"),
                ],
                explanation="A stamp sits in the corner of an envelope but can travel anywhere.",
                tags=["mail", "travel", "classic"]
            ),
            Riddle(
                id="en_obj_006",
                question="I'm tall when I'm young and short when I'm old. What am I?",
                answer="candle",
                category=RiddleCategory.OBJECT,
                difficulty=RiddleDifficulty.EASY,
                language=RiddleLanguage.ENGLISH,
                hints=[
                    Hint(1, "It provides light", "category"),
                    Hint(2, "First letter is 'C'", "first_letter"),
                    Hint(3, "You light it on fire", "description"),
                    Hint(4, "It melts over time", "description"),
                    Hint(5, "6 letters", "length"),
                ],
                explanation="A candle is tall when new but gets shorter as it burns.",
                tags=["object", "fire", "classic"]
            ),
            Riddle(
                id="en_obj_007",
                question="What has hands but cannot clap?",
                answer="clock",
                category=RiddleCategory.OBJECT,
                difficulty=RiddleDifficulty.EASY,
                language=RiddleLanguage.ENGLISH,
                hints=[
                    Hint(1, "It's something you look at", "category"),
                    Hint(2, "First letter is 'C'", "first_letter"),
                    Hint(3, "It tells you something", "description"),
                    Hint(4, "It has a face", "description"),
                    Hint(5, "5 letters", "length"),
                ],
                explanation="A clock has hands (hour, minute, second) but cannot clap.",
                alternative_answers=["watch"],
                tags=["time", "object", "wordplay"]
            ),
            Riddle(
                id="en_obj_008",
                question="What has legs but cannot walk?",
                answer="table",
                category=RiddleCategory.OBJECT,
                difficulty=RiddleDifficulty.EASY,
                language=RiddleLanguage.ENGLISH,
                hints=[
                    Hint(1, "It's a piece of furniture", "category"),
                    Hint(2, "First letter is 'T'", "first_letter"),
                    Hint(3, "You put things on it", "description"),
                    Hint(4, "You can sit at it", "description"),
                    Hint(5, "5 letters", "length"),
                ],
                explanation="Tables have legs but cannot walk.",
                alternative_answers=["chair", "desk", "stool"],
                tags=["furniture", "object", "wordplay"]
            ),
        ])
        
        # ============ 水平思考谜题 ============
        riddles.extend([
            Riddle(
                id="en_lateral_001",
                question="A man pushes his car to a hotel and tells the owner he's bankrupt. Why?",
                answer="he is playing monopoly",
                category=RiddleCategory.LATERAL,
                difficulty=RiddleDifficulty.HARD,
                language=RiddleLanguage.ENGLISH,
                hints=[
                    Hint(1, "This is not about a real car", "category"),
                    Hint(2, "Think about games", "description"),
                    Hint(3, "The 'hotel' is also part of the game", "description"),
                    Hint(4, "It's a board game", "description"),
                    Hint(5, "The car is a playing piece", "description"),
                ],
                explanation="He's playing Monopoly and his piece landed on a hotel property he can't afford.",
                alternative_answers=["monopoly", "playing monopoly", "it is monopoly"],
                tags=["lateral", "game", "classic"]
            ),
            Riddle(
                id="en_lateral_002",
                question="A woman shoots her husband. Then she holds him under water for over 5 minutes. Finally, she hangs him. But 5 minutes later they both go out together and enjoy a wonderful dinner. How is this possible?",
                answer="she is a photographer",
                category=RiddleCategory.LATERAL,
                difficulty=RiddleDifficulty.HARD,
                language=RiddleLanguage.ENGLISH,
                hints=[
                    Hint(1, "The words have different meanings", "category"),
                    Hint(2, "Think about photography", "description"),
                    Hint(3, "'Shoot' can mean take a picture", "description"),
                    Hint(4, "'Hang' can mean display", "description"),
                    Hint(5, "Water is part of developing photos", "description"),
                ],
                explanation="She's a photographer - she shoots (takes photos), develops (water), and hangs (displays) his picture.",
                alternative_answers=["photographer", "taking photos", "photography"],
                tags=["lateral", "wordplay", "classic"]
            ),
        ])
        
        # ============ 数学谜题 ============
        riddles.extend([
            Riddle(
                id="math_001",
                question="如果 1=5，2=25，3=125，4=625，那么 5=?",
                answer="1",
                category=RiddleCategory.MATH,
                difficulty=RiddleDifficulty.HARD,
                language=RiddleLanguage.CHINESE,
                hints=[
                    Hint(1, "仔细看第一个等式", "description"),
                    Hint(2, "不要被规律迷惑", "description"),
                    Hint(3, "如果 1=5，那么 5=?", "description"),
                    Hint(4, "这是等式，不是函数", "description"),
                    Hint(5, "等号是双向的", "description"),
                ],
                explanation="既然 1=5，那么 5=1，等号是双向的。很多人会算出 5=3125，但第一行已经给出了答案。",
                tags=["数学", "逻辑", "陷阱"]
            ),
            Riddle(
                id="math_002",
                question="一个篮子里有 5 个苹果，要分给 5 个人，每人分到一个，但篮子里还要剩一个，怎么分？",
                answer="最后一个人连篮子一起拿",
                category=RiddleCategory.MATH,
                difficulty=RiddleDifficulty.MEDIUM,
                language=RiddleLanguage.CHINESE,
                hints=[
                    Hint(1, "篮子也可以被拿走", "description"),
                    Hint(2, "题目没说苹果要单独拿出来", "description"),
                    Hint(3, "想想'篮子里剩一个'的另一种理解", "description"),
                    Hint(4, "最后一个人可以拿着篮子", "description"),
                    Hint(5, "苹果在篮子里，人拿着篮子", "description"),
                ],
                explanation="4个人各拿一个苹果，最后一个人连苹果带篮子一起拿走，篮子里还剩一个苹果。",
                tags=["数学", "逻辑", "脑筋急转弯"]
            ),
        ])
        
        # ============ 幽默谜题 ============
        riddles.extend([
            Riddle(
                id="zh_humor_001",
                question="什么水不能喝？",
                answer="薪水",
                category=RiddleCategory.HUMOR,
                difficulty=RiddleDifficulty.EASY,
                language=RiddleLanguage.CHINESE,
                hints=[
                    Hint(1, "这是谐音谜", "description"),
                    Hint(2, "和工作有关", "description"),
                    Hint(3, "两个字的词", "length"),
                    Hint(4, "每个月都有", "description"),
                    Hint(5, "和钱有关", "description"),
                ],
                explanation="'薪水'里的'水'是谐音，指的是工资，不是真的水。",
                tags=["幽默", "谐音", "工作"]
            ),
            Riddle(
                id="zh_humor_002",
                question="为什么青蛙跳得比树高？",
                answer="树不会跳",
                category=RiddleCategory.HUMOR,
                difficulty=RiddleDifficulty.EASY,
                language=RiddleLanguage.CHINESE,
                hints=[
                    Hint(1, "这是一个脑筋急转弯", "description"),
                    Hint(2, "想想树能做什么", "description"),
                    Hint(3, "青蛙能跳", "description"),
                    Hint(4, "树能...", "description"),
                    Hint(5, "树不能跳", "description"),
                ],
                explanation="树根本不会跳，所以青蛙当然跳得比树高。",
                tags=["幽默", "脑筋急转弯", "经典"]
            ),
            Riddle(
                id="zh_humor_003",
                question="什么东西越洗越脏？",
                answer="水",
                category=RiddleCategory.HUMOR,
                difficulty=RiddleDifficulty.EASY,
                language=RiddleLanguage.CHINESE,
                hints=[
                    Hint(1, "想想'洗'的过程", "description"),
                    Hint(2, "用什么来洗", "description"),
                    Hint(3, "一个字", "length"),
                    Hint(4, "洗东西的时候它变脏了", "description"),
                    Hint(5, "洗完后水变黑了", "description"),
                ],
                explanation="用水洗东西，脏东西进入水里，水就变脏了。",
                tags=["幽默", "脑筋急转弯", "生活"]
            ),
        ])
        
        return riddles
    
    def get_riddle(self, riddle_id: str) -> Optional[Riddle]:
        """
        根据 ID 获取谜语
        
        Args:
            riddle_id: 谜语 ID
            
        Returns:
            谜语对象，如果不存在返回 None
        """
        return self._riddles.get(riddle_id)
    
    def get_random(
        self,
        category: Optional[RiddleCategory] = None,
        difficulty: Optional[RiddleDifficulty] = None,
        language: Optional[RiddleLanguage] = None
    ) -> Riddle:
        """
        获取随机谜语
        
        Args:
            category: 类别过滤
            difficulty: 难度过滤
            language: 语言过滤
            
        Returns:
            随机谜语
        """
        candidates = list(self._riddles.values())
        
        if category:
            candidates = [r for r in candidates if r.category == category]
        if difficulty:
            candidates = [r for r in candidates if r.difficulty == difficulty]
        if language:
            candidates = [r for r in candidates if r.language == language or r.language == RiddleLanguage.BOTH]
        
        if not candidates:
            raise ValueError("没有符合条件的谜语")
        
        return random.choice(candidates)
    
    def get_by_category(self, category: RiddleCategory) -> List[Riddle]:
        """获取指定类别的所有谜语"""
        return [r for r in self._riddles.values() if r.category == category]
    
    def get_by_difficulty(self, difficulty: RiddleDifficulty) -> List[Riddle]:
        """获取指定难度的所有谜语"""
        return [r for r in self._riddles.values() if r.difficulty == difficulty]
    
    def get_hint(self, riddle_id: str, level: int = 1) -> Optional[Hint]:
        """
        获取谜语提示
        
        Args:
            riddle_id: 谜语 ID
            level: 提示级别 1-5（1 最隐晦，5 最明显）
            
        Returns:
            提示对象
        """
        riddle = self.get_riddle(riddle_id)
        if not riddle:
            return None
        
        if level < 1 or level > 5:
            raise ValueError("提示级别必须在 1-5 之间")
        
        # 找到不超过请求级别的最接近提示
        available_hints = [h for h in riddle.hints if h.level <= level]
        if not available_hints:
            return None
        
        # 返回最高级别的可用提示
        return max(available_hints, key=lambda h: h.level)
    
    def get_all_hints(self, riddle_id: str) -> List[Hint]:
        """获取谜语的所有提示（按级别排序）"""
        riddle = self.get_riddle(riddle_id)
        if not riddle:
            return []
        return sorted(riddle.hints, key=lambda h: h.level)
    
    def check_answer(
        self,
        riddle_id: str,
        answer: str,
        fuzzy: bool = True,
        case_sensitive: bool = False
    ) -> Tuple[bool, str]:
        """
        检查答案
        
        Args:
            riddle_id: 谜语 ID
            answer: 用户答案
            fuzzy: 是否启用模糊匹配（忽略空格、标点等）
            case_sensitive: 是否区分大小写
            
        Returns:
            (是否正确, 反馈消息)
        """
        riddle = self.get_riddle(riddle_id)
        if not riddle:
            return False, "谜语不存在"
        
        def normalize(s: str) -> str:
            """标准化字符串"""
            s = s.strip()
            if not case_sensitive:
                s = s.lower()
            if fuzzy:
                # 移除空格和常见标点
                s = re.sub(r'[\s\-_\.,;:!?。，；：！？]', '', s)
            return s
        
        normalized_answer = normalize(answer)
        normalized_correct = normalize(riddle.answer)
        
        # 检查主答案
        if normalized_answer == normalized_correct:
            return True, "🎉 正确！你真聪明！"
        
        # 检查别名答案
        for alt in riddle.alternative_answers:
            if normalized_answer == normalize(alt):
                return True, "🎉 正确！你真聪明！"
        
        # 模糊匹配（相似度）
        if fuzzy:
            similarity = self._calculate_similarity(normalized_answer, normalized_correct)
            if similarity >= 0.8:
                return True, f"🎉 基本正确！答案是「{riddle.answer}」"
        
        return False, "❌ 不对哦，再想想？"
    
    def _calculate_similarity(self, s1: str, s2: str) -> float:
        """计算字符串相似度（Levenshtein 距离）"""
        if not s1 or not s2:
            return 0.0
        
        m, n = len(s1), len(s2)
        dp = [[0] * (n + 1) for _ in range(m + 1)]
        
        for i in range(m + 1):
            dp[i][0] = i
        for j in range(n + 1):
            dp[0][j] = j
        
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if s1[i-1] == s2[j-1]:
                    dp[i][j] = dp[i-1][j-1]
                else:
                    dp[i][j] = min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1]) + 1
        
        distance = dp[m][n]
        max_len = max(m, n)
        return 1 - distance / max_len if max_len > 0 else 1.0
    
    def create_session(self, riddle_id: str) -> RiddleSession:
        """创建谜语会话"""
        session = RiddleSession(riddle_id=riddle_id)
        self._sessions[f"{riddle_id}_{datetime.now().timestamp()}"] = session
        return session
    
    def get_daily_riddle(self, date_obj: Optional[date] = None) -> Riddle:
        """
        获取每日谜语
        
        基于日期确定性地选择谜语
        
        Args:
            date_obj: 日期对象，默认今天
            
        Returns:
            每日谜语
        """
        if date_obj is None:
            date_obj = date.today()
        
        date_str = date_obj.isoformat()
        hash_val = int(hashlib.md5(date_str.encode()).hexdigest(), 16)
        riddles = list(self._riddles.values())
        index = hash_val % len(riddles)
        return riddles[index]
    
    def add_riddle(self, riddle: Riddle) -> None:
        """添加自定义谜语"""
        self._riddles[riddle.id] = riddle
    
    def remove_riddle(self, riddle_id: str) -> bool:
        """移除谜语"""
        if riddle_id in self._riddles:
            del self._riddles[riddle_id]
            return True
        return False
    
    def get_categories(self) -> List[RiddleCategory]:
        """获取所有谜语类别"""
        return list(set(r.category for r in self._riddles.values()))
    
    def get_difficulties(self) -> List[RiddleDifficulty]:
        """获取所有难度级别"""
        return list(RiddleDifficulty)
    
    def get_languages(self) -> List[RiddleLanguage]:
        """获取所有语言"""
        return list(RiddleLanguage)
    
    def count(self) -> int:
        """获取谜语总数"""
        return len(self._riddles)
    
    def count_by_category(self) -> Dict[RiddleCategory, int]:
        """按类别统计谜语数量"""
        counts = {}
        for r in self._riddles.values():
            counts[r.category] = counts.get(r.category, 0) + 1
        return counts
    
    def search(self, keyword: str) -> List[Riddle]:
        """
        搜索谜语
        
        Args:
            keyword: 搜索关键词
            
        Returns:
            匹配的谜语列表
        """
        keyword = keyword.lower()
        results = []
        
        for r in self._riddles.values():
            if (keyword in r.question.lower() or
                keyword in r.answer.lower() or
                any(keyword in tag.lower() for tag in r.tags)):
                results.append(r)
        
        return results
    
    def export_to_dict(self) -> Dict:
        """导出为字典（用于序列化）"""
        return {
            "riddles": [
                {
                    "id": r.id,
                    "question": r.question,
                    "answer": r.answer,
                    "category": r.category.value,
                    "difficulty": r.difficulty.value,
                    "language": r.language.value,
                    "hints": [{"level": h.level, "content": h.content, "reveal_type": h.reveal_type} for h in r.hints],
                    "explanation": r.explanation,
                    "alternative_answers": r.alternative_answers,
                    "tags": r.tags,
                    "author": r.author,
                    "source": r.source,
                }
                for r in self._riddles.values()
            ]
        }
    
    def import_from_dict(self, data: Dict) -> None:
        """从字典导入"""
        for r_data in data.get("riddles", []):
            riddle = Riddle(
                id=r_data["id"],
                question=r_data["question"],
                answer=r_data["answer"],
                category=RiddleCategory(r_data["category"]),
                difficulty=RiddleDifficulty(r_data["difficulty"]),
                language=RiddleLanguage(r_data["language"]),
                hints=[Hint(h["level"], h["content"], h["reveal_type"]) for h in r_data.get("hints", [])],
                explanation=r_data.get("explanation", ""),
                alternative_answers=r_data.get("alternative_answers", []),
                tags=r_data.get("tags", []),
                author=r_data.get("author", ""),
                source=r_data.get("source", ""),
            )
            self._riddles[riddle.id] = riddle


class RiddleGenerator:
    """
    谜语生成器
    
    基于规则生成简单谜语
    
    Examples:
        >>> gen = RiddleGenerator()
        >>> riddle = gen.generate_object_riddle("钟表", "计时工具，有指针，会走动")
        >>> print(riddle.question)
    """
    
    # 物品特征模板
    OBJECT_TEMPLATES = [
        "我有{name}但没有{missing}，我能{ability}但不能{cannot}。我是什么？",
        "没有{missing}，却有{name}，整天{ability}，从来{cannot}。猜猜我是谁？",
        "{feature1}是我的特点，{feature2}是我的本领，{feature3}是我的命运。",
    ]
    
    def __init__(self, seed: Optional[int] = None):
        if seed is not None:
            random.seed(seed)
    
    def generate_object_riddle(
        self,
        name: str,
        features: Dict[str, str],
        difficulty: RiddleDifficulty = RiddleDifficulty.MEDIUM
    ) -> Riddle:
        """
        生成物品谜语
        
        Args:
            name: 物品名称（答案）
            features: 特征字典，包含：
                - missing: 没有的东西
                - ability: 能做的事情
                - cannot: 不能做的事情
                - feature1, feature2, feature3: 特征描述
                
        Returns:
            生成的谜语
        """
        template = random.choice(self.OBJECT_TEMPLATES)
        
        question = template.format(
            name=features.get("name", "头"),
            missing=features.get("missing", "身"),
            ability=features.get("ability", "动"),
            cannot=features.get("cannot", "走"),
            feature1=features.get("feature1", "有用"),
            feature2=features.get("feature2", "能干"),
            feature3=features.get("feature3", "被人用"),
        )
        
        hints = []
        if "category_hint" in features:
            hints.append(Hint(1, features["category_hint"], "category"))
        if "first_letter" in features:
            hints.append(Hint(2, f"第一个字是'{features['first_letter']}'", "first_letter"))
        hints.append(Hint(4, f"{len(name)}个字", "length"))
        
        return Riddle(
            id=f"gen_{name}_{datetime.now().timestamp():.0f}",
            question=question,
            answer=name,
            category=RiddleCategory.OBJECT,
            difficulty=difficulty,
            language=RiddleLanguage.CHINESE,
            hints=hints,
            explanation=features.get("explanation", f"答案是{name}。"),
            tags=["自动生成", "物品"],
        )
    
    def generate_character_riddle(
        self,
        character: str,
        composition: str,
        meaning: str,
        difficulty: RiddleDifficulty = RiddleDifficulty.MEDIUM
    ) -> Riddle:
        """
        生成字谜
        
        Args:
            character: 汉字（答案）
            composition: 结构描述
            meaning: 含义提示
            
        Returns:
            生成的字谜
        """
        question = f"{composition}，猜一个字。"
        
        hints = [
            Hint(1, f"和'{meaning}'有关", "description"),
            Hint(2, f"这个字的意思是：{meaning}", "description"),
            Hint(3, f"{len(character)}个字", "length"),
        ]
        
        return Riddle(
            id=f"gen_char_{character}_{datetime.now().timestamp():.0f}",
            question=question,
            answer=character,
            category=RiddleCategory.CHARACTER,
            difficulty=difficulty,
            language=RiddleLanguage.CHINESE,
            hints=hints,
            explanation=f"'{character}'字{composition}。",
            tags=["自动生成", "字谜"],
        )


class RiddleQuiz:
    """
    谜语问答游戏
    
    管理谜语游戏的流程和计分
    
    Examples:
        >>> quiz = RiddleQuiz()
        >>> quiz.start_round(category=RiddleCategory.ANIMAL)
        >>> print(quiz.current_question())
        >>> hint = quiz.get_hint()
        >>> result = quiz.answer("答案")
        >>> print(f"得分: {result['score']}")
    """
    
    def __init__(self, manager: Optional[RiddleManager] = None):
        self.manager = manager or RiddleManager()
        self._session: Optional[RiddleSession] = None
        self._current_riddle: Optional[Riddle] = None
        self._total_score = 0
        self._rounds_played = 0
        self._correct_answers = 0
    
    def start_round(
        self,
        category: Optional[RiddleCategory] = None,
        difficulty: Optional[RiddleDifficulty] = None,
        language: Optional[RiddleLanguage] = None
    ) -> Riddle:
        """
        开始新一轮
        
        Args:
            category: 类别过滤
            difficulty: 难度过滤
            language: 语言过滤
            
        Returns:
            当前谜语
        """
        self._current_riddle = self.manager.get_random(category, difficulty, language)
        self._session = RiddleSession(riddle_id=self._current_riddle.id)
        self._rounds_played += 1
        return self._current_riddle
    
    def current_question(self) -> str:
        """获取当前问题"""
        if not self._current_riddle:
            raise ValueError("请先调用 start_round() 开始游戏")
        return self._current_riddle.question
    
    def get_hint(self) -> str:
        """获取提示"""
        if not self._current_riddle or not self._session:
            raise ValueError("请先调用 start_round() 开始游戏")
        
        self._session.hints_used += 1
        hint = self.manager.get_hint(self._current_riddle.id, level=self._session.hints_used)
        
        if hint:
            return f"💡 提示 {hint.level}: {hint.content}"
        return "没有更多提示了"
    
    def answer(self, user_answer: str) -> Dict:
        """
        提交答案
        
        Args:
            user_answer: 用户答案
            
        Returns:
            结果字典，包含是否正确、反馈、得分等
        """
        if not self._current_riddle or not self._session:
            raise ValueError("请先调用 start_round() 开始游戏")
        
        self._session.attempts += 1
        is_correct, feedback = self.manager.check_answer(
            self._current_riddle.id, user_answer
        )
        
        result = {
            "correct": is_correct,
            "feedback": feedback,
            "attempts": self._session.attempts,
            "hints_used": self._session.hints_used,
            "answer": self._current_riddle.answer,
            "explanation": self._current_riddle.explanation,
        }
        
        if is_correct:
            self._session.solved = True
            self._session.solved_at = datetime.now()
            score = self._session.calculate_score()
            self._total_score += score
            self._correct_answers += 1
            result["score"] = score
            result["total_score"] = self._total_score
        else:
            result["score"] = 0
        
        return result
    
    def give_up(self) -> Dict:
        """放弃当前谜语"""
        if not self._current_riddle:
            raise ValueError("请先调用 start_round() 开始游戏")
        
        return {
            "correct": False,
            "feedback": "放弃了！",
            "answer": self._current_riddle.answer,
            "explanation": self._current_riddle.explanation,
            "hints_used": self._session.hints_used if self._session else 0,
            "attempts": self._session.attempts if self._session else 0,
        }
    
    def get_stats(self) -> Dict:
        """获取游戏统计"""
        return {
            "rounds_played": self._rounds_played,
            "correct_answers": self._correct_answers,
            "total_score": self._total_score,
            "accuracy": self._correct_answers / self._rounds_played if self._rounds_played > 0 else 0,
        }
    
    def reset(self) -> None:
        """重置游戏"""
        self._session = None
        self._current_riddle = None
        self._total_score = 0
        self._rounds_played = 0
        self._correct_answers = 0


# 便捷函数
def get_random_riddle(
    category: Optional[str] = None,
    difficulty: Optional[int] = None,
    language: Optional[str] = None
) -> Riddle:
    """
    获取随机谜语
    
    Args:
        category: 类别名称字符串
        difficulty: 难度级别 1-4
        language: 语言代码 'zh' 或 'en'
        
    Returns:
        随机谜语
    """
    manager = RiddleManager()
    
    cat = None
    if category:
        try:
            cat = RiddleCategory(category.lower())
        except ValueError:
            pass
    
    diff = None
    if difficulty:
        try:
            diff = RiddleDifficulty(difficulty)
        except ValueError:
            pass
    
    lang = None
    if language:
        try:
            lang = RiddleLanguage(language.lower())
        except ValueError:
            pass
    
    return manager.get_random(category=cat, difficulty=diff, language=lang)


def get_daily_riddle() -> Riddle:
    """获取今日谜语"""
    manager = RiddleManager()
    return manager.get_daily_riddle()


def check_riddle_answer(riddle_id: str, answer: str) -> Tuple[bool, str]:
    """
    检查谜语答案
    
    Args:
        riddle_id: 谜语 ID
        answer: 用户答案
        
    Returns:
        (是否正确, 反馈消息)
    """
    manager = RiddleManager()
    return manager.check_answer(riddle_id, answer)


if __name__ == "__main__":
    # 简单演示
    manager = RiddleManager()
    
    print("=== 谜语工具库演示 ===\n")
    
    # 获取随机谜语
    riddle = manager.get_random()
    print(f"谜面：{riddle.question}")
    print(f"类别：{riddle.category.value}")
    print(f"难度：{riddle.difficulty.name}\n")
    
    # 获取提示
    hint = manager.get_hint(riddle.id, level=1)
    if hint:
        print(f"提示：{hint.content}\n")
    
    # 检查答案
    is_correct, feedback = manager.check_answer(riddle.id, riddle.answer)
    print(f"答案：{riddle.answer}")
    print(f"结果：{feedback}")
    print(f"解释：{riddle.explanation}\n")
    
    # 统计
    print(f"谜语总数：{manager.count()}")
    print(f"类别分布：{[(k.value, v) for k, v in manager.count_by_category().items()]}")