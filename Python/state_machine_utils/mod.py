"""
State Machine Utils - 有限状态机工具

提供完整的有限状态机 (FSM) 实现功能。
零外部依赖，仅使用 Python 标准库。

核心功能：
- 状态定义与转换
- 条件触发转换
- 进入/退出状态回调
- 历史状态支持
- 并行状态支持
- 状态持久化与恢复
- 事件队列处理
- 状态机可视化

使用示例：
    from state_machine_utils import StateMachine, State, Transition
    
    # 创建状态
    idle = State("idle")
    running = State("running")
    paused = State("paused")
    
    # 创建状态机
    sm = StateMachine(initial_state=idle)
    
    # 添加转换
    sm.add_transition(idle, running, "start")
    sm.add_transition(running, paused, "pause")
    sm.add_transition(paused, running, "resume")
    sm.add_transition(running, idle, "stop")
    
    # 触发事件
    sm.send("start")  # idle -> running
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Callable, Any, Set, Tuple
from enum import Enum
import json
import copy


class StateType(Enum):
    """状态类型"""
    BASIC = "basic"           # 基本状态
    COMPOSITE = "composite"   # 复合状态（包含子状态）
    FINAL = "final"          # 终止状态
    INITIAL = "initial"      # 初始状态
    HISTORY = "history"      # 历史状态
    PARALLEL = "parallel"    # 并行状态


@dataclass
class State:
    """状态定义"""
    name: str
    state_type: StateType = StateType.BASIC
    on_enter: Optional[Callable[[], None]] = None
    on_exit: Optional[Callable[[], None]] = None
    parent: Optional['State'] = None
    children: List['State'] = field(default_factory=list)
    initial_child: Optional['State'] = None
    history: Optional['State'] = None
    
    def __eq__(self, other):
        if isinstance(other, State):
            return self.name == other.name
        return False
    
    def __hash__(self):
        return hash(self.name)
    
    def __repr__(self):
        return f"State({self.name})"
    
    def add_child(self, child: 'State', is_initial: bool = False) -> 'State':
        """添加子状态"""
        child.parent = self
        self.children.append(child)
        if is_initial:
            self.initial_child = child
        self.state_type = StateType.COMPOSITE
        return self
    
    def is_active(self, context: 'StateMachineContext') -> bool:
        """检查状态是否激活"""
        return self in context.active_states


@dataclass
class Transition:
    """状态转换定义"""
    from_state: State
    to_state: State
    event: str
    guard: Optional[Callable[[], bool]] = None
    action: Optional[Callable[[], None]] = None
    
    def __repr__(self):
        return f"Transition({self.from_state.name} --[{self.event}]--> {self.to_state.name})"


@dataclass
class Event:
    """事件定义"""
    name: str
    data: Any = None
    timestamp: float = 0.0
    
    def __repr__(self):
        return f"Event({self.name})"


@dataclass
class StateMachineContext:
    """状态机上下文"""
    active_states: Set[State] = field(default_factory=set)
    history: Dict[str, State] = field(default_factory=dict)
    data: Dict[str, Any] = field(default_factory=dict)
    event_queue: List[Event] = field(default_factory=list)
    
    def set_data(self, key: str, value: Any):
        """设置上下文数据"""
        self.data[key] = value
    
    def get_data(self, key: str, default: Any = None) -> Any:
        """获取上下文数据"""
        return self.data.get(key, default)
    
    def to_dict(self) -> Dict:
        """序列化为字典"""
        return {
            "active_states": [s.name for s in self.active_states],
            "history": {k: v.name for k, v in self.history.items()},
            "data": self.data
        }
    
    @classmethod
    def from_dict(cls, data: Dict, state_map: Dict[str, State]) -> 'StateMachineContext':
        """从字典反序列化"""
        ctx = cls()
        ctx.active_states = {state_map[n] for n in data.get("active_states", []) if n in state_map}
        ctx.history = {k: state_map[v] for k, v in data.get("history", {}).items() if v in state_map}
        ctx.data = data.get("data", {})
        return ctx


class StateMachine:
    """有限状态机"""
    
    def __init__(self, initial_state: Optional[State] = None, name: str = "StateMachine"):
        self.name = name
        self.states: Dict[str, State] = {}
        self.transitions: List[Transition] = []
        self.context = StateMachineContext()
        self.initial_state: Optional[State] = initial_state
        self.current_state: Optional[State] = None
        self.event_handlers: Dict[str, List[Callable]] = {}
        self._transition_count = 0
        self._event_count = 0
        self._history: List[Tuple[str, State, State]] = []  # (event, from, to)
        
        if initial_state:
            self.add_state(initial_state)
    
    def add_state(self, state: State, set_initial: bool = False) -> 'StateMachine':
        """添加状态"""
        self.states[state.name] = state
        if set_initial:
            self.initial_state = state
        if state.children:
            for child in state.children:
                self.add_state(child)
        return self
    
    def add_transition(
        self,
        from_state: State,
        to_state: State,
        event: str,
        guard: Optional[Callable[[], bool]] = None,
        action: Optional[Callable[[], None]] = None
    ) -> 'StateMachine':
        """添加状态转换"""
        # 确保状态已添加
        if from_state.name not in self.states:
            self.add_state(from_state)
        if to_state.name not in self.states:
            self.add_state(to_state)
        
        transition = Transition(from_state, to_state, event, guard, action)
        self.transitions.append(transition)
        return self
    
    def on_event(self, event_name: str, handler: Callable) -> 'StateMachine':
        """注册事件处理器"""
        if event_name not in self.event_handlers:
            self.event_handlers[event_name] = []
        self.event_handlers[event_name].append(handler)
        return self
    
    def start(self) -> 'StateMachine':
        """启动状态机"""
        if not self.initial_state:
            raise ValueError("Initial state not set")
        
        self.current_state = self.initial_state
        self.context.active_states.add(self.initial_state)
        self._enter_state(self.initial_state)
        return self
    
    def send(self, event_name: str, data: Any = None) -> bool:
        """发送事件"""
        if not self.current_state:
            raise ValueError("State machine not started")
        
        self._event_count += 1
        event = Event(event_name, data)
        
        # 查找匹配的转换
        for transition in self.transitions:
            if (transition.from_state == self.current_state and 
                transition.event == event_name):
                
                # 检查守卫条件
                if transition.guard and not transition.guard():
                    continue
                
                # 执行转换
                self._execute_transition(transition, event)
                return True
        
        # 处理未匹配的事件
        if event_name in self.event_handlers:
            for handler in self.event_handlers[event_name]:
                handler(event)
        
        return False
    
    def send_async(self, event_name: str, data: Any = None) -> None:
        """异步发送事件（加入队列）"""
        event = Event(event_name, data)
        self.context.event_queue.append(event)
    
    def process_queue(self) -> int:
        """处理事件队列，返回处理的事件数"""
        processed = 0
        while self.context.event_queue:
            event = self.context.event_queue.pop(0)
            self.send(event.name, event.data)
            processed += 1
        return processed
    
    def _execute_transition(self, transition: Transition, event: Event) -> None:
        """执行状态转换"""
        from_state = transition.from_state
        to_state = transition.to_state
        
        # 记录历史
        self._history.append((event.name, from_state, to_state))
        self._transition_count += 1
        
        # 保存历史状态
        self.context.history[from_state.name] = from_state
        
        # 退出当前状态
        self._exit_state(from_state)
        
        # 执行转换动作
        if transition.action:
            transition.action()
        
        # 进入新状态
        self.current_state = to_state
        self.context.active_states.discard(from_state)
        self.context.active_states.add(to_state)
        self._enter_state(to_state)
    
    def _enter_state(self, state: State) -> None:
        """进入状态"""
        if state.on_enter:
            state.on_enter()
        
        # 如果是复合状态，进入初始子状态
        if state.state_type == StateType.COMPOSITE and state.initial_child:
            self.current_state = state.initial_child
            self.context.active_states.add(state.initial_child)
            self._enter_state(state.initial_child)
        
        # 如果是历史状态，恢复历史
        if state.state_type == StateType.HISTORY and state.name in self.context.history:
            history_state = self.context.history[state.name]
            self.current_state = history_state
            self.context.active_states.add(history_state)
            self._enter_state(history_state)
    
    def _exit_state(self, state: State) -> None:
        """退出状态"""
        if state.on_exit:
            state.on_exit()
    
    def is_in_state(self, state: State) -> bool:
        """检查是否在指定状态"""
        return self.current_state == state
    
    def can_transition(self, event: str) -> bool:
        """检查是否可以转换"""
        for transition in self.transitions:
            if (transition.from_state == self.current_state and 
                transition.event == event):
                if transition.guard and not transition.guard():
                    return False
                return True
        return False
    
    def get_available_events(self) -> List[str]:
        """获取当前状态可用的事件"""
        events = []
        for transition in self.transitions:
            if transition.from_state == self.current_state:
                events.append(transition.event)
        return list(set(events))
    
    def get_transitions(self) -> List[Dict]:
        """获取所有转换定义"""
        return [
            {
                "from": t.from_state.name,
                "to": t.to_state.name,
                "event": t.event
            }
            for t in self.transitions
        ]
    
    def save_state(self) -> str:
        """保存状态机状态"""
        return json.dumps({
            "current_state": self.current_state.name if self.current_state else None,
            "context": self.context.to_dict(),
            "transition_count": self._transition_count,
            "event_count": self._event_count
        })
    
    def load_state(self, state_json: str) -> None:
        """加载状态机状态"""
        data = json.loads(state_json)
        if data.get("current_state"):
            self.current_state = self.states[data["current_state"]]
        self.context = StateMachineContext.from_dict(data.get("context", {}), self.states)
        self._transition_count = data.get("transition_count", 0)
        self._event_count = data.get("event_count", 0)
    
    def reset(self) -> None:
        """重置状态机"""
        self.current_state = None
        self.context = StateMachineContext()
        self._transition_count = 0
        self._event_count = 0
        self._history = []
    
    def get_history(self) -> List[Tuple[str, str, str]]:
        """获取转换历史"""
        return [(e, f.name, t.name) for e, f, t in self._history]
    
    def visualize(self, format: str = "text") -> str:
        """可视化状态机"""
        if format == "text":
            lines = [f"State Machine: {self.name}", "=" * 40]
            lines.append(f"\nStates: {list(self.states.keys())}")
            lines.append(f"\nCurrent State: {self.current_state}")
            lines.append(f"\nTransitions:")
            for t in self.transitions:
                guard_str = " [guard]" if t.guard else ""
                lines.append(f"  {t.from_state.name} --[{t.event}]--> {t.to_state.name}{guard_str}")
            lines.append(f"\nStatistics:")
            lines.append(f"  Transitions: {self._transition_count}")
            lines.append(f"  Events: {self._event_count}")
            return "\n".join(lines)
        elif format == "mermaid":
            lines = ["stateDiagram-v2"]
            for t in self.transitions:
                lines.append(f"    {t.from_state.name} --> {t.to_state.name} : {t.event}")
            return "\n".join(lines)
        elif format == "dot":
            lines = ["digraph StateMachine {"]
            lines.append('    rankdir=LR;')
            for t in self.transitions:
                lines.append(f'    "{t.from_state.name}" -> "{t.to_state.name}" [label="{t.event}"];')
            lines.append("}")
            return "\n".join(lines)
        return ""
    
    @property
    def stats(self) -> Dict:
        """获取统计信息"""
        return {
            "state_count": len(self.states),
            "transition_count": len(self.transitions),
            "total_transitions": self._transition_count,
            "total_events": self._event_count
        }


class StateMachineBuilder:
    """状态机构建器（流式API）"""
    
    def __init__(self, name: str = "StateMachine"):
        self._name = name
        self._states: Dict[str, State] = {}
        self._transitions: List[Dict] = []
        self._initial_state: Optional[str] = None
    
    def state(self, name: str, on_enter: Optional[Callable] = None, 
              on_exit: Optional[Callable] = None) -> 'StateMachineBuilder':
        """定义状态"""
        s = State(name, on_enter=on_enter, on_exit=on_exit)
        self._states[name] = s
        return self
    
    def initial(self, name: str) -> 'StateMachineBuilder':
        """设置初始状态"""
        self._initial_state = name
        return self
    
    def transition(self, from_state: str, to_state: str, event: str,
                   guard: Optional[Callable] = None, 
                   action: Optional[Callable] = None) -> 'StateMachineBuilder':
        """定义转换"""
        self._transitions.append({
            "from": from_state,
            "to": to_state,
            "event": event,
            "guard": guard,
            "action": action
        })
        return self
    
    def build(self) -> StateMachine:
        """构建状态机"""
        if not self._initial_state:
            raise ValueError("Initial state not set")
        
        initial = self._states.get(self._initial_state)
        if not initial:
            raise ValueError(f"Initial state '{self._initial_state}' not defined")
        
        sm = StateMachine(initial_state=initial, name=self._name)
        
        # 添加所有状态
        for state in self._states.values():
            if state != initial:
                sm.add_state(state)
        
        # 添加所有转换
        for t in self._transitions:
            from_s = self._states.get(t["from"])
            to_s = self._states.get(t["to"])
            if from_s and to_s:
                sm.add_transition(from_s, to_s, t["event"], t.get("guard"), t.get("action"))
        
        return sm


class ParallelStateMachine:
    """并行状态机"""
    
    def __init__(self, name: str = "ParallelStateMachine"):
        self.name = name
        self.regions: List[StateMachine] = []
        self._event_count = 0
    
    def add_region(self, state_machine: StateMachine) -> 'ParallelStateMachine':
        """添加并行区域"""
        self.regions.append(state_machine)
        return self
    
    def start(self) -> 'ParallelStateMachine':
        """启动所有区域"""
        for region in self.regions:
            region.start()
        return self
    
    def send(self, event_name: str, data: Any = None) -> Dict[str, bool]:
        """发送事件到所有区域"""
        self._event_count += 1
        results = {}
        for region in self.regions:
            results[region.name] = region.send(event_name, data)
        return results
    
    def get_states(self) -> Dict[str, Optional[State]]:
        """获取所有区域的当前状态"""
        return {region.name: region.current_state for region in self.regions}
    
    @property
    def stats(self) -> Dict:
        """获取统计信息"""
        return {
            "region_count": len(self.regions),
            "total_events": self._event_count,
            "regions": {r.name: r.stats for r in self.regions}
        }


# ==================== 工具函数 ====================

def create_simple_fsm(
    states: List[str],
    transitions: List[Tuple[str, str, str]],
    initial: str
) -> StateMachine:
    """
    快速创建简单状态机
    
    Args:
        states: 状态名称列表
        transitions: 转换列表 [(from, to, event), ...]
        initial: 初始状态名
    
    Returns:
        StateMachine 实例
    
    Example:
        sm = create_simple_fsm(
            states=["idle", "running", "paused"],
            transitions=[
                ("idle", "running", "start"),
                ("running", "paused", "pause"),
                ("paused", "running", "resume"),
                ("running", "idle", "stop")
            ],
            initial="idle"
        )
        sm.start()
        sm.send("start")
    """
    state_objs = {name: State(name) for name in states}
    initial_state = state_objs.get(initial)
    
    if not initial_state:
        raise ValueError(f"Initial state '{initial}' not found")
    
    sm = StateMachine(initial_state=initial_state)
    
    for name, state in state_objs.items():
        if name != initial:
            sm.add_state(state)
    
    for from_s, to_s, event in transitions:
        sm.add_transition(state_objs[from_s], state_objs[to_s], event)
    
    return sm


def validate_state_machine(sm: StateMachine) -> List[str]:
    """
    验证状态机定义
    
    Returns:
        错误消息列表，空列表表示验证通过
    """
    errors = []
    
    # 检查初始状态
    if not sm.initial_state:
        errors.append("Initial state not set")
    
    # 检查孤立状态
    transition_states = set()
    for t in sm.transitions:
        transition_states.add(t.from_state.name)
        transition_states.add(t.to_state.name)
    
    for state_name in sm.states:
        if state_name not in transition_states and state_name != sm.initial_state.name:
            errors.append(f"Isolated state: {state_name}")
    
    # 检查不可达状态
    reachable = set()
    if sm.initial_state:
        reachable.add(sm.initial_state.name)
        changed = True
        while changed:
            changed = False
            for t in sm.transitions:
                if t.from_state.name in reachable and t.to_state.name not in reachable:
                    reachable.add(t.to_state.name)
                    changed = True
    
    for state_name in sm.states:
        if state_name not in reachable:
            errors.append(f"Unreachable state: {state_name}")
    
    # 检查最终状态（无出转换）
    has_final = False
    for state_name in sm.states:
        has_out = any(t.from_state.name == state_name for t in sm.transitions)
        if not has_out:
            has_final = True
    
    return errors


def fsm_to_json(sm: StateMachine) -> str:
    """导出状态机定义为JSON"""
    return json.dumps({
        "name": sm.name,
        "states": list(sm.states.keys()),
        "initial_state": sm.initial_state.name if sm.initial_state else None,
        "transitions": sm.get_transitions()
    }, indent=2)


def json_to_fsm(json_str: str) -> StateMachine:
    """从JSON导入状态机定义"""
    data = json.loads(json_str)
    
    states = {name: State(name) for name in data["states"]}
    initial = states.get(data["initial_state"])
    
    if not initial:
        raise ValueError("Initial state not found in JSON")
    
    sm = StateMachine(initial_state=initial, name=data.get("name", "StateMachine"))
    
    for name, state in states.items():
        if name != initial.name:
            sm.add_state(state)
    
    for t in data["transitions"]:
        sm.add_transition(states[t["from"]], states[t["to"]], t["event"])
    
    return sm


def get_state_diagram(sm: StateMachine) -> str:
    """获取状态图（Mermaid格式）"""
    return sm.visualize("mermaid")


def simulate_fsm(sm: StateMachine, events: List[str], start: bool = True) -> List[str]:
    """
    模拟状态机执行
    
    Args:
        sm: 状态机实例
        events: 事件列表
        start: 是否自动启动
    
    Returns:
        状态变化列表
    """
    if start:
        sm.start()
    
    history = [f"Initial: {sm.current_state.name}"]
    
    for event in events:
        success = sm.send(event)
        if success:
            history.append(f"{event} -> {sm.current_state.name}")
        else:
            history.append(f"{event} (no transition)")
    
    return history


# ==================== 常用状态机模板 ====================

def create_turnstile_fsm() -> StateMachine:
    """创建旋转门状态机"""
    return create_simple_fsm(
        states=["locked", "unlocked"],
        transitions=[
            ("locked", "unlocked", "coin"),
            ("unlocked", "locked", "push"),
            ("unlocked", "locked", "timeout")
        ],
        initial="locked"
    )


def create_traffic_light_fsm() -> StateMachine:
    """创建交通灯状态机"""
    return create_simple_fsm(
        states=["red", "green", "yellow"],
        transitions=[
            ("red", "green", "timer"),
            ("green", "yellow", "timer"),
            ("yellow", "red", "timer")
        ],
        initial="red"
    )


def create_order_fsm() -> StateMachine:
    """创建订单状态机"""
    return create_simple_fsm(
        states=["created", "paid", "shipped", "delivered", "cancelled"],
        transitions=[
            ("created", "paid", "pay"),
            ("created", "cancelled", "cancel"),
            ("paid", "shipped", "ship"),
            ("paid", "cancelled", "cancel"),
            ("shipped", "delivered", "deliver"),
            ("shipped", "cancelled", "return")
        ],
        initial="created"
    )


def create_tcp_fsm() -> StateMachine:
    """创建TCP连接状态机（简化版）"""
    return create_simple_fsm(
        states=["CLOSED", "LISTEN", "SYN_SENT", "SYN_RECEIVED", 
                "ESTABLISHED", "FIN_WAIT_1", "FIN_WAIT_2", 
                "CLOSE_WAIT", "CLOSING", "LAST_ACK", "TIME_WAIT"],
        transitions=[
            ("CLOSED", "LISTEN", "open"),
            ("LISTEN", "SYN_SENT", "send_syn"),
            ("LISTEN", "SYN_RECEIVED", "receive_syn"),
            ("SYN_SENT", "ESTABLISHED", "receive_syn_ack"),
            ("SYN_SENT", "CLOSED", "timeout"),
            ("SYN_RECEIVED", "ESTABLISHED", "send_ack"),
            ("ESTABLISHED", "FIN_WAIT_1", "close"),
            ("ESTABLISHED", "CLOSE_WAIT", "receive_fin"),
            ("FIN_WAIT_1", "FIN_WAIT_2", "receive_ack"),
            ("FIN_WAIT_1", "CLOSING", "receive_fin"),
            ("FIN_WAIT_2", "TIME_WAIT", "receive_fin"),
            ("CLOSE_WAIT", "LAST_ACK", "close"),
            ("CLOSING", "TIME_WAIT", "receive_ack"),
            ("LAST_ACK", "CLOSED", "receive_ack"),
            ("TIME_WAIT", "CLOSED", "timeout")
        ],
        initial="CLOSED"
    )


if __name__ == "__main__":
    # 简单示例
    print("=" * 50)
    print("State Machine Utils Demo")
    print("=" * 50)
    
    # 使用快速创建函数
    sm = create_simple_fsm(
        states=["idle", "running", "paused", "stopped"],
        transitions=[
            ("idle", "running", "start"),
            ("running", "paused", "pause"),
            ("paused", "running", "resume"),
            ("running", "stopped", "stop"),
            ("paused", "stopped", "stop"),
            ("stopped", "idle", "reset")
        ],
        initial="idle"
    )
    
    sm.start()
    print(f"\nInitial state: {sm.current_state}")
    
    # 模拟事件
    events = ["start", "pause", "resume", "stop", "reset"]
    results = simulate_fsm(sm, events, start=False)
    print("\nSimulation:")
    for r in results:
        print(f"  {r}")
    
    # 可视化
    print("\nMermaid Diagram:")
    print(sm.visualize("mermaid"))
    
    # 统计
    print(f"\nStats: {sm.stats}")
    
    # 验证
    errors = validate_state_machine(sm)
    print(f"\nValidation: {'PASS' if not errors else errors}")