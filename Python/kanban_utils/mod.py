"""
Kanban Board Utilities - 看板工具库

功能:
- 看板状态管理 (创建、移动、归档卡片)
- 列管理 (带 WIP 限制)
- 流程指标 (周期时间、交付时间)
- 瓶颈检测
- 累积流图数据生成
- 统计分析

零依赖，纯 Python 标准库实现
"""

from dataclasses import dataclass, field
from typing import Optional, Callable, List, Dict, Any
from datetime import datetime, timedelta
from collections import defaultdict
from enum import Enum
import json


# Python 3.6 兼容的 ISO 格式日期解析
def _parse_iso_datetime(s: str) -> datetime:
    """解析 ISO 格式日期字符串（兼容 Python 3.6）"""
    if not s:
        return None
    # 处理带时区的格式
    if '+' in s or s.endswith('Z'):
        s = s.replace('Z', '+00:00')
        # 简化处理：移除时区部分
        if '+' in s:
            s = s.split('+')[0]
    # 处理微秒
    if '.' in s:
        parts = s.split('.')
        base = parts[0]
        micros = parts[1][:6]  # 取前 6 位
        s = f"{base}.{micros}"
        return datetime.strptime(s, '%Y-%m-%dT%H:%M:%S.%f')
    else:
        return datetime.strptime(s, '%Y-%m-%dT%H:%M:%S')


class CardStatus(Enum):
    """卡片状态"""
    ACTIVE = "active"
    BLOCKED = "blocked"
    ARCHIVED = "archived"


@dataclass
class Card:
    """看板卡片"""
    id: str
    title: str
    column: str
    created_at: datetime = field(default_factory=datetime.now)
    moved_at: Optional[datetime] = None
    status: CardStatus = CardStatus.ACTIVE
    priority: int = 0  # 0=普通, 1=高, 2=紧急
    blocked_reason: Optional[str] = None
    blocked_at: Optional[datetime] = None
    tags: List[str] = field(default_factory=list)
    custom_fields: Dict[str, Any] = field(default_factory=dict)
    history: List[tuple] = field(default_factory=list)  # [(column, moved_at), ...]
    
    def __post_init__(self):
        """初始化历史记录"""
        if not self.history:
            self.history = [(self.column, self.created_at)]
    
    def move_to(self, column: str, timestamp: Optional[datetime] = None) -> None:
        """移动卡片到新列"""
        timestamp = timestamp or datetime.now()
        self.column = column
        self.moved_at = timestamp
        self.history.append((column, timestamp))
    
    def block(self, reason: str, timestamp: Optional[datetime] = None) -> None:
        """阻塞卡片"""
        self.status = CardStatus.BLOCKED
        self.blocked_reason = reason
        self.blocked_at = timestamp or datetime.now()
    
    def unblock(self, timestamp: Optional[datetime] = None) -> None:
        """解除阻塞"""
        self.status = CardStatus.ACTIVE
        self.blocked_reason = None
        self.blocked_at = None
    
    def archive(self, timestamp: Optional[datetime] = None) -> None:
        """归档卡片"""
        self.status = CardStatus.ARCHIVED
        self.moved_at = timestamp or datetime.now()
    
    def time_in_column(self, column: str) -> timedelta:
        """计算在指定列的停留时间"""
        total_time = timedelta()
        entry_time = None
        
        for i, (col, time) in enumerate(self.history):
            if col == column and entry_time is None:
                entry_time = time
            elif entry_time is not None and col != column:
                total_time += time - entry_time
                entry_time = None
        
        # 如果当前还在该列
        if entry_time is not None and self.column == column:
            total_time += datetime.now() - entry_time
        
        return total_time
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            'id': self.id,
            'title': self.title,
            'column': self.column,
            'created_at': self.created_at.isoformat(),
            'moved_at': self.moved_at.isoformat() if self.moved_at else None,
            'status': self.status.value,
            'priority': self.priority,
            'blocked_reason': self.blocked_reason,
            'blocked_at': self.blocked_at.isoformat() if self.blocked_at else None,
            'tags': self.tags,
            'custom_fields': self.custom_fields,
            'history': [(col, ts.isoformat()) for col, ts in self.history]
        }


@dataclass
class Column:
    """看板列"""
    name: str
    wip_limit: int = 0  # 0 表示无限制
    order: int = 0
    is_start: bool = False
    is_end: bool = False
    _cards: Dict[str, Card] = field(default_factory=dict, repr=False)
    
    def add_card(self, card: Card) -> None:
        """添加卡片"""
        self._cards[card.id] = card
    
    def remove_card(self, card_id: str) -> Optional[Card]:
        """移除卡片"""
        return self._cards.pop(card_id, None)
    
    def get_cards(self, include_archived: bool = False) -> List[Card]:
        """获取列中的卡片"""
        if include_archived:
            return list(self._cards.values())
        return [c for c in self._cards.values() if c.status != CardStatus.ARCHIVED]
    
    def count(self, include_archived: bool = False) -> int:
        """统计卡片数量"""
        return len(self.get_cards(include_archived))
    
    def is_over_wip(self) -> bool:
        """是否超过 WIP 限制"""
        if self.wip_limit == 0:
            return False
        return self.count() > self.wip_limit
    
    def wip_remaining(self) -> int:
        """剩余 WIP 容量"""
        if self.wip_limit == 0:
            return float('inf')
        return max(0, self.wip_limit - self.count())
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            'name': self.name,
            'wip_limit': self.wip_limit,
            'order': self.order,
            'is_start': self.is_start,
            'is_end': self.is_end,
            'card_count': self.count()
        }


class KanbanBoard:
    """看板管理器"""
    
    def __init__(self, name: str = "Default Board"):
        self.name = name
        self._columns: Dict[str, Column] = {}
        self._cards: Dict[str, Card] = {}
        self._column_order: List[str] = []
        self._created_at = datetime.now()
    
    # ==================== 列管理 ====================
    
    def add_column(self, name: str, wip_limit: int = 0, 
                   is_start: bool = False, is_end: bool = False) -> Column:
        """添加列"""
        if name in self._columns:
            raise ValueError(f"Column '{name}' already exists")
        
        column = Column(
            name=name,
            wip_limit=wip_limit,
            order=len(self._column_order),
            is_start=is_start,
            is_end=is_end
        )
        self._columns[name] = column
        self._column_order.append(name)
        return column
    
    def remove_column(self, name: str) -> bool:
        """移除列（卡片会被归档）"""
        if name not in self._columns:
            return False
        
        # 归档该列的所有卡片
        column = self._columns[name]
        for card in column.get_cards():
            card.archive()
        
        del self._columns[name]
        self._column_order.remove(name)
        return True
    
    def get_column(self, name: str) -> Optional[Column]:
        """获取列"""
        return self._columns.get(name)
    
    def get_columns(self) -> List[Column]:
        """获取所有列（按顺序）"""
        return [self._columns[name] for name in self._column_order]
    
    def set_wip_limit(self, column_name: str, limit: int) -> bool:
        """设置 WIP 限制"""
        column = self.get_column(column_name)
        if column:
            column.wip_limit = limit
            return True
        return False
    
    def get_start_column(self) -> Optional[Column]:
        """获取起始列"""
        for column in self._columns.values():
            if column.is_start:
                return column
        # 默认返回第一列
        if self._column_order:
            return self._columns[self._column_order[0]]
        return None
    
    def get_end_column(self) -> Optional[Column]:
        """获取终点列"""
        for column in self._columns.values():
            if column.is_end:
                return column
        # 默认返回最后一列
        if self._column_order:
            return self._columns[self._column_order[-1]]
        return None
    
    # ==================== 卡片管理 ====================
    
    def add_card(self, card_id: str, title: str, column: str,
                 priority: int = 0, tags: List[str] = None,
                 custom_fields: Dict[str, Any] = None) -> Card:
        """添加卡片"""
        if card_id in self._cards:
            raise ValueError(f"Card '{card_id}' already exists")
        if column not in self._columns:
            raise ValueError(f"Column '{column}' does not exist")
        
        card = Card(
            id=card_id,
            title=title,
            column=column,
            priority=priority,
            tags=tags or [],
            custom_fields=custom_fields or {}
        )
        
        self._cards[card_id] = card
        self._columns[column].add_card(card)
        return card
    
    def get_card(self, card_id: str) -> Optional[Card]:
        """获取卡片"""
        return self._cards.get(card_id)
    
    def move_card(self, card_id: str, to_column: str,
                  timestamp: Optional[datetime] = None) -> bool:
        """移动卡片"""
        card = self.get_card(card_id)
        if not card:
            return False
        if to_column not in self._columns:
            return False
        
        old_column = card.column
        if old_column == to_column:
            return True
        
        # 从旧列移除
        self._columns[old_column].remove_card(card_id)
        
        # 移动卡片
        card.move_to(to_column, timestamp)
        
        # 添加到新列
        self._columns[to_column].add_card(card)
        return True
    
    def block_card(self, card_id: str, reason: str,
                   timestamp: Optional[datetime] = None) -> bool:
        """阻塞卡片"""
        card = self.get_card(card_id)
        if card:
            card.block(reason, timestamp)
            return True
        return False
    
    def unblock_card(self, card_id: str,
                     timestamp: Optional[datetime] = None) -> bool:
        """解除阻塞"""
        card = self.get_card(card_id)
        if card:
            card.unblock(timestamp)
            return True
        return False
    
    def archive_card(self, card_id: str,
                     timestamp: Optional[datetime] = None) -> bool:
        """归档卡片"""
        card = self.get_card(card_id)
        if card:
            card.archive(timestamp)
            return True
        return False
    
    def delete_card(self, card_id: str) -> bool:
        """删除卡片"""
        card = self._cards.pop(card_id, None)
        if card:
            self._columns[card.column].remove_card(card_id)
            return True
        return False
    
    def get_cards_by_column(self, column: str, 
                            include_archived: bool = False) -> List[Card]:
        """获取指定列的卡片"""
        col = self.get_column(column)
        if col:
            return col.get_cards(include_archived)
        return []
    
    def get_all_cards(self, include_archived: bool = False) -> List[Card]:
        """获取所有卡片"""
        if include_archived:
            return list(self._cards.values())
        return [c for c in self._cards.values() if c.status != CardStatus.ARCHIVED]
    
    def get_blocked_cards(self) -> List[Card]:
        """获取所有被阻塞的卡片"""
        return [c for c in self._cards.values() if c.status == CardStatus.BLOCKED]
    
    def get_cards_by_tag(self, tag: str) -> List[Card]:
        """按标签获取卡片"""
        return [c for c in self._cards.values() if tag in c.tags]
    
    def get_cards_by_priority(self, priority: int) -> List[Card]:
        """按优先级获取卡片"""
        return [c for c in self._cards.values() if c.priority == priority]
    
    # ==================== 统计分析 ====================
    
    def get_column_counts(self) -> Dict[str, int]:
        """获取每列的卡片数量"""
        return {name: col.count() for name, col in self._columns.items()}
    
    def get_wip_status(self) -> Dict[str, Dict[str, Any]]:
        """获取 WIP 状态"""
        result = {}
        for name, column in self._columns.items():
            result[name] = {
                'count': column.count(),
                'limit': column.wip_limit,
                'is_over': column.is_over_wip(),
                'remaining': column.wip_remaining()
            }
        return result
    
    def detect_bottlenecks(self) -> List[Dict[str, Any]]:
        """检测瓶颈列"""
        bottlenecks = []
        avg_count = len(self._cards) / max(len(self._columns), 1)
        
        for name, column in self._columns.items():
            count = column.count()
            if count > avg_count * 1.5:  # 超过平均值 50%
                bottlenecks.append({
                    'column': name,
                    'count': count,
                    'average': avg_count,
                    'ratio': count / max(avg_count, 1),
                    'is_wip_violation': column.is_over_wip()
                })
        
        return sorted(bottlenecks, key=lambda x: x['ratio'], reverse=True)
    
    def calculate_cycle_time(self, card_id: str, 
                             start_column: str = None,
                             end_column: str = None) -> Optional[timedelta]:
        """计算周期时间（从开始列到结束列）"""
        card = self.get_card(card_id)
        if not card:
            return None
        
        start_col = start_column or self.get_start_column()
        end_col = end_column or self.get_end_column()
        
        if not start_col or not end_col:
            return None
        
        start_name = start_col.name if isinstance(start_col, Column) else start_col
        end_name = end_col.name if isinstance(end_col, Column) else end_col
        
        start_time = None
        end_time = None
        
        for col, time in card.history:
            if col == start_name and start_time is None:
                start_time = time
            if col == end_name and start_time is not None:
                end_time = time
                break
        
        if start_time and end_time:
            return end_time - start_time
        return None
    
    def calculate_lead_time(self, card_id: str,
                            end_column: str = None) -> Optional[timedelta]:
        """计算交付时间（从创建到结束列）"""
        card = self.get_card(card_id)
        if not card:
            return None
        
        end_col = end_column or self.get_end_column()
        if not end_col:
            return None
        
        end_name = end_col.name if isinstance(end_col, Column) else end_col
        
        end_time = None
        for col, time in card.history:
            if col == end_name:
                end_time = time
                break
        
        if end_time:
            return end_time - card.created_at
        return None
    
    def get_flow_metrics(self) -> Dict[str, Any]:
        """获取流程指标"""
        completed_cards = [
            c for c in self._cards.values()
            if c.status == CardStatus.ARCHIVED or
               (self.get_end_column() and c.column == self.get_end_column().name)
        ]
        
        cycle_times = []
        lead_times = []
        
        for card in completed_cards:
            ct = self.calculate_cycle_time(card.id)
            lt = self.calculate_lead_time(card.id)
            if ct:
                cycle_times.append(ct.total_seconds() / 3600)  # 小时
            if lt:
                lead_times.append(lt.total_seconds() / 3600)
        
        def percentile(data, p):
            if not data:
                return 0
            sorted_data = sorted(data)
            idx = int(len(sorted_data) * p / 100)
            return sorted_data[min(idx, len(sorted_data) - 1)]
        
        return {
            'total_cards': len(self._cards),
            'completed_cards': len(completed_cards),
            'active_cards': len([c for c in self._cards.values() 
                                 if c.status == CardStatus.ACTIVE]),
            'blocked_cards': len(self.get_blocked_cards()),
            'cycle_time': {
                'avg_hours': sum(cycle_times) / len(cycle_times) if cycle_times else 0,
                'min_hours': min(cycle_times) if cycle_times else 0,
                'max_hours': max(cycle_times) if cycle_times else 0,
                'p50_hours': percentile(cycle_times, 50),
                'p85_hours': percentile(cycle_times, 85),
                'p95_hours': percentile(cycle_times, 95)
            },
            'lead_time': {
                'avg_hours': sum(lead_times) / len(lead_times) if lead_times else 0,
                'min_hours': min(lead_times) if lead_times else 0,
                'max_hours': max(lead_times) if lead_times else 0,
                'p50_hours': percentile(lead_times, 50),
                'p85_hours': percentile(lead_times, 85),
                'p95_hours': percentile(lead_times, 95)
            },
            'throughput': len(completed_cards)  # 可扩展为每日/每周
        }
    
    def generate_cfd_data(self, start_date: datetime = None,
                          end_date: datetime = None,
                          interval_hours: int = 24) -> List[Dict[str, Any]]:
        """生成累积流图数据"""
        if not start_date:
            start_date = self._created_at
        if not end_date:
            end_date = datetime.now()
        
        # 收集所有历史事件
        events = []  # [(timestamp, card_id, from_col, to_col), ...]
        for card in self._cards.values():
            for i, (col, ts) in enumerate(card.history):
                events.append((ts, card.id, card.history[i-1][0] if i > 0 else None, col))
        
        events.sort(key=lambda x: x[0])
        
        # 生成时间点数据
        cfd_data = []
        current_time = start_date
        column_counts = {name: 0 for name in self._column_order}
        
        event_idx = 0
        while current_time <= end_date:
            # 处理到当前时间的所有事件
            while event_idx < len(events) and events[event_idx][0] <= current_time:
                _, _, from_col, to_col = events[event_idx]
                if from_col and from_col in column_counts:
                    column_counts[from_col] -= 1
                if to_col in column_counts:
                    column_counts[to_col] += 1
                event_idx += 1
            
            cfd_data.append({
                'timestamp': current_time.isoformat(),
                **{name: count for name, count in column_counts.items()}
            })
            
            current_time += timedelta(hours=interval_hours)
        
        return cfd_data
    
    def get_throughput(self, days: int = 7) -> Dict[str, Any]:
        """获取吞吐量统计"""
        now = datetime.now()
        start_date = now - timedelta(days=days)
        
        completed_in_period = []
        for card in self._cards.values():
            # 检查卡片是否在时间段内完成
            end_col = self.get_end_column()
            if end_col:
                for col, ts in card.history:
                    if col == end_col.name and start_date <= ts <= now:
                        completed_in_period.append(card)
                        break
        
        # 按天分组
        daily_counts = defaultdict(int)
        for card in completed_in_period:
            for col, ts in card.history:
                if col == self.get_end_column().name:
                    daily_counts[ts.date().isoformat()] += 1
                    break
        
        total = len(completed_in_period)
        avg_per_day = total / days
        
        return {
            'period_days': days,
            'total_completed': total,
            'average_per_day': round(avg_per_day, 2),
            'daily_breakdown': dict(daily_counts)
        }
    
    # ==================== 导入导出 ====================
    
    def to_dict(self) -> Dict[str, Any]:
        """导出为字典"""
        return {
            'name': self.name,
            'created_at': self._created_at.isoformat(),
            'columns': [col.to_dict() for col in self.get_columns()],
            'cards': [card.to_dict() for card in self._cards.values()]
        }
    
    def to_json(self) -> str:
        """导出为 JSON"""
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=2)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'KanbanBoard':
        """从字典导入"""
        board = cls(name=data.get('name', 'Imported Board'))
        
        # 导入列
        for col_data in data.get('columns', []):
            board.add_column(
                name=col_data['name'],
                wip_limit=col_data.get('wip_limit', 0),
                is_start=col_data.get('is_start', False),
                is_end=col_data.get('is_end', False)
            )
        
        # 导入卡片
        for card_data in data.get('cards', []):
            card = board.add_card(
                card_id=card_data['id'],
                title=card_data['title'],
                column=card_data['column'],
                priority=card_data.get('priority', 0),
                tags=card_data.get('tags', []),
                custom_fields=card_data.get('custom_fields', {})
            )
            
            # 恢复状态
            if card_data.get('status') == 'blocked':
                card.block(card_data.get('blocked_reason', ''), 
                          _parse_iso_datetime(card_data['blocked_at']) if card_data.get('blocked_at') else None)
            elif card_data.get('status') == 'archived':
                card.status = CardStatus.ARCHIVED
            
            # 恢复历史
            card.history = [
                (col, _parse_iso_datetime(ts)) 
                for col, ts in card_data.get('history', [])
            ]
            card.created_at = _parse_iso_datetime(card_data['created_at'])
            if card_data.get('moved_at'):
                card.moved_at = _parse_iso_datetime(card_data['moved_at'])
        
        return board
    
    @classmethod
    def from_json(cls, json_str: str) -> 'KanbanBoard':
        """从 JSON 导入"""
        return cls.from_dict(json.loads(json_str))


# ==================== 辅助函数 ====================

def create_standard_kanban(name: str = "Standard Board",
                           wip_limits: Dict[str, int] = None) -> KanbanBoard:
    """创建标准看板（To Do -> In Progress -> Done）"""
    board = KanbanBoard(name)
    
    defaults = {'To Do': 0, 'In Progress': 3, 'Done': 0}
    limits = wip_limits or defaults
    
    board.add_column('To Do', wip_limit=limits.get('To Do', 0), is_start=True)
    board.add_column('In Progress', wip_limit=limits.get('In Progress', 3))
    board.add_column('Done', wip_limit=limits.get('Done', 0), is_end=True)
    
    return board


def create_scrum_kanban(name: str = "Sprint Board",
                        wip_limits: Dict[str, int] = None) -> KanbanBoard:
    """创建 Scrum 看板"""
    board = KanbanBoard(name)
    
    defaults = {
        'Backlog': 0,
        'Sprint Backlog': 10,
        'In Progress': 3,
        'In Review': 2,
        'Testing': 2,
        'Done': 0
    }
    limits = wip_limits or defaults
    
    board.add_column('Backlog', wip_limit=limits.get('Backlog', 0), is_start=True)
    board.add_column('Sprint Backlog', wip_limit=limits.get('Sprint Backlog', 10))
    board.add_column('In Progress', wip_limit=limits.get('In Progress', 3))
    board.add_column('In Review', wip_limit=limits.get('In Review', 2))
    board.add_column('Testing', wip_limit=limits.get('Testing', 2))
    board.add_column('Done', wip_limit=limits.get('Done', 0), is_end=True)
    
    return board


def calculate_efficiency(board: KanbanBoard) -> Dict[str, Any]:
    """计算看板效率指标"""
    metrics = board.get_flow_metrics()
    
    blocked_cards = board.get_blocked_cards()
    total_block_time = timedelta()
    for card in blocked_cards:
        if card.blocked_at:
            total_block_time += datetime.now() - card.blocked_at
    
    wip_status = board.get_wip_status()
    wip_violations = sum(1 for s in wip_status.values() if s['is_over'])
    
    return {
        'flow_efficiency': round(
            (metrics['cycle_time']['avg_hours'] / max(metrics['lead_time']['avg_hours'], 0.1)) * 100, 2
        ) if metrics['lead_time']['avg_hours'] > 0 else 0,
        'blocked_cards': len(blocked_cards),
        'wip_violations': wip_violations,
        'bottleneck_columns': len(board.detect_bottlenecks()),
        'throughput_per_day': metrics['throughput'],
        'avg_cycle_time_hours': round(metrics['cycle_time']['avg_hours'], 2),
        'avg_lead_time_hours': round(metrics['lead_time']['avg_hours'], 2)
    }