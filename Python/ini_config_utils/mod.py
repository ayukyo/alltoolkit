#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AllToolkit - INI Config Utilities
INI配置文件解析工具模块

功能特性:
- 完整的INI文件读写支持
- 节(section)和键值对(key-value)操作
- 注释保留和智能处理
- 类型自动转换(int, float, bool)
- 默认值支持
- 配置文件验证

作者: AllToolkit
许可证: MIT
"""

import re
import os
from typing import Dict, List, Optional, Union, Any, Tuple
from io import StringIO


class IniConfigError(Exception):
    """INI配置相关异常基类"""
    pass


class SectionNotFoundError(IniConfigError):
    """节不存在异常"""
    pass


class KeyNotFoundError(IniConfigError):
    """键不存在异常"""
    pass


class ParseError(IniConfigError):
    """解析错误异常"""
    pass


class IniSection:
    """
    INI配置文件节(section)类
    
    表示INI文件中的一个节，包含该节下的所有键值对。
    支持字典式访问和属性式访问。
    
    Attributes:
        name: 节名称
        _data: 存储键值对的字典
        _comments: 存储键的注释
    """
    
    def __init__(self, name: str):
        """
        初始化节对象
        
        Args:
            name: 节名称
        """
        self.name = name
        self._data: Dict[str, str] = {}
        self._comments: Dict[str, Optional[str]] = {}
    
    def get(self, key: str, default: Any = None, 
            type_func: Optional[type] = None) -> Any:
        """
        获取键值，支持类型转换和默认值
        
        Args:
            key: 键名
            default: 默认值，键不存在时返回
            type_func: 类型转换函数(int, float, bool等)
        
        Returns:
            键值或默认值
        
        Example:
            >>> section.get('port', 8080, int)
            8080
            >>> section.get('debug', False, bool)
            True
        """
        if key not in self._data:
            return default
        
        value = self._data[key]
        if type_func is None:
            return value
        
        try:
            if type_func == bool:
                return self._str_to_bool(value)
            else:
                return type_func(value)
        except (ValueError, TypeError):
            return default
    
    def get_int(self, key: str, default: int = 0) -> int:
        """获取整数值"""
        return self.get(key, default, int)
    
    def get_float(self, key: str, default: float = 0.0) -> float:
        """获取浮点数值"""
        return self.get(key, default, float)
    
    def get_bool(self, key: str, default: bool = False) -> bool:
        """获取布尔值"""
        return self.get(key, default, bool)
    
    def get_list(self, key: str, default: Optional[List[str]] = None, 
                 separator: str = ',') -> List[str]:
        """
        获取列表值
        
        Args:
            key: 键名
            default: 默认值
            separator: 分隔符，默认为逗号
        
        Returns:
            字符串列表
        """
        if key not in self._data:
            return default if default is not None else []
        
        value = self._data[key]
        if not value.strip():
            return []
        
        return [item.strip() for item in value.split(separator)]
    
    def set(self, key: str, value: Any, comment: Optional[str] = None) -> None:
        """
        设置键值
        
        Args:
            key: 键名
            value: 值，可以是str, int, float, bool, list等
            comment: 该键的注释
        """
        if isinstance(value, bool):
            str_value = 'true' if value else 'false'
        elif isinstance(value, (list, tuple)):
            str_value = ', '.join(str(item) for item in value)
        else:
            str_value = str(value)
        
        self._data[key] = str_value
        if comment is not None:
            self._comments[key] = comment
    
    def has(self, key: str) -> bool:
        """检查键是否存在"""
        return key in self._data
    
    def remove(self, key: str) -> bool:
        """
        删除键
        
        Args:
            key: 键名
        
        Returns:
            是否成功删除
        """
        if key in self._data:
            del self._data[key]
            self._comments.pop(key, None)
            return True
        return False
    
    def keys(self) -> List[str]:
        """获取所有键名"""
        return list(self._data.keys())
    
    def items(self) -> List[Tuple[str, str]]:
        """获取所有键值对"""
        return list(self._data.items())
    
    def clear(self) -> None:
        """清空节内所有数据"""
        self._data.clear()
        self._comments.clear()
    
    def copy(self) -> 'IniSection':
        """创建节的深拷贝"""
        new_section = IniSection(self.name)
        new_section._data = self._data.copy()
        new_section._comments = self._comments.copy()
        return new_section
    
    @staticmethod
    def _str_to_bool(value: str) -> bool:
        """字符串转布尔值"""
        return value.lower() in ('true', 'yes', '1', 'on', 'enabled')
    
    def __getitem__(self, key: str) -> str:
        """字典式访问: section['key']"""
        if key not in self._data:
            raise KeyNotFoundError(f"Key '{key}' not found in section '{self.name}'")
        return self._data[key]
    
    def __setitem__(self, key: str, value: Any) -> None:
        """字典式设置: section['key'] = value"""
        self.set(key, value)
    
    def __contains__(self, key: str) -> bool:
        """in操作符: 'key' in section"""
        return key in self._data
    
    def __len__(self) -> int:
        """获取键值对数量"""
        return len(self._data)
    
    def __repr__(self) -> str:
        return f"IniSection('{self.name}', {len(self._data)} keys)"


class IniConfig:
    """
    INI配置文件管理类
    
    提供完整的INI文件解析、修改和生成功能。
    支持多节配置、注释保留、类型转换等特性。
    
    Attributes:
        _sections: 存储所有节的字典
        _section_comments: 存储节的注释
        _global_comments: 全局注释(文件开头)
    
    Example:
        >>> config = IniConfig()
        >>> config.read_file('config.ini')
        >>> db_section = config.section('database')
        >>> host = db_section.get('host', 'localhost')
        >>> port = db_section.get_int('port', 3306)
        >>> config.set('database', 'timeout', 30)
        >>> config.write_file('config.ini')
    """
    
    def __init__(self):
        """初始化空的配置对象"""
        self._sections: Dict[str, IniSection] = {}
        self._section_comments: Dict[str, Optional[str]] = {}
        self._global_comments: List[str] = []
    
    def section(self, name: str, create: bool = False) -> IniSection:
        """
        获取或创建节
        
        Args:
            name: 节名称
            create: 不存在时是否创建
        
        Returns:
            IniSection对象
        
        Raises:
            SectionNotFoundError: 节不存在且create=False时
        """
        if name not in self._sections:
            if create:
                self._sections[name] = IniSection(name)
            else:
                raise SectionNotFoundError(f"Section '{name}' not found")
        return self._sections[name]
    
    def has_section(self, name: str) -> bool:
        """检查节是否存在"""
        return name in self._sections
    
    def add_section(self, name: str, comment: Optional[str] = None) -> IniSection:
        """
        添加新节
        
        Args:
            name: 节名称
            comment: 节注释
        
        Returns:
            新创建的节对象
        """
        if name in self._sections:
            raise IniConfigError(f"Section '{name}' already exists")
        
        section = IniSection(name)
        self._sections[name] = section
        if comment is not None:
            self._section_comments[name] = comment
        return section
    
    def remove_section(self, name: str) -> bool:
        """
        删除节
        
        Args:
            name: 节名称
        
        Returns:
            是否成功删除
        """
        if name in self._sections:
            del self._sections[name]
            self._section_comments.pop(name, None)
            return True
        return False
    
    def sections(self) -> List[str]:
        """获取所有节名称"""
        return list(self._sections.keys())
    
    def get(self, section: str, key: str, default: Any = None,
            type_func: Optional[type] = None) -> Any:
        """
        获取配置值(便捷方法)
        
        Args:
            section: 节名称
            key: 键名
            default: 默认值
            type_func: 类型转换函数
        
        Returns:
            配置值或默认值
        """
        try:
            sec = self.section(section)
            return sec.get(key, default, type_func)
        except SectionNotFoundError:
            return default
    
    def get_int(self, section: str, key: str, default: int = 0) -> int:
        """获取整数值(便捷方法)"""
        return self.get(section, key, default, int)
    
    def get_float(self, section: str, key: str, default: float = 0.0) -> float:
        """获取浮点数值(便捷方法)"""
        return self.get(section, key, default, float)
    
    def get_bool(self, section: str, key: str, default: bool = False) -> bool:
        """获取布尔值(便捷方法)"""
        return self.get(section, key, default, bool)
    
    def get_list(self, section: str, key: str, 
                 default: Optional[List[str]] = None,
                 separator: str = ',') -> List[str]:
        """获取列表值(便捷方法)"""
        try:
            sec = self.section(section)
            return sec.get_list(key, default, separator)
        except SectionNotFoundError:
            return default if default is not None else []
    
    def set(self, section: str, key: str, value: Any,
            comment: Optional[str] = None) -> None:
        """
        设置配置值(便捷方法)
        
        Args:
            section: 节名称
            key: 键名
            value: 值
            comment: 注释
        """
        sec = self.section(section, create=True)
        sec.set(key, value, comment)
    
    def has(self, section: str, key: Optional[str] = None) -> bool:
        """
        检查配置是否存在
        
        Args:
            section: 节名称
            key: 键名，为None时只检查节
        
        Returns:
            是否存在
        """
        if section not in self._sections:
            return False
        if key is None:
            return True
        return self._sections[section].has(key)
    
    def remove(self, section: str, key: Optional[str] = None) -> bool:
        """
        删除配置
        
        Args:
            section: 节名称
            key: 键名，为None时删除整个节
        
        Returns:
            是否成功删除
        """
        if key is None:
            return self.remove_section(section)
        
        if section in self._sections:
            return self._sections[section].remove(key)
        return False
    
    def read_file(self, filepath: str, encoding: str = 'utf-8') -> None:
        """
        从文件读取配置
        
        Args:
            filepath: 文件路径
            encoding: 文件编码
        
        Raises:
            FileNotFoundError: 文件不存在
            ParseError: 解析错误
        """
        with open(filepath, 'r', encoding=encoding) as f:
            content = f.read()
        self.read_string(content)
    
    def read_string(self, content: str) -> None:
        """
        从字符串读取配置
        
        Args:
            content: INI格式字符串
        
        Raises:
            ParseError: 解析错误
        """
        self._sections.clear()
        self._section_comments.clear()
        self._global_comments.clear()
        
        current_section: Optional[IniSection] = None
        pending_comment: Optional[str] = None
        
        for line_num, line in enumerate(content.split('\n'), 1):
            line = line.rstrip()
            
            # 空行 - 不重置pending_comment，保留给下一个键或节
            if not line.strip():
                continue
            
            # 注释行
            if line.strip().startswith(('#', ';')):
                comment = line.strip()[1:].strip()
                if current_section is None:
                    self._global_comments.append(comment)
                else:
                    pending_comment = comment
                continue
            
            # 节定义 [section]
            section_match = re.match(r'^\s*\[([^\]]+)\]\s*$', line)
            if section_match:
                section_name = section_match.group(1).strip()
                current_section = IniSection(section_name)
                self._sections[section_name] = current_section
                if pending_comment:
                    self._section_comments[section_name] = pending_comment
                    pending_comment = None
                continue
            
            # 键值对 key = value
            kv_match = re.match(r'^\s*([^=]+?)\s*=\s*(.*)$', line)
            if kv_match:
                key = kv_match.group(1).strip()
                value = kv_match.group(2).strip()
                
                # 去除值两端的引号
                if (value.startswith('"') and value.endswith('"')) or \
                   (value.startswith("'") and value.endswith("'")):
                    value = value[1:-1]
                
                if current_section is None:
                    raise ParseError(f"Line {line_num}: Key '{key}' outside of section")
                
                current_section.set(key, value, pending_comment)
                pending_comment = None
                continue
            
            # 无法解析的行
            raise ParseError(f"Line {line_num}: Cannot parse '{line}'")
    
    def write_file(self, filepath: str, encoding: str = 'utf-8') -> None:
        """
        写入配置文件
        
        Args:
            filepath: 文件路径
            encoding: 文件编码
        """
        content = self.write_string()
        
        # 确保目录存在
        dir_path = os.path.dirname(filepath)
        if dir_path and not os.path.exists(dir_path):
            os.makedirs(dir_path, exist_ok=True)
        
        with open(filepath, 'w', encoding=encoding) as f:
            f.write(content)
    
    def write_string(self) -> str:
        """
        生成配置字符串
        
        Returns:
            INI格式字符串
        """
        lines: List[str] = []
        
        # 全局注释
        for comment in self._global_comments:
            lines.append(f"# {comment}")
        
        if self._global_comments:
            lines.append("")
        
        # 各节
        first_section = True
        for section_name, section in self._sections.items():
            if not first_section:
                lines.append("")
            first_section = False
            
            # 节注释
            if section_name in self._section_comments:
                lines.append(f"# {self._section_comments[section_name]}")
            
            lines.append(f"[{section_name}]")
            
            # 键值对
            for key, value in section.items():
                # 键注释
                if key in section._comments:
                    lines.append(f"# {section._comments[key]}")
                
                # 需要引号的值
                if any(c in value for c in ('=', '#', ';', ' ', '\t', '\n')):
                    value = f'"{value}"'
                lines.append(f"{key} = {value}")
        
        return '\n'.join(lines)
    
    def to_dict(self) -> Dict[str, Dict[str, str]]:
        """
        转换为字典
        
        Returns:
            嵌套字典 {section: {key: value}}
        """
        return {
            name: dict(section.items())
            for name, section in self._sections.items()
        }
    
    def from_dict(self, data: Dict[str, Dict[str, Any]]) -> None:
        """
        从字典加载
        
        Args:
            data: 嵌套字典 {section: {key: value}}
        """
        self._sections.clear()
        self._section_comments.clear()
        
        for section_name, items in data.items():
            section = self.add_section(section_name)
            for key, value in items.items():
                section.set(key, value)
    
    def copy(self) -> 'IniConfig':
        """创建配置的深拷贝"""
        new_config = IniConfig()
        new_config._global_comments = self._global_comments.copy()
        new_config._section_comments = self._section_comments.copy()
        for name, section in self._sections.items():
            new_config._sections[name] = section.copy()
        return new_config
    
    def clear(self) -> None:
        """清空所有配置"""
        self._sections.clear()
        self._section_comments.clear()
        self._global_comments.clear()
    
    def merge(self, other: 'IniConfig', overwrite: bool = True) -> None:
        """
        合并另一个配置
        
        Args:
            other: 要合并的配置
            overwrite: 是否覆盖已有值
        """
        for section_name, section in other._sections.items():
            if section_name not in self._sections:
                self._sections[section_name] = section.copy()
            else:
                for key, value in section.items():
                    if overwrite or not self._sections[section_name].has(key):
                        self._sections[section_name].set(key, value)
    
    def validate(self, schema: Dict[str, List[str]]) -> List[str]:
        """
        验证配置结构
        
        Args:
            schema: 期望的结构 {section: [key1, key2, ...]}
        
        Returns:
            错误信息列表
        """
        errors: List[str] = []
        
        for section_name, required_keys in schema.items():
            if not self.has_section(section_name):
                errors.append(f"Missing required section: '{section_name}'")
                continue
            
            section = self.section(section_name)
            for key in required_keys:
                if not section.has(key):
                    errors.append(f"Missing required key '{key}' in section '{section_name}'")
        
        return errors
    
    def __contains__(self, section: str) -> bool:
        """in操作符: 'section' in config"""
        return section in self._sections
    
    def __getitem__(self, section: str) -> IniSection:
        """字典式访问: config['section']"""
        return self.section(section)
    
    def __setitem__(self, section: str, value: Union[IniSection, Dict[str, Any]]) -> None:
        """字典式设置: config['section'] = {...}"""
        if isinstance(value, IniSection):
            self._sections[section] = value
        else:
            sec = IniSection(section)
            for k, v in value.items():
                sec.set(k, v)
            self._sections[section] = sec
    
    def __repr__(self) -> str:
        return f"IniConfig({len(self._sections)} sections)"


# 便捷函数

def read_ini(filepath: str, encoding: str = 'utf-8') -> IniConfig:
    """
    读取INI文件
    
    Args:
        filepath: 文件路径
        encoding: 文件编码
    
    Returns:
        IniConfig对象
    
    Example:
        >>> config = read_ini('config.ini')
        >>> print(config.get('database', 'host'))
    """
    config = IniConfig()
    config.read_file(filepath, encoding)
    return config


def write_ini(config: IniConfig, filepath: str, encoding: str = 'utf-8') -> None:
    """
    写入INI文件
    
    Args:
        config: IniConfig对象
        filepath: 文件路径
        encoding: 文件编码
    
    Example:
        >>> config = IniConfig()
        >>> config.set('app', 'name', 'MyApp')
        >>> write_ini(config, 'config.ini')
    """
    config.write_file(filepath, encoding)


def parse_ini(content: str) -> IniConfig:
    """
    解析INI字符串
    
    Args:
        content: INI格式字符串
    
    Returns:
        IniConfig对象
    
    Example:
        >>> config = parse_ini('[app]\\nname = test')
        >>> print(config.get('app', 'name'))
        test
    """
    config = IniConfig()
    config.read_string(content)
    return config


def create_ini(data: Dict[str, Dict[str, Any]]) -> IniConfig:
    """
    从字典创建配置
    
    Args:
        data: 嵌套字典 {section: {key: value}}
    
    Returns:
        IniConfig对象
    
    Example:
        >>> config = create_ini({'app': {'name': 'test'}})
        >>> print(config.to_dict())
    """
    config = IniConfig()
    config.from_dict(data)
    return config
