"""
Quote Utilities - 名言警句工具

提供名言警句的获取、管理、格式化和输出功能，包括：
- 内置中英文名言库（按主题分类）
- 名言随机获取与筛选
- 名言格式化输出（多种样式）
- 名言收藏管理
- 名言卡片生成
- 每日名言推荐

零外部依赖，纯 Python 实现。
"""

from typing import List, Dict, Optional, Tuple, Set
from dataclasses import dataclass, field
from datetime import datetime, date, timedelta
from enum import Enum
import json
import hashlib
import random


class QuoteCategory(Enum):
    """名言类别"""
    LIFE = "life"  # 人生
    SUCCESS = "success"  # 成功
    WISDOM = "wisdom"  # 智慧
    LOVE = "love"  # 爱情
    COURAGE = "courage"  # 勇气
    MOTIVATION = "motivation"  # 激励
    LEARNING = "learning"  # 学习
    WORK = "work"  # 工作
    HEALTH = "health"  # 健康
    FRIENDSHIP = "friendship"  # 友谊
    TIME = "time"  # 时间
    HAPPINESS = "happiness"  # 幸福
    PHILOSOPHY = "philosophy"  # 哲学
    NATURE = "nature"  # 自然
    HUMOR = "humor"  # 幽默
    CHINESE = "chinese"  # 中国古语


class QuoteStyle(Enum):
    """输出样式"""
    SIMPLE = "simple"  # 简洁
    CARD = "card"  # 卡片式
    BANNER = "banner"  # 横幅
    SIGNATURE = "signature"  # 签名档
    MINIMAL = "minimal"  # 极简
    DECORATED = "decorated"  # 装饰


@dataclass
class Quote:
    """名言对象"""
    text: str  # 名言内容
    author: str  # 作者
    category: QuoteCategory = QuoteCategory.WISDOM
    language: str = "zh"  # 语言: zh/en
    source: Optional[str] = None  # 出处
    tags: List[str] = field(default_factory=list)  # 标签
    rating: int = 5  # 评分 1-5
    created_at: Optional[date] = None  # 创建日期
    is_favorite: bool = False  # 是否收藏
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = date.today()
    
    def to_dict(self) -> Dict[str, any]:
        """转换为字典"""
        return {
            'text': self.text,
            'author': self.author,
            'category': self.category.value,
            'language': self.language,
            'source': self.source,
            'tags': self.tags,
            'rating': self.rating,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'is_favorite': self.is_favorite,
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, any]) -> 'Quote':
        """从字典创建"""
        created_at = None
        if data.get('created_at'):
            # 兼容 Python 3.6: 使用 datetime.strptime 替代 date.fromisoformat
            created_at = datetime.strptime(data['created_at'], "%Y-%m-%d").date()
        
        return cls(
            text=data['text'],
            author=data['author'],
            category=QuoteCategory(data.get('category', 'wisdom')),
            language=data.get('language', 'zh'),
            source=data.get('source'),
            tags=data.get('tags', []),
            rating=data.get('rating', 5),
            created_at=created_at,
            is_favorite=data.get('is_favorite', False),
        )
    
    def get_id(self) -> str:
        """获取唯一标识（基于内容哈希）"""
        content = f"{self.text}|{self.author}"
        return hashlib.md5(content.encode()).hexdigest()[:8]
    
    def format(self, style: QuoteStyle = QuoteStyle.SIMPLE) -> str:
        """
        格式化名言
        
        Args:
            style: 输出样式
            
        Returns:
            格式化后的字符串
        """
        if style == QuoteStyle.SIMPLE:
            return f'"{self.text}" — {self.author}'
        
        elif style == QuoteStyle.CARD:
            lines = [
                "┌─────────────────────────────┐",
                "│                             │",
            ]
            # 分行处理长文本
            words = self.text
            max_width = 27
            while len(words) > max_width:
                line = words[:max_width]
                words = words[max_width:]
                lines.append(f"│  {line}│")
            lines.append(f"│  {words}{' ' * (max_width - len(words) - 2)}│")
            lines.extend([
                "│                             │",
                f"│          — {self.author}{' ' * (20 - len(self.author))}│",
                "│                             │",
                "└─────────────────────────────┘",
            ])
            return '\n'.join(lines)
        
        elif style == QuoteStyle.BANNER:
            border = "=" * (len(self.text) + 4)
            return f"\n{border}\n  {self.text}  \n{border}\n        — {self.author}\n"
        
        elif style == QuoteStyle.SIGNATURE:
            return f"\n╭══════════════════════════════╮\n║  {self.text}\n║\n║                    — {self.author}\n╰══════════════════════════════╯\n"
        
        elif style == QuoteStyle.MINIMAL:
            return f'{self.text}\n—{self.author}'
        
        elif style == QuoteStyle.DECORATED:
            return f'✨ "{self.text}" ✨\n   📖 {self.author}'
        
        return self.format(QuoteStyle.SIMPLE)


# 内置中文名言库
BUILTIN_QUOTES_ZH: List[Dict[str, any]] = [
    # 人生
    {"text": "人生就像一杯茶，不会苦一辈子，但总会苦一阵子。", "author": "林清玄", "category": "life"},
    {"text": "生活不是等待风暴过去，而是学会在雨中跳舞。", "author": "维维安·格林", "category": "life"},
    {"text": "人生最大的荣耀不在于从不跌倒，而在于每次跌倒后都能爬起来。", "author": "孔子", "category": "life"},
    {"text": "生命不是要超越别人，而是要超越自己。", "author": "佚名", "category": "life"},
    {"text": "人生最重要的不是所站的位置，而是所朝的方向。", "author": "霍姆斯", "category": "life"},
    
    # 成功
    {"text": "成功不是终点，失败也不是终结，唯有继续前进的勇气才是最重要的。", "author": "丘吉尔", "category": "success"},
    {"text": "天才是百分之一的灵感加上百分之九十九的汗水。", "author": "爱迪生", "category": "success"},
    {"text": "成功的秘诀在于坚持自己的目标和信念。", "author": "佚名", "category": "success"},
    {"text": "不经历风雨，怎能见彩虹。", "author": "佚名", "category": "success"},
    {"text": "成功属于那些从失败中汲取教训的人。", "author": "佚名", "category": "success"},
    
    # 智慧
    {"text": "知之为知之，不知为不知，是知也。", "author": "孔子", "category": "wisdom"},
    {"text": "三人行，必有我师焉。", "author": "孔子", "category": "wisdom"},
    {"text": "学而不思则罔，思而不学则殆。", "author": "孔子", "category": "wisdom"},
    {"text": "温故而知新，可以为师矣。", "author": "孔子", "category": "wisdom"},
    {"text": "己所不欲，勿施于人。", "author": "孔子", "category": "wisdom"},
    {"text": "知足常乐，能忍自安。", "author": "老子", "category": "wisdom"},
    
    # 勇气
    {"text": "勇敢不是没有恐惧，而是带着恐惧仍然前行。", "author": "佚名", "category": "courage"},
    {"text": "勇气是所有品质中最重要的，因为它保证了其他品质的存在。", "author": "丘吉尔", "category": "courage"},
    {"text": "真正的勇气是在知道生活真相后依然热爱生活。", "author": "罗曼·罗兰", "category": "courage"},
    {"text": "不害怕失败的人，才能真正成功。", "author": "佚名", "category": "courage"},
    
    # 激励
    {"text": "每一天都是一个新的开始。", "author": "佚名", "category": "motivation"},
    {"text": "相信自己，你比想象中更强大。", "author": "佚名", "category": "motivation"},
    {"text": "不要等待机会，而要创造机会。", "author": "佚名", "category": "motivation"},
    {"text": "只有不断努力，才能不断进步。", "author": "佚名", "category": "motivation"},
    {"text": "梦想不会逃跑，逃跑的永远是自己。", "author": "佚名", "category": "motivation"},
    
    # 学习
    {"text": "书山有路勤为径，学海无涯苦作舟。", "author": "韩愈", "category": "learning"},
    {"text": "读万卷书，行万里路。", "author": "刘彝", "category": "learning"},
    {"text": "活到老，学到老。", "author": "佚名", "category": "learning"},
    {"text": "学如逆水行舟，不进则退。", "author": "佚名", "category": "learning"},
    {"text": "书籍是人类进步的阶梯。", "author": "高尔基", "category": "learning"},
    
    # 工作
    {"text": "业精于勤荒于嬉，行成于思毁于随。", "author": "韩愈", "category": "work"},
    {"text": "千里之行，始于足下。", "author": "老子", "category": "work"},
    {"text": "细节决定成败。", "author": "佚名", "category": "work"},
    {"text": "态度决定一切。", "author": "佚名", "category": "work"},
    
    # 健康
    {"text": "健康是最大的财富。", "author": "佚名", "category": "health"},
    {"text": "早睡早起使人健康、富有和明智。", "author": "本杰明·富兰克林", "category": "health"},
    {"text": "生命在于运动。", "author": "伏尔泰", "category": "health"},
    
    # 爱情
    {"text": "爱是生命的火焰，没有它，一切变成黑夜。", "author": "罗兰", "category": "love"},
    {"text": "真正的爱情能够鼓舞人，唤醒他内心沉睡着的力量。", "author": "薄伽丘", "category": "love"},
    
    # 时间
    {"text": "时间就是生命，时间就是金钱。", "author": "佚名", "category": "time"},
    {"text": "一寸光阴一寸金，寸金难买寸光阴。", "author": "佚名", "category": "time"},
    {"text": "明日复明日，明日何其多。", "author": "钱福", "category": "time"},
    
    # 幸福
    {"text": "幸福不是拥有更多，而是要求更少。", "author": "佚名", "category": "happiness"},
    {"text": "快乐不是因为拥有的多，而是计较的少。", "author": "佚名", "category": "happiness"},
    
    # 哲学
    {"text": "我思故我在。", "author": "笛卡尔", "category": "philosophy"},
    {"text": "存在即合理。", "author": "黑格尔", "category": "philosophy"},
    {"text": "道可道，非常道。名可名，非常名。", "author": "老子", "category": "philosophy"},
    
    # 中国古语
    {"text": "君子坦荡荡，小人长戚戚。", "author": "孔子", "category": "chinese"},
    {"text": "己所不欲，勿施于人。", "author": "孔子", "category": "chinese"},
    {"text": "有朋自远方来，不亦乐乎。", "author": "孔子", "category": "chinese"},
    {"text": "四海之内皆兄弟。", "author": "孔子", "category": "chinese"},
    {"text": "上善若水。", "author": "老子", "category": "chinese"},
    {"text": "千里之堤，溃于蚁穴。", "author": "韩非", "category": "chinese"},
    {"text": "塞翁失马，焉知非福。", "author": "淮南子", "category": "chinese"},
    {"text": "宝剑锋从磨砺出，梅花香自苦寒来。", "author": "佚名", "category": "chinese"},
    {"text": "锲而不舍，金石可镂。", "author": "荀子", "category": "chinese"},
    {"text": "路漫漫其修远兮，吾将上下而求索。", "author": "屈原", "category": "chinese"},
]

# 内置英文名言库
BUILTIN_QUOTES_EN: List[Dict[str, any]] = [
    # Life
    {"text": "Life is what happens when you're busy making other plans.", "author": "John Lennon", "category": "life"},
    {"text": "The purpose of our lives is to be happy.", "author": "Dalai Lama", "category": "life"},
    {"text": "Life is really simple, but we insist on making it complicated.", "author": "Confucius", "category": "life"},
    {"text": "In the end, it's not the years in your life that count. It's the life in your years.", "author": "Abraham Lincoln", "category": "life"},
    
    # Success
    {"text": "Success is not final, failure is not fatal: it is the courage to continue that counts.", "author": "Winston Churchill", "category": "success"},
    {"text": "The way to get started is to quit talking and begin doing.", "author": "Walt Disney", "category": "success"},
    {"text": "Success usually comes to those who are too busy to be looking for it.", "author": "Henry David Thoreau", "category": "success"},
    
    # Wisdom
    {"text": "The only true wisdom is in knowing you know nothing.", "author": "Socrates", "category": "wisdom"},
    {"text": "Wisdom begins in wonder.", "author": "Socrates", "category": "wisdom"},
    {"text": "The wise man does not lay up his own treasures. The more he gives to others, the more he has for his own.", "author": "Lao Tzu", "category": "wisdom"},
    
    # Motivation
    {"text": "Believe you can and you're halfway there.", "author": " Theodore Roosevelt", "category": "motivation"},
    {"text": "The only impossible journey is the one you never begin.", "author": "Tony Robbins", "category": "motivation"},
    {"text": "Act as if what you do makes a difference. It does.", "author": "William James", "category": "motivation"},
    {"text": "What lies behind us and what lies before us are tiny matters compared to what lies within us.", "author": "Ralph Waldo Emerson", "category": "motivation"},
    
    # Courage
    {"text": "Courage is resistance to fear, mastery of fear, not absence of fear.", "author": "Mark Twain", "category": "courage"},
    {"text": "It takes courage to grow up and become who you really are.", "author": "E.E. Cummings", "category": "courage"},
    
    # Learning
    {"text": "The more that you read, the more things you will know. The more that you learn, the more places you'll go.", "author": "Dr. Seuss", "category": "learning"},
    {"text": "Live as if you were to die tomorrow. Learn as if you were to live forever.", "author": "Mahatma Gandhi", "category": "learning"},
    
    # Work
    {"text": "Choose a job you love, and you will never have to work a day in your life.", "author": "Confucius", "category": "work"},
    {"text": "The only way to do great work is to love what you do.", "author": "Steve Jobs", "category": "work"},
    
    # Philosophy
    {"text": "I think, therefore I am.", "author": "René Descartes", "category": "philosophy"},
    {"text": "To be yourself in a world that is constantly trying to make you something else is the greatest accomplishment.", "author": "Ralph Waldo Emerson", "category": "philosophy"},
    
    # Happiness
    {"text": "Happiness depends upon ourselves.", "author": "Aristotle", "category": "happiness"},
    {"text": "The greatest happiness you can have is knowing that you do not necessarily require happiness.", "author": "William Saroyan", "category": "happiness"},
    
    # Time
    {"text": "Time you enjoy wasting is not wasted time.", "author": "Marthe Troly-Curtin", "category": "time"},
    {"text": "The past cannot be changed. The future is yet in your power.", "author": "Unknown", "category": "time"},
]


class QuoteManager:
    """
    名言管理器
    
    管理名言库，提供获取、搜索、收藏等功能。
    
    Example:
        >>> manager = QuoteManager()
        >>> quote = manager.get_random_quote()
        >>> print(quote.format())
    """
    
    def __init__(self):
        """初始化名言管理器"""
        self.quotes: List[Quote] = []
        self.favorites: Set[str] = set()  # 收藏的名言ID
        self._load_builtin_quotes()
        self._daily_quote: Optional[Quote] = None
        self._daily_quote_date: Optional[date] = None
    
    def _load_builtin_quotes(self) -> None:
        """加载内置名言库"""
        for q in BUILTIN_QUOTES_ZH:
            self.quotes.append(Quote(
                text=q['text'],
                author=q['author'],
                category=QuoteCategory(q.get('category', 'wisdom')),
                language='zh',
            ))
        
        for q in BUILTIN_QUOTES_EN:
            self.quotes.append(Quote(
                text=q['text'],
                author=q['author'],
                category=QuoteCategory(q.get('category', 'wisdom')),
                language='en',
            ))
    
    def add_quote(self,
                  text: str,
                  author: str,
                  category: QuoteCategory = QuoteCategory.WISDOM,
                  language: str = "zh",
                  source: Optional[str] = None,
                  tags: Optional[List[str]] = None,
                  rating: int = 5) -> Quote:
        """
        添加名言
        
        Args:
            text: 名言内容
            author: 作者
            category: 类别
            language: 语言
            source: 出处
            tags: 标签
            rating: 评分
            
        Returns:
            创建的名言对象
        """
        quote = Quote(
            text=text,
            author=author,
            category=category,
            language=language,
            source=source,
            tags=tags or [],
            rating=rating,
        )
        self.quotes.append(quote)
        return quote
    
    def remove_quote(self, quote_id: str) -> bool:
        """
        删除名言
        
        Args:
            quote_id: 名言ID
            
        Returns:
            是否删除成功
        """
        for i, quote in enumerate(self.quotes):
            if quote.get_id() == quote_id:
                self.quotes.pop(i)
                if quote_id in self.favorites:
                    self.favorites.remove(quote_id)
                return True
        return False
    
    def get_random_quote(self,
                         category: Optional[QuoteCategory] = None,
                         language: Optional[str] = None,
                         min_rating: int = 1) -> Optional[Quote]:
        """
        获取随机名言
        
        Args:
            category: 类别筛选
            language: 语言筛选
            min_rating: 最低评分
            
        Returns:
            随机名言
        """
        filtered = self._filter_quotes(category, language, min_rating)
        if not filtered:
            return None
        return random.choice(filtered)
    
    def get_quote_by_id(self, quote_id: str) -> Optional[Quote]:
        """
        根据ID获取名言
        
        Args:
            quote_id: 名言ID
            
        Returns:
            名言对象
        """
        for quote in self.quotes:
            if quote.get_id() == quote_id:
                return quote
        return None
    
    def get_quotes_by_author(self, author: str) -> List[Quote]:
        """
        根据作者获取名言
        
        Args:
            author: 作者名
            
        Returns:
            名言列表
        """
        return [q for q in self.quotes if q.author.lower() == author.lower()]
    
    def get_quotes_by_category(self, category: QuoteCategory) -> List[Quote]:
        """
        根据类别获取名言
        
        Args:
            category: 类别
            
        Returns:
            名言列表
        """
        return [q for q in self.quotes if q.category == category]
    
    def search_quotes(self, keyword: str) -> List[Quote]:
        """
        搜索名言
        
        Args:
            keyword: 关键词
            
        Returns:
            匹配的名言列表
        """
        keyword_lower = keyword.lower()
        return [q for q in self.quotes 
                if keyword_lower in q.text.lower() or keyword_lower in q.author.lower()]
    
    def _filter_quotes(self,
                       category: Optional[QuoteCategory] = None,
                       language: Optional[str] = None,
                       min_rating: int = 1) -> List[Quote]:
        """筛选名言"""
        filtered = self.quotes
        
        if category:
            filtered = [q for q in filtered if q.category == category]
        
        if language:
            filtered = [q for q in filtered if q.language == language]
        
        filtered = [q for q in filtered if q.rating >= min_rating]
        
        return filtered
    
    def get_daily_quote(self,
                        category: Optional[QuoteCategory] = None,
                        language: Optional[str] = None) -> Quote:
        """
        获取每日名言（每天固定返回同一条）
        
        Args:
            category: 类别筛选
            language: 语言筛选
            
        Returns:
            每日名言
        """
        today = date.today()
        
        # 如果已缓存且是今天的，直接返回
        if self._daily_quote and self._daily_quote_date == today:
            return self._daily_quote
        
        # 基于日期生成随机索引
        filtered = self._filter_quotes(category, language)
        if not filtered:
            filtered = self.quotes
        
        # 使用日期作为种子，确保同一天返回同一条
        seed = int(today.strftime("%Y%m%d"))
        random.seed(seed)
        self._daily_quote = random.choice(filtered)
        self._daily_quote_date = today
        random.seed()  # 恢复随机状态
        
        return self._daily_quote
    
    def add_to_favorites(self, quote_id: str) -> bool:
        """
        添加到收藏
        
        Args:
            quote_id: 名言ID
            
        Returns:
            是否添加成功
        """
        quote = self.get_quote_by_id(quote_id)
        if quote:
            self.favorites.add(quote_id)
            quote.is_favorite = True
            return True
        return False
    
    def remove_from_favorites(self, quote_id: str) -> bool:
        """
        从收藏移除
        
        Args:
            quote_id: 名言ID
            
        Returns:
            是否移除成功
        """
        if quote_id in self.favorites:
            self.favorites.remove(quote_id)
            quote = self.get_quote_by_id(quote_id)
            if quote:
                quote.is_favorite = False
            return True
        return False
    
    def get_favorites(self) -> List[Quote]:
        """获取收藏的名言"""
        return [q for q in self.quotes if q.get_id() in self.favorites]
    
    def get_top_quotes(self, n: int = 10, category: Optional[QuoteCategory] = None) -> List[Quote]:
        """
        获取评分最高的名言
        
        Args:
            n: 数量
            category: 类别筛选
            
        Returns:
            高评分名言列表
        """
        filtered = self._filter_quotes(category)
        sorted_quotes = sorted(filtered, key=lambda q: q.rating, reverse=True)
        return sorted_quotes[:n]
    
    def get_stats(self) -> Dict[str, any]:
        """获取统计信息"""
        category_counts = {}
        for cat in QuoteCategory:
            category_counts[cat.value] = len([q for q in self.quotes if q.category == cat])
        
        language_counts = {
            'zh': len([q for q in self.quotes if q.language == 'zh']),
            'en': len([q for q in self.quotes if q.language == 'en']),
        }
        
        return {
            'total_quotes': len(self.quotes),
            'favorites_count': len(self.favorites),
            'category_counts': category_counts,
            'language_counts': language_counts,
        }
    
    def export_data(self) -> str:
        """导出数据为JSON"""
        data = {
            'quotes': [q.to_dict() for q in self.quotes],
            'favorites': list(self.favorites),
            'exported_at': datetime.now().isoformat(),
        }
        return json.dumps(data, ensure_ascii=False, indent=2)
    
    def import_data(self, json_str: str) -> int:
        """从JSON导入数据"""
        data = json.loads(json_str)
        count = 0
        
        for q_data in data.get('quotes', []):
            quote = Quote.from_dict(q_data)
            # 避免重复添加内置名言
            if quote.get_id() not in [q.get_id() for q in self.quotes]:
                self.quotes.append(quote)
                count += 1
        
        self.favorites.update(data.get('favorites', []))
        return count
    
    def save_to_file(self, filepath: str) -> None:
        """保存到文件"""
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(self.export_data())
    
    def load_from_file(self, filepath: str) -> int:
        """从文件加载"""
        with open(filepath, 'r', encoding='utf-8') as f:
            return self.import_data(f.read())


class QuoteFormatter:
    """
    名言格式化工具
    
    提供多种名言输出格式。
    """
    
    @staticmethod
    def format_simple(quote: Quote) -> str:
        """简洁格式"""
        return quote.format(QuoteStyle.SIMPLE)
    
    @staticmethod
    def format_card(quote: Quote) -> str:
        """卡片格式"""
        return quote.format(QuoteStyle.CARD)
    
    @staticmethod
    def format_banner(quote: Quote) -> str:
        """横幅格式"""
        return quote.format(QuoteStyle.BANNER)
    
    @staticmethod
    def format_twitter(quote: Quote) -> str:
        """Twitter格式（带标签）"""
        text = f'"{quote.text}" — {quote.author}'
        if quote.tags:
            tags = ' '.join([f'#{tag}' for tag in quote.tags[:3]])
            text += f'\n{tags}'
        return text
    
    @staticmethod
    def format_markdown(quote: Quote) -> str:
        """Markdown格式"""
        lines = [
            f'> "{quote.text}"',
            f'> ',
            f'> — *{quote.author}*',
        ]
        if quote.source:
            lines.append(f'> 《{quote.source}》')
        return '\n'.join(lines)
    
    @staticmethod
    def format_html(quote: Quote) -> str:
        """HTML格式"""
        html = f'<blockquote>\n  <p>"{quote.text}"</p>\n  <cite>— {quote.author}</cite>\n</blockquote>'
        return html
    
    @staticmethod
    def format_with_translation(quote: Quote, translation: str) -> str:
        """带翻译的格式"""
        return f'"{quote.text}"\n（{translation}）\n— {quote.author}'
    
    @staticmethod
    def format_list(quotes: List[Quote], style: QuoteStyle = QuoteStyle.SIMPLE) -> str:
        """格式化名言列表"""
        lines = []
        for i, quote in enumerate(quotes, 1):
            lines.append(f'{i}. {quote.format(style)}')
        return '\n\n'.join(lines)


class QuoteUtils:
    """
    名言工具高级接口
    
    提供简化的静态方法。
    """
    
    _manager: Optional[QuoteManager] = None
    
    @classmethod
    def get_manager(cls) -> QuoteManager:
        """获取名言管理器（单例）"""
        if cls._manager is None:
            cls._manager = QuoteManager()
        return cls._manager
    
    @staticmethod
    def random_quote(category: Optional[str] = None,
                     language: Optional[str] = None) -> Optional[Quote]:
        """获取随机名言"""
        manager = QuoteUtils.get_manager()
        cat = QuoteCategory(category) if category else None
        return manager.get_random_quote(cat, language)
    
    @staticmethod
    def daily_quote(category: Optional[str] = None,
                    language: Optional[str] = None) -> Quote:
        """获取每日名言"""
        manager = QuoteUtils.get_manager()
        cat = QuoteCategory(category) if category else None
        return manager.get_daily_quote(cat, language)
    
    @staticmethod
    def search(keyword: str) -> List[Quote]:
        """搜索名言"""
        manager = QuoteUtils.get_manager()
        return manager.search_quotes(keyword)
    
    @staticmethod
    def by_author(author: str) -> List[Quote]:
        """按作者获取名言"""
        manager = QuoteUtils.get_manager()
        return manager.get_quotes_by_author(author)
    
    @staticmethod
    def by_category(category: str) -> List[Quote]:
        """按类别获取名言"""
        manager = QuoteUtils.get_manager()
        return manager.get_quotes_by_category(QuoteCategory(category))
    
    @staticmethod
    def format(quote: Quote, style: str = "simple") -> str:
        """格式化名言"""
        style_enum = QuoteStyle(style)
        return quote.format(style_enum)
    
    @staticmethod
    def categories() -> List[str]:
        """获取所有类别"""
        return [cat.value for cat in QuoteCategory]
    
    @staticmethod
    def add_custom_quote(text: str, author: str, **kwargs) -> Quote:
        """添加自定义名言"""
        manager = QuoteUtils.get_manager()
        cat_value = kwargs.pop('category', 'wisdom')
        category = QuoteCategory(cat_value)
        return manager.add_quote(text, author, category=category, **kwargs)


# 便捷函数
def get_quote(category: Optional[str] = None, language: Optional[str] = None) -> Optional[Quote]:
    """获取随机名言便捷函数"""
    return QuoteUtils.random_quote(category, language)


def get_daily_quote(category: Optional[str] = None, language: Optional[str] = None) -> Quote:
    """获取每日名言便捷函数"""
    return QuoteUtils.daily_quote(category, language)


def search_quotes(keyword: str) -> List[Quote]:
    """搜索名言便捷函数"""
    return QuoteUtils.search(keyword)


def format_quote(quote: Quote, style: str = "simple") -> str:
    """格式化名言便捷函数"""
    return QuoteUtils.format(quote, style)


def list_categories() -> List[str]:
    """列出所有类别便捷函数"""
    return QuoteUtils.categories()


if __name__ == "__main__":
    # 简单演示
    print("=== 名言警句工具演示 ===")
    
    manager = QuoteManager()
    
    # 获取随机名言
    print("\n--- 随机名言 ---")
    quote = manager.get_random_quote()
    print(quote.format(QuoteStyle.SIMPLE))
    
    # 获取每日名言
    print("\n--- 每日名言 ---")
    daily = manager.get_daily_quote()
    print(daily.format(QuoteStyle.CARD))
    
    # 按类别获取
    print("\n--- 激励类名言 ---")
    quotes = manager.get_quotes_by_category(QuoteCategory.MOTIVATION)[:3]
    for q in quotes:
        print(f"  • {q.format(QuoteStyle.MINIMAL)}")
    
    # 搜索
    print("\n--- 搜索 '成功' ---")
    results = manager.search_quotes("成功")
    for q in results[:3]:
        print(f"  • {q.text}")
    
    # 统计
    print("\n--- 统计信息 ---")
    stats = manager.get_stats()
    print(f"  总名言数: {stats['total_quotes']}")
    print(f"  中文名言: {stats['language_counts']['zh']}")
    print(f"  英文名言: {stats['language_counts']['en']}")
    
    # 格式化样式
    print("\n--- 多种格式 ---")
    quote = manager.get_random_quote(language="zh")
    print("简洁格式:")
    print(quote.format(QuoteStyle.SIMPLE))
    print("\n装饰格式:")
    print(quote.format(QuoteStyle.DECORATED))