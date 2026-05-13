"""
Mahjong Utils - 日本立直麻将工具库
====================================

零依赖的麻将工具库，提供：
- 牌的表示与操作（万子、筒子、索子、风牌、三元牌）
- 手牌解析与管理
- 和牌检测（标准役种判断）
- 得分计算（符数与番数）
- 进张效率计算
- 牌山模拟

支持日本立直麻将规则。
"""

from enum import Enum
from typing import List, Dict, Optional, Tuple, Set, Union
from collections import Counter
from dataclasses import dataclass
import random


# ==================== 枚举定义 ====================

class TileType(Enum):
    """牌类型"""
    MAN = "m"      # 万子
    PIN = "p"     # 筒子
    SOU = "s"     # 索子
    WIND = "w"    # 风牌
    DRAGON = "d"  # 三元牌


class Wind(Enum):
    """风牌"""
    EAST = "东"
    SOUTH = "南"
    WEST = "西"
    NORTH = "北"


class Dragon(Enum):
    """三元牌"""
    WHITE = "白"    # 白
    GREEN = "发"    # 发
    RED = "中"      # 中


class YakuType(Enum):
    """役种"""
    # 一番
    RIICHI = "立直"
    IPPATSU = "一发"
    TANYAO = "断幺九"
    PINFU = "平和"
    IIPETSKO = "一杯口"
    HAISETSU = "海底摸月/河底捞鱼"
    TSUMO = "自摸"
    HAITEI = "海底/河底"
    RINSHAN = "岭上开花"
    CHANKAN = "抢杠"
    MENZEN_TSUMO = "门前清自摸"
    # 二番
    DOUBLE_RIICHI = "两立直"
    CHANTA = "混全带幺九"
    HONROUTOU = "混老头"
    SANSHOKU_DOUJUN = "三色同顺"
    ITTSU = "一气通贯"
    TOITOI = "对对和"
    SANANKOU = "三暗刻"
    SANKANTSU = "三杠子"
    SHOSANGEN = "小三元"
    CHIITOU = "七对子"
    HONITSU = "混一色"
    # 三番
    JUNCHAN = "纯全带幺九"
    RYANPEIKOU = "二杯口"
    # 六番
    CHINITSU = "清一色"
    # 役满
    KOKUSHI = "国士无双"
    SUUANKOU = "四暗刻"
    DAISANGEN = "大三元"
    TSUUIISOU = "字一色"
    SHOUSUUSHI = "小四喜"
    DAISUUSHI = "大四喜"
    RYUUIISOU = "绿一色"
    CHINROUTOU = "清老头"
    SUUKANTSU = "四杠子"
    CHUUREN = "九莲宝灯"
    KOKUSHI_13 = "国士无双十三面"
    SUUANKOU_TANKI = "四暗刻单骑"
    JUNSEI_CHUUREN = "纯正九莲宝灯"


# ==================== 牌定义 ====================

@dataclass(frozen=True)
class Tile:
    """麻将牌"""
    tile_type: TileType
    number: int  # 1-9 for numbered tiles, 1-4 for winds, 1-3 for dragons
    
    def __post_init__(self):
        """验证牌的有效性"""
        if self.tile_type in (TileType.MAN, TileType.PIN, TileType.SOU):
            if not 1 <= self.number <= 9:
                raise ValueError(f"Invalid number {self.number} for {self.tile_type.value}")
        elif self.tile_type == TileType.WIND:
            if not 1 <= self.number <= 4:
                raise ValueError(f"Invalid wind number {self.number}")
        elif self.tile_type == TileType.DRAGON:
            if not 1 <= self.number <= 3:
                raise ValueError(f"Invalid dragon number {self.number}")
    
    @property
    def is_honor(self) -> bool:
        """是否为字牌（风牌或三元牌）"""
        return self.tile_type in (TileType.WIND, TileType.DRAGON)
    
    @property
    def is_terminal(self) -> bool:
        """是否为幺九牌（1或9的数牌）"""
        return not self.is_honor and self.number in (1, 9)
    
    @property
    def is_terminal_or_honor(self) -> bool:
        """是否为幺九牌（包括字牌）"""
        return self.is_terminal or self.is_honor
    
    @property
    def is_simple(self) -> bool:
        """是否为中张牌（2-8的数牌）"""
        return not self.is_honor and 2 <= self.number <= 8
    
    @property
    def is_green(self) -> bool:
        """是否为绿牌（可用于绿一色）"""
        # 索子：2, 3, 4, 6, 8；发
        if self.tile_type == TileType.SOU and self.number in (2, 3, 4, 6, 8):
            return True
        if self.tile_type == TileType.DRAGON and self.number == 2:  # 发
            return True
        return False
    
    def __str__(self) -> str:
        """字符串表示"""
        if self.tile_type == TileType.MAN:
            return f"{self.number}m"
        elif self.tile_type == TileType.PIN:
            return f"{self.number}p"
        elif self.tile_type == TileType.SOU:
            return f"{self.number}s"
        elif self.tile_type == TileType.WIND:
            winds = ["东", "南", "西", "北"]
            return winds[self.number - 1]
        else:  # Dragon
            dragons = ["白", "发", "中"]
            return dragons[self.number - 1]
    
    def to_chinese(self) -> str:
        """中文表示"""
        if self.tile_type == TileType.MAN:
            nums = ["一", "二", "三", "四", "五", "六", "七", "八", "九"]
            return nums[self.number - 1] + "万"
        elif self.tile_type == TileType.PIN:
            nums = ["一", "二", "三", "四", "五", "六", "七", "八", "九"]
            return nums[self.number - 1] + "筒"
        elif self.tile_type == TileType.SOU:
            nums = ["一", "二", "三", "四", "五", "六", "七", "八", "九"]
            return nums[self.number - 1] + "索"
        elif self.tile_type == TileType.WIND:
            winds = ["东", "南", "西", "北"]
            return winds[self.number - 1] + "风"
        else:
            dragons = ["白板", "发财", "红中"]
            return dragons[self.number - 1]
    
    @classmethod
    def from_string(cls, s: str) -> 'Tile':
        """从字符串解析"""
        s = s.strip().lower()
        if len(s) == 2 and s[1] in "mps":
            number = int(s[0])
            if s[1] == 'm':
                return cls(TileType.MAN, number)
            elif s[1] == 'p':
                return cls(TileType.PIN, number)
            else:
                return cls(TileType.SOU, number)
        elif s in ["东", "东1", "1w"]:
            return cls(TileType.WIND, 1)
        elif s in ["南", "南2", "2w"]:
            return cls(TileType.WIND, 2)
        elif s in ["西", "西3", "3w"]:
            return cls(TileType.WIND, 3)
        elif s in ["北", "北4", "4w"]:
            return cls(TileType.WIND, 4)
        elif s in ["白", "白板", "1d"]:
            return cls(TileType.DRAGON, 1)
        elif s in ["发", "发财", "2d"]:
            return cls(TileType.DRAGON, 2)
        elif s in ["中", "红中", "3d"]:
            return cls(TileType.DRAGON, 3)
        raise ValueError(f"Invalid tile string: {s}")


# 预定义所有牌
def create_all_tiles() -> List[Tile]:
    """创建所有麻将牌（每样4张）"""
    tiles = []
    # 数牌
    for tile_type in [TileType.MAN, TileType.PIN, TileType.SOU]:
        for num in range(1, 10):
            tiles.append(Tile(tile_type, num))
    # 风牌
    for num in range(1, 5):
        tiles.append(Tile(TileType.WIND, num))
    # 三元牌
    for num in range(1, 4):
        tiles.append(Tile(TileType.DRAGON, num))
    return tiles


# ==================== 手牌管理 ====================

class Hand:
    """麻将手牌"""
    
    def __init__(self, tiles: Optional[List[Tile]] = None):
        """初始化手牌"""
        self._tiles: List[Tile] = []
        self._melds: List[List[Tile]] = []  # 副露的牌组
        if tiles:
            self._tiles = list(tiles)
    
    @property
    def tiles(self) -> List[Tile]:
        """手牌列表"""
        return self._tiles.copy()
    
    @property
    def melds(self) -> List[List[Tile]]:
        """副露牌组"""
        return [m.copy() for m in self._melds]
    
    @property
    def is_closed(self) -> bool:
        """是否门前清"""
        return len(self._melds) == 0
    
    def add_tile(self, tile: Tile) -> 'Hand':
        """添加牌"""
        self._tiles.append(tile)
        return self
    
    def remove_tile(self, tile: Tile) -> 'Hand':
        """移除牌"""
        if tile in self._tiles:
            self._tiles.remove(tile)
        return self
    
    def add_meld(self, meld: List[Tile]) -> 'Hand':
        """添加副露"""
        self._melds.append(meld)
        return self
    
    def sort(self) -> 'Hand':
        """排序手牌"""
        self._tiles.sort(key=lambda t: (t.tile_type.value, t.number))
        return self
    
    def count_tile(self, tile: Tile) -> int:
        """计算某张牌的数量"""
        return sum(1 for t in self._tiles if t == tile)
    
    def get_tile_counts(self) -> Counter:
        """获取牌计数"""
        return Counter(self._tiles)
    
    def get_tile_types(self) -> Dict[TileType, Counter]:
        """按类型分组计数"""
        result = {tt: Counter() for tt in TileType}
        for tile in self._tiles:
            result[tile.tile_type][tile.number] += 1
        return result
    
    def to_tile_string(self) -> str:
        """转换为牌字符串表示"""
        self.sort()
        result = []
        for tile_type in [TileType.MAN, TileType.PIN, TileType.SOU]:
            nums = [str(t.number) for t in self._tiles if t.tile_type == tile_type]
            if nums:
                result.append(''.join(nums) + tile_type.value)
        
        # 字牌
        winds = [t for t in self._tiles if t.tile_type == TileType.WIND]
        dragons = [t for t in self._tiles if t.tile_type == TileType.DRAGON]
        if winds:
            wind_str = ''.join([str(t.number) for t in sorted(winds, key=lambda x: x.number)]) + 'z'
            result.append(wind_str)
        if dragons:
            dragon_str = ''.join([str(t.number) for t in sorted(dragons, key=lambda x: x.number)]) + 'z'
            result.append(dragon_str)
        
        return ' '.join(result)
    
    @classmethod
    def from_string(cls, s: str) -> 'Hand':
        """从字符串解析手牌"""
        tiles = []
        s = s.strip()
        
        for part in s.split():
            part = part.strip()
            if not part:
                continue
            
            # 找到最后一个字符作为类型
            tile_type_char = part[-1].lower()
            nums = part[:-1]
            
            if tile_type_char == 'm':
                for c in nums:
                    tiles.append(Tile(TileType.MAN, int(c)))
            elif tile_type_char == 'p':
                for c in nums:
                    tiles.append(Tile(TileType.PIN, int(c)))
            elif tile_type_char == 's':
                for c in nums:
                    tiles.append(Tile(TileType.SOU, int(c)))
            elif tile_type_char == 'z':
                # 字牌：1-4风，5-7三元
                for c in nums:
                    n = int(c)
                    if 1 <= n <= 4:
                        tiles.append(Tile(TileType.WIND, n))
                    elif 5 <= n <= 7:
                        tiles.append(Tile(TileType.DRAGON, n - 4))
        
        return cls(tiles)
    
    def __len__(self) -> int:
        return len(self._tiles)
    
    def __str__(self) -> str:
        return self.to_tile_string()
    
    def __repr__(self) -> str:
        return f"Hand({self.to_tile_string()})"


# ==================== 牌组定义 ====================

@dataclass
class Meld:
    """牌组"""
    tiles: List[Tile]
    meld_type: str  # 'chi'(顺子), 'pon'(刻子), 'kan'(杠子), 'pair'(对子)
    is_open: bool = False  # 是否副露
    
    @property
    def is_sequence(self) -> bool:
        return self.meld_type == 'chi'
    
    @property
    def is_triplet(self) -> bool:
        return self.meld_type == 'pon'
    
    @property
    def is_kan(self) -> bool:
        return self.meld_type == 'kan'
    
    @property
    def is_pair(self) -> bool:
        return self.meld_type == 'pair'


# ==================== 和牌检测 ====================

class WinDetector:
    """和牌检测器"""
    
    def __init__(self, hand: Hand, win_tile: Optional[Tile] = None):
        """
        初始化检测器
        
        Args:
            hand: 手牌（14张或13张+win_tile）
            win_tile: 和牌
        """
        self._hand = hand
        self._win_tile = win_tile
        self._tiles = list(hand.tiles)
        if win_tile:
            self._tiles.append(win_tile)
    
    def can_win(self) -> bool:
        """是否可以和牌"""
        return self.is_standard_win() or self.is_seven_pairs() or self.is_thirteen_orphans()
    
    def is_standard_win(self) -> bool:
        """是否为标准形和牌（4面子+1雀头）"""
        if len(self._tiles) != 14:
            return False
        
        counts = Counter(self._tiles)
        
        # 尝试每种可能的雀头
        for tile, cnt in counts.items():
            if cnt >= 2:
                # 移除雀头
                remaining = self._tiles.copy()
                for _ in range(2):
                    remaining.remove(tile)
                
                # 检查剩余是否可以组成4个面子
                if self._can_form_melds(remaining):
                    return True
        
        return False
    
    def is_seven_pairs(self) -> bool:
        """是否为七对子"""
        if len(self._tiles) != 14:
            return False
        
        counts = Counter(self._tiles)
        pairs = sum(1 for c in counts.values() if c == 2)
        return pairs == 7
    
    def is_thirteen_orphans(self) -> bool:
        """是否为国士无双"""
        if len(self._tiles) != 14:
            return False
        
        # 幺九牌集合
        terminals_honors = set()
        for tile in self._tiles:
            if tile.is_terminal_or_honor:
                terminals_honors.add(tile)
        
        # 需要所有13种幺九牌各一张，且其中一张重复
        if len(terminals_honors) != 13:
            return False
        
        counts = Counter(self._tiles)
        # 检查是否有一张牌重复（即凑成和牌）
        return any(c == 2 for c in counts.values())
    
    def _can_form_melds(self, tiles: List[Tile]) -> bool:
        """检查牌是否能组成面子"""
        if len(tiles) == 0:
            return True
        if len(tiles) % 3 != 0:
            return False
        
        counts = Counter(tiles)
        sorted_tiles = sorted(set(tiles), key=lambda t: (t.tile_type.value, t.number))
        
        return self._try_form_melds(counts, sorted_tiles, 0)
    
    def _try_form_melds(self, counts: Counter, sorted_tiles: List[Tile], index: int) -> bool:
        """递归尝试组成面子"""
        # 找到下一个非零数量的牌
        while index < len(sorted_tiles) and counts[sorted_tiles[index]] == 0:
            index += 1
        
        if index >= len(sorted_tiles):
            return True
        
        tile = sorted_tiles[index]
        count = counts[tile]
        
        if count == 0:
            return True
        
        # 尝试刻子
        if count >= 3:
            counts[tile] -= 3
            if self._try_form_melds(counts, sorted_tiles, index):
                counts[tile] += 3
                return True
            counts[tile] += 3
        
        # 尝试顺子（仅数牌，且号码<=7）
        if not tile.is_honor and tile.number <= 7:
            next1 = Tile(tile.tile_type, tile.number + 1)
            next2 = Tile(tile.tile_type, tile.number + 2)
            
            if next1 in counts and next2 in counts:
                if counts[next1] >= 1 and counts[next2] >= 1:
                    counts[tile] -= 1
                    counts[next1] -= 1
                    counts[next2] -= 1
                    if self._try_form_melds(counts, sorted_tiles, index):
                        counts[tile] += 1
                        counts[next1] += 1
                        counts[next2] += 1
                        return True
                    counts[tile] += 1
                    counts[next1] += 1
                    counts[next2] += 1
        
        return False
    
    def get_win_decomposition(self) -> Optional[List[Meld]]:
        """获取和牌分解"""
        if not self.can_win():
            return None
        
        # 尝试标准形
        if self.is_standard_win():
            decomposition = self._decompose_standard()
            if decomposition:
                return decomposition
        
        # 七对子
        if self.is_seven_pairs():
            counts = Counter(self._tiles)
            pairs = []
            for tile, cnt in counts.items():
                pairs.append(Meld([tile] * 2, 'pair'))
            return pairs
        
        # 国士无双
        if self.is_thirteen_orphans():
            melds = []
            counts = Counter(self._tiles)
            for tile, cnt in counts.items():
                if cnt == 2:
                    melds.append(Meld([tile] * 2, 'pair'))
                else:
                    melds.append(Meld([tile], 'pair'))  # 单张也用pair表示
            return melds
        
        return None
    
    def _decompose_standard(self) -> Optional[List[Meld]]:
        """分解标准形"""
        counts = Counter(self._tiles)
        
        for tile, cnt in counts.items():
            if cnt >= 2:
                # 尝试以该牌为雀头
                remaining_counts = counts.copy()
                remaining_counts[tile] -= 2
                if remaining_counts[tile] == 0:
                    del remaining_counts[tile]
                
                melds = [Meld([tile] * 2, 'pair')]
                if self._form_melds_recursive(remaining_counts, melds):
                    return melds
        
        return None
    
    def _form_melds_recursive(self, counts: Counter, melds: List[Meld]) -> bool:
        """递归形成面子"""
        if not counts:
            return True
        
        # 找最小的牌
        sorted_tiles = sorted(counts.keys(), key=lambda t: (t.tile_type.value, t.number))
        tile = sorted_tiles[0]
        count = counts[tile]
        
        # 尝试刻子
        if count >= 3:
            new_counts = counts.copy()
            new_counts[tile] -= 3
            if new_counts[tile] == 0:
                del new_counts[tile]
            melds.append(Meld([tile] * 3, 'pon'))
            if self._form_melds_recursive(new_counts, melds):
                return True
            melds.pop()
        
        # 尝试顺子
        if not tile.is_honor and tile.number <= 7:
            next1 = Tile(tile.tile_type, tile.number + 1)
            next2 = Tile(tile.tile_type, tile.number + 2)
            
            if next1 in counts and next2 in counts:
                new_counts = counts.copy()
                new_counts[tile] -= 1
                new_counts[next1] -= 1
                new_counts[next2] -= 1
                
                if new_counts[tile] == 0:
                    del new_counts[tile]
                if new_counts[next1] == 0:
                    del new_counts[next1]
                if new_counts[next2] == 0:
                    del new_counts[next2]
                
                melds.append(Meld([tile, next1, next2], 'chi'))
                if self._form_melds_recursive(new_counts, melds):
                    return True
                melds.pop()
        
        return False


# ==================== 役种检测 ====================

class YakuDetector:
    """役种检测器"""
    
    def __init__(self, hand: Hand, win_tile: Tile, 
                 is_tsumo: bool = False,
                 is_riichi: bool = False,
                 is_double_riichi: bool = False,
                 is_ippatsu: bool = False,
                 round_wind: Wind = Wind.EAST,
                 seat_wind: Wind = Wind.EAST,
                 dora_tiles: Optional[List[Tile]] = None,
                 winning_tile_source: str = "draw"):  # "draw", "discard", "kan", "rob_kan"
        self._hand = hand
        self._win_tile = win_tile
        self._is_tsumo = is_tsumo
        self._is_riichi = is_riichi
        self._is_double_riichi = is_double_riichi
        self._is_ippatsu = is_ippatsu
        self._round_wind = round_wind
        self._seat_wind = seat_wind
        self._dora_tiles = dora_tiles or []
        self._winning_tile_source = winning_tile_source
        
        # 构建完整手牌
        self._all_tiles = list(hand.tiles) + [win_tile]
        self._tile_counts = Counter(self._all_tiles)
        
        # 检测器
        self._detector = WinDetector(hand, win_tile)
        self._decomposition = self._detector.get_win_decomposition()
    
    def detect_yaku(self) -> List[Tuple[YakuType, int]]:
        """检测所有成立的役种"""
        if not self._detector.can_win():
            return []
        
        yaku_list = []
        
        # 立直相关
        if self._is_riichi:
            if self._is_double_riichi:
                yaku_list.append((YakuType.DOUBLE_RIICHI, 2))
            else:
                yaku_list.append((YakuType.RIICHI, 1))
        
        if self._is_ippatsu and self._is_riichi:
            yaku_list.append((YakuType.IPPATSU, 1))
        
        # 自摸
        if self._is_tsumo and self._hand.is_closed:
            yaku_list.append((YakuType.MENZEN_TSUMO, 1))
        
        # 牌型相关
        if self._detector.is_seven_pairs():
            yaku_list.append((YakuType.CHIITOU, 2))
            # 七对子可以复合的役：断幺九、混一色、清一色
            if self._is_tanyao():
                yaku_list.append((YakuType.TANYAO, 1))
            itsu_type = self._check_itsu()
            if itsu_type == "chinitsu":
                yaku_list.append((YakuType.CHINITSU, 6 if self._hand.is_closed else 5))
            elif itsu_type == "honitsu":
                yaku_list.append((YakuType.HONITSU, 3 if self._hand.is_closed else 2))
            return yaku_list
        
        if self._detector.is_thirteen_orphans():
            if self._tile_counts[self._win_tile] == 2:
                yaku_list.append((YakuType.KOKUSHI_13, 2))  # 双倍役满
            else:
                yaku_list.append((YakuType.KOKUSHI, 1))  # 役满
            return yaku_list  # 国士无双不复合其他役
        
        # 断幺九
        if self._is_tanyao():
            yaku_list.append((YakuType.TANYAO, 1))
        
        # 平和
        if self._is_pinfu():
            yaku_list.append((YakuType.PINFU, 1))
        
        # 一杯口/二杯口
        peikou_count = self._count_peikou()
        if peikou_count >= 2:
            yaku_list.append((YakuType.RYANPEIKOU, 3))
        elif peikou_count == 1:
            yaku_list.append((YakuType.IIPETSKO, 1))
        
        # 混全带幺九/纯全带幺九/混老头/清老头
        chanta_type = self._check_chanta()
        if chanta_type == "chinroutou":
            yaku_list.append((YakuType.CHINROUTOU, 2))  # 役满
        elif chanta_type == "honroutou":
            yaku_list.append((YakuType.HONROUTOU, 2))
        elif chanta_type == "junchan":
            yaku_list.append((YakuType.JUNCHAN, 3 if self._hand.is_closed else 2))
        elif chanta_type == "chanta":
            yaku_list.append((YakuType.CHANTA, 2 if self._hand.is_closed else 1))
        
        # 三色同顺
        if self._has_sanshoku_doujun():
            yaku_list.append((YakuType.SANSHOKU_DOUJUN, 2 if self._hand.is_closed else 1))
        
        # 一气通贯
        if self._has_ittsu():
            yaku_list.append((YakuType.ITTSU, 2 if self._hand.is_closed else 1))
        
        # 对对和
        if self._is_toitoi():
            yaku_list.append((YakuType.TOITOI, 2))
        
        # 三暗刻
        ankou_count = self._count_ankou()
        if ankou_count == 4:
            # 检查是否单骑
            if self._is_tanki():
                yaku_list.append((YakuType.SUUANKOU_TANKI, 2))  # 双倍役满
            else:
                yaku_list.append((YakuType.SUUANKOU, 1))  # 役满
        elif ankou_count == 3:
            yaku_list.append((YakuType.SANANKOU, 2))
        
        # 混一色/清一色
        itsu_type = self._check_itsu()
        if itsu_type == "chinitsu":
            yaku_list.append((YakuType.CHINITSU, 6 if self._hand.is_closed else 5))
        elif itsu_type == "honitsu":
            yaku_list.append((YakuType.HONITSU, 3 if self._hand.is_closed else 2))
        
        # 字一色
        if self._is_tsuuiisou():
            yaku_list.append((YakuType.TSUUIISOU, 1))  # 役满
        
        # 绿一色
        if self._is_ryuuiisou():
            yaku_list.append((YakuType.RYUUIISOU, 1))  # 役满
        
        # 大三元/小三元
        sangen_count, has_pair = self._count_sangen()
        if sangen_count == 3:
            yaku_list.append((YakuType.DAISANGEN, 1))  # 役满
        elif sangen_count == 2 and has_pair:
            yaku_list.append((YakuType.SHOSANGEN, 2))
        
        # 小四喜/大四喜
        wind_count, wind_pair = self._count_winds()
        if wind_count == 4:
            yaku_list.append((YakuType.DAISUUSHI, 2))  # 双倍役满
        elif wind_count == 3 and wind_pair:
            yaku_list.append((YakuType.SHOUSUUSHI, 1))  # 役满
        
        return yaku_list
    
    def _is_tanyao(self) -> bool:
        """断幺九"""
        return all(tile.is_simple for tile in self._all_tiles)
    
    def _is_pinfu(self) -> bool:
        """平和"""
        if not self._hand.is_closed:
            return False
        
        decomp = self._decomposition
        if not decomp:
            return False
        
        # 需要全部是顺子
        sequences = [m for m in decomp if m.meld_type == 'chi']
        pairs = [m for m in decomp if m.meld_type == 'pair']
        
        if len(sequences) != 4 or len(pairs) != 1:
            return False
        
        # 雀头不能是役牌
        pair_tile = pairs[0].tiles[0]
        if pair_tile.is_honor:
            # 检查是否为自风或场风
            if pair_tile.tile_type == TileType.WIND:
                if pair_tile.number == self._seat_wind.value:
                    return False
                if pair_tile.number == self._round_wind.value:
                    return False
            return False
        
        # 和牌必须是两面听
        # 检查和牌是否在顺子的两端
        for seq in sequences:
            if self._win_tile in seq.tiles:
                # 检查是否为边张或嵌张
                numbers = sorted([t.number for t in seq.tiles])
                if self._win_tile.number == numbers[1]:
                    # 嵌张
                    return False
                if numbers[0] == 1 and self._win_tile.number == 1:
                    # 边张
                    return False
                if numbers[2] == 9 and self._win_tile.number == 9:
                    # 边张
                    return False
                return True
        
        return False
    
    def _count_peikou(self) -> int:
        """计算一杯口的数量"""
        if not self._hand.is_closed:
            return 0
        
        decomp = self._decomposition
        if not decomp:
            return 0
        
        sequences = [m for m in decomp if m.meld_type == 'chi']
        
        # 按牌型分组
        sequence_types = {}
        for seq in sequences:
            tile_type_val = seq.tiles[0].tile_type.value
            start_num = min(t.number for t in seq.tiles)
            key = (tile_type_val, start_num)
            if key not in sequence_types:
                sequence_types[key] = []
            sequence_types[key].append(seq)
        
        # 计算相同顺子的对数
        peikou_count = 0
        for seqs in sequence_types.values():
            if len(seqs) >= 2:
                peikou_count += 1
        
        return peikou_count
    
    def _check_chanta(self) -> str:
        """检查混全带幺九/纯全带幺九/混老头/清老头"""
        decomp = self._decomposition
        if not decomp:
            return ""
        
        # 检查每个面子是否包含幺九牌
        has_honors = False
        has_simples = False
        has_terminals = False
        
        for tile in self._all_tiles:
            if tile.is_honor:
                has_honors = True
            elif tile.is_terminal:
                has_terminals = True
            elif tile.is_simple:
                has_simples = True
        
        # 清老头：全是幺九牌且无数牌
        if not has_simples and has_terminals and not has_honors:
            return "chinroutou"
        
        # 混老头：全是幺九牌（包括字牌）
        if not has_simples:
            return "honroutou"
        
        # 检查是否每个面子都包含幺九牌
        for meld in decomp:
            if meld.meld_type == 'pair':
                if not meld.tiles[0].is_terminal_or_honor:
                    return ""
            else:
                # 面子必须包含至少一张幺九牌
                has_yao = any(t.is_terminal_or_honor for t in meld.tiles)
                if not has_yao:
                    return ""
        
        # 纯全带幺九：所有面子包含幺九牌，无数牌
        if not has_honors:
            return "junchan"
        
        # 混全带幺九
        return "chanta"
    
    def _has_sanshoku_doujun(self) -> bool:
        """三色同顺"""
        decomp = self._decomposition
        if not decomp:
            return False
        
        sequences = [m for m in decomp if m.meld_type == 'chi']
        
        # 按起始数字分组
        for num in range(1, 8):
            found_m = found_p = found_s = False
            for seq in sequences:
                start_num = min(t.number for t in seq.tiles)
                if start_num == num:
                    if seq.tiles[0].tile_type == TileType.MAN:
                        found_m = True
                    elif seq.tiles[0].tile_type == TileType.PIN:
                        found_p = True
                    elif seq.tiles[0].tile_type == TileType.SOU:
                        found_s = True
            
            if found_m and found_p and found_s:
                return True
        
        return False
    
    def _has_ittsu(self) -> bool:
        """一气通贯"""
        decomp = self._decomposition
        if not decomp:
            return False
        
        sequences = [m for m in decomp if m.meld_type == 'chi']
        
        # 按类型分组
        for tile_type in [TileType.MAN, TileType.PIN, TileType.SOU]:
            start_nums = set()
            for seq in sequences:
                if seq.tiles[0].tile_type == tile_type:
                    start_nums.add(min(t.number for t in seq.tiles))
            
            if {1, 4, 7}.issubset(start_nums):
                return True
        
        return False
    
    def _is_toitoi(self) -> bool:
        """对对和"""
        decomp = self._decomposition
        if not decomp:
            return False
        
        # 需要全部是刻子或杠子
        for meld in decomp:
            if meld.meld_type not in ('pon', 'kan', 'pair'):
                return False
        
        # 至少3个刻子
        triplets = [m for m in decomp if m.meld_type in ('pon', 'kan')]
        return len(triplets) >= 4
    
    def _count_ankou(self) -> int:
        """统计暗刻数量"""
        decomp = self._decomposition
        if not decomp:
            return 0
        
        count = 0
        for meld in decomp:
            if meld.meld_type == 'pon' and not meld.is_open:
                count += 1
        
        return count
    
    def _is_tanki(self) -> bool:
        """是否单骑听牌"""
        decomp = self._decomposition
        if not decomp:
            return False
        
        # 和牌必须是对子中的一张
        for meld in decomp:
            if meld.meld_type == 'pair':
                return self._win_tile in meld.tiles
        
        return False
    
    def _check_itsu(self) -> str:
        """检查混一色/清一色"""
        types = set(tile.tile_type for tile in self._all_tiles)
        
        # 清一色
        if len(types) == 1:
            tile_type = list(types)[0]
            if tile_type in [TileType.MAN, TileType.PIN, TileType.SOU]:
                return "chinitsu"
            return ""  # 字一色
        
        # 混一色
        if len(types) == 2:
            honors_present = TileType.WIND in types or TileType.DRAGON in types
            numbered = [t for t in types if t in [TileType.MAN, TileType.PIN, TileType.SOU]]
            if honors_present and len(numbered) == 1:
                return "honitsu"
        
        return ""
    
    def _is_tsuuiisou(self) -> bool:
        """字一色"""
        return all(tile.is_honor for tile in self._all_tiles)
    
    def _is_ryuuiisou(self) -> bool:
        """绿一色"""
        return all(tile.is_green for tile in self._all_tiles)
    
    def _count_sangen(self) -> Tuple[int, bool]:
        """统计三元牌面子"""
        decomp = self._decomposition
        if not decomp:
            return 0, False
        
        triplet_count = 0
        has_pair = False
        
        for meld in decomp:
            if meld.tiles[0].tile_type == TileType.DRAGON:
                if meld.meld_type in ('pon', 'kan'):
                    triplet_count += 1
                elif meld.meld_type == 'pair':
                    has_pair = True
        
        return triplet_count, has_pair
    
    def _count_winds(self) -> Tuple[int, bool]:
        """统计风牌面子"""
        decomp = self._decomposition
        if not decomp:
            return 0, False
        
        triplet_count = 0
        has_pair = False
        
        for meld in decomp:
            if meld.tiles[0].tile_type == TileType.WIND:
                if meld.meld_type in ('pon', 'kan'):
                    triplet_count += 1
                elif meld.meld_type == 'pair':
                    has_pair = True
        
        return triplet_count, has_pair
    
    def calculate_han(self) -> int:
        """计算总番数"""
        yaku_list = self.detect_yaku()
        return sum(han for _, han in yaku_list)
    
    def is_yakuman(self) -> bool:
        """是否役满"""
        yakuman_types = {
            YakuType.KOKUSHI, YakuType.KOKUSHI_13,
            YakuType.SUUANKOU, YakuType.SUUANKOU_TANKI,
            YakuType.DAISANGEN, YakuType.TSUUIISOU,
            YakuType.SHOUSUUSHI, YakuType.DAISUUSHI,
            YakuType.RYUUIISOU, YakuType.CHINROUTOU,
            YakuType.SUUKANTSU, YakuType.CHUUREN,
            YakuType.JUNSEI_CHUUREN
        }
        
        yaku_list = self.detect_yaku()
        return any(yt in yakuman_types for yt, _ in yaku_list)


# ==================== 得分计算 ====================

class ScoreCalculator:
    """得分计算器"""
    
    # 符数表
    BASE_FU = 20  # 基础符
    
    # 番数-点数对照表（庄家/闲家）
    SCORE_TABLE = {
        # (番数, 符数): (闲家荣和, 庄家荣和, 闲家自摸每人, 庄家自摸每人)
        1: {30: (1000, 1500, 300, 500), 40: (1300, 2000, 400, 700), 
            50: (1600, 2400, 400, 800), 60: (2000, 2900, 500, 1000),
            70: (2300, 3400, 600, 1200), 80: (2600, 3900, 700, 1300),
            90: (2900, 4400, 800, 1500), 100: (3200, 4800, 800, 1600),
            110: (3600, 5300, 900, 1800)},
        2: {25: (1600, 2400, 400, 800), 30: (2000, 2900, 500, 1000),
            40: (2600, 3900, 700, 1300), 50: (3200, 4800, 800, 1600),
            60: (3900, 5800, 1000, 2000), 70: (4500, 6800, 1200, 2300)},
        3: {20: (2600, 3900, 700, 1300), 25: (3200, 4800, 800, 1600),
            30: (3900, 5800, 1000, 2000), 40: (5200, 7700, 1300, 2600)},
        4: {20: (5200, 7700, 1300, 2600), 25: (6400, 9600, 1600, 3200),
            30: (7700, 11600, 2000, 3900)},
        5: {"mangan": (8000, 12000, 2000, 4000)},  # 满贯
        6: {"haneman": (12000, 18000, 3000, 6000)},  # 跳满
        7: {"haneman": (12000, 18000, 3000, 6000)},
        8: {"baiman": (16000, 24000, 4000, 8000)},  # 倍满
        9: {"baiman": (16000, 24000, 4000, 8000)},
        10: {"baiman": (16000, 24000, 4000, 8000)},
        11: {"sanbaiman": (24000, 36000, 6000, 12000)},  # 三倍满
        12: {"sanbaiman": (24000, 36000, 6000, 12000)},
        13: {"yakuman": (32000, 48000, 8000, 16000)},  # 役满
    }
    
    def __init__(self, hand: Hand, win_tile: Tile, 
                 is_tsumo: bool = False,
                 is_dealer: bool = False,
                 yaku_detector: Optional[YakuDetector] = None):
        self._hand = hand
        self._win_tile = win_tile
        self._is_tsumo = is_tsumo
        self._is_dealer = is_dealer
        self._yaku_detector = yaku_detector
    
    def calculate_fu(self) -> int:
        """计算符数"""
        if not self._yaku_detector:
            return 0
        
        # 七对子固定25符
        detector = WinDetector(self._hand, self._win_tile)
        if detector.is_seven_pairs():
            return 25
        
        decomp = self._yaku_detector._decomposition
        if not decomp:
            return 0
        
        fu = self.BASE_FU
        
        # 和牌方式
        if not self._is_tsumo:
            fu += 10  # 荣和
        elif self._hand.is_closed:
            fu += 2  # 门前自摸
        
        # 面子符数
        for meld in decomp:
            if meld.meld_type == 'pair':
                # 役牌雀头
                tile = meld.tiles[0]
                if tile.tile_type == TileType.DRAGON:
                    fu += 2
                elif tile.tile_type == TileType.WIND:
                    if tile.number == self._yaku_detector._seat_wind.value:
                        fu += 2
                    if tile.number == self._yaku_detector._round_wind.value:
                        fu += 2
            
            elif meld.meld_type in ('pon', 'kan'):
                tile = meld.tiles[0]
                base = 2 if meld.meld_type == 'pon' else 8
                if tile.is_terminal_or_honor:
                    base *= 2
                if meld.is_open:
                    fu += base
                else:
                    fu += base * 2
            
            elif meld.meld_type == 'chi':
                # 顺子不加符
                pass
        
        # 听牌形式
        fu += self._calculate_wait_fu(decomp)
        
        # 向上取整到10
        return ((fu + 9) // 10) * 10
    
    def _calculate_wait_fu(self, decomp: List[Meld]) -> int:
        """计算听牌符"""
        for meld in decomp:
            if meld.meld_type == 'pair':
                # 单骑
                if self._win_tile in meld.tiles:
                    return 2
            
            elif meld.meld_type == 'chi':
                numbers = sorted([t.number for t in meld.tiles])
                if self._win_tile in meld.tiles:
                    win_num = self._win_tile.number
                    # 嵌张
                    if win_num == numbers[1]:
                        return 2
                    # 边张
                    if (numbers[0] == 1 and win_num == 3) or \
                       (numbers[2] == 9 and win_num == 7):
                        return 2
        
        return 0
    
    def calculate_score(self) -> Dict[str, int]:
        """计算得分"""
        if not self._yaku_detector:
            return {"total": 0}
        
        han = self._yaku_detector.calculate_han()
        fu = self.calculate_fu()
        
        # 役满
        if self._yaku_detector.is_yakuman():
            yakuman_count = sum(1 for yt, _ in self._yaku_detector.detect_yaku() 
                               if yt in {YakuType.KOKUSHI, YakuType.KOKUSHI_13,
                                        YakuType.SUUANKOU, YakuType.SUUANKOU_TANKI,
                                        YakuType.DAISANGEN, YakuType.TSUUIISOU,
                                        YakuType.SHOUSUUSHI, YakuType.DAISUUSHI,
                                        YakuType.RYUUIISOU, YakuType.CHINROUTOU,
                                        YakuType.SUUKANTSU, YakuType.CHUUREN,
                                        YakuType.JUNSEI_CHUUREN})
            
            base = 32000 * yakuman_count
            if self._is_dealer:
                if self._is_tsumo:
                    return {"total": base * 3, "each": base}
                else:
                    return {"total": base}
            else:
                if self._is_tsumo:
                    return {"total": base // 2 + base, "dealer": base, "non_dealer": base // 2}
                else:
                    return {"total": base}
        
        # 满贯及以上
        if han >= 13:
            return self._get_score_by_name("yakuman")
        elif han >= 11:
            return self._get_score_by_name("sanbaiman")
        elif han >= 8:
            return self._get_score_by_name("baiman")
        elif han >= 6:
            return self._get_score_by_name("haneman")
        elif han >= 5 or (han >= 4 and fu >= 40) or (han >= 3 and fu >= 70):
            return self._get_score_by_name("mangan")
        
        # 查表
        if han not in self.SCORE_TABLE:
            return {"total": 0}
        
        # 找到最接近的符数
        fu_options = self.SCORE_TABLE[han]
        actual_fu = fu
        
        if actual_fu not in fu_options:
            # 找到大于等于actual_fu的最小值
            available_fu = sorted(fu_options.keys())
            for f in available_fu:
                if f >= actual_fu:
                    actual_fu = f
                    break
            else:
                actual_fu = available_fu[-1]
        
        scores = fu_options[actual_fu]
        
        if self._is_dealer:
            if self._is_tsumo:
                return {"total": scores[3] * 3, "each": scores[3]}
            else:
                return {"total": scores[1]}
        else:
            if self._is_tsumo:
                return {"total": scores[2] + scores[3] * 2, "dealer": scores[3], "non_dealer": scores[2]}
            else:
                return {"total": scores[0]}
    
    def _get_score_by_name(self, name: str) -> Dict[str, int]:
        """根据名称获取得分"""
        scores = {
            "mangan": (8000, 12000, 2000, 4000),
            "haneman": (12000, 18000, 3000, 6000),
            "baiman": (16000, 24000, 4000, 8000),
            "sanbaiman": (24000, 36000, 6000, 12000),
            "yakuman": (32000, 48000, 8000, 16000),
        }
        
        s = scores[name]
        
        if self._is_dealer:
            if self._is_tsumo:
                return {"total": s[3] * 3, "each": s[3]}
            else:
                return {"total": s[1]}
        else:
            if self._is_tsumo:
                return {"total": s[2] + s[3] * 2, "dealer": s[3], "non_dealer": s[2]}
            else:
                return {"total": s[0]}


# ==================== 进张计算 ====================

class TileEfficiency:
    """进张效率计算"""
    
    def __init__(self, hand: Hand):
        self._hand = hand
    
    def get_shanten(self) -> int:
        """计算向听数（-1=和牌，0=听牌）"""
        tiles = list(self._hand.tiles)
        
        # 检查国士无双向听
        shanten = self._calculate_thirteen_orphans_shanten(tiles)
        min_shanten = shanten
        
        # 检查七对子向听
        shanten = self._calculate_seven_pairs_shanten(tiles)
        min_shanten = min(min_shanten, shanten)
        
        # 检查标准形向听
        shanten = self._calculate_standard_shanten(tiles)
        min_shanten = min(min_shanten, shanten)
        
        return min_shanten
    
    def _calculate_thirteen_orphans_shanten(self, tiles: List[Tile]) -> int:
        """国士无双向听数"""
        # 幺九牌
        terminals_honors = set()
        for t in tiles:
            if t.is_terminal_or_honor:
                terminals_honors.add(t)
        
        # 向听数 = 13 - 种类数 - (是否有对子)
        has_pair = any(tiles.count(t) >= 2 for t in terminals_honors)
        return 13 - len(terminals_honors) - (1 if has_pair else 0)
    
    def _calculate_seven_pairs_shanten(self, tiles: List[Tile]) -> int:
        """七对子向听数"""
        counts = Counter(tiles)
        pairs = sum(1 for c in counts.values() if c >= 2)
        singles = sum(1 for c in counts.values() if c == 1)
        
        # 向听数 = 6 - 对子数 + max(0, 7 - 对子数 - 单张数)
        return 6 - pairs + max(0, 7 - pairs - min(singles, 7 - pairs))
    
    def _calculate_standard_shanten(self, tiles: List[Tile]) -> int:
        """标准形向听数"""
        counts = Counter(tiles)
        
        min_shanten = 8  # 最大向听数
        
        # 尝试每种可能的雀头
        for tile, cnt in counts.items():
            if cnt >= 2:
                remaining = tiles.copy()
                remaining.remove(tile)
                remaining.remove(tile)
                shanten = self._calculate_melds_shanten(remaining, 0, 0, 4)
                min_shanten = min(min_shanten, shanten - 1)
        
        # 不选雀头
        shanten = self._calculate_melds_shanten(tiles, 0, 0, 4)
        min_shanten = min(min_shanten, shanten)
        
        return min_shanten
    
    def _calculate_melds_shanten(self, tiles: List[Tile], melds: int, taatsu: int, target_melds: int) -> int:
        """计算面子向听"""
        if not tiles:
            return 8 - 2 * melds - taatsu
        
        if melds + taatsu >= 4:
            return 8 - 2 * melds - taatsu
        
        counts = Counter(tiles)
        sorted_tiles = sorted(set(tiles), key=lambda t: (t.tile_type.value, t.number))
        
        tile = sorted_tiles[0]
        count = counts[tile]
        
        min_shanten = 8
        
        # 尝试刻子
        if count >= 3:
            remaining = tiles.copy()
            for _ in range(3):
                remaining.remove(tile)
            shanten = self._calculate_melds_shanten(remaining, melds + 1, taatsu, target_melds)
            min_shanten = min(min_shanten, shanten)
        
        # 尝试顺子
        if not tile.is_honor and tile.number <= 7:
            next1 = Tile(tile.tile_type, tile.number + 1)
            next2 = Tile(tile.tile_type, tile.number + 2)
            
            if next1 in counts and next2 in counts:
                remaining = tiles.copy()
                remaining.remove(tile)
                remaining.remove(next1)
                remaining.remove(next2)
                shanten = self._calculate_melds_shanten(remaining, melds + 1, taatsu, target_melds)
                min_shanten = min(min_shanten, shanten)
        
        # 尝试对子（搭子）
        if count >= 2:
            remaining = tiles.copy()
            remaining.remove(tile)
            remaining.remove(tile)
            shanten = self._calculate_melds_shanten(remaining, melds, taatsu + 1, target_melds)
            min_shanten = min(min_shanten, shanten)
        
        # 尝试两面/嵌张/边张搭子
        if not tile.is_honor and tile.number <= 8:
            next1 = Tile(tile.tile_type, tile.number + 1)
            if next1 in counts:
                remaining = tiles.copy()
                remaining.remove(tile)
                remaining.remove(next1)
                shanten = self._calculate_melds_shanten(remaining, melds, taatsu + 1, target_melds)
                min_shanten = min(min_shanten, shanten)
        
        if not tile.is_honor and tile.number <= 7:
            next2 = Tile(tile.tile_type, tile.number + 2)
            if next2 in counts:
                remaining = tiles.copy()
                remaining.remove(tile)
                remaining.remove(next2)
                shanten = self._calculate_melds_shanten(remaining, melds, taatsu + 1, target_melds)
                min_shanten = min(min_shanten, shanten)
        
        # 不使用这张牌
        remaining = tiles.copy()
        remaining.remove(tile)
        shanten = self._calculate_melds_shanten(remaining, melds, taatsu, target_melds)
        min_shanten = min(min_shanten, shanten)
        
        return min_shanten
    
    def get_waiting_tiles(self) -> List[Tile]:
        """获取听牌时的等待牌"""
        if self.get_shanten() != 0:
            return []
        
        waiting = []
        all_tiles = create_all_tiles()
        
        for tile in all_tiles:
            # 临时添加这张牌测试
            test_tiles = list(self._hand.tiles) + [tile]
            test_hand = Hand(test_tiles)
            detector = WinDetector(test_hand)
            if detector.can_win():
                waiting.append(tile)
        
        return waiting
    
    def calculate_ukeire(self) -> Dict[Tile, int]:
        """计算每张待牌的进张数"""
        shanten = self.get_shanten()
        
        if shanten == -1:
            return {}  # 已经和牌
        
        result = {}
        all_tiles = create_all_tiles()
        
        for tile in all_tiles:
            # 计算剩余牌数
            remaining = 4 - self._hand.count_tile(tile)
            if remaining <= 0:
                continue
            
            # 临时添加这张牌测试
            test_tiles = list(self._hand.tiles) + [tile]
            test_hand = Hand(test_tiles)
            test_efficiency = TileEfficiency(test_hand)
            new_shanten = test_efficiency.get_shanten()
            
            if new_shanten < shanten:
                result[tile] = remaining
        
        return result
    
    def find_best_discard(self) -> Optional[Tile]:
        """找到最佳切牌"""
        shanten = self.get_shanten()
        
        if shanten == -1:
            return None  # 已经和牌
        
        best_tile = None
        best_ukeire = -1
        
        counts = self._hand.get_tile_counts()
        
        for tile, cnt in counts.items():
            if cnt <= 0:
                continue
            
            # 模拟切牌
            test_tiles = list(self._hand.tiles)
            test_tiles.remove(tile)
            test_hand = Hand(test_tiles)
            test_efficiency = TileEfficiency(test_hand)
            
            # 计算新向听数
            new_shanten = test_efficiency.get_shanten()
            
            if new_shanten > shanten:
                continue  # 向听数增加，不是好切牌
            
            # 计算进张数
            ukeire = sum(test_efficiency.calculate_ukeire().values())
            
            if ukeire > best_ukeire:
                best_ukeire = ukeire
                best_tile = tile
        
        return best_tile


# ==================== 牌山模拟 ====================

class Wall:
    """牌山"""
    
    def __init__(self, seed: Optional[int] = None):
        """初始化牌山"""
        self._tiles: List[Tile] = []
        self._drawn: List[Tile] = []
        self._seed = seed
        
        if seed is not None:
            random.seed(seed)
        
        # 创建所有牌（每种4张）
        all_tiles = create_all_tiles()
        for tile in all_tiles:
            self._tiles.extend([tile] * 4)
        
        # 洗牌
        random.shuffle(self._tiles)
    
    def draw(self) -> Optional[Tile]:
        """摸牌"""
        if self._tiles:
            tile = self._tiles.pop()
            self._drawn.append(tile)
            return tile
        return None
    
    def draw_multiple(self, count: int) -> List[Tile]:
        """摸多张牌"""
        tiles = []
        for _ in range(count):
            tile = self.draw()
            if tile:
                tiles.append(tile)
        return tiles
    
    @property
    def remaining_count(self) -> int:
        """剩余牌数"""
        return len(self._tiles)
    
    @property
    def drawn_count(self) -> int:
        """已摸牌数"""
        return len(self._drawn)
    
    def peek(self, index: int = 0) -> Optional[Tile]:
        """查看牌山顶部的牌（不移除）"""
        if index < len(self._tiles):
            return self._tiles[-(index + 1)]
        return None


# ==================== 游戏辅助 ====================

class MahjongGame:
    """麻将游戏辅助类"""
    
    def __init__(self, player_count: int = 4):
        """初始化游戏"""
        self._player_count = player_count
        self._wall: Optional[Wall] = None
        self._hands: List[Hand] = []
        self._discards: List[List[Tile]] = []
        self._dora_indicators: List[Tile] = []
        self._current_player = 0
    
    def start_game(self, seed: Optional[int] = None):
        """开始游戏"""
        self._wall = Wall(seed)
        self._hands = []
        self._discards = [[] for _ in range(self._player_count)]
        self._dora_indicators = []
        self._current_player = 0
        
        # 发牌（每人13张）
        for i in range(self._player_count):
            tiles = self._wall.draw_multiple(13)
            self._hands.append(Hand(tiles))
        
        # 翻开宝牌指示牌
        indicator = self._wall.draw()
        if indicator:
            self._dora_indicators.append(indicator)
    
    def draw_tile(self, player: int) -> Optional[Tile]:
        """玩家摸牌"""
        if player < 0 or player >= self._player_count:
            return None
        
        tile = self._wall.draw()
        if tile:
            self._hands[player].add_tile(tile)
        return tile
    
    def discard_tile(self, player: int, tile: Tile) -> bool:
        """玩家打牌"""
        if player < 0 or player >= self._player_count:
            return False
        
        if tile not in self._hands[player].tiles:
            return False
        
        self._hands[player].remove_tile(tile)
        self._discards[player].append(tile)
        self._current_player = (player + 1) % self._player_count
        return True
    
    def get_dora_tiles(self) -> List[Tile]:
        """获取宝牌"""
        dora = []
        for indicator in self._dora_indicators:
            dora.append(self._get_next_tile(indicator))
        return dora
    
    def _get_next_tile(self, tile: Tile) -> Tile:
        """获取下一张牌（宝牌）"""
        if tile.tile_type in [TileType.MAN, TileType.PIN, TileType.SOU]:
            next_num = tile.number % 9 + 1
            return Tile(tile.tile_type, next_num)
        elif tile.tile_type == TileType.WIND:
            next_num = tile.number % 4 + 1
            return Tile(TileType.WIND, next_num)
        else:  # Dragon
            next_num = tile.number % 3 + 1
            return Tile(TileType.DRAGON, next_num)
    
    @property
    def remaining_tiles(self) -> int:
        """剩余牌数"""
        return self._wall.remaining_count if self._wall else 0
    
    def get_player_hand(self, player: int) -> Optional[Hand]:
        """获取玩家手牌"""
        if 0 <= player < self._player_count:
            return self._hands[player]
        return None


# ==================== 便捷函数 ====================

def parse_hand(s: str) -> Hand:
    """解析手牌字符串"""
    return Hand.from_string(s)


def create_tile(s: str) -> Tile:
    """创建牌"""
    return Tile.from_string(s)


def can_win(tiles: List[Tile]) -> bool:
    """检查是否可以和牌"""
    hand = Hand(tiles)
    detector = WinDetector(hand)
    return detector.can_win()


def calculate_shanten(tiles: List[Tile]) -> int:
    """计算向听数"""
    hand = Hand(tiles)
    efficiency = TileEfficiency(hand)
    return efficiency.get_shanten()


def get_waiting_tiles(tiles: List[Tile]) -> List[Tile]:
    """获取等待牌"""
    hand = Hand(tiles)
    efficiency = TileEfficiency(hand)
    return efficiency.get_waiting_tiles()


def detect_yaku(tiles: List[Tile], win_tile: Tile, **kwargs) -> List[Tuple[YakuType, int]]:
    """检测役种"""
    hand = Hand(tiles)
    detector = YakuDetector(hand, win_tile, **kwargs)
    return detector.detect_yaku()


def calculate_score(tiles: List[Tile], win_tile: Tile, **kwargs) -> Dict[str, int]:
    """计算得分"""
    hand = Hand(tiles)
    yaku_detector = YakuDetector(hand, win_tile, **kwargs)
    calculator = ScoreCalculator(hand, win_tile, yaku_detector=yaku_detector, **kwargs)
    return calculator.calculate_score()


# 导出
__all__ = [
    # 枚举
    'TileType', 'Wind', 'Dragon', 'YakuType',
    # 类
    'Tile', 'Hand', 'Meld', 'WinDetector', 'YakuDetector',
    'ScoreCalculator', 'TileEfficiency', 'Wall', 'MahjongGame',
    # 函数
    'create_all_tiles', 'parse_hand', 'create_tile', 'can_win',
    'calculate_shanten', 'get_waiting_tiles', 'detect_yaku', 'calculate_score',
]