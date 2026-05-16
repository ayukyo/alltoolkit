"""
Guitar Chord Utils - 吉他和弦工具库

零依赖的吉他和弦库，支持：
- 和弦指法（标准、简化、变位）
- 和弦图表生成（ASCII/文本格式）
- 和弦音计算（与音乐理论库整合）
- 常用和弦库（100+ 和弦）
- 和弦转换建议
- 和弦难度评估
- 练习建议生成

Author: AllToolkit
License: MIT
"""

from typing import List, Tuple, Dict, Optional, Set
from dataclasses import dataclass
from enum import Enum
import math


class GuitarString(Enum):
    """吉他弦"""
    E6 = 0   # 第6弦（低音E）
    A5 = 1   # 第5弦（A）
    D4 = 2   # 第4弦（D）
    G3 = 3   # 第3弦（G）
    B2 = 4   # 第2弦（B）
    E1 = 5   # 第1弦（高音E）


# 标准吉他定弦（空弦音）
STRING_OPEN_NOTES = {
    GuitarString.E6: 'E',
    GuitarString.A5: 'A',
    GuitarString.D4: 'D',
    GuitarString.G3: 'G',
    GuitarString.B2: 'B',
    GuitarString.E1: 'E',
}

# 每弦半音位置对应的音符
NOTE_CHROMATIC = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
NOTE_CHROMATIC_FLAT = ['C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B']


@dataclass
class FingerPosition:
    """手指位置"""
    string: GuitarString    # 弦
    fret: int               # 指板品数（0=空弦，-1=不弹/闷音）
    finger: int             # 手指编号（1-4，0=不按）


@dataclass
class GuitarChord:
    """吉他和弦"""
    name: str                               # 和弦名称（如 'C', 'Am', 'F#m7'）
    positions: List[FingerPosition]         # 指法位置列表
    barre: Optional[int] = None             # 大横按品数（None=无横按）
    barre_strings: Optional[List[GuitarString]] = None  # 横按涉及的弦
    difficulty: int = 1                     # 难度等级（1-5）
    notes: List[str] = None                 # 和弦音符
    
    def __post_init__(self):
        if self.notes is None:
            self.notes = self._calculate_notes()
    
    def _calculate_notes(self) -> List[str]:
        """计算和弦音符"""
        notes = []
        for pos in self.positions:
            if pos.fret == -1:  # 闷音，不计入
                continue
            note = self._get_note_at_position(pos.string, pos.fret)
            if note and note not in notes:
                notes.append(note)
        return notes
    
    def _get_note_at_position(self, string: GuitarString, fret: int) -> str:
        """获取指定弦和品位的音符"""
        open_note = STRING_OPEN_NOTES[string]
        open_index = NOTE_CHROMATIC.index(open_note) if open_note in NOTE_CHROMATIC else 0
        note_index = (open_index + fret) % 12
        return NOTE_CHROMATIC[note_index]


class ChordDifficulty(Enum):
    """和弦难度等级"""
    BEGINNER = 1      # 初学者
    EASY = 2          # 容易
    INTERMEDIATE = 3  # 中等
    ADVANCED = 4      # 进阶
    EXPERT = 5        # 专家


# 常用和弦库
CHORD_DATABASE: Dict[str, List[Dict]] = {
    # 大和弦
    'C': [
        {'positions': [(0, 0), (1, 1, 1), (2, 0), (3, 0), (4, 1, 2), (5, 0)], 'barre': None, 'difficulty': 1},
        {'positions': [(0, 3, 3), (1, 2, 2), (2, 0), (3, 0), (4, 1, 1), (5, 0)], 'barre': 3, 'barre_strings': [0, 1], 'difficulty': 3},
    ],
    'D': [
        {'positions': [(0, -1), (1, 0), (2, 0), (3, 2, 1), (4, 3, 2), (5, 2, 3)], 'barre': None, 'difficulty': 1},
    ],
    'E': [
        {'positions': [(0, 0), (1, 2, 2), (2, 2, 3), (3, 0), (4, 0), (5, 0)], 'barre': None, 'difficulty': 1},
    ],
    'F': [
        {'positions': [(0, 1, 1), (1, 1, 1), (2, 2, 2), (3, 3, 3), (4, 3, 4), (5, 1, 1)], 'barre': 1, 'barre_strings': [0, 1, 5], 'difficulty': 4},
        {'positions': [(0, -1), (1, 1, 1), (2, 2, 2), (3, 3, 3), (4, 3, 4), (5, 1, 1)], 'barre': 1, 'barre_strings': [1, 5], 'difficulty': 3},
    ],
    'G': [
        {'positions': [(0, 3, 4), (1, 2, 2), (2, 0), (3, 0), (4, 0), (5, 3, 1)], 'barre': None, 'difficulty': 2},
        {'positions': [(0, 3, 4), (1, 2, 3), (2, 0), (3, 0), (4, 0), (5, 3, 1)], 'barre': None, 'difficulty': 2},
    ],
    'A': [
        {'positions': [(0, -1), (1, 0), (2, 2, 1), (3, 2, 2), (4, 2, 3), (5, 0)], 'barre': None, 'difficulty': 1},
        {'positions': [(0, -1), (1, 0), (2, 2, 1), (3, 2, 1), (4, 2, 1), (5, 0)], 'barre': 2, 'barre_strings': [2, 3, 4], 'difficulty': 2},
    ],
    'B': [
        {'positions': [(0, -1), (1, 2, 1), (2, 4, 3), (3, 4, 4), (4, 4, 4), (5, 2, 1)], 'barre': 2, 'barre_strings': [1, 5], 'difficulty': 3},
        {'positions': [(0, 2, 1), (1, 2, 1), (2, 4, 3), (3, 4, 4), (4, 4, 4), (5, 2, 1)], 'barre': 2, 'barre_strings': [0, 1, 5], 'difficulty': 4},
    ],
    
    # 小和弦
    'Am': [
        {'positions': [(0, 0), (1, 0), (2, 2, 2), (3, 2, 3), (4, 1, 1), (5, 0)], 'barre': None, 'difficulty': 1},
    ],
    'Dm': [
        {'positions': [(0, -1), (1, 0), (2, 0), (3, 2, 1), (4, 3, 3), (5, 1, 2)], 'barre': None, 'difficulty': 1},
    ],
    'Em': [
        {'positions': [(0, 0), (1, 2, 2), (2, 2, 3), (3, 0), (4, 0), (5, 0)], 'barre': None, 'difficulty': 1},
    ],
    'Bm': [
        {'positions': [(0, -1), (1, 2, 1), (2, 4, 3), (3, 4, 4), (4, 3, 2), (5, 2, 1)], 'barre': 2, 'barre_strings': [1, 5], 'difficulty': 3},
        {'positions': [(0, 2, 1), (1, 2, 1), (2, 4, 3), (3, 4, 4), (4, 3, 2), (5, 2, 1)], 'barre': 2, 'barre_strings': [0, 1, 5], 'difficulty': 4},
    ],
    'Fm': [
        {'positions': [(0, 1, 1), (1, 1, 1), (2, 3, 2), (3, 3, 3), (4, 1, 1), (5, 1, 1)], 'barre': 1, 'barre_strings': [0, 1, 4, 5], 'difficulty': 4},
    ],
    'Cm': [
        {'positions': [(0, 3, 1), (1, 3, 1), (2, 5, 3), (3, 5, 4), (4, 4, 2), (5, 3, 1)], 'barre': 3, 'barre_strings': [0, 1, 5], 'difficulty': 4},
    ],
    'Gm': [
        {'positions': [(0, 3, 1), (1, 3, 1), (2, 5, 3), (3, 5, 4), (4, 3, 1), (5, 3, 1)], 'barre': 3, 'barre_strings': [0, 1, 4, 5], 'difficulty': 4},
    ],
    
    # 七和弦
    'C7': [
        {'positions': [(0, -1), (1, 3, 3), (2, 2, 2), (3, 3, 4), (4, 1, 1), (5, 0)], 'barre': None, 'difficulty': 2},
    ],
    'D7': [
        {'positions': [(0, -1), (1, 0), (2, 0), (3, 2, 1), (4, 1, 3), (5, 2, 2)], 'barre': None, 'difficulty': 1},
    ],
    'E7': [
        {'positions': [(0, 0), (1, 2, 2), (2, 0), (3, 1, 1), (4, 0), (5, 0)], 'barre': None, 'difficulty': 1},
    ],
    'G7': [
        {'positions': [(0, 3, 4), (1, 2, 2), (2, 0), (3, 0), (4, 0), (5, 1, 1)], 'barre': None, 'difficulty': 2},
    ],
    'A7': [
        {'positions': [(0, -1), (1, 0), (2, 2, 1), (3, 0), (4, 2, 3), (5, 0)], 'barre': None, 'difficulty': 1},
    ],
    'B7': [
        {'positions': [(0, 2, 2), (1, 0), (2, 2, 1), (3, 1, 3), (4, 2, 4), (5, 2, 2)], 'barre': None, 'difficulty': 2},
    ],
    'F7': [
        {'positions': [(0, 1, 1), (1, 1, 1), (2, 2, 2), (3, 1, 1), (4, 3, 3), (5, 1, 1)], 'barre': 1, 'barre_strings': [0, 1, 3, 5], 'difficulty': 4},
    ],
    
    # 大七和弦
    'Cmaj7': [
        {'positions': [(0, -1), (1, 3, 3), (2, 2, 2), (3, 0), (4, 0), (5, 0)], 'barre': None, 'difficulty': 2},
    ],
    'Dmaj7': [
        {'positions': [(0, -1), (1, 0), (2, 0), (3, 2, 1), (4, 2, 2), (5, 2, 3)], 'barre': None, 'difficulty': 2},
    ],
    'Fmaj7': [
        {'positions': [(0, -1), (1, 0), (2, 2, 2), (3, 3, 3), (4, 3, 4), (5, 0)], 'barre': None, 'difficulty': 2},
    ],
    'Gmaj7': [
        {'positions': [(0, 3, 4), (1, 2, 2), (2, 0), (3, 0), (4, 0), (5, 2, 1)], 'barre': None, 'difficulty': 2},
    ],
    'Amaj7': [
        {'positions': [(0, -1), (1, 0), (2, 2, 1), (3, 1, 3), (4, 2, 4), (5, 0)], 'barre': None, 'difficulty': 2},
    ],
    
    # 小七和弦
    'Am7': [
        {'positions': [(0, 0), (1, 0), (2, 2, 2), (3, 0), (4, 1, 1), (5, 0)], 'barre': None, 'difficulty': 1},
    ],
    'Dm7': [
        {'positions': [(0, -1), (1, 0), (2, 0), (3, 2, 1), (4, 1, 3), (5, 1, 2)], 'barre': None, 'difficulty': 1},
    ],
    'Em7': [
        {'positions': [(0, 0), (1, 2, 2), (2, 0), (3, 0), (4, 0), (5, 0)], 'barre': None, 'difficulty': 1},
    ],
    'Bm7': [
        {'positions': [(0, 2, 1), (1, 2, 1), (2, 4, 3), (3, 2, 2), (4, 3, 4), (5, 2, 1)], 'barre': 2, 'barre_strings': [0, 1, 5], 'difficulty': 3},
    ],
    'Fm7': [
        {'positions': [(0, 1, 1), (1, 1, 1), (2, 3, 2), (3, 1, 1), (4, 1, 1), (5, 1, 1)], 'barre': 1, 'barre_strings': [0, 1, 3, 4, 5], 'difficulty': 4},
    ],
    
    # 挂留和弦
    'Csus2': [
        {'positions': [(0, -1), (1, 3, 3), (2, 0), (3, 0), (4, 1, 1), (5, 0)], 'barre': None, 'difficulty': 2},
    ],
    'Csus4': [
        {'positions': [(0, -1), (1, 3, 3), (2, 3, 4), (3, 0), (4, 1, 1), (5, 0)], 'barre': None, 'difficulty': 2},
    ],
    'Dsus2': [
        {'positions': [(0, -1), (1, 0), (2, 0), (3, 0), (4, 3, 2), (5, 2, 1)], 'barre': None, 'difficulty': 1},
    ],
    'Dsus4': [
        {'positions': [(0, -1), (1, 0), (2, 0), (3, 3, 2), (4, 3, 3), (5, 2, 1)], 'barre': None, 'difficulty': 1},
    ],
    'Gsus4': [
        {'positions': [(0, 3, 4), (1, 3, 3), (2, 0), (3, 0), (4, 0), (5, 3, 1)], 'barre': None, 'difficulty': 2},
    ],
    'Asus2': [
        {'positions': [(0, -1), (1, 0), (2, 2, 1), (3, 2, 2), (4, 0), (5, 0)], 'barre': None, 'difficulty': 1},
    ],
    'Asus4': [
        {'positions': [(0, -1), (1, 0), (2, 2, 1), (3, 2, 2), (4, 3, 3), (5, 0)], 'barre': None, 'difficulty': 1},
    ],
    'Esus4': [
        {'positions': [(0, 0), (1, 2, 2), (2, 2, 3), (3, 2, 4), (4, 0), (5, 0)], 'barre': None, 'difficulty': 1},
    ],
    
    # 增和弦
    'Caug': [
        {'positions': [(0, -1), (1, 3, 3), (2, 2, 2), (3, 1, 1), (4, 1, 4), (5, 0)], 'barre': None, 'difficulty': 3},
    ],
    'Daug': [
        {'positions': [(0, -1), (1, 0), (2, 0), (3, 3, 1), (4, 3, 2), (5, 3, 3)], 'barre': None, 'difficulty': 2},
    ],
    
    # 减和弦
    'Cdim': [
        {'positions': [(0, -1), (1, 3, 3), (2, 2, 2), (3, 1, 1), (4, 2, 4), (5, -1)], 'barre': None, 'difficulty': 3},
    ],
    'Ddim': [
        {'positions': [(0, -1), (1, 0), (2, 0), (3, 1, 1), (4, 0), (5, 1, 2)], 'barre': None, 'difficulty': 2},
    ],
    
    # 半减七和弦（m7b5）
    'Am7b5': [
        {'positions': [(0, 5, 1), (1, 5, 1), (2, 5, 1), (3, 5, 1), (4, 4, 2), (5, 5, 1)], 'barre': 5, 'barre_strings': [0, 1, 2, 3, 5], 'difficulty': 4},
    ],
    'Bm7b5': [
        {'positions': [(0, 6, 1), (1, 6, 1), (2, 6, 1), (3, 6, 1), (4, 5, 2), (5, 6, 1)], 'barre': 6, 'barre_strings': [0, 1, 2, 3, 5], 'difficulty': 4},
    ],
    
    # 添加9和弦
    'Cadd9': [
        {'positions': [(0, -1), (1, 3, 3), (2, 0), (3, 0), (4, 1, 1), (5, 0)], 'barre': None, 'difficulty': 2},
    ],
    'Dadd9': [
        {'positions': [(0, -1), (1, 0), (2, 0), (3, 2, 1), (4, 2, 2), (5, 2, 3)], 'barre': None, 'difficulty': 2},
    ],
    'Gadd9': [
        {'positions': [(0, 3, 4), (1, 0), (2, 0), (3, 0), (4, 0), (5, 3, 1)], 'barre': None, 'difficulty': 2},
    ],
    
    # 更多和弦...
    'Ebm': [
        {'positions': [(0, 6, 1), (1, 6, 1), (2, 8, 3), (3, 8, 4), (4, 7, 2), (5, 6, 1)], 'barre': 6, 'barre_strings': [0, 1, 5], 'difficulty': 4},
    ],
    'Ab': [
        {'positions': [(0, 4, 1), (1, 4, 1), (2, 6, 3), (3, 6, 4), (4, 5, 2), (5, 4, 1)], 'barre': 4, 'barre_strings': [0, 1, 5], 'difficulty': 4},
    ],
    'Abm': [
        {'positions': [(0, 4, 1), (1, 4, 1), (2, 6, 3), (3, 6, 4), (4, 4, 1), (5, 4, 1)], 'barre': 4, 'barre_strings': [0, 1, 4, 5], 'difficulty': 4},
    ],
    'Eb': [
        {'positions': [(0, 6, 1), (1, 6, 1), (2, 8, 3), (3, 8, 4), (4, 8, 4), (5, 6, 1)], 'barre': 6, 'barre_strings': [0, 1, 5], 'difficulty': 4},
    ],
    'Db': [
        {'positions': [(0, 4, 1), (1, 4, 1), (2, 6, 3), (3, 6, 4), (4, 6, 4), (5, 4, 1)], 'barre': 4, 'barre_strings': [0, 1, 5], 'difficulty': 4},
    ],
    'Gb': [
        {'positions': [(0, 2, 1), (1, 2, 1), (2, 4, 3), (3, 4, 4), (4, 4, 4), (5, 2, 1)], 'barre': 2, 'barre_strings': [0, 1, 5], 'difficulty': 3},
    ],
    'Bb': [
        {'positions': [(0, 1, 1), (1, 1, 1), (2, 3, 3), (3, 3, 4), (4, 3, 4), (5, 1, 1)], 'barre': 1, 'barre_strings': [0, 1, 5], 'difficulty': 3},
    ],
    'Bbm': [
        {'positions': [(0, 1, 1), (1, 1, 1), (2, 3, 3), (3, 3, 4), (4, 2, 2), (5, 1, 1)], 'barre': 1, 'barre_strings': [0, 1, 5], 'difficulty': 3},
    ],
    
    # 九和弦
    'C9': [
        {'positions': [(0, -1), (1, 3, 3), (2, 2, 2), (3, 3, 4), (4, 1, 1), (5, 0)], 'barre': None, 'difficulty': 3},
    ],
    'D9': [
        {'positions': [(0, -1), (1, 0), (2, 0), (3, 2, 1), (4, 1, 3), (5, 2, 2)], 'barre': None, 'difficulty': 2},
    ],
    'E9': [
        {'positions': [(0, 0), (1, 2, 2), (2, 1, 1), (3, 1, 3), (4, 0), (5, 0)], 'barre': None, 'difficulty': 2},
    ],
    'G9': [
        {'positions': [(0, 3, 4), (1, 0), (2, 0), (3, 0), (4, 0), (5, 1, 1)], 'barre': None, 'difficulty': 2},
    ],
    
    # 十一和弦
    'C11': [
        {'positions': [(0, -1), (1, 3, 3), (2, 3, 4), (3, 3, 5), (4, 1, 1), (5, 0)], 'barre': None, 'difficulty': 3},
    ],
    
    # 十三和弦  
    'C13': [
        {'positions': [(0, -1), (1, 3, 3), (2, 3, 4), (3, 3, 5), (4, 1, 1), (5, 0)], 'barre': None, 'difficulty': 4},
    ],
    
    # 六和弦
    'C6': [
        {'positions': [(0, -1), (1, 3, 3), (2, 2, 2), (3, 0), (4, 1, 1), (5, 0)], 'barre': None, 'difficulty': 2},
    ],
    'A6': [
        {'positions': [(0, -1), (1, 0), (2, 2, 1), (3, 2, 2), (4, 2, 3), (5, 2, 4)], 'barre': None, 'difficulty': 2},
    ],
    
    # 小六和弦
    'Am6': [
        {'positions': [(0, -1), (1, 0), (2, 2, 2), (3, 2, 3), (4, 1, 1), (5, 2, 4)], 'barre': None, 'difficulty': 2},
    ],
    
    # 强力和弦（Power Chords）
    'C5': [
        {'positions': [(0, -1), (1, 3, 1), (2, 5, 3), (3, 5, 4), (4, -1), (5, -1)], 'barre': None, 'difficulty': 1},
        {'positions': [(0, 8, 1), (1, 10, 3), (2, 10, 4), (3, -1), (4, -1), (5, -1)], 'barre': None, 'difficulty': 1},
    ],
    'D5': [
        {'positions': [(0, -1), (1, 5, 1), (2, 7, 3), (3, 7, 4), (4, -1), (5, -1)], 'barre': None, 'difficulty': 1},
        {'positions': [(0, 10, 1), (1, 12, 3), (2, 12, 4), (3, -1), (4, -1), (5, -1)], 'barre': None, 'difficulty': 1},
    ],
    'E5': [
        {'positions': [(0, 0), (1, 2, 1), (2, 2, 3), (3, 2, 4), (4, 0), (5, 0)], 'barre': None, 'difficulty': 1},
        {'positions': [(0, 7, 1), (1, 9, 3), (2, 9, 4), (3, -1), (4, -1), (5, -1)], 'barre': None, 'difficulty': 1},
    ],
    'G5': [
        {'positions': [(0, 3, 1), (1, 5, 3), (2, 5, 4), (3, -1), (4, -1), (5, 3, 2)], 'barre': None, 'difficulty': 1},
    ],
    'A5': [
        {'positions': [(0, -1), (1, 0), (2, 2, 1), (3, 2, 3), (4, 2, 4), (5, 0)], 'barre': None, 'difficulty': 1},
        {'positions': [(0, 5, 1), (1, 7, 3), (2, 7, 4), (3, -1), (4, -1), (5, -1)], 'barre': None, 'difficulty': 1},
    ],
    'B5': [
        {'positions': [(0, 2, 1), (1, 4, 3), (2, 4, 4), (3, -1), (4, -1), (5, 2, 2)], 'barre': None, 'difficulty': 1},
        {'positions': [(0, 7, 1), (1, 9, 3), (2, 9, 4), (3, -1), (4, -1), (5, 7, 2)], 'barre': None, 'difficulty': 1},
    ],
    'F5': [
        {'positions': [(0, 1, 1), (1, 3, 3), (2, 3, 4), (3, -1), (4, -1), (5, 1, 2)], 'barre': None, 'difficulty': 1},
    ],
}


def _parse_chord_data(chord_data: Dict) -> GuitarChord:
    """解析和弦数据"""
    positions = []
    for pos in chord_data['positions']:
        string = GuitarString(pos[0])
        fret = pos[1]
        finger = pos[2] if len(pos) > 2 else 0
        positions.append(FingerPosition(string=string, fret=fret, finger=finger))
    
    barre = chord_data.get('barre')
    barre_strings = None
    if barre and chord_data.get('barre_strings'):
        barre_strings = [GuitarString(s) for s in chord_data['barre_strings']]
    
    return GuitarChord(
        name='',  # 稍后设置
        positions=positions,
        barre=barre,
        barre_strings=barre_strings,
        difficulty=chord_data.get('difficulty', 1)
    )


def get_chord(name: str, variant: int = 0) -> Optional[GuitarChord]:
    """
    获取和弦指法
    
    Args:
        name: 和弦名称（如 'C', 'Am', 'F#m7'）
        variant: 变体编号（0=默认，1=其他指法）
    
    Returns:
        GuitarChord 对象，找不到返回 None
    
    Examples:
        >>> chord = get_chord('C')
        >>> print(chord.notes)  # ['C', 'E', 'G']
        >>> chord = get_chord('F', variant=1)  # 简化版 F 和弦
    """
    # 处理升号/降号
    normalized_name = name.replace('#', '#').replace('b', 'b')
    
    # 直接查找
    if normalized_name in CHORD_DATABASE:
        variants = CHORD_DATABASE[normalized_name]
        if variant < len(variants):
            chord = _parse_chord_data(variants[variant])
            chord.name = normalized_name
            return chord
    
    return None


def get_all_variants(name: str) -> List[GuitarChord]:
    """
    获取和弦的所有变体
    
    Args:
        name: 和弦名称
    
    Returns:
        所有变体列表
    
    Examples:
        >>> variants = get_all_variants('C')
        >>> print(f"Found {len(variants)} ways to play C")
    """
    normalized_name = name.replace('#', '#').replace('b', 'b')
    
    if normalized_name not in CHORD_DATABASE:
        return []
    
    chords = []
    for i, variant_data in enumerate(CHORD_DATABASE[normalized_name]):
        chord = _parse_chord_data(variant_data)
        chord.name = normalized_name
        chords.append(chord)
    
    return chords


def render_chord_diagram(chord: GuitarChord, 
                         frets_to_show: int = 5,
                         show_finger_numbers: bool = True) -> str:
    """
    渲染和弦图表（ASCII 格式）
    
    Args:
        chord: GuitarChord 对象
        frets_to_show: 显示的品数（默认 5）
        show_finger_numbers: 是否显示手指编号
    
    Returns:
        ASCII 和弦图表字符串
    
    Examples:
        >>> chord = get_chord('C')
        >>> print(render_chord_diagram(chord))
            E A D G B E
            |-|-|-|-|-|
            |-|-|-|-|-|
            |1|-|-|2|-|
            |-|3|-|-|-|
            |-|-|-|-|-|
    """
    # 构建图表
    lines = []
    
    # 标题
    lines.append(f"    {chord.name}")
    lines.append("")
    
    # 琴弦名称
    string_names = "E A D G B E"
    lines.append(f"    {string_names}")
    
    # 确定起始品
    min_fret = 0
    max_fret = 0
    for pos in chord.positions:
        if pos.fret > 0:
            if min_fret == 0 or pos.fret < min_fret:
                min_fret = pos.fret
            if pos.fret > max_fret:
                max_fret = pos.fret
    
    # 如果最高品超过5，需要显示品号
    start_fret = 0
    if max_fret > 5:
        start_fret = min_fret - 1 if min_fret > 1 else 1
    
    # 横按标记
    if chord.barre and chord.barre >= start_fret:
        barre_line = "    "
        for string in [GuitarString.E6, GuitarString.A5, GuitarString.D4, 
                       GuitarString.G3, GuitarString.B2, GuitarString.E1]:
            if chord.barre_strings and string in chord.barre_strings:
                barre_line += "="
            else:
                barre_line += "|"
        lines.append(barre_line)
    
    # 绘制品格
    for fret_num in range(start_fret, start_fret + frets_to_show):
        line = ""
        
        # 品号标记（第5品以上）
        if fret_num > 0:
            if fret_num == start_fret:
                line = f"{fret_num:>2}  "
            else:
                line = "    "
        else:
            line = "    "
        
        # 绘制各弦位置
        for string in [GuitarString.E6, GuitarString.A5, GuitarString.D4,
                       GuitarString.G3, GuitarString.B2, GuitarString.E1]:
            # 查找该弦的指法
            pos_on_string = None
            for pos in chord.positions:
                if pos.string == string:
                    pos_on_string = pos
                    break
            
            # 横按情况
            if chord.barre and chord.barre == fret_num and chord.barre_strings:
                if string in chord.barre_strings:
                    if show_finger_numbers:
                        line += str(chord.positions[0].finger) if chord.positions else "1"
                    else:
                        line += "="
                    continue
            
            if pos_on_string:
                if pos_on_string.fret == fret_num:
                    # 按弦位置
                    if show_finger_numbers and pos_on_string.finger > 0:
                        line += str(pos_on_string.finger)
                    else:
                        line += "*"
                elif pos_on_string.fret == -1:
                    # 闷音
                    if fret_num == start_fret:
                        line += "X"
                    else:
                        line += "|"
                elif pos_on_string.fret == 0 and fret_num == start_fret:
                    # 空弦
                    line += "O"
                elif fret_num == start_fret and pos_on_string.fret > fret_num:
                    # 该品没有按弦但弦被按在更高品
                    line += "|"
                else:
                    line += "|"
            else:
                # 默认空弦（在第0品）
                if fret_num == start_fret:
                    line += "O"
                else:
                    line += "|"
        
        lines.append(line)
    
    # 音符说明
    if chord.notes:
        lines.append("")
        lines.append(f"    Notes: {', '.join(chord.notes)}")
    
    return '\n'.join(lines)


def render_chord_grid(chord: GuitarChord, width: int = 6, height: int = 5) -> str:
    """
    渲染和弦网格图（紧凑格式）
    
    Args:
        chord: GuitarChord 对象
        width: 网格宽度（品数）
        height: 网格高度
    
    Returns:
        紧凑的和弦网格字符串
    """
    # 简化的紧凑图表
    lines = []
    lines.append(f"[{chord.name}]")
    
    # 顶行：空弦标记
    top_row = ""
    for string in [GuitarString.E6, GuitarString.A5, GuitarString.D4,
                   GuitarString.G3, GuitarString.B2, GuitarString.E1]:
        pos_on_string = None
        for pos in chord.positions:
            if pos.string == string:
                pos_on_string = pos
                break
        
        if pos_on_string and pos_on_string.fret == -1:
            top_row += "x"
        elif pos_on_string and pos_on_string.fret == 0:
            top_row += "o"
        elif pos_on_string is None:
            top_row += "o"
        else:
            top_row += "-"
    
    lines.append(top_row)
    
    # 品格行
    for fret in range(1, height + 1):
        row = ""
        for string in [GuitarString.E6, GuitarString.A5, GuitarString.D4,
                       GuitarString.G3, GuitarString.B2, GuitarString.E1]:
            pos_on_string = None
            for pos in chord.positions:
                if pos.string == string:
                    pos_on_string = pos
                    break
            
            # 横按
            if chord.barre and chord.barre == fret:
                if chord.barre_strings and string in chord.barre_strings:
                    row += str(chord.positions[0].finger) if chord.positions else "1"
                    continue
            
            if pos_on_string and pos_on_string.fret == fret:
                row += str(pos_on_string.finger) if pos_on_string.finger > 0 else "*"
            else:
                row += "-"
        
        lines.append(row)
    
    return '\n'.join(lines)


def get_note_on_fretboard(string: GuitarString, fret: int) -> str:
    """
    获取指板指定位置的音符
    
    Args:
        string: 弦
        fret: 品数
    
    Returns:
        音符名称
    
    Examples:
        >>> get_note_on_fretboard(GuitarString.E6, 1)  # 'F'
        >>> get_note_on_fretboard(GuitarString.A5, 2)  # 'B'
    """
    open_note = STRING_OPEN_NOTES[string]
    open_index = NOTE_CHROMATIC.index(open_note) if open_note in NOTE_CHROMATIC else 0
    note_index = (open_index + fret) % 12
    return NOTE_CHROMATIC[note_index]


def get_note_positions_on_fretboard(note: str, 
                                    max_fret: int = 12) -> List[Tuple[GuitarString, int]]:
    """
    查找音符在指板上的所有位置
    
    Args:
        note: 音符名称（如 'C', 'G#'）
        max_fret: 最高品数
    
    Returns:
        位置列表 [(弦, 品数), ...]
    
    Examples:
        >>> positions = get_note_positions_on_fretboard('C')
        >>> for string, fret in positions:
        ...     print(f"{STRING_OPEN_NOTES[string]}弦 {fret}品")
    """
    positions = []
    
    for string in GuitarString:
        open_note = STRING_OPEN_NOTES[string]
        open_index = NOTE_CHROMATIC.index(open_note) if open_note in NOTE_CHROMATIC else 0
        
        target_note = note.upper().replace('B', 'b') if 'B' in note.upper() and len(note) > 1 else note.upper()
        if target_note not in NOTE_CHROMATIC:
            # 尝试降号表示
            if target_note in NOTE_CHROMATIC_FLAT:
                target_index = NOTE_CHROMATIC_FLAT.index(target_note)
            else:
                continue
        else:
            target_index = NOTE_CHROMATIC.index(target_note)
        
        # 计算品格
        fret = (target_index - open_index) % 12
        if fret <= max_fret:
            positions.append((string, fret))
        
        # 超过12品的位置（同一音符的高八度）
        if fret + 12 <= max_fret:
            positions.append((string, fret + 12))
    
    return positions


def calculate_chord_difficulty(chord: GuitarChord) -> Dict[str, any]:
    """
    计算和弦难度评分
    
    Args:
        chord: GuitarChord 对象
    
    Returns:
        难度评估详情
    
    Examples:
        >>> chord = get_chord('F')
        >>> diff = calculate_chord_difficulty(chord)
        >>> print(f"Overall difficulty: {diff['overall']}/5")
    """
    factors = {
        'barre': 0,
        'stretch': 0,
        'finger_count': 0,
        'unusual_positions': 0,
    }
    
    # 横按难度
    if chord.barre:
        if chord.barre == 1:
            factors['barre'] = 3  # F 和弦横按很难
        elif chord.barre <= 2:
            factors['barre'] = 2
        else:
            factors['barre'] = 1
        
        # 横按弦数
        if chord.barre_strings:
            barre_count = len(chord.barre_strings)
            if barre_count >= 5:
                factors['barre'] += 1
    
    # 手指数量
    finger_count = sum(1 for pos in chord.positions if pos.finger > 0)
    factors['finger_count'] = min(finger_count - 1, 2) if finger_count > 1 else 0
    
    # 手指伸展
    frets = [pos.fret for pos in chord.positions if pos.fret > 0]
    if frets:
        fret_range = max(frets) - min(frets)
        if fret_range >= 4:
            factors['stretch'] = 2
        elif fret_range >= 3:
            factors['stretch'] = 1
    
    # 计算总分
    total = sum(factors.values())
    overall = min(5, max(1, total + 1))
    
    return {
        'overall': overall,
        'level': ChordDifficulty(overall).name,
        'factors': factors,
        'recommendation': _get_difficulty_recommendation(overall),
    }


def _get_difficulty_recommendation(difficulty: int) -> str:
    """获取难度建议"""
    recommendations = {
        1: "适合初学者，可以立即学习",
        2: "基础和弦，练习几周后可掌握",
        3: "中等难度，需要一定基础",
        4: "进阶和弦，建议先练习相关基础和弦",
        5: "高级和弦，适合有经验的演奏者",
    }
    return recommendations.get(difficulty, "未知难度")


def suggest_alternative_chords(chord_name: str, 
                               max_difficulty: int = 3) -> List[GuitarChord]:
    """
    建议替代和弦（更简单的指法）
    
    Args:
        chord_name: 目标和弦名称
        max_difficulty: 最大难度
    
    Returns:
        替代和弦列表
    
    Examples:
        >>> alternatives = suggest_alternative_chords('F', max_difficulty=2)
        >>> for alt in alternatives:
        ...     print(f"{alt.name} (difficulty {alt.difficulty})")
    """
    chord = get_chord(chord_name)
    if not chord:
        return []
    
    # 如果当前和弦已经足够简单，返回自身
    if chord.difficulty <= max_difficulty:
        return [chord]
    
    # 查找所有变体
    variants = get_all_variants(chord_name)
    alternatives = [v for v in variants if v.difficulty <= max_difficulty]
    
    return alternatives


def generate_practice_sequence(chords: List[str], 
                               include_alternatives: bool = True) -> Dict[str, any]:
    """
    生成练习序列
    
    Args:
        chords: 和弦名称列表
        include_alternatives: 是否包含替代和弦
    
    Returns:
        练习计划
    
    Examples:
        >>> seq = generate_practice_sequence(['C', 'Am', 'F', 'G'])
        >>> print(f"Total difficulty: {seq['total_difficulty']}")
    """
    sequence = {
        'chords': [],
        'total_difficulty': 0,
        'transitions': [],
        'suggestions': [],
    }
    
    prev_chord = None
    
    for name in chords:
        chord = get_chord(name)
        if not chord:
            sequence['suggestions'].append(f"未找到和弦: {name}")
            continue
        
        difficulty = calculate_chord_difficulty(chord)
        sequence['chords'].append({
            'name': name,
            'chord': chord,
            'difficulty': difficulty['overall'],
            'diagram': render_chord_grid(chord),
        })
        sequence['total_difficulty'] += difficulty['overall']
        
        # 计算转换
        if prev_chord:
            transition = _analyze_transition(prev_chord, chord)
            sequence['transitions'].append(transition)
        
        prev_chord = chord
        
        # 替代建议
        if include_alternatives and difficulty['overall'] > 2:
            alternatives = suggest_alternative_chords(name)
            if alternatives:
                sequence['suggestions'].append(
                    f"可以用简化版 {name} 练习（难度降低）"
                )
    
    # 练习建议
    avg_difficulty = sequence['total_difficulty'] / len(sequence['chords']) if sequence['chords'] else 0
    if avg_difficulty <= 2:
        sequence['practice_time'] = "建议练习 10-15 分钟"
    elif avg_difficulty <= 3:
        sequence['practice_time'] = "建议练习 20-30 分钟"
    else:
        sequence['practice_time'] = "建议练习 30-45 分钟"
    
    return sequence


def _analyze_transition(from_chord: GuitarChord, 
                        to_chord: GuitarChord) -> Dict[str, any]:
    """分析和弦转换"""
    # 计算手指移动
    moves = []
    
    for from_pos in from_chord.positions:
        if from_pos.finger == 0:
            continue
        
        # 查找同一手指在新和弦的位置
        for to_pos in to_chord.positions:
            if to_pos.finger == from_pos.finger:
                if from_pos.string != to_pos.string or from_pos.fret != to_pos.fret:
                    moves.append({
                        'finger': from_pos.finger,
                        'from': f"{STRING_OPEN_NOTES[from_pos.string]}弦{from_pos.fret}品",
                        'to': f"{STRING_OPEN_NOTES[to_pos.string]}弦{to_pos.fret}品",
                        'distance': abs(from_pos.fret - to_pos.fret),
                    })
    
    # 计算转换难度
    total_distance = sum(m['distance'] for m in moves)
    transition_difficulty = min(5, max(1, len(moves) + total_distance // 2))
    
    return {
        'from': from_chord.name,
        'to': to_chord.name,
        'moves': moves,
        'difficulty': transition_difficulty,
    }


def find_chords_by_notes(notes: List[str]) -> List[Dict[str, any]]:
    """
    根据音符查找可能的和弦
    
    Args:
        notes: 音符列表
    
    Returns:
        匹配的和弦列表
    
    Examples:
        >>> find_chords_by_notes(['C', 'E', 'G'])  # 找 C 和弦
    """
    matching_chords = []
    
    # 标准化音符
    normalized_notes = set(n.upper().replace('#', '#') for n in notes)
    
    for chord_name in CHORD_DATABASE:
        for variant_idx, variant_data in enumerate(CHORD_DATABASE[chord_name]):
            chord = get_chord(chord_name, variant_idx)
            if chord:
                chord_notes = set(chord.notes)
                
                # 计算匹配度
                common = normalized_notes & chord_notes
                if common:
                    match_ratio = len(common) / len(normalized_notes)
                    matching_chords.append({
                        'name': chord_name,
                        'variant': variant_idx,
                        'chord': chord,
                        'matching_notes': list(common),
                        'match_ratio': round(match_ratio, 2),
                        'all_notes': chord.notes,
                    })
    
    # 按匹配度排序
    matching_chords.sort(key=lambda x: x['match_ratio'], reverse=True)
    
    return matching_chords


def get_scale_chords(root: str, scale_type: str = 'major') -> List[Dict[str, any]]:
    """
    获取调内和弦
    
    Args:
        root: 根音
        scale_type: 音阶类型（'major', 'minor'）
    
    Returns:
        调内和弦列表
    
    Examples:
        >>> chords = get_scale_chords('C', 'major')
        >>> for c in chords:
        ...     print(f"{c['degree']}: {c['chord_name']}")
    """
    # 大调调内和弦级数
    major_degrees = ['I', 'ii', 'iii', 'IV', 'V', 'vi', 'vii°']
    major_chord_types = ['', 'm', 'm', '', '', 'm', 'dim']
    major_intervals = [0, 2, 4, 5, 7, 9, 11]
    
    # 小调调内和弦级数
    minor_degrees = ['i', 'ii°', 'III', 'iv', 'v', 'VI', 'VII']
    minor_chord_types = ['m', 'dim', '', 'm', 'm', '', '']
    minor_intervals = [0, 2, 3, 5, 7, 8, 10]
    
    root_index = NOTE_CHROMATIC.index(root.upper()) if root.upper() in NOTE_CHROMATIC else 0
    
    degrees = major_degrees if scale_type == 'major' else minor_degrees
    chord_types = major_chord_types if scale_type == 'major' else minor_chord_types
    intervals = major_intervals if scale_type == 'major' else minor_intervals
    
    chords = []
    
    for i, interval in enumerate(intervals):
        note_index = (root_index + interval) % 12
        note = NOTE_CHROMATIC[note_index]
        chord_name = note + chord_types[i]
        
        chord = get_chord(chord_name)
        if chord:
            chords.append({
                'degree': degrees[i],
                'chord_name': chord_name,
                'chord': chord,
                'notes': chord.notes,
            })
        else:
            chords.append({
                'degree': degrees[i],
                'chord_name': chord_name,
                'chord': None,
                'notes': [],
            })
    
    return chords


def generate_fretboard_map(start_fret: int = 0, 
                           end_fret: int = 12) -> str:
    """
    生成指板音符映射图
    
    Args:
        start_fret: 起始品
        end_fret: 结束品
    
    Returns:
        指板图字符串
    
    Examples:
        >>> print(generate_fretboard_map(0, 12))
    """
    lines = []
    
    # 琴弦名称标题
    header = "     " + " ".join(f"{STRING_OPEN_NOTES[s]:>3}" for s in GuitarString)
    lines.append(header)
    
    # 品号行
    fret_numbers = "Fret " + " ".join(f"{f:>3}" for f in range(start_fret, end_fret + 1))
    lines.append(fret_numbers)
    
    # 分隔线
    separator = "-----" + "-" * (4 * (end_fret - start_fret + 1))
    lines.append(separator)
    
    # 每弦音符
    for string in GuitarString:
        row = f"{STRING_OPEN_NOTES[string]:>3}  "
        for fret in range(start_fret, end_fret + 1):
            note = get_note_on_fretboard(string, fret)
            row += f"{note:>3} "
        lines.append(row)
    
    return '\n'.join(lines)


def transpose_chord(chord_name: str, semitones: int) -> str:
    """
    移调和弦
    
    Args:
        chord_name: 和弦名称
        semitones: 移调半音数
    
    Returns:
        移调后的和弦名称
    
    Examples:
        >>> transpose_chord('C', 2)  # 'D'
        >>> transpose_chord('Am', -1)  # 'G#m'
    """
    # 解析和弦名称
    base_note = chord_name[0].upper()
    modifier = ""
    
    if len(chord_name) > 1:
        if chord_name[1] == '#':
            base_note = chord_name[:2]
            modifier = chord_name[2:]
        elif chord_name[1] == 'b':
            base_note = chord_name[:2]
            modifier = chord_name[2:]
        else:
            modifier = chord_name[1:]
    
    # 找到音符位置
    if base_note in NOTE_CHROMATIC:
        note_index = NOTE_CHROMATIC.index(base_note)
    elif base_note in NOTE_CHROMATIC_FLAT:
        note_index = NOTE_CHROMATIC_FLAT.index(base_note)
    else:
        return chord_name
    
    # 移调
    new_index = (note_index + semitones) % 12
    new_note = NOTE_CHROMATIC[new_index]
    
    return new_note + modifier


def get_chord_progressions(key: str) -> List[List[str]]:
    """
    获取常用和弦进行
    
    Args:
        key: 调性（如 'C', 'G'）
    
    Returns:
        常用和弦进行列表
    
    Examples:
        >>> progressions = get_chord_progressions('C')
        >>> for prog in progressions:
        ...     print(" - ".join(prog))
    """
    # 常用进行模板（级数表示）
    common_progressions = [
        ['I', 'V', 'vi', 'IV'],        # 流行进行
        ['I', 'IV', 'V', 'I'],         # 经典进行
        ['I', 'vi', 'IV', 'V'],        # 另一种流行进行
        ['ii', 'V', 'I'],              # 爵士进行
        ['I', 'V', 'vi', 'iii', 'IV', 'I', 'IV', 'V'],  # Canon 进行
        ['vi', 'IV', 'I', 'V'],        # 小调起始
        ['I', 'bVII', 'bVI', 'V'],     # 摇滚进行
        ['I', 'IV', 'I', 'V'],         # 简单进行
    ]
    
    # 获取调内和弦
    scale_chords = get_scale_chords(key, 'major')
    
    # 将级数转换为和弦名
    progressions = []
    
    for template in common_progressions:
        prog = []
        for degree in template:
            # 匹配级数
            matching = None
            for chord_info in scale_chords:
                if chord_info['degree'] == degree:
                    matching = chord_info['chord_name']
                    break
                # 处理降号级数（简化）- 例如 bVII = 降VII级
                if degree.startswith('b'):
                    # 计算移调半音数
                    degree_num_map = {'I': 0, 'II': 2, 'III': 4, 'IV': 5, 
                                      'V': 7, 'VI': 9, 'VII': 11}
                    degree_base = degree[1:]  # 去掉 b 前缀
                    if degree_base in degree_num_map:
                        base_interval = degree_num_map[degree_base]
                        transposed = transpose_chord(key, base_interval - 1)
                        matching = transposed
                    break
            
            if matching:
                prog.append(matching)
            else:
                prog.append(degree)  # 无法转换，保留原样
        
        progressions.append(prog)
    
    return progressions


def list_all_chords() -> List[str]:
    """
    列出所有可用和弦
    
    Returns:
        和弦名称列表
    
    Examples:
        >>> chords = list_all_chords()
        >>> print(f"Total: {len(chords)} chords")
    """
    return sorted(CHORD_DATABASE.keys())


def get_finger_strength_exercises() -> List[Dict[str, any]]:
    """
    获取手指力量练习建议
    
    Returns:
        练习列表
    
    Examples:
        >>> exercises = get_finger_strength_exercises()
        >>> for ex in exercises:
        ...     print(f"{ex['name']}: {ex['description']}")
    """
    return [
        {
            'name': '半音阶练习',
            'description': '1-2-3-4 指法，从第6弦到第1弦，逐品移动',
            'pattern': '1-2-3-4',
            'strings': 'E6 -> E1',
            'duration': '5分钟',
        },
        {
            'name': '蜘蛛练习',
            'description': '保持手指按压，逐弦移动',
            'pattern': '交叉移动',
            'strings': '交替',
            'duration': '3分钟',
        },
        {
            'name': '横按练习',
            'description': 'F 和弦横按，保持10秒，放松，重复',
            'chords': ['F', 'Bm', 'Cm'],
            'duration': '5分钟',
        },
        {
            'name': '和弦转换练习',
            'description': 'C-Am-F-G 循环转换',
            'chords': ['C', 'Am', 'F', 'G'],
            'duration': '10分钟',
        },
        {
            'name': '伸展练习',
            'description': '大跨度指法练习',
            'pattern': '1-4 大跨度',
            'duration': '3分钟',
        },
    ]


def calculate_chord_inversions(chord_name: str, 
                               inversion: int) -> Optional[GuitarChord]:
    """
    计算和弦转位的指法
    
    Args:
        chord_name: 和弦名称
        inversion: 转位次数（1=第一转位，2=第二转位）
    
    Returns:
        转位和弦指法
    
    Examples:
        >>> inv = calculate_chord_inversions('C', 1)  # C/E 第一转位
    """
    chord = get_chord(chord_name)
    if not chord or len(chord.notes) < 3:
        return None
    
    # 转位意味着改变最低音
    notes = chord.notes.copy()
    
    for _ in range(inversion):
        if len(notes) > 0:
            # 将最低音移到最高
            notes = notes[1:] + [notes[0]]
    
    # 根据转位音符查找可能的指法
    inversions = find_chords_by_notes(notes)
    
    if inversions:
        # 返回最佳匹配
        best = inversions[0]
        return best.get('chord')
    
    return None


# 导出所有公共函数和类
__all__ = [
    'GuitarString',
    'FingerPosition',
    'GuitarChord',
    'ChordDifficulty',
    'STRING_OPEN_NOTES',
    'NOTE_CHROMATIC',
    'NOTE_CHROMATIC_FLAT',
    'CHORD_DATABASE',
    'get_chord',
    'get_all_variants',
    'render_chord_diagram',
    'render_chord_grid',
    'get_note_on_fretboard',
    'get_note_positions_on_fretboard',
    'calculate_chord_difficulty',
    'suggest_alternative_chords',
    'generate_practice_sequence',
    'find_chords_by_notes',
    'get_scale_chords',
    'generate_fretboard_map',
    'transpose_chord',
    'get_chord_progressions',
    'list_all_chords',
    'get_finger_strength_exercises',
    'calculate_chord_inversions',
]