#!/usr/bin/env python3
"""
State Machine Utils 基础示例

演示有限状态机的基本用法。
"""

import sys
sys.path.insert(0, '..')

from mod import (
    State, StateMachine, StateMachineBuilder,
    create_simple_fsm, simulate_fsm, create_turnstile_fsm,
    create_traffic_light_fsm, create_order_fsm, create_tcp_fsm
)


def example_basic_state_machine():
    """基础状态机示例"""
    print("=" * 60)
    print("示例1: 基础状态机")
    print("=" * 60)
    
    # 创建状态机
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
    print(f"\n初始状态: {sm.current_state}")
    
    # 发送事件
    events = ["start", "pause", "resume", "stop", "reset"]
    for event in events:
        result = sm.send(event)
        print(f"事件 '{event}': {'成功' if result else '失败'} -> {sm.current_state}")
    
    # 统计
    print(f"\n统计: {sm.stats}")


def example_with_callbacks():
    """带回调的状态机示例"""
    print("\n" + "=" * 60)
    print("示例2: 带回调的状态机")
    print("=" * 60)
    
    # 定义回调
    def on_enter_running():
        print("  🏃 开始运行")
    
    def on_exit_running():
        print("  🛑 停止运行")
    
    def on_enter_paused():
        print("  ⏸️ 已暂停")
    
    # 创建状态
    idle = State("idle")
    running = State("running", on_enter=on_enter_running, on_exit=on_exit_running)
    paused = State("paused", on_enter=on_enter_paused)
    
    # 创建状态机
    sm = StateMachine(initial_state=idle)
    sm.add_state(running)
    sm.add_state(paused)
    
    sm.add_transition(idle, running, "start")
    sm.add_transition(running, paused, "pause")
    sm.add_transition(paused, running, "resume")
    sm.add_transition(running, idle, "stop")
    
    print("\n启动状态机...")
    sm.start()
    
    print("\n发送 'start' 事件...")
    sm.send("start")
    
    print("\n发送 'pause' 事件...")
    sm.send("pause")
    
    print("\n发送 'resume' 事件...")
    sm.send("resume")
    
    print("\n发送 'stop' 事件...")
    sm.send("stop")


def example_with_guards():
    """带守卫条件的状态机示例"""
    print("\n" + "=" * 60)
    print("示例3: 带守卫条件的状态机")
    print("=" * 60)
    
    # 模拟余额
    balance = [0]
    
    def has_balance():
        return balance[0] >= 100
    
    def deduct():
        balance[0] -= 100
        print(f"  💰 扣款成功，余额: {balance[0]}")
    
    idle = State("idle")
    paid = State("paid")
    
    sm = StateMachine(initial_state=idle)
    sm.add_state(paid)
    
    # 只有余额足够时才能支付
    sm.add_transition(idle, paid, "pay", guard=has_balance, action=deduct)
    sm.add_transition(paid, idle, "reset")
    
    sm.start()
    
    print(f"\n初始余额: {balance[0]}")
    print("尝试支付...")
    sm.send("pay")  # 应该失败
    print(f"当前状态: {sm.current_state}")
    
    # 充值
    balance[0] = 150
    print(f"\n充值后余额: {balance[0]}")
    print("尝试支付...")
    sm.send("pay")  # 应该成功
    print(f"当前状态: {sm.current_state}")


def example_builder_pattern():
    """流式API示例"""
    print("\n" + "=" * 60)
    print("示例4: 流式API构建")
    print("=" * 60)
    
    sm = (StateMachineBuilder("MediaPlayer")
        .state("stopped")
        .state("playing")
        .state("paused")
        .initial("stopped")
        .transition("stopped", "playing", "play")
        .transition("playing", "paused", "pause")
        .transition("paused", "playing", "resume")
        .transition("playing", "stopped", "stop")
        .transition("paused", "stopped", "stop")
        .build())
    
    sm.start()
    print(f"\n初始状态: {sm.current_state}")
    
    # 模拟
    history = simulate_fsm(sm, ["play", "pause", "resume", "stop"])
    print("\n模拟历史:")
    for h in history:
        print(f"  {h}")


def example_templates():
    """预定义模板示例"""
    print("\n" + "=" * 60)
    print("示例5: 预定义模板")
    print("=" * 60)
    
    # 旋转门
    print("\n--- 旋转门状态机 ---")
    turnstile = create_turnstile_fsm()
    turnstile.start()
    print(f"初始: {turnstile.current_state}")
    turnstile.send("coin")
    print(f"投币后: {turnstile.current_state}")
    turnstile.send("push")
    print(f"推门后: {turnstile.current_state}")
    
    # 交通灯
    print("\n--- 交通灯状态机 ---")
    traffic = create_traffic_light_fsm()
    traffic.start()
    print(f"初始: {traffic.current_state}")
    for _ in range(5):
        traffic.send("timer")
        print(f"计时后: {traffic.current_state}")
    
    # 订单
    print("\n--- 订单状态机 ---")
    order = create_order_fsm()
    order.start()
    print(f"初始: {order.current_state}")
    order.send("pay")
    print(f"支付后: {order.current_state}")
    order.send("ship")
    print(f"发货后: {order.current_state}")
    order.send("deliver")
    print(f"送达后: {order.current_state}")


def example_visualization():
    """可视化示例"""
    print("\n" + "=" * 60)
    print("示例6: 可视化输出")
    print("=" * 60)
    
    sm = create_simple_fsm(
        states=["A", "B", "C"],
        transitions=[
            ("A", "B", "next"),
            ("B", "C", "next"),
            ("C", "A", "reset")
        ],
        initial="A"
    )
    
    print("\n--- 文本格式 ---")
    print(sm.visualize("text"))
    
    print("\n--- Mermaid 格式 ---")
    print(sm.visualize("mermaid"))
    
    print("\n--- DOT 格式 ---")
    print(sm.visualize("dot"))


def example_persistence():
    """状态持久化示例"""
    print("\n" + "=" * 60)
    print("示例7: 状态持久化")
    print("=" * 60)
    
    sm = create_simple_fsm(
        states=["draft", "review", "published"],
        transitions=[
            ("draft", "review", "submit"),
            ("review", "published", "approve"),
            ("review", "draft", "reject"),
            ("published", "draft", "unpublish")
        ],
        initial="draft"
    )
    
    sm.start()
    sm.send("submit")
    sm.send("approve")
    
    print(f"\n当前状态: {sm.current_state}")
    
    # 保存状态
    saved = sm.save_state()
    print(f"\n保存的状态:\n{saved}")
    
    # 重置并恢复
    sm.reset()
    print(f"\n重置后状态: {sm.current_state}")
    
    sm.load_state(saved)
    print(f"\n恢复后状态: {sm.current_state}")


def example_tcp_state_machine():
    """TCP状态机示例"""
    print("\n" + "=" * 60)
    print("示例8: TCP连接状态机（简化版）")
    print("=" * 60)
    
    tcp = create_tcp_fsm()
    tcp.start()
    
    print(f"\n初始状态: {tcp.current_state}")
    
    # 建立连接
    tcp.send("open")
    print(f"open() -> {tcp.current_state}")
    
    tcp.send("send_syn")
    print(f"send_syn() -> {tcp.current_state}")
    
    tcp.send("receive_syn_ack")
    print(f"receive_syn_ack() -> {tcp.current_state}")
    
    # 关闭连接
    tcp.send("close")
    print(f"close() -> {tcp.current_state}")
    
    tcp.send("receive_ack")
    print(f"receive_ack() -> {tcp.current_state}")
    
    tcp.send("receive_fin")
    print(f"receive_fin() -> {tcp.current_state}")
    
    tcp.send("timeout")
    print(f"timeout() -> {tcp.current_state}")


def main():
    """运行所有示例"""
    example_basic_state_machine()
    example_with_callbacks()
    example_with_guards()
    example_builder_pattern()
    example_templates()
    example_visualization()
    example_persistence()
    example_tcp_state_machine()
    
    print("\n" + "=" * 60)
    print("所有示例运行完成!")
    print("=" * 60)


if __name__ == "__main__":
    main()