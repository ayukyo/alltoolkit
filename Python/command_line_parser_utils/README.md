# Command Line Parser Utils


命令行参数解析工具
================

零外部依赖的命令行参数解析器，支持：
- 短选项 (-v) 和长选项 (--verbose)
- 选项参数 (--file=foo.txt 或 --file foo.txt)
- 位置参数
- 子命令
- 自动生成帮助信息
- 参数验证和类型转换
- 默认值支持

作者: AllToolkit 自动生成
日期: 2026-04-26


## 功能

### 类

- **ArgType**: 参数类型
- **Argument**: 参数定义
  方法: get_dest
- **Command**: 子命令定义
- **ParseResult**: 解析结果
  方法: get
- **CommandLineParser**: 命令行参数解析器
  方法: add_argument, add_command, parse, format_help, format_usage

### 函数

- **create_parser(prog, description, version**) - 创建命令行解析器的便捷函数
- **int_converter(value**) - 整数转换器
- **float_converter(value**) - 浮点数转换器
- **bool_converter(value**) - 布尔值转换器
- **list_converter(separator**) - 列表转换器工厂
- **range_converter(value**) - 范围转换器
- **get_dest(self**) - 获取结果中的键名
- **get(self, key, default**) - 获取参数值
- **add_argument(self, name, short**, ...) - 添加参数
- **add_command(self, name, help_text**, ...) - 添加子命令

... 共 14 个函数

## 使用示例

```python
from mod import create_parser

# 使用 create_parser
result = create_parser()
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
