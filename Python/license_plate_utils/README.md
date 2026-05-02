# Python License Plate Utils 🚗

中国车牌号工具模块，支持车牌验证、生成、解析、批量分析等功能。

## ✨ 特性

- **零依赖** - 仅使用 Python 标准库
- **功能丰富** - 30+ 个实用函数
- **支持新能源车牌** - D/F 类型电动车牌
- **支持特殊车牌** - 警车、教练车、使馆车等
- **生产就绪** - 121 个测试用例全部通过

## 📦 安装

将 `mod.py` 添加到您的项目中：

```bash
cp Python/license_plate_utils/mod.py YourProject/license_plate_utils.py
```

## 🚀 快速开始

```python
from mod import validate, parse, generate, get_province

# 验证车牌
print(validate("京A12345"))  # True
print(validate("粤B12345警"))  # True

# 解析车牌信息
info = parse("粤B12345警")
print(info.province)       # 粤
print(info.province_name)  # 广东省
print(info.special_type)   # 警
print(info.is_special())   # True

# 生成随机车牌
print(generate())           # 随机省份随机号码
print(generate(province="京"))  # 京X...

# 获取省份
print(get_province("沪C12345"))  # 上海市
```

## 📚 API 文档

### 验证函数

| 函数 | 描述 | 返回类型 |
|------|------|---------|
| `validate(plate)` | 验证车牌是否有效 | `bool` |
| `parse(plate)` | 解析车牌详细信息 | `LicensePlate \| None` |
| `validate_format(plate)` | 验证格式并返回错误信息 | `Tuple[bool, str]` |

### 生成函数

| 函数 | 描述 | 参数 |
|------|------|------|
| `generate()` | 生成随机车牌 | `province, city_code, special_type` |
| `generate_batch(count)` | 批量生成 | `count, province, city_code, special_type` |
| `generate_nice_number()` | 生成靓号车牌 | `province, city_code, pattern` |

靓号模式：
- `'sequential'` - 连号 (如 12345)
- `'repeat'` - 重复号 (如 88888)
- `'palindrome'` - 回文号 (如 12321)
- `'mixed_repeat'` - 混合重复 (如 AA888)

### 解析函数

| 函数 | 描述 | 返回类型 |
|------|------|---------|
| `get_province(plate)` | 获取省份名称 | `str \| None` |
| `get_province_short(plate)` | 获取省份简称 | `str \| None` |
| `get_city_code(plate)` | 获取城市代码 | `str \| None` |
| `get_number(plate)` | 获取号码部分 | `str \| None` |
| `get_type(plate)` | 获取类型描述 | `str \| None` |

### 类型判断

| 函数 | 描述 |
|------|------|
| `is_special(plate)` | 是否为特殊车牌 |
| `is_police(plate)` | 是否为警用车牌 |
| `is_learner(plate)` | 是否为教练车 |
| `is_embassy(plate)` | 是否为使馆车 |
| `is_temporary(plate)` | 是否为临时车牌 |
| `is_electric(plate)` | 是否为电动车牌 |

### 编码函数

| 函数 | 描述 |
|------|------|
| `encode_number(plate)` | 将号码编码为数值 |
| `decode_number(code)` | 将数值解码为号码 |

### 比较与匹配

| 函数 | 描述 |
|------|------|
| `compare(plate1, plate2)` | 比较两个车牌 |
| `match_pattern(plate, pattern)` | 模式匹配 |

模式语法：
- `?` - 匹配任意单个字符
- `*` - 匹配任意多个字符
- `[ABC]` - 匹配 A、B 或 C
- `[!ABC]` - 不匹配 A、B 或 C

### 统计函数

| 函数 | 描述 |
|------|------|
| `analyze_batch(plates)` | 批量分析车牌 |

### 格式化函数

| 函数 | 描述 |
|------|------|
| `format_plate(plate, separator)` | 格式化输出 |
| `format_with_province(plate)` | 显示车牌和省份 |

### 辅助函数

| 函数 | 描述 |
|------|------|
| `list_provinces()` | 列出所有省份简称 |
| `list_province_names()` | 列出省份名称映射 |
| `list_special_types()` | 列出特殊车牌类型 |
| `is_valid_char(char)` | 检查字符是否有效 |
| `get_char_type(char)` | 获取字符类型 |

## 📝 使用示例

### 车牌验证

```python
from mod import validate, validate_format

# 快速验证
print(validate("京A12345"))      # True
print(validate("粤B12345警"))    # True
print(validate("粤AD1234"))      # True (新能源)
print(validate("京I12345"))      # False (含I)

# 详细验证
result, msg = validate_format("京A12345")
print(result)  # True
print(msg)     # "车牌格式有效"
```

### 解析车牌信息

```python
from mod import parse

info = parse("粤B12345警")
print(info.full_plate)       # 粤B12345警
print(info.province)         # 粤
print(info.province_name)    # 广东省
print(info.city_code)        # B
print(info.number)           # 12345
print(info.special_type)     # 警
print(info.get_type_description())  # 警用车辆
print(info.is_special())     # True
```

### 生成车牌

```python
from mod import generate, generate_batch, generate_nice_number

# 随机生成
print(generate())           # 随机车牌
print(generate(province="京"))  # 京X...

# 指定省份和城市
print(generate(province="粤", city_code="A"))  # 粤A...

# 生成特殊车牌
print(generate(province="京", special_type="警"))  # 京X...警

# 批量生成
plates = generate_batch(10, province="沪")
print(len(plates))  # 10

# 靓号车牌
print(generate_nice_number(pattern='repeat'))  # 如 京A88888
print(generate_nice_number(pattern='palindrome'))  # 如 京A12321
```

### 类型判断

```python
from mod import is_police, is_learner, is_electric

print(is_police("京A12345警"))    # True
print(is_learner("鲁B12345学"))   # True
print(is_electric("粤AD1234"))    # True (纯电)
print(is_electric("粤AF1234"))    # True (插电混动)
print(is_electric("京A12345电"))  # True
```

### 模式匹配

```python
from mod import match_pattern

# 查找北京车牌
print(match_pattern("京A12345", "[京津沪]A*"))  # True

# 查找警车
print(match_pattern("京A12345警", "*警"))       # True

# 查找特定号码
print(match_pattern("京A88888", "京A?????"))    # True
```

### 批量分析

```python
from mod import analyze_batch

plates = ["京A12345", "粤B12345", "沪C12345", "京A12345警"]
result = analyze_batch(plates)
print(result['total'])              # 4
print(result['valid'])              # 4
print(result['province_distribution'])  # {'京': 2, '粤': 1, '沪': 1}
```

### 车牌集合管理

```python
from mod import LicensePlateSet

# 创建集合
plate_set = LicensePlateSet()
plate_set.add("京A12345")
plate_set.add("粤B12345")
plate_set.add("京A12345警")

# 查询
print(plate_set.contains("京A12345"))  # True
print(plate_set.count())               # 3

# 筛选
print(plate_set.filter_by_province("京"))  # ['京A12345', '京A12345警']
print(plate_set.filter_by_special_type("警"))  # ['京A12345警']

# 分析
analysis = plate_set.analyze()
print(analysis)
```

## 🧪 测试

运行测试：

```bash
python Python/license_plate_utils/test_license_plate.py
```

测试覆盖：
- ✅ 常量测试 (5 个测试)
- ✅ 验证测试 (12 个测试)
- ✅ 解析测试 (10 个测试)
- ✅ validate_format 测试 (3 个测试)
- ✅ 生成测试 (10 个测试)
- ✅ 靓号生成测试 (3 个测试)
- ✅ 获取信息测试 (6 个测试)
- ✅ 类型判断测试 (10 个测试)
- ✅ 编码测试 (5 个测试)
- ✅ 比较测试 (5 个测试)
- ✅ 模式匹配测试 (5 个测试)
- ✅ 批量分析测试 (5 个测试)
- ✅ 格式化测试 (5 个测试)
- ✅ 辅助函数测试 (7 个测试)
- ✅ LicensePlate 类测试 (6 个测试)
- ✅ LicensePlateSet 类测试 (12 个测试)
- ✅ 边界值测试 (9 个测试)
- ✅ 特殊字符测试 (4 个测试)

**总计：121 个测试用例**

## 📋 支持的车牌类型

### 标准车牌
- 格式：省份简称 + 城市代码 + 5位字母/数字
- 示例：京A12345、粤B12345

### 新能源车牌
- 格式：省份简称 + 城市代码 + D/F + 4位字母/数字
- D：纯电动车
- F：非纯电动车（插电混动）
- 示例：粤AD1234、粤AF1234

### 特殊车牌
- 警：警用车辆
- 学：教练车辆
- 使：使馆车辆
- 领：领馆车辆
- 港：香港入境车辆
- 澳：澳门入境车辆
- 临：临时车牌
- 挂：挂车
- 电：电动车辆

## 📄 许可证

MIT License - 详见 [LICENSE](../../LICENSE)

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

---

**最后更新**: 2026-05-02
**版本**: 1.0.0