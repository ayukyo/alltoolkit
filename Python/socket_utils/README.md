# Socket Utils 🔌

**Python 套接字工具模块 - 零依赖，生产就绪**

---

## 📖 概述

`socket_utils` 是一个全面的 Python 套接字工具模块，提供 TCP/UDP 客户端/服务器、连接池、SSL/TLS 支持、长度前缀协议等功能。所有实现均使用 Python 标准库（`socket`、`ssl`、`select` 等），零外部依赖。

### ✨ 特性

- **零依赖** - 仅使用 Python 标准库
- **TCP 客户端/服务器** - 完整的连接管理
- **UDP 客户端** - 数据报通信支持
- **SSL/TLS 支持** - 安全套接字层
- **连接池** - 线程安全的连接复用
- **长度前缀协议** - 可靠的消息边界
- **JSON over Sockets** - 结构化数据传输
- **端口扫描** - 网络探测工具
- **类型安全** - 完整的类型注解
- **生产就绪** - 完整的错误处理和边界检查
- **全面测试** - 100+ 测试用例覆盖所有功能

---

## 📦 安装

无需安装！直接复制 `mod.py` 到你的项目即可使用。

```bash
# 从 AllToolkit 复制
cp AllToolkit/Python/socket_utils/mod.py your_project/

# 或者克隆整个仓库
git clone https://github.com/ayukyo/alltoolkit.git
```

---

## 🚀 快速开始

### TCP 客户端

```python
from mod import TCPClient, SocketConfig

# 创建客户端并连接
client = TCPClient(SocketConfig(host='localhost', port=8080, timeout=10.0))
client.connect()

# 发送和接收数据
client.send(b"Hello, Server!")
response = client.recv(1024)
print(response)

# 关闭连接
client.close()

# 或使用上下文管理器
with TCPClient(SocketConfig(host='localhost', port=8080)) as client:
    client.connect()
    client.send(b"Hello!")
    print(client.recv(1024))
```

### TCP 服务器

```python
from mod import TCPServer

def handle_client(client_sock, client_addr):
    print(f"Client connected: {client_addr}")
    while True:
        data = client_sock.recv(1024)
        if not data:
            break
        client_sock.sendall(b"ACK: " + data)
    client_sock.close()

# 启动服务器
with TCPServer('0.0.0.0', 8080) as server:
    server.set_client_handler(handle_client)
    
    while server.running:
        try:
            client_sock, client_addr = server.accept_one(timeout=1.0)
            # 在线程中处理客户端
            import threading
            threading.Thread(
                target=handle_client,
                args=(client_sock, client_addr),
                daemon=True
            ).start()
        except TimeoutError:
            continue
```

### UDP 客户端

```python
from mod import UDPClient

with UDPClient() as client:
    client.bind('0.0.0.0', 0)  # 绑定到随机端口
    
    # 发送数据
    client.send_to(b"Hello!", ('192.168.1.1', 5000))
    
    # 接收数据
    data, addr = client.recv_from(1024)
    print(f"Received from {addr}: {data}")
    
    # 广播
    client.broadcast(b"Broadcast!", port=5000)
```

### 连接池

```python
from mod import ConnectionPool

with ConnectionPool('localhost', 8080, max_connections=10) as pool:
    # 从池中获取连接
    with pool.connection() as sock:
        sock.sendall(b"Hello from pool!")
        response = sock.recv(1024)
    
    # 连接自动返回池中
    print(f"Pool size: {pool.size}, In use: {pool.in_use}")
```

---

## 📚 API 参考

### 套接字创建

#### `create_socket(family, protocol, timeout, **options)`

创建配置好的套接字。

```python
# 默认 TCP 套接字
sock = create_socket()

# UDP 套接字
sock = create_socket(protocol=SocketProtocol.UDP)

# IPv6 套接字
sock = create_socket(family=SocketFamily.IPv6)

# 自定义选项
sock = create_socket(
    timeout=10.0,
    keep_alive=True,
    tcp_nodelay=True,
    send_buffer_size=65536
)
```

#### `create_ssl_socket(sock, server_hostname, certfile, keyfile, ca_certs, ...)`

为套接字添加 SSL/TLS 包装。

```python
sock = create_socket()
sock.connect(('example.com', 443))

ssl_sock = create_ssl_socket(
    sock,
    server_hostname='example.com',
    ca_certs='/path/to/ca-bundle.crt'
)
```

---

### TCP 客户端

#### `TCPClient(config)`

TCP 客户端类，管理连接生命周期。

```python
config = SocketConfig(
    host='localhost',
    port=8080,
    timeout=30.0,
    ssl_enabled=False
)

client = TCPClient(config)
client.connect()

# 发送数据（支持字符串和字节）
client.send(b"bytes data")
client.send("string data")

# 接收数据
data = client.recv(1024)

# 接收指定字节数
exact_data = client.recv_all(100)

# 发送并接收
response = client.send_recv(b"request")

# 获取连接信息
info = client.connection_info
print(info.remote_addr)
print(info.ssl)

# 获取统计信息
stats = client.get_stats()
print(f"Bytes sent: {stats.bytes_sent}")
print(f"Throughput: {stats.throughput} B/s")

client.close()
```

---

### TCP 服务器

#### `TCPServer(host, port, backlog, config)`

TCP 服务器类，处理传入连接。

```python
server = TCPServer('0.0.0.0', 8080, backlog=128)

# 设置客户端处理器
def handler(client_sock, client_addr):
    data = client_sock.recv(1024)
    client_sock.sendall(b"OK")
    client_sock.close()

server.set_client_handler(handler)
server.start()

# 接受连接
client_sock, client_addr = server.accept_one(timeout=5.0)

# 服务器状态
print(f"Running: {server.running}")
print(f"Clients: {server.client_count}")

server.stop()
```

---

### UDP 客户端

#### `UDPClient(config)`

UDP 客户端类，用于数据报通信。

```python
client = UDPClient()
client.bind('0.0.0.0', 5000)

# 发送到特定地址
client.send_to(b"Hello", ('192.168.1.1', 6000))

# 接收数据
data, addr = client.recv_from(1024)

# 发送并接收
response, addr = client.send_recv(b"Ping", ('192.168.1.1', 6000))

# 广播
client.broadcast(b"Hello everyone!", port=6000)

client.close()
```

---

### 连接池

#### `ConnectionPool(host, port, max_connections, config)`

线程安全的连接池。

```python
pool = ConnectionPool('localhost', 8080, max_connections=10)

# 获取连接
sock = pool.acquire(timeout=5.0)
sock.sendall(b"data")
pool.release(sock)

# 使用上下文管理器
with pool.connection() as sock:
    sock.sendall(b"data")

# 池状态
print(f"Available: {pool.available}")
print(f"In use: {pool.in_use}")
print(f"Size: {pool.size}")

pool.close_all()
```

---

### 网络工具函数

#### `get_local_ip()`

获取本地 IP 地址。

```python
ip = get_local_ip()
print(ip)  # '192.168.1.100'
```

#### `get_hostname()`

获取系统主机名。

```python
hostname = get_hostname()
print(hostname)
```

#### `resolve_hostname(hostname)`

解析主机名为 IP 地址列表。

```python
ips = resolve_hostname('google.com')
print(ips)  # ['142.250.80.46', ...]
```

#### `is_port_open(host, port, timeout)`

检查端口是否开放。

```python
if is_port_open('localhost', 8080):
    print("Port is open")
```

#### `scan_ports(host, ports, timeout)`

扫描多个端口。

```python
results = scan_ports('localhost', [22, 80, 443, 8080])
for port, is_open in results.items():
    if is_open:
        print(f"Port {port} is open")
```

#### `wait_for_readable(sockets, timeout)`

等待套接字可读。

```python
readable = wait_for_readable([sock1, sock2, sock3], timeout=5.0)
for sock in readable:
    data = sock.recv(1024)
```

---

### 协议辅助函数

#### `send_length_prefixed(sock, data)`

发送带 4 字节长度前缀的数据。

```python
send_length_prefixed(sock, b"Hello")
# 发送：[0, 0, 0, 5, 'H', 'e', 'l', 'l', 'o']
```

#### `recv_length_prefixed(sock)`

接收长度前缀的数据。

```python
data = recv_length_prefixed(sock)
```

#### `send_json(sock, data)`

发送 JSON 数据（带长度前缀）。

```python
send_json(sock, {"name": "Alice", "age": 30})
```

#### `recv_json(sock)`

接收 JSON 数据。

```python
data = recv_json(sock)
print(data["name"])
```

---

### 工具函数

#### `set_socket_options(sock, **options)`

设置多个套接字选项。

```python
set_socket_options(
    sock,
    reuse_addr=True,
    keep_alive=True,
    tcp_nodelay=True,
    send_buffer_size=65536,
    linger=30
)
```

#### `socket_to_info(sock)`

获取套接字详细信息。

```python
info = socket_to_info(sock)
print(info.local_addr)
print(info.remote_addr)
print(info.connected)
```

#### `format_socket_address(addr)`

格式化套接字地址。

```python
formatted = format_socket_address(('192.168.1.1', 8080))
print(formatted)  # '192.168.1.1:8080'
```

#### `parse_socket_address(addr_str)`

解析套接字地址字符串。

```python
addr = parse_socket_address('192.168.1.1:8080')
print(addr)  # ('192.168.1.1', 8080)
```

---

### 数据类

#### `SocketConfig`

套接字配置。

```python
config = SocketConfig(
    host='localhost',
    port=8080,
    timeout=30.0,
    buffer_size=4096,
    reuse_addr=True,
    keep_alive=True,
    tcp_nodelay=True,
    ssl_enabled=False,
    ssl_certfile=None,
    ssl_keyfile=None,
    ssl_ca_certs=None,
    ssl_check_hostname=True
)
```

#### `ConnectionInfo`

连接信息。

```python
info = ConnectionInfo(
    local_addr=('127.0.0.1', 50000),
    remote_addr=('192.168.1.1', 8080),
    family=socket.AF_INET,
    type=socket.SOCK_STREAM,
    connected=True,
    ssl=False
)
```

#### `TransferStats`

传输统计。

```python
stats = client.get_stats()
print(f"Bytes sent: {stats.bytes_sent}")
print(f"Bytes received: {stats.bytes_received}")
print(f"Packets sent: {stats.packets_sent}")
print(f"Duration: {stats.duration:.2f}s")
print(f"Throughput: {stats.throughput:.2f} B/s")
```

---

## 📝 示例

### 简单的 Echo 服务器

```python
from mod import TCPServer, TCPClient, SocketConfig
import threading

# 服务器
def echo_handler(client_sock, client_addr):
    print(f"Client {client_addr} connected")
    try:
        while True:
            data = client_sock.recv(1024)
            if not data:
                break
            client_sock.sendall(data)  # Echo back
    finally:
        client_sock.close()

server = TCPServer('0.0.0.0', 8080)
server.set_client_handler(echo_handler)
server.start()

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

threading.Thread(target=run_server, daemon=True).start()

# 客户端
with TCPClient(SocketConfig(host='localhost', port=8080)) as client:
    client.connect()
    client.send(b"Hello!")
    print(client.recv(1024))  # b"Hello!"
```

### SSL/TLS 安全连接

```python
from mod import TCPClient, SocketConfig, create_ssl_socket
import socket

# 创建普通套接字
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('example.com', 443))

# 包装为 SSL
ssl_sock = create_ssl_socket(
    sock,
    server_hostname='example.com',
    ca_certs='/etc/ssl/certs/ca-certificates.crt'
)

# 发送 HTTPS 请求
ssl_sock.sendall(b"GET / HTTP/1.1\r\nHost: example.com\r\n\r\n")
response = ssl_sock.recv(4096)
print(response.decode())

ssl_sock.close()
```

### 使用连接池的 HTTP 客户端

```python
from mod import ConnectionPool
import threading

pool = ConnectionPool('httpbin.org', 80, max_connections=5)

def make_request(path):
    with pool.connection() as sock:
        request = f"GET {path} HTTP/1.1\r\nHost: httpbin.org\r\n\r\n"
        sock.sendall(request.encode())
        return sock.recv(4096)

# 并发请求
paths = ['/get', '/ip', '/headers', '/user-agent']
results = []

threads = []
for path in paths:
    t = threading.Thread(target=lambda p=path: results.append(make_request(p)))
    threads.append(t)
    t.start()

for t in threads:
    t.join()

print(f"Completed {len(results)} requests")
print(f"Pool stats: {pool.available} available, {pool.in_use} in use")

pool.close_all()
```

---

## 🧪 运行测试

```bash
cd socket_utils
python socket_utils_test.py
```

测试覆盖：
- 套接字创建和配置
- TCP 客户端/服务器
- UDP 客户端
- 连接池
- SSL/TLS
- 长度前缀协议
- JSON over Sockets
- 网络工具函数
- 并发场景

---

## 🔒 安全注意事项

1. **SSL/TLS 验证**：始终启用主机名验证 (`ssl_check_hostname=True`) 并提供 CA 证书。

2. **超时设置**：始终设置合理的超时，避免连接挂起。

3. **资源清理**：使用上下文管理器确保套接字正确关闭。

4. **输入验证**：解析地址字符串时验证格式。

5. **端口扫描**：仅在你有权扫描的系统上使用端口扫描功能。

---

## 📊 性能提示

- **连接池**：对于频繁的连接，使用连接池避免重复的 TCP 握手。
- **缓冲区大小**：根据应用场景调整缓冲区大小（默认 4KB）。
- **TCP_NODELAY**：对于实时应用，启用 `tcp_nodelay` 禁用 Nagle 算法。
- **SO_KEEPALIVE**：长连接启用 keepalive 检测断线。
- **非阻塞 I/O**：使用 `wait_for_readable` 实现多路复用。

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

---

## 📄 许可证

MIT License
