# Permission Utils 🔐

Unix 文件权限处理工具，提供完整的权限解析、转换、验证功能。

## 特性

- ✅ **权限模式解析** - 数字模式(755)、符号模式(u+rwx)、chmod风格
- ✅ **权限验证与检查** - 验证文件访问权限
- ✅ **umask 计算** - 计算新文件的默认权限
- ✅ **权限比较** - 分析两个权限模式的差异
- ✅ **权限推荐** - 基于文件类型推荐权限
- ✅ **零依赖** - 仅使用 Python 标准库

## 快速开始

### 解析权限

```python
from permission_utils import parse_mode, format_mode, PermissionInfo

# 解析数字模式
info = parse_mode(0o755)
print(f"所有者: r={'是' if info.owner_read else '否'}")
print(f"组: r={'是' if info.group_read else '否'}")
print(f"其他: r={'是' if info.other_read else '否'}")

# 格式化权限
print(format_mode(0o644))  # 'rw-r--r--'
```

### 验证权限

```python
from permission_utils import check_permission, has_permission

# 检查权限位
has_exec = has_permission(0o755, "owner_execute")
print(has_exec)  # True

# 完整权限检查
info = parse_mode(0o750)
print(info.owner_read)   # True
print(info.group_execute)  # True
print(info.other_read)   # False
```

### umask 计算

```python
from permission_utils import apply_umask, calculate_umask

# 计算文件权限
file_mode = apply_umask(0o666, 0o022)
print(f"{file_mode:o}")  # 644

# 计算 umask
umask = calculate_umask(0o666, 0o644)
print(f"{umask:o}")  # 22
```

## API 参考

### 权限位类

- `PermissionBit` - 权限位标志枚举

### 核心函数

| 函数 | 说明 |
|------|------|
| `parse_mode(mode)` | 解析权限模式为 PermissionInfo |
| `format_mode(mode)` | 格式化权限模式为字符串 |
| `has_permission(mode, permission)` | 检查权限位是否存在 |
| `check_permission(mode, owner, group, other)` | 检查权限 |
| `apply_umask(mode, umask)` | 应用 umask |
| `calculate_umask(desired, result)` | 计算 umask 值 |
