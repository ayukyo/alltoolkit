# Ini Config Utils


AllToolkit - INI Config Utilities
INI配置文件解析工具模块

功能特性:
- 完整的INI文件读写支持
- 节(section)和键值对(key-value)操作
- 注释保留和智能处理
- 类型自动转换(int, float, bool)
- 默认值支持
- 配置文件验证

作者: AllToolkit
许可证: MIT


## 功能

### 类

- **IniConfigError**: INI配置相关异常基类
- **SectionNotFoundError**: 节不存在异常
- **KeyNotFoundError**: 键不存在异常
- **ParseError**: 解析错误异常
- **IniSection**: INI配置文件节(section)类

表示INI文件中的一个节，包含该节下的所有键值对。
支持字典式访问和属性式访问。

Attributes:
    name: 节名称
    _data: 存储键值对的字典
    _comments: 存储键的注释
  方法: get, get_int, get_float, get_bool, get_list ... (12 个方法)
- **IniConfig**: INI配置文件管理类

提供完整的INI文件解析、修改和生成功能。
支持多节配置、注释保留、类型转换等特性。

Attributes:
    _sections: 存储所有节的字典
    _section_comments: 存储节的注释
    _global_comments: 全局注释(文件开头)

Example:
    >>> config = IniConfig()
    >>> config
  方法: section, has_section, add_section, remove_section, sections ... (23 个方法)

### 函数

- **read_ini(filepath, encoding**) - 读取INI文件
- **write_ini(config, filepath, encoding**) - 写入INI文件
- **parse_ini(content**) - 解析INI字符串
- **create_ini(data**) - 从字典创建配置
- **get(self, key, default**, ...) - 获取键值，支持类型转换和默认值
- **get_int(self, key, default**) - 获取整数值
- **get_float(self, key, default**) - 获取浮点数值
- **get_bool(self, key, default**) - 获取布尔值
- **get_list(self, key, default**, ...) - 获取列表值
- **set(self, key, value**, ...) - 设置键值

... 共 39 个函数

## 使用示例

```python
from mod import read_ini

# 使用 read_ini
result = read_ini()
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
