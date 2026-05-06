"""
Keyboard Layout Utilities - 键盘布局工具库

提供多种键盘布局支持、按键距离计算、打字分析等功能。
零外部依赖，纯 Python 标准库实现。

主要功能：
- 多种键盘布局支持（QWERTY, Dvorak, Colemak, AZERTY, QWERTZ 等）
- 按键位置坐标
- 按键距离计算（欧几里得距离）
- 打字便利性分析（手指行程、交替手使用）
- 键盘模式检测（连续键、重复键等）
- 布局转换
- 密码强度辅助（键盘模式检测）
"""

from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Optional, Tuple, Set


class Finger(Enum):
    """手指枚举"""
    LEFT_PINKY = "left_pinky"
    LEFT_RING = "left_ring"
    LEFT_MIDDLE = "left_middle"
    LEFT_INDEX = "left_index"
    LEFT_THUMB = "left_thumb"
    RIGHT_THUMB = "right_thumb"
    RIGHT_INDEX = "right_index"
    RIGHT_MIDDLE = "right_middle"
    RIGHT_RING = "right_ring"
    RIGHT_PINKY = "right_pinky"


class Hand(Enum):
    """手枚举"""
    LEFT = "left"
    RIGHT = "right"
    BOTH = "both"  # 拇指或空格


@dataclass
class KeyPosition:
    """按键位置信息"""
    key: str
    row: int  # 行号，0=数字行，1=上行，2=中行，3=下行
    col: int  # 列号，从左到右
    finger: Finger
    hand: Hand
    shift_key: Optional[str] = None  # Shift 后的字符
    alt_key: Optional[str] = None   # AltGr 后的字符（部分布局）


@dataclass
class TypingAnalysis:
    """打字分析结果"""
    total_distance: float  # 总行程距离
    average_distance: float  # 平均每键距离
    hand_alternations: int  # 交替手次数
    same_hand_sequences: int  # 同手连续次数
    finger_usage: Dict[Finger, int]  # 各手指使用次数
    hand_usage: Dict[Hand, int]  # 各手使用次数
    rolling_sequences: int  # 滚动序列数（相邻手指连续按键）
    home_row_usage: int  # 基准行使用次数
    top_row_usage: int  # 上行使用次数
    bottom_row_usage: int  # 下行使用次数
    number_row_usage: int  # 数字行使用次数


# 键盘布局定义
# 格式：每行按键，每键包含 (主字符, shift字符, 手指)

QWERTY_LAYOUT = {
    "name": "QWERTY",
    "variant": "US",
    "rows": [
        # 数字行
        [("`", "~", Finger.LEFT_PINKY), ("1", "!", Finger.LEFT_PINKY), ("2", "@", Finger.LEFT_RING),
         ("3", "#", Finger.LEFT_MIDDLE), ("4", "$", Finger.LEFT_INDEX), ("5", "%", Finger.LEFT_INDEX),
         ("6", "^", Finger.RIGHT_INDEX), ("7", "&", Finger.RIGHT_INDEX), ("8", "*", Finger.RIGHT_MIDDLE),
         ("9", "(", Finger.RIGHT_RING), ("0", ")", Finger.RIGHT_PINKY), ("-", "_", Finger.RIGHT_PINKY),
         ("=", "+", Finger.RIGHT_PINKY)],
        # 上行 (QWERTY row)
        [("tab", "tab", Finger.LEFT_PINKY), ("q", "Q", Finger.LEFT_PINKY), ("w", "W", Finger.LEFT_RING),
         ("e", "E", Finger.LEFT_MIDDLE), ("r", "R", Finger.LEFT_INDEX), ("t", "T", Finger.LEFT_INDEX),
         ("y", "Y", Finger.RIGHT_INDEX), ("u", "U", Finger.RIGHT_INDEX), ("i", "I", Finger.RIGHT_MIDDLE),
         ("o", "O", Finger.RIGHT_RING), ("p", "P", Finger.RIGHT_PINKY), ("[", "{", Finger.RIGHT_PINKY),
         ("]", "}", Finger.RIGHT_PINKY), ("\\", "|", Finger.RIGHT_PINKY)],
        # 中行 (home row)
        [("caps", "caps", Finger.LEFT_PINKY), ("a", "A", Finger.LEFT_PINKY), ("s", "S", Finger.LEFT_RING),
         ("d", "D", Finger.LEFT_MIDDLE), ("f", "F", Finger.LEFT_INDEX), ("g", "G", Finger.LEFT_INDEX),
         ("h", "H", Finger.RIGHT_INDEX), ("j", "J", Finger.RIGHT_INDEX), ("k", "K", Finger.RIGHT_MIDDLE),
         ("l", "L", Finger.RIGHT_RING), (";", ":", Finger.RIGHT_PINKY), ("'", '"', Finger.RIGHT_PINKY),
         ("enter", "enter", Finger.RIGHT_PINKY)],
        # 下行
        [("shift_l", "shift_l", Finger.LEFT_PINKY), ("z", "Z", Finger.LEFT_PINKY), ("x", "X", Finger.LEFT_RING),
         ("c", "C", Finger.LEFT_MIDDLE), ("v", "V", Finger.LEFT_INDEX), ("b", "B", Finger.LEFT_INDEX),
         ("n", "N", Finger.RIGHT_INDEX), ("m", "M", Finger.RIGHT_INDEX), (",", "<", Finger.RIGHT_MIDDLE),
         (".", ">", Finger.RIGHT_RING), ("/", "?", Finger.RIGHT_PINKY), ("shift_r", "shift_r", Finger.RIGHT_PINKY)],
        # 空格行
        [("ctrl_l", "ctrl_l", Finger.LEFT_PINKY), ("win_l", "win_l", Finger.LEFT_PINKY),
         ("alt_l", "alt_l", Finger.LEFT_PINKY), ("space", " ", Finger.LEFT_THUMB),
         ("alt_r", "alt_r", Finger.RIGHT_THUMB), ("win_r", "win_r", Finger.RIGHT_THUMB),
         ("menu", "menu", Finger.RIGHT_THUMB), ("ctrl_r", "ctrl_r", Finger.RIGHT_PINKY)]
    ]
}

DVORAK_LAYOUT = {
    "name": "Dvorak",
    "variant": "US",
    "rows": [
        # 数字行
        [("`", "~", Finger.LEFT_PINKY), ("1", "!", Finger.LEFT_PINKY), ("2", "@", Finger.LEFT_RING),
         ("3", "#", Finger.LEFT_MIDDLE), ("4", "$", Finger.LEFT_INDEX), ("5", "%", Finger.LEFT_INDEX),
         ("6", "^", Finger.RIGHT_INDEX), ("7", "&", Finger.RIGHT_INDEX), ("8", "*", Finger.RIGHT_MIDDLE),
         ("9", "(", Finger.RIGHT_RING), ("0", ")", Finger.RIGHT_PINKY), ("[", "{", Finger.RIGHT_PINKY),
         ("]", "}", Finger.RIGHT_PINKY)],
        # 上行
        [("tab", "tab", Finger.LEFT_PINKY), ("'", '"', Finger.LEFT_PINKY), (",", "<", Finger.LEFT_RING),
         (".", ">", Finger.LEFT_MIDDLE), ("p", "P", Finger.LEFT_INDEX), ("y", "Y", Finger.LEFT_INDEX),
         ("f", "F", Finger.RIGHT_INDEX), ("g", "G", Finger.RIGHT_INDEX), ("c", "C", Finger.RIGHT_MIDDLE),
         ("r", "R", Finger.RIGHT_RING), ("l", "L", Finger.RIGHT_PINKY), ("/", "?", Finger.RIGHT_PINKY),
         ("=", "+", Finger.RIGHT_PINKY), ("\\", "|", Finger.RIGHT_PINKY)],
        # 中行 (home row) - Dvorak 设计让元音在左手
        [("caps", "caps", Finger.LEFT_PINKY), ("a", "A", Finger.LEFT_PINKY), ("o", "O", Finger.LEFT_RING),
         ("e", "E", Finger.LEFT_MIDDLE), ("u", "U", Finger.LEFT_INDEX), ("i", "I", Finger.LEFT_INDEX),
         ("d", "D", Finger.RIGHT_INDEX), ("h", "H", Finger.RIGHT_INDEX), ("t", "T", Finger.RIGHT_MIDDLE),
         ("n", "N", Finger.RIGHT_RING), ("s", "S", Finger.RIGHT_PINKY), ("-", "_", Finger.RIGHT_PINKY),
         ("enter", "enter", Finger.RIGHT_PINKY)],
        # 下行
        [("shift_l", "shift_l", Finger.LEFT_PINKY), (";", ":", Finger.LEFT_PINKY), ("q", "Q", Finger.LEFT_RING),
         ("j", "J", Finger.LEFT_MIDDLE), ("k", "K", Finger.LEFT_INDEX), ("x", "X", Finger.LEFT_INDEX),
         ("b", "B", Finger.RIGHT_INDEX), ("m", "M", Finger.RIGHT_INDEX), ("w", "W", Finger.RIGHT_MIDDLE),
         ("v", "V", Finger.RIGHT_RING), ("z", "Z", Finger.RIGHT_PINKY), ("shift_r", "shift_r", Finger.RIGHT_PINKY)],
        # 空格行
        [("ctrl_l", "ctrl_l", Finger.LEFT_PINKY), ("win_l", "win_l", Finger.LEFT_PINKY),
         ("alt_l", "alt_l", Finger.LEFT_PINKY), ("space", " ", Finger.LEFT_THUMB),
         ("alt_r", "alt_r", Finger.RIGHT_THUMB), ("win_r", "win_r", Finger.RIGHT_THUMB),
         ("menu", "menu", Finger.RIGHT_THUMB), ("ctrl_r", "ctrl_r", Finger.RIGHT_PINKY)]
    ]
}

COLEMAK_LAYOUT = {
    "name": "Colemak",
    "variant": "US",
    "rows": [
        # 数字行 (同 QWERTY)
        [("`", "~", Finger.LEFT_PINKY), ("1", "!", Finger.LEFT_PINKY), ("2", "@", Finger.LEFT_RING),
         ("3", "#", Finger.LEFT_MIDDLE), ("4", "$", Finger.LEFT_INDEX), ("5", "%", Finger.LEFT_INDEX),
         ("6", "^", Finger.RIGHT_INDEX), ("7", "&", Finger.RIGHT_INDEX), ("8", "*", Finger.RIGHT_MIDDLE),
         ("9", "(", Finger.RIGHT_RING), ("0", ")", Finger.RIGHT_PINKY), ("-", "_", Finger.RIGHT_PINKY),
         ("=", "+", Finger.RIGHT_PINKY)],
        # 上行 - Colemak 重新排列
        [("tab", "tab", Finger.LEFT_PINKY), ("q", "Q", Finger.LEFT_PINKY), ("w", "W", Finger.LEFT_RING),
         ("f", "F", Finger.LEFT_MIDDLE), ("p", "P", Finger.LEFT_INDEX), ("g", "G", Finger.LEFT_INDEX),
         ("j", "J", Finger.RIGHT_INDEX), ("l", "L", Finger.RIGHT_INDEX), ("u", "U", Finger.RIGHT_MIDDLE),
         ("y", "Y", Finger.RIGHT_RING), (";", ":", Finger.RIGHT_PINKY), ("[", "{", Finger.RIGHT_PINKY),
         ("]", "}", Finger.RIGHT_PINKY), ("\\", "|", Finger.RIGHT_PINKY)],
        # 中行 (home row) - Colemak 优化
        [("caps", "caps", Finger.LEFT_PINKY), ("a", "A", Finger.LEFT_PINKY), ("r", "R", Finger.LEFT_RING),
         ("s", "S", Finger.LEFT_MIDDLE), ("t", "T", Finger.LEFT_INDEX), ("d", "D", Finger.LEFT_INDEX),
         ("h", "H", Finger.RIGHT_INDEX), ("n", "N", Finger.RIGHT_INDEX), ("e", "E", Finger.RIGHT_MIDDLE),
         ("i", "I", Finger.RIGHT_RING), ("o", "O", Finger.RIGHT_PINKY), ("'", '"', Finger.RIGHT_PINKY),
         ("enter", "enter", Finger.RIGHT_PINKY)],
        # 下行
        [("shift_l", "shift_l", Finger.LEFT_PINKY), ("z", "Z", Finger.LEFT_PINKY), ("x", "X", Finger.LEFT_RING),
         ("c", "C", Finger.LEFT_MIDDLE), ("v", "V", Finger.LEFT_INDEX), ("b", "B", Finger.LEFT_INDEX),
         ("k", "K", Finger.RIGHT_INDEX), ("m", "M", Finger.RIGHT_INDEX), (",", "<", Finger.RIGHT_MIDDLE),
         (".", ">", Finger.RIGHT_RING), ("/", "?", Finger.RIGHT_PINKY), ("shift_r", "shift_r", Finger.RIGHT_PINKY)],
        # 空格行
        [("ctrl_l", "ctrl_l", Finger.LEFT_PINKY), ("win_l", "win_l", Finger.LEFT_PINKY),
         ("alt_l", "alt_l", Finger.LEFT_PINKY), ("space", " ", Finger.LEFT_THUMB),
         ("alt_r", "alt_r", Finger.RIGHT_THUMB), ("win_r", "win_r", Finger.RIGHT_THUMB),
         ("menu", "menu", Finger.RIGHT_THUMB), ("ctrl_r", "ctrl_r", Finger.RIGHT_PINKY)]
    ]
}

AZERTY_LAYOUT = {
    "name": "AZERTY",
    "variant": "French",
    "rows": [
        # 数字行
        [("²", "³", Finger.LEFT_PINKY), ("&", "1", Finger.LEFT_PINKY), ("é", "2", Finger.LEFT_RING),
         ('"', "3", Finger.LEFT_MIDDLE), ("'", "4", Finger.LEFT_INDEX), ("(", "5", Finger.LEFT_INDEX),
         ("-", "6", Finger.RIGHT_INDEX), ("è", "7", Finger.RIGHT_INDEX), ("_", "8", Finger.RIGHT_MIDDLE),
         ("ç", "9", Finger.RIGHT_RING), ("à", "0", Finger.RIGHT_PINKY), (")", "°", Finger.RIGHT_PINKY),
         ("=", "+", Finger.RIGHT_PINKY)],
        # 上行
        [("tab", "tab", Finger.LEFT_PINKY), ("a", "A", Finger.LEFT_PINKY), ("z", "Z", Finger.LEFT_RING),
         ("e", "E", Finger.LEFT_MIDDLE), ("r", "R", Finger.LEFT_INDEX), ("t", "T", Finger.LEFT_INDEX),
         ("y", "Y", Finger.RIGHT_INDEX), ("u", "U", Finger.RIGHT_INDEX), ("i", "I", Finger.RIGHT_MIDDLE),
         ("o", "O", Finger.RIGHT_RING), ("p", "P", Finger.RIGHT_PINKY), ("^", "¨", Finger.RIGHT_PINKY),
         ("$", "£", Finger.RIGHT_PINKY), ("*", "µ", Finger.RIGHT_PINKY)],
        # 中行 (home row)
        [("caps", "caps", Finger.LEFT_PINKY), ("q", "Q", Finger.LEFT_PINKY), ("s", "S", Finger.LEFT_RING),
         ("d", "D", Finger.LEFT_MIDDLE), ("f", "F", Finger.LEFT_INDEX), ("g", "G", Finger.LEFT_INDEX),
         ("h", "H", Finger.RIGHT_INDEX), ("j", "J", Finger.RIGHT_INDEX), ("k", "K", Finger.RIGHT_MIDDLE),
         ("l", "L", Finger.RIGHT_RING), ("m", "M", Finger.RIGHT_PINKY), ("ù", "%", Finger.RIGHT_PINKY),
         ("enter", "enter", Finger.RIGHT_PINKY)],
        # 下行
        [("shift_l", "shift_l", Finger.LEFT_PINKY), ("<", ">", Finger.LEFT_PINKY), ("w", "W", Finger.LEFT_RING),
         ("x", "X", Finger.LEFT_MIDDLE), ("c", "C", Finger.LEFT_INDEX), ("v", "V", Finger.LEFT_INDEX),
         ("b", "B", Finger.RIGHT_INDEX), ("n", "N", Finger.RIGHT_INDEX), (",", "?", Finger.RIGHT_MIDDLE),
         (";", ".", Finger.RIGHT_RING), (":", "/", Finger.RIGHT_PINKY), ("shift_r", "shift_r", Finger.RIGHT_PINKY)],
        # 空格行
        [("ctrl_l", "ctrl_l", Finger.LEFT_PINKY), ("win_l", "win_l", Finger.LEFT_PINKY),
         ("alt_l", "alt_l", Finger.LEFT_PINKY), ("space", " ", Finger.LEFT_THUMB),
         ("alt_r", "alt_r", Finger.RIGHT_THUMB), ("win_r", "win_r", Finger.RIGHT_THUMB),
         ("menu", "menu", Finger.RIGHT_THUMB), ("ctrl_r", "ctrl_r", Finger.RIGHT_PINKY)]
    ]
}

QWERTZ_LAYOUT = {
    "name": "QWERTZ",
    "variant": "German",
    "rows": [
        # 数字行
        [("^", "°", Finger.LEFT_PINKY), ("1", "!", Finger.LEFT_PINKY), ("2", '"', Finger.LEFT_RING),
         ("3", "§", Finger.LEFT_MIDDLE), ("4", "$", Finger.LEFT_INDEX), ("5", "%", Finger.LEFT_INDEX),
         ("6", "&", Finger.RIGHT_INDEX), ("7", "/", Finger.RIGHT_INDEX), ("8", "(", Finger.RIGHT_MIDDLE),
         ("9", ")", Finger.RIGHT_RING), ("0", "=", Finger.RIGHT_PINKY), ("ß", "?", Finger.RIGHT_PINKY),
         ("´", "`", Finger.RIGHT_PINKY)],
        # 上行
        [("tab", "tab", Finger.LEFT_PINKY), ("q", "Q", Finger.LEFT_PINKY), ("w", "W", Finger.LEFT_RING),
         ("e", "E", Finger.LEFT_MIDDLE), ("r", "R", Finger.LEFT_INDEX), ("t", "T", Finger.LEFT_INDEX),
         ("z", "Z", Finger.RIGHT_INDEX), ("u", "U", Finger.RIGHT_INDEX), ("i", "I", Finger.RIGHT_MIDDLE),
         ("o", "O", Finger.RIGHT_RING), ("p", "P", Finger.RIGHT_PINKY), ("ü", "Ü", Finger.RIGHT_PINKY),
         ("+", "*", Finger.RIGHT_PINKY), ("#", "'", Finger.RIGHT_PINKY)],
        # 中行 (home row)
        [("caps", "caps", Finger.LEFT_PINKY), ("a", "A", Finger.LEFT_PINKY), ("s", "S", Finger.LEFT_RING),
         ("d", "D", Finger.LEFT_MIDDLE), ("f", "F", Finger.LEFT_INDEX), ("g", "G", Finger.LEFT_INDEX),
         ("h", "H", Finger.RIGHT_INDEX), ("j", "J", Finger.RIGHT_INDEX), ("k", "K", Finger.RIGHT_MIDDLE),
         ("l", "L", Finger.RIGHT_RING), ("ö", "Ö", Finger.RIGHT_PINKY), ("ä", "Ä", Finger.RIGHT_PINKY),
         ("enter", "enter", Finger.RIGHT_PINKY)],
        # 下行
        [("shift_l", "shift_l", Finger.LEFT_PINKY), ("<", ">", Finger.LEFT_PINKY), ("y", "Y", Finger.LEFT_RING),
         ("x", "X", Finger.LEFT_MIDDLE), ("c", "C", Finger.LEFT_INDEX), ("v", "V", Finger.LEFT_INDEX),
         ("b", "B", Finger.RIGHT_INDEX), ("n", "N", Finger.RIGHT_INDEX), (",", ";", Finger.RIGHT_MIDDLE),
         (".", ":", Finger.RIGHT_RING), ("-", "_", Finger.RIGHT_PINKY), ("shift_r", "shift_r", Finger.RIGHT_PINKY)],
        # 空格行
        [("ctrl_l", "ctrl_l", Finger.LEFT_PINKY), ("win_l", "win_l", Finger.LEFT_PINKY),
         ("alt_l", "alt_l", Finger.LEFT_PINKY), ("space", " ", Finger.LEFT_THUMB),
         ("alt_r", "alt_r", Finger.RIGHT_THUMB), ("win_r", "win_r", Finger.RIGHT_THUMB),
         ("menu", "menu", Finger.RIGHT_THUMB), ("ctrl_r", "ctrl_r", Finger.RIGHT_PINKY)]
    ]
}

# 键盘宽度估算（单位：键宽）
KEY_WIDTH = 1.0
KEY_HEIGHT = 1.0
# 标准键盘行水平偏移
ROW_OFFSETS = {
    0: 0.0,    # 数字行
    1: 0.25,   # 上行（QWERTY row）
    2: 0.5,    # 中行（home row）
    3: 0.75,   # 下行
    4: 0.0     # 空格行（特殊处理）
}


class KeyboardLayout:
    """键盘布局类"""
    
    def __init__(self, layout: Dict):
        """初始化键盘布局
        
        Args:
            layout: 布局定义字典
        """
        self.name = layout["name"]
        self.variant = layout.get("variant", "standard")
        self.rows = layout["rows"]
        self._build_key_map()
    
    def _build_key_map(self):
        """构建按键映射表"""
        self.key_map: Dict[str, KeyPosition] = {}
        self.key_map_lower: Dict[str, KeyPosition] = {}
        self.key_map_upper: Dict[str, KeyPosition] = {}
        
        for row_idx, row in enumerate(self.rows):
            for col_idx, key_info in enumerate(row):
                main_char, shift_char, finger = key_info
                
                # 计算坐标
                x = col_idx * KEY_WIDTH + ROW_OFFSETS.get(row_idx, 0)
                y = row_idx * KEY_HEIGHT
                
                # 确定手
                hand = Hand.LEFT if finger.value.startswith("left") else Hand.RIGHT
                
                # 创建位置信息
                pos = KeyPosition(
                    key=main_char,
                    row=row_idx,
                    col=col_idx,
                    finger=finger,
                    hand=hand,
                    shift_key=shift_char if shift_char != main_char else None
                )
                
                # 添加到映射
                self.key_map[main_char.lower()] = pos
                self.key_map[main_char.upper()] = pos
                self.key_map_lower[main_char.lower()] = pos
                
                if shift_char and shift_char != main_char:
                    self.key_map[shift_char] = pos
                    self.key_map_upper[shift_char] = pos
    
    def get_key_position(self, char: str) -> Optional[KeyPosition]:
        """获取字符的按键位置
        
        Args:
            char: 要查找的字符
            
        Returns:
            按键位置信息，未找到返回 None
        """
        return self.key_map.get(char)
    
    def get_coordinates(self, char: str) -> Optional[Tuple[float, float]]:
        """获取字符的坐标位置
        
        Args:
            char: 要查找的字符
            
        Returns:
            (x, y) 坐标元组，未找到返回 None
        """
        pos = self.get_key_position(char)
        if pos is None:
            return None
        
        x = pos.col * KEY_WIDTH + ROW_OFFSETS.get(pos.row, 0)
        y = pos.row * KEY_HEIGHT
        return (x, y)
    
    def get_finger(self, char: str) -> Optional[Finger]:
        """获取字符对应的手指
        
        Args:
            char: 要查找的字符
            
        Returns:
            手指枚举，未找到返回 None
        """
        pos = self.get_key_position(char)
        return pos.finger if pos else None
    
    def get_hand(self, char: str) -> Optional[Hand]:
        """获取字符对应的手
        
        Args:
            char: 要查找的字符
            
        Returns:
            手枚举，未找到返回 None
        """
        pos = self.get_key_position(char)
        return pos.hand if pos else None


class KeyboardUtils:
    """键盘工具类"""
    
    LAYOUTS = {
        "qwerty": QWERTY_LAYOUT,
        "dvorak": DVORAK_LAYOUT,
        "colemak": COLEMAK_LAYOUT,
        "azerty": AZERTY_LAYOUT,
        "qwertz": QWERTZ_LAYOUT,
    }
    
    def __init__(self, layout: str = "qwerty"):
        """初始化键盘工具
        
        Args:
            layout: 键盘布局名称（qwerty, dvorak, colemak, azerty, qwertz）
        """
        layout_lower = layout.lower()
        if layout_lower not in self.LAYOUTS:
            raise ValueError(f"Unknown layout: {layout}. Available: {list(self.LAYOUTS.keys())}")
        
        self.layout_name = layout_lower
        self._layout = KeyboardLayout(self.LAYOUTS[layout_lower])
    
    @property
    def layout(self) -> KeyboardLayout:
        """获取当前布局对象"""
        return self._layout
    
    def distance(self, char1: str, char2: str) -> float:
        """计算两个按键之间的欧几里得距离
        
        Args:
            char1: 第一个字符
            char2: 第二个字符
            
        Returns:
            距离（单位：键宽），如果任一字符未找到返回 float('inf')
        """
        coord1 = self._layout.get_coordinates(char1)
        coord2 = self._layout.get_coordinates(char2)
        
        if coord1 is None or coord2 is None:
            return float('inf')
        
        return ((coord1[0] - coord2[0]) ** 2 + (coord1[1] - coord2[1]) ** 2) ** 0.5
    
    def total_distance(self, text: str) -> float:
        """计算输入文本的总行程距离
        
        Args:
            text: 输入的文本
            
        Returns:
            总距离（单位：键宽）
        """
        if not text:
            return 0.0
        
        total = 0.0
        prev_char = None
        
        for char in text:
            if prev_char is not None:
                total += self.distance(prev_char, char)
            prev_char = char
        
        return total
    
    def analyze(self, text: str) -> TypingAnalysis:
        """分析输入文本的打字特征
        
        Args:
            text: 输入的文本
            
        Returns:
            打字分析结果
        """
        if not text:
            return TypingAnalysis(
                total_distance=0.0,
                average_distance=0.0,
                hand_alternations=0,
                same_hand_sequences=0,
                finger_usage={f: 0 for f in Finger},
                hand_usage={h: 0 for h in Hand},
                rolling_sequences=0,
                home_row_usage=0,
                top_row_usage=0,
                bottom_row_usage=0,
                number_row_usage=0
            )
        
        total_dist = 0.0
        hand_alternations = 0
        same_hand_sequences = 0
        finger_usage: Dict[Finger, int] = {f: 0 for f in Finger}
        hand_usage: Dict[Hand, int] = {h: 0 for h in Hand}
        rolling_sequences = 0
        home_row_usage = 0
        top_row_usage = 0
        bottom_row_usage = 0
        number_row_usage = 0
        
        prev_pos = None
        prev_finger = None
        prev_hand = None
        
        for char in text:
            pos = self._layout.get_key_position(char)
            if pos is None:
                continue
            
            # 统计行使用
            if pos.row == 0:
                number_row_usage += 1
            elif pos.row == 1:
                top_row_usage += 1
            elif pos.row == 2:
                home_row_usage += 1
            elif pos.row == 3:
                bottom_row_usage += 1
            
            # 统计手指和手使用
            finger_usage[pos.finger] += 1
            hand_usage[pos.hand] += 1
            
            # 计算距离
            if prev_pos is not None:
                dist = self.distance(prev_pos.key, char)
                if dist != float('inf'):
                    total_dist += dist
                
                # 统计交替手和同手序列
                if prev_hand is not None:
                    if pos.hand != prev_hand:
                        hand_alternations += 1
                    else:
                        same_hand_sequences += 1
                
                # 检测滚动序列（相邻手指连续按键）
                if prev_finger is not None and pos.hand == prev_hand:
                    finger_order = list(Finger)
                    idx1 = finger_order.index(prev_finger)
                    idx2 = finger_order.index(pos.finger)
                    if abs(idx1 - idx2) == 1:
                        rolling_sequences += 1
            
            prev_pos = pos
            prev_finger = pos.finger
            prev_hand = pos.hand
        
        count = len(text)
        avg_dist = total_dist / count if count > 0 else 0.0
        
        return TypingAnalysis(
            total_distance=total_dist,
            average_distance=avg_dist,
            hand_alternations=hand_alternations,
            same_hand_sequences=same_hand_sequences,
            finger_usage=finger_usage,
            hand_usage=hand_usage,
            rolling_sequences=rolling_sequences,
            home_row_usage=home_row_usage,
            top_row_usage=top_row_usage,
            bottom_row_usage=bottom_row_usage,
            number_row_usage=number_row_usage
        )
    
    def is_same_hand(self, char1: str, char2: str) -> bool:
        """判断两个字符是否用同一只手输入
        
        Args:
            char1: 第一个字符
            char2: 第二个字符
            
        Returns:
            是否用同一只手
        """
        hand1 = self._layout.get_hand(char1)
        hand2 = self._layout.get_hand(char2)
        
        if hand1 is None or hand2 is None:
            return False
        
        return hand1 == hand2 and hand1 != Hand.BOTH
    
    def is_same_finger(self, char1: str, char2: str) -> bool:
        """判断两个字符是否用同一根手指输入
        
        Args:
            char1: 第一个字符
            char2: 第二个字符
            
        Returns:
            是否用同一根手指
        """
        finger1 = self._layout.get_finger(char1)
        finger2 = self._layout.get_finger(char2)
        
        if finger1 is None or finger2 is None:
            return False
        
        return finger1 == finger2
    
    def is_adjacent_finger(self, char1: str, char2: str) -> bool:
        """判断两个字符是否用相邻手指输入（同一只手）
        
        Args:
            char1: 第一个字符
            char2: 第二个字符
            
        Returns:
            是否用相邻手指
        """
        finger1 = self._layout.get_finger(char1)
        finger2 = self._layout.get_finger(char2)
        hand1 = self._layout.get_hand(char1)
        hand2 = self._layout.get_hand(char2)
        
        if finger1 is None or finger2 is None:
            return False
        
        if hand1 != hand2 or hand1 == Hand.BOTH:
            return False
        
        # 定义手指相邻关系
        finger_order = [
            Finger.LEFT_PINKY, Finger.LEFT_RING, Finger.LEFT_MIDDLE, Finger.LEFT_INDEX,
            Finger.LEFT_THUMB, Finger.RIGHT_THUMB,
            Finger.RIGHT_INDEX, Finger.RIGHT_MIDDLE, Finger.RIGHT_RING, Finger.RIGHT_PINKY
        ]
        
        idx1 = finger_order.index(finger1)
        idx2 = finger_order.index(finger2)
        
        return abs(idx1 - idx2) == 1
    
    def is_home_row(self, char: str) -> bool:
        """判断字符是否在基准行（home row）
        
        Args:
            char: 字符
            
        Returns:
            是否在基准行
        """
        pos = self._layout.get_key_position(char)
        return pos is not None and pos.row == 2
    
    def is_top_row(self, char: str) -> bool:
        """判断字符是否在上行（QWERTY row）
        
        Args:
            char: 字符
            
        Returns:
            是否在上行
        """
        pos = self._layout.get_key_position(char)
        return pos is not None and pos.row == 1
    
    def is_bottom_row(self, char: str) -> bool:
        """判断字符是否在下行
        
        Args:
            char: 字符
            
        Returns:
            是否在下行
        """
        pos = self._layout.get_key_position(char)
        return pos is not None and pos.row == 3
    
    def is_number_row(self, char: str) -> bool:
        """判断字符是否在数字行
        
        Args:
            char: 字符
            
        Returns:
            是否在数字行
        """
        pos = self._layout.get_key_position(char)
        return pos is not None and pos.row == 0
    
    def is_consecutive(self, char1: str, char2: str) -> bool:
        """判断两个字符是否在键盘上相邻
        
        Args:
            char1: 第一个字符
            char2: 第二个字符
            
        Returns:
            是否相邻
        """
        return self.distance(char1, char2) <= 1.5  # 约1.5个键宽以内
    
    def get_keyboard_patterns(self, text: str) -> List[Dict]:
        """检测文本中的键盘模式
        
        Args:
            text: 输入的文本
            
        Returns:
            检测到的模式列表
        """
        patterns = []
        
        if not text or len(text) < 2:
            return patterns
        
        # 检测连续相邻键
        for i in range(len(text) - 1):
            if self.is_consecutive(text[i], text[i + 1]):
                patterns.append({
                    "type": "consecutive",
                    "start": i,
                    "end": i + 1,
                    "chars": text[i:i + 2]
                })
        
        # 检测同指重复
        for i in range(len(text) - 1):
            if self.is_same_finger(text[i], text[i + 1]):
                patterns.append({
                    "type": "same_finger",
                    "start": i,
                    "end": i + 1,
                    "chars": text[i:i + 2]
                })
        
        # 检测直线模式（水平或垂直）
        for i in range(len(text) - 2):
            coord1 = self._layout.get_coordinates(text[i])
            coord2 = self._layout.get_coordinates(text[i + 1])
            coord3 = self._layout.get_coordinates(text[i + 2])
            
            if coord1 and coord2 and coord3:
                # 检查是否在同一直线上
                dx1, dy1 = coord2[0] - coord1[0], coord2[1] - coord1[1]
                dx2, dy2 = coord3[0] - coord2[0], coord3[1] - coord2[1]
                
                # 水平或垂直直线
                if (abs(dy1) < 0.1 and abs(dy2) < 0.1) or (abs(dx1) < 0.1 and abs(dx2) < 0.1):
                    patterns.append({
                        "type": "straight_line",
                        "start": i,
                        "end": i + 2,
                        "chars": text[i:i + 3]
                    })
        
        return patterns
    
    def convert_to_layout(self, text: str, target_layout: str) -> str:
        """将文本从一个布局转换到另一个布局（位置转换）
        
        注意：这是基于位置的转换，保持手指位置不变
        
        Args:
            text: 原始文本
            target_layout: 目标布局名称
            
        Returns:
            转换后的文本
        """
        if target_layout.lower() not in self.LAYOUTS:
            raise ValueError(f"Unknown target layout: {target_layout}")
        
        target = KeyboardLayout(self.LAYOUTS[target_layout.lower()])
        
        result = []
        for char in text:
            # 获取当前布局中的位置
            pos = self._layout.get_key_position(char)
            if pos is None:
                result.append(char)
                continue
            
            # 在目标布局中查找相同位置的字符
            target_char = self._find_char_at_position(target, pos.row, pos.col)
            result.append(target_char if target_char else char)
        
        return ''.join(result)
    
    def _find_char_at_position(self, layout: KeyboardLayout, row: int, col: int) -> Optional[str]:
        """在布局中查找指定位置的字符
        
        Args:
            layout: 键盘布局
            row: 行号
            col: 列号
            
        Returns:
            字符，未找到返回 None
        """
        if row < 0 or row >= len(layout.rows):
            return None
        
        row_keys = layout.rows[row]
        if col < 0 or col >= len(row_keys):
            return None
        
        return row_keys[col][0]  # 返回主字符
    
    def get_efficiency_score(self, text: str) -> float:
        """计算文本的打字效率分数
        
        基于：
        - 基准行使用率（越高越好）
        - 手交替率（越高越好）
        - 总行程距离（越短越好）
        - 滚动序列（越多越好）
        
        Args:
            text: 输入的文本
            
        Returns:
            效率分数（0-100）
        """
        if not text:
            return 100.0
        
        analysis = self.analyze(text)
        count = len(text)
        
        # 基准行使用率得分（目标：50%以上）
        home_row_score = min(100, (analysis.home_row_usage / count) * 200)
        
        # 手交替得分（目标：50%以上）
        total_transitions = analysis.hand_alternations + analysis.same_hand_sequences
        if total_transitions > 0:
            alt_score = min(100, (analysis.hand_alternations / total_transitions) * 200)
        else:
            alt_score = 100
        
        # 行程距离得分（每键平均距离越小越好，假设最优约1.0）
        dist_score = max(0, 100 - analysis.average_distance * 20)
        
        # 滚动序列得分
        if count > 1:
            rolling_score = min(100, (analysis.rolling_sequences / (count - 1)) * 300)
        else:
            rolling_score = 0
        
        # 综合得分
        return (home_row_score * 0.3 + alt_score * 0.3 + dist_score * 0.3 + rolling_score * 0.1)
    
    def suggest_alternatives(self, text: str) -> List[Dict]:
        """为文本中的低效字符序列提供替代建议
        
        Args:
            text: 输入的文本
            
        Returns:
            建议列表
        """
        suggestions = []
        
        if not text or len(text) < 2:
            return suggestions
        
        for i in range(len(text) - 1):
            char1, char2 = text[i], text[i + 1]
            
            # 同指连续
            if self.is_same_finger(char1, char2):
                suggestions.append({
                    "position": i,
                    "type": "same_finger",
                    "chars": f"{char1}{char2}",
                    "message": f"'{char1}' 和 '{char2}' 使用同一根手指，可能导致减速"
                })
            
            # 长距离跳跃
            dist = self.distance(char1, char2)
            if dist > 3.0:
                suggestions.append({
                    "position": i,
                    "type": "long_jump",
                    "chars": f"{char1}{char2}",
                    "distance": round(dist, 2),
                    "message": f"'{char1}' 到 '{char2}' 距离较长（{dist:.2f} 键宽）"
                })
            
            # 连续使用小指
            finger1 = self._layout.get_finger(char1)
            finger2 = self._layout.get_finger(char2)
            pinky_fingers = {Finger.LEFT_PINKY, Finger.RIGHT_PINKY}
            if finger1 in pinky_fingers and finger2 in pinky_fingers:
                suggestions.append({
                    "position": i,
                    "type": "double_pinky",
                    "chars": f"{char1}{char2}",
                    "message": f"'{char1}' 和 '{char2}' 都使用小指，可能影响速度"
                })
        
        return suggestions


# 便捷函数
_default_utils: Optional[KeyboardUtils] = None


def get_utils(layout: str = "qwerty") -> KeyboardUtils:
    """获取键盘工具实例
    
    Args:
        layout: 键盘布局名称
        
    Returns:
        KeyboardUtils 实例
    """
    global _default_utils
    if _default_utils is None or _default_utils.layout_name != layout.lower():
        _default_utils = KeyboardUtils(layout)
    return _default_utils


def distance(char1: str, char2: str, layout: str = "qwerty") -> float:
    """计算两个按键之间的距离
    
    Args:
        char1: 第一个字符
        char2: 第二个字符
        layout: 键盘布局
        
    Returns:
        距离
    """
    return get_utils(layout).distance(char1, char2)


def total_distance(text: str, layout: str = "qwerty") -> float:
    """计算输入文本的总行程距离
    
    Args:
        text: 输入的文本
        layout: 键盘布局
        
    Returns:
        总距离
    """
    return get_utils(layout).total_distance(text)


def analyze(text: str, layout: str = "qwerty") -> TypingAnalysis:
    """分析输入文本的打字特征
    
    Args:
        text: 输入的文本
        layout: 键盘布局
        
    Returns:
        打字分析结果
    """
    return get_utils(layout).analyze(text)


def get_key_position(char: str, layout: str = "qwerty") -> Optional[KeyPosition]:
    """获取字符的按键位置
    
    Args:
        char: 字符
        layout: 键盘布局
        
    Returns:
        按键位置信息
    """
    return get_utils(layout).layout.get_key_position(char)


def get_coordinates(char: str, layout: str = "qwerty") -> Optional[Tuple[float, float]]:
    """获取字符的坐标位置
    
    Args:
        char: 字符
        layout: 键盘布局
        
    Returns:
        (x, y) 坐标元组
    """
    return get_utils(layout).layout.get_coordinates(char)


def get_finger(char: str, layout: str = "qwerty") -> Optional[Finger]:
    """获取字符对应的手指
    
    Args:
        char: 字符
        layout: 键盘布局
        
    Returns:
        手指枚举
    """
    return get_utils(layout).layout.get_finger(char)


def get_hand(char: str, layout: str = "qwerty") -> Optional[Hand]:
    """获取字符对应的手
    
    Args:
        char: 字符
        layout: 键盘布局
        
    Returns:
        手枚举
    """
    return get_utils(layout).layout.get_hand(char)


def efficiency_score(text: str, layout: str = "qwerty") -> float:
    """计算文本的打字效率分数
    
    Args:
        text: 输入的文本
        layout: 键盘布局
        
    Returns:
        效率分数（0-100）
    """
    return get_utils(layout).get_efficiency_score(text)


def get_keyboard_patterns(text: str, layout: str = "qwerty") -> List[Dict]:
    """检测文本中的键盘模式
    
    Args:
        text: 输入的文本
        layout: 键盘布局
        
    Returns:
        检测到的模式列表
    """
    return get_utils(layout).get_keyboard_patterns(text)


def suggest_improvements(text: str, layout: str = "qwerty") -> List[Dict]:
    """为文本提供改进建议
    
    Args:
        text: 输入的文本
        layout: 键盘布局
        
    Returns:
        建议列表
    """
    return get_utils(layout).suggest_alternatives(text)


def available_layouts() -> List[str]:
    """获取可用的键盘布局列表
    
    Returns:
        布局名称列表
    """
    return list(KeyboardUtils.LAYOUTS.keys())