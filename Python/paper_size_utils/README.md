# Paper Size Utils 📄

纸张尺寸工具模块，提供国际标准纸张尺寸查询、转换、计算等功能。

## 特性

- ✅ **ISO A/B/C 系列** - 完整的国际标准纸张尺寸
- ✅ **北美纸张系列** - Letter、Legal、ANSI、Arch 等美国标准
- ✅ **JIS B 系列** - 日本工业标准纸张尺寸
- ✅ **中国标准** - D 系列图纸尺寸
- ✅ **照片尺寸** - 2R ~ 12R 等常用照片打印尺寸
- ✅ **名片尺寸** - 各国标准名片尺寸
- ✅ **信封尺寸** - ISO C 系列、美国标准信封
- ✅ **像素转换** - DPI 计算、毫米与像素互转
- ✅ **智能查找** - 根据尺寸、面积、宽高比查找纸张
- ✅ **ISO 计算** - 计算任意 ISO 系列纸张尺寸

## 快速开始

### 获取纸张尺寸

```python
from paper_size_utils import get_paper_size, PaperSize

# 获取 A4 信息
a4 = get_paper_size("A4")
print(f"A4: {a4.width_mm}×{a4.height_mm}mm")

# 获取像素尺寸
width_px, height_px = a4.to_pixels(300)  # 300 DPI
print(f"A4 @ 300 DPI: {width_px}×{height_px}px")
```

### 获取所有纸张尺寸

```python
from paper_size_utils import get_all_paper_sizes, list_available_papers

# 列出所有可用纸张名称
papers = list_available_papers()
print(f"共 {len(papers)} 种纸张")

# 获取全部纸张尺寸字典
all_sizes = get_all_paper_sizes()
```

### 按系列获取

```python
from paper_size_utils import get_paper_sizes_by_series, PaperSeries

# 获取 ISO A 系列
a_series = get_paper_sizes_by_series(PaperSeries.ISO_A)
for name, paper in a_series.items():
    print(f"{name}: {paper.width_mm}×{paper.height_mm}mm")
```

### 搜索纸张

```python
from paper_size_utils import search_paper_sizes

# 搜索信封
envelopes = search_paper_sizes("信封")
for env in envelopes:
    print(f"{env.name}: {env.description}")
```

### 单位转换

```python
from paper_size_utils import mm_to_pixels, pixels_to_mm, inch_to_mm, mm_to_inch

# 毫米转像素（300 DPI）
pixels = mm_to_pixels(210, 300)  # 2481

# 像素转毫米
mm = pixels_to_mm(2481, 300)  # 210.0

# 英寸转毫米
mm = inch_to_mm(8.5)  # 215.9

# 毫米转英寸
inch = mm_to_inch(210)  # 8.2677
```

### 根据尺寸查找纸张

```python
from paper_size_utils import find_paper_by_dimensions

# 查找 210×297mm 对应的纸张
papers = find_paper_by_dimensions(210, 297, "mm")
print([p.name for p in papers])  # ['A4']
```

### 根据面积查找

```python
from paper_size_utils import find_paper_by_area

# 查找面积约 62370 mm² 的纸张（A4）
papers = find_paper_by_area(62370, "mm2")
```

### 根据宽高比查找

```python
from paper_size_utils import find_paper_by_aspect_ratio

# ISO 系列宽高比为 √2 ≈ 0.707
papers = find_paper_by_aspect_ratio(0.707, 0.01)
for p in papers[:5]:
    print(f"{p.name}: ratio={p.aspect_ratio:.4f}")
```

### 计算任意 ISO 尺寸

```python
from paper_size_utils import calculate_iso_paper_size

# 计算 A15（扩展尺寸）
a15 = calculate_iso_paper_size("A", 15)
print(f"A15: {a15.width_mm:.4f}×{a15.height_mm:.4f}mm")

# 计算 B 系列
b5 = calculate_iso_paper_size("B", 5)
```

### 比较纸张

```python
from paper_size_utils import compare_paper_sizes

result = compare_paper_sizes("A4", "Letter")
print(f"A4 比 Letter 小 {result['area_ratio']:.2%}")
print(f"宽度差异: {result['width_difference_mm']:.2f}mm")
```

### 查找最佳匹配纸张

```python
from paper_size_utils import get_best_fit_paper

# 找到能容纳 200×280mm 的最小纸张
paper = get_best_fit_paper(200, 280, "mm")
print(paper.name)  # A4
```

### 打印详细信息

```python
from paper_size_utils import print_paper_info

info = print_paper_info("A4")
print(info)
```

## PaperSize 数据类

```python
class PaperSize:
    name: str          # 纸张名称
    width_mm: float    # 宽度（毫米）
    height_mm: float   # 高度（毫米）
    series: PaperSeries # 纸张系列
    description: str   # 描述
    
    @property
    def width_cm: float        # 宽度（厘米）
    @property
    def height_cm: float       # 高度（厘米）
    @property
    def width_inch: float      # 宽度（英寸）
    @property
    def height_inch: float     # 高度（英寸）
    @property
    def area_mm2: float        # 面积（平方毫米）
    @property
    def area_cm2: float        # 面积（平方厘米）
    @property
    def area_inch2: float      # 面积（平方英寸）
    @property
    def aspect_ratio: float    # 宽高比
    
    def to_pixels(dpi: int)    # 转换为像素
    def get_orientation()      # 获取方向
    def flip()                 # 翻转方向
    def to_dict()              # 转换为字典
```

## 支持的纸张系列

| 系列 | 说明 |
|------|------|
| ISO A | 国际标准 A 系列（A0-A10） |
| ISO B | ISO B 系列（介于 A 系列之间） |
| ISO C | ISO C 系列（信封尺寸） |
| North American | 北美标准（Letter、Legal、ANSI、Arch） |
| JIS B | 日本工业标准 B 系列 |
| Chinese | 中国 D 系列图纸 |
| Photo | 照片尺寸（2R-12R） |
| Business Card | 名片尺寸 |
| Envelope | 信封尺寸 |

## 常用纸张尺寸

| 名称 | 尺寸 (mm) | 用途 |
|------|-----------|------|
| A4 | 210×297 | 标准办公纸张 |
| A3 | 297×420 | 图表、海报 |
| A5 | 148×210 | 笔记本、小册子 |
| Letter | 216×279 | 美国标准办公纸张 |
| Legal | 216×356 | 美国法律文件 |
| B5 | 176×250 | 书籍 |
| 4R | 102×152 | 标准照片 |

## 测试

```bash
python Python/paper_size_utils/paper_size_utils_test.py
```

## 许可证

MIT License