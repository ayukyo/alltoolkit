# License Key Utilities

一个纯 Python 实现的软件许可证密钥生成和验证工具库，零外部依赖。

## 功能特性

- **多种许可证类型**: Trial、Standard、Professional、Enterprise
- **灵活的过期时间**: 支持永久许可证和限时许可证
- **功能限制**: 基于功能集的许可证控制
- **硬件绑定**: 支持将许可证绑定到特定硬件
- **签名验证**: 使用 HMAC 进行密钥签名验证
- **许可证管理**: 完整的许可证生命周期管理
- **导入导出**: 支持许可证的可移植格式

## 安装

无需安装，直接复制 `license_key_utils.py` 到项目中即可使用。

```python
from license_key_utils import LicenseKeyGenerator, LicenseManager, LicenseType
```

## 快速开始

### 生成许可证

```python
from license_key_utils import LicenseKeyGenerator, LicenseType

generator = LicenseKeyGenerator()

# 生成标准许可证
key, info = generator.generate_license(
    license_type=LicenseType.STANDARD,
    product_name="MyApp",
    customer_name="John Doe",
    customer_email="john@example.com"
)

print(f"License Key: {key}")
# 输出: XXXX-XXXX-XXXX-XXXX-XXXX 格式
```

### 生成试用许可证

```python
# 14天试用许可证
key, info = generator.generate_license(
    license_type=LicenseType.TRIAL,
    product_name="MyApp",
    customer_name="Trial User",
    customer_email="trial@example.com",
    validity_days=14,
    features={"basic", "export"}
)
```

### 企业许可证（含功能限制和硬件绑定）

```python
# 生成硬件ID
hwid = LicenseKeyGenerator.generate_hardware_id()

# 企业许可证
key, info = generator.generate_license(
    license_type=LicenseType.ENTERPRISE,
    product_name="EnterpriseSuite",
    customer_name="Big Corp",
    customer_email="license@bigcorp.com",
    validity_days=365,
    features={"reporting", "api_access", "sso", "audit"},
    hardware_id=hwid,
    max_users=500
)
```

### 验证许可证

```python
# 快速验证
from license_key_utils import quick_validate

status = quick_validate("XXXX-XXXX-XXXX-XXXX-XXXX")
print(f"Status: {status.value}")  # VALID, INVALID_FORMAT, INVALID_SIGNATURE
```

### 完整验证（通过管理器）

```python
from license_key_utils import LicenseManager, LicenseStatus

manager = LicenseManager()

# 创建许可证
key, info = manager.create_license(
    license_type=LicenseType.PROFESSIONAL,
    product_name="MyApp",
    customer_name="Pro User",
    customer_email="pro@example.com",
    validity_days=365,
    features={"basic", "advanced", "api_access"}
)

# 验证许可证
status, validated = manager.validate_license(
    key,
    required_features={"basic", "api_access"}
)

if status == LicenseStatus.VALID:
    print("License is valid!")
else:
    print(f"License invalid: {status.value}")
```

### 许可证管理

```python
manager = LicenseManager()

# 列出所有许可证
all_licenses = manager.list_licenses()

# 按类型筛选
trial_licenses = manager.list_licenses(license_type=LicenseType.TRIAL)

# 按过期状态筛选
expired_licenses = manager.list_licenses(expired=True)
active_licenses = manager.list_licenses(expired=False)

# 撤销许可证
manager.revoke_license(license_id)

# 导出许可证
exported = manager.export_license(license_id)

# 导入许可证
imported = manager.import_license(exported_string)
```

## 许可证类型

| 类型 | 说明 |
|------|------|
| `TRIAL` | 试用许可证，通常有时限 |
| `STANDARD` | 标准许可证，基本功能 |
| `PROFESSIONAL` | 专业许可证，高级功能 |
| `ENTERPRISE` | 企业许可证，完整功能 + 多用户 |

## 验证状态

| 状态 | 说明 |
|------|------|
| `VALID` | 许可证有效 |
| `EXPIRED` | 许可证已过期 |
| `INVALID_SIGNATURE` | 签名验证失败 |
| `INVALID_FORMAT` | 密钥格式错误 |
| `HARDWARE_MISMATCH` | 硬件ID不匹配 |
| `FEATURE_NOT_LICENSED` | 未授权请求的功能 |

## 许可证信息字段

```python
@dataclass
class LicenseInfo:
    license_id: str           # 唯一许可证ID
    license_type: LicenseType  # 许可证类型
    product_name: str          # 产品名称
    customer_name: str         # 客户名称
    customer_email: str        # 客户邮箱
    issued_at: datetime        # 签发时间
    expires_at: Optional[datetime]  # 过期时间（None表示永久）
    features: Set[str]         # 授权功能集
    hardware_id: Optional[str] # 硬件绑定ID
    max_users: int             # 最大用户数
    metadata: Dict[str, str]   # 额外元数据
```

## 安全注意事项

1. **密钥管理**: 在生产环境中，请使用自定义的 `secret_key` 参数
2. **密钥存储**: 许可证管理器默认使用内存存储，生产环境请使用数据库
3. **硬件绑定**: 硬件ID基于系统信息生成，可被篡改，请结合其他安全措施

```python
# 使用自定义密钥
import os
secret = os.environ.get('LICENSE_SECRET').encode()
generator = LicenseKeyGenerator(secret_key=secret)
```

## API 参考

### LicenseKeyGenerator

```python
class LicenseKeyGenerator:
    def __init__(self, secret_key: Optional[bytes] = None)
    
    def generate_key(self, info: LicenseInfo) -> str
    def generate_license(...) -> Tuple[str, LicenseInfo]
    def validate_key(self, key: str, ...) -> Tuple[LicenseStatus, Optional[LicenseInfo]]
    def validate_key_basic(self, key: str) -> LicenseStatus
    
    @staticmethod
    def generate_hardware_id() -> str
```

### LicenseManager

```python
class LicenseManager:
    def __init__(self, secret_key: Optional[bytes] = None)
    
    def create_license(...) -> Tuple[str, LicenseInfo]
    def validate_license(...) -> Tuple[LicenseStatus, Optional[LicenseInfo]]
    def get_license(self, license_id: str) -> Optional[LicenseInfo]
    def revoke_license(self, license_id: str) -> bool
    def list_licenses(...) -> List[LicenseInfo]
    def export_license(self, license_id: str) -> Optional[str]
    def import_license(self, exported: str) -> Optional[LicenseInfo]
```

### 便捷函数

```python
def generate_trial_license(
    product_name: str,
    customer_email: str,
    validity_days: int = 14,
    features: Optional[Set[str]] = None
) -> Tuple[str, LicenseInfo]

def quick_validate(key: str) -> LicenseStatus
```

## 运行测试

```bash
python test_license_key_utils.py
```

## 运行示例

```bash
python examples.py
```

## 许可证

MIT License

## 作者

AllToolkit - 自动化工具生成