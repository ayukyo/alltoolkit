# XML Utils

Lua XML 解析与序列化工具库 - 零依赖，生产就绪

## 功能列表

- **DOM 解析** - 将 XML 字符串解析为 DOM 树结构
- **SAX 解析器** - 流式解析接口，支持大文件处理
- **XML 编码** - 将 Lua 表或 DOM 节点序列化为 XML 字符串
- **CSS 选择器** - 支持 `tag`, `#id`, `.class`, `[attr]`, `[attr=value]` 查询
- **格式化/压缩** - 美化输出或压缩 XML
- **实体处理** - 自动编解码 XML 特殊字符（`&`, `<`, `>`, `"`, `'`）
- **程序化构建** - 使用 API 创建 XML 元素

## 快速开始

```lua
local XmlUtils = require("mod")

-- 解析 XML
local doc = XmlUtils.parse("<root><item id='1'>Hello</item></root>")

-- 查询元素
local items = XmlUtils.select(doc, "item")
local item = items[1]
print(XmlUtils.getText(item))  -- Hello
print(XmlUtils.getAttr(item, "id"))  -- 1

-- 编码为 XML
local xml = XmlUtils.encode(node, { pretty = true })

-- Lua 表转 XML
local data = { name = "Alice", age = "30" }
local xml = XmlUtils.encodeTable(data, "person")
```

## API 参考

### 解析

- `XmlUtils.parse(xml)` - 解析 XML 字符串为 DOM 树
- `XmlUtils.format(xml)` - 格式化 XML
- `XmlUtils.minify(xml)` - 压缩 XML

### 查询

- `XmlUtils.select(root, selector)` - CSS 选择器查询
- `XmlUtils.children(node, name)` - 获取子元素
- `XmlUtils.firstChild(node, name)` - 获取第一个子元素
- `XmlUtils.getText(node)` - 获取文本内容
- `XmlUtils.getAttr(node, attr)` - 获取属性
- `XmlUtils.setAttr(node, attr, value)` - 设置属性

### 编码

- `XmlUtils.encode(node, config)` - DOM 节点转 XML
- `XmlUtils.encodeTable(data, rootName)` - Lua 表转 XML
- `XmlUtils.element(name, attrs, children, text)` - 创建元素

### 配置

```lua
XmlUtils.Config = {
    max_depth = 200,      -- 最大嵌套深度
    indent = "  ",         -- 缩进字符
    pretty = true,         -- 美化输出
    xml_decl = true,       -- 输出 XML 声明
    attr_quote = '"',     -- 属性引号
}
```

## 选择器示例

```lua
local doc = XmlUtils.parse(xml)

-- 标签选择器
local divs = XmlUtils.select(doc, "div")

-- ID 选择器
local header = XmlUtils.select(doc, "#main-header")[1]

-- 类选择器
local active = XmlUtils.select(doc, ".active")

-- 属性选择器
local link = XmlUtils.select(doc, "[href]")[1]
local external = XmlUtils.select(doc, '[target="_blank"]')[1]
```

## 零外部依赖

纯 Lua 标准库实现，适用于任何 Lua 5.1+ 环境。