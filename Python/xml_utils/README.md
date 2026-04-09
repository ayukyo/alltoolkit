# AllToolkit - XML Utilities 📄

**零依赖 Python XML 处理工具库**

---

## 📖 概述

`xml_utils` 是一个功能完整的 XML 处理工具模块，提供解析、创建、查询、转换、修改、验证等功能。完全使用 Python 标准库实现（xml.etree.ElementTree, json, re），无需任何外部依赖。

### 核心功能

- 📥 **XML 解析**: 字符串/文件解析，XML 转字典
- 📤 **XML 创建**: 元素创建，文档生成
- 🔍 **XML 查询**: XPath 查找，文本/属性提取
- 🔄 **格式转换**: XML ↔ JSON, XML → CSV
- ✏️ **XML 修改**: 文本/属性修改，增删子元素
- ✅ **XML 验证**: 有效性检查，结构验证
- 🎨 **格式化**: 美化输出，压缩，文本提取
- 📦 **批量处理**: 批量解析，批量提取
- 🏷️ **命名空间**: 命名空间注册和查找

---

## 🚀 快速开始

### 安装

无需安装！直接复制 `mod.py` 到你的项目：

```bash
cp AllToolkit/Python/xml_utils/mod.py your_project/
```

### 基础使用

```python
from mod import *

# 解析 XML
xml_str = """
<library>
    <book id="1">
        <title>Python 编程</title>
        <author>张三</author>
    </book>
</library>
"""

root = parse_xml(xml_str)

# 查询元素
books = find_elements(root, './/book')
title = find_element(root, './/title')
print(get_element_text(title))  # Python 编程

# 获取属性
first_book = find_element(root, './/book')
print(get_attribute(first_book, 'id'))  # 1

# 转换为字典
data = xml_to_dict(root)
print(data)

# 转换为 JSON
json_str = xml_to_json(xml_str)
print(json_str)
```

---

## 📚 API 参考

### 解析函数

| 函数 | 描述 | 示例 |
|------|------|------|
| `parse_xml(xml_string)` | 解析 XML 字符串 | `parse_xml('<root/>')` |
| `parse_xml_file(file_path)` | 解析 XML 文件 | `parse_xml_file('data.xml')` |
| `xml_to_dict(element)` | XML 转字典 | `xml_to_dict(root)` |
| `dict_to_xml(data, root_tag)` | 字典转 XML | `dict_to_xml(data, 'root')` |

### 创建函数

| 函数 | 描述 | 示例 |
|------|------|------|
| `create_element(tag, text, attributes, children)` | 创建元素 | `create_element('div', 'Hello')` |
| `create_xml_document(root_tag, children, attributes)` | 创建文档 | `create_xml_document('root', children)` |

### 查询函数

| 函数 | 描述 | 示例 |
|------|------|------|
| `find_elements(root, xpath)` | 查找所有匹配元素 | `find_elements(root, './/book')` |
| `find_element(root, xpath)` | 查找单个元素 | `find_element(root, './/title')` |
| `get_element_text(element, default)` | 获取文本内容 | `get_element_text(title)` |
| `get_attribute(element, attr, default)` | 获取属性值 | `get_attribute(elem, 'id')` |
| `find_all_text(root, xpath)` | 批量获取文本 | `find_all_text(root, './/title')` |

### 转换函数

| 函数 | 描述 | 示例 |
|------|------|------|
| `xml_to_json(xml_string, indent)` | XML 转 JSON | `xml_to_json(xml_str)` |
| `json_to_xml(json_string, root_tag)` | JSON 转 XML | `json_to_xml(json_str)` |
| `xml_to_csv(xml_string, row_xpath, columns)` | XML 转 CSV | `xml_to_csv(xml, './/row', cols)` |
| `xml_to_text(xml_string)` | 提取纯文本 | `xml_to_text(xml_str)` |

### 修改函数

| 函数 | 描述 | 示例 |
|------|------|------|
| `set_element_text(element, text)` | 设置文本 | `set_element_text(elem, 'New')` |
| `set_attribute(element, name, value)` | 设置属性 | `set_attribute(elem, 'id', '1')` |
| `add_child(parent, child, index)` | 添加子元素 | `add_child(parent, child)` |
| `remove_element(parent, child)` | 移除元素 | `remove_element(parent, child)` |

### 验证函数

| 函数 | 描述 | 示例 |
|------|------|------|
| `is_valid_xml(xml_string)` | 检查有效性 | `is_valid_xml(xml_str)` |
| `has_required_elements(root, xpaths)` | 检查必需元素 | `has_required_elements(root, xpaths)` |
| `validate_xml_structure(root, schema)` | Schema 验证 | `validate_xml_structure(root, schema)` |

### 格式化函数

| 函数 | 描述 | 示例 |
|------|------|------|
| `format_xml(xml_string, indent)` | 美化格式化 | `format_xml(xml_str)` |
| `minify_xml(xml_string)` | 压缩 XML | `minify_xml(xml_str)` |

### 批量处理

| 函数 | 描述 | 示例 |
|------|------|------|
| `batch_parse_xml(xml_strings)` | 批量解析 | `batch_parse_xml([xml1, xml2])` |
| `batch_extract(xml_string, xpaths)` | 批量提取 | `batch_extract(xml, xpaths)` |

### 便捷函数

| 函数 | 描述 | 示例 |
|------|------|------|
| `quick_xml(tag, text, **attrs)` | 快速创建 | `quick_xml('div', 'Hi', class_='c')` |
| `count_elements(root, tag)` | 统计元素 | `count_elements(root, 'book')` |
| `get_all_tags(root)` | 获取所有标签 | `get_all_tags(root)` |

---

## 💡 实用示例

### 1. 解析配置文件

```python
config_xml = """
<config>
    <database host="localhost" port="5432">
        <name>mydb</name>
        <user>admin</user>
    </database>
    <logging level="INFO">
        <file>/var/log/app.log</file>
    </logging>
</config>
"""

root = parse_xml(config_xml)
db = find_element(root, './/database')
host = get_attribute(db, 'host')
db_name = get_element_text(find_element(db, './/name'))
print(f"数据库：{db_name} @ {host}")
```

### 2. 数据导出为 CSV

```python
data_xml = """
<products>
    <product id="1">
        <name>商品 A</name>
        <price>99.00</price>
        <stock>100</stock>
    </product>
    <product id="2">
        <name>商品 B</name>
        <price>199.00</price>
        <stock>50</stock>
    </product>
</products>
"""

columns = {
    'ID': '@id',
    '名称': 'name',
    '价格': 'price',
    '库存': 'stock'
}

csv_data = xml_to_csv(data_xml, './/product', columns)
print(csv_data)
# 输出:
# ID，名称，价格，库存
# 1，商品 A,99.00,100
# 2，商品 B,199.00,50
```

### 3. 构建 XML 文档

```python
# 创建 RSS 订阅
items = [
    create_element('item', children=[
        create_element('title', text='文章标题 1'),
        create_element('link', text='https://example.com/1'),
    ]),
    create_element('item', children=[
        create_element('title', text='文章标题 2'),
        create_element('link', text='https://example.com/2'),
    ]),
]

channel = create_element('channel', children=[
    create_element('title', text='我的博客'),
    create_element('link', text='https://example.com'),
] + items)

rss = create_xml_document('rss', children=[channel])
print(rss)
```

### 4. 数据验证

```python
user_xml = """
<user id="123">
    <name>张三</name>
    <email>zhangsan@example.com</email>
</user>
"""

root = parse_xml(user_xml)

# 检查必需字段
required = ['.//name', './/email']
valid, missing = has_required_elements(root, required)

if not valid:
    print(f"缺少字段：{missing}")
else:
    print("数据完整 ✓")

# Schema 验证
schema = {
    'tag': 'user',
    'required_children': ['name', 'email'],
    'required_attributes': ['id'],
}

valid, errors = validate_xml_structure(root, schema)
if not valid:
    for err in errors:
        print(f"验证错误：{err}")
```

### 5. XML 与 JSON 互转

```python
# XML → JSON
xml_data = """
<person>
    <name>Alice</name>
    <age>25</age>
    <skills>
        <skill>Python</skill>
        <skill>JavaScript</skill>
    </skills>
</person>
"""

json_str = xml_to_json(xml_data)
print(json_str)

# JSON → XML
json_data = '{"book": {"title": "Python", "year": 2024}}'
xml_str = json_to_xml(json_data, 'library')
print(xml_str)
```

### 6. 批量处理

```python
# 批量解析多个 XML
xml_list = [xml1, xml2, xml3]
results = batch_parse_xml(xml_list)

for i, (root, error) in enumerate(results):
    if error:
        print(f"文件 {i} 解析失败：{error}")
    else:
        print(f"文件 {i} 解析成功")

# 批量提取数据
xpaths = ['.//title', './/author', './/price']
data = batch_extract(xml_data, xpaths)

for xpath, values in data.items():
    print(f"{xpath}: {values}")
```

---

## 🔧 高级用法

### 命名空间处理

```python
# 带命名空间的 XML
ns_xml = """
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
    <soap:Body>
        <ns:GetData xmlns:ns="http://example.com">
            <ns:Id>123</ns:Id>
        </ns:GetData>
    </soap:Body>
</soap:Envelope>
"""

register_namespace('soap', 'http://schemas.xmlsoap.org/soap/envelope/')
register_namespace('ns', 'http://example.com')

root = parse_xml(ns_xml)
namespaces = {
    'soap': 'http://schemas.xmlsoap.org/soap/envelope/',
    'ns': 'http://example.com'
}

elements = find_with_namespace(root, './/ns:Id', namespaces)
print(get_element_text(elements[0]))  # 123
```

### 自定义 Schema 验证

```python
schema = {
    'tag': 'catalog',
    'required_children': ['book'],
    'optional_children': ['magazine'],
    'required_attributes': ['version'],
    'children_schema': {
        'book': {
            'required_children': ['title', 'author'],
            'required_attributes': ['isbn'],
        }
    }
}

valid, errors = validate_xml_structure(root, schema)
if not valid:
    for error in errors:
        print(f"❌ {error}")
```

---

## 🧪 运行测试

```bash
cd AllToolkit/Python/xml_utils
python xml_utils_test.py
```

---

## 📝 注意事项

1. **零依赖**: 仅使用 Python 标准库，无需安装额外包
2. **Python 3.6+**: 需要 Python 3.6 或更高版本
3. **编码**: 默认使用 UTF-8 编码
4. **XPath 支持**: 使用 ElementTree 的有限 XPath 支持
5. **大文件**: 处理大文件建议使用 `parse_xml_file` 而非字符串解析

---

## 📄 License

MIT License - 自由使用、修改和分发
