# cli_args_utils

**Zig 命令行参数解析工具** - 零依赖、功能完整的 CLI 参数解析库

## 特性

- ✅ **零外部依赖** - 仅使用 Zig 标准库
- ✅ **完整功能** - 支持短选项、长选项、组合标志、位置参数
- ✅ **灵活语法** - 支持 `-f value`、`-fvalue`、`--option=value` 多种语法
- ✅ **类型安全** - 编译时类型检查，运行时安全
- ✅ **帮助生成** - 自动生成格式化的帮助文本
- ✅ **默认值** - 支持选项默认值
- ✅ **必填验证** - 支持标记必填参数

## 安装

将 `mod.zig` 复制到你的项目中，或者：

```bash
# 在 build.zig.zon 中添加依赖
zig fetch --save cli_args_utils git+https://github.com/ayukyo/alltoolkit#Zig/cli_args_utils
```

## 快速开始

### 基础用法

```zig
const std = @import("std");
const cli = @import("mod.zig");

pub fn main() !void {
    var gpa = std.heap.GeneralPurposeAllocator(.{}){};
    defer _ = gpa.deinit();
    const allocator = gpa.allocator();

    // 创建解析器
    var parser = cli.CliParser.init(allocator);
    defer parser.deinit();

    // 添加布尔标志
    _ = try parser.addFlag("verbose", 'v', "verbose", "Enable verbose output");
    _ = try parser.addFlag("help", 'h', "help", "Show help message");

    // 添加选项（带值）
    _ = try parser.addOption("output", 'o', "output", "Output file", false, "output.txt");
    _ = try parser.addOption("count", 'c', "count", "Number of iterations", false, "1");

    // 解析参数
    var result = try parser.parse();
    defer result.deinit();

    // 使用结果
    if (result.isPresent("verbose")) {
        std.debug.print("Verbose mode enabled\n", .{});
    }

    if (result.getValue("output")) |output| {
        std.debug.print("Output: {s}\n", .{output});
    }
}
```

### 快速检测标志

```zig
const cli = @import("mod.zig");

pub fn main() !void {
    // 简单标志检测
    const argv = try std.process.argsAlloc(allocator);
    
    if (cli.hasFlag(argv, 'v', "verbose")) {
        std.debug.print("Verbose!\n", .{});
    }
    
    if (cli.hasFlag(argv, 'h', "help")) {
        printHelp();
    }
}
```

### 快速解析

```zig
const cli = @import("mod.zig");

pub fn main() !void {
    const argv = [_][]const u8{ "app", "--name=Alice", "--verbose", "--count=42" };
    
    var result = try cli.parseSimple(allocator, &argv);
    defer {
        var iter = result.iterator();
        while (iter.next()) |entry| {
            if (entry.value_ptr.*) |v| allocator.free(v);
            allocator.free(entry.key_ptr.*);
        }
        result.deinit();
    }
    
    // name = "Alice"
    // verbose = null (标志)
    // count = "42"
}
```

## 支持的语法

### 短选项

| 语法 | 示例 | 说明 |
|------|------|------|
| `-f` | `-v` | 布尔标志 |
| `-f value` | `-o output.txt` | 选项带值（空格分隔） |
| `-fvalue` | `-ooutput.txt` | 选项带值（紧附） |
| `-abc` | `-vaf` | 组合布尔标志（等同于 `-v -a -f`） |

### 长选项

| 语法 | 示例 | 说明 |
|------|------|------|
| `--flag` | `--verbose` | 布尔标志 |
| `--option value` | `--output file.txt` | 选项带值（空格分隔） |
| `--option=value` | `--output=file.txt` | 选项带值（等号连接） |

### 位置参数

```bash
myapp -v --output=result.txt file1.txt file2.txt file3.txt
#                                 ^^^^^^^^ ^^^^^^^^ ^^^^^^^^
#                                 位置参数
```

## API 参考

### CliParser

```zig
var parser = cli.CliParser.init(allocator);
defer parser.deinit();
```

#### 配置方法

| 方法 | 说明 |
|------|------|
| `setProgramName(name)` | 设置程序名称（用于帮助文本） |
| `setDescription(desc)` | 设置程序描述 |
| `addFlag(name, short, long, description)` | 添加布尔标志 |
| `addOption(name, short, long, desc, required, default)` | 添加带值选项 |

#### 解析方法

| 方法 | 说明 |
|------|------|
| `parse()` | 从 os.argv 解析 |
| `parseFromSlice(argv)` | 从字符串数组解析 |

### ParseResult

```zig
var result = try parser.parse();
defer result.deinit();
```

| 方法 | 返回类型 | 说明 |
|------|----------|------|
| `isPresent(name)` | `bool` | 检查参数是否出现 |
| `getValue(name)` | `?[]const u8` | 获取参数值 |
| `get(name)` | `?ParsedArg` | 获取完整参数信息 |
| `getPositional(index)` | `?[]const u8` | 获取位置参数 |

### 工具函数

```zig
// 快速检测标志
cli.hasFlag(argv, short, long) bool

// 快速获取选项值
cli.getOption(argv, short, long) ?[]const u8

// 快速解析
cli.parseSimple(allocator, argv) !StringHashMap(?[]const u8)

// 获取位置参数
cli.getPositionalArgs(allocator, argv) ![][]const u8
cli.countPositionalArgs(argv) usize
```

## 示例

### 文件处理 CLI

```zig
var parser = cli.CliParser.init(allocator);
defer parser.deinit();

_ = parser.setProgramName("fileproc");
_ = try parser.addFlag("verbose", 'v', "verbose", "Verbose output");
_ = try parser.addFlag("recursive", 'r', "recursive", "Process recursively");
_ = try parser.addOption("output", 'o', "output", "Output dir", false, ".");
_ = try parser.addOption("suffix", 's', "suffix", "File suffix", false, ".txt");

var result = try parser.parse();
defer result.deinit();

// 处理文件
for (result.positional.items) |file| {
    if (result.isPresent("verbose")) {
        std.debug.print("Processing: {s}\n", .{file});
    }
    // ... 处理逻辑
}
```

### 生成帮助文本

```zig
var parser = cli.CliParser.init(allocator);
defer parser.deinit();

_ = parser.setProgramName("myapp");
_ = parser.setDescription("A powerful CLI tool");
_ = try parser.addFlag("verbose", 'v', "verbose", "Enable verbose output");
_ = try parser.addOption("output", 'o', "output", "Output directory", false, ".");
_ = try parser.addOption("config", 'c', "config", "Config file", true, null);

// 生成帮助
var buffer = std.ArrayList(u8).init(allocator);
defer buffer.deinit();
try parser.generateHelp(buffer.writer());
std.debug.print("{s}", .{buffer.items});
```

输出：
```
Usage: myapp [options]

A powerful CLI tool

Options:
  -v, --verbose          Enable verbose output
  -o, --output <value>   Output directory (default: .)
  -c, --config <value>   Config file [required]
```

## 运行测试

```bash
cd Zig/cli_args_utils
zig test cli_args_utils_test.zig
```

## 运行示例

```bash
cd Zig/cli_args_utils
zig run examples/usage_examples.zig
```

## 许可证

MIT License