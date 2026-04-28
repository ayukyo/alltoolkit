# Country Utils - 国家代码工具库

ISO 3166 国家代码和信息查询工具，零外部依赖，纯 Python 实现。

## 功能特性

- **ISO 3166-1 代码**: 支持 alpha-2、alpha-3、numeric 三种代码格式
- **国家信息**: 英文名称、中文名称、所属大陆、区域
- **电话代码**: 国际电话区号
- **货币代码**: ISO 4217 货币代码
- **国旗表情**: 自动生成国旗表情符号 🇺🇸 🇨🇳 🇯🇵
- **搜索功能**: 支持英文/中文搜索国家
- **代码转换**: alpha-2 ↔ alpha-3 ↔ numeric 互转
- **验证功能**: 验证国家代码是否有效

## 安装使用

```python
from country_utils.mod import (
    get_country,
    get_by_alpha2,
    get_by_alpha3,
    get_by_numeric,
    get_by_name,
    search_countries,
    get_flag_emoji,
    get_calling_code,
    get_currency,
)
```

## API 文档

### 查询函数

#### `get_country(code)`
根据任意代码格式查询国家（支持 alpha-2、alpha-3、numeric）。

```python
>>> get_country("US")
Country(US, United States)

>>> get_country("USA")
Country(US, United States)

>>> get_country("840")
Country(US, United States)
```

#### `get_by_alpha2(alpha2)`
根据 ISO 3166-1 alpha-2 代码查询国家。

```python
>>> get_by_alpha2("CN").name_zh
'中国'

>>> get_by_alpha2("JP").flag_emoji
'🇯🇵'
```

#### `get_by_alpha3(alpha3)`
根据 ISO 3166-1 alpha-3 代码查询国家。

```python
>>> get_by_alpha3("CHN").alpha2
'CN'

>>> get_by_alpha3("JPN").name_en
'Japan'
```

#### `get_by_numeric(numeric)`
根据 ISO 3166-1 numeric 代码查询国家。

```python
>>> get_by_numeric("156").name_en
'China'

>>> get_by_numeric("392").name_zh
'日本'
```

#### `get_by_name(name)`
根据国家名称查询（支持英文和中文）。

```python
>>> get_by_name("United States").alpha2
'US'

>>> get_by_name("中国").alpha2
'CN'

>>> get_by_name("日本").name_en
'Japan'
```

### 搜索函数

#### `search_countries(query, limit=10)`
搜索国家（支持模糊匹配、英文/中文）。

```python
>>> search_countries("United")
[Country(GB, United Kingdom), Country(US, United States)]

>>> search_countries("韩")
[Country(KR, South Korea)]

>>> search_countries("land", limit=5)
[Country(FI, Finland), Country(IS, Iceland), ...]
```

### 分组函数

#### `get_all_countries()`
获取所有国家列表。

```python
>>> len(get_all_countries())
195+

>>> get_all_countries()[0].alpha2
'AF'
```

#### `get_countries_by_continent(continent)`
按大陆获取国家列表。

```python
>>> len(get_countries_by_continent("Asia"))
48

>>> get_countries_by_continent("Europe")[0].continent
'Europe'
```

#### `get_countries_by_region(region)`
按区域获取国家列表。

```python
>>> get_countries_by_region("East Asia")
[Country(CN, China), Country(HK, Hong Kong), ...]
```

### 验证函数

#### `validate_alpha2(code)`
验证 alpha-2 代码是否有效。

```python
>>> validate_alpha2("US")
True

>>> validate_alpha2("XX")
False
```

#### `validate_alpha3(code)`
验证 alpha-3 代码是否有效。

```python
>>> validate_alpha3("USA")
True

>>> validate_alpha3("XXX")
False
```

#### `validate_numeric(code)`
验证 numeric 代码是否有效。

```python
>>> validate_numeric("840")
True

>>> validate_numeric("000")
False
```

### 转换函数

#### `alpha2_to_alpha3(alpha2)`
alpha-2 转 alpha-3。

```python
>>> alpha2_to_alpha3("US")
'USA'

>>> alpha2_to_alpha3("CN")
'CHN'
```

#### `alpha3_to_alpha2(alpha3)`
alpha-3 转 alpha-2。

```python
>>> alpha3_to_alpha2("USA")
'US'
```

#### `alpha2_to_numeric(alpha2)`
alpha-2 转 numeric。

```python
>>> alpha2_to_numeric("US")
'840'
```

#### `numeric_to_alpha2(numeric)`
numeric 转 alpha-2。

```python
>>> numeric_to_alpha2("840")
'US'
```

### 信息函数

#### `get_flag_emoji(code)`
获取国旗表情符号。

```python
>>> get_flag_emoji("US")
'🇺🇸'

>>> get_flag_emoji("CN")
'🇨🇳'

>>> get_flag_emoji("JP")
'🇯🇵'
```

#### `get_calling_code(code)`
获取国际电话区号。

```python
>>> get_calling_code("US")
'+1'

>>> get_calling_code("CN")
'+86'

>>> get_calling_code("JP")
'+81'
```

#### `get_currency(code)`
获取货币代码。

```python
>>> get_currency("US")
'USD'

>>> get_currency("CN")
'CNY'

>>> get_currency("JP")
'JPY'
```

#### `get_continents()`
获取所有大陆名称。

```python
>>> sorted(get_continents())
['Africa', 'Asia', 'Europe', 'North America', 'Oceania', 'South America']
```

#### `get_regions()`
获取所有区域名称。

```python
>>> 'East Asia' in get_regions()
True
```

## Country 数据类

```python
@dataclass
class Country:
    alpha2: str           # ISO 3166-1 alpha-2 code (e.g., "US")
    alpha3: str           # ISO 3166-1 alpha-3 code (e.g., "USA")
    numeric: str          # ISO 3166-1 numeric code (e.g., "840")
    name_en: str          # English name
    name_zh: str          # Chinese name
    continent: str        # Continent
    region: str           # Region
    calling_code: str     # International calling code
    currency: str         # ISO 4217 currency code
    flag_emoji: str       # Flag emoji
    
    def to_dict(self) -> Dict:
        """Convert to dictionary"""
```

## 大陆和区域划分

### 大陆 (Continents)
- Asia (亚洲)
- Europe (欧洲)
- Africa (非洲)
- North America (北美洲)
- South America (南美洲)
- Oceania (大洋洲)

### 区域 (Regions)
- East Asia (东亚): CN, JP, KR, KP, TW, HK, MO, MN
- Southeast Asia (东南亚): VN, TH, MY, SG, ID, PH, MM, LA, KH, BN, TL
- South Asia (南亚): IN, PK, BD, LK, NP, BT, MV, AF
- Central Asia (中亚): KZ, UZ, KG, TJ, TM
- West Asia (西亚): SA, AE, IL, TR, IR, IQ, JO, LB, SY, PS, YE, OM, KW, QA, BH, CY, GE, AM, AZ
- Northern Europe (北欧): GB, IE, SE, NO, DK, FI, IS, EE, LV, LT
- Western Europe (西欧): DE, FR, NL, BE, LU, AT, CH, LI, MC
- Southern Europe (南欧): IT, ES, PT, GR, MT, VA, SM, AD
- Eastern Europe (东欧): PL, CZ, SK, HU, RO, BG, UA, BY, MD, RU, SI, HR, RS, BA, ME, MK, AL, XK
- Northern Africa (北非): EG, LY, TN, DZ, MA, SD
- Western Africa (西非): NG, GH, CI, SN, ML, BF, NE
- Eastern Africa (东非): KE, ET, TZ, UG, RW, SO
- Southern Africa (南非): ZA, ZW, ZM, BW, NA, MZ, AO
- Central Africa (中非): CF, TD, CG, CD, GQ, GA
- Central America (中美): GT, BZ, SV, HN, NI, CR, PA
- Caribbean (加勒比): CU, JM, HT, DO, PR, BS, TT

## 示例

参见 `examples/demo.py`。

## 测试

```bash
python country_utils_test.py
```

## 作者

AllToolkit

## 许可证

MIT