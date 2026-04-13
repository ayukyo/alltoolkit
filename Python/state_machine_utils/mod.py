"""
State Machine Utils - 零依赖状态机工具库

提供完整的状态机实现，包括：
- 状态定义和转换规则
- 条件转换验证
- 进入/退出状态回调
- 状态历史记录
- 异步状态转换
- 状态持久化和恢复
"""

from typing import Any, Callable, Dict, List, Optional, Set, Tuple, Union
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime
import json
import copy
import re


def _parse_iso_datetime(dt_str: str) -> datetime:
    """解析 ISO 格式日期时间字符串（兼容 Python 3.6）"""
    if not dt_str:
        return None
    # 支持 YYYY-MM-DDTHH:MM:SS 和 YYYY-MM-DDTHH:MM:SS.ffffff
    pattern = r'^(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2}):(\d{2})(?:\.(\d+))?$'
    match = re.match(pattern, dt_str)
    if match:
        year, month, day, hour, minute, second = map(int, match.groups()[:6])
        microsecond = 0
        if match.group(7):
            # 处理微秒部分（可能不是6位）
            us_str = match.group(7)
            if len(us_str) > 6:
                us_str = us_str[:6]
            microsecond = int(us_str.ljust(6, '0'))
        return datetime(year, month, day, hour, minute, second, microsecond)
    raise ValueError(f"Invalid ISO datetime format: {dt_str}")


class TransitionError(Exception):
    """状态转换错误"""
    pass


class StateError(Exception):
    """状态错误"""
    pass


@dataclass
class Transition:
    """状态转换定义"""
    from_state: str
    to_state: str
    condition: Optional[Callable[[], bool]] = None
    action: Optional[Callable[[], Any]] = None
    event: Optional[str] = None  # 触发转换的事件名
    
    def check_condition(self) -> bool:
        """检查转换条件"""
        if self.condition is None:
            return True
        return self.condition()
    
    def execute_action(self) -> Any:
        """执行转换动作"""
        if self.action is None:
            return None
        return self.action()


@dataclass
class StateConfig:
    """状态配置"""
    name: str
    on_enter: Optional[Callable[[], Any]] = None
    on_exit: Optional[Callable[[], Any]] = None
    final: bool = False  # 是否为终态
    data: Dict[str, Any] = field(default_factory=dict)
    
    def enter(self) -> Any:
        """进入状态时执行"""
        if self.on_enter is None:
            return None
        return self.on_enter()
    
    def exit(self) -> Any:
        """退出状态时执行"""
        if self.on_exit is None:
            return None
        return self.on_exit()


@dataclass
class StateRecord:
    """状态历史记录"""
    state: str
    entered_at: datetime
    exited_at: Optional[datetime] = None
    duration_ms: Optional[float] = None
    transition_event: Optional[str] = None
    data: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'state': self.state,
            'entered_at': self.entered_at.isoformat() if self.entered_at else None,
            'exited_at': self.exited_at.isoformat() if self.exited_at else None,
            'duration_ms': self.duration_ms,
            'transition_event': self.transition_event,
            'data': self.data
        }


class StateMachine:
    """
    状态机核心类
    
    示例:
        sm = StateMachine('idle')
        sm.add_state('idle', on_enter=lambda: print('进入空闲状态'))
        sm.add_state('running', on_enter=lambda: print('进入运行状态'))
        sm.add_state('completed', final=True)
        
        sm.add_transition('idle', 'running', event='start')
        sm.add_transition('running', 'completed', event='finish')
        
        sm.trigger('start')  # idle -> running
    """
    
    def __init__(
        self,
        initial_state: str,
        name: Optional[str] = None,
        enable_history: bool = True,
        max_history: int = 100
    ):
        """
        初始化状态机
        
        Args:
            initial_state: 初始状态名
            name: 状态机名称
            enable_history: 是否启用历史记录
            max_history: 最大历史记录数
        """
        self.name = name or 'StateMachine'
        self._states: Dict[str, StateConfig] = {}
        self._transitions: List[Transition] = []
        self._current_state: str = initial_state
        self._initial_state: str = initial_state
        self._context: Dict[str, Any] = {}
        self._enable_history = enable_history
        self._max_history = max_history
        self._history: List[StateRecord] = []
        self._current_record: Optional[StateRecord] = None
        self._on_transition_callback: Optional[Callable] = None
        self._on_state_change_callback: Optional[Callable] = None
        
        # 记录初始状态
        if enable_history:
            self._current_record = StateRecord(
                state=initial_state,
                entered_at=datetime.now()
            )
    
    @property
    def current_state(self) -> str:
        """当前状态"""
        return self._current_state
    
    @property
    def context(self) -> Dict[str, Any]:
        """上下文数据"""
        return self._context
    
    @property
    def history(self) -> List[StateRecord]:
        """状态历史"""
        return self._history.copy()
    
    @property
    def is_final(self) -> bool:
        """是否处于终态"""
        state_config = self._states.get(self._current_state)
        return state_config.final if state_config else False
    
    def add_state(
        self,
        name: str,
        on_enter: Optional[Callable[[], Any]] = None,
        on_exit: Optional[Callable[[], Any]] = None,
        final: bool = False,
        data: Optional[Dict[str, Any]] = None
    ) -> 'StateMachine':
        """
        添加状态
        
        Args:
            name: 状态名
            on_enter: 进入状态回调
            on_exit: 退出状态回调
            final: 是否为终态
            data: 状态关联数据
            
        Returns:
            self，支持链式调用
        """
        self._states[name] = StateConfig(
            name=name,
            on_enter=on_enter,
            on_exit=on_exit,
            final=final,
            data=data or {}
        )
        return self
    
    def add_transition(
        self,
        from_state: str,
        to_state: str,
        condition: Optional[Callable[[], bool]] = None,
        action: Optional[Callable[[], Any]] = None,
        event: Optional[str] = None
    ) -> 'StateMachine':
        """
        添加状态转换
        
        Args:
            from_state: 源状态
            to_state: 目标状态
            condition: 转换条件函数
            action: 转换时执行的动作
            event: 触发转换的事件名
            
        Returns:
            self，支持链式调用
        """
        self._transitions.append(Transition(
            from_state=from_state,
            to_state=to_state,
            condition=condition,
            action=action,
            event=event
        ))
        return self
    
    def on_transition(self, callback: Callable) -> 'StateMachine':
        """
        设置状态转换回调
        
        Args:
            callback: 回调函数 (from_state, to_state, event) -> None
            
        Returns:
            self
        """
        self._on_transition_callback = callback
        return self
    
    def on_state_change(self, callback: Callable) -> 'StateMachine':
        """
        设置状态变更回调
        
        Args:
            callback: 回调函数 (old_state, new_state) -> None
            
        Returns:
            self
        """
        self._on_state_change_callback = callback
        return self
    
    def can_transition_to(self, to_state: str) -> bool:
        """
        检查是否可以转换到指定状态
        
        Args:
            to_state: 目标状态
            
        Returns:
            是否可以转换
        """
        for transition in self._transitions:
            if transition.from_state == self._current_state and transition.to_state == to_state:
                return transition.check_condition()
        return False
    
    def get_available_transitions(self) -> List[Tuple[str, Optional[str]]]:
        """
        获取当前状态可用的转换
        
        Returns:
            列表，每项为 (目标状态, 事件名)
        """
        available = []
        for transition in self._transitions:
            if transition.from_state == self._current_state:
                if transition.check_condition():
                    available.append((transition.to_state, transition.event))
        return available
    
    def trigger(
        self,
        event: str,
        **kwargs
    ) -> bool:
        """
        通过事件触发状态转换
        
        Args:
            event: 事件名
            **kwargs: 传递给回调的参数
            
        Returns:
            是否成功转换
        """
        # 查找匹配的转换
        matching_transitions = []
        for transition in self._transitions:
            if transition.from_state == self._current_state and transition.event == event:
                matching_transitions.append(transition)
        
        if not matching_transitions:
            return False
        
        # 执行第一个满足条件的转换
        for transition in matching_transitions:
            if transition.check_condition():
                self._execute_transition(transition, **kwargs)
                return True
        
        return False
    
    def transition_to(
        self,
        to_state: str,
        **kwargs
    ) -> bool:
        """
        直接转换到指定状态
        
        Args:
            to_state: 目标状态
            **kwargs: 传递给回调的参数
            
        Returns:
            是否成功转换
        """
        for transition in self._transitions:
            if transition.from_state == self._current_state and transition.to_state == to_state:
                if transition.check_condition():
                    self._execute_transition(transition, **kwargs)
                    return True
        return False
    
    def _execute_transition(self, transition: Transition, **kwargs):
        """执行状态转换"""
        from_state = self._current_state
        to_state = transition.to_state
        
        # 执行退出回调
        if from_state in self._states:
            self._states[from_state].exit()
        
        # 执行转换动作
        transition.execute_action()
        
        # 更新当前状态
        old_state = self._current_state
        self._current_state = to_state
        
        # 记录历史
        if self._enable_history and self._current_record:
            self._current_record.exited_at = datetime.now()
            duration = (self._current_record.exited_at - self._current_record.entered_at).total_seconds() * 1000
            self._current_record.duration_ms = duration
            self._current_record.transition_event = transition.event
            self._history.append(self._current_record)
            
            # 限制历史记录数量
            if len(self._history) > self._max_history:
                self._history = self._history[-self._max_history:]
        
        # 创建新的状态记录
        if self._enable_history:
            self._current_record = StateRecord(
                state=to_state,
                entered_at=datetime.now()
            )
        
        # 执行进入回调
        if to_state in self._states:
            self._states[to_state].enter()
        
        # 触发回调
        if self._on_transition_callback:
            self._on_transition_callback(from_state, to_state, transition.event, **kwargs)
        
        if self._on_state_change_callback:
            self._on_state_change_callback(old_state, to_state, **kwargs)
    
    def force_state(self, state: str):
        """
        强制设置状态（不触发转换）
        
        Args:
            state: 目标状态
        """
        self._current_state = state
        if self._enable_history:
            if self._current_record:
                self._current_record.exited_at = datetime.now()
                self._history.append(self._current_record)
            self._current_record = StateRecord(
                state=state,
                entered_at=datetime.now()
            )
    
    def reset(self):
        """重置到初始状态"""
        self._current_state = self._initial_state
        self._context.clear()
        self._history.clear()
        if self._enable_history:
            self._current_record = StateRecord(
                state=self._initial_state,
                entered_at=datetime.now()
            )
    
    def to_dict(self) -> Dict[str, Any]:
        """导出状态机状态为字典"""
        return {
            'name': self.name,
            'current_state': self._current_state,
            'initial_state': self._initial_state,
            'context': copy.deepcopy(self._context),
            'history': [r.to_dict() for r in self._history]
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'StateMachine':
        """从字典恢复状态机"""
        sm = cls(
            initial_state=data['initial_state'],
            name=data.get('name')
        )
        sm._current_state = data['current_state']
        sm._context = data.get('context', {})
        sm._history = [
            StateRecord(
                state=r['state'],
                entered_at=_parse_iso_datetime(r['entered_at']) if r.get('entered_at') else None,
                exited_at=_parse_iso_datetime(r['exited_at']) if r.get('exited_at') else None,
                duration_ms=r.get('duration_ms'),
                transition_event=r.get('transition_event'),
                data=r.get('data', {})
            )
            for r in data.get('history', [])
        ]
        return sm
    
    def to_json(self) -> str:
        """导出为 JSON 字符串"""
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=2)
    
    @classmethod
    def from_json(cls, json_str: str) -> 'StateMachine':
        """从 JSON 字符串恢复"""
        return cls.from_dict(json.loads(json_str))
    
    def __repr__(self) -> str:
        return f"<StateMachine name={self.name} current={self._current_state} states={len(self._states)} transitions={len(self._transitions)}>"


class HierarchicalStateMachine(StateMachine):
    """
    层次状态机
    
    支持嵌套状态，形成状态层次结构
    """
    
    def __init__(
        self,
        initial_state: str,
        name: Optional[str] = None,
        enable_history: bool = True,
        max_history: int = 100
    ):
        super().__init__(initial_state, name, enable_history, max_history)
        self._parent_states: Dict[str, str] = {}  # 子状态 -> 父状态
        self._child_states: Dict[str, Set[str]] = {}  # 父状态 -> 子状态集合
        self._initial_substates: Dict[str, str] = {}  # 父状态 -> 默认子状态
    
    def add_substate(
        self,
        parent: str,
        child: str,
        is_initial: bool = False
    ) -> 'HierarchicalStateMachine':
        """
        添加子状态
        
        Args:
            parent: 父状态名
            child: 子状态名
            is_initial: 是否为父状态的默认子状态
            
        Returns:
            self
        """
        self._parent_states[child] = parent
        if parent not in self._child_states:
            self._child_states[parent] = set()
        self._child_states[parent].add(child)
        
        if is_initial:
            self._initial_substates[parent] = child
        
        return self
    
    def get_parent(self, state: str) -> Optional[str]:
        """获取父状态"""
        return self._parent_states.get(state)
    
    def get_children(self, state: str) -> Set[str]:
        """获取子状态"""
        return self._child_states.get(state, set()).copy()
    
    def get_state_path(self, state: str) -> List[str]:
        """
        获取状态的完整路径（从根到叶）
        
        Args:
            state: 状态名
            
        Returns:
            状态路径列表
        """
        path = [state]
        current = state
        while current in self._parent_states:
            current = self._parent_states[current]
            path.insert(0, current)
        return path
    
    def is_in_state(self, state: str) -> bool:
        """
        检查当前状态是否属于某状态（包括层次关系）
        
        Args:
            state: 状态名
            
        Returns:
            是否处于该状态或其子状态
        """
        current = self._current_state
        while current:
            if current == state:
                return True
            current = self._parent_states.get(current)
        return False
    
    def exit_to_ancestor(self, ancestor: str) -> List[str]:
        """
        从当前状态退出到祖先状态
        
        Args:
            ancestor: 目标祖先状态
            
        Returns:
            经过的状态列表
        """
        exited = []
        current = self._current_state
        while current and current != ancestor:
            exited.append(current)
            if current in self._states:
                self._states[current].exit()
            current = self._parent_states.get(current)
        return exited
    
    def enter_from_ancestor(self, ancestor: str, target: str) -> List[str]:
        """
        从祖先状态进入目标状态
        
        Args:
            ancestor: 起始祖先状态
            target: 目标状态
            
        Returns:
            进入的状态列表
        """
        # 计算路径
        path = []
        current = target
        while current and current != ancestor:
            path.insert(0, current)
            current = self._parent_states.get(current)
        
        # 依次进入
        for state in path:
            if state in self._states:
                self._states[state].enter()
        
        return path


class StateMachineBuilder:
    """
    状态机构建器
    
    使用流式 API 构建状态机
    """
    
    def __init__(self, name: Optional[str] = None):
        self._name = name
        self._initial_state: Optional[str] = None
        self._states: Dict[str, StateConfig] = {}
        self._transitions: List[Transition] = []
        self._enable_history = True
        self._max_history = 100
    
    def initial(self, state: str) -> 'StateMachineBuilder':
        """设置初始状态"""
        self._initial_state = state
        return self
    
    def state(
        self,
        name: str,
        on_enter: Optional[Callable] = None,
        on_exit: Optional[Callable] = None,
        final: bool = False
    ) -> 'StateMachineBuilder':
        """添加状态"""
        self._states[name] = StateConfig(
            name=name,
            on_enter=on_enter,
            on_exit=on_exit,
            final=final
        )
        return self
    
    def transition(
        self,
        from_state: str,
        to_state: str,
        event: Optional[str] = None,
        condition: Optional[Callable[[], bool]] = None,
        action: Optional[Callable[[], Any]] = None
    ) -> 'StateMachineBuilder':
        """添加转换"""
        self._transitions.append(Transition(
            from_state=from_state,
            to_state=to_state,
            event=event,
            condition=condition,
            action=action
        ))
        return self
    
    def with_history(self, enable: bool = True, max_records: int = 100) -> 'StateMachineBuilder':
        """配置历史记录"""
        self._enable_history = enable
        self._max_history = max_records
        return self
    
    def build(self) -> StateMachine:
        """构建状态机"""
        if not self._initial_state:
            raise StateError("初始状态未设置")
        
        sm = StateMachine(
            initial_state=self._initial_state,
            name=self._name,
            enable_history=self._enable_history,
            max_history=self._max_history
        )
        
        for name, config in self._states.items():
            sm.add_state(
                name=name,
                on_enter=config.on_enter,
                on_exit=config.on_exit,
                final=config.final
            )
        
        for transition in self._transitions:
            sm.add_transition(
                from_state=transition.from_state,
                to_state=transition.to_state,
                condition=transition.condition,
                action=transition.action,
                event=transition.event
            )
        
        return sm


# 常用状态机模式工厂函数

def create_order_state_machine() -> StateMachine:
    """
    创建订单状态机
    
    状态流转: pending -> paid -> processing -> shipped -> delivered
    可取消: pending, paid, processing -> cancelled
    """
    sm = StateMachine('pending', name='OrderStateMachine')
    
    sm.add_state('pending')
    sm.add_state('paid')
    sm.add_state('processing')
    sm.add_state('shipped')
    sm.add_state('delivered', final=True)
    sm.add_state('cancelled', final=True)
    
    # 正常流程
    sm.add_transition('pending', 'paid', event='pay')
    sm.add_transition('paid', 'processing', event='process')
    sm.add_transition('processing', 'shipped', event='ship')
    sm.add_transition('shipped', 'delivered', event='deliver')
    
    # 取消流程
    sm.add_transition('pending', 'cancelled', event='cancel')
    sm.add_transition('paid', 'cancelled', event='cancel')
    sm.add_transition('processing', 'cancelled', event='cancel')
    
    return sm


def create_task_state_machine() -> StateMachine:
    """
    创建任务状态机
    
    状态流转: todo -> in_progress -> done
    可暂停: in_progress -> paused -> in_progress
    """
    sm = StateMachine('todo', name='TaskStateMachine')
    
    sm.add_state('todo')
    sm.add_state('in_progress')
    sm.add_state('paused')
    sm.add_state('done', final=True)
    sm.add_state('archived', final=True)
    
    sm.add_transition('todo', 'in_progress', event='start')
    sm.add_transition('in_progress', 'done', event='complete')
    sm.add_transition('in_progress', 'paused', event='pause')
    sm.add_transition('paused', 'in_progress', event='resume')
    sm.add_transition('done', 'archived', event='archive')
    
    return sm


def create_game_character_state_machine() -> StateMachine:
    """
    创建游戏角色状态机
    
    状态流转: idle -> moving -> attacking -> idle
    受伤/死亡状态
    """
    sm = StateMachine('idle', name='GameCharacterStateMachine')
    
    sm.add_state('idle')
    sm.add_state('moving')
    sm.add_state('attacking')
    sm.add_state('hurt')
    sm.add_state('dead', final=True)
    
    # 移动
    sm.add_transition('idle', 'moving', event='move')
    sm.add_transition('moving', 'idle', event='stop')
    
    # 攻击
    sm.add_transition('idle', 'attacking', event='attack')
    sm.add_transition('moving', 'attacking', event='attack')
    sm.add_transition('attacking', 'idle', event='attack_end')
    
    # 受伤
    sm.add_transition('idle', 'hurt', event='take_damage')
    sm.add_transition('moving', 'hurt', event='take_damage')
    sm.add_transition('attacking', 'hurt', event='take_damage')
    sm.add_transition('hurt', 'idle', event='recover')
    
    # 死亡
    sm.add_transition('idle', 'dead', event='die')
    sm.add_transition('moving', 'dead', event='die')
    sm.add_transition('attacking', 'dead', event='die')
    sm.add_transition('hurt', 'dead', event='die')
    
    return sm


def create_tcp_connection_state_machine() -> StateMachine:
    """
    创建 TCP 连接状态机
    
    状态流转: CLOSED -> SYN_SENT -> ESTABLISHED -> FIN_WAIT -> CLOSED
    """
    sm = StateMachine('CLOSED', name='TCPConnectionStateMachine')
    
    sm.add_state('CLOSED')
    sm.add_state('LISTEN')
    sm.add_state('SYN_SENT')
    sm.add_state('SYN_RECEIVED')
    sm.add_state('ESTABLISHED')
    sm.add_state('FIN_WAIT_1')
    sm.add_state('FIN_WAIT_2')
    sm.add_state('CLOSING')
    sm.add_state('TIME_WAIT')
    sm.add_state('CLOSE_WAIT')
    sm.add_state('LAST_ACK')
    
    # 主动打开
    sm.add_transition('CLOSED', 'SYN_SENT', event='active_open')
    sm.add_transition('SYN_SENT', 'ESTABLISHED', event='syn_ack_received')
    
    # 被动打开
    sm.add_transition('CLOSED', 'LISTEN', event='passive_open')
    sm.add_transition('LISTEN', 'SYN_RECEIVED', event='syn_received')
    sm.add_transition('SYN_RECEIVED', 'ESTABLISHED', event='ack_received')
    
    # 主动关闭
    sm.add_transition('ESTABLISHED', 'FIN_WAIT_1', event='active_close')
    sm.add_transition('FIN_WAIT_1', 'FIN_WAIT_2', event='ack_received')
    sm.add_transition('FIN_WAIT_2', 'TIME_WAIT', event='fin_received')
    sm.add_transition('TIME_WAIT', 'CLOSED', event='timeout')
    
    # 被动关闭
    sm.add_transition('ESTABLISHED', 'CLOSE_WAIT', event='fin_received')
    sm.add_transition('CLOSE_WAIT', 'LAST_ACK', event='active_close')
    sm.add_transition('LAST_ACK', 'CLOSED', event='ack_received')
    
    # 同时关闭
    sm.add_transition('FIN_WAIT_1', 'CLOSING', event='fin_received')
    sm.add_transition('CLOSING', 'TIME_WAIT', event='ack_received')
    
    return sm