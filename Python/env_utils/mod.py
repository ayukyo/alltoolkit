# -*- coding: utf-8 -*-
"""
AllToolkit - Environment Utilities 🔧

零依赖环境变量与配置管理工具库。
完全使用 Python 标准库实现（os, re, pathlib, json, typing），无需任何外部依赖。

功能特性:
- 环境变量读写与管理
- .env 文件解析与生成
- 配置快照与恢复
- 变量验证与类型转换
- 敏感信息脱敏
- 跨平台支持

Author: AllToolkit Team
License: MIT
Version: 1.0.0
"""

import os
import re
import json
from pathlib import Path
from typing import Dict, Any, Optional, Tuple, Union, List, Callable
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime
from copy import deepcopy


# =============================================================================
# 常量定义
# =============================================================================

DEFAULT_ENV_FILE = '.env'
DEFAULT_ENCODING = 'utf-8'


# =============================================================================
# 枚举与数据类
# =============================================================================

class VarType(Enum):
    """环境变量类型"""
    STRING = 'string'
    INTEGER = 'integer'
    FLOAT = 'float'
    BOOLEAN = 'boolean'
    LIST = 'list'
    JSON = 'json'


class ValidationRule(Enum):
    """验证规则"""
    REQUIRED = 'required'
    NOT_EMPTY = 'not_empty'
    MIN_LENGTH = 'min_length'
    MAX_LENGTH = 'max_length'
    PATTERN = 'pattern'
    CHOICES = 'choices'
    MIN_VALUE = 'min_value'
    MAX_VALUE = 'max_value'


@dataclass
class EnvVar:
    """环境变量定义"""
    name: str
    value: str = ''
    var_type: VarType = VarType.STRING
    required: bool = False
    default: Optional[str] = None
    description: str = ''
    sensitive: bool = False  # 是否为敏感信息（密码、密钥等）
    validators: List[Dict[str, Any]] = field(default_factory=list)
    
    def get_typed_value(self) -> Any:
        """获取类型化后的值"""
        return convert_value(self.value, self.var_type)
    
    def mask_value(self) -> str:
        """获取脱敏后的值"""
        if not self.sensitive:
            return self.value
        if len(self.value) <= 4:
            return '*' * len(self.value)
        return self.value[:2] + '*' * (len(self.value) - 4) + self.value[-2:]


@dataclass
class EnvSnapshot:
    """环境变量快照"""
    timestamp: str
    variables: Dict[str, str]
    source: str = 'system'
    description: str = ''
    
    @property
    def variable_count(self) -> int:
        """变量数量"""
        return len(self.variables)
    
    @classmethod
    def capture(cls, source: str = 'system', description: str = '') -> 'EnvSnapshot':
        """捕获当前环境变量快照"""
        return cls(
            timestamp=datetime.now().isoformat(),
            variables=dict(os.environ),
            source=source,
            description=description
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            'timestamp': self.timestamp,
            'source': self.source,
            'description': self.description,
            'variable_count': self.variable_count,
            'variables': self.variables
        }


@dataclass
class ValidationResult:
    """验证结果"""
    valid: bool
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    
    def __bool__(self) -> bool:
        return self.valid
    
    def add_error(self, message: str):
        self.errors.append(message)
        self.valid = False
    
    def add_warning(self, message: str):
        self.warnings.append(message)


# =============================================================================
# 核心工具函数
# =============================================================================

# -----------------------------------------------------------------------------
# 环境变量读写
# -----------------------------------------------------------------------------

def get_env(name: str, default: Optional[str] = None, required: bool = False) -> Optional[str]:
    """
    获取环境变量值
    
    Args:
        name: 环境变量名
        default: 默认值（当变量不存在时返回）
        required: 是否必需（必需但不存在时抛出异常）
    
    Returns:
        环境变量值或默认值
    
    Raises:
        EnvironmentError: 当 required=True 但变量不存在时
    
    Example:
        >>> get_env('HOME')
        '/home/user'
        >>> get_env('NONEXISTENT', default='fallback')
        'fallback'
        >>> get_env('REQUIRED_VAR', required=True)  # 不存在时抛出异常
    """
    value = os.environ.get(name)
    
    if value is None:
        if required:
            raise EnvironmentError(f"必需的环境变量 '{name}' 未设置")
        return default
    
    return value


def set_env(name: str, value: str) -> bool:
    """
    设置环境变量
    
    Args:
        name: 环境变量名
        value: 环境变量值
    
    Returns:
        是否设置成功
    
    Example:
        >>> set_env('MY_VAR', 'hello')
        True
    """
    try:
        os.environ[name] = value
        return True
    except Exception:
        return False


def delete_env(name: str) -> bool:
    """
    删除环境变量
    
    Args:
        name: 环境变量名
    
    Returns:
        是否删除成功
    
    Example:
        >>> delete_env('MY_VAR')
        True
    """
    try:
        if name in os.environ:
            del os.environ[name]
            return True
        return False
    except Exception:
        return False


def has_env(name: str) -> bool:
    """
    检查环境变量是否存在
    
    Args:
        name: 环境变量名
    
    Returns:
        是否存在
    
    Example:
        >>> has_env('HOME')
        True
    """
    return name in os.environ


def get_all_env() -> Dict[str, str]:
    """
    获取所有环境变量
    
    Returns:
        环境变量字典
    
    Example:
        >>> env = get_all_env()
        >>> 'HOME' in env
        True
    """
    return dict(os.environ)


def clear_env(names: Optional[List[str]] = None) -> int:
    """
    清除环境变量
    
    Args:
        names: 要清除的变量名列表（None 则清除所有）
    
    Returns:
        清除的变量数量
    
    Example:
        >>> set_env('TEMP1', 'value1')
        >>> set_env('TEMP2', 'value2')
        >>> clear_env(['TEMP1', 'TEMP2'])
        2
    """
    count = 0
    if names is None:
        # 清除所有（危险操作，仅用于测试）
        keys = list(os.environ.keys())
        for key in keys:
            del os.environ[key]
            count += 1
    else:
        for name in names:
            if name in os.environ:
                del os.environ[name]
                count += 1
    return count


# -----------------------------------------------------------------------------
# 类型转换
# -----------------------------------------------------------------------------

def convert_value(value: str, var_type: VarType) -> Any:
    """
    将字符串值转换为指定类型
    
    Args:
        value: 字符串值
        var_type: 目标类型
    
    Returns:
        转换后的值
    
    Example:
        >>> convert_value('42', VarType.INTEGER)
        42
        >>> convert_value('true', VarType.BOOLEAN)
        True
        >>> convert_value('[1,2,3]', VarType.LIST)
        ['1', '2', '3']
    """
    if not value:
        return None
    
    if var_type == VarType.STRING:
        return value
    
    elif var_type == VarType.INTEGER:
        try:
            return int(value)
        except ValueError:
            raise ValueError(f"无法将 '{value}' 转换为整数")
    
    elif var_type == VarType.FLOAT:
        try:
            return float(value)
        except ValueError:
            raise ValueError(f"无法将 '{value}' 转换为浮点数")
    
    elif var_type == VarType.BOOLEAN:
        return value.lower() in ('true', '1', 'yes', 'on', 'enabled')
    
    elif var_type == VarType.LIST:
        # 支持逗号或分号分隔
        if value.startswith('[') and value.endswith(']'):
            value = value[1:-1]
        return [item.strip() for item in re.split(r'[;,]', value) if item.strip()]
    
    elif var_type == VarType.JSON:
        try:
            return json.loads(value)
        except json.JSONDecodeError as e:
            raise ValueError(f"无法解析 JSON: {e}")
    
    return value


def get_env_as(name: str, var_type: VarType, default: Any = None) -> Any:
    """
    获取环境变量并转换为指定类型
    
    Args:
        name: 环境变量名
        var_type: 目标类型
        default: 默认值
    
    Returns:
        类型化后的值
    
    Example:
        >>> os.environ['PORT'] = '8080'
        >>> get_env_as('PORT', VarType.INTEGER)
        8080
        >>> os.environ['DEBUG'] = 'true'
        >>> get_env_as('DEBUG', VarType.BOOLEAN)
        True
    """
    value = os.environ.get(name)
    if value is None:
        return default
    try:
        return convert_value(value, var_type)
    except (ValueError, json.JSONDecodeError):
        return default


# -----------------------------------------------------------------------------
# .env 文件操作
# -----------------------------------------------------------------------------

def parse_env_file(filepath: Union[str, Path], encoding: str = DEFAULT_ENCODING) -> Dict[str, str]:
    """
    解析 .env 文件
    
    Args:
        filepath: .env 文件路径
        encoding: 文件编码
    
    Returns:
        环境变量字典
    
    Example:
        # .env 文件内容:
        # DATABASE_URL=postgres://localhost/mydb
        # DEBUG=true
        >>> parse_env_file('.env')
        {'DATABASE_URL': 'postgres://localhost/mydb', 'DEBUG': 'true'}
    """
    filepath = Path(filepath)
    if not filepath.exists():
        raise FileNotFoundError(f".env 文件不存在：{filepath}")
    
    env_vars = {}
    
    with open(filepath, 'r', encoding=encoding) as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            
            # 跳过空行和注释
            if not line or line.startswith('#'):
                continue
            
            # 解析 KEY=VALUE
            match = re.match(r'^([A-Za-z_][A-Za-z0-9_]*)\s*=\s*(.*)$', line)
            if match:
                key, value = match.groups()
                # 移除引号
                value = value.strip()
                if (value.startswith('"') and value.endswith('"')) or \
                   (value.startswith("'") and value.endswith("'")):
                    value = value[1:-1]
                env_vars[key] = value
    
    return env_vars


def load_env_file(filepath: Union[str, Path], encoding: str = DEFAULT_ENCODING, override: bool = False) -> Dict[str, str]:
    """
    加载 .env 文件到环境变量
    
    Args:
        filepath: .env 文件路径
        encoding: 文件编码
        override: 是否覆盖已存在的环境变量
    
    Returns:
        加载的变量字典
    
    Example:
        >>> load_env_file('.env')
        {'DATABASE_URL': 'postgres://localhost/mydb'}
    """
    env_vars = parse_env_file(filepath, encoding)
    
    for key, value in env_vars.items():
        if override or key not in os.environ:
            os.environ[key] = value
    
    return env_vars


def save_env_file(filepath: Union[str, Path], variables: Optional[Dict[str, str]] = None, 
                  encoding: str = DEFAULT_ENCODING, include_system: bool = False) -> int:
    """
    保存环境变量到 .env 文件
    
    Args:
        filepath: 输出文件路径
        variables: 要保存的变量（None 则使用当前环境变量）
        encoding: 文件编码
        include_system: 是否包含所有系统环境变量
    
    Returns:
        保存的变量数量
    
    Example:
        >>> save_env_file('.env', {'DATABASE_URL': 'postgres://localhost/mydb'})
        1
    """
    filepath = Path(filepath)
    
    if variables is None:
        variables = dict(os.environ) if include_system else {}
    
    with open(filepath, 'w', encoding=encoding) as f:
        f.write(f"# Generated by AllToolkit env_utils\n")
        f.write(f"# {datetime.now().isoformat()}\n\n")
        
        for key, value in sorted(variables.items()):
            # 转义特殊字符
            if any(c in value for c in ' \t\n\r"\'\\'):
                value = '"' + value.replace('\\', '\\\\').replace('"', '\\"') + '"'
            f.write(f"{key}={value}\n")
    
    return len(variables)


def merge_env_files(filepaths: List[Union[str, Path]], output: Optional[Union[str, Path]] = None) -> Dict[str, str]:
    """
    合并多个 .env 文件
    
    Args:
        filepaths: 输入文件路径列表
        output: 输出文件路径（可选）
    
    Returns:
        合并后的变量字典（后者覆盖前者）
    
    Example:
        >>> merge_env_files(['.env.base', '.env.local'], output='.env.merged')
        {'DATABASE_URL': 'postgres://localhost/mydb', 'DEBUG': 'true'}
    """
    merged = {}
    
    for filepath in filepaths:
        env_vars = parse_env_file(filepath)
        merged.update(env_vars)
    
    if output:
        save_env_file(output, merged)
    
    return merged


# -----------------------------------------------------------------------------
# 验证
# -----------------------------------------------------------------------------

def validate_env(name: str, rules: List[Dict[str, Any]]) -> ValidationResult:
    """
    验证环境变量
    
    Args:
        name: 环境变量名
        rules: 验证规则列表
    
    Returns:
        验证结果
    
    Example:
        >>> os.environ['PORT'] = '8080'
        >>> result = validate_env('PORT', [
        ...     {'rule': 'required'},
        ...     {'rule': 'min_value', 'value': 1024},
        ...     {'rule': 'max_value', 'value': 65535}
        ... ])
        >>> result.valid
        True
    """
    result = ValidationResult(valid=True)
    value = os.environ.get(name)
    
    for rule_def in rules:
        rule = rule_def.get('rule')
        
        if rule == ValidationRule.REQUIRED.value:
            if value is None:
                result.add_error(f"'{name}' 是必需的环境变量")
        
        elif rule == ValidationRule.NOT_EMPTY.value:
            if value is not None and not value.strip():
                result.add_error(f"'{name}' 不能为空")
        
        elif rule == ValidationRule.MIN_LENGTH.value:
            min_len = rule_def.get('value', 0)
            if value and len(value) < min_len:
                result.add_error(f"'{name}' 长度不能少于 {min_len} 个字符")
        
        elif rule == ValidationRule.MAX_LENGTH.value:
            max_len = rule_def.get('value', float('inf'))
            if value and len(value) > max_len:
                result.add_error(f"'{name}' 长度不能超过 {max_len} 个字符")
        
        elif rule == ValidationRule.PATTERN.value:
            pattern = rule_def.get('value', '')
            if value and not re.match(pattern, value):
                result.add_error(f"'{name}' 格式不符合要求")
        
        elif rule == ValidationRule.CHOICES.value:
            choices = rule_def.get('value', [])
            if value and value not in choices:
                result.add_error(f"'{name}' 必须是以下值之一：{', '.join(choices)}")
        
        elif rule == ValidationRule.MIN_VALUE.value:
            min_val = rule_def.get('value', float('-inf'))
            try:
                if value and float(value) < min_val:
                    result.add_error(f"'{name}' 不能小于 {min_val}")
            except ValueError:
                result.add_error(f"'{name}' 不是有效的数字")
        
        elif rule == ValidationRule.MAX_VALUE.value:
            max_val = rule_def.get('value', float('inf'))
            try:
                if value and float(value) > max_val:
                    result.add_error(f"'{name}' 不能大于 {max_val}")
            except ValueError:
                result.add_error(f"'{name}' 不是有效的数字")
    
    return result


def validate_env_schema(schema: Dict[str, Dict[str, Any]]) -> ValidationResult:
    """
    根据 schema 验证多个环境变量
    
    Args:
        schema: 验证 schema，格式为 {var_name: {rules: [...]}}
    
    Returns:
        验证结果
    
    Example:
        >>> schema = {
        ...     'DATABASE_URL': {'rules': [{'rule': 'required'}]},
        ...     'PORT': {'rules': [
        ...         {'rule': 'required'},
        ...         {'rule': 'min_value', 'value': 1024},
        ...         {'rule': 'max_value', 'value': 65535}
        ...     ]}
        ... }
        >>> result = validate_env_schema(schema)
    """
    result = ValidationResult(valid=True)
    
    for name, spec in schema.items():
        rules = spec.get('rules', [])
        var_result = validate_env(name, rules)
        
        result.errors.extend(var_result.errors)
        result.warnings.extend(var_result.warnings)
        if not var_result.valid:
            result.valid = False
    
    return result


# -----------------------------------------------------------------------------
# 快照与恢复
# -----------------------------------------------------------------------------

def capture_snapshot(description: str = '') -> EnvSnapshot:
    """
    捕获当前环境变量快照
    
    Args:
        description: 快照描述
    
    Returns:
        环境变量快照
    
    Example:
        >>> snapshot = capture_snapshot('Before deployment')
        >>> snapshot.variable_count > 0
        True
    """
    return EnvSnapshot.capture(description=description)


def restore_snapshot(snapshot: EnvSnapshot, clear_first: bool = False) -> int:
    """
    从快照恢复环境变量
    
    Args:
        snapshot: 环境变量快照
        clear_first: 是否先清除当前环境变量
    
    Returns:
        恢复的变量数量
    
    Example:
        >>> snapshot = capture_snapshot()
        >>> set_env('NEW_VAR', 'value')
        >>> restore_snapshot(snapshot, clear_first=True)
        42
    """
    if clear_first:
        clear_env()
    
    count = 0
    for key, value in snapshot.variables.items():
        os.environ[key] = value
        count += 1
    
    return count


def save_snapshot(snapshot: EnvSnapshot, filepath: Union[str, Path]) -> bool:
    """
    保存快照到文件
    
    Args:
        snapshot: 环境变量快照
        filepath: 输出文件路径
    
    Returns:
        是否保存成功
    
    Example:
        >>> snapshot = capture_snapshot('Backup')
        >>> save_snapshot(snapshot, 'snapshot.json')
        True
    """
    try:
        filepath = Path(filepath)
        with open(filepath, 'w', encoding=DEFAULT_ENCODING) as f:
            json.dump(snapshot.to_dict(), f, indent=2)
        return True
    except Exception:
        return False


def load_snapshot(filepath: Union[str, Path]) -> Optional[EnvSnapshot]:
    """
    从文件加载快照
    
    Args:
        filepath: 快照文件路径
    
    Returns:
        环境变量快照或 None
    
    Example:
        >>> snapshot = load_snapshot('snapshot.json')
        >>> snapshot is not None
        True
    """
    try:
        filepath = Path(filepath)
        with open(filepath, 'r', encoding=DEFAULT_ENCODING) as f:
            data = json.load(f)
        
        return EnvSnapshot(
            timestamp=data['timestamp'],
            variables=data['variables'],
            source=data.get('source', 'file'),
            description=data.get('description', '')
        )
    except Exception:
        return None


def diff_snapshots(before: EnvSnapshot, after: EnvSnapshot) -> Dict[str, Any]:
    """
    比较两个快照的差异
    
    Args:
        before: 之前的快照
        after: 之后的快照
    
    Returns:
        差异字典，包含 added, removed, changed
    
    Example:
        >>> before = capture_snapshot()
        >>> set_env('NEW_VAR', 'value')
        >>> after = capture_snapshot()
        >>> diff = diff_snapshots(before, after)
        >>> 'NEW_VAR' in diff['added']
        True
    """
    before_vars = set(before.variables.keys())
    after_vars = set(after.variables.keys())
    
    added = after_vars - before_vars
    removed = before_vars - after_vars
    common = before_vars & after_vars
    
    changed = {}
    for key in common:
        if before.variables[key] != after.variables[key]:
            changed[key] = {
                'old': before.variables[key],
                'new': after.variables[key]
            }
    
    return {
        'added': list(added),
        'removed': list(removed),
        'changed': changed,
        'summary': {
            'added_count': len(added),
            'removed_count': len(removed),
            'changed_count': len(changed)
        }
    }


# -----------------------------------------------------------------------------
# 敏感信息处理
# -----------------------------------------------------------------------------

def mask_sensitive_vars(variables: Dict[str, str], 
                        sensitive_patterns: Optional[List[str]] = None) -> Dict[str, str]:
    """
    脱敏敏感环境变量
    
    Args:
        variables: 环境变量字典
        sensitive_patterns: 敏感变量名模式列表（默认包含常见敏感变量）
    
    Returns:
        脱敏后的字典
    
    Example:
        >>> vars = {'DATABASE_PASSWORD': 'secret123', 'APP_NAME': 'MyApp'}
        >>> masked = mask_sensitive_vars(vars)
        >>> masked['DATABASE_PASSWORD']
        'se******23'
    """
    if sensitive_patterns is None:
        sensitive_patterns = [
            'PASSWORD', 'PASSWD', 'PWD', 'SECRET', 'TOKEN', 'KEY', 'API_KEY',
            'APIKEY', 'AUTH', 'CREDENTIAL', 'PRIVATE', 'ACCESS_KEY', 'SECRET_KEY'
        ]
    
    masked = {}
    for key, value in variables.items():
        is_sensitive = any(pattern in key.upper() for pattern in sensitive_patterns)
        
        if is_sensitive:
            if len(value) <= 4:
                masked[key] = '*' * len(value)
            else:
                masked[key] = value[:2] + '*' * (len(value) - 4) + value[-2:]
        else:
            masked[key] = value
    
    return masked


def get_safe_env_dump(sensitive_patterns: Optional[List[str]] = None) -> str:
    """
    获取安全的环境变量转储（敏感信息已脱敏）
    
    Args:
        sensitive_patterns: 敏感变量名模式列表
    
    Returns:
        格式化的环境变量字符串
    
    Example:
        >>> dump = get_safe_env_dump()
        >>> 'PASSWORD' in dump  # 可能包含脱敏后的密码
        True
    """
    masked = mask_sensitive_vars(dict(os.environ), sensitive_patterns)
    lines = [f"{key}={value}" for key, value in sorted(masked.items())]
    return '\n'.join(lines)


# -----------------------------------------------------------------------------
# 工具函数
# -----------------------------------------------------------------------------

def expand_env_vars(text: str, default: str = '') -> str:
    """
    展开文本中的环境变量引用
    
    Args:
        text: 包含 ${VAR} 或 $VAR 引用的文本
        default: 变量不存在时的默认值
    
    Returns:
        展开后的文本
    
    Example:
        >>> os.environ['HOME'] = '/home/user'
        >>> expand_env_vars('Path: $HOME/documents')
        'Path: /home/user/documents'
        >>> expand_env_vars('Value: ${NONEXISTENT:-default}')
        'Value: default'
    """
    def replace(match):
        var_expr = match.group(1)
        
        # 处理 ${VAR:-default} 语法
        if ':-' in var_expr:
            var_name, default_val = var_expr.split(':-', 1)
            return os.environ.get(var_name, default_val)
        
        # 处理 ${VAR-default} 语法
        if '-' in var_expr and ':' not in var_expr:
            var_name, default_val = var_expr.split('-', 1)
            return os.environ.get(var_name, default_val)
        
        # 简单变量引用
        return os.environ.get(var_expr, default)
    
    # 匹配 ${VAR} 或 $VAR
    text = re.sub(r'\$\{([^}]+)\}', replace, text)
    text = re.sub(r'\$([A-Za-z_][A-Za-z0-9_]*)', replace, text)
    
    return text


def interpolate_env_vars(config: Any) -> Any:
    """
    递归插值配置中的环境变量
    
    Args:
        config: 配置对象（字典、列表或字符串）
    
    Returns:
        插值后的配置
    
    Example:
        >>> os.environ['DB_HOST'] = 'localhost'
        >>> config = {'database': {'host': '${DB_HOST}', 'port': 5432}}
        >>> interpolate_env_vars(config)
        {'database': {'host': 'localhost', 'port': 5432}}
    """
    if isinstance(config, str):
        return expand_env_vars(config)
    elif isinstance(config, dict):
        return {k: interpolate_env_vars(v) for k, v in config.items()}
    elif isinstance(config, list):
        return [interpolate_env_vars(item) for item in config]
    else:
        return config


def get_env_tree(prefix: str = '') -> Dict[str, Any]:
    """
    获取环境变量的树状结构（基于下划线分隔）
    
    Args:
        prefix: 变量名前缀过滤
    
    Returns:
        树状结构字典
    
    Example:
        >>> os.environ['DATABASE_HOST'] = 'localhost'
        >>> os.environ['DATABASE_PORT'] = '5432'
        >>> tree = get_env_tree('DATABASE')
        >>> 'HOST' in tree
        True
    """
    tree = {}
    
    for key, value in os.environ.items():
        if prefix and not key.startswith(prefix):
            continue
        
        parts = key[len(prefix):].lstrip('_').split('_')
        
        current = tree
        for i, part in enumerate(parts[:-1]):
            if part not in current:
                current[part] = {}
            current = current[part]
        
        if parts:
            current[parts[-1]] = value
    
    return tree


# -----------------------------------------------------------------------------
# 便捷函数
# -----------------------------------------------------------------------------

def is_production() -> bool:
    """检查是否为生产环境"""
    env = get_env('ENV', get_env('NODE_ENV', get_env('APP_ENV', '')))
    return env.lower() in ('production', 'prod')


def is_development() -> bool:
    """检查是否为开发环境"""
    env = get_env('ENV', get_env('NODE_ENV', get_env('APP_ENV', '')))
    return env.lower() in ('development', 'dev', 'development')


def is_testing() -> bool:
    """检查是否为测试环境"""
    env = get_env('ENV', get_env('NODE_ENV', get_env('APP_ENV', '')))
    return env.lower() in ('test', 'testing')


def get_app_info() -> Dict[str, str]:
    """获取应用环境信息"""
    return {
        'environment': get_env('ENV', get_env('NODE_ENV', 'unknown')),
        'app_name': get_env('APP_NAME', 'unknown'),
        'app_version': get_env('APP_VERSION', 'unknown'),
        'app_port': get_env('PORT', get_env('APP_PORT', '3000')),
        'debug': get_env('DEBUG', 'false')
    }


def require_envs(*names: str) -> Dict[str, str]:
    """
    要求多个环境变量存在并返回它们的值
    
    Args:
        names: 环境变量名列表
    
    Returns:
        环境变量字典
    
    Raises:
        EnvironmentError: 当任何变量不存在时
    
    Example:
        >>> require_envs('DATABASE_URL', 'API_KEY')
        {'DATABASE_URL': 'postgres://...', 'API_KEY': '...'}
    """
    result = {}
    missing = []
    
    for name in names:
        value = os.environ.get(name)
        if value is None:
            missing.append(name)
        else:
            result[name] = value
    
    if missing:
        raise EnvironmentError(f"缺少必需的环境变量：{', '.join(missing)}")
    
    return result


# =============================================================================
# 命令行接口
# =============================================================================

def cli_main():
    """命令行入口"""
    import sys
    
    if len(sys.argv) < 2:
        print("AllToolkit env_utils - 环境变量管理工具")
        print("\n用法:")
        print("  env_utils get <NAME>           获取环境变量")
        print("  env_utils set <NAME> <VALUE>   设置环境变量")
        print("  env_utils list [PATTERN]       列出环境变量")
        print("  env_utils load <FILE>          加载 .env 文件")
        print("  env_utils save <FILE>          保存环境变量")
        print("  env_utils validate <SCHEMA>    验证环境变量")
        print("  env_utils snapshot             捕获快照")
        print("  env_utils mask                 脱敏输出")
        sys.exit(0)
    
    command = sys.argv[1]
    
    if command == 'get':
        if len(sys.argv) < 3:
            print("错误：请指定变量名")
            sys.exit(1)
        name = sys.argv[2]
        value = os.environ.get(name)
        if value:
            print(value)
        else:
            print(f"变量 '{name}' 未设置")
            sys.exit(1)
    
    elif command == 'set':
        if len(sys.argv) < 4:
            print("错误：请指定变量名和值")
            sys.exit(1)
        name, value = sys.argv[2], sys.argv[3]
        set_env(name, value)
        print(f"已设置 {name}={value}")
    
    elif command == 'list':
        pattern = sys.argv[2] if len(sys.argv) > 2 else None
        for key, value in sorted(os.environ.items()):
            if pattern is None or pattern in key:
                print(f"{key}={value}")
    
    elif command == 'load':
        if len(sys.argv) < 3:
            print("错误：请指定 .env 文件路径")
            sys.exit(1)
        filepath = sys.argv[2]
        try:
            vars = load_env_file(filepath, override=True)
            print(f"已加载 {len(vars)} 个变量")
        except FileNotFoundError as e:
            print(f"错误：{e}")
            sys.exit(1)
    
    elif command == 'save':
        if len(sys.argv) < 3:
            print("错误：请指定输出文件路径")
            sys.exit(1)
        filepath = sys.argv[2]
        count = save_env_file(filepath)
        print(f"已保存 {count} 个变量到 {filepath}")
    
    elif command == 'mask':
        masked = mask_sensitive_vars(dict(os.environ))
        for key, value in sorted(masked.items()):
            print(f"{key}={value}")
    
    elif command == 'snapshot':
        snapshot = capture_snapshot()
        print(f"快照捕获于 {snapshot.timestamp}")
        print(f"变量数量：{snapshot.variable_count}")
    
    else:
        print(f"未知命令：{command}")
        sys.exit(1)


if __name__ == '__main__':
    cli_main()
