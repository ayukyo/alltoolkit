"""
昵称生成器工具集 (Nickname Generator Utils)
提供多种风格的昵称生成、用户名建议、游戏ID生成等功能
零外部依赖，纯 Python 标准库实现

功能列表:
1. NicknameGenerator - 昵称生成器（支持多种风格）
2. UsernameGenerator - 用户名生成器（适合注册账号）
3. GameIdGenerator - 游戏ID生成器（适合游戏昵称）
4. PetNameGenerator - 宠物名字生成器
5. TeamNameGenerator - 团队/小组名称生成器
6. FantasyNameGenerator - 奇幻角色名生成器
"""

import random
import re
from typing import List, Optional, Dict, Tuple
from dataclasses import dataclass
from enum import Enum


class NameStyle(Enum):
    """昵称风格"""
    CUTE = "可爱"           # 可爱风格
    COOL = "酷炫"           # 酷炫风格
    FUNNY = "搞笑"          # 搞笑风格
    MYSTIC = "神秘"         # 神秘风格
    HEROIC = "英雄"         # 英雄风格
    NATURE = "自然"         # 自然风格
    TECH = "科技"           # 科技风格
    FOOD = "美食"           # 美食风格
    ANIMAL = "动物"         # 动物风格
    FANTASY = "奇幻"        # 奇幻风格
    CHINESE = "中文"        # 中文风格
    MINIMAL = "简约"        # 简约风格


class NameCategory(Enum):
    """名字类别"""
    ADJECTIVE = "形容词"
    NOUN = "名词"
    VERB = "动词"
    PREFIX = "前缀"
    SUFFIX = "后缀"


@dataclass
class GeneratedName:
    """生成的名字结果"""
    name: str
    style: NameStyle
    components: List[str]  # 组成部分
    meaning: str           # 含义描述
    alternatives: List[str]  # 变体
    
    def __str__(self) -> str:
        return self.name


# ==================== 词库数据 ====================

# 中文词库
CHINESE_ADJECTIVES = {
    "可爱": ["可爱", "萌萌", "甜甜", "软软", "乖乖", "暖心", "治愈", "温馨", "柔软", "俏皮"],
    "酷炫": ["炫酷", "霸气", "狂野", "犀利", "锐利", "震撼", "震撼", "绝世", "无敌", "极致"],
    "神秘": ["神秘", "幽深", "玄妙", "深邃", "迷离", "幻影", "暗影", "幽暗", "飘渺", "虚无"],
    "英雄": ["英勇", "无畏", "坚强", "无畏", "荣耀", "传奇", "辉煌", "伟岸", "圣洁", "神圣"],
    "自然": ["清新", "淡雅", "素雅", "纯净", "澄澈", "通透", "明亮", "明媚", "温润", "恬静"],
    "搞笑": ["搞怪", "逗比", "欢乐", "开心", "愉快", "有趣", "有趣", "奇葩", "沙雕", "欢乐"],
    "科技": ["智能", "极速", "精准", "高效", "前沿", "领先", "创新", "先锋", "精英", "高端"],
    "美食": ["美味", "香甜", "可口", "酥脆", "软糯", "清新", "甜蜜", "香醇", "浓郁", "醇厚"],
}

CHINESE_NOUNS = {
    "可爱": ["小猫", "小兔", "小熊", "小鹿", "小羊", "小猪", "小兔", "星星", "月亮", "云朵", 
             "糖果", "蛋糕", "布丁", "奶茶", "小可爱", "小宝贝", "小甜心", "小仙女", "小公主"],
    "酷炫": ["王者", "霸主", "战神", "剑客", "刺客", "骑士", "猎人", "战士", "龙骑士", "暗影",
             "闪电", "风暴", "雷霆", "烈焰", "寒冰", "星辰", "银河", "宇宙", "黑洞", "光束"],
    "神秘": ["幽灵", "幻影", "暗夜", "迷雾", "梦境", "星尘", "虚空", "深渊", "黑洞", "月光",
             "星辰", "银河", "彩虹", "极光", "幻境", "仙境", "迷境", "幽谷", "幽林", "幽湖"],
    "英雄": ["勇士", "骑士", "圣者", "智者", "守护者", "守望者", "拯救者", "先锋", "领袖", "冠军",
             "传奇", "王者", "霸主", "英雄", "圣骑士", "龙骑士", "暗骑士", "圣战士", "圣射手"],
    "自然": ["清风", "明月", "流云", "细雨", "微澜", "晨露", "晚霞", "春水", "秋叶", "冬雪",
             "夏日", "春风", "秋月", "冬梅", "兰花", "竹子", "菊花", "梅花", "樱花", "桃花"],
    "搞笑": ["土豆", "番茄", "黄瓜", "咸鱼", "腊肉", "鸡腿", "鸡翅", "鸡爪", "猪蹄", "牛排",
             "奶茶", "咖啡", "可乐", "雪碧", "芬达", "薯片", "泡面", "火锅", "烤肉", "串串"],
    "科技": ["机器人", "AI", "算法", "代码", "程序", "系统", "网络", "云端", "数据", "信息",
             "量子", "原子", "电子", "光子", "粒子", "星球", "太空", "火箭", "飞船", "卫星"],
    "美食": ["蛋糕", "布丁", "奶茶", "咖啡", "可乐", "汉堡", "披萨", "寿司", "拉面", "火锅",
             "烧烤", "串串", "薯条", "鸡翅", "甜甜圈", "马卡龙", "巧克力", "冰淇淋", "雪糕"],
}

# 英文词库
ENGLISH_ADJECTIVES = {
    "cute": ["Cute", "Sweet", "Lovely", "Adorable", "Charming", "Precious", "Darling", "Cuddly", 
             "Fluffy", "Soft", "Tiny", "Little", "Baby", "Mini", "Petite", "Gentle", "Warm"],
    "cool": ["Cool", "Awesome", "Epic", "Legendary", "Supreme", "Ultimate", "Elite", "Pro", 
             "Master", "Boss", "King", "Queen", "Alpha", "Prime", "Elite", "Ace", "Top"],
    "funny": ["Funny", "Crazy", "Wacky", "Silly", "Goofy", "Nutty", "Zany", "Kooky", 
              "Bonkers", "Mad", "Wild", "Crazy", "Bizarre", "Odd", "Weird", "Quirky"],
    "mystic": ["Mystic", "Shadow", "Dark", "Phantom", "Ghost", "Spirit", "Spectral", "Ethereal",
               "Void", "Nether", "Abyss", "Eclipse", "Twilight", "Midnight", "Moonlight"],
    "heroic": ["Heroic", "Brave", "Bold", "Valiant", "Gallant", "Noble", "Royal", "Knightly",
               "Warrior", "Champion", "Defender", "Guardian", "Protector", "Savior", "Victor"],
    "nature": ["Fresh", "Green", "Wild", "Natural", "Pure", "Clean", "Clear", "Fresh",
               "Breezy", "Sunny", "Cloudy", "Rainy", "Stormy", "Misty", "Foggy", "Dewy"],
    "tech": ["Cyber", "Digital", "Tech", "Neo", "Quantum", "Atomic", "Binary", "Pixel",
             "Byte", "Bit", "Code", "Data", "Info", "Net", "Web", "Cloud", "Ai", "Bot"],
    "food": ["Sweet", "Spicy", "Salty", "Sour", "Tasty", "Delicious", "Yummy", "Savory",
             "Crunchy", "Creamy", "Juicy", "Fresh", "Hot", "Cold", "Warm", "Cool"],
}

ENGLISH_NOUNS = {
    "cute": ["Cat", "Kitten", "Puppy", "Bunny", "Bear", "Deer", "Fox", "Owl", 
             "Star", "Moon", "Cloud", "Rainbow", "Flower", "Rose", "Heart", "Angel",
             "Princess", "Baby", "Sweetie", "Cutie", "Honey", "Sugar", "Cookie"],
    "cool": ["King", "Queen", "Boss", "Master", "Pro", "Ace", "Star", "Hero",
             "Legend", "Dragon", "Phoenix", "Tiger", "Wolf", "Lion", "Eagle", "Hawk",
             "Storm", "Thunder", "Flash", "Blaze", "Frost", "Shadow", "Blade"],
    "funny": ["Potato", "Tomato", "Banana", "Apple", "Orange", "Pickle", "Noodle",
              "Donut", "Pizza", "Burger", "Taco", "Burrito", "Sushi", "Ramen",
              "Coffee", "Tea", "Milk", "Juice", "Soda", "Beer", "Wine"],
    "mystic": ["Shadow", "Phantom", "Ghost", "Spirit", "Soul", "Dream", "Nightmare",
               "Moon", "Star", "Galaxy", "Universe", "Void", "Abyss", "Realm",
               "Portal", "Gate", "Key", "Eye", "Hand", "Heart", "Mind"],
    "heroic": ["Knight", "Warrior", "Champion", "Hero", "Guardian", "Defender",
               "Protector", "Savior", "Victor", "Leader", "Commander", "Captain",
               "General", "Marshal", "Paladin", "Ranger", "Scout", "Hunter"],
    "nature": ["Forest", "Mountain", "Valley", "River", "Lake", "Ocean", "Sea",
               "Sky", "Sun", "Moon", "Star", "Cloud", "Wind", "Rain", "Snow",
               "Leaf", "Tree", "Flower", "Garden", "Meadow", "Field", "Grove"],
    "tech": ["Bot", "Ai", "Bot", "Android", "Cyborg", "Mech", "Drone", "Robot",
             "Computer", "Server", "Node", "Pixel", "Byte", "Bit", "Code",
             "Data", "Info", "Net", "Web", "Link", "Chain", "Block"],
    "food": ["Cake", "Cookie", "Donut", "Pie", "Tart", "Pudding", "Mousse",
             "Icecream", "Chocolate", "Candy", "Lollipop", "Gummy", "Jelly",
             "Coffee", "Tea", "Milk", "Juice", "Smoothie", "Shake", "Soda"],
}

# 特殊前缀/后缀
PREFIXES = {
    "tech": ["Cyber", "Neo", "Ultra", "Super", "Hyper", "Mega", "Giga", "Tera", 
             "Quantum", "Atomic", "Binary", "Digital", "Virtual", "Synthetic"],
    "cool": ["The", "Dark", "Shadow", "Night", "Storm", "Thunder", "Frost", "Blaze",
             "Elite", "Pro", "Master", "Lord", "King", "Queen", "Boss", "Chief"],
    "mystic": ["Shadow", "Dark", "Void", "Abyss", "Nether", "Ethereal", "Phantom",
               "Ghost", "Spirit", "Spectral", "Mystic", "Arcane", "Ancient"],
    "heroic": ["Sir", "Lord", "Captain", "General", "Commander", "Master", "Chief",
               "Elder", "Grand", "High", "Royal", "Noble", "Sacred", "Holy"],
}

SUFFIXES = {
    "tech": ["Bot", "Ai", "X", "Byte", "Bit", "Code", "Data", "Node", "Link",
             "Net", "Web", "Cloud", "Lab", "Hub", "Core", "Zone"],
    "cool": ["X", "Pro", "Ace", "Star", "King", "Boss", "Master", "Lord",
             "Elite", "Prime", "Alpha", "Omega", "Zero", "One"],
    "mystic": ["X", "Shadow", "Walker", "Seeker", "Hunter", "Keeper", "Watcher",
               "Guardian", "Defender", "Protector", "Slayer", "Master"],
    "heroic": ["Knight", "Warrior", "Guardian", "Defender", "Champion", "Hero",
               "Leader", "Master", "Lord", "King", "Queen", "Prince", "Princess"],
}

# 数字装饰
NUMBER_DECORATIONS = ["007", "01", "02", "03", "99", "88", "66", "77", "123", "321", "888", "666"]

# 特殊符号装饰
SYMBOL_DECORATIONS = ["_", "-", ".", "*", "~", "x", "X"]


class NicknameGenerator:
    """
    昵称生成器
    生成多种风格的昵称，支持中文和英文
    """
    
    def __init__(self, seed: Optional[int] = None):
        """
        初始化昵称生成器
        
        Args:
            seed: 随机种子（用于可重复生成）
        """
        if seed is not None:
            random.seed(seed)
    
    def generate(self, 
                style: NameStyle = NameStyle.CUTE,
                language: str = "chinese",
                count: int = 1) -> List[GeneratedName]:
        """
        生成昵称
        
        Args:
            style: 昵称风格
            language: 语言（chinese/english）
            count: 生成数量
        
        Returns:
            生成的昵称列表
        """
        results = []
        for _ in range(count):
            name = self._generate_single(style, language)
            results.append(name)
        return results
    
    def _generate_single(self, style: NameStyle, language: str) -> GeneratedName:
        """生成单个昵称"""
        style_key = self._get_style_key(style)
        
        if language == "chinese":
            adj_list = CHINESE_ADJECTIVES.get(style_key, CHINESE_ADJECTIVES["可爱"])
            noun_list = CHINESE_NOUNS.get(style_key, CHINESE_NOUNS["可爱"])
        else:
            adj_list = ENGLISH_ADJECTIVES.get(style_key, ENGLISH_ADJECTIVES["cute"])
            noun_list = ENGLISH_NOUNS.get(style_key, ENGLISH_NOUNS["cute"])
        
        # 随机组合
        adj = random.choice(adj_list)
        noun = random.choice(noun_list)
        
        # 生成主名字
        if language == "chinese":
            name = adj + noun
        else:
            # 英文可以有多种组合方式
            format_type = random.choice(["adj_noun", "noun_adj", "adj_noun_sep"])
            if format_type == "adj_noun":
                name = adj + noun
            elif format_type == "noun_adj":
                name = noun + adj
            else:
                sep = random.choice(SYMBOL_DECORATIONS[:3])
                name = f"{adj}{sep}{noun}"
        
        # 生成变体
        alternatives = self._generate_alternatives(name, style, language)
        
        # 含义描述
        meaning = f"{style.value}风格的昵称，由{adj}和{noun}组成"
        
        return GeneratedName(
            name=name,
            style=style,
            components=[adj, noun],
            meaning=meaning,
            alternatives=alternatives
        )
    
    def _get_style_key(self, style: NameStyle) -> str:
        """获取风格对应的键名"""
        mapping = {
            NameStyle.CUTE: "可爱" if random.choice([True, False]) else "cute",
            NameStyle.COOL: "酷炫" if random.choice([True, False]) else "cool",
            NameStyle.FUNNY: "搞笑" if random.choice([True, False]) else "funny",
            NameStyle.MYSTIC: "神秘" if random.choice([True, False]) else "mystic",
            NameStyle.HEROIC: "英雄" if random.choice([True, False]) else "heroic",
            NameStyle.NATURE: "自然" if random.choice([True, False]) else "nature",
            NameStyle.TECH: "科技" if random.choice([True, False]) else "tech",
            NameStyle.FOOD: "美食" if random.choice([True, False]) else "food",
        }
        return mapping.get(style, "可爱")
    
    def _generate_alternatives(self, base_name: str, style: NameStyle, language: str) -> List[str]:
        """生成变体名字"""
        alternatives = []
        
        # 添加数字装饰
        for num in random.sample(NUMBER_DECORATIONS, 3):
            alternatives.append(base_name + num)
        
        # 添加符号装饰
        if language != "chinese":
            for sym in random.sample(SYMBOL_DECORATIONS, 2):
                alternatives.append(base_name.replace(" ", sym))
        
        return alternatives[:5]
    
    def generate_mixed(self, count: int = 5) -> List[GeneratedName]:
        """
        生成混合风格的昵称
        
        Args:
            count: 生成数量
        
        Returns:
            昵称列表
        """
        results = []
        styles = list(NameStyle)
        for i in range(count):
            style = styles[i % len(styles)]
            language = random.choice(["chinese", "english"])
            results.extend(self.generate(style, language, 1))
        return results
    
    def generate_with_prefix_suffix(self,
                                    style: NameStyle = NameStyle.COOL,
                                    language: str = "english") -> GeneratedName:
        """
        生成带前缀/后缀的昵称
        
        Args:
            style: 风格
            language: 语言
        
        Returns:
            生成的昵称
        """
        style_key = self._get_style_key(style)
        
        # 选择前缀或后缀
        use_prefix = random.choice([True, False])
        
        if language == "chinese":
            # 中文风格直接组合
            adj_list = CHINESE_ADJECTIVES.get(style_key, CHINESE_ADJECTIVES["酷炫"])
            noun_list = CHINESE_NOUNS.get(style_key, CHINESE_NOUNS["酷炫"])
            name = random.choice(adj_list) + random.choice(noun_list)
        else:
            prefix_list = PREFIXES.get(style_key, PREFIXES["cool"])
            suffix_list = SUFFIXES.get(style_key, SUFFIXES["cool"])
            noun_list = ENGLISH_NOUNS.get(style_key, ENGLISH_NOUNS["cool"])
            
            noun = random.choice(noun_list)
            
            if use_prefix:
                prefix = random.choice(prefix_list)
                name = prefix + noun
                components = [prefix, noun]
            else:
                suffix = random.choice(suffix_list)
                name = noun + suffix
                components = [noun, suffix]
        
        alternatives = self._generate_alternatives(name, style, language)
        
        return GeneratedName(
            name=name,
            style=style,
            components=components if language != "chinese" else [],
            meaning=f"{style.value}风格的昵称",
            alternatives=alternatives
        )


class UsernameGenerator:
    """
    用户名生成器
    适合注册账号使用，确保用户名格式规范
    """
    
    def __init__(self, seed: Optional[int] = None):
        if seed is not None:
            random.seed(seed)
    
    def generate(self,
                base_name: Optional[str] = None,
                min_length: int = 6,
                max_length: int = 20,
                use_numbers: bool = True,
                use_special: bool = False,
                count: int = 1) -> List[str]:
        """
        生成用户名
        
        Args:
            base_name: 基础名字（可选）
            min_length: 最小长度
            max_length: 最大长度
            use_numbers: 是否使用数字
            use_special: 是否使用特殊字符
            count: 生成数量
        
        Returns:
            用户名列表
        """
        results = []
        
        for _ in range(count):
            if base_name:
                name = self._customize_base(base_name, use_numbers, use_special)
            else:
                name = self._generate_random(min_length, max_length, use_numbers, use_special)
            
            # 验证长度
            if len(name) < min_length:
                name = name + str(random.randint(10, 99))
            if len(name) > max_length:
                name = name[:max_length]
            
            results.append(name)
        
        return results
    
    def _customize_base(self, base: str, use_numbers: bool, use_special: bool) -> str:
        """自定义基础名字"""
        # 清理基础名字
        base = re.sub(r'[^\w]', '', base)
        
        name = base
        
        # 添加装饰
        if use_numbers:
            name = base + str(random.randint(1, 999))
        
        if use_special and random.choice([True, False]):
            special = random.choice(["_", "-"])
            pos = random.randint(1, len(base))
            name = base[:pos] + special + base[pos:]
        
        return name
    
    def _generate_random(self, min_len: int, max_len: int, 
                        use_numbers: bool, use_special: bool) -> str:
        """随机生成用户名"""
        # 使用英文词库组合
        categories = list(ENGLISH_NOUNS.keys())
        cat = random.choice(categories)
        
        noun = random.choice(ENGLISH_NOUNS[cat])
        adj = random.choice(ENGLISH_ADJECTIVES.get(cat, ENGLISH_ADJECTIVES["cute"]))
        
        # 组合方式
        formats = ["adjnoun", "nounadj", "adj_noun"]
        fmt = random.choice(formats)
        
        if fmt == "adjnoun":
            name = adj.lower() + noun.lower()
        elif fmt == "nounadj":
            name = noun.lower() + adj.lower()
        else:
            name = adj.lower() + "_" + noun.lower()
        
        # 添加数字
        if use_numbers:
            name = name + str(random.randint(1, 99))
        
        return name
    
    def check_availability_format(self, username: str) -> Tuple[bool, List[str]]:
        """
        检查用户名格式是否符合常见平台要求
        
        Args:
            username: 用户名
        
        Returns:
            (是否有效, 错误列表)
        """
        errors = []
        
        if len(username) < 3:
            errors.append("用户名太短，至少需要3个字符")
        
        if len(username) > 30:
            errors.append("用户名太长，最多30个字符")
        
        if not re.match(r'^[a-zA-Z0-9_-]+$', username):
            errors.append("用户名只能包含字母、数字、下划线和连字符")
        
        if username[0].isdigit():
            errors.append("用户名不能以数字开头")
        
        return len(errors) == 0, errors


class GameIdGenerator:
    """
    游戏ID生成器
    适合游戏昵称，支持各种游戏风格
    """
    
    # 游戏类型风格映射
    GAME_STYLES = {
        "fps": ["酷炫", "cool"],       # 第一人称射击
        "moba": ["英雄", "heroic"],    # MOBA游戏
        "mmorpg": ["奇幻", "fantasy"], # MMORPG
        "casual": ["可爱", "cute"],    # 休闲游戏
        "strategy": ["科技", "tech"],  # 策略游戏
        "racing": ["酷炫", "cool"],    # 竞速游戏
    }
    
    def __init__(self, seed: Optional[int] = None):
        if seed is not None:
            random.seed(seed)
    
    def generate(self,
                game_type: str = "fps",
                include_clan: bool = False,
                clan_name: Optional[str] = None,
                count: int = 1) -> List[str]:
        """
        生成游戏ID
        
        Args:
            game_type: 游戏类型
            include_clan: 是否包含战队/公会前缀
            clan_name: 战队/公会名称
            count: 生成数量
        
        Returns:
            游戏ID列表
        """
        results = []
        
        # 获取游戏对应风格
        style_keys = self.GAME_STYLES.get(game_type, ["酷炫", "cool"])
        
        for _ in range(count):
            # 随机选择风格
            style = random.choice(style_keys)
            
            # 生成基础ID
            if style in ENGLISH_ADJECTIVES:
                adj = random.choice(ENGLISH_ADJECTIVES[style])
                noun = random.choice(ENGLISH_NOUNS.get(style, ENGLISH_NOUNS["cool"]))
                
                # 组合方式
                formats = ["{adj}{noun}", "{adj}_{noun}", "{adj}-{noun}", 
                          "{noun}{adj}", "{noun}_{adj}", "The{noun}"]
                fmt = random.choice(formats)
                
                base_id = fmt.format(adj=adj, noun=noun)
            else:
                adj = random.choice(CHINESE_ADJECTIVES.get(style, CHINESE_ADJECTIVES["酷炫"]))
                noun = random.choice(CHINESE_NOUNS.get(style, CHINESE_NOUNS["酷炫"]))
                base_id = adj + noun
            
            # 添加战队前缀
            if include_clan:
                if clan_name:
                    prefix = clan_name
                else:
                    prefix = self._generate_clan_prefix()
                game_id = f"[{prefix}]{base_id}"
            else:
                game_id = base_id
            
            # 添加数字装饰（可选）
            if random.choice([True, False]):
                num = random.choice(NUMBER_DECORATIONS)
                game_id = game_id + num
            
            results.append(game_id)
        
        return results
    
    def _generate_clan_prefix(self) -> str:
        """生成战队前缀"""
        prefixes = ["Pro", "Elite", "Team", "Gang", "Club", "Squad", 
                   "军团", "战队", "公会", "联盟", "骑士团"]
        return random.choice(prefixes)
    
    generate_game_id = generate  # 别名


class PetNameGenerator:
    """
    宠物名字生成器
    生成可爱的宠物名字
    """
    
    # 宠物类型词库
    PET_NAMES = {
        "dog": {
            "chinese": ["旺财", "豆豆", "小黑", "小白", "毛毛", "欢欢", "乐乐", 
                       "豆包", "汤圆", "馒头", "包子", "饺子", "米粒", "奶茶",
                       "旺旺", "来福", "福福", "多多", "甜甜", "糖糖"],
            "english": ["Buddy", "Max", "Charlie", "Cooper", "Rocky", "Bear", 
                       "Duke", "Tucker", "Jack", "Oliver", "Milo", "Leo", 
                       "Bella", "Lucy", "Daisy", "Luna", "Sadie", "Molly"]
        },
        "cat": {
            "chinese": ["咪咪", "喵喵", "小橘", "小白", "花花", "雪球", "布丁",
                       "奶茶", "糯米", "汤圆", "麻薯", "芝士", "可乐", "蜜糖",
                       "橘子", "柠檬", "桃子", "芒果", "樱桃", "草莓"],
            "english": ["Whiskers", "Mittens", "Shadow", "Simba", "Luna", 
                       "Milo", "Oliver", "Jasper", "Felix", "Cleo", 
                       "Nala", "Bella", "Chloe", "Sophie", "Lily"]
        },
        "bird": {
            "chinese": ["小鸟", "飞飞", "羽羽", "翅膀", "蓝蓝", "黄黄", "叽叽",
                       "喳喳", "啾啾", "嘟嘟", "云朵", "天空", "彩虹", "星晴"],
            "english": ["Sky", "Blue", "Sunny", "Tweet", "Feather", "Wing", 
                       "Chirp", "Peep", "Angel", "Cloud", "Rainbow"]
        },
        "fish": {
            "chinese": ["小鱼", "泡泡", "波波", "水水", "蓝蓝", "金金", "银银",
                       "锦鲤", "鲤鱼", "金龙", "银龙", "小宝", "宝儿"],
            "english": ["Bubble", "Goldie", "Splash", "Fin", "Blue", 
                       "Nemo", "Dory", "Aqua", "Marine"]
        },
        "rabbit": {
            "chinese": ["兔兔", "蹦蹦", "跳跳", "小白", "雪球", "棉花", "软软",
                       "萌萌", "耳朵", "萝卜", "胡萝卜", "小萝卜"],
            "english": ["Bunny", "Hop", "Skip", "Snowball", "Cotton", 
                       "Fluffy", "Earl", "Carrot", "Nibbles"]
        },
        "hamster": {
            "chinese": ["仓仓", "鼠鼠", "小仓", "球球", "圆圆", "糯米", "团子",
                       "小团", "小圆", "豆豆", "米米", "粒粒"],
            "english": ["Hammy", "Nibbles", "Peanut", "Gizmo", "Puff", 
                       "Mochi", "Chubby", "Tiny", "Pocket"]
        }
    }
    
    def __init__(self, seed: Optional[int] = None):
        if seed is not None:
            random.seed(seed)
    
    def generate(self,
                pet_type: str = "dog",
                language: str = "chinese",
                count: int = 1) -> List[str]:
        """
        生成宠物名字
        
        Args:
            pet_type: 宠物类型（dog/cat/bird/fish/rabbit/hamster）
            language: 语言
            count: 生成数量
        
        Returns:
            名字列表
        """
        names = self.PET_NAMES.get(pet_type, self.PET_NAMES["dog"])
        name_list = names.get(language, names["chinese"])
        
        results = []
        for _ in range(count):
            results.append(random.choice(name_list))
        
        return results
    
    def generate_cute_combo(self, count: int = 3) -> List[str]:
        """
        生成可爱的组合名字
        
        Args:
            count: 生成数量
        
        Returns:
            名字列表
        """
        results = []
        
        cute_adj = CHINESE_ADJECTIVES["可爱"] + ENGLISH_ADJECTIVES["cute"]
        food_nouns = CHINESE_NOUNS["美食"] + ENGLISH_NOUNS["food"]
        
        for _ in range(count):
            adj = random.choice(cute_adj)
            noun = random.choice(food_nouns)
            results.append(adj + noun)
        
        return results


class TeamNameGenerator:
    """
    团队名称生成器
    生成团队、小组、工作室名称
    """
    
    TEAM_TYPES = {
        "tech": {
            "prefixes": ["智能", "数字", "云端", "数据", "算法", "Cyber", "Digital", "Tech"],
            "suffixes": ["实验室", "工作室", "团队", "小组", "Lab", "Team", "Studio", "Hub"]
        },
        "creative": {
            "prefixes": ["创意", "艺术", "设计", "灵感", "Creative", "Art", "Design"],
            "suffixes": ["工作室", "团队", "空间", "Lab", "Studio", "Space", "House"]
        },
        "business": {
            "prefixes": ["精英", "领袖", "巅峰", "荣耀", "Elite", "Prime", "Top"],
            "suffixes": ["团队", "联盟", "集团", "Team", "Union", "Group", "Corp"]
        },
        "gaming": {
            "prefixes": ["游戏", "电竞", "冠军", "王者", "Game", "Pro", "Elite"],
            "suffixes": ["战队", "俱乐部", "联盟", "Team", "Club", "Guild", "Squad"]
        },
        "academic": {
            "prefixes": ["学术", "研究", "探索", "发现", "Research", "Study", "Quest"],
            "suffixes": ["小组", "学会", "协会", "Group", "Society", "Association"]
        }
    }
    
    def __init__(self, seed: Optional[int] = None):
        if seed is not None:
            random.seed(seed)
    
    def generate(self,
                team_type: str = "tech",
                language: str = "chinese",
                count: int = 1) -> List[str]:
        """
        生成团队名称
        
        Args:
            team_type: 团队类型
            language: 语言
            count: 生成数量
        
        Returns:
            名称列表
        """
        team_data = self.TEAM_TYPES.get(team_type, self.TEAM_TYPES["tech"])
        
        results = []
        for _ in range(count):
            prefix = random.choice(team_data["prefixes"])
            suffix = random.choice(team_data["suffixes"])
            
            # 检查语言匹配
            if language == "chinese":
                # 使用中文词汇
                chinese_prefixes = [p for p in team_data["prefixes"] if self._is_chinese(p)]
                chinese_suffixes = [s for s in team_data["suffixes"] if self._is_chinese(s)]
                if chinese_prefixes and chinese_suffixes:
                    prefix = random.choice(chinese_prefixes)
                    suffix = random.choice(chinese_suffixes)
            else:
                # 使用英文词汇
                english_prefixes = [p for p in team_data["prefixes"] if not self._is_chinese(p)]
                english_suffixes = [s for s in team_data["suffixes"] if not self._is_chinese(s)]
                if english_prefixes and english_suffixes:
                    prefix = random.choice(english_prefixes)
                    suffix = random.choice(english_suffixes)
            
            name = prefix + suffix
            results.append(name)
        
        return results
    
    def _is_chinese(self, text: str) -> bool:
        """判断是否包含中文"""
        return any('\u4e00' <= c <= '\u9fff' for c in text)
    
    def generate_with_name(self,
                          leader_name: str,
                          team_type: str = "tech") -> List[str]:
        """
        生成带有领导者名字的团队名
        
        Args:
            leader_name: 领导者名字
            team_type: 团队类型
        
        Returns:
            名称列表
        """
        team_data = self.TEAM_TYPES.get(team_type, self.TEAM_TYPES["tech"])
        suffix = random.choice(team_data["suffixes"])
        
        return [f"{leader_name}{suffix}", f"{leader_name}的{suffix}"]


class FantasyNameGenerator:
    """
    奇幻角色名生成器
    生成适合奇幻小说、游戏的角色名字
    """
    
    # 奇幻词根
    FANTASY_PREFIXES = {
        "elven": ["Ael", "El", "Gal", "Thal", "Val", "Sy", "Ly", "My", "Ara", "Ela"],
        "dwarven": ["Thor", "Bar", "Gor", "Dur", "Krag", "Magni", "Bor", "Hro", "Dain"],
        "human": ["Al", "Ed", "Wil", "Thom", "Ric", "John", "Har", "Mar", "Rob"],
        "demonic": ["Mal", "Zar", "Mor", "Ven", "Kha", "Dra", "Gor", "Nar", "Xar"],
        "angelic": ["Ser", "Ari", "Gab", "Raph", "Uri", "Met", "Az", "Is", "Ra"]
    }
    
    FANTASY_SUFFIXES = {
        "elven": ["driel", "rion", "thiel", "wen", "lis", "nor", "ian", "ara", "ea", "iel"],
        "dwarven": ["in", "on", "um", "or", "gar", "rik", "und", "orn", "heim"],
        "human": ["ard", "on", "en", "er", "son", "ton", "ric", "ald"],
        "demonic": ["gor", "thul", "rax", "zul", "mon", "dar", "vos", "gar"],
        "angelic": ["iel", "ael", "on", "us", "im", "iel", "pha", "iel"]
    }
    
    # 中文奇幻词根
    CHINESE_FANTASY = {
        "prefixes": ["龙", "凤", "剑", "影", "月", "星", "云", "霜", "雪", "火",
                    "天", "地", "玄", "魔", "神", "圣", "灵", "仙", "妖", "鬼"],
        "suffixes": ["剑", "刀", "影", "魂", "心", "翼", "瞳", "灵", "风", "雨",
                    "霜", "雪", "炎", "焰", "光", "影", "夜", "月", "星", "云"]
    }
    
    def __init__(self, seed: Optional[int] = None):
        if seed is not None:
            random.seed(seed)
    
    def generate(self,
                race: str = "elven",
                language: str = "english",
                count: int = 1) -> List[str]:
        """
        生成奇幻角色名
        
        Args:
            race: 种族（elven/dwarven/human/demonic/angelic）
            language: 语言
            count: 生成数量
        
        Returns:
            名字列表
        """
        results = []
        
        for _ in range(count):
            if language == "chinese":
                prefix = random.choice(self.CHINESE_FANTASY["prefixes"])
                suffix = random.choice(self.CHINESE_FANTASY["suffixes"])
                # 添加中间字
                middle = random.choice(["傲", "凌", "梦", "幻", "霄", "苍", "玄", "幽"])
                name = prefix + middle + suffix
            else:
                prefix = random.choice(self.FANTASY_PREFIXES.get(race, self.FANTASY_PREFIXES["elven"]))
                suffix = random.choice(self.FANTASY_SUFFIXES.get(race, self.FANTASY_SUFFIXES["elven"]))
                name = prefix + suffix
            
            results.append(name)
        
        return results
    
    def generate_full_name(self,
                          race: str = "elven",
                          language: str = "english") -> str:
        """
        生成全名（名字+姓氏）
        
        Args:
            race: 种族
            language: 语言
        
        Returns:
            全名
        """
        first_name = self.generate(race, language, 1)[0]
        last_name = self.generate(race, language, 1)[0]
        
        if language == "chinese":
            return first_name + last_name
        else:
            return f"{first_name} {last_name}"


# ==================== 便捷函数 ====================

def generate_nickname(style: str = "可爱", language: str = "chinese") -> str:
    """
    快速生成昵称
    
    Args:
        style: 风格名称
        language: 语言
    
    Returns:
        昵称
    """
    style_enum = NameStyle.CUTE
    for s in NameStyle:
        if s.value == style or s.name.lower() == style.lower():
            style_enum = s
            break
    
    gen = NicknameGenerator()
    result = gen.generate(style_enum, language, 1)[0]
    return result.name


def generate_username(base: Optional[str] = None) -> str:
    """
    快速生成用户名
    
    Args:
        base: 基础名字
    
    Returns:
        用户名
    """
    gen = UsernameGenerator()
    return gen.generate(base_name=base, count=1)[0]


def generate_game_id(game_type: str = "fps") -> str:
    """
    快速生成游戏ID
    
    Args:
        game_type: 游戏类型
    
    Returns:
        游戏ID
    """
    gen = GameIdGenerator()
    return gen.generate(game_type=game_type, count=1)[0]


def generate_pet_name(pet_type: str = "dog") -> str:
    """
    快速生成宠物名
    
    Args:
        pet_type: 宠物类型
    
    Returns:
        宠物名
    """
    gen = PetNameGenerator()
    return gen.generate(pet_type=pet_type, count=1)[0]


def generate_team_name(team_type: str = "tech") -> str:
    """
    快速生成团队名
    
    Args:
        team_type: 团队类型
    
    Returns:
        团队名
    """
    gen = TeamNameGenerator()
    return gen.generate(team_type=team_type, count=1)[0]


def generate_fantasy_name(race: str = "elven") -> str:
    """
    快速生成奇幻角色名
    
    Args:
        race: 种族
    
    Returns:
        奇幻名
    """
    gen = FantasyNameGenerator()
    return gen.generate(race=race, count=1)[0]


def generate_names_bulk(style: str = "可爱", 
                        language: str = "chinese",
                        count: int = 10) -> List[str]:
    """
    批量生成昵称
    
    Args:
        style: 风格
        language: 语言
        count: 数量
    
    Returns:
        昵称列表
    """
    gen = NicknameGenerator()
    results = gen.generate_mixed(count)
    return [r.name for r in results]