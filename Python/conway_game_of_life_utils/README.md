# Conway's Game of Life Utils

**康威生命游戏工具集** - 一个完整的细胞自动机模拟器

## 🎮 功能特性

- ✅ **基本生命游戏模拟** - 标准 B3/S23 规则
- ✅ **多种规则变体** - HighLife, Day & Night, Seeds 等 12+ 种规则
- ✅ **内置经典模式** - 滑翔机、枪、振荡器、Methuselah 等
- ✅ **RLE 格式支持** - 导入/导出标准 RLE 格式
- ✅ **无限网格** - 支持无限扩展的网格系统
- ✅ **统计分析** - 细胞计数、密度、边界、振荡周期等
- ✅ **ASCII 可视化** - 网格的字符串表示
- ✅ **模式检测** - 自动检测模式类型（静止生命、振荡器、太空船）
- ✅ **零外部依赖** - 仅使用 Python 标准库

## 📦 安装

```bash
# 直接使用
python -m conway_game_of_life_utils.mod

# 或者复制 mod.py 到你的项目中
```

## 🚀 快速开始

### 基本使用

```python
from conway_game_of_life_utils.mod import GameOfLife, Pattern

# 创建游戏
game = GameOfLife()

# 加载滑翔机模式
game.load_pattern_by_name('glider')

# 显示初始状态
print(game.to_string(alive='■', dead='·'))

# 演化 4 代
game.step(4)

# 显示演化后的状态
print(game.to_string())
```

### 使用不同规则

```python
from conway_game_of_life_utils.mod import GameOfLife, RULES, Rule

# 使用 HighLife 规则
game = GameOfLife(rule=RULES['highlife'])

# 使用自定义规则
custom_rule = Rule({3, 6}, {2, 3}, "MyRule")
game = GameOfLife(rule=custom_rule)

# 从字符串创建规则
rule = Rule.from_string("B36/S23")
```

### 加载内置模式

```python
from conway_game_of_life_utils.mod import Pattern

# 获取模式列表
glider = Pattern.get('glider')
block = Pattern.get('block')
pulsar = Pattern.get('pulsar')
glider_gun = Pattern.get('glider_gun')
```

## 📚 内置模式

### 仍然生命 (Still Lifes)
- `block` - 方块 (4 细胞)
- `beehive` - 蜂巢 (6 细胞)
- `loaf` - 面包 (7 细胞)
- `boat` - 船 (5 细胞)
- `tub` - 盆 (4 细胞)

### 振荡器 (Oscillators)
- `blinker` - 闪烁器 (周期 2)
- `toad` - 癞蛤蟆 (周期 2)
- `beacon` - 信标 (周期 2)
- `pulsar` - 脉冲星 (周期 3)
- `pentadecathlon` - 十五连环 (周期 15)

### 太空船 (Spaceships)
- `glider` - 滑翔机 (最小太空船)
- `lwss` - 轻量级太空船
- `mwss` - 中量级太空船
- `hwss` - 重量级太空船

### 枪 (Guns)
- `glider_gun` - Gosper 滑翔机枪

### Methuselah (长期不稳定模式)
- `r_pentomino` - R 五连块
- `acorn` - 橡子
- `diehard` - 死硬派

## 🔧 API 参考

### GameOfLife 类

```python
class GameOfLife:
    def __init__(self, rule=None, width=100, height=100):
        """初始化游戏"""
    
    def set_cell(self, x, y, alive=True):
        """设置单元格状态"""
    
    def toggle_cell(self, x, y):
        """切换单元格状态"""
    
    def get_cell(self, x, y):
        """获取单元格状态"""
    
    def clear(self):
        """清空网格"""
    
    def load_pattern(self, pattern, offset=(0, 0)):
        """加载模式"""
    
    def load_pattern_by_name(self, name, offset=(0, 0)):
        """根据名称加载内置模式"""
    
    def load_rle(self, rle, offset=(0, 0)):
        """从 RLE 格式加载"""
    
    def to_rle(self):
        """导出为 RLE 格式"""
    
    def step(self, generations=1):
        """演化指定代数"""
    
    def get_bounds(self):
        """获取活细胞边界"""
    
    def get_grid(self, padding=0):
        """获取网格表示"""
    
    def to_string(self, alive='█', dead=' ', padding=0):
        """转换为字符串表示"""
    
    def count_cells(self):
        """获取活细胞数量"""
    
    def get_statistics(self):
        """获取统计信息"""
    
    def copy(self):
        """创建游戏副本"""
```

### Rule 类

```python
class Rule:
    def __init__(self, birth, survival, name="Custom"):
        """初始化规则"""
    
    @classmethod
    def from_string(cls, rule_str, name="Custom"):
        """从规则字符串创建"""
    
    def __str__(self):
        """返回规则字符串表示"""
```

### 辅助函数

```python
def run_simulation(pattern, generations=100, rule=None, stop_if_stable=True):
    """运行模拟并分析结果"""

def detect_pattern_type(cells, max_generations=4):
    """检测模式类型"""

def pattern_to_ascii(pattern, alive='■', dead='·'):
    """将模式转换为 ASCII 艺术"""

def generate_random_pattern(density=0.3, width=20, height=20, seed=None):
    """生成随机模式"""

def compare_patterns(pattern1, pattern2):
    """比较两个模式"""
```

## 📊 预定义规则

| 规则 | 符号 | 描述 |
|------|------|------|
| Conway's Life | B3/S23 | 标准规则 |
| HighLife | B36/S23 | 支持 B6 复制 |
| Day & Night | B3678/S3678 | 对称规则 |
| Seeds | B2/S | 爆炸性增长 |
| Maze | B3/S12345 | 生成迷宫 |
| Diamoeba | B35678/S5678 | 钻石形 |
| Anneal | B35678/S4678 | 收缩规则 |
| 2x2 | B36/S125 | 2x2 块规则 |
| Live Free or Die | B3/S012345678 | 无死亡规则 |
| Gnarl | B1/S1 | 极简规则 |
| Replicator | B1357/S1357 | 复制规则 |
| Plow World | B3/S123456 | 类迷宫 |
| Serviettes | B234/S | 瀑布效应 |

## 📝 RLE 格式

RLE (Run Length Encoded) 是生命游戏的标准模式格式：

```
#C Name: Glider
#C Author: Richard K. Guy
x = 3, y = 3, rule = B3/S23
bo$2bo$3o!
```

- `#C` - 注释行
- `x`, `y` - 模式尺寸
- `rule` - 游戏规则
- `b` 或 `.` - 死细胞
- `o` 或 `*` - 活细胞
- `$` - 换行
- `!` - 结束
- 数字前缀表示重复次数

## 🎯 使用示例

### 演化滑翔机枪

```python
game = GameOfLife()
game.load_pattern_by_name('glider_gun')

# 观察滑翔机产生
for gen in [0, 30, 60, 90]:
    temp = game.copy()
    temp.step(gen)
    print(f"第 {gen} 代: {temp.count_cells()} 个活细胞")
```

### 模式类型检测

```python
cells = set(Pattern.BLINKER)
type_str = detect_pattern_type(cells)
print(type_str)  # "Oscillator"
```

### 比较模式

```python
result = compare_patterns(set(Pattern.GLIDER), set(Pattern.LWSS))
print(f"相似度: {result['similarity']}")
```

## 🧪 测试

```bash
python conway_game_of_life_utils_test.py
```

测试覆盖：
- 规则创建和解析
- 模式加载和演化
- 仍然生命稳定性
- 振荡器周期验证
- 太空船移动
- RLE 格式导入/导出
- 不同规则变体
- 边界值（空、单细胞、大坐标等）

## 📄 许可证

MIT License

---

**最后更新**: 2026-05-17