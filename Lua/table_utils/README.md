# Table Utils 📦

**Lua 表格工具模块 - 零依赖，生产就绪**

---

## 📖 概述

`table_utils` 是一个全面的 Lua 表格操作工具模块，提供深度复制、合并、过滤、映射、排序、搜索、集合操作等功能。所有实现均使用 Lua 标准库，零外部依赖。

### ✨ 特性

- **零依赖** - 仅使用 Lua 标准库
- **全面功能** - 50+ 个实用函数覆盖所有表格操作场景
- **深度操作** - 支持深度复制、深度合并、嵌套路径访问
- **函数式编程** - filter、map、reduce、find、some、every
- **数组操作** - push、pop、slice、concat、unique、flatten
- **集合操作** - union、intersection、difference
- **类型安全** - 完整的类型检查和边界处理
- **生产就绪** - 完整的错误处理和循环引用保护
- **全面测试** - 100+ 测试用例覆盖所有功能

---

## 📦 安装

无需安装！直接复制 `mod.lua` 到你的项目即可使用。

```bash
# 从 AllToolkit 复制
cp AllToolkit/Lua/table_utils/mod.lua your_project/

# 或者克隆整个仓库
git clone https://github.com/ayukyo/alltoolkit.git
```

---

## 🚀 快速开始

```lua
local table_utils = require("mod")

-- 深度复制
local original = {a = 1, b = {c = 2}}
local copy = table_utils.deepcopy(original)

-- 合并表格
local merged = table_utils.merge({a = 1}, {b = 2}, {c = 3})

-- 过滤
local numbers = {a = 1, b = 2, c = 3, d = 4}
local evens = table_utils.filter(numbers, function(v) return v % 2 == 0 end)

-- 映射
local doubled = table_utils.map(numbers, function(v) return v * 2 end)

-- 查找
local found = table_utils.find(numbers, function(v) return v > 2 end)

-- 数组操作
local arr = {1, 2, 3, 4, 5}
table_utils.push(arr, 6)
local sliced = table_utils.slice(arr, 2, 4)
local unique = table_utils.unique({1, 2, 2, 3, 3, 3})
```

---

## 📚 API 参考

### 基本操作

#### `deepcopy(original)`

深度复制表格，处理循环引用。

```lua
local original = {a = 1, b = {c = 2, d = {e = 3}}}
local copy = table_utils.deepcopy(original)

copy.b.c = 999
print(original.b.c)  -- 输出：2（原表格不受影响）
```

#### `shallowcopy(original)`

浅复制表格。

```lua
local original = {a = 1, b = {c = 2}}
local copy = table_utils.shallowcopy(original)

-- 注意：嵌套表格共享引用
```

#### `isempty(tbl)`

检查表格是否为空。

```lua
table_utils.isempty({})           -- true
table_utils.isempty({1, 2, 3})    -- false
table_utils.isempty({a = 1})      -- false
```

#### `clear(tbl)`

清空表格。

```lua
local tbl = {a = 1, b = 2, c = 3}
table_utils.clear(tbl)
print(table_utils.isempty(tbl))  -- true
```

#### `count(tbl)`

获取表格键值对数量。

```lua
table_utils.count({a = 1, b = 2, c = 3})  -- 3
table_utils.count({})                      -- 0
```

---

### 合并操作

#### `merge(...)`

浅合并多个表格，后面的覆盖前面的。

```lua
local result = table_utils.merge(
    {a = 1, b = 2},
    {c = 3, d = 4},
    {b = 99, e = 5}
)
-- 结果：{a = 1, b = 99, c = 3, d = 4, e = 5}
```

#### `deepmerge(...)`

深度合并多个表格。

```lua
local t1 = {a = 1, b = {c = 2, d = 3}}
local t2 = {b = {c = 99, e = 4}, f = 5}

local result = table_utils.deepmerge(t1, t2)
-- 结果：{a = 1, b = {c = 99, d = 3, e = 4}, f = 5}
```

#### `update(target, source)`

将 source 的值复制到 target。

```lua
local target = {a = 1, b = 2}
local source = {b = 99, c = 3}

table_utils.update(target, source)
-- target: {a = 1, b = 99, c = 3}
```

---

### 转换操作

#### `keys(tbl)`

获取所有键。

```lua
local keys = table_utils.keys({a = 1, b = 2, c = 3})
-- 结果：{"a", "b", "c"}（顺序不保证）
```

#### `values(tbl)`

获取所有值。

```lua
local values = table_utils.values({a = 1, b = 2, c = 3})
-- 结果：{1, 2, 3}（顺序不保证）
```

#### `invert(tbl)`

键值互换。

```lua
local inverted = table_utils.invert({a = 1, b = 2, c = 3})
-- 结果：{[1] = "a", [2] = "b", [3] = "c"}
```

#### `topairs(tbl)`

转换为键值对数组。

```lua
local pairs = table_utils.topairs({a = 1, b = 2})
-- 结果：{{key = "a", value = 1}, {key = "b", value = 2}}
```

---

### 过滤和映射

#### `filter(tbl, predicate)`

过滤表格。

```lua
local numbers = {a = 1, b = 2, c = 3, d = 4, e = 5}
local odds = table_utils.filter(numbers, function(v) 
    return v % 2 == 1 
end)
-- 结果：{a = 1, c = 3, e = 5}
```

#### `map(tbl, func)`

映射表格。

```lua
local numbers = {a = 1, b = 2, c = 3}
local doubled = table_utils.map(numbers, function(v) 
    return v * 2 
end)
-- 结果：{a = 2, b = 4, c = 6}
```

#### `mapkeys(tbl, func)`

映射键。

```lua
local tbl = {a = 1, b = 2}
local result = table_utils.mapkeys(tbl, function(k) 
    return string.upper(k) 
end)
-- 结果：{A = 1, B = 2}
```

#### `reduce(tbl, func, initial)`

归约表格。

```lua
local numbers = {a = 1, b = 2, c = 3, d = 4}
local sum = table_utils.reduce(numbers, function(acc, v) 
    return acc + v 
end, 0)
-- 结果：10
```

#### `find(tbl, predicate)`

查找第一个满足条件的元素。

```lua
local numbers = {a = 1, b = 2, c = 3, d = 4}
local value, key = table_utils.find(numbers, function(v) 
    return v > 2 
end)
-- 结果：value = 3, key = "c"（或 d/4）
```

#### `some(tbl, predicate)`

检查是否存在满足条件的元素。

```lua
table_utils.some({1, 2, 3}, function(v) return v > 2 end)  -- true
table_utils.some({1, 2, 3}, function(v) return v > 10 end) -- false
```

#### `every(tbl, predicate)`

检查所有元素是否满足条件。

```lua
table_utils.every({1, 2, 3}, function(v) return v > 0 end)  -- true
table_utils.every({1, 2, 3}, function(v) return v > 1 end)  -- false
```

---

### 数组操作

#### `push(tbl, value)`

推入数组末尾。

```lua
local arr = {1, 2, 3}
table_utils.push(arr, 4)
-- arr: {1, 2, 3, 4}
```

#### `pop(tbl)`

从数组末尾弹出。

```lua
local arr = {1, 2, 3, 4}
local last = table_utils.pop(arr)
-- last = 4, arr: {1, 2, 3}
```

#### `unshift(tbl, value)`

推入数组开头。

```lua
local arr = {2, 3, 4}
table_utils.unshift(arr, 1)
-- arr: {1, 2, 3, 4}
```

#### `shift(tbl)`

从数组开头弹出。

```lua
local arr = {1, 2, 3, 4}
local first = table_utils.shift(arr)
-- first = 1, arr: {2, 3, 4}
```

#### `concat(...)`

连接多个数组。

```lua
local result = table_utils.concat({1, 2}, {3, 4}, {5, 6})
-- 结果：{1, 2, 3, 4, 5, 6}
```

#### `slice(tbl, start, finish)`

切片数组。

```lua
local arr = {1, 2, 3, 4, 5}
local sliced = table_utils.slice(arr, 2, 4)
-- 结果：{2, 3, 4}
```

#### `join(tbl, separator, start, finish)`

拼接数组为字符串。

```lua
table_utils.join({"a", "b", "c"}, ", ")      -- "a, b, c"
table_utils.join({"a", "b", "c"}, "-")       -- "a-b-c"
table_utils.join({1, 2, 3, 4, 5}, "+", 2, 4) -- "2+3+4"
```

#### `unique(tbl)`

数组去重。

```lua
local result = table_utils.unique({1, 2, 2, 3, 3, 3, 4})
-- 结果：{1, 2, 3, 4}
```

#### `flatten(tbl, depth)`

数组展平。

```lua
local nested = {1, {2, 3}, {4, {5, 6}}}

table_utils.flatten(nested, 1)  -- {1, 2, 3, 4, {5, 6}}
table_utils.flatten(nested, 2)  -- {1, 2, 3, 4, 5, 6}
```

#### `compact(tbl)`

移除 nil 值。

```lua
local result = table_utils.compact({1, nil, 2, nil, 3})
-- 结果：{1, 2, 3}
```

---

### 排序操作

#### `sort(tbl, comp)`

排序表格。

```lua
local result = table_utils.sort({3, 1, 4, 1, 5, 9, 2, 6})
-- 结果：{1, 1, 2, 3, 4, 5, 6, 9}

-- 自定义比较函数
local result = table_utils.sort({3, 1, 4}, function(a, b) 
    return a > b 
end)
-- 结果：{4, 3, 1}
```

#### `sortby(tbl, key, ascending)`

按指定键排序表格数组。

```lua
local people = {
    {name = "Alice", age = 30},
    {name = "Bob", age = 25},
    {name = "Charlie", age = 35}
}

-- 按年龄升序
local sorted = table_utils.sortby(people, "age")

-- 按年龄降序
local sorted = table_utils.sortby(people, "age", false)
```

#### `reverse(tbl)`

反转表格。

```lua
local result = table_utils.reverse({1, 2, 3, 4, 5})
-- 结果：{5, 4, 3, 2, 1}
```

---

### 搜索和查找

#### `indexof(tbl, value)`

查找值的索引。

```lua
table_utils.indexof({"a", "b", "c", "d"}, "c")  -- 3
table_utils.indexof({"a", "b", "c"}, "z")       -- nil
```

#### `lastindexof(tbl, value)`

查找值的最后一个索引。

```lua
table_utils.lastindexof({1, 2, 3, 2, 1}, 2)  -- 4
```

#### `includes(tbl, value)`

检查是否包含值。

```lua
table_utils.includes({1, 2, 3, 4, 5}, 3)   -- true
table_utils.includes({1, 2, 3, 4, 5}, 10)  -- false
```

#### `haskey(tbl, key)`

检查是否包含键。

```lua
table_utils.haskey({a = 1, b = 2}, "b")  -- true
table_utils.haskey({a = 1, b = 2}, "z")  -- false
```

---

### 集合操作

#### `union(tbl1, tbl2)`

并集。

```lua
local result = table_utils.union({1, 2, 3, 4}, {3, 4, 5, 6})
-- 结果：{1, 2, 3, 4, 5, 6}
```

#### `intersection(tbl1, tbl2)`

交集。

```lua
local result = table_utils.intersection({1, 2, 3, 4}, {3, 4, 5, 6})
-- 结果：{3, 4}
```

#### `difference(tbl1, tbl2)`

差集（tbl1 - tbl2）。

```lua
local result = table_utils.difference({1, 2, 3, 4}, {3, 4, 5, 6})
-- 结果：{1, 2}
```

---

### 实用工具

#### `range(start, finish, step)`

创建范围数组。

```lua
table_utils.range(1, 5)        -- {1, 2, 3, 4, 5}
table_utils.range(0, 10, 2)    -- {0, 2, 4, 6, 8, 10}
table_utils.range(5, 1, -1)    -- {5, 4, 3, 2, 1}
```

#### `fill(length, value)`

创建填充数组。

```lua
table_utils.fill(5, "x")  -- {"x", "x", "x", "x", "x"}
```

#### `sequence(length, func)`

创建序列数组。

```lua
local squares = table_utils.sequence(5, function(i) 
    return i * i 
end)
-- 结果：{1, 4, 9, 16, 25}
```

#### `groupby(tbl, keyfunc)`

分组表格。

```lua
local people = {
    {name = "Alice", group = "A"},
    {name = "Bob", group = "B"},
    {name = "Charlie", group = "A"},
    {name = "David", group = "B"}
}

local grouped = table_utils.groupby(people, function(p) 
    return p.group 
end)
-- 结果：{A = {{name="Alice",...}, {name="Charlie",...}}, B = {...}}
```

#### `partition(tbl, predicate)`

分区表格。

```lua
local numbers = {1, 2, 3, 4, 5, 6}
local evens, odds = table_utils.partition(numbers, function(v) 
    return v % 2 == 0 
end)
-- evens: {2, 4, 6}
-- odds: {1, 3, 5}
```

---

### 路径操作

#### `get(tbl, path, default)`

获取嵌套值。

```lua
local data = {user = {profile = {name = "Alice", age = 30}}}

table_utils.get(data, "user.profile.name")           -- "Alice"
table_utils.get(data, {"user", "profile", "name"})   -- "Alice"
table_utils.get(data, "user.profile.email", "N/A")   -- "N/A"
```

#### `set(tbl, path, value)`

设置嵌套值。

```lua
local data = {user = {profile = {}}}

table_utils.set(data, "user.profile.name", "Alice")
table_utils.set(data, "user.profile.age", 30)
table_utils.set(data, "settings.theme", "dark")  -- 自动创建中间表格
```

#### `delete(tbl, path)`

删除嵌套值。

```lua
local data = {user = {profile = {name = "Alice", age = 30}}}

local deleted = table_utils.delete(data, "user.profile.name")
-- deleted = "Alice"
-- data.user.profile.name = nil
```

---

### 类型检查

#### `isarray(tbl)`

检查是否为数组。

```lua
table_utils.isarray({1, 2, 3})      -- true
table_utils.isarray({a = 1, b = 2}) -- false
table_utils.isarray({})             -- true
```

#### `isassociative(tbl)`

检查是否为关联数组。

```lua
table_utils.isassociative({a = 1, b = 2}) -- true
table_utils.isassociative({1, 2, 3})      -- false
table_utils.isassociative({})             -- false
```

---

### 调试输出

#### `tostring(tbl, indent)`

将表格转换为字符串表示。

```lua
local data = {a = 1, b = {c = 2, d = 3}}
print(table_utils.tostring(data))
-- 输出：
-- {
--   a = 1,
--   b = {
--     c = 2,
--     d = 3,
--   },
-- }
```

#### `print(tbl, name)`

打印表格（用于调试）。

```lua
table_utils.print({a = 1, b = 2}, "data")
-- 输出：data = { ... }
```

---

## 📝 示例

查看 `examples/` 目录获取更多使用示例：

- `basic_usage.lua` - 基本用法示例
- `data_processing.lua` - 数据处理示例
- `nested_data.lua` - 嵌套数据操作示例
- `functional_style.lua` - 函数式编程风格示例

---

## 🧪 运行测试

```bash
cd table_utils
lua table_utils_test.lua
```

测试覆盖：
- 基本操作（复制、清空、计数）
- 合并操作（浅合并、深合并、更新）
- 转换操作（键、值、反转）
- 过滤和映射（filter、map、reduce、find）
- 数组操作（push、pop、slice、concat、unique、flatten）
- 排序操作（sort、sortby、reverse）
- 搜索和查找（indexof、includes、haskey）
- 集合操作（union、intersection、difference）
- 实用工具（range、fill、groupby、partition）
- 路径操作（get、set、delete）
- 类型检查（isarray、isassociative）

---

## 🔧 性能提示

1. **深度复制**：对于大型嵌套表格，`deepcopy` 会创建完整副本，注意内存使用
2. **循环引用**：`deepcopy` 内置循环引用检测，可安全处理自引用表格
3. **数组 vs 关联数组**：对于纯数组操作，使用 `ipairs` 相关的函数性能更好
4. **批量操作**：对于大量数据，考虑使用 `reduce` 而非多次遍历

---

## 📊 与其他语言对比

| 功能 | Lua table_utils | JavaScript Lodash | Python |
|------|----------------|-------------------|--------|
| 深度复制 | `deepcopy` | `_.cloneDeep` | `copy.deepcopy` |
| 过滤 | `filter` | `_.filter` | `filter()` / 列表推导 |
| 映射 | `map` | `_.map` | `map()` / 列表推导 |
| 归约 | `reduce` | `_.reduce` | `functools.reduce` |
| 查找 | `find` | `_.find` | `next()` |
| 去重 | `unique` | `_.uniq` | `set()` |
| 展平 | `flatten` | `_.flatten` | 列表推导 |
| 分组 | `groupby` | `_.groupBy` | `itertools.groupby` |

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

---

## 📄 许可证

MIT License
