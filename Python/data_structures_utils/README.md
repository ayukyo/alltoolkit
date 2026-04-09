# Data Structures Utils 🗂️

**Python 数据结构工具模块 - 零依赖，生产就绪**

---

## 📖 概述

`data_structures_utils` 是一个全面的 Python 数据结构实现模块，提供常用的数据结构类和工具函数。所有实现均使用 Python 标准库，零外部依赖。

### ✨ 特性

- **零依赖** - 仅使用 Python 标准库
- **类型安全** - 完整的类型注解
- **生产就绪** - 完整的错误处理和边界检查
- **全面测试** - 60+ 测试用例覆盖所有功能
- **文档完善** - 每个函数都有详细的文档字符串

---

## 📦 安装

无需安装！直接复制 `mod.py` 到你的项目即可使用。

```bash
# 或者从 AllToolkit 克隆
git clone https://github.com/ayukyo/alltoolkit.git
cp AllToolkit/Python/data_structures_utils/mod.py your_project/
```

---

## 🚀 快速开始

```python
from mod import Stack, Queue, LinkedList, BinarySearchTree

# 栈 - LIFO
stack = Stack[int]()
stack.push(1)
stack.push(2)
print(stack.pop())  # 2

# 队列 - FIFO
queue = Queue[str]()
queue.enqueue("first")
queue.enqueue("second")
print(queue.dequeue())  # "first"

# 链表
ll = LinkedList[int]()
ll.append(1)
ll.append(2)
ll.prepend(0)
print(ll.to_list())  # [0, 1, 2]

# 二叉搜索树
bst = BinarySearchTree[int]()
bst.insert(5)
bst.insert(3)
bst.insert(7)
print(bst.search(3))  # True
print(bst.inorder())  # [3, 5, 7]
```

---

## 📚 API 参考

### 栈 (Stack)

后进先出 (LIFO) 数据结构。

```python
stack = Stack[int]()

stack.push(item)      # 压栈
stack.pop() -> T      # 弹栈
stack.peek() -> T     # 查看栈顶
stack.is_empty() -> bool
stack.size() -> int
stack.clear()
stack.to_list() -> List[T]
```

### 队列 (Queue)

先进先出 (FIFO) 数据结构。

```python
queue = Queue[int]()

queue.enqueue(item)   # 入队
queue.dequeue() -> T  # 出队
queue.front() -> T    # 查看队首
queue.back() -> T     # 查看队尾
queue.is_empty() -> bool
queue.size() -> int
```

### 优先队列 (PriorityQueue)

按优先级出队的队列，优先级数值越小优先级越高。

```python
pq = PriorityQueue[str]()

pq.push(priority, item)  # 入队（带优先级）
pq.pop() -> T            # 出队（最高优先级）
pq.peek() -> T           # 查看最高优先级元素
```

### 循环队列 (CircularQueue)

固定容量的循环队列。

```python
cq = CircularQueue[int](capacity=5)

cq.enqueue(item) -> bool  # 入队（满时返回 False）
cq.dequeue() -> T
cq.is_full() -> bool
cq.capacity() -> int
```

### 链表 (LinkedList)

 singly linked list.

```python
ll = LinkedList[int]()

ll.append(value)         # 尾部添加
ll.prepend(value)        # 头部添加
ll.insert(index, value)  # 指定位置插入
ll.remove(value) -> bool # 删除值
ll.remove_at(index) -> T # 删除指定位置
ll.get(index) -> T       # 获取值
ll.set(index, value)     # 设置值
ll.find(value) -> int    # 查找索引
ll.reverse()             # 反转链表
ll.to_list() -> List[T]  # 转为 Python 列表
```

### 双向链表 (DoublyLinkedList)

双向链表实现。

```python
dll = DoublyLinkedList[int]()

dll.append(value)
dll.prepend(value)
dll.remove(value) -> bool
dll.to_list() -> List[T]
```

### 二叉搜索树 (BinarySearchTree)

二叉搜索树实现。

```python
bst = BinarySearchTree[int]()

bst.insert(value)        # 插入
bst.search(value) -> bool  # 搜索
bst.remove(value) -> bool  # 删除
bst.inorder() -> List[T]   # 中序遍历（排序）
bst.preorder() -> List[T]  # 前序遍历
bst.postorder() -> List[T] # 后序遍历
bst.height() -> int        # 树高度
```

### 哈希表 (HashTable)

哈希表实现，使用链地址法处理冲突。

```python
ht = HashTable[str]()

ht.put(key, value)       # 插入/更新
ht.get(key, default) -> T  # 获取
ht.remove(key) -> bool   # 删除
ht.contains(key) -> bool # 检查是否存在
ht.keys() -> List[str]   # 所有键
ht.values() -> List[T]   # 所有值
ht.items() -> List[Tuple]

# 也支持字典式操作
ht["key"] = "value"
value = ht["key"]
```

### 图 (Graph)

图实现，支持有向和无向图。

```python
g = Graph(directed=False)

g.add_vertex(vertex)           # 添加顶点
g.add_edge(from_v, to_v)       # 添加边
g.remove_edge(from_v, to_v)    # 删除边
g.neighbors(vertex) -> List    # 邻居
g.bfs(start) -> List[str]      # 广度优先搜索
g.dfs(start) -> List[str]      # 深度优先搜索
g.has_edge(from_v, to_v) -> bool
g.num_vertices() -> int
g.num_edges() -> int
```

### 堆 (MinHeap / MaxHeap)

最小堆和最大堆实现。

```python
min_heap = MinHeap[int]()
max_heap = MaxHeap[int]()

heap.push(item)
heap.pop() -> T
heap.peek() -> T
heap.is_empty() -> bool
heap.size() -> int
```

### 字典树 (Trie)

前缀树，用于高效的字符串操作。

```python
trie = Trie()

trie.insert(word)                    # 插入单词
trie.search(word) -> bool            # 搜索完整单词
trie.starts_with(prefix) -> bool     # 前缀匹配
trie.remove(word) -> bool            # 删除单词
trie.find_words_with_prefix(prefix)  # 查找所有前缀匹配的单词
```

---

## 🛠️ 工具函数

### 括号平衡检查

```python
from mod import is_balanced_brackets

is_balanced_brackets("([]{})")  # True
is_balanced_brackets("([)]")    # False
```

### 后缀表达式求值

```python
from mod import evaluate_postfix

evaluate_postfix("3 4 + 2 *")  # 14.0
```

### 中缀转后缀

```python
from mod import infix_to_postfix

infix_to_postfix("3 + 4 * 2")  # "3 4 2 * +"
```

### 合并有序列表

```python
from mod import merge_sorted_lists

merge_sorted_lists([[1, 4, 5], [1, 3, 4], [2, 6]])
# [1, 1, 2, 3, 4, 4, 5, 6]
```

### 第 K 大元素

```python
from mod import find_kth_largest

find_kth_largest([3, 2, 1, 5, 6, 4], 2)  # 5
```

### Top K 频繁元素

```python
from mod import top_k_frequent

top_k_frequent([1, 1, 1, 2, 2, 3], 2)  # [1, 2]
```

---

## 🧪 运行测试

```bash
cd AllToolkit/Python/data_structures_utils
python data_structures_utils_test.py
```

### 测试覆盖

- ✅ Stack: 10 个测试用例
- ✅ Queue: 6 个测试用例
- ✅ PriorityQueue: 3 个测试用例
- ✅ CircularQueue: 7 个测试用例
- ✅ LinkedList: 12 个测试用例
- ✅ DoublyLinkedList: 3 个测试用例
- ✅ BinarySearchTree: 10 个测试用例
- ✅ HashTable: 10 个测试用例
- ✅ Graph: 7 个测试用例
- ✅ MinHeap/MaxHeap: 5 个测试用例
- ✅ Trie: 5 个测试用例
- ✅ 工具函数: 12 个测试用例

**总计：90+ 测试用例**

---

## 📝 使用示例

### 示例 1: 使用栈检查括号平衡

```python
from mod import Stack, is_balanced_brackets

def check_expression(expr: str) -> bool:
    """检查数学表达式的括号是否平衡"""
    return is_balanced_brackets(expr)

print(check_expression("(a + b) * [c - d]"))  # True
print(check_expression("(a + b * [c - d)"))   # False
```

### 示例 2: 使用 BFS 查找最短路径

```python
from mod import Graph

def find_shortest_path(graph: Graph, start: str, end: str) -> List[str]:
    """使用 BFS 查找最短路径"""
    visited = set()
    queue = Queue[Tuple[str, List[str]]]()
    queue.enqueue((start, [start]))
    
    while not queue.is_empty():
        current, path = queue.dequeue()
        
        if current == end:
            return path
        
        if current not in visited:
            visited.add(current)
            for neighbor in graph.neighbors(current):
                if neighbor not in visited:
                    queue.enqueue((neighbor, path + [neighbor]))
    
    return []

# 使用示例
g = Graph(directed=False)
g.add_edge("A", "B")
g.add_edge("B", "C")
g.add_edge("C", "D")
g.add_edge("A", "D")

path = find_shortest_path(g, "A", "D")
print(path)  # ['A', 'D']
```

### 示例 3: 使用 Trie 实现自动补全

```python
from mod import Trie

class AutoComplete:
    def __init__(self):
        self.trie = Trie()
    
    def add_word(self, word: str) -> None:
        self.trie.insert(word)
    
    def suggest(self, prefix: str, max_results: int = 5) -> List[str]:
        return self.trie.find_words_with_prefix(prefix, max_results)

# 使用示例
ac = AutoComplete()
for word in ["apple", "application", "apply", "appreciate", "apricot"]:
    ac.add_word(word)

print(ac.suggest("app"))  # ['apple', 'appreciate', 'application', 'apply']
```

### 示例 4: 使用优先队列实现任务调度

```python
from mod import PriorityQueue

class TaskScheduler:
    def __init__(self):
        self.queue = PriorityQueue[str]()
    
    def add_task(self, task: str, priority: int) -> None:
        self.queue.push(priority, task)
    
    def next_task(self) -> str:
        return self.queue.pop()
    
    def has_tasks(self) -> bool:
        return not self.queue.is_empty()

# 使用示例
scheduler = TaskScheduler()
scheduler.add_task("低优先级任务", 3)
scheduler.add_task("高优先级任务", 1)
scheduler.add_task("中优先级任务", 2)

while scheduler.has_tasks():
    print(scheduler.next_task())
# 输出:
# 高优先级任务
# 中优先级任务
# 低优先级任务
```

---

## 🤝 贡献

欢迎贡献代码、测试、文档！

1. Fork 项目
2. 创建特性分支
3. 提交更改
4. 推送到分支
5. 开启 Pull Request

---

## 📄 许可证

MIT License

---

## 🔗 相关链接

- [AllToolkit 主项目](https://github.com/ayukyo/alltoolkit)
- [Python 模块列表](../README.md)
- [贡献指南](../../docs/contributing.md)
