"""
State Machine Utils 测试用例

测试有限状态机工具的所有核心功能。
"""

import unittest
import json
from mod import (
    State, StateMachine, StateMachineBuilder, StateMachineContext,
    StateType, Transition, Event, ParallelStateMachine,
    create_simple_fsm, validate_state_machine, fsm_to_json, json_to_fsm,
    get_state_diagram, simulate_fsm,
    create_turnstile_fsm, create_traffic_light_fsm, create_order_fsm, create_tcp_fsm
)


class TestState(unittest.TestCase):
    """测试 State 类"""
    
    def test_state_creation(self):
        """测试状态创建"""
        state = State("idle")
        self.assertEqual(state.name, "idle")
        self.assertEqual(state.state_type, StateType.BASIC)
    
    def test_state_equality(self):
        """测试状态相等性"""
        state1 = State("idle")
        state2 = State("idle")
        state3 = State("running")
        
        self.assertEqual(state1, state2)
        self.assertNotEqual(state1, state3)
    
    def test_state_hash(self):
        """测试状态哈希"""
        state1 = State("idle")
        state2 = State("idle")
        
        # 同名状态应该有相同的哈希值
        self.assertEqual(hash(state1), hash(state2))
        
        # 可以作为集合元素
        states = {state1, state2}
        self.assertEqual(len(states), 1)
    
    def test_state_with_callbacks(self):
        """测试带回调的状态"""
        entered = []
        exited = []
        
        def on_enter():
            entered.append("entered")
        
        def on_exit():
            exited.append("exited")
        
        state = State("test", on_enter=on_enter, on_exit=on_exit)
        self.assertIsNotNone(state.on_enter)
        self.assertIsNotNone(state.on_exit)
    
    def test_composite_state(self):
        """测试复合状态"""
        parent = State("parent")
        child1 = State("child1")
        child2 = State("child2")
        
        parent.add_child(child1, is_initial=True)
        parent.add_child(child2)
        
        self.assertEqual(parent.state_type, StateType.COMPOSITE)
        self.assertEqual(len(parent.children), 2)
        self.assertEqual(parent.initial_child, child1)
        self.assertEqual(child1.parent, parent)
        self.assertEqual(child2.parent, parent)


class TestStateMachine(unittest.TestCase):
    """测试 StateMachine 类"""
    
    def setUp(self):
        """设置测试状态机"""
        self.idle = State("idle")
        self.running = State("running")
        self.paused = State("paused")
        
        self.sm = StateMachine(initial_state=self.idle)
        self.sm.add_state(self.running)
        self.sm.add_state(self.paused)
        
        self.sm.add_transition(self.idle, self.running, "start")
        self.sm.add_transition(self.running, self.paused, "pause")
        self.sm.add_transition(self.paused, self.running, "resume")
        self.sm.add_transition(self.running, self.idle, "stop")
        self.sm.add_transition(self.paused, self.idle, "stop")
    
    def test_initialization(self):
        """测试初始化"""
        self.assertEqual(len(self.sm.states), 3)
        self.assertEqual(len(self.sm.transitions), 5)
        self.assertEqual(self.sm.initial_state, self.idle)
    
    def test_start(self):
        """测试启动"""
        self.sm.start()
        self.assertEqual(self.sm.current_state, self.idle)
        self.assertTrue(self.sm.is_in_state(self.idle))
    
    def test_send_event(self):
        """测试发送事件"""
        self.sm.start()
        
        # idle -> running
        result = self.sm.send("start")
        self.assertTrue(result)
        self.assertEqual(self.sm.current_state, self.running)
        
        # running -> paused
        result = self.sm.send("pause")
        self.assertTrue(result)
        self.assertEqual(self.sm.current_state, self.paused)
        
        # paused -> running
        result = self.sm.send("resume")
        self.assertTrue(result)
        self.assertEqual(self.sm.current_state, self.running)
        
        # running -> idle
        result = self.sm.send("stop")
        self.assertTrue(result)
        self.assertEqual(self.sm.current_state, self.idle)
    
    def test_invalid_event(self):
        """测试无效事件"""
        self.sm.start()
        result = self.sm.send("invalid_event")
        self.assertFalse(result)
        self.assertEqual(self.sm.current_state, self.idle)
    
    def test_guard_condition(self):
        """测试守卫条件"""
        can_start = [True]
        
        def guard():
            return can_start[0]
        
        sm = StateMachine(initial_state=self.idle)
        sm.add_state(self.running)
        sm.add_transition(self.idle, self.running, "start", guard=guard)
        sm.start()
        
        # 守卫通过
        result = sm.send("start")
        self.assertTrue(result)
        
        # 重置并测试守卫失败
        sm.reset()
        sm.start()
        can_start[0] = False
        result = sm.send("start")
        self.assertFalse(result)
    
    def test_transition_action(self):
        """测试转换动作"""
        actions = []
        
        def action():
            actions.append("action_executed")
        
        sm = StateMachine(initial_state=self.idle)
        sm.add_state(self.running)
        sm.add_transition(self.idle, self.running, "start", action=action)
        sm.start()
        sm.send("start")
        
        self.assertEqual(actions, ["action_executed"])
    
    def test_state_callbacks(self):
        """测试状态回调"""
        entered = []
        exited = []
        
        def on_enter_running():
            entered.append("running")
        
        def on_exit_running():
            exited.append("running")
        
        running = State("running", on_enter=on_enter_running, on_exit=on_exit_running)
        
        sm = StateMachine(initial_state=self.idle)
        sm.add_state(running)
        sm.add_transition(self.idle, running, "start")
        sm.add_transition(running, self.idle, "stop")
        
        sm.start()
        sm.send("start")
        self.assertEqual(entered, ["running"])
        
        sm.send("stop")
        self.assertEqual(exited, ["running"])
    
    def test_can_transition(self):
        """测试转换检查"""
        self.sm.start()
        
        self.assertTrue(self.sm.can_transition("start"))
        self.assertFalse(self.sm.can_transition("pause"))
        self.assertFalse(self.sm.can_transition("invalid"))
    
    def test_get_available_events(self):
        """测试获取可用事件"""
        self.sm.start()
        
        events = self.sm.get_available_events()
        self.assertEqual(events, ["start"])
        
        self.sm.send("start")
        events = self.sm.get_available_events()
        self.assertIn("pause", events)
        self.assertIn("stop", events)
    
    def test_reset(self):
        """测试重置"""
        self.sm.start()
        self.sm.send("start")
        
        self.sm.reset()
        
        self.assertIsNone(self.sm.current_state)
        self.assertEqual(len(self.sm.context.active_states), 0)
        self.assertEqual(self.sm._transition_count, 0)
    
    def test_save_load_state(self):
        """测试状态保存和加载"""
        self.sm.start()
        self.sm.send("start")
        
        # 保存状态
        saved = self.sm.save_state()
        self.assertIn("running", saved)
        
        # 重置并加载
        self.sm.reset()
        self.sm.load_state(saved)
        
        self.assertEqual(self.sm.current_state, self.running)
    
    def test_history(self):
        """测试转换历史"""
        self.sm.start()
        self.sm.send("start")
        self.sm.send("pause")
        
        history = self.sm.get_history()
        self.assertEqual(len(history), 2)
        self.assertEqual(history[0], ("start", "idle", "running"))
        self.assertEqual(history[1], ("pause", "running", "paused"))
    
    def test_stats(self):
        """测试统计信息"""
        self.sm.start()
        self.sm.send("start")
        self.sm.send("pause")
        
        stats = self.sm.stats
        self.assertEqual(stats["state_count"], 3)
        self.assertEqual(stats["transition_count"], 5)
        self.assertEqual(stats["total_transitions"], 2)
        self.assertEqual(stats["total_events"], 2)
    
    def test_async_events(self):
        """测试异步事件队列"""
        self.sm.start()
        
        self.sm.send_async("start")
        self.sm.send_async("pause")
        
        self.assertEqual(len(self.sm.context.event_queue), 2)
        
        processed = self.sm.process_queue()
        self.assertEqual(processed, 2)
        self.assertEqual(self.sm.current_state, self.paused)


class TestStateMachineBuilder(unittest.TestCase):
    """测试 StateMachineBuilder 类"""
    
    def test_fluent_api(self):
        """测试流式API"""
        sm = (StateMachineBuilder("TestSM")
              .state("idle")
              .state("running")
              .state("paused")
              .initial("idle")
              .transition("idle", "running", "start")
              .transition("running", "paused", "pause")
              .transition("paused", "running", "resume")
              .transition("running", "idle", "stop")
              .build())
        
        sm.start()
        self.assertEqual(sm.current_state.name, "idle")
        
        sm.send("start")
        self.assertEqual(sm.current_state.name, "running")
        
        sm.send("pause")
        self.assertEqual(sm.current_state.name, "paused")
    
    def test_builder_without_initial(self):
        """测试缺少初始状态"""
        builder = StateMachineBuilder().state("idle")
        
        with self.assertRaises(ValueError):
            builder.build()


class TestStateMachineContext(unittest.TestCase):
    """测试 StateMachineContext 类"""
    
    def test_data_operations(self):
        """测试数据操作"""
        ctx = StateMachineContext()
        
        ctx.set_data("key1", "value1")
        ctx.set_data("key2", 123)
        
        self.assertEqual(ctx.get_data("key1"), "value1")
        self.assertEqual(ctx.get_data("key2"), 123)
        self.assertIsNone(ctx.get_data("nonexistent"))
        self.assertEqual(ctx.get_data("nonexistent", "default"), "default")
    
    def test_serialization(self):
        """测试序列化"""
        idle = State("idle")
        running = State("running")
        
        ctx = StateMachineContext()
        ctx.active_states.add(idle)
        ctx.history["previous"] = running
        ctx.set_data("test", "value")
        
        data = ctx.to_dict()
        
        self.assertIn("idle", data["active_states"])
        self.assertEqual(data["history"]["previous"], "running")
        self.assertEqual(data["data"]["test"], "value")
        
        # 反序列化
        state_map = {"idle": idle, "running": running}
        ctx2 = StateMachineContext.from_dict(data, state_map)
        
        self.assertIn(idle, ctx2.active_states)
        self.assertEqual(ctx2.history["previous"], running)
        self.assertEqual(ctx2.get_data("test"), "value")


class TestParallelStateMachine(unittest.TestCase):
    """测试 ParallelStateMachine 类"""
    
    def test_parallel_regions(self):
        """测试并行区域"""
        # 创建两个独立的状态机
        sm1 = create_simple_fsm(
            states=["off1", "on1"],
            transitions=[("off1", "on1", "toggle"), ("on1", "off1", "toggle")],
            initial="off1"
        )
        sm1.name = "switch1"
        
        sm2 = create_simple_fsm(
            states=["off2", "on2"],
            transitions=[("off2", "on2", "toggle"), ("on2", "off2", "toggle")],
            initial="off2"
        )
        sm2.name = "switch2"
        
        # 创建并行状态机
        parallel = ParallelStateMachine()
        parallel.add_region(sm1).add_region(sm2)
        parallel.start()
        
        # 检查初始状态
        states = parallel.get_states()
        self.assertEqual(states["switch1"].name, "off1")
        self.assertEqual(states["switch2"].name, "off2")
        
        # 发送事件
        results = parallel.send("toggle")
        self.assertTrue(results["switch1"])
        self.assertTrue(results["switch2"])
        
        states = parallel.get_states()
        self.assertEqual(states["switch1"].name, "on1")
        self.assertEqual(states["switch2"].name, "on2")


class TestUtilityFunctions(unittest.TestCase):
    """测试工具函数"""
    
    def test_create_simple_fsm(self):
        """测试快速创建函数"""
        sm = create_simple_fsm(
            states=["a", "b", "c"],
            transitions=[
                ("a", "b", "next"),
                ("b", "c", "next"),
                ("c", "a", "reset")
            ],
            initial="a"
        )
        
        sm.start()
        self.assertEqual(sm.current_state.name, "a")
        
        sm.send("next")
        self.assertEqual(sm.current_state.name, "b")
        
        sm.send("next")
        self.assertEqual(sm.current_state.name, "c")
    
    def test_validate_state_machine(self):
        """测试验证函数"""
        # 有效状态机
        sm = create_simple_fsm(
            states=["a", "b"],
            transitions=[("a", "b", "go")],
            initial="a"
        )
        errors = validate_state_machine(sm)
        # 注意：b 是最终状态（无出转换），这不算错误
        self.assertEqual(len(errors), 0)
        
        # 带孤立状态的无效状态机
        sm2 = StateMachine(initial_state=State("a"))
        sm2.add_state(State("isolated"))
        
        errors = validate_state_machine(sm2)
        self.assertIn("Unreachable state: isolated", errors)
    
    def test_fsm_to_json(self):
        """测试JSON导出"""
        sm = create_simple_fsm(
            states=["a", "b"],
            transitions=[("a", "b", "go")],
            initial="a"
        )
        
        json_str = fsm_to_json(sm)
        data = json.loads(json_str)
        
        self.assertEqual(data["states"], ["a", "b"])
        self.assertEqual(data["initial_state"], "a")
        self.assertEqual(len(data["transitions"]), 1)
    
    def test_json_to_fsm(self):
        """测试JSON导入"""
        json_str = '''{
            "name": "TestSM",
            "states": ["a", "b", "c"],
            "initial_state": "a",
            "transitions": [
                {"from": "a", "to": "b", "event": "go"},
                {"from": "b", "to": "c", "event": "go"}
            ]
        }'''
        
        sm = json_to_fsm(json_str)
        
        sm.start()
        self.assertEqual(sm.current_state.name, "a")
        
        sm.send("go")
        self.assertEqual(sm.current_state.name, "b")
        
        sm.send("go")
        self.assertEqual(sm.current_state.name, "c")
    
    def test_get_state_diagram(self):
        """测试状态图生成"""
        sm = create_simple_fsm(
            states=["a", "b"],
            transitions=[("a", "b", "go")],
            initial="a"
        )
        
        diagram = get_state_diagram(sm)
        self.assertIn("stateDiagram-v2", diagram)
        self.assertIn("a --> b", diagram)
    
    def test_simulate_fsm(self):
        """测试模拟函数"""
        sm = create_simple_fsm(
            states=["a", "b", "c"],
            transitions=[
                ("a", "b", "go"),
                ("b", "c", "go"),
                ("c", "a", "reset")
            ],
            initial="a"
        )
        
        history = simulate_fsm(sm, ["go", "go", "reset", "invalid", "go"])
        
        self.assertEqual(len(history), 6)  # Initial + 5 events
        self.assertIn("Initial: a", history[0])
        self.assertIn("go -> b", history[1])
        self.assertIn("go -> c", history[2])
        self.assertIn("reset -> a", history[3])
        self.assertIn("invalid (no transition)", history[4])


class TestTemplates(unittest.TestCase):
    """测试预定义模板"""
    
    def test_turnstile_fsm(self):
        """测试旋转门状态机"""
        sm = create_turnstile_fsm()
        sm.start()
        
        self.assertEqual(sm.current_state.name, "locked")
        
        sm.send("coin")
        self.assertEqual(sm.current_state.name, "unlocked")
        
        sm.send("push")
        self.assertEqual(sm.current_state.name, "locked")
    
    def test_traffic_light_fsm(self):
        """测试交通灯状态机"""
        sm = create_traffic_light_fsm()
        sm.start()
        
        self.assertEqual(sm.current_state.name, "red")
        
        sm.send("timer")
        self.assertEqual(sm.current_state.name, "green")
        
        sm.send("timer")
        self.assertEqual(sm.current_state.name, "yellow")
        
        sm.send("timer")
        self.assertEqual(sm.current_state.name, "red")
    
    def test_order_fsm(self):
        """测试订单状态机"""
        sm = create_order_fsm()
        sm.start()
        
        self.assertEqual(sm.current_state.name, "created")
        
        sm.send("pay")
        self.assertEqual(sm.current_state.name, "paid")
        
        sm.send("ship")
        self.assertEqual(sm.current_state.name, "shipped")
        
        sm.send("deliver")
        self.assertEqual(sm.current_state.name, "delivered")
        
        # 测试取消
        sm2 = create_order_fsm()
        sm2.start()
        sm2.send("cancel")
        self.assertEqual(sm2.current_state.name, "cancelled")
    
    def test_tcp_fsm(self):
        """测试TCP状态机"""
        sm = create_tcp_fsm()
        sm.start()
        
        self.assertEqual(sm.current_state.name, "CLOSED")
        
        sm.send("open")
        self.assertEqual(sm.current_state.name, "LISTEN")
        
        sm.send("send_syn")
        self.assertEqual(sm.current_state.name, "SYN_SENT")
        
        sm.send("receive_syn_ack")
        self.assertEqual(sm.current_state.name, "ESTABLISHED")


class TestVisualization(unittest.TestCase):
    """测试可视化功能"""
    
    def test_text_visualization(self):
        """测试文本可视化"""
        sm = create_simple_fsm(
            states=["a", "b"],
            transitions=[("a", "b", "go")],
            initial="a"
        )
        
        text = sm.visualize("text")
        
        self.assertIn("State Machine:", text)
        self.assertIn("States:", text)
        self.assertIn("Current State:", text)
        self.assertIn("Transitions:", text)
    
    def test_mermaid_visualization(self):
        """测试Mermaid可视化"""
        sm = create_simple_fsm(
            states=["a", "b"],
            transitions=[("a", "b", "go")],
            initial="a"
        )
        
        mermaid = sm.visualize("mermaid")
        
        self.assertIn("stateDiagram-v2", mermaid)
        self.assertIn("a --> b", mermaid)
    
    def test_dot_visualization(self):
        """测试DOT可视化"""
        sm = create_simple_fsm(
            states=["a", "b"],
            transitions=[("a", "b", "go")],
            initial="a"
        )
        
        dot = sm.visualize("dot")
        
        self.assertIn("digraph StateMachine", dot)
        self.assertIn("a", dot)
        self.assertIn("b", dot)


class TestEventHandlers(unittest.TestCase):
    """测试事件处理器"""
    
    def test_event_handler_registration(self):
        """测试事件处理器注册"""
        handled_events = []
        
        def handler(event):
            handled_events.append(event.name)
        
        idle = State("idle")
        sm = StateMachine(initial_state=idle)
        sm.on_event("custom_event", handler)
        sm.start()
        
        # 发送未匹配的事件
        sm.send("custom_event")
        
        self.assertEqual(handled_events, ["custom_event"])


class TestComplexScenarios(unittest.TestCase):
    """测试复杂场景"""
    
    def test_vending_machine(self):
        """测试自动售货机状态机"""
        # 状态
        idle = State("idle")
        select = State("select")
        paying = State("paying")
        dispensing = State("dispensing")
        
        # 上下文数据
        context_data = {"balance": 0, "selection": None}
        
        def on_enter_paying():
            print(f"Paying for {context_data['selection']}")
        
        paying.on_enter = on_enter_paying
        
        sm = StateMachine(initial_state=idle)
        sm.add_state(select)
        sm.add_state(paying)
        sm.add_state(dispensing)
        
        sm.add_transition(idle, select, "select")
        sm.add_transition(select, paying, "pay")
        sm.add_transition(paying, dispensing, "confirm")
        sm.add_transition(dispensing, idle, "complete")
        sm.add_transition(select, idle, "cancel")
        sm.add_transition(paying, idle, "cancel")
        
        sm.start()
        
        # 模拟购物流程
        sm.send("select")
        self.assertEqual(sm.current_state, select)
        
        sm.send("pay")
        self.assertEqual(sm.current_state, paying)
        
        sm.send("confirm")
        self.assertEqual(sm.current_state, dispensing)
        
        sm.send("complete")
        self.assertEqual(sm.current_state, idle)
    
    def test_game_state(self):
        """测试游戏状态机"""
        sm = create_simple_fsm(
            states=["menu", "playing", "paused", "game_over"],
            transitions=[
                ("menu", "playing", "start"),
                ("playing", "paused", "pause"),
                ("paused", "playing", "resume"),
                ("playing", "game_over", "die"),
                ("game_over", "menu", "restart"),
                ("game_over", "playing", "continue")
            ],
            initial="menu"
        )
        
        sm.start()
        
        # 开始游戏
        sm.send("start")
        self.assertEqual(sm.current_state.name, "playing")
        
        # 暂停
        sm.send("pause")
        self.assertEqual(sm.current_state.name, "paused")
        
        # 继续
        sm.send("resume")
        self.assertEqual(sm.current_state.name, "playing")
        
        # 死亡
        sm.send("die")
        self.assertEqual(sm.current_state.name, "game_over")
        
        # 重新开始
        sm.send("restart")
        self.assertEqual(sm.current_state.name, "menu")


if __name__ == "__main__":
    unittest.main(verbosity=2)