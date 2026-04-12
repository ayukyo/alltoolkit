#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""AllToolkit Socket Utils - Basic Usage Examples

演示 socket_utils 模块的基本用法。
"""

import sys
import os

# 添加父目录到路径 (go up two levels from examples/ to AllToolkit/Python/)
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mod import (
    TCPClient, TCPServer, UDPClient,
    SocketConfig, ConnectionPool,
    create_socket, get_local_ip, get_hostname,
    is_port_open, scan_ports,
    send_length_prefixed, recv_length_prefixed,
    send_json, recv_json,
    SocketProtocol, SocketFamily
)


def example_1_basic_socket():
    """示例 1: 基本套接字创建"""
    print("=" * 60)
    print("示例 1: 基本套接字创建")
    print("=" * 60)
    
    # 创建默认 TCP 套接字
    sock = create_socket(timeout=10.0)
    print(f"✓ 创建 TCP 套接字：family={sock.family}, type={sock.type}")
    sock.close()
    
    # 创建 UDP 套接字
    sock = create_socket(protocol=SocketProtocol.UDP)
    print(f"✓ 创建 UDP 套接字：type={sock.type}")
    sock.close()
    
    # 创建 IPv6 套接字
    sock = create_socket(family=SocketFamily.IPv6)
    print(f"✓ 创建 IPv6 套接字：family={sock.family}")
    sock.close()
    
    print()


def example_2_network_info():
    """示例 2: 网络信息查询"""
    print("=" * 60)
    print("示例 2: 网络信息查询")
    print("=" * 60)
    
    # 获取本地 IP
    ip = get_local_ip()
    print(f"✓ 本地 IP: {ip}")
    
    # 获取主机名
    hostname = get_hostname()
    print(f"✓ 主机名：{hostname}")
    
    # 检查端口
    port_80 = is_port_open('127.0.0.1', 80, timeout=1.0)
    print(f"✓ 端口 80 开放：{port_80}")
    
    # 扫描端口
    results = scan_ports('127.0.0.1', [22, 80, 443, 8080], timeout=0.5)
    print("✓ 端口扫描结果:")
    for port, is_open in results.items():
        status = "开放" if is_open else "关闭"
        print(f"  - 端口 {port}: {status}")
    
    print()


def example_3_tcp_client_server():
    """示例 3: TCP 客户端和服务器"""
    print("=" * 60)
    print("示例 3: TCP 客户端和服务器")
    print("=" * 60)
    
    import threading
    import time
    
    received_messages = []
    
    # 简单的回显服务器处理器
    def echo_handler(client_sock, client_addr):
        try:
            while True:
                data = client_sock.recv(1024)
                if not data:
                    break
                received_messages.append(data.decode('utf-8'))
                client_sock.sendall(b"ECHO: " + data)
        except Exception:
            pass
        finally:
            client_sock.close()
    
    # 启动服务器
    server = TCPServer('127.0.0.1', 18888, backlog=5)
    server.set_client_handler(echo_handler)
    server.start()
    print("✓ 服务器启动在 127.0.0.1:18888")
    
    def run_server():
        while server.running:
            try:
                client_sock, client_addr = server.accept_one(timeout=1.0)
                threading.Thread(
                    target=echo_handler,
                    args=(client_sock, client_addr),
                    daemon=True
                ).start()
            except TimeoutError:
                continue
            except Exception:
                break
    
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()
    time.sleep(0.5)
    
    # 客户端连接
    with TCPClient(SocketConfig(host='127.0.0.1', port=18888, timeout=5.0)) as client:
        client.connect()
        print("✓ 客户端已连接")
        
        # 发送消息
        messages = ["Hello", "World", "测试中文"]
        for msg in messages:
            client.send(msg)
            response = client.recv(1024).decode('utf-8')
            print(f"✓ 发送：'{msg}' -> 接收：'{response}'")
        
        # 获取统计信息
        stats = client.get_stats()
        print(f"✓ 统计：发送={stats.bytes_sent}字节，接收={stats.bytes_received}字节")
    
    server.stop()
    time.sleep(0.5)
    print()


def example_4_udp_client():
    """示例 4: UDP 客户端"""
    print("=" * 60)
    print("示例 4: UDP 客户端")
    print("=" * 60)
    
    # 创建两个 UDP 套接字进行通信
    sender = UDPClient(SocketConfig(timeout=2.0))
    sender.bind('127.0.0.1', 19991)
    print(f"✓ 发送方绑定到 {sender.sock.getsockname()}")
    
    receiver = UDPClient(SocketConfig(timeout=2.0))
    receiver.bind('127.0.0.1', 19992)
    print(f"✓ 接收方绑定到 {receiver.sock.getsockname()}")
    
    # 发送数据
    test_data = "UDP 测试消息".encode('utf-8')
    sender.send_to(test_data, ('127.0.0.1', 19992))
    print(f"✓ 发送：{test_data}")
    
    # 接收数据
    data, addr = receiver.recv_from(1024)
    print(f"✓ 接收：{data} 来自 {addr}")
    
    sender.close()
    receiver.close()
    print()


def example_5_connection_pool():
    """示例 5: 连接池"""
    print("=" * 60)
    print("示例 5: 连接池")
    print("=" * 60)
    
    import threading
    import time
    
    # 启动一个简单的服务器
    def dummy_handler(client_sock, client_addr):
        try:
            while True:
                data = client_sock.recv(1)
                if not data:
                    break
        except Exception:
            pass
        finally:
            client_sock.close()
    
    server = TCPServer('127.0.0.1', 17777, backlog=10)
    server.set_client_handler(dummy_handler)
    server.start()
    
    def run_server():
        while server.running:
            try:
                client_sock, client_addr = server.accept_one(timeout=1.0)
                threading.Thread(
                    target=dummy_handler,
                    args=(client_sock, client_addr),
                    daemon=True
                ).start()
            except TimeoutError:
                continue
            except Exception:
                break
    
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()
    time.sleep(0.5)
    
    # 使用连接池
    with ConnectionPool('127.0.0.1', 17777, max_connections=3) as pool:
        print(f"✓ 连接池创建：最大连接数=3")
        
        # 获取连接
        with pool.connection() as sock:
            print(f"✓ 从池中获取连接")
            print(f"  池状态：可用={pool.available}, 使用中={pool.in_use}")
            sock.sendall(b"test")
        
        print(f"✓ 连接返回池中")
        print(f"  池状态：可用={pool.available}, 使用中={pool.in_use}")
    
    server.stop()
    print()


def example_6_length_prefixed_protocol():
    """示例 6: 长度前缀协议"""
    print("=" * 60)
    print("示例 6: 长度前缀协议")
    print("=" * 60)
    
    import threading
    import time
    
    # 服务器：接收并回显长度前缀数据
    def handler(client_sock, client_addr):
        try:
            while True:
                data = recv_length_prefixed(client_sock)
                if not data:
                    break
                send_length_prefixed(client_sock, b"ECHO: " + data)
        except Exception:
            pass
        finally:
            client_sock.close()
    
    server = TCPServer('127.0.0.1', 16666, backlog=5)
    server.set_client_handler(handler)
    server.start()
    
    def run_server():
        while server.running:
            try:
                client_sock, client_addr = server.accept_one(timeout=1.0)
                threading.Thread(
                    target=handler,
                    args=(client_sock, client_addr),
                    daemon=True
                ).start()
            except TimeoutError:
                continue
            except Exception:
                break
    
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()
    time.sleep(0.5)
    
    # 客户端
    sock = create_socket(timeout=5.0)
    sock.connect(('127.0.0.1', 16666))
    
    # 发送长度前缀消息
    messages = ["短消息".encode('utf-8'), "这是一个比较长的消息用来测试".encode('utf-8'), b"Third message"]
    for msg in messages:
        send_length_prefixed(sock, msg)
        response = recv_length_prefixed(sock)
        print(f"✓ 发送：{msg} -> 接收：{response}")
    
    sock.close()
    server.stop()
    print()


def example_7_json_over_sockets():
    """示例 7: JSON over Sockets"""
    print("=" * 60)
    print("示例 7: JSON over Sockets")
    print("=" * 60)
    
    import threading
    import time
    
    # 服务器：接收 JSON 并回显
    def json_handler(client_sock, client_addr):
        try:
            while True:
                data = recv_json(client_sock)
                # 处理 JSON 数据
                data['received'] = True
                send_json(client_sock, data)
        except Exception:
            pass
        finally:
            client_sock.close()
    
    server = TCPServer('127.0.0.1', 15555, backlog=5)
    server.set_client_handler(json_handler)
    server.start()
    
    def run_server():
        while server.running:
            try:
                client_sock, client_addr = server.accept_one(timeout=1.0)
                threading.Thread(
                    target=json_handler,
                    args=(client_sock, client_addr),
                    daemon=True
                ).start()
            except TimeoutError:
                continue
            except Exception:
                break
    
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()
    time.sleep(0.5)
    
    # 客户端
    sock = create_socket(timeout=5.0)
    sock.connect(('127.0.0.1', 15555))
    
    # 发送 JSON 数据
    test_data = {
        "name": "Alice",
        "age": 30,
        "city": "上海",
        "hobbies": ["读书", "编程", "音乐"]
    }
    
    print(f"✓ 发送 JSON: {test_data}")
    send_json(sock, test_data)
    
    response = recv_json(sock)
    print(f"✓ 接收 JSON: {response}")
    
    sock.close()
    server.stop()
    print()


def main():
    """运行所有示例"""
    print("\n")
    print("╔" + "═" * 68 + "╗")
    print("║" + " " * 15 + "AllToolkit Socket Utils 示例" + " " * 21 + "║")
    print("╚" + "═" * 68 + "╝")
    print("\n")
    
    try:
        example_1_basic_socket()
        example_2_network_info()
        example_3_tcp_client_server()
        example_4_udp_client()
        example_5_connection_pool()
        example_6_length_prefixed_protocol()
        example_7_json_over_sockets()
        
        print("=" * 60)
        print("✓ 所有示例运行完成!")
        print("=" * 60)
        
    except Exception as e:
        print(f"✗ 示例运行出错：{e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
