#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Load Balancer Demo - 演示各种负载均衡策略

运行: cd Python/load_balancer_utils && python examples/demo.py
"""

import sys
import os
import time
import random

# Add current directory to path (mod.py is in the same directory)
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    LoadBalancer,
    LoadBalancerStrategy,
    ServerState,
    HealthChecker,
)


def print_separator(title: str):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print('='*60)


def demo_round_robin():
    """演示轮询策略"""
    print_separator("轮询策略 (Round Robin)")
    
    lb = LoadBalancer(strategy=LoadBalancerStrategy.ROUND_ROBIN)
    lb.add_server("server-1", "192.168.1.1:8080")
    lb.add_server("server-2", "192.168.1.2:8080")
    lb.add_server("server-3", "192.168.1.3:8080")
    
    print("\n服务器列表:")
    for s in lb.servers:
        print(f"  - {s.id}: {s.target}")
    
    print("\n模拟 10 次请求:")
    for i in range(10):
        server = lb.select()
        print(f"  请求 {i+1:2d} -> {server.id}")
    
    print("\n✓ 轮询按顺序依次分配")


def demo_weighted_round_robin():
    """演示加权轮询策略"""
    print_separator("加权轮询策略 (Weighted Round Robin)")
    
    lb = LoadBalancer(strategy=LoadBalancerStrategy.WEIGHTED_ROUND_ROBIN)
    lb.add_server("high", "192.168.1.1:8080", weight=5)
    lb.add_server("medium", "192.168.1.2:8080", weight=3)
    lb.add_server("low", "192.168.1.3:8080", weight=1)
    
    print("\n服务器列表 (权重):")
    for s in lb.servers:
        print(f"  - {s.id}: {s.target} (weight={s.weight})")
    
    print("\n模拟 18 次请求 (权重之和):")
    counts = {}
    for i in range(18):
        server = lb.select()
        counts[server.id] = counts.get(server.id, 0) + 1
    
    for server_id, count in sorted(counts.items()):
        weight = lb.get_server(server_id).weight
        print(f"  {server_id}: {count} 次 (权重={weight})")
    
    print("\n✓ 加权轮询按权重比例分配请求")


def demo_least_connections():
    """演示最少连接策略"""
    print_separator("最少连接策略 (Least Connections)")
    
    lb = LoadBalancer(strategy=LoadBalancerStrategy.LEAST_CONNECTIONS)
    lb.add_server("server-1", "192.168.1.1:8080")
    lb.add_server("server-2", "192.168.1.2:8080")
    lb.add_server("server-3", "192.168.1.3:8080")
    
    print("\n模拟连接分配:")
    
    # 模拟连接
    connections = []
    for i in range(5):
        server = lb.select()
        ctx = lb.connection(server)
        ctx.__enter__()
        connections.append((server, ctx))
        print(f"  新连接 -> {server.id} (active={server.stats.active_connections})")
    
    print("\n当前连接数:")
    for s in lb.servers:
        print(f"  {s.id}: {s.stats.active_connections} 个连接")
    
    # 关闭一些连接
    print("\n关闭 2 个连接...")
    for _ in range(2):
        server, ctx = connections.pop()
        ctx.__exit__(None, None, None)
        print(f"  关闭连接: {server.id}")
    
    print("\n新连接会分配给连接数最少的服务器:")
    server = lb.select()
    print(f"  选择: {server.id} (active={server.stats.active_connections})")
    
    # 清理
    for server, ctx in connections:
        ctx.__exit__(None, None, None)
    
    print("\n✓ 最少连接策略动态分配到最空闲的服务器")


def demo_random():
    """演示随机策略"""
    print_separator("随机策略 (Random)")
    
    lb = LoadBalancer(strategy=LoadBalancerStrategy.RANDOM)
    lb.add_server("server-1", "192.168.1.1:8080")
    lb.add_server("server-2", "192.168.1.2:8080")
    lb.add_server("server-3", "192.168.1.3:8080")
    
    print("\n模拟 1000 次请求:")
    counts = {}
    for _ in range(1000):
        server = lb.select()
        counts[server.id] = counts.get(server.id, 0) + 1
    
    for server_id, count in sorted(counts.items()):
        pct = count / 10
        bar = "█" * int(pct / 2)
        print(f"  {server_id}: {count:4d} ({pct:.1f}%) {bar}")
    
    print("\n✓ 随机策略均匀分布请求")


def demo_weighted_random():
    """演示加权随机策略"""
    print_separator("加权随机策略 (Weighted Random)")
    
    lb = LoadBalancer(strategy=LoadBalancerStrategy.WEIGHTED_RANDOM)
    lb.add_server("high", "192.168.1.1:8080", weight=5)
    lb.add_server("medium", "192.168.1.2:8080", weight=3)
    lb.add_server("low", "192.168.1.3:8080", weight=1)
    
    print("\n服务器权重:")
    for s in lb.servers:
        print(f"  - {s.id}: weight={s.weight}")
    
    print("\n模拟 1000 次请求:")
    counts = {}
    for _ in range(1000):
        server = lb.select()
        counts[server.id] = counts.get(server.id, 0) + 1
    
    total_weight = sum(s.weight for s in lb.servers)
    for s in lb.servers:
        count = counts.get(s.id, 0)
        expected_pct = s.weight / total_weight * 100
        actual_pct = count / 10
        bar = "█" * int(actual_pct / 2)
        print(f"  {s.id}: {count:4d} ({actual_pct:.1f}%) [期望 {expected_pct:.1f}%] {bar}")
    
    print("\n✓ 加权随机按权重概率分配")


def demo_ip_hash():
    """演示 IP 哈希策略"""
    print_separator("IP 哈希策略 (IP Hash)")
    
    lb = LoadBalancer(strategy=LoadBalancerStrategy.IP_HASH)
    lb.add_server("server-1", "192.168.1.1:8080")
    lb.add_server("server-2", "192.168.1.2:8080")
    lb.add_server("server-3", "192.168.1.3:8080")
    
    print("\n客户端 IP 路由映射:")
    
    client_ips = [
        "192.168.1.100",
        "192.168.1.101",
        "192.168.1.102",
        "10.0.0.1",
        "10.0.0.2",
        "172.16.0.1",
    ]
    
    mapping = {}
    for ip in client_ips:
        server = lb.select(key=ip)
        mapping[ip] = server.id
        print(f"  {ip} -> {server.id}")
    
    print("\n验证一致性 (相同 IP 总是路由到同一服务器):")
    for ip in client_ips:
        server1 = lb.select(key=ip)
        server2 = lb.select(key=ip)
        server3 = lb.select(key=ip)
        consistent = (server1.id == server2.id == server3.id)
        status = "✓" if consistent else "✗"
        print(f"  {ip}: {server1.id} -> {server2.id} -> {server3.id} {status}")
    
    print("\n✓ IP 哈希确保相同客户端始终路由到同一服务器")


def demo_health_check():
    """演示健康检查"""
    print_separator("健康检查 (Health Checking)")
    
    class MockHealthChecker(HealthChecker):
        def __init__(self, failing_servers):
            self.failing_servers = failing_servers
        
        def check(self, server):
            # 模拟某些服务器健康检查失败
            return server.id not in self.failing_servers
    
    health_checker = MockHealthChecker(failing_servers={"server-2"})
    lb = LoadBalancer(health_checker=health_checker)
    lb.add_server("server-1", "192.168.1.1:8080")
    lb.add_server("server-2", "192.168.1.2:8080")
    lb.add_server("server-3", "192.168.1.3:8080")
    
    print("\n服务器状态:")
    for s in lb.servers:
        print(f"  - {s.id}: {s.state.name}")
    
    print("\n执行健康检查...")
    results = lb.run_health_checks()
    
    print("\n健康检查结果:")
    for server_id, is_healthy in results.items():
        status = "健康" if is_healthy else "不健康"
        print(f"  - {server_id}: {status}")
    
    print("\n更新后的服务器状态:")
    for s in lb.servers:
        print(f"  - {s.id}: {s.state.name}")
    
    print("\n选择服务器 (跳过不健康服务器):")
    for i in range(6):
        server = lb.select()
        print(f"  请求 {i+1} -> {server.id}")
    
    print("\n✓ 健康检查自动排除故障服务器")


def demo_statistics():
    """演示统计信息"""
    print_separator("统计信息 (Statistics)")
    
    lb = LoadBalancer(strategy=LoadBalancerStrategy.ROUND_ROBIN)
    lb.add_server("server-1", "192.168.1.1:8080")
    lb.add_server("server-2", "192.168.1.2:8080")
    lb.add_server("server-3", "192.168.1.3:8080")
    
    print("\n模拟 100 次请求:")
    for i in range(100):
        server = lb.select()
        with lb.connection(server):
            # 模拟请求处理
            response_time = random.uniform(10, 100)
            time.sleep(0.001)  # 模拟处理时间
            
            # 随机失败 5% 的请求
            if random.random() < 0.05:
                lb.record_failure(server)
            else:
                lb.record_success(server, response_time)
    
    stats = lb.get_stats()
    
    print(f"\n负载均衡器统计:")
    print(f"  策略: {stats['strategy']}")
    print(f"  总服务器: {stats['total_servers']}")
    print(f"  健康服务器: {stats['healthy_servers']}")
    print(f"  总请求数: {stats['total_requests']}")
    print(f"  成功请求: {stats['successful_requests']}")
    print(f"  失败请求: {stats['failed_requests']}")
    print(f"  成功率: {stats['success_rate']:.2f}%")
    
    print(f"\n各服务器统计:")
    for server_id, s in stats['servers'].items():
        print(f"  {server_id}:")
        print(f"    总请求: {s['total_requests']}")
        print(f"    成功率: {s['success_rate']:.2f}%")
        print(f"    平均响应时间: {s['avg_response_time_ms']:.2f}ms")
    
    print("\n✓ 统计信息可用于监控和告警")


def demo_server_management():
    """演示服务器管理"""
    print_separator("服务器管理 (Server Management)")
    
    lb = LoadBalancer()
    lb.add_server("server-1", "192.168.1.1:8080")
    lb.add_server("server-2", "192.168.1.2:8080")
    lb.add_server("server-3", "192.168.1.3:8080")
    
    print("\n初始服务器列表:")
    for s in lb.servers:
        print(f"  - {s.id}: {s.target} [{s.state.name}]")
    
    print("\n标记 server-2 为不健康...")
    lb.mark_server_unhealthy("server-2")
    
    print("\n当前可用服务器:")
    for s in lb.healthy_servers:
        print(f"  - {s.id}")
    
    print("\n排空 server-3 (不接受新连接)...")
    lb.drain_server("server-3")
    
    print("\n服务器状态:")
    for s in lb.servers:
        print(f"  - {s.id}: {s.state.name}")
    
    print("\n修改 server-1 权重为 5...")
    lb.set_server_weight("server-1", 5)
    print(f"  {lb.get_server('server-1').id} weight = {lb.get_server('server-1').weight}")
    
    print("\n移除 server-3...")
    lb.remove_server("server-3")
    
    print("\n最终服务器列表:")
    for s in lb.servers:
        print(f"  - {s.id}: {s.target} [{s.state.name}] (weight={s.weight})")
    
    print("\n✓ 灵活的服务器管理支持动态扩缩容")


def main():
    print("\n" + "=" * 60)
    print("  负载均衡器演示程序")
    print("  Load Balancer Demo")
    print("=" * 60)
    
    demo_round_robin()
    demo_weighted_round_robin()
    demo_least_connections()
    demo_random()
    demo_weighted_random()
    demo_ip_hash()
    demo_health_check()
    demo_statistics()
    demo_server_management()
    
    print_separator("演示完成")
    print("\n  所有演示已完成！")
    print("  查看源码了解更多 API 细节")
    print("\n" + "=" * 60 + "\n")


if __name__ == "__main__":
    main()