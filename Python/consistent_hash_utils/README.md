# Consistent Hash Utils


AllToolkit - Python Consistent Hash Utilities

A zero-dependency, production-ready consistent hashing utility module.
Supports virtual nodes, weighted nodes, and smooth data migration.

Consistent hashing is used in distributed systems for:
- Distributed caching (Redis cluster, Memcached)
- Load balancing
- Data sharding
- Distributed storage

Author: AllToolkit
License: MIT


## 功能

### 类

- **Node**: Represents a node in the consistent hash ring
- **Migration**: Represents a data migration between nodes
- **ConsistentHash**: Basic consistent hash ring implementation
  方法: virtual_nodes, hash_algorithm, node_count, nodes, add_node ... (14 个方法)
- **WeightedConsistentHash**: Consistent hash ring with weighted node distribution
  方法: add_node, get_weight_distribution, rebalance
- **RendezvousHash**: Rendezvous (HRW) hashing implementation
  方法: node_count, nodes, add_node, remove_node, get_node ... (7 个方法)
- **JumpConsistentHash**: Jump consistent hash implementation
  方法: num_buckets, get_bucket, get_bucket_for_int, resize, get_distribution
- **MultiHash**: Multi-hash consistent hashing for high availability
  方法: node_count, nodes, add_node, remove_node, get_primary_node ... (8 个方法)

### 函数

- **create_ring(nodes, virtual_nodes, hash_algorithm**) - Create a consistent hash ring with the given nodes.
- **distribute_keys(keys, nodes, virtual_nodes**) - Distribute keys evenly across nodes.
- **analyze_distribution(keys, nodes, virtual_nodes**) - Analyze key distribution across nodes.
- **virtual_nodes(self**) - Get number of virtual nodes per physical node.
- **hash_algorithm(self**) - Get the hash algorithm used.
- **node_count(self**) - Get number of physical nodes.
- **nodes(self**) - Get list of node names.
- **add_node(self, name, weight**, ...) - Add a node to the hash ring.
- **remove_node(self, name**) - Remove a node from the hash ring.
- **get_node(self, key**) - Get the node responsible for a key.

... 共 40 个函数

## 使用示例

```python
from mod import create_ring

# 使用 create_ring
result = create_ring()
```

## 测试

运行测试：

```bash
python *_test.py
```

## 文件结构

```
{module_name}/
├── mod.py              # 主模块
├── *_test.py           # 测试文件
├── README.md           # 本文档
└── examples/           # 示例代码
    └── usage_examples.py
```

---

**Last updated**: 2026-04-28
