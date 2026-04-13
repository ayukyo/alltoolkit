"""
状态机工具库使用示例

展示状态机的基本使用、条件转换、回调函数、层次状态机等高级功能
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    StateMachine,
    HierarchicalStateMachine,
    StateMachineBuilder,
    create_order_state_machine,
    create_task_state_machine,
    create_game_character_state_machine,
    create_tcp_connection_state_machine
)


def basic_usage():
    """基本使用示例"""
    print("\n" + "=" * 50)
    print("1. 基本使用")
    print("=" * 50)
    
    # 创建一个简单的状态机
    sm = StateMachine('idle')
    
    # 添加状态
    sm.add_state('idle')
    sm.add_state('running')
    sm.add_state('paused')
    sm.add_state('completed', final=True)
    
    # 添加转换
    sm.add_transition('idle', 'running', event='start')
    sm.add_transition('running', 'paused', event='pause')
    sm.add_transition('paused', 'running', event='resume')
    sm.add_transition('running', 'completed', event='finish')
    
    # 使用事件触发转换
    print(f"当前状态: {sm.current_state}")
    
    sm.trigger('start')
    print(f"触发 start 后: {sm.current_state}")
    
    sm.trigger('pause')
    print(f"触发 pause 后: {sm.current_state}")
    
    sm.trigger('resume')
    print(f"触发 resume 后: {sm.current_state}")
    
    sm.trigger('finish')
    print(f"触发 finish 后: {sm.current_state}")
    print(f"是否终态: {sm.is_final}")


def conditional_transition():
    """条件转换示例"""
    print("\n" + "=" * 50)
    print("2. 条件转换")
    print("=" * 50)
    
    # 创建一个带条件的状态机
    balance = {'amount': 100}
    
    def has_enough_balance():
        return balance['amount'] >= 50
    
    sm = StateMachine('ready')
    sm.add_state('ready')
    sm.add_state('purchased')
    sm.add_state('insufficient')
    
    # 只有余额 >= 50 才能购买
    sm.add_transition('ready', 'purchased', event='buy', condition=has_enough_balance)
    sm.add_transition('ready', 'insufficient', event='buy_failed')
    
    print(f"余额: {balance['amount']}")
    print(f"可以转换到 'purchased': {sm.can_transition_to('purchased')}")
    
    # 测试购买
    if sm.trigger('buy'):
        print("购买成功!")
    else:
        print("购买失败!")
    
    # 减少余额
    balance['amount'] = 30
    sm.reset()
    print(f"\n余额: {balance['amount']}")
    print(f"可以转换到 'purchased': {sm.can_transition_to('purchased')}")
    
    if sm.trigger('buy'):
        print("购买成功!")
    else:
        print("购买失败!")


def callbacks_example():
    """回调函数示例"""
    print("\n" + "=" * 50)
    print("3. 回调函数")
    print("=" * 50)
    
    logs = []
    
    def on_enter_running():
        logs.append("进入运行状态")
        print("🔔 进入运行状态")
    
    def on_exit_running():
        logs.append("退出运行状态")
        print("🔔 退出运行状态")
    
    def log_transition(from_state, to_state, event, **kwargs):
        logs.append(f"{from_state} -> {to_state} (事件: {event})")
        print(f"📝 转换: {from_state} -> {to_state} (事件: {event})")
    
    sm = StateMachine('stopped')
    sm.add_state('stopped')
    sm.add_state('running', on_enter=on_enter_running, on_exit=on_exit_running)
    sm.add_state('finished')
    
    sm.add_transition('stopped', 'running', event='start')
    sm.add_transition('running', 'finished', event='finish')
    
    sm.on_transition(log_transition)
    
    print("触发 start...")
    sm.trigger('start')
    
    print("\n触发 finish...")
    sm.trigger('finish')
    
    print(f"\n日志记录: {logs}")


def history_example():
    """历史记录示例"""
    print("\n" + "=" * 50)
    print("4. 历史记录")
    print("=" * 50)
    
    sm = StateMachine('start', enable_history=True, max_history=10)
    
    sm.add_state('start')
    sm.add_state('step1')
    sm.add_state('step2')
    sm.add_state('end', final=True)
    
    sm.add_transition('start', 'step1', event='next')
    sm.add_transition('step1', 'step2', event='next')
    sm.add_transition('step2', 'end', event='finish')
    
    # 遍历状态
    for event in ['next', 'next', 'finish']:
        sm.trigger(event)
    
    # 查看历史
    print("\n状态历史:")
    for i, record in enumerate(sm.history, 1):
        duration = f"{record.duration_ms:.2f}ms" if record.duration_ms else "N/A"
        print(f"  {i}. {record.state} (停留: {duration})")
    
    # 导出为 JSON
    print("\n导出为 JSON:")
    print(sm.to_json())


def builder_pattern():
    """构建器模式示例"""
    print("\n" + "=" * 50)
    print("5. 构建器模式")
    print("=" * 50)
    
    # 使用构建器创建状态机
    sm = (StateMachineBuilder('TrafficLightSM')
          .initial('red')
          .state('red')
          .state('green')
          .state('yellow')
          .transition('red', 'green', event='timer')
          .transition('green', 'yellow', event='timer')
          .transition('yellow', 'red', event='timer')
          .with_history(True, max_records=20)
          .build())
    
    print(f"状态机名称: {sm.name}")
    print(f"当前状态: {sm.current_state}")
    
    # 模拟几个循环
    for i in range(7):
        sm.trigger('timer')
        print(f"  -> {sm.current_state}")


def hierarchical_state_machine():
    """层次状态机示例"""
    print("\n" + "=" * 50)
    print("6. 层次状态机")
    print("=" * 50)
    
    hsm = HierarchicalStateMachine('off')
    
    # 定义状态层次: off -> on -> (working, idle)
    hsm.add_state('off')
    hsm.add_state('on')
    hsm.add_state('working')
    hsm.add_state('idle')
    
    hsm.add_substate('on', 'working', is_initial=True)
    hsm.add_substate('on', 'idle')
    
    hsm.add_transition('off', 'working', event='turn_on')
    hsm.add_transition('working', 'idle', event='rest')
    hsm.add_transition('idle', 'working', event='work')
    hsm.add_transition('working', 'off', event='turn_off')
    
    print("状态层次:")
    print(f"  on 的子状态: {hsm.get_children('on')}")
    print(f"  working 的父状态: {hsm.get_parent('working')}")
    
    print(f"\n当前状态: {hsm.current_state}")
    print(f"working 的状态路径: {hsm.get_state_path('working')}")
    
    hsm.trigger('turn_on')
    print(f"turn_on 后: {hsm.current_state}")
    print(f"是否在 'on' 状态: {hsm.is_in_state('on')}")
    
    hsm.trigger('rest')
    print(f"rest 后: {hsm.current_state}")
    print(f"是否在 'on' 状态: {hsm.is_in_state('on')}")


def order_state_machine():
    """订单状态机示例"""
    print("\n" + "=" * 50)
    print("7. 订单状态机")
    print("=" * 50)
    
    sm = create_order_state_machine()
    
    print(f"初始状态: {sm.current_state}")
    print(f"可用转换: {sm.get_available_transitions()}")
    
    # 模拟订单流程
    print("\n模拟正常订单流程:")
    events = ['pay', 'process', 'ship', 'deliver']
    for event in events:
        sm.trigger(event)
        print(f"  {event} -> {sm.current_state}")
        available = sm.get_available_transitions()
        if available:
            print(f"  可用事件: {[e for _, e in available]}")
    
    # 模拟取消流程
    print("\n模拟取消订单流程:")
    sm.reset()
    sm.trigger('pay')
    print(f"  pay -> {sm.current_state}")
    sm.trigger('cancel')
    print(f"  cancel -> {sm.current_state}")
    print(f"  是否终态: {sm.is_final}")


def task_state_machine():
    """任务状态机示例"""
    print("\n" + "=" * 50)
    print("8. 任务状态机")
    print("=" * 50)
    
    sm = create_task_state_machine()
    
    print(f"初始状态: {sm.current_state}")
    
    # 模拟任务执行
    sm.trigger('start')
    print(f"start -> {sm.current_state}")
    
    sm.trigger('pause')
    print(f"pause -> {sm.current_state}")
    
    sm.trigger('resume')
    print(f"resume -> {sm.current_state}")
    
    sm.trigger('complete')
    print(f"complete -> {sm.current_state}")
    print(f"是否终态: {sm.is_final}")


def game_character_state_machine():
    """游戏角色状态机示例"""
    print("\n" + "=" * 50)
    print("9. 游戏角色状态机")
    print("=" * 50)
    
    sm = create_game_character_state_machine()
    
    print(f"初始状态: {sm.current_state}")
    
    # 模拟游戏行为
    actions = [
        ('move', '角色开始移动'),
        ('attack', '角色开始攻击'),
        ('attack_end', '攻击结束'),
        ('take_damage', '受到伤害'),
        ('recover', '恢复'),
        ('move', '再次移动'),
        ('die', '角色死亡'),
    ]
    
    for event, desc in actions:
        sm.trigger(event)
        print(f"  {event} ({desc}) -> {sm.current_state}")
        if sm.is_final:
            print("  角色已死亡!")
            break


def tcp_state_machine():
    """TCP 连接状态机示例"""
    print("\n" + "=" * 50)
    print("10. TCP 连接状态机")
    print("=" * 50)
    
    sm = create_tcp_connection_state_machine()
    
    print("模拟 TCP 三次握手:")
    print(f"  初始状态: {sm.current_state}")
    
    sm.trigger('active_open')
    print(f"  发送 SYN: {sm.current_state}")
    
    sm.trigger('syn_ack_received')
    print(f"  收到 SYN-ACK: {sm.current_state}")
    
    print("\n模拟 TCP 四次挥手:")
    sm.trigger('active_close')
    print(f"  发送 FIN: {sm.current_state}")
    
    sm.trigger('ack_received')
    print(f"  收到 ACK: {sm.current_state}")
    
    sm.trigger('fin_received')
    print(f"  收到 FIN: {sm.current_state}")
    
    sm.trigger('timeout')
    print(f"  超时: {sm.current_state}")


def persistence_example():
    """持久化示例"""
    print("\n" + "=" * 50)
    print("11. 状态持久化")
    print("=" * 50)
    
    # 创建状态机并执行一些操作
    sm = StateMachine('draft')
    sm.add_state('draft')
    sm.add_state('review')
    sm.add_state('approved')
    sm.add_state('rejected')
    
    sm.add_transition('draft', 'review', event='submit')
    sm.add_transition('review', 'approved', event='approve')
    sm.add_transition('review', 'rejected', event='reject')
    
    sm.context['document_id'] = 'DOC-001'
    sm.context['author'] = 'Alice'
    sm.trigger('submit')
    
    # 导出状态
    json_data = sm.to_json()
    print("导出的状态:")
    print(json_data)
    
    # 模拟从持久化存储恢复
    print("\n从 JSON 恢复状态机...")
    restored = StateMachine.from_json(json_data)
    print(f"恢复后状态: {restored.current_state}")
    print(f"上下文数据: {restored.context}")


def direct_transition():
    """直接转换示例"""
    print("\n" + "=" * 50)
    print("12. 直接转换")
    print("=" * 50)
    
    sm = StateMachine('waiting')
    sm.add_state('waiting')
    sm.add_state('processing')
    sm.add_state('done')
    
    sm.add_transition('waiting', 'processing')
    sm.add_transition('processing', 'done')
    
    # 使用 transition_to 直接指定目标状态
    print(f"当前状态: {sm.current_state}")
    
    sm.transition_to('processing')
    print(f"直接转换到 processing: {sm.current_state}")
    
    sm.transition_to('done')
    print(f"直接转换到 done: {sm.current_state}")


def main():
    """运行所有示例"""
    print("\n" + "=" * 60)
    print("状态机工具库使用示例")
    print("=" * 60)
    
    basic_usage()
    conditional_transition()
    callbacks_example()
    history_example()
    builder_pattern()
    hierarchical_state_machine()
    order_state_machine()
    task_state_machine()
    game_character_state_machine()
    tcp_state_machine()
    persistence_example()
    direct_transition()
    
    print("\n" + "=" * 60)
    print("所有示例运行完成!")
    print("=" * 60)


if __name__ == '__main__':
    main()