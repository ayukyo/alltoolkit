# Terminal Spinner Utils

终端加载动画工具集，提供多种风格的加载动画，用于显示长时间操作的进度。

## 功能特性

- 🎨 **25+ 内置动画样式** - dots, arrow, pulse, moon, hearts 等
- 🌈 **颜色支持** - 支持所有 ANSI 颜色
- ⏱️ **时间显示** - 显示已用时间
- 📊 **进度显示** - 百分比进度条
- 🔄 **迭代器支持** - 自动为迭代添加进度
- 🎯 **装饰器支持** - 一行代码为函数添加动画
- 📦 **零依赖** - 纯 Python 标准库实现
- 🔧 **高度可定制** - 自定义帧、颜色、间隔

## 安装

无需安装外部依赖，直接复制 `mod.py` 到项目中使用。

## 快速开始

### 基本使用

```python
from mod import Spinner

# 使用上下文管理器
with Spinner("Loading..."):
    time.sleep(2)

# 手动控制
spinner = Spinner("Processing...")
spinner.start()
# 执行长时间操作
spinner.stop()
```

### 选择动画样式

```python
# 内置样式
styles = ['dots', 'arrow', 'pulse', 'moon', 'hearts', 'clock']

for style in styles:
    with Spinner(f"Using {style} style", style=style):
        time.sleep(1)
```

### 添加颜色

```python
# 支持的颜色
colors = ['red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'white']

with Spinner("Colored spinner", color='cyan'):
    time.sleep(2)
```

### 显示时间和进度

```python
# 显示已用时间
with Spinner("Computing...", show_elapsed=True):
    time.sleep(3)

# 显示进度百分比
spinner = Spinner("Processing...", show_progress=True)
spinner.start()
for i in range(100):
    spinner.set_progress(i / 100)
    time.sleep(0.02)
spinner.stop()
```

## 高级用法

### 快捷上下文管理器

```python
from mod import spinner

with spinner("Loading...", style='dots', color='blue'):
    time.sleep(2)
```

### 函数装饰器

```python
from mod import spin

@spin("Downloading file...", style='earth')
def download_file(url):
    # 执行下载
    time.sleep(2)
    return "downloaded"

result = download_file("https://example.com/file")
```

### 迭代器包装

```python
from mod import SpinnerIterator

items = range(100)
for item in SpinnerIterator(items, "Processing items"):
    process(item)
```

### 动画等待

```python
from mod import animated_wait

# 等待5秒，显示动画
animated_wait(5, "Please wait...", style='moon')
```

### 多任务并发

```python
from mod import MultiSpinner

with MultiSpinner() as ms:
    task1 = ms.add("Downloading file 1", 'dots', 'blue')
    task2 = ms.add("Processing data", 'arrow', 'green')
    
    time.sleep(1)
    ms.complete(task1, success=True)
    
    time.sleep(0.5)
    ms.complete(task2, success=False, message="Failed!")
```

### 自定义动画帧

```python
frames = ['😊', '😄', '😃', '😀', '😃', '😄']
with Spinner("Happy loading...", frames=frames):
    time.sleep(2)
```

### 动态更新消息

```python
with Spinner("Initializing...") as s:
    time.sleep(0.5)
    s.update("Loading config...")
    time.sleep(0.5)
    s.update("Connecting to server...")
    time.sleep(0.5)
    s.update("Done!")
```

## 内置样式

| 样式名 | 描述 |
|--------|------|
| `dots` | 经典点阵旋转 |
| `dots2` | 方块旋转 |
| `dots3` | 点阵渐变 |
| `line` | 线条旋转 |
| `line2` | 渐变线 |
| `pipe` | 管道旋转 |
| `arrow` | 箭头旋转 |
| `arrow2` | 箭头流动 |
| `bounce` | 弹跳进度条 |
| `pulse` | 脉冲条 |
| `wave` | 波浪效果 |
| `triangle` | 三角旋转 |
| `square` | 方块闪烁 |
| `star` | 星星闪烁 |
| `moon` | 月相变化 🌙 |
| `earth` | 地球旋转 🌍 |
| `clock` | 时钟旋转 🕐 |
| `hearts` | 爱心跳动 ❤️ |
| `hamburger` | 汉堡食物 🍔 |
| `weather` | 天气变化 ⛅ |
| `balloon` | 气球庆祝 🎈 |

## API 参考

### Spinner 类

```python
Spinner(
    message: str = "Loading...",
    style: str = 'dots',
    color: Optional[str] = None,
    interval: float = 0.1,
    frames: Optional[List[str]] = None,
    show_elapsed: bool = False,
    show_progress: bool = False,
    output: Any = sys.stderr
)
```

**参数:**
- `message` - 显示的消息
- `style` - 动画样式名称
- `color` - 颜色名称 (red, green, blue, yellow, cyan, magenta, white)
- `interval` - 帧间隔时间（秒）
- `frames` - 自定义动画帧
- `show_elapsed` - 是否显示已用时间
- `show_progress` - 是否显示进度百分比
- `output` - 输出流

**方法:**
- `start()` - 启动动画
- `stop(message=None, success=True)` - 停止动画
- `update(message)` - 更新消息
- `set_progress(progress)` - 设置进度 (0.0-1.0)

### 辅助函数

```python
# 快捷上下文管理器
with spinner(message, style='dots', color=None, interval=0.1):
    pass

# 函数装饰器
@spin(message, style='dots', color=None)
def my_function():
    pass

# 动画等待
animated_wait(seconds, message="Waiting", style='dots', color=None)

# 列出所有样式
styles = list_styles()

# 预览所有样式
preview_styles()
```

### SpinnerIterator 类

```python
for item in SpinnerIterator(iterable, message, style='dots', color=None):
    process(item)
```

### MultiSpinner 类

```python
with MultiSpinner(interval=0.1) as ms:
    task_id = ms.add(message, style='dots', color=None)
    ms.complete(task_id, success=True, message=None, symbol=None)
```

## 使用场景

- 📥 文件下载进度
- 🔄 数据处理任务
- 🌐 网络请求等待
- 📊 数据库查询
- 🔧 系统初始化
- 📦 包安装过程
- 🧪 测试运行

## 示例

查看 `examples/` 目录获取更多示例代码。

## 测试

运行测试套件：

```bash
python spinner_utils_test.py
```

## 许可证

MIT License