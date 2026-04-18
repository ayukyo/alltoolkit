"""
塔罗牌工具模块 (Tarot Card Utilities)
提供完整的塔罗牌牌组、抽牌、牌阵解读等功能
零外部依赖，纯 Python 标准库实现

功能：
- 完整 78 张塔罗牌牌组（22张大阿卡纳 + 56张小阿卡纳）
- 单牌抽取
- 三牌牌阵（过去/现在/未来）
- 凯尔特十字牌阵（10张牌）
- 牌面解读
- 正位/逆位判断
- 牌组信息查询
"""

import random
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
from enum import Enum


class CardType(Enum):
    """牌的类型"""
    MAJOR_ARCANA = "大阿卡纳"
    MINOR_ARCANA = "小阿卡纳"


class Suit(Enum):
    """小阿卡纳花色"""
    WANDS = "权杖"
    CUPS = "圣杯"
    SWORDS = "宝剑"
    PENTACLES = "金币"


class Orientation(Enum):
    """牌的朝向"""
    UPRIGHT = "正位"
    REVERSED = "逆位"


@dataclass
class TarotCard:
    """塔罗牌数据结构"""
    id: int
    name: str
    english_name: str
    card_type: CardType
    suit: Optional[Suit]
    number: Optional[int]  # 小阿卡纳编号 1-14 (A-10, 侍从/骑士/王后/国王)
    keywords_upright: List[str]
    keywords_reversed: List[str]
    meaning_upright: str
    meaning_reversed: str
    element: Optional[str] = None  # 元素属性
    zodiac: Optional[str] = None  # 对应星座
    planet: Optional[str] = None   # 对应行星


# 大阿卡纳牌组 (22张)
MAJOR_ARCANA = [
    TarotCard(
        id=0, name="愚者", english_name="The Fool",
        card_type=CardType.MAJOR_ARCANA, suit=None, number=None,
        keywords_upright=["新开始", "冒险", "纯真", "自由", "自发"],
        keywords_reversed=["鲁莽", "轻率", "愚蠢", "冒险精神过头"],
        meaning_upright="愚者代表新的旅程即将开始，保持开放的心态，拥抱未知的可能性。这是一张充满希望和潜力的牌。",
        meaning_reversed="逆位的愚者警告你可能过于鲁莽或轻率。在行动前请三思，不要因为冲动而做出错误决定。",
        element="风", planet="天王星"
    ),
    TarotCard(
        id=1, name="魔术师", english_name="The Magician",
        card_type=CardType.MAJOR_ARCANA, suit=None, number=None,
        keywords_upright=["创造力", "技能", "意志力", "资源", "新机会"],
        keywords_reversed=["操纵", "欺骗", "浪费才能", "缺乏计划"],
        meaning_upright="魔术师象征着你有能力将想法变为现实。你拥有所需的一切资源，只需要行动起来。",
        meaning_reversed="逆位的魔术师提醒你可能正在浪费自己的才能，或者有人正在试图欺骗你。",
        element="风", planet="水星"
    ),
    TarotCard(
        id=2, name="女祭司", english_name="The High Priestess",
        card_type=CardType.MAJOR_ARCANA, suit=None, number=None,
        keywords_upright=["直觉", "神秘", "潜意识", "内在智慧", "隐藏知识"],
        keywords_reversed=["秘密", "脱离现实", "隐瞒真相", "表面化"],
        meaning_upright="女祭司邀请你倾听内心的声音。答案就在你的潜意识中，静下心来便能听见。",
        meaning_reversed="逆位表示你可能忽视了直觉，或者有人在隐藏重要信息。",
        element="水", planet="月亮"
    ),
    TarotCard(
        id=3, name="女皇", english_name="The Empress",
        card_type=CardType.MAJOR_ARCANA, suit=None, number=None,
        keywords_upright=["丰饶", "母性", "创造力", "自然", "富足"],
        keywords_reversed=["依赖", "空虚", "创意枯竭", "过度保护"],
        meaning_upright="女皇代表丰盛与创造。这是孕育新事物、享受生活美好的时期。",
        meaning_reversed="逆位提醒你要注意是否过度依赖他人，或者自己的创造力正在枯竭。",
        element="地", planet="金星"
    ),
    TarotCard(
        id=4, name="皇帝", english_name="The Emperor",
        card_type=CardType.MAJOR_ARCANA, suit=None, number=None,
        keywords_upright=["权威", "结构", "控制", "父亲形象", "稳定"],
        keywords_reversed=["专制", "僵化", "控制欲", "滥用权力"],
        meaning_upright="皇帝象征秩序与权威。现在是建立结构、承担责任的时候。",
        meaning_reversed="逆位警告你可能过于专制，或者正在面对一个滥用权力的人。",
        element="火", planet="白羊座"
    ),
    TarotCard(
        id=5, name="教皇", english_name="The Hierophant",
        card_type=CardType.MAJOR_ARCANA, suit=None, number=None,
        keywords_upright=["传统", "信仰", "教育", "精神指引", " conformity"],
        keywords_reversed=["叛逆", "打破常规", "新观点", "自由思想"],
        meaning_upright="教皇代表传统价值观和信仰体系。寻求精神指引或遵循传统路径可能是正确的选择。",
        meaning_reversed="逆位暗示你可能需要打破常规，走一条与众不同的道路。",
        element="地", planet="金牛座"
    ),
    TarotCard(
        id=6, name="恋人", english_name="The Lovers",
        card_type=CardType.MAJOR_ARCANA, suit=None, number=None,
        keywords_upright=["爱情", "选择", "关系", "价值观", "和谐"],
        keywords_reversed=["不和谐", "失衡", "错误选择", "价值观冲突"],
        meaning_upright="恋人牌象征重要的选择和关系。这是关于爱与和谐的时期，但要做出明智的选择。",
        meaning_reversed="逆位提示关系中的不和谐，或者你正在面临价值观的冲突。",
        element="风", planet="双子座"
    ),
    TarotCard(
        id=7, name="战车", english_name="The Chariot",
        card_type=CardType.MAJOR_ARCANA, suit=None, number=None,
        keywords_upright=["胜利", "意志力", "决心", "控制", "进展"],
        keywords_reversed=["失控", "攻击性", "方向迷失", "障碍"],
        meaning_upright="战车代表通过决心和意志力获得胜利。保持专注，你将克服障碍达成目标。",
        meaning_reversed="逆位暗示你正在失去控制，或者过度的攻击性反而造成障碍。",
        element="水", planet="巨蟹座"
    ),
    TarotCard(
        id=8, name="力量", english_name="Strength",
        card_type=CardType.MAJOR_ARCANA, suit=None, number=None,
        keywords_upright=["勇气", "耐心", "内在力量", "温柔控制", "自信"],
        keywords_reversed=["自我怀疑", "软弱", "缺乏自信", "过度使用力量"],
        meaning_upright="力量牌提醒你，真正的力量来自内心的勇气和耐心，而非蛮力。相信自己。",
        meaning_reversed="逆位表示你可能正在经历自我怀疑，或者错误地使用了你的力量。",
        element="火", planet="狮子座"
    ),
    TarotCard(
        id=9, name="隐士", english_name="The Hermit",
        card_type=CardType.MAJOR_ARCANA, suit=None, number=None,
        keywords_upright=["内省", "独处", "寻求真理", "智慧", "指引"],
        keywords_reversed=["孤立", "孤独", "退缩", "拒绝帮助"],
        meaning_upright="隐士邀请你暂时抽离喧嚣，独自思考。答案在内心深处等待被发现。",
        meaning_reversed="逆位警告你可能在过度孤立自己，或者拒绝接受他人的帮助。",
        element="地", planet="处女座"
    ),
    TarotCard(
        id=10, name="命运之轮", english_name="Wheel of Fortune",
        card_type=CardType.MAJOR_ARCANA, suit=None, number=None,
        keywords_upright=["改变", "循环", "命运", "机遇", "转折点"],
        keywords_reversed=["厄运", "抗拒改变", "失控", "命运逆转"],
        meaning_upright="命运之轮预示着变化的到来。命运的转折点即将出现，拥抱变化吧。",
        meaning_reversed="逆位暗示你可能正在抗拒必要的改变，或者经历一段不如意的时期。",
        element="火", planet="木星"
    ),
    TarotCard(
        id=11, name="正义", english_name="Justice",
        card_type=CardType.MAJOR_ARCANA, suit=None, number=None,
        keywords_upright=["公正", "真相", "因果", "法律", "平衡"],
        keywords_reversed=["不公", "逃避责任", "偏见", "法律问题"],
        meaning_upright="正义牌提醒你，公正和真相终将得到彰显。你的决定将产生深远影响。",
        meaning_reversed="逆位暗示不公正的情况，或者你正在试图逃避应承担的责任。",
        element="风", planet="天秤座"
    ),
    TarotCard(
        id=12, name="倒吊人", english_name="The Hanged Man",
        card_type=CardType.MAJOR_ARCANA, suit=None, number=None,
        keywords_upright=["牺牲", "等待", "新视角", "放手", "停滞"],
        keywords_reversed=["拖延", "无谓牺牲", "反抗改变", "僵局"],
        meaning_upright="倒吊人邀请你换个角度看问题。有时暂时的停滞是为了更好的前进。",
        meaning_reversed="逆位提示你可能在无谓地牺牲，或者在拖延必要的决定。",
        element="水", planet="海王星"
    ),
    TarotCard(
        id=13, name="死神", english_name="Death",
        card_type=CardType.MAJOR_ARCANA, suit=None, number=None,
        keywords_upright=["转变", "结束", "重生", "放下", "新开始"],
        keywords_reversed=["抗拒改变", "停滞不前", "无法放手", "恐惧"],
        meaning_upright="死神牌象征着转变与重生。旧的正在结束，新的即将开始，接受变化吧。",
        meaning_reversed="逆位表示你正在抗拒必要的改变，导致停滞不前。",
        element="水", planet="天蝎座"
    ),
    TarotCard(
        id=14, name="节制", english_name="Temperance",
        card_type=CardType.MAJOR_ARCANA, suit=None, number=None,
        keywords_upright=["平衡", "调和", "耐心", "适度", "治愈"],
        keywords_reversed=["失衡", "过度", "缺乏耐心", "冲突"],
        meaning_upright="节制牌提醒你寻求平衡与和谐。耐心和适度是成功的关键。",
        meaning_reversed="逆位暗示生活中的失衡，或者你正在某个方面过度。",
        element="火", planet="射手座"
    ),
    TarotCard(
        id=15, name="恶魔", english_name="The Devil",
        card_type=CardType.MAJOR_ARCANA, suit=None, number=None,
        keywords_upright=["束缚", "诱惑", "物质主义", "阴影面", "依赖"],
        keywords_reversed=["解放", "突破", "摆脱束缚", "面对阴影"],
        meaning_upright="恶魔牌揭示了你可能正在被某些东西束缚——可能是习惯、关系或欲望。",
        meaning_reversed="逆位是积极的，表示你正在挣脱枷锁，获得解放。",
        element="地", planet="摩羯座"
    ),
    TarotCard(
        id=16, name="高塔", english_name="The Tower",
        card_type=CardType.MAJOR_ARCANA, suit=None, number=None,
        keywords_upright=["突变", "毁灭", "觉醒", "真相大白", "解脱"],
        keywords_reversed=["避免灾难", "恐惧改变", "延迟崩溃", "内部转变"],
        meaning_upright="高塔预示着突如其来的变化。虽然过程可能痛苦，但这是为了让你从虚假中解脱。",
        meaning_reversed="逆位表示你可能正在试图避免不可避免的改变，或者这种转变是内在的。",
        element="火", planet="火星"
    ),
    TarotCard(
        id=17, name="星星", english_name="The Star",
        card_type=CardType.MAJOR_ARCANA, suit=None, number=None,
        keywords_upright=["希望", "灵感", "治愈", "平静", "信心"],
        keywords_reversed=["绝望", "失去信心", "断开连接", "挫败"],
        meaning_upright="星星带来希望和治愈。风暴过后，平静和光明正在等待着你。",
        meaning_reversed="逆位暗示你正在失去信心，或者感到与灵感断开连接。",
        element="风", planet="水瓶座"
    ),
    TarotCard(
        id=18, name="月亮", english_name="The Moon",
        card_type=CardType.MAJOR_ARCANA, suit=None, number=None,
        keywords_upright=["幻象", "直觉", "潜意识", "恐惧", "不确定性"],
        keywords_reversed=["释放恐惧", "真相浮现", "清晰", "正视内在"],
        meaning_upright="月亮牌提醒你事物可能并非表面那样。相信直觉，探索潜意识中的真相。",
        meaning_reversed="逆位是积极的，表示迷雾正在散去，你开始看清真相。",
        element="水", planet="双鱼座"
    ),
    TarotCard(
        id=19, name="太阳", english_name="The Sun",
        card_type=CardType.MAJOR_ARCANA, suit=None, number=None,
        keywords_upright=["成功", "喜悦", "活力", "积极", "光明"],
        keywords_reversed=["暂时挫折", "过度乐观", "内在小孩", "寻求快乐"],
        meaning_upright="太阳是最积极的牌之一。成功、喜悦和光明正等着你。",
        meaning_reversed="逆位不代表完全的负面，只是成功可能有所延迟，或者需要调整期望。",
        element="火", planet="太阳"
    ),
    TarotCard(
        id=20, name="审判", english_name="Judgement",
        card_type=CardType.MAJOR_ARCANA, suit=None, number=None,
        keywords_upright=["重生", "觉醒", "召唤", "反思", "赦免"],
        keywords_reversed=["自我怀疑", "拒绝召唤", "逃避审判", "后悔"],
        meaning_upright="审判牌象征着精神的觉醒和重生。聆听内心的召唤，迎接新的开始。",
        meaning_reversed="逆位暗示你可能在拒绝成长的机会，或者被自我怀疑所困。",
        element="火", planet="冥王星"
    ),
    TarotCard(
        id=21, name="世界", english_name="The World",
        card_type=CardType.MAJOR_ARCANA, suit=None, number=None,
        keywords_upright=["完成", "成就", "圆满", "旅程结束", "整合"],
        keywords_reversed=["未完成", "延迟成功", "缺乏收尾", "寻求结束"],
        meaning_upright="世界牌代表一个周期的完美完成。你的努力即将得到回报，享受这份圆满。",
        meaning_reversed="逆位表示某件事情尚未完成，或者成功被延迟了。",
        element="地", planet="土星"
    ),
]


def _create_minor_arcana() -> List[TarotCard]:
    """创建小阿卡纳牌组 (56张)"""
    cards = []
    card_id = 22
    
    # 数字牌编号对应的名称
    number_names = {
        1: "A", 2: "二", 3: "三", 4: "四", 5: "五",
        6: "六", 7: "七", 8: "八", 9: "九", 10: "十",
        11: "侍从", 12: "骑士", 13: "王后", 14: "国王"
    }
    
    # 各花色的元素和主题
    suit_info = {
        Suit.WANDS: {
            "element": "火",
            "theme": "行动、激情、创意",
            "upright_keywords": ["行动", "创意", "激情", "能量", "冒险"],
            "reversed_keywords": ["延迟", "挫折", "能量受阻", "冲动"]
        },
        Suit.CUPS: {
            "element": "水",
            "theme": "情感、关系、直觉",
            "upright_keywords": ["情感", "直觉", "关系", "创造力", "心灵"],
            "reversed_keywords": ["情感压抑", "逃避", "失望", "情绪化"]
        },
        Suit.SWORDS: {
            "element": "风",
            "theme": "思维、沟通、冲突",
            "upright_keywords": ["思维", "真相", "沟通", "决定", "清晰"],
            "reversed_keywords": ["困惑", "冲突", "思想混乱", "残酷"]
        },
        Suit.PENTACLES: {
            "element": "地",
            "theme": "物质、财富、实践",
            "upright_keywords": ["财富", "物质", "工作", "实际", "健康"],
            "reversed_keywords": ["损失", "贪婪", "物质主义", "不安全感"]
        }
    }
    
    for suit in Suit:
        info = suit_info[suit]
        for num in range(1, 15):
            name = f"{suit.value}{number_names[num]}"
            
            # 根据编号和花色生成含义
            if num == 1:  # A牌
                upright_meaning = f"{suit.value}A代表新的机会和纯粹的{info['theme']}能量开始显现。"
                reversed_meaning = f"{suit.value}A逆位表示新的机会被延迟或{info['theme']}方面的阻碍。"
            elif num == 11:  # 侍从
                upright_meaning = f"{suit.value}侍从代表{info['theme']}方面的新消息或学习机会。"
                reversed_meaning = f"{suit.value}侍从逆位表示不成熟的态度或{info['theme']}方面的延误消息。"
            elif num == 12:  # 骑士
                upright_meaning = f"{suit.value}骑士代表在{info['theme']}方面的行动和追求。"
                reversed_meaning = f"{suit.value}骑士逆位表示冲动或{info['theme']}方面的过度行为。"
            elif num == 13:  # 王后
                upright_meaning = f"{suit.value}王后代表{info['theme']}方面的成熟和内在智慧。"
                reversed_meaning = f"{suit.value}王后逆位表示{info['theme']}方面的情感依赖或不安全感。"
            elif num == 14:  # 国王
                upright_meaning = f"{suit.value}国王代表{info['theme']}方面的掌控和成功。"
                reversed_meaning = f"{suit.value}国王逆位表示{info['theme']}方面的过度控制或滥用权力。"
            else:  # 数字牌 2-10
                upright_meaning = f"{suit.value}{number_names[num]}反映{info['theme']}方面的平衡与进展。"
                reversed_meaning = f"{suit.value}{number_names[num]}逆位表示{info['theme']}方面的失衡或挑战。"
            
            card = TarotCard(
                id=card_id,
                name=name,
                english_name=f"{number_names[num]} of {suit.name.capitalize()}",
                card_type=CardType.MINOR_ARCANA,
                suit=suit,
                number=num,
                keywords_upright=info["upright_keywords"].copy(),
                keywords_reversed=info["reversed_keywords"].copy(),
                meaning_upright=upright_meaning,
                meaning_reversed=reversed_meaning,
                element=info["element"]
            )
            cards.append(card)
            card_id += 1
    
    return cards


# 小阿卡纳牌组
MINOR_ARCANA = _create_minor_arcana()

# 完整牌组
FULL_DECK = MAJOR_ARCANA + MINOR_ARCANA


class TarotDeck:
    """塔罗牌牌组类"""
    
    def __init__(self, seed: Optional[int] = None):
        """
        初始化牌组
        
        Args:
            seed: 随机种子，用于可重复的抽取结果
        """
        self.seed = seed
        if seed is not None:
            random.seed(seed)
        self._deck = FULL_DECK.copy()
        self._drawn_cards: List[Tuple[TarotCard, Orientation]] = []
    
    def shuffle(self) -> None:
        """洗牌"""
        self._deck = FULL_DECK.copy()
        random.shuffle(self._deck)
        self._drawn_cards = []
    
    def draw_card(self, orientation_random: bool = True) -> Tuple[TarotCard, Orientation]:
        """
        抽取一张牌
        
        Args:
            orientation_random: 是否随机正逆位
        
        Returns:
            元组 (牌, 朝向)
        """
        if not self._deck:
            self.shuffle()
        
        card = self._deck.pop()
        orientation = Orientation.REVERSED if orientation_random and random.random() < 0.5 else Orientation.UPRIGHT
        result = (card, orientation)
        self._drawn_cards.append(result)
        return result
    
    def draw_cards(self, count: int, orientation_random: bool = True) -> List[Tuple[TarotCard, Orientation]]:
        """
        抽取多张牌
        
        Args:
            count: 牌数量
            orientation_random: 是否随机正逆位
        
        Returns:
            牌列表，每项为 (牌, 朝向)
        """
        return [self.draw_card(orientation_random) for _ in range(count)]
    
    def get_drawn_cards(self) -> List[Tuple[TarotCard, Orientation]]:
        """获取已抽取的牌"""
        return self._drawn_cards.copy()
    
    def remaining_count(self) -> int:
        """获取剩余牌数"""
        return len(self._deck)


class TarotReading:
    """塔罗牌解读类"""
    
    def __init__(self, deck: Optional[TarotDeck] = None):
        """
        初始化解读器
        
        Args:
            deck: 使用的牌组，如果为 None 则创建新牌组
        """
        self.deck = deck or TarotDeck()
    
    def single_card_reading(self, question: Optional[str] = None) -> Dict:
        """
        单牌解读
        
        Args:
            question: 问题（可选）
        
        Returns:
            解读结果字典
        """
        self.deck.shuffle()
        card, orientation = self.deck.draw_card()
        
        return {
            "spread_type": "单牌牌阵",
            "question": question,
            "cards": [{
                "position": "指引牌",
                "card": card.name,
                "english_name": card.english_name,
                "orientation": orientation.value,
                "type": card.card_type.value,
                "keywords": card.keywords_upright if orientation == Orientation.UPRIGHT else card.keywords_reversed,
                "meaning": card.meaning_upright if orientation == Orientation.UPRIGHT else card.meaning_reversed,
                "element": card.element,
                "zodiac": card.zodiac,
                "planet": card.planet
            }],
            "interpretation": self._interpret_single(card, orientation, question)
        }
    
    def three_card_reading(self, question: Optional[str] = None, 
                          positions: Tuple[str, str, str] = ("过去", "现在", "未来")) -> Dict:
        """
        三牌牌阵解读
        
        Args:
            question: 问题（可选）
            positions: 三个位置的含义，默认为过去/现在/未来
        
        Returns:
            解读结果字典
        """
        self.deck.shuffle()
        cards = self.deck.draw_cards(3)
        
        card_results = []
        for i, (card, orientation) in enumerate(cards):
            card_results.append({
                "position": positions[i],
                "card": card.name,
                "english_name": card.english_name,
                "orientation": orientation.value,
                "type": card.card_type.value,
                "keywords": card.keywords_upright if orientation == Orientation.UPRIGHT else card.keywords_reversed,
                "meaning": card.meaning_upright if orientation == Orientation.UPRIGHT else card.meaning_reversed,
                "element": card.element
            })
        
        return {
            "spread_type": "三牌牌阵",
            "positions": list(positions),
            "question": question,
            "cards": card_results,
            "interpretation": self._interpret_three(cards, positions, question)
        }
    
    def celtic_cross_reading(self, question: Optional[str] = None) -> Dict:
        """
        凯尔特十字牌阵解读（10张牌）
        
        位置含义：
        1. 现状 - 你目前的情况
        2. 挑战 - 你面临的障碍或挑战
        3. 根源 - 问题的根源或基础
        4. 过去 - 已经过去的影响
        5. 近期未来 - 即将发生的事
        6. 远期未来 - 最终结果或趋势
        7. 你的态度 - 你对此事的心态
        8. 外部环境 - 他人的影响或环境因素
        9. 希望与恐惧 - 你的期望和担忧
        10. 最终结果 - 事情的结局
        
        Args:
            question: 问题（可选）
        
        Returns:
            解读结果字典
        """
        self.deck.shuffle()
        cards = self.deck.draw_cards(10)
        
        positions = [
            "现状", "挑战", "根源", "过去", "近期未来", "远期未来",
            "你的态度", "外部环境", "希望与恐惧", "最终结果"
        ]
        
        position_meanings = [
            "你目前的情况和处境",
            "你面临的障碍或挑战",
            "问题的根源或基础",
            "已经过去的影响因素",
            "即将发生的事情",
            "最终的结果或发展趋势",
            "你对此事的心态和立场",
            "他人的影响或环境因素",
            "你的期望和担忧",
            "事情的最终结局"
        ]
        
        card_results = []
        for i, (card, orientation) in enumerate(cards):
            card_results.append({
                "position": positions[i],
                "position_meaning": position_meanings[i],
                "card": card.name,
                "english_name": card.english_name,
                "orientation": orientation.value,
                "type": card.card_type.value,
                "keywords": card.keywords_upright if orientation == Orientation.UPRIGHT else card.keywords_reversed,
                "meaning": card.meaning_upright if orientation == Orientation.UPRIGHT else card.meaning_reversed,
                "element": card.element
            })
        
        return {
            "spread_type": "凯尔特十字牌阵",
            "question": question,
            "cards": card_results,
            "interpretation": self._interpret_celtic_cross(cards, question)
        }
    
    def yes_no_reading(self, question: str) -> Dict:
        """
        是非问题解读
        
        Args:
            question: 是非问题
        
        Returns:
            解读结果字典
        """
        self.deck.shuffle()
        card, orientation = self.deck.draw_card()
        
        # 基于牌的编号和朝向判断是非
        # 大阿卡纳的前半部分（0-10）倾向于是，后半部分（11-21）倾向否
        # 正位倾向是，逆位倾向否
        
        if card.card_type == CardType.MAJOR_ARCANA:
            base_score = 1 if card.id <= 10 else -1
        else:
            # 小阿卡纳根据花色判断
            suit_scores = {
                Suit.WANDS: 1,      # 权杖积极
                Suit.CUPS: 1,       # 圣杯积极
                Suit.SWORDS: -1,    # 宝剑消极
                Suit.PENTACLES: 0   # 金币中性
            }
            base_score = suit_scores.get(card.suit, 0)
        
        orientation_score = 1 if orientation == Orientation.UPRIGHT else -1
        total_score = base_score * orientation_score
        
        if total_score > 0:
            answer = "是的"
            confidence = "高" if abs(total_score) == 2 else "中"
        elif total_score < 0:
            answer = "不是"
            confidence = "高" if abs(total_score) == 2 else "中"
        else:
            answer = "不确定"
            confidence = "低"
        
        return {
            "spread_type": "是非牌阵",
            "question": question,
            "answer": answer,
            "confidence": confidence,
            "card": {
                "name": card.name,
                "orientation": orientation.value,
                "meaning": card.meaning_upright if orientation == Orientation.UPRIGHT else card.meaning_reversed
            },
            "interpretation": f"牌面【{card.name}】({orientation.value})的指引：{card.meaning_upright if orientation == Orientation.UPRIGHT else card.meaning_reversed}"
        }
    
    def _interpret_single(self, card: TarotCard, orientation: Orientation, 
                         question: Optional[str]) -> str:
        """解读单牌"""
        meaning = card.meaning_upright if orientation == Orientation.UPRIGHT else card.meaning_reversed
        keywords = "、".join(card.keywords_upright if orientation == Orientation.UPRIGHT else card.keywords_reversed)
        
        interpretation = f"【{card.name}】{orientation.value}\n\n"
        interpretation += f"关键词：{keywords}\n\n"
        interpretation += f"解读：{meaning}\n\n"
        
        if question:
            interpretation += f"针对你的问题，这张牌建议你关注{keywords}这些方面。"
        
        return interpretation
    
    def _interpret_three(self, cards: List[Tuple[TarotCard, Orientation]], 
                        positions: Tuple[str, str, str], question: Optional[str]) -> str:
        """解读三牌牌阵"""
        interpretation = "【牌阵解读】\n\n"
        
        for i, (card, orientation) in enumerate(cards):
            meaning = card.meaning_upright if orientation == Orientation.UPRIGHT else card.meaning_reversed
            interpretation += f"【{positions[i]}】{card.name}({orientation.value})：{meaning}\n\n"
        
        # 综合解读
        major_count = sum(1 for c, _ in cards if c.card_type == CardType.MAJOR_ARCANA)
        reversed_count = sum(1 for _, o in cards if o == Orientation.REVERSED)
        
        interpretation += "【综合分析】\n"
        if major_count >= 2:
            interpretation += "多张大阿卡纳牌出现，说明这是一个重要的转折点，具有深刻的精神意义。\n"
        if reversed_count >= 2:
            interpretation += "多张逆位牌提示可能需要反思内部因素，或者当前面临一些阻碍。\n"
        
        return interpretation
    
    def _interpret_celtic_cross(self, cards: List[Tuple[TarotCard, Orientation]], 
                               question: Optional[str]) -> str:
        """解读凯尔特十字牌阵"""
        positions = ["现状", "挑战", "根源", "过去", "近期未来", "远期未来",
                    "你的态度", "外部环境", "希望与恐惧", "最终结果"]
        
        interpretation = "【凯尔特十字牌阵解读】\n\n"
        
        # 第一部分：现状分析
        interpretation += "━━━ 现状分析 ━━━\n"
        for i in range(6):
            card, orientation = cards[i]
            meaning = card.meaning_upright if orientation == Orientation.UPRIGHT else card.meaning_reversed
            interpretation += f"【{positions[i]}】{card.name}({orientation.value})\n{meaning}\n\n"
        
        # 第二部分：建议与结果
        interpretation += "━━━ 指引与结果 ━━━\n"
        for i in range(6, 10):
            card, orientation = cards[i]
            meaning = card.meaning_upright if orientation == Orientation.UPRIGHT else card.meaning_reversed
            interpretation += f"【{positions[i]}】{card.name}({orientation.value})\n{meaning}\n\n"
        
        # 综合分析
        major_count = sum(1 for c, _ in cards if c.card_type == CardType.MAJOR_ARCANA)
        reversed_count = sum(1 for _, o in cards if o == Orientation.REVERSED)
        
        interpretation += "【综合分析】\n"
        interpretation += f"大阿卡纳牌数：{major_count}/10\n"
        interpretation += f"逆位牌数：{reversed_count}/10\n\n"
        
        if major_count >= 5:
            interpretation += "大量大阿卡纳牌出现，这是一个命运性的时刻，事件具有深远的精神意义。\n"
        elif major_count <= 2:
            interpretation += "大阿卡纳牌较少，事件更多是日常事务，可以主动掌控。\n"
        
        # 最终结果牌特别强调
        final_card, final_orientation = cards[9]
        interpretation += f"【最终结果】{final_card.name}({final_orientation.value})：{final_card.meaning_upright if final_orientation == Orientation.UPRIGHT else final_card.meaning_reversed}"
        
        return interpretation


# 便捷函数
def draw_single_card(question: Optional[str] = None, seed: Optional[int] = None) -> Dict:
    """
    快速单牌解读
    
    Args:
        question: 问题（可选）
        seed: 随机种子
    
    Returns:
        解读结果
    """
    reading = TarotReading(TarotDeck(seed))
    return reading.single_card_reading(question)


def draw_three_cards(question: Optional[str] = None, 
                    positions: Tuple[str, str, str] = ("过去", "现在", "未来"),
                    seed: Optional[int] = None) -> Dict:
    """
    快速三牌牌阵解读
    
    Args:
        question: 问题（可选）
        positions: 位置含义
        seed: 随机种子
    
    Returns:
        解读结果
    """
    reading = TarotReading(TarotDeck(seed))
    return reading.three_card_reading(question, positions)


def draw_celtic_cross(question: Optional[str] = None, seed: Optional[int] = None) -> Dict:
    """
    快速凯尔特十字牌阵解读
    
    Args:
        question: 问题（可选）
        seed: 随机种子
    
    Returns:
        解读结果
    """
    reading = TarotReading(TarotDeck(seed))
    return reading.celtic_cross_reading(question)


def ask_yes_no(question: str, seed: Optional[int] = None) -> Dict:
    """
    快速是非问题解读
    
    Args:
        question: 是非问题
        seed: 随机种子
    
    Returns:
        解读结果
    """
    reading = TarotReading(TarotDeck(seed))
    return reading.yes_no_reading(question)


def get_card_info(card_name: str) -> Optional[Dict]:
    """
    获取特定牌的信息
    
    Args:
        card_name: 牌名称（支持中文名称如"愚者"、"权杖A"）
    
    Returns:
        牌信息字典，如果未找到返回 None
    """
    for card in FULL_DECK:
        if card.name == card_name or card.english_name.lower() == card_name.lower():
            return {
                "id": card.id,
                "name": card.name,
                "english_name": card.english_name,
                "type": card.card_type.value,
                "suit": card.suit.value if card.suit else None,
                "number": card.number,
                "keywords_upright": card.keywords_upright,
                "keywords_reversed": card.keywords_reversed,
                "meaning_upright": card.meaning_upright,
                "meaning_reversed": card.meaning_reversed,
                "element": card.element,
                "zodiac": card.zodiac,
                "planet": card.planet
            }
    return None


def list_all_cards() -> List[str]:
    """
    列出所有牌名
    
    Returns:
        牌名列表
    """
    return [card.name for card in FULL_DECK]


def list_major_arcana() -> List[str]:
    """列出所有大阿卡纳牌名"""
    return [card.name for card in MAJOR_ARCANA]


def list_minor_arcana() -> List[str]:
    """列出所有小阿卡纳牌名"""
    return [card.name for card in MINOR_ARCANA]


def list_cards_by_suit(suit: Suit) -> List[str]:
    """
    列出特定花色的牌名
    
    Args:
        suit: 花色
    
    Returns:
        牌名列表
    """
    return [card.name for card in MINOR_ARCANA if card.suit == suit]


if __name__ == "__main__":
    # 演示用法
    print("=" * 50)
    print("塔罗牌工具模块演示")
    print("=" * 50)
    
    print("\n【单牌解读】")
    result = draw_single_card("今天运势如何？", seed=42)
    print(f"问题: {result['question']}")
    for card in result['cards']:
        print(f"牌面: {card['card']} ({card['orientation']})")
        print(f"关键词: {', '.join(card['keywords'])}")
    print(f"\n解读:\n{result['interpretation']}")
    
    print("\n" + "=" * 50)
    print("【三牌牌阵】")
    result = draw_three_cards("近期感情发展", seed=42)
    for card in result['cards']:
        print(f"【{card['position']}】{card['card']} ({card['orientation']})")
    
    print("\n" + "=" * 50)
    print("【是非问题】")
    result = ask_yes_no("我应该接受这份新工作吗？", seed=42)
    print(f"问题: {result['question']}")
    print(f"答案: {result['answer']} (置信度: {result['confidence']})")
    print(f"牌面: {result['card']['name']} ({result['card']['orientation']})")
    
    print("\n" + "=" * 50)
    print(f"牌组总数: {len(FULL_DECK)} 张")
    print(f"大阿卡纳: {len(MAJOR_ARCANA)} 张")
    print(f"小阿卡纳: {len(MINOR_ARCANA)} 张")