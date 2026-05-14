# Chinese ID Utils 🆔

中国身份证工具模块 - 提供中国大陆居民身份证号码的验证、解析和信息提取功能。

## 功能特性

- **格式验证** - 15位和18位身份证格式校验
- **校验码验证** - 符合GB 11643-1999标准
- **地区码解析** - 省/市/区三级地区信息
- **出生日期提取** - 从身份证号提取生日
- **性别判断** - 根据第17位判断性别
- **年龄计算** - 自动计算当前年龄
- **15位转18位** - 旧版身份证升级
- **批量解析** - 支持批量处理身份证信息

## 快速开始

```python
from chinese_id_utils.mod import validate, parse, IDInfo

# 基础验证
is_valid, message = validate("110105199003072334")
print(is_valid)  # True/False
print(message)   # 错误信息

# 解析身份证信息
info = parse("110105199003072334")
print(info)
# IDInfo(
#     valid=True,
#     id_number='110105199003072334',
#     province='北京市',
#     city='北京市市辖区',
#     district='朝阳区',
#     birth_date=date(1990, 3, 7),
#     gender='男',
#     age=34,
#     checksum_valid=True,
#     format_valid=True,
#     error_message=None
# )
```

## 核心函数

### validate(id_number)

验证身份证号码是否有效。

```python
from chinese_id_utils.mod import validate

valid, msg = validate("110105199003072334")
if valid:
    print("身份证有效")
else:
    print(f"无效: {msg}")
```

### parse(id_number)

解析身份证号码，返回详细信息。

```python
from chinese_id_utils.mod import parse

info = parse("110105199003072334")
print(f"省份: {info.province}")
print(f"出生日期: {info.birth_date}")
print(f"性别: {info.gender}")
print(f"年龄: {info.age}")
```

### convert_15_to_18(id_15)

将15位身份证号码转换为18位。

```python
from chinese_id_utils.mod import convert_15_to_18

id_18 = convert_15_to_18("110105900307233")
print(id_18)  # 11010519900307233X
```

## 其他功能

### 获取地区信息

```python
from chinese_id_utils.mod import get_region_info

region = get_region_info("110105")
print(region)
# {'province': '北京市', 'city': '北京市市辖区', 'district': '朝阳区'}
```

### 批量验证

```python
from chinese_id_utils.mod import validate_batch

ids = ["110105199003072334", "31010119800101001X", "invalid_id"]
results = validate_batch(ids)
for id_num, valid, msg in results:
    print(f"{id_num}: {'有效' if valid else '无效'}")
```

### 生成测试身份证

```python
from chinese_id_utils.mod import generate_test_id

# 生成测试用的身份证号
test_id = generate_test_id(
    province_code="11",  # 北京市
    birth_date="19900101",
    gender="male"
)
print(test_id)
```

## 身份证结构

### 18位身份证结构

```
110105 1990 03 07 233 4
├──┴── └─┴─ └─┴─ └─┴─ └─┴─ └─┴─
地区码   年份  月  日  顺序码 校验码
(6位)   (4位)(2位)(2位)(3位) (1位)
```

- **地区码 (1-6位)**: 省/市/区代码
- **出生日期 (7-14位)**: YYYYMMDD
- **顺序码 (15-17位)**: 第17位奇数为男性，偶数为女性
- **校验码 (18位)**: 根据ISO 7064:1983.MOD 11-2计算

## 支持的地区

包含全国31个省/自治区/直辖市的地区代码：

- 北京市 (110000)
- 上海市 (310000)
- 广东省 (440000)
- ... 等

## 测试

```bash
python Python/chinese_id_utils/chinese_id_utils_test.py
```

## 注意事项

- 此模块仅用于数据格式验证和信息提取
- 不涉及任何身份证核验服务
- 测试数据不包含真实身份证号码
- 请遵守相关法律法规使用

## 许可证

MIT License