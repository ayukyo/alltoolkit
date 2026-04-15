# Dependency Resolver Utils

依赖解析工具模块 - 基于拓扑排序的依赖关系解析，支持循环检测、并行执行层级计算。

## 功能特性

- **拓扑排序**: 将依赖图转换为线性执行顺序
- **循环检测**: 检测并报告循环依赖
- **并行层级**: 计算可并行执行的任务层级
- **依赖图可视化**: 文本格式的依赖关系图
- **子图提取**: 提取指定节点及其依赖的子图
- **序列化支持**: JSON 格式的导入导出

## 使用场景

- 包管理器依赖解析
- 构建系统任务调度
- 插件加载顺序
- 模块初始化顺序
- 任务调度系统
- CI/CD 流水线规划
- 微服务启动顺序

## 快速开始

```python
from dependency_resolver_utils.mod import DependencyGraph, topological_sort

# 方式一: 使用便捷函数
deps = {"C": ["A", "B"], "B": ["A"], "A": []}
order = topological_sort(deps)
print(order)  # ['A', 'B', 'C']

# 方式二: 使用 DependencyGraph 类
graph = DependencyGraph(name="项目依赖")
graph.add_node("A")
graph.add_node("B", dependencies=["A"])
graph.add_node("C", dependencies=["B"])

result = graph.resolve()
print(f"执行顺序: {result.order}")
print(f"并行层级: {result.levels}")
```

## API 参考

### DependencyGraph 类

主要依赖图管理类。

```python
graph = DependencyGraph(name="MyGraph")

# 添加节点
graph.add_node("A")
graph.add_node("B", dependencies=["A"], metadata={"version": "1.0"})

# 添加/移除依赖
graph.add_dependency("B", "A")
graph.remove_dependency("B", "A")

# 获取信息
graph.get_roots()           # 根节点列表
graph.get_leaves()          # 叶节点列表
graph.get_dependencies("B") # 直接依赖
graph.get_all_dependencies("B")  # 所有传递依赖

# 解析
result = graph.resolve(allow_cycles=False)  # 解析依赖

# 可视化
print(graph.visualize())

# 序列化
json_str = graph.to_json()
graph2 = DependencyGraph.from_json(json_str)
```

### ResolutionResult 类

解析结果对象。

```python
result.order      # 拓扑排序结果
result.levels     # 并行层级列表
result.has_cycles # 是否存在循环
result.cycles     # 循环路径列表
result.to_dict()  # 转换为字典
result.to_json()  # 转换为 JSON
```

### 便捷函数

```python
from dependency_resolver_utils.mod import (
    topological_sort,       # 快速拓扑排序
    resolve_dependencies,   # 快速依赖解析
    find_cycles,            # 快速循环检测
)

# 拓扑排序
order = topological_sort({"C": ["A", "B"], "B": ["A"], "A": []})

# 依赖解析
result = resolve_dependencies({"C": ["A", "B"], "B": ["A"], "A": []})

# 循环检测
cycles = find_cycles({"A": ["B"], "B": ["C"], "C": ["A"]})
```

## 示例场景

### 包管理器

```python
packages = {
    "react": [],
    "react-dom": ["react"],
    "redux": [],
    "react-redux": ["react", "redux"],
}

result = resolve_dependencies(packages)
for i, level in enumerate(result.levels, 1):
    print(f"第{i}批安装: {level}")
```

### CI/CD 流水线

```python
stages = {
    "checkout": [],
    "install": ["checkout"],
    "lint": ["install"],
    "test": ["install"],
    "build": ["lint", "test"],
    "deploy": ["build"],
}

graph = DependencyGraph(name="CI流水线")
for stage, deps in stages.items():
    graph.add_node(stage, dependencies=deps)

print("执行计划:")
for i, level in enumerate(graph.get_parallel_levels(), 1):
    print(f"阶段{i}: {' | '.join(level)}")
```

### 循环依赖检测

```python
graph = DependencyGraph()
graph.add_node("A", dependencies=["B"])
graph.add_node("B", dependencies=["C"])
graph.add_node("C", dependencies=["A"])  # 循环!

cycles = graph.detect_cycles()
if cycles:
    print(f"检测到循环: {cycles[0]}")
```

## 测试

```bash
python dependency_resolver_utils_test.py
```

## 文件结构

```
dependency_resolver_utils/
├── mod.py                        # 核心模块
├── dependency_resolver_utils_test.py  # 测试文件
├── README.md                     # 说明文档
└── examples/
    ├── basic_usage.py            # 基础用法示例
    └── advanced_usage.py         # 高级用法示例
```

## 零依赖

本模块仅使用 Python 标准库，无需安装任何第三方包。兼容 Python 3.6+。

## 许可证

MIT License