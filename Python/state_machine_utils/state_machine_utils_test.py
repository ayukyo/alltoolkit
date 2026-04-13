"""
状态机工具库测试

测试覆盖：
- 基本状态转换
- 条件转换
- 回调函数
- 历史记录
- 状态持久化
- 层次状态机
- 构建器模式
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mod import (
    StateMachine,
    HierarchicalStateMachine,
    StateMachineBuilder,
    StateError,
    TransitionError,
    StateRecord,
    create_order_state_machine,
    create_task_state_machine,
    create_game_character_state_machine,
    create_tcp_connection_state_machine
)
from datetime import datetime
import time


def test_basic_state_machine():
    """测试基本状态机功能"""
    print("\n=== 测试基本状态机 ===")
    
    sm = StateMachine('idle')
    sm.add_state('idle')
    sm.add_state('running')
    sm.add_state('stopped')
    
    sm.add_transition('idle', 'running', event='start')
    sm.add_transition('running', 'stopped', event='stop')
    
    assert sm.current_state == 'idle'
    assert not sm.is_final
    
    # 测试事件触发
    result = sm.trigger('start')
    assert result == True
    assert sm.current_state == 'running'
    
    result = sm.trigger('stop')
    assert result == True
    assert sm.current_state == 'stopped'
    
    # 测试无效事件
    result = sm.trigger('invalid')
    assert result == False
    
    print("✅ 基本状态机测试通过")


def test_final_state():
    """测试终态"""
    print("\n=== 测试终态 ===")
    
    sm = StateMachine('start')
    sm.add_state('start')
    sm.add_state('end', final=True)
    sm.add_transition('start', 'end', event='finish')
    
    assert not sm.is_final
    
    sm.trigger('finish')
    assert sm.current_state == 'end'
    assert sm.is_final
    
    print("✅ 终态测试通过")


def test_conditional_transition():
    """测试条件转换"""
    print("\n=== 测试条件转换 ===")
    
    counter = {'value': 0}
    
    def can_proceed():
        return counter['value'] >= 3
    
    sm = StateMachine('waiting')
    sm.add_state('waiting')
    sm.add_state('ready')
    
    sm.add_transition('waiting', 'ready', event='check', condition=can_proceed)
    
    # 条件不满足
    result = sm.trigger('check')
    assert result == False
    assert sm.current_state == 'waiting'
    
    # 满足条件
    counter['value'] = 3
    result = sm.trigger('check')
    assert result == True
    assert sm.current_state == 'ready'
    
    print("✅ 条件转换测试通过")


def test_transition_actions():
    """测试转换动作"""
    print("\n=== 测试转换动作 ===")
    
    actions = []
    
    def on_enter_running():
        actions.append('enter_running')
    
    def on_exit_running():
        actions.append('exit_running')
    
    def on_transition():
        actions.append('transition')
    
    sm = StateMachine('idle')
    sm.add_state('idle')
    sm.add_state('running', on_enter=on_enter_running, on_exit=on_exit_running)
    sm.add_state('done')
    
    sm.add_transition('idle', 'running', event='start', action=on_transition)
    sm.add_transition('running', 'done', event='finish')
    
    sm.trigger('start')
    assert 'enter_running' in actions
    assert 'transition' in actions
    
    actions.clear()
    sm.trigger('finish')
    assert 'exit_running' in actions
    
    print("✅ 转换动作测试通过")


def test_callbacks():
    """测试回调函数"""
    print("\n=== 测试回调函数 ===")
    
    transitions = []
    state_changes = []
    
    sm = StateMachine('a')
    sm.add_state('a')
    sm.add_state('b')
    sm.add_state('c')
    
    sm.add_transition('a', 'b', event='go_b')
    sm.add_transition('b', 'c', event='go_c')
    
    sm.on_transition(lambda f, t, e, **kw: transitions.append((f, t, e)))
    sm.on_state_change(lambda o, n, **kw: state_changes.append((o, n)))
    
    sm.trigger('go_b')
    sm.trigger('go_c')
    
    assert len(transitions) == 2
    assert len(state_changes) == 2
    
    print("✅ 回调函数测试通过")


def test_history():
    """测试历史记录"""
    print("\n=== 测试历史记录 ===")
    
    sm = StateMachine('a', enable_history=True)
    sm.add_state('a')
    sm.add_state('b')
    sm.add_state('c')
    
    sm.add_transition('a', 'b', event='go_b')
    sm.add_transition('b', 'c', event='go_c')
    
    sm.trigger('go_b')
    sm.trigger('go_c')
    
    history = sm.history
    assert len(history) == 2
    assert history[0].state == 'a'
    assert history[1].state == 'b'
    assert history[0].exited_at is not None
    assert history[0].duration_ms is not None
    
    print("✅ 历史记录测试通过")


def test_available_transitions():
    """测试获取可用转换"""
    print("\n=== 测试获取可用转换 ===")
    
    sm = StateMachine('start')
    sm.add_state('start')
    sm.add_state('middle')
    sm.add_state('end')
    
    sm.add_transition('start', 'middle', event='go_middle')
    sm.add_transition('start', 'end', event='go_end')
    
    available = sm.get_available_transitions()
    assert len(available) == 2
    assert ('middle', 'go_middle') in available
    assert ('end', 'go_end') in available
    
    print("✅ 获取可用转换测试通过")


def test_force_state():
    """测试强制设置状态"""
    print("\n=== 测试强制设置状态 ===")
    
    sm = StateMachine('a')
    sm.add_state('a')
    sm.add_state('b')
    sm.add_state('c')
    
    sm.force_state('c')
    assert sm.current_state == 'c'
    
    print("✅ 强制设置状态测试通过")


def test_reset():
    """测试重置状态机"""
    print("\n=== 测试重置状态机 ===")
    
    sm = StateMachine('initial')
    sm.add_state('initial')
    sm.add_state('other')
    
    sm.context['data'] = 'value'
    sm.add_transition('initial', 'other', event='go')
    sm.trigger('go')
    
    sm.reset()
    
    assert sm.current_state == 'initial'
    assert len(sm.context) == 0
    assert len(sm.history) == 0
    
    print("✅ 重置状态机测试通过")


def test_persistence():
    """测试状态持久化"""
    print("\n=== 测试状态持久化 ===")
    
    sm = StateMachine('start')
    sm.add_state('start')
    sm.add_state('middle')
    sm.add_state('end')
    
    sm.add_transition('start', 'middle', event='go')
    sm.add_transition('middle', 'end', event='finish')
    
    sm.context['user'] = 'test_user'
    sm.trigger('go')
    
    # 导出为字典
    data = sm.to_dict()
    assert data['current_state'] == 'middle'
    assert data['context']['user'] == 'test_user'
    
    # 从字典恢复
    sm2 = StateMachine.from_dict(data)
    assert sm2.current_state == 'middle'
    assert sm2.context['user'] == 'test_user'
    
    # JSON 序列化
    json_str = sm.to_json()
    sm3 = StateMachine.from_json(json_str)
    assert sm3.current_state == 'middle'
    
    print("✅ 状态持久化测试通过")


def test_builder_pattern():
    """测试构建器模式"""
    print("\n=== 测试构建器模式 ===")
    
    sm = (StateMachineBuilder('TestSM')
          .initial('ready')
          .state('ready')
          .state('running')
          .state('done', final=True)
          .transition('ready', 'running', event='start')
          .transition('running', 'done', event='finish')
          .build())
    
    assert sm.current_state == 'ready'
    assert sm.name == 'TestSM'
    
    sm.trigger('start')
    assert sm.current_state == 'running'
    
    sm.trigger('finish')
    assert sm.current_state == 'done'
    assert sm.is_final
    
    print("✅ 构建器模式测试通过")


def test_hierarchical_state_machine():
    """测试层次状态机"""
    print("\n=== 测试层次状态机 ===")
    
    hsm = HierarchicalStateMachine('off')
    
    # 添加状态层次: off -> on -> (working, idle)
    hsm.add_state('off')
    hsm.add_state('on')
    hsm.add_state('working')
    hsm.add_state('idle')
    
    hsm.add_substate('on', 'working', is_initial=True)
    hsm.add_substate('on', 'idle')
    
    assert hsm.get_parent('working') == 'on'
    assert hsm.get_parent('idle') == 'on'
    assert 'working' in hsm.get_children('on')
    assert 'idle' in hsm.get_children('on')
    
    # 测试状态路径
    assert hsm.get_state_path('working') == ['on', 'working']
    assert hsm.get_state_path('idle') == ['on', 'idle']
    
    print("✅ 层次状态机测试通过")


def test_order_state_machine():
    """测试订单状态机"""
    print("\n=== 测试订单状态机 ===")
    
    sm = create_order_state_machine()
    
    assert sm.current_state == 'pending'
    
    # 正常流程
    sm.trigger('pay')
    assert sm.current_state == 'paid'
    
    sm.trigger('process')
    assert sm.current_state == 'processing'
    
    sm.trigger('ship')
    assert sm.current_state == 'shipped'
    
    sm.trigger('deliver')
    assert sm.current_state == 'delivered'
    assert sm.is_final
    
    print("✅ 订单状态机测试通过")


def test_task_state_machine():
    """测试任务状态机"""
    print("\n=== 测试任务状态机 ===")
    
    sm = create_task_state_machine()
    
    assert sm.current_state == 'todo'
    
    sm.trigger('start')
    assert sm.current_state == 'in_progress'
    
    sm.trigger('pause')
    assert sm.current_state == 'paused'
    
    sm.trigger('resume')
    assert sm.current_state == 'in_progress'
    
    sm.trigger('complete')
    assert sm.current_state == 'done'
    assert sm.is_final
    
    print("✅ 任务状态机测试通过")


def test_game_character_state_machine():
    """测试游戏角色状态机"""
    print("\n=== 测试游戏角色状态机 ===")
    
    sm = create_game_character_state_machine()
    
    assert sm.current_state == 'idle'
    
    # 移动
    sm.trigger('move')
    assert sm.current_state == 'moving'
    
    # 攻击
    sm.trigger('attack')
    assert sm.current_state == 'attacking'
    
    # 攻击结束
    sm.trigger('attack_end')
    assert sm.current_state == 'idle'
    
    # 受伤流程
    sm.trigger('take_damage')
    assert sm.current_state == 'hurt'
    
    sm.trigger('recover')
    assert sm.current_state == 'idle'
    
    print("✅ 游戏角色状态机测试通过")


def test_tcp_connection_state_machine():
    """测试 TCP 连接状态机"""
    print("\n=== 测试 TCP 连接状态机 ===")
    
    sm = create_tcp_connection_state_machine()
    
    assert sm.current_state == 'CLOSED'
    
    # 主动打开
    sm.trigger('active_open')
    assert sm.current_state == 'SYN_SENT'
    
    sm.trigger('syn_ack_received')
    assert sm.current_state == 'ESTABLISHED'
    
    # 主动关闭
    sm.trigger('active_close')
    assert sm.current_state == 'FIN_WAIT_1'
    
    sm.trigger('ack_received')
    assert sm.current_state == 'FIN_WAIT_2'
    
    sm.trigger('fin_received')
    assert sm.current_state == 'TIME_WAIT'
    
    sm.trigger('timeout')
    assert sm.current_state == 'CLOSED'
    
    print("✅ TCP 连接状态机测试通过")


def test_direct_transition():
    """测试直接转换"""
    print("\n=== 测试直接转换 ===")
    
    sm = StateMachine('a')
    sm.add_state('a')
    sm.add_state('b')
    sm.add_state('c')
    
    sm.add_transition('a', 'b')
    sm.add_transition('b', 'c')
    
    # 直接转换
    result = sm.transition_to('b')
    assert result == True
    assert sm.current_state == 'b'
    
    # 无效直接转换
    result = sm.transition_to('a')  # 没有这个转换
    assert result == False
    assert sm.current_state == 'b'
    
    print("✅ 直接转换测试通过")


def test_can_transition_to():
    """测试检查是否可转换"""
    print("\n=== 测试检查是否可转换 ===")
    
    sm = StateMachine('start')
    sm.add_state('start')
    sm.add_state('end')
    
    sm.add_transition('start', 'end', condition=lambda: True)
    
    assert sm.can_transition_to('end') == True
    assert sm.can_transition_to('invalid') == False
    
    print("✅ 检查是否可转换测试通过")


def test_context():
    """测试上下文数据"""
    print("\n=== 测试上下文数据 ===")
    
    sm = StateMachine('init')
    sm.add_state('init')
    sm.add_state('next')
    sm.add_transition('init', 'next', event='go')
    
    sm.context['user_id'] = 123
    sm.context['session'] = {'name': 'test'}
    
    sm.trigger('go')
    
    assert sm.context['user_id'] == 123
    assert sm.context['session']['name'] == 'test'
    
    print("✅ 上下文数据测试通过")


def test_chained_calls():
    """测试链式调用"""
    print("\n=== 测试链式调用 ===")
    
    sm = (StateMachine('a')
          .add_state('a')
          .add_state('b')
          .add_state('c')
          .add_transition('a', 'b', event='go_b')
          .add_transition('b', 'c', event='go_c'))
    
    assert sm.current_state == 'a'
    sm.trigger('go_b')
    assert sm.current_state == 'b'
    
    print("✅ 链式调用测试通过")


def run_all_tests():
    """运行所有测试"""
    print("=" * 50)
    print("状态机工具库测试")
    print("=" * 50)
    
    tests = [
        test_basic_state_machine,
        test_final_state,
        test_conditional_transition,
        test_transition_actions,
        test_callbacks,
        test_history,
        test_available_transitions,
        test_force_state,
        test_reset,
        test_persistence,
        test_builder_pattern,
        test_hierarchical_state_machine,
        test_order_state_machine,
        test_task_state_machine,
        test_game_character_state_machine,
        test_tcp_connection_state_machine,
        test_direct_transition,
        test_can_transition_to,
        test_context,
        test_chained_calls,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"❌ {test.__name__} 失败: {e}")
            failed += 1
        except Exception as e:
            print(f"❌ {test.__name__} 异常: {e}")
            failed += 1
    
    print("\n" + "=" * 50)
    print(f"测试结果: {passed} 通过, {failed} 失败")
    print("=" * 50)
    
    return failed == 0


if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)